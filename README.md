# vibe-research

Original research carried out by Claude models (Fable and Opus), organized by
field, with the evidence for every claim kept next to the claim.

The aim is work that is useful or beneficial to people, and that includes work
people will simply appreciate or find impressive: a new proof, an overlooked
object in a sky survey, a correct answer to a question nobody had worked out.

## What belongs here

- **Objective questions.** A claim must be checkable: by proof, by rerunning
  code, or against a cited source. Matters of taste, interpretation, and values
  are out of scope.
- **No physical apparatus.** Nothing here needs a wet lab, a telescope, a dig
  site, or a new measurement. Reasoning, computation, and existing data only.
- **Existing data is welcome, with a disclaimer.** Published datasets and
  results can be used even though the measurements behind them cannot be
  reproduced here. Every project says which of its conclusions rest on such
  data.
- **Capable and willing.** Work the models can actually do well, and that is
  safe to do. The limits are in
  [`docs/research-standards.md`](docs/research-standards.md#what-we-will-not-do).

## Domains

| Domain | Covers |
|---|---|
| [Computer Science](domains/computer-science/) | Algorithms, complexity, verification, systems, defensive security |
| [AI and Machine Learning](domains/ai-and-machine-learning/) | Interpretability, evaluation, safety, learning theory |
| [Statistics and Methodology](domains/statistics-and-methodology/) | Statistical theory, causal inference, simulation studies |
| [Physics](domains/physics/) | Theory, simulation, re-analysis of open experimental data |
| [Astronomy and Cosmology](domains/astronomy-and-cosmology/) | Archival surveys, exoplanets, gravitational waves, celestial mechanics |
| [Chemistry and Materials Science](domains/chemistry-and-materials/) | Computational chemistry, cheminformatics, materials screening |
| [Biology and Bioinformatics](domains/biology-and-bioinformatics/) | Genomics, protein analysis, ecology, mathematical biology |
| [Medicine and Public Health](domains/medicine-and-public-health/) | Evidence synthesis, epidemiology, trial-registry analysis |
| [Neuroscience and Cognitive Science](domains/neuroscience-and-cognitive-science/) | Open neural and behavioural data, computational models |
| [Earth and Climate Science](domains/earth-and-climate-science/) | Climate, weather, oceans, seismology, remote sensing |
| [Economics and Quantitative Social Science](domains/economics-and-social-science/) | Theory, econometrics, mechanism design, replication |
| [Linguistics](domains/linguistics/) | Corpus, historical, typological, and formal linguistics |
| [History and Digital Humanities](domains/history-and-digital-humanities/) | Digitized texts and inscriptions, published archaeological data, chronology |
| [Engineering and Applied Science](domains/engineering/) | Design and optimization in simulation, coding theory, operations research |
| [Metascience](domains/metascience/) | Reproducibility, error detection in the literature, audits of this repository |
| [Interdisciplinary](domains/interdisciplinary/) | Work that spans fields |

**Mathematics lives in its own repository:
[rabidlorax/math](https://github.com/rabidlorax/math).** All mathematics goes there, as machine-checked Lean. So does any proof that a
project in one of the domains above depends on; the project cites the
theorem by name and commit, with a permalink.

Each domain README gives its scope, how results are verified in that field,
public data sources, seed directions, and field-specific cautions.

## How a project works

```
domains/<domain>/projects/<project-slug>/
  README.md   question, claims with evidence labels, method, reproduction, disclaimers, review log
  src/        code that produces every number and figure
  data/       small inputs and fetch scripts (large raw data is not committed)
  results/    outputs, figures, proofs, write-ups
```

Start one:

```bash
python scripts/new_project.py physics my-question "A short title"
```

Validate the repository and refresh the index:

```bash
python scripts/check_repo.py --write-index
```

All projects are listed in [`PROJECTS.md`](PROJECTS.md).

## Reading results from this repository

Everything here was produced by AI models. Treat it accordingly:

- Each claim carries an **evidence label** (`proved-formal`, `proved-informal`,
  `computed`, `external-data`, `literature`, `conjecture`). The label tells you
  how far to trust it and how to check it.
- Formal proofs are not in this repository. They are in
  [rabidlorax/math](https://github.com/rabidlorax/math), and each
  `proved-formal` claim names the theorem and the commit to check, and links
  to its statement at that commit.
- A project's **status** says whether anyone has independently re-checked it.
  `result` means not yet; `verified` means a separate review is logged.
- **Novelty** is `unchecked` unless a literature search is documented. The
  models cannot see everything published, so "new" always means "not found in
  the search described".
- Nothing here has been peer reviewed, and nothing is medical, legal, financial,
  or engineering advice.

Failed attempts and refuted hypotheses are kept, not deleted. They are results.

## Licence

Everything original in this repository (text, code, figures, results) is
dedicated to the public domain under [CC0 1.0](LICENSE). Anyone may copy,
modify, publish, and use it for any purpose, including commercially, without
asking and without credit. It comes with no warranty.

The same freedom applies to the name "vibe-research" and to any wordmark,
logo or other branding from this repository: the owner waives trademark rights
in them, which CC0 on its own does not do. See [TRADEMARKS.md](TRADEMARKS.md).

This covers only what was created here. External datasets and published
sources that a project uses keep their own licences, which each project
records. Do not commit third-party material that cannot be released this way;
commit the script that fetches it instead.

## Further reading

- [`docs/research-standards.md`](docs/research-standards.md): evidence labels,
  status lifecycle, citation and data rules, limits
- [`docs/environment.md`](docs/environment.md): which data sources are reachable
  from a research session, and their quirks
- [`CLAUDE.md`](CLAUDE.md): working instructions for models contributing here
- [`templates/project-README.md`](templates/project-README.md): the project template
