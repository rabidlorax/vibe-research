---
title: Exhaustive accuracy of NumPy float32 math functions over all 2^32 inputs
domain: computer-science
status: result
evidence: computed
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-24
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

NumPy's reference documentation gives no accuracy guarantee for these
functions. What exists is a 2021 mailing-list announcement ("up to 4 ULP in
the worst case" for some functions) and sampled tests with tolerances of 2 to
4 ULP (see Prior work). float32 is small enough to check completely, so those
figures can be replaced by the true worst case. People who rely on float32 results (reproducibility
across machines, rotations built from sin/cos, values that must stay inside
[-1, 1]) can then see exactly what they get.

## Summary of result

Scope of every statement below: the NumPy 2.5.3 wheel from PyPI
(`manylinux`, CPython 3.13) running on one Intel Xeon with AVX-512 (Sapphire
Rapids class; NumPy reports the `AVX512_SPR` dispatch level), Linux, glibc
2.39. Other CPUs select other code paths and are **not** covered. Details in
`results/environment.json`.

Items 1 to 4, 6 and 7 describe the result of the plain call `np.f(x)` on a
contiguous array. Item 5 shows that for 15 functions a negative-stride array
takes a different code path with different results; the accuracy and
monotonicity of that path were measured only on a sample.

All 2^32 float32 bit patterns were run through 21 unary functions and compared
with the correctly rounded result (round-to-nearest-even of the exact value).
Full tables: [`results/summary.md`](results/summary.md).

1. **Worst-case error.** No function reaches 3.91 ULP. The largest errors are
   `tan` 3.9000 (3.90005 to five decimals), `log` 3.832, `log10` 3.491, `arcsin` 3.120, `exp2` 2.843,
   `expm1` 2.620, `exp` 2.541, `cosh` 2.478. `sqrt` is correctly rounded for
   every input. This is inside the "up to 4 ULP" of the 2021
   announcement and replaces it with exact per-function figures for this
   build.
2. **How often the result is not the correctly rounded one.** Leaving
   out `sqrt` (never), it varies by a factor of about 600. As a share of the
   inputs whose result is not NaN: `arcsinh` 0.09 %, `log2` 0.49 %, `exp`
   4.9 %, `tan` 13.2 %, `cbrt` 35.5 %, `log10` 55.1 %.
3. **Monotonicity is violated** by 10 of the 18 functions checked. Counting
   adjacent float32 inputs whose results go the wrong way: `cosh` 39,658,
   `exp` 19,245, `log` 2,873, `cbrt` 1,184, `expm1` 94, `log10` 76, `arcsin`
   58, `arccos` 40, `arctan` 8, `tanh` 2. Example:
   `np.exp(np.float32(0.0024074981920421124))` is `1.0024104`, but for the next
   float32 up, `0.002407498424872756`, it is `1.0024103`.
4. **`exp2` exceeds the tolerance of NumPy's own accuracy test.** That test
   (`assert_array_max_ulp`) counts representable values between the result
   and the correctly rounded one, and the test data shipped in the wheel allow
   2 for float32 `exp2`. For 476 inputs the result is 3 values away, for
   example at `x = 126.56739807128906` (2.843 ULP from the exact value). The
   shipped test passes because none of the 476 is among its 714 samples.
   Every other function stays inside its shipped tolerance on every input.
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
7. **float16.** On this build every float16 function, called on a contiguous
   array, is within 0.5003 ULP for all 65,536 inputs, with at most 8 inputs
   per function not correctly rounded. That is consistent with the
   low-precision AVX512-FP16 path reported in numpy/numpy issue 30821 no
   longer being used in 2.5.3. Results for 11 functions still depend on
   stride for a handful of inputs (at most 20).

Evidence label for all of the above: `computed`.

## Claims

"Exhaustive" means all 2^32 float32 (or all 2^16 float16) bit patterns. ULP is
measured against the exact value, in units of the spacing of the target format
in the binade of the exact value (subnormal spacing below the smallest normal).
"Steps" is the number of representable values between the result and the
correctly rounded value. Claims 1 to 4, 7 and 8 are about the plain call on a
contiguous array.

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | For the stated build and CPU, the worst-case error of each float32 function over all inputs is the value in the "max error" column of `results/summary.md` (largest: `tan` 3.9000 ULP at `0x67997c79`) | computed | `python src/sweep.py <func>` for each function, then `python src/report.py`; compare `max_err_ulp` and `worst` in `results/float32_<func>.json` |
| 2 | The number of float32 inputs whose result is not correctly rounded is the "not correctly rounded" column (smallest nonzero: `arccosh` 3,212,890; largest: `cbrt` 1,518,074,730); `sqrt` has none | computed | same; field `misrounded` |
| 3 | Adjacent-input monotonicity violations per function are as in the "monotonicity violations" column; 10 of 18 checked functions have at least one, 8 have none (`exp2`, `log2`, `log1p`, `sinh`, `arcsinh`, `arccosh`, `arctanh`, `sqrt`) | computed | same; fields `mono_viol`, `mono_examples_hex`. One-line check of the example in the summary: `python -c "import numpy as np; print(np.exp(np.array([0.0024074981920421124, 0.002407498424872756], dtype=np.float32)))"` |
| 4 | float32 `exp2` is 3 steps from the correctly rounded value for 476 inputs (for example `0x42fd2282`) and never more, which is outside the tolerance of 2 in the wheel's `umath-validation-set-exp2.csv`; 10,694 inputs have error above 2 ULP from the exact value. For every other function with an entry in the wheel's test data, no input is beyond the tolerance | computed | `results/float32_<func>.json` (`steps_ge_1_to_5`, `max_steps`, `hist_err_gt`, `worst`); columns "max steps", "tolerance" and "inputs beyond that tolerance" of `results/summary.md`, the tolerance being read from the installed wheel by `src/report.py` |
| 5 | Exhaustively: reversing the input (`x[::-1]`) changes the result bits for 15 functions (counts in the "reversed" column), and never for `exp`, `log`, `sin`, `cos`, `tanh`, `sqrt`. Exhaustively: input stride 2, start offset 1, and inner loops of length 3 never change the bits for any float32 function | computed | fields `layout_reversed`, `layout_stride2`, `layout_offset1`, `layout_len3` |
| 6 | On a fixed-seed sample of 2^22 inputs: input strides -1 and -2 and a reversed output array give the same set of differing inputs; input stride 3, output stride 2, and inner loops of length 1, 2, 7, 15, 16, 17 give no differences. On the first 2^15 of those: scalar calls equal the array result, and the negative-stride result equals glibc's scalar float function, for all 15 affected functions | computed (sample, not exhaustive) | `python src/layout_probe.py`; `results/layout_probe.json` |
| 7 | Exhaustively, for all 21 float32 functions: no NaN-ness mismatch, no zero-sign mismatch, no infinity mismatch against the reference; `sin`, `cos`, `tanh` never exceed 1 in magnitude | computed | fields `nan_mismatch`, `zero_sign_mismatch`, `inf_mismatch`, `abs_gt_1` |
| 8 | For all 65,536 float16 inputs, each of the 21 functions, on a contiguous array, has maximum error at most 0.5003 ULP and at most 8 inputs not correctly rounded; 11 functions give different bits for 1 to 20 inputs when the input has stride 2 or is reversed (the accuracy of those other results was not measured) | computed | `python src/sweep.py <func> --dtype float16`; `results/float16_<func>.json` |
| 9 | The reference used in claims 1 to 8 agrees bit for bit, including the sign of zero and NaN-ness, with MPFR rounding directly to the target format, on: 2,000,012 sampled float32 inputs per function (579,846 to 1,996,113 of them with a non-NaN result, depending on the function's domain), a further 314 to 2,095 hard inputs per function (26,662 in total) taken from 16 blocks of 2^22 consecutive inputs, and all 65,536 float16 inputs per function. 0 disagreements in 21 + 21 runs | computed | `python src/validate.py`; `results/validate.json` (fields `compared_non_nan`, `both_nan`, `hard_inputs_compared`, `disagree`) |

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
tested by `src/validate.py` (claim 9), whose oracle is MPFR called through
gmpy2 with precision 24, the binary32 exponent range and subnormalisation, so
that MPFR itself returns the correctly rounded float32. That oracle shares no
code with the reference: no float64 step, no margin test, no mpmath and no
`mp_round`.

**Comparison.** Bitwise equality with the reference, any NaN equal to any NaN.
Mismatches are split into NaN-ness, sign of zero, infinity, and ordinary
misrounding. The error in ULP is computed per input from A (accurate to about
1e-9 ULP of float32); the eight largest per function are recomputed with
mpmath and the maximum of those is reported. The "> 1 ULP" style counts use
the A-based error. Separately, the distance in steps between the result and
the reference is counted exactly from the bit patterns (an infinity counts as
the value after the largest finite one, and the two zeros as one point).

**Monotonicity.** Within each sign half, consecutive bit patterns are
consecutive floats. For each function known to be monotone on that half, a
violation is a pair of adjacent inputs (NaN results skipped) whose results
move the wrong way. Pairs that straddle a chunk boundary are evaluated in a
64-element window. The pair (-0, +0) joining the two halves is not checked. `sin`, `cos`, `tan` are not checked; `log`, `log2`,
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
(`cbrt` of a negative) and failed on infinite values; an early version of
`validate.py` caught both before the `cbrt` sweep ran, and they were fixed.
The first `exp2` sweep aborted on the exact tie at -150, which led to the tie
handling above. After those fixes every sweep was run again. A review inside
the authoring session (not the independent review this repository requires)
then asked for the step counts and for an oracle independent of `mp_round`;
both were added and everything was run a third time. The committed files are
from the third run. The second run is in the history at commit `d9e01a4`:
the sweep files there differ from the current ones only in the run time and
in the added fields `steps_ge_1_to_5` and `max_steps`, and
`layout_probe.json` is unchanged, so the numbers were reproduced exactly. The
first run is not in the repository; it gave the same numbers, which a reader
cannot check. The machine was restarted during the second run, so
`results/environment.json` was written after the restart; only the kernel
build string changed.

## Reproduction

Requires Linux x86-64, `gcc`, Python 3.13, and a CPU with AVX-512 to reach the
same code paths. No network access after installing the packages.

```bash
cd domains/computer-science/projects/numpy-float32-exhaustive-accuracy
pip install -r src/requirements.txt     # numpy==2.5.3 mpmath==1.3.0 gmpy2==2.2.1
sh src/run_all.sh                       # everything in results/
```

`run_all.sh` records the environment, runs `validate.py` (a few minutes),
the 21 float16 sweeps (seconds), the 21 float32 sweeps, `layout_probe.py`
(a few minutes) and `report.py`. The float32 sweeps took 103 minutes in
total on 4 cores and 15 GB of memory, between 4.4 and 6.4 minutes per
function. A single function is `python src/sweep.py tanh`.

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
(logged-out view, 2026-11-23). Three further web searches with other terms
on 2026-11-24, done by the in-session reviewer, also found no report of the
monotonicity, stride or `exp2` findings. Alternative names covered: ULP error, correct
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
  Its figures for five functions agree with ours when ours are rounded up to
  two decimals, as an upper bound from interval arithmetic would be: exp 2.55
  (here 2.541), log 3.84 (3.832), sin 1.49 (1.486), cos 1.49 (1.488), tanh
  1.38 (1.374). Other functions differ a
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
  ULP." (This message, the issue and the pull request below were retrieved
  through a page-fetching subagent of this session, which returned the quoted
  text.) The NumPy 2.5 reference pages for `numpy.tanh` and for ufunc basics
  give no accuracy guarantee. NumPy's test-suite checks sampled inputs against
  per-function tolerances of 2 to 4 ULP (data files in the wheel). The same
  test-suite (`numpy/_core/tests/test_umath.py` in the wheel) deliberately
  runs some functions on "Oddly strided arrays which may not be SIMD
  compatible", including stride -1, so NumPy's developers know that the
  stride selects the loop. What was not found is a statement of how many
  results change, or by how much.
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
  `sin`, `cos`, `sqrt` on glibc alone. The MPFR check (claim 9) covers about
  two million sampled inputs per function, roughly one in 2,000, plus a
  sample of the hard inputs. A proof would need a check of all inputs, by
  interval enclosures as Ozaki does or against MPFR or CORE-MATH. That was
  not done, for reasons of run time: at the speed of the Python loop in
  `validate.py` it would need several CPU-hours per function.
- **mpmath is trusted** for the hard cases and for the reported worst-case
  errors, at 1200 bits, with the gmpy2 backend. MPFR (through gmpy2) is
  trusted as the oracle in claim 9.
- **The tie argument is informal.** Apart from `exp2` at integers, we rely on
  the code raising an error if any value sits within 2^-300 of a midpoint. No
  error was raised, so no such case occurred among hard inputs.
- **Monotonicity counts adjacent pairs only.** A function with zero adjacent
  violations is monotone on each sign half, among non-NaN results. The count
  does not measure how large the reversals are.
- **The negative-stride path is not characterised exhaustively.** Its
  worst-case error, misrounding counts and monotonicity were not measured.
  Findings 1 to 4 do not carry over to it: for example the reversed call
  returns the correctly rounded `exp2` at `0x42fd2282`.
- **Layouts not tried:** unaligned buffers, in-place output (`out=x`),
  byte-swapped input, and float64 input cast to the float32 loop.
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
