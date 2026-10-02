"""Alpha Scout public demo: the full app, wrapped with demo guards.

What the wrapper changes, all before the real app.py runs:
- each visitor gets a private SQLite file, copied from demo/examples.db, so
  saved searches, target lists and the blacklist never leak across visitors
- every Tavily and Gemini call is metered against a shared daily cap, and
  live searches are capped per session
- email sending is off

Run locally:  venv/bin/streamlit run demo/app.py
"""
import os
import runpy
import shutil
import sqlite3
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)  # app.py opens assets with relative paths

import streamlit as st  # noqa: E402

VIDEO = "https://www.youtube.com/watch?v=PyaJmPB9MVI"
CASE_STUDY = "https://alexandrecela10.github.io/projects/alpha-scout/"
SEED_DB = ROOT / "demo" / "examples.db"

st.set_page_config(page_title="Alpha Scout demo", page_icon="📡", layout="wide")
st.set_page_config = lambda *a, **k: None  # app.py calls it again; the first call wins

try:
    for k in ("GEMINI_API_KEY", "TAVILY_API_KEY", "DEMO_DAILY_TAVILY_CALLS", "DEMO_DAILY_GEMINI_CALLS"):
        if k in st.secrets:
            os.environ[k] = str(st.secrets[k])
except FileNotFoundError:
    pass  # local run without a secrets file

from demo import meter as m  # noqa: E402


@st.cache_resource
def patch_once():
    """Process-wide patches. Cached so they run once, not on every rerun."""
    import persistence
    import reporting
    import search

    def session_connection():
        # st.session_state is per visitor, even though sessions share this process.
        conn = sqlite3.connect(st.session_state["demo_db_path"])
        conn.row_factory = sqlite3.Row
        return conn

    persistence.get_connection = session_connection
    reporting.send_email_report = lambda *a, **k: (False, "Email is turned off in this demo.")

    original_search = search.search_similar_companies

    def gated_search(*args, **kwargs):
        if st.session_state.get("demo_searches", 0) >= m.SESSION_SEARCHES:
            raise RuntimeError("Demo limit: 2 live searches per visit. Load a saved example from the sidebar.")
        if not daily.can_afford_search():
            raise RuntimeError("Today's shared demo budget is used up. Load a saved example from the sidebar.")
        st.session_state["demo_searches"] = st.session_state.get("demo_searches", 0) + 1
        kwargs["max_results"] = min(kwargs.get("max_results", m.MAX_RESULTS), m.MAX_RESULTS)
        return original_search(*args, **kwargs)

    search.search_similar_companies = gated_search

    # Import every module that calls Gemini, then meter all of them.
    import ingest, reviewer, scorer, source_enrichment, tracing, vc_chat  # noqa: F401,E401
    m.install(daily)
    return True


daily = m.DailyMeter()
patch_once()

if "demo_db_path" not in st.session_state:
    path = Path(tempfile.gettempdir()) / f"alpha_scout_{uuid.uuid4().hex}.db"
    if SEED_DB.exists():
        shutil.copy(SEED_DB, path)
    st.session_state["demo_db_path"] = str(path)

with st.sidebar:
    st.info(
        f"**Demo.** Fictional portfolio seeds. Saved examples load free from *Load Previous Search*. "
        f"Live searches: {max(0, m.SESSION_SEARCHES - st.session_state.get('demo_searches', 0))} left this visit, "
        f"up to {m.MAX_RESULTS} companies each. Results name real companies found in public sources.  \n"
        f"[Video walkthrough]({VIDEO}) · [Case study]({CASE_STUDY})"
    )

runpy.run_path(str(ROOT / "app.py"), run_name="__main__")
