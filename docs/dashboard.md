# Dashboard (v1.0.0)

`index.html` is the study's dashboard: every block of both city sets (7,556 blocks;
42,470 sampling units), the city models and the pooled models of the three
classifications, and building heights, floors, coverage (GSI) and intensity (FSI), in 3D.

- View in the browser: https://cdml-lab.github.io/cross-city-block-morphology/
- Download (release v1.0.0): https://github.com/cdml-lab/cross-city-block-morphology/releases/download/v1.0.0/block-morphology-studio.html

Controls: **View** (by city, or the three classifications side by side), **Cities**,
**Classification scope** (per city; 3 cities (pooled); 13 cities (pooled)), **Colour by**, background map and layers. "How it works" explains
the models. Tel Aviv-Yafo, Manhattan and Amsterdam show the blocks of the three-city set
in the per-city and 3 cities scopes and those of the thirteen-city set in the 13 cities
scope.

Requirements:
- **Internet:** the maps load deck.gl 9.0.35 (unpkg.com) and the background maps from
  their providers.
- **WebGL 2** and a current Chrome, Edge, Firefox or Safari (the page unpacks its data
  with `DecompressionStream`).
- One file, 41 MB. Each city is stored compressed and unpacked when it is first shown.

Every block label in the page equals `results/<set>/assignments.csv`. Not included:
construction years and building-level detector classes.
