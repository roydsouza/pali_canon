import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"
GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"

def check_file(filename, source="github"):
    url = (GITHUB if source == "github" else TIPITAKA).format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read()
            try:
                text = content.decode('utf-16')
            except:
                text = content.decode('utf-8', errors='replace')
            
            # Find the first few headings or paras
            headings = []
            for m in re.finditer(r'<p rend="subhead.*?">(.*?)</p>', text, re.DOTALL):
                clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                headings.append(clean)
            for m in re.finditer(r'<p rend="title">(.*?)</p>', text, re.DOTALL):
                clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                headings.append("TITLE: " + clean)
            for m in re.finditer(r'<p rend="book">(.*?)</p>', text, re.DOTALL):
                clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                headings.append("BOOK: " + clean)
            print(f"File: {filename} ({len(content)} bytes)")
            print(f"Headings/Titles found: {headings[:10]}\n")
    except Exception as e:
        print(f"File: {filename} failed: {e}\n")

# Let's check potential files for DN1, DN16, DN21
# DN1 is Brahmajālasutta (Sīlakkhandhavagga)
# DN16 is Mahāparinibbānasutta (Mahāvagga)
# DN21 is Sakkapañhasutta (Mahāvagga)

print("Checking Sīlakkhandhavagga Atthakatha:")
for i in range(14):
    check_file(f"s0101a.att{i}.xml")

print("Checking Mahāvagga Atthakatha:")
for i in range(12):
    check_file(f"s0102a.att{i}.xml")
