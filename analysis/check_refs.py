#!/usr/bin/env python3
"""Check every reference URL for link rot and confirm blocked pages exist.

Publisher sites routinely return 403 or 429 to automated clients without the
article being gone, so a non-200 status is not by itself link rot. For those
entries the script asks Crossref whether the DOI (or, failing that, the title)
resolves to a real record whose title matches the citation.

Network dependent, so it is not part of CI. Run manually:

    python analysis/check_refs.py

Exit status is non-zero when a URL is genuinely dead (404/410), when no URL is
present, or when a blocked entry cannot be matched to a Crossref record.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "docs" / "references.md"
UA = "whey-evidence-review/1.0 (mailto:kevinedwards7289@gmail.com)"
DEAD = {404, 410, 451}
BLOCKED = {0, 401, 403, 405, 406, 429, 500, 502, 503}

URL = re.compile(r"https?://\S+")
DOI = re.compile(r"10\.\d{4,9}/[^\s;,)\]]+")
STUDY = re.compile(r"\*\*(S\d{2})\*\*")


def request(url: str, timeout: int = 25):
    return urllib.request.Request(url, headers={"User-Agent": UA})


def status_of(url: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(request(url), timeout=25) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, url
    except Exception as exc:  # noqa: BLE001 - any transport failure is "unreachable"
        return 0, f"{type(exc).__name__}: {exc}"


def crossref(params: dict[str, str]) -> dict | None:
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {**params, "rows": "1"}
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request(url), timeout=30) as response:
                items = json.load(response)["message"]["items"]
                return items[0] if items else None
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503):
                time.sleep(2 * (attempt + 1))
                continue
            return None
        except Exception:  # noqa: BLE001 - network flake, retry
            time.sleep(2 * (attempt + 1))
    return None


def tokens(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-z]{4,}", text.lower())}


def parse_blocks() -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current: list[str] = []
    for line in REFERENCES.read_text(encoding="utf-8").splitlines():
        if line.startswith("- "):
            if current:
                blocks.append(_finish(current))
            current = [line[2:].strip()]
        elif current and line.strip():
            current.append(line.strip())
    if current:
        blocks.append(_finish(current))
    return [block for block in blocks if block.get("url")]


def _finish(lines: list[str]) -> dict[str, str]:
    text = " ".join(lines)
    study = STUDY.search(text)
    url = URL.search(text)
    doi = DOI.search(text)
    return {
        "text": text,
        "id": study.group(1) if study else "",
        "url": url.group(0).rstrip(".,;") if url else "",
        "doi": doi.group(0) if doi else "",
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    blocks = parse_blocks()
    print(f"{len(blocks)} reference entries with a URL\n")
    problems: list[str] = []
    unconfirmed: list[str] = []
    confirmed = 0
    for block in blocks:
        label = block["id"] or block["text"][:60]
        status, _ = status_of(block["url"])
        note = ""
        if status in DEAD:
            problems.append(f"{label}: HTTP {status} (dead) {block['url']}")
            note = "DEAD"
        elif status in BLOCKED or status >= 500:
            scholarly = bool(block["id"] or block["doi"])
            if not scholarly:
                unconfirmed.append(block["url"])
                print(f"{label:>4} {status:>3} {block['url'][:78]}")
                print("      BLOCKED by publisher, not a scholarly record (status only)")
                time.sleep(1.0)
                continue
            record = crossref({"filter": f"doi:{block['doi']}"}) if block["doi"] else None
            if record is None:
                record = crossref({"query.bibliographic": block["text"][:300]})
            if record is None:
                problems.append(f"{label}: HTTP {status} and no Crossref record {block['url']}")
                note = "BLOCKED, no Crossref match"
            else:
                title = (record.get("title") or [""])[0]
                overlap = len(tokens(title) & tokens(block["text"])) / max(len(tokens(title)), 1)
                if overlap < 0.5:
                    problems.append(f"{label}: Crossref title mismatch ({overlap:.0%}): {title!r}")
                    note = f"BLOCKED, title match {overlap:.0%}: {title[:60]}"
                else:
                    confirmed += 1
                    note = f"BLOCKED by publisher, Crossref confirms: {title[:60]}"
        elif status != 200:
            note = f"HTTP {status}"
        print(f"{label:>4} {status:>3} {block['url'][:78]}")
        if note:
            print(f"      {note}")
        time.sleep(1.0)

    print(
        f"\n{len(blocks)} URLs checked, {confirmed} bot-blocked scholarly pages confirmed "
        f"against Crossref, {len(unconfirmed)} blocked non-scholarly pages, {len(problems)} problems"
    )
    for problem in problems:
        print(f"  - {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
