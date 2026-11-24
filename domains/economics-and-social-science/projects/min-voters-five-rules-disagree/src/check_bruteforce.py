"""Compare the integer-programming minima with the exhaustive enumerations.

  python src/check_bruteforce.py

Reads results/bruteforce_*.txt, results/table_*.json and
results/robust_table_*.json. For every (m, rule set, convention) present in
both, the brute-force minimum must equal the solver minimum, or brute force
must have found nothing up to its bound N while the solver minimum exceeds N
(or does not exist). The two kinds of agreement are counted separately: only
the first is a positive match of a minimum.
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
n = npos = 0
for f in sorted(glob.glob(R + "/bruteforce_*.txt")):
    lines = open(f).read().split("\n")
    if not lines[0]:
        continue  # run not finished
    h = re.match(r"m=(\d+) N=(\d+)(?: convention=(\w+))?", lines[0])
    m, N, conv = int(h[1]), int(h[2]), h[3] or "strict"
    k = pos = 0
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
            pos += 1
        k += 1
    n += k
    npos += pos
    print(f"{os.path.basename(f)} (m={m}, all profiles up to {N} voters, {conv}): "
          f"{pos} minima equal, {k - pos} with nothing up to {N} voters and solver minimum above {N} or none")
assert n, "nothing compared: results/table_*.json or results/bruteforce_*.txt missing"
print(f"total: {npos} minima equal, {n - npos} consistent non-existence up to the bound")
