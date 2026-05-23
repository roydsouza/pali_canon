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

print("--- SN 1.3 Khaggavisana commentary sample ---")
for idx in range(198, 210):
    rend, p_text = ps[idx]
    print(f"[{idx}] rend={rend}: {p_text[:200]}...")

print("\n--- SN 1.8 Metta commentary sample ---")
for idx in range(695, 705):
    rend, p_text = ps[idx]
    print(f"[{idx}] rend={rend}: {p_text[:200]}...")
