#!/usr/bin/env python3
import urllib.request
import json

def test_fetch(sc_id):
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            keys = data.get("keys_order", [])
            print(f"Success: {sc_id} has {len(keys)} segments")
            if keys:
                print(f"  First key: {keys[0]}")
                print(f"  Pali: {data['root_text'].get(keys[0])}")
                print(f"  English: {data['translation_text'].get(keys[0])}")
    except Exception as e:
        print(f"Error {sc_id}: {e}")

# Let's test a few different IDs for AN 1
test_fetch("an1.1-10")
test_fetch("an1.1")
test_fetch("an1.11")
test_fetch("an1.21-30")
