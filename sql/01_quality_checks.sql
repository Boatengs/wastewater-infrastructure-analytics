DROP VIEW IF EXISTS asset_quality_summary;

CREATE VIEW asset_quality_summary AS
SELECT
    COUNT(*) AS asset_count,
    COUNT(DISTINCT asset_id) AS distinct_asset_ids,
    SUM(CASE WHEN asset_id IS NULL OR TRIM(asset_id) = '' THEN 1 ELSE 0 END) AS blank_asset_ids,
    SUM(CASE WHEN asset_type IS NULL OR TRIM(asset_type) = '' THEN 1 ELSE 0 END) AS blank_asset_types,
    SUM(CASE WHEN likelihood_of_failure IS NULL THEN 1 ELSE 0 END) AS missing_lof,
    SUM(CASE WHEN consequence_of_failure IS NULL THEN 1 ELSE 0 END) AS missing_cof,
    SUM(CASE WHEN likelihood_of_failure IS NOT NULL AND (likelihood_of_failure < 1 OR likelihood_of_failure > 5) THEN 1 ELSE 0 END) AS invalid_lof,
    SUM(CASE WHEN consequence_of_failure IS NOT NULL AND (consequence_of_failure < 1 OR consequence_of_failure > 5) THEN 1 ELSE 0 END) AS invalid_cof,
    SUM(CASE WHEN criticality_multiplier IS NOT NULL AND criticality_multiplier <= 0 THEN 1 ELSE 0 END) AS invalid_criticality
FROM assets;

SELECT * FROM asset_quality_summary;
