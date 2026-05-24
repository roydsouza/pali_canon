import os
import json
import urllib.request
import re
import html

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
SCRATCH_DIR = os.path.join(VAULT, "scratch")
OUTPUT_MULA = os.path.join(VAULT, "mula/sutta/majjhima_nikaya/mn118.md")
OUTPUT_ATT = os.path.join(VAULT, "atthakatha/sutta/majjhima_nikaya/mn118_att.md")
OUTPUT_TIK = os.path.join(VAULT, "tika/sutta/majjhima_nikaya/mn118_tik.md")

MULA_URL = "https://raw.githubusercontent.com/suttacentral/bilara-data/published/root/pli/ms/sutta/mn/mn118_root-pli-ms.json"
BASE_XML_URL = "https://raw.githubusercontent.com/siongui/vri-tipitaka-xml-mirror/main/romn/cscd/"

def download_file(url, filename):
    filepath = os.path.join(SCRATCH_DIR, filename)
    if os.path.exists(filepath):
        print(f"File {filename} already downloaded.")
        return filepath
    print(f"Downloading {url} to {filepath}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(filepath, "wb") as f:
                f.write(response.read())
        print("Download complete.")
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def read_file_content(path):
    for encoding in ['utf-16', 'utf-8', 'utf-16-le', 'utf-16-be', 'utf-8-sig', 'latin-1']:
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
                if '<' in content:
                    return content
        except Exception:
            pass
    with open(path, 'r', encoding='latin-1') as f:
        return f.read()

def clean_xml_text(text):
    # 1. Strip page breaks
    text = re.sub(r'<pb[^>]*/>', '', text)
    # 2. Convert bold highlights to markdown bold
    text = re.sub(r'<hi\s+rend=["\']bold["\']>(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    # 3. Strip paranum and dot tags but preserve content
    text = re.sub(r'<hi\s+rend=["\']paranum["\']>(.*?)</hi>', r'\1', text, flags=re.DOTALL)
    # Note: sometimes it has space inside
    text = re.sub(r'<hi\s+rend=["\']dot["\']>(.*?)</hi>', r'\1', text, flags=re.DOTALL)
    # 4. Strip any remaining XML/HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # 5. Decode HTML entities
    text = html.unescape(text)
    # 6. Normalize spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def process_mula():
    print("--- Processing Mula Sutta ---")
    json_path = os.path.join(SCRATCH_DIR, "mn118_root.json")
    en_json_path = os.path.join(SCRATCH_DIR, "mn118_translation-en-sujato.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data_root = json.load(f)
        
    data_en = {}
    if os.path.exists(en_json_path):
        with open(en_json_path, "r", encoding="utf-8") as f:
            data_en = json.load(f)
            
    markdown_lines = []
    
    # Header block
    markdown_lines.append("# Majjhima Nikāya 118")
    markdown_lines.append("")
    markdown_lines.append("**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / [[mula/sutta/INDEX|Sutta]] / [[mula/sutta/majjhima_nikaya/INDEX|Majjhima Nikāya]]")
    markdown_lines.append("**Related Texts**: [[mn118_att|Commentary (Atthakatha)]] | [[mn118_tik|Sub-commentary (Tīkā)]]")
    markdown_lines.append("")
    
    title_pali = data_root.get("mn118:0.2", "Ānāpānassatisutta").strip()
    title_en = data_en.get("mn118:0.2", "Mindfulness of Breathing").strip()
    markdown_lines.append(f"## {title_pali} ({title_en})")
    markdown_lines.append("")
    
    # Body logic - grouped by segment index
    all_keys = sorted(data_root.keys(), key=lambda x: [int(y) for y in re.findall(r'\d+', x)])
    for key in all_keys:
        # Skip header keys
        if key in ["mn118:0.1", "mn118:0.2"]:
            continue
            
        pali_text = data_root[key].strip()
        en_text = data_en.get(key, "").strip()
        
        if not pali_text and not en_text:
            continue
            
        if pali_text:
            markdown_lines.append(f"**{pali_text}**  ")
        if en_text:
            markdown_lines.append(f"*{en_text}*")
            
        markdown_lines.append("")
        
    content = '\n'.join(markdown_lines).strip()
    
    frontmatter = """---
id: MN118
title_pali: Ānāpānasati Sutta
type: mula
pitaka: sutta
nikaya: majjhima
sutta_number: 118
commentary_file: /atthakatha/sutta/majjhima_nikaya/mn118_att.md
sub_commentary_file: /tika/sutta/majjhima_nikaya/mn118_tik.md
---

"""
    
    with open(OUTPUT_MULA, "w", encoding="utf-8") as f:
        f.write(frontmatter + content + "\n")
        
    word_count = len(content.split())
    print(f"Interleaved Mula Sutta written to {OUTPUT_MULA} ({word_count} words).")
    return frontmatter, word_count

def process_commentary():
    print("--- Processing Commentary ---")
    xml_path = os.path.join(SCRATCH_DIR, "s0203a.att1.xml")
    content_xml = read_file_content(xml_path)
    
    ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', content_xml, re.DOTALL)
    
    markdown_lines = []
    # Index 176 to 193 is our range
    for i in range(176, 194):
        rend, text = ps[i]
        clean_text = clean_xml_text(text)
        
        if rend == 'subhead':
            markdown_lines.append(f"### {clean_text}")
        elif rend == 'centre':
            markdown_lines.append(f"*{clean_text}*")
        else:
            markdown_lines.append(clean_text)
        markdown_lines.append("")
        
    content = '\n'.join(markdown_lines).strip()
    
    frontmatter = """---
id: MN118_att
title_pali: Ānāpānasati Suttavaṇṇanā
type: atthakatha
pitaka: sutta
nikaya: majjhima
sutta_number: 118
mula_file: /mula/sutta/majjhima_nikaya/mn118.md
sub_commentary_file: /tika/sutta/majjhima_nikaya/mn118_tik.md
---

"""
    
    with open(OUTPUT_ATT, "w", encoding="utf-8") as f:
        f.write(frontmatter + content + "\n")
        
    word_count = len(content.split())
    print(f"Commentary written to {OUTPUT_ATT} ({word_count} words).")
    return frontmatter, word_count

def process_sub_commentary():
    print("--- Processing Sub-commentary ---")
    xml_path = os.path.join(SCRATCH_DIR, "s0203t.tik1.xml")
    content_xml = read_file_content(xml_path)
    
    ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', content_xml, re.DOTALL)
    
    markdown_lines = []
    # Index 144 to 159 is our range
    for i in range(144, 160):
        rend, text = ps[i]
        clean_text = clean_xml_text(text)
        
        if rend == 'subhead':
            markdown_lines.append(f"### {clean_text}")
        elif rend == 'centre':
            markdown_lines.append(f"*{clean_text}*")
        else:
            markdown_lines.append(clean_text)
        markdown_lines.append("")
        
    content = '\n'.join(markdown_lines).strip()
    
    frontmatter = """---
id: MN118_tik
title_pali: Ānāpānasati Suttavaṇṇanātīkā
type: tika
pitaka: sutta
nikaya: majjhima
sutta_number: 118
mula_file: /mula/sutta/majjhima_nikaya/mn118.md
commentary_file: /atthakatha/sutta/majjhima_nikaya/mn118_att.md
---

"""
    
    with open(OUTPUT_TIK, "w", encoding="utf-8") as f:
        f.write(frontmatter + content + "\n")
        
    word_count = len(content.split())
    print(f"Sub-commentary written to {OUTPUT_TIK} ({word_count} words).")
    return frontmatter, word_count

def main():
    os.makedirs(os.path.dirname(OUTPUT_MULA), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_ATT), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_TIK), exist_ok=True)
    
    mula_fm, mula_wc = process_mula()
    att_fm, att_wc = process_commentary()
    tik_fm, tik_wc = process_sub_commentary()
    
    print("\n================== SUMMARY ==================")
    print(f"Mula: {mula_wc} words")
    print(f"Commentary: {att_wc} words")
    print(f"Sub-commentary: {tik_wc} words")
    print("=============================================\n")

if __name__ == "__main__":
    main()
