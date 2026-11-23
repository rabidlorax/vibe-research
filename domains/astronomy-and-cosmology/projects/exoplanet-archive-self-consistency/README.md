---
title: Internal consistency of planet and star parameters in the NASA Exoplanet Archive
domain: astronomy-and-cosmology
status: result
evidence: external-data
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Internal consistency of planet and star parameters in the NASA Exoplanet Archive

## Question

Each row of the NASA Exoplanet Archive's Planetary Systems table (`ps`) is
meant to be one published parameter set from one reference. Several of its
columns are tied together by exact physical or geometric identities: Kepler's
third law (period, semi-major axis, stellar mass), stellar surface gravity
(mass, radius), stellar density, the Stefan-Boltzmann law (luminosity, radius,
effective temperature), planet density (mass, radius), the radius ratio and
scaled semi-major axis, and the unit pairs (Earth and Jupiter units of the same
quantity). How often do rows that come from a single reference violate these
identities by more than their stated uncertainties allow, and which rows
violate them so badly that a transcription, unit, or ingestion error is the
likely cause?

An answer is: for each identity, the number of rows tested, the distribution of
the discrepancy, the fraction outside a stated tolerance, and a list of the
most discrepant rows that a reader can check against the cited papers.

## Why it matters

The archive is the default input for exoplanet population studies, and users
commonly combine columns (for example, deriving insolation or density
themselves). A measured error rate per identity tells them how far to trust
that, and a list of grossly inconsistent rows is something the archive's
maintainers can correct.

## Summary of result

Snapshot: `ps` table downloaded 2026-11-23, 40,428 rows, 6,473 planets
(sha256 `f7f15dab…1f2e0d`, full value in `data/ps.sha256`).

1. **A unit error affects the stellar density of 18% of planets in the
   archive's composite table.** For three references, the value in the
   `st_dens` column (documented unit g/cm³) equals M★/R★³ in *solar* units and
   is a factor 1.41 too low for g/cm³: Fulton & Petigura 2018 (1,414 rows),
   Torres et al. 2017 (22) and MacDonald et al. 2016 (11). That is 1,447 rows
   for 1,423 planets. In the composite table (`pscomppars`), 1,062 of the 5,859
   planets that have a stellar density (18.1%) take it from one of these three
   references. For Fulton & Petigura 2018 the cause is in the paper: its
   Table 2 heads the density column "g/cc" while the tabulated values are in
   solar units (KOI-1: M = 0.99, R = 1.04, ρ = 0.87; 0.99/1.04³ = 0.88). The
   archive reproduces the paper faithfully. Evidence: `external-data`, plus
   `literature` for the paper's table.

2. **Rows from a single published reference are mostly, but not always,
   self-consistent.** The archive's documentation says "any one row in the
   Planetary Systems Table provides a self-consistent set of parameters".
   Among published rows whose planet and star parameters cite the same
   reference, the tabulated semi-major axis differs from the Kepler's-third-law
   value by more than 5% in 5.6% of 7,132 rows and by more than 20% in 1.3%
   (92 rows). Rates for the other identities are in the table under Method.
   Counting only rows that differ by more than 5% *and* by more than 3σ of
   their own stated uncertainties, the rate is 0.1% to 1.5% per identity, with
   stellar density (15%, dominated by item 1) the exception. Evidence:
   `external-data`.

3. **In rows from the Kepler KOI tables, `st_dens` and `pl_ratdor` are not the
   quantities their names suggest when combined with other columns.** The
   stellar density differs from 3M★/4πR★³ by a median of 56% and a/R★ differs
   from `pl_orbsmax`/`st_rad` by a median of 25%, while Kepler's third law,
   log g and Rp/R★ hold to within 5% in over 99.9% of the same rows. A
   likely reason, not verified here, is that these two columns are fitted
   transit-model quantities. Either way a user should not mix them with the
   mass, radius and semi-major axis columns. Evidence: `external-data` for the
   numbers, `conjecture` for the reason.

4. `results/outliers.csv` lists the 3,276 published rows (2,595 planets) that
   violate an identity by more than 20%. Only two entries were traced to their
   papers (item 1, and TOI-1227 below). The rest are leads, not confirmed
   errors.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | In the 2026-11-23 snapshot, `st_dens` for rows citing Fulton & Petigura 2018, Torres et al. 2017 and MacDonald et al. 2016 (1,447 rows, 1,423 planets) matches M★/R★³ in solar units (median ratio 1.010, 0.990, 0.995; 93%, 82%, 100% of rows within 10%) and not in g/cm³ (median ratio 0.716, 0.703, 0.706; 0.1%, 0%, 0% within 10%). No other reference with ≥ 5 rows, of 151, meets the same criterion | `external-data` | `python src/density_units.py`; see `results/density_units.md` |
| 2 | 1,062 of 5,859 planets with a stellar density in `pscomppars` (18.1%) take it from one of those three references | `external-data` | same command |
| 3 | Fulton & Petigura 2018, Table 2, gives the unit of ρ_iso as "g/cc" and lists KOI-1 with R = 1.04 R☉, M_iso = 0.99 M☉, ρ_iso = 0.87; the archive's row for TrES-2 b (KOI-1) from that reference has `st_dens` = 0.87 | `literature` | Read Table 2 of arXiv:1805.01453; query the archive for TrES-2 b |
| 4 | Per-identity violation rates for published, KOI and TESS rows are as in `results/summary.md` (excerpt under Method) | `external-data` | `python src/audit.py` |
| 5 | Mann et al. 2022 (TOI-1227) report L★ = (2.51 ± 0.17) × 10⁻³ L☉ with R★ = 0.56 R☉ and Teff = 3072 K, which imply 2.5 × 10⁻² L☉; the archive's `st_lum` = −2.600 matches the paper's printed value | `literature` for the paper's values, `external-data` for the archive's | Read the stellar-parameter table of arXiv:2110.09531; row in `results/outliers.csv` |
| 6 | The factor of ten in claim 5 is a typo in the paper's luminosity exponent rather than an error in R★ or Teff (the paper's insolation, 3.21 S⊕ at 0.0886 au, needs L★ ≈ 2.5 × 10⁻² L☉) | `conjecture` | Ask the authors, or recompute L★ from the paper's bolometric flux and the Gaia distance |
| 7 | In Kepler KOI-table rows, `st_dens` and `pl_ratdor` are fitted transit quantities, which is why they disagree with the mass, radius and semi-major axis columns | `conjecture` | Read the Kepler KOI table documentation for the corresponding KOI columns |

## Method

`src/fetch.py` downloads 25 parameter columns with their uncertainties and
limit flags, plus provenance columns, for every row of `ps` through the
archive's TAP service. `src/audit.py` then evaluates, per row, the ratio of a
tabulated value to the value implied by other columns of the same row, for
twelve identities:

| id | Tabulated | Implied by | Exactness |
|---|---|---|---|
| K3 | `pl_orbsmax` | (G M★ P² / 4π²)^(1/3) | exact up to planet mass; circumbinary rows excluded |
| LOGG | `st_logg` | log(G M★ / R★²) | exact |
| RHOS | `st_dens` | 3 M★ / 4π R★³ | exact |
| LUM | `st_lum` | log(R★² Teff⁴) in solar units | exact |
| RHOP | `pl_dens` | 3 Mp / 4π Rp³ (true masses only) | exact |
| URAD, UMASS, UMSINI | Earth-unit column | Jupiter-unit column × conversion | exact up to rounding |
| RATROR | `pl_ratror` | Rp / R★ | exact |
| RATDOR | `pl_ratdor` | a / R★ | exact for circular orbits |
| DEPTH | `pl_trandep` | 100 (Rp/R★)² | approximate: limb darkening and grazing transits shift it by tens of per cent |
| INSOL | `pl_insol` | L★ / a² | exact for circular orbits |

Constants are the IAU 2015 nominal solar and planetary values and CODATA 2018
G. Values flagged as upper or lower limits are dropped. Rows are split by
source: "published" (`soltype` Published Confirmed or Published Candidate),
Kepler KOI tables, and TESS/ExoFOP. For identities that join planet and star
columns, published rows are further split by whether `pl_refname` equals
`st_refname`; only the equal case tests a single reference.

Where every input has a two-sided uncertainty, z = ln(ratio)/σ, with σ from
first-order propagation treating the errors as independent. Published
uncertainties on a, M★ and R★ are usually positively correlated, so this σ is
generally too large and the "> 3σ" counts are conservative.

Excerpt of `results/summary.md` (real output; published rows; "> 3σ" column is
rows off by more than 5% and more than 3σ, as a share of rows with errors):

| check | stratum | rows | median off | > 5% | > 20% | rows > 20% | rows > 2× | > 3σ and > 5% |
|---|---|---|---|---|---|---|---|---|
| K3 | published, same ref | 7,132 | 0.06% | 5.59% | 1.29% | 92 | 5 | 0.93% |
| K3 | published, mixed refs | 356 | 0.51% | 6.18% | 0.28% | 1 | 1 | 0.63% |
| K3 | Kepler KOI | 13,124 | 0.09% | 0.00% | 0.00% | 0 | 0 | no errors given |
| LOGG | published | 12,691 | 0.23% | 13.58% | 6.07% | 770 | 90 | 0.58% |
| RHOS | published | 9,261 | 0.04% | 23.99% | 21.25% | 1,968 | 252 | 15.43% |
| RHOS | Kepler KOI | 13,363 | 56.3% | 77.21% | 67.48% | 9,018 | 5,076 | 6.15% |
| LUM | published | 7,209 | 0.00% | 4.51% | 1.15% | 83 | 24 | 0.34% |
| RHOP | published | 2,524 | 0.63% | 21.55% | 3.01% | 76 | 16 | 0.24% |
| URAD | published | 13,203 | 0.00% | 0.05% | 0.00% | 0 | 0 | n/a |
| UMASS | published | 4,839 | 0.00% | 0.25% | 0.04% | 2 | 0 | n/a |
| RATROR | published, same ref | 7,470 | 0.23% | 3.24% | 0.28% | 21 | 2 | 0.14% |
| RATDOR | published, same ref | 2,143 | 0.19% | 12.65% | 3.92% | 84 | 6 | 1.05% |
| RATDOR | Kepler KOI | 13,124 | 24.6% | 86.91% | 56.39% | 7,401 | 1,562 | no errors given |
| DEPTH | published | 1,225 | 5.09% | 50.12% | 12.73% | 156 | 15 | 8.97% |
| INSOL | published, same ref | 766 | 0.49% | 13.71% | 3.13% | 24 | 9 | 1.48% |

Reading the table: the two UMASS rows above 20% are one-significant-figure
rounding (0.002 M_J beside 0.5 M⊕), not errors. Many LOGG rows differ
because papers quote a spectroscopic log g beside an isochrone mass and
radius; that is a real inconsistency in the published set but not a
transcription error. The median discrepancy for published rows is far below
1% for every exact identity, so the typical row is self-consistent.

`src/audit.py` also groups published rows by reference and reports
references whose median ratio is displaced by more than 10%
(`results/by_reference.csv`). That table is what exposed the density offset.
`src/density_units.py` then tests each reference's densities against both
unit hypotheses and counts affected composite-table planets.

Things tried that are not headline results: the largest single outliers
(HAT-P-7 b with a = 3.0 au at P = 2.2 d under Yang et al. 2025; TOI-2049 b
with Rp/R★ = 1.49 under Guenther et al. 2026) could not be checked because
the ADS pages for those papers returned no content from this session. They
are in `results/outliers.csv` unverified.

## Reproduction

From the repository root, with Python 3.13, pandas 3.0.5, numpy 2.5.3,
matplotlib 3.11.2 (the versions used):

```bash
cd domains/astronomy-and-cosmology/projects/exoplanet-archive-self-consistency
python src/fetch.py           # ~31 MB from exoplanetarchive.ipac.caltech.edu, about 1 minute
python src/audit.py           # about 5 seconds; writes results/summary.*, outliers.csv, by_reference.csv, PNG
python src/density_units.py   # one more small TAP query (pscomppars); --offline skips it
```

The archive changes continuously. A fresh download will not match
`data/ps.sha256`, and counts will move as rows are added or corrected. The
committed results are for the snapshot whose checksum and query are in
`data/fetch_meta.json`. The raw file is not committed.

## External data and what we could not reproduce

- **NASA Exoplanet Archive**, Planetary Systems table (`ps`) and Planetary
  Systems Composite Parameters table (`pscomppars`), via
  `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`, accessed 2026-11-23.
  Exact queries are in `src/fetch.py` and `src/density_units.py`. Table DOIs
  10.26133/NEA12 and 10.26133/NEA13 `[from memory, unverified]`. Licence: the
  archive's data are public and free to use with acknowledgement `[from
  memory, unverified; the terms page was not read in this session]`. Only
  derived ratios and the identifying values of outlier rows are committed.
- **Published papers** read for claims 3 and 5: Fulton & Petigura 2018
  (arXiv:1805.01453, read through the ar5iv HTML rendering) and Mann et al.
  2022 (arXiv:2110.09531v2, arXiv HTML).

None of the underlying measurements were made here and none can be
reproduced here. Every claim depends on the archive snapshot. Claims 1 to 3
would fall if the archive's mass, radius and density columns for those
references were not what the papers published; claim 3 checks one star.

Known problems with the source: the archive states that the composite table
is "not necessarily self-consistent", and it kept a page of confirmed
discrepancies between literature and archive values (66 hosts; marked as no
longer updated from August 2026, with discrepancies now recorded on System
Overview pages). None of the three density references appears on that page
as fetched on 2026-11-23. The System Overview notes were not searched.

No fetched page contained instructions addressed to an AI.

## Prior work and novelty

Searched on 2026-11-23, before the analysis: web search (five queries on
exoplanet-archive internal consistency, self-consistency, Kepler's third law
checks, catalogue errors and typos, and the Fulton & Petigura density
units); OpenAlex (three queries: "exoplanet catalog internal consistency
parameters", "exoplanet archive data quality errors catalogue",
"self-consistent exoplanet catalog homogeneous parameters inconsistencies");
arXiv API ("exoplanet archive" with "inconsistencies", "internal
consistency", "self-consistency", "unit error"); and the archive's own
documentation. Alternative names used: self-consistency, internal
consistency, Keplerian consistency, catalogue validation, data quality,
literature discrepancies.

Found:

- Decocq, Swain, Dang, Ciardi & Bryden, "Comparing Results from Two Uniform
  Phase Curve Surveys", arXiv:2605.10427 (May 2026). They recompute periods
  from Kepler's third law for the archive's default parameters, identify five
  outliers by eye (TOI-6130, TOI-3714, EPIC 201757695, K2-216, TOI-2266), and
  conclude: "it is therefore prudent to check for Keplerian consistency when
  selecting exoplanet system parameters." They give no rates, test default
  rows only, and test no identity other than Kepler's third law and an
  equilibrium-temperature relation. Read as the arXiv HTML, partly through a
  summarising tool; the page was truncated, so details beyond the quoted
  sentence are second-hand.
- Bashi, Helled & Zucker 2018, "A Quantitative Comparison of Exoplanet
  Catalogs" (arXiv:1808.10236) and Alei et al. 2020, "Exo-MerCat". These
  compare catalogues with each other, not columns within a row. Titles and
  abstracts only.
- The archive's "Discrepancies Between Literature and Archive Values" page:
  individually reported typos, found by community reports rather than by a
  systematic test.
- Li et al. 2023 (arXiv:2311.01427) use Kepler's third law to fill missing
  archive values, not to test them (first two thirds of the paper read).

Not found in the search described: a per-identity violation rate for the
`ps` table, or any statement that Fulton & Petigura 2018 densities are in
solar units in the paper or the archive. Hence `partially-known`: the
Kepler's-law check on archive rows exists; the systematic multi-identity
rates and the density unit finding were not found. The search was short and
the archive's helpdesk history is not public, so the maintainers may already
know.

## Limitations and open questions

- One snapshot. The archive is edited daily.
- Claim 1 was confirmed against the paper for one of three references and one
  star. Torres et al. 2017 and MacDonald et al. 2016 were inferred from the
  ratio alone; their tables were not read.
- A discrepancy does not say which column is wrong, or whether the paper or
  the archive introduced it. Both cases checked here trace to the paper.
- K3 ignores the companion's mass, which matters at the per-cent level for
  brown-dwarf companions; some K3 rows between 1% and 5% are of this kind.
  RATDOR and INSOL assume circular orbits.
- LOGG, RHOS and DEPTH discrepancies often reflect different measurement
  routes (spectroscopic gravity, transit-derived density, limb darkening),
  not mistakes.
- Propagated σ assumes independent errors and symmetrises asymmetric ones.
- `pl_refname == st_refname` is taken as "single reference". Whether the
  archive ever fills individual cells of such a row from elsewhere was not
  checked.
- Open: trace the remaining factor-of-two outliers to their papers; check
  the two unread density references; report confirmed cases to the archive
  helpdesk (needs the repository owner; nothing has been sent).

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
