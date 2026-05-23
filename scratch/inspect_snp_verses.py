import urllib.request
import json
import re
import time

sc_ids = ["snp1.1", "snp1.2", "snp1.4", "snp1.5", "snp1.6", "snp1.7", "snp1.9", "snp1.10", "snp1.11", "snp1.12"]
api_base = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

for sc_id in sc_ids:
    url = api_base.format(sc_id)
    print(f"\nFetching {sc_id}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
        root = data.get("root_text", {})
        keys = data.get("keys_order", [])
        
        # Parse verse numbers
        verses = set()
        for k in keys:
            if re.search(r':0\.\d+$', k):
                continue
            m = re.search(r':(\d+)\.(\d+)$', k)
            if m:
                verses.add(int(m.group(1)))
        
        print(f"  SUCCESS! Total segments: {len(keys)}")
        if verses:
            print(f"  Verse range: {min(verses)} to {max(verses)} (Total verses: {len(verses)})")
        else:
            print("  No standard verse keys found.")
            # Print first 5 keys
            print(f"  First 5 keys: {keys[:5]}")
            
    except Exception as e:
        print(f"  FAILED: {e}")
    time.sleep(0.5)
