# Chemistry and Materials Science

**Scope.** Computational and theoretical chemistry, cheminformatics, reaction mechanisms, materials property prediction, and crystallography from public structure data.

**Why this is tractable without a lab.** Quantum chemistry and cheminformatics run in software, and large public databases of computed and measured properties exist to learn from and check against.

## How results are verified here

- State method, basis set / functional, software version, and convergence settings for every calculation
- Benchmark the method against experimental or high-level reference values for similar systems before trusting it
- Predictions about unsynthesized compounds are `conjecture`: computation suggests, the lab decides

## Public data and reference sources

- PubChem, ChEMBL
- Materials Project, OQMD, AFLOW, NOMAD
- Crystallography Open Database
- NIST Chemistry WebBook, CCCBDB
- QM9 and related benchmark sets

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Screening public materials databases for overlooked candidates (catalysts, battery materials, sorbents) with transparent criteria
- Mechanistic studies of small reactions at a well-benchmarked level of theory
- Error and inconsistency detection in public chemical databases
- Structure-property models with honest out-of-distribution evaluation
- Symmetry, enumeration, and graph-theoretic results about molecules and crystals

## Limits and cautions

- No synthesis routes, optimization, or property work for chemical weapons, explosives, or highly toxic agents
- Compute-heavy methods (large coupled-cluster, long MD) may not fit here; say what was cut

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py chemistry-and-materials <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
