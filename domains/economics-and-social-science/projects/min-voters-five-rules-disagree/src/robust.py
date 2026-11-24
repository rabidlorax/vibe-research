"""Minimum number of voters under the "robust" tie convention.

  python src/robust.py M RULES      (RULES must contain P and H)

Robust convention: ties are allowed, but each rule must elect the same
candidate however ties are broken. For rule sets containing plurality this
changes only Hare (README, Method): a tie for the plurality or Borda winner
would make that winner depend on the tie-break, the Condorcet winner is
strict by definition, and the runoff must be between the unique
plurality winner and a unique runner-up, decided strictly.

Because every winner has a different role, candidates are named by role:
the winners are 0..k-1 in the order of RULES; other candidates are k..m-1.

Hare is handled by branch and bound over "tie trees". A node fixes, for some
sets S of surviving candidates, the set L(S) of candidates tied for fewest
first places within S. Any of them may be eliminated, so every S minus one
element of L(S) must be handled too; the Hare winner may never be in L(S).
Each node is an integer program (equalities inside L(S), strict inequalities
to the rest of S). Its optimum bounds every profile below it, so a node is
cut when the optimum is not below the best profile found.

Two passes: HiGHS finds the minimum n*; CP-SAT (exact arithmetic) then
re-explores the whole tree with the extra constraint "at most n* - 1 voters"
and must find nothing.
"""
import json, sys, time
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from ortools.sat.python import cp_model
from model import Builder
from rules import winners_robust


def base_rows(m, rules):
    w = {k: i for i, k in enumerate(rules)}
    b = Builder(m)
    b.plurality(w["P"])
    if "R" in rules:
        b.runoff(w["R"], w["P"])
    if "B" in rules:
        b.borda(w["B"])
    if "C" in rules:
        b.condorcet(w["C"])
    return b, w


def highs(ge, eq, n):
    cons = [LinearConstraint(np.array(ge), lb=1, ub=np.inf)]
    if eq:
        cons.append(LinearConstraint(np.array(eq), lb=0, ub=0))
    res = milp(c=np.ones(n), constraints=cons, integrality=np.ones(n), bounds=Bounds(0, np.inf))
    if res.status == 2:
        return None, None
    assert res.status == 0, res.message
    x = np.rint(res.x).astype(int)
    assert (x >= 0).all() and (np.array(ge) @ x >= 1).all()
    assert not eq or (np.array(eq) @ x == 0).all()
    return int(x.sum()), x


def cpsat(ge, eq, n, ub):
    md = cp_model.CpModel()
    x = [md.NewIntVar(0, ub, f"x{i}") for i in range(n)]
    for rows, is_eq in ((ge, False), (eq, True)):
        for row in rows:
            e = sum(int(row[i]) * x[i] for i in np.nonzero(row)[0])
            md.Add(e == 0) if is_eq else md.Add(e >= 1)
    md.Add(sum(x) <= ub)
    md.Minimize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.num_workers = 4
    st = s.Solve(md)
    if st == cp_model.INFEASIBLE:
        return None, None
    assert st == cp_model.OPTIMAL
    v = np.array([s.Value(xi) for xi in x])
    return int(v.sum()), v


def search(m, rules, solver, cap):
    """Smallest robust profile with at most cap voters (cap None: unbounded, HiGHS only)."""
    b, w = base_rows(m, rules)
    h = w["H"]
    nvar = len(b.rankings)
    best = dict(n=(cap + 1) if cap is not None else 10**9, x=None)
    stats = dict(nodes=0, leaves=0)

    def solve(ge, eq):
        stats["nodes"] += 1
        if solver == "highs":
            return highs(ge, eq, nvar)
        return cpsat(ge, eq, nvar, best["n"] - 1)

    def rec(ge, eq, done, pending):
        n, x = solve(ge, eq)
        if n is None or n >= best["n"]:
            return
        pending = [S for S in pending if S not in done and len(S) > 1]
        if not pending:
            stats["leaves"] += 1
            best["n"], best["x"] = n, x
            return
        S = max(pending, key=len)
        rest = [S2 for S2 in pending if S2 != S]
        cand = sorted(S - {h})
        for size in range(1, len(cand) + 1):
            for L in combinations(cand, size):
                ge2, eq2 = list(ge), list(eq)
                alive = sorted(S)
                fl = {c: b.first(c, alive) for c in alive}
                for c in L[1:]:
                    eq2.append(fl[c] - fl[L[0]])
                for d in alive:
                    if d not in L:
                        ge2.append(fl[d] - fl[L[0]])
                rec(ge2, eq2, done | {S}, rest + [S - {c} for c in L])

    rec(list(b.rows), [], frozenset(), [frozenset(range(m))])
    return best, stats, b.rankings


def main():
    m, rules = int(sys.argv[1]), sys.argv[2]
    assert "P" in rules and "H" in rules
    t0 = time.time()
    best, st1, rk = search(m, rules, "highs", None)
    out = dict(m=m, rules=rules, convention="robust")
    if best["x"] is None:
        out["min_voters"] = None
    else:
        n = best["n"]
        prof = {rk[i]: int(k) for i, k in enumerate(best["x"]) if k}
        wr = winners_robust(prof, m, rules)
        assert wr == {k: i for i, k in enumerate(rules)}, wr
        best2, st2, _ = search(m, rules, "cpsat", n - 1)
        assert best2["x"] is None, "CP-SAT found a smaller profile"
        out.update(min_voters=n, highs_nodes=st1["nodes"], cpsat_nodes_below_min=st2["nodes"],
                   witness=[["".join("ABCDEFGH"[c] for c in r), k] for r, k in sorted(prof.items())],
                   witness_winners={k: "ABCDEFGH"[v] for k, v in wr.items()})
    out["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
