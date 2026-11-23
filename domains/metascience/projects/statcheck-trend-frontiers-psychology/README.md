---
title: Trend in statistical reporting inconsistencies in an open-access psychology journal, 2010 to 2026
domain: metascience
status: result
evidence: external-data
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-23
---

# Trend in statistical reporting inconsistencies in an open-access psychology journal, 2010 to 2026

## Question

Among articles in the open-access journal *Frontiers in Psychology* with
machine-readable full text, what fraction of null-hypothesis test results
reported in the standard form (a t, F, chi-square, r or z statistic with its
degrees of freedom and a p-value) give a p-value that does not match the one
recomputed from the reported statistic and degrees of freedom, for each
publication year from 2010 to 2026? Has that fraction, and the fraction of
mismatches that change the verdict at the 0.05 level, gone up, gone down, or
stayed the same over that period?

An answer is a table by publication year of: articles sampled, articles with
at least one extractable result, results extracted, the share of results that
are inconsistent, the share that are decision-changing, and the share of
articles with at least one of each, with confidence intervals that account for
results clustering within articles; a trend estimate with its uncertainty; and
a hand-checked sample of the automated flags with the false-positive rate.

Scope as run: the feasibility check showed that every article could be
fetched, so the analysis covers all of them and no sampling was needed. No
second journal was added.

## Why it matters

A widely cited 2016 study using the `statcheck` program found that about half
of psychology articles from 1985 to 2013 contained at least one p-value that
did not match its test statistic (Nuijten et al. 2016, read in this session;
see Prior work). Since then the field has gone through a decade of
reform aimed at more careful reporting, some journals run automated checks at
submission, and writing tools have changed. Whether reporting accuracy in the
published record has actually improved is an empirical question that authors,
editors and readers of this literature have a stake in, and it can be answered
from public full text with a few thousand lines of arithmetic.

## Summary of result

Every *Frontiers in Psychology* article with open-access full text in Europe
PMC and PubMed Central on 2026-11-23 was analysed: 54,015 articles, of which
17,210 contain at least one test result in the form the extractor reads, for
188,597 results in total.

1. **From 2010 to 2025 the rate did not move.** In each of those sixteen years
   between 9.4% and 12.8% of extracted results had a p-value that does not
   match the reported statistic and degrees of freedom. A logistic trend over
   2010-2025 gives an odds ratio of 1.004 per year (95% interval 0.994 to
   1.014). A decade of reform left this measure where it was.
2. **Decision-changing mismatches also show no robust trend to 2025.** They
   were between 0.96% and 1.97% of results each year. Under the primary
   definition they drift upward (odds ratio 1.030 per year, 1.011 to 1.048),
   but without the one-tailed allowance the drift is not distinguishable from
   zero (1.011, 0.994 to 1.028), so the rise is not a finding.
3. **In 2026 the rate fell by about a third.** 7.2% of results (6.1 to 8.5)
   were inconsistent in 2026, against 11.1% in 2023-2025 (odds ratio 0.62,
   0.51 to 0.75). Decision-changing mismatches fell from 1.55% to 0.87% (odds
   ratio 0.56, 0.39 to 0.81). By half-year the fall is concentrated in
   articles published electronically from July 2026 (5.7%, 4.3 to 7.3). It
   appears in every kind of test and for both exactly reported and inequality
   p-values. This comparison was made after seeing the yearly table and is
   post hoc. 2026 is one incomplete year; whether the fall persists is not yet
   known.
4. **Why it fell is not established here.** See claim 8.

Evidence label for the project: `external-data`. All counts come from article
text that was not written here, read by an automatic extractor; a hand-check
of 250 extracted results is reported below.

![Yearly rates](results/trend.png)

| Year | Articles | With results | Results | Inconsistent % (95% interval) | Decision % (95% interval) | Articles with at least one inconsistency % |
|---|---|---|---|---|---|---|
| 2010 | 142 | 54 | 581 | 11.5 (6.9-17.1) | 1.55 (0.59-2.75) | 50.0 |
| 2011 | 397 | 173 | 2,387 | 12.8 (10.2-15.7) | 1.97 (1.29-2.75) | 54.3 |
| 2012 | 621 | 282 | 3,693 | 10.2 (8.4-12.1) | 1.08 (0.67-1.54) | 43.3 |
| 2013 | 996 | 461 | 6,029 | 9.4 (8.0-10.7) | 0.96 (0.67-1.34) | 46.9 |
| 2014 | 1,607 | 723 | 9,644 | 11.2 (9.9-12.6) | 1.47 (1.13-1.85) | 48.4 |
| 2015 | 2,045 | 990 | 12,810 | 10.6 (9.4-11.8) | 1.16 (0.93-1.39) | 45.5 |
| 2016 | 2,074 | 947 | 11,844 | 10.6 (9.5-12.0) | 1.05 (0.83-1.27) | 45.2 |
| 2017 | 2,366 | 1,051 | 13,430 | 11.7 (10.1-13.5) | 1.30 (0.99-1.67) | 44.1 |
| 2018 | 2,783 | 1,242 | 15,043 | 10.1 (9.1-11.1) | 1.10 (0.90-1.31) | 43.6 |
| 2019 | 3,075 | 1,248 | 15,359 | 10.1 (9.2-11.1) | 1.18 (0.97-1.42) | 42.5 |
| 2020 | 4,088 | 1,421 | 15,593 | 11.3 (10.1-12.6) | 1.74 (1.34-2.22) | 41.9 |
| 2021 | 6,675 | 1,997 | 20,969 | 11.0 (9.7-12.2) | 1.62 (1.30-1.98) | 36.4 |
| 2022 | 8,500 | 1,876 | 19,128 | 11.3 (10.1-12.6) | 1.64 (1.35-1.94) | 39.7 |
| 2023 | 4,634 | 1,179 | 12,124 | 11.5 (10.2-12.9) | 1.70 (1.25-2.30) | 39.5 |
| 2024 | 3,477 | 831 | 8,330 | 10.9 (9.5-12.2) | 1.50 (1.13-1.95) | 39.2 |
| 2025 | 4,525 | 1,075 | 9,025 | 10.8 (9.4-12.3) | 1.40 (1.09-1.74) | 32.1 |
| 2026 (to early November) | 6,010 | 1,660 | 12,608 | 7.2 (6.1-8.5) | 0.87 (0.60-1.15) | 18.9 |

Source: `results/yearly.csv`. Percentages in the fifth and sixth columns are
of extracted results; the last column is of articles with at least one
extracted result. Intervals resample whole articles.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | The corpus is 54,015 articles (every PMCID returned by the Europe PMC query in Method on 2026-11-23; all were retrieved with a body), 17,210 with at least one extracted result, 188,597 extracted results. | external-data | Run the Reproduction commands; `python src/extract.py` prints the counts. The corpus grows, so a later run returns more articles; the ID lists used are in `data/ids/`. |
| 2 | For each year 2010-2025 the share of extracted results flagged inconsistent is between 9.37% (2013) and 12.82% (2011), and the logistic trend over 2010-2025 is an odds ratio of 1.0040 per year (0.9944 to 1.0137, standard errors clustered on article). | external-data | `results/yearly.csv`, `results/post_hoc.txt` (line "trend 2010-2025, error_1t"). The restriction to 2010-2025 was chosen after seeing 2026; the pre-specified trend over all years is in `results/trend.txt`, first line (0.9918, 0.9833 to 1.0003). |
| 3 | Decision inconsistencies are between 0.96% and 1.97% of results in each year 2010-2025. Their 2010-2025 trend is an odds ratio of 1.0295 per year (1.0114 to 1.0480) with the one-tailed allowance and 1.0108 (0.9938 to 1.0280) without it. | external-data | `results/yearly.csv`, `results/yearly_no_one_tailed_allowance.csv`, `results/post_hoc.txt`. |
| 4 | In 2026, 7.18% of results are flagged inconsistent (6.06 to 8.46) against 11.09% in 2023-2025 pooled (odds ratio 0.620, 0.510 to 0.754), and 0.87% against 1.55% for decision inconsistencies (odds ratio 0.559, 0.388 to 0.805). Without the one-tailed allowance: 7.61% against 11.54% (odds ratio 0.632, 0.523 to 0.764). Post hoc. | external-data | `results/post_hoc.txt`. |
| 5 | By half-year of electronic publication the rate is 12.3, 11.6, 10.4, 11.0, 13.2, 9.2% for 2023H1 to 2025H2, 9.1% for 2026H1 and 5.7% (4.3 to 7.3) for 2026H2 (July to early November). The 2026 fall is present for each test type (F 9.6 to 5.9%, chi-square 10.4 to 4.8%, t 12.7 to 10.0%, z 13.8 to 10.5%, r 22.0 to 11.6%) and for exactly reported p (16.9 to 11.8%) and inequality p (4.4 to 1.8%). Post hoc. | external-data | `results/half_years_2023_2026.csv`, `results/post_hoc.txt`. |
| 6 | Among articles with at least one extracted result, the share with at least one flagged inconsistency fell from 50.0% and 54.3% in 2010 and 2011 to 39.2% in 2024, 32.1% in 2025 and 18.9% in 2026. Part of this is arithmetic: the median number of extracted results per such article fell from 8-10 before 2019 to 5 in 2025 and 4 in 2026. Adjusted for the logarithm of the number of results the odds ratio is 0.9625 per year (0.9541 to 0.9709) over 2010-2026. | external-data | `results/yearly.csv`, `results/trend.txt`. |
| 7 | In a hand-check of 200 flagged results, 178 (89%) are inconsistent as printed with no explanation visible in the 150 characters either side, 5 carry a stated correction, 14 are probably one-tailed tests the keyword rule did not credit, and 2 are extraction errors. All 50 unflagged results checked were correctly extracted. The split is similar in each period, including July-November 2026 (18 of 20 inconsistent as printed). | external-data | `results/handcheck.csv` lists every item with its label; `python src/sample_handcheck.py` rebuilds the text snippets from the downloaded articles for re-reading. The labels are one model's reading. |
| 8 | The 2026 fall has a cause this project does not identify. Candidate explanations are automated checking by authors or their writing tools, checking introduced in the journal's process, and a change in who publishes what in the journal. | conjecture | Not checkable from this data. What would settle it: the journal stating whether and when it introduced statistical checks; the same analysis on other journals for 2026 (a fall everywhere at the same time points to authors' tools, a fall in one publisher points to the publisher); and rerunning this analysis in 2027. |
| 9 | Benchmark: for 2010-2013 this pipeline finds 2,156 articles, 970 with results, 12,690 results, and a mean per-article inconsistency rate of 11.4% when `p = .000` is counted as wrong. | external-data | `results/trend.txt`, last line. |
| 10 | Nuijten et al. (2016) report, for the same journal and years with the original `statcheck`, 2,139 articles, 702 with results, 10,149 results, and a mean per-article inconsistency rate of 12.8%. | literature | Nuijten et al. 2016, Table 1 and the text under Figure 3 (quoted in Prior work). |

## Method

**Corpus.** Europe PMC REST search, one query per year 2010-2026:
`JOURNAL:"Front Psychol" AND PUB_YEAR:<year> AND OPEN_ACCESS:y AND IN_EPMC:y`,
paged to exhaustion (`src/fetch_ids.py`). The PMCIDs are in `data/ids/`. The
JATS XML of every one was then downloaded from NCBI E-utilities (`efetch`,
`db=pmc`, 100 IDs per request; `src/fetch_fulltext.py`). All 54,015 came back
with a `<body>`. No article type was excluded: editorials, reviews and
corrections are in the denominator of "articles" but contribute results only
if they report any (a variant restricted to `research-article` is reported).
"Year" in the yearly table is the year of the Europe PMC query that returned
the article; the half-year table uses the electronic publication date in the
XML.

**Text.** `src/extract.py` flattens each article body to one string: inline
markup (italic, superscript, subscript, cross-references) disappears so that
`<italic>t</italic>(23)` becomes `t(23)`, block elements become spaces, table
cells are separated by ` | `, MathML keeps its characters, TeX duplicates and
display formulas are dropped, and typographic minus signs and spaces are
mapped to ASCII. Abstracts and reference lists are not read.

**Extraction and checking.** `src/statcheck_py.py` is an independent Python
re-implementation of the core of the `statcheck` method, written from the
published description, not ported from the R code. It reads only results of
the form *statistic(df) = value, p <=> value* for t, F, r, chi-square and z
(z has no df), with a comma or semicolon directly between the statistic and
`p`. For each it computes the two-tailed (t, r, z) or upper-tail (F,
chi-square) p-value over the whole range of statistics that round to the
printed one, and calls the result

- *inconsistent* if no p in that range rounds to the reported p (for `p =`),
  or lies below it (for `p <`), or above it (for `p >`);
- a *decision inconsistency* if it is inconsistent and the reported p is on
  one side of .05 while the whole recomputed range is on the other
  (`p = .05` counts as significant; `p < .10` or `p > .01` cannot be placed
  and are never decision inconsistencies).

`p = .000` is read as "rounds to zero at three decimals" and is not
automatically wrong. As in `statcheck`, if the article body contains
"one-tailed", "one-sided" or "directional" anywhere, a t, r or z result that
would be consistent as a one-tailed test is not flagged; this is the primary
definition, and every table is also given without that allowance.
`src/test_statcheck_py.py` holds 36 hand-computed cases.

**Analysis.** `src/analyze.py`. Yearly shares with 95% percentile intervals
from 2,000 bootstrap resamples of whole articles (seed 20261123); Wilson
intervals for article-level shares; logistic regression of the result-level
flag on year with standard errors clustered on article; an article-level
logistic regression of "any inconsistency" on year and log number of results.

**What was fixed in advance and what was not.** The extractor, the yearly
table, the trend model and the eight variants in `results/variants.csv` were
committed (`c7e1ecc`) when only 2010-2016 had been downloaded and looked at.
After the full yearly table showed the 2026 fall, the following were added
and are post hoc: the table without the one-tailed allowance, the half-year
table, the 2026 versus 2023-2025 contrast, the 2010-2025 trend, the breakdown
of the fall by test type and p form, and the extra hand-check stratum for
July-November 2026. One extractor bug found in the hand-check (a p-value in
scientific notation, `p = 1.00E-04`, read as `p = 1.00`) was fixed afterwards;
it removed 4 of 188,601 results.

**Variants** (`results/variants.csv`; trend over all of 2010-2026, which the
2026 fall pulls down):

| Variant | 2010-2013 | 2023-2026 | Odds ratio per year (95% interval) |
|---|---|---|---|
| Primary | 10.35% | 9.92% | 0.992 (0.983-1.000) |
| No one-tailed allowance | 11.17% | 10.36% | 0.989 (0.980-0.997) |
| `p = .000` counted as inconsistent | 10.71% | 11.00% | 0.998 (0.990-1.007) |
| Exactly reported p only | 16.55% | 15.37% | 0.994 (0.983-1.004) |
| Inequality p only | 4.96% | 3.61% | 0.968 (0.955-0.982) |
| `research-article` only | 10.33% | 9.61% | 0.990 (0.981-0.998) |
| t and F only | 10.07% | 9.58% | 0.989 (0.980-0.999) |
| Excluding 2026 (last column is 2023-2025) | 10.35% | 11.09% | 1.004 (0.994-1.014) |

**Hand-check.** `src/sample_handcheck.py --redraw` drew, per period
(2010-2015, 2016-2021, 2022-2026), 40 flagged results that are not decision
inconsistencies, 20 decision inconsistencies and 10 unflagged results, plus
(post hoc) 20 flagged and 20 unflagged from July-November 2026: 250 items.
Each was read with 150 characters of context either side and labelled
`inconsistent_as_printed`, `explained_by_stated_correction`,
`probably_one_tailed`, `extraction_error` or `correctly_extracted`.

| Stratum | Period | Inconsistent as printed | Stated correction | Probably one-tailed | Extraction error |
|---|---|---|---|---|---|
| Flagged, not decision | 2010-2015 | 39 | 1 | 0 | 0 |
| Flagged, not decision | 2016-2021 | 36 | 3 | 1 | 0 |
| Flagged, not decision | 2022-2026 | 38 | 0 | 2 | 0 |
| Flagged (any) | Jul-Nov 2026 | 18 | 0 | 2 | 0 |
| Decision | 2010-2015 | 16 | 0 | 4 | 0 |
| Decision | 2016-2021 | 18 | 0 | 2 | 0 |
| Decision | 2022-2026 | 14 | 1 | 3 | 2 |

"Inconsistent as printed" means the three printed numbers cannot all be right;
it does not say which one is wrong or why. At least 10 of the 178 are a floor
value such as `p = .001` printed for a far smaller p, 15 sit next to results
that look multiplicity-adjusted although no adjustment is stated in the text
read, and 9 are cases where the authors appear to have printed a different
quantity in place of the statistic or its degrees of freedom. These notes are
in `results/handcheck.csv`.

## Reproduction

Python 3.13 with the packages in `requirements.txt`. From the project folder:

```bash
python src/test_statcheck_py.py     # 36 hand-computed cases; prints "all tests passed"
python src/fetch_ids.py             # Europe PMC; about 12 minutes; rewrites data/ids/
python src/fetch_fulltext.py        # NCBI efetch; about 30 minutes; 1.4 GB into data/raw/xml/
python src/extract.py               # about 2 minutes on 4 cores; writes data/*.csv.gz
python src/analyze.py               # about 1 minute; writes results/
python src/sample_handcheck.py      # rebuilds the hand-check snippets in data/raw/
```

To reproduce the numbers above exactly, skip `fetch_ids.py` and use the
committed `data/ids/` (SHA-256 of the 17 files concatenated in name order:
`8bf3d80215ad17872a131145f3a6935790dc4b29ac4c7a1ad5b7dee918e977d3`). Rerunning
it later returns more 2026 articles. `data/articles.csv.gz` and
`data/results.csv.gz` are committed, so `analyze.py` runs without any
download. `results/analyze_stdout.txt` is the output of the run reported here.
Network: `www.ebi.ac.uk` and `eutils.ncbi.nlm.nih.gov`, no key. PMC can revise
an article's XML after deposit, so a fresh download may differ in a few
results.

## External data and what we could not reproduce

- **Article full text**: *Frontiers in Psychology*, 2010 to early November
  2026, as deposited in PubMed Central and indexed by Europe PMC. IDs from the
  Europe PMC REST API (`https://www.ebi.ac.uk/europepmc/webservices/rest/search`),
  XML from NCBI E-utilities
  (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`, `db=pmc`).
  Accessed 2026-11-23. Articles are published under CC BY; the XML is not
  committed. What is committed is derived: PMCIDs, DOIs, article type, dates,
  and the extracted statistic strings (for example `t(28) = 2.20, p = .03`).
  `results/handcheck.csv` identifies each checked string by PMCID.
- The studies behind these articles were not run here and none of their
  statistics can be recomputed from data here. This project checks only
  whether three printed numbers agree with each other.
- Every claim in the Claims table rests on this source. If PMC's copy of an
  article differs from the publisher's version, the affected results are
  wrong in the same way.
- Known problems: (a) the deposit format changed in November 2025 (the
  publication date moved to a different tag); rates under the new format in
  January-April 2026 were still 8-12%, so the format change does not by
  itself produce the fall; (b) November 2026 is incomplete (165 articles);
  (c) Europe PMC's `PUB_YEAR` differs from the electronic publication year
  for 7-12% of articles in each year from 2021; (d) no retraction or correction
  status was used, and 862 items in the corpus are corrections.
- Claim 10 rests on Nuijten et al. (2016) as published.

Listing an article in `results/handcheck.csv` says only that a printed
p-value and test statistic do not agree. It is not a statement about the
study's conclusions or about its authors.

## Prior work and novelty

Searched on 2026-11-23: web search (six queries) and OpenAlex (seven
queries) for `statcheck`, "statistical reporting inconsistencies",
"statistical reporting errors" combined with psychology, trend, over time,
prevalence, *Frontiers in Psychology*, PLOS ONE, 2015-2024, and
`JATSdecoder`; alternative names used in the literature and searched:
"p-value inconsistencies", "reporting errors", "gross inconsistencies",
"decision inconsistencies / decision errors", "incongruent p-values".
Full texts were opened where marked "read".

- Nuijten, Hartgerink, van Assen, Epskamp & Wicherts (2016), "The prevalence
  of statistical reporting errors in psychology (1985-2013)", *Behavior
  Research Methods*, doi:10.3758/s13428-015-0664-2 (read, PMC5101263). Eight
  journals including this one for 2010-2013. Table 1 row: "FP | General |
  2010-2013 | 2,139 | 702 | (32.8 %) | 10,149 | 10". Text: "PLoS showed the
  highest percentage of inconsistent p-values per article overall, followed
  by FP (14.0 % and 12.8 %, respectively)" and "The trends for PS, FP, and
  PLoS are hard to interpret given the limited number of years of covarage."
  This is the method and the baseline; it stops at 2013.
- Nuijten et al. (2017), "Journal data sharing policies and statistical
  reporting inconsistencies in psychology", *Collabra: Psychology*,
  doi:10.1525/collabra.102 (abstract only). Compares this journal with PLOS
  journals by data-sharing policy; not a time trend.
- Nuijten & Wicherts (2024), "Implementing statcheck during peer review is
  related to a steep decline in statistical-reporting inconsistencies",
  *AMPPS*, doi:10.1177/25152459241258945 (abstract only). Four other
  journals, before and after two of them adopted `statcheck`.
- Etemady & Roettger (2024 preprint), "Statistical reporting inconsistencies
  in experimental linguistics", doi:10.31234/osf.io/pwjky (abstract only).
  Eight linguistics journals, 2000-2023; rates "seem stable over publication
  years".
- Böschen (2021), "Evaluation of JATSdecoder as an automated text extraction
  tool for statistical results in scientific reports", *Scientific Reports*
  (read, PMC8484375), and Böschen (2023), "Changes in methodological study
  characteristics in psychology between 2010-2021", *PLOS ONE*,
  doi:10.1371/journal.pone.0283353 (read as reprinted in the author's
  dissertation). Both process this journal's XML through 2021 with a
  different extractor. The yearly tables seen in the second cover alpha
  levels, confidence intervals, multiple-testing corrections, one-tailed
  tests and sample sizes; no yearly p-value inconsistency rate was found in
  it.
- Böschen (2024), arXiv:2408.07948 (abstract only), argues `statcheck`'s
  strict pattern misses many results. That applies equally to the extractor
  here.

Not found in this search: a published inconsistency rate for this journal
for any year after 2013 as a time series, or any study of 2025-2026 articles
in any journal. Three of the closest papers were read only as abstracts, and
preprints from 2026 may not be indexed yet.

Conclusion of the search: go ahead as an extension. `novelty:
partially-known`. The method and the 2010-2013 level are known; the
2014-2025 series for this journal and the 2026 fall were not found elsewhere.

## Limitations and open questions

- **One journal.** Nothing here says what happened in psychology at large.
  This journal grew from 142 to several thousand articles a year and its mix
  of topics, article types and author populations changed; the flat line to
  2025 is the net of all that.
- **Only strictly formatted results are read.** 68% of articles yield no
  extracted result, and that share rose (from about 55% before 2019 to about
  75% in 2022-2025). Results in tables, results with an effect size between
  the statistic and `p`, and anything not written as *statistic(df) = value,
  p ...* are invisible. If careful and careless authors differ in how they
  format results, the extracted set is not representative, and a change in
  formatting habits over time could move the rate without any change in
  accuracy.
- **A flag is not an error in the study.** About one in ten flagged results in
  the hand-check (21 of 200) had a visible or probable innocent explanation or
  was an extraction error, and others
  may have one outside the 150 characters read (corrections described in the
  Methods section, for example). The hand-check was done by the same model
  that wrote the extractor, reading short snippets, not whole articles.
- **The one-tailed keyword rule is crude and its input drifted.** The share
  of articles containing "one-tailed", "one-sided" or "directional" (which
  also matches "bidirectional" and "directionality") rose from 12-15% in
  2023-2024 to 36% in the second half of 2026. That makes the primary
  definition more forgiving in 2026. The fall is nearly the same without the
  allowance (claim 4), so this is not what produces it.
- **The 2026 finding is post hoc, from one incomplete year.** It was not a
  hypothesis; it was seen in the table and then tested. Month-level rates are
  noisy. It needs another year of data and other journals.
- **The cause of the 2026 fall is unknown** (claim 8). Things that changed at
  the same time and could be related or coincidental: articles got longer
  (median body 43-44 thousand characters in 2023-2025, 51 thousand in 2026),
  results per article fell, three-decimal p-values rose from 73-78% to 87% of
  results, and monthly article counts rose. Nothing here measures the use of
  any tool by authors or by the journal.
- **Not `statcheck` itself.** The extractor is a re-implementation and was
  not run side by side with the R package. On 2010-2013 it extracts 25% more
  results from 38% more articles than Nuijten et al. report, and finds a
  per-article rate of 11.4% against their 12.8%. Differences in which results
  are read (semicolons and capital `Z` are accepted here; chi-square inside
  MathML is read) probably account for this, but that was not verified.
- **Decision inconsistencies are rare events.** Yearly counts are between 9
  and 340; year-to-year movements within 2010-2025 are mostly noise.
- **No proof is involved**, so nothing here is a candidate for formalization.

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
