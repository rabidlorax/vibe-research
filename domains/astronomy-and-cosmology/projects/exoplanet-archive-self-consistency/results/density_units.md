rho_sun used: 1.4098 g/cm^3
published rows tested: 9261; references with >= 5 rows: 151

References where >= 80% of rows match M*/R*^3 in SOLAR units within 10% and <= 20% match in g/cm^3:

                   ref  rows  planets  median_ratio_if_cgs  median_ratio_if_solar  pct_within10_if_cgs  pct_within10_if_solar
Fulton & Petigura 2018  1414     1405               0.7163                 1.0099                  0.1                   93.4
    Torres et al. 2017    22       22               0.7025                 0.9904                  0.0                   81.8
 MacDonald et al. 2016    11        6               0.7056                 0.9948                  0.0                  100.0

Affected ps rows: 1447 (1423 planets, 850 host stars); of these, default_flag=1 rows: 14

Other published rows (KOI-table stars excluded) with st_dens within 3% of M*/R*^3 in solar units: 56 rows, 54 planets; control window (same width, opposite side): 56 rows.
By reference (rows matching / rows tested): Mann et al. 2017 (13/19); H&eacute;brard et al. 2014 (4/4); Van Eylen et al. 2021 (3/3); Psaridi et al. 2023 (3/3); Almenara et al. 2025 (3/6); Brahm et al. 2020 (3/6); Orosz et al. 2012 (3/3); Esposito et al. 2017 (2/2)

Composite table (pscomppars): 5859 planets have a stellar density; 1062 (18.1%) take it from an affected reference:
ref
Fulton & Petigura 2018    1049
Torres et al. 2017           8
MacDonald et al. 2016        5

For those composite rows, st_dens / (M*/R*^3 in solar units) has median 0.995 (composite mass and radius may come from other references).
