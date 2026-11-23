#!/usr/bin/env python3
"""Internal-consistency audit of the NASA Exoplanet Archive `ps` table.

For each identity, compares a tabulated value ("obs") with the value implied
by other columns of the same row ("pred"). d = ln(obs/pred). "Off by more
than x%" means |d| > ln(1 + x/100), i.e. a factor of more than 1 + x/100 in
either direction. Where every
input has a reported two-sided uncertainty, z = d / sigma with sigma from
first-order propagation assuming independent errors.

Usage: python src/audit.py [path/to/ps.csv]
Writes results/summary.csv, results/summary.md, results/outliers.csv,
results/discrepancy_histograms.png. Uses no randomness.
"""
import hashlib
import html
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent
CSV = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "data" / "raw" / "ps.csv"

# IAU 2015 Resolution B3 nominal values and CODATA 2018 G (SI).
G = 6.67430e-11
GM_SUN, GM_EARTH, GM_JUP = 1.3271244e20, 3.986004e14, 1.2668653e17
R_SUN, R_EARTH, R_JUP = 6.957e8, 6.3781e6, 7.1492e7   # equatorial nominal
AU, DAY, TEFF_SUN = 1.495978707e11, 86400.0, 5772.0
LOGG_SUN = np.log10(GM_SUN / R_SUN**2 * 100)                      # cgs
RHO_SUN = GM_SUN / G / (4 / 3 * np.pi * R_SUN**3) / 1000          # g/cm^3
RHO_EARTH = GM_EARTH / G / (4 / 3 * np.pi * R_EARTH**3) / 1000    # g/cm^3
LN10 = np.log(10)


def val(d, c):
    """Column c with limit-flagged values removed (positivity is enforced by pos())."""
    v = d[c].where(d[c + "lim"].fillna(0) == 0)
    return v


def rel(d, c):
    """Symmetrised fractional 1-sigma error of column c (NaN if not given)."""
    e = (d[c + "err1"].abs() + d[c + "err2"].abs()) / 2
    return (e / d[c].abs()).where(e > 0)


def absd(d, c):
    """Symmetrised absolute error, for columns that are already logarithms."""
    e = (d[c + "err1"].abs() + d[c + "err2"].abs()) / 2
    return e.where(e > 0)


def pos(*xs):
    m = np.ones(len(xs[0]), bool)
    for x in xs:
        m &= (x > 0).to_numpy()
    return m


def checks(d):
    """Yield (id, description, obs-column, mask, d, sigma, cross_ref, exactness)."""
    P, a, Ms, Rs = val(d, "pl_orbper"), val(d, "pl_orbsmax"), val(d, "st_mass"), val(d, "st_rad")
    Teff, logg, rho_s, lum = val(d, "st_teff"), val(d, "st_logg"), val(d, "st_dens"), val(d, "st_lum")
    Re, Rj, Me, Mj = val(d, "pl_rade"), val(d, "pl_radj"), val(d, "pl_masse"), val(d, "pl_massj")
    rho_p, k, aR = val(d, "pl_dens"), val(d, "pl_ratror"), val(d, "pl_ratdor")
    dep, S = val(d, "pl_trandep"), val(d, "pl_insol")

    # K3: Kepler's third law, planet mass neglected, circumbinary rows excluded.
    pred = (GM_SUN * Ms * (P * DAY) ** 2 / (4 * np.pi**2)) ** (1 / 3) / AU
    m = pos(P, a, Ms) & (d.cb_flag == 0).to_numpy()
    sig = np.sqrt(rel(d, "pl_orbsmax") ** 2 + (rel(d, "st_mass") / 3) ** 2 + (2 * rel(d, "pl_orbper") / 3) ** 2)
    yield "K3", "a vs (G M* P^2 / 4 pi^2)^(1/3)", "pl_orbsmax", m, np.log(a / pred), sig, True, "exact up to planet mass"

    # LOGG: surface gravity from mass and radius.
    pred = LOGG_SUN + np.log10(Ms) - 2 * np.log10(Rs)
    m = pos(Ms, Rs) & logg.notna().to_numpy()
    sig = np.sqrt((absd(d, "st_logg") * LN10) ** 2 + rel(d, "st_mass") ** 2 + (2 * rel(d, "st_rad")) ** 2)
    yield "LOGG", "log g vs log(G M*/R*^2)", "st_logg", m, (logg - pred) * LN10, sig, False, "exact"

    # RHOS: mean stellar density.
    pred = RHO_SUN * Ms / Rs**3
    m = pos(Ms, Rs, rho_s)
    sig = np.sqrt(rel(d, "st_dens") ** 2 + rel(d, "st_mass") ** 2 + (3 * rel(d, "st_rad")) ** 2)
    yield "RHOS", "rho* vs 3 M*/(4 pi R*^3)", "st_dens", m, np.log(rho_s / pred), sig, False, "exact"

    # LUM: Stefan-Boltzmann.
    pred = 2 * np.log10(Rs) + 4 * np.log10(Teff / TEFF_SUN)
    m = pos(Rs, Teff) & lum.notna().to_numpy()
    sig = np.sqrt((absd(d, "st_lum") * LN10) ** 2 + (2 * rel(d, "st_rad")) ** 2 + (4 * rel(d, "st_teff")) ** 2)
    yield "LUM", "log L* vs log(R*^2 Teff^4)", "st_lum", m, (lum - pred) * LN10, sig, False, "exact"

    # RHOP: planet bulk density (true masses only).
    pred = RHO_EARTH * Me / Re**3
    m = pos(Me, Re, rho_p)
    sig = np.sqrt(rel(d, "pl_dens") ** 2 + rel(d, "pl_masse") ** 2 + (3 * rel(d, "pl_rade")) ** 2)
    yield "RHOP", "rho_p vs 3 M_p/(4 pi R_p^3)", "pl_dens", m, np.log(rho_p / pred), sig, False, "exact"

    # Unit pairs.
    m = pos(Re, Rj)
    yield "URAD", "R_p[Earth] vs R_p[Jup] x R_J/R_E", "pl_rade", m, np.log(Re / (Rj * R_JUP / R_EARTH)), None, False, "exact"
    m = pos(Me, Mj)
    yield "UMASS", "M_p[Earth] vs M_p[Jup] x M_J/M_E", "pl_masse", m, np.log(Me / (Mj * GM_JUP / GM_EARTH)), None, False, "exact"
    msie, msij = val(d, "pl_msinie"), val(d, "pl_msinij")
    m = pos(msie, msij)
    yield "UMSINI", "M sin i [Earth] vs [Jup] x M_J/M_E", "pl_msinie", m, np.log(msie / (msij * GM_JUP / GM_EARTH)), None, False, "exact"

    # RATROR: radius ratio.
    pred = Re * R_EARTH / (Rs * R_SUN)
    m = pos(Re, Rs, k)
    sig = np.sqrt(rel(d, "pl_ratror") ** 2 + rel(d, "pl_rade") ** 2 + rel(d, "st_rad") ** 2)
    yield "RATROR", "Rp/R* vs R_p / R*", "pl_ratror", m, np.log(k / pred), sig, True, "exact"

    # RATDOR: scaled semi-major axis.
    pred = a * AU / (Rs * R_SUN)
    m = pos(a, Rs, aR)
    sig = np.sqrt(rel(d, "pl_ratdor") ** 2 + rel(d, "pl_orbsmax") ** 2 + rel(d, "st_rad") ** 2)
    yield "RATDOR", "a/R* vs a / R*", "pl_ratdor", m, np.log(aR / pred), sig, True, "exact"

    # DEPTH: transit depth vs squared radius ratio (limb darkening and grazing
    # geometry make this approximate: tens of per cent is expected).
    pred = 100 * k**2
    m = pos(k, dep)
    sig = np.sqrt(rel(d, "pl_trandep") ** 2 + (2 * rel(d, "pl_ratror")) ** 2)
    yield "DEPTH", "depth[%] vs 100 (Rp/R*)^2", "pl_trandep", m, np.log(dep / pred), sig, False, "approximate"

    # INSOL: insolation from luminosity and semi-major axis (circular-orbit value).
    pred = 10**lum / a**2
    m = pos(a, S) & lum.notna().to_numpy()
    sig = np.sqrt(rel(d, "pl_insol") ** 2 + (absd(d, "st_lum") * LN10) ** 2 + (2 * rel(d, "pl_orbsmax")) ** 2)
    yield "INSOL", "S vs L*/a^2", "pl_insol", m, np.log(S / pred), sig, True, "exact for circular orbits"


def source_class(s):
    if s.startswith("Published"):
        return "published"
    if s.startswith("Kepler"):
        return "kepler-koi"
    return "tess-exofop"


def refshort(col):
    return col.str.extract(r">\s*([^<]+?)\s*</a>")[0].fillna(col).map(html.unescape, na_action="ignore")


def refkey(col):
    """Short name plus ADS bibcode. The short name alone is not unique:
    several hundred of them (e.g. "Mann et al. 2017") stand for 2+ papers."""
    short = refshort(col)
    bib = col.str.extract(r"/abs/([^/\s]+)/abstract")[0].str.replace("%26", "&")
    return (short + " [" + bib + "]").where(bib.notna(), short)


STELLAR = ("LOGG", "RHOS", "LUM")
# References whose st_dens values are in solar units (see density_units.py).
SOLAR_UNIT_BIBCODES = ("2018AJ....156..264F", "2017AJ....154..264T", "2016AJ....152..105M", "2017AJ....153..267M")
THR = [("gt1pct", np.log(1.01)), ("gt5pct", np.log(1.05)), ("gt20pct", np.log(1.20)), ("gt2x", np.log(2.0))]


def main():
    raw = CSV.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    d = pd.read_csv(CSV, low_memory=False)
    d = pd.concat([d, pd.DataFrame({
        "cls": d.soltype.map(source_class), "pl_ref": refkey(d.pl_refname),
        "st_ref": refkey(d.st_refname), "same_ref": d.pl_refname == d.st_refname})], axis=1)
    solar_ref = d.st_ref.str.extract(r"\[(.+)\]$")[0].isin(SOLAR_UNIT_BIBCODES)
    catalogue_star = d.st_ref.str.contains("KOI Table|TICv8", na=False)
    rows, outl, byref, hist, comp, tic_viol = [], [], [], {}, {}, {}
    with np.errstate(all="ignore"):
        for cid, desc, obscol, m, dd, sig, cross, exact in checks(d):
            dd = pd.Series(np.asarray(dd, float), index=d.index)
            z = dd / sig if sig is not None else pd.Series(np.nan, index=d.index)
            m = m & np.isfinite(dd.to_numpy())
            # A cross-reference identity is only a test of one parameter set
            # when planet and star values cite the same reference.
            strata = [("published", (d.cls == "published"))]
            if cross:
                strata = [("published, same ref", (d.cls == "published") & d.same_ref),
                          ("published, mixed refs", (d.cls == "published") & ~d.same_ref)]
            if cid in STELLAR:
                # Published planet rows can carry stellar values from TICv8
                # (consistent by construction) or from a Kepler KOI table
                # (density is the transit-fitted koi_srho). The literature
                # stratum drops both and, for density, the references whose
                # values are in solar units (see density_units.py).
                lit = (d.cls == "published") & ~catalogue_star
                if cid == "RHOS":
                    lit &= ~solar_ref
                strata.append(("published, literature star ref", lit))
            strata.append(("kepler-koi", d.cls == "kepler-koi"))
            if cid in STELLAR:
                # KOI rows of the DR25 Supplemental table take their stellar
                # values from TICv8, so split by where the star comes from.
                strata.append(("kepler-koi, KOI-table star ref",
                               (d.cls == "kepler-koi") & d.st_ref.str.contains("KOI Table", na=False)))
                strata.append(("kepler-koi, TICv8 star ref",
                               (d.cls == "kepler-koi") & d.st_ref.str.contains("TICv8", na=False)))
            strata.append(("tess-exofop", d.cls == "tess-exofop"))
            for sname, sm in strata:
                sel = m & sm.to_numpy()
                x, zz = dd[sel], z[sel]
                if len(x) == 0:
                    continue
                zok = zz.notna()
                r = {"check": cid, "identity": desc, "exactness": exact, "stratum": sname, "n": len(x),
                     "median_abs_pct": round(100 * np.expm1(x.abs().median()), 3)}
                for name, t in THR:
                    r["n_" + name] = int((x.abs() > t).sum())
                    r["pct_" + name] = round(100 * (x.abs() > t).mean(), 2)
                r["n_with_errors"] = int(zok.sum())
                sig3 = zok & (zz.abs() > 3) & (x.abs() > np.log(1.05))
                r["n_gt3sigma_and_gt5pct"] = int(sig3.sum())
                r["pct_gt3sigma_and_gt5pct"] = round(100 * sig3.sum() / max(zok.sum(), 1), 2)
                # Which reference contributes most of the > 5% rows.
                refcol = d.loc[x.index, "st_ref" if cid in STELLAR else "pl_ref"]
                vc = refcol[x.abs() > np.log(1.05)].value_counts()
                for i in range(min(2, len(vc))):
                    r[f"top{i + 1}_ref_gt5pct"] = vc.index[i]
                    r[f"top{i + 1}_ref_n_gt5pct"] = int(vc.iloc[i])
                    r[f"top{i + 1}_ref_rows_in_stratum"] = int((refcol == vc.index[i]).sum())
                if cid in STELLAR and sname == "published":
                    comp[cid] = refcol.value_counts().head(4)
                    tic = refcol.str.contains("TICv8", na=False)
                    tic_viol[cid] = (int(tic.sum()), int((tic & (x.abs() > np.log(1.05))).sum()))
                rows.append(r)
                if sname in ("published", "published, same ref"):
                    hist[cid] = (x.to_numpy(), desc)
                    o = d.loc[x.index, ["pl_name", "default_flag", "pl_ref", "st_ref", "pl_pubdate"]].copy()
                    o.insert(0, "check", cid)
                    o["obs_column"], o["obs"] = obscol, d.loc[x.index, obscol]
                    o["ratio_obs_over_pred"] = np.exp(x).round(5)
                    o["z"] = zz.round(2)
                    outl.append(o[x.abs() > np.log(1.20)])
                    # Per-reference offsets: a whole reference displaced by a
                    # constant factor points at a unit or definition problem.
                    ref = d.loc[x.index, "st_ref" if cid in STELLAR else "pl_ref"]
                    g = pd.DataFrame({"ref": ref, "d": x}).groupby("ref").d
                    b = pd.DataFrame({"n_rows": g.size(), "median_ratio": np.exp(g.median()).round(4),
                                      "q25_ratio": np.exp(g.quantile(.25)).round(4),
                                      "q75_ratio": np.exp(g.quantile(.75)).round(4)}).reset_index()
                    b.insert(0, "check", cid)
                    byref.append(b[(b.n_rows >= 5) & (np.log(b.median_ratio).abs() > np.log(1.10))])
    res = HERE / "results"
    summ = pd.DataFrame(rows)
    summ.to_csv(res / "summary.csv", index=False)
    out = pd.concat(outl)
    n_distinct_rows = out.index.nunique()
    out["absln"] = np.log(out.ratio_obs_over_pred).abs()
    out = out.sort_values(["check", "absln", "pl_name"], ascending=[True, False, True]).drop(columns="absln")
    out.to_csv(res / "outliers.csv", index=False)

    br = pd.concat(byref).sort_values(["check", "n_rows"], ascending=[True, False])
    br.to_csv(res / "by_reference.csv", index=False)

    cols = ["check", "stratum", "n", "median_abs_pct", "pct_gt1pct", "pct_gt5pct", "pct_gt20pct", "n_gt20pct",
            "n_gt2x", "n_with_errors", "n_gt3sigma_and_gt5pct", "pct_gt3sigma_and_gt5pct"]
    lines = [f"Input: {CSV.name}, sha256 {sha}, {len(d)} rows, {d.pl_name.nunique()} planets.", "",
             "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in summ.iterrows():
        v = [str(r[c]) for c in cols]
        if r.n_with_errors == 0:  # no z statistic without errors
            v[-2:] = ["n/a", "n/a"]
        lines.append("| " + " | ".join(v) + " |")
    lines += ["", "Two references contributing most rows off by > 5%, per stratum "
              "(count of the stratum's > 5% rows / that reference's rows in the stratum):", ""]
    for _, r in summ.iterrows():
        parts = [f"{r[f'top{i}_ref_gt5pct']} ({int(r[f'top{i}_ref_n_gt5pct'])} of {r.n_gt5pct} / "
                 f"{int(r[f'top{i}_ref_rows_in_stratum'])})"
                 for i in (1, 2) if isinstance(r.get(f"top{i}_ref_gt5pct"), str)]
        if parts:
            lines.append(f"- {r.check}, {r.stratum}: " + "; ".join(parts))
    lines += ["", "Stellar-parameter references of the 'published' stellar strata (top 4 by rows):", ""]
    for cid, vc in comp.items():
        lines.append(f"- {cid}: " + "; ".join(f"{k} ({v})" for k, v in vc.items()))
    lines += ["", "Published rows with TICv8 stellar parameters (rows / rows off by > 5%): "
              + "; ".join(f"{k} {a} / {b}" for k, (a, b) in tic_viol.items())]
    bib = d.st_refname.str.extract(r"/abs/([^/\s]+)/abstract")[0]
    amb = (pd.DataFrame({"s": refshort(d.st_refname), "b": bib})[(d.cls == "published").to_numpy()]
           .dropna().drop_duplicates().groupby("s").b.nunique())
    lines += [f"Short reference names in st_refname (published rows) standing for more than one bibcode: "
              f"{int((amb > 1).sum())}"]
    lines += ["", f"Outlier entries (published, |d| > 20%): {len(out)} row-identity entries, "
              f"{n_distinct_rows} distinct rows, "
              f"{out.pl_name.nunique()} planets, {out.groupby('check').size().to_dict()}"]
    o_sol = (out.check == "RHOS") & out.st_ref.str.extract(r"\[(.+)\]$")[0].isin(SOLAR_UNIT_BIBCODES)
    o_koi = (out.check == "RHOS") & out.st_ref.str.contains("KOI Table", na=False)
    o_dep, o_um = out.check == "DEPTH", out.check == "UMASS"
    rest = out[~(o_sol | o_koi | o_dep | o_um)]
    lines += [f"Of these entries: {int(o_sol.sum())} RHOS solar-unit references, {int(o_koi.sum())} RHOS KOI-table "
              f"stars, {int(o_dep.sum())} DEPTH (approximate identity), {int(o_um.sum())} UMASS (rounding); "
              f"remaining {len(rest)} entries, {rest.index.nunique()} distinct rows, {rest.pl_name.nunique()} planets."]
    # Clustering of factor-2 outliers by reference.
    big = out[np.abs(np.log(out.ratio_obs_over_pred)) > np.log(2)]
    lines += ["", "Factor-of-2 outliers by check and reference (top 5 references per check):", ""]
    for cid, g in big.groupby("check"):
        ref = g.st_ref if cid in STELLAR else g.pl_ref
        top = ref.value_counts().head(5)
        lines.append(f"- {cid}: {len(g)} rows; " + "; ".join(f"{k} ({v})" for k, v in top.items()))
    lines += ["", "References with >= 5 published rows whose median obs/pred is off by more than 10%:", "",
              "| check | reference | rows | median ratio | q25 | q75 |", "|---|---|---|---|---|---|"]
    for _, r in br.iterrows():
        lines.append(f"| {r.check} | {r.ref} | {r.n_rows} | {r.median_ratio} | {r.q25_ratio} | {r.q75_ratio} |")
    (res / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(3, 4, figsize=(15, 9))
    for ax, (cid, (x, desc)) in zip(axs.ravel(), hist.items()):
        ax.hist(np.clip(x / LN10, -1.5, 1.5), bins=121, color="#3b6ea5")
        ax.set_yscale("log")
        ax.set_title(f"{cid}: {desc}", fontsize=8)
        ax.set_xlabel("log10(obs/pred), clipped to ±1.5", fontsize=8)
    fig.suptitle("Published rows of the NASA Exoplanet Archive ps table (same-reference rows for K3, RATROR, RATDOR, INSOL):\n"
                 "tabulated value over value implied by the same row")
    fig.tight_layout()
    fig.savefig(res / "discrepancy_histograms.png", dpi=110)


if __name__ == "__main__":
    main()
