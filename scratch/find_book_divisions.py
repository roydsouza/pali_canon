import urllib.request
import re
import html as hmod

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def get_first_paras(f):
    url = GITHUB.format(f)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
    except Exception:
        url = TIPITAKA.format(f)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                raw = r.read()
        except:
            return ""
    try:
        content = raw.decode('utf-16')
    except:
        content = raw.decode('utf-8', errors='replace')
    return content

for i in range(15):
    f = f"s0403a.att{i}.xml"
    content = get_first_paras(f)
    if not content:
        continue
    # Let's extract paragraphs containing 'nipāta' or starting with 'TITLE' or book tags
    paras = re.findall(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL)
    for j, (attrs, body) in enumerate(paras[:40]):
        body_clean = re.sub(r'<[^>]+>', '', body)
        body_clean = hmod.unescape(body_clean).strip()
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ""
        if "nipā" in body_clean.lower() or rend in ("book", "title") or re.search(r'^[1-9]\.\s+', body_clean):
            print(f"{f} [{j}]: rend={rend} | {body_clean[:120]}")
