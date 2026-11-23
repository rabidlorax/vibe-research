# Biology and Bioinformatics

**Scope.** Genomics, comparative and evolutionary biology, protein sequence and structure analysis, systems biology, ecology, and mathematical biology, using public data and models.

**Why this is tractable without a lab.** Sequencing and structure databases grow faster than anyone analyses them. Analysis, modelling, and hypothesis generation are computational; validation in the wet lab is not, and is handed off explicitly.

## How results are verified here

- Pipelines pinned to database release versions and accession numbers
- Multiple-testing correction, appropriate null models, and held-out validation
- Every biological conclusion from data is `external-data`; mechanistic claims without experiment are `conjecture`
- State the experiment that would confirm or refute each hypothesis

## Public data and reference sources

- NCBI (GenBank, SRA, GEO), Ensembl, UniProt
- PDB, AlphaFold DB
- GTEx, ENCODE, Human Cell Atlas
- GBIF, eBird, Open Tree of Life
- BioModels

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Comparative genomics of under-analysed public genomes
- Re-analysis of public expression datasets with improved methods; check whether headline findings replicate
- Annotation of proteins of unknown function from structure and context
- Ecological and biodiversity trend analyses from occurrence data, with sampling-bias handling
- Mathematical models of biological dynamics with rigorous analysis

## Limits and cautions

- Nothing that enhances pathogen transmissibility, virulence, or immune evasion, and no toxin or pathogen design work, regardless of framing
- No re-identification of individuals from genomic data; respect controlled-access terms

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py biology-and-bioinformatics <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).
