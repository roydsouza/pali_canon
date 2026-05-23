import urllib.request
import re
import time
import html as hmod

GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

# Target suttas we want to map
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
    "sn36": "Vedanā",
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
    "an6.25": "Anussatiṭṭhāna",
    "an8.54": "Dīghajāṇu",
    "an8.63": "Saṅkhitta",
    "an8.73": "Maraṇassati",
    "an9.34": "Nibbānasukha",
    "an9.35": "Gāvīupama",
    "an11.12": "Mahānāma",
    "an11.15": "Mettā",
}

# We'll search these potential XML files for both Atthakatha (.att) and Tika (.tik)
FILES_TO_CHECK = [
    # DN Atthakatha
    "s0101a.att1.xml", "s0101a.att2.xml", "s0101a.att3.xml",
    "s0102a.att1.xml", "s0102a.att2.xml", "s0102a.att3.xml", "s0102a.att4.xml", "s0102a.att5.xml", "s0102a.att6.xml", "s0102a.att7.xml", "s0102a.att8.xml", "s0102a.att9.xml", "s0102a.att10.xml", "s0102a.att11.xml", "s0102a.att12.xml", "s0102a.att13.xml",
    # DN Tika
    "s0101t.tik1.xml", "s0101t.tik2.xml", "s0101t.tik3.xml",
    "s0102t.tik1.xml", "s0102t.tik2.xml", "s0102t.tik3.xml", "s0102t.tik4.xml", "s0102t.tik5.xml", "s0102t.tik6.xml", "s0102t.tik7.xml", "s0102t.tik8.xml", "s0102t.tik9.xml", "s0102t.tik10.xml", "s0102t.tik11.xml", "s0102t.tik12.xml", "s0102t.tik13.xml",
    # MN Atthakatha
    "s0201a.att1.xml", "s0201a.att2.xml", "s0201a.att3.xml", "s0201a.att4.xml", "s0201a.att5.xml",
    "s0202a.att1.xml", "s0202a.att2.xml", "s0202a.att3.xml", "s0202a.att4.xml", "s0202a.att5.xml",
    "s0203a.att1.xml", "s0203a.att2.xml", "s0203a.att3.xml", "s0203a.att4.xml", "s0203a.att5.xml",
    # MN Tika
    "s0201t.tik1.xml", "s0201t.tik2.xml", "s0201t.tik3.xml", "s0201t.tik4.xml", "s0201t.tik5.xml",
    "s0202t.tik1.xml", "s0202t.tik2.xml", "s0202t.tik3.xml", "s0202t.tik4.xml", "s0202t.tik5.xml",
    "s0203t.tik1.xml", "s0203t.tik2.xml", "s0203t.tik3.xml", "s0203t.tik4.xml", "s0203t.tik5.xml",
    # SN Atthakatha
    "s0301a.att.xml", "s0302a.att.xml", "s0303a.att1.xml", "s0303a.att2.xml", "s0304a.att.xml",
    "s0305a.att1.xml", "s0305a.att2.xml", "s0305a.att3.xml", "s0305a.att4.xml", "s0305a.att5.xml", "s0305a.att6.xml", "s0305a.att7.xml", "s0305a.att8.xml",
    # SN Tika
    "s0301t.tik.xml", "s0302t.tik.xml", "s0303t.tik.xml", "s0304t.tik.xml",
    "s0305t.tik1.xml", "s0305t.tik2.xml", "s0305t.tik3.xml", "s0305t.tik4.xml", "s0305t.tik5.xml", "s0305t.tik6.xml", "s0305t.tik7.xml", "s0305t.tik8.xml",
    # AN Atthakatha
    "s0401a.att.xml", "s0402a.att1.xml", "s0402a.att2.xml", "s0402a.att3.xml", "s0402a.att4.xml",
    "s0403a.att1.xml", "s0403a.att2.xml", "s0403a.att3.xml", "s0403a.att4.xml", "s0403a.att5.xml",
    "s0404a.att1.xml", "s0404a.att2.xml", "s0404a.att3.xml", "s0404a.att4.xml",
    # AN Tika
    "s0401t.tik.xml", "s0402t.tik1.xml", "s0402t.tik2.xml", "s0402t.tik3.xml", "s0402t.tik4.xml",
    "s0403t.tik1.xml", "s0403t.tik2.xml", "s0403t.tik3.xml", "s0403t.tik4.xml", "s0403t.tik5.xml",
    "s0404t.tik1.xml", "s0404t.tik2.xml", "s0404t.tik3.xml", "s0404t.tik4.xml"
]

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

print("Starting scan of CSCD XML files...")
mappings = {}

for f in FILES_TO_CHECK:
    content = fetch_content(f)
    if not content:
        continue
    
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paragraphs:
        p_clean = re.sub(r'<[^>]+>', '', p)
        p_clean = hmod.unescape(p_clean)
        
        for tid, keyword in TARGETS.items():
            # Match only headings: e.g. "1. Sabbāsavasuttavaṇṇanā" or "4. Mettāsahagatasuttavaṇṇanā"
            m = re.search(r'^\s*(\d+)\.\s+(\w*' + keyword + r'\w*(?:[vaV]aṇṇanā|ṭīkā|sutta)\w*)', p_clean, re.IGNORECASE)
            if m:
                pnum = m.group(1)
                heading = m.group(2)
                layer = "tika" if "tik" in f else "att"
                mappings.setdefault(tid, {}).setdefault(layer, []).append({
                    "file": f,
                    "heading": p_clean.strip(),
                    "pattern": rf"{pnum}\.\s+{re.escape(heading)}"
                })

# Print findings in structured format
import json
print(json.dumps(mappings, indent=2))
