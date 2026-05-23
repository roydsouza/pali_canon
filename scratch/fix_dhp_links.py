#!/usr/bin/env python3
import os
import re

DHP_DIR = "/Users/rds/pali_canon/atthakatha/sutta/khuddaka_nikaya/dhammapada"

ranges = [
    (1, 20, "dhp_01_yamakavagga"),
    (21, 32, "dhp_02_appamadavagga"),
    (33, 43, "dhp_03_cittavagga"),
    (44, 59, "dhp_04_pupphavagga"),
    (60, 75, "dhp_05_balavagga"),
    (76, 89, "dhp_06_panditavagga"),
    (90, 99, "dhp_07_arahantavagga"),
    (100, 115, "dhp_08_sahassavagga"),
    (116, 128, "dhp_09_papavagga"),
    (129, 145, "dhp_10_dandavagga"),
    (146, 156, "dhp_11_jaravagga"),
    (157, 166, "dhp_12_attavagga"),
    (167, 178, "dhp_13_lokavagga"),
    (179, 196, "dhp_14_buddhavagga"),
    (197, 208, "dhp_15_sukhavagga"),
    (209, 220, "dhp_16_piyavagga"),
    (221, 234, "dhp_17_kodhavagga"),
    (235, 255, "dhp_18_malavagga"),
    (256, 272, "dhp_19_dhammatthavagga"),
    (273, 289, "dhp_20_maggavagga"),
    (290, 305, "dhp_21_pakinnakavagga"),
    (306, 319, "dhp_22_nirayavagga"),
    (320, 333, "dhp_23_nagavagga"),
    (334, 359, "dhp_24_tanhavagga"),
    (360, 382, "dhp_25_bhikkhuvagga"),
    (383, 423, "dhp_26_brahmanavagga"),
]

def get_correct_slug(verse_num):
    for start, end, slug in ranges:
        if start <= verse_num <= end:
            return slug
    return None

def fix_links_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Match [[dhp_XX_YY#ZZ|Dhp ZZ]] or [[dhp_XX_YY#ZZ]]
    # Let's replace any dhp_XX_YY with correct slug based on ZZ
    pattern = re.compile(r'\[\[(dhp_\d+_\w+)#(\d+)([^\]]*)\]\]')
    
    replacements = 0
    
    def repl_func(match):
        nonlocal replacements
        old_slug = match.group(1)
        verse_num_str = match.group(2)
        rest = match.group(3)
        verse_num = int(verse_num_str)
        correct_slug = get_correct_slug(verse_num)
        if correct_slug and old_slug != correct_slug:
            replacements += 1
            return f"[[{correct_slug}#{verse_num_str}{rest}]]"
        return match.group(0)

    new_content = pattern.sub(repl_func, content)
    
    if replacements > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {replacements} links in {os.path.basename(filepath)}")

def main():
    for filename in os.listdir(DHP_DIR):
        if filename.endswith(".md") and filename != "INDEX.md":
            fix_links_in_file(os.path.join(DHP_DIR, filename))

if __name__ == "__main__":
    main()
