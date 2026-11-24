"""Compare the SAT minima (catalogue_check CSVs) with the SAT-free brute-force
enumeration (brute_force.py output).

  * 4 variables: brute force to 7 gates covers every monotone function, so
    every class minimum must agree exactly.
  * 5 variables: brute force to 5 gates. Classes with SAT minimum <= 5 must
    have exactly that brute-force value; classes with SAT minimum > 5 must be
    absent from the brute-force output.

The catalogue numbers a function by its truth table; we recompute the truth
table from the catalogue's list of true points rather than rely on that.
Usage: python cross_check.py
"""
import csv
from catalogue_check import parse


def brute(path):
    best = {}
    for l in open(path):
        p = l.split()
        if len(p) == 2 and p[0].isdigit():
            best[int(p[0])] = int(p[1])
    return best


def table(true_pts, n):
    t = 0
    for r in range(1 << n):
        if tuple(r >> i & 1 for i in range(n)) in true_pts:
            t |= 1 << r
    return t


for n, cat, res, bf, depth in (
        (4, "../data/raw/MonoCatFileA4var.txt", "../results/catalogue_check_4var.csv",
         "../results/brute_force_n4_d7.txt", 7),
        (5, "../data/raw/MonoCatFileA5var.txt", "../results/catalogue_check.csv",
         "../results/brute_force_n5_d5.txt", 5)):
    sat = {int(r["function"]): int(r["minimum_gates"]) for r in csv.DictReader(open(res))}
    b = brute(bf)
    agree = absent = 0
    for num, true_pts, _ in parse(cat):
        t = table(true_pts, n)
        if t in (0, (1 << (1 << n)) - 1):
            continue                       # constants: brute force starts from inputs
        if sat[num] <= depth:
            assert b.get(t) == sat[num], (n, num, sat[num], b.get(t))
            agree += 1
        else:
            assert t not in b, (n, num)
            absent += 1
    print(f"n={n}: {agree} classes agree exactly with brute force (<= {depth} gates); "
          f"{absent} classes with SAT minimum > {depth} are correctly not reachable in {depth} gates")
