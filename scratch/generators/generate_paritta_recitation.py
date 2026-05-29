#!/usr/bin/env python3
import os
import re

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")

PARITTAS = [
    {
        "mula_path": "mula/sutta/khuddaka_nikaya/sutta_nipata/snp1_8.md",
        "out_path": "paritta/karaniya_metta_sutta_pali.md",
        "id": "KARANIYA_METTA_SUTTA_PALI",
        "title_pali": "Karaṇīyamettasutta",
        "title_en": "The Discourse on Loving-Kindness (Pali Recitation)",
        "source_sutta": "[[snp1_8|Snp 1.8]]"
    },
    {
        "mula_path": "mula/sutta/khuddaka_nikaya/sutta_nipata/snp2_1.md",
        "out_path": "paritta/ratana_sutta_pali.md",
        "id": "RATANA_SUTTA_PALI",
        "title_pali": "Ratanasutta",
        "title_en": "The Jewel Discourse (Pali Recitation)",
        "source_sutta": "[[snp2_1|Snp 2.1]]"
    },
    {
        "mula_path": "mula/sutta/khuddaka_nikaya/sutta_nipata/snp2_4.md",
        "out_path": "paritta/mangala_sutta_pali.md",
        "id": "MANGALA_SUTTA_PALI",
        "title_pali": "Maṅgalasutta",
        "title_en": "The Discourse on Blessings (Pali Recitation)",
        "source_sutta": "[[snp2_4|Snp 2.4]]"
    },
    {
        "mula_path": "mula/sutta/anguttara_nikaya/an4_67.md",
        "out_path": "paritta/khandha_paritta_pali.md",
        "id": "KHANDHA_PARITTA_PALI",
        "title_pali": "Khandhaparitta (Ahirājasutta)",
        "title_en": "The Snake Safeguard (Pali Recitation)",
        "source_sutta": "[[an4_67|AN 4.67]]"
    }
]

def extract_pali_from_mula(file_path):
    pali_lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find all bold markers **...**
    # We want to extract lines or sections that have bold text.
    # Sutta contents usually start after the metadata block and main headers.
    lines = content.split("\n")
    in_sutta_body = False
    
    for line in lines:
        if line.strip().startswith("---"):
            continue
        if line.strip().startswith("#"):
            if "Navigation" in line or "Related" in line or "Mātikā" in line:
                continue
            # Header is fine, but we only want body text
            continue
        
        # Detect start of sutta content (usually after header)
        if "Navigation" in line or "Related Texts" in line or "Mātikā" in line or "Related Commentary" in line or "[!info]" in line:
            in_sutta_body = True
            continue
            
        if line.strip().startswith(">"):
            continue
        if "Commentary" in line or "Sub-commentary" in line or "Atthakathā" in line or "Tīkā" in line:
            continue
        
        # Extract bold matches
        matches = re.findall(r"\*\*(.*?)\*\*", line)
        if matches:
            # Reconstruct the line using only the bold parts
            # Clean up trailing spaces or punctuation inside bold tags if needed
            pali_text = " ".join(matches).strip()
            # If the original line had spacing or line breaks, preserve line-level structure
            if pali_text:
                # Add back some formatting if it's a verse or section end
                # e.g., if original line had <br> or was double-spaced
                # We also remove trailing '—' or similar if they were part of segment anchors
                pali_text = re.sub(r'—$', '', pali_text).strip()
                pali_lines.append(pali_text)
        elif line.strip() == "" and len(pali_lines) > 0 and pali_lines[-1] != "":
            # Keep blank lines between stanzas/paragraphs, but avoid duplicates
            pali_lines.append("")

    # Clean up trailing empty lines
    while pali_lines and pali_lines[-1] == "":
        pali_lines.pop()
        
    return "\n".join(pali_lines)

def main():
    for p in PARITTAS:
        full_mula_path = os.path.join(VAULT, p["mula_path"])
        full_out_path = os.path.join(VAULT, p["out_path"])
        
        print(f"Extracting Pali from {p['mula_path']}...")
        pali_text = extract_pali_from_mula(full_mula_path)
        
        header = "\n".join([
            "---",
            f"id: {p['id']}",
            f"title_pali: {p['title_pali']}",
            f"title_en: {p['title_en']}",
            "type: practice",
            "pitaka: sutta",
            "tags:",
            "  - paritta",
            "  - chanting",
            "  - pali_only",
            "---",
            "",
            f"# {p['title_pali']} — Pali Recitation",
            "",
            f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[paritta/INDEX|Paritta Collection]]",
            f"**Source Discourse**: {p['source_sutta']}",
            "",
            "---",
            "",
            "## Recitation Text",
            "",
            "```text"
        ])
        
        footer = "\n".join([
            "```",
            "",
            "---",
            "",
            f"*Recited for protection and mental clarity. Texts derived from the corresponding mūla translations in this vault.*"
        ])
        
        # Format text to look clean
        # Replace empty lines in the code block with a single empty line
        body = "\n".join(line for line in pali_text.split("\n"))
        
        full_content = header + "\n" + body + "\n" + footer
        
        with open(full_out_path, "w", encoding="utf-8") as f:
            f.write(full_content + "\n")
            
        print(f"Generated paritta recitation: {p['out_path']}")

if __name__ == "__main__":
    main()
