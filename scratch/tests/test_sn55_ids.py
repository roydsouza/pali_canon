import urllib.request
import json
import time

API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

IDS = [
    "sn55.1",
    "sn55.2",
    "sn55.3",
    "sn55.4",
    "sn55.5",
    "sn55.7",
    "sn55.21",
    "sn55.22",
    "sn55.24",
    "sn55.25",
    "sn55.26",
    "sn55.37",
    "sn55.40",
    "sn55.53",
    "sn55.54",
]

for sc_id in IDS:
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        title = data["translation_text"].get(f"{sc_id}:0.3", data["translation_text"].get(f"{sc_id}:0.2", "No title"))
        print(f"{sc_id}: {title} - {len(data['keys_order'])} segments")
    except Exception as e:
        print(f"{sc_id}: ERROR - {e}")
    time.sleep(0.2)
