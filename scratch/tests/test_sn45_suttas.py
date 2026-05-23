import urllib.request
import json

def test():
    for sc_id in ("sn45.2", "sn45.3"):
        url = f"https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode('utf-8'))
                print(f"\nSutta {sc_id}:")
                # print first few lines of translation
                keys = data["keys_order"]
                count = 0
                for k in keys:
                    if not k.endswith(':0.1') and not k.endswith(':0.2') and not k.endswith(':0.3') and not k.endswith(':0.4'):
                        p = data["root_text"].get(k, "")
                        e = data["translation_text"].get(k, "")
                        if p or e:
                            print(f"  Pali: {p}")
                            print(f"  English: {e}")
                            count += 1
                            if count >= 3:
                                break
        except Exception as e:
            print(f"Error {sc_id}: {e}")

if __name__ == "__main__":
    test()
