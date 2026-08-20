"""Unit tests for the expense analyzer's parsing and aggregation logic."""

import tempfile
import unittest
from pathlib import Path

from analyze import build_summary, load_transactions, save_charts, totals_by_category, totals_by_month

SAMPLE_CSV = """date,category,amount
2026-01-01,Groceries,20.00
2026-01-15,Transport,10.00
2026-02-01,Groceries,25.00
2026-02-10,Rent,400.00
"""


class ExpenseAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.tmp_dir.name) / "expenses.csv"
        self.csv_path.write_text(SAMPLE_CSV, encoding="utf-8")
        self.transactions = load_transactions(self.csv_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_load_transactions_count(self):
        self.assertEqual(len(self.transactions), 4)
        self.assertEqual(self.transactions[0]["category"], "Groceries")
        self.assertEqual(self.transactions[0]["amount"], 20.00)

    def test_totals_by_category(self):
        totals = totals_by_category(self.transactions)
        self.assertEqual(totals["Groceries"], 45.00)
        self.assertEqual(totals["Rent"], 400.00)
        self.assertEqual(totals["Transport"], 10.00)

    def test_totals_by_month(self):
        totals = totals_by_month(self.transactions)
        self.assertEqual(totals["2026-01"], 30.00)
        self.assertEqual(totals["2026-02"], 425.00)

    def test_build_summary(self):
        summary = build_summary(self.transactions)
        self.assertEqual(summary["count"], 4)
        self.assertEqual(summary["total"], 455.00)
        self.assertEqual(summary["average"], 113.75)

    def test_empty_transactions_summary(self):
        summary = build_summary([])
        self.assertEqual(summary["count"], 0)
        self.assertEqual(summary["total"], 0.0)
        self.assertEqual(summary["by_category"], {})

    def test_save_charts_creates_png_files(self):
        summary = build_summary(self.transactions)
        with tempfile.TemporaryDirectory() as out_dir:
            save_charts(summary, out_dir)
            self.assertTrue((Path(out_dir) / "by_category.png").exists())
            self.assertTrue((Path(out_dir) / "by_month.png").exists())


if __name__ == "__main__":
    unittest.main()
