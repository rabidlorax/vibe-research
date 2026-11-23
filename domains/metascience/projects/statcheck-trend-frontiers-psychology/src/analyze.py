#!/usr/bin/env python3
"""Yearly rates of statistical reporting inconsistencies and their trend.

Reads data/articles.csv.gz and data/results.csv.gz (written by extract.py) and
writes results/yearly.csv, results/variants.csv, results/trend.txt,
results/by_kind.csv and results/trend.png.

Usage: python src/analyze.py        (about 2 minutes; seed fixed)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

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


def gee_trend(res, col, extra=None):
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
    arts = pd.read_csv(ROOT / "data" / "articles.csv.gz")
    res = pd.read_csv(ROOT / "data" / "results.csv.gz", dtype={"stat": str, "p_rep": str})
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
        "excluding 2026 (incomplete year)": (res[res.year < 2026], "error_1t", "decision_error_1t"),
    }
    lines, vrows = [], []
    for name, (d, e, dcol) in variants.items():
        for label, col in (("inconsistent", e), ("decision", dcol)):
            orr, lo, hi, p = gee_trend(d, col)
            first = d[d.year <= 2013][col].mean() * 100
            last = d[d.year >= 2023][col].mean() * 100
            vrows.append({"variant": name, "outcome": label, "n_results": len(d), "pct_2010_2013": first,
                          "pct_2023_2026": last, "odds_ratio_per_year": orr, "or_lo": lo, "or_hi": hi, "p": p})
            lines.append(f"{name:55s} {label:12s} n={len(d):7d}  2010-13 {first:5.2f}%  2023-26 {last:5.2f}%  "
                         f"OR/yr {orr:.4f} [{lo:.4f}, {hi:.4f}]  p={p:.2g}")
    pd.DataFrame(vrows).to_csv(OUT / "variants.csv", index=False, float_format="%.5f")

    # Article level: any inconsistency, adjusting for how many results the article reports.
    per = res.groupby(["pmcid", "year"]).agg(n=("error_1t", "size"), e=("error_1t", "sum"),
                                             d=("decision_error_1t", "sum")).reset_index()
    for label, col in (("any inconsistency", "e"), ("any decision inconsistency", "d")):
        X = sm.add_constant(pd.DataFrame({"year": per.year - 2018, "log_n": np.log(per.n)}))
        m = sm.Logit((per[col] > 0).astype(int), X).fit(disp=0)
        ci = m.conf_int().loc["year"]
        lines.append(f"article level, {label}, adjusted for log(number of results): OR/yr "
                     f"{np.exp(m.params['year']):.4f} [{np.exp(ci[0]):.4f}, {np.exp(ci[1]):.4f}] "
                     f"p={m.pvalues['year']:.2g}  (n articles = {len(per)})")

    # Benchmark against Nuijten et al. (2016), Frontiers in Psychology 2010-2013: 12.8 %.
    early = res[res.year <= 2013]
    pe = early.groupby("pmcid").agg(n=("error_1t", "size"), e=("error_strict0", "sum"), e2=("error_1t", "sum"))
    lines.append(f"benchmark 2010-2013: articles={arts[arts.year <= 2013].shape[0]} with results={len(pe)} "
                 f"results={len(early)} mean per-article % inconsistent: {100 * (pe.e / pe.n).mean():.2f} "
                 f"(p=.000 wrong, statcheck-2016 convention), {100 * (pe.e2 / pe.n).mean():.2f} (primary)")
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
                      "pct_articles_mentioning_one_tailed_words": 100 * am[am.half == h].one_tail_text.mean()})
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
        orr, lo, hi, pv = gee_trend(res[res.year <= 2025], col)
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
        a.plot(yr.year, yr[c], "o-", color="#3b6ea8")
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
