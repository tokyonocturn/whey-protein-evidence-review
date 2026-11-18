# Flavours: what changes, and what it tells you

Flavour is not cosmetic. It changes the ingredient list, the allergen declarations, the calorie and
carbohydrate content, and, most importantly, the **heavy metal load**, because cocoa is the single
biggest contaminant driver in protein powders.

This review captured **56 flavour entries across six product lines** in `data/flavors.csv`: Optimum
Nutrition Gold Standard (24), Dymatize ISO100 (10), Legion Whey+ (7), Isopure Low Carb (6), Ascent
Native Fuel (5) and Transparent Labs Grass-Fed Isolate (4). Flavour lists rotate and vary by market;
`list_status` marks whether the manufacturer's full published list was captured.

## The five flavour families, and what they add

| Family | Examples | What is added | Main consequence |
|---|---|---|---|
| Chocolate | Double Rich Chocolate, Dutch Chocolate, Fudge Brownie | Cocoa powder, cocoa butter, chocolate flavour | **Higher cadmium and lead**; +10-25 kcal; +1-2 g carbs |
| Vanilla/cream | French Vanilla, Vanilla Ice Cream, Creamy Vanilla | Vanilla flavour, cream flavour, sometimes dairy creamer | Lowest contaminant load; lowest calories |
| Fruit/cream | Strawberry, Banana Cream, Strawberries & Cream | Fruit flavour, acid, colour | Colourings; little macro change |
| Coffee | Cappuccino, Café Mocha, Caramel Macchiato | Instant coffee, cocoa in mocha | Small caffeine dose; cocoa risk in mocha |
| Cookies/baked/cereal | Cookies & Cream, S'Mores, Cinnamon Roll, Cocoa Pebbles | Cookie pieces, wheat flour, sugar, cocoa | **Gluten**, sugar, cocoa; highest carb count |
| Caramel/nut | Salted Caramel, Chocolate Peanut Butter | Caramel flavour, peanut flour, hazelnut | Peanut/tree nut allergens; +fat |

Unflavoured products are a separate category: no sweetener, no flavour, no gums (in the case of Naked
Whey and Isopure Unflavoured) and, in independent testing, the lowest contaminant levels.

## The cocoa problem

Cocoa plants accumulate cadmium from soil and lead from dust and processing. That is why chocolate
products consistently test worse:

- Clean Label Project's 2025 study found **65% of chocolate-flavoured protein powders exceeded the
  Prop 65 lead benchmark**, versus 28% of whey products overall, and reported that chocolate powders
  carried about **4x the lead of vanilla** and, in its category summary, up to **110x the cadmium of
  vanilla** formulations.
- Consumer Reports' 2025 testing found no meaningful difference between average lead in chocolate
  and vanilla across its sample, but its highest-lead products were plant-based and several were
  chocolate. The two datasets disagree on magnitude, not on direction.
- The Clean Label Project's "Clean Sixteen" (non-detect for lead, cadmium, arsenic and mercury) is
  dominated by **vanilla and unflavoured** products, including ON Gold Standard Vanilla Ice Cream,
  Dymatize ISO100 Gourmet Vanilla, Isopure Unflavoured, Premier Protein Vanilla, Garden of Life Grass
  Fed Whey Vanilla and Body Fortress Vanilla.

Practical rule: **if you use a powder daily, choose vanilla or unflavoured. Treat chocolate as an
occasional flavour.** This single switch does more for contaminant exposure than changing brands.

## Sweetener systems by brand

| Brand / line | Sweetener | Notes |
|---|---|---|
| Optimum Nutrition Gold Standard | Sucralose + acesulfame K | Classic artificial system; some flavours also contain cellulose gum |
| Dymatize ISO100 | Sucralose + acesulfame K | Hydrolysed isolate base |
| BSN Syntha-6 | Sucralose + acesulfame K | Higher fat/carb blend |
| Body Fortress | Sucralose + acesulfame K | Also contains taurine/creatine |
| Premier Protein | Sucralose + acesulfame K | Mass-market |
| Isopure | Sucralose | Low-carb isolate |
| Myprotein Impact | Sucralose (some flavours stevia) | Sweetener varies by flavour |
| Transparent Labs | Stevia (steviol glycosides) | No artificial sweetener |
| Legion Whey+ | Stevia (steviol glycosides + Reb A) | Xanthan gum, sunflower lecithin |
| Ascent Native Fuel | Stevia | Informed Sport |
| Garden of Life Sport | Stevia | Organic line |
| Thorne, Klean, Momentous, BPN | Stevia and/or monk fruit | Clinician/athlete channels |
| Naked Whey | None | Single ingredient |

This is a genuine preference axis: if you want to avoid synthetic sweeteners, the stevia/monk fruit
lines are a coherent choice, and they are also the lines most likely to hold sport certification. You
pay for it: the stevia-sweetened isolates in our cost table run $1.93-$4.03 per 25 g of protein
versus $1.51 for the sucralose-sweetened market leader.

## Allergen differences between flavours

The base powder is dairy. Flavours add:

- **Soy** (lecithin) in most mass-market lines.
- **Wheat/gluten** in cookies, cereal, cinnamon roll, malt and s'mores flavours.
- **Peanut** in chocolate peanut butter.
- **Tree nut** in hazelnut, coconut and rocky road.
- **Milk** always, and sometimes additional dairy creamers.

A "gluten-free" claim on the base product does not automatically extend to every flavour. If you have
coeliac disease, check the specific flavour's allergen panel, not the brand's home page.

## Do flavours change protein content?

Rarely by much, and usually downward. Flavour powders, cocoa, salt and sweeteners displace protein:

- ON Gold Standard: 24 g protein in 30.4 g across flavours; chocolate versions are about 130 kcal,
  vanilla about 120 kcal.
- Dymatize ISO100: 25 g protein in 32 g; chocolate 120 kcal, cookie/cereal flavours about 130-140.
- Legion Whey+: 22 g in 26 g; 100 kcal for most flavours, 110 for cookies and peanut butter.

The pattern across the dataset: **chocolate and inclusion flavours add 10-30 kcal and 1-3 g of
carbohydrate per serving; fruit and vanilla flavours are closest to the base.** If you are counting
calories precisely, the flavour is worth 5-10% of the serving.

## Flavour list completeness

| Brand | Flavours captured | Status |
|---|---|---|
| Optimum Nutrition Gold Standard | 24 | Complete as published |
| Dymatize ISO100 | 10 | Partial: seasonal and licensed flavours rotate |
| Legion Whey+ | 7 | Partial |
| Isopure Low Carb | 6 | Complete for the Low Carb line |
| Ascent Native Fuel | 5 | Partial |
| Transparent Labs Grass-Fed Isolate | 4 | Partial |

Where `data_status` is `varies`, the row documents what the flavour adds but not an exact panel,
because the manufacturer's page renders nutrition dynamically. Those rows are marked rather than
guessed.

## Buying advice by flavour

1. **Daily driver:** vanilla or unflavoured. Lowest contaminants, lowest calories, least allergen
   complexity.
2. **Occasional treat:** chocolate, cookies and cream, peanut butter. Accept the cocoa and allergen
   load.
3. **Coffee flavours:** fine, but check caffeine if you are sensitive; mocha contains cocoa.
4. **Fruit flavours:** useful for people who dislike creamy textures; watch for colourings.
5. **Unflavoured:** best for cooking, smoothies and stacking with your own flavours; also the best
   choice if you want to inspect the protein itself.

## Bottom line

Flavour is a real nutritional variable, not a marketing detail. Chocolate flavours carry more
cadmium and lead; cookie and cereal flavours add gluten and sugar; nut flavours add allergens;
vanilla and unflavoured are the cleanest and lowest-calorie options. If you use whey every day,
make vanilla or unflavoured your default and treat the rest as rotation.

## Key sources

Flavour composition is transcribed from manufacturer labels in `data/flavors.csv`. Contaminant
contrasts between chocolate and vanilla come from [S30] and [S31]; full citations are in
[references.md](references.md).
