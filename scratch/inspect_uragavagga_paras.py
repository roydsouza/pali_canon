import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/s0505a.att0.xml"

print("Fetching XML...")
req = urllib.request.Request(TIPITAKA, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    content = r.read()

try:
    text = content.decode('utf-16')
except:
    text = content.decode('utf-8', errors='replace')

ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', text, re.DOTALL)
print(f"Total paragraphs parsed: {len(ps)}")

print("\n--- Subheads and paragraph indexes ---")
for idx, (rend, p_text) in enumerate(ps):
    # Clean tags from text
    clean_text = re.sub(r'<[^>]+>', '', p_text).strip()
    if rend == "subhead" or "vaṇṇanā" in clean_text.lower():
        print(f"Index {idx}: rend={rend}, text={clean_text[:60]}")
