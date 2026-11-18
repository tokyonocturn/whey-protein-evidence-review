#!/usr/bin/env python3
"""Fetch abstracts for every study in data/studies.csv.

Resolves a DOI for each study (from the citation, or via Crossref), then asks
Europe PMC for the abstract, falling back to PubMed. Writes a plain-text digest
so the abstracts can be read alongside the claims they are supposed to support.

    python analysis/fetch_abstracts.py [_abstracts.txt]

Network dependent, so it is not part of CI.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "whey-evidence-review/1.0 (mailto:kevinedwards7289@gmail.com)"


def get_json(url: str, timeout: int = 30) -> dict | None:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503):
                time.sleep(2 * (attempt + 1))
                continue
            return None
        except Exception:  # noqa: BLE001 - retry transport failures
            time.sleep(2 * (attempt + 1))
    return None


def resolve_doi(row: dict[str, str]) -> str:
    found = re.search(r"10\.\d{4,9}/[^\s;,]+", row["citation"])
    if found:
        return found.group(0).rstrip(".")
    query = urllib.parse.urlencode(
        {"query.bibliographic": row["citation"][:250], "rows": "1", "select": "DOI"}
    )
    payload = get_json(f"https://api.crossref.org/works?{query}")
    if payload and payload["message"]["items"]:
        return payload["message"]["items"][0]["DOI"]
    return ""


def europe_pmc(doi: str) -> tuple[str, str]:
    query = urllib.parse.urlencode(
        {"query": f'DOI:"{doi}"', "resultType": "core", "format": "json", "pageSize": "1"}
    )
    payload = get_json(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{query}")
    if not payload:
        return "", ""
    results = payload.get("resultList", {}).get("result", [])
    if not results:
        return "", ""
    record = results[0]
    abstract = re.sub(r"<[^>]+>", " ", record.get("abstractText", "") or "")
    return re.sub(r"\s+", " ", abstract).strip(), record.get("pmcid", "") or ""


def pubmed_abstract(doi: str) -> str:
    search = urllib.parse.urlencode({"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"})
    payload = get_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{search}")
    ids = (payload or {}).get("esearchresult", {}).get("idlist", [])
    if not ids:
        return ""
    fetch = urllib.parse.urlencode(
        {"db": "pubmed", "id": ids[0], "rettype": "abstract", "retmode": "text"}
    )
    request = urllib.request.Request(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{fetch}",
        headers={"User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", "replace").strip()
    except Exception:  # noqa: BLE001
        return ""


def main() -> int:
    rows = list(csv.DictReader((ROOT / "data" / "studies.csv").open(encoding="utf-8")))
    out = io.StringIO()
    missing: list[str] = []
    for row in rows:
        doi = resolve_doi(row)
        abstract, pmcid = europe_pmc(doi) if doi else ("", "")
        if not abstract and doi:
            abstract = pubmed_abstract(doi)
        if not abstract:
            missing.append(row["id"])
        out.write(
            f"\n===== {row['id']} doi={doi or '-'} pmcid={pmcid or '-'} =====\n"
            f"{abstract[:3500] or 'NO ABSTRACT RETRIEVED'}\n"
        )
        time.sleep(0.5)
    digest = out.getvalue()
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if target:
        target.write_text(digest, encoding="utf-8")
        print(f"Wrote {len(rows)} entries to {target}; missing abstracts: {missing or 'none'}")
    else:
        print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
