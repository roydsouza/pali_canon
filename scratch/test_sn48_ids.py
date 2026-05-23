import urllib.request
import json
import time

def check_sutta(sc_id):
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        root = data.get("root_text", {})
        tr = data.get("translation_text", {})
        title_pali = root.get(f"{sc_id}:0.3", root.get(f"{sc_id}:0.2", "")).strip()
        title_en = tr.get(f"{sc_id}:0.3", tr.get(f"{sc_id}:0.2", "")).strip()
        if not title_pali:
            title_pali = root.get(f"{sc_id}:0.1", "").strip()
        if not title_en:
            title_en = tr.get(f"{sc_id}:0.1", "").strip()
        print(f"{sc_id}: {title_pali} — {title_en}")
        return True
    except Exception as e:
        # print(f"{sc_id}: ERROR {e}")
        return False

print("Probing SN 48 suttas...")
available = []
for i in range(1, 150):
    sc_id = f"sn48.{i}"
    if check_sutta(sc_id):
        available.append(i)
    time.sleep(0.1)
print(f"Total available: {len(available)}")
print("Available IDs:", available)
