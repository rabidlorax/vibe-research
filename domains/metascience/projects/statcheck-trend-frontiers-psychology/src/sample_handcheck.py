#!/usr/bin/env python3
"""Draw the fixed random sample of extracted results that is read by hand.

Per period (2010-2015, 2016-2021, 2022-2026): 40 results flagged inconsistent,
20 flagged as decision inconsistencies, 10 not flagged. Written with context to
data/raw/handcheck_sample.csv (article text, CC BY, not committed).

Usage: python src/sample_handcheck.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261123
PERIODS = [(2010, 2015), (2016, 2021), (2022, 2026)]


def main():
    c = pd.read_csv(ROOT / "data" / "raw" / "contexts.csv.gz")
    r = pd.read_csv(ROOT / "data" / "results.csv.gz", usecols=["decision_error_1t"])
    c["decision_error_1t"] = r.decision_error_1t.to_numpy()  # same row order as results.csv.gz
    parts = []
    for i, (a, b) in enumerate(PERIODS):
        p = c[(c.year >= a) & (c.year <= b)]
        dec = p[p.decision_error_1t == 1].sample(20, random_state=SEED + i)
        inc = p[(p.error_1t == 1) & ~p.index.isin(dec.index)].sample(40, random_state=SEED + 10 + i)
        ok = p[p.error_1t == 0].sample(10, random_state=SEED + 20 + i)
        for name, d in (("inconsistent", inc), ("decision", dec), ("not_flagged", ok)):
            parts.append(d.assign(stratum=name, period=f"{a}-{b}"))
    s = pd.concat(parts).reset_index(drop=True)
    s.insert(0, "id", range(1, len(s) + 1))
    s.to_csv(ROOT / "data" / "raw" / "handcheck_sample.csv", index=False)
    print(s.groupby(["period", "stratum"]).size())


if __name__ == "__main__":
    main()
