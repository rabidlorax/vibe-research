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
[rabidlorax/math](https://github.com/rabidlorax/math).** Pure, experimental,
and recreational mathematics goes there. A proof that supports a project in
one of the domains above stays with that project.

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
- A project's **status** says whether anyone has independently re-checked it.
  `result` means not yet; `verified` means a separate review is logged.
- **Novelty** is `unchecked` unless a literature search is documented. The
  models cannot see everything published, so "new" always means "not found in
  the search described".
- Nothing here has been peer reviewed, and nothing is medical, legal, financial,
  or engineering advice.

Failed attempts and refuted hypotheses are kept, not deleted. They are results.

## Further reading

- [`docs/research-standards.md`](docs/research-standards.md): evidence labels,
  status lifecycle, citation and data rules, limits
- [`CLAUDE.md`](CLAUDE.md): working instructions for models contributing here
- [`templates/project-README.md`](templates/project-README.md): the project template
