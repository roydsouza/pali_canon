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

suttas = [
    {"name": "Uraga", "start": 41, "end": 134},
    {"name": "Dhaniya", "start": 135, "end": 197},
    {"name": "Kasibharadvaja", "start": 505, "end": 571},
    {"name": "Cunda", "start": 572, "end": 594},
    {"name": "Parabhava", "start": 595, "end": 629},
    {"name": "Vasala", "start": 630, "end": 694},
    {"name": "Hemavata", "start": 765, "end": 826},
    {"name": "Alavaka", "start": 827, "end": 897},
    {"name": "Vijaya", "start": 898, "end": 946},
    {"name": "Muni", "start": 947, "end": 997}
]

for s in suttas:
    print(f"\n=== Sutta: {s['name']} (range {s['start']} to {s['end']}) ===")
    found = []
    for idx in range(s['start'], s['end'] + 1):
        rend, p_text = ps[idx]
        m = re.search(r'<hi rend="paranum">([^<]+)</hi>', p_text)
        if m:
            found.append((idx, m.group(1)))
    print(f"Total paranums found: {len(found)}")
    if found:
        print(f"First 3: {found[:3]}")
        print(f"Last 3: {found[-3:]}")
