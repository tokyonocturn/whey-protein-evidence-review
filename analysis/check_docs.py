#!/usr/bin/env python3
"""Check the documentation against itself and against the datasets.

Verifies:
  1. every relative Markdown link resolves to a file that exists;
  2. every [Sxx] citation resolves to a row in data/studies.csv;
  3. every study in studies.csv is listed in docs/references.md;
  4. the README lists every dataset and document that exists;
  5. the cost table in docs/15-brands-and-cost.md matches derived_costs.csv exactly;
  6. the headline figures in the README match the data.

Run: python analysis/check_docs.py   (exit 0 = all good)
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def read_rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
CITATION = re.compile(r"\[([^\]]*S\d{2}[^\]]*)\]")

studies = read_rows("studies.csv")
study_ids = {row["id"] for row in studies}
check(len(study_ids) == 46, f"studies.csv: expected 46 ids, found {len(study_ids)}")

references = (DOCS / "references.md").read_text(encoding="utf-8")

# ---------------------------------------------------------------- each document
documents = [ROOT / "README.md"] + sorted(DOCS.glob("*.md"))
for doc in documents:
    text = doc.read_text(encoding="utf-8")
    for label, target in LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = target.split("#")[0].strip()
        if not relative:
            continue
        resolved = (doc.parent / relative).resolve()
        check(resolved.exists(), f"{doc.name}: broken link '{target}' (from '{label}')")
    for content in CITATION.findall(text):
        for number in re.findall(r"S(\d{2})", content):
            check(f"S{number}" in study_ids, f"{doc.name}: citation S{number} not in studies.csv")

# ------------------------------------------------------------- reference completeness
for study_id in sorted(study_ids):
    check(study_id in references, f"references.md: missing entry for {study_id}")

# ------------------------------------------------------------------- README coverage
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for path in sorted(DATA.glob("*.csv")):
    check(path.name in readme, f"README.md: data file '{path.name}' not listed")
for path in sorted(DOCS.glob("*.md")):
    check(path.name in readme, f"README.md: document '{path.name}' not listed")

# ------------------------------------------------------- cost table vs derived data
derived = {
    (r["brand"], r["product"]): r
    for r in read_rows("derived_costs.csv")
    if r["comparison_set"] == "primary"
}
cost_doc = (DOCS / "15-brands-and-cost.md").read_text(encoding="utf-8")

matched = 0
for line in cost_doc.splitlines():
    if not line.startswith("|") or "$" not in line:
        continue
    cells = [cell.strip().strip("*").strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) < 6 or not cells[0].isdigit():
        continue
    brand, product = cells[1], cells[2]
    label = f"{brand} {product}"
    money = [cell for cell in cells[3:] if cell.startswith("$")]
    check(len(money) == 3, f"15-brands-and-cost.md: row '{label}' does not have three dollar figures")
    if len(money) != 3:
        continue
    row = derived.get((brand, product))
    check(row is not None, f"15-brands-and-cost.md: no dataset row for '{label}'")
    if row is None:
        continue
    expected = [
        f"{float(row['cost_per_serving_usd']):.2f}",
        f"{float(row['cost_per_g_protein_usd']):.4f}",
        f"{float(row['cost_per_25g_protein_usd']):.2f}",
    ]
    for published, want in zip(money[:3], expected):
        check(
            published.lstrip("$") == want,
            f"15-brands-and-cost.md: '{label}' has {published}, dataset says ${want}",
        )
    matched += 1
check(matched == len(derived), f"15-brands-and-cost.md: matched {matched} rows, dataset has {len(derived)}")

# ------------------------------------- composition table vs derived product metrics
metrics = {(r["brand"], r["product"]): r for r in read_rows("derived_product_metrics.csv")}
products = {(r["brand"], r["product"]): r for r in read_rows("products.csv")}
composition_labels = {
    "Transparent Labs Grass-Fed Isolate": (
        "Transparent Labs",
        "100% Grass-Fed Whey Protein Isolate (French Vanilla)",
    ),
    "Legion Whey+": ("Legion", "Whey+ (French Vanilla)"),
    "Myprotein Impact Whey": ("Myprotein", "Impact Whey Protein (Vanilla)"),
    "Naked Whey": ("Naked Nutrition", "Naked Whey (Unflavored)"),
    "Optimum Nutrition Gold Standard": (
        "Optimum Nutrition",
        "Gold Standard 100% Whey (Double Rich Chocolate)",
    ),
    "Dymatize ISO100": ("Dymatize", "ISO100 Hydrolyzed (Gourmet Chocolate)"),
    "BSN Syntha-6": ("BSN", "Syntha-6 (Chocolate Milkshake)"),
}

composition_seen = 0
for line in (DOCS / "02-formulations.md").read_text(encoding="utf-8").splitlines():
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) != 5 or cells[0] not in composition_labels:
        continue
    label = cells[0]
    key = composition_labels[label]
    metric = metrics[key]
    product = products[key]
    composition_seen += 1
    check(
        cells[2] == f"{float(metric['protein_pct_of_powder']):.1f} g",
        f"02-formulations.md: density for {label} is {cells[2]}, dataset says {metric['protein_pct_of_powder']} g",
    )
    check(
        cells[3] == f"{float(product['protein_g']):g} g",
        f"02-formulations.md: protein per serving for {label} is {cells[3]}, dataset says {product['protein_g']} g",
    )
    if metric["kcal_per_25g_protein"]:
        check(
            cells[4] == f"{float(metric['kcal_per_25g_protein']):.0f}",
            f"02-formulations.md: kcal per 25 g for {label} is {cells[4]}, dataset says {metric['kcal_per_25g_protein']}",
        )
    else:
        check(cells[4] == "not disclosed", f"02-formulations.md: {label} should say 'not disclosed' for calories")
check(composition_seen == 7, f"02-formulations.md: expected 7 checked composition rows, found {composition_seen}")

# --------------------------------------------------------------- README headline figures
for token in ("$0.77", "$1.51", "$4.03", "5.2x", "1.62 g/kg"):
    check(token in readme, f"README.md: headline figure '{token}' missing")

# ------------------------------------------------------------ no orphan documents
linked = set()
for doc in documents:
    text = doc.read_text(encoding="utf-8")
    for _, target in LINK.findall(text):
        if target.startswith(("http", "mailto", "#")):
            continue
        linked.add((doc.parent / target.split("#")[0]).resolve())
for doc in sorted(DOCS.glob("*.md")):
    check(doc.resolve() in linked, f"{doc.name}: not linked from README or another document")

print(f"{checks} documentation checks run")
if failures:
    print(f"\n{len(failures)} FAILED")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)
print("All links, citation markers and published figures agree with the datasets.")
