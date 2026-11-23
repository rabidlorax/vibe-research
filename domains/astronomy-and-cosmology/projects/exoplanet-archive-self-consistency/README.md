---
title: Internal consistency of planet and star parameters in the NASA Exoplanet Archive
domain: astronomy-and-cosmology
status: proposed
evidence: conjecture
novelty: unchecked
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Internal consistency of planet and star parameters in the NASA Exoplanet Archive

## Question

Each row of the NASA Exoplanet Archive's Planetary Systems table (`ps`) is
meant to be one published parameter set from one reference. Several of its
columns are tied together by exact physical or geometric identities: Kepler's
third law (period, semi-major axis, stellar mass), stellar surface gravity
(mass, radius), stellar density, the Stefan-Boltzmann law (luminosity, radius,
effective temperature), planet density (mass, radius), the radius ratio and
scaled semi-major axis, and the unit pairs (Earth and Jupiter units of the same
quantity). How often do rows that come from a single reference violate these
identities by more than their stated uncertainties allow, and which rows
violate them so badly that a transcription, unit, or ingestion error is the
likely cause?

An answer is: for each identity, the number of rows tested, the distribution of
the discrepancy, the fraction outside a stated tolerance, and a list of the
most discrepant rows that a reader can check against the cited papers.

## Why it matters

The archive is the default input for exoplanet population studies, and users
commonly combine columns (for example, deriving insolation or density
themselves). A measured error rate per identity tells them how far to trust
that, and a list of grossly inconsistent rows is something the archive's
maintainers can correct.

## Summary of result

Empty until there is one. State the headline claim in plain language, then its
evidence label. Negative and null results go here too.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 |       |          |              |

Evidence labels are defined in `docs/research-standards.md`. For a
`proved-formal` claim, "How to check" gives the Lean declaration name in
[rabidlorax/math](https://github.com/rabidlorax/math) as a permalink at the
full commit hash, that commit hash, and the axioms used.

## Method

What was done, in enough detail to redo it.

## Reproduction

Exact commands, from a clean checkout, that regenerate every number and figure.
State runtime and any network access needed.

## External data and what we could not reproduce

List every external dataset or published result relied on: source, version or
access date, licence. State plainly that the underlying measurements were not
and cannot be reproduced here. Write "None" if the project is self-contained.

## Prior work and novelty

What was searched (including alternative names for the same thing), on what
date and against which versions, and what was found. Leave `novelty: unchecked` in the
front matter until a real literature search has been done.

## Limitations and open questions

What could be wrong, what was not checked, and what would change the conclusion.

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
