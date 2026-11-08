# Verification records

| file | content |
|---|---|
| `reproduction_three_cities.json` | `scripts/check_reproduction.py` on the three-city set: 12 models, REPRODUCTION_OK |
| `reproduction_thirteen_cities.json` | the same for the thirteen-city set: 42 models, REPRODUCTION_OK |
| `reproduction_three_cities_clean_github_install.json` | the three-city set in a clean environment installed from GitHub (`requirements.txt`): 12 models, REPRODUCTION_OK |
| `reproduction_thirteen_cities_clean_github_install.json` | the thirteen-city set in the same clean environment: 42 models, REPRODUCTION_OK |

Each report lists, per model, the blocks, the expected and reproduced K and status, the ARI,
whether the type numbers are identical and the comparison of the K sweep, with the
package and library versions of the run (8 November 2026; `docs/reproduction.md`).
