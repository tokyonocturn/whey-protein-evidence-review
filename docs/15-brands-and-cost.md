# Brand comparison and cost per gram of protein

All figures below are computed by `analysis/compute_costs.py` from `data/prices.csv`, using a single
price snapshot dated per row (November 2026 unless noted). Cost per 25 g of protein is the headline
metric because 25 g is close to a typical effective dose; cost per gram is included for other dosing.

## The full cost table

| # | Brand | Product | $/serving | $/g protein | $/25 g protein |
|---|---|---|---|---|---|
| 1 | Body Fortress | Super Advanced Whey Protein (Chocolate) | $0.93 | $0.0309 | **$0.77** |
| 2 | Myprotein | Impact Whey Protein (Vanilla) | $1.00 | $0.0476 | **$1.19** |
| 3 | Optimum Nutrition | Gold Standard 100% Whey (Double Rich Chocolate) | $1.45 | $0.0605 | **$1.51** |
| 4 | Premier Protein | 100% Whey Protein Powder (Chocolate Milkshake) | $2.03 | $0.0676 | **$1.69** |
| 5 | BSN | Syntha-6 (Chocolate Milkshake) | $1.58 | $0.0720 | **$1.80** |
| 6 | Naked Nutrition | Naked Whey (Unflavored) | $1.84 | $0.0737 | **$1.84** |
| 7 | Transparent Labs | 100% Grass-Fed Whey Protein Isolate (French Vanilla) | $2.17 | $0.0774 | **$1.93** |
| 8 | Ascent | Native Fuel Whey (Vanilla Bean) | $2.07 | $0.0827 | **$2.07** |
| 9 | Dymatize | ISO100 Hydrolyzed (Gourmet Chocolate) | $2.17 | $0.0867 | **$2.17** |
| 10 | Isopure | Low Carb (Creamy Vanilla) | $2.18 | $0.0871 | **$2.18** |
| 11 | Garden of Life | Sport Grass Fed Whey (Vanilla) | $2.10 | $0.0875 | **$2.19** |
| 12 | Legion | Whey+ (French Vanilla) | $2.00 | $0.0909 | **$2.27** |
| 13 | Thorne | Whey Protein Isolate (Vanilla) | $2.17 | $0.1032 | **$2.58** |
| 14 | Bare Performance Nutrition | Whey Isolate (Vanilla) | $2.60 | $0.1040 | **$2.60** |
| 15 | Momentous | Whey Protein Isolate (Vanilla) | $2.80 | $0.1400 | **$3.50** |
| 16 | Klean Athlete | Klean Isolate (Vanilla) | $3.23 | $0.1613 | **$4.03** |

**Spread: 5.2x** between the cheapest (Body Fortress) and the most expensive (Klean) per gram of
labelled protein. Excluding the two extremes, most of the market sits between $1.51 and $2.60 per
25 g.

## Pack size matters as much as brand

Optimum Nutrition Gold Standard 5 lb is **$1.51 per 25 g**. The same product in a 2 lb tub is
**$2.68 per 25 g**, 77% more per gram. Small tubs, single-serve sachets and subscription-free
retail purchases are where value disappears. If you are confident you will use the product, buy the
largest size with a reasonable expiry date.

The same effect appears across the market: 5 lb and 4.5 lb tubs are consistently the value sizes,
2 lb and 1 lb sizes carry a 40-80% premium per gram.

## What the price buys

| Price band | What you get | Examples |
|---|---|---|
| Under $1.25/25 g | Concentrate or blend, often with free amino acids or lower protein density | Body Fortress, Myprotein |
| $1.50-$1.90/25 g | Mainstream blend or single-ingredient concentrate; often certified | ON Gold Standard, Premier, BSN, Naked |
| $1.90-$2.30/25 g | Isolate, grass-fed, stevia, or sport certification | Transparent Labs, Ascent, ISO100, Isopure, Garden of Life, Legion |
| $2.50-$4.00/25 g | Clinician-channel or premium isolate; certification and brand premium | Thorne, BPN, Momentous, Klean |

The correlation between price and protein quality is weak. DIAAS for a $1.51 blend and a $4.03
isolate differ by about 0.12 (1.09 vs 0.97), which is not a meaningful difference in a mixed diet.
What you actually pay for above $2.00 is lactose removal, certification, sweetener preference,
flavour, grass-fed/organic claims, and brand positioning.

## Brand notes

### Optimum Nutrition Gold Standard: the benchmark

A WPI-led blend with WPC and hydrolysed peptides, 24 g protein in 30.4 g (78.9% density), 5.5 g BCAAs,
sucralose and ace-K, soy lecithin. Widely certified, widely tested, and the cheapest credible
mainstream option at $1.51 per 25 g. Its vanilla SKU is one of the Clean Sixteen (non-detect for all
four heavy metals). The chocolate SKUs are not. This is the default recommendation for most people.

### Dymatize ISO100: the hydrolysate isolate

25 g protein in 32 g, hydrolysed WPI plus WPI, 2.6 g leucine, 5.5 g BCAAs, 120 kcal. Informed Choice.
$2.17 per 25 g. Its Gourmet Vanilla is in the Clean Sixteen. A good choice for lactose-sensitive
lifters who want a fast protein; the hydrolysate premium buys absorption speed, not extra muscle.

### Transparent Labs: certified grass-fed isolate

28 g protein in 34.3 g, stevia, NSF Certified for Sport and Informed Choice, $1.93 per 25 g. One of
the best combinations of certification, formulation and price in the isolate segment.

### Ascent Native Fuel: native whey, every batch tested

25 g protein, stevia, Informed Sport on every batch, $2.07 per 25 g. Native whey has a faster
leucine peak and similar MPS. A strong pick for drug-tested athletes who want a concentrate.

### Legion Whey+: grass-fed isolate with stevia

22 g protein in 26 g, stevia, xanthan gum, sunflower lecithin, NSF/ANSI 173 (contents, not sport),
$2.27 per 25 g. Clean label, good flavour reputation, mid-premium price.

### Naked Whey: one ingredient

25 g protein in 30 g, grass-fed WPC, no sweetener, no flavour, no lecithin, Informed Choice, $1.84 per
25 g. The purest expression of "whey protein" in the dataset. Less pleasant to drink; excellent for
smoothies and cooking.

### Isopure: low-carb isolate

25 g protein in 34 g, sucralose, Informed Choice, $2.18 per 25 g. Its unflavoured SKU is in the Clean
Sixteen. Fine product, unremarkable value.

### Garden of Life Sport: organic grass-fed whey

24 g protein in 33 g, stevia, NSF Certified for Sport, $2.19 per 25 g. The organic whey option. Its
vanilla SKU tested non-detect; the brand's plant line is a separate story and not part of this whey
review.

### Premier Protein: mass-market value

30 g protein in 41 g, sucralose/ace-K, $1.69 per 25 g. CR measured 0.38 µg lead/serving and its
vanilla is in the Clean Sixteen. Cheap, widely available, and better tested than its price suggests.

### BSN Syntha-6: a milkshake, not a protein concentrate

22 g protein in 46 g (47.8% density), 15 g carbs, 6 g fat, 200 kcal, $1.80 per 25 g. Pleasant to
drink, poor protein density, 227 kcal per 25 g of protein. Buy it as a treat or a mass-gaining tool,
not as an efficient protein source.

### Body Fortress: cheapest, with a caveat

30 g protein in 43 g (69.8% density), $0.77 per 25 g. The cheapest labelled protein in the dataset.
But the product lists taurine, creatine and free amino acids, and plaintiffs alleged about 28% of the
labelled protein came from non-whey nitrogen. Its vanilla SKU is in the Clean Sixteen for heavy
metals. If the protein number is inflated, the real cost per gram of whey protein is materially higher
than $0.77.

### Thorne, BPN, Momentous, Klean: clinician and athlete premiums

$2.58-$4.03 per 25 g for 20-25 g isolates with NSF Certified for Sport. Excellent manufacturing and
certification; the price is 1.7-2.7x the mainstream blend. Justified for athletes who need
certification and for people who value the brands' testing transparency. Not justified on protein
quality grounds.

### Myprotein: the value concentrate

21 g protein in 25 g (84% density), sucralose, $1.19 per 25 g on the 1 kg listing. The cheapest
credible concentrate. Certification varies by market and SKU, and brand-direct pricing swings wildly
between sales; the 5.5 lb listings also report inconsistent serving counts, so check the label.

## Cost per gram of protein across forms

Averaging the products in this dataset (unweighted): concentrates and blends cluster at
$0.03-$0.09/g; isolates at $0.077-$0.16/g. The isolate premium is roughly 30-100% per gram of
protein. You are buying lactose removal, lower fat, and often certification, not more protein per
dollar.

## How to shop

1. Decide whether you need isolate (lactose sensitivity, very low calorie) or concentrate/blend
   (everyone else).
2. Set a certification floor: Informed Sport or NSF Certified for Sport if drug-tested; otherwise any
   documented testing.
3. Buy the largest size you will finish.
4. Choose vanilla or unflavoured for daily use.
5. Compute cost per 25 g yourself: `price / (servings x protein) x 25`. Ignore "per serving" claims
   from brands with 20 g servings.
6. Check the ingredient list for free amino acids.

## Bottom line

The best value in the category is a mainstream WPI/WPC blend at roughly $1.50 per 25 g of protein
(Optimum Nutrition Gold Standard), with Myprotein and Premier as cheaper alternatives and Naked as
the single-ingredient option. Isolates and certified grass-fed products cost $1.90-$2.30 and are
worth it for specific needs. Above $2.50 per 25 g you are paying for brand, certification and
convenience, not protein. The cheapest product in the dataset (Body Fortress) is also the one with
the strongest quality caveat, which is the category in miniature: price and quality are correlated,
but not reliably.

## Key sources

All costs are computed from `data/prices.csv` by `analysis/compute_costs.py`; the ranked output is
`data/derived_costs.csv`. Certification status comes from certification registers. Contaminant status
references [S30] and [S31]. Full citations in [references.md](references.md).
