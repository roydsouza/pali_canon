#!/usr/bin/env python3
import os
import json
import re
import time
import html as hmod
import urllib.request
import subprocess

VAULT = "/Users/rds/pali_canon"
TIPITAKA_BASE = "https://tipitaka.org/romn/cscd/{}"
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

CHAPTERS_METADATA = {
    2: {
        "xml": "s0505a.att1.xml",
        "sc_prefix": "snp2.",
        "start_indices": [1, 114, 140, 161, 402, 416, 439, 483, 498, 512, 523, 539, 575, 630],
        "default_tags": ["ethics", "conduct", "lay_practice"],
        "default_matika": "[[five_precepts|Five Precepts]]",
        "special": {
            "snp2.1": {
                "tags": ["ratana", "paritta", "three_refuges"],
                "matika": "[[three_refuges|Three Refuges]]"
            },
            "snp2.4": {
                "tags": ["mangala", "paritta", "ethics", "five_precepts"],
                "matika": "[[five_precepts|Five Precepts]]"
            }
        }
    },
    3: {
        "xml": "s0505a.att2.xml",
        "sc_prefix": "snp3.",
        "start_indices": [1, 17, 47, 70, 111, 137, 187, 272, 311, 368, 401, 460],
        "default_tags": ["monastic", "going_forth", "path"],
        "default_matika": "[[noble_eightfold_path|Noble Eightfold Path]]",
        "special": {
            "snp3.12": {
                "tags": ["dvayatanupassana", "vipassana", "dependent_origination", "three_marks"],
                "matika": "[[dependent_origination|Dependent Origination]] | [[three_marks|Three Marks]]"
            }
        }
    },
    4: {
        "xml": "s0505a.att3.xml",
        "sc_prefix": "snp4.",
        "start_indices": [1, 10, 23, 38, 52, 62, 79, 91, 120, 143, 162, 180, 197, 219, 240, 262],
        "default_tags": ["atthakavagga", "non-clinging", "views", "three_marks"],
        "default_matika": "[[three_marks|Three Marks]] | [[five_aggregates|Five Aggregates]]",
        "special": {}
    },
    5: {
        "xml": "s0505a.att4.xml",
        "sc_prefix": "snp5.",
        "start_indices": [1, 40, 52, 59, 68, 82, 90, 101, 108, 113, 119, 125, 131, 138, 146, 153, 161, 168, 171],
        "default_tags": ["parayanavagga", "questions", "wisdom", "four_noble_truths"],
        "default_matika": "[[four_noble_truths|Four Noble Truths]] | [[dependent_origination|Dependent Origination]]",
        "special": {}
    }
}

def fetch_xml(filename):
    url = TIPITAKA_BASE.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    try:
        return raw.decode('utf-16')
    except Exception:
        return raw.decode('utf-8', errors='replace')

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def parse_paragraphs(xml_text):
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', xml_text, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*([\d\-]+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text = clean_xml(body)
        results.append((rend, paranum, text))
    return results

def fetch_mula(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def parse_segment_key(key):
    # Match the first number after the colon, followed by a dot
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
        en_title = re.sub(r'^\d+\.\s*', '', en_title)
        
    if not pali_title:
        pali_title = sc_id.upper()
    if not en_title:
        en_title = sc_id.upper()
        
    return pali_title, en_title

def git_commit(sc_id, name):
    try:
        mula_file = f"mula/sutta/khuddaka_nikaya/sutta_nipata/{sc_id}.md"
        att_file = f"atthakatha/sutta/khuddaka_nikaya/sutta_nipata/{sc_id}_att.md"
        
        # Git add
        subprocess.run(["git", "add", mula_file, att_file], cwd=VAULT, check=True)
        # Git commit
        commit_msg = f"feat: migrate {sc_id.upper()} {name} (mūla/att)"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=VAULT, check=True)
        print(f"  Git: Committed successfully.")
    except Exception as e:
        print(f"  Git commit failed for {sc_id}: {e}")

def generate_mula_sutta(sc_id, pali_title, en_title, tags, matika, data):
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
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
        
        # Link to commentary file
        lines.append("")
        lines.append("> [!info]- Related Commentary")
        lines.append(f"> - **Commentary (Atthakathā)**: [[{sc_id}_att|Commentary]]")
        lines.append("")
        
    return "\n".join(lines)

def generate_atthakatha_sutta(sc_id, pali_title, en_title, start_idx, end_idx, paras, commentary_title):
    title_en = f"Commentary on {en_title}"
    mula_link = f"[[{sc_id}|{sc_id.upper()}: {pali_title}]]"
    
    lines = [
        "---",
        f"id: {sc_id}_att",
        f"title_pali: {commentary_title}",
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
        f"## {commentary_title}",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). Use Simsapa DPD for word lookups (double-click any Pali word).*",
        ""
    ]
    
    in_intro = True
    for idx in range(start_idx, end_idx + 1):
        if idx >= len(paras):
            break
        rend, paranum, text = paras[idx]
        if not text:
            continue
            
        if rend == "subhead":
            if idx > start_idx:
                lines.append(f"### {text}\n")
            continue
            
        if paranum:
            in_intro = False
            lines.append(f"### §{paranum}\n")
            lines.append(f"> [!info]- Related Links")
            lines.append(f"> - **Mūla**: [[{sc_id}|{sc_id.upper()} Mūla]]")
            lines.append("")
        elif in_intro and idx == start_idx + 1:
            lines.append("### Introduction\n")
            
        if rend in ('gatha1', 'gatha2', 'gathalast', 'gatha', 'indent'):
            lines.append(f"  {text}  ")
        else:
            lines.append(f"{text}\n")
            
    return "\n".join(lines)

def main():
    mula_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/sutta_nipata")
    att_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/sutta_nipata")
    os.makedirs(mula_dir, exist_ok=True)
    os.makedirs(att_dir, exist_ok=True)
    
    for ch_num, meta in CHAPTERS_METADATA.items():
        print(f"\n================ CHAPTER {ch_num} ================")
        xml_file = meta["xml"]
        print(f"Fetching commentary XML {xml_file}...", flush=True)
        xml_text = fetch_xml(xml_file)
        paras = parse_paragraphs(xml_text)
        print(f"Parsed {len(paras)} commentary paragraphs.")
        
        starts = meta["start_indices"]
        sc_prefix = meta["sc_prefix"]
        
        for i in range(len(starts)):
            sc_id = f"{sc_prefix}{i+1}"
            start = starts[i]
            end = starts[i+1] - 1 if i+1 < len(starts) else len(paras) - 1
            
            # Find commentary title from subhead
            comm_title = "Commentary"
            for idx in range(start, end + 1):
                if idx >= len(paras):
                    break
                if paras[idx][0] == "subhead":
                    comm_title = paras[idx][2]
                    break
            
            print(f"\nProcessing {sc_id} (commentary paras {start}-{end})...", flush=True)
            
            # Fetch Mūla from SuttaCentral
            data = None
            retries = 3
            for r in range(retries):
                try:
                    data = fetch_mula(sc_id)
                    break
                except Exception as e:
                    print(f"  Retry {r+1} failed: {e}")
                    time.sleep(2)
            
            if not data:
                print(f"  Failed to fetch Mūla for {sc_id}. Skipping.")
                continue
                
            pali_title, en_title = extract_titles(sc_id, data)
            print(f"  Titles: {pali_title} / {en_title}")
            
            # Resolve tags and matika
            tags = meta["default_tags"]
            matika = meta["default_matika"]
            if sc_id in meta["special"]:
                tags = meta["special"][sc_id]["tags"]
                matika = meta["special"][sc_id]["matika"]
                
            # Generate files
            mula_content = generate_mula_sutta(sc_id, pali_title, en_title, tags, matika, data)
            att_content = generate_atthakatha_sutta(sc_id, pali_title, en_title, start, end, paras, comm_title)
            
            mula_dest = os.path.join(mula_dir, f"{sc_id}.md")
            att_dest = os.path.join(att_dir, f"{sc_id}_att.md")
            
            with open(mula_dest, "w", encoding="utf-8") as f:
                f.write(mula_content + "\n")
            with open(att_dest, "w", encoding="utf-8") as f:
                f.write(att_content + "\n")
                
            print(f"  Saved Mūla & Commentary.")
            
            # Git commit
            # git_commit(sc_id, pali_title)
            
            time.sleep(0.1)

    print("\nAll Chapters generated and committed!")

if __name__ == "__main__":
    main()
