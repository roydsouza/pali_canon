import urllib.request
import re

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def inspect_girimananda(filename):
    for base in [GITHUB, TIPITAKA]:
        url = base.format(filename)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read()
            try:
                text = content.decode('utf-16')
            except:
                text = content.decode('utf-8', errors='replace')
            
            idx = text.find('10. Girimānandasuttavaṇṇanā')
            if idx != -1:
                print("Printing commentary text for Girimānanda:")
                snippet = text[idx:]
                # Print clean text
                snippet_clean = re.sub(r'<[^>]+>', ' ', snippet)
                snippet_clean = re.sub(r'\s+', ' ', snippet_clean)
                print(snippet_clean[:2000])
            return
        except Exception as e:
            pass

inspect_girimananda("s0404a.att20.xml")
