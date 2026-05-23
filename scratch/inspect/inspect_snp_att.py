import urllib.request
import re
import html

TIPITAKA = "https://tipitaka.org/romn/cscd/s0505a.att0.xml"

print("Downloading s0505a.att0.xml...")
req = urllib.request.Request(TIPITAKA, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    content = r.read()

try:
    text = content.decode('utf-16')
except:
    text = content.decode('utf-8', errors='replace')

ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', text, re.DOTALL)
print(f"Total paragraphs found: {len(ps)}")

# Print subheads and titles to map out the file structure
for idx, (rend, p_text) in enumerate(ps):
    clean = re.sub(r'<[^>]+>', '', p_text).strip()
    if rend in ['title', 'subhead', 'chapter', 'book']:
        print(f"[{idx}] rend={rend}: {clean}")
