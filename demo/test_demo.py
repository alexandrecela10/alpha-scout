"""Tests for the Alpha Scout demo cost guards. No network, no API keys.

Run:  venv/bin/python -m unittest demo.test_demo
"""
import tempfile
import unittest
from pathlib import Path

from demo import meter as m


class MeterTests(unittest.TestCase):
    def setUp(self):
        self.meter = m.DailyMeter({"tavily": 3, "gemini": 50}, Path(tempfile.mkdtemp()) / "b.json")

    def test_spend_stops_at_cap(self):
        for _ in range(3):
            self.meter.spend("tavily")
        with self.assertRaises(m.BudgetExhausted):
            self.meter.spend("tavily")
        self.assertEqual(self.meter.remaining("tavily"), 0)

    def test_search_needs_worst_case_budget(self):
        self.assertFalse(self.meter.can_afford_search())  # 3 Tavily calls < 31 needed
        big = m.DailyMeter({"tavily": 31, "gemini": 60}, Path(tempfile.mkdtemp()) / "b.json")
        self.assertTrue(big.can_afford_search())

    def test_install_meters_tavily_and_gemini(self):
        import scorer
        import search
        import source_enrichment
        from tavily import TavilyClient
        m.install(self.meter)
        self.assertTrue(getattr(TavilyClient.search, "_metered", False))
        for mod in (search, source_enrichment, scorer):
            self.assertEqual(mod.call_gemini.__name__, "metered_gemini", mod.__name__)


class PortfolioTests(unittest.TestCase):
    def test_portfolio_seeds_are_fictional(self):
        from config import PORTFOLIO_COMPANIES
        for name, attrs in PORTFOLIO_COMPANIES.items():
            self.assertTrue(name.startswith("Portfolio "), name)
            self.assertTrue(attrs["website"].endswith(".example"), name)


if __name__ == "__main__":
    unittest.main()
