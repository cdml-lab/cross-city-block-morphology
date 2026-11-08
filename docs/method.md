# Method

The three classifications type the same blocks under the same `block_key`
(`<city>-<block_id>`). Their inputs, preprocessing and model are documented in the
packages; this page summarises them and records the settings of the two city sets.

## Blocks and sampling units
Blocks are street enclosures (momepy, OpenStreetMap streets) that contain buildings, at
least 1,500 m² and with building coverage of at least 3 %. In the thirteen-city set, open
blocks are trimmed to their built envelope and mega-blocks that hold several fabrics are
split into sampling units: along internal streets where available, by building patches,
or into partitions of about 150 buildings. Minor ways cut blocks where the street
hierarchy is incompletely mapped. The rules and parameters are in
`urban-block-morphology-morphometric` (`docs/method.md`, `configs/sets/thirteen_cities.yaml`).

## A · morphometric
46 descriptors of block size and shape, built intensity, height, building size and shape,
arrangement, street interface and neighbourhood context, after an explicit missing-data
treatment (`urban-block-morphology`, descriptor set `morphometric46`; building sources and
height selection per city in `urban-block-morphology-morphometric`). No building-form input:
the supervised detector of the earlier framework is not used.

## B · image (DINOv3)
Each block is cut from the aerial image as a square crop centred on the block, with the
surroundings dimmed. A frozen DINOv3 ViT-L/16 backbone pretrained on 493 million
satellite images embeds the crop into 2,048 values (class token and mean patch token,
register tokens excluded), reduced by PCA to 50. Next to it, 23 component-structure
measures describe the shares, mixing, fragmentation and adjacency of vegetation, roads and
paving, roofs and open ground, weighted 1.5 after standardisation
(`urban-block-morphology-ssl`).

## C · united
The standardised morphometric matrix of A and the matrix of B before its final PCA are
each scaled to unit total variance and joined (50:50), so neither half dominates
(`urban-block-morphology-united`).

## Model
Whitened PCA with d components, K-means (10 initialisations, seed 42), K from 5 to 15
(5 to 25 for the pooled thirteen-city models, whose 13 cities hold more distinct fabrics).
K is chosen by one rule: every type holds at least 12 blocks, K is at or above the inertia
elbow, and among those K the best mean of the min–max normalised silhouette,
Calinski–Harabasz and inverted Davies–Bouldin indices wins. If no K meets both
conditions, the best K that keeps every type at 12 blocks is reported as a **fallback**
(exploratory). One model in the study is a fallback: Tel Aviv-Yafo, B, three-city set
(K = 6).

City models are fitted on one city; pooled models on all cities of a set, stacked in the
set's pooling order (K-means initialisation depends on the row order).

## Dimension d: the decision rule
The rule was fixed on 22 October 2026, before the models of the article were refitted, and
is applied once per classification and set, on the pooled model; the city models of a set
use the same d.

- **Candidates:** d ∈ {2, 5, 8}; for B and C of the thirteen-city set {2, 5}. Each
  candidate is evaluated at the K the K rule selects.
- **Exclusions:** E1, Cramér's V between type and "block without any measured height"
  exceeds that of d = 2 by more than 0.10; E2, no admissible K.
- **Improvement over d = 2, all three required:** C1, the silhouette gap above a matched
  Gaussian null exceeds that of d = 2 by at least 0.02; C2, the median pairwise ARI over
  100 subsamples (80 %) is not lower by more than 0.05; C3, the share of 100 subsamples in
  which the K rule repeats its K is not lower by more than 0.10.
- **Choice:** the smallest qualifying d; if none qualifies, d = 2.

Construction years and every other external variable play no part.

| set | classification | d | K | C1 gap Δ | C2 stability (d vs 2) | C3 K repeat (d vs 2) | E1 V (d vs 2) | qualifies |
|---|---|---|---|---|---|---|---|---|
| three-city | A | **5** | 8 | +0.053 | 0.87 vs 0.88 | 85 % vs 31 % | 0.22 vs 0.19 | yes |
| three-city | B | **5** | 10 | +0.053 | 0.92 vs 0.84 | 100 % vs 77 % | 0.20 vs 0.13 | yes |
| three-city | B | 8 | 9 | +0.077 | 0.90 vs 0.84 | 96 % vs 77 % | 0.25 vs 0.13 ✗ | no (E1) |
| three-city | C | 5 | 8 | +0.067 | 0.71 vs 0.94 ✗ | 46 % vs 57 % ✗ | 0.22 vs 0.20 | no (C2, C3) |
| three-city | C | **8** | 10 | +0.071 | 0.90 vs 0.94 | 99 % vs 57 % | 0.23 vs 0.20 | yes |
| thirteen-city | A | **5** | 12 | +0.053 | 0.91 vs 0.81 | 98 % vs 53 % | 0.22 vs 0.17 | yes |
| thirteen-city | B | 5 | 12 | +0.051 | 0.95 vs 0.89 | 51 % vs 90 % ✗ | 0.09 vs 0.09 | no (C3) → **d = 2** (K 11) |
| thirteen-city | C | **5** | 14 | +0.070 | 0.96 vs 0.72 | 82 % vs 41 % | 0.17 vs 0.17 | yes |

For B of the thirteen-city set, d = 8 was run later and would pass C1–C3; it was not a
candidate when the rule was fixed and is reported as a sensitivity result only.

## Stability
Partition stability: 100 refits of the whole space and K-means on 80 % subsamples (seed
42 + i), median pairwise ARI over the blocks shared by each pair. K stability: the share of
the subsamples in which the K rule repeats its K. Both are in `results/<set>/models.csv`.
