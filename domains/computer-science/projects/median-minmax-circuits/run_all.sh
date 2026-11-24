#!/bin/sh
# Regenerates every file in results/. Run from the project folder.
# Needs: pip install -r requirements.txt ; network only for the catalogue fetch.
# Rough runtimes on 4 cores of an Intel Xeon @ 2.10GHz are given per step.
set -e
./data/fetch_catalogue.sh                                   # seconds, network
cd src
python baseline.py                                          # <1 s
python verify.py ../results/baseline_median5.txt ../results/baseline_median7.txt ../results/baseline_median9.txt   # ~10 s
python lower_bounds.py 3 4  > ../results/lower_bounds_3.log
python lower_bounds.py 5 10 > ../results/lower_bounds_5.log                    # ~10 s
python lower_bounds.py 5 10 glucose4 > ../results/lower_bounds_5_glucose4.log  # ~20 s
python search.py 5 10 --out ../results/median5_10.txt       # ~4 s
python verify.py ../results/median5_10.txt
(for s in 1 2 3 4 5 6 7 8; do python search.py 5 $s --sym 0 | head -1; done) > ../results/median5_nosym_sizes1to8.log   # ~30 s
python search.py 5 9 --sym 0 > ../results/median5_size9_nosym.log   # ~18 min
python catalogue_check.py ../data/raw/MonoCatFileA4var.txt ../results/catalogue_check_4var.csv 4    # seconds
python catalogue_check.py ../data/raw/MonoCatFileA5var.txt ../results/catalogue_check.csv 4 > ../results/catalogue_check.log   # ~40 min
python nosym_check.py ../data/raw/MonoCatFileA4var.txt ../results/catalogue_check_4var.csv ../results/nosym_check_4var.log 4   # seconds
python nosym_check.py ../data/raw/MonoCatFileA5var.txt ../results/catalogue_check.csv ../results/nosym_check.log 4             # ~1 hour
python brute_force.py 4 7 > ../results/brute_force_n4_d7.txt    # ~1 min, ~3 GB of memory
python brute_force.py 5 5 > ../results/brute_force_n5_d5.txt    # ~10 s
python cross_check.py > ../results/cross_check.log
python lower_bounds.py 7 11 > ../results/lower_bounds_7.log     # ~70 s
python lower_bounds.py 9 13 > ../results/lower_bounds_9.log     # ~20 min, almost all in size 13
python local_improve.py ../results/baseline_median7.txt 11 60 11 3000000 > ../results/local7_keep11.log   # ~27 min
