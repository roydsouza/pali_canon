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
        return False

print("Probing Itivuttaka (s0504) files...")
for i in range(12):
    probe_file(f"s0504m.mul{i}.xml")
    probe_file(f"s0504a.att{i}.xml")
    probe_file(f"s0504t.tik{i}.xml")
