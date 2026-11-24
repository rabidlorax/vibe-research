#!/usr/bin/env python3
"""List every float32 input where np.exp2 is 3 or more representable values
from the correctly rounded result, and check whether any of them is among the
samples of NumPy's own accuracy test (umath-validation-set-exp2.csv in the
installed wheel).  Writes results/exp2_beyond_tolerance.json.  About 5 minutes.
"""
import csv
import json
import os
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import sweep

FMT = sweep.FMT["float32"]
N = 1 << 22


def work(start):
    with np.errstate(all="ignore"):
        bits = np.arange(start, start + N, dtype=np.uint64).astype(np.uint32)
        x = bits.view(np.float32)
        y = np.exp2(x)
        ref, _, _, _ = sweep.reference("exp2", x, FMT)
        both = ~np.isnan(y) & ~np.isnan(ref)
        steps = np.where(both, np.abs(sweep.ordinal(y, FMT) - sweep.ordinal(ref, FMT)), 0)
        return [int(b) for b in bits[steps >= 3]], int(steps.max())


if __name__ == "__main__":
    sweep.build_lib()
    with Pool(os.cpu_count()) as pool:
        res = pool.map(work, range(0, 1 << 32, N), chunksize=1)
    found = sorted(b for r in res for b in r[0])
    csv_path = Path(np.__file__).parent / "_core/tests/data/umath-validation-set-exp2.csv"
    samples = set()
    with open(csv_path) as fh:
        for row in csv.reader(r for r in fh if r[0] not in "$#"):
            if row and row[0] == "np.float32":
                samples.add(int(row[1], 16))
    xs = np.array(found, dtype=np.uint32).view(np.float32)
    out = {
        "numpy": np.__version__,
        "inputs_3_or_more_steps": len(found),
        "max_steps": max(r[1] for r in res),
        "smallest_x": float(xs.min()), "largest_x": float(xs.max()),
        "float32_samples_in_wheel_csv": len(samples),
        "of_those_inputs_in_csv": len(samples & set(found)),
        "inputs_hex": [f"{b:#x}" for b in found],
    }
    (sweep.RESULTS / "exp2_beyond_tolerance.json").write_text(json.dumps(out, indent=1) + "\n")
    print({k: v for k, v in out.items() if k != "inputs_hex"})
