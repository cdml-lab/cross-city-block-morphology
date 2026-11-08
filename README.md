# cross-city-block-morphology

Study repository of the article *What aerial imagery adds to block morphometrics:
self-supervised, morphometric and united classifications of urban block morphology
across cities*. It holds the configurations of the study's two city sets, a check that
refits every model of the article with the pinned packages and compares it block by
block with the published labels, the results tables, and the interactive dashboard.

Everything of the article is in this repository. The code of the three classifications is
included as Git submodules in `packages/`, pinned at v1.0.0; each package has its own
documentation, tests and verification.

| classification | package (v1.0.0), in `packages/` | what it does |
|---|---|---|
| A · morphometric | [`urban-block-morphology-morphometric`](https://github.com/cdml-lab/urban-block-morphology-morphometric) | blocks, sampling units and 46 morphometric descriptors from building footprints, heights and streets |
| B · image (DINOv3) | [`urban-block-morphology-ssl`](https://github.com/cdml-lab/urban-block-morphology-ssl) | block crops of aerial imagery, a frozen DINOv3 ViT-L/16 satellite backbone and 23 component-structure measures |
| C · united | [`urban-block-morphology-united`](https://github.com/cdml-lab/urban-block-morphology-united) | A and B, each scaled to half of the total variance |

The three build on the core package `urban-block-morphology` v1.0.0 (blocks, descriptors,
K rule), which `requirements.txt` installs.

Every classification uses the same model: whitened PCA with d components, K-means, and
one rule for the number of types K (every type holds at least 12 blocks, K is at or above
the inertia elbow, the best combined quality score wins; a K that meets only one condition
is reported as a fallback).

## Dashboard

All blocks of both city sets, the city models and the pooled models of the three
classifications, building heights, coverage and intensity, in 2D and 3D:
**[view in the browser](https://cdml-lab.github.io/cross-city-block-morphology/)** ·
[download v1.0.0](https://github.com/cdml-lab/cross-city-block-morphology/releases/download/v1.0.0/block-morphology-studio.html) ·
`docs/index.html`.

It is one self-contained file (41 MB). The cities are stored compressed inside the page
and unpacked when they are first shown, so the page also opens directly from disk. The
3D maps need WebGL 2 and an internet connection for deck.gl and the background maps
(`docs/dashboard.md`).

## City sets

| set | cities (pooling order) | blocks | d (A / B / C) | pooled K (A / B / C) |
|---|---|---|---|---|
| three-city | Tel Aviv-Yafo, Manhattan, Amsterdam | 7,556 | 5 / 5 / 8 | 8 / 10 / 10 |
| thirteen-city | the three, Montreal, Barcelona, Rio de Janeiro, São Paulo, Nairobi, Cairo, Lagos, Mumbai, Tokyo, Sydney | 42,470 sampling units | 5 / 2 / 5 | 12 / 11 / 14 |

Each set has one pooled model per classification and one model per city: 12 models in the
three-city set and 42 in the thirteen-city set, 54 in all. The settings of every model are
in `configs/three_cities.yaml` and `configs/thirteen_cities.yaml`; how d was decided is in
`docs/method.md`.

## Install

```bash
git clone --recursive https://github.com/cdml-lab/cross-city-block-morphology.git
cd cross-city-block-morphology
python -m venv .venv            # then activate it
pip install -r requirements.txt # the core and the three packages at v1.0.0
# or: conda env create -f environment.yml
```

Without `--recursive`, `packages/` stays empty (`git submodule update --init` fills it);
`requirements.txt` installs the packages from their repositories either way.

Exact versions of the verification run: `requirements-lock.txt`.

## Reproduce the models

```bash
python scripts/check_reproduction.py configs/three_cities.yaml    --inputs ../study-inputs/three_cities
python scripts/check_reproduction.py configs/thirteen_cities.yaml --inputs ../study-inputs/thirteen_cities
```

The script refits each model with the packages and compares it with
`results/<set>/assignments.csv`. A model passes when K and the rule status equal the
published ones, the partition is identical (ARI = 1, identical type numbers) and, where the
study's K sweep is given, every K-sweep value matches. It prints `REPRODUCTION_OK` or
`REPRODUCTION_DIFFERS`.

The inputs are the study's descriptor tables (Track A) and image features (Track B). The
image features are derived from licensed aerial imagery and are not part of this
repository (`docs/reproduction.md`). All 54 models were reproduced exactly on 8 November
2026 (`verification/`).

## Results

| file | content |
|---|---|
| `results/<set>/assignments.csv` | every block: city-model and pooled-model type of A, B and C |
| `results/<set>/types.csv` | every type of every model: code, name, colour, blocks, median profile |
| `results/<set>/models.csv` | every model: d, K, rule status, silhouette, gap above noise, stability |

`docs/results.md` documents every column. Block keys are `<city>-<block_id>`, as in the
packages' outputs.

## Not included

- aerial imagery and image crops (provider terms);
- DINOv3 weights (distributed by Meta under the DINOv3 licence; downloaded by the user);
- the image embeddings and structure measures (derived from licensed imagery);
- construction-year, land-use and price layers, and the post hoc associations with them
  (from the municipal and national sources cited in the article).

Materials marked as not included are shared for research use on request: open an issue
in this repository or contact the corresponding author of the article; requests are
subject to approval and to the terms of the source data.

## Licence and citation

Code: MIT (`LICENSE`). Results tables and the dashboard's map data: derived from
OpenStreetMap (© OpenStreetMap contributors, ODbL 1.0) and Overture Maps data, with
building heights from 3D-GloBFP and Open Buildings 2.5D (CC BY 4.0) and municipal open
data (`docs/data.md`). Please cite with `CITATION.cff`.
