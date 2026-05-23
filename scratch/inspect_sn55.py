import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def inspect_cscd(filename):
    print(f"\nInspecting {filename}...")
    url = TIPITAKA.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            content = r.read()
        try:
            text = content.decode('utf-16')
        except:
            text = content.decode('utf-8', errors='replace')
        
        # Print first 2000 characters
        print("FIRST 2000 CHARACTERS:")
        print(text[:2000])
        
        # Search for headings
        print("\nHEADINGS FOUND:")
        for m in re.finditer(r'<p rend="(?:chapter|section|subhead)">(.*?)</p>', text):
            body = re.sub(r'<[^>]+>', '', m.group(1))
            print(f"  [{m.group(0)}] -> {body}")
            
    except Exception as e:
        print(f"ERROR: {e}")

inspect_cscd("s0305a.att10.xml")
inspect_cscd("s0305t.tik10.xml")
