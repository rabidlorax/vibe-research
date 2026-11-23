---
title: Fewest voters for which five textbook voting rules elect five different winners
domain: economics-and-social-science
status: result
evidence: computed
novelty: partially-known
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
for which this can happen with `m = 5`, when no tie occurs at any step (made
precise under Summary of result)?** An answer is a number `n*`, a profile with `n*` voters
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

Conventions. **Strict**: no tie at any step of any rule as carried out
here: unique plurality winner, unique runoff pair, unique Borda winner,
strict pairwise majorities, and a unique candidate with fewest first places
in every elimination round, where elimination continues until one candidate
is left. This also forbids some ties that could not change the outcome (two
candidates with no first places; a tie after someone already has a
majority). **Majority-stop**: as strict, except that elimination stops as
soon as a candidate has more than half of the first places, and only the
rounds before that must be free of ties. **Robust**: ties may occur, but
every rule elects the same candidate however they are broken.

- **Strict convention: the minimum is 12 voters** (`computed`). This agrees
  with a number stated without a profile or proof in a footnote of Brandt,
  Matthäus and Saile (2022). A 12-voter profile needs only **5 different
  ballots**, not the 7 that footnote mentions:

  | Voters | Ballot (best to worst) |
  |---|---|
  | 4 | D A B C E |
  | 3 | C B A E D |
  | 2 | B A E C D |
  | 2 | E B A C D |
  | 1 | A E D C B |

  Plurality elects D (first places A1 B2 C3 D4 E2). The runoff is D against
  C, and C wins 7 to 5. Elimination removes A, then B, then C, and E beats D
  8 to 4. Borda scores are A 32, B 31, C 21, D 18, E 18, so A wins. B beats
  A 7:5, C 8:4, D 7:5 and E 9:3, so B is the Condorcet winner.

- **Robust convention: the minimum is 11 voters** (`computed`):

  | Voters | Ballot |
  |---|---|
  | 3 | A E D B C |
  | 2 | B D E C A |
  | 2 | C E D B A |
  | 1 | A D B C E |
  | 1 | B D A E C |
  | 1 | D C B E A |
  | 1 | E C D A B |

  Plurality A (first places A4 B3 C2 D1 E1); runoff B beats A 6:5; D and E
  tie for first elimination, and C wins the elimination whichever goes
  first; Borda D (A 19, B 21, C 17, D 28, E 25); Condorcet E (6:5 over A, B
  and D, 7:4 over C). An 11-voter profile published by Wiseman also has a
  first-round tie, but there the elimination winner is C or D depending on
  how the tie is broken, and D is also its Borda winner.

- A sixth candidate does not help: with `m = 6` the minima are still 12
  (strict) and 11 (robust) (`computed`).
- The majority-stop convention gives the same numbers as strict: 12 voters
  for `m = 5` and `m = 6`, and 5 ballots at 12 voters (`computed`).
- Under the strict convention a profile exists for every `n` from 12 to 140
  (`computed`).

The textbook example has 55 voters; the smallest previously printed strict
profile found in the search has 14.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | With 5 candidates and the strict convention, the five rules elect five different candidates for some profile of 12 voters and for no profile of 11 or fewer | computed | `python src/solve.py 5 PRHBC` (HiGHS and CP-SAT agree); `--full` repeats it without the renaming argument; the 12-voter profile above can be checked by hand |
| 2 | With 5 candidates and the robust convention the minimum is 11 voters | computed | `python src/robust.py 5 PRHBC`; profile above checkable by hand |
| 3 | With 12 voters (strict) the fewest different ballots is 5 | computed | `python src/extras.py`, key `min_types_with_12_voters` |
| 4 | Over all strict profiles with at most 100 voters, the fewest different ballots is 4, and with 4 ballots the fewest voters is 14 | computed | `python src/extras.py`; agrees with the caption of Table 4 in Brandt et al. |
| 5 | A strict profile with exactly `n` voters exists for every `n` in 12..140 and for no `n` in 1..11 | computed | `python src/extras.py`, key `feasible_n_1_to_140` |
| 6 | With 6 candidates the minima are 12 (strict) and 11 (robust) | computed | `python src/table6.py`, `python src/robust.py 6 PRHBC` |
| 7 | The minima for every set of two or more of the five rules, 3 to 6 candidates, are as in the table under Method | computed | `python src/table.py 5`, `python src/table6.py`, `python src/robust_table.py 5` |
| 8 | The published profiles of Malkevitch (55 voters) and Brandt et al. (14 voters) give five different winners under both conventions; Wiseman's 11-voter profile does not under either, because its elimination winner is C or D depending on a tie-break | computed | `python src/extras.py`, key `published` |
| 10 | Under the majority-stop convention: minimum 12 voters for 5 and for 6 candidates; with 12 voters the fewest ballots is 5; fewest ballots overall (at most 100 voters) is 4, needing 14 voters; a profile exists for exactly the `n` in 12..140 among 1..140 | computed | `python src/solve.py 5 PRHBC --majority-stop`, same with `6`, `python src/extras.py --majority-stop` |
| 11 | No profile of any size exists for the six strict entries marked "none" in the table (all with 3 candidates) | computed | `python src/none_check.py`: an exactly verified Farkas certificate for every labelled case |
| 9 | Brandt, Matthäus and Saile state that 12 voters suffice (with 7 ballot types) and print a 14-voter, 4-type profile; Wiseman states "as few as 11 voters" with a tie | literature | Sources and quotations under Prior work |

## Method

**Model.** With `m` candidates there are `m!` rankings; the unknowns are the
non-negative integer numbers of voters holding each ranking. Once it is fixed
who wins under each rule, which candidate loses the runoff, and in which
order candidates are eliminated, every requirement is a strict linear
inequality between integer quantities, written as `a.x >= 1`
(`src/model.py`). Minimising the number of voters over all such "cases" gives
the answer. Because candidates can be renamed, it is enough to take the
elimination order A, B, ..., and try every assignment of the other winners
(24 cases for the main problem). `--full` drops this shortcut and solves all
2880 labelled cases: 240 have minimum 12, 240 have 17, 360 have 27, 360
have 47 and 1680 are infeasible, which is 120 times the reduced counts.

**Two solvers.** HiGHS (through `scipy.optimize.milp`, floating-point branch
and bound) minimises each case. CP-SAT (OR-Tools, exact integer arithmetic)
separately computes the overall minimum among profiles of at most 400
voters: it goes through the cases keeping the best profile so far, and for
each case either finds a smaller profile or proves there is none. The two
overall minima must agree, and the witness is re-evaluated by `src/rules.py`, which
implements the rules directly and shares no code with the model.

**Majority-stop convention** (`--majority-stop`). One case per round `k` at
which the count stops: unique lowest candidate in rounds before `k`, and in
round `k` the winner has more than half of all first places.

**Robust convention** (`src/robust.py`, rule sets containing plurality and
elimination). Plurality, Borda and Condorcet winners are strict by
definition. The plurality winner is unique, so the runoff is between that
candidate and whoever is second; if several tied for second, each would have
to beat the plurality winner and the runoff winner would depend on the
tie-break, so second place is unique and the contest strict. Only the
elimination rule changes. It is handled by branch and bound over "tie
trees": for a set `S` of surviving candidates the program chooses the set
`L(S)` tied for fewest first places (never containing the intended winner),
adds equalities inside `L(S)` and strict inequalities to the rest, and must
then also handle `S` minus each member of `L(S)`. Each node is an integer
program whose optimum bounds everything below it. HiGHS finds the minimum
`n*`; CP-SAT then re-explores the tree with "at most `n* - 1` voters" added
and finds nothing.

**Exhaustive cross-check** (`src/bruteforce.c`, a third implementation of the
rules). It enumerates every profile up to a bound and records the smallest
number of voters for each rule set. `src/check_bruteforce.py` compares, and
counts separately the rule sets where both methods give the same minimum
and those where brute force finds nothing up to its bound and the solver
minimum lies above the bound (or is "none"):

```
bruteforce_m3_N40.txt (m=3, all profiles up to 40 voters, strict): 14 minima equal, 6 with nothing up to 40 voters and solver minimum above 40 or none
bruteforce_m3_N40_robust.txt (m=3, all profiles up to 40 voters, robust): 3 minima equal, 1 with nothing up to 40 voters and solver minimum above 40 or none
bruteforce_m4_N14.txt (m=4, all profiles up to 14 voters, strict): 24 minima equal, 1 with nothing up to 14 voters and solver minimum above 14 or none
bruteforce_m4_N14_robust.txt (m=4, all profiles up to 14 voters, robust): 7 minima equal, 0 with nothing up to 14 voters and solver minimum above 14 or none
bruteforce_m5_N6.txt (m=5, all profiles up to 6 voters, strict): 7 minima equal, 19 with nothing up to 6 voters and solver minimum above 6 or none
total: 55 minima equal, 27 consistent non-existence up to the bound
```

With 4 candidates every strict minimum in the table is matched, including
all rule sets containing both R and H (14 or 15 voters). For 5 candidates
full enumeration is only feasible up to 6 voters (about 4.9 billion
profiles), which matches only the seven rule sets with minimum at most 6;
claims 1 to 6 and 10 therefore rest on the two solvers and not on
enumeration.

**Table for all rule sets** (P plurality, R runoff, H elimination, B Borda,
C Condorcet; `m` candidates). "none" means no profile of any size exists.
For the strict entries this is proved exactly by `src/none_check.py` (claim
11). The one robust "none", PRH with 3 candidates, is what the search
reports (every branch infeasible for HiGHS, and brute force finds nothing up
to 40 voters); it has no exact certificate, but the reason is simple: the
plurality winner is unique and, as argued above, so is the runner-up; the
third candidate therefore has strictly the fewest first places and is
eliminated first, and the last elimination round is the same contest as the
runoff, so the two rules cannot elect different candidates.
Blank in a strict column means more rules than candidates, which is
impossible. Blank in a robust column means not computed: the robust search
covers only sets containing P and H. When a set
does not contain P, the strict convention for R requires only that the
runoff pair is determined.

| Rules | strict m=3 | m=4 | m=5 | m=6 | robust m=3 | m=4 | m=5 |
|---|---|---|---|---|---|---|---|
| PR | 9 | 7 | 7 | 7 |  |  |  |
| PH | 9 | 8 | 8 | 12 | 9 | 7 | 7 |
| PB | 4 | 3 | 3 | 3 |  |  |  |
| PC | 7 | 5 | 5 | 5 |  |  |  |
| RH | none | 14 | 11 | 11 |  |  |  |
| RB | 5 | 3 | 3 | 3 |  |  |  |
| RC | 5 | 5 | 5 | 5 |  |  |  |
| HB | 5 | 5 | 8 | 11 |  |  |  |
| HC | 5 | 5 | 8 | 11 |  |  |  |
| BC | 5 | 3 | 3 | 3 |  |  |  |
| PRH | none | 14 | 12 | 12 | none | 14 | 11 |
| PRB | 9 | 7 | 7 | 7 |  |  |  |
| PRC | 9 | 7 | 7 | 7 |  |  |  |
| PHB | 9 | 8 | 8 | 12 | 9 | 7 | 7 |
| PHC | 9 | 8 | 8 | 12 | 9 | 7 | 7 |
| PBC | 19 | 7 | 5 | 5 |  |  |  |
| RHB | none | 14 | 11 | 11 |  |  |  |
| RHC | none | 14 | 11 | 11 |  |  |  |
| RBC | none | 7 | 5 | 5 |  |  |  |
| HBC | none | 7 | 8 | 11 |  |  |  |
| PRHB |  | 14 | 12 | 12 |  | 14 | 11 |
| PRHC |  | 14 | 12 | 12 |  | 14 | 11 |
| PRBC |  | 11 | 7 | 7 |  |  |  |
| PHBC |  | 9 | 8 | 12 |  | 9 | 7 |
| RHBC |  | 15 | 11 | 11 |  |  |  |
| PRHBC |  |  | 12 | 12 |  |  | 11 |

The strict minima are not monotone in `m` (for example H and B: 5, 5, 8,
11). With many candidates and few voters several candidates have no first
places, and the strict convention forbids that tie; the robust convention
does not, which is why it is the more natural one for larger `m`.

## Reproduction

From the project folder, Python 3.13 and gcc 13.3 on 4 cores:

```bash
pip install -r requirements.txt
python src/solve.py 5 PRHBC --out results/m5_PRHBC.json             # 1 s
python src/solve.py 5 PRHBC --full --out results/m5_PRHBC_full.json # 1 min
python src/robust.py 5 PRHBC > results/robust_m5_PRHBC.json         # 3 s
python src/robust.py 6 PRHBC > results/robust_m6_PRHBC.json         # 1 min
python src/extras.py > results/extras.json                          # 2 min
python src/table.py 5 > results/table_m3to5.json                    # 10 s
python src/table6.py > results/table_m6.json                        # 2 min
python src/robust_table.py 5 > results/robust_table_m3to5.json      # 20 s
python src/solve.py 5 PRHBC --majority-stop --out results/m5_PRHBC_majority_stop.json  # 2 s
python src/solve.py 6 PRHBC --majority-stop --out results/m6_PRHBC_majority_stop.json  # 2 min
python src/extras.py --majority-stop > results/extras_majority_stop.json               # 6 min
python src/none_check.py > results/none_check.txt                   # 1 s
gcc -O2 -o /tmp/bruteforce src/bruteforce.c
/tmp/bruteforce 3 40 > results/bruteforce_m3_N40.txt
/tmp/bruteforce 3 40 robust > results/bruteforce_m3_N40_robust.txt
/tmp/bruteforce 4 14 > results/bruteforce_m4_N14.txt                # 35 min
/tmp/bruteforce 4 14 robust > results/bruteforce_m4_N14_robust.txt  # 50 min
/tmp/bruteforce 5 6 > results/bruteforce_m5_N6.txt                  # 20 min
python src/check_bruteforce.py > results/check_bruteforce.txt
```

No network access is needed after installing the packages. Runtimes are
approximate. The solvers may return a different optimal profile on another
run or version; the minima should not change.

Output of the main command, as run on 2026-11-23:

```
{"m": 5, "rules": "PRHBC", "cases": 24, "full": false, "majority_stop": false, "highs_case_minima": [12, 12, 17, 17, 27, 27, 27, 47, 47, 47], "highs_infeasible_cases": 14, "highs_min": 12, "highs_seconds": 0.1, "cpsat_min": 12, "cpsat_cap": 400, "cpsat_seconds": 0.2, "min_voters": 12, "witness": [["AECBD", 1], ["BAECD", 1], ["BAEDC", 1], ["CABDE", 1], ["CAEBD", 1], ["CBAED", 1], ["DABEC", 1], ["DBACE", 2], ["DBAEC", 1], ["EABCD", 1], ["EBACD", 1]], "witness_winners": {"P": "D", "R": "C", "H": "E", "B": "A", "C": "B"}}
```

## External data and what we could not reproduce

None. The project uses no dataset. Three published profiles (Malkevitch,
Brandt et al., Wiseman) are typed into `src/extras.py` for comparison; they
are short factual tables, attributed under Prior work.

## Prior work and novelty

Searched on 2026-11-23, before the computations, by a web search tool,
OpenAlex, the arXiv API and OEIS. Terms included: "minimal voting
paradoxes"; "five voting rules" / "five voting methods" with "five different
winners"; "four different winners"; "smallest election"; "fewest voters" /
"minimum number of voters" with plurality, Borda, IRV, Hare, runoff,
Condorcet; "different winners" "voting rules" minimal profile; Malkevitch 55
voters; Balinski "Le scrutin"; and the names Nurmi, Felsenthal, Saari,
Ratliff. Also the works citing Brandt et al. in OpenAlex (13, by title).

Found:

- F. Brandt, M. Matthäus, C. Saile, "Minimal voting paradoxes", *Journal of
  Theoretical Politics* 34(4), 2022, doi:10.1177/09516298221122104. Read in
  the authors' preprint
  (<https://pub.dss.in.tum.de/brandt-research/minpara.pdf>); the publisher's
  version was not accessible. Same five rules. Their tie convention is close
  to the majority-stop convention here, not identical to strict: they
  consider only profiles with a unique winner, and of instant runoff, which
  in their definition stops when a candidate has a majority, they write "we
  only consider preference profiles in which no ties of this kind occur at
  any iteration". Claim 10 shows the numbers compared here are the same
  under strict and majority-stop. Table 4 is a 14-voter, 4-ballot profile, with the caption "No
  preference profile of this kind requires fewer types of voters and no
  profile of this kind with 4 types of voters requires fewer voters."
  Footnote 15: "The same phenomenon can be achieved with only 12 voters, but
  7 different types of voters." No 12-voter profile is printed, the footnote
  does not say that 12 is the minimum, and no code was found. The preprint
  is not consistent about ballot types: its text says the Table 4 profile
  "requires 14 voters and 5 types of voters", while the table and caption
  show 4.
- J. Wiseman, "Non-Intuitive Features of Electoral Systems",
  <https://jdawiseman.com/papers/electsys/conundrum.html>: "There can be as
  few as 11 voters, albeit at the price of having a draw in the first round
  of STV", followed by the profile evaluated in claim 8. No method or
  minimality argument is given.
- J. Malkevitch, <https://web.york.cuny.edu/~malk/courses/elections/election-one.html>
  (1999): the 55-voter profile. Its table is an image and was transcribed by
  eye; Wiseman's page gives the same profile in text. The AMS feature column
  that popularised it returned HTTP 403 and was not read.
- D. MacIver, "The worst election" (2016),
  <https://drmaciver.com/2016/12/the-worst-election/>: 4 candidates and 4
  rules (no runoff), 13 voters, minimal for fewest different ballots first
  and a fixed elimination order. The absolute minimum here is 9 (PHBC, m=4).
- N. Peek, "Automatic Analysis of Voting Procedures", BSc thesis,
  University of Amsterdam, 2008
  (<https://staff.fnwi.uva.nl/u.endriss/teaching/NadyaPeekBSc2008.pdf>), and
  S. Heilmaier, "Optimal Voting Rules for Few Candidates", MSc thesis, TU
  München, 2020
  (<https://pub.dss.in.tum.de/brandt-research/heilmaier_thesis.pdf>). Both
  were retrieved and searched by keyword, not read in full; they treat two
  or three rules on 3 or 4 candidates.
- Brandt et al. credit the five-rule example to Balinski (2002, 100 voters)
  and mention Nurmi (1987); neither was retrieved.

Not found in this search: a proof or computation showing that 12 is the
strict minimum; a printed 12-voter strict profile; a 12-voter profile with
fewer than 7 ballot types; the minimum under a tie-robust convention or an
11-voter profile that does not depend on a tie-break; the 6-candidate
values; the table over rule sets. Hence `partially-known`: the number 12 is
in the literature as an assertion, and the rest was not found. The site
searches of math.stackexchange, MathOverflow, electowiki and the
election-methods list were made only through the general web search tool,
which returned nothing from them.

## Limitations and open questions

- The lower bounds for 5 and 6 candidates rest on two integer-programming
  solvers agreeing, one of them exact. No independently checkable
  certificate (for example a proof log verified by a separate checker, or a
  Lean proof) was produced. That would be the way to upgrade claims 1 and 2.
- The model and the two solvers share `src/model.py`. A wrong constraint
  there that makes a case too restrictive would raise the reported minimum
  without any witness failing. The brute-force comparison guards against
  this only as far as it reaches: minima are matched for 3 and 4 candidates
  and, with 5 candidates, only for the seven rule sets whose minimum is at
  most 6. Rule sets containing both R and H, which drive the headline, are
  matched only at 4 candidates (minimum 14 or 15). The majority-stop model
  has no brute-force counterpart.
- Claim 4 holds for profiles of at most 100 voters. In `solve.py` CP-SAT
  considers at most 400 voters, while HiGHS has no cap; a case that HiGHS
  reports infeasible is therefore confirmed exactly only up to 400 voters,
  except for the "none" entries covered by claim 11.
- Claim 5 stops at 140. Adding one voter of each of the 120 rankings to a
  profile leaves every strict comparison unchanged, which with claim 5 would
  give "every n >= 12"; this argument is written here only as a remark and
  is neither formalized nor claimed.
- Brandt et al.'s "7 different types" may refer to something this project
  did not reconstruct (only the preprint was read). Claim 3 does not depend
  on it: the 5-ballot profile is checked by hand above.
- Not computed: the fewest ballot types under the robust convention; robust
  minima for rule sets without plurality; 7 or more candidates; other rules
  (Coombs, approval, Copeland).
- "Robust" here means the winner does not depend on how ties are broken one
  candidate at a time. Rules that eliminate all tied candidates at once were
  not modelled.
- No fetched source contained instructions addressed to a model.

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
