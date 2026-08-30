from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from wastewater_infrastructure_analytics.risk import classify_risk, risk_priority_number


REQUIRED_COLUMNS = {"asset_id", "asset_type", "likelihood_of_failure", "consequence_of_failure"}


def build(project: Path) -> pd.DataFrame:
    source = project / "data" / "processed" / "assets_clean.csv"
    if not source.exists():
        raise FileNotFoundError(f"Processed asset file not found: {source}")

    df = pd.read_csv(source, dtype={"asset_id": "string", "asset_type": "string"})
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Priority model requires columns: {sorted(missing)}")

    for column in ["likelihood_of_failure", "consequence_of_failure", "criticality_multiplier"]:
        if column not in df.columns:
            if column == "criticality_multiplier":
                df[column] = 1.0
            else:
                raise ValueError(f"Missing required scoring field: {column}")
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[["likelihood_of_failure", "consequence_of_failure"]].isna().any().any():
        raise ValueError("LoF and CoF must be populated for all assets included in the priority model")

    df["risk_priority_number"] = df.apply(
        lambda r: risk_priority_number(
            r["likelihood_of_failure"],
            r["consequence_of_failure"],
            r["criticality_multiplier"],
        ),
        axis=1,
    )
    df["risk_category"] = df["risk_priority_number"].map(classify_risk)

    if "replacement_cost" in df.columns:
        df["replacement_cost"] = pd.to_numeric(df["replacement_cost"], errors="coerce")
        df["cost_per_risk_point"] = df["replacement_cost"] / df["risk_priority_number"].replace(0, pd.NA)

    sort_cols = ["risk_priority_number", "asset_id"]
    df = df.sort_values(sort_cols, ascending=[False, True]).reset_index(drop=True)
    df.insert(0, "priority_rank", range(1, len(df) + 1))

    results = project / "results"
    results.mkdir(parents=True, exist_ok=True)
    df.to_csv(results / "asset_engineering_priority.csv", index=False)
    df.head(25).to_csv(results / "top_25_engineering_priorities.csv", index=False)

    summary = {
        "asset_count": int(len(df)),
        "very_high_count": int((df["risk_category"] == "very_high").sum()),
        "high_count": int((df["risk_category"] == "high").sum()),
        "moderate_count": int((df["risk_category"] == "moderate").sum()),
        "low_count": int((df["risk_category"] == "low").sum()),
        "max_risk_priority_number": float(df["risk_priority_number"].max()) if len(df) else None,
    }
    (results / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Build wastewater engineering-priority outputs.")
    parser.add_argument("--project", type=Path, default=Path("."))
    args = parser.parse_args()
    df = build(args.project.resolve())
    print(df[["priority_rank", "asset_id", "asset_type", "risk_priority_number", "risk_category"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
