"""Minimum voters for every set of >= 2 rules and m = 3..MAXM candidates.

  python src/table.py MAXM > results/table.json
"""
import json, sys
from itertools import combinations
from solve import solve

maxm = int(sys.argv[1])
rows = []
for m in range(3, maxm + 1):
    for k in range(2, 6):
        if k > m:
            continue
        for sub in combinations("PRHBC", k):
            r = solve(m, "".join(sub))
            rows.append(r)
            print(m, "".join(sub), r["min_voters"], r["cases"], file=sys.stderr, flush=True)
json.dump(rows, sys.stdout, indent=0)
