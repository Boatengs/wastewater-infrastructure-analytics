from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"asset_id", "asset_type"}
NUMERIC_COLUMNS = [
    "install_year",
    "diameter_in",
    "length_ft",
    "condition_score",
    "likelihood_of_failure",
    "consequence_of_failure",
    "criticality_multiplier",
    "failure_count_5yr",
    "capacity_score",
    "service_consequence_score",
    "environmental_consequence_score",
    "replacement_cost",
    "latitude",
    "longitude",
]


def load_assets(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"asset_id": "string", "asset_type": "string"})
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["asset_id"] = df["asset_id"].astype("string").str.strip()
    df["asset_type"] = df["asset_type"].astype("string").str.strip().str.lower()

    if df["asset_id"].isna().any() or df["asset_id"].eq("").any():
        raise ValueError("asset_id cannot be blank")
    if df["asset_id"].duplicated().any():
        duplicates = df.loc[df["asset_id"].duplicated(), "asset_id"].tolist()
        raise ValueError(f"Duplicate asset_id values found: {duplicates[:10]}")

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "criticality_multiplier" not in df.columns:
        df["criticality_multiplier"] = 1.0
    else:
        df["criticality_multiplier"] = df["criticality_multiplier"].fillna(1.0)

    if (df["criticality_multiplier"] <= 0).any():
        raise ValueError("criticality_multiplier must be greater than 0")

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a wastewater asset CSV.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--processed", type=Path, required=True)
    args = parser.parse_args()

    df = load_assets(args.input)
    args.db.parent.mkdir(parents=True, exist_ok=True)
    args.processed.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(args.processed, index=False)
    with sqlite3.connect(args.db) as conn:
        df.to_sql("assets", conn, if_exists="replace", index=False)
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_assets_asset_id ON assets(asset_id)")
        conn.commit()

    print(f"Loaded {len(df):,} wastewater assets into {args.db}")


if __name__ == "__main__":
    main()
