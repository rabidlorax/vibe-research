# Economics and Quantitative Social Science

**Scope.** Economic theory, econometrics, game theory, mechanism design, social choice, demography, and empirical social science from public data.

**Why this is tractable without a lab.** Theory here is mathematics, and much empirical work rests on public statistical releases and replication packages that can be rerun.

## How results are verified here

- Theoretical results are proved, and labelled `proved-formal` or `proved-informal` per `docs/research-standards.md`
- Empirical work commits a pre-analysis plan before looking at outcomes, and reports all specifications run
- Identification assumptions are stated explicitly and stress-tested
- Replications start from the authors' replication package where one exists

## Public data and reference sources

- FRED, BLS, BEA, Eurostat, OECD, World Bank, IMF
- IPUMS, national census releases
- Penn World Table
- Journal replication archives (AEA, Harvard Dataverse, ICPSR open collections)

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Computational replication and robustness checks of influential empirical papers
- New results in mechanism design, matching, voting theory, and fair division, including formalized proofs
- Agent-based and structural models with transparent calibration
- Demographic projections with proper uncertainty

## Limits and cautions

- Descriptive and causal claims only; normative conclusions are outside the 'objective' remit and are kept out of results
- No forecasts presented as investment advice
- Aggregate data only: no attempts to identify individuals

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py economics-and-social-science <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
