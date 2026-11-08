# Results tables

One folder per city set: `results/three_cities/` (7,556 blocks) and
`results/thirteen_cities/` (42,470 sampling units). Codes: A morphometric, B image
(DINOv3), C united. Type numbers are those of the article and the dashboard.

## assignments.csv
One row per block, in city order and within a city by `block_id`.

| column | content |
|---|---|
| `block_key` | `<city>-<block_id>`, as in the outputs of the packages |
| `area` | city code (TLV, MAN, AMS, MTL, BCN, RIO, SAO, NBO, CAI, LOS, BOM, TYO, SYD) |
| `block_id` | block number within the city |
| `A_city`, `B_city`, `C_city` | type in the city model of the classification |
| `A_pooled`, `B_pooled`, `C_pooled` | type in the pooled model of the set |

Tel Aviv-Yafo, Manhattan and Amsterdam belong to both sets. Their blocks differ between
the sets where the thirteen-city set trims open blocks or splits mega-blocks, so each
set's file holds its own rows for them.

## types.csv
One row per type of every model.

| column | content |
|---|---|
| `track`, `model`, `type` | classification, model (`pooled` or a city code) and type number |
| `code` | type code as in the article (`<track><type>`, e.g. C3) |
| `name` | name from the controlled vocabulary of the article (median block) |
| `colour` | colour in the article and the dashboard |
| `blocks` | number of blocks |
| `block_area_ha`, `gsi`, `fsi` | median block area, building coverage and floor-space index |
| `height_m` | median of the blocks' footprint-weighted mean building height |
| `mean_footprint_m2`, `buildings` | median mean footprint and median number of buildings |

## models.csv
One row per model.

| column | content |
|---|---|
| `track`, `model` | classification and model |
| `d` | components of the whitened PCA (`docs/method.md`) |
| `K`, `status` | number of types and the status of the K rule (`rule` or `fallback`) |
| `silhouette`, `gap_above_null` | silhouette at K and its gap above a matched Gaussian null |
| `elbow`, `smallest_type` | inertia elbow and blocks in the smallest type |
| `stability_median_ari`, `stability_q25`, `stability_q75` | partition stability over 100 refits on 80 % subsamples (quartiles for the city models) |
| `k_repeat_share` | share of the subsamples in which the K rule repeats K (where computed) |
