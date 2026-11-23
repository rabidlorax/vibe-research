"""SAT encoding: is there a monotone {AND, OR} circuit with s two-input gates
computing a k-out-of-n threshold function (k = (n+1)/2 gives majority)?

AND corresponds to min and OR to max, so by the threshold principle a model
is a straight-line min/max program computing the k-th largest of n values
(the median when k = (n+1)/2).

Nodes 0..n-1 are the inputs, nodes n..n+s-1 the gates, the last gate is the
output.  A monotone circuit computes a monotone function, so it computes the
threshold function iff it outputs 0 on every input of weight k-1 and 1 on
every input of weight k.  Only those rows are encoded, and each needs only
one direction of the gate semantics:

  * on a weight-k row ("1-row") we need: value variable true  => node is truly 1
  * on a weight-(k-1) row ("0-row") we need: value variable false => node is truly 0

Symmetry breaking (each `sym` level includes the previous ones; all are
"without loss of generality", argued in the README):

  1  operands ordered a < b; gates listed in non-decreasing colexicographic
     order of (b, a); two gates with identical operands are AND then OR;
     every non-output gate is used by a later gate.
  2  (majority only, k = (n+1)/2) the first gate is AND(x0, x1).
  3  input variables are first used in index order.
"""
from itertools import combinations


class CNF:
    def __init__(self):
        self.nv = 0
        self.clauses = []

    def var(self):
        self.nv += 1
        return self.nv

    def add(self, *lits):
        self.clauses.append([l for l in lits])

    def exactly_one(self, lits):
        self.add(*lits)
        for x, y in combinations(lits, 2):
            self.add(-x, -y)

    def write(self, path):
        with open(path, "w") as f:
            f.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            for c in self.clauses:
                f.write(" ".join(map(str, c)) + " 0\n")


def rows(n, w):
    """All 0/1 vectors of length n and weight w, as tuples."""
    out = []
    for ones in combinations(range(n), w):
        r = [0] * n
        for i in ones:
            r[i] = 1
        out.append(tuple(r))
    return out


def encode(n, s, k=None, sym=3, prefix=(), one_rows=None, zero_rows=None):
    """Return (cnf, meta).  meta maps names to variables for decoding.

    one_rows / zero_rows: instead of a threshold function, encode an arbitrary
    monotone function given by rows on which the output must be 1 and rows on
    which it must be 0 (its minimal true points and maximal false points are
    enough, by monotonicity).  Only sym<=1 is valid then, since sym 2 and 3
    use the symmetry and self-duality of majority.

    prefix: optional list of (op, a, b) fixing the first gates.  This restricts
    the search (useful only for finding programs, never for lower bounds) and
    must be combined with sym<=1.  With a prefix, the sym=1 constraints
    (ordering, every gate used) are applied to the free gates only.
    """
    assert not prefix or sym <= 1
    first_free = n + len(prefix)
    if k is None:
        k = (n + 1) // 2
    cnf = CNF()
    N = n + s
    gates = range(n, N)
    isor = {g: cnf.var() for g in gates}                      # 1 = OR/max, 0 = AND/min
    A = {g: {j: cnf.var() for j in range(0, g - 1)} for g in gates}   # first operand
    B = {g: {j: cnf.var() for j in range(1, g)} for g in gates}       # second operand
    for g in gates:
        cnf.exactly_one(list(A[g].values()))
        cnf.exactly_one(list(B[g].values()))
        # a < b
        for j in A[g]:
            for l in B[g]:
                if l <= j:
                    cnf.add(-A[g][j], -B[g][l])

    if one_rows is None:
        one_rows = rows(n, k)
        zero_rows = rows(n, k - 1)
    else:
        assert sym <= 1
    for pol, rs in ((1, one_rows), (0, zero_rows)):
        for r in rs:
            v = {g: cnf.var() for g in gates}
            for g in gates:
                p, q = cnf.var(), cnf.var()        # operand values on this row
                for j, sel in A[g].items():
                    _link(cnf, pol, sel, p, j, r, v, n)
                for j, sel in B[g].items():
                    _link(cnf, pol, sel, q, j, r, v, n)
                if pol == 1:
                    # v true => gate truly 1
                    cnf.add(-v[g], isor[g], p)           # AND: both
                    cnf.add(-v[g], isor[g], q)
                    cnf.add(-v[g], -isor[g], p, q)       # OR: one
                else:
                    # v false => gate truly 0  (p, q false mean operand truly 0)
                    cnf.add(v[g], -isor[g], -p)          # OR: both 0
                    cnf.add(v[g], -isor[g], -q)
                    cnf.add(v[g], isor[g], -p, -q)       # AND: one 0
            cnf.add(v[N - 1] if pol == 1 else -v[N - 1])

    for i, (op, a, b) in enumerate(prefix):
        cnf.add(A[n + i][a])
        cnf.add(B[n + i][b])
        cnf.add(isor[n + i] if op == "max" else -isor[n + i])

    if sym >= 1:
        # every non-output gate is used later
        for g in range(first_free, N - 1):
            cnf.add(*[A[h][g] for h in range(g + 1, N) if g in A[h]],
                    *[B[h][g] for h in range(g + 1, N) if g in B[h]])
        # colex order on (b, a) between consecutive gates, ties: AND before OR
        for g in range(first_free, N - 1):
            h = g + 1
            for b in B[g]:
                for b2 in B[h]:
                    if b2 < b:
                        cnf.add(-B[g][b], -B[h][b2])
                if b in B[h]:
                    for a in A[g]:
                        for a2 in A[h]:
                            if a2 < a:
                                cnf.add(-B[g][b], -B[h][b], -A[g][a], -A[h][a2])
                        if a in A[h]:
                            # same operands: g is AND, h is OR
                            cnf.add(-B[g][b], -B[h][b], -A[g][a], -A[h][a], -isor[g])
                            cnf.add(-B[g][b], -B[h][b], -A[g][a], -A[h][a], isor[h])
    if sym >= 2 and 2 * k == n + 1:
        cnf.add(A[n][0])
        cnf.add(B[n][1])
        cnf.add(-isor[n])
    if sym >= 3:
        # variable i+1 is not used by gate g unless variable i is used by some gate <= g
        # (as operand of an earlier gate, or as the first operand of g itself)
        used = {}
        for i in range(n):
            for g in gates:
                u = cnf.var()
                used[i, g] = u
                # u <=> used[i, g-1] or A[g][i] or B[g][i]
                parts = []
                if g > n:
                    parts.append(used[i, g - 1])
                if i in A[g]:
                    parts.append(A[g][i])
                if i in B[g]:
                    parts.append(B[g][i])
                cnf.add(-u, *parts)
                for x in parts:
                    cnf.add(u, -x)
        for i in range(n - 1):
            for g in gates:
                prev = used[i, g - 1] if g > n else None
                # using i+1 at gate g requires i used before g, or i is g's first operand
                for sel in ([A[g][i + 1]] if i + 1 in A[g] else []) + \
                           ([B[g][i + 1]] if i + 1 in B[g] else []):
                    lits = [-sel]
                    if prev is not None:
                        lits.append(prev)
                    if i in A[g]:
                        lits.append(A[g][i])
                    cnf.add(*lits)
    return cnf, dict(n=n, s=s, k=k, isor=isor, A=A, B=B)


def _link(cnf, pol, sel, pv, j, r, v, n):
    """Tie operand-value variable pv to node j's value when selector sel holds."""
    if j < n:
        if pol == 1 and r[j] == 0:
            cnf.add(-sel, -pv)       # pv true would claim a 1 that is not there
        if pol == 0 and r[j] == 1:
            cnf.add(-sel, pv)        # pv false would claim a 0 that is not there
    else:
        if pol == 1:
            cnf.add(-sel, -pv, v[j])
        else:
            cnf.add(-sel, pv, -v[j])


def decode(model, meta):
    """Return the circuit as a list of (op, a, b) with op in {'min', 'max'}."""
    pos = set(l for l in model if l > 0)
    out = []
    for g in range(meta["n"], meta["n"] + meta["s"]):
        a = next(j for j, x in meta["A"][g].items() if x in pos)
        b = next(j for j, x in meta["B"][g].items() if x in pos)
        out.append(("max" if meta["isor"][g] in pos else "min", a, b))
    return out
