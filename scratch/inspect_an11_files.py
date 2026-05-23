import urllib.request
import re
import html as hmod

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"
GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"

def check_file(filename):
    url = GITHUB.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read()
    except Exception:
        url = TIPITAKA.format(filename)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read()
        except:
            return
            
    try:    text = content.decode('utf-16')
    except: text = content.decode('utf-8', errors='replace')
    
    headings = []
    for m in re.finditer(r'<p rend="subhead.*?">(.*?)</p>', text, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        headings.append(clean)
    for m in re.finditer(r'<p rend="title">(.*?)</p>', text, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        headings.append("TITLE: " + clean)
    for m in re.finditer(r'<p rend="book">(.*?)</p>', text, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        headings.append("BOOK: " + clean)
        
    print(f"File: {filename} ({len(content)} bytes)")
    print(f"  Headings: {headings[:10]}\n")

for i in range(25, 33):
    check_file(f"s0404a.att{i}.xml")
