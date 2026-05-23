#!/usr/bin/env python3
import os
import re
import urllib.request
import json

VAULT = "/Users/rds/pali_canon"
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

def fetch(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def parse_segment_key(key):
    m = re.search(r':(\d+)\.(\d+)$', key)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None

def crosslink_mula_snp13():
    sc_id = "snp1.3"
    print("Cross-linking Mula snp1.3...")
    data = fetch(sc_id)
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    tags = ["solitude", "renunciation", "rhinoceros", "five_hindrances", "three_marks"]
    yaml_tags = "\n".join(f"  - {t}" for t in tags)
    
    lines = [
        "---",
        "id: SNP1.3",
        "title_pali: Khaggavisāṇasutta",
        "title_en: The Rhinoceros Horn",
        "type: mula",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: sutta_nipata",
        "sutta_number: snp1.3",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        yaml_tags,
        "---",
        "",
        "# Khuddaka Nikāya: Sutta Nipāta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[mula/sutta/khuddaka_nikaya/sutta_nipata/INDEX|Sutta Nipāta]]",
        "**Related Texts**: [[snp1.3_att|Commentary (Atthakathā)]] | (No Ṭīkā available)",
        "**Mātikā**: [[five_hindrances|Five Hindrances]] | [[three_marks|Three Marks]]",
        "",
        "## SNP 1.3: Khaggavisāṇasutta — *The Rhinoceros Horn*",
        ""
    ]
    
    # Group segment keys by verse number
    verses = {}
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue
        v_num, l_num = parse_segment_key(key)
        if v_num is not None:
            verses.setdefault(v_num, []).append((key, root.get(key, "").strip(), tr.get(key, "").strip()))
            
    for v_num in sorted(verses.keys()):
        lines.append(f"### Verse {v_num}")
        lines.append("")
        for key, p, e in verses[v_num]:
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
        
        # Add callout
        if v_num == 11 or v_num == 12:
            att_para = "45-46"
        else:
            att_para = str(v_num + 34)
        lines.append("")
        lines.append("> [!info]- Related Commentary")
        lines.append(f"> - **Commentary (Atthakathā)**: [[snp1.3_att#§{att_para}|Khaggavisāṇasuttavaṇṇanā §{att_para}]]")
        lines.append("")
        
    dest = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/sutta_nipata/snp1.3.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved cross-linked Mula snp1.3 to {dest}")

def crosslink_mula_snp18():
    sc_id = "snp1.8"
    print("Cross-linking Mula snp1.8...")
    data = fetch(sc_id)
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    tags = ["loving-kindness", "metta", "four_sublime_states"]
    yaml_tags = "\n".join(f"  - {t}" for t in tags)
    
    lines = [
        "---",
        "id: SNP1.8",
        "title_pali: Mettasutta",
        "title_en: The Loving-Kindness Discourse",
        "type: mula",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: sutta_nipata",
        "sutta_number: snp1.8",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        yaml_tags,
        "---",
        "",
        "# Khuddaka Nikāya: Sutta Nipāta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]] / [[mula/sutta/khuddaka_nikaya/sutta_nipata/INDEX|Sutta Nipāta]]",
        "**Related Texts**: [[snp1.8_att|Commentary (Atthakathā)]] | (No Ṭīkā available)",
        "**Mātikā**: [[four_sublime_states|Four Sublime States]]",
        "",
        "## SNP 1.8: Mettasutta — *The Loving-Kindness Discourse*",
        ""
    ]
    
    # Group segment keys by verse number
    verses = {}
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue
        v_num, l_num = parse_segment_key(key)
        if v_num is not None:
            verses.setdefault(v_num, []).append((key, root.get(key, "").strip(), tr.get(key, "").strip()))
            
    for v_num in sorted(verses.keys()):
        lines.append(f"### Verse {v_num}")
        lines.append("")
        for key, p, e in verses[v_num]:
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
        
        # Add callout
        att_para = v_num + 142 # Verse 1 maps to §143
        lines.append("")
        lines.append("> [!info]- Related Commentary")
        lines.append(f"> - **Commentary (Atthakathā)**: [[snp1.8_att#§{att_para}|Mettasuttavaṇṇanā §{att_para}]]")
        lines.append("")
        
    dest = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/sutta_nipata/snp1.8.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved cross-linked Mula snp1.8 to {dest}")

def crosslink_att_snp13():
    path = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/sutta_nipata/snp1.3_att.md")
    print(f"Cross-linking Atthakatha {path}...")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        new_lines.append(line)
        m = re.match(r'^### §([\d\-]+)', line)
        if m:
            para = m.group(1)
            if para == "45-46":
                callout = (
                    "\n"
                    "> [!info]- Related Links\n"
                    "> - **Mūla**: [[snp1.3#Verse 11|Mūla Verse 11]] & [[snp1.3#Verse 12|Mūla Verse 12]]\n"
                    "\n"
                )
            else:
                p_num = int(para)
                verse_num = p_num - 34
                callout = (
                    "\n"
                    "> [!info]- Related Links\n"
                    f"> - **Mūla**: [[snp1.3#Verse {verse_num}|Mūla Verse {verse_num}]]\n"
                    "\n"
                )
            new_lines.append(callout)
            
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Atthakatha snp1.3_att.md updated.")

def crosslink_att_snp18():
    path = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/sutta_nipata/snp1.8_att.md")
    print(f"Cross-linking Atthakatha {path}...")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        new_lines.append(line)
        m = re.match(r'^### §([\d\-]+)', line)
        if m:
            para = int(m.group(1))
            verse_num = para - 142
            callout = (
                "\n"
                "> [!info]- Related Links\n"
                f"> - **Mūla**: [[snp1.8#Verse {verse_num}|Mūla Verse {verse_num}]]\n"
                "\n"
            )
            new_lines.append(callout)
            
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Atthakatha snp1.8_att.md updated.")

def main():
    crosslink_mula_snp13()
    crosslink_mula_snp18()
    crosslink_att_snp13()
    crosslink_att_snp18()
    print("Done.")

if __name__ == "__main__":
    main()
