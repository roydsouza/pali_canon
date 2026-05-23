import urllib.request
import re
import concurrent.futures

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def probe_file(filename):
    url = TIPITAKA.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
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
            
        return filename, chapter, title, len(content)
    except:
        return filename, None, None, None

files_to_probe = []
for i in range(15):
    for suffix in [f"mul{i}", f"att{i}", f"tik{i}"]:
        files_to_probe.append(f"s0505m.{suffix}.xml" if "mul" in suffix else f"s0505a.{suffix}.xml" if "att" in suffix else f"s0505t.{suffix}.xml")

print("Probing Sutta Nipata (s0505) files concurrently...")
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(probe_file, files_to_probe)

for filename, chapter, title, size in results:
    if size is not None:
        print(f"FOUND {filename}: {chapter} / {title} ({size} bytes)")
