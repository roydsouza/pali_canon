import urllib.request
import re
import time

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
    except:
        return False

print("Probing s0503 (Udana)...")
for i in range(12):
    probe_file(f"s0503m.mul{i}.xml")
    probe_file(f"s0503a.att{i}.xml")
    probe_file(f"s0503t.tik{i}.xml")

print("\nProbing s0505 (Sutta Nipata)...")
for i in range(12):
    probe_file(f"s0505m.mul{i}.xml")
    probe_file(f"s0505a.att{i}.xml")
    probe_file(f"s0505t.tik{i}.xml")
