#!/usr/bin/env python3
"""
Udāna (KN) atthakatha layer from CSCD (Paramatthadīpanī).
Files are s0503a.att0.xml to s0503a.att8.xml.
"""

import os, re, time, html as hmod, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def fetch_bytes_with_retry(filename, retries=3, delay=1.0):
    url = TIPITAKA.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if attempt == retries - 1:
                raise e
            print(f"Error fetching {filename} (attempt {attempt+1}/{retries}): {e}. Retrying in {delay}s...")
            time.sleep(delay)

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def load_cscd_paras(raw):
    try:    content = raw.decode('utf-16')
    except: content = raw.decode('utf-8', errors='replace')
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs   = m.group(1)
        body    = m.group(2)
        rend_m  = re.search(r'rend="([^"]+)"', attrs)
        rend    = rend_m.group(1) if rend_m else ''
        pnum_m  = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body    = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text    = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results

def paras_to_markdown(paras):
    lines = []
    for rend, paranum, text in paras:
        if not text:
            continue
        # Check by rend first to be robust
        if rend == 'chapter' or re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE):
            lines.append(f"\n## {text}\n")
        elif rend == 'subhead' or re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|suttavaṇṇanā|vaGGan|vanGana)', text, re.IGNORECASE):
            lines.append(f"\n### {text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            prefix = f"({paranum}) " if paranum else ""
            lines.append(f"{prefix}{text}\n")
    return "\n".join(lines)

def build_att_file(pali_body, para_count):
    nav_link  = "[[atthakatha/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]]"
    mula_link = "[[udana|Udāna — Inspired Utterances]]"

    header = "\n".join([
        "---",
        "id: UD_att",
        "title_pali: Udānavaṇṇanā",
        "title_en: Commentary on Udāna",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "mula_file: [[udana]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        "# Commentary on Khuddaka Nikāya: Udāna",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/INDEX|Atthakathā]] / "
        f"[[atthakatha/sutta/INDEX|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        "",
        "*Paramatthadīpanī (Udāna-aṭṭhakathā)*",
        f"*{para_count} paragraphs — Pali text CSCD (s0503a.att0.xml to s0503a.att8.xml).*",
        "",
        "## Udānavaṇṇanā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body

def main():
    all_paras = []
    
    print("\nUdāna Atthakathā Generation")
    for i in range(9):
        filename = f"s0503a.att{i}.xml"
        print(f"  Fetching {filename}...", end=" ", flush=True)
        try:
            raw = fetch_bytes_with_retry(filename)
            paras = load_cscd_paras(raw)
            all_paras.extend(paras)
            print(f"OK, parsed {len(paras)} paragraphs")
        except Exception as e:
            print(f"FAILED: {e}")
        time.sleep(0.3)

    pali_body = paras_to_markdown(all_paras)
    content = build_att_file(pali_body, len(all_paras))
    
    out_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya")
    os.makedirs(out_dir, exist_ok=True)
    fname   = "udana_att.md"
    with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
        f.write(content + "\n")

    wc = len(content.split())
    print(f"  → {fname}: {wc:,} words ({len(all_paras)} paragraphs total)")
    print("\nDone.")

if __name__ == "__main__":
    main()
