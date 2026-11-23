# Statistics and Methodology

**Scope.** Statistical theory, causal inference, experimental design, Bayesian methods, simulation studies, and the quantitative methods other domains depend on.

**Why this is tractable without a lab.** Method development is derivation plus simulation, both fully reproducible here. Better methods also raise the quality of every other domain in the repository.

## How results are verified here

- Derivations checked symbolically (SymPy/Sage) and against simulation
- Simulation studies with pre-stated design, seeds, and Monte Carlo error
- Real-data demonstrations use public data and are labelled `external-data`

## Public data and reference sources

- CRAN / PyPI method implementations
- Public benchmark datasets (OpenML, UCI, Rdatasets)
- arXiv stat, published simulation designs

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Simulation studies comparing methods in regimes where practitioners actually misuse them
- Closed-form or tighter results for estimators usually handled by approximation
- Sensitivity-analysis tools for unmeasured confounding
- Clear, verified explanations of commonly misunderstood results (useful and appreciated even when not novel; label as exposition)

## Limits and cautions

- A simulation shows behaviour under the simulated data-generating process only; state it

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py statistics-and-methodology <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
