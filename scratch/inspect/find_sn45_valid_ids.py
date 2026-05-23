import urllib.request
import json

def test():
    valid = []
    ranges = []
    print("Checking individual suttas...")
    for i in range(1, 181):
        sc_id = f"sn45.{i}"
        url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read().decode('utf-8'))
                if "root_text" in data and len(data["root_text"]) > 0:
                    p = data["root_text"].get(f"{sc_id}:0.3", data["root_text"].get(f"{sc_id}:0.2", "N/A"))
                    e = data["translation_text"].get(f"{sc_id}:0.3", data["translation_text"].get(f"{sc_id}:0.2", "N/A"))
                    valid.append((sc_id, p.strip(), e.strip()))
        except Exception:
            pass
            
    print(f"Found {len(valid)} valid individual suttas.")
    for v in valid:
        print(f"  {v[0]}: {v[1]} - {v[2]}")

if __name__ == "__main__":
    test()
