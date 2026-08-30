# Wastewater Infrastructure Analytics

A reproducible analytics project for evaluating wastewater infrastructure condition, risk, performance, and capital-improvement priorities.

## Project goals

- Consolidate wastewater asset and inspection data into analysis-ready datasets.
- Quantify asset risk using likelihood-of-failure and consequence-of-failure measures.
- Identify high-priority infrastructure for maintenance, rehabilitation, or replacement.
- Support transparent capital planning with repeatable metrics and documented assumptions.
- Produce maps, tables, and decision-ready summaries as the project develops.

## Repository structure

```text
.
├── data/
│   ├── raw/          # Source data; keep original files unchanged
│   └── processed/    # Cleaned and derived datasets
├── notebooks/        # Exploratory analyses and prototypes
├── src/
│   └── wastewater_infrastructure_analytics/
│       ├── __init__.py
│       └── risk.py   # Core risk-scoring helpers
├── tests/            # Automated tests
├── .github/workflows/ci.yml
└── pyproject.toml
```

## Getting started

Requires Python 3.11+.

```bash
git clone https://github.com/Boatengs/wastewater-infrastructure-analytics.git
cd wastewater-infrastructure-analytics
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

For geospatial work:

```bash
pip install -e ".[dev,geo]"
```

## Initial analytical model

The starter package includes a transparent asset-risk calculation based on:

- **Likelihood of failure (LoF):** 1–5
- **Consequence of failure (CoF):** 1–5
- **Criticality multiplier:** positive value, default 1.0

The risk priority number is:

```text
Risk = LoF × CoF × Criticality
```

This is intentionally simple. It provides a testable baseline that can later be calibrated using CCTV condition grades, pipe age/material, work orders, capacity constraints, environmental sensitivity, service population, failure history, and cost data.

## Suggested next data fields

A useful asset-level table can begin with:

| Field | Example |
|---|---|
| `asset_id` | `MH-001245` |
| `asset_type` | `gravity_main` |
| `install_year` | `1987` |
| `material` | `PVC` |
| `diameter_in` | `12` |
| `condition_score` | `4` |
| `likelihood_of_failure` | `3` |
| `consequence_of_failure` | `5` |
| `criticality_multiplier` | `1.2` |
| `latitude` / `longitude` | coordinates |
| `replacement_cost` | estimated cost |

## Data handling

Raw and processed data directories are included as placeholders. Large, sensitive, or restricted utility datasets should not be committed directly to Git. Use approved storage and add local-only file patterns to `.gitignore` as needed.

## Development roadmap

1. Define the source datasets and data dictionary.
2. Build ingestion and validation routines.
3. Create condition and failure-risk features.
4. Add geospatial network/context analysis.
5. Build prioritization and capital-planning outputs.
6. Add dashboards or reports once the core metrics are stable.

## License

No license has been selected yet.
