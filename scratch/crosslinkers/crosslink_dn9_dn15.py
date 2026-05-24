#!/usr/bin/env python3
"""
Cross-link DN 9 and DN 15 mūla ↔ atthakathā ↔ tīkā files.

Following the established MN 118 pattern:
  att: Insert "### §NNN" heading before bold paragraph markers + "→ Tīkā" callouts
  tik: Insert "### §NNN" heading before bold paragraph markers
  mula: Insert collapsible callouts before key Pali phrases
"""

import os
import re

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")

# ── DN 9 Configuration ─────────────────────────────────────────────────────

DN9_ATT  = f"{VAULT}/atthakatha/sutta/digha_nikaya/dn9_att.md"
DN9_TIK  = f"{VAULT}/tika/sutta/digha_nikaya/dn9_tik.md"
DN9_MULA = f"{VAULT}/mula/sutta/digha_nikaya/dn9.md"
# Key paragraphs present in both att and tik for DN 9
DN9_PARAS = [406, 407, 410, 413, 416, 417, 421, 422, 428, 429, 438]

# Paragraph → distinctive Pali phrase in the mūla (unique substring)
DN9_MULA_ANCHORS = {
    406: "**Evaṁ me sutaṁ—**",
    407: "**Tena kho pana samayena poṭṭhapādo paribbājako samayappavādake",
    410: "**Svāgataṁ, bhante, bhagavato.**",
    413: "**“Saññā kho, poṭṭhapāda, paṭhamaṁ uppajjati, pacchā ñāṇaṁ",
    416: "**“Saññā nu kho, bhante, purisassa attā",
    417: "**“Kaṁ pana tvaṁ, poṭṭhapāda, attānaṁ paccesī”ti?**",
    421: "**Atha kho te paribbājakā acirapakkantassa bhagavato poṭṭhapādaṁ paribbājakaṁ samantato vācā sannitodakena sañjhabbharimakaṁsu:**",
    422: "**Atha kho dvīhatīhassa accayena citto ca hatthisāriputto poṭṭhapādo ca paribbājako",
    428: "**“Tayo kho me, poṭṭhapāda, attapaṭilābhā—**",
    429: "**‘yathāpaṭipannānaṁ vo saṅkilesikā dhammā pahīyissanti",
    438: "**Sace taṁ, citta, evaṁ puccheyyuṁ:**",
}

DN9_LABELS = {
    406: "Opening — Evaṁ me sutaṁ",
    407: "Setting — Poṭṭhapāda at the Tindukācīra",
    410: "How perception arises and ceases (abhisaññānirodha)",
    413: "Perception arises first, knowledge after (saññā → ñāṇa)",
    416: "Is perception the self? (saññā = attā?)",
    417: "What kind of self do you hold? (kaṁ attānaṁ paccesi)",
    421: "The wanderers' verbal barrage (vācāsaṇṇitoḍaka)",
    422: "Citta Hatthisāriputta and Poṭṭhapāda approach the Buddha",
    428: "Three kinds of acquired self (tayo attapaṭilābhā)",
    429: "Wisdom's fulfillment (paññāpāripūri)",
    438: "Past/future/present self — mere designation (nāmamatta)",
}

# ── DN 15 Configuration ────────────────────────────────────────────────────

DN15_ATT  = f"{VAULT}/atthakatha/sutta/digha_nikaya/dn15_att.md"
DN15_TIK  = f"{VAULT}/tika/sutta/digha_nikaya/dn15_tik.md"
DN15_MULA = f"{VAULT}/mula/sutta/digha_nikaya/dn15.md"

# Key paragraphs for DN 15 (selected for thematic importance)
DN15_PARAS = [95, 99, 100, 103, 112, 113, 115, 116, 117, 118, 119, 121, 122, 123, 124]

DN15_MULA_ANCHORS = {
    95: "**Evaṁ me sutaṁ—**",
    99: "**Gambhīro cāyaṁ, ānanda, paṭiccasamuppādo gambhīrāvabhāso ca.**",
    100: "**Iti kho, ānanda, nāmarūpapaccayā viññāṇaṁ, viññāṇapaccayā nāmarūpaṁ,",
    103: "**‘Jātipaccayā jarāmaraṇan’ti iti kho panetaṁ vuttaṁ",
    112: "**‘Nāmarūpapaccayā phasso’ti iti kho panetaṁ vuttaṁ",
    113: "**cakkhusamphasso sotasamphasso ghānasamphasso jivhāsamphasso",
    115: "**‘Viññāṇapaccayā nāmarūpan’ti iti kho panetaṁ vuttaṁ",
    116: "**‘Nāmarūpapaccayā viññāṇan’ti iti kho panetaṁ vuttaṁ",
    117: "**Kittāvatā ca, ānanda, attānaṁ paññapento paññapeti?**",
    118: "**Rūpiṁ vā hi, ānanda, parittaṁ attānaṁ paññapento paññapeti:**",
    119: "**Kittāvatā ca, ānanda, attānaṁ na paññapento na paññapeti?**",
    121: "**Kittāvatā ca, ānanda, attānaṁ samanupassamāno samanupassati?**",
    122: "**Vedanaṁ vā hi, ānanda, attānaṁ samanupassamāno samanupassati:**",
    123: "**Sukhāpi kho, ānanda, vedanā aniccā saṅkhatā paṭiccasamuppannā",
    124: "**‘yattha panāvuso, sabbaso vedayitaṁ natthi",
}

DN15_LABELS = {
    95: "Opening — Evaṁ me sutaṁ",
    99: "Profundity of Dependent Origination (gambhīro paṭiccasamuppādo)",
    100: "Full chain — nāmarūpa ↔ viññāṇa mutual dependence",
    103: "Explanation: birth conditions ageing-and-death",
    112: "Explanation: nāmarūpa conditions contact (phassa)",
    113: "Contact → feeling through six sense bases",
    115: "Explanation: consciousness conditions name-and-form",
    116: "Explanation: name-and-form conditions consciousness (mutual dependence)",
    117: "How one designates a self (attānaṁ paññapento)",
    118: "Four views of self — material/immaterial × limited/infinite",
    119: "One who does not designate a self in these ways",
    121: "How one does not regard self (na samanupassati)",
    122: "Three views: feeling is self / not-self / subject to feeling",
    123: "Feelings are impermanent, conditioned, dependently arisen",
    124: "Where feeling is absent — is there 'I am'?",
}


# ── Cross-linking functions ─────────────────────────────────────────────────

def process_commentary(path, paras, insert_tik_links, slug):
    """Insert ### §NNN headings and optionally tīkā callout links."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Idempotency check
    if "### §" in content:
        print(f"  Skipped {path.split('/')[-1]} (already crosslinked)")
        return

    lines = content.splitlines(keepends=True)
    para_pat = re.compile(r'^\((\d+)\)')
    markers = []
    for i, line in enumerate(lines):
        m = para_pat.match(line)
        if m:
            n = int(m.group(1))
            if n in paras:
                markers.append((i, n))

    for idx in range(len(markers) - 1, -1, -1):
        line_i, para_num = markers[idx]

        if insert_tik_links:
            if idx + 1 < len(markers):
                next_line = markers[idx + 1][0]
            else:
                next_line = len(lines)
            insert_after = next_line - 1
            while insert_after > line_i and not lines[insert_after].strip():
                insert_after -= 1
            tik_link = (
                f"\n> [!abstract]- Tīkā §{para_num}\n"
                f"> [[{slug}_tik#§{para_num}|Sumaṅgalavilāsinī-ṭīkā §{para_num}]]\n"
            )
            lines.insert(insert_after + 1, tik_link)

        heading = f"\n### §{para_num}\n\n"
        lines.insert(line_i, heading)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"  Updated {path.split('/')[-1]}: {len(markers)} paragraph headings")


def process_mula(path, anchors, labels, slug):
    """Insert collapsible commentary callouts in the mūla file."""
    with open(path, encoding="utf-8") as f:
        text = f.read()

    inserted = 0
    for para_num, anchor in anchors.items():
        # Idempotency check: if callout already exists, skip
        if f"[[{slug}_att#§{para_num}" in text:
            continue
        if anchor not in text:
            print(f"  WARNING: anchor for §{para_num} not found in mūla — skipping")
            continue
        label = labels[para_num]
        callout = (
            f"\n> [!info]- Commentary — {label}\n"
            f"> **Atthakathā**: [[{slug}_att#§{para_num}|Sumaṅgalavilāsinī §{para_num}]]"
            f"  ·  **Tīkā**: [[{slug}_tik#§{para_num}|Ṭīkā §{para_num}]]\n\n"
        )
        text = text.replace(anchor, callout + anchor, 1)
        inserted += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"  Updated {path.split('/')[-1]}: {inserted} callouts inserted")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("DN 9 cross-linking")
    print("=" * 60)
    print("  Processing atthakathā...")
    process_commentary(DN9_ATT, DN9_PARAS, insert_tik_links=True, slug="dn9")
    print("  Processing tīkā...")
    process_commentary(DN9_TIK, DN9_PARAS, insert_tik_links=False, slug="dn9")
    print("  Processing mūla...")
    process_mula(DN9_MULA, DN9_MULA_ANCHORS, DN9_LABELS, "dn9")

    print()
    print("=" * 60)
    print("DN 15 cross-linking")
    print("=" * 60)
    print("  Processing atthakathā...")
    process_commentary(DN15_ATT, DN15_PARAS, insert_tik_links=True, slug="dn15")
    print("  Processing tīkā...")
    process_commentary(TIK_PATH := DN15_TIK, DN15_PARAS, insert_tik_links=False, slug="dn15")
    print("  Processing mūla...")
    process_mula(DN15_MULA, DN15_MULA_ANCHORS, DN15_LABELS, "dn15")

    print("\nDone.")


if __name__ == "__main__":
    main()
