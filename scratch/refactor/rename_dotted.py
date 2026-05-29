#!/usr/bin/env python3
import os
import sys
import re
import argparse

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path

# Regex to match dotted filenames on disk (for renaming)
FILENAME_RE = re.compile(r'^([a-z]+[0-9]+)\.([0-9]+)(_att|_tik)?\.md$')

# Regex to match both dotted and underscore filenames (for building the link map)
PATTERN_RE = re.compile(r'^([a-z]+[0-9]+)[._]([0-9]+)(_att|_tik)?\.md$')

# Regexes for rewriting links
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]')
MARKDOWN_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
FRONTMATTER_FIELD_RE = re.compile(r'^(commentary_file|sub_commentary_file|mula_file|part_of|covers)\s*:\s*([^\s]+)', re.MULTILINE)

def find_dotted_files(vault_dir):
    dotted_files = []
    for root, dirs, files in os.walk(vault_dir):
        # Exclude git and archive directories
        if ".git" in dirs:
            dirs.remove(".git")
        if "archive" in dirs:
            dirs.remove("archive")
        
        for file in files:
            if FILENAME_RE.match(file):
                dotted_files.append(os.path.join(root, file))
    return sorted(dotted_files)

def build_rename_maps(dotted_files, vault_dir):
    rename_map = {}
    link_map = {}
    
    # 1. Build rename map for any remaining dotted files on disk
    for abs_path in dotted_files:
        dir_name, filename = os.path.split(abs_path)
        m = FILENAME_RE.match(filename)
        if not m:
            continue
        prefix, num, suffix = m.group(1), m.group(2), m.group(3) or ""
        new_filename = f"{prefix}_{num}{suffix}.md"
        new_abs_path = os.path.join(dir_name, new_filename)
        rename_map[abs_path] = new_abs_path

    # 2. Build the link_map by scanning the vault for all files matching the pattern.
    # This ensures that even if files have already been renamed, we can map dotted names to underscore names.
    for root, dirs, files in os.walk(vault_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        if "archive" in dirs:
            dirs.remove("archive")
            
        for file in files:
            m = PATTERN_RE.match(file)
            if m:
                prefix, num, suffix = m.group(1), m.group(2), m.group(3) or ""
                old_base = f"{prefix}.{num}{suffix}"
                new_base = f"{prefix}_{num}{suffix}"
                link_map[old_base] = new_base
        
    return rename_map, link_map

def rename_files_on_disk(rename_map, dry_run=True):
    if not rename_map:
        print("No files to rename on disk (already renamed).")
        return
    print(f"\n--- Renaming Files (Dry-run={dry_run}) ---")
    for old_path, new_path in rename_map.items():
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        print(f"Rename: {old_name} -> {new_name}")
        if not dry_run:
            os.rename(old_path, new_path)
    print(f"Total files: {len(rename_map)}")

def rewrite_file_references(filepath, link_map, dry_run=True):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified_content = content
    
    # 1. Replace Wikilinks: [[target#anchor|display]]
    def replace_wikilink(match):
        target_raw = match.group(1).strip()
        anchor = match.group(2) or ""
        display = match.group(3) or ""
        
        # Handle backslash-escaped pipe inside tables (e.g. [[target\|display]])
        escaped_pipe = False
        target = target_raw
        if target.endswith('\\'):
            target = target[:-1].strip()
            escaped_pipe = True
            
        parts = target.split('/')
        filename = parts[-1]
        
        has_md = filename.endswith('.md')
        base_name = filename[:-3] if has_md else filename
        
        if base_name in link_map:
            new_base = link_map[base_name]
            new_filename = f"{new_base}.md" if has_md else new_base
            parts[-1] = new_filename
            new_target = "/".join(parts)
            if escaped_pipe:
                new_target = new_target + '\\'
            return f"[[{new_target}{anchor}{display}]]"
        return match.group(0)
        
    modified_content = WIKILINK_RE.sub(replace_wikilink, modified_content)
    
    # 2. Replace Markdown Links: [display](path)
    def replace_markdown_link(match):
        display = match.group(1)
        path = match.group(2)
        parts = path.split('/')
        filename = parts[-1]
        
        filename_parts = filename.split('#')
        base_filename = filename_parts[0]
        anchor = "#" + filename_parts[1] if len(filename_parts) > 1 else ""
        
        has_md = base_filename.endswith('.md')
        base_name = base_filename[:-3] if has_md else base_filename
        
        if base_name in link_map:
            new_base = link_map[base_name]
            new_filename = f"{new_base}.md" if has_md else new_base
            parts[-1] = new_filename + anchor
            new_path = "/".join(parts)
            return f"[{display}]({new_path})"
        return match.group(0)
        
    modified_content = MARKDOWN_LINK_RE.sub(replace_markdown_link, modified_content)
    
    # 3. Replace Frontmatter Fields
    def replace_frontmatter_field(match):
        field = match.group(1)
        path = match.group(2)
        parts = path.split('/')
        filename = parts[-1]
        
        has_md = filename.endswith('.md')
        base_name = filename[:-3] if has_md else filename
        
        if base_name in link_map:
            new_base = link_map[base_name]
            new_filename = f"{new_base}.md" if has_md else new_base
            parts[-1] = new_filename
            new_path = "/".join(parts)
            return f"{field}: {new_path}"
        return match.group(0)
        
    modified_content = FRONTMATTER_FIELD_RE.sub(replace_frontmatter_field, modified_content)
    
    if modified_content != content:
        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(modified_content)
        return True
    return False

def rewrite_all_references(vault_dir, link_map, dry_run=True):
    print(f"\n--- Rewriting References (Dry-run={dry_run}) ---")
    modified_count = 0
    
    for root, dirs, files in os.walk(vault_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        if "archive" in dirs:
            dirs.remove("archive")
            
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                # Check if this file was renamed (meaning we should check the new path if not dry run)
                # But during walk, we encounter the old path if dry_run=True, or new path if dry_run=False
                # So we just process whatever .md file we encounter.
                try:
                    is_modified = rewrite_file_references(filepath, link_map, dry_run)
                    if is_modified:
                        rel = os.path.relpath(filepath, vault_dir)
                        print(f"Modified: {rel}")
                        modified_count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    
    print(f"Total files modified: {modified_count}")

def main():
    parser = argparse.ArgumentParser(description="Rename dotted filenames to underscores and update links.")
    parser.add_argument("--execute", action="store_true", help="Actually execute the renaming and rewrites (not a dry-run)")
    args = parser.parse_args()
    
    vault_dir = get_vault_path()
    print(f"Vault Root: {vault_dir}")
    
    dotted_files = find_dotted_files(vault_dir)
    print(f"Found {len(dotted_files)} dotted files on disk.")
    
    rename_map, link_map = build_rename_maps(dotted_files, vault_dir)
    print(f"Built link map with {len(link_map)} mappings.")
    
    dry_run = not args.execute
    if dry_run:
        print("\n*** DRY RUN MODE - NO CHANGES WILL BE MADE TO DISK ***")
        print("Use --execute to apply changes.")
        
    # Step 1: Rename files
    if dotted_files:
        rename_files_on_disk(rename_map, dry_run=dry_run)
    else:
        print("No files to rename on disk (already renamed).")
    
    # Step 2: Rewrite references vault-wide
    rewrite_all_references(vault_dir, link_map, dry_run=dry_run)
    
    print("\nDone.")

if __name__ == "__main__":
    main()
