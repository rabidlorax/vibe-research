#!/usr/bin/env python3
"""Check whether st_dens and pl_ratdor in the ps rows that come from the
Kepler KOI tables are those tables' fitted transit quantities koi_srho and
koi_dor.

Usage: python src/koi_columns.py   (five TAP queries; needs data/raw/ps.csv)
Writes results/koi_columns.md and data/koi_tables.sha256.
"""
import hashlib
import io
import pathlib
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent
TABLES = ["q1_q8_koi", "q1_q12_koi", "q1_q16_koi", "q1_q17_dr24_koi", "q1_q17_dr25_koi"]


def main():
    ps = pd.read_csv(HERE / "data" / "raw" / "ps.csv", low_memory=False)
    out, shas = [], []
    for t in TABLES:
        q = f"select kepoi_name,kepler_name,koi_srho,koi_dor from {t} where kepler_name is not null"
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q) + "&format=csv"
        req = urllib.request.Request(url, headers={"User-Agent": "vibe-research-consistency-audit/0.1 (research script)"})
        raw = urllib.request.urlopen(req, timeout=300).read()
        (HERE / "data" / "raw" / f"{t}.csv").write_bytes(raw)
        shas.append(f"{hashlib.sha256(raw).hexdigest()}  {t}.csv  query: {q}")
        k = pd.read_csv(io.BytesIO(raw))
        d = ps[ps.soltype == f"Kepler Project Candidate ({t})"]
        m = d.merge(k.drop_duplicates("kepler_name"), left_on="pl_name", right_on="kepler_name")
        line = f"{t}: {len(d)} ps rows, {len(m)} matched to a KOI by planet name"
        for a, b in (("st_dens", "koi_srho"), ("pl_ratdor", "koi_dor")):
            both = m[m[a].notna() & m[b].notna()]
            same = np.isclose(both[a], both[b], rtol=1e-6, atol=0)
            line += f"; {a} == {b} in {int(same.sum())} of {len(both)} rows with both values"
        out.append(line)
    sup = ps[ps.soltype == "Kepler Project Candidate (q1_q17_dr25_sup_koi)"]
    out.append(f"q1_q17_dr25_sup_koi: {len(sup)} ps rows, not compared; stellar reference: "
               + "; ".join(f"{k} ({v})" for k, v in sup.st_refname.str.extract(r">\s*([^<]+?)\s*</a>")[0].value_counts().items())
               + f"; rows with pl_ratdor: {int(sup.pl_ratdor.notna().sum())}")
    (HERE / "data" / "koi_tables.sha256").write_text("\n".join(shas) + "\n")
    (HERE / "results" / "koi_columns.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
