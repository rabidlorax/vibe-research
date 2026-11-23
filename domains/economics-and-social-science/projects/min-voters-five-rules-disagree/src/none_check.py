"""Exact proof for every "none" entry of the strict table.

  python src/none_check.py > results/none_check.txt

A case asks for integers x >= 0 with A x >= 1. If rational x >= 0 with
A x >= 1 exists, multiplying by a common denominator gives an integer
solution, so "no profile of any size" is equivalent to infeasibility of the
linear program. By Farkas' lemma that holds iff there is y >= 0 with
y.A <= 0 (componentwise) and sum(y) > 0. This script finds such a y for
every labelled case (reduce=False) of every (m, rules) whose table entry is
none, rounds it to small integers, and verifies y >= 0, y.A <= 0, sum(y) > 0
in exact integer arithmetic. The floating-point LP only proposes y; the
check does not depend on it.
"""
import glob, json, os
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from model import cases

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
todo = []
for f in sorted(glob.glob(R + "/table_*.json")):
    for r in json.load(open(f)):
        if r["min_voters"] is None:
            todo.append((r["m"], r["rules"]))
for m, rules in todo:
    ncase = 0
    for desc, A, _ in cases(m, rules, reduce=False):
        k = A.shape[0]
        res = linprog(np.zeros(k), A_ub=A.T, b_ub=np.zeros(A.shape[1]),
                      A_eq=np.ones((1, k)), b_eq=[1], bounds=(0, None), method="highs-ds")
        assert res.status == 0, (m, rules, desc, res.message)
        fr = [Fraction(float(v)).limit_denominator(1000) for v in res.x]
        den = int(np.lcm.reduce([f.denominator for f in fr]))
        y = [int(f * den) for f in fr]
        assert all(v >= 0 for v in y) and sum(y) > 0
        comb = [sum(y[i] * int(A[i, j]) for i in range(k)) for j in range(A.shape[1])]
        assert all(c <= 0 for c in comb), (m, rules, desc)
        ncase += 1
    print(f"m={m} {rules}: all {ncase} labelled cases have an exactly verified Farkas certificate")
