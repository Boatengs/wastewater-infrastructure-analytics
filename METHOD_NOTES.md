# Method Notes

## Decision-support language
This project is an engineering and capital-planning screening tool. Risk scores are prioritization signals, not predictions of an exact failure date and not substitutes for field inspection, hydraulic analysis, or design engineering.

## Baseline risk framework
The initial model uses:

```text
Risk Priority Number = Likelihood of Failure × Consequence of Failure × Criticality Multiplier
```

Baseline LoF and CoF scores use a 1–5 ordinal scale. The criticality multiplier is positive and defaults to 1.0. Utilities should calibrate all scoring rules to local asset-management standards and risk tolerance.

## Likelihood of failure
Candidate evidence includes condition grade, age, material, failure history, infiltration/inflow indicators, structural defects, pump/alarm history, corrosion environment, and maintenance burden. Missing evidence remains visible rather than automatically receiving a favorable score.

## Consequence of failure
Candidate evidence includes service population, roadway/rail crossing, environmental sensitivity, overflow potential, redundancy, critical customers, treatment-process dependency, repair access, and public-safety impact.

## Cost layer
Lifecycle and capital-allocation outputs should distinguish:
- source facts from utilities or bid documents
- planning-level unit-cost assumptions
- modeled low/base/high scenarios
- actual project estimates or bids

## Capital prioritization
A high risk score does not automatically mean immediate replacement. Project sequencing should also consider intervention feasibility, coordination opportunities, readiness, redundancy, regulatory commitments, and lifecycle economics.

## Reproducibility
Configuration values belong in `config/`, analytical transformations in `src/` and `sql/`, reviewer-facing extracts in `results/`, and interpretive findings in `reports/`.
