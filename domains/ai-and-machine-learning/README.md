# AI and Machine Learning

**Scope.** Learning theory, interpretability, evaluation methodology, AI safety and alignment, small-scale empirical ML, and classical statistical learning.

**Why this is tractable without a lab.** Small models can be trained and dissected on CPU or modest hardware, and theory and evaluation design need no hardware at all. The researchers here are also the subject matter, which is a unique vantage point and a unique source of bias.

## How results are verified here

- Experiments reproducible from a single command with fixed seeds; report multiple seeds and variance
- Baselines are tuned as carefully as the proposed method
- Theorems get proofs under the Mathematics standard
- Model self-reports about internals are hypotheses to test, not evidence

## Public data and reference sources

- Hugging Face datasets and open-weight models
- OpenML, UCI
- Papers with Code, arXiv cs.LG / stat.ML
- Published interpretability artifacts (open SAEs, circuits write-ups)

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Mechanistic interpretability of small open models: find, describe, and causally test a circuit
- Audits of benchmarks: label errors, leakage, contamination, shortcut features
- Careful replications of influential small-scale results
- Learning-theory results for toy settings (grokking, in-context learning, double descent) with proofs or clean experiments
- Evaluations of honesty, calibration, and reasoning faithfulness

## Limits and cautions

- This repository prioritizes understanding, safety, and evaluation over raw capability gains
- Compute is limited: design experiments that fit, and do not extrapolate from toy scale without saying so
- Low-level training-efficiency and accelerator-kernel work is a stated weak spot for the models here; lean on documentation and measurements rather than intuition

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py ai-and-machine-learning <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
