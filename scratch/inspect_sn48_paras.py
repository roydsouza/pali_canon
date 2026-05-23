import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def inspect_paras_detailed(filename):
    print(f"\n==================== {filename} ====================")
    url = TIPITAKA.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            content = r.read()
        try:
            text = content.decode('utf-16')
        except:
            text = content.decode('utf-8', errors='replace')
        
        matches = list(re.finditer(r'<p rend="subhead">(.*?)</p>', text))
        for idx, m in enumerate(matches):
            subhead_title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            start_pos = m.end()
            end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
            
            sub_text = text[start_pos:end_pos]
            pnums = re.findall(r'<hi rend="paranum">\s*(\d+)\s*</hi>', sub_text)
            if not pnums:
                paras_in_section = []
                for pm in re.finditer(r'<p([^>]*)>(.*?)</p>', sub_text, re.DOTALL):
                    attrs = pm.group(1)
                    body = pm.group(2)
                    pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
                    pnum = pnum_m.group(1) if pnum_m else 'None'
                    clean_body = re.sub(r'<[^>]+>', '', body)[:60].strip()
                    paras_in_section.append((pnum, clean_body))
                print(f"Subhead: {subhead_title} -> Paras (No paranums in subhead tag, but in body): {paras_in_section}")
            else:
                print(f"Subhead: {subhead_title} -> Paras: {pnums}")
            
    except Exception as e:
        print(f"ERROR: {e}")

inspect_paras_detailed("s0305t.tik3.xml")
