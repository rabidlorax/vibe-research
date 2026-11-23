"""Try to shorten a known program by one operation: keep a random
predecessor-closed subset of its gates fixed and ask the SAT solver to rebuild
everything else with one gate fewer. A hit is a strictly shorter program; a
miss proves nothing beyond "no completion of this particular kept subset".

Usage: python local_improve.py PROGRAM keep trials seed [conflict_budget]
"""
import random
import sys
import time

from pysat.solvers import Solver

from encode import encode, decode
from verify import load
from search import write_program


def random_closed_subset(n, prog, keep, rng):
    """Random topological order of the gates, first `keep` of them, renumbered."""
    done, order = set(range(n)), []
    remaining = set(range(len(prog)))
    while len(order) < keep:
        ready = [i for i in remaining if prog[i][1] in done and prog[i][2] in done]
        i = rng.choice(ready)
        order.append(i); remaining.discard(i); done.add(n + i)
    ren = {i: i for i in range(n)}
    ren.update({n + i: n + j for j, i in enumerate(order)})
    out = []
    for i in order:
        op, a, b = prog[i]
        a, b = sorted((ren[a], ren[b]))
        out.append((op, a, b))
    return out


if __name__ == "__main__":
    path, keep, trials, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    budget = int(sys.argv[5]) if len(sys.argv) > 5 else 2_000_000
    n, k, prog = load(path)
    rng = random.Random(seed)
    target = len(prog) - 1
    for t in range(trials):
        prefix = random_closed_subset(n, prog, keep, rng)
        cnf, meta = encode(n, target, k, sym=1, prefix=prefix)
        t0 = time.time()
        with Solver(name="cadical153", bootstrap_with=cnf.clauses) as S:
            S.conf_budget(budget) if hasattr(S, "conf_budget") else None
            try:
                ok = S.solve_limited(expect_interrupt=False)
            except NotImplementedError:
                ok = S.solve()
            model = S.get_model() if ok else None
        res = "SAT" if ok else ("UNSAT" if ok is False else "BUDGET")
        print(f"trial {t} seed {seed} keep {keep} target {target}: {res} in {time.time()-t0:.1f}s", flush=True)
        if ok:
            out = path.replace(".txt", f"_improved_{target}.txt")
            write_program(out, n, k, decode(model, meta),
                          f"local_improve.py from {path}, keep={keep}, seed={seed}, trial={t}")
            print("wrote", out)
            break
