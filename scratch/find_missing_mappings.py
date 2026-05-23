import urllib.request
import re
import html as hmod

GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

# We want to find mappings for:
# AN 9.35 (Gāvīupamasutta / Gāvīupama / Gāvī)
# AN 8.63 Saṅkhittasutta (or Saṃkhittasutta)
# SN 36.6 Sallasutta (or Sallatha or Salla)
# AN 4.99 Sikkhāpadasutta (or Sikkhāpada)

KEYWORDS = ["gāvī", "gāvi", "saṅkhitt", "saṃkhitt", "salla", "sikkhāpad"]

# Generate candidate files to check
FILES_TO_CHECK = []
# SN files
for i in range(15):
    FILES_TO_CHECK.append(f"s0301a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0301t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0302a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0302t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0303a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0303t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0304a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0304t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0305a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0305t.tik{i}.xml")

# AN files
for i in range(25):
    FILES_TO_CHECK.append(f"s0401a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0401t.tik{i}.xml")
for i in range(45):
    FILES_TO_CHECK.append(f"s0402a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0402t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0403a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0403t.tik{i}.xml")
for i in range(35):
    FILES_TO_CHECK.append(f"s0404a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0404t.tik{i}.xml")

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
    except:
        if use_github:
            return fetch_content(filename, use_github=False)
        return ""

print("Searching for missing suttas...")
for f in FILES_TO_CHECK:
    content = fetch_content(f)
    if not content:
        continue
    
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for i, p in enumerate(paragraphs):
        p_clean = re.sub(r'<[^>]+>', '', p)
        p_clean = hmod.unescape(p_clean).strip()
        
        # Check if any keyword matches
        for kw in KEYWORDS:
            if kw in p_clean.lower():
                # Let's see if this paragraph looks like a heading (e.g. starts with a number)
                # or contains vaṇṇanā / sutta / ṭīkā
                if re.search(r'^\s*\d+\.', p_clean) or "vaṇṇanā" in p_clean or "ṭīkā" in p_clean or "sutta" in p_clean:
                    print(f"File: {f} | Para {i} | Content: {p_clean}")
