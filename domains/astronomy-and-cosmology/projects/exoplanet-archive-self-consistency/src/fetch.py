#!/usr/bin/env python3
"""Download the columns used by the audit from the NASA Exoplanet Archive
Planetary Systems (ps) table via its TAP service.

Writes data/raw/ps.csv (not committed) and data/ps.sha256 + data/fetch_meta.json.
The archive is updated continuously, so a later download will differ; the
checksum identifies the snapshot the committed results were computed from.
"""
import datetime
import hashlib
import json
import pathlib
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent.parent
VALS = ["pl_orbper", "pl_orbsmax", "pl_orbeccen", "pl_orbincl", "pl_rade",
        "pl_radj", "pl_masse", "pl_massj", "pl_msinie", "pl_msinij",
        "pl_bmasse", "pl_bmassj", "pl_dens", "pl_ratror", "pl_ratdor",
        "pl_trandep", "pl_imppar", "pl_insol", "pl_eqt", "st_teff", "st_rad",
        "st_mass", "st_lum", "st_logg", "st_dens"]
META = ["pl_name", "hostname", "default_flag", "soltype", "pl_refname",
        "st_refname", "pl_bmassprov", "cb_flag", "sy_snum", "discoverymethod",
        "pl_controv_flag", "pl_pubdate", "rowupdate", "releasedate"]
cols = META + [c + s for c in VALS for s in ("", "err1", "err2", "lim")]
QUERY = "select " + ",".join(cols) + " from ps"
URL = ("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="
       + urllib.parse.quote(QUERY) + "&format=csv")


def main():
    req = urllib.request.Request(
        URL, headers={"User-Agent": "vibe-research-consistency-audit/0.1 (research script)"})
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(req, timeout=600).read()
            break
        except Exception as e:  # network hiccup: retry with backoff
            print("retry", attempt, e)
            time.sleep(5 * 2 ** attempt)
    else:
        raise SystemExit("download failed")
    raw = HERE / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "ps.csv").write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    (HERE / "data" / "ps.sha256").write_text(digest + "  ps.csv\n")
    (HERE / "data" / "fetch_meta.json").write_text(json.dumps({
        "accessed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "query": QUERY, "url": URL, "bytes": len(data),
        "rows": data.count(b"\n") - 1, "sha256": digest}, indent=1) + "\n")
    print(len(data), "bytes", data.count(b"\n") - 1, "rows", digest)


if __name__ == "__main__":
    main()
