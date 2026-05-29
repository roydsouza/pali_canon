#!/usr/bin/env python3
import os
import sys
import re
import argparse

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path, parse_frontmatter

def normalize_pali(text):
    """Normalize Pali words by removing markdown, accents, punctuation, and lowercasing."""
    if not text:
        return ""
    # Replace * with space to avoid word concatenation in split bold tags
    text = text.replace('*', ' ')
    # Safely escape regex brackets
    text = re.sub(r'[\[\]#|—\-–]', ' ', text)
    text = text.lower()
    
    # Strip all Pali diacritics/accents
    replacements = {
        'ā': 'a', 'ī': 'i', 'ū': 'u',
        'ṅ': 'n', 'ñ': 'n', 'ṇ': 'n',
        'ṭ': 't', 'ḍ': 'd', 'ḷ': 'l', 
        'ṁ': 'm', 'ṃ': 'm'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
        
    text = re.sub(r'[^a-z\s]', '', text)
    return ' '.join(text.split())

def extract_anchors_from_att(att_content):
    """Parses Atthakatha content to find paragraph numbers and their corresponding Pali commentary anchors."""
    # Matches (NNN) **Pali**ti or (NNN) **Pali**nti
    # We match the first portion of the paragraph after (NNN) up to the commentary markers
    pattern = re.compile(r'\((\d+)\)\s+(.*?)(?:nti|ti)\b', re.DOTALL)
    anchors = {}
    
    for m in pattern.finditer(att_content):
        para_num = int(m.group(1))
        anchor_text = m.group(2).strip()
        # Clean up tags and extra text
        anchor_cleaned = re.sub(r'<[^>]+>', '', anchor_text)
        # Get first few words
        words = anchor_cleaned.split()
        if len(words) > 10:
            anchor_cleaned = " ".join(words[:6])
        anchors[para_num] = anchor_cleaned
        
    return anchors

def get_basenames(mula_path, att_path, tik_path):
    mula_base = os.path.basename(mula_path).replace(".md", "")
    att_base = os.path.basename(att_path).replace(".md", "") if att_path else ""
    tik_base = os.path.basename(tik_path).replace(".md", "") if tik_path else ""
    return mula_base, att_base, tik_base

def crosslink_att_tik(att_path, tik_path, para_numbers, att_base, tik_base, tik_paras=None):
    """Ensures ### §NNN headings exist in Att and Tik, and Att links to Tik."""
    if not att_path or not os.path.exists(att_path):
        return
        
    with open(att_path, "r", encoding="utf-8") as f:
        att_content = f.read()
        
    att_lines = att_content.splitlines(keepends=True)
    att_modified = False
    
    # Process each paragraph
    for para_num in sorted(para_numbers):
        para_marker = f"({para_num})"
        heading_marker = f"### §{para_num}"
        has_tik_para = tik_paras is not None and para_num in tik_paras
        
        # Check if the Tīkā link callout is already there
        has_link = tik_base and f"[[{tik_base}#§{para_num}" in att_content
        
        # We search for the paragraph line
        for idx, line in enumerate(att_lines):
            if line.lstrip().startswith(para_marker):
                # 1. Insert heading if not present
                if heading_marker not in att_content:
                    heading = f"\n### §{para_num}\n\n"
                    att_lines.insert(idx, heading)
                    att_modified = True
                    # Re-serialize to update indices
                    att_content = "".join(att_lines)
                    att_lines = att_content.splitlines(keepends=True)
                    # Find the paragraph line index again since we modified the list
                    for new_idx, new_line in enumerate(att_lines):
                        if new_line.lstrip().startswith(para_marker):
                            idx = new_idx
                            break
                
                # 2. Insert Tīkā callout if needed and not present
                if tik_base and has_tik_para and not has_link:
                    tik_link = (
                        f"\n> [!abstract]- Tīkā §{para_num}\n"
                        f"> [[{tik_base}#§{para_num}|Sub-commentary §{para_num}]]\n"
                    )
                    # Insert right after the paragraph line
                    att_lines.insert(idx + 1, tik_link)
                    att_modified = True
                    att_content = "".join(att_lines)
                    att_lines = att_content.splitlines(keepends=True)
                break
                
    if att_modified:
        with open(att_path, "w", encoding="utf-8") as f:
            f.write(att_content)
        print(f"Updated {att_base} with paragraph links/headings.")
        
    if tik_path and os.path.exists(tik_path):
        with open(tik_path, "r", encoding="utf-8") as f:
            tik_content = f.read()
            
        tik_lines = tik_content.splitlines(keepends=True)
        tik_modified = False
        
        for para_num in sorted(para_numbers):
            para_marker = f"({para_num})"
            heading_marker = f"### §{para_num}"
            
            if heading_marker not in tik_content:
                for idx, line in enumerate(tik_lines):
                    if line.lstrip().startswith(para_marker):
                        heading = f"\n### §{para_num}\n\n"
                        tik_lines.insert(idx, heading)
                        tik_modified = True
                        tik_content = "".join(tik_lines)
                        tik_lines = tik_content.splitlines(keepends=True)
                        break
                        
        if tik_modified:
            with open(tik_path, "w", encoding="utf-8") as f:
                f.write(tik_content)
            print(f"Updated {tik_base} with paragraph headings.")

def crosslink_mula(mula_path, att_anchors, att_base, tik_base, tik_paras=None):
    """Search for anchors in Mula and insert collapsed commentary callout boxes."""
    if not os.path.exists(mula_path):
        print(f"Mula file not found: {mula_path}")
        return
        
    with open(mula_path, "r", encoding="utf-8") as f:
        mula_content = f.read()
        
    mula_lines = mula_content.splitlines(keepends=True)
    mula_modified = False
    
    # We sort anchors by paragraph number
    for para_num, anchor_text in sorted(att_anchors.items()):
        # Idempotency check
        if f"[[{att_base}#§{para_num}" in mula_content:
            continue
            
        norm_anchor = normalize_pali(anchor_text)
        if not norm_anchor:
            continue
            
        # Search for matching line in Mula
        matched_idx = -1
        for idx, line in enumerate(mula_lines):
            # Skip code blocks, headers, frontmatter
            if line.startswith("#") or line.startswith("---") or line.startswith(">"):
                continue
            norm_line = normalize_pali(line)
            if norm_anchor in norm_line:
                matched_idx = idx
                break
                
        if matched_idx != -1:
            # Build the commentary callout box
            callout = (
                f"\n> [!info]- Commentary §{para_num}\n"
                f"> **Atthakathā**: [[{att_base}#§{para_num}|Commentary §{para_num}]]"
            )
            # Only include Tīkā link if the paragraph exists in Tīkā
            has_tik_para = tik_paras is not None and para_num in tik_paras
            if tik_base and has_tik_para:
                callout += f"  ·  **Tīkā**: [[{tik_base}#§{para_num}|Sub-commentary §{para_num}]]"
            callout += "\n\n"
            
            # Insert the callout before the matched line
            mula_lines.insert(matched_idx, callout)
            mula_modified = True
            # Re-join and re-split to update indices correctly for subsequent inserts
            mula_content = "".join(mula_lines)
            mula_lines = mula_content.splitlines(keepends=True)
        else:
            print(f"  Warning: could not resolve Mūla anchor '{anchor_text}' for §{para_num}")
            
    if mula_modified:
        with open(mula_path, "w", encoding="utf-8") as f:
            f.write(mula_content)
        print(f"Updated Mūla file {os.path.basename(mula_path)} with paragraph callouts.")
    else:
        print(f"No new callouts needed for Mūla file {os.path.basename(mula_path)}.")

def main():
    parser = argparse.ArgumentParser(description="Generic paragraph-level crosslinker for Pali Canon suttas.")
    parser.add_argument("--mula", required=True, help="Path to Mula markdown file")
    parser.add_argument("--att", required=True, help="Path to Atthakatha markdown file")
    parser.add_argument("--tik", help="Path to Tika markdown file")
    
    args = parser.parse_args()
    
    vault = get_vault_path()
    mula_path = os.path.join(vault, args.mula) if not os.path.isabs(args.mula) else args.mula
    att_path = os.path.join(vault, args.att) if not os.path.isabs(args.att) else args.att
    tik_path = None
    if args.tik:
        tik_path = os.path.join(vault, args.tik) if not os.path.isabs(args.tik) else args.tik
        
    print(f"Starting generic cross-linking for:")
    print(f"  Mūla: {mula_path}")
    print(f"  Atthakathā: {att_path}")
    if tik_path:
        print(f"  Tīkā: {tik_path}")
        
    if not os.path.exists(att_path):
        print(f"Error: Atthakatha file not found at {att_path}")
        sys.exit(1)
        
    with open(att_path, "r", encoding="utf-8") as f:
        att_content = f.read()
        
    att_anchors = extract_anchors_from_att(att_content)
    if not att_anchors:
        print("No paragraph anchors of the form (NNN) found in Atthakatha file.")
        sys.exit(0)
        
    print(f"Found {len(att_anchors)} paragraph anchors in Atthakathā.")
    
    # Parse available paragraph numbers from Tīkā
    tik_paras = set()
    if tik_path and os.path.exists(tik_path):
        with open(tik_path, "r", encoding="utf-8") as f:
            tik_content = f.read()
        for m in re.finditer(r'^\s*\((\d+)\)', tik_content, re.MULTILINE):
            tik_paras.add(int(m.group(1)))
        print(f"Found {len(tik_paras)} paragraph anchors in Tīkā.")
        
    mula_base, att_base, tik_base = get_basenames(mula_path, att_path, tik_path)
    
    # Establish Att + Tik cross-links and headings
    crosslink_att_tik(att_path, tik_path, att_anchors.keys(), att_base, tik_base, tik_paras)
    
    # Establish Mula cross-links
    crosslink_mula(mula_path, att_anchors, att_base, tik_base, tik_paras)
    
    print("Cross-linking process completed successfully.")

if __name__ == "__main__":
    main()
