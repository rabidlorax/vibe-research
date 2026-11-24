"""Robust-convention minima for every rule set containing P and H, m = 3..MAXM.

  python src/robust_table.py 5 > results/robust_table_m3to5.json
"""
import json, subprocess, sys
from itertools import combinations

maxm = int(sys.argv[1])
rows = []
for m in range(3, maxm + 1):
    for k in range(0, 4):
        for extra in combinations("RBC", k):
            rules = "".join(c for c in "PRHBC" if c in "PH" + "".join(extra))
            if len(rules) > m:
                continue
            r = json.loads(subprocess.run([sys.executable, __file__.replace("robust_table", "robust"), str(m), rules],
                                          capture_output=True, text=True, check=True).stdout)
            rows.append(r)
            print(m, rules, r["min_voters"], file=sys.stderr, flush=True)
json.dump(rows, sys.stdout, indent=0)
