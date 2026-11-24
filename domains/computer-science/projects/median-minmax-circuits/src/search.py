"""Run the SAT search for one (n, s).

Usage: python search.py n s [--k K] [--sym L] [--solver NAME] [--out FILE]
                        [--comparators C]
Prints SAT/UNSAT and the time; on SAT writes the program in the format read
by verify.py.
"""
import argparse
import sys
import time

from pysat.solvers import Solver

from encode import encode, decode


def solve(n, s, k=None, sym=3, solver="cadical153", prefix=()):
    cnf, meta = encode(n, s, k, sym, prefix)
    t = time.time()
    with Solver(name=solver, bootstrap_with=cnf.clauses) as S:
        ok = S.solve()
        model = S.get_model() if ok else None
    dt = time.time() - t
    return ok, (decode(model, meta) if ok else None), dt, cnf, meta


def write_program(path, n, k, prog, note=""):
    with open(path, "w") as f:
        f.write(f"# {note}\n{n} {k}\n")
        for op, a, b in prog:
            f.write(f"{op} {a} {b}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("s", type=int)
    ap.add_argument("--k", type=int)
    ap.add_argument("--sym", type=int, default=3)
    ap.add_argument("--solver", default="cadical153")
    ap.add_argument("--out")
    ap.add_argument("--comparators", type=int, default=0,
                    help="fix the first gates to be this many comparators on inputs (0,1),(2,3),...; limits sym to at most 1")
    a = ap.parse_args()
    prefix = []
    for c in range(a.comparators):
        prefix += [("min", 2 * c, 2 * c + 1), ("max", 2 * c, 2 * c + 1)]
    if prefix:
        a.sym = min(a.sym, 1)
    ok, prog, dt, cnf, meta = solve(a.n, a.s, a.k, a.sym, a.solver, prefix)
    print(f"n={a.n} k={meta['k']} s={a.s} sym={a.sym} comparators={a.comparators} solver={a.solver} "
          f"vars={cnf.nv} clauses={len(cnf.clauses)} -> {'SAT' if ok else 'UNSAT'} in {dt:.1f}s",
          flush=True)
    if ok:
        for i, (op, x, y) in enumerate(prog):
            print(f"  t{a.n + i} = {op}(t{x}, t{y})")
        if a.out:
            write_program(a.out, a.n, meta["k"], prog,
                          f"found by search.py n={a.n} s={a.s} sym={a.sym} solver={a.solver}")
