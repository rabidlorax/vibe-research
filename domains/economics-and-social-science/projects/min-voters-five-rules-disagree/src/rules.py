"""Direct implementations of the five rules on a profile.

A profile is a dict {ranking: count}; a ranking is a tuple of candidate
indices, best first. Every function in the first part returns the winner, or
None when a tie occurs at any step of the rule (the "strict" convention of
the README; hare() continues until one candidate is left). This file is deliberately independent of model.py: it is the
referee that checks witnesses produced by the solvers.
"""


def first_places(profile, alive):
    f = {c: 0 for c in alive}
    for r, k in profile.items():
        for c in r:
            if c in f:
                f[c] += k
                break
    return f


def beats(profile, a, b):
    """Voters ranking a above b minus voters ranking b above a."""
    d = 0
    for r, k in profile.items():
        d += k if r.index(a) < r.index(b) else -k
    return d


def unique_max(score):
    best = max(score.values())
    top = [c for c, s in score.items() if s == best]
    return top[0] if len(top) == 1 else None


def plurality(profile, m):
    return unique_max(first_places(profile, range(m)))


def runoff(profile, m):
    f = first_places(profile, range(m))
    order = sorted(f, key=lambda c: -f[c])
    a, b = order[0], order[1]
    if m > 2 and f[b] == f[order[2]]:
        return None  # who reaches the runoff is not determined
    d = beats(profile, a, b)
    return a if d > 0 else b if d < 0 else None


def hare(profile, m):
    alive = set(range(m))
    while len(alive) > 1:
        f = first_places(profile, alive)
        low = min(f.values())
        losers = [c for c in alive if f[c] == low]
        if len(losers) != 1:
            return None
        alive.remove(losers[0])
    return alive.pop()


def hare_majority_stop(profile, m):
    """Hare, stopping as soon as someone has more than half of the first places."""
    n = sum(profile.values())
    alive = set(range(m))
    while True:
        f = first_places(profile, alive)
        for c in alive:
            if 2 * f[c] > n:
                return c
        low = min(f.values())
        losers = [c for c in alive if f[c] == low]
        if len(losers) != 1:
            return None
        alive.remove(losers[0])


def borda(profile, m):
    s = {c: 0 for c in range(m)}
    for r, k in profile.items():
        for pos, c in enumerate(r):
            s[c] += k * (m - 1 - pos)
    return unique_max(s)


def condorcet(profile, m):
    for c in range(m):
        if all(beats(profile, c, d) > 0 for d in range(m) if d != c):
            return c
    return None


RULES = {"P": plurality, "R": runoff, "H": hare, "B": borda, "C": condorcet}


def winners(profile, m, rules="PRHBC", majority_stop=False):
    table = dict(RULES, H=hare_majority_stop) if majority_stop else RULES
    return {k: table[k](profile, m) for k in rules}


# --- "robust" convention: ties allowed, winner must not depend on tie-breaks ---

def hare_winner_set(profile, m, alive=None):
    alive = frozenset(range(m)) if alive is None else alive
    if len(alive) == 1:
        return set(alive)
    f = first_places(profile, alive)
    low = min(f.values())
    out = set()
    for c in alive:
        if f[c] == low:
            out |= hare_winner_set(profile, m, alive - {c})
    return out


def hare_robust(profile, m):
    s = hare_winner_set(profile, m)
    return s.pop() if len(s) == 1 else None


def runoff_robust(profile, m):
    f = first_places(profile, range(m))
    vals = sorted(f.values(), reverse=True)
    top = [c for c in f if f[c] == vals[0]]
    if len(top) >= 2:
        pairs = [(a, b) for a in top for b in top if a < b]
    else:
        pairs = [(top[0], c) for c in f if f[c] == vals[1]]
    out = set()
    for a, b in pairs:
        d = beats(profile, a, b)
        if d == 0:
            return None
        out.add(a if d > 0 else b)
    return out.pop() if len(out) == 1 else None


ROBUST = dict(RULES, R=runoff_robust, H=hare_robust)


def winners_robust(profile, m, rules="PRHBC"):
    return {k: ROBUST[k](profile, m) for k in rules}
