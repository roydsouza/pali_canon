#!/usr/bin/env python3
import urllib.request

GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"

print("Checking s0401a files...")
for i in range(25):
    f_att = f"s0401a.att{i}.xml"
    f_tik = f"s0401t.tik{i}.xml"
    
    # Try fetching att
    req_att = urllib.request.Request(GITHUB.format(f_att), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req_att, timeout=3) as r:
            print(f"  Found Atthakatha: {f_att}")
    except:
        pass
        
    # Try fetching tik
    req_tik = urllib.request.Request(GITHUB.format(f_tik), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req_tik, timeout=3) as r:
            print(f"  Found Tika: {f_tik}")
    except:
        pass

# Also try without index, e.g. s0401a.att.xml
for suffix in ["a.att.xml", "t.tik.xml"]:
    f = f"s0401{suffix}"
    req = urllib.request.Request(GITHUB.format(f), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            print(f"  Found: {f}")
    except:
        pass
