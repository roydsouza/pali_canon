import json
import re
import urllib.request
import html as hmod

GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

TARGETS = [
    "mn128", "an9.34", "an9.35", "mn8", "an8.63", "mn148", "sn36.6", "sn36.11", "sn36.21",
    "mn28", "mn140", "mn2", "mn7", "dn13", "an11.15", "an6.10", "an11.12", "an6.25",
    "mn27", "mn51", "an8.54", "an4.99", "an6.19", "an6.20", "an8.73", "an4.67"
]

def fetch_content(filename):
    for base in [GITHUB, TIPITAKA]:
        url = base.format(filename)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                raw = r.read()
                try:
                    return raw.decode('utf-16')
                except:
                    return raw.decode('utf-8', errors='replace')
        except:
            pass
    return ""

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_cscd_paras(filename):
    content = fetch_content(filename)
    if not content:
        return []
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs   = m.group(1)
        body    = m.group(2)
        rend_m  = re.search(r'rend="([^"]+)"', attrs)
        rend    = rend_m.group(1) if rend_m else ''
        pnum_m  = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body    = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text    = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results

def extract_section(paras, section_pattern):
    if not section_pattern:
        return paras
    pat = re.compile(section_pattern, re.IGNORECASE)
    # Stop pattern matching any number (single or range) followed by a dot and heading keywords
    stop_pat = re.compile(r'^(?:\d+-\d+|\d+)\.\s+\S*(?:sutta|suttā|vaṇṇanā|ṭīkā|vagga|Vagga|Sutta|Vaṇṇanā|Ṭīkā)', re.IGNORECASE)
    start = None
    for i, (rend, pnum, text) in enumerate(paras):
        if start is None:
            if pat.search(text):
                start = i
        else:
            if stop_pat.match(text) and not pat.search(text):
                return paras[start:i]
    if start is None:
        return []
    return paras[start:]

with open("scratch/cscd_mappings_all.json") as f:
    mappings = json.load(f)

print("Starting dry-run extraction test...")
for sc_id in TARGETS:
    entry = mappings.get(sc_id)
    if not entry:
        print(f"[{sc_id}] ERROR: No mapping entry!")
        continue
    
    # Atthakatha
    att_map = entry["att"][0]
    att_file = att_map["file"]
    att_pat = att_map["pattern"]
    att_paras = load_cscd_paras(att_file)
    extracted_att = extract_section(att_paras, att_pat)
    
    # Tika (if available)
    tika_file, tika_pat, extracted_tika = "None", "None", []
    if "tika" in entry and entry["tika"]:
        tika_map = entry["tika"][0]
        tika_file = tika_map["file"]
        tika_pat = tika_map["pattern"]
        tika_paras = load_cscd_paras(tika_file)
        extracted_tika = extract_section(tika_paras, tika_pat)
    
    print(f"[{sc_id}] Att: {att_file} ({len(extracted_att)} paras) | Tika: {tika_file} ({len(extracted_tika)} paras)")
    if len(extracted_att) == 0:
        print(f"  --> ERROR: 0 paragraphs extracted for Atthakatha! Pattern was: {att_pat}")
    if "tika" in entry and entry["tika"] and len(extracted_tika) == 0:
        print(f"  --> ERROR: 0 paragraphs extracted for Tika! Pattern was: {tika_pat}")
