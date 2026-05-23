import urllib.request
import re

for i in range(15, 45):
    url = f"https://tipitaka.org/romn/cscd/s0403a.att{i}.xml"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            content = r.read()
            try:
                text = content.decode('utf-16')
            except:
                text = content.decode('utf-8', errors='replace')
            print(f"File {i}: {len(text)} chars")
            
            # Find the first few headings
            headings = []
            for m in re.finditer(r'<p rend="subhead.*?">(.*?)</p>', text, re.DOTALL):
                clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                headings.append(clean)
            for m in re.finditer(r'<p rend="book">(.*?)</p>', text, re.DOTALL):
                clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                headings.append("BOOK: " + clean)
            print(f"  Headings: {headings[:5]}")
    except Exception as e:
        pass
