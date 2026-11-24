"""Minimum number of voters, by two independent solvers.

  python src/solve.py M RULES [--full] [--solver highs|cpsat|both]

HiGHS (via scipy.optimize.milp, floating point branch and bound) minimises
the number of voters in every case. CP-SAT (exact integer arithmetic) then
computes the overall minimum on its own: it goes through the cases keeping
the best profile found so far, and for each case either finds a profile
with fewer voters or proves there is none (so it does not report a minimum
for every case, only the global one). The best profile of each solver is
checked with the independent rule implementations in rules.py.
--full enumerates all labelled cases instead of one per renaming class.
--majority-stop uses the other Hare convention (see model.cases).
"""
import argparse, json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
from ortools.sat.python import cp_model
from model import cases
from rules import winners


def highs_min(A):
    n = A.shape[1]
    res = milp(c=np.ones(n), constraints=LinearConstraint(csr_matrix(A), lb=1, ub=np.inf),
               integrality=np.ones(n), bounds=Bounds(0, np.inf))
    if res.status == 2:
        return None, None
    assert res.status == 0, res.message
    x = np.rint(res.x).astype(int)
    assert (A @ x >= 1).all() and (x >= 0).all()
    return int(x.sum()), x


def cpsat_solve(A, ub, minimise):
    """Exact: is there x >= 0 integer, A x >= 1, sum x <= ub?  Optionally minimise."""
    md = cp_model.CpModel()
    n = A.shape[1]
    x = [md.NewIntVar(0, ub, f"x{i}") for i in range(n)]
    for row in A:
        nz = np.nonzero(row)[0]
        md.Add(sum(int(row[i]) * x[i] for i in nz) >= 1)
    md.Add(sum(x) <= ub)
    if minimise:
        md.Minimize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.num_workers = 4
    st = s.Solve(md)
    if st == cp_model.INFEASIBLE:
        return None, None
    assert st == cp_model.OPTIMAL, s.StatusName(st)
    v = np.array([s.Value(xi) for xi in x])
    assert (A @ v >= 1).all()
    return int(v.sum()), v


def profile_of(x, rankings):
    return {rankings[i]: int(k) for i, k in enumerate(x) if k}


def referee(found, m, rules, ms):
    """Check a solver's profile with rules.py; return the profile and its winners."""
    n, x, desc, rk = found
    prof = profile_of(x, rk)
    w = winners(prof, m, rules, majority_stop=ms)
    assert sum(prof.values()) == n
    assert None not in w.values() and len(set(w.values())) == len(w), w
    assert w == desc["winners"]
    return prof, w


def solve(m, rules, full=False, solver="both", majority_stop=False):
    a = argparse.Namespace(m=m, rules=rules, full=full, solver=solver)
    ms = majority_stop
    t0 = time.time()
    allc = list(cases(a.m, a.rules, reduce=not a.full, majority_stop=ms))
    out = dict(m=a.m, rules=a.rules, cases=len(allc), full=a.full, majority_stop=ms)
    best = None
    if a.solver in ("highs", "both"):
        opt = []
        for desc, A, rk in allc:
            n, x = highs_min(A)
            opt.append(n)
            if n is not None and (best is None or n < best[0]):
                best = (n, x, desc, rk)
        out["highs_case_minima"] = sorted(v for v in opt if v is not None)
        out["highs_infeasible_cases"] = sum(v is None for v in opt)
        out["highs_min"] = best[0] if best else None
        out["highs_seconds"] = round(time.time() - t0, 1)
    if a.solver in ("cpsat", "both"):
        t1 = time.time()
        cap = 400  # generous a-priori cap on the number of voters
        cbest = None
        for desc, A, rk in allc:
            ub = cap if cbest is None else cbest[0] - 1
            n, x = cpsat_solve(A, ub, minimise=True)
            if n is not None:
                cbest = (n, x, desc, rk)
        if cbest:
            referee(cbest, a.m, a.rules, ms)
        out["cpsat_min"] = cbest[0] if cbest else None
        out["cpsat_cap"] = cap
        out["cpsat_seconds"] = round(time.time() - t1, 1)
        if best is None:
            best = cbest
        if a.solver == "both":
            assert out["cpsat_min"] == out["highs_min"], (out["cpsat_min"], out["highs_min"])
    if best:
        n, x, desc, rk = best
        prof, w = referee(best, a.m, a.rules, ms)
        out["min_voters"] = n
        out["witness"] = [["".join("ABCDEFGH"[c] for c in r), k] for r, k in sorted(prof.items())]
        out["witness_winners"] = {k: "ABCDEFGH"[v] for k, v in w.items()}
    else:
        out["min_voters"] = None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("rules")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--solver", default="both")
    ap.add_argument("--majority-stop", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    out = solve(a.m, a.rules, a.full, a.solver, a.majority_stop)
    s = json.dumps(out)
    print(s)
    if a.out:
        open(a.out, "w").write(s + "\n")


if __name__ == "__main__":
    sys.exit(main())
