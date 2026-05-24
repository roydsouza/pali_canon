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

if __name__ == "__main__":
    unittest.main()
