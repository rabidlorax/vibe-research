"""Independent check of a min/max straight-line program. Shares no code with
the SAT encoding.

Program file format (results/*.txt): first non-comment line "n k", then one
line per operation "min a b" or "max a b"; operands are node indices, inputs
are 0..n-1 and the i-th operation defines node n+i. The last operation is the
output. Lines starting with # are comments.

Two checks, each sufficient on its own:
  1. Boolean: on all 2^n 0/1 inputs, with min = AND and max = OR, the output
     is 1 exactly when at least k inputs are 1.
  2. Direct: on all n! orderings of n distinct integers (and on random inputs
     with ties), the output equals the k-th largest value.

Usage: python verify.py results/median5_10.txt [...]
"""
import random
import sys
from itertools import permutations, product


def load(path):
    lines = [l.split("#")[0].split() for l in open(path)]
    lines = [l for l in lines if l]
    n, k = int(lines[0][0]), int(lines[0][1])
    prog = [(op, int(a), int(b)) for op, a, b in lines[1:]]
    for i, (op, a, b) in enumerate(prog):
        assert op in ("min", "max") and 0 <= a < n + i and 0 <= b < n + i, (i, op, a, b)
    return n, k, prog


def run(prog, xs):
    vals = list(xs)
    for op, a, b in prog:
        vals.append(min(vals[a], vals[b]) if op == "min" else max(vals[a], vals[b]))
    return vals[-1]


def check(path):
    n, k, prog = load(path)
    for bits in product((0, 1), repeat=n):
        assert run(prog, bits) == (1 if sum(bits) >= k else 0), bits
    nperm = 0
    for perm in permutations(range(n)):
        assert run(prog, perm) == n - k, perm      # k-th largest of 0..n-1
        nperm += 1
    rng = random.Random(0)
    for _ in range(20000):
        xs = [rng.randint(0, 4) for _ in range(n)]
        assert run(prog, xs) == sorted(xs, reverse=True)[k - 1], xs
    print(f"{path}: OK  n={n} k={k} ops={len(prog)} "
          f"(min={sum(op == 'min' for op, _, _ in prog)}, max={sum(op == 'max' for op, _, _ in prog)}); "
          f"checked {2**n} 0/1 inputs, {nperm} permutations, 20000 random inputs with ties")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        check(p)
