rho_sun used: 1.4098 g/cm^3
published rows tested: 9261; references (short name + bibcode) with >= 5 rows: 140

References where >= 80% of rows match M*/R*^3 in SOLAR units within 10% and <= 20% match in g/cm^3:

                                         ref  rows  planets  hosts  median_ratio_if_cgs  median_ratio_if_solar  pct_within10_if_cgs  pct_within10_if_solar
Fulton & Petigura 2018 [2018AJ....156..264F]  1414     1405    838               0.7163                 1.0099                  0.1                   93.4
    Torres et al. 2017 [2017AJ....154..264T]    22       22     16               0.7025                 0.9904                  0.0                   81.8
      Mann et al. 2017 [2017AJ....153..267M]    13       13      7               0.7092                 0.9998                  0.0                  100.0
 MacDonald et al. 2016 [2016AJ....152..105M]    11        6      1               0.7056                 0.9948                  0.0                  100.0

Affected ps rows: 1460 (1435 planets, 856 host stars); of these, default_flag=1 rows: 16

Remaining published rows (KOI-table and TICv8 stars excluded): 3045.
Rows with st_dens within 3% of M*/R*^3 in solar units (r_cgs = 0.7093): 43 rows, 41 planets, 33 hosts.
Control windows of the same width: r_cgs = 0.6500: 5 rows; r_cgs = 0.7600: 9 rows; r_cgs = 1.4098: 10 rows
References with >= 2 rows, all of them in the solar-unit window (rows / hosts), none read:
H&eacute;brard et al. 2014 [2014A&A...572A..93H] (4/4); Psaridi et al. 2023 [2023A&A...675A..39P] (3/3); Almenara et al. 2025 [2025A&A...703A.167A] (3/1); Van Eylen et al. 2021 [2021MNRAS.507.2154V] (3/1); Esposito et al. 2017 [2017A&A...601A..53E] (2/2); Schlieder et al. 2016 [2016ApJ...818...87S] (2/2); Azevedo Silva et al. 2022 [2022A&A...657A..68A] (2/1); Hord et al. 2022 [2022AJ....164...13H] (2/1); Orosz et al. 2012 [2012Sci...337.1511O] (2/1); Tey et al. 2023 [2023AJ....165...93T] (2/1)

pscomppars download sha256 52641b302c83851aa6732947be3de370ce02619770da99308ba1dadc0a77c828
Composite table (pscomppars): 6473 planets, 5859 with a stellar density; 1067 (18.2% of those, 16.5% of all) take it from an affected reference:
ref
Fulton & Petigura 2018 [2018AJ....156..264F]    1049
Torres et al. 2017 [2017AJ....154..264T]           8
Mann et al. 2017 [2017AJ....153..267M]             5
MacDonald et al. 2016 [2016AJ....152..105M]        5

For those composite rows, st_dens / (M*/R*^3 in solar units) has median 0.998 (composite mass and radius may come from other references).
