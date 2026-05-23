import urllib.request
import re

url = 'https://tipitaka.org/romn/cscd/s0102t.tik2.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    b = r.read()

try:
    content = b.decode('utf-16')
except Exception:
    content = b.decode('utf-8', errors='replace')

pnums = [int(x) for x in re.findall(r'<hi rend="paranum">\s*(\d+)\s*</hi>', content)]
print("Total paragraph numbers:", len(pnums))
print("Max paragraph numbers:", sorted(list(set(pnums)))[-15:])
