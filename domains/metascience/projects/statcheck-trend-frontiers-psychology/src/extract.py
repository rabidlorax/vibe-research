#!/usr/bin/env python3
"""Read the downloaded JATS XML in data/raw/xml/, pull the body text of every
article, run the statcheck-style extractor on it, and write

  data/articles.csv.gz       one row per article
  data/results.csv.gz        one row per extracted test result (no article text)
  data/raw/contexts.csv.gz   the same results with their position and 150 characters of context
                             either side (CC BY article text; not committed)

Usage: python src/extract.py        (about 3 minutes on 4 cores)
"""
import csv
import gzip
import hashlib
import io
import re
import sys
from multiprocessing import Pool
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from statcheck_py import ONE_TAIL, ONE_TAIL_STRICT, extract, normalize  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "xml"
MML = "{http://www.w3.org/1998/Math/MathML}"
INLINE = {"italic", "bold", "sub", "sup", "sc", "underline", "monospace", "roman", "sans-serif",
          "styled-content", "named-content", "ext-link", "uri", "inline-formula",
          "alternatives", "email", "overline", "strike"}
DROP = {"tex-math", "graphic", "inline-graphic", "media", "object-id"}
CELL = {"td", "th"}

ART_COLS = ["pmcid", "doi", "year", "epub_year", "epub_month", "received_year", "received_month",
            "new_date_markup", "article_type", "section", "ai_statement", "country", "has_body", "body_chars",
            "one_tail_text", "one_tail_strict", "n_results"]
FLAGS = ["error", "decision_error", "error_1t", "decision_error_1t", "error_1t_strict",
         "decision_error_1t_strict", "half_p_consistent", "p_zero"]
RES_COLS = ["pmcid", "year", "kind", "df1", "df2", "stat", "p_cmp", "p_rep", "p_min", "p_max"] + FLAGS
AI_USED = re.compile(r"Gen(erative)? AI was used", re.I)
AI_NOT = re.compile(r"Gen(erative)? AI was not used|no Gen(erative)? AI was used", re.I)


def ai_statement(article):
    """'' if the article has no generative-AI statement section, else what it declares."""
    sec = article.find(".//sec[@sec-type='ai-statement']")
    if sec is None:
        return ""
    text = " ".join("".join(sec.itertext()).split())
    if AI_NOT.search(text):
        return "not_used"
    return "used" if AI_USED.search(text) else "other"


COUNTRY = {"usa": "United States", "united states of america": "United States", "u.s.a.": "United States",
           "us": "United States", "uk": "United Kingdom", "people's republic of china": "China",
           "pr china": "China", "p.r. china": "China", "turkey": "Türkiye", "the netherlands": "Netherlands"}


def first_country(meta):
    """Country of the first affiliation: the last comma-separated part of its <country> element."""
    c = meta.find(".//aff//country")
    if c is None or not "".join(c.itertext()).strip():
        return ""
    name = "".join(c.itertext()).split(",")[-1].strip().rstrip(".")
    return COUNTRY.get(name.lower().replace("\u2019", "'"), name)


class HashingGzip:
    """Text writer to a gzip file with no timestamp in the header (so the file is
    byte-reproducible) that also keeps a SHA-256 of the uncompressed content."""

    def __init__(self, path):
        self.raw = open(path, "wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.text = io.TextIOWrapper(self.gz, encoding="utf-8", newline="")
        self.sha = hashlib.sha256()

    def write(self, s):
        self.sha.update(s.encode("utf-8"))
        return self.text.write(s)

    def close(self):
        self.text.close()
        self.raw.close()
        return self.sha.hexdigest()


def flatten(el, out):
    """Serialize an element to text: inline markup vanishes, block markup
    becomes a space, table cells are separated by ' | ', TeX duplicates and
    display formulas are dropped, MathML keeps its characters. Cross-references
    (xref) count as block markup, so a footnote marker cannot fuse with a number
    before it ("p = 0.01" + marker "3" must not become "p = 0.013")."""
    tag = el.tag
    if not isinstance(tag, str):  # comment / processing instruction
        out.append(el.tail or "")
        return
    if tag in DROP or tag == "disp-formula":
        out.append(" " + (el.tail or ""))
        return
    if tag.startswith(MML):
        if tag == MML + "math":
            out.append("".join(el.itertext()))
        out.append(el.tail or "") if tag == MML + "math" else None
        return
    inline = tag in INLINE
    if not inline:
        out.append(" | " if tag in CELL else " ")
    out.append(el.text or "")
    for child in el:
        flatten(child, out)
    if not inline:
        out.append(" ")
    out.append(el.tail or "")


def first(el, path):
    r = el.find(path)
    return (r.text or "").strip() if r is not None else ""


def process(path):
    year = path.name.split("_")[0]
    root = etree.fromstring(gzip.open(path).read())
    arts, ress, ctxs = [], [], []
    for a in root.findall("article"):
        meta = a.find("front/article-meta")
        ids = {e.get("pub-id-type"): (e.text or "").strip() for e in meta.findall("article-id")}
        pmcid = ids.get("pmcid") or ("PMC" + ids.get("pmcaid", ""))
        subjects = [s.text or "" for s in meta.findall(".//article-categories//subject")]
        epub = meta.find("pub-date[@pub-type='epub']")  # JATS as deposited up to 2025
        if epub is None:  # newer deposits use date-type / publication-format instead
            epub = meta.find("pub-date[@date-type='pub']")
        ey, em = (first(epub, "year"), first(epub, "month")) if epub is not None else ("", "")
        new_format = int(meta.find("pub-date[@pub-type='epub']") is None)
        rec = meta.find("history/date[@date-type='received']")
        ry, rm = (first(rec, "year"), first(rec, "month")) if rec is not None else ("", "")
        body = a.find("body")
        text = ""
        if body is not None:
            out = []
            saved_tail, body.tail = body.tail, None
            flatten(body, out)
            body.tail = saved_tail
            text = normalize("".join(out))
        found = sorted(extract(text), key=lambda r: r["start"])
        for r in found:
            row = {"pmcid": pmcid, "year": year, **r}
            row["p_min"], row["p_max"] = f"{r['p_min']:.6g}", f"{r['p_max']:.6g}"
            for k in FLAGS:
                row[k] = int(r[k])
            ress.append([row[c] for c in RES_COLS])
            ctxs.append([pmcid, year, r["kind"], r["raw"], r["start"], int(r["error"]), int(r["decision_error"]),
                         int(r["error_1t"]), text[max(0, r["start"] - 150):r["end"] + 150]])
        arts.append([pmcid, ids.get("doi", ""), year, ey, em, ry, rm, new_format,
                     a.get("article-type", ""), subjects[-1] if subjects else "", ai_statement(a), first_country(meta),
                     int(body is not None), len(text), int(bool(ONE_TAIL.search(text))),
                     int(bool(ONE_TAIL_STRICT.search(text))), len(found)])
    return arts, ress, ctxs


def main():
    files = sorted(RAW.glob("*.xml.gz"))
    seen = set()
    fa = HashingGzip(ROOT / "data" / "articles.csv.gz")
    fr = HashingGzip(ROOT / "data" / "results.csv.gz")
    with Pool(4) as pool, gzip.open(ROOT / "data" / "raw" / "contexts.csv.gz", "wt", newline="") as fc:
        wa, wr, wc = csv.writer(fa), csv.writer(fr), csv.writer(fc)
        wa.writerow(ART_COLS)
        wr.writerow(RES_COLS)
        wc.writerow(["pmcid", "year", "kind", "raw", "start", "error", "decision_error", "error_1t", "context"])
        n_res = 0
        for arts, ress, ctxs in pool.imap(process, files, chunksize=4):
            keep = {a[0] for a in arts if a[0] not in seen}
            seen |= keep
            wa.writerows(a for a in arts if a[0] in keep)
            # a PMCID listed under two years is kept under the first only
            first_year = {a[0]: a[2] for a in arts if a[0] in keep}
            wr.writerows(r for r in ress if first_year.get(r[0]) == r[1])
            wc.writerows(c for c in ctxs if first_year.get(c[0]) == c[1])
            n_res += sum(1 for r in ress if first_year.get(r[0]) == r[1])
    requested = set()
    for f in (ROOT / "data" / "ids").glob("*.txt"):
        requested |= set(f.read_text().split())
    print(f"files={len(files)} articles={len(seen)} results={n_res} "
          f"requested_ids={len(requested)} not_returned={len(requested - seen)}")
    print(f"sha256 of uncompressed articles.csv: {fa.close()}")
    print(f"sha256 of uncompressed results.csv:  {fr.close()}")


if __name__ == "__main__":
    main()
