#!/usr/bin/env python3
"""Draw, or look up again, the sample of extracted results that was read by hand.

--redraw draws a new sample. Per period (2010-2015, 2016-2021, 2022-2026): 20
results flagged as decision inconsistencies, then 40 flagged results of any kind
from those left (so this second stratum also contains some decision
inconsistencies), then 10 unflagged results; plus 20 flagged and 20 unflagged
from articles published July-November 2026.

The sample that was actually read is recorded in results/handcheck.csv. It was
drawn from an earlier state of the extraction (before the fixes described in the
README), so --redraw on the current data gives a different draw. Without
arguments this script looks the recorded items up in the current extraction and
writes them with 150 characters of context to data/raw/handcheck_sample.csv
(article text, CC BY, not committed), so the labels can be re-read. Items are
matched on article and extracted string; when the same string occurs more than
once in an article the first occurrence is shown, which may not be the one
originally read.

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
