"""Reproduce every model of the study from its inputs and compare it with the published labels.

For one city set (configs/three_cities.yaml or configs/thirteen_cities.yaml), every model of the
three classifications is refitted with the pinned packages, block for block:

    A  morphometric      urban-block-morphology-morphometric  (blockmorph_morphometric.model.fit_track_a)
    B  image (DINOv3)    urban-block-morphology-ssl     (blockssl.model.fit)
    C  united            urban-block-morphology-united  (blocktypes.model.fit)

for each city model and for the pooled model (cities stacked in the set's pooling order). A model
passes when the number of blocks, K and the rule status equal the published ones and the
partition is identical (ARI = 1, identical type ids); with --sweeps, the K sweep is compared too.

    python scripts/check_reproduction.py configs/three_cities.yaml --inputs ../study-inputs/three_cities
           [--tracks A B C] [--report reproduction_three_cities.json]

Inputs (not part of this repository; docs/reproduction.md):
    <inputs>/descriptors/<CITY>.parquet   46 treated morphometric descriptors per block (Track A, C)
    <inputs>/features/<CITY>/             ssl_embeddings.npy, ssl_block_ids.csv,
                                          structure_features.parquet (Track B, C)
    <inputs>/sweeps/<CITY|pooled>_<morpho|ssl|united>.csv   optional, the study's K sweeps
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import adjusted_rand_score

# the study's K-sweep tables -> the packages' sweep columns
SWEEP_FLOAT = {"silhouette": "silhouette", "sil_gap": "silhouette_gap", "calinski": "calinski",
               "davies": "davies", "inertia": "inertia", "combined": "combined"}
SWEEP_EXACT = {"min_cluster": "min_type_size", "admissible": "size_ok", "elbow_k": "elbow_k"}
TRACK_FILE = {"A": "morpho", "B": "ssl", "C": "united"}


def krange(v):
    return tuple(range(int(v[0]), int(v[1]) + 1))


def load_city(inputs: Path, city: str, need_desc: bool, need_feat: bool):
    out = {}
    if need_feat:
        from blockssl.features import load_features
        f = load_features(inputs / "features" / city)
        out.update(emb=f["embeddings"], sf=f["structure"], ids=f["block_ids"])
    if need_desc:
        from blockmorph_morphometric.descriptors import as_model_input
        p = inputs / "descriptors" / f"{city}.parquet"
        d = pd.read_parquet(p) if p.exists() else pd.read_csv(p.with_suffix(".csv"), index_col="block_id")
        d.index = d.index.astype(int)
        d = as_model_input(d)
        ids = out.get("ids", np.sort(d.index.to_numpy()))
        if set(ids) != set(d.index):
            raise ValueError(f"{city}: descriptors and image features cover different blocks")
        out.update(desc=d.loc[ids], ids=ids)
    return out


def fit(track, data, prm):
    if track == "A":
        from blockmorph_morphometric.model import fit_track_a
        r = fit_track_a(data["desc"], prm)
        return r.labels, r.sweep, r.status
    if track == "B":
        from blockssl.model import fit as fit_b
        labels, sweep, status, _, _ = fit_b(data["emb"], data["sf"], prm)
        return labels, sweep, status
    from blocktypes.model import fit as fit_c
    labels, sweep, status, _, _ = fit_c(data["desc"], data["emb"], data["sf"], prm)
    return labels, sweep, status


def params(track, cfg, model):
    t = cfg["tracks"][track]
    kr = krange(t["k_range_pooled"] if model == "pooled" else t["k_range_city"])
    m = cfg.get("model", {})
    if track == "A":
        # the core parameters of urban-block-morphology-morphometric's set configuration
        # (configs/sets/<set>.yaml, model:), as given in this repository's set configuration
        from dataclasses import replace
        from blockmorph.params import Params as CoreParams
        return replace(CoreParams(), pca_components=int(t["d"]), pca_whiten=bool(m.get("pca_whiten", True)),
                       k_range=kr, min_type_size=int(m.get("min_type_size", 12)),
                       kmeans_n_init=int(m.get("kmeans_n_init", 10)), random_state=int(m.get("random_state", 42)))
    if track == "B":
        from blockssl.params import Params
    else:
        from blocktypes.params import Params
    return Params.from_dict({"pca_components": int(t["d"]), "k_range": list(kr),
                             "pca_whiten": bool(m.get("pca_whiten", True)),
                             "min_type_size": int(m.get("min_type_size", 12)),
                             "kmeans_n_init": int(m.get("kmeans_n_init", 10)),
                             "random_state": int(m.get("random_state", 42))})


def compare_sweep(sweep: pd.DataFrame, path: Path) -> dict:
    """The study's K sweep against the reproduced one: every metric within 1e-6 (relative), the
    smallest type, the size condition, the elbow and the selected K identical."""
    ref = pd.read_csv(path).set_index("k")
    got = sweep.set_index("k")
    if list(ref.index) != list(got.index):
        return {"ok": False, "reason": f"K range {list(got.index)} vs {list(ref.index)}"}
    rel = {a: float(np.nanmax(np.abs(got[b] - ref[a]) / np.maximum(np.abs(ref[a]), 1e-12)))
           for a, b in SWEEP_FLOAT.items() if a in ref and b in got}
    exact = {a: bool((got[b].fillna(-1).astype(int) == ref[a].fillna(-1).astype(int)).all())
             for a, b in SWEEP_EXACT.items() if a in ref and b in got}
    if "chosen_k" in ref and "selected" in got:
        exact["chosen_k"] = int(ref["chosen_k"].iloc[0]) == int(got.index[got["selected"].astype(bool)][0])
    return {"ok": bool(all(v <= 1e-6 for v in rel.values()) and all(exact.values())),
            "max_relative_difference": max(rel.values()) if rel else None, "exact": exact}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("config")
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--tracks", nargs="+", default=["A", "B", "C"])
    ap.add_argument("--report")
    a = ap.parse_args(argv)
    cpath = Path(a.config).resolve()
    cfg = yaml.safe_load(cpath.read_text(encoding="utf-8"))
    root = cpath.parent.parent
    inputs = Path(a.inputs).resolve()
    labels = pd.read_csv(root / cfg["labels"])
    cities = [str(c) for c in cfg["cities"]]
    need_desc = bool({"A", "C"} & set(a.tracks))
    need_feat = bool({"B", "C"} & set(a.tracks))
    t0 = time.time()
    data = {c: load_city(inputs, c, need_desc, need_feat) for c in cities}
    lab = {c: labels[labels.area == c].set_index("block_id").loc[data[c]["ids"]] for c in cities}
    res = []
    for track in a.tracks:
        exp_k = cfg["tracks"][track]["expected_k"]
        for model in cities + ["pooled"]:
            if model == "pooled":
                d = {k: (np.vstack([data[c][k] for c in cities]) if k == "emb" else
                         pd.concat([data[c][k] for c in cities]) if k in ("sf", "desc") else None)
                     for k in data[cities[0]] if k != "ids"}
                exp = np.concatenate([lab[c][f"{track}_pooled"].to_numpy() for c in cities])
            else:
                d = data[model]
                exp = lab[model][f"{track}_city"].to_numpy()
            got, sweep, status = fit(track, d, params(track, cfg, model))
            got = np.asarray(got)
            ek, est = exp_k[model]
            r = {"set": cfg["name"], "track": track, "model": model, "blocks": int(len(got)),
                 "expected_k": int(ek), "reproduced_k": int(status["selected_k"]),
                 "expected_status": est, "status": status["status"],
                 "ari": round(float(adjusted_rand_score(exp, got)), 6),
                 "identical_type_ids": bool((exp == got).all())}
            sp = inputs / "sweeps" / f"{model}_{TRACK_FILE[track]}.csv"
            if sp.exists():
                r["sweep"] = compare_sweep(sweep, sp)
            r["ok"] = bool(r["expected_k"] == r["reproduced_k"] and r["status"] == est and r["ari"] == 1.0
                           and r["identical_type_ids"] and r.get("sweep", {"ok": True})["ok"])
            res.append(r)
            print(f"{track} {model:>7} {r['blocks']:>6} K {r['expected_k']:>2}/{r['reproduced_k']:>2} "
                  f"{r['status']:>8} ARI {r['ari']:.4f} ids {'same' if r['identical_type_ids'] else 'DIFF'}"
                  f" sweep {'-' if 'sweep' not in r else ('same' if r['sweep']['ok'] else 'DIFF')}", flush=True)
    ok = all(r["ok"] for r in res)
    print(("REPRODUCTION_OK" if ok else "REPRODUCTION_DIFFERS") + f"  ({len(res)} models, {time.time() - t0:.0f} s)")
    if a.report:
        import blockmorph
        import sklearn
        vers = {}
        for m in ("blockmorph", "blockmorph_morphometric", "blockssl", "blocktypes"):
            try:
                vers[m] = getattr(__import__(m), "__version__", "?")
            except ImportError:
                vers[m] = None
        rep = {"result": "REPRODUCTION_OK" if ok else "REPRODUCTION_DIFFERS", "config": cfg["name"],
               "packages": vers, "python": sys.version.split()[0], "numpy": np.__version__,
               "pandas": pd.__version__, "scikit_learn": sklearn.__version__, "blockmorph_core": blockmorph.__version__,
               "seconds": round(time.time() - t0, 1), "models": res}
        Path(a.report).write_text(json.dumps(rep, indent=1), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
