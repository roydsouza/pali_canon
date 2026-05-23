#!/usr/bin/env python3
import os
import json
import re
import time
import urllib.request

VAULT = "/Users/rds/pali_canon"
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

THAG_RANGES = {
    1: 59, 2: 49, 3: 16, 4: 12, 5: 12, 6: 14, 7: 5, 8: 3, 9: 1, 10: 7,
    11: 1, 12: 2, 13: 1, 14: 2, 15: 2, 16: 10, 17: 3, 18: 1, 19: 1, 20: 1,
    21: 1
}

THIG_RANGES = {
    1: 18, 2: 10, 3: 8, 4: 1, 5: 12, 6: 8, 7: 3, 8: 1, 9: 1, 10: 1,
    11: 1, 12: 1, 13: 5, 14: 1, 15: 1, 16: 1
}

def fetch_mula(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def parse_segment_key(key):
    m = re.search(r':(\d+)\.', key)
    if m:
        return int(m.group(1))
    return None

def extract_titles(sc_id, data):
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    pali_title = ""
    en_title = ""
    
    header_keys = [k for k in keys if re.search(rf"^{sc_id}:0\.\d+$", k)]
    if header_keys:
        last_key = header_keys[-1]
        pali_title = root.get(last_key, "").strip()
        en_title = tr.get(last_key, "").strip()
        
        pali_title = re.sub(r'^\d+\.\s*', '', pali_title)
        pali_title = re.sub(r'ttheragāthā$', 'theragāthā', pali_title)
        pali_title = re.sub(r'ttherīgāthā$', 'therīgāthā', pali_title)
        en_title = re.sub(r'^\d+\.\s*', '', en_title)
        
    if not pali_title:
        pali_title = sc_id.upper()
    if not en_title:
        en_title = sc_id.upper()
        
    return pali_title, en_title

def generate_gatha_sutta(sc_id, subcoll, pali_title, en_title, tags, matika, data):
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    subcoll_name = "Theragāthā" if subcoll == "theragatha" else "Therīgāthā"
    
    yaml_tags = "\n".join(f"  - {t}" for t in tags)
    lines = [
        "---",
        f"id: {sc_id.upper()}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        "nikaya: khuddaka",
        f"subcollection: {subcoll}",
        f"sutta_number: {sc_id}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        yaml_tags,
        "---",
        "",
        f"# Khuddaka Nikāya: {subcoll_name}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[mula/sutta/khuddaka_nikaya/{subcoll}/INDEX|{subcoll_name}]]",
        "**Related Texts**: (No Commentary or Ṭīkā migrated)",
        f"**Mātikā**: {matika}",
        "",
        f"## {sc_id.upper()}: {pali_title} — *{en_title}*",
        ""
    ]
    
    verses = {}
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue
        v_num = parse_segment_key(key)
        if v_num is not None:
            verses.setdefault(v_num, []).append((key, root.get(key, "").strip(), tr.get(key, "").strip()))
            
    for v_num in sorted(verses.keys()):
        lines.append(f"### Section {v_num}")
        lines.append("")
        for key, p, e in verses[v_num]:
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
        lines.append("")
        
    return "\n".join(lines)

def process_collection(subcoll, ranges, tags, matika):
    out_dir = os.path.join(VAULT, f"mula/sutta/khuddaka_nikaya/{subcoll}")
    os.makedirs(out_dir, exist_ok=True)
    
    sc_prefix = "thag" if subcoll == "theragatha" else "thig"
    
    for nip, count in ranges.items():
        print(f"\nProcessing {subcoll_name_of(subcoll)} Nipāta {nip}...", flush=True)
        for sutta in range(1, count + 1):
            sc_id = f"{sc_prefix}{nip}.{sutta}"
            print(f"  Fetching {sc_id}...", end="", flush=True)
            
            data = None
            retries = 3
            for r in range(retries):
                try:
                    data = fetch_mula(sc_id)
                    break
                except Exception as e:
                    time.sleep(1)
            
            if not data:
                print(" FAILED")
                continue
                
            pali_title, en_title = extract_titles(sc_id, data)
            content = generate_gatha_sutta(sc_id, subcoll, pali_title, en_title, tags, matika, data)
            
            dest = os.path.join(out_dir, f"{sc_id}.md")
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            print(" DONE")
            time.sleep(0.01)

def subcoll_name_of(subcoll):
    return "Theragāthā" if subcoll == "theragatha" else "Therīgāthā"

def main():
    # 1. Generate Theragatha
    process_collection(
        "theragatha",
        THAG_RANGES,
        ["monk", "verses", "renunciation", "liberation", "path"],
        "[[noble_eightfold_path|Noble Eightfold Path]] | [[four_sublime_states|Four Sublime States]]"
    )
    
    # 2. Generate Therigatha
    process_collection(
        "therigatha",
        THIG_RANGES,
        ["nun", "verses", "renunciation", "liberation", "path"],
        "[[four_foundations_of_mindfulness|Four Foundations of Mindfulness]] | [[four_sublime_states|Four Sublime States]]"
    )

if __name__ == "__main__":
    main()
