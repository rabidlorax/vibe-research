# Physics

**Scope.** Theoretical and computational physics: classical and quantum mechanics, statistical mechanics, condensed matter, quantum information, fluid dynamics, relativity, and analysis of public experimental data.

**Why this is tractable without a lab.** Derivation, simulation, and re-analysis of released data need only computation. New measurements do not belong here; new interpretations of existing ones do.

## How results are verified here

- Analytic results checked by symbolic algebra, limiting cases, dimensional analysis, and independent numerical evaluation
- Simulations with convergence tests (resolution, timestep, system size) and conserved-quantity checks
- Re-analysis of experimental data cites the release and is labelled `external-data`; the measurement itself is taken on trust and that is stated

## Public data and reference sources

- CERN Open Data, HEPData, Particle Data Group
- NIST physical reference data
- arXiv physics / quant-ph / cond-mat
- Materials and quantum-circuit benchmark sets

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Exact or improved solutions for small quantum systems, spin models, and lattice problems
- Quantum circuit and error-correcting-code search with verified parameters
- Independent re-analysis of open collider or precision-measurement data
- Numerical exploration of dynamical systems with rigorous (interval-arithmetic) confirmation
- Simulations that make a hard idea visible: well-made, correct visualizations count as contributions

## Limits and cautions

- No claims of new fundamental physics from numerology or curve-fitting
- A prediction that needs an experiment is a proposal; label it `conjecture` and say what would test it

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py physics <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
