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

Mathematics is not a domain here, and this repository holds no Lean code. All
mathematics, and every proof needed by a project in any domain, goes in
<https://github.com/rabidlorax/math>. A proof specific to one project
goes in that repository's `MathApplied/<Domain>/<Project>/` (CamelCase of the
domain and project slug here). The project cites the theorem by Lean
declaration name, commit hash, axioms, and a permalink pinned to that full
commit hash. Never link to a branch of the math repository. See "Proofs live
in the math repository" in `docs/research-standards.md`.

## Commands

- New project: `python scripts/new_project.py <domain> <slug> "Title"`
- Validate and refresh index: `python scripts/check_repo.py --write-index`
  (run before every commit; CI runs the same check)

## Before starting, and when finishing

Full rules are in "Claiming work and independent review" in
`docs/research-standards.md`.

- **Claim first.** Fetch `main` and check `PROJECTS.md`, open pull requests
  and branches for the same question. If nobody has it, scaffold the project,
  write the Question, leave `status: proposed`, and get that commit onto
  `main` before researching. Earliest claim on `main` wins.
- **Do not duplicate.** If a `proposed` or `active` project covers the
  question, join it or pick another. A project untouched for 14 days with no
  live branch may be taken over, noted in its review log.
- **Stay in your folder.** Research commits touch only your project. Changes
  to shared files go in their own commit.
- **Stop at `result`.** Review is done by a different session working from
  the repository alone, or by a human. The reviewer sets `verified` or
  `refuted` and logs what they checked.
- **Nothing to do?** Review the oldest project at `result`.

## Rules

- Every claim gets an evidence label. Do not label above what was actually
  done: code that was not run is not `computed`, a proof sketch is not
  `proved-informal`.
- Run the code. Paste real output. If something could not be run (network
  blocked, too slow), say so in the README instead of describing expected
  output.
- Never fabricate a citation, dataset, number, or quotation. Mark anything
  recalled but not retrieved as `[from memory, unverified]`.
- Formalize proofs. `proved-informal` is a temporary label, not an end state.
- Do the prior-art search before starting the work and report what it finds.
  Search alternative names, and date every "not found" statement.
- Leave `novelty: unchecked` unless you searched and documented the search.
- Any use of external data requires the disclaimer section filled in.
- Never set `status: verified` on a project you authored. That status is set
  by an independent reviewer and recorded in the review log.
- When a result turns out wrong, set `status: refuted`, explain, and keep the
  project. Do not delete or quietly rewrite history.
- Add your model ID to the `models` list in the project front matter and bump
  `updated`. Do not put model IDs in commit messages or code comments.
- Everything committed is released under CC0 (`LICENSE`). Do not commit
  third-party data or text that cannot be; commit the fetch script and record
  the source's licence.
- Stay inside the limits in "What we will not do". If a project idea is near
  one, write down the boundary in its README before starting.
- A new domain needs a `README.md` with the same sections as the existing ones
  and a row in the top-level `README.md` table.

## Choosing work

Prefer questions that are well-posed, where an answer can be checked cheaply,
and where a person would care about the answer. A small result that is
certainly right beats a large one that is probably right.
