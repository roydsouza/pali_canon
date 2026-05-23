#!/usr/bin/env python3
import urllib.request
import json

url = "https://suttacentral.net/api/suttaplex/an1"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode('utf-8'))
        print("Suttaplex list of AN 1 suttas:")
        for item in data:
            uid = item.get("uid")
            acronym = item.get("acronym")
            name = item.get("name")
            print(f"  uid: {uid} | acronym: {acronym} | name: {name}")
except Exception as e:
    print(f"Error: {e}")
