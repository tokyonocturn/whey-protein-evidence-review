# Limitations, uncertainties and how to read this review

## The biggest limitation: no primary testing

This review did not commission laboratory assays. Every contamination figure is a synthesis of
someone else's measurements, with different methods, sample sizes, detection limits and benchmarks.
That is enough to rank categories and products **relative to each other**, and it is not enough to
tell you that a specific tub is safe.

If you need product-level assurance, look for a lot-specific certificate from an accredited lab, or
choose a product that appears in the Clean Sixteen or in Consumer Reports' low-lead results.

## Advocacy data is used for ranking, not absolute risk

The Clean Label Project and Consumer Reports are advocacy organisations. Their testing is useful
because it is independent of the brands, and it is limited because:

- Sample sizes are small relative to the market (160 products, 23 products, 5 products).
- Benchmarks differ: Prop 65's 0.5 µg/day lead MADL is far stricter than FDA's 2.2 µg/day interim
  reference level for children.
- Cohort-level percentages cannot be converted into a risk estimate for an individual.
- Publication is selected for newsworthiness; products with unremarkable results get less attention.

The correct use of these data is: **plant worse than whey, chocolate worse than vanilla, organic not
protective, and some cheap products are cleaner than expensive ones.**

## Label data is not lab-verified

Macros and ingredient lists were transcribed from manufacturer and retailer pages. Independent
surveys find that 5-30% of products are off-label to some degree, usually modestly and occasionally
severely. Where a product's label is central to a conclusion (protein density, amino acid spiking),
the review says so and cites the underlying dispute.

## Prices are a snapshot

Prices were captured in November 2026 (some March and June 2026). They move daily, vary by flavour,
seller and subscription, and differ by country. The **ranking** is more stable than the absolute
numbers, and the method (`analysis/compute_costs.py`) lets you recompute with today's prices.

## Flavour coverage is incomplete for some brands

Optimum Nutrition's full 24-flavour list was captured. Dymatize, Legion, Ascent and Transparent Labs
publish rotating and market-specific lists, and only a subset could be confirmed. Those rows are
marked `partial`. Per-flavour macros are marked `verified` only where the label was read; `varies`
rows document what changes without inventing numbers.

## The evidence base has structural weaknesses

- Most whey trials are small (n < 30), short (4-12 weeks), and enrol young trained men.
- Many are funded by dairy or supplement companies.
- Surrogate outcomes (acute MPS) are more common than hard outcomes (lean mass, strength, health
  events).
- Publication bias favours positive findings.
- The Morton breakpoint (1.62 g/kg) comes from a meta-regression with wide confidence intervals
  (1.03-2.20); it is a population average, not an individual prescription.

## Contested areas

| Question | State of evidence | This review's position |
|---|---|---|
| Do very high protein intakes damage healthy kidneys over decades? | No long-term RCT; mechanistic concern | Probably safe at 1.2-2.2 g/kg; uncertain above 2.5 g/kg |
| Does erythritol increase cardiovascular risk? | One intervention study plus associations; EFSA found no causal link | Avoid excessive intake if concerned; not a reason to reject a product |
| Does whey worsen acne? | Case-control positive, RCT negative | Possible individual susceptibility; trial elimination |
| Is hydrolysate worth the premium? | Faster absorption, similar MPS | No for most; yes for specific needs |
| Is organic safer? | No for heavy metals; modest fatty acid benefit in milk | Not a safety purchase |
| Do sweeteners harm the microbiome? | Animal signals, limited human data | Low concern at typical doses |

## What this review cannot tell you

- Whether a specific tub you own is contaminated.
- Whether you personally will tolerate a product.
- Your individual protein requirement (that needs a dietitian and your medical history).
- Whether a brand will reformulate next month.
- Whether a certification will still be valid at the lot level.

## How to use the datasets

- `data/products.csv`: label composition for 16 products.
- `data/prices.csv`: prices with retailer, date and basis.
- `data/derived_costs.csv`: computed cost metrics, ranked.
- `data/flavors.csv`: 56 flavour entries with ingredient and allergen flags.
- `data/amino_acids.csv`: typical whey amino acid composition.
- `data/contaminants.csv`: study-level laboratory findings.
- `data/recalls.csv`: recalls and enforcement actions.
- `data/certifications.csv`: certification programme comparison.
- `data/studies.csv`: 46 studies with design, result and certainty.

Every derived number can be regenerated with two standard-library Python scripts. If a number in a
document disagrees with the CSV, the CSV and the script win; please open an issue.

## A note on medical advice

This is an evidence review, not medical advice. Protein intake interacts with kidney disease, liver
disease, pregnancy, bariatric surgery, eating disorders and drug interactions. If any of those apply
to you, the relevant guideline in doc 11 is a starting point for a conversation with a clinician, not
a prescription.

## Key sources

Evidence weights are recorded in `data/studies.csv` ([S01]-[S46]); laboratory and regulatory sources
are in `data/contaminants.csv` and [references.md](references.md). The contested-claims table above
reflects the balance of those sources, not a single study.

## Corrections

Formulations, prices and test results change. Corrections with a source are welcome; the repository
is designed so that a single CSV edit plus a rerun of the scripts updates every derived table.
