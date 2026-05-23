#!/usr/bin/env python3
import urllib.request
import json

print("Checking AN 1 ranges...")
for i in range(1, 600, 10):
    # Try different formats, e.g., i to i+9
    start = i
    end = i + 9
    sc_id = f"an1.{start}-{end}"
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            keys = data.get("keys_order", [])
            if keys:
                print(f"  Valid: {sc_id} ({len(keys)} segments)")
    except:
        # Maybe it's a different range size? Let's check if we can fetch individual or other sizes
        pass
