#!/usr/bin/env python3
import os
import json
import re
import time
import html as hmod
import urllib.request

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/s0505a.att0.xml"
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

# Suttas definitions with metadata
SUTTAS = [
    {
        "sc_id": "snp1.1",
        "title_pali": "Uragasutta",
        "title_en": "The Serpent",
        "tags": ["serpent", "anger", "craving", "conceit", "three_unwholesome_roots", "ten_fetters"],
        "matika_links": "[[three_unwholesome_roots|Three Unwholesome Roots]] | [[ten_fetters|Ten Fetters]]",
        "commentary_title": "Uragasuttavaṇṇanā",
        "start": 41,
        "end": 134,
        "offset": 0,
        "map_mula_to_att": lambda v: (
            "5" if v == 6 else
            "10-13" if v in (10, 11, 12, 13) else
            str(v)
        ),
        "map_att_to_mula": lambda p: int(p)
    },
    {
        "sc_id": "snp1.2",
        "title_pali": "Dhaniyasutta",
        "title_en": "Dhaniya the Herdsman",
        "tags": ["herdsman", "clinging", "security", "refuge"],
        "matika_links": "[[three_refuges|Three Refuges]]",
        "commentary_title": "Dhaniyasuttavaṇṇanā",
        "start": 135,
        "end": 197,
        "offset": 17,
        "map_mula_to_att": lambda v: (
            "31-32" if v in (14, 15) else
            str(v + 17)
        ),
        "map_att_to_mula": lambda p: p - 17
    },
    {
        "sc_id": "snp1.4",
        "title_pali": "Kasībhāradvājasutta",
        "title_en": "Kasībhāradvāja",
        "tags": ["farming", "faith", "wisdom", "five_spiritual_faculties"],
        "matika_links": "[[five_spiritual_faculties|Five Spiritual Faculties]]",
        "commentary_title": "Kasibhāradvājasuttavaṇṇanā",
        "start": 505,
        "end": 571,
        "map_mula_to_att": lambda v: {
            1: "76-77", 2: "76-77", 3: "76-77", 4: "76-77", 5: "76-77", 6: "76-77",
            7: "78", 8: "79", 9: "80", 10: "80", 11: "81", 12: "81",
            13: "82", 14: "82", 15: "82", 16: "82"
        }.get(v, "76-77"),
        "map_att_to_mula": lambda p: {
            76: 6, 77: 6, 78: 7, 79: 8, 80: 9, 81: 11, 82: 13
        }.get(p, 1)
    },
    {
        "sc_id": "snp1.5",
        "title_pali": "Cundasutta",
        "title_en": "Cunda",
        "tags": ["cunda", "disciple", "monks", "ethical_conduct"],
        "matika_links": "[[five_precepts|Five Precepts]]",
        "commentary_title": "Cundasuttavaṇṇanā",
        "start": 572,
        "end": 594,
        "offset": 82,
        "map_mula_to_att": lambda v: str(v + 82),
        "map_att_to_mula": lambda p: p - 82
    },
    {
        "sc_id": "snp1.6",
        "title_pali": "Parābhavasutta",
        "title_en": "Downfall",
        "tags": ["downfall", "ethics", "precepts", "lay_practice", "five_precepts"],
        "matika_links": "[[five_precepts|Five Precepts]]",
        "commentary_title": "Parābhavasuttavaṇṇanā",
        "start": 595,
        "end": 629,
        "map_mula_to_att": lambda v: {
            1: "91", 2: "91", 3: "92", 4: "93",
            5: "94", 6: "94",
            7: "96", 8: "96",
            9: "98", 10: "98",
            11: "100", 12: "100",
            13: "102", 14: "102",
            15: "104", 16: "104",
            17: "106", 18: "106",
            19: "108", 20: "108",
            21: "110", 22: "110",
            23: "112", 24: "112",
            25: "114", 26: "114"
        }.get(v, "91"),
        "map_att_to_mula": lambda p: p - 89
    },
    {
        "sc_id": "snp1.7",
        "title_pali": "Vasalasutta",
        "title_en": "The Outcast",
        "tags": ["outcast", "ethics", "conduct", "pride", "five_precepts"],
        "matika_links": "[[five_precepts|Five Precepts]]",
        "commentary_title": "Aggikabhāradvājasuttavaṇṇanā",
        "start": 630,
        "end": 694,
        "map_mula_to_att": lambda v: (
            "116" if v == 1 else
            str(v + 114) if v <= 22 else
            "137-139" if v <= 25 else
            "140-141" if v <= 27 else
            "142"
        ),
        "map_att_to_mula": lambda p: (
            1 if p <= 116 else
            p - 114 if p <= 136 else
            23 if p <= 139 else
            26 if p <= 141 else
            28
        )
    },
    {
        "sc_id": "snp1.9",
        "title_pali": "Hemavatasutta",
        "title_en": "Hemavata",
        "tags": ["yaksha", "devotion", "refuge", "moral_conduct"],
        "matika_links": "[[three_refuges|Three Refuges]]",
        "commentary_title": "Hemavatasuttavaṇṇanā",
        "start": 765,
        "end": 826,
        "offset": 152,
        "map_mula_to_att": lambda v: (
            "165-166" if v in (13, 14) else
            str(v + 152)
        ),
        "map_att_to_mula": lambda p: p - 152
    },
    {
        "sc_id": "snp1.10",
        "title_pali": "Āḷavakasutta",
        "title_en": "Āḷavaka",
        "tags": ["yaksha", "faith", " wisdom", "effort", "five_spiritual_faculties"],
        "matika_links": "[[five_spiritual_faculties|Five Spiritual Faculties]]",
        "commentary_title": "Āḷavakasuttavaṇṇanā",
        "start": 827,
        "end": 897,
        "map_mula_to_att": lambda v: (
            "183" if v <= 3 else
            "184" if v == 4 else
            "185-6" if v <= 6 else
            str(v + 180) if v <= 14 else
            "194"
        ),
        "map_att_to_mula": lambda p: (
            3 if p <= 183 else
            4 if p == 184 else
            5 if p <= 186 else
            p - 180 if p <= 193 else
            15
        )
    },
    {
        "sc_id": "snp1.11",
        "title_pali": "Vijayasutta",
        "title_en": "Victory",
        "tags": ["body_contemplation", "impurity", "asubha", "mindfulness", "four_foundations_of_mindfulness"],
        "matika_links": "[[four_foundations_of_mindfulness|Four Foundations of Mindfulness]]",
        "commentary_title": "Vijayasuttavaṇṇanā",
        "start": 898,
        "end": 946,
        "offset": 194,
        "map_mula_to_att": lambda v: (
            "199-200" if v in (4, 5, 6) else
            "207-208" if v in (13, 14) else
            str(v + 194)
        ),
        "map_att_to_mula": lambda p: p - 194
    },
    {
        "sc_id": "snp1.12",
        "title_pali": "Munisutta",
        "title_en": "The Sage",
        "tags": ["sage", "solitude", "silence", "non-attachment", "five_hindrances"],
        "matika_links": "[[five_hindrances|Five Hindrances]]",
        "commentary_title": "Munisuttavaṇṇanā",
        "start": 947,
        "end": 997,
        "map_mula_to_att": lambda v: str(min(v + 208, 223)),
        "map_att_to_mula": lambda p: p - 208
    }
]

def fetch_xml():
    req = urllib.request.Request(TIPITAKA, headers={"User-Agent": "Mozilla/5.0"})
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
    m = re.search(r':(\d+)\.(\d+)$', key)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None

def generate_mula_sutta(sutta_info, data):
    sc_id = sutta_info["sc_id"]
    pali_title = sutta_info["title_pali"]
    en_title = sutta_info["title_en"]
    tags = sutta_info["tags"]
    matika_links = sutta_info["matika_links"]
    map_mula_to_att = sutta_info["map_mula_to_att"]
    
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
        f"**Mātikā**: {matika_links}",
        "",
        f"## {sc_id.upper()}: {pali_title} — *{en_title}*",
        ""
    ]
    
    verses = {}
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue
        v_num, l_num = parse_segment_key(key)
        if v_num is not None:
            verses.setdefault(v_num, []).append((key, root.get(key, "").strip(), tr.get(key, "").strip()))
            
    for v_num in sorted(verses.keys()):
        # Print Section or Verse header depending on if prose or verse
        # (For Sutta Nipata, we display them as Verse/Section headers)
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
                
        # Link to commentary paragraph
        att_para = map_mula_to_att(v_num)
        lines.append("")
        lines.append("> [!info]- Related Commentary")
        lines.append(f"> - **Commentary (Atthakathā)**: [[{sc_id}_att#§{att_para}|{sutta_info['commentary_title']} §{att_para}]]")
        lines.append("")
        
    return "\n".join(lines)

def generate_atthakatha_sutta(sutta_info, paras):
    sc_id = sutta_info["sc_id"]
    pali_title = sutta_info["commentary_title"]
    start_idx = sutta_info["start"]
    end_idx = sutta_info["end"]
    map_att_to_mula = sutta_info["map_att_to_mula"]
    
    title_en = f"Commentary on {sutta_info['title_en']}"
    mula_link = f"[[{sc_id}|{sc_id.upper()}: {sutta_info['title_pali']}]]"
    
    lines = [
        "---",
        f"id: {sc_id}_att",
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
            
            # Back-link to Mula verse
            # Split grouped paranums like 76-77 or 185-6
            m = re.match(r'^(\d+)', paranum)
            if m:
                p_num = int(m.group(1))
                try:
                    verse_num = map_att_to_mula(p_num)
                    lines.append(f"> [!info]- Related Links")
                    lines.append(f"> - **Mūla**: [[{sc_id}#Section {verse_num}|Mūla Section {verse_num}]]")
                    lines.append("")
                except Exception:
                    pass
            
        elif in_intro and idx == start_idx + 1:
            lines.append("### Introduction\n")
            
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
    
    mula_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/sutta_nipata")
    att_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/sutta_nipata")
    os.makedirs(mula_dir, exist_ok=True)
    os.makedirs(att_dir, exist_ok=True)
    
    for s in SUTTAS:
        sc_id = s["sc_id"]
        print(f"\nProcessing {sc_id} ({s['title_pali']})...", flush=True)
        
        # Mūla
        try:
            mula_data = fetch_mula(sc_id)
            mula_content = generate_mula_sutta(s, mula_data)
            mula_dest = os.path.join(mula_dir, f"{sc_id}.md")
            with open(mula_dest, "w", encoding="utf-8") as f:
                f.write(mula_content + "\n")
            print(f"  Saved Mūla to {mula_dest}")
        except Exception as e:
            print(f"  Error generating Mūla for {sc_id}: {e}")
            
        # Atthakathā
        try:
            att_content = generate_atthakatha_sutta(s, paras)
            att_dest = os.path.join(att_dir, f"{sc_id}_att.md")
            with open(att_dest, "w", encoding="utf-8") as f:
                f.write(att_content + "\n")
            print(f"  Saved Atthakathā to {att_dest}")
        except Exception as e:
            print(f"  Error generating Atthakathā for {sc_id}: {e}")
            
        time.sleep(0.5)
        
    print("\nGeneration and cross-linking complete.")

if __name__ == "__main__":
    main()
