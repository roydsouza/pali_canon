import urllib.request
import re
import html as hmod

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def load_cscd_paras(filename):
    req = urllib.request.Request(GITHUB.format(filename), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read()
    except Exception:
        req = urllib.request.Request(TIPITAKA.format(filename), headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read()
    
    try:    content = content.decode('utf-16')
    except: content = content.decode('utf-8', errors='replace')
    
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs  = m.group(1); body = m.group(2)
        pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body   = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text   = clean_xml(body)
        if text:
            results.append((paranum, text))
    return results

for label, filename in [("DN 1", "s0101a.att1.xml"), ("DN 16", "s0102a.att2.xml"), ("DN 21", "s0102a.att7.xml")]:
    print(f"=== {label}: {filename} ===")
    paras = load_cscd_paras(filename)
    p_with_num = [(pnum, text) for pnum, text in paras if pnum]
    print(f"Total paragraphs with numbers: {len(p_with_num)}")
    print("First 5 paragraphs with numbers:")
    for pnum, text in p_with_num[:5]:
        print(f"  ({pnum}) {text[:120]}...")
    print("Last 5 paragraphs with numbers:")
    for pnum, text in p_with_num[-5:]:
        print(f"  ({pnum}) {text[:120]}...")
    print()
