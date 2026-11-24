#!/usr/bin/env python3
"""Download JATS full-text XML for every PMCID in data/ids/<year>.txt from
NCBI E-utilities (efetch, db=pmc), 100 articles per request, into
data/raw/xml/<year>_<batch>.xml.gz. Existing files are skipped.

Usage: python src/fetch_fulltext.py
Network: eutils.ncbi.nlm.nih.gov. No key needed; at most one request a second.
data/raw/ is not committed (third-party text, CC BY).
"""
import gzip
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "vibe-research-statcheck/0.1 (research script; no personal data)"
URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ROOT = Path(__file__).resolve().parent.parent
IDS, RAW = ROOT / "data" / "ids", ROOT / "data" / "raw" / "xml"
BATCH = 100


def fetch(ids, tries=6):
    body = urllib.parse.urlencode({
        "db": "pmc", "id": ",".join(i[3:] for i in ids),
        "tool": "vibe-research-statcheck"}).encode()
    for i in range(tries):
        try:
            req = urllib.request.Request(URL, data=body, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            if b"</pmc-articleset>" in data[-200:]:
                return data
            raise IOError("truncated response")
        except Exception as e:  # retried with backoff
            print(f"  retry {i + 1}: {e}", file=sys.stderr, flush=True)
            time.sleep(10 * (i + 1))
    raise SystemExit("giving up")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for f in sorted(IDS.glob("*.txt")):
        ids = f.read_text().split()
        for b in range(0, len(ids), BATCH):
            out = RAW / f"{f.stem}_{b // BATCH:03d}.xml.gz"
            if out.exists():
                continue
            data = fetch(ids[b:b + BATCH])
            tmp = out.with_suffix(".tmp")
            with gzip.open(tmp, "wb", compresslevel=6) as g:
                g.write(data)
            tmp.rename(out)
            time.sleep(1.0)
        print(f"{f.stem}: {len(ids)} ids done", flush=True)


if __name__ == "__main__":
    main()
