# Current Findings

## Current analytical state
The repository now supports a reproducible wastewater asset-management decision chain from asset ingestion through engineering-risk ranking, lifecycle-cost scenarios, capital-allocation screening, and reviewer-facing figures.

## What can be concluded now
- The baseline risk method is transparent and decomposable: LoF × CoF × criticality.
- Source-data quality is treated as part of the engineering problem rather than hidden through automatic imputation.
- Asset prioritization and capital allocation are deliberately separated: high risk identifies need, while cost/readiness determine feasible program sequencing.
- Cost assumptions are externalized in configuration instead of being embedded in notebooks or unexplained code constants.

## What cannot be concluded yet
No utility-specific production dataset has been committed, so this repository does **not** yet claim:
- a real ranked list of municipal wastewater assets
- calibrated failure probabilities
- verified rehabilitation/replacement costs for a specific utility
- current hydraulic deficiencies for a specific system
- a recommended adopted capital improvement program

## Next evidence needed
1. Asset inventory and source-system metadata.
2. CCTV/condition inspection history.
3. Failure, overflow, work-order, and maintenance records.
4. Hydraulic/capacity indicators where relevant.
5. Consequence/criticality framework approved by the utility.
6. Local bid history and planning-level unit costs.
7. Project readiness, coordination, and delivery constraints.

This report should be updated with dated quantitative findings once validated source data are connected.
