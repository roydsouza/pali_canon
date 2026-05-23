import urllib.request
import re
import html as hmod

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def fetch_file(filename):
    for base in [GITHUB, TIPITAKA]:
        url = base.format(filename)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                content = r.read()
            try:
                return content.decode('utf-16')
            except:
                return content.decode('utf-8', errors='replace')
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
    raise RuntimeError(f"Could not fetch {filename} from any source.")

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def load_paras(content):
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results

def inspect_range(paras, start_num, end_num):
    found = []
    started = False
    for rend, pnum, text in paras:
        if pnum:
            val = int(pnum)
            if val == start_num:
                started = True
            elif val > end_num:
                break
        if started:
            found.append((rend, pnum, text))
    return found

print("=== MN 19 Atthakatha (s0201a.att2.xml) ===")
att_content = fetch_file("s0201a.att2.xml")
att_paras = load_paras(att_content)
print(f"Total paragraphs parsed: {len(att_paras)}")
# Let's search for paragraph containing "Dvedhāvitakka" to verify
mn19_att_start = None
mn19_att_end = None
for i, (rend, pnum, text) in enumerate(att_paras):
    if "9. Dvedhāvitakkasuttavaṇṇanā" in text:
        mn19_att_start = i
    if "Dvedhāvitakkasuttavaṇṇanā niṭṭhitā" in text:
        mn19_att_end = i
        break

print(f"MN 19 Att range: {mn19_att_start} to {mn19_att_end}")
if mn19_att_start is not None and mn19_att_end is not None:
    for idx in range(mn19_att_start, mn19_att_end + 1):
        rend, pnum, text = att_paras[idx]
        print(f"[{idx}] pnum={pnum} ({rend}): {text[:150]}...")

print("\n=== MN 19 Tika (s0201t.tik2.xml) ===")
tik_content = fetch_file("s0201t.tik2.xml")
tik_paras = load_paras(tik_content)
print(f"Total paragraphs parsed: {len(tik_paras)}")

mn19_tik_start = None
mn19_tik_end = None
for i, (rend, pnum, text) in enumerate(tik_paras):
    if "9. Dvedhāvitakkasuttavaṇṇanā" in text:
        mn19_tik_start = i
    if "Dvedhāvitakkasuttavaṇṇanā niṭṭhitā" in text or "Vitakkasaṇṭhānasuttavaṇṇanātīkā" in text:
        # Let's see if there is a niṭṭhitā
        pass

# Let's find by pnum or text
for i, (rend, pnum, text) in enumerate(tik_paras):
    if "9. Dvedhāvitakkasuttavaṇṇanā" in text:
        mn19_tik_start = i
    if mn19_tik_start is not None and i > mn19_tik_start:
        if "Vitakkasaṇṭhāna" in text or "10." in text:
            mn19_tik_end = i - 1
            break
if mn19_tik_end is None:
    mn19_tik_end = len(tik_paras) - 1

print(f"MN 19 Tik range: {mn19_tik_start} to {mn19_tik_end}")
if mn19_tik_start is not None:
    for idx in range(mn19_tik_start, mn19_tik_end + 1):
        rend, pnum, text = tik_paras[idx]
        print(f"[{idx}] pnum={pnum} ({rend}): {text[:150]}...")

print("\n=== AN 10.60 Atthakatha (s0404a.att20.xml) ===")
an_content = fetch_file("s0404a.att20.xml")
an_paras = load_paras(an_content)
print(f"Total paragraphs parsed: {len(an_paras)}")
for idx, (rend, pnum, text) in enumerate(an_paras):
    print(f"[{idx}] pnum={pnum} ({rend}): {text[:150]}...")

