# Reproducing the models of the article

## What is reproduced
All 54 models of the article: the city models and the pooled model of the three
classifications (A morphometric, B image, C united) in the three-city set (12 models) and
the thirteen-city set (42 models). Each model is refitted with the pinned packages and
compared, block by block, with the published labels in `results/<set>/assignments.csv`.

```bash
python scripts/check_reproduction.py configs/three_cities.yaml    --inputs ../study-inputs/three_cities    --report reproduction_three_cities.json
python scripts/check_reproduction.py configs/thirteen_cities.yaml --inputs ../study-inputs/thirteen_cities --report reproduction_thirteen_cities.json
```

`--tracks A` (or `B`, `C`) checks one classification only. The script prints one line per
model and `REPRODUCTION_OK` or `REPRODUCTION_DIFFERS`.

## Inputs
The inputs are the study's precomputed values, one folder per city:

```
study-inputs/<three_cities|thirteen_cities>/
  descriptors/<CITY>.parquet          46 treated descriptors per block (index block_id)
  features/<CITY>/ssl_embeddings.npy   2,048 DINOv3 values per block
                  ssl_block_ids.csv    block ids, in the row order of the embeddings
                  structure_features.parquet   23 component-structure measures per block
  sweeps/<CITY|pooled>_<morpho|ssl|united>.csv   the study's K sweeps (optional)
```

- **Descriptors** are recomputed from open data with `urban-block-morphology-morphometric`
  (`blockmorph-morphometric run`; its `docs/reproduction.md` verifies the descriptors and the
  sampling units of both sets).
- **Image features** are computed from aerial imagery with `urban-block-morphology-ssl`
  (`blockssl run`, imagery path). They are derived from licensed imagery and are not part
  of this repository. They are available on request for research use (open an issue or
  contact the corresponding author of the article; subject to approval and to the
  imagery terms). Features recomputed from other imagery, hardware or library versions
  match within the tolerances of `urban-block-morphology-ssl` (`docs/reproduction.md`)
  but can move single blocks between types.

## Criteria
| quantity | criterion |
|---|---|
| blocks per model | identical |
| K and the status of the K rule (`rule` or `fallback`) | identical |
| partition | ARI = 1 and identical type numbers |
| K sweep (silhouette, gap above noise, Calinski–Harabasz, Davies–Bouldin, inertia, combined score) | relative difference ≤ 1e-6 |
| K sweep (smallest type, size condition, elbow, selected K) | identical |

## Result (8 November 2026)
All 54 models were reproduced: identical K and status, ARI 1.0000 and identical type
numbers in every model, and every K-sweep value within a relative 1e-13. Reports:
`verification/reproduction_three_cities.json` and
`verification/reproduction_thirteen_cities.json`.

| set | classification | d | city models (K) | pooled K | result |
|---|---|---|---|---|---|
| three-city | A | 5 | TLV 9, MAN 8, AMS 11 | 8 | identical |
| three-city | B | 5 | TLV 6 (fallback), MAN 8, AMS 8 | 10 | identical |
| three-city | C | 8 | TLV 9, MAN 9, AMS 10 | 10 | identical |
| thirteen-city | A | 5 | TLV 9, MAN 8, AMS 11, MTL 8, BCN 9, RIO 8, SAO 8, NBO 9, CAI 11, LOS 8, BOM 9, TYO 8, SYD 8 | 12 | identical |
| thirteen-city | B | 2 | TLV 8, MAN 8, AMS 10, MTL 14, BCN 12, RIO 11, SAO 12, NBO 9, CAI 10, LOS 8, BOM 9, TYO 9, SYD 14 | 11 | identical |
| thirteen-city | C | 5 | TLV 9, MAN 8, AMS 9, MTL 9, BCN 9, RIO 9, SAO 8, NBO 9, CAI 12, LOS 8, BOM 8, TYO 8, SYD 9 | 14 | identical |

Environments:
- the study environment: Python 3.13.5, numpy 2.4.4, pandas 2.3.3, scikit-learn 1.7.2,
  geopandas 1.1.3, momepy 1.0.0, Windows 11; the four packages at v1.0.0
  (`requirements-lock.txt`);
- a clean environment installed from GitHub with `pip install -r requirements.txt`
  (Python 3.13.5, numpy 2.5.4, pandas 3.1.1, scikit-learn 1.9.1): the same result for all
  54 models (`verification/reproduction_*_clean_github_install.json`).
The run takes about 2 minutes for the three-city set and 50 minutes for the thirteen-city
set (silhouettes of 42,470 units for K = 5–25).
