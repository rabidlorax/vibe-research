"""Strict minima for m = 6 only:  python src/table6.py > results/table_m6.json"""
import json, sys
from itertools import combinations
from solve import solve
rows = []
for k in range(2, 6):
    for sub in combinations("PRHBC", k):
        r = solve(6, "".join(sub))
        rows.append(r)
        print(6, "".join(sub), r["min_voters"], r["cases"], file=sys.stderr, flush=True)
json.dump(rows, sys.stdout, indent=0)
