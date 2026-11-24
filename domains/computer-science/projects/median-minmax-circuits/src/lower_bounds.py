"""Lower bounds for majority: run sizes 1, 2, ... in order, stop at first SAT
or at smax. All sizes are run because the symmetry breaking assumes an
irredundant circuit, so UNSAT at size s alone only excludes size exactly s.

Usage: python lower_bounds.py n smax [solver]
"""
import sys
from search import solve

n, smax = int(sys.argv[1]), int(sys.argv[2])
solver = sys.argv[3] if len(sys.argv) > 3 else "cadical153"
for s in range(1, smax + 1):
    ok, prog, dt, cnf, meta = solve(n, s, sym=3, solver=solver)
    print(f"n={n} s={s} solver={solver} vars={cnf.nv} clauses={len(cnf.clauses)} "
          f"{'SAT' if ok else 'UNSAT'} {dt:.1f}s", flush=True)
    if ok:
        break
