import urllib.request
import json
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/s0505a.att0.xml"
api_base = "https://suttacentral.net/api/bilarasuttas/snp1.4/sujato"

print("Fetching XML...")
req = urllib.request.Request(TIPITAKA, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    xml_content = r.read()

try:
    xml_text = xml_content.decode('utf-16')
except:
    xml_text = xml_content.decode('utf-8', errors='replace')

ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', xml_text, re.DOTALL)

print("Fetching Mūla...")
req2 = urllib.request.Request(api_base, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req2, timeout=30) as r:
    mula_data = json.loads(r.read().decode('utf-8'))

root = mula_data.get("root_text", {})
keys = mula_data.get("keys_order", [])

print("\n--- Mūla Verse Keys and Text ---")
for k in keys:
    if re.search(r':0\.\d+$', k):
        continue
    p = root.get(k, "").strip()
    m = re.search(r':(\d+)\.(\d+)$', k)
    if m:
        v_num, l_num = m.group(1), m.group(2)
        if l_num == "1":
            print(f"Verse {v_num}: {p[:60]}")

print("\n--- Commentary Paragraphs for Snp 1.4 ---")
for idx in range(505, 572):
    rend, p_text = ps[idx]
    clean_text = re.sub(r'<[^>]+>', '', p_text).strip()
    m = re.search(r'<hi rend="paranum">([^<]+)</hi>', p_text)
    if m:
        print(f"Index {idx}: paranum={m.group(1)}, text={clean_text[:100]}")
    elif rend == "subhead":
        print(f"Index {idx}: SUBHEAD={clean_text}")
