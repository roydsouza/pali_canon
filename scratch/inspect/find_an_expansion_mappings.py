#!/usr/bin/env python3
import urllib.request
import re
import json
import html as hmod

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

# Target suttas
TARGETS = {
    "an7.65": "Satthusāsana", # AN 7.65 Satthusāsanā / Bojjhaṅga
    "an8.53": "Gotamī",      # AN 8.53 Gotamīsutta
    "an11.1": "Kimatthiya",  # AN 11.1 Kimatthiyasutta
    "an11.2": "Cetanākaraṇīya", # AN 11.2 Cetanākaraṇīyasutta
    "an11.3": "Paṭhamaupanisa", # AN 11.3 Upanisasutta / Upanisā
    "an11.4": "Dutiyaupanisa",
    "an11.5": "Tatiyaupanisa",
    "mn22": "Alagaddūpama",  # MN 22 Alagaddūpama
    "mn117": "Mahācattārīsaka", # MN 117 Mahācattārīsaka
}

def fetch_content(filename, use_github=True):
    base = GITHUB if use_github else TIPITAKA
    url = base.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            try:
                return raw.decode('utf-16')
            except:
                return raw.decode('utf-8', errors='replace')
    except Exception as e:
        if use_github:
            return fetch_content(filename, use_github=False)
        return ""

# We will generate a list of files to check.
# For AN, s0403a.att*.xml ranges from att0 to att40+; let's scan all of them!
files_to_check = []
# AN 7 and 8 are in s0403a / s0403t
for i in range(50):
    files_to_check.append(f"s0403a.att{i}.xml")
    files_to_check.append(f"s0403t.tik{i}.xml")
# AN 11 is in s0404a / s0404t
for i in range(40):
    files_to_check.append(f"s0404a.att{i}.xml")
    files_to_check.append(f"s0404t.tik{i}.xml")
# MN 22 is in s0201a.att3.xml / s0201t.tik3.xml
# MN 117 is in s0203a.att1.xml / s0203t.tik1.xml
files_to_check.extend([
    "s0201a.att3.xml", "s0201t.tik3.xml",
    "s0203a.att1.xml", "s0203t.tik1.xml"
])

print("Scanning files for mappings...")
mappings = {}

for f in files_to_check:
    content = fetch_content(f)
    if not content:
        continue
    
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paragraphs:
        p_clean = re.sub(r'<[^>]+>', '', p)
        p_clean = hmod.unescape(p_clean)
        
        for tid, keyword in TARGETS.items():
            m = re.search(r'^\s*(\d+[-–]\d+|\d+)\.\s+(\w*' + keyword + r'\w*(?:[vaV]aṇṇanā|ṭīkā|sutta|suttā)\w*)', p_clean, re.IGNORECASE)
            if m:
                pnum = m.group(1)
                heading = m.group(2)
                layer = "tika" if "tik" in f else "att"
                mappings.setdefault(tid, {}).setdefault(layer, []).append({
                    "file": f,
                    "heading": p_clean.strip(),
                    "pattern": rf"{pnum}\.\s+{re.escape(heading)}"
                })

print("\nScan complete. Mappings found:")
print(json.dumps(mappings, indent=2))
