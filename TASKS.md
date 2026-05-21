# Project Tasks Checklist

This file tracks the roadmap and pending tasks for the Pali Canon Vault.

## Active Phase: Majjhima Nikāya Expansion & Cross-Linking

### 1. Leaf Translation and Interleaving
- [ ] Migrate and interleave key meditation discourses (Mūla, Commentary, and Sub-commentary):
  - [ ] **MN 10: Satipaṭṭhāna Sutta** (Foundations of Mindfulness)
  - [ ] **MN 20: Vitakkasaṇṭhāna Sutta** (Removal of Distracting Thoughts)
  - [ ] **MN 119: Kāyagatāsati Sutta** (Mindfulness of the Body)
  - [ ] **MN 121: Cūḷasuññata Sutta** (Lesser Discourse on Emptiness)
  - [ ] **DN 2: Sāmaññaphala Sutta** (Fruits of the Recluse Life - Gradual Training)
  - [ ] **AN 4.41: Samādhibhāvanā Sutta** (Four Developments of Concentration)

### 2. Sutta-Commentary-Subcommentary Cross-Linking
- [ ] Cross-link MN 118 Mūla ([mn118.md](file:///Users/rds/pali_canon/mula/sutta/majjhima_nikaya/mn118.md)) segments directly to their commentary references in [mn118_att.md](file:///Users/rds/pali_canon/atthakatha/sutta/majjhima_nikaya/mn118_att.md)
- [ ] Cross-link MN 118 Commentary ([mn118_att.md](file:///Users/rds/pali_canon/atthakatha/sutta/majjhima_nikaya/mn118_att.md)) sections directly to the explanatory sub-commentary in [mn118_tik.md](file:///Users/rds/pali_canon/tika/sutta/majjhima_nikaya/mn118_tik.md)
- [ ] Embed anchor points or line-link targets in markdown files for precise reference jumping

### 3. Vault & Navigation Improvements
- [x] Implement a CSS snippet in `.obsidian/snippets/` to allow toggling translations on/off → `pali-translation-toggle.css` (enable in Obsidian Appearance settings; hotkey via Settings → Hotkeys)
- [x] Install Simsapa Dhamma Reader + Obsidian plugin for double-click Pali word lookup (DPD)
- [x] Install Dataview plugin for metadata queries across the vault
- [x] Install Templater plugin; hotkey `Templater: Insert toggle_translations` toggles translation CSS
- [x] Create templates folder with mula/atthakatha/tika sutta templates
- [x] Initialize git repository with `.gitignore`
- [x] Scaffold Khuddaka Nikāya, Abhidhamma Piṭaka, and Vinaya Piṭaka folder structures
- [ ] Build a script to automatically parse VRI XML files for commentaries and sub-commentaries of other Nikāyas
- [ ] Maintain the link validation script to verify vault health as new files are added
- [ ] Add Dataview query blocks to nikaya INDEX files for live sutta lists

### 4. Dhammapada (Khuddaka Nikāya)
- [x] Generate all 26 vaggas (423 verses) from SuttaCentral — Bhikkhu Sujato translation
- [x] Interleaved mula files: `mula/sutta/khuddaka_nikaya/dhammapada/dhp_01_*.md` through `dhp_26_*.md`
- [ ] Dhammapada-aṭṭhakathā (commentary) — famous origin stories for each verse
- [ ] Dhammapada Tīkā (sub-commentary)
- [ ] Cross-link vagga files to relevant mātikā entries

### 5. Expansion of Other Nikāyas (Future Phases)
- [ ] Dīgha Nikāya (Dīgha Nikāya Sutta, Commentary, Sub-commentary)
- [ ] Saṃyutta Nikāya (Saṃyutta Nikāya Sutta, Commentary, Sub-commentary)
- [ ] Aṅguttara Nikāya (Aṅguttara Nikāya Sutta, Commentary, Sub-commentary)

## Orthogonal Buddhist Lists (Mātika)
- [x] Create `matika/INDEX.md` index file
- [x] Create core lists with Pali and English translation:
  - [x] [[four_noble_truths|Four Noble Truths (Cattāri Ariyasaccāni)]]
  - [x] [[noble_eightfold_path|Noble Eightfold Path (Ariyo Aṭṭhaṅgiko Maggo)]]
  - [x] [[three_marks|Three Marks of Existence (Tilakkhaṇa)]]
  - [x] [[five_aggregates|Five Aggregates (Pañcupādānakkhandhā)]]
  - [x] [[dependent_origination|Dependent Origination (Paṭiccasamuppāda)]]
  - [x] [[five_precepts|Five Precepts (Pañcasīla)]]
  - [x] [[five_hindrances|Five Hindrances (Pañca Nīvaraṇāni)]]
  - [x] [[seven_awakening_factors|Seven Awakening Factors (Satta Bojjhaṅgā)]]
  - [x] [[four_foundations_of_mindfulness|Four Foundations of Mindfulness (Cattāro Satipaṭṭhānā)]]
  - [x] [[eight_precepts|Eight Precepts (Aṭṭhaṅgasīla)]]
  - [x] [[three_refuges|Three Refuges (Tisarana / Tiratana)]]
  - [x] [[ten_perfections|Ten Perfections (Dasa Pāramī)]]
  - [x] [[four_sublime_states|Four Sublime States (Cattāro Brahmavihārā)]]
  - [x] [[five_spiritual_faculties|Five Spiritual Faculties (Pañcindriya)]]
  - [x] [[three_unwholesome_roots|Three Unwholesome Roots (Akusalamūla)]]
  - [x] [[four_right_exertions|Four Right Exertions (Cattāro Sammappadhānā)]]
- [ ] Link lists to corresponding canonical occurrences as new suttas are added (e.g., link Satipaṭṭhāna Sutta when migrated)

