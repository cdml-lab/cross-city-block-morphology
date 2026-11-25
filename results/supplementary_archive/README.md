# Extended results archive (supplementary material)

Numerical outputs and diagnostics referenced by the supplementary material of the manuscript "Measuring and Learning
Urban Form: A Cross-City Comparison of Morphometric and Self-Supervised Representations". All files are aggregate
statistics of the adopted models; no figures, imagery, block-level construction years, land use or prices are included
(those layers are available from the cited providers). Representations: A morphometric, B self-supervised image,
C combined. Effect sizes: Kruskal-Wallis eta2H = (H - k + 1) / (n - k); land-use composition: PERMANOVA R2 on
Bray-Curtis distances of seven harmonised use shares. Bootstrap intervals: 1,000 paired resamples of blocks (iid) or of
500 m grid cells within each city (spatial).

| Supplement | File | Content |
|---|---|---|
| S4 | image_support/spatial_support.csv | share of blocks at least 99 % inside the 154 m and 169 m windows, by city |
| S6, Table S5 | model_selection/dimensionality_rule_diagnostics.csv | every candidate d: gap, stability, K repetition, exclusion and criteria flags |
| S8, Table S7 | robustness/fusion_weight_sensitivity.csv | morphometric variance share 0.3-0.7, K by rule and K = 10 |
| S8, Table S8 | robustness/imagery_source_sensitivity.csv | Manhattan and Amsterdam re-embedded from the Tel Aviv-Yafo provider |
| S9.1, Table S9 | external_assessment/matched_k_all_measures.csv | year, mixing entropy, price rank, modal-use V, composition R2 at K = 8, 10, 12 (pooled and within city) |
| S9.1 | external_assessment/landuse_composition_r2_points.csv | composition R2 by representation, K and scope |
| S9.1 | external_assessment/landuse_permanova_check.csv | R2 from the distance form, the study code and principal-coordinate space |
| S9.1 | external_assessment/landuse_mixing_entropy_effect_sizes.csv | mixing-entropy eta2H, city and pooled models (pooled within city: matched_k_all_measures.csv) |
| S9.2, Table S10 | external_assessment/paired_bootstrap_eta2_all.csv | paired differences, iid and spatial, year, mixing entropy and price rank |
| S9.2, Table S10 | external_assessment/landuse_composition_r2_bootstrap.csv | composition R2 values and paired differences with CIs |
| Figure 7 | external_assessment/effect_sizes_by_scope.csv | point estimates and spatial CIs by model and scope |
| S9.3 | external_assessment/landuse_dispersion_permdisp.csv, landuse_dispersion_by_type.csv | PERMDISP F, p and distance to type centroid |
| S9.4 | external_assessment/price_effect_sizes.csv | exploratory price association: eta2H of price and within-city price rank |
| S10, Table S11, Figure 6a | tel_aviv_a2/ | A2 by image type: profiles, cross-tabulation, eta2 of every descriptor and component measure, year effect sizes, representative blocks (rule in S10) |
| S11, Table S12 | ../thirteen_cities/revision_type_examples/ | thirteen-city type profiles and examples |
