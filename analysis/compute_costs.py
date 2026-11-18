#!/usr/bin/env python3
"""Compute cost per serving and cost per gram of protein from data/prices.csv.

Inputs : data/prices.csv, data/products.csv
Outputs: data/derived_costs.csv, data/derived_product_metrics.csv, stdout table

All maths is deliberately simple and integer-exact where possible so the
published numbers can be re-derived by hand.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(value: str) -> float | None:
    value = (value or "").strip()
    if value == "":
        return None
    return float(value)


def money(value: float) -> str:
    return f"{value:,.2f}"


def main() -> None:
    prices = read_csv("prices.csv")
    products = read_csv("products.csv")

    product_index = {(p["brand"], p["product"]): p for p in products}

    rows: list[dict[str, object]] = []
    for row in prices:
        price = num(row["price_usd"])
        servings = num(row["servings"])
        protein = num(row["protein_g"])
        if price is None or servings is None or protein is None:
            raise ValueError(f"missing numeric field in prices row: {row}")

        total_protein = servings * protein
        cost_per_serving = price / servings
        cost_per_g = price / total_protein
        cost_per_25g = cost_per_g * 25

        product = product_index.get((row["brand"], row["product"]), {})
        serving_g = num(product.get("serving_g", ""))
        kcal = num(product.get("kcal", ""))
        protein_pct = (protein / serving_g * 100) if serving_g else None
        kcal_per_25g = (kcal * 25 / protein) if kcal else None

        rows.append(
            {
                "brand": row["brand"],
                "product": row["product"],
                "size_label": row["size_label"],
                "comparison_set": row["comparison_set"],
                "price_usd": f"{price:.2f}",
                "servings": f"{servings:g}",
                "protein_g": f"{protein:g}",
                "total_protein_g": f"{total_protein:.0f}",
                "cost_per_serving_usd": f"{cost_per_serving:.3f}",
                "cost_per_g_protein_usd": f"{cost_per_g:.4f}",
                "cost_per_25g_protein_usd": f"{cost_per_25g:.3f}",
                "protein_pct_of_powder": "" if protein_pct is None else f"{protein_pct:.1f}",
                "kcal_per_25g_protein": "" if kcal_per_25g is None else f"{kcal_per_25g:.0f}",
            }
        )

    primary = [r for r in rows if r["comparison_set"] == "primary"]
    primary.sort(key=lambda r: float(r["cost_per_g_protein_usd"]))
    for rank, row in enumerate(primary, start=1):
        row["rank_by_cost_per_g"] = rank
    for row in rows:
        row.setdefault("rank_by_cost_per_g", "")

    fieldnames = [
        "rank_by_cost_per_g",
        "brand",
        "product",
        "size_label",
        "comparison_set",
        "price_usd",
        "servings",
        "protein_g",
        "total_protein_g",
        "cost_per_serving_usd",
        "cost_per_g_protein_usd",
        "cost_per_25g_protein_usd",
        "protein_pct_of_powder",
        "kcal_per_25g_protein",
    ]
    with (DATA / "derived_costs.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        for row in primary + [r for r in rows if r["comparison_set"] != "primary"]:
            writer.writerow(row)

    print("Cost per 25 g of protein, cheapest first (primary pack sizes)\n")
    header = f"{'#':>2}  {'Brand / product':<62} {'$/serv':>7} {'$/g prot':>8} {'$/25 g':>7}"
    print(header)
    print("-" * len(header))
    for row in primary:
        label = f"{row['brand']} - {row['product']}"
        if len(label) > 62:
            label = label[:59] + "..."
        print(
            f"{row['rank_by_cost_per_g']:>2}  {label:<62} "
            f"{float(row['cost_per_serving_usd']):>7.2f} "
            f"{float(row['cost_per_g_protein_usd']):>8.4f} "
            f"{float(row['cost_per_25g_protein_usd']):>7.2f}"
        )

    spread = (
        float(primary[-1]["cost_per_g_protein_usd"])
        / float(primary[0]["cost_per_g_protein_usd"])
    )
    print(f"\nCheapest to most expensive per gram of protein: {spread:.1f}x spread")
    print(f"Wrote {len(rows)} priced products to data/derived_costs.csv")

    # Product-level composition metrics.
    metric_rows = []
    for p in products:
        serving_g = num(p["serving_g"])
        protein = num(p["protein_g"])
        kcal = num(p["kcal"])
        metric_rows.append(
            {
                "brand": p["brand"],
                "product": p["product"],
                "whey_type": p["whey_type"],
                "protein_pct_of_powder": f"{protein / serving_g * 100:.1f}",
                "kcal_per_25g_protein": "" if not kcal else f"{kcal * 25 / protein:.0f}",
                "protein_g_per_dollar_100": "",
            }
        )
    with (DATA / "derived_product_metrics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "brand",
                "product",
                "whey_type",
                "protein_pct_of_powder",
                "kcal_per_25g_protein",
                "protein_g_per_dollar_100",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(metric_rows)
    print("Wrote data/derived_product_metrics.csv")


if __name__ == "__main__":
    main()
