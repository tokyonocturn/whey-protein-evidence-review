#!/usr/bin/env python3
"""Rebuild data/citation_audit.csv from the documentation.

One row per in-text citation marker instance, with the source actually used to
decide the verdict: the study's reference URL, or the open-access full text when
the abstract was not decisive. `basis` records which of those was read.

Where the accessible text still does not decide the claim, the instance is
listed in UNVERIFIED with the specific reason and no evidence is invented.

Run: python analysis/build_citation_audit.py
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# URL used for the verdict: open-access full text or published report where one
# was read, otherwise the reference URL from docs/references.md.
FULL_TEXT = {
    "S04": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5828430/",
    "S06": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2901380/",
    "S15": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9134787/",
    "S16": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4208946/",
    "S18": "https://jn.nutrition.org/article/S0022-3166(22)08633-3/fulltext",
    "S26": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10731997/",
    "S27": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12041894/",
    "S30": "https://cleanlabelproject.org/wp-content/uploads/CleanLabelProject_ProteinStudyWhitepaper_010625.pdf",
    "S31": "https://www.consumerreports.org/lead/protein-powders-and-shakes-contain-high-levels-of-lead-a4206364640",
    "S35": "https://protein.wetestyoutrust.com/sites/default/files/2025-05/IP_Supplements_Product_Survey_UK_MAY_2025.pdf",
    "S46": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6769754/",
}

BASIS = {
    "S04": "full text",
    "S06": "full text",
    "S15": "full text",
    "S16": "full text",
    "S18": "full text",
    "S26": "full text",
    "S27": "full text",
    "S30": "report",
    "S31": "report",
    "S33": "report",
    "S34": "report",
    "S35": "report",
    "S36": "report",
    "S39": "not accessible",
    "S40": "not accessible",
    "S46": "full text",
}

EVIDENCE = {
    "S01": "49 RCTs, 1,863 participants: protein supplementation raised FFM and 1RM strength; no further FFM gain beyond 1.62 g/kg/day.",
    "S02": "105 articles, 5,402 participants: +0.39 kg lean mass per 0.1 g/kg/day below 1.3 g/kg/day, +0.12 kg above it.",
    "S03": "82 articles: strength rose 0.72% per 0.1 g/kg/day up to 1.5 g/kg/day, then plateaued.",
    "S04": "Full text: 0.4 g/kg per meal across at least four meals to reach 1.6 g/kg/day, with 2.2 g/kg/day as the upper intake; whey is absorbed at about 10 g/hour.",
    "S05": "MPS after whey was about 122% greater than casein and 31% greater than soy; soy exceeded casein at rest and after exercise.",
    "S06": "Full text: WPI contains very little lactose, which may matter for people with lactose intolerance.",
    "S07": "1.3-1.8 g/kg/day as 3-4 isonitrogenous meals; leucine central to stimulating MPS.",
    "S08": "One-year crossover at 3.32 g/kg/day: no harmful effects on lipids, liver or kidney function and no fat gain.",
    "S09": "1.4-2.0 g/kg/day for most exercisers; 20-40 g per serving; higher intakes studied without evidence of harm.",
    "S10": "Change in GFR did not differ between higher and lower protein (SMD 0.11, 95% CI -0.05 to 0.27).",
    "S11": "22 RCTs: eGFR rose (SMD 0.39) but serum creatinine did not change; no consistent biochemical evidence of injury.",
    "S12": "Review argues a theoretical hyperfiltration concern without causal human evidence that high protein causes CKD.",
    "S13": "KDIGO 2024: 0.8 g/kg/day in CKD G3-G5 (2C); avoid >1.3 g/kg/day in adults at risk of progression.",
    "S14": "EASL 2019: 1.2-1.5 g/kg/day in cirrhosis; avoid protein restriction in hepatic encephalopathy.",
    "S15": "Full text, guidance 21 and 23: 1.2-1.5 g/kg ideal body weight/day, and protein should not be restricted in HE.",
    "S16": "Full text: 1.0-1.2 g/kg/day for healthy older adults and 1.2-1.5 g/kg/day in illness; a higher proportion of leucine is required for optimal MPS with age.",
    "S17": "Abstract: PDCAAS-like values overestimate protein quality relative to DIAAS.",
    "S18": "Table 5: DIAAS 1.09 WPI, 0.973 WPC, 0.898 soy isolate, 0.822 pea concentrate, 0.371 rice concentrate.",
    "S19": "DIAAS compilation: whey and soy high quality (>=75); rice and pea lower.",
    "S20": "ADPI industry guide: whey leucine 13.6% of protein (industry source, not independent).",
    "S21": "6-month double-blind RCT: whey was noninferior to no whey for acne lesion counts and severity change.",
    "S22": "Case-control: 47% of acne cases used whey versus 27.7% of controls (p=0.0047), robust to multivariable adjustment.",
    "S23": "14 studies, 78,529 participants: any dairy OR 1.25 (1.15-1.36); skim milk 1.32.",
    "S24": "12-week RCT: total testosterone rose more with whey concentrate; 17-beta-estradiol unchanged in all groups.",
    "S25": "Erythritol enhanced platelet reactivity and thrombosis; circulating erythritol associated with MACE.",
    "S26": "Full text: the available evidence does not demonstrate a causal relationship between dietary erythritol and cardiovascular risk.",
    "S27": "Full text: acesulfame K does not raise a concern for genotoxicity; ADI 15 mg/kg body weight/day.",
    "S29": "Review: saccharin, sucralose and stevia alter gut microbiota; human evidence limited and inconsistent.",
    "S30": "2024-25 whitepaper: 47% over at least one limit; 28% whey, 77% plant, 79% organic over Prop 65 lead; 65% of chocolate over lead.",
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
    "S46": "Full text: only one included trial was at low risk of bias; the authors describe low methodological quality and small samples.",
}

RECOVERY_EVIDENCE = (
    "Full text: 25 g whey hydrolysate restored peak isometric torque by 6 h, while the isolate "
    "and placebo groups were still depressed at 24 h."
)

# Claims from one study that need a different supporting sentence than the default.
ROW_EVIDENCE = [
    ("02-formulations.md", "S06", "Recovery", RECOVERY_EVIDENCE),
    ("04-efficacy.md", "S06", "Hydrolysed whey", RECOVERY_EVIDENCE),
]

UNVERIFIED = [
    (
        "04-efficacy.md",
        "S39",
        "insulin-resistance effect",
        "Abstract reports lipid outcomes only; the full text is paywalled, so the blood pressure and HOMA-IR null result could not be read.",
    ),
    (
        "04-efficacy.md",
        "S40",
        "diastolic fell only",
        "Abstract reports the systolic reduction only; no open-access full text exists, so the diastolic dose-subgroup claim could not be read.",
    ),
]

MARKER = re.compile(r"\[([^\]]*S\d{2}[^\]]*)\]")


def reference_urls() -> dict[str, str]:
    """First URL in each study's entry in docs/references.md."""
    text = (ROOT / "docs" / "references.md").read_text(encoding="utf-8")
    blocks: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("- "):
            if current:
                blocks.append(" ".join(current))
            current = [line[2:].strip()]
        elif current and line.strip():
            current.append(line.strip())
    if current:
        blocks.append(" ".join(current))
    urls: dict[str, str] = {}
    for block in blocks:
        study = re.search(r"\*\*(S\d{2})\*\*", block)
        url = re.search(r"https?://\S+", block)
        if study and url:
            urls[study.group(1)] = url.group(0).rstrip(".,;")
    return urls


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
    urls = reference_urls()
    out: list[list[str]] = []
    for doc, study, occurrence, claim in instances():
        verdict, reason = "supported", ""
        for u_doc, u_study, needle, u_reason in UNVERIFIED:
            if doc == u_doc and study == u_study and (not needle or needle in claim):
                verdict, reason = "unverified", u_reason
                break
        if verdict == "supported" and study not in EVIDENCE:
            raise SystemExit(f"No evidence recorded for {study} at {doc} #{occurrence}: {claim}")
        evidence = "" if verdict == "unverified" else next(
            (text for row_doc, row_study, needle, text in ROW_EVIDENCE
             if row_doc == doc and row_study == study and needle in claim),
            EVIDENCE[study],
        )
        source = FULL_TEXT.get(study) or urls.get(study, "")
        if not source:
            raise SystemExit(f"No source URL for {study}")
        basis = "not accessible" if verdict == "unverified" else BASIS.get(study, "abstract")
        out.append([doc, study, occurrence, claim, verdict, basis, source, evidence, reason])

    target = ROOT / "data" / "citation_audit.csv"
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            ["doc", "study", "occurrence", "claim", "verdict", "basis", "source", "evidence", "reason"]
        )
        writer.writerows(out)

    counts = Counter(row[4] for row in out)
    print(f"Wrote {len(out)} audited markers to {target}: {dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
