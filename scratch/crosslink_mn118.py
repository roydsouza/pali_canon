#!/usr/bin/env python3
"""
Add cross-links to MN 118 mūla, atthakathā, and tīkā files.

Strategy
--------
att (mn118_att.md):
  - Insert "### §NNN" heading before each bold paragraph marker
  - Append a collapsed callout "→ Tīkā §NNN" link after each block

tik (mn118_tik.md):
  - Insert "### §NNN" heading before each bold paragraph marker

mula (mn118.md):
  - Insert a collapsed Obsidian callout immediately before the key Pali
    phrase that each commentary paragraph explains.
"""

import re

VAULT = "/Users/rds/pali_canon"
ATT  = f"{VAULT}/atthakatha/sutta/majjhima_nikaya/mn118_att.md"
TIK  = f"{VAULT}/tika/sutta/majjhima_nikaya/mn118_tik.md"
MULA = f"{VAULT}/mula/sutta/majjhima_nikaya/mn118.md"

# Paragraph numbers present in both att and tik
PARAS = [144, 145, 146, 147, 149, 150, 152]

# -------------------------------------------------------------------
# ATT + TIK: insert headings (and for att, inter-paragraph tīkā links)
# -------------------------------------------------------------------

def process_commentary(path, insert_tik_links):
    """
    Read a commentary file and insert ### §NNN headings before each
    bold paragraph marker. If insert_tik_links is True also append a
    callout linking to the corresponding tīkā paragraph after each block.
    """
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    # Regex: bold paragraph marker at start of line, e.g. **144. ...
    para_pat = re.compile(r'^\*\*(\d+)\.\s')

    # Mark insertion points
    # We collect (line_index, para_num) for every paragraph heading
    markers = []
    for i, line in enumerate(lines):
        m = para_pat.match(line)
        if m:
            n = int(m.group(1))
            if n in PARAS:
                markers.append((i, n))

    # Build new lines by inserting before each marker
    # We also need to insert tīkā links AFTER each block (before next marker or EOF)
    # Process in reverse order so indices stay valid
    for idx in range(len(markers) - 1, -1, -1):
        line_i, para_num = markers[idx]

        if insert_tik_links:
            # Find end of this block = start of next marker or end of file
            if idx + 1 < len(markers):
                next_line = markers[idx + 1][0]
            else:
                next_line = len(lines)

            # Find last non-empty line in the block
            insert_after = next_line - 1
            while insert_after > line_i and not lines[insert_after].strip():
                insert_after -= 1

            tik_link = (
                f"\n> [!abstract]- Tīkā §{para_num}\n"
                f"> [[mn118_tik#§{para_num}|Papañcasūdanī-ṭīkā §{para_num}]]\n"
            )
            lines.insert(insert_after + 1, tik_link)
            # Adjust subsequent marker indices
            for j in range(idx - 1, -1, -1):
                pass  # Already processing in reverse; only future inserts matter

        # Insert heading before this paragraph
        heading = f"\n### §{para_num}\n\n"
        lines.insert(line_i, heading)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"  Updated {path.split('/')[-1]}: {len(markers)} paragraph headings added")


# -------------------------------------------------------------------
# MULA: insert collapsible callouts before key Pali phrases
# -------------------------------------------------------------------

# Map paragraph number → distinctive Pali phrase that starts (or uniquely
# identifies) the mūla passage the commentary is explaining.
# Using a substring that appears exactly once in mn118.md.
MULA_ANCHORS = {
    144: "**Evaṁ me sutaṁ—**",
    145: "**\"āraddhosmi, bhikkhave, imāya paṭipadāya;**",
    146: "**yathārūpaṁ parisaṁ alaṁ yojanagaṇanāni dassanāya gantuṁ puṭosenāpi.**",
    147: "**Santi, bhikkhave, bhikkhū imasmiṁ bhikkhusaṅghe catunnaṁ satipaṭṭhānānaṁ",
    149: "**Kāyesu kāyaññatarāhaṁ, bhikkhave, evaṁ vadāmi yadidaṁ—assāsapassāsā.**",
    150: ("**Yasmiṁ samaye, bhikkhave, bhikkhu kāye kāyānupassī viharati "
          "ātāpī sampajāno satimā vineyya loke abhijjhādomanassaṁ, "
          "upaṭṭhitāssa tasmiṁ samaye sati hoti asammuṭṭhā.**"),
    152: "**Idha, bhikkhave, bhikkhu satisambojjhaṅgaṁ bhāveti vivekanissitaṁ",
}

# Human-readable labels for each paragraph
LABELS = {
    144: "Opening (evaṁ me sutaṁ)",
    145: "Āraddhosmi — satisfaction with the practice",
    146: "Worth traveling leagues to see",
    147: "Types of monks in the Saṅgha",
    149: "Breath as aspect of the body (kāyaññatara)",
    150: "How ānāpānasati fulfills the bojjhaṅgas",
    152: "Bojjhaṅgas relying on seclusion → vijjāvimutti",
}

def callout(para_num):
    label = LABELS[para_num]
    return (
        f"\n> [!info]- Commentary — {label}\n"
        f"> **Atthakathā**: [[mn118_att#§{para_num}|Papañcasūdanī §{para_num}]]"
        f"  ·  **Tīkā**: [[mn118_tik#§{para_num}|Ṭīkā §{para_num}]]\n\n"
    )


def process_mula():
    with open(MULA, encoding="utf-8") as f:
        text = f.read()

    inserted = 0
    for para_num, anchor in MULA_ANCHORS.items():
        if anchor not in text:
            print(f"  WARNING: anchor for §{para_num} not found in mūla — skipping")
            continue
        replacement = callout(para_num) + anchor
        text = text.replace(anchor, replacement, 1)
        inserted += 1

    with open(MULA, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"  Updated {MULA.split('/')[-1]}: {inserted} callouts inserted")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    print("MN 118 cross-linking")
    print("  Processing atthakathā...")
    process_commentary(ATT, insert_tik_links=True)
    print("  Processing tīkā...")
    process_commentary(TIK, insert_tik_links=False)
    print("  Processing mūla...")
    process_mula()
    print("Done.")


if __name__ == "__main__":
    main()
