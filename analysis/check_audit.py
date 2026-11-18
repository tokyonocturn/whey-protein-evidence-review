#!/usr/bin/env python3
"""Verify that every in-text citation marker has an audit verdict.

Fails when a marker in README.md or docs/*.md has no row in
data/citation_audit.csv, when a row no longer matches the documented text, when
a verdict is unrecognised, or when a row lacks its supporting evidence or its
reason for being unverified.

Run: python analysis/check_audit.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "citation_audit.csv"
MARKER = re.compile(r"\[([^\]]*S\d{2}[^\]]*)\]")
VERDICTS = {"supported", "unverified"}

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def instances() -> list[tuple[str, str, int, str]]:
    rows: list[tuple[str, str, int, str]] = []
    seen: dict[tuple[str, str], int] = {}
    files = [ROOT / "README.md"] + sorted((ROOT / "docs").glob("*.md"))
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            for match in MARKER.finditer(line):
                for number in re.findall(r"S(\d{2})", match.group(1)):
                    study = f"S{number}"
                    key = (path.name, study)
                    seen[key] = seen.get(key, 0) + 1
                    claim = re.sub(r"\s+", " ", line).strip()[:220]
                    rows.append((path.name, study, seen[key], claim))
    return rows


with (ROOT / "data" / "studies.csv").open(encoding="utf-8") as handle:
    study_ids = {row["id"] for row in csv.DictReader(handle)}

with AUDIT.open(encoding="utf-8") as handle:
    audit_rows = list(csv.DictReader(handle))

audit = {}
for row in audit_rows:
    key = (row["doc"], row["study"], int(row["occurrence"]))
    check(key not in audit, f"citation_audit.csv: duplicate row {key}")
    audit[key] = row
    check(row["verdict"] in VERDICTS, f"{key}: unknown verdict '{row['verdict']}'")
    check(row["study"] in study_ids, f"{key}: study not in studies.csv")
    check(bool(row["claim"]), f"{key}: empty claim")
    if row["verdict"] == "supported":
        check(bool(row["evidence"]), f"{key}: supported row has no evidence")
        check(not row["reason"], f"{key}: supported row should not carry a reason")
    else:
        check(bool(row["reason"]), f"{key}: unverified row has no reason")
        check(not row["evidence"], f"{key}: unverified row should not claim evidence")

expected = instances()
check(
    len(expected) == len(audit),
    f"docs contain {len(expected)} marker instances but the audit has {len(audit)} rows",
)

for doc, study, occurrence, claim in expected:
    key = (doc, study, occurrence)
    row = audit.get(key)
    check(row is not None, f"no audit row for {doc} {study} #{occurrence}")
    if row is not None:
        check(
            row["claim"] == claim,
            f"{key}: audit claim is stale; rebuild with analysis/build_citation_audit.py",
        )

documented = {(doc, study, occurrence) for doc, study, occurrence, _ in expected}
for key in audit:
    check(key in documented, f"citation_audit.csv: row {key} no longer exists in the docs")

supported = sum(1 for row in audit_rows if row["verdict"] == "supported")
unverified = sum(1 for row in audit_rows if row["verdict"] == "unverified")

print(f"{checks} audit checks run over {len(audit_rows)} marker instances")
print(f"  supported by the cited source: {supported}")
print(f"  explicitly unverified:         {unverified}")
if failures:
    print(f"\n{len(failures)} FAILED")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)
print("Every in-text citation marker has an explicit verdict.")
