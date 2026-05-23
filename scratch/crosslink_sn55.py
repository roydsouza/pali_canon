#!/usr/bin/env python3
"""
Cross-link SN 55 mūla ↔ atthakatha ↔ tika files.
"""

import os

VAULT = "/Users/rds/pali_canon"
MULA = f"{VAULT}/mula/sutta/samyutta_nikaya/sn55.md"
ATT = f"{VAULT}/atthakatha/sutta/samyutta_nikaya/sn55_att.md"
TIK = f"{VAULT}/tika/sutta/samyutta_nikaya/sn55_tik.md"

# Targets mapping:
# para_num -> (sutta_id, header_in_mula, att_label, tik_label)
TARGETS = {
    999: (
        "SN 55.3",
        "## SN 55.3: Dīghāvuupāsakasutta — *With Dīghāvu*",
        "Sotāpattisaṃyuttavaṇṇanā §999",
        "Sotāpattisaṃyuttavaṇṇanāṭīkā §999"
    ),
    1003: (
        "SN 55.7",
        "## SN 55.7: Veḷudvāreyyasutta — *The People of Bamboo Gate*",
        "Sotāpattisaṃyuttavaṇṇanā §1003",
        "Sotāpattisaṃyuttavaṇṇanāṭīkā §1003"
    ),
    1050: (
        "SN 55.54",
        "## SN 55.54: Gilānasutta — *Sick*",
        "Sotāpattisaṃyuttavaṇṇanā §1050",
        "Sotāpattisaṃyuttavaṇṇanāṭīkā §1050"
    )
}

def process_mula():
    with open(MULA, "r", encoding="utf-8") as f:
        content = f.read()

    for para, (sutta_id, header, att_label, tik_label) in TARGETS.items():
        if header not in content:
            print(f"ERROR: Header not found in Mula: {header}")
            continue

        callout = (
            f"{header}\n\n"
            f"> [!info]- Related Commentary & Sub-commentary\n"
            f"> - **Commentary (Atthakathā)**: [[sn55_att#§{para}|{att_label}]]\n"
            f"> - **Sub-commentary (Ṭīkā)**: [[sn55_tik#§{para}|{tik_label}]]\n"
        )
        content = content.replace(header, callout, 1)

    with open(MULA, "w", encoding="utf-8") as f:
        f.write(content)
    print("Mūla cross-linking complete.")

def process_layer(file_path, is_att):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        matched = False
        for para, (sutta_id, header, att_label, tik_label) in TARGETS.items():
            prefix = f"({para})"
            if line.strip().startswith(prefix):
                hdr_link = f"### §{para}\n\n"
                if is_att:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: [[sn55#{sutta_id}|Mūla {sutta_id}]]\n"
                        f"> - **Tīkā**: [[sn55_tik#§{para}|Sotāpattisaṃyuttavaṇṇanāṭīkā §{para}]]\n\n"
                    )
                else:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: [[sn55#{sutta_id}|Mūla {sutta_id}]]\n"
                        f"> - **Atthakathā**: [[sn55_att#§{para}|Sotāpattisaṃyuttavaṇṇanā §{para}]]\n\n"
                    )
                new_lines.append(hdr_link + links)
                new_lines.append(line)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"{os.path.basename(file_path)} cross-linking complete.")

def main():
    print("Applying cross-links for SN 55...")
    process_mula()
    process_layer(ATT, is_att=True)
    process_layer(TIK, is_att=False)
    print("Done.")

if __name__ == "__main__":
    main()
