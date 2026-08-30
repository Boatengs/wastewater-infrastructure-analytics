from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def build(project: Path) -> None:
    figures = project / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    priority_path = project / "results" / "asset_engineering_priority.csv"
    if priority_path.exists():
        priority = pd.read_csv(priority_path, dtype={"asset_id": "string"}).head(15).copy()
        if not priority.empty:
            priority = priority.sort_values("risk_priority_number", ascending=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(priority["asset_id"].astype(str), priority["risk_priority_number"])
            ax.set_title("Top wastewater asset priorities")
            ax.set_xlabel("Risk priority number")
            ax.set_ylabel("Asset ID")
            fig.tight_layout()
            fig.savefig(figures / "executive_dashboard.svg", format="svg")
            plt.close(fig)

    allocation_path = project / "results" / "capital_allocation_summary.csv"
    if allocation_path.exists():
        allocation = pd.read_csv(allocation_path)
        if not allocation.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(allocation["budget"], allocation["selected_count"], marker="o")
            ax.set_title("Capital budget scenario reach")
            ax.set_xlabel("Budget")
            ax.set_ylabel("Assets selected")
            fig.tight_layout()
            fig.savefig(figures / "capital_allocation_portfolio_reach.svg", format="svg")
            plt.close(fig)

    print(f"Figure generation complete: {figures}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate wastewater reviewer-facing figures.")
    parser.add_argument("--project", type=Path, default=Path("."))
    args = parser.parse_args()
    build(args.project.resolve())


if __name__ == "__main__":
    main()
