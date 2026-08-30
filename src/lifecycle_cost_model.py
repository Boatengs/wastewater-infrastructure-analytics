from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml


def present_value_annuity_factor(rate: float, years: int) -> float:
    return sum(1.0 / ((1.0 + rate) ** year) for year in range(1, years + 1))


def build(project: Path) -> pd.DataFrame:
    cfg = yaml.safe_load((project / "config" / "lifecycle_cost_model.yaml").read_text())
    source = project / "results" / "asset_engineering_priority.csv"
    df = pd.read_csv(source, dtype={"asset_id": "string"})

    output_columns = [
        "asset_id",
        "asset_type",
        "scenario",
        "base_replacement_cost",
        "scenario_capex",
        "annual_om",
        "pv_om",
        "total_lifecycle_pv",
    ]

    if "replacement_cost" not in df.columns:
        out = pd.DataFrame(columns=output_columns)
    else:
        df["replacement_cost"] = pd.to_numeric(df["replacement_cost"], errors="coerce")
        df = df[df["replacement_cost"].gt(0)].copy()

        rate = float(cfg["discount_rate"])
        years = int(cfg["analysis_horizon_years"])
        annuity = present_value_annuity_factor(rate, years)

        rows: list[dict[str, object]] = []
        for _, asset in df.iterrows():
            base = float(asset["replacement_cost"])
            for scenario in ["low", "base", "high"]:
                capex = base * float(cfg["capital_cost_factor"][scenario])
                annual_om = base * float(cfg["annual_om_fraction_of_base_capex"][scenario])
                pv_om = annual_om * annuity
                rows.append(
                    {
                        "asset_id": asset["asset_id"],
                        "asset_type": asset["asset_type"],
                        "scenario": scenario,
                        "base_replacement_cost": base,
                        "scenario_capex": round(capex, 2),
                        "annual_om": round(annual_om, 2),
                        "pv_om": round(pv_om, 2),
                        "total_lifecycle_pv": round(capex + pv_om, 2),
                    }
                )
        out = pd.DataFrame(rows, columns=output_columns)

    results = project / "results"
    results.mkdir(parents=True, exist_ok=True)
    out.to_csv(results / "lifecycle_cost_scenarios.csv", index=False)
    print(f"Wrote {len(out):,} lifecycle-cost scenario rows.")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build wastewater lifecycle-cost scenarios.")
    parser.add_argument("--project", type=Path, default=Path("."))
    args = parser.parse_args()
    build(args.project.resolve())


if __name__ == "__main__":
    main()
