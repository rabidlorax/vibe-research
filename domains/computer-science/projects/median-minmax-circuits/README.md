---
title: Fewest min/max operations to compute a median of 5, 7 or 9 values
domain: computer-science
status: result
evidence: external-data
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-24
---

# Fewest min/max operations to compute a median of 5, 7 or 9 values

## Question

What is the smallest number of two-input `min` and `max` operations in a
straight-line program (results may be reused any number of times) that
computes the median of n values, for n = 5, 7 and 9? By the threshold (0-1)
principle this equals the monotone Boolean circuit complexity of the majority
function MAJ_n over the basis {AND, OR}. An answer is, for each n, a verified
program of size s (upper bound) and a SAT-solver refutation of size s-1
(lower bound); where the two cannot be made to meet, the best pair found.

A side question raised by the prior-art search: a 2022 catalogue of minimal
monotone circuits (B. A. Seidler, "Minimal circuits for Boolean functions of
few variables") reports that MAJ_5 needs 13 gates, while pruning the standard
7-comparator median-of-5 network appears to give 10. Which is right?

## Why it matters

Median-of-5, 7 and 9 kernels built from SIMD `min`/`max` instructions are
used as the inner loop of median filters in image and signal processing, so
one operation saved is saved per pixel; the usual kernels are comparator
networks with the unused half-comparators removed `[both statements about
practice are from memory, unverified; no claim depends on them]`. General straight-line programs are a larger
class (a value may feed any number of later operations, not just one
comparator), and whether they can be smaller for these sizes is a concrete
question with a checkable answer. The exact values are also small data points
for monotone circuit complexity of majority.

## Summary of result

Terms: a *program* is a sequence of operations `t = min(a, b)` or
`t = max(a, b)` whose operands are inputs or earlier results; its *size* is
the number of operations. "Gate" means the same thing in circuit language
(AND = min, OR = max).

- **Median of 5: exactly 10 operations** (`computed`). (For 3 values the
  same method gives 4, the value Seidler's manuscript also lists for 3-input
  majority in its 3-variable catalogue; `results/lower_bounds_3.log`.) A 10-operation program
  is verified on every input ordering, and a SAT solver finds no program of
  any size from 1 to 9. The classical 7-exchange network, with unused
  half-exchanges removed, already has size 10, so reusing values buys nothing
  for five inputs.
- **A catalogue presented as minimal is not minimal** (`external-data`).
  Seidler's catalogue of "minimal" monotone circuits for the 210 classes of
  monotone 5-variable functions (a 2022 manuscript, and Chapter 2 of the
  author's 2023 Rutgers dissertation) lists 13 gates for 5-input majority;
  the true minimum is 10. In total 19 of the 210 entries are larger than the
  minimum (table below). Every program in the catalogue is correct; only
  minimality fails. The author's own text warns that a pruning step in the
  search can discard an optimal circuit that shares a gate between both sides
  of its output, and the dissertation says that this may make some entries
  of the *general* 4-variable catalogue non-minimal; neither version
  flags the monotone 5-variable table (details and quotations below). That
  pruning is the likely cause here too, though we did not confirm it by
  running the author's code.
  With the corrected values no 5-variable monotone
  function needs more than 10 gates, and 7 classes need exactly 10, so
  majority is not the unique hardest function as the manuscript states. The
  4-variable catalogue (30 classes) is confirmed minimal.
- **Median of 7: between 12 and 20 operations; median of 9: between 14 and 30**
  (`computed`). The upper bounds are the pruned classical networks. The lower
  bounds are SAT refutations of all smaller sizes under symmetry-breaking
  constraints justified by a written, unformalized proof (claim 8,
  `proved-informal`). The question for 7 and 9 is
  **not settled**: 60 attempts (covering 23 distinct sub-problems) to shorten
  the 20-operation median-of-7 program by one operation all failed, which is
  weak evidence and proves nothing.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | The program in `results/median5_10.txt` (10 operations) computes the median of 5 values | computed | `python verify.py ../results/median5_10.txt` (all 32 0/1 inputs, all 120 orderings, random inputs with ties) |
| 2 | No min/max program with 9 or fewer operations computes the median of 5 values | computed | `results/lower_bounds_5.log` (sizes 1 to 9 UNSAT); regenerate with `python lower_bounds.py 5 10`. Confirmed without any symmetry breaking (`results/median5_nosym_sizes1to8.log`, `results/median5_size9_nosym.log`); other cross-checks in Method |
| 3 | The programs obtained by pruning the classical exchange networks compute the medians of 5, 7, 9 values in 10, 20, 30 operations | computed | `python baseline.py`, then `python verify.py ../results/baseline_median*.txt` |
| 4 | Under the constraints `sym=3` of `src/encode.py`, there is no circuit of any size 1 to 11 for 7-input majority and none of any size 1 to 13 for 9-input majority. Together with claim 8 this gives: no program with 11 or fewer operations computes the median of 7 values, and none with 13 or fewer the median of 9. That conclusion is only as strong as claim 8 | computed | `results/lower_bounds_7.log`, `results/lower_bounds_9.log`; regenerate with `python lower_bounds.py 7 11` and `python lower_bounds.py 9 13` |
| 5 | Of the 210 entries in Seidler's 5-variable monotone catalogue (as fetched 2026-11-23), all 210 listed programs compute the listed function, and exactly 19 use more gates than the minimum; the majority entry lists 13 and the minimum is 10 | external-data | `results/catalogue_check.csv`; regenerate with `../data/fetch_catalogue.sh` and `python catalogue_check.py ../data/raw/MonoCatFileA5var.txt out.csv`. The upper-bound half (a smaller circuit exists for each of the 19) needs no trust in the SAT solver: the circuits are in the CSV and are re-evaluated on all 32 inputs. The lower-bound half ("exactly 19") is confirmed with no symmetry breaking by `results/nosym_check.log` (`python nosym_check.py ../data/raw/MonoCatFileA5var.txt ../results/catalogue_check.csv out.log`, about 1 hour) |
| 6 | Minimum monotone {AND, OR} circuit sizes of the 210 classes of 5-variable monotone functions are distributed as: 0 gates: 3 classes, 1: 2, 2: 4, 3: 10, 4: 26, 5: 16, 6: 45, 7: 32, 8: 51, 9: 14, 10: 7 | external-data | Same CSV, and `results/nosym_check.log`: for every class with minimum m of 2 or more, size m-1 is UNSAT with no symmetry breaking. The list of class representatives is taken from the catalogue rather than regenerated here. For classes with minimum 7 or more the lower bound rests on SAT UNSAT answers with no certificate (the brute-force check stops at 5 gates, which also settles minimum 6) |
| 7 | All 30 entries of Seidler's 4-variable monotone catalogue are minimal | external-data | `results/catalogue_check_4var.csv`. Independently of any SAT solver: `python brute_force.py 4 7 > ../results/brute_force_n4_d7.txt` (about 1 minute, 3 GB of memory), then `python cross_check.py`, which compares the two files. Also `results/nosym_check_4var.log` (no symmetry breaking). All need the catalogue fetched first (`../data/fetch_catalogue.sh`) |
| 8 | Symmetry lemma: a smallest monotone circuit for majority of an odd number of inputs has a presentation satisfying the `sym=3` constraints of `src/encode.py`, so adding them does not change satisfiability at the minimum size | proved-informal | Read the proof under "Symmetry breaking and why it loses nothing" in Method. Not formalized (see Limitations). Only claim 4 uses it |

Commands in the table are run from the project's `src/` folder.

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

**Symmetry breaking and why it loses nothing** (claim 8). The searches use
extra constraints to go faster. They are justified as follows. This is a
written proof, not a machine-checked one. Only claim 4 depends on it: the
lower bounds for 5 inputs and for every catalogue class are also confirmed
with the constraints switched off.

Take a circuit of the smallest possible size s. Every gate has a path to the
output (otherwise delete it), so the output is the only gate nobody uses and
comes last in any valid numbering. No gate has two equal operands (it would
be a copy of its operand) and no two gates have the same operands and type
(otherwise merge them). Describe each gate by the triple (b, a, type)
with operands a < b, and order triples by b, then a, then type with
AND < OR. Consider every *presentation* of the circuit: a numbering of the
gates in which operands precede users, together with a renaming of the input
variables and, when the function is its own dual, optionally the exchange of
AND and OR throughout (which computes the dual function, hence the same
function). Pick a presentation whose sequence of triples, listed gate by
gate, is lexicographically smallest. Each constraint below holds for it,
because otherwise a single change would give a presentation with a strictly
smaller sequence.

1. *Triples strictly increase from each gate to the next.* If gate g+1 had a
   smaller triple than gate g, its larger operand would be at most that of g,
   hence below g, so it does not use g. Exchanging the two gates' numbers is
   a valid numbering; both gates keep their triples (their operands are below
   g), so position g now holds the smaller triple and earlier positions are
   unchanged. Equal triples are excluded above. In terms of the code: pairs
   (b, a) are non-decreasing, and two consecutive gates with the same pair
   are AND then OR. (Constraint level `sym=1`; valid for any function, with
   no dualisation and no renaming needed.)
2. *The first gate is AND(x0, x1)* (majority only). The first gate's operands
   are inputs. Renaming them to 0 and 1 and, if the gate is OR, exchanging
   AND and OR (majority of an odd number of inputs is its own dual) gives a
   presentation whose first triple is (1, 0, AND), the smallest triple there
   is; so the minimal presentation starts with it. (`sym=2`.)
3. *Input i+1 is not used before input i* (symmetric functions only). If gate
   g is the first to use i+1, and i is used neither earlier nor as g's smaller
   operand, then g does not use i at all (its larger operand cannot be i when
   it uses i+1 as the smaller one). Exchanging the names i and i+1 leaves
   earlier gates unchanged and makes g's triple smaller. (`sym=3`.)

Because the constraints assume a smallest circuit, UNSAT at size s excludes
only size exactly s. `lower_bounds.py` therefore runs every size from 1 up.

**Cross-checks of the lower bounds.**

- Two solvers (CaDiCaL 1.5.3 and Glucose 4, as shipped in PySAT) agree on
  sizes 1 to 10 for n = 5 (`results/lower_bounds_5*.log`).
- With no symmetry breaking (`--sym 0`; the only restriction left is that a
  gate's two operands are distinct, which loses nothing because a gate with
  equal operands is a copy of its operand; and since unused gates are then
  allowed, a smaller circuit can be padded to any larger size, so UNSAT at
  one size excludes all smaller sizes), sizes 1 to 8 for n = 5 are
  UNSAT (`results/median5_nosym_sizes1to8.log`), and so is size 9
  (`results/median5_size9_nosym.log`, 1069 s). So claim 2 does not depend on
  the symmetry argument; claim 4 does.
- The catalogue run uses only `sym=1` and independently gives 10 for majority.
- `src/nosym_check.py` repeats the decisive lower bound for every catalogue
  class with no symmetry breaking: for each class with minimum m of at least
  2, size m-1 is UNSAT (`results/nosym_check.log`, 205 classes;
  `results/nosym_check_4var.log`, 25 classes). Without the constraints a
  smaller circuit with at least one gate could be padded to size m-1, so
  this excludes every smaller size from 1 up; size 0 (a constant or a single
  variable) is excluded by a direct truth-table test in
  `catalogue_check.py`. The catalogue claims therefore do not depend on claim 8.
- `src/brute_force.py` enumerates all circuits without any SAT solver or
  encoding: every 4-variable class (up to 7 gates) and every 5-variable class
  with minimum at most 5 gates agrees exactly, and no 5-variable class with a
  larger SAT minimum is reachable in 5 gates (`python cross_check.py`,
  output in `results/cross_check.log`: 28 + 59 classes agree, 149 correctly
  unreachable).
- In all 210 + 30 catalogue classes the SAT minimum is at most the size of
  the catalogue's own circuit, as it must be if the encoding does not
  over-constrain; in 221 of the 240 it is equal.

No UNSAT proof certificate (DRAT) was produced or checked. The brute-force
check stops at 5 gates on 5 inputs, so claim 2 at sizes 6 to 9 rests on the
solvers alone (two solvers with symmetry breaking, one without).

**Catalogue comparison** (`src/catalogue_check.py`). For each entry: parse the
listed true points and straight-line program (gate type 1 = AND, 5 = OR in
the catalogue's notation), evaluate the program on all 32 inputs, then find
the minimum by SAT for sizes 1, 2, ... The circuit found is re-evaluated on
all 32 inputs by code separate from the encoder.

**Upper-bound attempts for 7 and 9** (`src/local_improve.py`). Keep a random
predecessor-closed set of 11 of the 20 gates of the pruned median-of-7
network and ask for a completion with exactly 8 more gates (19 total) in
which every added gate is used and the added gates are in canonical order. 60 random
choices, all UNSAT (`results/local7_keep11.log`). The 60 choices contain
only 23 distinct kept sets (the same 11 gates drawn in a different order
give the same problem), so this is 23 distinct questions, not 60. What did not work: plain
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
./run_all.sh                        # from the project folder; regenerates everything in results/
```

`run_all.sh` lists each step with its approximate runtime (4 cores, Intel
Xeon 2.10 GHz, 15 GB). Totals: everything except the last three steps takes
about two hours: the 5-variable catalogue (about 40 minutes), its repeat
without symmetry breaking (about 1 hour) and the size-9 run for majority
without symmetry breaking (18 minutes); the last three steps add about 50
minutes. The last sizes of the
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
  <https://sites.math.rutgers.edu/~bas312/Research/slp/SLP.pdf>; the same
  work as Chapter 2 of B. Seidler, "Experimental Mathematics Techniques for
  Boolean Functions and Combinatorial Games", PhD dissertation, Rutgers,
  October 2023,
  <https://sites.math.rutgers.edu/~bas312/Research/Seidler.pdf> (marked
  "ALL RIGHTS RESERVED"; read, not redistributed); and the catalogue files `MonoCatFileA4var.txt` and `MonoCatFileA5var.txt` in the
  same directory. The manuscript and catalogue files were accessed 2026-11-23, the
  dissertation 2026-11-24. No licence is stated for the manuscript or the
  catalogue files, so the files are
  not committed; `data/fetch_catalogue.sh` fetches them and
  `data/catalogue.sha256` records the checksums of the copies used.
- This is a computed catalogue, not a measurement. We did not rerun the
  author's Maple code. Claims 5, 6 and 7 are statements about the files as
  fetched on that date and fall if the files differ from what the author
  intended or are later changed. Claim 6 additionally trusts the catalogue's
  list of 210 class representatives to be complete (the count 210 agrees with
  the number of monotone 5-variable functions up to permutation of variables,
  OEIS A003182, retrieved 2026-11-24, OEIS content is under CC BY-SA 4.0
  `[licence from memory, unverified]`; only the number 210 is used: "inequivalent monotone Boolean
  functions of n or fewer variables", 2, 3, 5, 10, 30, 210, ...).
- Quoted from the manuscript, so the comparison is exact. Abstract: "we produce
  minimum-size circuits for every Boolean function of four or fewer variables
  and every monotone Boolean function of five variables." Results: "among the
  5-variable functions, 18290559 requires 13 gates while no other function
  requires more than 11 [...] this is the majority function on five
  variables". The manuscript's Table 5 row for 5 variables (3, 2, 4, 10, 26, 16,
  42, 35, 44, 18, 3, 6, 0, 1 classes at 0 to 13 gates) matches a count of the
  gates in the fetched file, so the file is the one the manuscript describes.
- Known problems, disclosed by the source itself. Section 2.1 (pages 7-8)
  describes a pruning that keeps one sub-program per function and then says:
  "After completing this catalog, we realized that there is a potential issue
  with this last pruning in the case that the optimal circuit for computing a
  function f uses some gate G in each subcircuit of its output gate. [...]
  Unfortunately, this means that the last pruning we did is technically
  invalid. [...] The circuits are still small enough that we have reason to
  believe that gate reuse is not an issue, but it likely will be for larger
  numbers of variables." Section 3.2 says the monotone method is "nearly
  identical". The 10-gate majority circuit above does share gates between the
  two operands of its output, so this caveat is the probable cause of the 19
  non-minimal entries. That is a hypothesis: we did not run or analyse the
  Maple code.
- Later partial correction by the author. The 2023 dissertation (found in
  the third quality-control round, after the results) keeps the pruning,
  drops the sentence "we have reason to believe that gate reuse is not an
  issue", and says of the *general* 4-variable table that entries "marked
  with *'s for four-variable functions may be inaccurate due the gate reuse
  issue", that "If we assume that Saarinen's values are accurate, then the
  circuits we produce for several BEC's are seven-gate circuits when some six-gate
  circuit would suffice" (Saarinen being a 2006 exhaustive search it cites),
  and (Section 2.2.3) that the pruning "may
  inadvertently discard this circuit. If it is the only six-gate circuit
  which computes f, the entry in our catalog for f is not minimal." Its
  monotone results (Section 2.3.3, Table 2.5) are unchanged from the
  manuscript and carry no such mark: "we have compiled catalogs of minimal
  circuits for all monotone Boolean functions of up to 5 variables", with the
  same 5-variable row ending in one class at 13 gates. The sentence singling
  out majority at 13 gates is not in the dissertation. So the author has
  identified the flaw and its possible effect on the general 4-variable
  catalogue;
  what this project adds is that the monotone 5-variable catalogue also has
  non-minimal entries, 19 of them, named, with the correct values (whether
  this flaw is what produced them remains the hypothesis stated above). The catalogue
  file fetched on 2026-11-23 still has the gate counts of the 2022
  manuscript's table, so the posted monotone catalogue had not been corrected
  by then. The author has not been contacted.
- The classical exchange networks in `src/baseline.py` (7, 13 and 19
  exchanges, usually attributed to Paeth and to Devillard's `opt_med`
  routines) were typed `[from memory, unverified]` as to source and
  attribution. Their correctness does not depend on the source: claim 3 is
  checked exhaustively.

## Prior work and novelty

Searched on 2026-11-23. The first six web queries were run before any code
was written; the last two (after the 5-input result), and the reading of the two arXiv papers and the
Sergeev abstract below, were done after the results, during write-up.

- Eight queries with a general web search engine. Terms: "exact monotone
  circuit complexity majority 5 7 9 AND OR gates minimum SAT"; "median of 9
  minimum number of min/max operations lower bound"; "optimal selection
  networks median SAT lower bound comparators"; "monotone complexity
  threshold function T_3^5 majority five variables Knuth 7.1.2"; "median of
  7 / 9 min max straight-line program superoptimization SIMD median filter";
  "majority seven variables monotone circuit AND OR exact synthesis MAJ7
  T_4^7"; "monotone circuit complexity MAJ_5 T_3^5 exactly 10 gates";
  "Knuth 7.1.2 Boolean chains median of five monotone chain cost".
  Alternative names covered: majority, median, threshold function T_k^n,
  selection network, monotone Boolean chain, min/max network.
- arXiv API, title search for "Minimal circuits for Boolean functions of few
  variables": no entry (the Seidler manuscript is not on arXiv under that
  title). OEIS search for "monotone majority circuit gates": no results.
- Read in full: Seidler's manuscript, and Chapter 2 of the dissertation
  (above). It is the only source found
  that states an exact monotone {AND, OR} size for 5-input majority, and it
  states 13.
- Read (abstract, statement of results, and a text search of the full paper
  for "monotone", "majority", "threshold"): A. S. Kulikov, D. Pechenev,
  N. Slezkin, "SAT-based Circuit Local Improvement", arXiv:2102.12579v3. It
  improves upper bounds for symmetric functions by SAT-based local search,
  the same idea as `local_improve.py` here. Its threshold results are
  asymptotic upper bounds ("size(THR_k^n) <= (4.5 - 2^(2-ceil(log2 k))) n +
  o(n) for 4 <= k = O(1)") and its constructions use XOR gates, so they are
  not monotone circuits. It also reports concrete small circuits found by
  its program for 4-threshold functions on 5 to 8 inputs (its Table 2:
  "23 -> 10", "28 -> 14", "31 -> 17", "40 -> 22"). The 7-input row is 7-input
  majority: a 17-gate circuit in the unrestricted binary basis, where gates
  such as XOR are allowed. That does not bound the {AND, OR} count studied
  here (monotone circuits can need more gates, and a min/max program cannot
  use XOR), but it shows the non-monotone analogue of the 7-input question
  has been attacked by the same method. Its only monotone statement found by the text
  search is a citation of Sergeev for the 2-threshold. No exact monotone
  value for small majority.
- Read (abstract and a text search of the full paper for exact small cases):
  N. Dobrokhotova-Maikova, A. Kozachinskiy, V. Podolskii, "Towards Simpler
  Sorting Networks and Monotone Circuits for Majority", arXiv:2310.12270v1.
  It concerns depth of monotone circuits for majority for large n (an
  explicit monotone circuit of depth O(log_2^{5/3} n), in the abstract's
  words "we provide an explicit monotone circuit of depth"), not size for small n.
- Abstract only (via Crossref and OpenAlex; the paper itself was not
  obtained): I. Sergeev, "On the complexity of monotone circuits for
  threshold symmetric Boolean functions", Diskretnaya Matematika 32 (2020),
  doi:10.4213/dm1547; English version doi:10.1515/dma-2021-0031. Abstract:
  "the complexity of a threshold-2 function is proved to be 2n +
  Theta(sqrt n), and the complexity of a threshold-3 function is shown to be
  3n + O(log n), the corresponding lower bounds are put forward." 5-input
  majority is the threshold-3 function at n = 5. The abstract gives
  asymptotic forms only; whether the body contains an exact value at n = 5
  was not checked. This is the most likely place, after Knuth, for prior
  knowledge of the value 10.
- Leads not followed: P. E. Dunne's 1984 Warwick thesis "Techniques for the
  analysis of monotone Boolean networks" and I. Wegener's 1987 book *The
  Complexity of Boolean Functions* (Section 6.2), both cited by Kulikov et
  al. for threshold upper bounds. Neither was obtained. Either could contain
  exact small values.
- Other search hits concerned different models (circuits of majority-of-3
  gates; depth-3 circuits; adaptive comparison counts for selection). They
  were not read and are not cited.
- Not found in what was read: a statement that 10 is the exact monotone
  circuit size of 5-input majority; exact values or SAT lower bounds for 7 or
  9 inputs in the {AND, OR} basis; any statement that entries of Seidler's
  *monotone* catalogue are not minimal (the author's general caveat, and the
  dissertation's concession for the general 4-variable catalogue, are quoted
  in the previous section). Knuth's *The Art of Computer Programming*
  7.1.1 and 7.1.2 are an obvious place for the 5-input value and could not be
  read here (not openly accessible), so it may well be recorded there.

- Topical database searches, run 2026-11-24 during quality control (after
  the results). arXiv API, five queries, none of whose hits is on this
  question by title: `"monotone circuit" AND majority AND exact` (0 hits);
  `"median" AND "min/max" AND network` (3 hits, on sensor networks and
  optimisation); `"monotone" AND "threshold function" AND "circuit
  complexity"` (2 hits, on decision trees and extended formulations);
  `"selection network" AND median AND optimal` (0); `"exact synthesis" AND
  monotone AND majority` (0). OpenAlex full-text search, four queries, first
  8 results of each examined by title: "monotone circuit complexity majority
  exact small"; "minimum monotone circuit threshold function five
  variables"; "median min max operations optimal network lower bound";
  "optimal selection network median comparators". DBLP's search API returned
  HTTP 202 with no results and was not searched.
- A second on-topic title in the same OpenAlex results, seen and not read:
  "Selection Networks" (1991, doi:10.1137/0220054). From the title it is
  about comparator selection networks, the same different cost model as the
  next item; nothing is claimed about its content.
- One OpenAlex hit looked into, abstract only read (single source, a Zenodo
  record, so `literature` at best): R. Martino, "Optimality of a
  25-Comparator Median Selection Network on Eleven Inputs", 2026-11-20,
  doi:10.5281/zenodo.24397283. Its abstract states that "exactly 25
  comparators are necessary and sufficient to select the sixth smallest of
  eleven inputs" in a comparator-network model, with the upper bound being
  "Bert Dobbelaere's published construction". That is a different cost model
  from the one here (a comparator is one unit and produces both min and max
  on fixed wires; here min and max are counted separately and results may be
  reused freely), and neither model's bounds transfer exactly to the other.
  It indicates that exact comparator counts for median selection on fewer
  inputs are an active, possibly settled, topic; that literature (including
  Dobbelaere's lists) was not read, and a specialist would start there for
  7 and 9 inputs. The abstract also contains instructions to readers for
  running its verification scripts; nothing from that record was downloaded
  or run.

What is known: the 10-, 20- and 30-operation programs (upper bounds) are
classical. What was not found elsewhere: the matching lower bound for 5 in
the min/max-operation model, the lower bounds for 7 and 9, and the 19
corrections to the catalogue. Hence `partially-known`. The search was a few
hours' work by a model, not a specialist's survey.

Outcome of the search: go ahead, with the scope as stated in the Question.
The pre-work search found one source giving a value for 5 inputs (13, which
the baseline network already contradicts), and nothing for 7 or 9.

## Limitations and open questions

- The lower bounds depend on SAT solvers reporting UNSAT with no certificate
  checked and, for 7 and 9 inputs only (claim 4), on the written symmetry
  argument. Producing DRAT proofs and
  checking them with an independent checker, or a Lean-checked certificate in
  the math repository, would remove both. Not done.
- Claim 8, the symmetry lemma, is a written proof and only claim 4 (the
  lower bounds for 7 and 9 inputs) relies on it. The standards expect written
  proofs to be formalized. That was not attempted in this session, by choice
  of where to spend the time: the route in `docs/environment.md` (write the
  Lean proof on a local branch of the math repository, build it, hand the
  patch to the owner) was open and was not taken. Formalizing the lemma alone
  would still leave the solver's UNSAT answers uncertified; the formal
  statement worth having is a Lean-checked UNSAT certificate, also not
  attempted. Formalizing claim 8 is the first follow-up task for this
  project. Until
  then claim 4's conclusion about medians of 7 and 9 values should be read as
  a computation plus an unformalized lemma. For 5 inputs the lemma is
  corroborated, not proved, by the fact that symmetry levels 1 and 3 give
  the same answers as no symmetry breaking in the committed logs.
- Sizes for 7 and 9 inputs are open: 12 to 20 and 14 to 30. The lower bounds
  are far from the upper bounds and say little. Each extra size costs roughly
  6 to 17 times more solver time (n=9: 10 s, 68 s, 1146 s for sizes 11, 12,
  13; n=7: 6 s, 60 s for sizes 10, 11). Size 12 for n=7 and size 14 for n=9 were started and did not
  finish: the n=7 size-12 run was stopped after more than 30 minutes on a
  shared machine, the n=9 size-14 run after a few minutes.
- The failed local search is not evidence of optimality of 20: it only
  explored completions of 23 distinct 11-gate subsets of one particular
  program.
- Only single-output programs are covered. Median filters over sliding
  windows share work between neighbouring windows; that is a different
  problem.
- Operation count is not speed. Depth, register pressure and instruction
  latency matter in practice and are not studied.
- Claim 6 covers classes under permutation of variables only, as in the
  catalogue.
- No source fetched for this project contained instructions addressed to an
  AI or other manipulation attempts.
- The claim commit was made before the research but was pushed to the
  session branch, not directly to `main`; it reached `main` in a later merge
  while the work was under way. No competing claim on this question existed
  on `main` at any point checked (start of work and final merge).

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
| 2026-11-23 | claude-fable-5-2, subagent of the authoring session (pre-review quality control, **not** an independent review under the standards) | Briefed with the repository only, not the author's conclusions. Reran all steps under 5 minutes, re-derived both CSVs against the catalogue with its own parser, read the encoder against the symmetry argument, checked quotations against the manuscript | No number found wrong. Ten issues, all fixed: the manuscript's own caveat about its search had not been quoted; a gap in the symmetry argument (now argued with triples); command paths; runtime totals; wording |
| 2026-11-23 | claude-fable-5-2, second fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief. In addition found UNSAT without symmetry breaking at minimum-1 for all 142 catalogue classes with minimum 6 to 9 (its own scratch run, not committed here) | No number found wrong. Twelve issues, fixed: unread search hits described without being read (now read or dropped); claim 4's dependence on the unformalized argument made explicit; this log; smaller wording and command fixes. Not fixable without rewriting history: commit 2198bee combines a merge of `main` with project edits |
| 2026-11-24 | claude-fable-5-2, third fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief. In addition wrote an independent SAT formulation (pair selectors, full truth table, no symmetry breaking) and confirmed minimum-1 UNSAT for the 186 classes with minimum 1 to 8 and 13 of the 14 with minimum 9; confirmed the 210 catalogue entries are 210 distinct classes out of 7581 monotone functions (scratch runs, not committed here) | No number found wrong. Seven issues, fixed: the author's 2023 dissertation had been missed (now read and quoted); catalogue lower bounds leaned on the symmetry argument (now rerun without it, `results/nosym_check.log`); the lemma is now its own `proved-informal` claim; wording and memory figures |
| 2026-11-24 | claude-fable-5-2, fourth fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reran all steps under 5 minutes, own catalogue parser, replayed the local search's random stream, re-fetched and checked all quoted sources | No number found wrong. Six issues, fixed: the 60 local-search trials are 23 distinct problems; `updated` date; topical arXiv and OpenAlex searches added and the search outcome stated; access dates; `results/cross_check.log` now saved |
| 2026-11-24 | claude-fable-5-2, fifth fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reruns, own parser, enumeration of all 7581 monotone 5-variable functions into 210 classes, all quoted sources re-fetched | No number found wrong; no blocking or should-fix issue. Two wording points, fixed: the description of arXiv:2102.12579 and the stated reason for not formalizing claim 8 |
| 2026-11-24 | claude-fable-5-2, sixth fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reruns, own parser, enumeration of all presentations of three programs against the lemma, sources re-fetched | No number found wrong. Four points, fixed: arXiv:2102.12579's table includes 7-input majority at 17 gates in the unrestricted basis (previously misdescribed); two statements about where brute force stops; one quotation |
| 2026-11-24 | claude-fable-5-2, seventh fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reruns, own parser, sentence-by-sentence comparison of quotations with re-fetched sources | No number found wrong; no blocking or should-fix issue. Four wording points, fixed: one limitation was unqualified; a quotation from the dissertation had lost its condition; two imprecise sentences |
| 2026-11-24 | claude-fable-5-2, eighth fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reruns, own parser, all sources re-fetched and search queries replayed | No number found wrong; no blocking or should-fix issue. Two wording points, fixed: "every symmetry level" narrowed to the levels with committed logs; a second on-topic search hit now listed as seen and not read. It also noted, for the owner, that claim 8 remains `proved-informal` at `status: result` |
| 2026-11-24 | claude-fable-5-2, ninth fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reruns, own parser on a fresh fetch, sources and search queries replayed | No number found wrong; no blocking or should-fix issue. Two wording points, fixed: two paraphrases of the dissertation were firmer than its conditional wording; a docstring in `src/encode.py` |
| 2026-11-24 | claude-fable-5-2, tenth fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief; reruns, own parser on a fresh fetch, sources and search queries replayed | No number found wrong; no blocking or should-fix issue. Two wording points, fixed: unsourced statements about practice in "Why it matters" now marked as from memory; a docstring in `src/local_improve.py` |
| 2026-11-24 | claude-fable-5-2, eleventh fresh subagent of the authoring session (pre-review quality control, **not** an independent review) | Same brief, extended to docstrings and introductory sections; wrote its own SAT formulation for majority of 3 and 5 (two-sided semantics, full truth table) and reproduced 4 and 10 | No number found wrong; no blocking or should-fix issue. Four wording points, fixed: padding does not cover size 0 (covered by a direct test); one sentence stated the hypothesised cause as fact; an unsourced "well-known"; two usage lines in docstrings |
