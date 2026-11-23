#!/usr/bin/env python3
"""Test the hypothesis that some references' stellar densities are stored in
solar units in the g/cm^3 column `st_dens`.

For every reference with >= 5 published rows, compares st_dens with
M*/R*^3 (a) in g/cm^3 and (b) in solar units, and reports which fits. Then
fetches the composite table (pscomppars) density provenance to count how
many planets' composite stellar density comes from an affected reference.

Usage: python src/density_units.py [--offline]
Writes results/density_units.md and results/density_units_by_reference.csv.
"""
import hashlib
import io
import pathlib
import sys
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent
RHO_SUN = 1.3271244e20 / 6.67430e-11 / (4 / 3 * np.pi * 6.957e8**3) / 1000
REF = r">\s*([^<]+?)\s*</a>"


def refkey(col):
    """Short name plus ADS bibcode; the short name alone is not unique."""
    short = col.str.extract(REF)[0].str.replace("&amp;", "&")
    bib = col.str.extract(r"/abs/([^/\s]+)/abstract")[0].str.replace("%26", "&")
    return (short + " [" + bib + "]").where(bib.notna(), short)


def within(x, centre, tol=1.03):
    return np.abs(np.log(x / centre)) < np.log(tol)


def main():
    d = pd.read_csv(HERE / "data" / "raw" / "ps.csv", low_memory=False)
    d = d[d.soltype.str.startswith("Published") & (d.st_denslim.fillna(0) == 0)]
    d = d[(d.st_masslim.fillna(0) == 0) & (d.st_radlim.fillna(0) == 0)]
    d = d[(d.st_mass > 0) & (d.st_rad > 0) & (d.st_dens > 0)].copy()
    d["ref"] = refkey(d.st_refname)
    d["r_cgs"] = d.st_dens / (RHO_SUN * d.st_mass / d.st_rad**3)   # 1 if g/cm^3
    d["r_solar"] = d.st_dens / (d.st_mass / d.st_rad**3)           # 1 if solar units
    g = d.groupby("ref")
    t = pd.DataFrame({
        "rows": g.size(), "planets": g.pl_name.nunique(), "hosts": g.hostname.nunique(),
        "median_ratio_if_cgs": g.r_cgs.median().round(4),
        "median_ratio_if_solar": g.r_solar.median().round(4),
        "pct_within10_if_cgs": (100 * g.r_cgs.apply(lambda x: within(x, 1, 1.1).mean())).round(1),
        "pct_within10_if_solar": (100 * g.r_solar.apply(lambda x: within(x, 1, 1.1).mean())).round(1),
    }).reset_index()
    t = t[t.rows >= 5]
    sol = t[(t.pct_within10_if_solar >= 80) & (t.pct_within10_if_cgs <= 20)].sort_values("rows", ascending=False)
    t.sort_values("rows", ascending=False).to_csv(HERE / "results" / "density_units_by_reference.csv", index=False)
    out = [f"rho_sun used: {RHO_SUN:.4f} g/cm^3",
           f"published rows tested: {len(d)}; references (short name + bibcode) with >= 5 rows: {len(t)}", "",
           "References where >= 80% of rows match M*/R*^3 in SOLAR units within 10% and <= 20% match in g/cm^3:", "",
           sol.to_string(index=False), ""]
    bad = set(sol.ref)
    aff = d[d.ref.isin(bad)]
    out += [f"Affected ps rows: {len(aff)} ({aff.pl_name.nunique()} planets, {aff.hostname.nunique()} host stars); "
            f"of these, default_flag=1 rows: {int((aff.default_flag == 1).sum())}", ""]
    # Row-level leads in the remaining literature rows: st_dens within 3% of
    # the solar-unit value, i.e. r_cgs within 3% of 1/rho_sun. Controls are
    # windows of the same logarithmic width elsewhere in r_cgs, including the
    # mirror image (r_cgs = rho_sun), which this unit slip cannot produce.
    rest = d[~d.ref.isin(bad) & ~d.ref.str.contains("KOI Table|TICv8", na=False)]
    lead = rest[within(rest.r_cgs, 1 / RHO_SUN)]
    out += [f"Remaining published rows (KOI-table and TICv8 stars excluded): {len(rest)}.",
            f"Rows with st_dens within 3% of M*/R*^3 in solar units (r_cgs = {1 / RHO_SUN:.4f}): "
            f"{len(lead)} rows, {lead.pl_name.nunique()} planets, {lead.hostname.nunique()} hosts.",
            "Control windows of the same width: " + "; ".join(
                f"r_cgs = {c:.4f}: {int(within(rest.r_cgs, c).sum())} rows" for c in (0.65, 0.76, RHO_SUN))]
    gl = lead.groupby("ref")
    full = pd.DataFrame({"match": gl.size(), "hosts": gl.hostname.nunique()})
    full["tested"] = rest.groupby("ref").size().reindex(full.index)
    full = full[(full.match == full.tested) & (full.match >= 2)].sort_values(["match", "hosts"], ascending=False)
    out += ["References with >= 2 rows, all of them in the solar-unit window (rows / hosts), none read:",
            "; ".join(f"{k} ({r.match}/{r.hosts})" for k, r in full.iterrows()), ""]
    if "--offline" not in sys.argv:
        q = "select pl_name,st_dens,st_dens_reflink,st_mass,st_rad from pscomppars where st_dens is not null"
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q) + "&format=csv"
        req = urllib.request.Request(url, headers={"User-Agent": "vibe-research-consistency-audit/0.1 (research script)"})
        raw = urllib.request.urlopen(req, timeout=300).read()
        (HERE / "data" / "raw" / "pscomppars_dens.csv").write_bytes(raw)
        sha = hashlib.sha256(raw).hexdigest()
        (HERE / "data" / "pscomppars_dens.sha256").write_text(f"{sha}  pscomppars_dens.csv\nquery: {q}\n")
        c = pd.read_csv(io.BytesIO(raw))
        c["ref"] = refkey(c.st_dens_reflink)
        ca = c[c.ref.isin(bad)]
        r = ca.st_dens / (ca.st_mass / ca.st_rad**3)
        ntot = int(pd.read_csv(io.BytesIO(urllib.request.urlopen(urllib.request.Request(
            "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+pscomppars&format=csv",
            headers={"User-Agent": "vibe-research-consistency-audit/0.1 (research script)"}), timeout=300).read())).n[0])
        out += [f"pscomppars download sha256 {sha}",
                f"Composite table (pscomppars): {ntot} planets, {len(c)} with a stellar density; "
                f"{len(ca)} ({100 * len(ca) / len(c):.1f}% of those, {100 * len(ca) / ntot:.1f}% of all) "
                f"take it from an affected reference:",
                ca.ref.value_counts().to_string(), "",
                f"For those composite rows, st_dens / (M*/R*^3 in solar units) has median {r.median():.3f} "
                f"(composite mass and radius may come from other references)."]
    (HERE / "results" / "density_units.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
