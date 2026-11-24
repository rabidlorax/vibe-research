#!/bin/sh
# Regenerate every file in results/.  About 100 minutes on 4 cores for float32.
set -e
cd "$(dirname "$0")"
FUNCS="exp exp2 expm1 log log2 log10 log1p sin cos tan arcsin arccos arctan sinh cosh tanh arcsinh arccosh arctanh cbrt sqrt"
python environment.py
python validate.py
for f in $FUNCS; do python sweep.py "$f" --dtype float16; done
for f in $FUNCS; do python sweep.py "$f"; done
python layout_probe.py
python exp2_tolerance.py
python report.py
