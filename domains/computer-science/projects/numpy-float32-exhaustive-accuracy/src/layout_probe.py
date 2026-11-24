#!/usr/bin/env python3
"""Which array layouts change the bits of a float32 result, and how accurate is each path?

A fixed-seed sample of 2**22 bit patterns (not exhaustive).  For each function
the result of the plain contiguous call is compared with the same inputs
presented as: several strided / reversed views, a strided output, short arrays,
and NumPy scalars.  Each distinct path is also compared with the correctly
rounded reference from sweep.reference() and with the C library's float
function (expf, sinf, ...), to identify the fallback.

Usage: python layout_probe.py
"""
import ctypes
import ctypes.util
import json

import numpy as np

import sweep

N = 1 << 22
NSCALAR = 1 << 15
fmt = sweep.FMT["float32"]
rng = np.random.default_rng(20261123)
bits = rng.integers(0, 1 << 32, size=N, dtype=np.uint64).astype(np.uint32)
x = bits.view(np.float32).copy()
libm = ctypes.CDLL(ctypes.util.find_library("m"))
CNAME = {"arcsin": "asin", "arccos": "acos", "arctan": "atan", "arcsinh": "asinh",
         "arccosh": "acosh", "arctanh": "atanh"}


def cfloat(name, xs):
    fn = getattr(libm, CNAME.get(name, name) + "f")
    fn.argtypes = [ctypes.c_float]
    fn.restype = ctypes.c_float
    return np.array([fn(float(v)) for v in xs], dtype=np.float32)


def ndiff(a, b):
    return int(np.count_nonzero(~sweep.same(a, b, fmt)))


out = {}
with np.errstate(all="ignore"):
    for name in sweep.NAMES:
        f = getattr(np, name)
        y = f(x)
        ref, _, _, _ = sweep.reference(name, x, fmt)
        r = {"sample": N}
        # views of a buffer that place x at the given stride
        def strided(step):
            buf = np.zeros(N * abs(step), dtype=np.float32)
            v = buf[::abs(step)]
            v[:] = x if step > 0 else x[::-1]
            view = v if step > 0 else buf[::abs(step)][::-1]
            res = f(view)
            return res
        res = {step: strided(step) for step in (2, 3, -1, -2)}
        for step in (2, 3, -1, -2):
            r[f"in_stride_{step}"] = ndiff(res[step], y)
        ob = np.zeros(2 * N, dtype=np.float32)
        f(x, out=ob[::2])
        r["out_stride_2"] = ndiff(ob[::2], y)
        ob = np.zeros(N, dtype=np.float32)
        f(x, out=ob[::-1])
        r["out_reversed"] = ndiff(ob[::-1], y)
        # do the three negative-stride layouts return the same bits as each other?
        r["negative_layouts_mutually_identical"] = bool(
            ndiff(res[-1], res[-2]) == 0 and ndiff(res[-1], ob[::-1]) == 0)
        # (a row length of 1 would be merged into one strided loop, so it is
        # not listed; length-1 loops are covered by the scalar calls below)
        for L in (2, 7, 15, 16, 17):
            m = N // L
            b = np.zeros((m, L + 1), dtype=np.float32)
            b[:, :L] = x[:m * L].reshape(m, L)
            r[f"rows_of_{L}"] = ndiff(f(b[:, :L]).ravel(), y[:m * L])
        xs = x[:NSCALAR]
        ys = np.array([f(v) for v in xs], dtype=np.float32)        # NumPy scalar calls
        r["scalar_calls"] = NSCALAR
        r["scalar_vs_array"] = ndiff(ys, y[:NSCALAR])
        yrev = f(x[::-1])[::-1]
        yc = cfloat(name, xs)
        r["reversed_vs_libm_float"] = ndiff(yrev[:NSCALAR], yc)
        r["contiguous_vs_libm_float"] = ndiff(y[:NSCALAR], yc)
        valid = ~np.isnan(ref)
        r["contiguous_misrounded"] = ndiff(y[valid], ref[valid])
        r["reversed_misrounded"] = ndiff(yrev[valid], ref[valid])
        r["libm_float_misrounded_in_scalar_subset"] = ndiff(yc[valid[:NSCALAR]], ref[:NSCALAR][valid[:NSCALAR]])
        out[name] = r
        print(name, r, flush=True)
(sweep.RESULTS / "layout_probe.json").write_text(json.dumps(out, indent=1) + "\n")
