---
title: Exhaustive accuracy of NumPy float32 math functions over all 2^32 inputs
domain: computer-science
status: proposed
evidence: conjecture
novelty: unchecked
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Exhaustive accuracy of NumPy float32 math functions over all 2^32 inputs

## Question

For each unary float32 math function that NumPy computes with its own SIMD
code or with its bundled copy of Intel SVML (exp, log, sin, cos, tan, the
inverse and hyperbolic functions, and relatives), what is the exact worst-case
error in ULPs, and the exact number of inputs that are not correctly rounded,
taken over **every one of the 2^32 float32 bit patterns**, for a stated NumPy
build on a stated CPU? Secondary: are the results free of monotonicity
violations and out-of-range values, and do they depend on where an element
sits in the array?

An answer is a table per function (worst error, worst input, count of
misrounded inputs) that anyone can regenerate with one command, with the
reference values proved correct by a rounding test rather than assumed.

## Why it matters

NumPy's documentation and the pull requests that added these loops state
error bounds ("up to 4 ULP") that come from the vendor or from sampled tests.
float32 is small enough to check completely, so the bound can be replaced by
the true worst case. People who rely on float32 results (reproducibility
across machines, rotations built from sin/cos, values that must stay inside
[-1, 1]) can then see exactly what they get.

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
