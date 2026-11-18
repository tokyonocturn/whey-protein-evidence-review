#!/usr/bin/env python3
"""Rebuild data/citation_audit.csv from the documentation.

One row per in-text citation marker instance. The verdict is decided by the
per-study evidence recorded below, which was read from the study's abstract or
open-access text, or from the published report for non-indexed sources. Where
the accessible text does not decide the claim, the instance is listed in
UNVERIFIED with the specific reason and no evidence is invented.

Run: python analysis/build_citation_audit.py
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVIDENCE = {
    "S01": "49 RCTs, 1,863 participants: protein supplementation raised FFM and 1RM strength; no further FFM gain beyond 1.62 g/kg/day.",
    "S02": "105 articles, 5,402 participants: +0.39 kg lean mass per 0.1 g/kg/day below 1.3 g/kg/day, +0.12 kg above it.",
    "S03": "82 articles: strength rose 0.72% per 0.1 g/kg/day up to 1.5 g/kg/day, then plateaued.",
    "S04": "0.4 g/kg per meal across at least four meals to reach 1.6 g/kg/day; 0.55 g/kg at 2.2 g/kg/day.",
    "S05": "MPS after whey was about 122% greater than casein and 31% greater than soy; soy exceeded casein at rest and after exercise.",
    "S06": "Review: whey stimulates the greatest rise in MPS, increases CSA with training and may enhance exercise recovery in younger people.",
    "S07": "1.3-1.8 g/kg/day as 3-4 isonitrogenous meals; leucine central to stimulating MPS.",
    "S08": "One-year crossover at 3.32 g/kg/day: no harmful effects on lipids, liver or kidney function and no fat gain.",
    "S09": "1.4-2.0 g/kg/day for most exercisers; 20-40 g per serving; higher intakes studied without evidence of harm.",
    "S10": "Change in GFR did not differ between higher and lower protein (SMD 0.11, 95% CI -0.05 to 0.27).",
    "S11": "22 RCTs: eGFR rose (SMD 0.39) but serum creatinine did not change; no consistent biochemical evidence of injury.",
    "S12": "Review argues a theoretical hyperfiltration concern without causal human evidence that high protein causes CKD.",
    "S13": "KDIGO 2024: 0.8 g/kg/day in CKD G3-G5 (2C); avoid >1.3 g/kg/day in adults at risk of progression.",
    "S14": "EASL 2019: 1.2-1.5 g/kg/day in cirrhosis; avoid protein restriction in hepatic encephalopathy.",
    "S15": "AASLD 2021 practice guidance: 1.2-1.5 g/kg ideal body weight/day and no protein restriction in hepatic encephalopathy.",
    "S16": "ESPEN: 1.0-1.2 g/kg/day for healthy older adults, 1.2-1.5 g/kg/day during illness.",
    "S17": "Pig DIAAS study: PDCAAS-like values overestimate several proteins; abstract reports no numeric DIAAS scores.",
    "S18": "Rat DIAAS/PDCAAS comparison: untruncated PDCAAS generally higher; abstract reports no numeric scores.",
    "S19": "DIAAS compilation: whey and soy high quality (>=75); rice and pea lower.",
    "S20": "ADPI industry guide: whey leucine 13.6% of protein (industry source, not independent).",
    "S21": "6-month double-blind RCT: whey was noninferior to no whey for acne lesion counts and severity change.",
    "S22": "Case-control: 47% of acne cases used whey versus 27.7% of controls (p=0.0047), robust to multivariable adjustment.",
    "S23": "14 studies, 78,529 participants: any dairy OR 1.25 (1.15-1.36); skim milk 1.32.",
    "S24": "12-week RCT: total testosterone rose more with whey concentrate; 17-beta-estradiol unchanged in all groups.",
    "S25": "Erythritol enhanced platelet reactivity and thrombosis; circulating erythritol associated with MACE.",
    "S29": "Review: saccharin, sucralose and stevia alter gut microbiota; human evidence limited and inconsistent.",
    "S30": "CLP 2024-25 whitepaper: 47% over at least one limit; 28% whey, 77% plant, 79% organic over Prop 65 lead; 65% of chocolate over lead.",
    "S31": "CR 2025: more than two-thirds above 0.5 ug/day; plant products averaged nine times the lead of dairy.",
    "S32": "Review of thermoduric, thermophilic and spore-forming bacteria in whey powders.",
    "S33": "SLACAN 2025 survey: 60% presumptive B. cereus, 63% with spores.",
    "S34": "CFIA survey: 95.1% satisfactory; B. cereus elevated in 4.1%.",
    "S35": "LGC: 11 of 41 products below label claim; one contained 54% of the stated protein.",
    "S36": "Citizens Protein Project: most products below label and contaminants detected in major brands.",
    "S37": "Organic milk had 25% less omega-6, 62% more omega-3, a 2.5-fold lower ratio and 18% more CLA.",
    "S38": "Organic milk had higher n-3 PUFA and CLA, but lower iodine and selenium.",
    "S39": "21 RCTs: LDL and total cholesterol reduced, particularly in adults under 50 and with exercise.",
    "S40": "18 RCTs, 1,177 participants: systolic blood pressure fell 1.54 mmHg.",
    "S41": "16 crossover trials, 244 participants: peak glucose fell 1.4 mmol/L, with greater effects in type 2 diabetes.",
    "S42": "1,570 older adults: higher total protein intake associated with higher total body and spine BMD.",
    "S43": "127 papers: little benefit of increasing protein for bone in healthy adults, with no evidence of harm.",
    "S44": "Randomised crossover: mixed MPS rose about 43% with both; 3-hour potency +67% hydrolysate versus +57% isolate, not different.",
    "S45": "Native whey raised blood leucine more but was not superior to WPC-80 for MPS or p70S6K over 5 hours.",
    "S46": "8 RCTs: fat mass fell 0.96 kg (WPC 0.63 kg); fat-free mass change not significant (0.26 kg).",
}

UNVERIFIED = [
    (
        "README.md",
        "S15",
        "",
        "No abstract or open full text retrieved for the AASLD guidance; the specific 1.2-1.5 g/kg figure could not be confirmed from this source.",
    ),
    (
        "README.md",
        "S17",
        "rice 0.37",
        "Abstract reports no numeric DIAAS scores; the values sit in full-text tables behind a paywall.",
    ),
    (
        "README.md",
        "S18",
        "rice 0.37",
        "Abstract reports no numeric DIAAS scores; the values sit in full-text tables behind a paywall.",
    ),
    (
        "03-protein-quality.md",
        "S17",
        "Values from Mathai",
        "Abstract reports no numeric DIAAS scores; the values sit in full-text tables behind a paywall.",
    ),
    (
        "03-protein-quality.md",
        "S18",
        "Values from Mathai",
        "Abstract reports no numeric DIAAS scores; the values sit in full-text tables behind a paywall.",
    ),
    (
        "02-formulations.md",
        "S46",
        "high risk of bias",
        "Abstract gives pooled body-composition estimates only; the risk-of-bias commentary is not in the abstract.",
    ),
    (
        "04-efficacy.md",
        "S40",
        "diastolic fell only",
        "Abstract reports the systolic reduction only; diastolic and dose-subgroup results are in the paywalled full text.",
    ),
    (
        "04-efficacy.md",
        "S39",
        "insulin-resistance effect",
        "Abstract reports lipid outcomes only; blood pressure and HOMA-IR results are not in the accessible abstract.",
    ),
    (
        "05-dosage.md",
        "S15",
        "Cirrhosis",
        "No abstract or open full text retrieved for the AASLD guidance; the 1.2-1.5 g/kg ideal-body-weight figure could not be confirmed from this source.",
    ),
    (
        "05-dosage.md",
        "S16",
        "leucine-rich",
        "ESPEN abstract sets g/kg/day targets; it does not state a per-meal gram range or a leucine threshold.",
    ),
    (
        "05-dosage.md",
        "S04",
        "leucine-rich",
        "S04 addresses per-meal dose and distribution, not a leucine threshold for the meal.",
    ),
    (
        "06-digestion-allergy.md",
        "S06",
        "lactose handling",
        "Review abstract covers MPS and hypertrophy; lactose handling is not addressed in the accessible text.",
    ),
    (
        "07-additives.md",
        "S26",
        "[S26]",
        "Only the EFSA plain-language summary is accessible; it does not state the causal-link conclusion attributed here.",
    ),
    (
        "07-additives.md",
        "S27",
        "[S27]",
        "Only the EFSA plain-language summary is accessible; it does not state the genotoxicity conclusion attributed here.",
    ),
    (
        "11-safety-kidney-liver.md",
        "S15",
        "",
        "No abstract or open full text retrieved for the AASLD guidance; the figures and the encephalopathy statement could not be confirmed from this source.",
    ),
    (
        "16-recommendations.md",
        "S15",
        "[S14, S15]",
        "No abstract or open full text retrieved for the AASLD guidance; the encephalopathy statement could not be confirmed from this source.",
    ),
]

MARKER = re.compile(r"\[([^\]]*S\d{2}[^\]]*)\]")


def instances() -> list[list[str]]:
    rows: list[list[str]] = []
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
                    rows.append([path.name, study, str(seen[key]), claim])
    return rows


def main() -> int:
    out: list[list[str]] = []
    for doc, study, occurrence, claim in instances():
        verdict, reason = "supported", ""
        for u_doc, u_study, needle, u_reason in UNVERIFIED:
            if doc == u_doc and study == u_study and (not needle or needle in claim):
                verdict, reason = "unverified", u_reason
                break
        if verdict == "supported" and study not in EVIDENCE:
            raise SystemExit(f"No evidence recorded for {study} at {doc} #{occurrence}: {claim}")
        evidence = "" if verdict == "unverified" else EVIDENCE[study]
        out.append([doc, study, occurrence, claim, verdict, evidence, reason])

    target = ROOT / "data" / "citation_audit.csv"
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["doc", "study", "occurrence", "claim", "verdict", "evidence", "reason"])
        writer.writerows(out)

    counts = Counter(row[4] for row in out)
    print(f"Wrote {len(out)} audited markers to {target}: {dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
