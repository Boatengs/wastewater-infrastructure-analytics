from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml


CATEGORY_ORDER = {"low": 0, "moderate": 1, "high": 2, "very_high": 3}


def build(project: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    cfg = yaml.safe_load((project / "config" / "capital_allocation.yaml").read_text())
    source = project / "results" / "asset_engineering_priority.csv"
    df = pd.read_csv(source, dtype={"asset_id": "string"})

    selected_columns = [
        "budget",
        "selection_rank",
        "asset_id",
        "asset_type",
        "risk_priority_number",
        "risk_category",
        "replacement_cost",
        "risk_per_dollar",
    ]
    summary_columns = ["budget", "selected_count", "allocated_cost", "remaining_budget", "total_risk_score"]

    if "replacement_cost" not in df.columns:
        selected = pd.DataFrame(columns=selected_columns)
        summary = pd.DataFrame(columns=summary_columns)
    else:
        df["replacement_cost"] = pd.to_numeric(df["replacement_cost"], errors="coerce")
        df["risk_priority_number"] = pd.to_numeric(df["risk_priority_number"], errors="coerce")
        minimum = CATEGORY_ORDER[str(cfg.get("minimum_risk_category", "moderate"))]
        eligible = df[
            df["replacement_cost"].gt(0)
            & df["risk_category"].map(CATEGORY_ORDER).fillna(-1).ge(minimum)
        ].copy()
        eligible["risk_per_dollar"] = eligible["risk_priority_number"] / eligible["replacement_cost"]
        eligible = eligible.sort_values(
            ["risk_per_dollar", "risk_priority_number", "asset_id"],
            ascending=[False, False, True],
        )

        selected_rows: list[dict[str, object]] = []
        summary_rows: list[dict[str, object]] = []
        for budget_value in cfg["budgets"]:
            budget = float(budget_value)
            spent = 0.0
            risk = 0.0
            rank = 0
            for _, asset in eligible.iterrows():
                cost = float(asset["replacement_cost"])
                if spent + cost > budget:
                    continue
                rank += 1
                spent += cost
                risk += float(asset["risk_priority_number"])
                selected_rows.append(
                    {
                        "budget": budget,
                        "selection_rank": rank,
                        "asset_id": asset["asset_id"],
                        "asset_type": asset["asset_type"],
                        "risk_priority_number": asset["risk_priority_number"],
                        "risk_category": asset["risk_category"],
                        "replacement_cost": cost,
                        "risk_per_dollar": asset["risk_per_dollar"],
                    }
                )
            summary_rows.append(
                {
                    "budget": budget,
                    "selected_count": rank,
                    "allocated_cost": round(spent, 2),
                    "remaining_budget": round(budget - spent, 2),
                    "total_risk_score": round(risk, 2),
                }
            )

        selected = pd.DataFrame(selected_rows, columns=selected_columns)
        summary = pd.DataFrame(summary_rows, columns=summary_columns)

    results = project / "results"
    results.mkdir(parents=True, exist_ok=True)
    selected.to_csv(results / "capital_allocation_selected_assets.csv", index=False)
    summary.to_csv(results / "capital_allocation_summary.csv", index=False)
    print(f"Evaluated {len(summary):,} capital budget scenarios.")
    return selected, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build wastewater capital-allocation scenarios.")
    parser.add_argument("--project", type=Path, default=Path("."))
    args = parser.parse_args()
    build(args.project.resolve())


if __name__ == "__main__":
    main()
