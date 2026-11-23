"""Compare the integer-programming minima with the exhaustive enumerations.

  python src/check_bruteforce.py

Reads results/bruteforce_*.txt, results/table_*.json and
results/robust_table_*.json. For every (m, rule set, convention) present in
both, the brute-force minimum must equal the solver minimum, or brute force
must have found nothing up to its bound N while the solver minimum exceeds N
(or does not exist).
"""
import glob, json, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
ilp = {}
for f in glob.glob(R + "/table_*.json"):
    for r in json.load(open(f)):
        ilp[(r["m"], r["rules"], "strict")] = r["min_voters"]
for f in glob.glob(R + "/robust_table_*.json"):
    for r in json.load(open(f)):
        ilp[(r["m"], r["rules"], "robust")] = r["min_voters"]
n = 0
for f in sorted(glob.glob(R + "/bruteforce_*.txt")):
    lines = open(f).read().split("\n")
    if not lines[0]:
        continue  # run not finished
    h = re.match(r"m=(\d+) N=(\d+)(?: convention=(\w+))?", lines[0])
    m, N, conv = int(h[1]), int(h[2]), h[3] or "strict"
    k = 0
    for line in lines[1:]:
        if not line:
            continue
        rules, v = line.split()
        key = (m, rules, conv)
        if key not in ilp:
            continue
        want = ilp[key]
        if v == "-":
            assert want is None or want > N, (key, v, want)
        else:
            assert want == int(v), (key, v, want)
        k += 1
    n += k
    print(f"{os.path.basename(f)}: {k} rule sets agree (m={m}, all profiles up to {N} voters, {conv})")
print("total comparisons:", n)
