#!/usr/bin/env python3
import os
import sys
import unittest
from unittest.mock import patch

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path, clean_xml, load_cscd_paras, parse_frontmatter

class TestPaliUtils(unittest.TestCase):
    
    def test_get_vault_path_default(self):
        # Temporarily clear env var to check default
        old_val = os.environ.get("PALI_VAULT")
        if "PALI_VAULT" in os.environ:
            del os.environ["PALI_VAULT"]
        try:
            self.assertEqual(get_vault_path(), "/Users/rds/pali_canon")
        finally:
            if old_val is not None:
                os.environ["PALI_VAULT"] = old_val

    def test_get_vault_path_env(self):
        old_val = os.environ.get("PALI_VAULT")
        os.environ["PALI_VAULT"] = "/custom/vault/path"
        try:
            self.assertEqual(get_vault_path(), "/custom/vault/path")
        finally:
            if old_val is not None:
                os.environ["PALI_VAULT"] = old_val
            else:
                del os.environ["PALI_VAULT"]

    def test_clean_xml_basic(self):
        self.assertEqual(clean_xml(""), "")
        self.assertEqual(clean_xml(None), "")
        self.assertEqual(clean_xml("Normal text"), "Normal text")

    def test_clean_xml_bold_hi(self):
        self.assertEqual(clean_xml('Hello <hi rend="bold">world</hi>!'), "Hello **world**!")
        self.assertEqual(clean_xml('Some <hi rend="bold">bold\nlines</hi>'), "Some **bold lines**")

    def test_clean_xml_pb(self):
        self.assertEqual(clean_xml('Text with <pb id="p_1a"/> page break'), "Text with page break")
        self.assertEqual(clean_xml('Another <pb id="p_1a"/>page break'), "Another page break")

    def test_clean_xml_other_tags(self):
        self.assertEqual(clean_xml('Hello <i>world</i> and <p rend="body">para</p>'), "Hello world and para")

    def test_clean_xml_html_entities(self):
        self.assertEqual(clean_xml("Some &amp; other &lt;text&gt;"), "Some & other <text>")

    def test_parse_frontmatter_string(self):
        fm_content = """---
id: MN118
title_pali: "Ānāpānasati Sutta"
sutta_number: 118
---
Some body content here
"""
        meta = parse_frontmatter(fm_content)
        self.assertEqual(meta.get("id"), "MN118")
        self.assertEqual(meta.get("title_pali"), "Ānāpānasati Sutta")
        self.assertEqual(meta.get("sutta_number"), "118")

    @patch('lib.pali_utils.fetch_bytes')
    def test_load_cscd_paras(self, mock_fetch):
        # Mock XML contents
        xml_data = b"""<?xml version="1.0" encoding="utf-8"?>
<p rend="subhead"><hi rend="paranum">1</hi> <hi rend="bold">Header Title</hi></p>
<p rend="body">Normal paragraph text &amp; more.</p>
"""
        mock_fetch.return_value = xml_data
        
        paras = load_cscd_paras("test.xml")
        
        self.assertEqual(len(paras), 2)
        self.assertEqual(paras[0], ("subhead", "1", "**Header Title**"))
        self.assertEqual(paras[1], ("body", "", "Normal paragraph text & more."))

class TestFrontmatterLinter(unittest.TestCase):
    def test_frontmatter_and_covers(self):
        # Configure path and import
        inspect_dir = os.path.join(SCRATCH_DIR, "inspect")
        if inspect_dir not in sys.path:
            sys.path.insert(0, inspect_dir)
        from lint_frontmatter import lint_all
        
        vault_dir = get_vault_path()
        errors = lint_all(vault_dir)
        
        if errors:
            for err in errors:
                print(f"\nLinter Error: [{err['file']}] {err['error']}", file=sys.stderr)
                
        self.assertEqual(len(errors), 0, f"Frontmatter linter found {len(errors)} errors.")

class TestIndexDashboard(unittest.TestCase):
    """
    Guard INDEX.md against known UX regressions.

    These tests encode two classes of bugs that have recurred:

    1. Dataview inline expressions ($= ...) inside HTML <div> blocks.
       They do not render in Obsidian when inside raw HTML — the plugin
       only processes Markdown sections. They silently show as raw code.

    2. Dashboard card badges (<span class="db-badge...">) that are not
       wrapped in <a> links. Every badge is a category label and should
       navigate to the top-level index for that layer.
    """

    @classmethod
    def setUpClass(cls):
        vault = get_vault_path()
        index_path = os.path.join(vault, "INDEX.md")
        with open(index_path, encoding="utf-8") as f:
            cls.content = f.read()
        cls.lines = cls.content.splitlines()

    def test_no_dataview_inline_in_html_blocks(self):
        """No `$= expr` Dataview inline expressions anywhere in INDEX.md."""
        import re
        bad_lines = [
            (i + 1, line)
            for i, line in enumerate(self.lines)
            if re.search(r'`\$=\s', line)
        ]
        self.assertEqual(
            bad_lines, [],
            "Dataview inline expressions (`$= ...`) found in INDEX.md — "
            "they do not render inside HTML <div> blocks. Use hardcoded "
            f"counts instead.\nOffending lines: {bad_lines}"
        )

    def test_all_db_badges_are_links(self):
        """Every <span class="db-badge..."> in a card header must be inside an <a> tag."""
        import re
        # Find every line with a db-badge span that is NOT preceded by <a on the same line
        bad_lines = []
        for i, line in enumerate(self.lines):
            if 'class="db-badge' in line and '<span' in line:
                # It's OK if wrapped in <a ... on the same line
                if '<a ' not in line and '</a>' not in line:
                    bad_lines.append((i + 1, line.strip()))
        self.assertEqual(
            bad_lines, [],
            "Found db-badge <span> elements not wrapped in an <a> link. "
            "Every card badge must link to the section's top-level index.\n"
            f"Offending lines: {bad_lines}"
        )

    def test_hardcoded_counts_are_integers(self):
        """Badge count labels must be plain integers or short strings, not expressions."""
        import re
        # Match content inside db-badge spans: should not contain backticks or dv.
        badge_contents = re.findall(r'<span class="db-badge[^"]*">([^<]+)</span>', self.content)
        bad = [b for b in badge_contents if '`' in b or 'dv.' in b or '$=' in b]
        self.assertEqual(
            bad, [],
            f"db-badge content contains dynamic expressions: {bad}"
        )


if __name__ == "__main__":
    unittest.main()
