import urllib.request
import re
import time
import html as hmod
import json

GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

TARGETS = {
    # MN
    "mn2": "Sabbāsava",
    "mn7": "Vattha",
    "mn8": "Sallekha",
    "mn27": "Cūḷahatthipad",
    "mn28": "Mahāhatthipad",
    "mn51": "Kandaraka",
    "mn128": "Upakkilesa",
    "mn140": "Dhātuvibhaṅga",
    "mn148": "Chachakka",
    # DN
    "dn13": "Tevijja",
    # SN
    "sn36.6": "Sallatha",
    "sn36.11": "Rahogata",
    "sn36.21": "Sīvaka",
    "sn46.54": "Mettāsahagata",
    "sn47.13": "Cunda",
    # AN
    "an4.67": "Ahi",
    "an4.99": "Sikkhāpada",
    "an4.125": "Mettā",
    "an4.126": "Mettā",
    "an6.10": "Mahānāma",
    "an6.19": "Maraṇassati",
    "an6.20": "Maraṇassati",
    "an6.25": "Anussati",
    "an8.54": "Dīghajāṇu",
    "an8.63": "Saṅkhitta",
    "an8.73": "Maraṇassati",
    "an9.34": "Nibbānasukha",
    "an9.35": "Gāvīupama",
    "an11.12": "Mahānāma",
    "an11.15": "Mettā",
}

# Generate FILES_TO_CHECK dynamically
FILES_TO_CHECK = []

# DN
for i in range(15):
    FILES_TO_CHECK.append(f"s0101a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0101t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0102a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0102t.tik{i}.xml")

# MN
for i in range(10):
    FILES_TO_CHECK.append(f"s0201a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0201t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0202a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0202t.tik{i}.xml")
    FILES_TO_CHECK.append(f"s0203a.att{i}.xml")
    FILES_TO_CHECK.append(f"s0203t.tik{i}.xml")

# SN
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

# AN
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

print(f"Starting scan of {len(FILES_TO_CHECK)} CSCD XML files...")
mappings = {}

for idx, f in enumerate(FILES_TO_CHECK):
    if idx % 20 == 0:
        print(f"  Scanned {idx}/{len(FILES_TO_CHECK)} files...")
    content = fetch_content(f)
    if not content:
        continue
    
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paragraphs:
        p_clean = re.sub(r'<[^>]+>', '', p)
        p_clean = hmod.unescape(p_clean).strip()
        
        for tid, keyword in TARGETS.items():
            # Loose heading pattern: starts with a number and contains keyword + suffix
            m = re.search(r'^\s*(\d+)\.\s+(\w*' + keyword + r'\w*(?:[vaV]aṇṇanā|ṭīkā|sutta)\w*)', p_clean, re.IGNORECASE)
            if m:
                pnum = m.group(1)
                heading = m.group(2)
                layer = "tika" if "tik" in f else "att"
                mappings.setdefault(tid, {}).setdefault(layer, []).append({
                    "file": f,
                    "heading": p_clean,
                    "pattern": rf"{pnum}\.\s+{re.escape(heading)}"
                })

# Save to JSON
out_path = "scratch/cscd_mappings_all.json"
with open(out_path, "w", encoding="utf-8") as f_out:
    json.dump(mappings, f_out, indent=2)
print(f"Mappings written to {out_path}")
