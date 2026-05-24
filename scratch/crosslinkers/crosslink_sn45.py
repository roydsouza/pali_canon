#!/usr/bin/env python3
"""
Cross-link SN 45 mūla ↔ atthakathā ↔ tīkā files.
"""

import os

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
MULA = f"{VAULT}/mula/sutta/samyutta_nikaya/sn45.md"
ATT = f"{VAULT}/atthakatha/sutta/samyutta_nikaya/sn45_att.md"
TIK = f"{VAULT}/tika/sutta/samyutta_nikaya/sn45_tik.md"

# Targets mapping:
# sutta_id -> (header_in_mula, para_anchor, att_label, tik_label)
TARGETS = {
    "SN 45.2": (
        "## SN 45.2: Upaḍḍhasutta — *Half the Spiritual Life*",
        "1-2",
        "Maggasaṃyuttavaṇṇanā §1-2",
        "Maggasaṃyuttavaṇṇanāṭīkā §1-2"
    ),
    "SN 45.3": (
        "## SN 45.3: Sāriputtasutta — *Sāriputta*",
        "3",
        "Maggasaṃyuttavaṇṇanā §3",
        "Maggasaṃyuttavaṇṇanāṭīkā §3"
    ),
    "SN 45.8": (
        "## SN 45.8: Vibhaṅgasutta — *Analysis*",
        "8",
        "Maggasaṃyuttavaṇṇanā §8",
        "Maggasaṃyuttavaṇṇanāṭīkā §8"
    ),
    "SN 45.139": (
        "## SN 45.139: Tathāgatasutta — *The Realized One*",
        "139",
        "Maggasaṃyuttavaṇṇanā §139",
        "Maggasaṃyuttavaṇṇanāṭīkā §139"
    )
}

def process_mula():
    with open(MULA, "r", encoding="utf-8") as f:
        content = f.read()

    for sutta_id, (header, para, att_label, tik_label) in TARGETS.items():
        if f"[[sn45_att#§{para}" in content:
            continue
        if header not in content:
            print(f"ERROR: Header not found in Mula: {header}")
            continue

        callout = (
            f"{header}\n\n"
            f"> [!info]- Related Commentary & Sub-commentary\n"
            f"> - **Commentary (Atthakathā)**: [[sn45_att#§{para}|{att_label}]]\n"
            f"> - **Sub-commentary (Ṭīkā)**: [[sn45_tik#§{para}|{tik_label}]]\n"
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

    # First, handle 1-2
    target_str = "1-2. Avijjāsuttādivaṇṇanā"
    if target_str in content:
        para = "1-2"
        sutta_id = "SN 45.2"
        if is_att:
            links = (
                f"### §{para}\n"
                f"> [!info]- Related Links\n"
                f"> - **Mūla**: [[sn45#SN 45.2|Mūla SN 45.2]]\n"
                f"> - **Tīkā**: [[sn45_tik#§{para}|Maggasaṃyuttavaṇṇanāṭīkā §{para}]]\n\n"
                f"{target_str}"
            )
        else:
            links = (
                f"### §{para}\n"
                f"> [!info]- Related Links\n"
                f"> - **Mūla**: [[sn45#SN 45.2|Mūla SN 45.2]]\n"
                f"> - **Atthakathā**: [[sn45_att#§{para}|Maggasaṃyuttavaṇṇanā §{para}]]\n\n"
                f"{target_str}"
            )
        content = content.replace(target_str, links, 1)

    # Convert to lines to handle other paragraphs: (3), (8), (139)
    lines = content.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        matched = False
        for sutta_id, (header, para, att_label, tik_label) in TARGETS.items():
            if para == "1-2":
                continue
            prefix = f"({para})"
            if line.strip().startswith(prefix):
                hdr_link = f"### §{para}\n\n"
                if is_att:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: [[sn45#{sutta_id}|Mūla {sutta_id}]]\n"
                        f"> - **Tīkā**: [[sn45_tik#§{para}|Maggasaṃyuttavaṇṇanāṭīkā §{para}]]\n\n"
                    )
                else:
                    links = (
                        f"> [!info]- Related Links\n"
                        f"> - **Mūla**: [[sn45#{sutta_id}|Mūla {sutta_id}]]\n"
                        f"> - **Atthakathā**: [[sn45_att#§{para}|Maggasaṃyuttavaṇṇanā §{para}]]\n\n"
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
    print("Applying cross-links for SN 45...")
    process_mula()
    process_layer(ATT, is_att=True)
    process_layer(TIK, is_att=False)
    print("Done.")

if __name__ == "__main__":
    main()
