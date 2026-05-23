import urllib.request
import re

TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def analyze_chapter_file(filename):
    print(f"\n===== Analyzing {filename} =====")
    url = TIPITAKA.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            content = r.read()
        try:
            text = content.decode('utf-16')
        except:
            text = content.decode('utf-8', errors='replace')
            
        ps = re.findall(r'<p rend="([^"]+)"[^>]*>(.*?)</p>', text, re.DOTALL)
        print(f"Total paragraphs: {len(ps)}")
        
        for idx, (rend, p_text) in enumerate(ps):
            clean = re.sub(r'<[^>]+>', '', p_text).strip()
            if rend in ['title', 'subhead', 'chapter', 'book']:
                # Print only first 40 chars of heading
                print(f"[{idx}] rend={rend}: {clean[:60]}")
    except Exception as e:
        print(f"Error {filename}: {e}")

analyze_chapter_file("s0504a.att1.xml")
analyze_chapter_file("s0504a.att2.xml")
analyze_chapter_file("s0504a.att3.xml")
analyze_chapter_file("s0504a.att4.xml")
