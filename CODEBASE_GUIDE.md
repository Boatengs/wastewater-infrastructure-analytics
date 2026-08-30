# Codebase Guide

If you are reviewing this project for an engineering, asset-management, analytics, or infrastructure-planning role, start here.

## Core analytical pipeline

```text
Wastewater asset / inspection / work-order data
    |
    v
src/ingest_assets.py
    |  normalized asset table + SQLite model
    v
sql/01_quality_checks.sql
sql/02_build_priority_views.sql
    |
    v
src/build_engineering_priority.py
    |  transparent LoF × CoF × criticality ranking
    +-------------------+
    |                   |
    v                   v
src/lifecycle_cost_model.py     src/capital_allocation.py
planning-level lifecycle cost   constrained capital-program scenarios
    |                   |
    +---------+---------+
              v
       src/generate_figures.py
```

## Run it

```bash
pip install -r requirements.txt
python run_pipeline.py --project .
```

The public repository ships with a tiny synthetic fixture for CI. Real utility data should be placed under `data/raw/` locally and should not be committed unless publication is explicitly approved.

## Where the methods live

- Priority assumptions: `config/priority_score.yaml`
- Lifecycle assumptions: `config/lifecycle_cost_model.yaml`
- Capital-allocation assumptions: `config/capital_allocation.yaml`
- Screening/data-completeness assumptions: `config/screening_scenarios.yaml`
- Data definitions: `DATA_DICTIONARY.md`
- Method boundaries and limitations: `METHOD_NOTES.md`

## Reviewer-friendly outputs

Planned public outputs follow the same pattern as the PFAS project:
- ranked asset priorities in `results/`
- lifecycle-cost scenario extracts in `results/`
- capital-allocation summaries in `results/`
- current findings in `reports/CURRENT_FINDINGS.md`
- figures in `figures/`
- source audit trail in `sources/SOURCE_REGISTER.md`

## Testing

`tests/assets_fixture.csv` is a tiny synthetic wastewater asset dataset. GitHub Actions runs unit tests plus an ingestion/SQL/priority smoke test against the fixture on pushes and pull requests.
