import urllib.request
import json

def test():
    for i in range(139, 149):
        sc_id = f"sn45.{i}"
        url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode('utf-8'))
                p = data["root_text"].get(f"{sc_id}:0.3", data["root_text"].get(f"{sc_id}:0.2", "N/A"))
                e = data["translation_text"].get(f"{sc_id}:0.3", data["translation_text"].get(f"{sc_id}:0.2", "N/A"))
                print(f"{sc_id}: {p.strip()} - {e.strip()}")
        except Exception as e:
            print(f"Error {sc_id}: {e}")

if __name__ == "__main__":
    test()
