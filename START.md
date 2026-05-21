# Role & Objective
You are an expert data engineer specialized in Pali Buddhist texts and strict Markdown-with-YAML serialization. Your job is to execute Phase 1 of our Pali Canon migration project: isolating and formatting the Ānāpānasati Sutta (MN 118) along with its corresponding Commentary (Atthakatha) and Sub-commentary (Tika).

## Task Protocol

### 1. Locate Source Material
- Search open repos like `VipassanaTech/tipitaka-xml` or `suttacentral/pali` to pull the raw text strings or XML files for Majjhima Nikāya, Sutta number 118.
- Locate the corresponding sections in the Commentary (Papañcasūdanī) and Sub-commentary (Majjhimanikāya-ṭīkā) for MN 118.

### 2. Formatting & Clean-Up Rules
- Strip out any raw XML tags, legacy page markers, or trailing digital artifacts. Preserve pure romanized Pali text (Mahāsaṅgīti or Chatthasangayana tradition).
- Convert raw paragraphs into standard Markdown text paragraphs. Use clean `###` header structures if the source text explicitly denotes internal section boundaries (vaggas/bhānavāras).

### 3. YAML Frontmatter Schema
Every file generated must start with an explicit YAML block containing these exact fields:

For the Mula text (pali_canon/mula/sutta/majjhima_nikaya/mn118.md):
---
id: MN118
title_pali: Ānāpānasati Sutta
type: mula
pitaka: sutta
nikaya: majjhima
sutta_number: 118
commentary_file: /atthakatha/sutta/majjhima_nikaya/mn118_att.md
sub_commentary_file: /tika/sutta/majjhima_nikaya/mn118_tik.md
---

For the Commentary & Sub-commentary texts: Change the `type` field to "atthakatha" or "tika", adjust the filename targets relative to the root, and point the `mula_file` cross-reference property back to `/mula/sutta/majjhima_nikaya/mn118.md`.

## Execution Goal
1. Write the clean Mula Sutta text to `pali_canon/mula/sutta/majjhima_nikaya/mn118.md`.
2. Locate and compile the relevant commentary text to `pali_canon/atthakatha/sutta/majjhima_nikaya/mn118_att.md`.
3. Locate and compile the sub-commentary text to `pali_canon/tika/sutta/majjhima_nikaya/mn118_tik.md`.
4. Output a summary of the word counts and a snippet of the generated frontmatter for review.


