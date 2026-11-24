---
title: Fewest voters for which five textbook voting rules elect five different winners
domain: economics-and-social-science
status: result
evidence: computed
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-24
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
here: unique plurality winner, unique runoff pair and a strict runoff
contest, unique Borda winner, a Condorcet winner who beats every other
candidate strictly (pairwise ties between other candidates are allowed), and
a unique candidate with fewest first places
in every elimination round, where elimination continues until one candidate
is left. This also forbids some ties that could not change the outcome (two
candidates with no first places; a tie after someone already has a
majority). **Majority-stop**: as strict, except that elimination stops as
soon as a candidate has more than half of the first places, and only the
rounds before that must be free of ties. **Robust**: ties may occur, but
every rule elects the same candidate however they are broken.

- **Strict convention: the minimum is 12 voters** (`computed`). That 12
  voters suffice was already known: Brandt, Matthäus and Saile (2022) say
  so in a footnote without a profile, and a 2008 web page by Wiseman prints
  a 12-voter profile with six candidates which, as checked here, still
  works when its unused candidate is deleted. What was not found in the
  search is any demonstration that 11 or fewer voters are impossible. With
  12 voters the fewest different ballots is **5** (the footnote mentions 7;
  Wiseman's profile also has 5). One such profile, found by an earlier run
  of `src/extras.py` and re-evaluated by it under the key
  `README strict 12` (the solver may return a different optimal profile on
  another run):

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
  (strict) and 11 (robust) (`computed`). Wiseman's 12-voter, 6-candidate
  profile already attains the strict value; the lower bounds were not found
  in the search.
- The majority-stop convention gives the same numbers as strict: 12 voters
  for `m = 5` and `m = 6`, and 5 ballots at 12 voters (`computed`).
- Under the strict convention a profile exists for every `n` from 12 to 140
  (`computed`).

The textbook example has 55 voters. The smallest previously printed
profiles found in the search have 14 voters (5 candidates, Brandt et al.)
and 12 voters (6 candidates, Wiseman).

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | With 5 candidates and the strict convention, the five rules elect five different candidates for some profile of 12 voters and for no profile of 11 or fewer | computed | `python src/solve.py 5 PRHBC` (HiGHS and CP-SAT agree); `--full` repeats it without the renaming argument; the 12-voter profile above can be checked by hand. The default run relies on the renaming argument, and both runs on the case list described under Method being complete |
| 2 | With 5 candidates and the robust convention the minimum is 11 voters | computed | `python src/robust.py 5 PRHBC`; profile above checkable by hand. The lower bound relies on two written arguments under Method that are not formalized: naming candidates by role, and the robust runoff being strict when plurality is in the rule set |
| 3 | With 12 voters (strict) the fewest different ballots is 5 | computed | `python src/extras.py`, key `min_types_with_12_voters` |
| 4 | Over all strict profiles with at most 100 voters, the fewest different ballots is 4, and with 4 ballots the fewest voters is 14 | computed | `python src/extras.py`; agrees with the caption of the five-rule table in Brandt et al. (Table 3 in the journal, Table 4 in the preprint) |
| 5 | A strict profile with exactly `n` voters exists for every `n` in 12..140 and for no `n` in 1..11 | computed | `python src/extras.py`, key `feasible_n_1_to_140` |
| 6 | With 6 candidates the minima are 12 (strict) and 11 (robust) | computed | `python src/table6.py`, `python src/robust.py 6 PRHBC`; same reliance on written arguments as claims 1 and 2 |
| 7 | The minima for every set of two or more of the five rules, 3 to 6 candidates, are as in the table under Method (numeric entries only; "none" is claim 11, "none found" is not claimed) | computed | `python src/table.py 5`, `python src/table6.py`, `python src/robust_table.py 5` |
| 8 | The published profiles of Malkevitch (55 voters, 5 candidates), Brandt et al. (14 voters, 5 candidates) and Wiseman (12 voters, 6 candidates) give five different winners under the strict, majority-stop and robust conventions, and so does Wiseman's 12-voter profile with its candidate E deleted (5 candidates, 5 ballots); Wiseman's 11-voter profile does not under any of the three, because its elimination winner is C or D depending on a tie-break | computed | `python src/extras.py` and `python src/extras.py --majority-stop`, key `published` |
| 9 | Brandt, Matthäus and Saile state that 12 voters suffice (with 7 ballot types) and print a 14-voter, 4-type profile; Wiseman prints a 12-voter, 6-candidate profile and states "as few as 11 voters" with a tie | literature | Sources and quotations under Prior work |
| 10 | Under the majority-stop convention: minimum 12 voters for 5 and for 6 candidates; with 12 voters the fewest ballots is 5; fewest ballots overall (at most 100 voters) is 4, needing 14 voters; a profile exists for exactly the `n` in 12..140 among 1..140 | computed | `python src/solve.py 5 PRHBC --majority-stop`, same with `6`, `python src/extras.py --majority-stop` |
| 11 | No profile of any size exists for the six strict entries marked "none" in the table (all with 3 candidates) | computed | `python src/none_check.py`: an exactly verified Farkas certificate for every labelled case that the model generates. Two kinds of labelled case are left out as contradictory by the arguments under Method: the Condorcet winner losing the runoff, and, when plurality is in the set, a runoff loser other than the plurality winner. The step from "no rational solution" to "no profile" (scaling by a common denominator) is also a written argument |

## Method

**Model.** With `m` candidates there are `m!` rankings; the unknowns are the
non-negative integer numbers of voters holding each ranking. Once it is fixed
who wins under each rule, which candidate loses the runoff, and in which
order candidates are eliminated, every requirement is a strict linear
inequality between integer quantities, written as `a.x >= 1`
(`src/model.py`). Minimising the number of voters over all such "cases" gives
the answer. Two kinds of case are never generated because they are
contradictory: a Condorcet winner cannot lose a runoff; and when plurality
is among the rules, its winner is one of the two runoff candidates and must
be the one who loses, since the runoff winner has to be someone else. Because candidates can be renamed, it is enough to take the
elimination order A, B, ..., and try every assignment of the other winners
(24 cases for the main problem). `--full` drops this shortcut and solves all
2880 labelled cases: according to HiGHS 240 have minimum 12, 240 have 17,
360 have 27, 360 have 47 and 1680 are infeasible, which is 120 times the
reduced counts. (These per-case figures come from HiGHS alone; CP-SAT only
establishes that no case has a profile with fewer than 12 voters.)

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

With 4 candidates 24 of the 25 strict minima in the table are matched,
including the rule sets RH, PRH, RHB, RHC, PRHB and PRHC at 14 voters. The
exception is RHBC, where the solver minimum is 15 and brute force only
confirms that nothing exists up to 14. For 5 candidates
full enumeration is only feasible up to 6 voters (about 4.9 billion
profiles), which matches only the seven rule sets with minimum at most 6;
claims 1 to 6 and 10 therefore rest on the two solvers and not on
enumeration.

**Table for all rule sets** (P plurality, R runoff, H elimination, B Borda,
C Condorcet; `m` candidates). In the strict columns "none" means no profile
of any size exists, proved exactly by `src/none_check.py` (claim 11); a
blank there means more rules than candidates, which is impossible. In the
robust columns a blank means not computed by the solver, which covers only
sets containing P and H. "none found" (robust PRH, 3 candidates) is not a
claim of non-existence: HiGHS reports every branch infeasible and brute
force finds nothing up to 40 voters, but there is no exact certificate. The
expected reason is that the plurality winner and, as argued above, the
runner-up are unique, so the third candidate is eliminated first and the
last elimination round is the runoff itself. Robust minima for sets without
plurality appear, for 3 and 4 candidates only, in
`results/bruteforce_*_robust.txt`; they come from the brute-force program
alone and are not claimed here. When a set
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
| PRH | none | 14 | 12 | 12 | none found | 14 | 11 |
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
python src/solve.py 6 PRHBC --majority-stop --out results/m6_PRHBC_majority_stop.json  # 4 min
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

Output of the main command, as run on 2026-11-24:

```
{"m": 5, "rules": "PRHBC", "cases": 24, "full": false, "majority_stop": false, "highs_case_minima": [12, 12, 17, 17, 27, 27, 27, 47, 47, 47], "highs_infeasible_cases": 14, "highs_min": 12, "highs_seconds": 0.1, "cpsat_min": 12, "cpsat_cap": 400, "cpsat_seconds": 0.3, "min_voters": 12, "witness": [["AECBD", 1], ["BAECD", 1], ["BAEDC", 1], ["CABDE", 1], ["CAEBD", 1], ["CBAED", 1], ["DABEC", 1], ["DBACE", 2], ["DBAEC", 1], ["EABCD", 1], ["EBACD", 1]], "witness_winners": {"P": "D", "R": "C", "H": "E", "B": "A", "C": "B"}}
```

## External data and what we could not reproduce

None. The project uses no dataset. Four published profiles (Malkevitch,
Brandt et al., two by Wiseman) are typed into `src/extras.py` for comparison; they
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
  (<https://pub.dss.in.tum.de/brandt-research/minpara.pdf>) and in the open
  copy of the journal version
  (<https://mediatum.ub.tum.de/doc/1690995/document.pdf>). Same five rules.
  As far as the paper describes it, their tie convention coincides with the majority-stop
  convention here rather than with strict: they consider only profiles with
  a unique winner; for the runoff, "we only consider preference profiles
  where there are exactly two candidates which are ranked more often than
  any other candidate"; and of instant runoff, which in their definition
  ends when a candidate has an absolute majority, "we only consider
  preference profiles in which no ties of this kind occur at any
  iteration". Claim 10 shows the numbers compared here are the same under
  strict and majority-stop. Table 3 (Table 4 in the preprint) is a 14-voter,
  4-ballot profile, with the caption "No
  preference profile of this kind requires fewer types of voters and no
  profile of this kind with 4 types of voters requires fewer voters."
  Footnote 15: "The same phenomenon can be achieved with only 12 voters, but
  7 different types of voters." No 12-voter profile is printed, the footnote
  does not say that 12 is the minimum, and no code was found. (The preprint
  text says "14 voters and 5 types of voters" where the journal version and
  both captions say 4.)
- J. Wiseman, "Non-Intuitive Features of Electoral Systems",
  <https://jdawiseman.com/papers/electsys/conundrum.html>. The page's main
  example has 12 voters, 6 candidates and 5 ballot types (4 ADEFBC, 3 BFEDCA,
  2 CFDBAE, 1 DCEBAF, 2 FDECBA). It was built to make six rules disagree,
  the sixth being approval voting ("In November 2008 approval voting was
  added to the list, without the STV draw"); on the five rules studied here
  it elects A, B, C, D and F with no tie (claim 8). Deleting candidate E,
  who wins only under approval, leaves a 5-candidate, 12-voter, 5-ballot
  profile that also works (claim 8); that derived profile is not printed on
  the page. The page also says "There can be as few as 11 voters, albeit at
  the price of having a draw in the first round of STV", followed by the
  11-voter profile evaluated in claim 8. No method or minimality argument
  is given.
- J. Malkevitch, <https://web.york.cuny.edu/~malk/courses/elections/election-one.html>
  (1999): the 55-voter profile. Its table is an image and was transcribed by
  eye; Wiseman's page gives the same profile in text. The AMS feature column
  that popularised it returned HTTP 403 and was not read.
- D. MacIver, "The worst election" (2016),
  <https://drmaciver.com/2016/12/the-worst-election/>: 4 candidates and 4
  rules (no runoff), 13 voters, minimal for fewest different ballots first
  and a fixed elimination order. Under the strict convention the minimum
  number of voters for those four rules and 4 candidates is 9 (PHBC, m=4);
  the majority-stop value, which matches MacIver's rule more closely, was
  not computed and is at most 9.
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

Not found in this search: a proof or computation showing that 11 or fewer
voters are impossible under the strict or majority-stop convention, for 5
or for 6 candidates; a printed 5-candidate strict profile with 12 voters
(one follows from Wiseman's by deleting a candidate); the statement that 5
is the fewest ballot types at 12 voters; the minimum under a tie-robust
convention, or an 11-voter profile that does not depend on a tie-break; the
table over rule sets. Hence `partially-known`: that 12 voters suffice was
known, with a printed 6-candidate example; the lower bounds, the robust
value and the table were not found. The site
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
  this only as far as it reaches: minima are matched for 3 candidates, for
  4 candidates except RHBC (solver 15, brute-force bound 14) and, with 5
  candidates, only for the seven rule sets whose minimum is at most 6. Rule
  sets containing both R and H, which drive the headline, are matched only
  at 4 candidates (minimum 14). The majority-stop model has no brute-force
  counterpart.
- The robust results for 5 and 6 candidates (claims 2 and 6) have no
  brute-force check and no run without the renaming shortcut. Their lower
  bounds also depend on the argument in Method that, when plurality is in
  the rule set, the robust runoff is the same as the strict one;
  `src/robust.py` builds that in. The argument is written out but not
  formalized.
- Claim 4 holds for profiles of at most 100 voters. In `solve.py` CP-SAT
  establishes the overall minimum `n*` exactly: once it holds a profile it
  asks of each further case only whether a smaller one exists. So for a
  case that HiGHS reports infeasible, or gives a minimum above `n*`, the
  exact confirmation is "nothing below `n*`", not infeasibility. When no
  profile is found at all, CP-SAT confirms that up to 400 voters; the
  strict "none" entries are settled without a cap by claim 11.
- Claim 5 stops at 140. Adding one voter of each of the 120 rankings to a
  profile leaves every strict comparison unchanged, which with claim 5 would
  give "every n >= 12"; this argument is written here only as a remark and
  is neither formalized nor claimed.
- Brandt et al.'s "7 different types" may refer to something this project
  did not reconstruct. Claim 3 does not depend on it: the 5-ballot profile
  is checked by hand above.
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
