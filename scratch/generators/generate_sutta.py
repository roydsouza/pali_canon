#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
import time
import urllib.request

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path, load_cscd_paras, clean_xml

API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

NIKAYA_MAPS = {
    "dn": ("digha_nikaya", "Dīgha Nikāya", "digha"),
    "mn": ("majjhima_nikaya", "Majjhima Nikāya", "majjhima"),
    "sn": ("samyutta_nikaya", "Saṃyutta Nikāya", "samyutta"),
    "an": ("anguttara_nikaya", "Aṅguttara Nikāya", "anguttara"),
    "snp": ("khuddaka_nikaya/sutta_nipata", "Khuddaka Nikāya", "khuddaka"),
    "dhp": ("khuddaka_nikaya/dhammapada", "Khuddaka Nikāya", "khuddaka"),
    "iti": ("khuddaka_nikaya/itivuttaka", "Khuddaka Nikāya", "khuddaka"),
    "ud": ("khuddaka_nikaya/udana", "Khuddaka Nikāya", "khuddaka")
}

def get_nikaya_details(sutta_id):
    for prefix, details in NIKAYA_MAPS.items():
        if sutta_id.startswith(prefix):
            return details
    return ("sutta_generic", "Sutta Piṭaka", "sutta")

def fetch_suttacentral(sutta_id):
    url = API_BASE.format(sutta_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))

def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None

def filter_cscd_paras(paras, pattern_str):
    if not pattern_str:
        return paras
    pat = re.compile(pattern_str, re.IGNORECASE)
    results = []
    started = False
    for rend, paranum, text in paras:
        if not started:
            if pat.search(text):
                started = True
                results.append((rend, paranum, text))
        else:
            # Stop if we hit the next section
            if re.match(r'^\d+\.\s+\w+(?:vaṇṇanā|ṭīkā|suttavaṇṇanā)', text, re.IGNORECASE):
                break
            results.append((rend, paranum, text))
    return results if results else paras

def generate_mula(vault, sutta_id, data):
    root = data.get("root_text", {})
    tr = data.get("translation_text", {})
    keys = data.get("keys_order", [])
    
    nikaya_dir, nikaya_label, nav_abbr = get_nikaya_details(sutta_id)
    
    # Try to extract titles
    title_pali = root.get(f"{sutta_id}:0.2", root.get(f"{sutta_id}:0.3", "Untitled")).strip()
    title_en = tr.get(f"{sutta_id}:0.2", tr.get(f"{sutta_id}:0.3", "Untitled")).strip()
    
    out_dir = os.path.join(vault, "mula/sutta", nikaya_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{sutta_id}.md")
    
    lines = [
        "---",
        f"id: {sutta_id.upper()}",
        f"title_pali: {title_pali}",
        f"title_en: {title_en}",
        "type: mula",
        "pitaka: sutta",
        f"nikaya: {nav_abbr}",
        f"sutta_number: {sutta_id}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "---",
        "",
        f"# {nikaya_label}: {title_pali}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]",
        f"**Related Texts**: [[{sutta_id}_att|Commentary (Atthakathā)]] | [[{sutta_id}_tik|Sub-commentary (Tīkā)]]",
        "",
        f"## {title_pali} ({title_en})",
        "",
    ]
    
    for key in keys:
        if is_meta(key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key, "").strip()
        if not p and not e:
            continue
            
        level = heading_level(key)
        if level is not None:
            marker = "##" if level == 1 else "###"
            lines.append(f"{marker} {e or p}\n" + (f"*{p}*\n" if p and e else ""))
        else:
            if p:
                lines.append(f"**{p}**  ")
            if e:
                lines.append(f"*{e}*")
            lines.append("")
            
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Generated Mūla: {out_path} ({len(lines)} lines)")

def generate_layer(vault, sutta_id, layer_name, mapping_info):
    if not mapping_info:
        return
        
    nikaya_dir, nikaya_label, nav_abbr = get_nikaya_details(sutta_id)
    
    filename = mapping_info.get("file")
    pattern = mapping_info.get("pattern")
    heading = mapping_info.get("heading", f"{sutta_id.upper()} {layer_name.capitalize()}")
    
    print(f"Loading {layer_name.upper()} from {filename}...")
    try:
        paras = load_cscd_paras(filename)
    except Exception as e:
        print(f"Failed to load CSCD file {filename}: {e}")
        return
        
    filtered = filter_cscd_paras(paras, pattern)
    
    suffix = "att" if layer_name == "att" else "tik"
    out_folder = "atthakatha" if layer_name == "att" else "tika"
    out_dir = os.path.join(vault, out_folder, "sutta", nikaya_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{sutta_id}_{suffix}.md")
    
    mula_ref = f"{sutta_id}"
    other_ref = f"{sutta_id}_tik" if suffix == "att" else f"{sutta_id}_att"
    other_label = "Tīkā" if suffix == "att" else "Atthakathā"
    
    lines = [
        "---",
        f"id: {sutta_id.upper()}_{suffix}",
        f"title_pali: {heading}",
        f"type: {out_folder}",
        "pitaka: sutta",
        f"nikaya: {nav_abbr}",
        f"mula_file: [[{mula_ref}]]",
    ]
    if suffix == "att":
        lines.append(f"tika_file: [[{other_ref}]]")
    else:
        lines.append(f"commentary_file: [[{other_ref}]]")
        
    lines.extend([
        "---",
        "",
        f"# {heading}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[{out_folder}/INDEX|{out_folder.capitalize()}]] / [[{out_folder}/sutta/INDEX|Sutta]] / [[{out_folder}/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]",
        f"**Mūla**: [[{mula_ref}]]",
        f"**{other_label}**: [[{other_ref}]]",
        "",
        f"*Pali text CSCD ({filename}).*",
        "",
    ])
    
    for rend, paranum, text in filtered:
        prefix = f"({paranum}) " if paranum else ""
        if rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            lines.append(f"{prefix}{text}\n")
            
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Generated {layer_name.upper()}: {out_path} ({len(lines)} lines)")

def main():
    parser = argparse.ArgumentParser(description="Unified Sutta generator engine.")
    parser.add_argument("--sutta", required=True, help="Sutta ID to generate (e.g. mn22, sn12.1)")
    args = parser.parse_args()
    
    sutta_id = args.sutta.lower().strip()
    vault = get_vault_path()
    
    print(f"Unified Generator starting for Sutta ID: {sutta_id}")
    
    # 1. Generate Mūla
    try:
        print("Fetching SuttaCentral segments...")
        sc_data = fetch_suttacentral(sutta_id)
        generate_mula(vault, sutta_id, sc_data)
    except Exception as e:
        print(f"Failed to generate Mūla layer from SuttaCentral: {e}")
        
    # 2. Check mappings for Att & Tika
    mapping_path = os.path.join(vault, "scratch", "cscd_mappings_all.json")
    if os.path.exists(mapping_path):
        with open(mapping_path, "r", encoding="utf-8") as f:
            mappings = json.load(f)
            
        sutta_map = mappings.get(sutta_id)
        if sutta_map:
            att_maps = sutta_map.get("att", [])
            tika_maps = sutta_map.get("tika", [])
            
            if att_maps:
                generate_layer(vault, sutta_id, "att", att_maps[0])
            if tika_maps:
                generate_layer(vault, sutta_id, "tika", tika_maps[0])
        else:
            print(f"No CSCD mappings found for {sutta_id} in cscd_mappings_all.json. Skipping commentary layers.")
    else:
        print("Mappings file cscd_mappings_all.json not found. Skipping commentary layers.")
        
    print("Generation complete.")

if __name__ == "__main__":
    main()
