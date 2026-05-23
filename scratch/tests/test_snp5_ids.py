import urllib.request
import json

for i in range(1, 25):
    sc_id = f"snp5.{i}"
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
        print(f"FOUND {sc_id}: root keys={len(data.get('root_text', {}))}")
    except Exception as e:
        print(f"NOT FOUND {sc_id}: {e}")
