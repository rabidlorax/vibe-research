---
title: Fewest min/max operations to compute a median of 5, 7 or 9 values
domain: computer-science
status: proposed
evidence: conjecture
novelty: unchecked
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Fewest min/max operations to compute a median of 5, 7 or 9 values

## Question

What is the smallest number of two-input `min` and `max` operations in a
straight-line program (results may be reused any number of times) that
computes the median of n values, for n = 5, 7 and 9? By the threshold (0-1)
principle this equals the monotone Boolean circuit complexity of the majority
function MAJ_n over the basis {AND, OR}. An answer is, for each n, a verified
program of size s (upper bound) and a machine-checked refutation of size s-1
(lower bound); where the two cannot be made to meet, the best pair found.

A side question raised by the prior-art search: a 2022 catalogue of minimal
monotone circuits (B. A. Seidler, "Minimal circuits for Boolean functions of
few variables") reports that MAJ_5 needs 13 gates, while pruning the standard
7-comparator median-of-5 network appears to give 10. Which is right?

## Why it matters

Median-of-5, 7 and 9 kernels built from SIMD `min`/`max` instructions are the
inner loop of median filters in image and signal processing; one operation
saved is saved per pixel. The usual kernels are pruned comparator networks,
which never reuse a value in two comparators' worth of different partners
beyond what the network shape allows; general straight-line programs are a
larger class, and whether they can be smaller for these sizes is a concrete
question with a checkable answer. The exact values are also small data points
for monotone circuit complexity of majority.

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
