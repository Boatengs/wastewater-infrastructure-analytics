# Data

This repository is designed to keep public code and methods separate from utility-sensitive source data.

## Local layout

```text
data/
├── raw/         # original source exports; do not modify in place
├── processed/   # normalized analysis-ready extracts
└── derived/     # SQLite database and intermediate analytical products
```

## Default pipeline input

The starter pipeline looks for `data/raw/assets.csv` unless another path is supplied with `--input`.

Minimum fields:

```text
asset_id,asset_type,likelihood_of_failure,consequence_of_failure
```

See `DATA_DICTIONARY.md` for the preferred asset schema.

## Data governance

Do not commit confidential GIS, security-sensitive facility details, customer information, restricted inspection media, or other utility-controlled datasets without explicit approval. The tiny file in `tests/assets_fixture.csv` is synthetic and exists only for reproducibility testing.
