"""SAT-free cross-check: exhaustive breadth-first enumeration of all monotone
{AND, OR} circuits on n inputs with up to `depth` gates, as sets of computed
functions (truth tables as integers). Reports, for every function reached,
the smallest number of gates in a circuit containing it.

A circuit with d gates computing d distinct non-input functions is a set of d
functions that can be ordered so each is the AND or OR of two earlier ones
(or inputs); a minimal circuit never computes the same function twice or
recomputes an input, so enumerating such sets level by level is exhaustive.

Usage: python brute_force.py n depth
"""
import sys

n, depth = int(sys.argv[1]), int(sys.argv[2])
R = 1 << n
inputs = []
for i in range(n):
    t = 0
    for r in range(R):
        if r >> i & 1:
            t |= 1 << r
    inputs.append(t)
base = frozenset(inputs)
best = {t: 0 for t in inputs}
level = {frozenset()}
for d in range(1, depth + 1):
    nxt = set()
    for S in level:
        avail = list(base | S)
        for i in range(len(avail)):
            for j in range(i + 1, len(avail)):
                for f in (avail[i] & avail[j], avail[i] | avail[j]):
                    if f not in S and f not in base:
                        nxt.add(S | {f})
                        if f not in best:
                            best[f] = d
    level = nxt
    print(f"gates={d}: {len(level)} circuits (as function sets), "
          f"{len(best)} functions reached so far", flush=True)
for t in sorted(best):
    print(f"{t} {best[t]}")
