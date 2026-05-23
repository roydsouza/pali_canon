import urllib.request
import json

url = "https://suttacentral.net/api/bilarasuttas/snp1.8/sujato"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode('utf-8'))

root = data.get("root_text", {})
trans = data.get("translation_text", {})

keys = data.get("keys_order", [])
print(f"Total keys: {len(keys)}")
# Print first 20 keys
print("--- First 20 keys ---")
for key in keys[:20]:
    print(f"{key} | P: {root.get(key, '')[:50]} | E: {trans.get(key, '')[:50]}")

# Print last 10 keys
print("\n--- Last 10 keys ---")
for key in keys[-10:]:
    print(f"{key} | P: {root.get(key, '')[:50]} | E: {trans.get(key, '')[:50]}")
