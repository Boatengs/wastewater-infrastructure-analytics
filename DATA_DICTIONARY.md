# Wastewater Infrastructure Analytics Data Dictionary

## Asset-level analytical grain
The core analytical table is designed around one record per wastewater asset or asset segment. Source systems may contain inspections, work orders, failures, costs, and hydraulic observations at different grains; those records should be preserved separately and summarized to the asset grain only through documented transformations.

| Field | Meaning | Project handling |
|---|---|---|
| `asset_id` | Stable utility asset or segment identifier | text; required |
| `asset_type` | Gravity main, force main, manhole, pump station, treatment asset, etc. | standardized text |
| `install_year` | Installation or in-service year | integer nullable |
| `material` | Primary construction material | standardized text |
| `diameter_in` | Nominal diameter, inches | numeric nullable |
| `length_ft` | Asset length, feet | numeric nullable |
| `condition_score` | Condition score on a documented local scale | numeric nullable |
| `likelihood_of_failure` | LoF score, baseline 1–5 | numeric nullable |
| `consequence_of_failure` | CoF score, baseline 1–5 | numeric nullable |
| `criticality_multiplier` | Local criticality adjustment | positive numeric; default 1.0 |
| `failure_count_5yr` | Documented failures in trailing five years | integer nullable |
| `capacity_score` | Capacity or hydraulic constraint indicator | numeric nullable |
| `service_consequence_score` | Service/public impact component | numeric nullable |
| `environmental_consequence_score` | Receiving-water/environmental consequence component | numeric nullable |
| `replacement_cost` | Planning-level replacement/rehabilitation cost | numeric nullable |
| `latitude` / `longitude` | Asset location when publishable | numeric nullable |
| `source_system` | GIS, CMMS, CCTV, hydraulic model, spreadsheet, etc. | text |
| `source_updated_at` | Source-system data date | date/datetime nullable |

## Derived fields
- `asset_age_years`
- `risk_priority_number = likelihood_of_failure × consequence_of_failure × criticality_multiplier`
- `risk_category`
- `cost_per_risk_point`
- `priority_rank`
- `recommended_action_class`
- `data_completeness_score`

## Event-level supporting tables
Where available, the project should retain separate source-grain tables for:
- CCTV/condition inspections
- work orders and maintenance history
- sanitary sewer overflows or failures
- pump runtime/alarm history
- hydraulic model results
- rehabilitation/replacement projects
- planning-level unit costs and bids

## Missing-data rule
Missing values remain missing unless an imputation rule is explicitly documented. Absence of a failure, inspection, or condition record must not automatically be interpreted as zero risk or good condition.
