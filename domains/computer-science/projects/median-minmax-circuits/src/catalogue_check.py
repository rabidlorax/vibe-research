"""Recompute the minimum monotone {AND, OR} circuit size of every class in
Seidler's catalogue of monotone 5-variable functions and compare.

For each catalogue entry: (1) check that the listed straight-line program
really computes the listed function; (2) find the true minimum by asking the
SAT solver for circuits of size 1, 2, ... until one exists.

Usage: python catalogue_check.py ../data/raw/MonoCatFileA5var.txt OUT.csv [processes]
(also works for MonoCatFileA4var.txt)
"""
import csv
import re
import sys
from itertools import product
from multiprocessing import Pool

from pysat.solvers import Solver

from encode import encode, decode

N = 5   # set from the catalogue file name (MonoCatFileA<N>var.txt) in main and workers


def parse(path):
    lines = open(path).read().split("\n")
    out = []
    for i, l in enumerate(lines):
        m = re.match(r"^(\d+): \{(.*)\}$", l)
        if not m:
            continue
        pts = [tuple(int(x) for x in p.split(",")) for p in re.findall(r"\[([^\]]*)\]", m.group(2))]
        true_pts = {tuple(1 if x == 1 else 0 for x in p) for p in pts}
        slp = [it.strip() for it in re.findall(r"\[([^\[\]]*)\]", lines[i + 1])]
        out.append((int(m.group(1)), true_pts, slp))
    return out


def run_slp(slp, bits):
    """Catalogue SLP: [i] = variable i, [TRUE]/[FALSE], [1,a,b] = AND, [5,a,b] = OR (1-indexed)."""
    vals = []
    for it in slp:
        parts = [p.strip() for p in it.split(",")]
        if len(parts) == 1:
            vals.append({"TRUE": 1, "FALSE": 0}.get(parts[0]) if parts[0] in ("TRUE", "FALSE")
                        else bits[int(parts[0]) - 1])
        else:
            t, a, b = map(int, parts)
            assert t in (1, 5), t
            x, y = vals[a - 1], vals[b - 1]
            vals.append(x & y if t == 1 else x | y)
    return vals[-1]


def leq(a, b):
    return all(x <= y for x, y in zip(a, b))


def work(entry):
    global N
    num, true_pts, slp = entry
    N = len(next(iter(true_pts))) if true_pts else N
    allpts = list(product((0, 1), repeat=N))
    # (1) listed program computes listed function; function is monotone
    slp_ok = all(run_slp(slp, p) == (p in true_pts) for p in allpts)
    assert all(q in true_pts for p in true_pts for q in allpts if leq(p, q)), num
    listed = sum(1 for it in slp if it.count(",") == 2)
    false_pts = [p for p in allpts if p not in true_pts]
    minterms = [p for p in true_pts if not any(q != p and leq(q, p) for q in true_pts)]
    maxfalse = [p for p in false_pts if not any(q != p and leq(p, q) for q in false_pts)]
    # 0 gates: constant or a single variable
    proj = any(all((p[i] == 1) == (p in true_pts) for p in allpts) for i in range(N))
    if not true_pts or not false_pts or proj:
        return num, listed, 0, slp_ok, ""
    s = 1
    while True:
        cnf, meta = encode(N, s, sym=1, one_rows=minterms, zero_rows=maxfalse)
        with Solver(name="cadical153", bootstrap_with=cnf.clauses) as S:
            if S.solve():
                prog = decode(S.get_model(), meta)
                break
        s += 1
    # independent check of the circuit found, on all 32 inputs
    for p in allpts:
        v = list(p)
        for op, a, b in prog:
            v.append(min(v[a], v[b]) if op == "min" else max(v[a], v[b]))
        assert v[-1] == (p in true_pts), (num, p)
    return num, listed, s, slp_ok, " ".join(f"{op}({a},{b})" for op, a, b in prog)


if __name__ == "__main__":
    N = int(re.search(r"A(\d)var", sys.argv[1]).group(1))
    entries = parse(sys.argv[1])
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    with Pool(procs) as pool, open(sys.argv[2], "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["function", "catalogue_gates", "minimum_gates", "catalogue_program_correct",
                    "minimum_circuit(inputs 0-4, gates numbered from 5; min=AND, max=OR)"])
        res = []
        for r in pool.imap_unordered(work, entries):
            res.append(r)
            print(r[:4], flush=True)
        for r in sorted(res):
            w.writerow(r)
    worse = [r for r in res if r[1] != r[2]]
    print(f"{len(res)} classes; catalogue programs correct: {sum(r[3] for r in res)}; "
          f"catalogue size not minimal: {len(worse)}")
