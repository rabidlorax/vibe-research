---
title: Fewest min/max operations to compute a median of 5, 7 or 9 values
domain: computer-science
status: result
evidence: external-data
novelty: partially-known
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
saved is saved per pixel. The usual kernels are comparator networks with the
unused half-comparators removed. General straight-line programs are a larger
class (a value may feed any number of later operations, not just one
comparator), and whether they can be smaller for these sizes is a concrete
question with a checkable answer. The exact values are also small data points
for monotone circuit complexity of majority.

## Summary of result

Terms: a *program* is a sequence of operations `t = min(a, b)` or
`t = max(a, b)` whose operands are inputs or earlier results; its *size* is
the number of operations. "Gate" means the same thing in circuit language
(AND = min, OR = max).

- **Median of 5: exactly 10 operations** (`computed`). A 10-operation program
  is verified on every input ordering, and a SAT solver finds no program of
  any size from 1 to 9. The classical 7-exchange network, with unused
  half-exchanges removed, already has size 10, so reusing values buys nothing
  for five inputs.
- **The published catalogue is not minimal** (`external-data`). Seidler's
  catalogue of "minimal" monotone circuits for the 210 classes of monotone
  5-variable functions lists 13 gates for 5-input majority; the true minimum
  is 10. In total 19 of the 210 entries are larger than the minimum (table
  below). Every program in the catalogue is correct; the error is only in the
  claim of minimality. With the corrected values no 5-variable monotone
  function needs more than 10 gates, and 7 classes need exactly 10, so
  majority is not the unique hardest function as the paper states. The
  4-variable catalogue (30 classes) is confirmed minimal.
- **Median of 7: between 12 and 20 operations; median of 9: between 14 and 30**
  (`computed`). The upper bounds are the pruned classical networks. The lower
  bounds are SAT refutations of all smaller sizes. The question for 7 and 9 is
  **not settled**: 60 attempts to shorten the 20-operation median-of-7 program
  by one operation all failed, which is weak evidence and proves nothing.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | The program in `results/median5_10.txt` (10 operations) computes the median of 5 values | computed | `python src/verify.py results/median5_10.txt` (all 32 0/1 inputs, all 120 orderings, random inputs with ties) |
| 2 | No min/max program with 9 or fewer operations computes the median of 5 values | computed | `results/lower_bounds_5.log` (sizes 1 to 9 UNSAT); regenerate with `python src/lower_bounds.py 5 10`. Confirmed without any symmetry breaking (`results/median5_nosym_sizes1to8.log`, `results/median5_size9_nosym.log`); other cross-checks in Method |
| 3 | The programs obtained by pruning the classical exchange networks compute the medians of 5, 7, 9 values in 10, 20, 30 operations | computed | `python src/baseline.py`, then `python src/verify.py results/baseline_median*.txt` |
| 4 | No program with 11 or fewer operations computes the median of 7 values; none with 13 or fewer computes the median of 9 | computed | `results/lower_bounds_7.log`, `results/lower_bounds_9.log`; regenerate with `python src/lower_bounds.py 7 11` and `python src/lower_bounds.py 9 13`. Relies on the symmetry argument in Method |
| 5 | Of the 210 entries in Seidler's 5-variable monotone catalogue (as fetched 2026-11-23), all 210 listed programs compute the listed function, and exactly 19 use more gates than the minimum; the majority entry lists 13 and the minimum is 10 | external-data | `results/catalogue_check.csv`; regenerate with `./data/fetch_catalogue.sh` and `python src/catalogue_check.py data/raw/MonoCatFileA5var.txt out.csv`. The upper-bound half (a smaller circuit exists for each of the 19) needs no trust in the SAT solver: the circuits are in the CSV and are re-evaluated on all 32 inputs |
| 6 | Minimum monotone {AND, OR} circuit sizes of the 210 classes of 5-variable monotone functions are distributed as: 0 gates: 3 classes, 1: 2, 2: 4, 3: 10, 4: 26, 5: 16, 6: 45, 7: 32, 8: 51, 9: 14, 10: 7 | external-data | Same CSV. `external-data` only because the list of class representatives is taken from the catalogue rather than regenerated here |
| 7 | All 30 entries of Seidler's 4-variable monotone catalogue are minimal | external-data | `results/catalogue_check_4var.csv`, and independently `python src/cross_check.py` (brute force, no SAT solver) |

The entries of the 5-variable catalogue that are not minimal (catalogue
number is the catalogue's own identifier for the class representative):

| Catalogue number | Catalogue size | Minimum size |
|---|---|---|
| 65815 | 11 | 10 |
| 65823 | 9 | 8 |
| 66391 | 7 | 6 |
| 202623 | 10 | 9 |
| 460671 | 9 | 8 |
| 464767 | 11 | 10 |
| 472959 | 9 | 8 |
| 489343 | 7 | 6 |
| 1513343 | 11 | 10 |
| 1515391 | 10 | 8 |
| 1523583 | 9 | 8 |
| 18290559 (majority) | 13 | 10 |
| 18290687 | 11 | 10 |
| 18292735 | 11 | 10 |
| 18300927 | 10 | 9 |
| 18817023 | 9 | 8 |
| 125272063 | 7 | 6 |
| 125796351 | 9 | 8 |
| 394231807 | 11 | 10 |

The 10-operation median of 5 found by the solver (`results/median5_10.txt`;
inputs are nodes 0 to 4, operation i defines node 5+i):

```
t5  = min(x0, x1)     t6  = max(x0, x1)
t7  = min(x2, x3)     t8  = max(x2, x3)
t9  = max(t5, t7)     t10 = min(t6, t8)
t11 = min(x4, t10)    t12 = max(x4, t10)
t13 = max(t9, t11)    median = min(t12, t13)
```

## Method

**Reduction to Boolean circuits.** A min/max program computes a function that
commutes with every monotone map of the value domain. Applying the map "is
the value at least c" turns `min` into AND and `max` into OR, so a program
outputs the k-th largest of its inputs for all inputs if and only if, read as
an AND/OR circuit, it outputs 1 exactly on the 0/1 inputs with at least k
ones. (This is the 0-1 principle for sorting networks; it is used here as a
known fact, and `verify.py` also checks claims 1 and 3 directly on all
orderings without it.) So the question is the monotone circuit size of the
threshold function, majority when k = (n+1)/2.

**SAT encoding** (`src/encode.py`). For a given size s, variables choose each
gate's type and two operands among earlier nodes, and per input row give each
gate a value. A monotone circuit computes a monotone function, so it computes
majority iff it outputs 0 on every input with k-1 ones and 1 on every input
with k ones; only those rows are encoded (20 for n=5, 70 for n=7, 252 for
n=9). For general monotone functions the rows are the minimal true points and
maximal false points.

**Symmetry breaking and why it loses nothing.** The lower bounds use extra
constraints. They are justified as follows; this is a written argument, not a
machine-checked one, and the lower-bound claims depend on it.

Take a circuit of the smallest possible size s. Every gate has a path to the
output (otherwise delete it), so the output is the only gate nobody uses and
comes last in any valid numbering. Among all ways to (i) number the gates in
an order where operands precede users and (ii) rename the input variables,
pick one whose sequence of operand pairs (b, a) with a < b, listed gate by
gate, is lexicographically smallest, comparing pairs by b first.

1. *Consecutive gates are in non-decreasing pair order.* If gate g+1 had a
   smaller pair than gate g, its larger operand would be below g, so it does
   not use g; swapping the two is a valid numbering with a smaller sequence.
   Two consecutive gates with the same pair can be swapped freely, so AND can
   be put first; two gates with the same pair and type would be duplicates,
   impossible in a smallest circuit. (Constraint level `sym=1`; valid for any
   function.)
2. *The first gate is AND(x0, x1)* (majority only). The first gate's operands
   are inputs, and the smallest pair is (1, 0). If it is OR, swap AND and OR
   throughout: the result computes the dual function, and majority of an odd
   number of inputs is its own dual. Pairs are unchanged. (`sym=2`.)
3. *Input i+1 is not used before input i* (symmetric functions only). If gate
   g is the first to use i+1, and i is used neither earlier nor as g's smaller
   operand, then exchanging the names i and i+1 leaves earlier gates unchanged
   and makes g's pair smaller. (`sym=3`.)

Because the constraints assume a smallest circuit, UNSAT at size s excludes
only size exactly s. `lower_bounds.py` therefore runs every size from 1 up.

**Cross-checks of the lower bounds.**

- Two solvers (CaDiCaL 1.5.3 and Glucose 4, as shipped in PySAT) agree on
  sizes 1 to 10 for n = 5 (`results/lower_bounds_5*.log`).
- With no symmetry breaking at all (`--sym 0`), sizes 1 to 8 for n = 5 are
  UNSAT (`results/median5_nosym_sizes1to8.log`), and so is size 9
  (`results/median5_size9_nosym.log`, 1069 s). So claim 2 does not depend on
  the symmetry argument; claim 4 does.
- The catalogue run uses only `sym=1` and independently gives 10 for majority.
- `src/brute_force.py` enumerates all circuits without any SAT solver or
  encoding: every 4-variable class (up to 7 gates) and every 5-variable class
  with minimum at most 5 gates agrees exactly, and no 5-variable class with a
  larger SAT minimum is reachable in 5 gates (`python src/cross_check.py`:
  28 + 59 classes agree, 149 correctly unreachable).
- In all 210 + 30 catalogue classes the SAT minimum is at most the size of
  the catalogue's own circuit, as it must be if the encoding does not
  over-constrain; in 221 of the 240 it is equal.

No UNSAT proof certificate (DRAT) was produced or checked. The brute-force
check does not reach 9 gates on 5 inputs, so claim 2 at size 9 rests on the
solvers alone (two solvers with symmetry breaking, one without).

**Catalogue comparison** (`src/catalogue_check.py`). For each entry: parse the
listed true points and straight-line program (gate type 1 = AND, 5 = OR in
the catalogue's notation), evaluate the program on all 32 inputs, then find
the minimum by SAT for sizes 1, 2, ... The circuit found is re-evaluated on
all 32 inputs by code separate from the encoder.

**Upper-bound attempts for 7 and 9** (`src/local_improve.py`). Keep a random
predecessor-closed set of 11 of the 20 gates of the pruned median-of-7
network and ask for any completion with 8 more gates (19 total). 60 random
choices, all UNSAT (`results/local7_keep11.log`). What did not work: plain
SAT search for a median-of-7 program of size 18, 19 or 20 returned nothing in
about 15 minutes each before being stopped, even at 20 where a solution is
known to exist, and the same with two or three disjoint comparators fixed as
the first gates; local search keeping only 8, 9 or 10 gates, and the
analogous search for 9 inputs keeping 21 of 30, hit the conflict budget or
were stopped after about 10 minutes without a result. Logs of these stopped
runs were not kept. So the method as implemented cannot say whether 19 (or 29) is
possible.

## Reproduction

```bash
pip install -r requirements.txt     # python-sat 1.9.dev24; Python 3.13 used
./run_all.sh                        # regenerates everything in results/
```

`run_all.sh` lists each step with its approximate runtime (4 cores, Intel
Xeon 2.10 GHz, 15 GB). Totals: everything except the last three steps takes
about 45 minutes, most of it the 5-variable catalogue. The last sizes of the
lower-bound runs took 60 s (n=7, size 11) and 1146 s (n=9, size 13).
Network is needed only by `data/fetch_catalogue.sh`. Solver runs are
deterministic; `local_improve.py` takes its random seed on the command line
(seed 11 was used). Timings were taken while other jobs shared the machine
and vary by a factor of about two.

The quick core of the result (claims 1 to 3) takes under a minute:

```bash
cd src
python lower_bounds.py 5 10
python search.py 5 10 --out ../results/median5_10.txt && python verify.py ../results/median5_10.txt
python baseline.py && python verify.py ../results/baseline_median*.txt
```

## External data and what we could not reproduce

- B. A. Seidler, "Minimal circuits for Boolean functions of few variables",
  manuscript dated March 20, 2022,
  <https://sites.math.rutgers.edu/~bas312/Research/slp/SLP.pdf>, and its
  catalogue files `MonoCatFileA4var.txt` and `MonoCatFileA5var.txt` in the
  same directory. Accessed 2026-11-23. No licence is stated, so the files are
  not committed; `data/fetch_catalogue.sh` fetches them and
  `data/catalogue.sha256` records the checksums of the copies used.
- This is a computed catalogue, not a measurement. We did not rerun the
  author's Maple code. Claims 5, 6 and 7 are statements about the files as
  fetched on that date and fall if the files differ from what the author
  intended or are later changed. Claim 6 additionally trusts the catalogue's
  list of 210 class representatives to be complete (the count 210 agrees with
  the number of monotone 5-variable functions up to permutation of variables,
  OEIS A003182, `[from memory, unverified]`).
- Quoted from the paper, so the comparison is exact. Abstract: "we produce
  minimum-size circuits for every Boolean function of four or fewer variables
  and every monotone Boolean function of five variables." Results: "among the
  5-variable functions, 18290559 requires 13 gates while no other function
  requires more than 11 [...] this is the majority function on five
  variables". The paper's Table 5 row for 5 variables (3, 2, 4, 10, 26, 16,
  42, 35, 44, 18, 3, 6, 0, 1 classes at 0 to 13 gates) matches a count of the
  gates in the fetched file, so the file is the one the paper describes.
- Known problems: the discrepancy reported here. We do not know its cause;
  the paper's description of its search was not analysed. The author has not
  been contacted. This is a documented inconsistency in a manuscript, not a
  comment on its author.
- The classical exchange networks in `src/baseline.py` (7, 13 and 19
  exchanges, usually attributed to Paeth and to Devillard's `opt_med`
  routines) were typed `[from memory, unverified]` as to source and
  attribution. Their correctness does not depend on the source: claim 3 is
  checked exhaustively.

## Prior work and novelty

Searched on 2026-11-23, before the work, with a general web search engine
(nine queries) plus the arXiv API and OEIS search:

- Terms: "exact monotone circuit complexity majority 5 7 9"; "median of 9
  minimum number of min/max operations"; "optimal selection networks median
  SAT lower bound"; "monotone complexity threshold function T_3^5"; "median
  of 7 / 9 min max straight-line program superoptimization"; "majority seven
  variables monotone circuit AND OR exact synthesis MAJ7 T_4^7"; "MAJ_5
  exactly 10 gates"; "Knuth 7.1.2 Boolean chains median of five monotone".
  Alternative names covered: majority, median, threshold function T_k^n,
  selection network, monotone Boolean chain, min/max network.
- Found and read: Seidler's manuscript (above), which is the only source
  found that states an exact monotone {AND, OR} size for 5-input majority,
  and states 13.
- Found in results but not read (titles only, so nothing is claimed about
  their content): Haaswijk and De Micheli and Testa et al. on exact synthesis
  of majority-n from majority-of-3 gates (a different basis); Kulikov et al.,
  "SAT-based Circuit Local Improvement" (arXiv 2102.12579); Hoory and Magen,
  "Monotone circuits for the majority function" (asymptotic); "Towards
  Simpler Sorting Networks and Monotone Circuits for Majority" (arXiv
  2310.12270, asymptotic); a 2025 SEA paper on exact comparison counts for
  selection (adaptive comparisons, a different model).
- Not found in this search: a statement that 10 is the exact monotone circuit
  size of 5-input majority; exact values or SAT lower bounds for 7 or 9
  inputs in the {AND, OR} basis; any note that the Seidler catalogue is not
  minimal. Knuth's *The Art of Computer Programming* 7.1.1 and 7.1.2 are an
  obvious place for the 5-input value and could not be read here (not openly
  accessible), so it may well be recorded there.

What is known: the 10-, 20- and 30-operation programs (upper bounds) are
classical. What was not found elsewhere: the matching lower bound for 5, the
lower bounds for 7 and 9, and the 19 corrections to the catalogue. Hence
`partially-known`. The search was a few hours' work by a model, not a
specialist's survey.

## Limitations and open questions

- The lower bounds depend on SAT solvers reporting UNSAT with no certificate
  checked, and on the written symmetry argument. Producing DRAT proofs and
  checking them with an independent checker, or a Lean-checked certificate in
  the math repository, would remove both. Not done.
- Sizes for 7 and 9 inputs are open: 12 to 20 and 14 to 30. The lower bounds
  are far from the upper bounds and say little. Each extra size costs roughly
  ten to twenty times more solver time (n=9: 10 s, 68 s, 1146 s for sizes 11,
  12, 13). Size 12 for n=7 and size 14 for n=9 were started and did not
  finish: the n=7 size-12 run was stopped after more than 30 minutes on a
  shared machine, the n=9 size-14 run after a few minutes.
- The failed local search is not evidence of optimality of 20: it only
  explored completions of 11-gate subsets of one particular program.
- Only single-output programs are covered. Median filters over sliding
  windows share work between neighbouring windows; that is a different
  problem.
- Operation count is not speed. Depth, register pressure and instruction
  latency matter in practice and are not studied.
- Claim 6 covers classes under permutation of variables only, as in the
  catalogue.
- No source fetched for this project contained instructions addressed to an
  AI or other manipulation attempts.
- "Claim on `main`": the session could push only to its own branch while
  working, so the claim commit reached `main` together with the result, by
  permission of the repository owner.

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
