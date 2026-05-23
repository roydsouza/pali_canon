#!/usr/bin/env python3
import os
import re
import time
import html as hmod
import urllib.request

VAULT = "/Users/rds/pali_canon"
TIPITAKA = "https://tipitaka.org/romn/cscd/s0505a.att0.xml"

def fetch_xml():
    req = urllib.request.Request(TIPITAKA, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    try:
        return raw.decode('utf-16')
    except Exception:
        return raw.decode('utf-8', errors='replace')

def clean_xml(text):
    # Convert bold tag
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    # Remove page breaks
    text = re.sub(r'<pb[^/]*/>', '', text)
    # Remove other XML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities
    text = hmod.unescape(text)
    # Collapse whitespaces
    return re.sub(r'\s+', ' ', text).strip()

def parse_paragraphs(xml_text):
    results = []
    # Find all paragraph tags
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', xml_text, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ''
        
        pnum_m = re.search(r'<hi rend="paranum">\s*([\d\-]+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        
        # Remove paranum and dot from body
        body = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text = clean_xml(body)
        
        results.append((rend, paranum, text))
    return results

def build_markdown(title, sc_id, start_idx, end_idx, paras):
    yaml_id = f"{sc_id}_att"
    pali_title = "Khaggavisāṇasuttavaṇṇanā" if "1.3" in title else "Mettasuttavaṇṇanā"
    title_en = f"Commentary on The Rhinoceros Horn" if "1.3" in title else "Commentary on The Loving-Kindness Discourse"
    mula_link = f"[[{sc_id}|{sc_id.upper()}: {'Khaggavisāṇasutta' if '1.3' in title else 'Mettasutta'}]]"
    
    lines = [
        "---",
        f"id: {yaml_id}",
        f"title_pali: {pali_title}",
        f"title_en: {title_en}",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: sutta_nipata",
        f"sutta_number: {sc_id}",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Commentary on Khuddaka Nikāya: Sutta Nipāta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/INDEX|Atthakathā]] / [[atthakatha/sutta/INDEX|Sutta]] / [[atthakatha/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[atthakatha/sutta/khuddaka_nikaya/sutta_nipata/INDEX|Sutta Nipāta]]",
        f"**Mūla**: {mula_link}",
        "**Tīkā**: (No Ṭīkā available)",
        "",
        f"*Paramatthajotikā II*",
        f"*{end_idx - start_idx + 1} paragraphs — Pali text CSCD.*",
        "",
        f"## {pali_title}",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). Use Simsapa DPD for word lookups (double-click any Pali word).*",
        ""
    ]
    
    # Track if we are in the introduction or have reached verse-specific commentary
    in_intro = True
    
    for idx in range(start_idx, end_idx + 1):
        if idx >= len(paras):
            break
        rend, paranum, text = paras[idx]
        if not text:
            continue
            
        if rend == "subhead":
            # This is the main title, which is already under our h2, but we can write it if it's not the start
            if idx > start_idx:
                lines.append(f"### {text}\n")
            continue
            
        if paranum:
            # We reached a verse paragraph!
            in_intro = False
            lines.append(f"### §{paranum}\n")
            
        elif in_intro and idx == start_idx + 1:
            # Start of introduction
            lines.append("### Introduction\n")
            
        # Format paragraph by rend type
        if rend in ('gatha1', 'gatha2', 'gathalast', 'gatha', 'indent'):
            lines.append(f"  {text}  ")
        else:
            lines.append(f"{text}\n")
            
    return "\n".join(lines)

def main():
    print("Fetching XML from tipitaka.org...", flush=True)
    xml_text = fetch_xml()
    print("Parsing paragraphs...", flush=True)
    paras = parse_paragraphs(xml_text)
    print(f"Parsed {len(paras)} paragraphs.")
    
    # Snp 1.3: indices 198 to 504 (inclusive)
    # Snp 1.8: indices 695 to 764 (inclusive)
    suttas = [
        {"title": "Snp 1.3 (Khaggavisāṇa)", "sc_id": "snp1.3", "start": 198, "end": 504},
        {"title": "Snp 1.8 (Mettā)", "sc_id": "snp1.8", "start": 695, "end": 764}
    ]
    
    out_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/sutta_nipata")
    os.makedirs(out_dir, exist_ok=True)
    
    for s in suttas:
        print(f"Generating commentary for {s['title']}...", flush=True)
        content = build_markdown(s["title"], s["sc_id"], s["start"], s["end"], paras)
        dest = os.path.join(out_dir, f"{s['sc_id']}_att.md")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"Saved to {dest}")

if __name__ == "__main__":
    main()
