#!/usr/bin/env python3
import os
import json
import re
import time
import urllib.request

VAULT = "/Users/rds/pali_canon"
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

SUTTAS = [
    {
        "sc_id": "snp1.3",
        "title_pali": "Khaggavisāṇasutta",
        "title_en": "The Rhinoceros Horn",
        "tags": ["solitude", "renunciation", "rhinoceros", "five_hindrances", "three_marks"],
        "matika_links": "[[five_hindrances|Five Hindrances]] | [[three_marks|Three Marks]]"
    },
    {
        "sc_id": "snp1.8",
        "title_pali": "Mettasutta",
        "title_en": "The Loving-Kindness Discourse",
        "tags": ["loving-kindness", "metta", "four_sublime_states"],
        "matika_links": "[[four_sublime_states|Four Sublime States]]"
    }
]

def fetch(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def parse_segment_key(key):
    # e.g., "snp1.3:1.1" -> ("1", "1")
    m = re.search(r':(\d+)\.(\d+)$', key)
    if m:
        return m.group(1), m.group(2)
    return None, None

def generate_mula_sutta(sutta_info, data):
    sc_id = sutta_info["sc_id"]
    pali_title = sutta_info["title_pali"]
    en_title = sutta_info["title_en"]
    tags = sutta_info["tags"]
    matika_links = sutta_info["matika_links"]
    
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    # Build YAML frontmatter
    yaml_tags = "\n".join(f"  - {t}" for t in tags)
    lines = [
        "---",
        f"id: {sc_id.upper()}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: sutta_nipata",
        f"sutta_number: {sc_id}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        yaml_tags,
        "---",
        "",
        "# Khuddaka Nikāya: Sutta Nipāta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[mula/sutta/khuddaka_nikaya/sutta_nipata/INDEX|Sutta Nipāta]]",
        f"**Related Texts**: [[{sc_id}_att|Commentary (Atthakathā)]] | (No Ṭīkā available)",
        f"**Mātikā**: {matika_links}",
        "",
        f"## {sc_id.upper()}: {pali_title} — *{en_title}*",
        ""
    ]
    
    current_verse = None
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue # skip headers
            
        p = root.get(key, "").strip()
        e = tr.get(key, "").strip()
        
        if not p and not e:
            continue
            
        verse_num, line_num = parse_segment_key(key)
        
        if verse_num is not None:
            if current_verse is not None and current_verse != verse_num:
                lines.append("") # blank line between verses
            current_verse = verse_num
            
            # Format: bold Pali with two spaces, then italic English
            # Use segment ID as markdown comment or anchor for linkage
            # We want bidirectional verse-level cross-links or anchors if needed.
            # In Mula, we will add commentary callouts under each verse.
            # For now, let's output the base Mula text, and we'll cross-link it later.
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
            lines.append("")
        else:
            # Fallback for non-standard keys
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
            lines.append("")
            
    return "\n".join(lines)

def main():
    out_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/sutta_nipata")
    os.makedirs(out_dir, exist_ok=True)
    
    for s in SUTTAS:
        sc_id = s["sc_id"]
        print(f"Fetching {sc_id}...", flush=True)
        try:
            data = fetch(sc_id)
            print(f"Fetched {len(data.get('keys_order', []))} keys.")
            content = generate_mula_sutta(s, data)
            dest = os.path.join(out_dir, f"{sc_id}.md")
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            print(f"Saved to {dest}")
        except Exception as e:
            print(f"Error fetching/writing {sc_id}: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
