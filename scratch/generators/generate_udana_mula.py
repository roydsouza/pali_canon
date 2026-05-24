#!/usr/bin/env python3
"""
Udāna (KN) mūla layer — all 80 suttas.
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

def fetch_with_retry(sc_id, retries=3, delay=1.0):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            print(f"Error fetching {sc_id} (attempt {attempt+1}/{retries}): {e}. Retrying in {delay}s...")
            time.sleep(delay)

def fetch_comments(sc_id, retries=3, delay=1.0):
    url = API_BASE.format(sc_id) + "?comment=true"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            return data.get("comment", {})
        except Exception:
            if attempt == retries - 1:
                return {}
            time.sleep(delay)

def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))

def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None

def render_sutta(sc_id, data, comments):
    root  = data["root_text"]
    tr    = data["translation_text"]
    keys  = data["keys_order"]

    # Try 0.2 first, then 0.3, then any other 0.x
    sutta_en = tr.get(f"{sc_id}:0.2", tr.get(f"{sc_id}:0.3", "")).strip()
    sutta_pali = root.get(f"{sc_id}:0.2", root.get(f"{sc_id}:0.3", "")).strip()
    
    if not sutta_pali:
        for k in keys:
            if k.startswith(f"{sc_id}:0.") and root.get(k):
                val = root[k].strip()
                if "Udāna" not in val and "Heartfelt" not in val:
                    sutta_pali = val
                    break
    if not sutta_en:
        for k in keys:
            if k.startswith(f"{sc_id}:0.") and tr.get(k):
                val = tr[k].strip()
                if "Udāna" not in val and "Heartfelt" not in val:
                    sutta_en = val
                    break

    parts = sc_id.split(".")
    vagga_num = parts[0][2:]
    sutta_num = parts[1]
    display_num = f"Ud {vagga_num}.{sutta_num}"

    lines = [f"## {display_num}: {sutta_pali} — *{sutta_en}*", ""]

    note_index = {}
    note_counter = [0]

    def maybe_note(key):
        if key in comments:
            note_counter[0] += 1
            idx = note_counter[0]
            note_index[idx] = (key, comments[key])
            return f"[^{sc_id.replace('.','_')}_{idx}]"
        return ""

    for key in keys:
        if is_meta(key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key,   "").strip()
        if not p and not e:
            continue
        level = heading_level(key)
        if level is not None:
            marker = "###" if level == 1 else "####"
            if e and p:
                lines.append(f"{marker} {e}")
                lines.append(f"*{p}*")
                lines.append("")
            else:
                lines.append(f"{marker} {e or p}")
                lines.append("")
        else:
            note = maybe_note(key)
            if p and e:
                lines.append(f"**{p}**{note}  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*{note}")
            else:
                lines.append(f"*{e}*{note}")
            lines.append("")

    if note_index:
        lines.append("")
        for idx, (key, text) in sorted(note_index.items()):
            fn_key = f"{sc_id.replace('.','_')}_{idx}"
            lines.append(f"[^{fn_key}]: **Note ({key})**: {text}")
        lines.append("")

    return "\n".join(lines)

def build_udana_file(sutta_blocks, selected_count):
    nav_link = "[[mula/sutta/khuddaka_nikaya/INDEX|Khuddaka Nikāya]]"
    att_slug = "udana_att"

    header = "\n".join([
        "---",
        "id: UD",
        "title_pali: Udāna",
        "title_en: Inspired Utterances",
        "type: mula",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        "  - udana",
        "  - inspired-utterances",
        "  - poetry",
        "  - early",
        "---",
        "",
        "# Khuddaka Nikāya: Udāna",
        "*Inspired Utterances*",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/INDEX|Mūla]] / "
        f"[[mula/sutta/INDEX|Sutta]] / {nav_link}",
        f"**Related Texts**: [[{att_slug}|Commentary (Atthakathā)]]",
        "**Mātikā**: [[three_marks|Three Marks of Existence]]",
        "",
        f"*Full collection of 80 suttas across 8 vaggas (Uraga, Mucalinda, Nanda, Meghiya, Soṇa, Jaccandha, Cūḷa, Pāṭaligāmiya).*",
        "",
        "---",
        "",
    ])

    return header + "\n\n".join(sutta_blocks)

def main():
    # Generate all 80 suttas
    sc_ids = []
    for v in range(1, 9):
        for s in range(1, 11):
            sc_ids.append(f"ud{v}.{s}")

    print(f"\nUdāna: {len(sc_ids)} suttas")

    sutta_blocks = []
    for sc_id in sc_ids:
        print(f"  {sc_id}...", end=" ", flush=True)
        try:
            data     = fetch_with_retry(sc_id)
            comments = fetch_comments(sc_id)
            block    = render_sutta(sc_id, data, comments)
            sutta_blocks.append(block)
            print(f"{len(data['keys_order'])} segs, {len(comments)} notes")
        except Exception as e:
            print(f"SKIP: {e}")
        time.sleep(0.3)

    content = build_udana_file(sutta_blocks, len(sutta_blocks))
    out_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya")
    os.makedirs(out_dir, exist_ok=True)
    fname   = "udana.md"
    with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
        f.write(content + "\n")

    wc = len(content.split())
    print(f"  → {fname}: {wc:,} words ({len(sutta_blocks)} suttas)")
    print("\nDone.")

if __name__ == "__main__":
    main()
