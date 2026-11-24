#!/usr/bin/env python3
"""Yearly rates of statistical reporting inconsistencies and their trend.

Reads data/articles.csv.gz and data/results.csv.gz (written by extract.py) and
writes, in results/: yearly.csv, variants.csv, trend.txt, by_kind.csv, trend.png
(planned before the full data were seen) and yearly_no_one_tailed_allowance.csv,
half_years_2023_2026.csv, received_quarters.csv, received_quarters_fast.csv,
received_months.csv, post_hoc.txt, descriptives.txt, handcheck_summary.csv (added
afterwards; descriptives_from_text.txt is rewritten only when data/raw/ is present).

Usage: python src/analyze.py        (under a minute; seed fixed)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from statcheck_py import _p, consistent  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
SEED, BOOT = 20261123, 2000


def cluster_boot(df, col, rng):
    """95% percentile interval for the pooled share sum(col)/n, resampling articles."""
    g = df.groupby("pmcid")[col].agg(["sum", "size"]).to_numpy()
    idx = rng.integers(0, len(g), size=(BOOT, len(g)))
    s = g[idx]
    share = s[:, :, 0].sum(1) / s[:, :, 1].sum(1)
    return np.percentile(share, [2.5, 97.5])


def wilson(k, n):
    if n == 0:
        return (np.nan, np.nan)
    z = 1.959964
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (c - h, c + h)


def yearly(res, arts, err="error_1t", dec="decision_error_1t"):
    rng = np.random.default_rng(SEED)
    rows = []
    for y, a in arts.groupby("year"):
        r = res[res.year == y]
        per = r.groupby("pmcid").agg(n=(err, "size"), e=(err, "sum"), d=(dec, "sum"))
        lo_e, hi_e = cluster_boot(r, err, rng)
        lo_d, hi_d = cluster_boot(r, dec, rng)
        k1, k2, n = int((per.e > 0).sum()), int((per.d > 0).sum()), len(per)
        w1, w2 = wilson(k1, n), wilson(k2, n)
        rows.append({
            "year": y, "articles": len(a), "articles_with_results": n,
            "pct_articles_with_results": 100 * n / len(a),
            "results": len(r), "median_results_per_article": per.n.median(),
            "pct_results_inconsistent": 100 * r[err].mean(), "ci_lo": 100 * lo_e, "ci_hi": 100 * hi_e,
            "pct_results_decision": 100 * r[dec].mean(), "dec_ci_lo": 100 * lo_d, "dec_ci_hi": 100 * hi_d,
            "mean_article_pct_inconsistent": 100 * (per.e / per.n).mean(),
            "mean_article_pct_decision": 100 * (per.d / per.n).mean(),
            "pct_articles_any_inconsistent": 100 * k1 / n, "any_ci_lo": 100 * w1[0], "any_ci_hi": 100 * w1[1],
            "pct_articles_any_decision": 100 * k2 / n, "anydec_ci_lo": 100 * w2[0], "anydec_ci_hi": 100 * w2[1],
            "pct_p_exact": 100 * (r.p_cmp == "=").mean(),
            "pct_p_zero": 100 * r.p_zero.mean(),
        })
    return pd.DataFrame(rows)


def clustered_trend(res, col, extra=None):
    """Logistic regression of a result-level flag on publication year with
    standard errors clustered on article. Returns odds ratio per year and CI."""
    X = pd.DataFrame({"const": 1.0, "year": res.year - 2018})
    if extra is not None:
        X = pd.concat([X, extra], axis=1)
    m = sm.GLM(res[col], X, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": res.pmcid.astype("category").cat.codes})
    b, se = m.params["year"], m.bse["year"]
    return np.exp(b), np.exp(b - 1.96 * se), np.exp(b + 1.96 * se), m.pvalues["year"]


def main():
    OUT.mkdir(exist_ok=True)
    arts = pd.read_csv(ROOT / "data" / "articles.csv.gz", dtype={"ai_statement": str, "country": str},
                       keep_default_na=False, low_memory=False,
                       na_values={"received_year": [""], "received_month": [""]})
    res = pd.read_csv(ROOT / "data" / "results.csv.gz", dtype={"stat": str, "p_rep": str})  # keep trailing zeros
    print(f"articles={len(arts)} with_body={int(arts.has_body.sum())} results={len(res)} "
          f"articles_with_results={res.pmcid.nunique()}")

    yr = yearly(res, arts)
    yr.to_csv(OUT / "yearly.csv", index=False, float_format="%.3f")
    show = ["year", "articles", "articles_with_results", "results", "pct_results_inconsistent", "ci_lo", "ci_hi",
            "pct_results_decision", "dec_ci_lo", "dec_ci_hi", "pct_articles_any_inconsistent",
            "pct_articles_any_decision"]
    print(yr[show].round(2).to_string(index=False))

    # Variants of the definition and of the population.
    res["error_strict0"] = ((res.error_1t == 1) | (res.p_zero == 1)).astype(int)  # p = .000 counted wrong
    research = set(arts.pmcid[arts.article_type == "research-article"])
    variants = {
        "primary (one-tailed forgiven when article mentions it)": (res, "error_1t", "decision_error_1t"),
        "no one-tailed allowance": (res, "error", "decision_error"),
        "p = .000 counted as inconsistent": (res, "error_strict0", "decision_error_1t"),
        "exactly reported p only (p = ...)": (res[res.p_cmp == "="], "error_1t", "decision_error_1t"),
        "inequality p only (p < or >)": (res[res.p_cmp != "="], "error_1t", "decision_error_1t"),
        "article-type research-article only": (res[res.pmcid.isin(research)], "error_1t", "decision_error_1t"),
        "t and F tests only": (res[res.kind.isin(["t", "F"])], "error_1t", "decision_error_1t"),
        "one-tailed allowance without the word 'directional' (added post hoc)":
            (res, "error_1t_strict", "decision_error_1t_strict"),
        "excluding 2026 (incomplete year)": (res[res.year < 2026], "error_1t", "decision_error_1t"),
    }
    lines, vrows = [], []
    for name, (d, e, dcol) in variants.items():
        for label, col in (("inconsistent", e), ("decision", dcol)):
            orr, lo, hi, p = clustered_trend(d, col)
            first = d[d.year <= 2013][col].mean() * 100
            last = d[d.year >= 2023][col].mean() * 100
            vrows.append({"variant": name, "outcome": label, "n_results": len(d), "pct_2010_2013": first,
                          "pct_2023_2026": last, "odds_ratio_per_year": orr, "or_lo": lo, "or_hi": hi, "p": p})
            lines.append(f"{name:68s} {label:12s} n={len(d):7d}  2010-13 {first:5.2f}%  2023-26 {last:5.2f}%  "
                         f"OR/yr {orr:.4f} [{lo:.4f}, {hi:.4f}]  p={p:.2g}")
    pd.DataFrame(vrows).to_csv(OUT / "variants.csv", index=False, float_format="%.5f")

    # Article level: any inconsistency, adjusting for how many results the article reports.
    per = res.groupby(["pmcid", "year"]).agg(n=("error_1t", "size"), e=("error_1t", "sum"),
                                             d=("decision_error_1t", "sum")).reset_index()
    for span, pp in (("2010-2026", per), ("2010-2025", per[per.year <= 2025])):
        for label, col in (("any inconsistency", "e"), ("any decision inconsistency", "d")):
            X = sm.add_constant(pd.DataFrame({"year": pp.year - 2018, "log_n": np.log(pp.n)}))
            m = sm.Logit((pp[col] > 0).astype(int), X).fit(disp=0)
            ci = m.conf_int().loc["year"]
            lines.append(f"article level {span}, {label}, adjusted for log(number of results): OR/yr "
                         f"{np.exp(m.params['year']):.4f} [{np.exp(ci[0]):.4f}, {np.exp(ci[1]):.4f}] "
                         f"p={m.pvalues['year']:.2g}  (n articles = {len(pp)})")

    # Benchmark against Nuijten et al. (2016), Frontiers in Psychology 2010-2013: 12.8 %.
    res["error_raw0"] = ((res.error == 1) | (res.p_zero == 1)).astype(int)
    for name, ok in (("all article types", arts.pmcid), ("research-article only", arts.pmcid[arts.article_type == "research-article"])):
        early = res[(res.year <= 2013) & res.pmcid.isin(set(ok))]
        pe = early.groupby("pmcid").agg(n=("error_1t", "size"), e=("error_strict0", "sum"), e2=("error_1t", "sum"),
                                        e3=("error_raw0", "sum"))
        lines.append(f"benchmark 2010-2013, {name}: articles={int(((arts.year <= 2013) & arts.pmcid.isin(set(ok))).sum())} "
                     f"with results={len(pe)} results={len(early)} mean per-article % inconsistent: "
                     f"{100 * (pe.e2 / pe.n).mean():.2f} (primary), "
                     f"{100 * (pe.e / pe.n).mean():.2f} (one-tailed allowance, p=.000 counted wrong), "
                     f"{100 * (pe.e3 / pe.n).mean():.2f} (no allowance, p=.000 counted wrong)")
    # Second benchmark: Nuijten et al. (2017), Study 2. Research articles published March 2010 to
    # April 2015, split by received before / from March 2014; they report 13.1% and 16.2%.
    b2 = res.merge(arts[["pmcid", "epub_year", "epub_month", "received_year", "received_month", "article_type"]],
                   on="pmcid").dropna(subset=["received_year"])
    b2 = b2[(b2.article_type == "research-article") & (b2.epub_year * 12 + b2.epub_month <= 2015 * 12 + 4)]
    b2a = arts[(arts.article_type == "research-article") & (arts.epub_year * 12 + arts.epub_month <= 2015 * 12 + 4)
               & arts.received_year.notna()]
    for name, sel, sela in (
            ("received before March 2014", b2.received_year * 12 + b2.received_month < 2014 * 12 + 3,
             b2a.received_year * 12 + b2a.received_month < 2014 * 12 + 3),
            ("received from March 2014", b2.received_year * 12 + b2.received_month >= 2014 * 12 + 3,
             b2a.received_year * 12 + b2a.received_month >= 2014 * 12 + 3)):
        d = b2[sel]
        pe = d.groupby("pmcid").agg(n=("error", "size"), e=("error_1t", "sum"), e3=("error_raw0", "sum"),
                                    e2=("error_strict0", "sum"), g=("decision_error", "sum"))
        lines.append(f"benchmark Nuijten 2017 split, {name}: research articles={int(sela.sum())} with results={len(pe)} "
                     f"results={len(d)} mean per-article % inconsistent: {100 * (pe.e / pe.n).mean():.2f} (primary), "
                     f"{100 * (pe.e2 / pe.n).mean():.2f} (one-tailed allowance, p=.000 counted wrong), "
                     f"{100 * (pe.e3 / pe.n).mean():.2f} (no allowance, p=.000 counted wrong); "
                     f"mean per-article % decision, no allowance: {100 * (pe.g / pe.n).mean():.2f}")
    (OUT / "trend.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    # ---- Added after the yearly table was first seen (post hoc; see README) ----
    # (a) the same table without the one-tailed allowance
    y2 = yearly(res, arts, "error", "decision_error")
    y2.to_csv(OUT / "yearly_no_one_tailed_allowance.csv", index=False, float_format="%.3f")
    # (b) half-years from 2023 by electronic publication date
    m = res.merge(arts[["pmcid", "epub_year", "epub_month", "one_tail_text"]], on="pmcid")
    m["half"] = m.epub_year.astype(int).astype(str) + "H" + np.where(m.epub_month <= 6, "1", "2")
    am = arts.assign(half=arts.epub_year.astype(int).astype(str) + "H" + np.where(arts.epub_month <= 6, "1", "2"))
    rng = np.random.default_rng(SEED + 1)
    hrows = []
    for h, d in m[m.epub_year >= 2023].groupby("half"):
        lo, hi = cluster_boot(d, "error_1t", rng)
        lo2, hi2 = cluster_boot(d, "error", rng)
        hrows.append({"half_year": h, "articles": int((am.half == h).sum()), "articles_with_results": d.pmcid.nunique(),
                      "results": len(d), "pct_inconsistent": 100 * d.error_1t.mean(), "ci_lo": 100 * lo,
                      "ci_hi": 100 * hi, "pct_inconsistent_no_allowance": 100 * d.error.mean(),
                      "na_ci_lo": 100 * lo2, "na_ci_hi": 100 * hi2, "pct_decision": 100 * d.decision_error_1t.mean(),
                      "pct_articles_mentioning_one_tailed_words": 100 * am[am.half == h].one_tail_text.mean(),
                      "pct_articles_one_tailed_or_one_sided_only": 100 * am[am.half == h].one_tail_strict.mean()})
    hy = pd.DataFrame(hrows)
    hy.to_csv(OUT / "half_years_2023_2026.csv", index=False, float_format="%.3f")
    print(hy.round(2).to_string(index=False))
    # (c) 2026 against 2023-2025, and the 2010-2025 trend, clustered on article
    post = []
    late = res[res.year >= 2023]
    for col in ("error_1t", "error", "decision_error_1t", "decision_error"):
        X = pd.DataFrame({"const": 1.0, "y2026": (late.year == 2026).astype(float)})
        g = sm.GLM(late[col], X, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": late.pmcid.astype("category").cat.codes})
        b, se = g.params["y2026"], g.bse["y2026"]
        post.append(f"2026 vs 2023-2025, {col}: {100 * late[late.year == 2026][col].mean():.2f}% vs "
                    f"{100 * late[late.year < 2026][col].mean():.2f}%, odds ratio {np.exp(b):.3f} "
                    f"[{np.exp(b - 1.96 * se):.3f}, {np.exp(b + 1.96 * se):.3f}] p={g.pvalues['y2026']:.2g}")
        orr, lo, hi, pv = clustered_trend(res[res.year <= 2025], col)
        post.append(f"trend 2010-2025, {col}: OR/yr {orr:.4f} [{lo:.4f}, {hi:.4f}] p={pv:.2g}")
    # (d) is the 2026 drop confined to one kind of test or one way of writing p?
    late = late.assign(group=np.where(late.year == 2026, "2026", "2023-2025"),
                       p_form=np.where(late.p_cmp == "=", "p = x", "p < x or p > x"))
    for key in ("kind", "p_form"):
        t = late.pivot_table(index=key, columns="group", values="error_1t", aggfunc=["size", "mean"])
        for k, row in t.iterrows():
            post.append(f"2026 drop by {key} = {k}: 2023-2025 {100 * row[('mean', '2023-2025')]:.2f}% of "
                        f"{int(row[('size', '2023-2025')])}; 2026 {100 * row[('mean', '2026')]:.2f}% of "
                        f"{int(row[('size', '2026')])}")
    for key in ("kind", "p_form"):
        for k, d in late.groupby(key):
            g = sm.GLM(d.error_1t, pd.DataFrame({"const": 1.0, "y2026": (d.year == 2026).astype(float)}),
                       family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": d.pmcid.astype("category").cat.codes})
            b, se = g.params["y2026"], g.bse["y2026"]
            post.append(f"2026 vs 2023-2025 odds ratio, {key} = {k}: {np.exp(b):.3f} "
                        f"[{np.exp(b - 1.96 * se):.3f}, {np.exp(b + 1.96 * se):.3f}]")

    # (e) by the date the manuscript was received (from the XML history), quarters from 2024
    cols = ["pmcid", "epub_year", "epub_month", "received_year", "received_month", "ai_statement"]
    mr = res.merge(arts[cols], on="pmcid", suffixes=("", "_a")).dropna(subset=["received_year"])
    mr["rq"] = (mr.received_year.astype(int).astype(str) + "Q"
                + ((mr.received_month.astype(int) - 1) // 3 + 1).astype(str))
    ar = arts.dropna(subset=["received_year"]).copy()
    ar["rq"] = (ar.received_year.astype(int).astype(str) + "Q"
                + ((ar.received_month.astype(int) - 1) // 3 + 1).astype(str))
    rng = np.random.default_rng(SEED + 2)
    qrows = []
    for q, d in mr[mr.received_year >= 2023].groupby("rq"):
        lo, hi = cluster_boot(d, "error_1t", rng)
        lo2, hi2 = cluster_boot(d, "error", rng)
        any_flag = d.groupby("pmcid").error.max()
        qrows.append({"received_quarter": q, "articles_published_so_far": int((ar.rq == q).sum()),
                      "articles_with_results": d.pmcid.nunique(), "results": len(d),
                      "pct_inconsistent": 100 * d.error_1t.mean(), "ci_lo": 100 * lo, "ci_hi": 100 * hi,
                      "pct_inconsistent_no_allowance": 100 * d.error.mean(), "na_ci_lo": 100 * lo2,
                      "na_ci_hi": 100 * hi2, "pct_decision_no_allowance": 100 * d.decision_error.mean(),
                      "pct_articles_any_inconsistent_no_allowance": 100 * any_flag.mean()})
    rq = pd.DataFrame(qrows)
    rq.to_csv(OUT / "received_quarters.csv", index=False, float_format="%.3f")
    print(rq.round(2).to_string(index=False))

    def rate(d, col="error"):
        if len(d) == 0:
            return "no results"
        lo, hi = cluster_boot(d, col, rng)
        return (f"{100 * d[col].mean():.2f}% [{100 * lo:.2f}, {100 * hi:.2f}] "
                f"({d.pmcid.nunique()} articles, {len(d)} results)")

    # (f) articles published July-November 2026, split by when they were received
    pub = mr[(mr.epub_year == 2026) & (mr.epub_month >= 7)]
    rmon = pub.received_year * 12 + pub.received_month
    for name, sel in (("received before April 2026", rmon < 2026 * 12 + 4),
                      ("received April-May 2026", (rmon >= 2026 * 12 + 4) & (rmon <= 2026 * 12 + 5)),
                      ("received June 2026 or later", rmon >= 2026 * 12 + 6)):
        post.append(f"published Jul-Nov 2026, {name}, no allowance: {rate(pub[sel])}")
    # (g) does a short received-to-published interval go with a lower rate in earlier years?
    mr["lag"] = (mr.epub_year * 12 + mr.epub_month) - (mr.received_year * 12 + mr.received_month)
    for a, b in ((2018, 2021), (2022, 2024)):
        d = mr[(mr.epub_year >= a) & (mr.epub_year <= b)]
        for name, sel in (("0-3 months", d.lag <= 3), ("4-5 months", (d.lag >= 4) & (d.lag <= 5)),
                          ("6-8 months", (d.lag >= 6) & (d.lag <= 8)), ("9+ months", d.lag >= 9)):
            post.append(f"published {a}-{b}, received-to-published {name}, no allowance: {rate(d[sel])}")
    # (h) by the article's generative-AI statement, half-years of publication from 2025
    mr["half"] = mr.epub_year.astype(int).astype(str) + "H" + np.where(mr.epub_month <= 6, "1", "2")
    for (h, st), d in mr[mr.epub_year >= 2025].groupby(["half", "ai_statement"]):
        post.append(f"published {h}, AI statement '{st or 'none'}', no allowance: {rate(d)}")
    for (q, st), d in mr[(mr.received_year == 2026)].groupby(["rq", "ai_statement"]):
        post.append(f"received {q}, AI statement '{st or 'none'}', no allowance: {rate(d)}")
    # ---- Added after a second quality-control review (post hoc) ----
    # (i) by month of receipt from January 2025
    mr["rm"] = mr.received_year.astype(int).astype(str) + "-" + mr.received_month.astype(int).astype(str).str.zfill(2)
    mrows = []
    for mth, d in mr[mr.received_year >= 2025].groupby("rm"):
        lo, hi = cluster_boot(d, "error", rng)
        mrows.append({"received_month": mth, "articles_with_results": d.pmcid.nunique(), "results": len(d),
                      "pct_inconsistent_no_allowance": 100 * d.error.mean(), "ci_lo": 100 * lo, "ci_hi": 100 * hi,
                      "pct_inconsistent": 100 * d.error_1t.mean()})
    pd.DataFrame(mrows).to_csv(OUT / "received_months.csv", index=False, float_format="%.3f")
    # (j) an earlier, smaller decline: received 2025Q2-2026Q1 against 2023Q1-2025Q1
    rmon_all = mr.received_year * 12 + mr.received_month
    d = mr[(rmon_all >= 2023 * 12 + 1) & (rmon_all <= 2026 * 12 + 3)]
    later = ((d.received_year * 12 + d.received_month) >= 2025 * 12 + 4).astype(float)
    for col in ("error", "error_1t"):
        g = sm.GLM(d[col], pd.DataFrame({"const": 1.0, "later": later}), family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": d.pmcid.astype("category").cat.codes})
        b, se = g.params["later"], g.bse["later"]
        post.append(f"received 2025Q2-2026Q1 vs 2023Q1-2025Q1, {col}: {100 * d[later == 1][col].mean():.2f}% vs "
                    f"{100 * d[later == 0][col].mean():.2f}%, odds ratio {np.exp(b):.3f} "
                    f"[{np.exp(b - 1.96 * se):.3f}, {np.exp(b + 1.96 * se):.3f}]")
    # (k) every receipt cohort restricted to articles published within 3 months of receipt,
    #     the only kind the newest cohorts can contain
    frows = []
    for q, d in mr[(mr.received_year >= 2022) & (mr.lag <= 3)].groupby("rq"):
        lo, hi = cluster_boot(d, "error", rng)
        frows.append({"received_quarter": q, "articles_with_results": d.pmcid.nunique(), "results": len(d),
                      "pct_inconsistent_no_allowance": 100 * d.error.mean(), "ci_lo": 100 * lo, "ci_hi": 100 * hi})
    fast = pd.DataFrame(frows)
    fast.to_csv(OUT / "received_quarters_fast.csv", index=False, float_format="%.3f")
    print(fast.round(2).to_string(index=False))
    # (l) composition: country of first affiliation, test type, repeated strings, by receipt period
    arm = ar.received_year * 12 + ar.received_month
    periods = (("received 2023-2024", 2023 * 12 + 1, 2024 * 12 + 12), ("received 2025Q1-2026Q1", 2025 * 12 + 1, 2026 * 12 + 3),
               ("received Apr-May 2026", 2026 * 12 + 4, 2026 * 12 + 5), ("received Jun 2026 on", 2026 * 12 + 6, 9e9))
    mr = mr.merge(arts[["pmcid", "country"]], on="pmcid")
    mr["group"] = np.where(mr.country == "China", "China", np.where(mr.country == "United States", "United States",
                                                                    "all other countries"))
    key = ["pmcid", "kind", "df1", "df2", "stat", "p_cmp", "p_rep"]
    mr["repeat"] = mr.duplicated(key, keep="first")
    rmon_all = mr.received_year * 12 + mr.received_month
    for name, a, b in periods:
        d = mr[(rmon_all >= a) & (rmon_all <= b)]
        aa = ar[(arm >= a) & (arm <= b)]
        post.append(f"{name}: articles {len(aa)}, first affiliation in China {100 * (aa.country == 'China').mean():.1f}%; "
                    f"of results, chi-square {100 * (d.kind == 'chi2').mean():.1f}%, repeated strings "
                    f"{100 * d.repeat.mean():.1f}%; rate excluding repeated strings, no allowance: "
                    f"{100 * d[~d.repeat].error.mean():.2f}%")
        for grp, dd in d.groupby("group"):
            post.append(f"{name}, {grp}, no allowance: {rate(dd)}")
    # (m) share of articles declaring generative-AI use, by receipt quarter (articles with results)
    for q, d in mr[mr.received_year >= 2025].drop_duplicates("pmcid").groupby("rq"):
        st = d.ai_statement
        post.append(f"received {q}: of {len(d)} articles with results, {100 * (st == 'used').mean():.1f}% declare "
                    f"generative AI used, {100 * (st == 'not_used').mean():.1f}% not used, "
                    f"{100 * (~st.isin(['used', 'not_used'])).mean():.1f}% no or other statement")
    # (n) are consistent p-values now exact recomputations of the printed statistic? Among consistent
    #     "p = x" results with three decimals whose rounding range spans more than one three-decimal value,
    #     the share whose p equals the one computed from the printed statistic taken at face value.
    c3 = mr[(mr.error == 0) & (mr.p_cmp == "=") & (mr.p_rep.str.split(".").str[1].str.len() == 3)
            & (mr.p_min.round(3) != mr.p_max.round(3))].copy()
    c3["p_face"] = [_p(k, abs(float(x)), a if a == a else None, b if b == b else None)
                    for k, x, a, b in zip(c3.kind, c3.stat, c3.df1, c3.df2)]
    c3["exact"] = (c3.p_face.round(3) - c3.p_rep.astype(float)).abs() < 5e-4
    cm = c3.received_year * 12 + c3.received_month
    for name, a, b in periods:
        d = c3[(cm >= a) & (cm <= b)]
        post.append(f"{name}: consistent three-decimal 'p =' results that match the face-value p exactly: "
                    f"{100 * d.exact.mean():.1f}% of {len(d)}")
    # (o) how far off are flagged "p = x" results?
    fl = res[(res.error == 1) & (res.p_cmp == "=")]
    dec = fl.p_rep.str.split(".").str[1].str.len()
    unit = 10.0 ** (-dec)
    pr = fl.p_rep.astype(float)
    near = (pr - 1.5 * unit <= fl.p_max) & (pr + 1.5 * unit >= fl.p_min)
    trunc = (pr <= fl.p_max) & (pr + unit >= fl.p_min)
    post.append(f"flagged 'p =' results ({len(fl)}): {100 * near.mean():.1f}% are within one further unit of the last "
                f"printed digit; {100 * trunc.mean():.1f}% would be consistent if p had been truncated, not rounded")

    # ---- Added after a third quality-control review (post hoc) ----
    # (p) the pooled 2010-2025 trend split by how p is written
    r25 = res[res.year <= 2025]
    for form, d in (("p = x", r25[r25.p_cmp == "="]), ("p < x or p > x", r25[r25.p_cmp != "="])):
        for col in ("error_1t", "error"):
            orr, lo, hi, pv = clustered_trend(d, col)
            post.append(f"trend 2010-2025, {form} only, {col}: OR/yr {orr:.4f} [{lo:.4f}, {hi:.4f}] p={pv:.2g}")
    # (q) where the decline begins: April-May and June-on receipts against 2025Q2-2026Q1
    rmon_all = mr.received_year * 12 + mr.received_month
    base = (rmon_all >= 2025 * 12 + 4) & (rmon_all <= 2026 * 12 + 3)
    for name, sel in (("received Apr-May 2026", (rmon_all >= 2026 * 12 + 4) & (rmon_all <= 2026 * 12 + 5)),
                      ("received Jun 2026 on", rmon_all >= 2026 * 12 + 6)):
        d = mr[base | sel]
        x = sel[d.index].astype(float)
        g = sm.GLM(d.error, pd.DataFrame({"const": 1.0, "x": x}), family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": d.pmcid.astype("category").cat.codes})
        b, se = g.params["x"], g.bse["x"]
        post.append(f"{name} vs received 2025Q2-2026Q1, no allowance: {100 * d[x == 1].error.mean():.2f}% vs "
                    f"{100 * d[x == 0].error.mean():.2f}%, odds ratio {np.exp(b):.3f} "
                    f"[{np.exp(b - 1.96 * se):.3f}, {np.exp(b + 1.96 * se):.3f}]")
    # (r) by test type: received June 2026 on against received 2023-2024
    old = (rmon_all >= 2023 * 12 + 1) & (rmon_all <= 2024 * 12 + 12)
    new = rmon_all >= 2026 * 12 + 6
    for k, d in mr[old | new].groupby("kind"):
        x = new[d.index].astype(float)
        if d[x == 1].error.sum() == 0:
            post.append(f"kind = {k}, received Jun 2026 on vs 2023-2024, no allowance: 0 flagged of {int(x.sum())} vs "
                        f"{100 * d[x == 0].error.mean():.2f}% of {int((1 - x).sum())}; odds ratio not estimated")
            continue
        g = sm.GLM(d.error, pd.DataFrame({"const": 1.0, "x": x}), family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": d.pmcid.astype("category").cat.codes})
        b, se = g.params["x"], g.bse["x"]
        post.append(f"kind = {k}, received Jun 2026 on vs 2023-2024, no allowance: {100 * d[x == 1].error.mean():.2f}% "
                    f"of {int(x.sum())} vs {100 * d[x == 0].error.mean():.2f}% of {int((1 - x).sum())}, odds ratio "
                    f"{np.exp(b):.3f} [{np.exp(b - 1.96 * se):.3f}, {np.exp(b + 1.96 * se):.3f}]")
    # (s) within the 2026 cohorts, do manuscripts published fast differ from slower ones?
    for name, lo_m, hi_m in (("received Apr-May 2026", 2026 * 12 + 4, 2026 * 12 + 5), ("received Jun 2026", 2026 * 12 + 6, 2026 * 12 + 6)):
        d = mr[(rmon_all >= lo_m) & (rmon_all <= hi_m)]
        post.append(f"{name}, published within 3 months, no allowance: {rate(d[d.lag <= 3])}")
        post.append(f"{name}, published after 4 or more months, no allowance: {rate(d[d.lag >= 4])}")
    late_a = ar[(arm >= 2026 * 12 + 6)]
    post.append(f"received Jun 2026 on: median body length {late_a.body_chars.median():.0f} characters "
                f"({len(late_a)} articles)")

    # Descriptive numbers quoted in the README
    desc = [f"article types: {arts.article_type.value_counts().to_dict()}"]
    mism = (arts.year != arts.epub_year).groupby(arts.year).mean()
    desc.append("share of articles whose PUB_YEAR differs from the electronic publication year, by PUB_YEAR: "
                + ", ".join(f"{k}: {100 * x:.1f}%" for k, x in mism.items()))
    desc.append(f"articles with electronic publication year 2026: {int((arts.epub_year == 2026).sum())}; of these with "
                f"PUB_YEAR 2025: {int(((arts.epub_year == 2026) & (arts.year == 2025)).sum())}; published November "
                f"2026: {int(((arts.epub_year == 2026) & (arts.epub_month == 11)).sum())}")
    e26 = arts[arts.epub_year == 2026]
    desc.append(f"articles published 2026 with a generative-AI statement of either kind: "
                f"{100 * e26.ai_statement.isin(['used', 'not_used']).mean():.1f}%")
    desc.append(f"articles without a received date: {int(arts.received_year.isna().sum())}; "
                f"without a first-affiliation country: {int((arts.country == '').sum())}")
    nores = 1 - (arts.n_results > 0).groupby(arts.year).mean()
    desc.append(f"share of articles with no extracted result: overall {100 * (arts.n_results == 0).mean():.1f}%; by year: "
                + ", ".join(f"{k}: {100 * x:.1f}%" for k, x in nores.items()))
    fsw = res[(res.kind == "F") & (res.df1 > res.df2)]
    desc.append(f"F results with df1 > df2: {len(fsw)}, flagged (no allowance) {100 * fsw.error.mean():.1f}%")
    tl = res[(res.kind == "t") & (res.df2 < 3)]
    desc.append(f"t results with df < 3: {len(tl)}, flagged (no allowance) {100 * tl.error.mean():.1f}%")
    dc = res[res.year <= 2025].groupby("year").decision_error_1t.sum()
    desc.append(f"decision inconsistencies per year 2010-2025 (primary): min {dc.min()}, max {dc.max()}")
    desc.append("median body length in characters by year: "
                + ", ".join(f"{k}: {x:.0f}" for k, x in arts.groupby("year").body_chars.median().items()))
    three = (res.p_rep.str.split(".").str[1].str.len() == 3).groupby(res.year).mean()
    desc.append("share of results whose p is printed with exactly three decimals, by year: "
                + ", ".join(f"{k}: {100 * x:.1f}%" for k, x in three.items()))
    desc.append("median extracted results per article with results, by year: "
                + ", ".join(f"{r.year}: {r.median_results_per_article:.0f}" for r in yr.itertuples()))
    ctx = ROOT / "data" / "raw" / "contexts.csv.gz"
    if ctx.exists():  # needs the downloaded article text; otherwise the committed file is left as it is
        c = pd.read_csv(ctx)
        z = c[c.kind == "z"]
        norm = z.context.str.contains("Kolmogorov|Shapiro|normality", case=False)
        (OUT / "descriptives_from_text.txt").write_text(
            f"z results: {len(z)}, flagged (no allowance) {int(z.error.sum())}; with Kolmogorov / Shapiro / "
            f"'normality' within 150 characters: {int(norm.sum())}, of which flagged {int(z[norm].error.sum())}\n")
    # hand-check tallies from the recorded labels
    hc = pd.read_csv(OUT / "handcheck.csv", dtype=str, keep_default_na=False)
    pd.crosstab([hc.stratum, hc.period], hc.label).to_csv(OUT / "handcheck_summary.csv")
    fl_s = hc[hc.stratum == "flagged"]
    desc.append(f"hand-check: {len(hc)} items; by stratum and label: "
                f"{pd.crosstab(hc.stratum, hc.label).to_dict('index')}")
    desc.append(f"hand-check: items in the 'flagged' stratum that are decision inconsistencies: "
                f"{int((fl_s.decision_flag == '1').sum())} of {len(fl_s)}; distinct non-empty notes: "
                f"{hc.note[hc.note != ''].nunique()}")
    other = (hc.label != "inconsistent_as_printed") | hc.note.str.startswith(
        ("neighbouring", "the printed value may", "degrees of freedom"))
    for st in ("flagged", "flagged_decision"):
        d = hc[hc.stratum == st]
        desc.append(f"hand-check, {st}: {len(d)} items, {int((d.label == 'inconsistent_as_printed').sum())} labelled "
                    f"inconsistent as printed, {int(other[d.index].sum())} with a label or note pointing to something "
                    f"other than a wrong number")
    a20 = arts[arts.year <= 2020]
    desc.append(f"PUB_YEAR 2010-2020: {len(a20)} articles, {int((a20.n_results > 0).sum())} with results "
                f"({100 * (a20.n_results > 0).mean():.0f}%), {int((res.year <= 2020).sum())} results")
    desc.append(f"flagged z results: {int(res[res.kind == 'z'].error.sum())} without the one-tailed allowance, "
                f"{int(res[res.kind == 'z'].error_1t.sum())} with it, of {int((res.kind == 'z').sum())}")
    ex = (res.p_cmp == "=").groupby(res.year).mean()
    desc.append("share of results with exactly reported p (p = x), by year: "
                + ", ".join(f"{k}: {100 * x:.1f}%" for k, x in ex.items()))
    for form, d in (("p = x", res[res.p_cmp == "="]), ("p < x or p > x", res[res.p_cmp != "="])):
        byy = d.groupby("year").error.mean()
        desc.append(f"rate (no allowance) for {form}: 2010 {100 * byy[2010]:.1f}%, 2025 {100 * byy[2025]:.1f}%, "
                    f"2026 {100 * byy[2026]:.1f}%")
    (OUT / "descriptives.txt").write_text("\n".join(desc) + "\n")
    print("\n".join(desc))
    (OUT / "post_hoc.txt").write_text("\n".join(post) + "\n")
    print("\n".join(post))

    bk = res.groupby(["kind"]).agg(results=("error_1t", "size"), pct_inconsistent=("error_1t", "mean"),
                                   pct_decision=("decision_error_1t", "mean")).reset_index()
    bk[["pct_inconsistent", "pct_decision"]] *= 100
    bk.to_csv(OUT / "by_kind.csv", index=False, float_format="%.3f")
    print(bk.round(2).to_string(index=False))

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for a, (c, lo, hi, t) in zip(ax, [("pct_results_inconsistent", "ci_lo", "ci_hi", "Inconsistent p-values"),
                                      ("pct_results_decision", "dec_ci_lo", "dec_ci_hi",
                                       "Decision inconsistencies (verdict at .05 changes)")]):
        a.fill_between(yr.year, yr[lo], yr[hi], alpha=0.25, color="#3b6ea8", linewidth=0)
        a.plot(yr.year, yr[c], "-", color="#3b6ea8")
        a.plot(yr.year[:-1], yr[c][:-1], "o", color="#3b6ea8")
        a.plot(yr.year[-1:], yr[c][-1:], "o", mfc="white", color="#3b6ea8")
        a.annotate("2026: to early\nNovember only", (2026, yr[c].iloc[-1]), xytext=(-8, -30),
                   textcoords="offset points", ha="right", fontsize=8)
        a.set_ylim(0, None)
        a.set_xlabel("Publication year")
        a.set_ylabel("% of extracted results")
        a.set_title(t, fontsize=10)
        a.grid(alpha=0.3)
    fig.suptitle("Frontiers in Psychology, 2010-2026: share of extracted test results whose p-value does not match\n"
                 "(band: 95% interval from resampling articles)", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "trend.png", dpi=150)


if __name__ == "__main__":
    main()
