#!/usr/bin/env python3
import os
import re
import sys

VAULT_DIR = "/Users/rds/pali_canon"
EXCLUDE_INDEX_DIRS = {".git", ".obsidian", "scratch", "templates"}
EXCLUDE_SCAN_DIRS = {".git", ".obsidian", "scratch", "templates"}

def get_markdown_files(vault_dir, exclude_dirs):
    md_files = []
    for root, dirs, files in os.walk(vault_dir):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def parse_headers_and_anchors(filepath):
    """Returns a set of normalized headers/anchors from the markdown file."""
    headers = set()
    # Read file content
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match ATX headings: e.g. "### §406" or "## The List" or "### 4.2. The Aggregates"
    heading_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
    for match in heading_pattern.finditer(content):
        heading = match.group(1).strip()
        headers.add(heading)
        # Normalize for anchor comparisons (standard Obsidian replaces spaces with hyphens, etc.
        # but let's also keep exact match as it's common in this vault)
        normalized = re.sub(r'[^\w\s§\-.]', '', heading).strip()
        headers.add(normalized)
    
    # Check for custom HTML anchors if any (like <a name="anchor"></a> or similar)
    anchor_pattern = re.compile(r'<a\s+name="([^"]+)"')
    for match in anchor_pattern.finditer(content):
        headers.add(match.group(1).strip())
        
    return headers

def validate_vault():
    all_files = get_markdown_files(VAULT_DIR, EXCLUDE_INDEX_DIRS)
    scan_files = get_markdown_files(VAULT_DIR, EXCLUDE_SCAN_DIRS)
    
    # Map from relative path from vault root (no ext), and filename (no ext) to absolute path
    # e.g., "mula/sutta/digha_nikaya/dn9" -> "/Users/rds/pali_canon/mula/sutta/digha_nikaya/dn9.md"
    # and "dn9" -> "/Users/rds/pali_canon/mula/sutta/digha_nikaya/dn9.md"
    path_map = {}
    file_map = {}
    
    for filepath in all_files:
        rel_path = os.path.relpath(filepath, VAULT_DIR)
        rel_no_ext = os.path.splitext(rel_path)[0]
        filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
        
        path_map[rel_no_ext] = filepath
        if filename_no_ext in file_map:
            # Ambiguity: keep list of files, but usually filenames are unique in this vault
            if isinstance(file_map[filename_no_ext], list):
                file_map[filename_no_ext].append(filepath)
            else:
                file_map[filename_no_ext] = [file_map[filename_no_ext], filepath]
        else:
            file_map[filename_no_ext] = filepath

    # Pre-parse headers for all files to check anchor resolution
    file_headers = {}
    for filepath in all_files:
        file_headers[filepath] = parse_headers_and_anchors(filepath)

    # Wikilink pattern: [[target]] or [[target|label]]
    # target may contain an anchor: e.g. target#anchor
    wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
    
    errors = []
    total_links_checked = 0
    
    for filepath in scan_files:
        rel_src = os.path.relpath(filepath, VAULT_DIR)
        with open(filepath, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                for match in wikilink_pattern.finditer(line):
                    total_links_checked += 1
                    raw_link = match.group(1).strip()
                    
                    # Split label if present (e.g. [[target|label]])
                    if '|' in raw_link:
                        target_part, label = raw_link.split('|', 1)
                        target_part = target_part.strip()
                    else:
                        target_part = raw_link
                    
                    # Split anchor if present (e.g. [[target#anchor]])
                    if '#' in target_part:
                        target_path, anchor = target_part.split('#', 1)
                        target_path = target_path.strip()
                        anchor = anchor.strip()
                    else:
                        target_path = target_part
                        anchor = None
                    
                    # Handle self-references (e.g., [[#anchor]])
                    if not target_path:
                        target_file = filepath
                    else:
                        # Clean backslash escapes in target (e.g. [[dn2\|DN 2]] is common due to markdown table cell escaping)
                        target_path = target_path.replace('\\', '')
                        
                        # Resolve target_path
                        target_file = None
                        
                        # 1. Direct path check from vault root
                        if target_path in path_map:
                            target_file = path_map[target_path]
                        # 2. Short filename check
                        elif target_path in file_map:
                            resolved = file_map[target_path]
                            if isinstance(resolved, list):
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Ambiguous link '{target_path}' matches multiple files: {[os.path.relpath(x, VAULT_DIR) for x in resolved]}"
                                })
                                continue
                            else:
                                target_file = resolved
                        # 3. Relative path check from current file directory
                        else:
                            curr_dir = os.path.dirname(filepath)
                            rel_candidate = os.path.normpath(os.path.join(curr_dir, target_path + ".md"))
                            if os.path.exists(rel_candidate):
                                target_file = rel_candidate
                                
                    if not target_file:
                        errors.append({
                            "file": rel_src,
                            "line": line_num,
                            "link": raw_link,
                            "error": f"Target file '{target_path}' not found"
                        })
                    elif anchor:
                        # Validate anchor exists in target_file
                        headers = file_headers[target_file]
                        # Exact check
                        if anchor not in headers:
                            # Try to normalize anchor as well
                            norm_anchor = re.sub(r'[^\w\s§\-.]', '', anchor).strip()
                            # Check normalized or check if any header contains the anchor
                            matched_anchor = False
                            for h in headers:
                                # Standard slugify: lowercase, replace spaces with hyphen
                                slug_h = h.lower().replace(' ', '-')
                                slug_anchor = anchor.lower().replace(' ', '-')
                                if h == anchor or norm_anchor == h or slug_h == slug_anchor or anchor in h:
                                    matched_anchor = True
                                    break
                            if not matched_anchor:
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Anchor '#{anchor}' not found in target '{os.path.relpath(target_file, VAULT_DIR)}'"
                                })

    print(f"Validated {len(scan_files)} markdown files.")
    print(f"Checked {total_links_checked} wikilinks.")
    
    if errors:
        print(f"\nFound {len(errors)} broken links/references:")
        for err in errors:
            print(f"  [{err['file']}:{err['line']}] {err['link']} -> {err['error']}")
        return False
    else:
        print("\nAll links and references are valid!")
        return True

if __name__ == "__main__":
    success = validate_vault()
    if not success:
        sys.exit(1)
