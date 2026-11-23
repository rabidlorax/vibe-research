#!/usr/bin/env python3
"""Check whether st_dens and pl_ratdor in the ps rows that come from the
Kepler Q1-Q17 DR25 KOI table are that table's fitted transit quantities
koi_srho and koi_dor.

Usage: python src/koi_columns.py   (one TAP query; needs data/raw/ps.csv)
Writes results/koi_columns.md.
"""
import io
import pathlib
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent


def main():
    q = "select kepoi_name,kepler_name,koi_srho,koi_dor from q1_q17_dr25_koi where kepler_name is not null"
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q) + "&format=csv"
    req = urllib.request.Request(url, headers={"User-Agent": "vibe-research-consistency-audit/0.1 (research script)"})
    raw = urllib.request.urlopen(req, timeout=300).read()
    (HERE / "data" / "raw" / "dr25_koi.csv").write_bytes(raw)
    k = pd.read_csv(io.BytesIO(raw))
    d = pd.read_csv(HERE / "data" / "raw" / "ps.csv", low_memory=False)
    d = d[d.soltype == "Kepler Project Candidate (q1_q17_dr25_koi)"]
    m = d.merge(k.drop_duplicates("kepler_name"), left_on="pl_name", right_on="kepler_name")
    out = [f"ps rows with soltype 'Kepler Project Candidate (q1_q17_dr25_koi)': {len(d)}; "
           f"matched to a DR25 KOI by planet name: {len(m)}"]
    for a, b in (("st_dens", "koi_srho"), ("pl_ratdor", "koi_dor")):
        both = m[m[a].notna() & m[b].notna()]
        same = np.isclose(both[a], both[b], rtol=1e-6, atol=0)
        out.append(f"{a} == {b}: {int(same.sum())} of {len(both)} rows with both values")
    (HERE / "results" / "koi_columns.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
