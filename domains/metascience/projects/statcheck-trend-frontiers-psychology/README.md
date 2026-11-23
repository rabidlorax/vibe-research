---
title: Trend in statistical reporting inconsistencies in an open-access psychology journal, 2010 to 2026
domain: metascience
status: active
evidence: conjecture
novelty: unchecked
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Trend in statistical reporting inconsistencies in an open-access psychology journal, 2010 to 2026

## Question

Among articles in the open-access journal *Frontiers in Psychology* with
machine-readable full text, what fraction of null-hypothesis test results
reported in the standard form (a t, F, chi-square, r or z statistic with its
degrees of freedom and a p-value) give a p-value that does not match the one
recomputed from the reported statistic and degrees of freedom, for each
publication year from 2010 to 2026? Has that fraction, and the fraction of
mismatches that change the verdict at the 0.05 level, gone up, gone down, or
stayed the same over that period?

An answer is a table by publication year of: articles sampled, articles with
at least one extractable result, results extracted, the share of results that
are inconsistent, the share that are decision-changing, and the share of
articles with at least one of each, with confidence intervals that account for
results clustering within articles; a trend estimate with its uncertainty; and
a hand-checked sample of the automated flags with the false-positive rate.

The scope may be narrowed or a second journal added once the prior-art search
and a feasibility check of the full-text source are done; any change will be
recorded here before the analysis is run.

## Why it matters

A widely cited 2016 study using the `statcheck` program found that about half
of psychology articles from 1985 to 2013 contained at least one p-value that
did not match its test statistic `[from memory, unverified; to be checked in
the prior-art search]`. Since then the field has gone through a decade of
reform aimed at more careful reporting, some journals run automated checks at
submission, and writing tools have changed. Whether reporting accuracy in the
published record has actually improved is an empirical question that authors,
editors and readers of this literature have a stake in, and it can be answered
from public full text with a few thousand lines of arithmetic.

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
