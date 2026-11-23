Input: ps.csv, sha256 f7f15dabf8bbae042698ab40c2f5188f9d20b08f79974348f7f2b679da1f2e0d, 40428 rows, 6473 planets.

| check | stratum | n | median_abs_pct | pct_gt1pct | pct_gt5pct | pct_gt20pct | n_gt20pct | n_gt2x | n_with_errors | n_gt3sigma_and_gt5pct | pct_gt3sigma_and_gt5pct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K3 | published, same ref | 7132 | 0.063 | 13.59 | 5.59 | 1.29 | 92 | 5 | 6205 | 58 | 0.93 |
| K3 | published, mixed refs | 356 | 0.509 | 38.76 | 6.18 | 0.28 | 1 | 1 | 315 | 2 | 0.63 |
| K3 | kepler-koi | 13124 | 0.088 | 1.23 | 0.0 | 0.0 | 0 | 0 | 0 | 0 | 0.0 |
| LOGG | published | 12691 | 0.233 | 31.03 | 13.58 | 6.07 | 770 | 90 | 9668 | 56 | 0.58 |
| LOGG | kepler-koi | 15671 | 0.088 | 5.6 | 0.08 | 0.0 | 0 | 0 | 13707 | 0 | 0.0 |
| RHOS | published | 9261 | 0.042 | 30.89 | 23.99 | 21.25 | 1968 | 252 | 6441 | 994 | 15.43 |
| RHOS | kepler-koi | 13363 | 56.294 | 80.18 | 77.21 | 67.48 | 9018 | 5076 | 11440 | 703 | 6.15 |
| LUM | published | 7209 | 0.001 | 14.15 | 4.51 | 1.15 | 83 | 24 | 4141 | 14 | 0.34 |
| LUM | kepler-koi | 2547 | 0.001 | 0.0 | 0.0 | 0.0 | 0 | 0 | 642 | 0 | 0.0 |
| RHOP | published | 2524 | 0.633 | 40.57 | 21.55 | 3.01 | 76 | 16 | 2501 | 6 | 0.24 |
| URAD | published | 13203 | 0.0 | 0.82 | 0.05 | 0.0 | 0 | 0 | 0 | 0 | 0.0 |
| URAD | kepler-koi | 13124 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0 | 0.0 |
| URAD | tess-exofop | 1563 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0 | 0.0 |
| UMASS | published | 4839 | 0.0 | 3.06 | 0.25 | 0.04 | 2 | 0 | 0 | 0 | 0.0 |
| UMSINI | published | 2760 | 0.001 | 1.12 | 0.11 | 0.0 | 0 | 0 | 0 | 0 | 0.0 |
| RATROR | published, same ref | 7470 | 0.233 | 25.41 | 3.24 | 0.28 | 21 | 2 | 6951 | 10 | 0.14 |
| RATROR | published, mixed refs | 236 | 0.059 | 16.1 | 7.2 | 2.12 | 5 | 4 | 224 | 6 | 2.68 |
| RATROR | kepler-koi | 13124 | 0.154 | 2.67 | 0.05 | 0.0 | 0 | 0 | 13062 | 0 | 0.0 |
| RATDOR | published, same ref | 2143 | 0.192 | 25.24 | 12.65 | 3.92 | 84 | 6 | 2092 | 22 | 1.05 |
| RATDOR | published, mixed refs | 33 | 0.277 | 36.36 | 9.09 | 0.0 | 0 | 0 | 30 | 0 | 0.0 |
| RATDOR | kepler-koi | 13124 | 24.563 | 97.12 | 86.91 | 56.39 | 7401 | 1562 | 0 | 0 | 0.0 |
| DEPTH | published | 1225 | 5.089 | 57.63 | 50.12 | 12.73 | 156 | 15 | 914 | 82 | 8.97 |
| DEPTH | kepler-koi | 13124 | 18.511 | 98.32 | 90.25 | 37.97 | 4983 | 121 | 10813 | 2927 | 27.07 |
| INSOL | published, same ref | 766 | 0.494 | 35.9 | 13.71 | 3.13 | 24 | 9 | 743 | 11 | 1.48 |
| INSOL | published, mixed refs | 9 | 0.448 | 11.11 | 11.11 | 0.0 | 0 | 0 | 9 | 0 | 0.0 |

Outlier rows (published, |d| > 20%): 3276 rows, 2595 planets, {'DEPTH': 156, 'INSOL': 24, 'K3': 92, 'LOGG': 770, 'LUM': 83, 'RATDOR': 84, 'RATROR': 21, 'RHOP': 76, 'RHOS': 1968, 'UMASS': 2}

Factor-of-2 outliers by check and reference (top 5 references per check):

- DEPTH: 15 rows; Kruse et al. 2019 (4); Guenther et al. 2026 (1); Wang et al. 2018 (1); Morello et al. 2014 (1); Ikwut-Ukwa et al. 2020 (1)
- INSOL: 9 rows; Lockley et al. 2025 (3); Barkaoui et al. 2025 (2); Sgro et al. 2024 (1); Mann et al. 2022 (1); Psaridi et al. 2022 (1)
- K3: 5 rows; Stassun et al. 2017 (2); Yang et al. 2025 (1); Ca&ntilde;as et al. 2023 (1); Everett et al. 2015 (1)
- LOGG: 90 rows; Stassun et al. 2017 (7); Fabrycky et al. 2012 (5); Steffen et al. 2012 (4); Hartogh et al. 2026 (4); Moutou et al. 2015 (3)
- LUM: 24 rows; West et al. 2009 (3); Moutou et al. 2011 (3); Lockley et al. 2025 (3); Barkaoui et al. 2025 (2); Niedzielski et al. 2009 (2)
- RATDOR: 6 rows; Livingston et al. 2018 (2); Montet et al. 2015 (1); Schwamb et al. 2013 (1); Kostov et al. 2014 (1); Schlieder et al. 2016 (1)
- RATROR: 2 rows; Guenther et al. 2026 (1); Beard et al. 2022 (1)
- RHOP: 16 rows; Hobson et al. 2026 (6); Yee et al. 2022 (2); Esteves et al. 2015 (2); Yahalomi et al. 2024 (1); G&uuml;nther et al. 2018 (1)
- RHOS: 252 rows; Q1-Q17 DR25 KOI Table (213); Livingston et al. 2018 (17); Soto et al. 2018 (5); Crouzet et al. 2017 (4); Dawson et al. 2014 (2)

References with >= 5 published rows whose median obs/pred is off by more than 10%:

| check | reference | rows | median ratio | q25 | q75 |
|---|---|---|---|---|---|
| DEPTH | Vanderburg et al. 2016 | 107 | 1.1789 | 1.1116 | 1.2231 |
| DEPTH | Torres et al. 2017 | 22 | 1.1446 | 0.9607 | 1.1668 |
| DEPTH | Libralato et al. 2016 | 7 | 1.1427 | 1.0354 | 1.1968 |
| DEPTH | Lissauer et al. 2013 | 6 | 1.1993 | 1.1728 | 1.2042 |
| DEPTH | Borucki et al. 2013 | 5 | 1.1904 | 1.1806 | 1.2166 |
| DEPTH | Lissauer et al. 2012 | 5 | 1.16 | 1.1548 | 1.1674 |
| INSOL | Guenther et al. 2026 | 5 | 0.8139 | 0.8054 | 0.8452 |
| K3 | Oddo et al. 2023 | 9 | 1.2025 | 1.0561 | 1.3989 |
| K3 | del Ser et al. 2023 | 6 | 0.8992 | 0.7867 | 0.9847 |
| K3 | Pel&aacute;ez-Torres et al. 2024 | 5 | 1.2238 | 1.1103 | 1.2761 |
| K3 | Quintana et al. 2014 | 5 | 0.9068 | 0.9044 | 0.9068 |
| LOGG | Johnson et al. 2011 | 21 | 1.1522 | 0.993 | 1.3746 |
| LOGG | Jenkins et al. 2025 | 15 | 0.8458 | 0.7193 | 1.05 |
| LOGG | Fabrycky et al. 2012 | 13 | 1.9577 | 0.771 | 2.2278 |
| LOGG | Johnson et al. 2010 | 11 | 1.7357 | 1.2771 | 1.8309 |
| LOGG | Lubin et al. 2022 | 11 | 0.7938 | 0.7938 | 0.7938 |
| LOGG | Demangeon et al. 2021 | 10 | 0.8852 | 0.6488 | 0.8885 |
| LOGG | Anderson et al. 2017 | 9 | 0.6407 | 0.5261 | 0.7281 |
| LOGG | Marmier et al. 2013 | 9 | 1.2671 | 0.8748 | 1.5185 |
| LOGG | Leleu et al. 2021 | 8 | 0.6702 | 0.6702 | 0.7422 |
| LOGG | Naef et al. 2010 | 8 | 1.1279 | 1.0212 | 1.3812 |
| LOGG | Steffen et al. 2012 | 8 | 0.7615 | 0.5752 | 1.4196 |
| LOGG | Barros et al. 2016 | 7 | 1.1339 | 1.1339 | 1.1544 |
| LOGG | Frensch et al. 2023 | 7 | 0.854 | 0.8222 | 1.1592 |
| LOGG | Jones et al. 2015 | 7 | 1.1076 | 0.9519 | 1.1076 |
| LOGG | Meschiari et al. 2011 | 7 | 1.987 | 0.9112 | 2.0177 |
| LOGG | Moutou et al. 2015 | 7 | 0.6588 | 0.1532 | 0.7652 |
| LOGG | Moutou et al. 2026 | 7 | 0.6885 | 0.6885 | 0.7248 |
| LOGG | Sato et al. 2008 | 7 | 0.8385 | 0.6079 | 0.9662 |
| LOGG | David et al. 2018 | 6 | 1.2976 | 1.0654 | 1.2976 |
| LOGG | Donati et al. 2023 | 6 | 1.3533 | 1.3533 | 1.3533 |
| LOGG | Leleu et al. 2024 | 6 | 0.6962 | 0.6962 | 0.6962 |
| LOGG | Lubin et al. 2024 | 6 | 0.7938 | 0.7938 | 0.7938 |
| LOGG | Moutou et al. 2011 | 6 | 1.1663 | 0.5345 | 1.2479 |
| LOGG | Moutou et al. 2014 | 6 | 1.1495 | 1.0157 | 1.4059 |
| LOGG | Triaud et al. 2010 | 6 | 1.3307 | 1.0759 | 1.4174 |
| LOGG | Vogt et al. 2015 | 6 | 0.8812 | 0.8812 | 0.8812 |
| LOGG | Badenas-Agusti et al. 2020 | 5 | 0.8892 | 0.8892 | 0.8892 |
| LOGG | Bonfanti et al. 2026 | 5 | 0.8832 | 0.8832 | 0.8832 |
| LOGG | Christiansen et al. 2018 | 5 | 1.1284 | 1.1284 | 1.1284 |
| LOGG | Fischer et al. 2007 | 5 | 1.2194 | 1.0302 | 1.2465 |
| LOGG | Gonz&aacute;lez Hern&aacute;ndez et al. 2024 | 5 | 0.612 | 0.612 | 0.612 |
| LOGG | Lillo-Box et al. 2026 | 5 | 1.1542 | 1.0044 | 1.1586 |
| LOGG | Motalebi et al. 2015 | 5 | 1.2072 | 1.2072 | 1.2072 |
| LOGG | Moutou et al. 2009 | 5 | 0.8445 | 0.4843 | 1.3077 |
| LOGG | Niraula et al. 2017 | 5 | 1.1755 | 1.1755 | 1.1755 |
| LOGG | Nowak et al. 2020 | 5 | 0.9066 | 0.9066 | 0.9066 |
| LOGG | Peterson et al. 2023 | 5 | 1.1326 | 1.1326 | 1.1326 |
| LOGG | Petigura et al. 2020 | 5 | 0.9017 | 0.9017 | 0.9017 |
| LOGG | Sato et al. 2013 | 5 | 0.8834 | 0.6509 | 0.8834 |
| LOGG | Schwarz et al. 2026 | 5 | 0.8982 | 0.8982 | 0.8982 |
| LUM | Liu et al. 2014 | 8 | 1.1104 | 0.9863 | 1.1603 |
| LUM | Moutou et al. 2011 | 6 | 0.7098 | 0.4908 | 1.0414 |
| LUM | West et al. 2009 | 6 | 1.9522 | 0.9981 | 3.8184 |
| LUM | Gillon et al. 2013 | 5 | 1.1086 | 0.9828 | 1.1086 |
| LUM | Gonz&aacute;lez Hern&aacute;ndez et al. 2024 | 5 | 1.1049 | 1.1049 | 1.1049 |
| LUM | Moutou et al. 2014 | 5 | 0.8185 | 0.8185 | 1.0398 |
| RATDOR | Sinukoff et al. 2016 | 26 | 0.8738 | 0.7538 | 0.9875 |
| RATROR | Hedges et al. 2019 | 7 | 0.7543 | 0.6497 | 0.8175 |
| RHOP | Borsato et al. 2021 | 7 | 0.8415 | 0.6724 | 1.1014 |
| RHOS | Fulton & Petigura 2018 | 1414 | 0.7163 | 0.6996 | 0.7297 |
| RHOS | Q1-Q17 DR25 KOI Table | 370 | 1.1424 | 0.438 | 2.3339 |
| RHOS | Livingston et al. 2018 | 59 | 1.1483 | 0.8258 | 1.4865 |
| RHOS | Torres et al. 2017 | 22 | 0.7025 | 0.7017 | 0.707 |
| RHOS | Mann et al. 2017 | 19 | 0.7099 | 0.7084 | 0.9942 |
| RHOS | MacDonald et al. 2016 | 11 | 0.7056 | 0.7056 | 0.7056 |
| RHOS | Borsato et al. 2021 | 7 | 0.9046 | 0.8033 | 1.0004 |
| RHOS | Almenara et al. 2025 | 6 | 0.8474 | 0.7074 | 1.0151 |
| RHOS | Brahm et al. 2020 | 6 | 0.8573 | 0.7173 | 1.0246 |
| RHOS | Tsantaki et al. 2014 | 6 | 0.7305 | 0.6517 | 1.0029 |
| RHOS | Hedges et al. 2021 | 5 | 0.8292 | 0.8292 | 0.8292 |
| RHOS | Soto et al. 2018 | 5 | 0.2334 | 0.1857 | 0.2334 |
