# Lifecycle Cost Analysis

## Purpose
Translate asset-level planning costs into explicit low/base/high lifecycle scenarios so risk rankings can be considered alongside long-term financial implications.

## Starter method
The model in `src/lifecycle_cost_model.py` reads `replacement_cost` from the ranked asset table and applies scenario factors from `config/lifecycle_cost_model.yaml`.

For each asset and scenario it calculates:
- scenario capital cost
- annual O&M allowance
- present value of O&M over the analysis horizon
- total lifecycle present value

## Interpretation
These scenarios are comparative planning tools. They are useful for sensitivity analysis and portfolio screening but should not be presented as final project estimates unless the underlying cost basis has been independently developed and documented.

## Next refinement
Segment cost assumptions by asset class and intervention type, incorporate rehabilitation alternatives and remaining useful life, and calibrate factors using local bid history.
