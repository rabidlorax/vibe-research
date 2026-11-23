#!/bin/sh
# Fetch B. A. Seidler's catalogues of monotone 4- and 5-variable circuits (not
# redistributed here; no licence is stated on the source page).
# Accessed 2026-11-23. sha256 of the files as fetched that day are in
# data/catalogue.sha256.
set -e
cd "$(dirname "$0")"
mkdir -p raw
for n in 4 5; do
  curl -sS -A "research-script/1.0" -o raw/MonoCatFileA${n}var.txt \
    https://sites.math.rutgers.edu/~bas312/Research/slp/MonoCatFileA${n}var.txt
done
sha256sum -c catalogue.sha256
