---
title: Trend in statistical reporting inconsistencies in an open-access psychology journal, 2010 to 2026
domain: metascience
status: result
evidence: external-data
novelty: partially-known
models: [claude-fable-5-2]
started: 2026-11-23
updated: 2026-11-24
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
of the psychology articles from 1985 to 2013 in which it could read test
results contained at least one p-value that did not match its test statistic
(Nuijten et al. 2016, read in this session; see Prior work). Since then the field has gone through a decade of
reform aimed at more careful reporting, some journals run automated checks at
submission, and writing tools have changed. Whether reporting accuracy in the
published record has actually improved is an empirical question that authors,
editors and readers of this literature have a stake in, and it can be answered
from public full text with a few thousand lines of arithmetic.

## Summary of result

Every *Frontiers in Psychology* article with open-access full text in Europe
PMC and PubMed Central on 2026-11-23 was analysed: 54,015 articles, of which
17,746 contain at least one test result in the form the extractor reads, for
205,835 results in total.

1. **No trend was detected in the pooled rate per result across publication
   years 2010 to 2025.** In each
   of those sixteen years between 9.3% and 12.5% of extracted results had a
   p-value that does not match the reported statistic and degrees of freedom.
   A logistic trend over 2010-2025 gives an odds ratio of 1.002 per year (95%
   interval 0.993 to 1.011). That is the pooled rate per result. At article
   level, allowing for the falling number of results per article, the chance
   that an article has at least one inconsistency declined slightly (odds
   ratio 0.986 per year, 0.977 to 0.996; post hoc). Inside the pooled rate,
   results
   reported as an inequality (`p < x`) became less often inconsistent (odds
   ratio 0.963 per year, 0.950 to 0.977, without the one-tailed allowance)
   while exactly reported p-values, which are flagged several times as often,
   stayed flat (1.003, 0.991 to 1.014) and grew from 37% to over half of
   results. This is one journal whose size and authorship
   changed a great deal over the period, so it is a statement about what was
   published there, not about the field.
2. **Decision-changing mismatches show no robust trend to 2025.** They were
   between 1.0% and 1.9% of results each year. Under the primary definition
   they drift upward (odds ratio 1.026 per year, 1.010 to 1.042), but without
   the one-tailed allowance the drift is not distinguishable from zero (1.009,
   0.993 to 1.024), so the rise is not a finding. In the hand-check one
   flagged decision inconsistency in five had a stated or probable innocent
   explanation or was an extraction error.
3. **Grouped by the date the manuscript was received, the rate is lower from
   mid-2025 and falls sharply for manuscripts received from June 2026.**
   Without the one-tailed allowance it is 9.5% to 12.9% for each quarter of
   receipt from 2023Q1 to 2025Q1 and 8.9% to 10.3% for 2025Q2 to 2026Q1
   (pooled 9.4% against 11.7% before; odds ratio 0.79, 0.67 to 0.93).
   Manuscripts received in April-May 2026 are at 6.3%, which is not clearly
   different from the preceding year (odds ratio 0.64, 0.39 to 1.06); the
   rate is low among articles with a first affiliation in China (3.4%) but
   not in the bulk of other countries (9.4%). Manuscripts
   received from June 2026 are at 2.7% (odds ratio 0.26, 0.18 to 0.38), in
   China and elsewhere and in each test type with enough results to tell. By publication year this shows up as
   6.8% in 2026 against 10.7% in 2023-2025, which mixes older and newer
   cohorts. All of this was found after looking at the data and is post hoc.
   The newest cohorts are incomplete: only manuscripts published within a few
   months of receipt are in the data yet. Restricting every cohort to such
   fast manuscripts gives the same picture.
4. **The cause is not known.** Articles that declare generative AI was used and articles that
   declare it was not both fall to about 2% for receipts of 2026Q3, and
   it is present for authors in China and elsewhere. Claim 11 states the open
   explanations as a conjecture; it is not a headline result.

Evidence label for the project: `external-data`. All counts come from article
text that was not written here, read by an automatic extractor; a hand-check
of 250 extracted results is reported below.

![Yearly rates](results/trend.png)

By year of publication (`results/yearly.csv`; primary definition):

| Year | Articles | With results | Results | Inconsistent % (95% interval) | Decision % (95% interval) | Articles with at least one inconsistency % |
|---|---|---|---|---|---|---|
| 2010 | 142 | 59 | 651 | 11.4 (7.1-16.4) | 1.38 (0.46-2.46) | 52.5 |
| 2011 | 397 | 175 | 2,649 | 12.5 (10.0-15.2) | 1.85 (1.21-2.58) | 59.4 |
| 2012 | 621 | 286 | 4,241 | 10.0 (8.4-11.7) | 1.11 (0.72-1.55) | 46.5 |
| 2013 | 996 | 471 | 6,866 | 9.3 (8.1-10.7) | 1.02 (0.72-1.35) | 49.0 |
| 2014 | 1,607 | 740 | 10,735 | 11.3 (10.0-12.7) | 1.47 (1.13-1.83) | 50.4 |
| 2015 | 2,045 | 1,010 | 14,324 | 10.3 (9.2-11.5) | 1.17 (0.95-1.40) | 46.8 |
| 2016 | 2,074 | 964 | 12,816 | 10.2 (9.1-11.3) | 1.04 (0.84-1.26) | 46.3 |
| 2017 | 2,366 | 1,083 | 14,455 | 11.3 (9.8-13.2) | 1.30 (0.98-1.66) | 45.0 |
| 2018 | 2,783 | 1,286 | 16,318 | 10.0 (9.1-10.9) | 1.08 (0.88-1.29) | 44.3 |
| 2019 | 3,075 | 1,278 | 16,726 | 10.1 (9.1-11.0) | 1.20 (0.99-1.41) | 44.1 |
| 2020 | 4,088 | 1,451 | 16,915 | 10.8 (9.7-12.0) | 1.71 (1.33-2.20) | 42.2 |
| 2021 | 6,675 | 2,061 | 22,715 | 10.7 (9.6-12.0) | 1.60 (1.29-1.93) | 36.5 |
| 2022 | 8,500 | 1,940 | 20,523 | 10.9 (9.8-12.1) | 1.64 (1.35-1.93) | 40.2 |
| 2023 | 4,634 | 1,235 | 13,086 | 10.8 (9.7-11.9) | 1.53 (1.26-1.83) | 40.5 |
| 2024 | 3,477 | 857 | 8,866 | 10.7 (9.5-12.1) | 1.50 (1.14-1.92) | 39.9 |
| 2025 | 4,525 | 1,111 | 9,914 | 10.6 (9.2-12.0) | 1.36 (1.08-1.69) | 32.9 |
| 2026 (to early November) | 6,010 | 1,739 | 14,035 | 6.8 (5.8-7.9) | 0.83 (0.60-1.12) | 19.3 |

Percentages in the fifth and sixth columns are of extracted results; the last
column is of articles with at least one extracted result. Intervals resample
whole articles.

By quarter in which the manuscript was received (`results/received_quarters.csv`):

| Manuscript received | Articles published so far | With results | Results | Inconsistent %, no one-tailed allowance (95% interval) | With allowance | Articles with at least one inconsistency %, no allowance |
|---|---|---|---|---|---|---|
| 2023Q1 | 1,259 | 346 | 3,731 | 11.9 (10.0-13.9) | 11.2 | 46.5 |
| 2023Q2 | 943 | 261 | 2,680 | 10.9 (8.6-13.2) | 10.8 | 41.0 |
| 2023Q3 | 1,075 | 266 | 2,710 | 12.5 (9.9-15.1) | 12.0 | 44.7 |
| 2023Q4 | 975 | 231 | 2,570 | 9.5 (7.3-11.8) | 9.0 | 36.8 |
| 2024Q1 | 918 | 223 | 1,972 | 12.9 (10.2-16.0) | 11.5 | 42.2 |
| 2024Q2 | 944 | 219 | 2,096 | 10.8 (8.3-13.5) | 10.3 | 38.8 |
| 2024Q3 | 821 | 197 | 1,961 | 12.2 (9.3-15.4) | 11.8 | 36.5 |
| 2024Q4 | 915 | 222 | 2,177 | 12.5 (9.2-16.4) | 11.9 | 37.8 |
| 2025Q1 | 963 | 267 | 2,888 | 12.3 (9.1-15.9) | 12.0 | 37.8 |
| 2025Q2 | 1,045 | 256 | 2,258 | 10.3 (8.1-12.7) | 9.8 | 34.0 |
| 2025Q3 | 1,328 | 332 | 2,462 | 9.3 (7.1-11.8) | 8.6 | 25.9 |
| 2025Q4 | 1,506 | 384 | 3,409 | 8.9 (7.1-10.7) | 8.6 | 31.8 |
| 2026Q1 | 1,763 | 476 | 3,909 | 9.5 (7.0-12.3) | 9.1 | 22.5 |
| 2026Q2 | 1,822 | 556 | 4,271 | 5.2 (3.5-7.3) | 4.9 | 13.8 |
| 2026Q3 | 764 | 248 | 1,888 | 2.2 (1.2-3.4) | 1.7 | 8.1 |

"Articles published so far" counts every article in the corpus received in
that quarter. For 2026Q2 and 2026Q3 more will be published later; those not
yet published took longer in review and could differ. The last column uses
the definition without the one-tailed allowance (the yearly table's last
column uses the primary definition). 2026Q4 is omitted: 3 articles with
results, 35 results. Monthly figures are in `results/received_months.csv`.

## Claims

| # | Claim | Evidence | How to check |
|---|-------|----------|--------------|
| 1 | The corpus is 54,015 articles (every PMCID returned by the Europe PMC query in Method on 2026-11-23; all were retrieved with a body), 17,746 with at least one extracted result, 205,835 extracted results. | external-data | Run the Reproduction commands; `python src/extract.py` prints the counts. The corpus grows, so a later run of the ID query returns more articles; the ID lists used are in `data/ids/`. |
| 2 | For each publication year 2010-2025 the share of extracted results flagged inconsistent is between 9.34% (2013) and 12.53% (2011). The logistic trend over 2010-2025 is an odds ratio of 1.0020 per year (0.9927 to 1.0113; standard errors clustered on article) with the one-tailed allowance and 0.9983 (0.9893 to 1.0074) without it. | external-data | `results/yearly.csv`, `results/post_hoc.txt` (lines "trend 2010-2025"). "Excluding 2026" and "no one-tailed allowance" were among the variants committed in advance; making 2010-2025 the headline was decided after seeing 2026. The planned primary trend over all years is the first line of `results/trend.txt` (0.9895, 0.9814 to 0.9977). Split by how p is written, the 2010-2025 trend is 1.0025 (0.9914 to 1.0137) for `p = x` and 0.9631 (0.9499 to 0.9765) for inequalities without the allowance (1.0054 and 0.9697 with it); the share of `p = x` results rose from 37% in 2010 to 52-56% in each year 2014-2024 (post hoc; `results/post_hoc.txt`, `results/descriptives.txt`). |
| 3 | Decision inconsistencies are between 1.02% (2013) and 1.85% (2011) of results in each year 2010-2025. Their 2010-2025 trend is an odds ratio of 1.0258 per year (1.0096 to 1.0422) with the one-tailed allowance and 1.0086 (0.9934 to 1.0240) without it. Of 60 flagged decision inconsistencies read by hand, 48 were labelled inconsistent as printed (claim 10). | external-data | `results/yearly.csv`, `results/yearly_no_one_tailed_allowance.csv`, `results/post_hoc.txt`, `results/handcheck.csv`. |
| 4 | By publication year, 6.82% of 2026 results are flagged inconsistent (5.76 to 7.89) against 10.70% in 2023-2025 pooled (odds ratio 0.611, 0.506 to 0.738), and 0.83% against 1.47% for decision inconsistencies (odds ratio 0.564, 0.401 to 0.793). Without the one-tailed allowance: 7.22% against 11.18% (odds ratio 0.618, 0.515 to 0.743). Split by test type, the odds ratio is 0.58 (0.45 to 0.74) for F and 0.45 (0.30 to 0.67) for chi-square; for t (0.74, 0.49 to 1.10), z (0.77, 0.50 to 1.20) and r (0.49, 0.21 to 1.17) the interval includes no change. Post hoc. | external-data | `results/post_hoc.txt`. |
| 5 | By quarter of manuscript receipt, the rate without the one-tailed allowance is 11.9, 10.9, 12.5, 9.5% for 2023Q1-Q4; 12.9, 10.8, 12.2, 12.5% for 2024Q1-Q4; 12.3, 10.3, 9.3, 8.9% for 2025Q1-Q4; 9.5% for 2026Q1; 5.2% (3.5 to 7.3) for 2026Q2; 2.2% (1.2 to 3.4) for 2026Q3. Receipts of 2025Q2-2026Q1 pooled are at 9.45% against 11.70% for 2023Q1-2025Q1 (odds ratio 0.787, 0.666 to 0.931). By month of receipt in 2026: January 6.7%, February 13.7%, March 8.2%, April 5.3%, May 7.0%, June 3.2%, July 1.7%, August 2.4% (monthly intervals are wide; November 2025 was at 6.1%). Against receipts of 2025Q2-2026Q1, April-May 2026 receipts are at 6.27% (odds ratio 0.641, 0.387 to 1.062) and receipts from June 2026 at 2.68% (odds ratio 0.264, 0.182 to 0.383). The 2026Q2 figure mixes the two. Post hoc. | external-data | `results/received_quarters.csv`, `results/received_months.csv`, `results/post_hoc.txt`. Receipt dates are the `received` dates in each article's XML. |
| 6 | The low rate in the newest cohorts is not produced by their containing only fast-published manuscripts. Restricting every receipt quarter from 2022Q1 to articles published within 3 months of receipt gives 6.3% to 14.8% for each quarter to 2026Q1 (53 to 256 articles each), then 4.3% (2.9 to 5.8; 344 articles) for 2026Q2 and 2.4% (1.3 to 3.7; 231 articles) for 2026Q3. Also, for articles published 2018-2021 the rate by receipt-to-publication interval (0-3, 4-5, 6-8, 9+ months) is 11.2, 10.7, 11.5, 11.1%, and for 2022-2024 it is 11.1, 10.5, 12.2, 12.0%. Within the 2026 cohorts themselves: of manuscripts received in April-May 2026, those published within 3 months are at 4.4% (2.5 to 6.7; 200 articles) and those published later at 8.6% (3.4 to 13.5; 155 articles), so the April-May figure may rise as that cohort completes; of manuscripts received in June 2026, those published within 3 months are at 4.1% (2.3 to 6.2; 144 articles) and those published later at 1.1% (0.2 to 2.2; 57 articles). Post hoc. | external-data | `results/received_quarters_fast.csv`, `results/post_hoc.txt`. |
| 7 | The decline does not depend on the article's generative-AI statement (97% of articles published in 2026 carry one). Received 2026Q1: 8.6% where the authors declare generative AI was not used, 11.4% where they declare it was. 2026Q2: 5.2% and 5.2%. 2026Q3: 2.2% and 2.3%. Over the same cohorts the share of articles (with results) declaring use rose: 9.7% for receipts of 2025Q1, 19.8% for 2025Q4, 28.4% for 2026Q1, 31.5% for 2026Q2, 43.1% for 2026Q3. Post hoc. | external-data | `results/post_hoc.txt`; `ai_statement` in `data/articles.csv.gz`. The statement is the authors' own declaration and was not verified. |
| 8 | The fall for receipts from June 2026 is not produced by a change in the mix of authors' countries or of test types. The share of articles whose first affiliation is in China rose from 29% (received 2023-2024) to 48% (2025Q1-2026Q1), 53% (April-May 2026) and 58% (from June 2026). Within China the rate goes 10.2%, 9.4%, 3.4%, 2.8% over those four periods; within all countries other than China and the United States 12.5%, 10.2%, 9.4%, 2.4%; United States 9.3%, 11.2%, then 4.2% and 6.2% on 14 and 12 articles. Chi-square results rose from 10% to 27% of results and strings repeated within an article from 1.7% to 6.8%; excluding repeats the rate goes 11.7%, 10.1%, 6.4%, 2.9%. By test type, receipts from June 2026 against receipts of 2023-2024: F 2.6% against 9.7% (odds ratio 0.25, 0.14 to 0.46), chi-square 1.8% against 10.2% (0.16, 0.08 to 0.34), t 3.4% against 14.7% (0.21, 0.10 to 0.43), z 3.9% against 13.5% (0.26, 0.13 to 0.52); r has 27 results in the new cohort, none flagged. In April-May 2026 the rate is low for China (3.4%) and, on 14 articles, the United States (4.2%); all other countries are at 9.4%. Post hoc. | external-data | `results/post_hoc.txt`; `country` in `data/articles.csv.gz` (first affiliation only). |
| 9 | Consistent p-values in the newest cohorts are not more often exact recomputations of the printed statistic. Among consistent three-decimal `p = x` results whose rounding range spans more than one value, the share equal to the p computed from the statistic exactly as printed is 49.2% (received 2023-2024), 45.8% (2025Q1-2026Q1), 42.1% (April-May 2026) and 51.2% (from June 2026). Post hoc. | external-data | `results/post_hoc.txt`. This argues against p-values being regenerated mechanically from the printed statistics; it does not separate other explanations. |
| 10 | Hand-check. Of 140 flagged results drawn at random, 131 (94%) were labelled inconsistent as printed; 4 carry a stated correction and 5 are probably one-tailed tests the keyword rule did not credit. Of 60 flagged decision inconsistencies, 48 (80%) were labelled inconsistent as printed, 8 probably one-tailed, 1 stated correction and 3 extraction errors (two fixed since). All 50 unflagged results checked were correctly extracted. In the flagged stratum the split is similar in each period (39, 36 and 38 of 40, and 18 of 20 for July-November 2026); in the decision stratum it is 17, 18 and 13 of 20, the last being 2022-2026. Among those labelled inconsistent as printed, notes mark a further 16 of the 140 and 13 of the 60 as possibly explained by something other than a wrong number. | external-data | `results/handcheck.csv` lists every item with its label and note; `python src/sample_handcheck.py` rebuilds the text snippets from the downloaded articles for re-reading. The labels are one model's reading of short snippets, made in the session that wrote the extractor. |
| 11 | Conjecture: the fall for manuscripts received from June 2026 reflects a change in how manuscripts are prepared or screened around the time of submission. At least two explanations remain open and are not separated here: a check applied by the journal or publisher at or after submission, and a change on the authors' side that took hold at the same time (for example drafting or checking of results with tools, declared or not). Several things shift together in that cohort: the chi-square share of results doubles, repeated strings rise, and the median article body reaches 54 thousand characters. The extractor, publication-speed selection, author country, declared AI use and test mix are argued against by claims 6 to 9 and the hand-check; claim 9 cannot see errors that were corrected, only whether consistent values look machine-generated. | conjecture | A statement from the journal on whether and when it introduced statistical checks; the same analysis on other journals of the same publisher and of other publishers for 2026; rerunning this analysis in 2027 when the 2026 cohorts are complete. |
| 12 | The publisher describes an automated screening system (AIRA) applied to every submission, running "more than 40" checks (posts of 16 September 2025 and 5 March 2026), and announced on 7 July 2025 that products of two vendors, "Cactus Communications' Paperpal Preflight and Clear Skies' Papermill Alarm and Oversight", "have been integrated" into it; the announcement presents them as fraud-screening tools. The vendor's page lists a "methodology/statistics" assessment domain under one of Preflight's modules (PeerPilot); the announcement does not say which modules were integrated. None of these pages says that p-values are checked against test statistics. On timing: the announcement falls in the same period as the smaller decline for receipts from 2025Q2 (claim 5), which is neither attributed to it nor excluded here; receipts of 2025Q3 to 2026Q1 then stay at about 9%, and nothing read here documents a change that coincides with the June 2026 fall. | literature | Pages fetched and read on 2026-11-23: frontiersin.org/news/2025/07/07/frontiers-broadens-ai-driven-integrity-checks-with-integration-of-cactus ("have been integrated into its own Artificial Intelligence Review Assistant (AIRA) submission-screening system"); frontiersin.org/news/2026/03/05/how-do-you-know-you-can-trust-the-science-you-read ("AIRA runs more than 40 AI-powered quality checks, flagging potential issues for human review on issues ranging from ethical compliance and plagiarism to signs of image manipulation"); frontiersin.org/news/2025/09/16/getting-to-know-aira-our-digital-teammate-and-detective ("AIRA performs over 40 rapid quality control checks on every submission"); paperpal.com/preflight ("Four-domain assessment: critical overview, literature review, methodology/statistics, and reporting compliance"). These are the publisher's and a vendor's own descriptions. |
| 13 | Article level: among articles with at least one extracted result, the share with at least one flagged inconsistency went from 52.5% and 59.4% in 2010 and 2011 to 39.9% in 2024, 32.9% in 2025 and 19.3% in 2026. Much of the decline before 2026 is arithmetic: the median number of extracted results per such article fell from 8-11 before 2021 to 5 in 2025 and 4 in 2026. Adjusted for the logarithm of the number of results, the odds ratio per year is 0.9861 (0.9765 to 0.9958) over 2010-2025 (post hoc) and 0.9607 (0.9525 to 0.9691) over 2010-2026 (planned). | external-data | `results/yearly.csv`, `results/trend.txt`, `results/descriptives.txt`. |
| 14 | Benchmarks. For 2010-2013 this pipeline finds 2,156 articles (1,537 of type `research-article`), 991 with results, 14,407 results, and a mean per-article inconsistency rate of 11.8% with the one-tailed allowance and `p = .000` counted as wrong, 12.9% without the allowance. For `research-article` items published to April 2015, split by receipt before or from March 2014, it finds 2,078 and 1,032 articles, 1,320 and 616 with results, 19,622 and 8,564 results, and rates of 11.9% and 11.7% with the one-tailed allowance and `p = .000` counted wrong, 13.0% and 12.5% without the allowance. | external-data | `results/trend.txt`, lines starting "benchmark". |
| 15 | Nuijten et al. (2016) report for this journal in 2010-2013, with the original `statcheck`, one-tailed detection on and `p = .000` counted wrong: 2,139 articles, 702 with results, 10,149 results, mean per-article rate 12.8%. Nuijten et al. (2017) report for research, clinical case and methods articles in this journal published March 2010 to April 2015, with `statcheck` 1.0.2: 1,819 articles received before March 2014 (804 with results, 11,079 results, 13.1%) and 873 received after (304 with results, 2,432 results, 16.2%). | literature | Passages quoted under Prior work. |

## Method

**Corpus.** Europe PMC REST search, one query per year 2010-2026:
`JOURNAL:"Front Psychol" AND PUB_YEAR:<year> AND OPEN_ACCESS:y AND IN_EPMC:y`,
paged to exhaustion (`src/fetch_ids.py`). The PMCIDs are in `data/ids/`. The
JATS XML of every one was then downloaded from NCBI E-utilities (`efetch`,
`db=pmc`, 100 IDs per request; `src/fetch_fulltext.py`). All 54,015 came back
with a `<body>`. No article type was excluded: 41,222 are `research-article`;
the rest include 3,622 reviews, 2,061 editorials, 862 corrections, 96
retraction notices and 2 expressions of concern. These are in the denominator
of "articles" but contribute results only if they report any (a variant
restricted to `research-article` is reported). No retraction status was used:
retracted articles are analysed like any other.

**Dates.** "Year" in the yearly table is the year of the Europe PMC query
that returned the article (`PUB_YEAR`). It differs from the year of
electronic publication in the XML for 1% to 12% of articles in each year
before 2026 (the article appeared online late in one year and is assigned to
the next year's volume, or the reverse). The half-year breakdown
(`results/half_years_2023_2026.csv`, not shown as a table here) uses the
electronic publication date, which is why it counts 6,551 articles in 2026
where the yearly table counts 6,010: 541 articles published online in 2026
have `PUB_YEAR` 2025. The quarter table uses the `received` date in the XML
history, present for all but 2 articles.

**Text.** `src/extract.py` flattens each article body to one string: inline
markup (italic, superscript, subscript) disappears so that
`<italic>t</italic>(23)` becomes `t(23)`, block elements and cross-reference
markers become spaces, table cells are separated by ` | `, MathML keeps its
characters, TeX duplicates and display formulas are dropped, and typographic
minus signs and spaces are mapped to ASCII. Only the `<body>` is read:
abstracts, reference lists, appendices and footnotes placed after the body
are not.

**Extraction and checking.** `src/statcheck_py.py` is an independent Python
re-implementation of the core of the `statcheck` method, written from the
published description, not ported from the R code. It reads only results of
the form *statistic(df) = value, p <=> value* for t, F, r, chi-square and z
(z has no df), with a comma or semicolon directly between the statistic and
`p`. A result is skipped if it cannot be checked: p above 1, |r| above 1,
degrees of freedom below 1, `p < .000`, a p-value continued by scientific
notation, a division or a range, or a `z =` that directly follows `y = ...`
(a brain coordinate). For each remaining result it computes the two-tailed
(t, r, z) or upper-tail (F, chi-square) p-value over the whole range of
statistics that round to the printed one, and calls the result

- *inconsistent* if no p in that range rounds to the reported p (for `p =`),
  or lies below it (for `p <`), or above it (for `p >`);
- a *decision inconsistency* if it is inconsistent and the reported p is on
  one side of .05 while the whole recomputed range is on the other
  (`p = .05` counts as significant; `p < .10` or `p > .01` cannot be placed
  and are never decision inconsistencies).

`p = .000` is read as "rounds to zero at three decimals" and is not
automatically wrong. As in `statcheck`, if the article body contains
"one-tailed", "one-sided" or "directional" anywhere, a t, r or z result that
would be consistent as a one-tailed test is not flagged. This is the primary
definition; results are also given with no allowance and with an allowance
that ignores the word "directional". `src/test_statcheck_py.py` holds 47
hand-computed cases.

**Analysis.** `src/analyze.py`. Shares with 95% percentile intervals from
2,000 bootstrap resamples of whole articles (seed 20261123); logistic
regression of the result-level flag on year, or on a 2026 indicator, with
standard errors clustered on article; an article-level logistic regression of
"any inconsistency" on year and log number of results.

**What was planned and what was not.** The extractor, the yearly table, the
trend model and the variants below (except the one marked post hoc) were
committed (`c7e1ecc`)
when only 2010-2016 had been downloaded and looked at. The only evidence of
that ordering in the repository is the commit history; the ID lists for all
years were committed just afterwards. The prior-art search was not finished
at that point, contrary to the repository's rule to search first: the
project README at that commit still had `novelty: unchecked`, and the 2017
paper closest to this work was found only in review afterwards. Everything else was added after the
full yearly table had been seen and is post hoc: the yearly table without the
one-tailed allowance (the corresponding trend variant was planned), the
half-year, received-quarter and received-month tables, the 2026 contrasts,
the use of 2010-2025 as the headline trend (the "excluding 2026" variant was
planned), its split by p form and the article-level model restricted to
2010-2025, the breakdowns by test type,
p form, receipt-to-publication interval, AI statement and country, the
exact-match diagnostic, and the extra hand-check stratum for July-November
2026. Several of these were suggested by reviewing agents (see Review log).

**Changes to the extractor after the first full run.** The hand-check and
reviews by separate agents found faults, all fixed before the numbers
reported here were produced: a p-value in scientific notation (`p =
1.00E-04`) was read as `p = 1.00`; a result whose p-value ended a sentence
(`p = .04.`) was dropped, which had excluded 8% of results; a footnote marker
could fuse with a p-value; `p < .000`, degrees of freedom below 1, a middle
dot in scientific notation, `.05/3`, a range such as `.01-.05` and brain
coordinates written `z = ...` were mishandled. The first committed results
(commit `568efa2`, 188,597 results) show the same pattern: 9.4% to 12.8% in
2010-2025 and 7.2% in 2026.

**Variants** (`results/variants.csv`; trend over all of 2010-2026, which the
2026 cohorts pull down):

| Variant | 2010-2013 | 2023-2026 | Odds ratio per year (95% interval) |
|---|---|---|---|
| Primary | 10.21% | 9.51% | 0.990 (0.981-0.998) |
| No one-tailed allowance | 11.04% | 9.97% | 0.987 (0.979-0.995) |
| `p = .000` counted as inconsistent | 10.54% | 10.54% | 0.996 (0.988-1.004) |
| Exactly reported p only | 16.31% | 15.18% | 0.994 (0.984-1.004) |
| Inequality p only | 4.85% | 2.89% | 0.955 (0.943-0.967) |
| `research-article` only | 10.19% | 9.24% | 0.988 (0.979-0.996) |
| t and F only | 9.97% | 9.25% | 0.988 (0.979-0.997) |
| One-tailed allowance without the word "directional" (post hoc) | 10.31% | 9.66% | 0.990 (0.982-0.998) |
| Excluding 2026 (the third column is then 2023-2025) | 10.21% | 10.70% | 1.002 (0.993-1.011) |

**Hand-check.** Before the fixes above, `src/sample_handcheck.py --redraw`
drew, per period (2010-2015, 2016-2021, 2022-2026), 20 flagged decision
inconsistencies, then 40 flagged results of any kind from those remaining,
and 10 unflagged results; plus (post hoc) 20 flagged and 20 unflagged from
July-November 2026: 250 items. The "flagged" stratum is therefore a
random sample of flagged results within each period, with equal numbers per
period although the periods differ greatly in size and with July-November
2026 over-represented, so pooled counts are unweighted; 24 of its 140 items
are themselves decision inconsistencies. Each item was read once, with 150 characters of
context either side, by the model that wrote the extractor, in the same
session; there was no separate prompt, and the only record is the label and
note per item. Labels: `inconsistent_as_printed`,
`explained_by_stated_correction`, `probably_one_tailed`, `extraction_error`,
`correctly_extracted`. Because the extraction has changed since the draw,
rerunning with `--redraw` gives a different sample, and 2 of the 250 items
(two of the three extraction errors) are no longer extracted.

| Stratum | Period | Inconsistent as printed | Stated correction | Probably one-tailed | Extraction error |
|---|---|---|---|---|---|
| Flagged | 2010-2015 | 39 | 1 | 0 | 0 |
| Flagged | 2016-2021 | 36 | 3 | 1 | 0 |
| Flagged | 2022-2026 | 38 | 0 | 2 | 0 |
| Flagged | Jul-Nov 2026 | 18 | 0 | 2 | 0 |
| Flagged decision | 2010-2015 | 17 | 0 | 3 | 0 |
| Flagged decision | 2016-2021 | 18 | 0 | 2 | 0 |
| Flagged decision | 2022-2026 | 13 | 1 | 3 | 3 |

"Inconsistent as printed" means that, read the way the extractor reads them,
the printed statistic, degrees of freedom and p-value do not agree, and the
reader did not judge the surrounding text to explain it. It does not say
which number is off or why. 61 of the 250 items also carry a note drawn from a
small set of fixed category sentences (13 distinct notes; they are
categories, not per-item commentary). Among the 179 items labelled
inconsistent as printed the notes mark: 15 that sit next to results that look
multiplicity-adjusted (10 in the flagged stratum, 5 in the decision stratum);
10 where the reported p is a floor value such as `p = .001` for a far smaller
p; 7 where the printed value may be a different quantity from the one its
letter suggests (Wilks' lambda or another multivariate statistic printed
after `F`, Mauchly's W after a chi-square symbol, a Kolmogorov-Smirnov or
publication-bias statistic after `z`), so that the article's numbers may all
be right and the flag is the extractor's misreading; and 7 with unusual
degrees of freedom (for example `F(1, 1)` or `t(2)`), one of them next to a
stated Greenhouse-Geisser correction. The notes were applied by judgement,
and a reviewing agent found three more items that deserved the last note
after the first count. Counting every item whose label or note points to something other
than a wrong number (stated corrections, probable one-tailed tests,
extraction errors, suspected adjustments, possibly different quantities,
unusual degrees of freedom), the totals are 25 of 140 flagged results (18%)
and 25 of 60 flagged decision inconsistencies (42%). A second reader
(a reviewing agent) recomputed all 250 items, confirmed every flag
arithmetically, and disagreed with the label or note on 4 items, which were
changed as it proposed; a later one proposed the 3 further notes mentioned
above.

No author was contacted about any item: the flags are automatic, a large
share have innocent explanations, and the project's subject is the rate, not
individual papers. The passages themselves are not committed because the
article text is CC BY and this repository is CC0; `src/sample_handcheck.py`
rebuilds them from the downloaded articles.

## Reproduction

Python 3.13 with the packages in `requirements.txt`. From the project folder:

```bash
python src/test_statcheck_py.py     # 47 hand-computed cases; prints "all tests passed"
python src/fetch_ids.py             # Europe PMC; about 12 minutes; rewrites data/ids/
python src/fetch_fulltext.py        # NCBI efetch; about 30 minutes; 1.4 GB into data/raw/xml/
python src/extract.py               # about 3 minutes on 4 cores; writes data/*.csv.gz
python src/analyze.py               # under a minute; writes results/
python src/sample_handcheck.py      # rebuilds the hand-check snippets in data/raw/
```

To reproduce the numbers above exactly, skip `fetch_ids.py` and use the
committed `data/ids/` (SHA-256 of the 17 files concatenated in name order:
`8bf3d80215ad17872a131145f3a6935790dc4b29ac4c7a1ad5b7dee918e977d3`). Rerunning
it later returns more 2026 articles. `data/articles.csv.gz` and
`data/results.csv.gz` are committed, so `analyze.py` runs without any
download; `extract.py` prints the SHA-256 of their uncompressed content,
which for the run reported here was

- articles.csv: `84ce8ea2b75d150b16f007a15bcbb0af9d8ab8871bd0deea5e9818ac7e15c0b8`
- results.csv: `f184c2e443726bd4bf7129b1fea7882b026980cc13f5fda4d8afe6ef637da181`

`results/analyze_stdout.txt` is the output of the run reported here.
`analyze.py` rewrites one file, `results/descriptives_from_text.txt`, only
when the downloaded text is present in `data/raw/`; everything else in
`results/` comes from the committed data (`results/handcheck.csv` is the
hand-made record and is an input). Network:
`www.ebi.ac.uk` and `eutils.ncbi.nlm.nih.gov`, no key. No checksum of the raw
XML is given: PMC can revise an article's XML after deposit, so a fresh
download may differ in a few results.

## External data and what we could not reproduce

- **Article full text**: *Frontiers in Psychology*, 2010 to early November
  2026, as deposited in PubMed Central and indexed by Europe PMC. IDs from the
  Europe PMC REST API (`https://www.ebi.ac.uk/europepmc/webservices/rest/search`),
  XML from NCBI E-utilities
  (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`, `db=pmc`).
  Accessed 2026-11-23. Articles are published under CC BY; the XML is not
  committed. What is committed is derived: PMCIDs, DOIs, article type, dates,
  the category of the generative-AI statement, the country of the first
  affiliation, and for each extracted result its parsed fields (test type,
  degrees of freedom, statistic, p-value as printed) with the computed flags.
  Only `results/handcheck.csv` holds verbatim strings: 250 extracted
  fragments such as `t(28) = 2.20, p = .03`, each identified by PMCID; they
  are short factual fragments of CC BY articles, attributed by that ID.
- The studies behind these articles were not run here and none of their
  statistics can be recomputed from data here. This project checks only
  whether three printed numbers agree with each other.
- Every claim in the Claims table rests on this source. If PMC's copy of an
  article differs from the publisher's version, the affected results are
  wrong in the same way.
- Known problems: (a) the deposit format changed in November 2025 (the
  publication date moved to a different tag); manuscripts received in 2026Q1
  and published under the new format are still at 9.5%, so the format change
  does not by itself produce the decline; (b) the most recent months are
  incomplete (165 articles for November 2026), and the 2026Q2 and 2026Q3
  receipt cohorts contain only manuscripts published quickly; (c) the
  generative-AI statement is self-declared and its wording changed during
  2025.
- Claim 15 rests on Nuijten et al. (2016, 2017) as published, and claim 12 on
  web pages of the publisher and a vendor, fetched and read on 2026-11-23;
  they are the companies' own descriptions.

A flag against a PMCID, whether in `results/handcheck.csv` or among the
roughly 22,000 automatically flagged results in `data/results.csv.gz`, says
only that a printed p-value and test statistic do not agree under the reading
described above. Most flags have not been looked at by anyone, and a
substantial share of those that were had innocent explanations. A flag is not
a statement about a study's conclusions or about its authors.

## Prior work and novelty

Searched on 2026-11-23: web search (eight queries) and OpenAlex (seven
queries) for `statcheck`, "statistical reporting inconsistencies",
"statistical reporting errors" combined with psychology, trend, over time,
prevalence, *Frontiers in Psychology*, PLOS ONE, 2015-2024, and
`JATSdecoder`; alternative names used in the literature and searched:
"p-value inconsistencies", "reporting errors", "gross inconsistencies",
"decision inconsistencies / decision errors". The first version of this
section missed the 2017 study's time comparison; a reviewing agent found it
by reading the full text. Two reviewing agents each repeated the search on
OpenAlex, Europe PMC and the web with their own terms and reported no further
series for this journal and no study of 2025-2026 articles. Full texts were opened where marked "read".

- Nuijten, Hartgerink, van Assen, Epskamp & Wicherts (2016), "The prevalence
  of statistical reporting errors in psychology (1985-2013)", *Behavior
  Research Methods*, doi:10.3758/s13428-015-0664-2 (read, PMC5101263). Eight
  journals including this one for 2010-2013. Table 1 row: "FP | General |
  2010-2013 | 2,139 | 702 | (32.8 %) | 10,149 | 10". Text: "PLoS showed the
  highest percentage of inconsistent p-values per article overall, followed
  by FP (14.0 % and 12.8 %, respectively)"; "In this manual download we did
  not include retractions, errata, and editorials"; "the current study counts
  p = .000 as incorrect"; and "The trends for PS, FP, and PLoS are hard to
  interpret given the limited number of years of covarage." This is the
  method and the baseline.
- Nuijten, Borghuis, Veldkamp, Dominguez-Alvarez, van Assen & Wicherts
  (2017), "Journal data sharing policies and statistical reporting
  inconsistencies in psychology", *Collabra: Psychology*,
  doi:10.1525/collabra.102 (read as the PsyArXiv preprint, osf.io/sgbta).
  Study 2 ran `statcheck` 1.0.2 on articles from this journal and PLOS
  ("we selected only the research articles, clinical (case) studies, and
  methods articles"), "published between March 8th 2010 and April 30th 2015",
  split by receipt before or after 1 March 2014 (1,819 and 873 articles from
  this journal). "The average percentage of inconsistencies within an article
  in FP increased over time from 13.1% to 16.2%"; gross inconsistencies "from
  1.7% to 2.0%". Its Figure 2 plots the rate per publication year. So a
  series for this journal to April 2015 exists, and it reports a rise where
  this project finds none: on a similar split this pipeline gives 11.9% and
  11.7% with one-tailed detection (which their procedure used) and `p = .000`
  counted wrong, or 13.0% and 12.5% without it (claim 14). In the first
  period this pipeline is about one point below theirs under matched
  settings, the same gap as against the 2016 study. In the second it is four
  to five points below, and that difference is unexplained. What can be said: this pipeline finds somewhat
  more articles in both periods (2,078 against 1,819, and 1,032 against 873)
  but far more results in the second (8,564 from 616 articles, against their
  2,432 from 304; in the first period 19,622 against 11,079). The two
  extractors therefore diverge much more for 2014-2015 than for 2010-2013.
  A documented candidate reason is that `statcheck`'s HTML reader
  under-extracts from this journal's markup: see Böschen (2021) below. Running the R package on the same articles
  would settle it and was not done (R was not available in the session).
- Nuijten & Wicherts (2024), "Implementing statcheck during peer review is
  related to a steep decline in statistical-reporting inconsistencies",
  *AMPPS*, doi:10.1177/25152459241258945 (abstract only). Four other
  journals, before and after two of them adopted `statcheck`: "the decrease
  in both inconsistencies and decision inconsistencies around p = .05 is
  considerably steeper in statcheck journals than in control journals". This
  is direct precedent for a journal-side check lowering the rate.
- Etemady & Roettger (2025), "Statistical reporting inconsistencies in
  experimental linguistics", *Glossa Psycholinguistics*,
  doi:10.5070/g6011.47896 (abstract only). Thirteen linguistics journals,
  2000-2023, 82,991 tests; rates "seem stable over publication years".
- Böschen (2021), "Evaluation of JATSdecoder as an automated text extraction
  tool for statistical results in scientific reports", *Scientific Reports*,
  doi:10.1038/s41598-021-98782-3 (read, PMC8484375), and Böschen (2023),
  "Changes in methodological study characteristics in psychology between
  2010-2021", *PLOS ONE*, doi:10.1371/journal.pone.0283353 (read in the copy
  bound into the author's dissertation; it is also open access). Both process
  this journal's XML with a different extractor, the first as downloaded at
  the start of 2021, the second for 2010-2021. The yearly tables in the
  second cover alpha levels, confidence intervals, multiple-testing
  corrections, one-tailed tests and sample sizes; no yearly p-value
  inconsistency rate was found in either. The first gives an external check
  on how much there is to extract: in 18,744 XML files of this journal
  (Tables 3 and 4), `statcheck`'s `checkHTML()` on the XML found 37,555
  checkable results in 4,465 articles (24%), while `statcheck()` on text
  cleaned by JATSdecoder found 98,842 in 7,734 articles (41%). This pipeline
  finds 116,696 results in 8,803 of the 20,194 articles with `PUB_YEAR`
  2010-2020 (44%; `results/descriptives.txt`), a somewhat larger corpus.
- Böschen (2024), arXiv:2408.07948 (abstract only), argues `statcheck`'s
  strict pattern misses many results; Nuijten (2025), "Statcheck does what it
  is designed to do: a reply to Böschen (2024)", doi:10.31234/osf.io/xyfjz
  (title only), replies. The criticism applies equally to the extractor here.
- Hartgerink (2016), "688,112 statistical results: content mining psychology
  articles for statistical test results", *Data*, doi:10.3390/data1030014
  (title only): a `statcheck` dataset from other publishers; whether it
  includes this journal was not checked.
- Colombo, Duev, Nuijten & Sprenger (2018), "Statistical reporting
  inconsistencies in experimental philosophy", *PLOS ONE*,
  doi:10.1371/journal.pone.0194360 (title only): the same method in another
  field.
- Dunleavy (2025 preprint), "Trends in the distribution, reporting and
  consistency of p-values in four social work journals: A cross-sectional
  meta-research study", doi:10.71240/lcyc.001439 (abstract only). It "uses
  the metacheck r package to examine difference and trends in social work
  research across four leading journals ... for the years 2005, 2015, and
  2025", including "the internal consistency of exact p-value reporting". So
  one study that includes 2025 articles exists, in another field and with
  another tool; its results were not read.
- A 2026 registered-report protocol, "Including the tool statcheck in peer
  review to increase analytical reproducibility: a randomized experiment in
  two psychology journals", doi:10.31222/osf.io/gs4ft_v1 (abstract only),
  plans a trial of the intervention; no results yet.

Not found in this search: an inconsistency rate for this journal for any
period after April 2015, or any study of articles from 2026 in any journal
(for 2025, only the Dunleavy preprint above).
Several of the closest papers were read only as abstracts, and preprints from
2026 may not be indexed yet.

Conclusion of the search: go ahead as an extension. `novelty:
partially-known`. The method, the 2010-2013 level and a 2010-April 2015
comparison are known. The series from mid-2015 to 2025 for this journal and
the 2026 decline by date of receipt were not found elsewhere.

## Limitations and open questions

- **One journal.** Nothing here says what happened in psychology at large.
  This journal grew from 142 to several thousand articles a year and its mix
  of topics, article types and author populations changed; the flat line to
  2025 is the net of all that. Country was looked at only for the 2026
  decline, and only as the first affiliation.
- **Only strictly formatted results are read.** 67% of articles yield no
  extracted result, and that share rose (51% to 58% in each year 2010-2019,
  73% to 77% in 2022-2025). A result with an effect size between the
  statistic and `p`, one written with `p ≤`, one split across table cells,
  and anything else not written as *statistic(df) = value, p ...* is
  invisible. If careful and careless authors differ in how they format
  results, the extracted set is not representative, and a change in
  formatting habits over time could move the rate without any change in
  accuracy.
- **A flag is not an error in the study.** See the hand-check: 18% of flagged
  results and 42% of flagged decision inconsistencies had a known, probable
  or suspected explanation other than a wrong number, and more may have one
  outside the 150 characters read (corrections described in a Methods
  section, for example). The hand-check was a single quick pass by the model
  that wrote the extractor, on short snippets; a second agent rechecked it
  but no person has. Of flagged `p =` results, 31% miss by no more than one
  further unit in the last printed digit and 11.5% would agree if the p-value
  had been truncated instead of rounded.
- **Known sources of false flags that remain.** Any `z =` or `Z =` is read as
  a standard normal statistic. z results have a 15.1% flag rate against about
  10% for t and F (primary definition; 16.6% without the allowance); statistics of other kinds printed with that letter are one
  cause, but a small one where it can be counted
  (`results/descriptives_from_text.txt`: 63 z results have
  "Kolmogorov", "Shapiro" or "normality" within 150 characters, 25 of them
  flagged, out of 2,435 z results flagged without the allowance), so most of
  the excess is
  unexplained. Correlations written `r(df)` have a 17.0% flag rate. 270 F
  results have a first degree of freedom larger than the second and 74% of
  them are flagged; 86 t results have fewer than 3 degrees of freedom and 80%
  are flagged; in both groups the parentheses often hold something else.
  Sphericity-corrected F tests printed with uncorrected degrees of freedom,
  and multiplicity-adjusted p-values, are flagged. Not handled and not
  counted: a p-value followed by a space and a stray digit, `p = .05 level`,
  and a one-decimal `p = .0`.
- **The one-tailed keyword rule is crude and its input drifted.** The share
  of articles containing one of the three trigger words rose from 12-15% in
  2023-2024 to 36% in the second half of 2026
  (`results/half_years_2023_2026.csv`), and almost all of the rise is
  the word "directional" (which also matches "bidirectional" and
  "directionality"); "one-tailed" or "one-sided" stayed at 2-3% of articles.
  That makes the primary definition more forgiving in 2026. The results are
  nearly the same with no allowance and with an allowance that ignores
  "directional", so this is not what produces the 2026 finding.
- **The 2026 finding is post hoc and rests on incomplete cohorts.** It was
  not a hypothesis; it was seen in the table and then examined, and the
  receipt-date view and the checks in claims 6, 8 and 9 were suggested by
  reviewing agents. Manuscripts received
  in 2026Q2 and Q3 and still in review are missing. Before 2026 fast and slow
  manuscripts had the same rate, and fast manuscripts alone show the same
  decline (claim 6), but manuscripts still in review could differ: in the
  April-May 2026 cohort the slower manuscripts published so far have a
  higher rate than the fast ones, in the June cohort a lower one. It
  needs another year of data and other journals.
- **The cause of the 2026 decline is unknown** (claims 11 and 12). Things
  that changed around the same time and could be related or coincidental:
  articles got longer (median body 43-44 thousand characters in 2023-2025, 51
  thousand in 2026), results per article fell, p-values printed with exactly
  three decimals rose from 73-78% of results in 2023-2025 to 87% in 2026,
  monthly article counts rose, and the share of authors declaring AI use and
  the share based in China both rose. Nothing here measures the use of any
  tool by authors or by the journal, and the publisher's pages that were read
  (claim 12) do not describe a statistical check. The word "statcheck" was not searched for in the articles.
- **Not `statcheck` itself.** The extractor is a re-implementation and was
  not run side by side with the R package. On 2010-2013 it extracts 42% more
  results from 41% more articles than Nuijten et al. (2016) report, and its
  per-article rate under their settings is 11.8% against their 12.8% (12.9%
  with no one-tailed allowance). It accepts semicolons and capital `Z` and
  reads chi-square inside MathML, which probably accounts for some of the
  extra results, but that was not verified; Böschen (2021) reports that
  `statcheck` reading this journal's XML directly finds far fewer results
  than it does on cleaned text (see Prior work), and the volume extracted
  here is close to the latter. For manuscripts received from
  March 2014 it extracts 3.5 times as many results as Nuijten et al. (2017)
  and does not reproduce the rise they report (see Prior work).
- **Decision inconsistencies are rare events.** Yearly counts in 2010-2025
  are between 9 and 363; year-to-year movements are mostly noise.
- **No proof is involved**, so nothing here is a candidate for formalization.

## Review log

| Date | Reviewer (model / human) | Scope | Outcome |
|------|--------------------------|-------|---------|
| 2026-11-23 | Quality-control agent 1 (claude-fable-5-2; started by the author with the repository path and a brief to find faults, without the author's notes or conclusions). This is the author's own quality control, not the independent review the standards require. | Reran tests, extraction and analysis; recomputed all 250 hand-check items; re-searched prior work. | Reproduced the numbers. Found a missed prior paper (Nuijten et al. 2017), an extractor fault that dropped 8% of results, smaller extractor faults, mislabelled hand-check strata, overstatements, and that the 2026 fall is sharper by date of manuscript receipt. All addressed. |
| 2026-11-23 | Quality-control agent 2 (same model and terms, fresh context) | As above on the revised project; recomputed all results independently; lag-matched cohorts, country, AI-statement share, exact-match diagnostic; publisher pages. | Reproduced every file byte for byte. Nothing blocking. Found one wrong number (three-decimal share), numbers with no generating command, "step" overstating a ramp that begins in mid-2025, an unsupported explanation of the mismatch with Nuijten et al. (2017), four hand-check labels or notes, untested extractor edge cases. All addressed in this version. Status stays `result`. |
| 2026-11-23 | Quality-control agent 3 (same model and terms, fresh context) | As above on the second revision; read the publisher pages; half-month receipt series; within-form trends; receipt-period rates by test type. | Reproduced every file byte for byte and all 205,835 flags. Found a wrong date and unread sources in claim 12, a hand-check table row that disagreed with its data, "steeply from April 2026" overstating an ambiguous April-May, opposite within-form trends hidden in the pooled 2010-2025 rate, a benchmark compared under unmatched settings, a "not found" statement contradicted by a cited preprint, and smaller inconsistencies. All addressed in this version. Status stays `result`. |
| 2026-11-24 | Quality-control agent 4 (same model and terms, fresh context) | As above on the third revision; placebo breakpoints for the mid-2025 contrast; extraction inside and outside tables; all sources re-fetched. | Reproduced every file byte for byte and all flags; no blocking defect and no wrong headline number. Found two stale sentences contradicting claim 12, an imprecise interval in claim 12, an article-level trend missing from the summary and not marked post hoc, three hand-check items missing a note, a sentence mixing two definitions, an unused external benchmark in a cited paper, and wording imprecisions. All addressed in this version. Status stays `result`. |
| 2026-11-24 | Quality-control agent 5 (same model and terms, fresh context) | As above on the fourth revision; adjusted and placebo versions of the cohort contrasts; all sources re-fetched and compared. | Reproduced every file byte for byte and all flags; no blocking defect and no wrong headline number. Found one stale interval in claim 4, a sentence saying every hand-check item has a note, an incomplete description of the July 2025 announcement, "the same size" overstating the AI-statement comparison, and lag evidence within the 2026 cohorts that was not reported. All addressed in this version. Status stays `result`. |
