"""An independent Python re-implementation of the core of `statcheck`
(Epskamp & Nuijten): find null-hypothesis test results reported in running
text as  <statistic>(<df>) = <value>, p <=> <value>  and recompute the p-value.

It is written from the published description of the method, not ported from
the R source, and it is deliberately strict: only a t, F, r, chi-square or z
statistic, reported with "=", followed directly by a comma or semicolon and
the p-value, is extracted.
"""
import math
import re

from scipy import stats

ALPHA = 0.05
NUM = r"-?\s?\d*\.?\d+"
PVAL = (r"\s?[,;]\s?[pP]\s?(?P<pc>[<>=])\s?(?P<p>\d?\.\d+)"
        # the p-value must end here: not more digits, a second decimal point, scientific
        # notation (x 10, E-4) or a division such as ".05/3". A sentence-ending full stop is fine.
        r"(?!\d|\.\d|\s?[×x*·⋅]\s?\d|\s?[eE]\s?-?\d|\s?/\s?\d)")
NB = r"(?<![A-Za-z0-9])"  # statistic letter must not be the tail of a word

PATTERNS = {
    "t": re.compile(NB + r"t\s?\(\s?(?P<df2>\d+\.?\d*)\s?\)\s?=\s?(?P<stat>" + NUM + ")" + PVAL),
    "F": re.compile(NB + r"F\s?\(\s?(?P<df1>\d+\.?\d*)\s?,\s?(?P<df2>\d+\.?\d*)\s?\)\s?=\s?(?P<stat>"
                    + NUM + ")" + PVAL),
    "r": re.compile(NB + r"r\s?\(\s?(?P<df2>\d+)\s?\)\s?=\s?(?P<stat>-?\s?[01]?\.\d+)" + PVAL),
    "chi2": re.compile(r"(?:χ|Χ|𝜒|(?<![A-Za-z0-9])[Xx]|[Cc]hi)\s?(?:2|²)\s?\(\s?(?P<df1>\d+)\s?"
                       r"(?:,\s?[Nn]\s?=\s?\d[\d,]*\s?)?\)\s?=\s?(?P<stat>" + NUM + ")" + PVAL),
    "z": re.compile(r"(?<![A-Za-z0-9\-])(?P<zcase>[zZ])\s?=\s?(?P<stat>" + NUM + ")" + PVAL),
}
ONE_TAIL = re.compile(r"one[- ]?tailed|one[- ]?sided|directional", re.I)  # the three statcheck words
ONE_TAIL_STRICT = re.compile(r"one[- ]?tailed|one[- ]?sided", re.I)  # without "directional"

_TRANS = str.maketrans({
    "−": "-", "–": "-", "‒": "-", "‐": "-", "‑": "-", "﹣": "-", "－": "-",
    " ": " ", " ": " ", " ": " ", " ": " ", " ": " ", " ": " ", " ": " ",
    " ": " ", " ": " ", "​": "", "﻿": "", "＜": "<", "＞": ">", "＝": "=",
    "，": ",", "（": "(", "）": ")",
})


def normalize(text):
    """Map typographic minus signs and spaces to ASCII and collapse whitespace."""
    return re.sub(r"\s+", " ", text.translate(_TRANS))


def decimals(s):
    return len(s.split(".")[1]) if "." in s else 0


def _p(kind, x, df1, df2, tails=2):
    """Upper-tail (F, chi2) or two-tailed (t, r, z) p-value of |x|."""
    if kind == "t":
        return min(1.0, tails * stats.t.sf(x, df2))
    if kind == "z":
        return min(1.0, tails * stats.norm.sf(x))
    if kind == "r":
        if x >= 1:
            return 0.0
        return min(1.0, tails * stats.t.sf(x * math.sqrt(df2 / (1 - x * x)), df2))
    if kind == "F":
        return float(stats.f.sf(x, df1, df2))
    if kind == "chi2":
        return float(stats.chi2.sf(x, df1))
    raise ValueError(kind)


def p_range(kind, stat_str, df1, df2, tails=2):
    """Smallest and largest p-value compatible with the reported statistic,
    given that it was rounded to the number of decimals shown."""
    x = abs(float(stat_str.replace(" ", "")))
    h = 0.5 * 10 ** (-decimals(stat_str))
    lo, hi = max(0.0, x - h), x + h
    return float(_p(kind, hi, df1, df2, tails)), float(_p(kind, lo, df1, df2, tails))


def consistent(pc, p_str, pmin, pmax):
    """Is the reported p compatible with a computed p anywhere in [pmin, pmax]?"""
    p, d = float(p_str), decimals(p_str)
    eps = 1e-12
    if pc == "=":
        h = 0.5 * 10 ** (-d)  # reported value stands for [p - h, p + h]
        return (p - h <= pmax + eps) and (p + h >= pmin - eps)
    if pc == "<":
        return pmin < p
    return pmax > p


def reported_significant(pc, p_str):
    """True / False / None (cannot tell) at alpha = .05; p = .05 counts as significant."""
    p = float(p_str)
    if pc == "<":
        return True if p <= ALPHA else None
    if pc == "=":
        return p <= ALPHA
    return False if p >= ALPHA else None


def check(kind, stat_str, df1, df2, pc, p_str, one_tail_text=False, one_tail_strict=False):
    """Return a dict of flags for one extracted result, or None if not computable."""
    try:
        df1 = float(df1) if df1 is not None else None
        df2 = float(df2) if df2 is not None else None
        p = float(p_str)
    except ValueError:
        return None
    # Not checkable: p above 1, degrees of freedom below 1 (usually a standard error
    # printed in the parentheses), or "p < .000", which no p-value can satisfy.
    if p > 1 or (df1 is not None and df1 < 1) or (df2 is not None and df2 < 1):
        return None
    if pc == "<" and p == 0:
        return None
    if kind == "r" and abs(float(stat_str.replace(" ", ""))) > 1:
        return None
    pmin, pmax = p_range(kind, stat_str, df1, df2)
    err = not consistent(pc, p_str, pmin, pmax)
    sig = reported_significant(pc, p_str)

    def decision(lo, hi):
        if sig is None:
            return False
        return (sig and lo > ALPHA) or ((not sig) and hi <= ALPHA)

    dec = err and decision(pmin, pmax)
    # Variant that forgives results matching a one-tailed test when the article
    # mentions one-tailed / one-sided / directional tests anywhere in its body.
    half_ok = err and kind in ("t", "r", "z") and consistent(pc, p_str, pmin / 2, pmax / 2)
    err1, dec1 = (False, False) if (half_ok and one_tail_text) else (err, dec)
    err1s, dec1s = (False, False) if (half_ok and one_tail_strict) else (err, dec)
    return {"p_min": pmin, "p_max": pmax, "error": err, "decision_error": dec,
            "error_1t": err1, "decision_error_1t": dec1,
            "error_1t_strict": err1s, "decision_error_1t_strict": dec1s, "half_p_consistent": bool(half_ok),
            "p_zero": pc == "=" and p == 0.0}


def extract(text):
    """Yield one dict per test result found in already-normalized text."""
    one_tail = bool(ONE_TAIL.search(text))
    strict = bool(ONE_TAIL_STRICT.search(text))
    for kind, pat in PATTERNS.items():
        for m in pat.finditer(text):
            g = m.groupdict()
            res = check(kind, g["stat"], g.get("df1"), g.get("df2"), g["pc"], g["p"], one_tail, strict)
            if res is None:
                continue
            res.update(kind=kind, df1=g.get("df1") or "", df2=g.get("df2") or "",
                       stat=g["stat"].replace(" ", ""), p_cmp=g["pc"], p_rep=g["p"],
                       raw=m.group(0), start=m.start(), end=m.end())
            yield res
