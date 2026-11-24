#!/usr/bin/env python3
"""Record the software and CPU the results were produced on (results/environment.json)."""
import json
import platform
import subprocess
import sys
from pathlib import Path

import mpmath
import numpy as np

info = {}
for line in open("/proc/cpuinfo"):
    if line.startswith("model name"):
        info["cpu"] = line.split(":", 1)[1].strip()
    if line.startswith("flags"):
        fl = line.split(":", 1)[1].split()
        info["cpu_flags_of_interest"] = sorted(f for f in fl if f.startswith(("avx", "fma", "sse4")))
        break
info["python"] = sys.version
info["numpy"] = np.__version__
info["numpy_simd"] = np._core._multiarray_umath.__cpu_features__ and sorted(
    k for k, v in np._core._multiarray_umath.__cpu_features__.items() if v)
info["mpmath"] = mpmath.__version__
info["mpmath_backend"] = mpmath.libmp.BACKEND
info["libc"] = " ".join(platform.libc_ver())
info["gcc"] = subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
info["kernel"] = platform.release()
out = Path(__file__).resolve().parent.parent / "results" / "environment.json"
out.write_text(json.dumps(info, indent=1) + "\n")
print(json.dumps(info, indent=1))
