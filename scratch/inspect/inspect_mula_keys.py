import json
import urllib.request
import re

API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

def inspect_mula(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.load(r)
    root = data["root_text"]
    keys = data["keys_order"]
    
    print(f"=== {sc_id} (Total segments: {len(keys)}) ===")
    # Print the first few keys and their text
    for k in keys[:15]:
        print(f"  {k}: {root.get(k, '')}")
    print("  ...")
    # Print some interesting middle keys (e.g. matching certain patterns)
    for k in keys:
        txt = root.get(k, '')
        if "parinibb" in txt.lower() or "ajjhimasīla" in txt.lower() or "mahāsīla" in txt.lower() or "āmantayāmi vo" in txt.lower() or "gambhīrā" in txt.lower() or "attamanā te" in txt.lower():
            print(f"  MATCH {k}: {txt[:100]}")
    # Print the last few keys
    for k in keys[-5:]:
        print(f"  {k}: {root.get(k, '')}")
    print()

for sc_id in ["dn1", "dn16", "dn21"]:
    inspect_mula(sc_id)
