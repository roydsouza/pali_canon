import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/s0505a.att0.xml"

req = urllib.request.Request(TIPITAKA, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    content = r.read()

try:
    text = content.decode('utf-16')
except:
    text = content.decode('utf-8', errors='replace')

ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', text, re.DOTALL)

print("--- SN 1.3 Commentary Paragraph Numbers ---")
for idx in range(198, 505):
    rend, p_text = ps[idx]
    m = re.search(r'<hi rend="paranum">(\d+)</hi>', p_text)
    if m:
        print(f"Index {idx} has paranum={m.group(1)}")

print("\n--- SN 1.8 Commentary Paragraph Numbers ---")
for idx in range(695, 765):
    rend, p_text = ps[idx]
    m = re.search(r'<hi rend="paranum">(\d+)</hi>', p_text)
    if m:
        print(f"Index {idx} has paranum={m.group(1)}")
