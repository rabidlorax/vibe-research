# Astronomy and Cosmology

**Scope.** Stellar, galactic, and planetary astronomy, exoplanets, gravitational waves, cosmology, and celestial mechanics, using archival survey data and simulation.

**Why this is tractable without a lab.** Astronomy has perhaps the richest open archives of any science; much of the sky has been observed and far from all of it has been looked at closely.

## How results are verified here

- Pipelines run end-to-end from the public archive query to the figure
- Detections report false-alarm probability and injection-recovery tests
- Cross-check against existing catalogues before claiming a new object
- All observational results are `external-data`: we did not take the observations

## Public data and reference sources

- Gaia, SDSS, Pan-STARRS, ZTF public releases
- MAST (Kepler, TESS, HST, JWST)
- NASA Exoplanet Archive
- GWOSC (LIGO/Virgo/KAGRA open strain data)
- Planck / ACT legacy archives, JPL Horizons, Minor Planet Center

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Searches for overlooked transits, eclipsing binaries, or variable stars in TESS / Kepler light curves
- Stellar streams, co-moving groups, and unusual objects in Gaia
- Independent re-analysis of gravitational-wave events from open strain data
- Long-term N-body stability studies of known exoplanet systems
- Orbit and ephemeris calculations of public interest (eclipses, conjunctions, close approaches) with stated uncertainty

## Limits and cautions

- Candidate detections stay `conjecture` until followed up by observers; say what observation would confirm them
- Archive downloads may be blocked by this environment's network policy; record the exact query so others can rerun it

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py astronomy-and-cosmology <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
