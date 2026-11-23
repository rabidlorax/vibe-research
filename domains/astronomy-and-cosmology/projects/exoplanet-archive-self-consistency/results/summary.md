Input: ps.csv, sha256 f7f15dabf8bbae042698ab40c2f5188f9d20b08f79974348f7f2b679da1f2e0d, 40428 rows, 6473 planets.

| check | stratum | n | median_abs_pct | pct_gt1pct | pct_gt5pct | pct_gt20pct | n_gt20pct | n_gt2x | n_with_errors | n_gt3sigma_and_gt5pct | pct_gt3sigma_and_gt5pct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K3 | published, same ref | 7132 | 0.063 | 13.59 | 5.59 | 1.29 | 92 | 5 | 6205 | 58 | 0.93 |
| K3 | published, mixed refs | 356 | 0.509 | 38.76 | 6.18 | 0.28 | 1 | 1 | 315 | 2 | 0.63 |
| K3 | kepler-koi | 13124 | 0.088 | 1.23 | 0.0 | 0.0 | 0 | 0 | 0 | n/a | n/a |
| LOGG | published | 12691 | 0.233 | 31.03 | 13.58 | 6.07 | 770 | 90 | 9668 | 56 | 0.58 |
| LOGG | published, literature star ref | 7935 | 0.979 | 49.29 | 21.73 | 9.7 | 770 | 90 | 7713 | 56 | 0.73 |
| LOGG | kepler-koi | 15671 | 0.088 | 5.6 | 0.08 | 0.0 | 0 | 0 | 13707 | 0 | 0.0 |
| LOGG | kepler-koi, KOI-table star ref | 13124 | 0.118 | 6.68 | 0.09 | 0.0 | 0 | 0 | 13065 | 0 | 0.0 |
| LOGG | kepler-koi, TICv8 star ref | 2547 | 0.001 | 0.0 | 0.0 | 0.0 | 0 | 0 | 642 | 0 | 0.0 |
| RHOS | published | 9261 | 0.042 | 30.89 | 23.99 | 21.25 | 1968 | 252 | 6441 | 994 | 15.43 |
| RHOS | published, literature star ref | 3045 | 0.554 | 33.89 | 13.37 | 6.27 | 191 | 37 | 3039 | 57 | 1.88 |
| RHOS | kepler-koi | 13363 | 56.294 | 80.18 | 77.21 | 67.48 | 9018 | 5076 | 11440 | 703 | 6.15 |
| RHOS | kepler-koi, KOI-table star ref | 10816 | 88.83 | 99.07 | 95.4 | 83.38 | 9018 | 5076 | 10798 | 703 | 6.51 |
| RHOS | kepler-koi, TICv8 star ref | 2547 | 0.003 | 0.0 | 0.0 | 0.0 | 0 | 0 | 642 | 0 | 0.0 |
| LUM | published | 7209 | 0.001 | 14.15 | 4.51 | 1.15 | 83 | 24 | 4141 | 14 | 0.34 |
| LUM | published, literature star ref | 2827 | 0.591 | 36.08 | 11.5 | 2.94 | 83 | 24 | 2560 | 14 | 0.55 |
| LUM | kepler-koi | 2547 | 0.001 | 0.0 | 0.0 | 0.0 | 0 | 0 | 642 | 0 | 0.0 |
| LUM | kepler-koi, TICv8 star ref | 2547 | 0.001 | 0.0 | 0.0 | 0.0 | 0 | 0 | 642 | 0 | 0.0 |
| RHOP | published | 2524 | 0.633 | 40.57 | 21.55 | 3.01 | 76 | 16 | 2501 | 6 | 0.24 |
| URAD | published | 13203 | 0.0 | 0.82 | 0.05 | 0.0 | 0 | 0 | 0 | n/a | n/a |
| URAD | kepler-koi | 13124 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | n/a | n/a |
| URAD | tess-exofop | 1563 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | n/a | n/a |
| UMASS | published | 4839 | 0.0 | 3.06 | 0.25 | 0.04 | 2 | 0 | 0 | n/a | n/a |
| UMSINI | published | 2760 | 0.001 | 1.12 | 0.11 | 0.0 | 0 | 0 | 0 | n/a | n/a |
| RATROR | published, same ref | 7470 | 0.233 | 25.41 | 3.24 | 0.28 | 21 | 2 | 6951 | 10 | 0.14 |
| RATROR | published, mixed refs | 236 | 0.059 | 16.1 | 7.2 | 2.12 | 5 | 4 | 224 | 6 | 2.68 |
| RATROR | kepler-koi | 13124 | 0.154 | 2.67 | 0.05 | 0.0 | 0 | 0 | 13062 | 0 | 0.0 |
| RATDOR | published, same ref | 2143 | 0.192 | 25.24 | 12.65 | 3.92 | 84 | 6 | 2092 | 22 | 1.05 |
| RATDOR | published, mixed refs | 33 | 0.277 | 36.36 | 9.09 | 0.0 | 0 | 0 | 30 | 0 | 0.0 |
| RATDOR | kepler-koi | 13124 | 24.563 | 97.12 | 86.91 | 56.39 | 7401 | 1562 | 0 | n/a | n/a |
| DEPTH | published | 1225 | 5.089 | 57.63 | 50.12 | 12.73 | 156 | 15 | 914 | 82 | 8.97 |
| DEPTH | kepler-koi | 13124 | 18.511 | 98.32 | 90.25 | 37.97 | 4983 | 121 | 10813 | 2927 | 27.07 |
| INSOL | published, same ref | 766 | 0.494 | 35.9 | 13.71 | 3.13 | 24 | 9 | 743 | 11 | 1.48 |
| INSOL | published, mixed refs | 9 | 0.448 | 11.11 | 11.11 | 0.0 | 0 | 0 | 9 | 0 | 0.0 |

Two references contributing most rows off by > 5%, per stratum (count of the stratum's > 5% rows / that reference's rows in the stratum):

- K3, published, same ref: Stassun et al. 2017 [2017AJ....153..136S] (118 of 399 / 204); Castro-González et al. 2022 [2022MNRAS.509.1075C] (13 of 399 / 22)
- K3, published, mixed refs: Butler et al. 2006 [2006ApJ...646..505B] (5 of 22 / 19); Wright et al. 2009 [2009ApJ...693.1084W] (4 of 22 / 26)
- LOGG, published: Mayo et al. 2018 [2018AJ....155..136M] (148 of 1724 / 167); Stassun et al. 2017 [2017AJ....153..136S] (122 of 1724 / 355)
- LOGG, published, literature star ref: Mayo et al. 2018 [2018AJ....155..136M] (148 of 1724 / 167); Stassun et al. 2017 [2017AJ....153..136S] (122 of 1724 / 355)
- LOGG, kepler-koi: Q1-Q8 KOI Table (12 of 12 / 2308)
- LOGG, kepler-koi, KOI-table star ref: Q1-Q8 KOI Table (12 of 12 / 2308)
- RHOS, published: Fulton & Petigura 2018 [2018AJ....156..264F] (1414 of 2222 / 1414); Q1-Q17 DR25 KOI Table (355 of 2222 / 370)
- RHOS, published, literature star ref: Livingston et al. 2018 [2018AJ....156..277L] (54 of 407 / 56); Marcy et al. 2014 [2014ApJS..210...20M] (20 of 407 / 49)
- RHOS, kepler-koi: Q1-Q16 KOI Table (2596 of 10318 / 2720); Q1-Q17 DR25 KOI Table (2587 of 10318 / 2718)
- RHOS, kepler-koi, KOI-table star ref: Q1-Q16 KOI Table (2596 of 10318 / 2720); Q1-Q17 DR25 KOI Table (2587 of 10318 / 2718)
- LUM, published: Naef et al. 2010 [2010A&A...523A..15N] (7 of 325 / 7); Marmier et al. 2013 [2013A&A...551A..90M] (6 of 325 / 8)
- LUM, published, literature star ref: Naef et al. 2010 [2010A&A...523A..15N] (7 of 325 / 7); Marmier et al. 2013 [2013A&A...551A..90M] (6 of 325 / 8)
- RHOP, published: Howard et al. 2025 [2025ApJS..278...52H] (39 of 544 / 63); Hadden & Lithwick 2017 [2017AJ....154....5H] (32 of 544 / 49)
- URAD, published: Yu et al. 2018 [2018AJ....156...22Y] (3 of 6 / 18); Kruse et al. 2019 [2019ApJS..244...11K] (2 of 6 / 300)
- UMASS, published: Marois et al. 2008 [2008Sci...322.1348M] (3 of 12 / 3); Hadden et al. 2014 [2014ApJ...787...80H] (2 of 12 / 139)
- UMSINI, published: Anglada-Escude et al. 2013 [2013A&A...556A.126A] (2 of 3 / 5); Lin et al. 2024 [2024AJ....168...27L] (1 of 3 / 7)
- RATROR, published, same ref: Vanderburg et al. 2016 [2016ApJS..222...14V] (90 of 242 / 107); Morton et al. 2016 [2016ApJ...822...86M] (56 of 242 / 2239)
- RATROR, published, mixed refs: Morton et al. 2016 [2016ApJ...822...86M] (10 of 17 / 15); Dressing et al. 2017 [2017AJ....154..207D] (2 of 17 / 4)
- RATROR, kepler-koi: Q1-Q8 KOI Table (5 of 7 / 2308); Q1-Q12 KOI Table (1 of 7 / 2678)
- RATDOR, published, same ref: Livingston et al. 2018 [2018AJ....156..277L] (65 of 271 / 79); Livingston et al. 2018 [2018AJ....156...78L] (33 of 271 / 45)
- RATDOR, published, mixed refs: Greklek-McKeon et al. 2025 [2025AJ....170...65G] (1 of 3 / 1); Dressing et al. 2017 [2017AJ....154..207D] (1 of 3 / 1)
- RATDOR, kepler-koi: Q1-Q16 KOI Table (2361 of 11406 / 2720); Q1-Q17 DR24 KOI Table (2348 of 11406 / 2700)
- DEPTH, published: Kruse et al. 2019 [2019ApJS..244...11K] (265 of 614 / 301); Vanderburg et al. 2016 [2016ApJS..222...14V] (103 of 614 / 107)
- DEPTH, kepler-koi: Q1-Q16 KOI Table (2540 of 11845 / 2720); Q1-Q17 DR24 KOI Table (2521 of 11845 / 2700)
- INSOL, published, same ref: Torres et al. 2017 [2017AJ....154..264T] (9 of 105 / 22); Guenther et al. 2026 [2026AJ....172...54G] (5 of 105 / 5)
- INSOL, published, mixed refs: Dressing et al. 2017 [2017AJ....154..207D] (1 of 1 / 1)

Stellar-parameter references of the 'published' stellar strata (top 4 by rows):

- LOGG: TICv8 [2019AJ....158..138S] (4386); Morton et al. 2016 [2016ApJ...822...86M] (2242); Q1-Q17 DR25 KOI Table (370); Stassun et al. 2017 [2017AJ....153..136S] (355)
- RHOS: TICv8 [2019AJ....158..138S] (4386); Fulton & Petigura 2018 [2018AJ....156..264F] (1414); Q1-Q17 DR25 KOI Table (370); Stassun et al. 2017 [2017AJ....153..136S] (151)
- LUM: TICv8 [2019AJ....158..138S] (4382); MacDougall et al. 2023 [2023AJ....166...33M] (112); Mann et al. 2013 [2013ApJ...779..188M] (85); Ment et al. 2018 [2018AJ....156..213M] (54)

K3, published, same ref, by discovery method (rows / off by > 5% / off by > 20%): Transit 4730 / 222 / 58; Radial Velocity 2298 / 165 / 29; Imaging 40 / 5 / 3; Transit Timing Variations 27 / 0 / 0; Microlensing 19 / 6 / 2; Astrometry 7 / 1 / 0; Pulsar Timing 6 / 0 / 0; Orbital Brightness Modulation 4 / 0 / 0; Pulsation Timing Variations 1 / 0 / 0

RHOP, published: rows with ratio 1.055-1.085 (Jupiter mean-radius density convention, factor 1.0694): 277; mirror window: 31; off by > 5% outside that window: 267 of 2247 (11.9%); median pl_dens / (M/R^3 in Jupiter units) in the window: 1.328 g/cm^3 (equatorial-radius Jupiter density 1.240, mean-radius 1.326)

Published rows with TICv8 stellar parameters (rows / rows off by > 5%): LOGG 4386 / 0; RHOS 4386 / 0; LUM 4382 / 0
Short reference names in st_refname (published rows) standing for more than one bibcode: 247

Outlier entries (published, |d| > 20%): 3276 row-identity entries, 3100 distinct rows, 2595 planets, {'DEPTH': 156, 'INSOL': 24, 'K3': 92, 'LOGG': 770, 'LUM': 83, 'RATDOR': 84, 'RATROR': 21, 'RHOP': 76, 'RHOS': 1968, 'UMASS': 2}
Of these entries: 1453 RHOS solar-unit references, 324 RHOS KOI-table stars, 156 DEPTH (approximate identity), 2 UMASS (rounding); remaining 1341 entries, 1192 distinct rows, 941 planets.

Factor-of-2 outliers by check and reference (top 5 references per check):

- DEPTH: 15 rows; Kruse et al. 2019 [2019ApJS..244...11K] (4); Guenther et al. 2026 [2026AJ....172...54G] (1); Wang et al. 2018 [2018PASP..130f4401W] (1); Morello et al. 2014 [2014ApJ...786...22M] (1); Ikwut-Ukwa et al. 2020 [2020AJ....160..209I] (1)
- INSOL: 9 rows; Lockley et al. 2025 [2025MNRAS.541..919L] (3); Barkaoui et al. 2025 [2025A&A...695A.281B] (2); Sgro et al. 2024 [2024AJ....168...26S] (1); Mann et al. 2022 [2022AJ....163..156M] (1); Psaridi et al. 2022 [2022A&A...664A..94P] (1)
- K3: 5 rows; Stassun et al. 2017 [2017AJ....153..136S] (2); Yang et al. 2025 [2025ApJ...986..117Y] (1); Cañas et al. 2023 [2023ApJS..265...50C] (1); Everett et al. 2015 [2015AJ....149...55E] (1)
- LOGG: 90 rows; Stassun et al. 2017 [2017AJ....153..136S] (7); Fabrycky et al. 2012 [2012ApJ...750..114F] (5); Steffen et al. 2012 [2012MNRAS.421.2342S] (4); Hartogh et al. 2026 [2026A&A...707A..93H] (4); Moutou et al. 2015 [2015A&A...576A..48M] (3)
- LUM: 24 rows; West et al. 2009 [2009A&A...502..395W] (3); Moutou et al. 2011 [2011A&A...527A..63M] (3); Lockley et al. 2025 [2025MNRAS.541..919L] (3); Barkaoui et al. 2025 [2025A&A...695A.281B] (2); Niedzielski et al. 2009 [2009ApJ...707..768N] (2)
- RATDOR: 6 rows; Livingston et al. 2018 [2018AJ....156..277L] (2); Montet et al. 2015 [2015ApJ...809...25M] (1); Schwamb et al. 2013 [2013ApJ...768..127S] (1); Kostov et al. 2014 [2014ApJ...784...14K] (1); Schlieder et al. 2016 [2016ApJ...818...87S] (1)
- RATROR: 2 rows; Guenther et al. 2026 [2026AJ....172...54G] (1); Beard et al. 2022 [2022ApJ...936...55B] (1)
- RHOP: 16 rows; Hobson et al. 2026 [2026A&A...711A.198H] (6); Yee et al. 2022 [2022AJ....164...70Y] (2); Esteves et al. 2015 [2015ApJ...804..150E] (2); Yahalomi et al. 2024 [2024MNRAS.527..620Y] (1); Günther et al. 2018 [2018MNRAS.478.4720G] (1)
- RHOS: 252 rows; Q1-Q17 DR25 KOI Table (213); Livingston et al. 2018 [2018AJ....156..277L] (17); Soto et al. 2018 [2018MNRAS.478.5356S] (5); Crouzet et al. 2017 [2017AJ....153...94C] (4); Dawson et al. 2014 [2014ApJ...791...89D] (2)

References with >= 5 published rows whose median obs/pred is off by more than 10%:

| check | reference | rows | median ratio | q25 | q75 |
|---|---|---|---|---|---|
| DEPTH | Vanderburg et al. 2016 [2016ApJS..222...14V] | 107 | 1.1789 | 1.1116 | 1.2231 |
| DEPTH | Torres et al. 2017 [2017AJ....154..264T] | 22 | 1.1446 | 0.9607 | 1.1668 |
| DEPTH | Heidari et al. 2026 [2026arXiv261008584H] | 9 | 1.1074 | 1.0396 | 1.1336 |
| DEPTH | Libralato et al. 2016 [2016MNRAS.463.1780L] | 7 | 1.1427 | 1.0354 | 1.1968 |
| DEPTH | Lissauer et al. 2013 [2013ApJ...770..131L] | 6 | 1.1993 | 1.1728 | 1.2042 |
| DEPTH | Borucki et al. 2013 [2013Sci...340..587B] | 5 | 1.1904 | 1.1806 | 1.2166 |
| DEPTH | Lissauer et al. 2012 [2012ApJ...750..112L] | 5 | 1.16 | 1.1548 | 1.1674 |
| INSOL | Guenther et al. 2026 [2026AJ....172...54G] | 5 | 0.8139 | 0.8054 | 0.8452 |
| K3 | Oddo et al. 2023 [2023AJ....165..134O] | 9 | 1.2025 | 1.0561 | 1.3989 |
| K3 | del Ser et al. 2023 [2023MNRAS.518..669D] | 6 | 0.8992 | 0.7867 | 0.9847 |
| K3 | Peláez-Torres et al. 2024 [2024A&A...690A..62P] | 5 | 1.2238 | 1.1103 | 1.2761 |
| K3 | Quintana et al. 2014 [2014Sci...344..277Q] | 5 | 0.9068 | 0.9044 | 0.9068 |
| LOGG | Johnson et al. 2011 [2011ApJS..197...26J] | 18 | 1.1805 | 1.0068 | 1.5458 |
| LOGG | Jenkins et al. 2025 [2025A&A...704A.283J] | 15 | 0.8458 | 0.7193 | 1.05 |
| LOGG | Fabrycky et al. 2012 [2012ApJ...750..114F] | 13 | 1.9577 | 0.771 | 2.2278 |
| LOGG | Lubin et al. 2022 [2022AJ....163..101L] | 11 | 0.7938 | 0.7938 | 0.7938 |
| LOGG | Anderson et al. 2017 [2017A&A...604A.110A] | 9 | 0.6407 | 0.5261 | 0.7281 |
| LOGG | Marmier et al. 2013 [2013A&A...551A..90M] | 9 | 1.2671 | 0.8748 | 1.5185 |
| LOGG | Naef et al. 2010 [2010A&A...523A..15N] | 8 | 1.1279 | 1.0212 | 1.3812 |
| LOGG | Steffen et al. 2012 [2012MNRAS.421.2342S] | 8 | 0.7615 | 0.5752 | 1.4196 |
| LOGG | Barros et al. 2016 [2016A&A...593A.113B] | 7 | 1.1339 | 1.1339 | 1.1544 |
| LOGG | Frensch et al. 2023 [2023A&A...675A.173F] | 7 | 0.854 | 0.8222 | 1.1592 |
| LOGG | Johnson et al. 2010 [2010PASP..122..701J] | 7 | 1.2788 | 1.2687 | 1.5544 |
| LOGG | Meschiari et al. 2011 [2011ApJ...727..117M] | 7 | 1.987 | 0.9112 | 2.0177 |
| LOGG | Moutou et al. 2015 [2015A&A...576A..48M] | 7 | 0.6588 | 0.1532 | 0.7652 |
| LOGG | Moutou et al. 2026 [2026A&A...705A.190M] | 7 | 0.6885 | 0.6885 | 0.7248 |
| LOGG | Demangeon et al. 2021 [2021A&A...653A..78D] | 6 | 0.6553 | 0.5923 | 0.8229 |
| LOGG | Donati et al. 2023 [2023MNRAS.525..455D] | 6 | 1.3533 | 1.3533 | 1.3533 |
| LOGG | Leleu et al. 2021 [2021A&A...649A..26L] | 6 | 0.6702 | 0.6702 | 0.6702 |
| LOGG | Leleu et al. 2024 [2024A&A...688A.211L] | 6 | 0.6962 | 0.6962 | 0.6962 |
| LOGG | Lubin et al. 2024 [2024AJ....168..196L] | 6 | 0.7938 | 0.7938 | 0.7938 |
| LOGG | Moutou et al. 2011 [2011A&A...527A..63M] | 6 | 1.1663 | 0.5345 | 1.2479 |
| LOGG | Triaud et al. 2010 [2010A&A...524A..25T] | 6 | 1.3307 | 1.0759 | 1.4174 |
| LOGG | Vogt et al. 2015 [2015ApJ...814...12V] | 6 | 0.8812 | 0.8812 | 0.8812 |
| LOGG | Badenas-Agusti et al. 2020 [2020AJ....160..113B] | 5 | 0.8892 | 0.8892 | 0.8892 |
| LOGG | Bonfanti et al. 2026 [2026A&A...709A.265B] | 5 | 0.8832 | 0.8832 | 0.8832 |
| LOGG | Burt et al. 2021 [2021AJ....161...10B] | 5 | 1.1238 | 0.8907 | 1.1571 |
| LOGG | Christiansen et al. 2018 [2018AJ....155...57C] | 5 | 1.1284 | 1.1284 | 1.1284 |
| LOGG | Fischer et al. 2007 [2007ApJ...669.1336F] | 5 | 1.2194 | 1.0302 | 1.2465 |
| LOGG | González Hernández et al. 2024 [2024A&A...690A..79G] | 5 | 0.612 | 0.612 | 0.612 |
| LOGG | Lillo-Box et al. 2026 [2026arXiv260719756L] | 5 | 1.1542 | 1.0044 | 1.1586 |
| LOGG | Motalebi et al. 2015 [2015A&A...584A..72M] | 5 | 1.2072 | 1.2072 | 1.2072 |
| LOGG | Moutou et al. 2009 [2009A&A...496..513M] | 5 | 0.8445 | 0.4843 | 1.3077 |
| LOGG | Moutou et al. 2014 [2014A&A...563A..22M] | 5 | 1.3008 | 1.0157 | 1.4428 |
| LOGG | Niraula et al. 2017 [2017AJ....154..266N] | 5 | 1.1755 | 1.1755 | 1.1755 |
| LOGG | Peterson et al. 2023 [2023Natur.617..701P] | 5 | 1.1326 | 1.1326 | 1.1326 |
| LOGG | Petigura et al. 2020 [2020AJ....159....2P] | 5 | 0.9017 | 0.9017 | 0.9017 |
| LOGG | Schwarz et al. 2026 [2026AN....34770059S] | 5 | 0.8982 | 0.8982 | 0.8982 |
| LUM | Liu et al. 2014 [2014RAA....14.1447L] | 8 | 1.1104 | 0.9863 | 1.1603 |
| LUM | Moutou et al. 2011 [2011A&A...527A..63M] | 6 | 0.7098 | 0.4908 | 1.0414 |
| LUM | Gillon et al. 2013 [2013A&A...552A..82G] | 5 | 1.1086 | 0.9828 | 1.1086 |
| LUM | González Hernández et al. 2024 [2024A&A...690A..79G] | 5 | 1.1049 | 1.1049 | 1.1049 |
| LUM | Moutou et al. 2014 [2014A&A...563A..22M] | 5 | 0.8185 | 0.8185 | 1.0398 |
| RATDOR | Sinukoff et al. 2016 [2016ApJ...827...78S] | 26 | 0.8738 | 0.7538 | 0.9875 |
| RATROR | Hedges et al. 2019 [2019ApJ...880L...5H] | 7 | 0.7543 | 0.6497 | 0.8175 |
| RHOP | Borsato et al. 2021 [2021MNRAS.506.3810B] | 7 | 0.8415 | 0.6724 | 1.1014 |
| RHOS | Fulton & Petigura 2018 [2018AJ....156..264F] | 1414 | 0.7163 | 0.6996 | 0.7297 |
| RHOS | Q1-Q17 DR25 KOI Table | 370 | 1.1424 | 0.438 | 2.3339 |
| RHOS | Livingston et al. 2018 [2018AJ....156..277L] | 56 | 1.1946 | 0.8186 | 1.5327 |
| RHOS | Torres et al. 2017 [2017AJ....154..264T] | 22 | 0.7025 | 0.7017 | 0.707 |
| RHOS | Mann et al. 2017 [2017AJ....153..267M] | 13 | 0.7092 | 0.7075 | 0.7099 |
| RHOS | MacDonald et al. 2016 [2016AJ....152..105M] | 11 | 0.7056 | 0.7056 | 0.7056 |
| RHOS | Borsato et al. 2021 [2021MNRAS.506.3810B] | 7 | 0.9046 | 0.8033 | 1.0004 |
| RHOS | Brahm et al. 2020 [2020AJ....160..235B] | 6 | 0.8573 | 0.7173 | 1.0246 |
| RHOS | Tsantaki et al. 2014 [2014A&A...570A..80T] | 6 | 0.7305 | 0.6517 | 1.0029 |
| RHOS | Hedges et al. 2021 [2021AJ....162...54H] | 5 | 0.8292 | 0.8292 | 0.8292 |
| RHOS | Soto et al. 2018 [2018MNRAS.478.5356S] | 5 | 0.2334 | 0.1857 | 0.2334 |
