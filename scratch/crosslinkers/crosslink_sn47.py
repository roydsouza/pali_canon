#!/usr/bin/env python3
"""
Cross-link SN 47 mūla ↔ atthakathā ↔ tīkā files.
"""

import os

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
MULA = f"{VAULT}/mula/sutta/samyutta_nikaya/sn47.md"
ATT = f"{VAULT}/atthakatha/sutta/samyutta_nikaya/sn47_att.md"
TIK = f"{VAULT}/tika/sutta/samyutta_nikaya/sn47_tik.md"

# Paragraph details
# para_num: (sutta_id, sutta_header, sutta_label)
TARGETS = {
    367: ("SN 47.1", "## SN 47.1: Ambapālisutta — *In Ambapālī’s Mango Grove*", "Ambapālisutta (SN 47.1)"),
    374: ("SN 47.8", "## SN 47.8: Sūdasutta — *Cooks*", "Sūdasutta (SN 47.8)"),
    375: ("SN 47.9", "## SN 47.9: Gilānasutta — *Sick*", "Gilānasutta (SN 47.9)"),
    386: ("SN 47.20", "## SN 47.20: Janapadakalyāṇīsutta — *The Finest Lady in the Land*", "Janapadakalyāṇīsutta (SN 47.20)")
}

def process_mula():
    with open(MULA, "r", encoding="utf-8") as f:
        content = f.read()

    for para, (sutta_id, header, label) in TARGETS.items():
        if f"[[sn47_att#§{para}" in content:
            continue
        if header not in content:
            print(f"ERROR: Header not found in Mula: {header}")
            continue

        callout = (
            f"{header}\n\n"
            f"> [!info]- Related Commentary & Sub-commentary\n"
            f"> - **Commentary (Atthakathā)**: [[sn47_att#§{para}|Satipaṭṭhānasaṃyuttavaṇṇanā §{para}]]\n"
            f"> - **Sub-commentary (Ṭīkā)**: [[sn47_tik#§{para}|Satipaṭṭhānasaṃyuttavaṇṇanāṭīkā §{para}]]\n"
        )
        content = content.replace(header, callout, 1)

    with open(MULA, "w", encoding="utf-8") as f:
        f.write(content)
    print("Mūla cross-linking complete.")

def process_layer(file_path, is_att):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Idempotency check
    if "### §" in content:
        print(f"  Skipped {os.path.basename(file_path)} (already crosslinked)")
        return

    lines = content.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        matched = False
        for para, (sutta_id, header, label) in TARGETS.items():
            prefix = f"({para})"
            if line.strip().startswith(prefix):
                # Prepend the header and links
                hdr_link = f"### §{para}\n\n"
                if is_att:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: [[sn47#{sutta_id}|Mūla {sutta_id}]]\n"
                        f"> - **Tīkā**: [[sn47_tik#§{para}|Satipaṭṭhānasaṃyuttavaṇṇanāṭīkā §{para}]]\n\n"
                    )
                else:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: [[sn47#{sutta_id}|Mūla {sutta_id}]]\n"
                        f"> - **Atthakathā**: [[sn47_att#§{para}|Satipaṭṭhānasaṃyuttavaṇṇanā §{para}]]\n\n"
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
    print("Applying cross-links for SN 47...")
    process_mula()
    process_layer(ATT, is_att=True)
    process_layer(TIK, is_att=False)
    print("Done.")

if __name__ == "__main__":
    main()
