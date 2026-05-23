import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def probe_file(filename):
    url = TIPITAKA.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            content = r.read()
        try:
            text = content.decode('utf-16')
        except:
            text = content.decode('utf-8', errors='replace')
        
        # Extract title or chapter headings
        chapter = "None"
        m = re.search(r'<p rend="chapter">(.*?)</p>', text)
        if m:
            chapter = re.sub(r'<[^>]+>', '', m.group(1))
        
        title = "None"
        m = re.search(r'<p rend="title">(.*?)</p>', text)
        if m:
            title = re.sub(r'<[^>]+>', '', m.group(1))
            
        print(f"FOUND {filename}: {chapter} / {title} ({len(content)} bytes)")
        return True
    except Exception as e:
        # print(f"NOT FOUND {filename}: {e}")
        return False

print("Probing Udana (s0503) files...")
for suffix in ["", "0", "1", "2"]:
    probe_file(f"s0503m.mul{suffix}.xml")
    probe_file(f"s0503a.att{suffix}.xml")
    probe_file(f"s0503t.tik{suffix}.xml")

print("\nProbing Sutta Nipata (s0505) files...")
for suffix in ["", "0", "1", "2"]:
    probe_file(f"s0505m.mul{suffix}.xml")
    probe_file(f"s0505a.att{suffix}.xml")
    probe_file(f"s0505t.tik{suffix}.xml")
