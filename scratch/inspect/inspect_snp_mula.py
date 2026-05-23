import urllib.request
import json

sc_ids = ["snp1.3", "snp1.8"]
api_base = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

for sc_id in sc_ids:
    url = api_base.format(sc_id)
    print(f"Fetching {sc_id} from {url}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        print(f"  SUCCESS! Keys in response: {list(data.keys())}")
        root = data.get("root_text", {})
        translation = data.get("translation_text", {})
        print(f"  Root text has {len(root)} segments.")
        print(f"  Translation text has {len(translation)} segments.")
        if root:
            first_key = list(root.keys())[0]
            print(f"  Sample [{first_key}]:")
            print(f"    Pali: {root[first_key]}")
            print(f"    English: {translation.get(first_key, 'N/A')}")
    except Exception as e:
        print(f"  FAILED: {e}")
