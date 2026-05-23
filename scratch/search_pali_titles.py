import urllib.request
import re
import html as hmod

GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

KEYWORDS = {
    "mn51": ["kandaraka"],
    "mn128": ["upakkilesa"],
    "mn140": ["dhātuvibhaṅga"],
    "mn148": ["chachakka"],
    "dn13": ["tevijja"],
    "sn36.6": ["sallatha"],
    "sn36.11": ["rahogata"],
    "sn36.21": ["sīvaka"],
    "sn46.54": ["mettā"],
    "sn47.13": ["cunda"],
    "an4.67": ["ahi", "khandha"],
    "an4.99": ["sikkhāpada"],
    "an4.125": ["mettā"],
    "an4.126": ["mettā"],
    "an6.10": ["mahānāma"],
    "an6.19": ["maraṇa"],
    "an6.20": ["maraṇa"],
    "an6.25": ["anussati"],
    "an8.54": ["dīghajāṇu", "vyagghapajja"],
    "an8.63": ["saṅkhitta", "sankhitta"],
    "an8.73": ["maraṇa"],
    "an9.34": ["nibbāna"],
    "an9.35": ["gāvī"],
    "an11.12": ["mahānāma"],
    "an11.15": ["mettā"],
}

FILES = [
    # DN
    "s0101a.att1.xml", "s0101a.att2.xml", "s0101a.att3.xml",
    "s0102a.att1.xml", "s0102a.att2.xml", "s0102a.att3.xml", "s0102a.att4.xml", "s0102a.att5.xml", "s0102a.att6.xml", "s0102a.att7.xml", "s0102a.att8.xml", "s0102a.att9.xml", "s0102a.att10.xml", "s0102a.att11.xml", "s0102a.att12.xml", "s0102a.att13.xml",
    # MN
    "s0201a.att1.xml", "s0201a.att2.xml", "s0201a.att3.xml", "s0201a.att4.xml", "s0201a.att5.xml",
    "s0202a.att1.xml", "s0202a.att2.xml", "s0202a.att3.xml", "s0202a.att4.xml", "s0202a.att5.xml",
    "s0203a.att1.xml", "s0203a.att2.xml", "s0203a.att3.xml", "s0203a.att4.xml", "s0203a.att5.xml",
    # SN
    "s0301a.att.xml", "s0302a.att.xml", "s0303a.att1.xml", "s0303a.att2.xml", "s0304a.att.xml",
    "s0305a.att1.xml", "s0305a.att2.xml", "s0305a.att3.xml", "s0305a.att4.xml", "s0305a.att5.xml", "s0305a.att6.xml", "s0305a.att7.xml", "s0305a.att8.xml",
    # AN
    "s0401a.att.xml", "s0402a.att1.xml", "s0402a.att2.xml", "s0402a.att3.xml", "s0402a.att4.xml",
    "s0403a.att1.xml", "s0403a.att2.xml", "s0403a.att3.xml", "s0403a.att4.xml", "s0403a.att5.xml",
    "s0404a.att1.xml", "s0404a.att2.xml", "s0404a.att3.xml", "s0404a.att4.xml"
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
    except:
        if use_github:
            return fetch_content(filename, use_github=False)
        return ""

print("Searching for headings...")
for f in FILES:
    content = fetch_content(f)
    if not content:
        continue
    
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for i, p in enumerate(paragraphs):
        p_clean = re.sub(r'<[^>]+>', '', p)
        p_clean = hmod.unescape(p_clean).strip()
        
        # Sutta headings typically start with a number
        m = re.match(r'^(\d+)\.\s+(.*)', p_clean)
        if m:
            pnum = m.group(1)
            title = m.group(2)
            # Check if any keyword matches the title
            for sutta_id, kw_list in KEYWORDS.items():
                for kw in kw_list:
                    if kw in title.lower():
                        print(f"[{sutta_id}] File: {f}, Para: {i}, Num: {pnum}, Title: {title}")
