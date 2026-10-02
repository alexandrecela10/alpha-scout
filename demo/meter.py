"""Cost guards for the public Alpha Scout demo.

Layer 1 (outside code): Gemini and Tavily keys sit on free plans with no
billing, so calls past the free quota fail instead of being charged.
Layer 2 (here): every Tavily and Gemini call made by any module is counted
against a daily cap shared by all visitors. A search only starts if the
remaining budget covers its worst case, so no search is cut off halfway.
"""
from __future__ import annotations

import fcntl
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Dict

MAX_RESULTS = int(os.environ.get("DEMO_MAX_RESULTS", "5"))  # companies per live search; examples use 10
SESSION_SEARCHES = 2                     # live searches per visitor session
# Worst case per search at MAX_RESULTS=5: 1 discovery search + 3 enrichment
# searches per candidate (2x overfetch = 10 candidates), 1 extraction call,
# up to 3 enrichment calls and 1 scoring call per candidate.
COST_PER_SEARCH = {"tavily": 31, "gemini": 60}  # +19 Gemini for the reviewer and judge steps
DAILY_CAPS = {
    # Tavily free plan: 1,000 credits/month. One 5-company search is about 31 calls (~60 credits).
    "tavily": int(os.environ.get("DEMO_DAILY_TAVILY_CALLS", "31")),
    "gemini": int(os.environ.get("DEMO_DAILY_GEMINI_CALLS", "200")),
}


class BudgetExhausted(RuntimeError):
    """Raised when a daily cap is reached."""


class DailyMeter:
    """File-backed per-day counters. The file lock keeps concurrent sessions consistent."""

    def __init__(self, caps: Dict[str, int] = None, path: Path = None):
        self.caps = caps or DAILY_CAPS
        self.path = path or Path(tempfile.gettempdir()) / "alpha_scout_budget.json"

    def _update(self, kind: str, add: int) -> int:
        """Add `add` to today's count for `kind` if it fits. Returns new count, or -1 if refused."""
        self.path.touch(exist_ok=True)
        with open(self.path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                data = json.loads(f.read() or "{}")
            except json.JSONDecodeError:
                data = {}
            today = data.get(date.today().isoformat(), {})
            used = today.get(kind, 0)
            if used + add > self.caps[kind]:
                return -1
            today[kind] = used + add
            f.seek(0)
            f.truncate()
            f.write(json.dumps({date.today().isoformat(): today}))
            return used + add

    def remaining(self, kind: str) -> int:
        return max(0, self.caps[kind] - self._update(kind, 0))

    def can_afford_search(self) -> bool:
        return all(self.remaining(k) >= v for k, v in COST_PER_SEARCH.items())

    def spend(self, kind: str) -> None:
        if self._update(kind, 1) < 0:
            raise BudgetExhausted(f"daily demo {kind} limit reached")


def install(meter: DailyMeter) -> None:
    """Route every Tavily and Gemini call in the app through the meter. Call once at startup."""
    import llm_client
    from tavily import TavilyClient

    if getattr(TavilyClient.search, "_metered", False):
        return

    original_search = TavilyClient.search

    def metered_search(self, *args, **kwargs):
        meter.spend("tavily")
        return original_search(self, *args, **kwargs)

    metered_search._metered = True
    TavilyClient.search = metered_search

    original_gemini = llm_client.call_gemini

    def metered_gemini(*args, **kwargs):
        meter.spend("gemini")
        return original_gemini(*args, **kwargs)

    # Modules did `from llm_client import call_gemini`, so rebind every copy.
    for mod in list(sys.modules.values()):
        if getattr(mod, "call_gemini", None) is original_gemini:
            mod.call_gemini = metered_gemini
