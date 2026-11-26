# Extended results archive (supplementary material)

Numerical outputs and diagnostics listed in Supplementary Section S13 (extended results archive) of the manuscript
"Measuring and Learning Urban Form: A Cross-City Comparison of Morphometric and Self-Supervised Representations". All
files are aggregate statistics of the adopted models; no figures, imagery, block-level construction years or land-use
records are included (those layers are available from the cited providers). Representations: A morphometric,
B self-supervised image, C combined. Effect sizes: Kruskal-Wallis eta2H = (H - k + 1) / (n - k); land-use composition:
PERMANOVA R2 on Bray-Curtis distances of seven harmonised use shares. Bootstrap intervals: 1,000 paired resamples of
blocks (iid) or of 500 m grid cells within each city (spatial).

Paths are relative to this folder (`results/supplementary_archive/`) unless stated otherwise.

| Item (Supplementary Section S13) | File | Content |
|---|---|---|
| Dimensionality rule, every candidate and criterion | `model_selection/dimensionality_rule_diagnostics.csv` | every candidate d: gap, stability, K repetition, exclusion and criteria flags |
| Fusion-weight sensitivity, by rule and at K = 10 | `robustness/fusion_weight_sensitivity.csv` | morphometric variance share 0.3-0.7, K by rule and K = 10 |
| Imagery-source sensitivity | `robustness/imagery_source_sensitivity.csv` | Manhattan and Amsterdam re-embedded from the Tel Aviv-Yafo provider: agreement with the adopted partitions and external effect sizes |
| Image-window coverage by city | `image_support/spatial_support.csv` | share of blocks at least 99 % inside the 154 m and 169 m windows, by city |
| All external measures at K = 8, 10, 12 (incl. secondary land-use measures) | `external_assessment/matched_k_all_measures.csv` | year, mixing entropy, modal-use V, composition R2 at K = 8, 10, 12 (pooled and within city) |
| Effect sizes with 95% CIs by model and scope (Figure 7) | `external_assessment/effect_sizes_by_scope.csv` | point estimates and spatial CIs by model and scope |
| Paired bootstrap, iid and spatial, η²H outcomes | `external_assessment/paired_bootstrap_eta2_all.csv` | paired differences between representations, iid and spatial, of the year and mixing-entropy eta2H |
| Land-use composition R²: values, bootstrap, implementation check | `external_assessment/landuse_composition_r2_points.csv`, `landuse_composition_r2_bootstrap.csv`, `landuse_permanova_check.csv` | composition R2 by representation, K and scope; values and paired differences with CIs; R2 from the distance form, the study code and principal-coordinate space |
| Dispersion (PERMDISP) by scope and type | `external_assessment/landuse_dispersion_permdisp.csv`, `landuse_dispersion_by_type.csv` | PERMDISP F, p and distance to type centroid |
| Land-use mixing entropy (effect sizes) | `external_assessment/landuse_mixing_entropy_effect_sizes.csv` | mixing-entropy eta2H, city and pooled models (pooled within city: `matched_k_all_measures.csv`) |
| Tel Aviv-Yafo A2: profiles, separation of every measure, year effect sizes, representatives | `tel_aviv_a2/` | A2 by image type: profiles, cross-tabulation, eta2 of every descriptor and component measure, year effect sizes, representative blocks |
| Thirteen-city type profiles and examples | `results/thirteen_cities/revision_type_examples/` (from the repository root) | type profiles by city, type summary, the examples' selection rule and units |
| Assignments, models and types of both samples | `results/three_cities/`, `results/thirteen_cities/` (from the repository root) | every block's types, every model, every type (documented in `docs/results.md`) |
