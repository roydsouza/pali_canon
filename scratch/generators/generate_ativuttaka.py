#!/usr/bin/env python3
import os
import json
import re
import time
import html as hmod
import urllib.request
import subprocess

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA_BASE = "https://tipitaka.org/romn/cscd/{}"
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

# Nipata definitions
NIPATAS_METADATA = {
    1: {
        "xml": "s0504a.att1.xml",
        "sc_prefix": "iti",
        "sc_start_id": 1,
        "sc_end_id": 27,
        "starts": [2, 50, 72, 83, 86, 89, 95, 103, 106, 111, 113, 123, 130, 146, 160, 168, 172, 181, 184, 196, 213, 234, 239, 245],
        "default_tags": ["ethics", "conduct", "virtue"],
        "default_matika": "[[five_precepts|Five Precepts]]",
        "special": {
            "iti1": {"tags": ["greed", "three_unwholesome_roots"], "matika": "[[three_unwholesome_roots|Three Unwholesome Roots]]"},
            "iti2": {"tags": ["hatred", "three_unwholesome_roots"], "matika": "[[three_unwholesome_roots|Three Unwholesome Roots]]"},
            "iti3": {"tags": ["delusion", "three_unwholesome_roots"], "matika": "[[three_unwholesome_roots|Three Unwholesome Roots]]"},
            "iti14": {"tags": ["ignorance", "five_hindrances", "ten_fetters"], "matika": "[[five_hindrances|Five Hindrances]] | [[ten_fetters|Ten Fetters]]"},
            "iti15": {"tags": ["craving", "ten_fetters"], "matika": "[[ten_fetters|Ten Fetters]]"},
            "iti22": {"tags": ["metta", "loving-kindness", "four_sublime_states"], "matika": "[[four_sublime_states|Four Sublime States]]"},
            "iti27": {"tags": ["metta", "loving-kindness", "four_sublime_states"], "matika": "[[four_sublime_states|Four Sublime States]]"}
        }
    },
    2: {
        "xml": "s0504a.att2.xml",
        "sc_prefix": "iti",
        "sc_start_id": 28,
        "sc_end_id": 49,
        "starts": [2, 19, 22, 27, 30, 33, 36, 42, 87, 90, 114, 324, 329, 336, 343, 362, 371, 385, 394, 412, 426, 432],
        "default_tags": ["virtue", "ethical_conduct", "monastic"],
        "default_matika": "[[five_precepts|Five Precepts]]",
        "special": {
            "iti44": {"tags": ["nibbana", "unconditioned", "liberation"], "matika": "[[four_noble_truths|Four Noble Truths]]"}
        }
    },
    3: {
        "xml": "s0504a.att3.xml",
        "sc_prefix": "iti",
        "sc_start_id": 50,
        "sc_end_id": 99,
        "starts": [2, 10, 20, 56, 64, 76, 80, 87, 99, 109, 120, 129, 135, 149, 153, 156, 160, 168, 172, 179, 187, 190, 199, 203, 280, 289, 305, 311, 318, 331, 337, 356, 366, 394, 407, 415, 423, 436, 472, 487, 534, 547, 560, 570, 575, 581, 589, 607, 622],
        "default_tags": ["ativuttaka", "tika", "path"],
        "default_matika": "[[noble_eightfold_path|Noble Eightfold Path]]",
        "special": {
            "iti50": {"tags": ["roots", "three_unwholesome_roots"], "matika": "[[three_unwholesome_roots|Three Unwholesome Roots]]"},
            "iti52": {"tags": ["feeling", "five_aggregates", "three_marks"], "matika": "[[five_aggregates|Five Aggregates]] | [[three_marks|Three Marks]]"},
            "iti53": {"tags": ["feeling", "five_aggregates", "three_marks"], "matika": "[[five_aggregates|Five Aggregates]] | [[three_marks|Three Marks]]"},
            "iti85": {"tags": ["asubha", "body_contemplation", "four_foundations_of_mindfulness"], "matika": "[[four_foundations_of_mindfulness|Four Foundations of Mindfulness]]"}
        }
    },
    4: {
        "xml": "s0504a.att4.xml",
        "sc_prefix": "iti",
        "sc_start_id": 100,
        "sc_end_id": 112,
        "starts": [1, 22, 31, 48, 51, 62, 66, 85, 93, 102, 126, 134, 184],
        "default_tags": ["ativuttaka", "catukka", "path"],
        "default_matika": "[[noble_eightfold_path|Noble Eightfold Path]]",
        "special": {
            "iti102": {"tags": ["asava", "taints", "four_noble_truths"], "matika": "[[four_noble_truths|Four Noble Truths]]"},
            "iti112": {"tags": ["world", "four_noble_truths", "three_marks"], "matika": "[[four_noble_truths|Four Noble Truths]] | [[three_marks|Three Marks]]"}
        }
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
        "subcollection: itivuttaka",
        f"sutta_number: {sc_id}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        yaml_tags,
        "---",
        "",
        "# Khuddaka Nikāya: Itivuttaka",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[mula/sutta/khuddaka_nikaya/itivuttaka/INDEX|Itivuttaka]]",
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
        "subcollection: itivuttaka",
        f"sutta_number: {sc_id}",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Commentary on Khuddaka Nikāya: Itivuttaka",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/INDEX|Atthakathā]] / [[atthakatha/sutta/INDEX|Sutta]] / [[atthakatha/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[atthakatha/sutta/khuddaka_nikaya/itivuttaka/INDEX|Itivuttaka]]",
        f"**Mūla**: {mula_link}",
        "**Tīkā**: (No Ṭīkā available)",
        "",
        f"*Paramatthadīpanī*",
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

def get_start_and_end(ch_num, idx, starts, total_paras):
    # This resolves the grouped starts for Itivuttaka
    if ch_num == 1:
        # Ekakanipato
        # starts map:
        # suttas 1-8 (idx 0-7) map to starts[0-7]
        # suttas 9-10 (idx 8-9) map to starts[8] (106)
        # suttas 11-13 (idx 10-12) map to starts[9] (111)
        # suttas 14-27 (idx 13-26) map to starts[10-23]
        if idx <= 7:
            start = starts[idx]
            end = starts[idx+1] - 1
        elif idx == 8:
            start = starts[8]
            end = starts[9] - 1
        elif idx == 9:
            start = starts[8]
            end = starts[9] - 1
        elif idx == 10:
            start = starts[9]
            end = starts[10] - 1
        elif idx == 11:
            start = starts[9]
            end = starts[10] - 1
        elif idx == 12:
            start = starts[9]
            end = starts[10] - 1
        else:
            starts_idx = idx - 3  # shifts left because suttas 9,10 share starts[8] and 11,12,13 share starts[9]
            start = starts[starts_idx]
            end = starts[starts_idx+1] - 1 if starts_idx+1 < len(starts) else total_paras - 1
            
    elif ch_num == 3:
        # Tikanipato
        # suttas 50-55 (idx 0-5) map to starts[0-5]
        # suttas 56-57 (idx 6-7) map to starts[6] (80)
        # suttas 58-99 (idx 8-49) map to starts[7-48]
        if idx <= 5:
            start = starts[idx]
            end = starts[idx+1] - 1
        elif idx == 6:
            start = starts[6]
            end = starts[7] - 1
        elif idx == 7:
            start = starts[6]
            end = starts[7] - 1
        else:
            starts_idx = idx - 1
            start = starts[starts_idx]
            end = starts[starts_idx+1] - 1 if starts_idx+1 < len(starts) else total_paras - 1
            
    else:
        # Dukanipato, Catukkanipato are 1-to-1
        start = starts[idx]
        end = starts[idx+1] - 1 if idx+1 < len(starts) else total_paras - 1
        
    return start, end

def main():
    mula_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/itivuttaka")
    att_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/itivuttaka")
    os.makedirs(mula_dir, exist_ok=True)
    os.makedirs(att_dir, exist_ok=True)
    
    for ch_num, meta in NIPATAS_METADATA.items():
        print(f"\n================ NIPATA {ch_num} ================")
        xml_file = meta["xml"]
        print(f"Fetching commentary XML {xml_file}...", flush=True)
        xml_text = fetch_xml(xml_file)
        paras = parse_paragraphs(xml_text)
        print(f"Parsed {len(paras)} commentary paragraphs.")
        
        starts = meta["starts"]
        sc_start = meta["sc_start_id"]
        sc_end = meta["sc_end_id"]
        sc_prefix = meta["sc_prefix"]
        
        for idx, sc_num in enumerate(range(sc_start, sc_end + 1)):
            sc_id = f"{sc_prefix}{sc_num}"
            start, end = get_start_and_end(ch_num, idx, starts, len(paras))
            
            # Find commentary title from subhead
            comm_title = "Commentary"
            for p_idx in range(start, end + 1):
                if p_idx >= len(paras):
                    break
                if paras[p_idx][0] == "subhead":
                    comm_title = paras[p_idx][2]
                    break
            
            print(f"Processing {sc_id} (commentary paras {start}-{end})...", flush=True)
            
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
            
            time.sleep(0.05)

    print("\nAll Itivuttaka suttas generated!")

if __name__ == "__main__":
    main()
