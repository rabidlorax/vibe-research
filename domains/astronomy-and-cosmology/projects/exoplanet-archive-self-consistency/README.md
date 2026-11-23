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

1. **A unit error affects the stellar density of 18% of the composite-table
   planets that have one.** For four references, the value in the `st_dens`
   column (documented unit g/cm³) equals M★/R★³ in *solar* units and is a
   factor 1.41 too low for g/cm³: Fulton & Petigura 2018 (1,414 rows), Torres
   et al. 2017 (22), Mann et al. 2017, AJ 153, 267 (13) and MacDonald et al.
   2016 (11 rows, all for one star, Kepler-80). That is 1,460 rows for 1,435
   planets. In the composite table (`pscomppars`), 1,067 of the 5,859 planets
   that have a stellar density (18.2%; 16.5% of all 6,473 planets) take it
   from one of these references, 1,049 of them from Fulton & Petigura. Two
   different mechanisms are involved:
   - *Fulton & Petigura 2018: the paper's label.* Its Table 2 heads the
     density column "g/cc" while the tabulated values are in solar units
     (KOI-1: M = 0.99, R = 1.04, ρ = 0.87; 0.99/1.04³ = 0.88). The archive
     reproduces the printed numbers.
   - *The other three: the archive's ingestion.* Each paper states solar
     units and the archive stores the same numbers in its g/cm³ column
     without converting. Torres et al. 2017, Table 6, column "(ρ☉)":
     KOI-3282 = Kepler-1455, 3.89. Mann et al. 2017, stellar table, column
     "(ρ⊙)": Kepler-138 5.00, Kepler-42 26.80. MacDonald et al. 2016, text:
     "a mean stellar density of ρ = 2.33 ± 0.15 ρ⊙" for Kepler-80. The
     archive does convert in other cases: Mann et al. 2022 print
     ρ★ = 0.94 ρ☉ for TOI-1227 and the archive has 1.325.

   The 1,460 is a lower bound. Among the remaining 3,045 literature rows, 43
   lie within 3% of the solar-unit value, against 5 to 10 in control windows
   of the same width; ten further references have all of their rows (2 to 4
   each) there. None of those was read, so they are leads only. Evidence:
   `external-data`; the papers' tables are supporting `literature`.

2. **Rows from a single published reference are mostly, but not always,
   self-consistent.** The archive's documentation says "any one row in the
   Planetary Systems Table provides a self-consistent set of parameters".
   Among published rows whose planet and star parameters cite the same
   reference, the tabulated semi-major axis differs from the Kepler's-third-law
   value by more than 5% in 5.6% of 7,132 rows (399 rows) and by more than 20%
   in 1.3% (92 rows). One reference, Stassun et al. 2017, supplies 118 of the
   399; it recomputes stellar masses and radii for already-known planets, so
   its rows may not be one orbital solution. Without it the rate is 281 of
   6,928, or 4.1%. Rates for the other identities are in the table under
   Method. Counting only rows that differ by more than 5% *and* by more than
   3σ of their own stated uncertainties, the rate for the exact identities is
   0.1% to 1.9% (same-reference strata for planet-star identities;
   literature-only strata for the stellar ones). The three stellar
   identities are the least well obeyed: in rows whose stellar parameters
   come from a paper, not from TICv8 or a KOI table, log g differs from the
   mass-radius value by more than 5% in 21.7% of 7,935 rows, density in
   13.4% of 3,045 (item 1 references removed) and luminosity in 11.5% of
   2,827. Evidence: `external-data`.

3. **In rows from the Kepler KOI tables, `st_dens` and `pl_ratdor` are
   transit-fitted quantities, not the mass-radius density or `pl_orbsmax`/
   `st_rad`.** There the stellar density differs from 3M★/4πR★³ by a median of
   56% and a/R★ differs from `pl_orbsmax`/`st_rad` by a median of 25%, while
   Kepler's third law, log g and Rp/R★ hold to within 5% in over 99.9% of the
   same rows. For the DR25 KOI table, all 2,683 matched rows have `st_dens`
   equal to the KOI table's `koi_srho` and `pl_ratdor` equal to `koi_dor`.
   The archive documents `koi_srho` as "Fitted stellar density ... a direct
   observable from the light curve ... completely independent from the listed
   stellar mass and radius". This is documented behaviour and the
   fitted-versus-catalogue density difference is a known effect; the point
   for users is that the `ps` column name does not distinguish the two, and
   that 370 "published" planet rows also carry these KOI-table stellar
   values. Evidence: `external-data`; the column definition is supporting
   `literature`.

4. `results/outliers.csv` lists 3,276 row-identity entries (3,100 distinct
   published rows, 2,595 planets) where the two sides of an identity differ
   by more than 20%. Of the entries, 1,453 are the item 1 densities, 324 are
   KOI-table fitted densities (item 3), 156 belong to the approximate DEPTH
   identity and 2 are rounding. The remaining 1,341 entries (1,192 rows, 941
   planets) are candidate inconsistencies. Only the cases named in this
   README were traced to their papers. The rest are leads, not confirmed
   errors.

The front-matter `evidence: external-data` is the label of headline items 1
to 3, which rest on claims 1, 2, 5 and 6. The `literature` claims (3, 4, 7,
8) support the interpretation of who introduced an error and are not
headline; claims 8 to 10 are a side result.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | In the 2026-11-23 snapshot, `st_dens` for rows citing Fulton & Petigura 2018, Torres et al. 2017, Mann et al. 2017 (bibcode 2017AJ....153..267M) and MacDonald et al. 2016 (1,460 rows, 1,435 planets, 856 hosts) matches M★/R★³ in solar units (median ratio 1.010, 0.990, 1.000, 0.995; 93%, 82%, 100%, 100% of rows within 10%) and not in g/cm³ (median ratio 0.716, 0.703, 0.709, 0.706; 0.1%, 0%, 0%, 0% within 10%). No other reference with ≥ 5 rows, of 140 (references keyed by name and bibcode), meets the same criterion (≥ 80% within 10% in solar units and ≤ 20% in g/cm³) | `external-data` | `python src/density_units.py`; see `results/density_units.md` |
| 2 | 1,067 of 5,859 planets with a stellar density in `pscomppars` (18.2%) take it from one of those four references | `external-data` | same command |
| 3 | Fulton & Petigura 2018, Table 2 (arXiv version), gives the unit of ρ_iso as "g/cc" and lists KOI-1 with R = 1.04 R☉, M_iso = 0.99 M☉, ρ_iso = 0.87; the archive's row for TrES-2 b (KOI-1) from that reference has `st_dens` = 0.87 | `literature` | Read Table 2 of arXiv:1805.01453; query the archive for TrES-2 b |
| 4 | Three papers give density in solar units with values the archive stores unchanged in `st_dens`: Torres et al. 2017, Table 6, "(ρ☉)", KOI-3282 0.544 / 0.518 / 3.89 (archive, Kepler-1455 b: same three numbers); Mann et al. 2017, stellar table, "(ρ⊙)", 5.00, 7.03, 26.80 for Kepler-138, -560, -42; MacDonald et al. 2016, "M = 0.730 ± 0.030 M⊙, a radius of R = 0.678 ± 0.023 R⊙, a mean stellar density of ρ = 2.33 ± 0.15 ρ⊙" | `literature` | Read arXiv:1711.01267 (Table 6), arXiv:1705.01545 (stellar table), arXiv:1607.07540 (stellar-parameter paragraph); compare with the archive rows in `results/outliers.csv` |
| 5 | Per-identity rates for published, KOI and TESS rows are as in `results/summary.md` (excerpt under Method) | `external-data` | `python src/audit.py` |
| 6 | For all 2,683 `ps` rows of the DR25 KOI table that match a DR25 KOI by planet name, `st_dens` = `koi_srho` and `pl_ratdor` = `koi_dor` | `external-data` | `python src/koi_columns.py` |
| 7 | The archive's KOI column documentation defines `koi_srho` as a fitted transit quantity "completely independent from the listed stellar mass and radius" | `literature` | Read `docs/API_kepcandidate_columns.html` on the archive |
| 8 | Mann et al. 2022 (TOI-1227) print L★ = (2.51 ± 0.17) × 10⁻³ L☉, R★ = 0.56 R☉, Teff = 3072 K, F_bol = 7.87 × 10⁻¹¹ erg cm⁻² s⁻¹ and X, Y, Z = 51.34, −85.22, −16.95 pc. The radius and temperature give 0.0252 L☉; the flux and position (100.9 pc) give 0.0251 L☉ | `literature` | Read the stellar-parameter table of arXiv:2110.09531; `python src/toi1227_luminosity.py` does the arithmetic |
| 9 | The archive's `st_lum` for TOI-1227 (−2.600) equals the printed 2.51 × 10⁻³ | `external-data` | TOI-1227 b rows in `results/outliers.csv` |
| 10 | The printed luminosity in claim 8 has a wrong exponent (10⁻³ for 10⁻²) | `conjecture` | Ask the authors or check for an erratum |

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
uncertainties are often correlated (for K3, a is commonly derived from M★ and
P, which would make this σ too large), but that was not tested, and for
identities whose two sides are measured independently the σ may be about
right. Treat the "> 3σ" counts as indicative.

Excerpt of `results/summary.md` (real output; published rows; "> 3σ" column is
rows off by more than 5% and more than 3σ, as a share of rows with errors):

| check | stratum | rows | median off | > 5% | > 20% | rows > 20% | rows > 2× | > 3σ and > 5% |
|---|---|---|---|---|---|---|---|---|
| K3 | published, same ref | 7,132 | 0.06% | 5.59% | 1.29% | 92 | 5 | 0.93% |
| K3 | published, mixed refs | 356 | 0.51% | 6.18% | 0.28% | 1 | 1 | 0.63% |
| K3 | Kepler KOI | 13,124 | 0.09% | 0.00% | 0.00% | 0 | 0 | no errors given |
| LOGG | published | 12,691 | 0.23% | 13.58% | 6.07% | 770 | 90 | 0.58% |
| LOGG | published, literature star ref | 7,935 | 0.98% | 21.73% | 9.70% | 770 | 90 | 0.73% |
| RHOS | published | 9,261 | 0.04% | 23.99% | 21.25% | 1,968 | 252 | 15.43% |
| RHOS | published, literature star ref | 3,045 | 0.55% | 13.37% | 6.27% | 191 | 37 | 1.88% |
| RHOS | Kepler KOI | 13,363 | 56.3% | 77.21% | 67.48% | 9,018 | 5,076 | 6.15% |
| LUM | published | 7,209 | 0.00% | 4.51% | 1.15% | 83 | 24 | 0.34% |
| LUM | published, literature star ref | 2,827 | 0.59% | 11.50% | 2.94% | 83 | 24 | 0.55% |
| RHOP | published | 2,524 | 0.63% | 21.55% | 3.01% | 76 | 16 | 0.24% |
| URAD | published | 13,203 | 0.00% | 0.05% | 0.00% | 0 | 0 | n/a |
| UMASS | published | 4,839 | 0.00% | 0.25% | 0.04% | 2 | 0 | n/a |
| RATROR | published, same ref | 7,470 | 0.23% | 3.24% | 0.28% | 21 | 2 | 0.14% |
| RATDOR | published, same ref | 2,143 | 0.19% | 12.65% | 3.92% | 84 | 6 | 1.05% |
| RATDOR | Kepler KOI | 13,124 | 24.6% | 86.91% | 56.39% | 7,401 | 1,562 | no errors given |
| DEPTH | published | 1,225 | 5.09% | 50.12% | 12.73% | 156 | 15 | 8.97% |
| INSOL | published, same ref | 766 | 0.49% | 13.71% | 3.13% | 24 | 9 | 1.48% |

Reading the table:

- "Published" is defined by the planet row's `soltype`. Its stellar columns
  can still come from a catalogue: of the 12,691 LOGG rows, 4,386 take their
  stellar values from TICv8 and 370 from the DR25 KOI table. The TICv8 rows
  show no violation above 5% in any stellar identity, so they dilute the
  plain "published" rates. The "literature star ref" lines drop TICv8 and
  KOI-table stars and, for density, the item 1 references; those are the
  lines to use for the stellar identities. The plain "RHOS published" line
  is dominated by the item 1 references (1,453 of its 1,968 rows above 20%)
  and KOI-table stars (324).
- The "> 3σ and > 5%" figure for the approximate DEPTH identity (8.97%) is
  expected and is not a count of errors. Mixed-reference strata are shown
  for comparison only (RATROR mixed: 2.68%, not in the excerpt).
- The two UMASS rows above 20% are one-significant-figure rounding (for
  example 0.002 M_J beside 0.5 M⊕), not errors.
- LOGG rows above 5% are led by Mayo et al. 2018 (148) and Stassun et al.
  2017 (122). A probable cause, not checked against any paper, is a
  spectroscopic log g quoted beside an isochrone mass and radius.
- The median discrepancy is below 1% for every exact identity in every
  published stratum, including the literature-only ones (largest: LOGG,
  0.98%), so the typical row is self-consistent.
- `results/summary.md` also lists, for every stratum, the reference that
  contributes most of the rows above 5%. References are keyed by short name
  plus ADS bibcode throughout, because 247 short names in `st_refname` (for
  example "Mann et al. 2017") stand for more than one paper.

`src/audit.py` also groups published rows by reference and reports
references whose median ratio is displaced by more than 10%
(`results/by_reference.csv`). That table is what exposed the density offset.
`src/density_units.py` then tests each reference's densities against both
unit hypotheses and counts affected composite-table planets. It also counts
row-level matches in the remaining literature rows: 43 rows lie within 3% of
the solar-unit value (ratio 0.709 to the g/cm³ value), against 5, 9 and 10
rows in windows of the same width centred on ratios 0.65, 0.76 and 1.41. The
excess is real, and `results/density_units.md` lists the ten references
whose rows all fall in the window.
`src/koi_columns.py` compares the DR25 KOI rows of `ps` with the KOI table
itself, and `src/toi1227_luminosity.py` redoes the TOI-1227 luminosity
arithmetic.

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
python src/koi_columns.py     # one more TAP query (q1_q17_dr25_koi)
python src/toi1227_luminosity.py   # no input, no network
```

The archive changes continuously. A later download may not match
`data/ps.sha256` (later downloads on the same day did), and counts will
move as rows are added or corrected. `fetch.py` keeps the committed
`data/fetch_meta.json` when the checksum matches. The two smaller downloads
have their checksums and queries in `data/pscomppars_dens.sha256` and
`data/dr25_koi.sha256`. The queries have no `ORDER BY`, so a checksum can
also change if the server returns rows in another order. The
committed results are for the snapshot whose checksum and query are in
`data/fetch_meta.json`. The raw file is not committed.

## External data and what we could not reproduce

- **NASA Exoplanet Archive**, Planetary Systems table (`ps`) and Planetary
  Systems Composite Parameters table (`pscomppars`), via
  `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`, accessed 2026-11-23.
  Exact queries are in `src/fetch.py` and `src/density_units.py`. Dataset DOIs
  10.26133/NEA12 (`ps`) and 10.26133/NEA13 (`pscomppars`), from the archive's
  `docs/doi.html`. The KOI table `q1_q17_dr25_koi` is queried by
  `src/koi_columns.py`. Licence: no licence statement was found; the
  archive's data are, as far as is known here, public and free to use with
  acknowledgement `[from memory, unverified]`. Only
  derived ratios and the identifying values of outlier rows are committed.
- **Published papers** read for claims 3, 4 and 8: Fulton & Petigura 2018
  (arXiv:1805.01453), Torres et al. 2017 (arXiv:1711.01267), Mann et al. 2017
  (arXiv:1705.01545) and MacDonald et al. 2016 (arXiv:1607.07540), through
  the ar5iv HTML rendering, and Mann et al. 2022 (arXiv:2110.09531v2, arXiv
  HTML). Only the arXiv versions were read, not the journal versions or
  their machine-readable tables, which could differ.
- **Archive documentation** quoted: `docs/pscp_about.html`,
  `docs/API_kepcandidate_columns.html`, `docs/lit_discrepancies.html`,
  `docs/doi.html`, all fetched 2026-11-23.

None of the underlying measurements were made here and none can be
reproduced here. Every claim depends on the archive snapshot. Claims 1 and 2
depend on the archive's mass, radius and density columns for those
references; claims 3 and 4 check one to three stars per paper.

Known problems with the source: the archive states that the composite table
is "not necessarily self-consistent", and it kept a page of confirmed
discrepancies between literature and archive values (66 hosts; marked as no
longer updated from August 2026, with discrepancies now recorded on System
Overview pages). None of the four density references appears on that page
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
  from Kepler's third law and plot them against the archive's periods, for
  all rows and for the default parameters. They highlight five outliers
  among the default rows (TOI-6130, TOI-3714, EPIC 201757695, K2-216,
  TOI-2266) and conclude: "it is therefore prudent to check for Keplerian
  consistency when selecting exoplanet system parameters." They give no
  rates and no numerical threshold for the archive comparison, and test no
  identity other than Kepler's third law and an equilibrium-temperature
  relation. Read as the arXiv HTML through a summarising tool; the quoted
  sentence was confirmed, the other details are second-hand.
- The difference between a transit-fitted stellar density and one from
  mass and radius (summary item 3) is a known and used effect. The archive's
  KOI documentation cites Seager & Mallén-Ornelas 2003 for it; the
  "asterodensity profiling" and "photoeccentric effect" literature (for
  example Sliski & Kipping 2014 `[not read]`) exploits it. Item 3 is
  therefore `known` in substance; only its counts are from this project.
- Bashi, Helled & Zucker 2018, "A Quantitative Comparison of Exoplanet
  Catalogs" (arXiv:1808.10236) and Alei et al. 2020, "Exo-MerCat". These
  compare catalogues with each other, not columns within a row. Titles and
  abstracts only.
- The archive's "Discrepancies Between Literature and Archive Values" page:
  individually reported typos, found by community reports rather than by a
  systematic test.
- Li et al. 2023 (arXiv:2311.01427) use Kepler's third law to fill missing
  archive values, not to test them (first two thirds of the paper read).

- "The Gaia spectroscopic catalogue of exoplanets and host stars",
  arXiv:2505.22205 (found by the second reviewer; passage read here). It
  recomputes host-star masses from the radii and surface gravities listed in
  online exoplanet databases and reports: "the stellar surface gravities and
  radii can be strongly inconsistent with the stellar mass: more than 21%
  and 8% of the EHS have a recomputed mass that differ by more than 5% and
  20%, respectively, with respect to the database values." That is the LOGG
  identity at the same thresholds, and it agrees with the literature-only
  LOGG line here (21.7% and 9.7%). Which database it used was not
  established. It also flags 278 planets whose recomputed mass or radius
  differs from the tabulated one by more than 10%. The LOGG rates here are
  therefore a replication.
- Lanzafame et al., "Tracking the evolution of sub-Neptunes. I.",
  arXiv:2611.00856, reported by the second reviewer to flag hosts whose
  log g differs by more than 0.3 dex from the mass-radius value; only the
  abstract was read here and it does not mention this.

An independent reviewer repeated the search on 2026-11-23 with different
terms (density mislabel or erratum, physically inconsistent rows, unit
mistakes in curated catalogues; web, OpenAlex and arXiv) and found no prior
statement of the density problem and no per-identity rate study.

Not found in the searches described: violation rates for the identities
other than log g, or any statement that Fulton & Petigura 2018 densities are in
solar units in the paper or the archive. Hence `partially-known`: the
Kepler's-law check on archive rows and a log g consistency rate exist; the
rates for the other identities and the density unit finding were not found. The search was short and
the archive's helpdesk history is not public, so the maintainers may already
know.

## Limitations and open questions

- One snapshot. The archive is edited daily.
- Claim 1 was checked against all four papers, one to three stars each, in
  their arXiv versions. The 1,460 rows are those of whole references that
  meet the criterion and are a lower bound: 43 further rows match solar
  units (25 of them in ten references whose rows all match), against a
  background of 5 to 10, and were not traced.
- A discrepancy does not say which column is wrong, or whether the paper or
  the archive introduced it. Of the five cases traced, two originate in the
  paper (Fulton & Petigura's unit label, the TOI-1227 luminosity) and three
  in the archive (Torres et al., Mann et al. 2017 and MacDonald et al.
  densities).
- The "published" strata mix literature solutions with catalogue stellar
  parameters (TICv8, KOI tables) and with re-analyses such as Stassun et al.
  2017, so their rates are not rates of error in individual papers.
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
  the ten further density references; report confirmed cases to the archive
  helpdesk (needs the repository owner; nothing has been sent).

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
| 2026-11-23 | Fresh agent session launched by the author's session, given the repository and the review rules but not the author's conclusions (model ID unknown: the agent did not report it) | Clean clone; reran all commands (checksum and all result files identical); read `src/` line by line and recomputed key numbers with separate code; fetched Fulton & Petigura 2018, Torres et al. 2017, Mann et al. 2022, Decocq et al. 2026 and the archive documentation; repeated the prior-art search with other terms. Not checked: MacDonald et al. 2016, Mann et al. 2017, journal versions, other outlier rows | Changes needed, none overturning a headline claim: 17 points (outlier entries miscounted as rows; a rate range that omitted DEPTH; undisclosed concentration of violations in catalogue stellar parameters and in Stassun et al. 2017; Torres et al. error is the archive's, not the paper's; denominator of the 18%; KOI-column and TOI-1227 claims labelled weaker than checkable; smaller wording and code points). All addressed in the following commit. Status stays `result` |
| 2026-11-23 | claude-fable-5-2, a second fresh agent session launched by the author's session on the same terms (same model as the author) | Clean clone; reran all five commands (all result files identical); recomputed the main counts with separate code; read `src/`; fetched Fulton & Petigura 2018, Torres et al. 2017, Mann et al. 2017 and 2022, MacDonald et al. 2016, Decocq et al. 2026 and the archive documentation; new prior-art search. Not checked: journal versions, the ten further density references, other outlier rows | Changes needed, headline items stand: 12 points. A bug made the density "control window" identical to the test window, reversing a stated conclusion; references were grouped by short name, which merged two "Mann et al. 2017" papers and hid a fourth affected reference; TICv8 rows diluted the stellar rates; a prior log g consistency rate (arXiv:2505.22205) was missed; claims with two labels; missing checksums. All addressed in the following commit. Status stays `result` |
