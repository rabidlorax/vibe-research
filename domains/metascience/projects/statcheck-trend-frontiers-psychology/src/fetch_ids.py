#!/usr/bin/env python3
"""List every Frontiers in Psychology article with open-access full text in
Europe PMC, by publication year, and write data/ids/<year>.txt (one PMCID per
line, sorted).

Usage: python src/fetch_ids.py [first_year last_year]
Network: www.ebi.ac.uk (Europe PMC REST search). No key needed.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "vibe-research-statcheck/0.1 (research script; no personal data)"
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OUT = Path(__file__).resolve().parent.parent / "data" / "ids"


def query(year):
    return f'JOURNAL:"Front Psychol" AND PUB_YEAR:{year} AND OPEN_ACCESS:y AND IN_EPMC:y'


def get(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except Exception as e:  # network errors are retried with backoff
            print(f"  retry {i + 1}: {e}", file=sys.stderr)
            time.sleep(5 * (i + 1))
    raise SystemExit(f"failed: {url}")


def year_ids(year):
    ids, cursor, hits = set(), "*", None
    while True:
        params = urllib.parse.urlencode({
            "query": query(year), "format": "json", "pageSize": 1000,
            "resultType": "idlist", "cursorMark": cursor})
        d = get(f"{BASE}?{params}")
        hits = d["hitCount"]
        res = d.get("resultList", {}).get("result", [])
        ids.update(r["pmcid"] for r in res if r.get("pmcid"))
        nxt = d.get("nextCursorMark")
        if not res or not nxt or nxt == cursor:
            break
        cursor = nxt
        time.sleep(0.3)
    return hits, sorted(ids, key=lambda s: int(s[3:]))


def main():
    y0, y1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (2010, 2026)
    OUT.mkdir(parents=True, exist_ok=True)
    for y in range(y0, y1 + 1):
        hits, ids = year_ids(y)
        (OUT / f"{y}.txt").write_text("\n".join(ids) + "\n")
        print(f"{y}: hitCount={hits} pmcids={len(ids)}", flush=True)


if __name__ == "__main__":
    main()
