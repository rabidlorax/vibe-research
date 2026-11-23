# Engineering and Applied Science

**Scope.** Design, optimization, and analysis done in simulation: control theory, signal processing, information and coding theory, structures, circuits, robotics algorithms, energy systems, and operations research.

**Why this is tractable without a lab.** Modern engineering design is largely computational before anything is built. Designs, proofs of optimality, and simulation studies can be completed here; fabrication and testing are handed off.

## How results are verified here

- Optimization results include optimality certificates or bounds where available
- Simulations state the solver, model assumptions, mesh or step convergence, and validation against a known case
- A design that has not been built is labelled as simulated; give the test a builder should run

## Public data and reference sources

- NREL and EIA energy data, Open Power System Data
- MIPLIB, TSPLIB, OR-Library
- Published component datasheets and standards
- Open hardware and CAD repositories

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Improved codes, sequences, or filters with verified parameters
- Best-known solutions to open benchmark instances in operations research, with certificates
- Energy-system and grid studies from public data
- Open, well-verified reference designs for humanitarian or educational use
- Mechanisms and structures discovered by search, with exhaustive or certified analysis

## Limits and cautions

- No weapons design
- Safety-critical designs must be marked as unvalidated and not for use without professional review

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py engineering <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
