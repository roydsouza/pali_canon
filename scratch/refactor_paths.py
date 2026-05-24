#!/usr/bin/env python3
import os
import re

def refactor_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Matches variables containing VAULT (like VAULT, VAULT_DIR) defined as a string literal "/Users/rds/pali_canon"
    # Matches: VAULT = "/Users/rds/pali_canon" or VAULT  = '/Users/rds/pali_canon' etc.
    # Excludes lines that already use os.environ
    pattern = r'^(\s*[A-Za-z0-9_]*VAULT[A-Za-z0-9_]*\s*=\s*)(["\'])/Users/rds/pali_canon\2'
    
    modified = False
    new_lines = []
    has_os = False
    
    lines = content.split('\n')
    for line in lines:
        if re.search(r'^\s*(import\s+[^#\n]*\bos\b|from\s+os\s+import)', line):
            has_os = True
            
        m = re.match(pattern, line)
        if m:
            var_part = m.group(1)
            new_line = f'{var_part}os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")'
            new_lines.append(new_line)
            modified = True
        else:
            new_lines.append(line)
            
    if modified:
        new_content = '\n'.join(new_lines)
        if not has_os:
            # Insert import os safely
            if new_content.startswith('#!'):
                parts = new_content.split('\n', 1)
                if len(parts) == 2:
                    new_content = f"{parts[0]}\nimport os\n{parts[1]}"
                else:
                    new_content = f"{parts[0]}\nimport os"
            else:
                new_content = f"import os\n{new_content}"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Refactored: {filepath}")
        return True
    return False

def main():
    scratch_dir = os.path.dirname(os.path.abspath(__file__))
    refactored_count = 0
    
    for root, _, files in os.walk(scratch_dir):
        if "__pycache__" in root or ".git" in root or ".obsidian" in root:
            continue
        for file in files:
            if file.endswith(".py") and file != "refactor_paths.py":
                filepath = os.path.join(root, file)
                if refactor_file(filepath):
                    refactored_count += 1
                    
    print(f"Total files refactored: {refactored_count}")

if __name__ == "__main__":
    main()
