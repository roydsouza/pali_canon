#!/usr/bin/env python3
import os
import re

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")

def parse_numbers(s):
    # Extracts numbers from strings like "2-5", "235-247", "80", "§80"
    s = re.sub(r'[^0-9\-–]', '', s)
    if not s:
        return []
    m = re.match(r'^(\d+)[-–](\d+)$', s)
    if m:
        return list(range(int(m.group(1)), int(m.group(2)) + 1))
    m = re.match(r'^(\d+)$', s)
    if m:
        return [int(m.group(1))]
    return []

def get_file_headings(path):
    if not os.path.exists(path):
        return []
    headings = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                # Extract heading text
                h_text = line.lstrip("#").strip()
                headings.append(h_text)
    return headings

def clean_anchor(anchor):
    # Obsidian normalizes anchors for links, but let's keep it simple
    return anchor.strip()

def find_best_heading_match(target_headings, source_anchor):
    # If it's a paragraph anchor
    source_nums = parse_numbers(source_anchor)
    if source_nums:
        # Try to find a target paragraph heading that intersects
        for h in target_headings:
            if h.startswith("§"):
                target_nums = parse_numbers(h)
                if any(n in target_nums for n in source_nums):
                    return h
                    
    # Try case-insensitive substring match
    clean_src = source_anchor.lower().replace("ṭīkā", "").replace("vaṇṇanā", "").replace("sutta", "").strip()
    for h in target_headings:
        clean_h = h.lower().replace("ṭīkā", "").replace("vaṇṇanā", "").replace("sutta", "").strip()
        if clean_src in clean_h or clean_h in clean_src:
            return h
            
    # Default to first H2 heading if available
    h2_headings = [h for h in target_headings if not h.startswith("§")]
    if h2_headings:
        return h2_headings[0]
        
    return None

def process_file(path, all_headings):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified = False
    
    # 1. Fix paragraph callout blocks
    # e.g., > [!abstract]- Tīkā §3-5\n> [[an11_2_5_tik#§3-5|Sub-commentary §3-5]]
    # We want to match these callout blocks and rewrite their links if the anchor doesn't exist
    def fix_callout(match):
        nonlocal modified
        callout_type = match.group(1) # e.g. [!abstract]- Tīkā §3-5
        target_file = match.group(2)
        anchor = match.group(3)
        label = match.group(4)
        
        target_path = find_target_path(target_file)
        if not target_path:
            return match.group(0) # target file not found, keep as is
            
        target_heads = all_headings.get(target_path, [])
        
        # Check if anchor exists exactly
        if anchor in target_heads:
            return match.group(0)
            
        # Try to find best match
        best_h = find_best_heading_match(target_heads, anchor)
        modified = True
        if best_h:
            return f"> {callout_type}\n> [[{target_file}#{best_h}|{label}]]"
        else:
            # Anchor doesn't exist and no match, link to file root rather than deleting
            print(f"Warning: Could not resolve anchor '{anchor}' in '{target_file}' for file '{os.path.basename(path)}'. Linking to file root.")
            return f"> {callout_type}\n> [[{target_file}|{label}]]"
            
    # Pattern for callouts:
    # > [!abstract]- Tīkā §3-5
    # > [[an11_2_5_tik#§3-5|Sub-commentary §3-5]]
    callout_re = r'>\s*(\[!abstract\]-.*?)\n>\s*\[\[([^#|\]]+)#([^|\]]+)\|([^\]]+)\]\]'
    content = re.sub(callout_re, fix_callout, content)
    
    # 2. Fix inline wikilinks
    # e.g. [[an11_1_tik#Kimatthiyasuttavaṇṇanāṭīkā|Kimatthiyasuttavaṇṇanāṭīkā]]
    def fix_wikilink(match):
        nonlocal modified
        target_file = match.group(1)
        anchor = match.group(2)
        label = match.group(3)
        
        target_path = find_target_path(target_file)
        if not target_path:
            return match.group(0)
            
        target_heads = all_headings.get(target_path, [])
        if anchor in target_heads:
            return match.group(0)
            
        best_h = find_best_heading_match(target_heads, anchor)
        modified = True
        if best_h:
            return f"[[{target_file}#{best_h}|{label}]]"
        else:
            return f"[[{target_file}|{label}]]"
            
    wikilink_re = r'\[\[([^#|\]]+)#([^|\]]+)\|([^\]]+)\]\]'
    content = re.sub(wikilink_re, fix_wikilink, content)
    
    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Repaired links in: {os.path.basename(path)}")

# Helper to find target file path in the vault
file_path_cache = {}
def find_target_path(filename):
    if filename in file_path_cache:
        return file_path_cache[filename]
        
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in {'.git', '.obsidian', 'archive'}]
        for f in files:
            if f == f"{filename}.md":
                path = os.path.join(root, f)
                file_path_cache[filename] = path
                return path
    return None

def main():
    print("Collecting all headings in the vault...")
    all_headings = {}
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in {'.git', '.obsidian', 'archive'}]
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                all_headings[path] = get_file_headings(path)
                
    print(f"Collected headings for {len(all_headings)} files.")
    
    print("Repairing broken anchors...")
    for path in all_headings.keys():
        process_file(path, all_headings)
        
    print("Link repair complete.")

if __name__ == "__main__":
    main()
