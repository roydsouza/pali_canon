import urllib.request
import json

def test():
    for sc_id in ("sn45.139", "sn45.149"):
        url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode('utf-8'))
                print(f"\nSutta {sc_id}:")
                print("Pali title:", data["root_text"].get(f"{sc_id}:0.3", data["root_text"].get(f"{sc_id}:0.2", "N/A")))
                print("English title:", data["translation_text"].get(f"{sc_id}:0.3", data["translation_text"].get(f"{sc_id}:0.2", "N/A")))
        except Exception as e:
            print(f"Error {sc_id}: {e}")

if __name__ == "__main__":
    test()
