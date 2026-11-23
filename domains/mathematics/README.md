# Mathematics

**Scope.** Pure and experimental mathematics: combinatorics, number theory, graph theory, algebra, analysis, geometry, probability, and recreational mathematics.

**Why this is tractable without a lab.** Mathematics is the field where the work product (a proof, a construction, a counterexample, a computed table) can be checked completely inside this repository. No physical apparatus is ever required.

## How results are verified here

- Formal proof in Lean 4 / Coq / Isabelle (strongest; label `proved-formal`)
- Written proof with every step explicit, independently re-derived by a second model session (`proved-informal`)
- Exhaustive or certified computation with code in `src/` (`computed`); SAT/SMT results ship with a checkable certificate (DRAT, LRAT) where possible
- Numerical evidence is evidence, never proof: label it `conjecture`

## Public data and reference sources

- OEIS (sequences, cross-references)
- Lean mathlib, Archive of Formal Proofs
- LMFDB (L-functions, modular forms, elliptic curves)
- House of Graphs, Erdős problem lists, Open Problem Garden
- arXiv math

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Formalize a published but not-yet-formalized theorem and report any gaps found in the original proof
- Improve a known bound or extend a table for a small combinatorial object (Ramsey-type numbers, covering designs, packing problems, cap sets) via search plus certificate
- Extend or find new formulas / proofs for OEIS sequences flagged as lacking them
- Counterexample searches for small-case conjectures in graph theory
- Recreational results people enjoy: new tilings, puzzles with proven optimal solutions, elegant visual proofs

## Limits and cautions

- A claim of having resolved a famous open problem requires a formal proof before the status may be anything other than `conjecture`
- Check the literature and OEIS before claiming novelty; many 'new' identities are classical

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py mathematics <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
