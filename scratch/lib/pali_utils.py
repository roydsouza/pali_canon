#!/usr/bin/env python3
import os
import re
import html
import urllib.request

def get_vault_path():
    """Safely retrieves the vault path from the PALI_VAULT env var, defaulting to /Users/rds/pali_canon."""
    return os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")

def clean_xml(text):
    """Cleans CSCD XML formatting tags, converting hi rend=bold to markdown bold and removing page breaks and other tags."""
    if not text:
        return ""
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def fetch_bytes(filename, base_url="https://tipitaka.org/romn/cscd/{}"):
    """Fetches raw bytes, checking the local scratch/xml_cache folder first before downloading."""
    vault = get_vault_path()
    cache_dir = os.path.join(vault, "scratch", "xml_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, filename)
    
    if os.path.exists(cache_path):
        return open(cache_path, "rb").read()
        
    url = base_url.format(filename) if "{}" in base_url else f"{base_url.rstrip('/')}/{filename}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        
    # Cache the file
    with open(cache_path, "wb") as f:
        f.write(data)
        
    return data

def load_cscd_paras(filename, base_url="https://tipitaka.org/romn/cscd/{}"):
    """Downloads a CSCD XML file, decodes it robustly, and parses it into (rend, paranum, clean_text) paragraphs."""
    raw = fetch_bytes(filename, base_url)
    
    # Robust decoding: try utf-8 first, then utf-16 variants, fallback to replace
    content = None
    for enc in ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']:
        try:
            decoded = raw.decode(enc)
            if '<p' in decoded or '<?xml' in decoded:
                content = decoded
                break
        except Exception:
            pass
            
    if content is None:
        content = raw.decode('utf-8', errors='replace')
            
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*([\d\-]+)\s*</hi>', body)
        paranum = pnum_m.group(1).strip() if pnum_m else ''
        body = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results

def parse_frontmatter(filepath_or_content):
    """Parses frontmatter dictionary from a markdown file path or file content."""
    meta = {}
    content = ""
    if isinstance(filepath_or_content, str) and os.path.exists(filepath_or_content):
        with open(filepath_or_content, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = str(filepath_or_content)
        
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta
