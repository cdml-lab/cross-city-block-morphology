# Thirteen-city type examples (manuscript revision, 2026-11-25)

Pooled combined classification of the thirteen-city set (K = 14, types U0–U13), computed from the
released labels, morphometric descriptors and image-component shares (no external variable).

- `type_city_profiles.csv` — per type and city: units, share of the city's units, city-normalised
  mass, presence (normalised mass >= 0.5/13), unit origins (street/patch/partition) and medians of
  height, GSI, FSI, mean footprint, buildings per ha, shared walls, street-edge share and unit area.
- `type_summary.csv` — per type: cities present, continents, city-specific flag (>= 50 % of
  normalised mass in one city), and the range of city medians relative to the range of type medians.
- `examples.csv` — the units shown in Figure 10, chosen by fixed rules: (R1) the type present in most
  cities, in one present city per continent; (R2) among the other types present in >= 4 cities, the one most
  different from R1, in every city where it is present; (R3) the two city-specific types closest in median
  height and coverage; (R4) the other city-specific types, each in its main city; each unit is the one nearest
  its type's median profile of the eight key descriptors and the five image-component shares (median/IQR
  standardised, the two groups weighted equally, as in the combined representation; revised 2026-11-25,
  previously the key descriptors alone). The `share c0`–`share c4` columns give the shown unit's component
  shares.
