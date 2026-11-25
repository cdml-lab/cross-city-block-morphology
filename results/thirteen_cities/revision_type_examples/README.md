# Thirteen-city type examples (manuscript revision, 2026-11-25)

Pooled combined classification of the thirteen-city set (K = 14, types U0–U13), computed from the
released labels and morphometric descriptors only.

- `type_city_profiles.csv` — per type and city: units, share of the city's units, city-normalised
  mass, presence (normalised mass >= 0.5/13), unit origins (street/patch/partition) and medians of
  height, GSI, FSI, mean footprint, buildings per ha, shared walls, street-edge share and unit area.
- `type_summary.csv` — per type: cities present, continents, city-specific flag (>= 50 % of
  normalised mass in one city), and the range of city medians relative to the range of type medians.
- `examples.csv` — the units shown in Figure 9, chosen by fixed rules: (R1) the type present in most
  cities, in three cities on different continents; (R2) among the other types present in >= 4 cities, the one most
  different from R1; (R3) the two city-specific types closest in median height and coverage; each
  unit is the one nearest its type's median profile.
