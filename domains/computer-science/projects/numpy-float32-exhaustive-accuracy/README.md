---
title: Exhaustive accuracy of NumPy float32 math functions over all 2^32 inputs
domain: computer-science
status: active
evidence: computed
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Exhaustive accuracy of NumPy float32 math functions over all 2^32 inputs

## Question

For each unary float32 math function that NumPy computes with its own SIMD
code or with its bundled copy of Intel SVML (exp, log, sin, cos, tan, the
inverse and hyperbolic functions, and relatives), what is the exact worst-case
error in ULPs, and the exact number of inputs that are not correctly rounded,
taken over **every one of the 2^32 float32 bit patterns**, for a stated NumPy
build on a stated CPU? Secondary: are the results free of monotonicity
violations and out-of-range values, and do they depend on where an element
sits in the array?

An answer is a table per function (worst error, worst input, count of
misrounded inputs) that anyone can regenerate with one command, with the
reference values proved correct by a rounding test rather than assumed.

## Why it matters

NumPy's documentation and the pull requests that added these loops state
error bounds ("up to 4 ULP") that come from the vendor or from sampled tests.
float32 is small enough to check completely, so the bound can be replaced by
the true worst case. People who rely on float32 results (reproducibility
across machines, rotations built from sin/cos, values that must stay inside
[-1, 1]) can then see exactly what they get.

## Summary of result

Scope of every statement below: the NumPy 2.5.3 wheel from PyPI
(`manylinux`, CPython 3.13) running on one Intel Xeon with AVX-512 (Sapphire
Rapids class; NumPy reports the `AVX512_SPR` dispatch level), Linux, glibc
2.39. Other CPUs select other code paths and are **not** covered. Details in
`results/environment.json`.

All 2^32 float32 bit patterns were run through 21 unary functions and compared
with the correctly rounded result (round-to-nearest-even of the exact value).
Full tables: [`results/summary.md`](results/summary.md).

1. **Worst-case error.** No function exceeds 3.90 ULP. The largest errors are
   `tan` 3.900, `log` 3.832, `log10` 3.491, `arcsin` 3.120, `exp2` 2.843,
   `expm1` 2.620, `exp` 2.541, `cosh` 2.478. `sqrt` is correctly rounded for
   every input. This agrees with NumPy's stated "up to 4 ULP" and replaces it
   with exact per-function figures for this build.
2. **How often the result is not the correctly rounded one.** It varies by
   three orders of magnitude: `arcsinh` 0.09 % of non-NaN inputs, `log2`
   0.49 %, `exp` 4.9 %, `tan` 13.3 %, `cbrt` 35.5 %, `log10` 55.1 %.
3. **Monotonicity is violated** by 10 of the 18 functions checked. Counting
   adjacent float32 inputs whose results go the wrong way: `cosh` 39,658,
   `exp` 19,245, `log` 2,873, `cbrt` 1,184, `expm1` 94, `log10` 76, `arcsin`
   58, `arccos` 40, `arctan` 8, `tanh` 2. Example:
   `np.exp(np.float32(0.0024074981920421124))` is `1.0024104`, but for the next
   float32 up, `0.002407498424872756`, it is `1.0024103`.
4. **`exp2` exceeds the tolerance of NumPy's own accuracy test.** The test data
   shipped in the wheel allow 2 ULP for float32 `exp2`; at `x = 126.56739807128906`
   the result is 3 representable values away from the correctly rounded one
   (2.843 ULP from the exact value). 10,694 inputs have error above 2 ULP.
   The shipped test passes because those inputs are not among its 714 samples.
   Every other function stays inside its shipped tolerance.
5. **A negative stride changes the bits.** For 15 of the 21 functions,
   `np.f(x[::-1])[::-1]` differs from `np.f(x)`: for example 1,169,154,177
   inputs for `log10` and 1,574,686,740 for `cbrt`. Positive strides, an
   offset start, rows of 3, short arrays and NumPy scalars all gave the same
   bits as the contiguous call (items exhaustive or sampled as stated in the
   claims table). On a sample, the negative-stride results were bit-identical
   to glibc's scalar float functions (`log10f`, ...), which are usually, but
   not always, more accurate than the vector path.
6. **Special values.** No function returned NaN where the reference is not
   NaN or the reverse, a zero of the wrong sign, or a wrong infinity/overflow
   decision. `sin`, `cos` and `tanh` never leave [-1, 1].
7. **float16.** On this build every float16 function is within 0.5003 ULP for
   all 65,536 inputs, with at most 8 inputs per function not correctly
   rounded. The low-precision AVX512-FP16 path reported in numpy/numpy issue
   30821 is not active in 2.5.3. Results for 11 functions still depend on
   stride for a handful of inputs (at most 20).

Evidence label for all of the above: `computed`.

## Claims

"Exhaustive" means all 2^32 float32 (or all 2^16 float16) bit patterns. ULP is
measured against the exact value, in units of the spacing of the target format
in the binade of the exact value (subnormal spacing below the smallest normal).

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | For the stated build and CPU, the worst-case error of each float32 function over all inputs is the value in the "max error" column of `results/summary.md` (largest: `tan` 3.9000 ULP at `0x67997c79`) | computed | `python src/sweep.py <func>` for each function, then `python src/report.py`; compare `max_err_ulp` and `worst` in `results/float32_<func>.json` |
| 2 | The number of float32 inputs whose result is not correctly rounded is the "not correctly rounded" column (smallest nonzero: `arccosh` 3,212,890; largest: `cbrt` 1,518,074,730); `sqrt` has none | computed | same; field `misrounded` |
| 3 | Adjacent-input monotonicity violations per function are as in the "monotonicity violations" column; 10 of 18 checked functions have at least one, 8 have none (`exp2`, `log2`, `log1p`, `sinh`, `arcsinh`, `arccosh`, `arctanh`, `sqrt`) | computed | same; fields `mono_viol`, `mono_examples_hex`. One-line check of the example in the summary: `python -c "import numpy as np; print(np.exp(np.array([0.0024074981920421124, 0.002407498424872756], dtype=np.float32)))"` |
| 4 | float32 `exp2` has 10,694 inputs with error above 2 ULP, and at `0x42fd2282` is 3 float32 steps from the correctly rounded value, which is outside the 2 ULP tolerance in the wheel's `umath-validation-set-exp2.csv`; every other function's worst case is inside its shipped tolerance | computed | `results/float32_exp2.json` (`hist_err_gt`, `worst`); tolerance column of `results/summary.md` is read from the installed wheel by `src/report.py` |
| 5 | Exhaustively: reversing the input (`x[::-1]`) changes the result bits for 15 functions (counts in the "reversed" column), and never for `exp`, `log`, `sin`, `cos`, `tanh`, `sqrt`. Exhaustively: input stride 2, start offset 1, and inner loops of length 3 never change the bits for any float32 function | computed | fields `layout_reversed`, `layout_stride2`, `layout_offset1`, `layout_len3` |
| 6 | On a fixed-seed sample of 2^22 inputs: input strides -1 and -2 and a reversed output array give the same set of differing inputs; input stride 3, output stride 2, and inner loops of length 1, 2, 7, 15, 16, 17 give no differences. On the first 2^15 of those: scalar calls equal the array result, and the negative-stride result equals glibc's scalar float function, for all 15 affected functions | computed (sample, not exhaustive) | `python src/layout_probe.py`; `results/layout_probe.json` |
| 7 | Exhaustively, for all 21 float32 functions: no NaN-ness mismatch, no zero-sign mismatch, no infinity mismatch against the reference; `sin`, `cos`, `tanh` never exceed 1 in magnitude | computed | fields `nan_mismatch`, `zero_sign_mismatch`, `inf_mismatch`, `abs_gt_1` |
| 8 | For all 65,536 float16 inputs, each of the 21 functions has maximum error at most 0.5003 ULP and at most 8 inputs not correctly rounded; 11 functions give different bits for 1 to 20 inputs when the input has stride 2 or is reversed | computed | `python src/sweep.py <func> --dtype float16`; `results/float16_<func>.json` |
| 9 | The reference used in claims 1 to 8 equals a rounding done by mpmath alone (1200 bits, no float64 step) on every one of 40,012 sampled float32 inputs per function and on all 65,536 float16 inputs per function, excluding inputs whose reference is NaN and infinite inputs: 0 disagreements in 21 + 21 runs | computed | `python src/validate.py`; `results/validate.json` |

Claims 1 to 8 for float32 rest on the reference being right for the inputs not
covered by claim 9. That is an assumption, stated under Method and
Limitations. For float16 the reference is checked on every finite input.

## Method

Code is in `src/`. Nothing is downloaded at run time.

**Inputs.** Every bit pattern `0 .. 2^32-1`, viewed as float32, in chunks of
2^22 consecutive patterns. NaN inputs are included (16,777,214 of them); the
functions must return NaN there.

**Result under test.** `np.<func>(x)` on the contiguous float32 chunk, inside
`np.errstate(all="ignore")`.

**Reference (`sweep.reference`).** The correctly rounded value is built in
three steps.

1. Two float64 values are computed for each input: A, the same NumPy ufunc on
   `x.astype(float64)`; and B, the C library's double function called from
   `src/ref_libm.c` (glibc 2.39). For `sin`, `cos` and `sqrt`, A and B were
   bit-identical on every input, so they are one reference there, not two.
   Elsewhere they differ by at most 3 float64 ULP over all inputs
   (`ref_max_ulp64` in the results).
2. An input is *hard* if A and B round to different float32 values, or if
   either is within 2^-16 of the local float32 spacing from a rounding
   boundary (a midpoint between adjacent float32 values, or the overflow
   threshold 2^128 - 2^103). The spacing is 2^29 float64 ULP, so the margin is
   about 8192 float64 ULP. A float64 value that is exactly a float32 value is
   not hard: it is far from every boundary.
3. Each hard input is recomputed with mpmath at 1200 bits and rounded with
   integer arithmetic (`mp_round`). The code raises an error if the value is
   within 2^-300 of a boundary, so a tie cannot be silently guessed. The one
   family of exact ties, `exp2(k)` for integer `k` (`exp2(-150) = 2^-150` is
   exactly half the smallest subnormal), is computed exactly by mpmath and
   broken to even. Between 6,052 and 131,272 inputs per function were hard;
   in 37 cases in total the mpmath rounding differed from the rounding of A.

   All other inputs take the rounding of A to float32.

The reference is therefore wrong at an input only if both float64 libraries
are off by more than about 8192 ULP there, in a way that leaves them agreeing
(or, for `sin`/`cos`/`sqrt`, if glibc alone is). That is not proved. It is
tested by `src/validate.py` (claim 9).

**Comparison.** Bitwise equality with the reference, any NaN equal to any NaN.
Mismatches are split into NaN-ness, sign of zero, infinity, and ordinary
misrounding. The error in ULP is computed per input from A (accurate to about
1e-9 ULP of float32); the eight largest per function are recomputed with
mpmath and the maximum of those is reported. The "> 1 ULP" style counts use
the A-based error.

**Monotonicity.** Within each sign half, consecutive bit patterns are
consecutive floats. For each function known to be monotone on that half, a
violation is a pair of adjacent inputs (NaN results skipped) whose results
move the wrong way. Pairs that straddle a chunk boundary are evaluated in a
64-element window. `sin`, `cos`, `tan` are not checked; `log`, `log2`,
`log10`, `arccosh`, `sqrt` are checked for positive inputs only.

**Layout.** Each chunk is evaluated again as: every second element of a
double-length buffer; starting from element 1; the first three columns of an
`(n/3, 4)` array, so each inner loop has length 3; and reversed. Each is
compared bitwise with the contiguous result. `src/layout_probe.py` tries more
layouts on a sample and compares the negative-stride result with glibc's
float functions through `ctypes`.

**float16.** The same code with `--dtype float16`.

**What was tried and changed along the way.** The first version of the
exact-rounding code skipped hard cases where mpmath returned a complex number
(`cbrt` of a negative) and failed on infinite values; `validate.py` caught
both before the `cbrt` sweep ran, and they were fixed. The first `exp2` sweep
aborted on the exact tie at -150, which led to the tie handling above. `exp`,
`exp2` and `tanh` were rerun with the final code; `sin` was not, because none
of the fixes can affect it (see Limitations). The `seconds` field for `sin`
(708) is inflated because two sweeps were running at once.

## Reproduction

Requires Linux x86-64, `gcc`, Python 3.13, and a CPU with AVX-512 to reach the
same code paths. No network access after installing the packages.

```bash
cd domains/computer-science/projects/numpy-float32-exhaustive-accuracy
pip install -r src/requirements.txt     # numpy==2.5.3 mpmath==1.3.0 gmpy2==2.2.1
sh src/run_all.sh                       # everything in results/
```

`run_all.sh` records the environment, runs `validate.py` (about 4 minutes),
the 21 float16 sweeps (seconds), the 21 float32 sweeps, `layout_probe.py`
(about 3 minutes) and `report.py`. The float32 sweeps took 103 minutes in
total on 4 cores and 15 GB of memory, about 4 to 6 minutes per function; peak
memory was about 2 GB. A single function is `python src/sweep.py tanh`.

No random numbers are used by `sweep.py`. `validate.py` and
`layout_probe.py` use `numpy.random.default_rng(20261123)`.

On a CPU without AVX-512, or with another NumPy version or build, the script
runs but measures different code, and the numbers will differ.

## External data and what we could not reproduce

None. The project uses no external dataset. The software under test (NumPy)
and the tools (glibc, mpmath, gmpy2) are installed from the standard
registries; nothing from them is committed here. The tolerance column in
`results/summary.md` is read at run time from the test data inside the
installed NumPy wheel (`numpy/_core/tests/data/umath-validation-set-*.csv`).

Published figures quoted under "Prior work" are `literature` and are not
relied on by any claim.

## Prior work and novelty

Searched on 2026-11-23, before the sweeps were run, with the web search tool
and by fetching the pages named.

Search terms used: "exhaustive test all float32 inputs numpy ufunc accuracy
ULP"; "Accuracy of Mathematical Functions in Single, Double, Double Extended,
and Quadruple Precision numpy"; "numpy float32 not monotonic / different
results array length position SIMD"; "numpy pull request AVX512 float32 max
ULP error"; "numpy issue float32 non-monotonic tanh arcsin cos SVML";
"numpy float16 AVX512_SPR SVML contiguous vs strided"; "numpy ufunc result
depends on stride contiguity float32"; "numpy test_umath_accuracy
umath-validation-set tolerance". GitHub issue searches on numpy/numpy for
`tanh float32 monotonic` and `float32 ulp exhaustive` returned no issues
(logged-out view, 2026-11-23). Alternative names covered: ULP error, correct
rounding, accuracy of elementary/transcendental functions, SVML, universal
intrinsics, strided/non-contiguous.

What was found:

- **K. Ozaki, "Accuracy of Low-Precision Elementary and Special Functions
  Using Verified Numerical Computations", J. Adv. Simulat. Sci. Eng. 12(1),
  113-130 (2025), doi:10.15748/jasse.12.113.** Read in full (PDF from
  J-STAGE). This is the closest prior work. It tests all FP32 inputs of 16
  NumPy functions against interval enclosures from INTLAB and reports the
  maximum ULP per function in its Table 14, for "NumPy (version 1.21.0) in
  Python 3.11" on "a laptop running Windows 11 with an Intel Core i7-12650H
  processor". It concludes "The ulp is less than four for all functions."
  Its figures for functions whose implementation has apparently not changed
  agree with ours to rounding: exp 2.55 (here 2.541), log 3.84 (3.832), sin
  1.49 (1.486), cos 1.49 (1.488), tanh 1.38 (1.374). Other functions differ a
  lot (tan 0.51 there, 3.900 here; cosh 0.51 there, 2.478 here), as expected
  from a different NumPy version, operating system and CPU. The paper uses
  Harrison's definition of ULP, which differs from ours only when the exact
  value is close to a power of two. It reports maxima only: no counts of
  misrounded inputs, nothing on monotonicity, nothing on layout, and no FP16
  results for NumPy.
- **B. Gladman, V. Innocente, J. Mather, K. Ozaki, P. Zimmermann, "Accuracy of
  Mathematical Functions in Single, Double, Double Extended, and Quadruple
  Precision", version dated August 2026**
  (<https://homepages.loria.fr/PZimmermann/papers/accuracy.pdf>; first three
  pages and reference list read). Exhaustive binary32 tests of C math
  libraries (glibc, Intel, AMD, LLVM and others). NumPy is not among the
  libraries tested; the paper points to Ozaki's for NumPy.
- **NumPy's own statements.** M. Picus, numpy-discussion, 2021-10-11, on
  merging SVML: "The accuracy is now defined as up to 4 ULP in the worst case
  for tan, cos, sin, asin, atan, expm1, but typically the error is up to 2
  ULP." The NumPy 2.5 reference pages for `numpy.tanh` and for ufunc basics
  give no accuracy guarantee. NumPy's test-suite checks sampled inputs against
  per-function tolerances of 2 to 4 ULP (data files in the wheel).
- **float16.** numpy/numpy issue 30821 (opened 2026-02-11) reported
  `np.tanh` on float16 arrays being 3 ULP off on Sapphire Rapids; pull
  request 31178 ("REV: Manual revert of float16 svml use", merged 2026-04-07)
  closed it. Our float16 result (claim 8) is consistent with that revert being
  in 2.5.3. The replies in the related mailing-list thread ("Should we revert
  float16 loops", S. Berg, 2026-03-10) were not read.

Not found in this search: an exhaustive float32 measurement of a NumPy
release that uses the SVML/AVX-512 paths; counts of non-monotone input pairs
for NumPy float32 functions; a report that a negative stride changes float32
results; a report that `exp2` exceeds its test tolerance.

Conclusion: `partially-known`. The worst-case table is a replication, on a
newer NumPy and an AVX-512 CPU, of a kind of measurement Ozaki already
published. Claims 2 to 8 were not found in the search described.

## Limitations and open questions

- **One build, one CPU.** NumPy chooses loops at run time from the CPU's
  features. Nothing here says what an AVX2-only x86 machine, an ARM machine,
  macOS or Windows returns, or what another NumPy version returns.
- **The float32 reference is not proved correct.** Inputs not sent to mpmath
  rely on both float64 libraries being accurate to about 8192 ULP, and for
  `sin`, `cos`, `sqrt` on glibc alone. The sample check (claim 9) covers
  40,012 inputs per function, about one in 100,000. A proof would need
  interval enclosures for all inputs, as Ozaki does, or a comparison with a
  library proved correctly rounded such as CORE-MATH. Neither was done.
- **mpmath is trusted** for the hard cases and for the reported worst-case
  errors, at 1200 bits, with the gmpy2 backend.
- **The tie argument is informal.** Apart from `exp2` at integers, we rely on
  the code raising an error if any value sits within 2^-300 of a midpoint. No
  error was raised, so no such case occurred among hard inputs.
- **`sin` was not rerun after the last code changes.** The changes concern
  complex or infinite exact values, the exact `exp2` tie, the overflow test in
  `mp_round`, and the recording of examples for monotonicity, none of which
  `sin` reaches. A reviewer who wants strict uniformity should rerun it.
- **Monotonicity counts adjacent pairs only.** A function with zero adjacent
  violations is monotone on each sign half, among non-NaN results. The count
  does not measure how large the reversals are.
- **Layout claims beyond the four exhaustive layouts are sampled** (claim 6).
  The cause of the negative-stride difference was not traced in NumPy's source;
  "falls back to glibc's float function" is an inference from bit-identical
  results on 32,768 inputs per function.
- **The "> k ULP" counts** use the float64 reference A and so could be off by
  a few inputs whose error is within about 1e-9 ULP of a threshold.
- **Not reported upstream.** The `exp2` tolerance, the monotonicity
  violations and the negative-stride difference have not been raised with
  NumPy. Doing so needs the person running the session.
- Open: the same sweep on an AVX2-only machine and on ARM; float64 cannot be
  swept, but the float32 worst inputs are natural seeds for a float64 search.

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
