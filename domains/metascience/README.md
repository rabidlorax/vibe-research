# Metascience

**Scope.** Research on research: reproducibility, error detection in the published literature, citation analysis, literature synthesis, and the study of AI-conducted research itself.

**Why this is tractable without a lab.** Checking published work for internal consistency at scale is tedious for humans and natural for models. This domain also turns the lens on this repository.

## How results are verified here

- Automated flags are hand-verified on a sample, with the false-positive rate reported
- Claims of error in a specific paper are stated precisely and conservatively, with the exact passage quoted, and are raised with the authors where practical
- Corpus-level statistics give corpus definition and sampling frame

## Public data and reference sources

- OpenAlex, Crossref, Semantic Scholar
- arXiv and PubMed Central open-access full text
- Retraction Watch database
- OSF, replication-project datasets

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Statistical-consistency checks (GRIM, statcheck-style) across open-access corpora
- Citation-accuracy audits: does the cited paper say what it is cited for?
- Mapping contradictory findings in a literature and what distinguishes them
- Audits of this repository: how often do our own `computed` and `proved-informal` claims survive independent re-checking?
- Finding 'undiscovered public knowledge': connections between literatures that do not cite each other

## Limits and cautions

- Criticism targets claims, not people; no allegations of misconduct, only documented inconsistencies
- An inconsistency is not necessarily an error; allow for typos and reporting conventions

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py metascience <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
