# Source Code

The wastewater project follows the same pipeline-oriented layout used in the PFAS decision-intelligence repository.

## Main scripts

- `ingest_assets.py` — validate and normalize a source asset CSV, write a clean CSV, and load SQLite.
- `run_sql.py` — execute auditable SQL QA and view-building scripts.
- `build_engineering_priority.py` — calculate LoF × CoF × criticality and rank assets.
- `lifecycle_cost_model.py` — build low/base/high planning-level lifecycle-cost scenarios when cost inputs are available.
- `capital_allocation.py` — rank/select candidate projects within configured capital budgets.
- `generate_figures.py` — create reviewer-facing plots from compact result extracts.
- `wastewater_infrastructure_analytics/risk.py` — tested core risk-scoring helpers.

## Expected source file

The default pipeline expects `data/raw/assets.csv`. At minimum it must contain:

```text
asset_id,asset_type,likelihood_of_failure,consequence_of_failure
```

Optional fields include `criticality_multiplier`, `replacement_cost`, `install_year`, `material`, `diameter_in`, `length_ft`, latitude/longitude, and source-system metadata.

See the root `DATA_DICTIONARY.md` for the full analytical contract.
