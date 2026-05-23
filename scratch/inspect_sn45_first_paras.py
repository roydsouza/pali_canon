import urllib.request
import re
import html as hmod

def inspect():
    url_att = "https://tipitaka.org/romn/cscd/s0305a.att0.xml"
    req = urllib.request.Request(url_att, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    
    try:
        content = raw.decode('utf-16')
    except:
        content = raw.decode('utf-8', errors='replace')
        
    paras = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text = re.sub(r'<[^>]+>', '', body)
        text = hmod.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        paras.append((rend, paranum, text))
        
    for i in range(4, 12):
        if i < len(paras):
            rend, paranum, text = paras[i]
            print(f"[{i}] ({paranum}) {text[:150]}")

if __name__ == "__main__":
    inspect()
