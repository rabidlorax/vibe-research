"""Integer-programming model: one linear system per "case".

Variables: x[r] >= 0 integer, the number of voters with ranking r, for all
m! rankings. A case fixes who wins under each rule and the auxiliary choices
that make every rule linear (Hare elimination order, runoff pair). Every
constraint has the form  a . x >= 1  with integer a (a strict inequality
between integer quantities).

cases(m, rules, reduce=True) uses the freedom to rename candidates;
reduce=False enumerates every labelled case and is used as a cross-check.
"""
from itertools import permutations
import numpy as np


class Builder:
    def __init__(self, m):
        self.m = m
        self.rankings = list(permutations(range(m)))
        self.pos = np.array([[r.index(c) for c in range(m)] for r in self.rankings])
        self.rows = []

    def first(self, c, alive):
        """Indicator vector: c is the top candidate of the ranking within alive."""
        others = [d for d in alive if d != c]
        if not others:
            return np.ones(len(self.rankings), dtype=np.int64)
        return (self.pos[:, [c]] < self.pos[:, others]).all(axis=1).astype(np.int64)

    def above(self, a, b):
        return (self.pos[:, a] < self.pos[:, b]).astype(np.int64)

    def gt(self, u, v):
        self.rows.append(u - v)

    def plurality(self, w):
        allc = range(self.m)
        for c in allc:
            if c != w:
                self.gt(self.first(w, allc), self.first(c, allc))

    def runoff(self, w, l):
        """w and l are the top two by first places; w beats l pairwise."""
        allc = range(self.m)
        for t in (w, l):
            for c in allc:
                if c not in (w, l):
                    self.gt(self.first(t, allc), self.first(c, allc))
        self.gt(self.above(w, l), self.above(l, w))

    def hare(self, order, stop=None):
        """order[0] is eliminated first, ..., order[-1] wins.

        stop=None: a unique candidate has fewest first places in every round.
        stop=k ("majority stop"): that holds in rounds 0..k-1 only, and in
        round k the winner has more than half of all first places, so the
        count ends there and later rounds are unconstrained.
        """
        rounds = self.m - 1 if stop is None else stop
        for k in range(rounds):
            alive = order[k:]
            for c in alive[1:]:
                self.gt(self.first(c, alive), self.first(alive[0], alive))
        if stop is not None:
            one = np.ones(len(self.rankings), dtype=np.int64)
            self.gt(2 * self.first(order[-1], order[stop:]), one)

    def borda(self, w):
        score = lambda c: (self.m - 1 - self.pos[:, c]).astype(np.int64)
        for c in range(self.m):
            if c != w:
                self.gt(score(w), score(c))

    def condorcet(self, w):
        for c in range(self.m):
            if c != w:
                self.gt(self.above(w, c), self.above(c, w))

    def matrix(self):
        return np.array(self.rows, dtype=np.int64)


def cases(m, rules="PRHBC", reduce=True, majority_stop=False):
    """Yield (description, A, rankings): profiles x >= 0 integer with A x >= 1.

    majority_stop=True replaces the Hare convention by "the count stops as
    soon as a candidate has a majority; no tie for fewest first places
    before that": one case per stopping round. (Only the first `stop`
    eliminated candidates are then distinguished, so with reduce=True some
    cases are equivalent to each other; that costs time, not correctness.)
    """
    rules = [k for k in "PRHBC" if k in rules]
    k = len(rules)
    assert m >= k
    seen = set()
    hare_orders = [tuple(range(m))] if reduce else list(permutations(range(m)))
    if "H" not in rules:
        hare_orders = [None]
    for order in hare_orders:
        for assign in permutations(range(m), k):
            w = dict(zip(rules, assign))
            if "H" in rules and w["H"] != order[-1]:
                continue
            if "R" in rules:
                if "P" in rules:
                    opps = [w["P"]]  # plurality winner is in the runoff and loses it
                else:
                    opps = [c for c in range(m) if c != w["R"]]
            else:
                opps = [None]
            stops = list(range(m - 1)) if (majority_stop and "H" in rules) else [None]
            for opp, stop in ((o, s) for o in opps for s in stops):
                if reduce and "H" not in rules:
                    # rename candidates: winners become 0..k-1 in rule order,
                    # a non-winning runoff opponent becomes k
                    if assign != tuple(range(k)):
                        continue
                    if opp is not None and opp >= k and opp != k:
                        continue
                if "C" in rules and opp is not None and opp == w["C"]:
                    continue  # a Condorcet winner cannot lose a runoff
                b = Builder(m)
                if "P" in rules:
                    b.plurality(w["P"])
                if "R" in rules:
                    b.runoff(w["R"], opp)
                if "H" in rules:
                    b.hare(order, stop)
                if "B" in rules:
                    b.borda(w["B"])
                if "C" in rules:
                    b.condorcet(w["C"])
                desc = dict(winners=w, hare_order=order, runoff_loser=opp, hare_stop=stop)
                key = repr(desc)
                assert key not in seen
                seen.add(key)
                yield desc, b.matrix(), b.rankings
