# Protein quality: PDCAAS, DIAAS, amino acids, leucine and digestibility

"High quality protein" is not a marketing phrase. It has a definition: a protein is high quality if
it delivers all nine indispensable (essential) amino acids in adequate amounts, in a form that is
digested and absorbed. Whey does that better than almost any other food protein. The interesting
questions are *how much better*, *whether the difference matters*, and *where the measurement is
being gamed*.

## The two scoring systems

**PDCAAS** (Protein Digestibility-Corrected Amino Acid Score) compares the amino acid profile of a
protein with a reference pattern, corrects for faecal crude-protein digestibility, and **truncates
the result at 1.00**. That truncation is why every decent protein scores 1.00 and the score stops
being useful: whey, casein, egg, soy and milk protein all hit the ceiling.

**DIAAS** (Digestible Indispensable Amino Acid Score) is the FAO-recommended replacement. It uses
true ileal digestibility for each individual amino acid rather than one faecal value for crude
protein, and it does **not** truncate, so proteins can score above 100 and be ranked against each
other.

| Protein | PDCAAS | DIAAS | First-limiting amino acid |
|---|---|---|---|
| Micellar casein | 1.00 | 1.17 | none |
| Milk protein concentrate | 1.00 | 1.18 | none |
| Whole milk | 1.00 | 1.43 | none |
| Egg | 1.00 | 1.13 | none |
| **Whey protein isolate** | **1.00** | **1.09** | histidine (DIAAR 1.09) |
| **Whey protein concentrate** | **1.00** | **0.97** | histidine |
| Soy protein isolate | 0.98 | 0.90 | methionine + cysteine |
| Pea protein concentrate | 0.89 | 0.82 | methionine + cysteine |
| Rice protein concentrate | 0.42 | 0.37 | lysine |
| Collagen | 0.00 | 0.00 | tryptophan |

Values from Rutherfurd et al. 2015 [S18], reproduced in the ADPI Protein Quality Guide [S20].
Mathai et al. 2017 likewise found that PDCAAS overstates the quality of dairy and plant proteins
relative to DIAAS [S17]. Note the detail that marketing rarely mentions: **WPI (1.09) scores higher than WPC
(0.97)** on DIAAS, because the isolate's lower ash and lactose content leaves a purer protein
fraction. Both are excellent; the isolate is marginally better.

What DIAAS does not mean: a score of 0.97 does not mean 3% of the protein is wasted in any practical
sense, and it does not mean a WPC product is inferior for muscle. It means that if WPC were the
*only* protein in the diet, histidine would become limiting slightly earlier than it would with
isolate. In a mixed diet, that is irrelevant.

## The amino acid profile of whey

Whey's strength is not one amino acid but the combination: a complete profile, high essential amino
acid content (about 50% of total protein), and the highest leucine content of any common protein.

Typical composition, grams per 100 g of protein (`data/amino_acids.csv`):

| Amino acid | g/100 g | Class |
|---|---|---|
| Leucine | 10.6 | essential, BCAA |
| Isoleucine | 6.1 | essential, BCAA |
| Valine | 5.8 | essential, BCAA |
| Lysine | 9.4 | essential |
| Threonine | 6.6 | essential |
| Phenylalanine | 3.2 | essential |
| Methionine | 2.1 | essential |
| Histidine | 1.7 | essential |
| Tryptophan | 1.7 | essential |
| Cysteine | 2.3 | conditionally essential |
| Glutamic acid | 16.8 | nonessential |
| Aspartic acid | 10.8 | nonessential |

Derived totals from the validation script: essential amino acids about **52.5 g/100 g**, BCAAs about
**22.5 g/100 g**, leucine **10.6 g/100 g**. That works out to **2.65 g leucine per 25 g of whey
protein**, which matches label claims: Dymatize states 2.6 g leucine per 25 g serving, and Optimum
Nutrition states 5.5 g BCAAs per 24 g serving.

The ADPI Protein Quality Guide puts whey's leucine content even higher, at 13.6%, and notes that
plant proteins sit at 6-8% and most animal proteins at 8.5-9%. The discrepancy with the 10.6% figure
reflects different analytical datasets and products; the practical range is **10-13% of protein**,
and the conclusion is the same: whey is the most leucine-dense common protein.

## Why leucine matters, and how much is enough

Leucine is the amino acid that most directly activates mTORC1 and initiates muscle protein synthesis.
The threshold concept: a meal needs enough leucine to raise blood leucine above a per-person
threshold, roughly **2-3 g** in young adults and possibly more in older adults because of anabolic
resistance.

2.65 g of leucine per 25 g of whey protein clears that threshold comfortably. This is why 20-25 g of
whey is treated as a minimum effective dose and why 20-25 g of a lower-leucine plant protein is not
equivalent without fortification or a larger dose. It is also why "leucine spiking" (adding free
leucine) is a real, if usually unnecessary, strategy in plant proteins.

## Digestibility and bioavailability

Whey is a "fast" protein: it leaves the stomach quickly, produces a sharp aminoacidemia peak at
roughly 60-90 minutes, and is largely absorbed by 3-4 hours. Casein is slow and flat. That kinetic
difference is the mechanistic basis for whey's higher acute MPS response [S05].

Bioavailability claims deserve scepticism. "Biological value" (BV) numbers circulating online (whey
104, casein 77, soy 74) come from older rat and nitrogen-balance work with methodological problems.
DIAAS is the better instrument. The honest summary: whey is highly digestible and its amino acids are
well absorbed; the differences between whey forms are small; the differences between whey and most
plant proteins are real but can be closed by blending or increasing the dose.

## Where quality claims get gamed

1. **Nitrogen spiking.** Protein is measured as nitrogen x 6.25, so glycine, taurine, creatine and
   free amino acids inflate the number without adding intact protein. See doc 02 and doc 07.
2. **"Amino acid profile" panels that list added aminos.** If the panel includes glycine or taurine
   at implausible levels for whey, they were added.
3. **"100% whey" with a blend of isolates and hydrolysates.** Legal, but the front label implies a
   single ingredient.
4. **PDCAAS 1.0 as a differentiator.** Every decent protein gets 1.0 because of truncation. It is not
   a comparison.
5. **"Enzyme-treated for 99% absorption."** Digestibility claims without a method (DIAAS? true ileal
   digestibility? in vitro?) are unverifiable.

## Bottom line

Whey is a genuinely high-quality protein: DIAAS 1.09 for isolate and 0.97 for concentrate, complete
amino acid profile, about 2.6 g leucine per 25 g, fast digestion. The quality gap between whey forms
is small; the gap between whey and unfortified plant protein is real but manageable. Once total daily
protein is adequate, protein quality differences stop being the limiting factor for muscle gain
[S01, S02]. Quality is a tiebreaker when choosing a powder, not the main event.
