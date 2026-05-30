#!/usr/bin/env python3
import urllib.request
import re

URL_PATTERN = "https://tipitaka.org/romn/cscd/s0403a.att{}.xml"

def search():
    for i in range(1, 55):
        url = URL_PATTERN.format(i)
        print(f"Checking {url}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read()
                # Try decoding as utf-16
                try:
                    text = content.decode('utf-16')
                except:
                    text = content.decode('utf-8', errors='ignore')
                
                # Search for keywords
                if "Hirottappe" in text or "hirīottappa" in text or "hirottappa" in text or "Hiriottappa" in text:
                    print(f"*** FOUND matching keyword in file: s0403a.att{i}.xml ***")
                    # print first 1000 characters around match
                    idx = text.find("Hirottappe")
                    if idx == -1: idx = text.lower().find("hirottappa")
                    print(text[max(0, idx-200):min(len(text), idx+500)])
                    print("="*40)
        except Exception as e:
            # print(f"Error {i}: {e}")
            pass

if __name__ == "__main__":
    search()
