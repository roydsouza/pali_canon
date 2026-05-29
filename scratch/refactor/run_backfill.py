#!/usr/bin/env python3
import os
import sys
import subprocess

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path

# Target configurations to cross-link
TARGETS = [
    {
        "name": "MN 36",
        "mula": "mula/sutta/majjhima_nikaya/mn36.md",
        "att": "atthakatha/sutta/majjhima_nikaya/mn36_att.md",
        "tik": "tika/sutta/majjhima_nikaya/mn36_tik.md"
    },
    {
        "name": "DN 22",
        "mula": "mula/sutta/digha_nikaya/dn22.md",
        "att": "atthakatha/sutta/digha_nikaya/dn22_att.md",
        "tik": "tika/sutta/digha_nikaya/dn22_tik.md"
    },
    {
        "name": "SN 12",
        "mula": "mula/sutta/samyutta_nikaya/sn12.md",
        "att": "atthakatha/sutta/samyutta_nikaya/sn12_att.md",
        "tik": "tika/sutta/samyutta_nikaya/sn12_tik.md"
    },
    {
        "name": "SN 22",
        "mula": "mula/sutta/samyutta_nikaya/sn22.md",
        "att": "atthakatha/sutta/samyutta_nikaya/sn22_att.md",
        "tik": "tika/sutta/samyutta_nikaya/sn22_tik.md"
    },
    {
        "name": "SN 35",
        "mula": "mula/sutta/samyutta_nikaya/sn35.md",
        "att": "atthakatha/sutta/samyutta_nikaya/sn35_att.md",
        "tik": "tika/sutta/samyutta_nikaya/sn35_tik.md"
    },
    {
        "name": "SN 46",
        "mula": "mula/sutta/samyutta_nikaya/sn46.md",
        "att": "atthakatha/sutta/samyutta_nikaya/sn46_att.md",
        "tik": "tika/sutta/samyutta_nikaya/sn46_tik.md"
    },
    {
        "name": "SN 54",
        "mula": "mula/sutta/samyutta_nikaya/sn54.md",
        "att": "atthakatha/sutta/samyutta_nikaya/sn54_att.md",
        "tik": "tika/sutta/samyutta_nikaya/sn54_tik.md"
    },
    {
        "name": "SN 56",
        "mula": "mula/sutta/samyutta_nikaya/sn56.md",
        "att": "atthakatha/sutta/samyutta_nikaya/sn56_att.md",
        "tik": "tika/sutta/samyutta_nikaya/sn56_tik.md"
    }
]

def main():
    vault_dir = get_vault_path()
    script_path = os.path.join(vault_dir, "scratch", "crosslinkers", "crosslink_generic.py")
    
    if not os.path.exists(script_path):
        print(f"Error: crosslink_generic.py not found at {script_path}")
        sys.exit(1)
        
    print(f"Starting Paragraph-Level Cross-Linking Backfill (8 targets)...")
    
    for idx, target in enumerate(TARGETS, 1):
        print(f"\n[{idx}/8] Processing {target['name']}...")
        
        mula_abs = os.path.join(vault_dir, target["mula"])
        att_abs = os.path.join(vault_dir, target["att"])
        tik_abs = os.path.join(vault_dir, target["tik"]) if target.get("tik") else None
        
        # Verify files exist
        if not os.path.exists(mula_abs):
            print(f"  Warning: Mula file not found: {target['mula']}")
            continue
        if not os.path.exists(att_abs):
            print(f"  Warning: Atthakatha file not found: {target['att']}")
            continue
        if tik_abs and not os.path.exists(tik_abs):
            print(f"  Warning: Tika file not found: {target['tik']}")
            tik_abs = None
            
        cmd = ["python3", script_path, "--mula", mula_abs, "--att", att_abs]
        if tik_abs:
            cmd.extend(["--tik", tik_abs])
            
        print(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  Success! {target['name']} crosslinked.")
            # Print a brief summary of output
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if "Found" in line or "Updated" in line or "No new" in line:
                    print(f"    {line}")
        else:
            print(f"  Failed with code {result.returncode} for {target['name']}")
            print(f"  Error: {result.stderr}")
            
    print("\nBackfill coordination completed.")

if __name__ == "__main__":
    main()
