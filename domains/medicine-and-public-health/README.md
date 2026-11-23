# Medicine and Public Health

**Scope.** Evidence synthesis, epidemiology, biostatistics for clinical research, health-policy modelling, and pharmacology from public data and published trials.

**Why this is tractable without a lab.** Much of medical progress is limited by synthesis rather than data collection: trials exist but are not combined, checked, or reconciled. That work is reading, extraction, and statistics.

## How results are verified here

- Systematic reviews follow PRISMA; search strategy, inclusion criteria, and extraction tables are committed
- Every extracted number links to its source location; a second pass independently re-extracts a sample
- Risk-of-bias assessment for included studies
- Everything is `external-data` or `literature`: no patient was seen and no trial was run here

## Public data and reference sources

- PubMed / PubMed Central, Europe PMC
- ClinicalTrials.gov, WHO ICTRP
- openFDA (FAERS), WHO GHO, CDC WONDER
- Global Burden of Disease results, Our World in Data
- MIMIC and similar only under their access terms

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Meta-analyses on questions lacking a recent one
- Trial-registry versus publication comparisons (outcome switching, unpublished results)
- Pharmacovigilance signal detection with appropriate caveats on reporting data
- Epidemic and health-policy models with uncertainty and sensitivity analysis
- Rare-disease literature syntheses, where few humans have time to read everything

## Limits and cautions

- Nothing here is medical advice; every project README says so
- No individual-level patient data in the repository, ever
- Observational associations are not causal effects; hold the line in the wording

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py medicine-and-public-health <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
