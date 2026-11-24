#!/usr/bin/env python3
"""Independent check of the reference used by sweep.py.

The oracle is MPFR (through gmpy2), asked to round directly to the target
format: precision 24 with the binary32 exponent range and subnormalisation
(precision 11 for binary16).  It shares no code with sweep.reference(): no
float64 step, no margin test, no mpmath, no sweep.mp_round.

Inputs compared with the oracle, bit for bit including the sign of zero:
  float32: 1,000,000 random bit patterns, 1,000,000 values uniform in [-12, 12),
           12 special values, and every *hard* input (the ones sweep.py sends
           to mpmath) found in 16 blocks of 2**22 consecutive bit patterns;
  float16: all 65,536 bit patterns.
Inputs whose reference is NaN are not compared (the oracle's NaN-ness is
compared instead: both must be NaN).

Usage: python validate.py
"""
import json
import sys

import gmpy2
import numpy as np

import sweep

CTX = {
    "float32": dict(precision=24, emax=128, emin=-148, subnormalize=True),
    "float16": dict(precision=11, emax=16, emin=-23, subnormalize=True),
}
GNAME = {"arcsin": "asin", "arccos": "acos", "arctan": "atan", "arcsinh": "asinh",
         "arccosh": "acosh", "arctanh": "atanh"}
# starts of the dense float32 blocks (bit patterns), chosen to cover small,
# moderate and large magnitudes of both signs
BLOCKS = [0x00000000, 0x00800000, 0x32000000, 0x3a000000, 0x3f000000, 0x3f7c0000,
          0x3f800000, 0x40490000, 0x42000000, 0x42f00000, 0x4a000000, 0x7f000000,
          0xbf000000, 0xbf800000, 0xc2000000, 0xc2f00000]
BLOCK = 1 << 22


def oracle(name, xs, dtype):
    fn = getattr(gmpy2, GNAME.get(name, name))
    out = np.empty(xs.size, dtype=sweep.FMT[dtype]["t"])
    with gmpy2.context(gmpy2.ieee(64), **CTX[dtype]):
        for i, v in enumerate(xs):
            out[i] = float(fn(gmpy2.mpfr(float(v))))
    return out


def compare(name, x, dtype, fmt, only=None):
    ref, _, st, hidx = sweep.reference(name, x, fmt)
    idx = np.arange(x.size) if only is None else (hidx if only == "hard" else only)
    orc = oracle(name, x[idx], dtype)
    r = ref[idx]
    rn, on = np.isnan(r), np.isnan(orc)
    bad = (rn != on) | (~rn & ~on & (r.view(fmt["u"]) != orc.view(fmt["u"])))
    for j in np.flatnonzero(bad)[:5]:
        print("MISMATCH", dtype, name, hex(int(x[idx][j:j + 1].view(fmt["u"])[0])), float(r[j]), float(orc[j]))
    return int(np.count_nonzero(~rn & ~on)), int(np.count_nonzero(rn & on)), int(np.count_nonzero(bad)), int(hidx.size)


report = {}
total_bad = 0
rng = np.random.default_rng(20261123)
f32 = sweep.FMT["float32"]
rand_bits = rng.integers(0, 1 << 32, size=1000000, dtype=np.uint64).astype(np.uint32)
mid = rng.uniform(-12, 12, size=1000000).astype(np.float32).view(np.uint32)
special = np.array([0, 1, 0x007fffff, 0x00800000, 0x3f800000, 0x7f7fffff, 0x7f800000,
                    0x80000000, 0x80000001, 0xbf800000, 0xff7fffff, 0xff800000], dtype=np.uint32)
xs32 = np.concatenate([rand_bits, mid, special]).view(np.float32)
for name in sweep.NAMES:
    cmp_n, nan_n, bad, _ = compare(name, xs32, "float32", f32)
    hard_cmp = 0
    for s in BLOCKS:
        xb = np.arange(s, s + BLOCK, dtype=np.uint64).astype(np.uint32).view(np.float32)
        c, n, b, h = compare(name, xb, "float32", f32, only="hard")
        hard_cmp += c
        bad += b
    report[f"float32_{name}"] = {"sampled": int(xs32.size), "compared_non_nan": cmp_n,
                                 "both_nan": nan_n, "hard_inputs_compared": hard_cmp, "disagree": bad}
    total_bad += bad
    print("float32", name, report[f"float32_{name}"], flush=True)
f16 = sweep.FMT["float16"]
x16 = np.arange(1 << 16, dtype=np.uint16).view(np.float16)
for name in sweep.NAMES:
    cmp_n, nan_n, bad, h = compare(name, x16, "float16", f16)
    report[f"float16_{name}"] = {"sampled": int(x16.size), "compared_non_nan": cmp_n,
                                 "both_nan": nan_n, "hard_inputs_in_sample": h, "disagree": bad}
    total_bad += bad
    print("float16", name, report[f"float16_{name}"], flush=True)
(sweep.RESULTS / "validate.json").write_text(json.dumps(report, indent=1) + "\n")
sys.exit(1 if total_bad else 0)
