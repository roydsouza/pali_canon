#!/usr/bin/env python3
import urllib.request
import re
import json
import html as hmod

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"

# 31 ranges from suttaplex
RANGES = [
    "an1.1-10", "an1.11-20", "an1.21-30", "an1.31-40", "an1.41-50",
    "an1.51-60", "an1.61-70", "an1.71-81", "an1.82-97", "an1.98-139",
    "an1.140-149", "an1.150-169", "an1.170-187", "an1.188-197", "an1.198-208",
    "an1.209-218", "an1.219-234", "an1.235-247", "an1.248-257", "an1.258-267",
    "an1.268-277", "an1.278-286", "an1.287-295", "an1.296-305", "an1.306-315",
    "an1.316-332", "an1.333-377", "an1.378-393", "an1.394-574", "an1.575-615",
    "an1.616-627"
]

def fetch_content(filename):
    url = GITHUB.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            return raw.decode('utf-16') if b'\xff\xfe' in raw or b'\xfe\xff' in raw else raw.decode('utf-8')
    except Exception as e:
        return ""

print("Fetching all CSCD AN 1 files...")
att_contents = {}
tik_contents = {}
for i in range(20):
    f_att = f"s0401a.att{i}.xml"
    content_att = fetch_content(f_att)
    if content_att:
        att_contents[f_att] = content_att
    f_tik = f"s0401t.tik{i}.xml"
    content_tik = fetch_content(f_tik)
    if content_tik:
        tik_contents[f_tik] = content_tik

print(f"Loaded {len(att_contents)} Atthakatha files and {len(tik_contents)} Tika files.")

# Let's inspect headings in each file
print("\nExtracting headings from Atthakatha files...")
att_headings = []
for f, text in att_contents.items():
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', text, re.DOTALL):
        p_clean = re.sub(r'<[^>]+>', '', m.group(1))
        p_clean = hmod.unescape(p_clean).strip()
        if re.match(r'^\s*(\d+[-–]\d+|\d+)\.\s+\w*vaggavaṇṇanā', p_clean, re.IGNORECASE) or "vaggavaṇṇanā" in p_clean.lower() or "vaṇṇanā" in p_clean.lower():
            if re.match(r'^\s*(\d+[-–]\d+|\d+)\.\s+', p_clean):
                att_headings.append((f, p_clean))
                print(f"  {f} -> {p_clean}")

print("\nExtracting headings from Tika files...")
tik_headings = []
for f, text in tik_contents.items():
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', text, re.DOTALL):
        p_clean = re.sub(r'<[^>]+>', '', m.group(1))
        p_clean = hmod.unescape(p_clean).strip()
        if "ṭīkā" in p_clean.lower() or "vaṇṇanā" in p_clean.lower():
            if re.match(r'^\s*(\d+[-–]\d+|\d+)\.\s+', p_clean):
                tik_headings.append((f, p_clean))
                print(f"  {f} -> {p_clean}")
