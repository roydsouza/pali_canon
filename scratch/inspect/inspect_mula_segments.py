import urllib.request
import json
import re

def fetch_sutta(sc_id):
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def search_text(data, word):
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    print(f"\nSearching for '{word}':")
    for k in keys:
        p = root.get(k, "")
        e = tr.get(k, "")
        if word.lower() in p.lower() or word.lower() in e.lower():
            print(f"[{k}] PALI: {p} | EN: {e}")

print("=== MN 19 Mula Fetch ===")
mn19_data = fetch_sutta("mn19")
print(f"Total segments: {len(mn19_data['keys_order'])}")
# Let's search for some typical terms or look at the start and headers
for k in mn19_data['keys_order'][:10]:
    print(f"[{k}] {mn19_data['root_text'].get(k)} // {mn19_data['translation_text'].get(k)}")

search_text(mn19_data, "dvedhāvitakka")
search_text(mn19_data, "appamattassa")
search_text(mn19_data, "kāmavitakko")
search_text(mn19_data, "byāpādavitakko")
search_text(mn19_data, "vihiṃsāvitakko")
search_text(mn19_data, "nekkhamma")
print("=== MN 19 Mula Second Half ===")
keys = mn19_data["keys_order"]
start_idx = 0
for idx, k in enumerate(keys):
    if "mn19:24" in k:
        start_idx = idx
        break
for k in keys[start_idx:]:
    p = mn19_data["root_text"].get(k, "")
    e = mn19_data["translation_text"].get(k, "")
    print(f"[{k}] PALI: {p} // EN: {e}")


print("\n=== AN 10.60 Mula Fetch ===")
an10_60_data = fetch_sutta("an10.60")
print(f"Total segments: {len(an10_60_data['keys_order'])}")
for k in an10_60_data['keys_order'][:5]:
    print(f"[{k}] {an10_60_data['root_text'].get(k)} // {an10_60_data['translation_text'].get(k)}")
search_text(an10_60_data, "girimānanda")
