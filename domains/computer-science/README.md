# Computer Science

**Scope.** Algorithms and data structures, complexity theory, programming languages, formal verification of software, distributed systems, databases, and defensive security.

**Why this is tractable without a lab.** Everything here is either a proof or a program, and programs can be run, benchmarked, fuzzed, and verified in a container.

## How results are verified here

- Correctness proofs (mechanized where feasible); model checking with TLA+ / Alloy
- Benchmarks with fixed seeds, pinned dependencies, stated hardware, and scripts that regenerate every number
- Differential testing and fuzzing against reference implementations
- Asymptotic claims need a proof; empirical speedups need the benchmark

## Public data and reference sources

- DBLP, arXiv cs
- SAT/SMT competition benchmarks, SV-COMP
- Public source code and its bug trackers
- Complexity Zoo, published lower-bound surveys

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Verified implementations of algorithms that only have paper proofs
- New or simpler algorithms for well-specified problems, with proofs and benchmarks against the state of the art
- Model-check published distributed protocols and report violations or confirm safety within stated bounds
- Superoptimization and automatically discovered small programs (sorting networks, bit tricks, peephole rules) with exhaustive verification
- Bug-finding studies in open-source software, reported upstream through responsible disclosure

## Limits and cautions

- Security work is defensive only: no weaponized exploits, no detection evasion, vulnerabilities are disclosed to maintainers before publication here
- Benchmarks run in a shared cloud container are noisy; say so and report variance

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py computer-science <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
