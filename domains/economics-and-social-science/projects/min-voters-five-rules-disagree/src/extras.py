"""Secondary computations for m = 5 and all five rules (strict convention).

  python src/extras.py > results/extras.json
  python src/extras.py --majority-stop > results/extras_majority_stop.json

1. Re-evaluates three published profiles with rules.py (key "strict" uses
   the convention selected on the command line).
2. Fewest ballot types: overall, and with exactly 12 voters (CP-SAT).
3. For which n from 1 to 140 a strict profile with exactly n voters exists.
"""
import json, sys
import numpy as np
from ortools.sat.python import cp_model
from model import cases
from rules import winners, winners_robust

MS = "--majority-stop" in sys.argv   # the other Hare convention, see model.cases
L = "ABCDE"
def prof(spec):
    return {tuple(L.index(ch) for ch in b): k for b, k in spec}

PUBLISHED = {
    "Malkevitch 55": ([("ADECB", 18), ("BEDCA", 12), ("CBEDA", 10), ("DCEBA", 9), ("EBDCA", 4), ("ECDBA", 2)], "PRHBC"),
    "Brandt-Matthaus-Saile Table 4, 14": ([("ACBDE", 5), ("EBCDA", 4), ("DCBEA", 3), ("BDECA", 2)], "PRHBC"),
    "Wiseman 11": ([("ADECB", 4), ("BEDCA", 3), ("CEDBA", 2), ("DCBEA", 1), ("EDCBA", 1)], "PRHBC"),
}
out = {"majority_stop": "--majority-stop" in sys.argv, "published": {}}
for name, (spec, rules) in PUBLISHED.items():
    p = prof(spec)
    name_of = lambda w: {k: (L[v] if v is not None else None) for k, v in w.items()}
    out["published"][name] = dict(voters=sum(p.values()), strict=name_of(winners(p, 5, rules, majority_stop=MS)),
                                  robust=name_of(winners_robust(p, 5, rules)))

allc = list(cases(5, "PRHBC", majority_stop=MS))

WITNESS = {}

def cp(A, total_eq=None, total_max=None, types=False, types_eq=None):
    md = cp_model.CpModel()
    n = A.shape[1]
    ub = total_eq or total_max
    x = [md.NewIntVar(0, ub, "") for _ in range(n)]
    for row in A:
        md.Add(sum(int(row[i]) * x[i] for i in np.nonzero(row)[0]) >= 1)
    if total_eq:
        md.Add(sum(x) == total_eq)
    else:
        md.Add(sum(x) <= total_max)
    if types or types_eq:
        y = [md.NewBoolVar("") for _ in range(n)]
        for i in range(n):
            md.Add(x[i] <= ub * y[i])
        if types_eq:
            md.Add(sum(y) == types_eq)
            md.Minimize(sum(x))
        else:
            md.Minimize(sum(y))
    s = cp_model.CpSolver()
    s.parameters.num_workers = 4
    st = s.Solve(md)
    if st == cp_model.INFEASIBLE:
        return None
    assert st == cp_model.OPTIMAL
    v = [s.Value(xi) for xi in x]
    WITNESS[(total_eq, types)] = v
    return int(round(s.ObjectiveValue())) if (types or types_eq) else True

def over_cases(**kw):
    """Minimum over all cases; also returns a profile attaining it."""
    best = None
    for _, A, rk in allc:
        v = cp(A, **kw)
        if v is not None and (best is None or v < best[0]):
            x = WITNESS[(kw.get("total_eq"), kw.get("types", False))]
            p = {rk[i]: k for i, k in enumerate(x) if k}
            w = winners(p, 5, majority_stop=MS)
            assert None not in w.values() and len(set(w.values())) == 5
            best = (v, [["".join(L[c] for c in r), k] for r, k in sorted(p.items())],
                    {k: L[c] for k, c in w.items()})
    return best

CAP = 100
t = over_cases(total_max=CAP, types=True)[0]
out["min_types_any_n_up_to_%d" % CAP] = t
r = over_cases(total_max=CAP, types_eq=t)
out["min_voters_with_that_many_types"] = dict(voters=r[0], profile=r[1], winners=r[2])
r = over_cases(total_eq=12, types=True)
out["min_types_with_12_voters"] = dict(types=r[0], profile=r[1], winners=r[2])
print("types done", file=sys.stderr, flush=True)
feas = []
for n in range(1, 141):
    for _, A, rk in allc:
        if cp(A, total_eq=n):
            x = WITNESS[(n, False)]
            p = {rk[i]: k for i, k in enumerate(x) if k}
            w = winners(p, 5, majority_stop=MS)   # referee every witness
            assert sum(p.values()) == n and None not in w.values() and len(set(w.values())) == 5
            feas.append(n)
            break
out["feasible_n_1_to_140"] = feas
json.dump(out, sys.stdout, indent=1)
