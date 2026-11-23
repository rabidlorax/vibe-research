#!/usr/bin/env python3
"""Draw the fixed random sample of extracted results that is read by hand.

Per period (2010-2015, 2016-2021, 2022-2026): 40 results flagged inconsistent,
20 flagged as decision inconsistencies, 10 not flagged; plus, added post hoc,
20 flagged and 20 not flagged from July-November 2026. Written with context to
data/raw/handcheck_sample.csv (article text, CC BY, not committed).

The sample that was actually read is recorded in results/handcheck.csv. It was
drawn with --redraw from the extraction as it stood before a bug fix removed
four results, so --redraw on the current data gives a different draw. Without
arguments this script looks the recorded sample up again and writes it with
context, so the labels can be re-read against the article text.

Usage: python src/sample_handcheck.py [--redraw]
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261123
PERIODS = [(2010, 2015), (2016, 2021), (2022, 2026)]


def lookup():
    keys = pd.read_csv(ROOT / "results" / "handcheck.csv")
    c = pd.read_csv(ROOT / "data" / "raw" / "contexts.csv.gz").drop_duplicates(["pmcid", "raw"])
    s = keys.merge(c[["pmcid", "raw", "context"]], left_on=["pmcid", "extracted"],
                   right_on=["pmcid", "raw"], how="left")
    s.drop(columns="raw").to_csv(ROOT / "data" / "raw" / "handcheck_sample.csv", index=False)
    print(f"{len(s)} recorded items, {int(s.context.isna().sum())} no longer extracted")


def main():
    if "--redraw" not in sys.argv:
        return lookup()
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
    # Post-hoc addition: second half of 2026 (electronic publication July onward),
    # where the rate fell, to check that extraction still works there.
    a = pd.read_csv(ROOT / "data" / "articles.csv.gz")
    late = set(a.pmcid[(a.epub_year == 2026) & (a.epub_month >= 7)])
    used = pd.concat(parts).index
    p = c[c.pmcid.isin(late) & ~c.index.isin(used)]
    parts.append(p[p.error_1t == 1].sample(20, random_state=SEED + 30).assign(stratum="inconsistent", period="2026H2"))
    parts.append(p[p.error_1t == 0].sample(20, random_state=SEED + 31).assign(stratum="not_flagged", period="2026H2"))
    s = pd.concat(parts).reset_index(drop=True)
    s.insert(0, "id", range(1, len(s) + 1))
    s.to_csv(ROOT / "data" / "raw" / "handcheck_sample.csv", index=False)
    print(s.groupby(["period", "stratum"]).size())


if __name__ == "__main__":
    main()
