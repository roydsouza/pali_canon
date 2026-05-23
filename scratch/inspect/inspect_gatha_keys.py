import urllib.request
import json

def inspect_keys(sc_id):
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        print(f"\n===== Keys for {sc_id} =====")
        keys = data.get("keys_order", [])
        for k in keys[:15]:
            print(f"  {k}: root='{data['root_text'].get(k)}' translation='{data['translation_text'].get(k)}'")
    except Exception as e:
        print(f"Error {sc_id}: {e}")

inspect_keys("thag1.1")
inspect_keys("thig1.1")
