#!/usr/bin/env python3
"""Exhaustive accuracy sweep of NumPy float32 / float16 unary math ufuncs.

For every bit pattern of the input type, compare NumPy's result with the
correctly rounded result (round-to-nearest-even of the exact value).

Reference construction (see README "Method"):
  A = the same NumPy ufunc evaluated in float64
  B = the C library's double function (src/ref_libm.c)
  An input is "hard" if A and B round to different target-precision values,
  or either lies within MARGIN of the gap from a rounding boundary.  Hard
  inputs are decided by mpmath at high precision.  All other inputs take the
  rounding of A.

Usage: python sweep.py FUNC [--dtype float32|float16] [--workers N]
"""
import argparse
import ctypes
import json
import math
import os
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import mpmath
from mpmath import mp, mpf

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"

# name, direction on negative inputs, direction on positive inputs
# (+1 nondecreasing in x, -1 nonincreasing, 0 not monotone / not checked)
FUNCS = [
    ("exp", 1, 1), ("exp2", 1, 1), ("expm1", 1, 1),
    ("log", 0, 1), ("log2", 0, 1), ("log10", 0, 1), ("log1p", 1, 1),
    ("sin", 0, 0), ("cos", 0, 0), ("tan", 0, 0),
    ("arcsin", 1, 1), ("arccos", -1, -1), ("arctan", 1, 1),
    ("sinh", 1, 1), ("cosh", -1, 1), ("tanh", 1, 1),
    ("arcsinh", 1, 1), ("arccosh", 0, 1), ("arctanh", 1, 1),
    ("cbrt", 1, 1), ("sqrt", 0, 1),
]
NAMES = [f[0] for f in FUNCS]
MP_PREC = 1200          # bits used to decide hard cases
MARGIN = 2.0 ** -16     # fraction of the gap between neighbours

MPF = {
    "exp": mpmath.exp, "exp2": lambda x: mpmath.power(2, x), "expm1": mpmath.expm1,
    "log": mpmath.log, "log2": lambda x: mpmath.log(x) / mpmath.log(2),
    "log10": lambda x: mpmath.log(x) / mpmath.log(10), "log1p": mpmath.log1p,
    "sin": mpmath.sin, "cos": mpmath.cos, "tan": mpmath.tan,
    "arcsin": mpmath.asin, "arccos": mpmath.acos, "arctan": mpmath.atan,
    "sinh": mpmath.sinh, "cosh": mpmath.cosh, "tanh": mpmath.tanh,
    "arcsinh": mpmath.asinh, "arccosh": mpmath.acosh, "arctanh": mpmath.atanh,
    "cbrt": lambda x: -mpmath.cbrt(-x) if x < 0 else mpmath.cbrt(x), "sqrt": mpmath.sqrt,
}

FMT = {
    # mantissa bits (excluding implicit), min normal exponent, max exponent+1, uint type
    "float32": dict(t=np.float32, u=np.uint32, bits=32, p=23, emin=-126, emax=128),
    "float16": dict(t=np.float16, u=np.uint16, bits=16, p=10, emin=-14, emax=16),
}


def build_lib():
    so = HERE / "ref_libm.so"
    src = HERE / "ref_libm.c"
    if not so.exists() or so.stat().st_mtime < src.stat().st_mtime:
        subprocess.check_call(["gcc", "-O2", "-fno-builtin", "-fno-fast-math", "-shared",
                               "-fPIC", str(src), "-o", str(so), "-lm"])
    lib = ctypes.CDLL(str(so))
    lib.apply.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    lib.apply.restype = None
    return lib


_lib = None


def libm(fid, xd):
    global _lib
    if _lib is None:
        _lib = build_lib()
    xd = np.ascontiguousarray(xd)
    out = np.empty_like(xd)
    _lib.apply(fid, xd.ctypes.data, out.ctypes.data, xd.size)
    return out


def is_exact(name, xf):
    """True when mp_exact returns the exact real value: exp2 at an integer."""
    return name == "exp2" and math.isfinite(xf) and xf == int(xf)


def mp_exact(name, xf):
    """Exact value f(x) as mpf at MP_PREC bits; x is a Python float (exact)."""
    mp.prec = MP_PREC
    return MPF[name](mpf(xf))


def mp_round(v, fmt, exact=False):
    """Round a real mpf to the target format, nearest-even. Returns Python float.
    exact=True asserts that v is the exact value (not an approximation), which
    is the only situation in which a tie can be recognised and broken to even."""
    mp.prec = MP_PREC
    if v == 0:
        return 0.0
    if mpmath.isinf(v):
        return math.inf if v > 0 else -math.inf
    s = -1.0 if v < 0 else 1.0
    a = abs(v)
    m, e = mpmath.frexp(a)             # a = m * 2**e, 0.5 <= m < 1
    k = max(int(e) - 1, fmt["emin"]) - fmt["p"]   # ulp = 2**k
    q = mpmath.ldexp(a, -k)
    n = int(mpmath.floor(q))
    frac = q - n
    if exact and frac == 0.5:
        n += n & 1
    elif abs(frac - 0.5) < mpf(2) ** -300:
        raise ArithmeticError("cannot separate value from a rounding midpoint")
    elif frac > 0.5:
        n += 1
    if n.bit_length() + k > fmt["emax"]:      # n * 2**k >= 2**emax
        return s * math.inf
    return s * math.ldexp(n, k)


def mp_ulp_err(name, xf, yf, fmt):
    """|y - f(x)| in ulps of the exact value's binade (ulp floored at the subnormal spacing)."""
    v = mp_exact(name, xf)
    a = abs(v)
    if a == 0:
        k = fmt["emin"] - fmt["p"]
    else:
        m, e = mpmath.frexp(a)
        k = max(int(e) - 1, fmt["emin"]) - fmt["p"]
    return float(abs(mpf(yf) - v) / mpf(2) ** k)


def near_boundary(yd, r, fmt):
    """True where the float64 value yd is within MARGIN*gap of the midpoint
    that separates r (its rounding to the target type) from the next value."""
    t = fmt["t"]
    big = 2.0 ** fmt["emax"]
    topgap = 2.0 ** (fmt["emax"] - 1 - fmt["p"])
    thresh = big - topgap / 2            # at or above this, rounds to inf
    fin = np.isfinite(yd)
    r64 = r.astype(np.float64)
    rinf = np.isinf(r64) & fin
    r64s = np.where(np.isfinite(r64), r64, 0.0)
    d = np.where(fin, yd, 0.0) - r64s
    toward = np.where(d > 0, np.inf, -np.inf).astype(t)
    nxt = np.nextafter(r, toward).astype(np.float64)
    gap = np.abs(nxt - r64s)
    gap = np.where(np.isfinite(gap), gap, topgap)
    near = fin & ~rinf & (d != 0) & (gap / 2 - np.abs(d) < MARGIN * gap)
    near |= rinf & (np.abs(np.where(fin, yd, 0.0)) - thresh < MARGIN * topgap)
    return near


def bits_of(a, fmt):
    return np.ascontiguousarray(a).view(fmt["u"])


def ordinal(a, fmt):
    """Map each non-NaN value to an integer so that adjacent floats differ by 1."""
    b = bits_of(a, fmt).astype(np.int64)
    mag = b & ((1 << (fmt["bits"] - 1)) - 1)
    return np.where(b >> (fmt["bits"] - 1), -mag, mag)


def same(a, b, fmt):
    """Bitwise equality, with any NaN equal to any NaN."""
    return (bits_of(a, fmt) == bits_of(b, fmt)) | (np.isnan(a) & np.isnan(b))


@np.errstate(all="ignore")
def reference(name, x, fmt):
    """Correctly rounded f(x) in the target type, for an array x of that type.
    Returns (ref, float64 reference A, statistics about the construction,
    indices of the hard inputs)."""
    t = fmt["t"]
    fid = NAMES.index(name)
    f = getattr(np, name)
    st = {}
    xd = x.astype(np.float64)
    ya = f(xd)
    yb = libm(fid, xd)
    ra = ya.astype(t)
    rb = yb.astype(t)
    nan_a, nan_b = np.isnan(ya), np.isnan(yb)
    st["ref_nan_disagree"] = int(np.count_nonzero(nan_a != nan_b))
    # disagreement between the two float64 references, in float64 ulps
    fin = np.isfinite(ya) & np.isfinite(yb) & (ya != yb)
    if fin.any():
        dd = np.abs(ya[fin] - yb[fin]) / np.spacing(np.abs(ya[fin]))
        st["ref_max_ulp64"] = float(dd.max())
    else:
        st["ref_max_ulp64"] = 0.0
    st["ref_inf_disagree"] = int(np.count_nonzero(np.isinf(ya) != np.isinf(yb)))
    hard = ~same(ra, rb, fmt) | near_boundary(ya, ra, fmt) | near_boundary(yb, rb, fmt)
    hard &= ~(nan_a & nan_b)
    hidx = np.flatnonzero(hard)
    ref = ra.copy()
    changed = 0
    for i in hidx:
        v = mp_exact(name, float(x[i]))
        if isinstance(v, mpmath.mpc) or mpmath.isnan(v):
            raise ArithmeticError(f"no real exact value for {name} at {float(x[i])!r}")
        c = t(mp_round(v, fmt, exact=is_exact(name, float(x[i]))))
        if bits_of(np.array([c]), fmt)[0] != bits_of(ref[i:i + 1], fmt)[0]:
            changed += 1
        ref[i] = c
    st["hard"] = int(hidx.size)
    st["hard_changed"] = changed
    return ref, ya, st, hidx


def chunk(args):
    name, dtype, start, n = args
    fmt = FMT[dtype]
    t, u = fmt["t"], fmt["u"]
    fid = NAMES.index(name)
    f = getattr(np, name)
    dneg, dpos = FUNCS[fid][1], FUNCS[fid][2]
    out = {"start": start, "n": n}
    with np.errstate(all="ignore"):
        bits = np.arange(start, start + n, dtype=np.uint64).astype(u)
        x = bits.view(t)
        y = f(x)                                   # the result under test
        assert y.dtype == t
        ref, ya, rstats, _ = reference(name, x, fmt)
        out.update(rstats)

        # --- comparison of y with the correctly rounded ref ---
        ynan, rnan = np.isnan(y), np.isnan(ref)
        out["n_nan_ref"] = int(np.count_nonzero(rnan))
        out["nan_mismatch"] = int(np.count_nonzero(ynan != rnan))
        both = ~ynan & ~rnan
        diff = both & (bits_of(y, fmt) != bits_of(ref, fmt))
        zs = diff & (y == 0) & (ref == 0)
        out["zero_sign_mismatch"] = int(np.count_nonzero(zs))
        infm = diff & (np.isinf(y) | np.isinf(ref))
        out["inf_mismatch"] = int(np.count_nonzero(infm))
        wrong = diff & ~zs
        out["misrounded"] = int(np.count_nonzero(wrong))
        out["n_valid"] = int(np.count_nonzero(both))
        # distance from the correctly rounded value in representable steps
        # (the measure NumPy's assert_array_max_ulp uses; inf counts as the
        # value after the largest finite one, +0 and -0 as the same point)
        steps = np.where(both, np.abs(ordinal(y, fmt) - ordinal(ref, fmt)), 0)
        out["steps_ge"] = [int(np.count_nonzero(steps >= k)) for k in (1, 2, 3, 4, 5)]
        out["max_steps"] = int(steps.max())
        ex = np.flatnonzero(zs | infm | (ynan != rnan))[:3]
        out["special_examples"] = [[int(bits[i]), int(bits_of(y, fmt)[i]), int(bits_of(ref, fmt)[i])] for i in ex]

        # error in ulps (ulp of the binade of the float64 reference value)
        ok = both & np.isfinite(y) & np.isfinite(ya)
        y64 = y.astype(np.float64)
        aa = np.abs(ya)
        _, e = np.frexp(aa)
        k = np.maximum(e - 1, fmt["emin"]) - fmt["p"]
        k = np.where(aa == 0, fmt["emin"] - fmt["p"], k)
        err = np.where(ok, np.abs(y64 - ya) / np.ldexp(1.0, k), 0.0)
        out["hist"] = [int(np.count_nonzero(err > th)) for th in (0.5, 1, 1.5, 2, 3, 4)]
        top = np.argsort(err)[-4:][::-1]
        out["top"] = [[int(bits[i]), float(err[i])] for i in top if err[i] > 0]
        out["sum_err"] = float(err.sum())
        out["n_err"] = int(np.count_nonzero(ok))

        # --- range ---
        if name in ("sin", "cos", "tanh"):
            out["abs_gt_1"] = int(np.count_nonzero(np.abs(y) > 1))

        # --- monotonicity in bit order, per sign half ---
        half = 1 << (fmt["bits"] - 1)
        direction = dpos if start < half else -dneg   # in increasing-bit order
        out["mono_dir"] = direction
        fy = y[~ynan]
        out["first"] = float(fy[0]) if fy.size else None
        out["last"] = float(fy[-1]) if fy.size else None
        if direction and fy.size > 1:
            dy = np.diff(fy.astype(np.float64)) * direction
            bad = dy < 0
            out["mono_viol"] = int(np.count_nonzero(bad))
            if bad.any():
                j = int(np.flatnonzero(bad)[0])
                xb = bits[~ynan]
                out["mono_example"] = [int(xb[j]), int(xb[j + 1])]
        else:
            out["mono_viol"] = 0

        # --- dependence on memory layout / loop length ---
        buf = np.zeros(2 * n, dtype=t)
        buf[::2] = x
        out["layout_stride2"] = int(np.count_nonzero(~same(f(buf[::2]), y, fmt)))
        out["layout_offset1"] = int(np.count_nonzero(~same(f(x[1:]), y[1:], fmt)))
        m3 = n // 3
        b3 = np.zeros((m3, 4), dtype=t)
        b3[:, :3] = x[:3 * m3].reshape(m3, 3)
        out["layout_len3"] = int(np.count_nonzero(~same(f(b3[:, :3]).ravel(), y[:3 * m3], fmt)))
        rev = f(x[::-1])[::-1]
        out["layout_reversed"] = int(np.count_nonzero(~same(rev, y, fmt)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("func", choices=NAMES)
    ap.add_argument("--dtype", default="float32", choices=list(FMT))
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--chunk-log2", type=int, default=22)
    ap.add_argument("--limit-chunks", type=int, default=0, help="debug: only the first N chunks")
    a = ap.parse_args()
    fmt = FMT[a.dtype]
    build_lib()
    total = 1 << fmt["bits"]
    n = min(1 << a.chunk_log2, total // 2)
    jobs = [(a.func, a.dtype, s, n) for s in range(0, total, n)]
    if a.limit_chunks:
        jobs = jobs[:a.limit_chunks]
    t0 = time.time()
    with Pool(a.workers) as pool:
        res = pool.map(chunk, jobs, chunksize=1)
    res.sort(key=lambda r: r["start"])

    S = lambda key: sum(r.get(key, 0) for r in res)
    agg = {
        "function": a.func, "dtype": a.dtype, "inputs": sum(r["n"] for r in res),
        "numpy": np.__version__, "mp_prec": MP_PREC, "margin": MARGIN,
    }
    for key in ("n_valid", "n_nan_ref", "misrounded", "nan_mismatch", "zero_sign_mismatch",
                "inf_mismatch", "hard", "hard_changed", "ref_nan_disagree", "ref_inf_disagree",
                "mono_viol", "layout_stride2", "layout_offset1", "layout_len3", "layout_reversed"):
        agg[key] = S(key)
    if any("abs_gt_1" in r for r in res):
        agg["abs_gt_1"] = S("abs_gt_1")
    agg["ref_max_ulp64"] = max(r["ref_max_ulp64"] for r in res)
    agg["hist_thresholds"] = [0.5, 1, 1.5, 2, 3, 4]
    agg["hist_err_gt"] = [sum(r["hist"][i] for r in res) for i in range(6)]
    agg["steps_ge_1_to_5"] = [sum(r["steps_ge"][i] for r in res) for i in range(5)]
    agg["max_steps"] = max(r["max_steps"] for r in res)
    agg["mean_err_ulp"] = S("sum_err") / max(S("n_err"), 1)
    # monotonicity across chunk boundaries: evaluate a 64-element window that
    # straddles each boundary inside one sign half
    half = total // 2
    cross_ex = []
    fn = getattr(np, a.func)
    for q in res[1:]:
        s0 = q["start"]
        dirn = q["mono_dir"]
        if s0 == half or not dirn:
            continue
        wb = np.arange(s0 - 32, s0 + 32, dtype=np.uint64).astype(fmt["u"])
        with np.errstate(all="ignore"):
            wy = fn(wb.view(fmt["t"])).astype(np.float64)
        if not (wy[31] == wy[31] and wy[32] == wy[32]):
            continue
        if (wy[32] < wy[31]) if dirn > 0 else (wy[32] > wy[31]):
            cross_ex.append([int(wb[31]), int(wb[32])])
    agg["mono_viol"] += len(cross_ex)
    agg["mono_checked"] = bool(FUNCS[NAMES.index(a.func)][1] or FUNCS[NAMES.index(a.func)][2])
    ex = (cross_ex + [r["mono_example"] for r in res if "mono_example" in r])[:8]
    agg["mono_examples_hex"] = [[f"{p:#x}", f"{q:#x}"] for p, q in ex]
    sp = [e for r in res for e in r["special_examples"]][:8]
    agg["special_examples_hex"] = [[f"{b:#x}" for b in e] for e in sp]
    # exact (mpmath) error of the worst inputs
    cand = sorted((t for r in res for t in r["top"]), key=lambda z: -z[1])[:8]
    worst = []
    f = getattr(np, a.func)
    for b, e64 in cand:
        x = np.array([b], dtype=fmt["u"]).view(fmt["t"])
        # evaluate inside a full-width array so the same vector path is used
        xs = np.full(64, x[0], dtype=fmt["t"])
        with np.errstate(all="ignore"):
            y = f(xs)[0]
        worst.append({"x_hex": f"{b:#x}", "x": float(x[0]), "y": float(y),
                      "err_ulp_float64ref": e64,
                      "err_ulp_mpmath": mp_ulp_err(a.func, float(x[0]), float(y), fmt),
                      "correct": mp_round(mp_exact(a.func, float(x[0])), fmt,
                                          exact=is_exact(a.func, float(x[0])))})
    agg["worst"] = worst
    agg["max_err_ulp"] = max((w["err_ulp_mpmath"] for w in worst), default=0.0)
    agg["seconds"] = round(time.time() - t0, 1)
    RESULTS.mkdir(exist_ok=True)
    suffix = "" if not a.limit_chunks else f".first{a.limit_chunks}"
    path = RESULTS / f"{a.dtype}_{a.func}{suffix}.json"
    path.write_text(json.dumps(agg, indent=1) + "\n")
    print(json.dumps({k: agg[k] for k in ("function", "dtype", "inputs", "misrounded", "max_err_ulp",
                                           "nan_mismatch", "zero_sign_mismatch", "inf_mismatch", "hard",
                                           "hard_changed", "ref_max_ulp64", "mono_viol", "layout_stride2",
                                           "layout_offset1", "layout_len3", "layout_reversed", "seconds")}))


if __name__ == "__main__":
    main()
