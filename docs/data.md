# Data sources and licences

| content | source | licence |
|---|---|---|
| building footprints | OpenStreetMap; Overture Maps buildings (conflated, incl. Microsoft and Google footprints) where OpenStreetMap is incomplete | ODbL 1.0 (OpenStreetMap-derived); CDLA Permissive 2.0 (other Overture sources) |
| streets and all derived block geometry | © OpenStreetMap contributors | ODbL 1.0 |
| building heights | OpenStreetMap tags; NYC roof heights (Manhattan); 3D-GloBFP (Che et al. 2024); Google Open Buildings 2.5D; storeys × 3.2 m | open-data terms of each source; CC BY 4.0 (3D-GloBFP, Open Buildings) |
| aerial imagery of the image classification | Esri World Imagery and national or municipal orthophotos, per city | provider copyright; not redistributed |
| DINOv3 backbone | Meta, `vit_large_patch16_dinov3.sat493m` | DINOv3 licence; downloaded by the user |
| construction year, land use, price (Tel Aviv-Yafo, Manhattan, Amsterdam) | municipal and national open data, cited in the article | used only after fitting; not redistributed here |

The results tables and the map data of the dashboard are derived from these sources and
are shared under ODbL 1.0 with the attributions above. The sources of each city, and the
height source selected for it: `urban-block-morphology-morphometric` (`docs/sources.md`).
