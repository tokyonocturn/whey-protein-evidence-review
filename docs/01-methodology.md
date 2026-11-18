# Methodology

## What this review is, and what it is not

This is a **secondary evidence review with reproducible datasets**. It synthesises peer-reviewed
research, independent laboratory reports, regulatory documents and manufacturer labels. **No new
laboratory testing was commissioned.** Every contamination number in this repository comes from
someone else's assay, and is attributed in `data/contaminants.csv`. That distinction matters: a
review can rank products on published test data, but it cannot certify any individual tub.

Research cut-off: **18 November 2026**. Prices are a single-day snapshot and are dated per row.
Formulations change without notice, so the label on the tub in your hand overrides this repository.

## Questions the review had to answer

1. Do concentrate, isolate and hydrolysate differ in any way that changes outcomes for a real person?
2. What does protein quality measurement actually show for whey, and where is it oversold?
3. How strong is the evidence for muscle, strength, recovery and general health?
4. What intake and serving size does the evidence support, by population?
5. Who will tolerate whey, and who must avoid it?
6. Which added ingredients are inert, which are irritating, and which are markers of low quality?
7. How much do flavours change the product?
8. What do independent labs find for heavy metals, microbes and pesticides?
9. What do certifications actually certify?
10. Is high protein safe long term, and for whom is it not?
11. Which hormonal and health claims survive scrutiny?
12. Do grass-fed, organic and conventional whey differ in any meaningful way?
13. How well is the category manufactured and regulated?
14. What does a gram of protein cost, and which products are worth it?

## Source hierarchy

Evidence was weighted in this order:

| Tier | Source type | Use in this review |
|---|---|---|
| 1 | Systematic reviews and meta-analyses of RCTs | Primary basis for efficacy and safety claims |
| 2 | Individual randomised controlled trials | Mechanism, dose-response, population-specific questions |
| 3 | Prospective cohorts and case-control studies | Long-term risk and observational associations, always labelled as such |
| 4 | Regulatory documents and clinical guidelines | Kidney, liver, labelling and safety boundaries |
| 5 | Independent laboratory reports | Contaminant rankings only, never efficacy |
| 6 | Manufacturer labels and product pages | Composition, ingredients, price, flavours |

Where tiers conflict, the higher tier wins and the conflict is stated. Where only tier 5 or 6 data
exist, the claim is marked as unverified.

## Product selection

Sixteen products were selected to cover the decisions a buyer actually faces, not to rank
popularity:

- **Formulation spread:** concentrate, isolate, hydrolysate/isolate, and multi-source blends.
- **Market presence:** the largest-selling whey line in the category (Optimum Nutrition Gold
  Standard) plus mass-market, pharmacy, direct-to-consumer and clinician-channel brands.
- **Certification spread:** products holding NSF Certified for Sport, Informed Sport, Informed
  Choice, or no certification, so certification can be compared with price and formulation.
- **Independent test coverage:** several selected products appear in the Clean Label Project's
  "Clean Sixteen" (non-detect for four heavy metals) or in Consumer Reports' 2025/2026 testing,
  which allows contamination to be discussed at product level rather than brand level.

Selection bias is real: brands with no public test data are under-represented in the contaminant
discussion, which is a statement about transparency, not about purity.

## Data capture rules

- **Label data** (`data/products.csv`) was transcribed from manufacturer or major-retailer listings.
  Each row carries a `label_confidence` field of `high` (label read directly, including ingredient
  list) or `medium` (macros from a retailer listing or a secondary compilation). Missing values are
  left empty rather than guessed.
- **Flavours** (`data/flavors.csv`) record the flavour list as published on the manufacturer site on
  the access date. `list_status` is `complete` where the full published list was captured and
  `partial` where the site renders flavours dynamically and only a subset could be confirmed.
  `data_status` is `verified` only where the per-flavour macros were read from a label; `varies`
  means the flavour exists but its exact panel was not transcribed, and the row explains what
  changes and why.
- **Prices** (`data/prices.csv`) record retailer, date, and whether the price was observed or list.
  One primary pack size per product is used for ranking; a second Optimum Nutrition row is kept
  outside the ranking to quantify pack-size effects.
- **Studies** (`data/studies.csv`) record design, n, population, intervention, outcome, result and a
  certainty label. Certainty uses GRADE-like language: high, moderate, low.

## Calculations

`analysis/compute_costs.py` derives every cost figure from `data/prices.csv` with three formulas:

```
cost_per_serving      = price / servings
cost_per_g_protein    = price / (servings x protein_g)
cost_per_25g_protein  = cost_per_g_protein x 25
```

Cost per 25 g is the headline because 25 g is close to a typical effective dose for a 70-80 kg adult
and normalises across products with 20-30 g servings. Cost per gram is provided for anyone dosing
differently. Protein density (`protein_g / serving_g`) and calories per 25 g of protein are derived
in `data/derived_product_metrics.csv`.

`analysis/validate.py` independently recomputes every published cost, checks that protein never
exceeds serving weight, that protein density is physiologically plausible, that the amino acid table
sums correctly and that EAA/BCAA/leucine totals fall in published ranges, that every priced product
has a label row and vice versa, that flavour rows reference real products, that study IDs are
sequential, and that every document and dataset referenced by the README exists. It exits non-zero
on any failure.

## Evidence grading used in the documents

- **Strong:** consistent findings across multiple meta-analyses or large RCTs.
- **Moderate:** at least one good meta-analysis or several consistent RCTs, some heterogeneity.
- **Weak:** single small trials, mechanistic reasoning, or observational data only.
- **Contested:** credible evidence on both sides; the review says so rather than picking a side.

## Known limitations

1. No primary testing; contamination conclusions inherit the methods, sample sizes and conflicts of
   the cited laboratories.
2. Advocacy-generated data (Clean Label Project, Consumer Reports) is used for **relative ranking**,
   which is its strength, not for absolute risk, which it cannot establish.
3. Retail prices move daily and vary by flavour, seller and subscription status.
4. Label macros are not lab-verified. Independent surveys find 5-30% of products off-label, usually
   modestly and occasionally severely.
5. The evidence base for whey is dominated by small, short studies, frequently funded by dairy or
   supplement interests.
6. Most trials enrol young, trained men; older adults, women, children and clinical populations are
   under-studied.

## Conflict of interest

None. No brand, retailer, laboratory or trade body reviewed this work, supplied data, or paid for
it. Every product was selected for analytical coverage, not commercial relationship.

## Reproducing this review

```bash
python analysis/compute_costs.py   # regenerates derived cost tables
python analysis/validate.py        # re-checks every number and cross-reference
```

Both scripts use only the Python standard library.

## Source register

Every claim in this repository is tied to a numbered study in `data/studies.csv` ([S01]-[S43]) or to
a laboratory, regulatory or product source listed in [references.md](references.md). If a sentence has
no citation, it is analysis rather than a finding.
