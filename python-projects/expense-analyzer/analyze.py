"""Expense Analyzer, a command line tool that summarizes spending from a CSV file.

Reads a CSV of transactions (date, category, amount), prints a text summary,
and generates two charts: total spending by category, and monthly trend.
"""

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_transactions(csv_path):
    transactions = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(
                {
                    "date": datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                    "category": row["category"].strip(),
                    "amount": float(row["amount"]),
                }
            )
    return transactions


def totals_by_category(transactions):
    totals = defaultdict(float)
    for t in transactions:
        totals[t["category"]] += t["amount"]
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def totals_by_month(transactions):
    totals = defaultdict(float)
    for t in transactions:
        key = t["date"].strftime("%Y-%m")
        totals[key] += t["amount"]
    return dict(sorted(totals.items()))


def build_summary(transactions):
    if not transactions:
        return {
            "total": 0.0,
            "count": 0,
            "average": 0.0,
            "by_category": {},
            "by_month": {},
        }
    by_category = totals_by_category(transactions)
    by_month = totals_by_month(transactions)
    total = sum(t["amount"] for t in transactions)
    return {
        "total": round(total, 2),
        "count": len(transactions),
        "average": round(total / len(transactions), 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "by_month": {k: round(v, 2) for k, v in by_month.items()},
    }


def print_summary(summary):
    print(f"Transactions: {summary['count']}")
    print(f"Total spent: {summary['total']:.2f}")
    print(f"Average per transaction: {summary['average']:.2f}")

    if summary["by_category"]:
        print("\nBy category:")
        for category, amount in summary["by_category"].items():
            print(f"  {category}: {amount:.2f}")

    if summary["by_month"]:
        print("\nBy month:")
        for month, amount in summary["by_month"].items():
            print(f"  {month}: {amount:.2f}")


def save_charts(summary, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if summary["by_category"]:
        categories = list(summary["by_category"].keys())
        values = list(summary["by_category"].values())
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.bar(categories, values, color="#3a5cff")
        ax.set_title("Spending by category")
        ax.set_ylabel("Amount")
        fig.autofmt_xdate(rotation=30)
        fig.tight_layout()
        fig.savefig(output_dir / "by_category.png", dpi=150)
        plt.close(fig)

    if summary["by_month"]:
        months = list(summary["by_month"].keys())
        values = list(summary["by_month"].values())
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(months, values, marker="o", color="#1ea672")
        ax.set_title("Monthly spending trend")
        ax.set_ylabel("Amount")
        fig.autofmt_xdate(rotation=30)
        fig.tight_layout()
        fig.savefig(output_dir / "by_month.png", dpi=150)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Summarize a CSV of expenses and generate charts."
    )
    parser.add_argument("csv_file", nargs="?", default="sample_expenses.csv")
    parser.add_argument("--output-dir", default="charts")
    parser.add_argument("--no-charts", action="store_true", help="Print the summary only")
    args = parser.parse_args()

    transactions = load_transactions(args.csv_file)
    summary = build_summary(transactions)
    print_summary(summary)

    if not args.no_charts:
        save_charts(summary, args.output_dir)
        print(f"\nCharts saved to {args.output_dir}/")


if __name__ == "__main__":
    main()
