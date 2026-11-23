# Working in this repository

This repository holds original research done by Claude models. Read
`docs/research-standards.md` before making or changing any research claim; it
is binding. The points below are the ones most often needed.

## Layout

- `domains/<domain>/README.md`: scope, verification standard, data sources,
  and cautions for that field. Read the one you are working in.
- `domains/<domain>/projects/<slug>/`: one project. `README.md` (from
  `templates/project-README.md`), `src/`, `data/`, `results/`.
- `PROJECTS.md`: generated index. Never edit by hand.

## Commands

- New project: `python scripts/new_project.py <domain> <slug> "Title"`
- Validate and refresh index: `python scripts/check_repo.py --write-index`
  (run before every commit; CI runs the same check)

## Rules

- Every claim gets an evidence label. Do not label above what was actually
  done: code that was not run is not `computed`, a proof sketch is not
  `proved-informal`.
- Run the code. Paste real output. If something could not be run (network
  blocked, too slow), say so in the README instead of describing expected
  output.
- Never fabricate a citation, dataset, number, or quotation. Mark anything
  recalled but not retrieved as `[from memory, unverified]`.
- Leave `novelty: unchecked` unless you searched and documented the search.
- Any use of external data requires the disclaimer section filled in.
- Do not set `status: verified` on your own work in the same session. That
  status needs an independent review recorded in the review log.
- When a result turns out wrong, set `status: refuted`, explain, and keep the
  project. Do not delete or quietly rewrite history.
- Add your model ID to the `models` list in the project front matter and bump
  `updated`. Do not put model IDs in commit messages or code comments.
- Stay inside the limits in "What we will not do". If a project idea is near
  one, write down the boundary in its README before starting.
- A new domain needs a `README.md` with the same sections as the existing ones
  and a row in the top-level `README.md` table.

## Choosing work

Prefer questions that are well-posed, where an answer can be checked cheaply,
and where a person would care about the answer. A small result that is
certainly right beats a large one that is probably right.
