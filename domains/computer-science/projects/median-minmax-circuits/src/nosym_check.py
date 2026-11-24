"""Lower bounds for every catalogue class with no symmetry breaking.

For each class with SAT minimum m >= 2 (read from the CSV written by
catalogue_check.py), ask for a circuit of size m-1 with sym=0. With sym=0 the
only restriction is that a gate's operands are distinct, and any smaller
circuit can be padded with extra gates to size m-1, so UNSAT here excludes
every size below m without relying on the symmetry argument.

Usage: python nosym_check.py CATALOGUE.txt RESULT.csv OUT.log [processes]
"""
import csv
import sys
import time
from itertools import product
from multiprocessing import Pool

from pysat.solvers import Solver

from catalogue_check import parse, leq
from encode import encode


def work(job):
    num, true_pts, m, n = job
    allpts = list(product((0, 1), repeat=n))
    false_pts = [p for p in allpts if p not in true_pts]
    minterms = [p for p in true_pts if not any(q != p and leq(q, p) for q in true_pts)]
    maxfalse = [p for p in false_pts if not any(q != p and leq(p, q) for q in false_pts)]
    cnf, _ = encode(n, m - 1, sym=0, one_rows=minterms, zero_rows=maxfalse)
    t = time.time()
    with Solver(name="cadical153", bootstrap_with=cnf.clauses) as S:
        ok = S.solve()
    return num, m, "SAT" if ok else "UNSAT", time.time() - t


if __name__ == "__main__":
    entries = parse(sys.argv[1])
    mins = {int(r["function"]): int(r["minimum_gates"]) for r in csv.DictReader(open(sys.argv[2]))}
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    jobs = [(num, tp, mins[num], len(next(iter(tp)))) for num, tp, _ in entries if mins[num] >= 2]
    jobs.sort(key=lambda j: j[2])
    bad = 0
    with Pool(procs) as pool, open(sys.argv[3], "w") as f:
        for num, m, res, dt in pool.imap_unordered(work, jobs):
            f.write(f"function {num}: minimum {m}; size {m-1} with sym=0: {res} in {dt:.1f}s\n")
            f.flush()
            bad += res != "UNSAT"
        f.write(f"{len(jobs)} classes with minimum >= 2 checked; not UNSAT: {bad}\n")
