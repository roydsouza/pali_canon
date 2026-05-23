import urllib.request
import re
import html as hmod

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

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
        text = clean_xml(body)
        if text:
            paras.append((rend, paranum, text))
            
    print(f"Total paragraphs: {len(paras)}")
    
    # Print headings and paragraphs with paranums
    print("\nHeadings and key paragraphs in SN 45 Atthakatha:")
    for idx, (rend, paranum, text) in enumerate(paras):
        is_heading = False
        if (re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or
            re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE)):
            is_heading = True
            print(f"[{idx}] (Heading) ## {text}")
        elif re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|suttavaṇṇanā|ṭīkā)', text):
            is_heading = True
            print(f"[{idx}] (Subheading) ### {text}")
        
        if paranum:
            # Print paranum along with its index and first 120 chars
            print(f"[{idx}] ({paranum}) {text[:120]}...")

if __name__ == "__main__":
    inspect()
