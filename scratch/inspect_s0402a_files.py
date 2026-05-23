import urllib.request
import re
import html as hmod

GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def get_content(f):
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
        return raw.decode('utf-16')
    except:
        return raw.decode('utf-8', errors='replace')

print("Scanning s0402a files...")
for i in range(40):
    f = f"s0402a.att{i}.xml"
    content = get_content(f)
    if not content:
        continue
    
    # Let's find any paragraph containing 'vaṇṇanā' or 'sutta' or starting with 'TITLE' or book tags
    paras = re.findall(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL)
    for j, (attrs, body) in enumerate(paras):
        body_clean = re.sub(r'<[^>]+>', '', body)
        body_clean = hmod.unescape(body_clean).strip()
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ""
        
        # Look for headings
        if "vaṇṇanā" in body_clean or "sutta" in body_clean.lower() or rend in ("book", "title") or re.search(r'^\d+\.\s+', body_clean):
            # Print if it looks like a heading
            if len(body_clean) < 100:
                print(f"{f} [{j}]: rend={rend} | {body_clean}")
