import urllib.request
import re
import json

def test_cscd():
    url_att = "https://tipitaka.org/romn/cscd/s0305a.att0.xml"
    url_tik = "https://tipitaka.org/romn/cscd/s0305t.tik0.xml"
    
    print("Testing Atthakatha XML...")
    req = urllib.request.Request(url_att, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            print(f"Success! Atthakatha size: {len(data)} bytes")
            # Decode to utf-16
            try:
                text = data.decode('utf-16')
            except:
                text = data.decode('utf-8', errors='replace')
            paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
            print(f"Total paragraphs: {len(paras)}")
            print("First 3 paragraphs:")
            for p in paras[:3]:
                print("-", re.sub(r'<[^>]+>', '', p)[:150])
    except Exception as e:
        print(f"Error fetching Atthakatha: {e}")

    print("\nTesting Tika XML...")
    req = urllib.request.Request(url_tik, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            print(f"Success! Tika size: {len(data)} bytes")
            try:
                text = data.decode('utf-8')
            except:
                try:
                    text = data.decode('utf-16')
                except:
                    text = data.decode('utf-8', errors='replace')
            paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
            print(f"Total paragraphs: {len(paras)}")
            print("First 3 paragraphs:")
            for p in paras[:3]:
                print("-", re.sub(r'<[^>]+>', '', p)[:150])
    except Exception as e:
        print(f"Error fetching Tika: {e}")

def test_suttacentral():
    url = "https://suttacentral.net/api/bilarasuttas/sn45.1/sujato"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
            print("\nSuttaCentral SN 45.1 test:")
            print("Pali title:", data["root_text"].get("sn45.1:0.3", data["root_text"].get("sn45.1:0.2", "N/A")))
            print("English title:", data["translation_text"].get("sn45.1:0.3", data["translation_text"].get("sn45.1:0.2", "N/A")))
    except Exception as e:
        print(f"Error fetching from SuttaCentral: {e}")

if __name__ == "__main__":
    test_cscd()
    test_suttacentral()
