#!/usr/bin/env python3
"""
Cross-link SN 48 mūla ↔ atthakatha ↔ tika files.
"""

import os

VAULT = "/Users/rds/pali_canon"
MULA = f"{VAULT}/mula/sutta/samyutta_nikaya/sn48.md"
ATT = f"{VAULT}/atthakatha/sutta/samyutta_nikaya/sn48_att.md"
TIK = f"{VAULT}/tika/sutta/samyutta_nikaya/sn48_tik.md"

# Targets mapping:
# para_num -> (sutta_ids, header_in_mula, att_match, tik_match, has_tika)
TARGETS = {
    "478": (
        ["SN 48.8"],
        "## SN 48.8: Daṭṭhabbasutta — *Should Be Seen*",
        "(478)",
        "(478)",
        True
    ),
    "479-480": (
        ["SN 48.9", "SN 48.10"],
        # Note: We will handle the two suttas pointing to this same paragraph range
        [
            "## SN 48.9: Paṭhamavibhaṅgasutta — *Analysis (1st)*",
            "## SN 48.10: Dutiyavibhaṅgasutta — *Analysis (2nd)*"
        ],
        "9-10. Paṭhamavibhaṅgasuttādivaṇṇanā",
        "9-10. Paṭhamavibhaṅgasuttādivaṇṇanā",
        True
    ),
    "512": (
        ["SN 48.42"],
        "## SN 48.42: Uṇṇābhabrāhmaṇasutta — *The Brahmin Uṇṇābha*",
        "(512)",
        "(512)",
        True
    ),
    "514": (
        ["SN 48.44"],
        "## SN 48.44: Pubbakoṭṭhakasutta — *At the Eastern Gate*",
        "(514)",
        None,
        False
    ),
    "520": (
        ["SN 48.50"],
        "## SN 48.50: Āpaṇasutta — *At Āpaṇa*",
        "(520)",
        "(520)",
        True
    ),
    "524-525": (
        ["SN 48.54"],
        "## SN 48.54: Padasutta — *Footprints*",
        "4-5. Padasuttādivaṇṇanā",
        None,
        False
    )
}

def process_mula():
    with open(MULA, "r", encoding="utf-8") as f:
        content = f.read()

    for para, (sutta_ids, headers, att_match, tik_match, has_tika) in TARGETS.items():
        if not isinstance(headers, list):
            headers = [headers]
        
        for header in headers:
            if header not in content:
                print(f"ERROR: Header not found in Mula: {header}")
                continue

            # Construct callout
            if has_tika:
                callout = (
                    f"{header}\n\n"
                    f"> [!info]- Related Commentary & Sub-commentary\n"
                    f"> - **Commentary (Atthakathā)**: [[sn48_att#§{para}|Indriyasaṃyuttavaṇṇanā §{para}]]\n"
                    f"> - **Sub-commentary (Ṭīkā)**: [[sn48_tik#§{para}|Indriyasaṃyuttavaṇṇanāṭīkā §{para}]]\n"
                )
            else:
                callout = (
                    f"{header}\n\n"
                    f"> [!info]- Related Commentary\n"
                    f"> - **Commentary (Atthakathā)**: [[sn48_att#§{para}|Indriyasaṃyuttavaṇṇanā §{para}]]\n"
                )
            content = content.replace(header, callout, 1)

    with open(MULA, "w", encoding="utf-8") as f:
        f.write(content)
    print("Mūla cross-linking complete.")

def process_atthakatha():
    with open(ATT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        matched = False
        for para, (sutta_ids, headers, att_match, tik_match, has_tika) in TARGETS.items():
            if att_match and line.startswith(att_match):
                # Prepend paragraph header and callout links
                hdr = f"### §{para}\n\n"
                
                # Links to Mula
                mula_links = []
                for sid in sutta_ids:
                    mula_links.append(f"[[sn48#{sid}|Mūla {sid}]]")
                mula_str = " & ".join(mula_links)
                
                if has_tika:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: {mula_str}\n"
                        f"> - **Tīkā**: [[sn48_tik#§{para}|Indriyasaṃyuttavaṇṇanāṭīkā §{para}]]\n\n"
                    )
                else:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: {mula_str}\n\n"
                    )
                new_lines.append(hdr + links)
                new_lines.append(line)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    with open(ATT, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Atthakathā cross-linking complete.")

def process_tika():
    with open(TIK, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        matched = False
        for para, (sutta_ids, headers, att_match, tik_match, has_tika) in TARGETS.items():
            if has_tika and tik_match and line.startswith(tik_match):
                # Prepend paragraph header and callout links
                hdr = f"### §{para}\n\n"
                
                # Links to Mula
                mula_links = []
                for sid in sutta_ids:
                    mula_links.append(f"[[sn48#{sid}|Mūla {sid}]]")
                mula_str = " & ".join(mula_links)
                
                links = (
                    f"> [!info]- Related Links\n"
                    f"> - **Mūla**: {mula_str}\n"
                    f"> - **Atthakathā**: [[sn48_att#§{para}|Indriyasaṃyuttavaṇṇanā §{para}]]\n\n"
                )
                new_lines.append(hdr + links)
                new_lines.append(line)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    with open(TIK, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Ṭīkā cross-linking complete.")

def main():
    print("Applying cross-links for SN 48...")
    process_mula()
    process_atthakatha()
    process_tika()
    print("Done.")

if __name__ == "__main__":
    main()
