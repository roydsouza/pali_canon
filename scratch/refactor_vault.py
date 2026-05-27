#!/usr/bin/env python3
import os
import re
import sys

VAULT_DIR = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")

# The 22 Matika lists
MATIKA_LISTS = {
    "four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates",
    "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors",
    "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections",
    "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions",
    "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"
}

def parse_yaml(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None, content
    
    yaml_text = match.group(1)
    body = content[len(match.group(0)):]
    
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
    return yaml_dict, body

def write_yaml(yaml_dict):
    lines = ["---"]
    for key, val in yaml_dict.items():
        if isinstance(val, list):
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {item}")
        else:
            val_str = str(val)
            # Wrap string if it has special characters like quotes or colon
            if ":" in val_str or '"' in val_str or "'" in val_str or val_str.startswith("http") or val_str == "":
                cleaned = val_str.replace('"', '\\"')
                lines.append(f'{key}: "{cleaned}"')
            else:
                lines.append(f"{key}: {val_str}")
    lines.append("---")
    return "\n".join(lines) + "\n"

def get_all_markdown_files(vault_dir):
    md_files = []
    for root, dirs, files in os.walk(vault_dir):
        # Exclude dot folders and scratch/templates
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ("scratch", "templates")]
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def infer_metadata_from_path(filepath):
    rel_path = os.path.relpath(filepath, VAULT_DIR)
    parts = rel_path.split(os.sep)
    
    type_val = parts[0]
    pitaka_val = None
    nikaya_val = None
    
    if len(parts) >= 2:
        if parts[1] in ("sutta", "vinaya", "abhidhamma"):
            pitaka_val = parts[1]
        else:
            # e.g. matika/filename.md
            pitaka_val = None
            
    if len(parts) >= 3:
        folder_name = parts[2]
        if folder_name == "majjhima_nikaya":
            nikaya_val = "majjhima"
        elif folder_name == "digha_nikaya":
            nikaya_val = "digha"
        elif folder_name == "samyutta_nikaya":
            nikaya_val = "samyutta"
        elif folder_name == "anguttara_nikaya":
            nikaya_val = "anguttara"
        elif folder_name == "khuddaka_nikaya":
            nikaya_val = "khuddaka"
            
    return type_val, pitaka_val, nikaya_val

def derive_id_and_number(filename, nikaya):
    base = os.path.splitext(filename)[0]
    
    if nikaya == "majjhima":
        m = re.match(r"^mn(\d+)$", base)
        if m:
            return f"MN{m.group(1)}", m.group(1)
    elif nikaya == "digha":
        m = re.match(r"^dn(\d+)$", base)
        if m:
            return f"DN{m.group(1)}", m.group(1)
    elif nikaya == "samyutta":
        m = re.match(r"^sn(\d+)_(\d+)$", base)
        if m:
            return f"SN{m.group(1)}.{m.group(2)}", f"{m.group(1)}.{m.group(2)}"
        m = re.match(r"^sn(\d+)$", base)
        if m:
            return f"SN{m.group(1)}", m.group(1)
    elif nikaya == "anguttara":
        m = re.match(r"^an(\d+)_(\d+)_(\d+)$", base)
        if m:
            return f"AN{m.group(1)}.{m.group(2)}-{m.group(3)}", f"{m.group(1)}.{m.group(2)}-{m.group(3)}"
        m = re.match(r"^an(\d+)_(\d+)$", base)
        if m:
            return f"AN{m.group(1)}.{m.group(2)}", f"{m.group(1)}.{m.group(2)}"
        m = re.match(r"^an(\d+)$", base)
        if m:
            return f"AN{m.group(1)}", m.group(1)
    elif nikaya == "khuddaka":
        if base.startswith("snp"):
            cleaned = base.replace("_", ".")
            m = re.match(r"^snp(\d+)\.(\d+)$", cleaned)
            if m:
                return f"Snp{m.group(1)}.{m.group(2)}", f"{m.group(1)}.{m.group(2)}"
        elif base.startswith("thag"):
            cleaned = base.replace("_", ".")
            m = re.match(r"^thag(\d+)\.(\d+)$", cleaned)
            if m:
                return f"Thag{m.group(1)}.{m.group(2)}", f"{m.group(1)}.{m.group(2)}"
        elif base.startswith("thig"):
            cleaned = base.replace("_", ".")
            m = re.match(r"^thig(\d+)\.(\d+)$", cleaned)
            if m:
                return f"Thig{m.group(1)}.{m.group(2)}", f"{m.group(1)}.{m.group(2)}"
        elif base.startswith("dhp"):
            m = re.match(r"^dhp_(\d+)(?:_.*)?$", base)
            if m:
                val = int(m.group(1))
                return f"DHP_{m.group(1)}", str(val)
            
    # Fallback/default logic:
    m = re.match(r"^([a-z]+)(\d+)(?:_(\d+))?$", base)
    if m:
        prefix = m.group(1).upper()
        if m.group(3):
            return f"{prefix}{m.group(2)}.{m.group(3)}", f"{m.group(2)}.{m.group(3)}"
        else:
            return f"{prefix}{m.group(2)}", m.group(2)
            
    return base.upper(), base

def refactor_vault():
    print("Step 1: Renaming conflicting path files and updating links...")
    # Overlapping files in paths/
    # paths/maranasati.md -> paths/maranasati_path.md
    # paths/gradual_training.md -> paths/gradual_training_path.md
    # paths/entering_jhana.md -> paths/entering_jhana_path.md
    
    renames = {
        os.path.join(VAULT_DIR, "paths", "maranasati.md"): os.path.join(VAULT_DIR, "paths", "maranasati_path.md"),
        os.path.join(VAULT_DIR, "paths", "gradual_training.md"): os.path.join(VAULT_DIR, "paths", "gradual_training_path.md"),
        os.path.join(VAULT_DIR, "paths", "entering_jhana.md"): os.path.join(VAULT_DIR, "paths", "entering_jhana_path.md")
    }
    
    for src, dst in renames.items():
        if os.path.exists(src):
            os.rename(src, dst)
            print(f"Renamed {os.path.basename(src)} -> {os.path.basename(dst)}")

    # Step 2: Build maps of all Mūla, Atthakathā, and Tīkā files to correct links
    all_files = get_all_markdown_files(VAULT_DIR)
    
    mula_paths = {}       # e.g. "mn118" -> "/mula/sutta/majjhima_nikaya/mn118.md"
    atthakatha_paths = {} # e.g. "mn118" -> "/atthakatha/sutta/majjhima_nikaya/mn118_att.md"
    tika_paths = {}       # e.g. "mn118" -> "/tika/sutta/majjhima_nikaya/mn118_tik.md"
    
    for filepath in all_files:
        rel = "/" + os.path.relpath(filepath, VAULT_DIR).replace(os.sep, "/")
        filename = os.path.basename(filepath)
        base = os.path.splitext(filename)[0]
        
        type_val, _, _ = infer_metadata_from_path(filepath)
        
        if type_val == "mula":
            mula_paths[base] = rel
        elif type_val == "atthakatha":
            # e.g. mn118_att -> mn118
            m = re.match(r"^(.*?)(?:_att)?$", base)
            if m:
                mula_paths_base = m.group(1)
                atthakatha_paths[mula_paths_base] = rel
        elif type_val == "tika":
            # e.g. mn118_tik -> mn118
            m = re.match(r"^(.*?)(?:_tik)?$", base)
            if m:
                mula_paths_base = m.group(1)
                tika_paths[mula_paths_base] = rel

    # Step 3: Run the normalization sweep on all files
    print("Step 3: Normalizing YAML frontmatter for all markdown files...")
    for filepath in all_files:
        filename = os.path.basename(filepath)
        base = os.path.splitext(filename)[0]
        
        # Read file
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # First, update any links in the body to renamed path files
        # Replace:
        # [[paths/maranasati| -> [[paths/maranasati_path|
        # [[paths/maranasati]] -> [[paths/maranasati_path]]
        # [[maranasati]] in paths/INDEX.md -> [[paths/maranasati_path]]
        # [[paths/gradual_training| -> [[paths/gradual_training_path|
        # [[paths/gradual_training]] -> [[paths/gradual_training_path]]
        # [[entering_jhana| -> [[paths/entering_jhana_path|
        # [[entering_jhana]] -> [[paths/entering_jhana_path]]
        content = re.sub(r'\[\[paths/maranasati(\||\s*\]\])', r'[[paths/maranasati_path\1', content)
        content = re.sub(r'\[\[paths/gradual_training(\||\s*\]\])', r'[[paths/gradual_training_path\1', content)
        content = re.sub(r'\[\[paths/entering_jhana(\||\s*\]\])', r'[[paths/entering_jhana_path\1', content)
        
        # Also clean direct wikilinks to renamed path pages if they are inside paths/ files
        if "paths" in filepath:
            content = re.sub(r'\[\[entering_jhana(\||\s*\]\])', r'[[entering_jhana_path\1', content)
            content = re.sub(r'\[\[gradual_training(\||\s*\]\])', r'[[paths/gradual_training_path\1', content)
            content = re.sub(r'\[\[maranasati(\||\s*\]\])', r'[[paths/maranasati_path\1', content)
            
        # Parse YAML
        yaml_dict, body = parse_yaml(content)
        if yaml_dict is None:
            # No YAML frontmatter. Let's add standard headers if appropriate, or skip
            # The root INDEX.md doesn't have YAML (or might, let's keep it safe)
            continue
            
        type_path, pitaka_path, nikaya_path = infer_metadata_from_path(filepath)
        
        # Build new yaml dictionary preserving order
        new_yaml = {}
        
        # Determine schema by type
        if type_path == "mula":
            mula_base = base
            mula_id, sutta_num = derive_id_and_number(mula_base, nikaya_path)
            
            new_yaml["id"] = mula_id
            new_yaml["title_pali"] = yaml_dict.get("title_pali", "")
            if "title_en" in yaml_dict or "title_en" in new_yaml:
                new_yaml["title_en"] = yaml_dict.get("title_en", "")
            new_yaml["type"] = "mula"
            new_yaml["pitaka"] = pitaka_path
            new_yaml["nikaya"] = nikaya_path
            new_yaml["sutta_number"] = sutta_num
            
            if "translator" in yaml_dict:
                new_yaml["translator"] = yaml_dict["translator"]
            if "source" in yaml_dict:
                new_yaml["source"] = yaml_dict["source"]
                
            # Exegesis mapping
            if mula_base in atthakatha_paths:
                new_yaml["commentary_file"] = atthakatha_paths[mula_base]
            if mula_base in tika_paths:
                new_yaml["sub_commentary_file"] = tika_paths[mula_base]
                
            # Carry over tags or other non-standard fields
            for k, v in yaml_dict.items():
                if k not in new_yaml and k not in ("commentary_file", "sub_commentary_file", "id", "sutta_number", "type", "pitaka", "nikaya"):
                    new_yaml[k] = v
                    
        elif type_path == "atthakatha":
            mula_base = re.match(r"^(.*?)(?:_att)?$", base).group(1)
            mula_id, sutta_num = derive_id_and_number(mula_base, nikaya_path)
            
            new_yaml["id"] = f"{mula_id}_att"
            new_yaml["title_pali"] = yaml_dict.get("title_pali", "")
            new_yaml["type"] = "atthakatha"
            new_yaml["pitaka"] = pitaka_path
            new_yaml["nikaya"] = nikaya_path
            new_yaml["sutta_number"] = sutta_num
            
            if mula_base in mula_paths:
                new_yaml["mula_file"] = mula_paths[mula_base]
            if mula_base in tika_paths:
                new_yaml["sub_commentary_file"] = tika_paths[mula_base]
                
            for k, v in yaml_dict.items():
                if k not in new_yaml and k not in ("mula_file", "sub_commentary_file", "id", "sutta_number", "type", "pitaka", "nikaya"):
                    new_yaml[k] = v
                    
        elif type_path == "tika":
            mula_base = re.match(r"^(.*?)(?:_tik)?$", base).group(1)
            mula_id, sutta_num = derive_id_and_number(mula_base, nikaya_path)
            
            new_yaml["id"] = f"{mula_id}_tik"
            new_yaml["title_pali"] = yaml_dict.get("title_pali", "")
            new_yaml["type"] = "tika"
            new_yaml["pitaka"] = pitaka_path
            new_yaml["nikaya"] = nikaya_path
            new_yaml["sutta_number"] = sutta_num
            
            if mula_base in mula_paths:
                new_yaml["mula_file"] = mula_paths[mula_base]
            if mula_base in atthakatha_paths:
                new_yaml["commentary_file"] = atthakatha_paths[mula_base]
                
            for k, v in yaml_dict.items():
                if k not in new_yaml and k not in ("mula_file", "commentary_file", "id", "sutta_number", "type", "pitaka", "nikaya"):
                    new_yaml[k] = v
                    
        elif type_path == "matika":
            new_yaml["id"] = base
            new_yaml["title_pali"] = yaml_dict.get("title_pali", "")
            new_yaml["type"] = "matika"
            
            category = "list" if base in MATIKA_LISTS else "factor"
            new_yaml["category"] = category
            
            for k, v in yaml_dict.items():
                if k not in new_yaml and k not in ("id", "type", "category"):
                    new_yaml[k] = v
                    
        elif type_path == "practice":
            new_yaml["id"] = base
            new_yaml["title"] = yaml_dict.get("title", base.replace("_", " ").title())
            new_yaml["type"] = "practice"
            for k, v in yaml_dict.items():
                if k not in new_yaml and k not in ("id", "type", "title"):
                    new_yaml[k] = v
                    
        elif type_path == "paths":
            # For paths, we determine ID based on renamed base
            new_yaml["id"] = base
            new_yaml["title"] = yaml_dict.get("title", base.replace("_", " ").title())
            new_yaml["type"] = "path"
            for k, v in yaml_dict.items():
                if k not in new_yaml and k not in ("id", "type", "title"):
                    new_yaml[k] = v
        else:
            # Fallback
            new_yaml["id"] = yaml_dict.get("id", base)
            new_yaml["type"] = yaml_dict.get("type", type_path)
            for k, v in yaml_dict.items():
                if k not in new_yaml:
                    new_yaml[k] = v
                    
        # Write back
        new_content = write_yaml(new_yaml) + body
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
            
    print("Vault refactoring complete.")

if __name__ == "__main__":
    refactor_vault()
