#!/usr/bin/env python3
"""Validate every dataset and recompute the published arithmetic.

Run:  python analysis/validate.py

Exit code 0 means every check passed. Any failure prints FAIL and exits 1,
so the repository can be checked in CI or by hand before publishing.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def read_csv(name: str) -> tuple[list[str], list[dict[str, str]]]:
    with (DATA / name).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def fnum(value: str) -> float | None:
    value = (value or "").strip()
    return None if value == "" else float(value)


EXPECTED_HEADERS = {
    "products.csv": [
        "brand", "product", "whey_type", "primary_protein_source", "serving_g",
        "protein_g", "kcal", "carbs_g", "fat_g", "sugar_g", "sodium_mg",
        "servings", "container_g", "sweetener", "gums", "lecithin",
        "free_amino_acids", "label_confidence", "notes",
    ],
    "prices.csv": [
        "brand", "product", "size_label", "price_usd", "servings", "protein_g",
        "retailer", "price_date", "price_basis", "comparison_set", "notes",
    ],
    "flavors.csv": [
        "brand", "product", "flavor", "flavor_class", "contains_cocoa",
        "allergen_flags", "sweetener", "protein_g", "kcal", "carbs_g", "fat_g",
        "data_status", "list_status", "notes",
    ],
    "amino_acids.csv": ["amino_acid", "class", "g_per_100g_protein", "notes"],
    "contaminants.csv": [
        "study", "year", "n_products", "matrix", "analytes", "key_findings",
        "threshold_used", "reported_limitation", "url",
    ],
    "recalls.csv": [
        "date", "company", "product", "issue", "agency_or_forum", "action", "source",
    ],
    "certifications.csv": [
        "program", "operator", "what_is_tested", "batch_or_product",
        "public_results", "banned_substance_screen", "cost_to_consumer", "notes",
    ],
    "studies.csv": [
        "id", "citation", "design", "n", "population", "intervention", "outcome",
        "result", "certainty",
    ],
}

datasets: dict[str, list[dict[str, str]]] = {}
for filename, expected in EXPECTED_HEADERS.items():
    header, rows = read_csv(filename)
    datasets[filename] = rows
    check(header == expected, f"{filename}: header mismatch\n  got {header}\n  want {expected}")
    check(len(rows) > 0, f"{filename}: no rows")

# ---------------------------------------------------------------- products
products = datasets["products.csv"]
check(len(products) == 16, f"products.csv: expected 16 rows, found {len(products)}")
type_counts: dict[str, int] = {}
for row in products:
    serving = fnum(row["serving_g"])
    protein = fnum(row["protein_g"])
    check(serving is not None and serving > 0, f"products.csv: bad serving_g for {row['product']}")
    check(protein is not None and protein > 0, f"products.csv: bad protein_g for {row['product']}")
    pct = protein / serving * 100
    check(
        40 <= pct <= 95,
        f"products.csv: implausible protein density {pct:.1f}% for {row['product']}",
    )
    check(row["label_confidence"] in {"high", "medium", "low"}, f"products.csv: bad confidence for {row['product']}")
    check(row["whey_type"] in {"concentrate", "isolate", "hydrolysate_isolate", "blend"}, f"products.csv: bad whey_type for {row['product']}")
    type_counts[row["whey_type"]] = type_counts.get(row["whey_type"], 0) + 1
    for field in ("kcal", "carbs_g", "fat_g", "sugar_g", "sodium_mg"):
        value = fnum(row[field])
        check(value is None or value >= 0, f"products.csv: negative {field} for {row['product']}")
check(len(type_counts) >= 3, "products.csv: expected at least three whey formulations represented")

# ------------------------------------------------------------------ prices
prices = datasets["prices.csv"]
primary = [r for r in prices if r["comparison_set"] == "primary"]
check(len(primary) == 16, f"prices.csv: expected 16 primary rows, found {len(primary)}")
check(all(r["comparison_set"] in {"primary", "size_sensitivity"} for r in prices), "prices.csv: bad comparison_set")
for row in prices:
    check(re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["price_date"]) is not None, f"prices.csv: bad date {row['price_date']}")
    check(row["price_basis"] in {"observed", "list"}, f"prices.csv: bad price_basis {row['price_basis']}")
    check(fnum(row["price_usd"]) and fnum(row["price_usd"]) > 0, f"prices.csv: bad price for {row['product']}")

product_keys = {(p["brand"], p["product"]) for p in products}
for row in prices:
    check((row["brand"], row["product"]) in product_keys, f"prices.csv: no matching product row for {row['brand']} {row['product']}")
for row in products:
    check(
        any(p["brand"] == row["brand"] and p["product"] == row["product"] for p in prices),
        f"products.csv: no price row for {row['brand']} {row['product']}",
    )

# Recompute costs independently and compare to the published table.
derived = {(r["brand"], r["product"], r["size_label"]): r for r in datasets.get("derived_costs.csv", [])}
if not derived:
    header, rows = read_csv("derived_costs.csv")
    derived = {(r["brand"], r["product"], r["size_label"]): r for r in rows}
for row in prices:
    key = (row["brand"], row["product"], row["size_label"])
    published = derived.get(key)
    check(published is not None, f"derived_costs.csv: missing {key}")
    if published is None:
        continue
    price, servings, protein = fnum(row["price_usd"]), fnum(row["servings"]), fnum(row["protein_g"])
    expected_g = price / (servings * protein)
    expected_25 = expected_g * 25
    check(abs(float(published["cost_per_g_protein_usd"]) - expected_g) < 1e-4, f"derived_costs.csv: cost/g mismatch for {key}")
    check(abs(float(published["cost_per_25g_protein_usd"]) - expected_25) < 1e-3, f"derived_costs.csv: cost/25g mismatch for {key}")
    check(abs(fnum(published["total_protein_g"]) - servings * protein) < 1, f"derived_costs.csv: total protein mismatch for {key}")

# Headline figures quoted in the documentation.
on = next(r for r in derived.values() if r["brand"] == "Optimum Nutrition" and r["size_label"] == "5 lb")
check(1.45 <= float(on["cost_per_25g_protein_usd"]) <= 1.55, "headline: ON Gold Standard $/25 g outside 1.45-1.55")
iso = next(r for r in derived.values() if r["brand"] == "Dymatize")
check(2.10 <= float(iso["cost_per_25g_protein_usd"]) <= 2.22, "headline: ISO100 $/25 g outside 2.10-2.22")
body = next(r for r in derived.values() if r["brand"] == "Body Fortress")
check(float(body["cost_per_g_protein_usd"]) < float(on["cost_per_g_protein_usd"]), "headline: Body Fortress should undercut ON per labelled gram")

ranks = sorted(int(r["rank_by_cost_per_g"]) for r in derived.values() if r["rank_by_cost_per_g"])
check(ranks == list(range(1, len(ranks) + 1)), "derived_costs.csv: ranks are not a clean 1..n sequence")

# ------------------------------------------------------------- amino acids
aa = datasets["amino_acids.csv"]
total = sum(fnum(r["g_per_100g_protein"]) for r in aa)
check(95 <= total <= 105, f"amino_acids.csv: total {total:.1f} g/100 g outside 95-105")
eaa_classes = {"essential", "essential_bcaa"}
eaa = sum(fnum(r["g_per_100g_protein"]) for r in aa if r["class"] in eaa_classes)
check(45 <= eaa <= 56, f"amino_acids.csv: EAA total {eaa:.1f} outside 45-56")
noteaa = sum(fnum(r["g_per_100g_protein"]) for r in aa if r["class"] not in eaa_classes)
check(abs((eaa + noteaa) - total) < 1e-9, "amino_acids.csv: class totals do not sum")
leucine = next(fnum(r["g_per_100g_protein"]) for r in aa if r["amino_acid"] == "Leucine")
check(9.5 <= leucine <= 12.0, "amino_acids.csv: leucine outside 9.5-12 g/100 g")
check(2.3 <= leucine / 100 * 25 <= 2.9, "amino_acids.csv: leucine per 25 g protein outside 2.3-2.9 g")
bcaa = sum(fnum(r["g_per_100g_protein"]) for r in aa if r["class"] == "essential_bcaa")
check(20 <= bcaa <= 25, f"amino_acids.csv: BCAA total {bcaa:.1f} outside 20-25")

# ----------------------------------------------------------------- flavors
flavors = datasets["flavors.csv"]
check(len(flavors) >= 55, f"flavors.csv: expected at least 55 rows, found {len(flavors)}")
allowed_classes = {"chocolate", "vanilla_cream", "fruit_cream", "coffee", "baked", "cookies", "caramel", "unflavored"}
cocoa_classes = {"chocolate", "coffee", "cookies", "baked"}
for row in flavors:
    check(row["flavor_class"] in allowed_classes, f"flavors.csv: bad class {row['flavor_class']}")
    check(row["contains_cocoa"] in {"yes", "no"}, f"flavors.csv: bad contains_cocoa for {row['flavor']}")
    check(row["data_status"] in {"verified", "protein_verified", "varies"}, f"flavors.csv: bad data_status for {row['flavor']}")
    check(row["list_status"] in {"complete", "partial"}, f"flavors.csv: bad list_status for {row['flavor']}")
    check(
        any(row["brand"] == brand and product_name.startswith(row["product"]) for brand, product_name in product_keys),
        f"flavors.csv: no product family row for {row['brand']} {row['product']}",
    )
    if row["contains_cocoa"] == "yes":
        check(row["flavor_class"] in cocoa_classes or row["flavor"] == "White Chocolate", f"flavors.csv: cocoa/class mismatch {row['flavor']}")
    protein = fnum(row["protein_g"])
    check(protein is not None and 18 <= protein <= 32, f"flavors.csv: implausible protein for {row['flavor']}")
    if row["data_status"] == "verified":
        check(fnum(row["kcal"]) is not None, f"flavors.csv: verified row without kcal: {row['flavor']}")
flavor_brands = {r["brand"] for r in flavors}
check(len(flavor_brands) == 6, f"flavors.csv: expected 6 brands, found {len(flavor_brands)}")

# ----------------------------------------------------------------- studies
studies = datasets["studies.csv"]
ids = [r["id"] for r in studies]
check(len(ids) == len(set(ids)), "studies.csv: duplicate ids")
check(ids == [f"S{i:02d}" for i in range(1, len(ids) + 1)], "studies.csv: ids are not sequential from S01")
for row in studies:
    check(row["certainty"] in {"High", "Moderate", "Low", "Low-moderate", "Moderate-low", "Low-moderate (association, not causation)", "Moderate (small n)", "Moderate (advocacy, aggregate data)", "Expert opinion", "Guideline", "Regulatory", "Industry source (not independent)", "Moderate-high", "Low (small, non-random)", "Low (conference abstract)", "Moderate (advocacy, aggregate data)"} or row["certainty"].startswith("Moderate"), f"studies.csv: unexpected certainty label {row['certainty']}")
    check(len(row["citation"]) > 20, f"studies.csv: citation too short for {row['id']}")

# -------------------------------------------------------------- URLs / refs
for dataset in ("contaminants.csv", "recalls.csv"):
    for row in datasets[dataset]:
        url = row["url"] if dataset == "contaminants.csv" else row["source"]
        check(url.startswith("http"), f"{dataset}: bad URL {url}")

# -------------------------------------------------------------------- docs
expected_docs = [
    "01-methodology.md", "02-formulations.md", "03-protein-quality.md",
    "04-efficacy.md", "05-dosage.md", "06-digestion-allergy.md",
    "07-additives.md", "08-flavors.md", "09-contaminants.md",
    "10-testing-certifications.md", "11-safety-kidney-liver.md",
    "12-hormones-myths.md", "13-production-claims.md",
    "14-manufacturing-recalls-regulation.md", "15-brands-and-cost.md",
    "16-recommendations.md", "17-limitations.md", "references.md",
]
for name in expected_docs:
    path = DOCS / name
    check(path.exists(), f"docs/{name}: missing")
    if path.exists():
        text = path.read_text(encoding="utf-8")
        check(len(text) > 1200, f"docs/{name}: suspiciously short")
        check("[S" in text or "http" in text, f"docs/{name}: no citation marker")

readme = ROOT / "README.md"
check(readme.exists(), "README.md: missing")
if readme.exists():
    text = readme.read_text(encoding="utf-8")
    check(len(text) > 4000, "README.md: suspiciously short")
    for token in ("data/products.csv", "data/derived_costs.csv", "analysis/validate.py", "docs/references.md"):
        check(token in text, f"README.md: missing reference to {token}")
    check("$1.51" in text or "1.51" in text, "README.md: headline ON cost figure missing")
    check("not medical advice" in text.lower(), "README.md: missing disclaimer")

# ------------------------------------------------------- cross-doc numbers
doc_15 = (DOCS / "15-brands-and-cost.md")
if doc_15.exists():
    text = doc_15.read_text(encoding="utf-8")
    for brand in ("Optimum Nutrition", "Dymatize", "Naked", "Body Fortress", "Klean"):
        check(brand in text, f"15-brands-and-cost.md: missing {brand}")

print(f"{checks} checks run")
if failures:
    print(f"\n{len(failures)} FAILED")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)
print("All dataset, arithmetic and documentation checks passed.")
