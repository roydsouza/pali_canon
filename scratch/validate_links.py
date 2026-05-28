#!/usr/bin/env python3
import os
import re
import sys

VAULT_DIR = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
EXCLUDE_INDEX_DIRS = {".git", ".obsidian", "scratch", "templates", "archive"}
EXCLUDE_SCAN_DIRS = {".git", ".obsidian", "scratch", "templates", "archive"}

def get_markdown_files(vault_dir, exclude_dirs):
    md_files = []
    for root, dirs, files in os.walk(vault_dir):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".md") and not file.startswith("FROM-CLAUDE"):
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

def parse_yaml(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None
    
    yaml_text = match.group(1)
    yaml_dict = {}
    current_key = None
    for line in yaml_text.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        if line.strip().startswith('- '):
            val = line.strip()[2:].strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if current_key and isinstance(yaml_dict.get(current_key), list):
                yaml_dict[current_key].append(val)
            continue
            
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if val == "":
                yaml_dict[key] = []
                current_key = key
            else:
                yaml_dict[key] = val
                current_key = key
    return yaml_dict

def validate_frontmatter(filepath, content, rel_src):
    errors = []
    filename = os.path.basename(filepath)
    if filename == "INDEX.md":
        return errors
        
    parts = rel_src.split(os.sep)
    if not parts or len(parts) < 2:
        return errors
        
    type_dir = parts[0]
    if type_dir not in {"mula", "atthakatha", "tika", "matika", "practice", "paths"}:
        return errors
        
    yaml_dict = parse_yaml(content)
    if yaml_dict is None:
        errors.append({
            "file": rel_src,
            "line": 1,
            "link": "Frontmatter",
            "error": "Missing or invalid YAML frontmatter block at start of file"
        })
        return errors
        
    expected_types = {
        "mula": "mula",
        "atthakatha": "atthakatha",
        "tika": "tika",
        "matika": "matika",
        "practice": "practice",
        "paths": "path"
    }
    
    if "id" not in yaml_dict or not yaml_dict["id"]:
        errors.append({
            "file": rel_src,
            "line": 1,
            "link": "id",
            "error": "Missing 'id' in frontmatter"
        })
        
    if "type" not in yaml_dict:
        errors.append({
            "file": rel_src,
            "line": 1,
            "link": "type",
            "error": "Missing 'type' in frontmatter"
        })
    elif yaml_dict["type"] != expected_types[type_dir]:
        errors.append({
            "file": rel_src,
            "line": 1,
            "link": "type",
            "error": f"Invalid type '{yaml_dict['type']}' for folder '{type_dir}/'. Expected '{expected_types[type_dir]}'."
        })
        
    if type_dir in {"mula", "atthakatha", "tika"}:
        required = ["title_pali", "pitaka", "nikaya", "sutta_number"]
        for field in required:
            if field not in yaml_dict or not yaml_dict[field]:
                errors.append({
                    "file": rel_src,
                    "line": 1,
                    "link": field,
                    "error": f"Missing required field '{field}' in canonical text frontmatter"
                })
        
        if "pitaka" in yaml_dict and yaml_dict["pitaka"] not in {"sutta", "vinaya", "abhidhamma"}:
            errors.append({
                "file": rel_src,
                "line": 1,
                "link": "pitaka",
                "error": f"Invalid pitaka value '{yaml_dict['pitaka']}'"
            })
        if "nikaya" in yaml_dict and yaml_dict["nikaya"] not in {"majjhima", "digha", "samyutta", "anguttara", "khuddaka", "None"}:
            errors.append({
                "file": rel_src,
                "line": 1,
                "link": "nikaya",
                "error": f"Invalid nikaya value '{yaml_dict['nikaya']}'"
            })
            
        for link_field in ["commentary_file", "sub_commentary_file", "mula_file"]:
            if link_field in yaml_dict and yaml_dict[link_field]:
                target_path = yaml_dict[link_field].lstrip("/")
                abs_target = os.path.join(VAULT_DIR, target_path)
                if not os.path.exists(abs_target):
                    errors.append({
                        "file": rel_src,
                        "line": 1,
                        "link": yaml_dict[link_field],
                        "error": f"Referenced {link_field} '{yaml_dict[link_field]}' does not exist."
                    })
                    
    elif type_dir == "matika":
        if "title_pali" not in yaml_dict or not yaml_dict["title_pali"]:
            errors.append({
                "file": rel_src,
                "line": 1,
                "link": "title_pali",
                "error": "Missing 'title_pali' in matika frontmatter"
            })
        if "category" not in yaml_dict or yaml_dict["category"] not in {"list_note", "factor_note"}:
            errors.append({
                "file": rel_src,
                "line": 1,
                "link": "category",
                "error": f"Invalid category '{yaml_dict.get('category')}' in matika"
            })
            
    elif type_dir in {"practice", "paths"}:
        if "title" not in yaml_dict or not yaml_dict["title"]:
            errors.append({
                "file": rel_src,
                "line": 1,
                "link": "title",
                "error": f"Missing 'title' in {type_dir} frontmatter"
            })
            
    return errors

def check_dataview_queries(content, filepath, rel_src):
    errors = []
    # Find all dataview code blocks
    blocks = re.findall(r"```dataview\n(.*?)\n```", content, re.DOTALL)
    for block in blocks:
        lines = block.split('\n')
        for line_offset, line in enumerate(lines, 1):
            cleaned = line.strip()
            
            # 1. Match "type" as a standalone word (not row.type, not file.type, not "type" in quotes)
            match_type = re.search(r"(?<!\.)\btype\b", cleaned)
            if match_type:
                if not cleaned.startswith("//") and not cleaned.startswith("#") and not ('"' in cleaned or "'" in cleaned):
                    errors.append({
                        "file": rel_src,
                        "line": line_offset,
                        "link": "Dataview Query",
                        "error": f"Potential Dataview query collision: Standalone keyword 'type' found on line: '{cleaned}'. Use 'row.type' or 'file.frontmatter.type' to avoid collision with Dataview's built-in type() function."
                    })
            
            # 2. Match "category = list" or similar which collides with LIST query type
            match_list = re.search(r"\bcategory\s*=\s*[\"']?list[\"']?\b", cleaned, re.IGNORECASE)
            if match_list:
                errors.append({
                    "file": rel_src,
                    "line": line_offset,
                    "link": "Dataview Query",
                    "error": f"Potential Dataview query collision: category filtered by 'list' found on line: '{cleaned}'. Use 'list_note' to avoid collision with Dataview's LIST query keyword."
                })
                
            # 3. Match absolute folder constraints: FROM "folder" (except FROM "")
            match_from = re.search(r'\bFROM\s+"([^"]+)"', cleaned, re.IGNORECASE)
            if match_from and match_from.group(1).strip() != "":
                errors.append({
                    "file": rel_src,
                    "line": line_offset,
                    "link": "Dataview Query",
                    "error": f"Potential nested vault failure: absolute FROM folder query '{cleaned}' found. Use 'WHERE contains(file.path, \"{match_from.group(1)}/\")' instead to ensure nested vault compatibility."
                })
    return errors

def validate_vault(target_files=None):
    all_files = get_markdown_files(VAULT_DIR, EXCLUDE_INDEX_DIRS)
    scan_files = target_files if target_files is not None else get_markdown_files(VAULT_DIR, EXCLUDE_SCAN_DIRS)
    
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

    # Lazy-loaded headers dictionary to avoid pre-parsing all files
    file_headers = {}

    # Wikilink pattern: [[target]] or [[target|label]]
    # target may contain an anchor: e.g. target#anchor
    wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
    html_link_pattern = re.compile(r'<a\s+[^>]*href="([^":\s]+\.md(?:#[^"]+)?)"[^>]*>')
    
    errors = []
    total_links_checked = 0
    
    for filepath in scan_files:
        rel_src = os.path.relpath(filepath, VAULT_DIR)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Validate frontmatter block first
        fm_errors = validate_frontmatter(filepath, content, rel_src)
        errors.extend(fm_errors)
        
        # Validate Dataview query blocks
        dv_errors = check_dataview_queries(content, filepath, rel_src)
        errors.extend(dv_errors)
        
        for line_num, line in enumerate(content.splitlines(), 1):
                # Check Wikilinks
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
                    
                    # Skip non-markdown resource embeds (audio, images, CSS, etc.)
                    non_md_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.flac',
                                        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
                                        '.pdf', '.css', '.js', '.json', '.csv')
                    if target_path and any(target_path.lower().endswith(ext) for ext in non_md_extensions):
                        continue
                    
                    # Handle self-references (e.g., [[#anchor]])
                    if not target_path:
                        target_file = filepath
                    else:
                        # Clean backslash escapes in target
                        target_path = target_path.replace('\\', '')
                        
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
                        headers = file_headers.get(target_file)
                        if headers is None:
                            headers = parse_headers_and_anchors(target_file)
                            file_headers[target_file] = headers
                        if anchor not in headers:
                            norm_anchor = re.sub(r'[^\w\s§\-.]', '', anchor).strip()
                            matched_anchor = False
                            for h in headers:
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

                # Check HTML internal links
                for match in html_link_pattern.finditer(line):
                    total_links_checked += 1
                    raw_link = match.group(1).strip()
                    
                    # Split anchor if present
                    if '#' in raw_link:
                        target_path, anchor = raw_link.split('#', 1)
                        target_path = target_path.strip()
                        anchor = anchor.strip()
                    else:
                        target_path = raw_link
                        anchor = None
                    
                    # Strip .md extension
                    if target_path.endswith(".md"):
                        target_path = target_path[:-3]
                        
                    # Handle self-references (e.g., href="#anchor")
                    if not target_path:
                        target_file = filepath
                    else:
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
                                    "error": f"Ambiguous HTML link '{target_path}' matches multiple files"
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
                            "error": f"Target HTML file '{target_path}.md' not found"
                        })
                    elif anchor:
                        headers = file_headers.get(target_file)
                        if headers is None:
                            headers = parse_headers_and_anchors(target_file)
                            file_headers[target_file] = headers
                        if anchor not in headers:
                            norm_anchor = re.sub(r'[^\w\s§\-.]', '', anchor).strip()
                            matched_anchor = False
                            for h in headers:
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
    import argparse
    parser = argparse.ArgumentParser(description="Pali Canon Vault Link Validator")
    parser.add_argument("--files", nargs="*", help="Specific files to validate. If empty, validates all files.")
    args = parser.parse_args()
    
    target_files = []
    if args.files:
        for f in args.files:
            abs_f = os.path.abspath(f)
            if os.path.exists(abs_f) and abs_f.endswith(".md"):
                filename = os.path.basename(abs_f)
                if filename.startswith("FROM-CLAUDE") or "archive" in abs_f.split(os.sep):
                    continue
                target_files.append(abs_f)
                
    success = validate_vault(target_files=target_files if target_files else None)
    if not success:
        sys.exit(1)
