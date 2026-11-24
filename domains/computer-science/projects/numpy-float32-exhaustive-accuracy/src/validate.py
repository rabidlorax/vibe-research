#!/usr/bin/env python3
"""Independent check of the reference used by sweep.py.

For each function, draw random bit patterns (fixed seed) plus a list of special
values, and compare sweep.reference() with a rounding of the exact value done
by mpmath alone (no float64, no margin test).  Any disagreement is an error.

Usage: python validate.py [--n 20000]
"""
import argparse
import json
import sys

import mpmath
import numpy as np

import sweep

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=20000)
a = ap.parse_args()
report = {}
bad = 0
for dtype, fmt in sweep.FMT.items():
    rng = np.random.default_rng(20261123)
    n = a.n if dtype == "float32" else 1 << 16
    if dtype == "float32":
        bits = rng.integers(0, 1 << 32, size=n, dtype=np.uint64).astype(np.uint32)
        # extra samples concentrated where results are not saturated
        mid = rng.uniform(-12, 12, size=n).astype(np.float32).view(np.uint32)
        special = np.array([0, 1, 0x007fffff, 0x00800000, 0x3f800000, 0x7f7fffff, 0x7f800000,
                            0x80000000, 0x80000001, 0xbf800000, 0xff7fffff, 0xff800000],
                           dtype=np.uint32)
        bits = np.concatenate([bits, mid, special])
    else:
        bits = np.arange(1 << 16, dtype=np.uint16)      # all of float16
    x = bits.view(fmt["t"])
    for name in sweep.NAMES:
        ref, _, st = sweep.reference(name, x, fmt)
        nd = 0
        for i in range(x.size):
            xf = float(x[i])
            if np.isnan(x[i]) or np.isnan(ref[i]):
                continue          # domain handled by the two float64 libraries agreeing
            if np.isinf(x[i]):
                continue
            v = sweep.mp_exact(name, xf)
            if isinstance(v, mpmath.mpc):
                nd += 1
                continue
            c = fmt["t"](sweep.mp_round(v, fmt, exact=sweep.is_exact(name, xf)))
            if c.tobytes() != ref[i].tobytes() and not (c == 0 and ref[i] == 0):
                nd += 1
                print("MISMATCH", dtype, name, hex(int(bits[i])), float(ref[i]), float(c))
        bad += nd
        report[f"{dtype}_{name}"] = {"checked": int(x.size), "disagree": nd, "hard": st["hard"]}
        print(dtype, name, report[f"{dtype}_{name}"], flush=True)
(sweep.RESULTS / "validate.json").write_text(json.dumps(report, indent=1) + "\n")
sys.exit(1 if bad else 0)
