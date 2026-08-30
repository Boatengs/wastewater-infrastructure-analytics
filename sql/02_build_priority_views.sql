DROP VIEW IF EXISTS asset_priority_inputs;

CREATE VIEW asset_priority_inputs AS
SELECT
    asset_id,
    asset_type,
    likelihood_of_failure,
    consequence_of_failure,
    COALESCE(criticality_multiplier, 1.0) AS criticality_multiplier,
    likelihood_of_failure * consequence_of_failure * COALESCE(criticality_multiplier, 1.0) AS risk_priority_number,
    CASE
        WHEN likelihood_of_failure * consequence_of_failure * COALESCE(criticality_multiplier, 1.0) >= 20 THEN 'very_high'
        WHEN likelihood_of_failure * consequence_of_failure * COALESCE(criticality_multiplier, 1.0) >= 12 THEN 'high'
        WHEN likelihood_of_failure * consequence_of_failure * COALESCE(criticality_multiplier, 1.0) >= 6 THEN 'moderate'
        ELSE 'low'
    END AS risk_category,
    replacement_cost
FROM assets
WHERE likelihood_of_failure IS NOT NULL
  AND consequence_of_failure IS NOT NULL;

SELECT *
FROM asset_priority_inputs
ORDER BY risk_priority_number DESC, asset_id;
