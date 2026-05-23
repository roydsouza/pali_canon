import urllib.request
import re
import html as hmod

url = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/s0201a.att1.xml"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    raw = r.read()
    try:
        content = raw.decode('utf-16')
    except:
        content = raw.decode('utf-8', errors='replace')

print("Length of content:", len(content))
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
print("Total paragraphs:", len(paragraphs))

# Print first 50 paragraphs that contain digits or 'sutta' or 'vaṇṇanā'
printed = 0
for i, p in enumerate(paragraphs):
    p_clean = re.sub(r'<[^>]+>', '', p)
    p_clean = hmod.unescape(p_clean)
    if any(keyword in p_clean.lower() for keyword in ["sutta", "vaṇṇanā", "vagga"]):
        print(f"[{i}] {p_clean[:120]}")
        printed += 1
        if printed >= 40:
            break
