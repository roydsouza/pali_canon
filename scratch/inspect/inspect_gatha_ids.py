import urllib.request
import json
import re

def probe_sutta(sc_id):
    url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
        return len(data.get("root_text", {}))
    except:
        return 0

print("Probing Theragatha (thag) IDs...")
# Theragatha has 21 nipatas. Let's see some typical IDs like thag1.1, thag2.1, etc.
for nip in range(1, 23):
    found = []
    for sutta in range(1, 60):
        sc_id = f"thag{nip}.{sutta}"
        keys_count = probe_sutta(sc_id)
        if keys_count > 0:
            found.append(sutta)
        else:
            # If sutta 1 doesn't exist, this nipata might not exist or starts differently
            if sutta == 1:
                break
    if found:
        print(f"Nipata {nip}: suttas {found[0]}-{found[-1]} ({len(found)} suttas)")

print("\nProbing Therigatha (thig) IDs...")
# Therigatha has 16 nipatas.
for nip in range(1, 18):
    found = []
    for sutta in range(1, 60):
        sc_id = f"thig{nip}.{sutta}"
        keys_count = probe_sutta(sc_id)
        if keys_count > 0:
            found.append(sutta)
        else:
            if sutta == 1:
                break
    if found:
        print(f"Nipata {nip}: suttas {found[0]}-{found[-1]} ({len(found)} suttas)")
