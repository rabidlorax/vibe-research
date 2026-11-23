---
title: Fewest voters for which five textbook voting rules elect five different winners
domain: economics-and-social-science
status: proposed
evidence: conjecture
novelty: unchecked
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Fewest voters for which five textbook voting rules elect five different winners

## Question

Take an election with `m` candidates in which each of `n` voters submits a
strict ranking of all candidates. Apply five rules found in introductory
textbooks to the same ballots:

1. **Plurality**: most first places.
2. **Plurality with runoff**: the two candidates with the most first places
   go to a pairwise majority contest.
3. **Sequential elimination** (Hare, instant runoff): repeatedly delete the
   candidate with the fewest first places among those remaining.
4. **Borda count**: `m-1` points for a first place down to 0 for last.
5. **Condorcet**: the candidate who beats every other in pairwise majority
   contests.

A widely reproduced classroom example with 55 voters and 5 candidates makes
the five rules elect five different candidates. **What is the smallest `n`
for which this can happen with `m = 5`, when no tie occurs at any step that
decides an outcome?** An answer is a number `n*`, a profile with `n*` voters
that anyone can check by hand, and an exhaustive argument that no profile
with fewer voters works. Secondary questions, if the main one is settled:
the same minimum for every subset of the five rules, for `m = 6`, and when
ties are allowed but must not affect which candidates could win.

## Why it matters

The 55-voter example is a standard way to teach that the choice of voting
rule can decide an election. A smallest possible example is easier to check
by hand and to put on a blackboard, and knowing the exact minimum says how
few voters are needed before the five rules can fully disagree.

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
