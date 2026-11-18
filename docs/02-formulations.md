# Concentrate, isolate, hydrolysate, native: what the labels actually mean

Whey is the liquid fraction left after casein curds form in cheese or casein manufacture. That
liquid is roughly 93% water, 0.6-0.9% protein, and most of the lactose and minerals. Drying it gives
whey powder; processing it further gives the products sold as protein supplements. The differences
between "whey protein concentrate", "whey protein isolate", "hydrolysed whey" and "native whey" are
**processing differences that change composition**, not different proteins with different anabolic
power.

## The four commercial forms

### Whey protein concentrate (WPC)

WPC is whey filtered by ultrafiltration to remove water, lactose, ash and some fat. The number on the
bag is the protein content on a dry basis:

| Grade | Protein | Lactose | Fat | Ash | Typical use |
|---|---|---|---|---|---|
| WPC 34 | 34-36% | 48-55% | low | high | Food ingredient, ice cream, infant formula |
| WPC 50 | 50-52% | 33-37% | moderate | moderate | Food ingredient, some budget powders |
| WPC 80 | 80-82% | 4-8% | 4-8% | 3-4% | The standard sports protein |

Industry specifications are published by the American Dairy Products Institute and the US Dairy
Export Council. WPC 80 is what almost every "whey protein" tub contains unless it says isolate. It
retains some fat and lactose, which is why it tastes better and mixes thicker than isolate.

### Whey protein isolate (WPI)

WPI is WPC that has been further processed by microfiltration, ultrafiltration/diafiltration or ion
exchange to reach **at least 90% protein**, with lactose around 0.5-1% and fat around 0.5-1%. The
extra step exists specifically to strip lactose and soluble minerals. That is the entire nutritional
case for isolate: more protein per gram of powder, less lactose, less fat, fewer calories per gram
of protein.

Isolate is not automatically "cleaner" or better absorbed. It is a more concentrated ingredient.

### Whey protein hydrolysate (WPH)

Hydrolysate is whey protein treated with enzymes (trypsin, chymotrypsin, pepsin, or microbial
proteases) to break peptide bonds into shorter peptides and free amino acids. The result is absorbed
faster and produces a higher, earlier peak in blood amino acids. It also tastes bitter, which is why
hydrolysates are usually blended with isolate and heavily flavoured, and why they cost more.

"Hydrolysed" is a real processing claim, but the degree of hydrolysis varies enormously and is
rarely disclosed. A product can call itself hydrolysed with a token percentage of WPH in the blend.

### Native whey

Native whey is produced by microfiltering **skim milk** directly rather than by recovering whey from
cheese manufacture. Because it never goes through the cheese vat's heat and acid steps, it retains
more of the intact, undenatured whey proteins (beta-lactoglobulin, alpha-lactalbumin,
lactoferrin, immunoglobulins) and has a higher leucine content per gram of protein in some
comparisons. Trials show native whey produces a faster and higher leucinaemia than WPC 80, but the
one head-to-head muscle protein synthesis trial found **no difference in MPS** between native whey
and WPC 80 over five hours [S06, S07].

## What actually differs, in numbers

Using the label data in `data/products.csv`:

| Product | Form | Protein per 100 g of powder | Protein per serving | Calories per 25 g protein |
|---|---|---|---|---|
| Transparent Labs Grass-Fed Isolate | isolate | 81.6 g | 28 g | not disclosed |
| Legion Whey+ | isolate | 84.6 g | 22 g | 114 |
| Myprotein Impact Whey | concentrate | 84.0 g | 21 g | not disclosed |
| Naked Whey | concentrate | 83.3 g | 25 g | 120 |
| Optimum Nutrition Gold Standard | blend | 79.0 g | 24 g | 135 |
| Dymatize ISO100 | hydrolysate/isolate | 78.1 g | 25 g | 120 |
| BSN Syntha-6 | blend | 47.8 g | 22 g | 227 |

The spread in protein density between a good concentrate and an isolate is smaller than marketing
suggests: 80-85% versus 85-90% for the powdered ingredient, and much less at the finished-product
level once flavourings and fillers are added. A 24 g serving from a 79%-protein blend and a 25 g
serving from a 78%-protein hydrolysate blend are, for practical purposes, the same dose.

## Does the form change outcomes?

**Muscle protein synthesis.** Whey, casein and soy given as 10 g essential amino acids produced
different MPS responses: whey roughly doubled the casein response at rest and after resistance
exercise, and beat soy after exercise [S05]. That is a *protein source* difference (whey is rapidly
digested and leucine-rich), not a concentrate-versus-isolate difference. Within whey, WPH and intact
whey produced statistically similar MPS (+67% vs +57%) in a randomised crossover trial [S06].

**Strength and body composition.** A meta-analysis of concentrated, hydrolysed and isolated whey
found fat-mass reduction with WPC but **no significant effect on fat-free mass in any subgroup**
[S02]. The authors flagged high risk of bias and small study numbers. Hydrolysate has not
demonstrated superior long-term hypertrophy in adequately controlled trials.

**Recovery.** One small trial found faster recovery of peak torque after eccentric exercise with
hydrolysed whey versus isolate [S06]; a systematic review of protein and exercise-induced muscle
damage found the evidence too inconsistent to recommend hydrolysate over intact whey.

**Lactose.** This is the one difference that reliably matters to consumers: WPC 80 carries roughly
1.2-2.4 g lactose per 30 g scoop, WPI about 0.15-0.3 g. Details in
[06-digestion-allergy.md](06-digestion-allergy.md).

## Blends, peptides and "whey matrix" claims

Many best-selling products are blends of WPI, WPC and WPH. A blend is not a compromise: mixing
isolate with concentrate can improve taste and mouthfeel at a lower cost than all-isolate, while
keeping protein density around 78-80%. The label tells you the order of ingredients by weight, so
"whey protein isolate" first means isolate predominates.

"Whey peptides" on a label usually means a small amount of hydrolysed whey added for marketing or
mixability, not a therapeutic dose. Unless the ingredient list shows a specific hydrolysed fraction
with a percentage, treat "peptides" as flavour text.

## Protein spiking: when the form on the label is not the protein in the tub

Protein content is usually measured as total nitrogen x 6.25. Any nitrogen-containing compound
inflates that number: glycine (about 19% nitrogen), taurine, creatine, glutamine, and free amino
acids. Adding these is cheaper than adding whey, and it lets a product declare more protein than it
contains as intact protein.

This is not hypothetical. In *Gubala v. CVS*, a lab report alleged a 26 g claim contained about
21.8 g of whey protein, with the rest from free amino acids. In *Porter v. NBTY*, plaintiffs alleged
roughly 28% of Body Fortress's labelled protein came from glycine, threonine, glutamine, BCAAs,
taurine and creatine. The court allowed the misleading-labelling claims to proceed; the case ended
without a public judgment. Regulators have a hook here: 21 CFR 101.36 states that protein **shall
not be declared** on labels of products that contain only individual amino acids.

Practical test: if the ingredient list names individual amino acids (glycine, taurine, glutamine,
creatine, or "BCAA blend") in a product marketed as whey, the grams on the front are not all whey.
That does not make the product unsafe, but it does make the cost per gram of real protein worse than
the label implies.

## Which form is worth buying

| Buyer | Best form | Why |
|---|---|---|
| Most people who tolerate dairy | WPC 80 or a WPI/WPC blend | Cheapest per gram of protein; taste and mixability are better; the anabolic difference is negligible |
| Lactose-sensitive | WPI, or WPI-dominant blend | 5-15x less lactose per serving |
| Wants lowest calorie per gram of protein | WPI | Less fat and carbohydrate per gram of protein |
| Diagnosed cow's milk protein allergy | **None of these** | Whey isolate still contains milk protein; see doc 06 |
| Drug-tested athlete | Any form, but certification matters more than form | Choose NSF Certified for Sport or Informed Sport |
| Budget-constrained | WPC 80 or blend | Isolate premium buys lactose removal, not extra muscle |

The hydrolysate premium is the weakest value proposition in the category. You pay 30-50% more per
gram of protein for faster aminoacidemia that has not translated into better hypertrophy or strength
in controlled trials. It is defensible for a lactose-sensitive athlete who wants the fastest possible
post-workout amino acid peak, and for people who find intact whey bloating; it is not necessary for
anyone else.
