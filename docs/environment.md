# Research environment

What a cloud session on the `vibe-research` environment can reach, and the
quirks found while testing it. Everything here was tested on 2026-11-23 unless
marked otherwise. Re-test before relying on it, and update this file when
something changes.

**Network access is unrestricted** (set by the owner on 2026-11-23): a session
on this environment can reach any public site. The tables below record what
has actually been tested, not the limit of what is reachable. Because access
is open, the "Untrusted content" rules in `CLAUDE.md` apply to everything
fetched.

A session started on another environment (including Default) has restricted
access and none of the saved keys. If a host is refused, check which
environment the session is on before anything else.

## Sources that need no key

All returned HTTP 200 to a real query on 2026-11-23.

| Purpose | Source | Host |
|---|---|---|
| Literature | arXiv | `export.arxiv.org`, `arxiv.org` |
| Literature | OpenAlex | `api.openalex.org` |
| Literature | Crossref | `api.crossref.org` |
| Literature | Europe PMC | `www.ebi.ac.uk` |
| Literature | PubMed and NCBI E-utilities | `eutils.ncbi.nlm.nih.gov` |
| Sequences | OEIS | `oeis.org` |
| Astronomy | Gaia archive (TAP) | `gea.esac.esa.int` |
| Astronomy | MAST | `mast.stsci.edu` |
| Astronomy | NASA Exoplanet Archive (TAP) | `exoplanetarchive.ipac.caltech.edu` |
| Biology | UniProt | `rest.uniprot.org` |
| Biology | PDB | `data.rcsb.org`, `files.rcsb.org` |
| Chemistry | PubChem | `pubchem.ncbi.nlm.nih.gov` |
| Chemistry | ChEMBL | `www.ebi.ac.uk` |
| Earth | USGS earthquake catalogue | `earthquake.usgs.gov` |
| Economics | World Bank | `api.worldbank.org` |
| General | Wikidata query service | `query.wikidata.org` |

Web search is also available as a tool and does not depend on this list.

## Sources with a saved key

The key is added to requests by the network proxy. Code never sees it and no
environment variable holds it. Send the request without the key; where a
client library refuses to run without one, give it a placeholder such as
`proxy-injected`. Never write a real key into code, a file, or a commit.

| Source | Host | Notes |
|---|---|---|
| FRED | `api.stlouisfed.org` | **v2 API only.** `/fred/v2/release/observations?release_id=<id>&format=json` works. The v1 endpoints (`/fred/series`, `/fred/series/observations`) fail with "api_key is not set", because v1 takes the key in the URL and the proxy only sets a header. Fetch by release and filter to the series needed. |
| Copernicus Climate Data Store | `cds.climate.copernicus.eu` | Key verified. Each dataset has its own licence that must be accepted on its web page before the API will serve it; this has not been done for any dataset yet. Ask the repository owner. |
| NASA Earthdata | `cmr.earthdata.nasa.gov` | Token saved for the catalogue (CMR) only. The catalogue answers public searches with or without a token, so the token is not yet proven. Data files are served from other hosts, one per data centre; each needs the token added by the owner. Tokens expire (about 60 days, from memory, unverified). |

## Known problems

- **Semantic Scholar** (`api.semanticscholar.org`): no key. Reachable but
  rate-limited; roughly one request in three succeeded. Retry with backoff, or
  use OpenAlex and Crossref instead.
- **GWOSC** (`gwosc.org`): fails TLS certificate verification. Unavailable. Do
  not disable verification to get around it.
- **Unpaywall** (`api.unpaywall.org`): reachable, but requires a contact email
  in each request. None has been approved for this use. Do not put the owner's
  email in requests without asking.
- **Paywalled journals**: not accessible. Use open-access copies and preprints,
  and say so in the project when a key paper could not be read.
- **Untested sources**: anything not listed here is reachable in principle but
  has not been tried. The Internet Archive, NOAA and Hugging Face answered a
  basic request on 2026-11-23; nothing more was checked.

## Client behaviour

- Identify the client. Send a descriptive `User-Agent` without personal
  details. Wikidata rejected requests that had none.
- Respect rate limits. arXiv asks for at most one request every three seconds
  across all machines, over a single connection. Several agents running at
  once share that budget.
- Cache responses inside the project's `data/` folder rather than re-fetching,
  and record the query and access date for the external-data section.
- Some hosts drop connections intermittently. Retry a few times with backoff
  before concluding a source is down.

## Software

The environment's setup script installs scipy, sympy, matplotlib, networkx and
statsmodels; numpy and pandas are already present. Other Python packages can
be installed from PyPI during a session; pin the versions in the project.

Lean is not installed and this repository holds no Lean code. A project that
needs a proof states the theorem precisely in its README and marks the claim
`conjecture` or `proved-informal` until the proof exists in
[rabidlorax/math](https://github.com/rabidlorax/math). Cloud sessions here
have read access to that repository, not write access.
