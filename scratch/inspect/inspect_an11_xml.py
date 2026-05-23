#!/usr/bin/env python3
import urllib.request
import re
import html as hmod

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"

def inspect_file(filename):
    url = GITHUB.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            text = raw.decode('utf-16') if b'\xff\xfe' in raw or b'\xfe\xff' in raw else raw.decode('utf-8')
            print(f"=== HEADINGS IN {filename} ===")
            for m in re.finditer(r'<p[^>]*>(.*?)</p>', text, re.DOTALL):
                p_clean = re.sub(r'<[^>]+>', '', m.group(1))
                p_clean = hmod.unescape(p_clean).strip()
                if re.match(r'^\s*(\d+[-–]\d+|\d+)\.\s+', p_clean):
                    print(f"  {p_clean}")
    except Exception as e:
        print(f"Error {filename}: {e}")

inspect_file("s0404a.att15.xml")
inspect_file("s0404t.tik13.xml")
