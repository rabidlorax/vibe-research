# Neuroscience and Cognitive Science

**Scope.** Computational and theoretical neuroscience, analysis of open neural and behavioural datasets, and quantitative models of perception, learning, and decision-making.

**Why this is tractable without a lab.** Open recordings and behavioural datasets are plentiful, and theory in this field is computational by nature.

## How results are verified here

- Preprocessing choices are stated and varied to show robustness
- Model comparison uses held-out data, with parameter-recovery checks
- Results from recordings are `external-data`

## Public data and reference sources

- OpenNeuro, DANDI Archive, Allen Brain Atlas / Brain Observatory
- International Brain Laboratory data
- Human Connectome Project (under its terms)
- OSF-hosted behavioural datasets, Psych-DS

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Re-analysis of open datasets to test published claims with alternative pipelines
- Normative and mechanistic models of behaviour fit to public data
- Theory of neural network dynamics and coding with proofs or simulations
- Comparisons between artificial and biological representations, with careful controls

## Limits and cautions

- Large imaging datasets may exceed container disk and compute; subsample transparently
- Avoid reverse inference and overreading of small-sample effects

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py neuroscience-and-cognitive-science <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
