# Capital Allocation Model

## Purpose
Test how a constrained wastewater capital budget could be allocated across eligible asset interventions while keeping the selection logic transparent.

## Starter method
`src/capital_allocation.py` uses the ranked asset table and budget scenarios in `config/capital_allocation.yaml`.

The current screening heuristic:
1. excludes assets without a positive planning cost from capital allocation while retaining them in risk ranking;
2. applies a minimum risk-category threshold;
3. ranks eligible assets by risk priority number per dollar;
4. selects projects greedily while remaining within each configured budget.

## Important limitation
This is intentionally simpler than a production capital-program optimizer. It does not yet model project bundling, geographic coordination, dependencies, regulatory commitments, construction windows, crew constraints, design readiness, equity objectives, or multi-year cash flow.

## Planned refinement
Once real project and cost data are available, replace or supplement the heuristic with a constrained optimization model and compare objectives such as maximum risk reduction, criticality coverage, geographic balance, and readiness-adjusted delivery.
