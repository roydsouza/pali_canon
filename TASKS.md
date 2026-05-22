# Project Tasks Checklist

This file tracks the roadmap and pending tasks for the Pali Canon Vault.

## Active Phase: Meditation Sutta Expansion — SN / AN / DN + Mātikā Integration

### 1. Leaf Translation and Interleaving
- [x] Migrate and interleave key meditation discourses (Mūla, Commentary, and Sub-commentary):
  - [x] **MN 10: Satipaṭṭhānasutta** — mūla complete (5,721 words, Sujato). `mula/sutta/majjhima_nikaya/mn10.md`
  - [x] **MN 20: Vitakkasaṇṭhānasutta** — mūla complete (1,798 words). `mn20.md`
  - [x] **MN 119: Kāyagatāsatisutta** — mūla complete (4,967 words). `mn119.md`
  - [x] **MN 121: Cūḷasuññatasutta** — mūla complete (2,760 words). `mn121.md`
  - [x] **DN 2: Sāmaññaphalasutta** — mūla complete (17,701 words). `mula/sutta/digha_nikaya/dn2.md`
  - [x] **AN 4.41: Samādhibhāvanāsutta** — mūla complete (745 words). `mula/sutta/anguttara_nikaya/an4_41.md`
  - [x] Commentary layer for all six — Pali (CSCD) + Sujato translator notes:
        - mn10_att.md — 362 paragraphs Papañcasūdanī + 49 notes (15,912 words)
        - mn20_att.md — 40 paragraphs + 11 notes (2,159 words)
        - mn119_att.md — 10 paragraphs + 18 notes (1,181 words)
        - mn121_att.md — 13 paragraphs + 15 notes (1,476 words)
        - dn2_att.md — 394 paragraphs Sumaṅgalavilāsinī + 141 notes (22,452 words)
        - an4_41_att.md — 15 paragraphs Manorathapūraṇī (952 words)
  - [x] Sub-commentary (tīkā) layer for all six:
        - mn10_tik.md — 232 paragraphs Papañcasūdanī-ṭīkā (11,365 words)
        - mn20_tik.md — 26 paragraphs (1,006 words)
        - mn119_tik.md — 8 paragraphs (358 words)
        - mn121_tik.md — 11 paragraphs (589 words)
        - dn2_tik.md — 259 paragraphs Sumaṅgalavilāsinī-ṭīkā (13,655 words)
        - an4_41_tik.md — 18 paragraphs Manorathapūraṇī-ṭīkā (996 words)

### 2. Sutta-Commentary-Subcommentary Cross-Linking
- [x] Cross-link MN 118 Mūla → Commentary → Tīkā:
      - `### §NNN` heading anchors added to mn118_att.md and mn118_tik.md (§144, 145, 146, 147, 149, 150, 152)
      - Collapsed `> [!info]- Commentary` callouts inserted in mn118.md at 7 key mūla passages
      - `> [!abstract]- Tīkā §NNN` links appended after each att paragraph block
      - Script: `scratch/crosslink_mn118.py` (reusable pattern for future suttas)

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
- [x] Dhammapada-aṭṭhakathā — 6 meditation chapters (2, 3, 7, 14, 20, 25): 61 origin stories, ~116K words; Bhante Ānandajoti (revised Burlingame). Files: `atthakatha/sutta/khuddaka_nikaya/dhammapada/*_att.md`
- [x] Dhammapada-aṭṭhakathā — remaining 20 chapters (233 more stories):
        - dhp_01_yamakavagga_att.md — 14 stories (52,410 words)
        - dhp_04_pupphavagga_att.md — 12 stories (37,953 words)
        - dhp_05_balavagga_att.md — 15 stories (30,954 words)
        - dhp_06_panditavagga_att.md — 10 stories (12,624 words)
        - dhp_08_sahassavagga_att.md — 14 stories (21,269 words)
        - dhp_09_papavagga_att.md — 12 stories (16,207 words)
        - dhp_10_dandavagga_att.md — 11 stories (16,947 words)
        - dhp_11_jaravagga_att.md — 9 stories (10,015 words)
        - dhp_12_attavagga_att.md — 10 stories (10,254 words)
        - dhp_13_lokavagga_att.md — 11 stories (14,524 words)
        - dhp_15_sukhavagga_att.md — 8 stories (5,623 words)
        - dhp_16_piyavagga_att.md — 9 stories (7,778 words)
        - dhp_17_kodhavagga_att.md — 8 stories (12,315 words)
        - dhp_18_malavagga_att.md — 12 stories (14,465 words)
        - dhp_19_dhammatthavagga_att.md — 10 stories (4,948 words)
        - dhp_21_pakinnakavagga_att.md — 9 stories (11,253 words)
        - dhp_22_nirayavagga_att.md — 9 stories (5,692 words)
        - dhp_23_nagavagga_att.md — 8 stories (8,050 words)
        - dhp_24_tanhavagga_att.md — 12 stories (13,836 words)
        - dhp_26_brahmanavagga_att.md — 40 stories (38,581 words)
        Script: `scratch/generate_dhammapada_att_remaining.py`
- [ ] Dhammapada Tīkā (sub-commentary)
- [ ] Cross-link vagga files to relevant mātikā entries

### 5. Next Meditation Sutta Tranche (Phase 2)

These high-value meditation suttas are the recommended next batch. All three layers
(mūla, atthakathā, tīkā) should be added per the established pipeline.

**Majjhima Nikāya — mindfulness & absorption:**
- [x] MN 36: Mahāsaccakasutta — mūla (9,139w), att (34¶+25 notes, 3,365w), tīkā (32¶, 1,364w)
- [x] MN 43: Mahāvedallasutta — mūla (3,877w), att (60¶+30 notes, 5,181w), tīkā (54¶, 4,322w)
- [x] MN 44: Cūḷavedallasutta — mūla (3,096w), att (39¶+27 notes, 4,209w), tīkā (40¶, 2,404w)
- [x] MN 52: Aṭṭhakanāgarasutta — mūla (1,696w), att (14¶+14 notes, 1,155w), tīkā (10¶, 528w)
- [x] MN 111: Anupadasutta — mūla (2,272w), att (26¶+18 notes, 2,415w), tīkā (38¶, 2,158w)
- [x] MN 118: Ānāpānasatisutta — mūla + att + tīkā complete; 7-point cross-links done (§144–152)

**Dīgha Nikāya — long discourses:**
- [x] DN 22: Mahāsatipaṭṭhānasutta — mūla (8,892w), att (293¶+78 notes, 14,411w), tīkā (236¶, 12,626w)
- [ ] DN 9: Poṭṭhapādasutta — consciousness, self, cessation of perception
- [ ] DN 15: Mahānidānasutta — dependent origination in detail

**Saṃyutta Nikāya — samādhi and bojjhaṅga:**
- [ ] SN 35 (Saḷāyatanasaṃyutta): selected suttas on the six sense bases
- [x] SN 46 (Bojjhaṅgasaṃyutta) — mūla (56 suttas, 23,919w), att (180¶, 6,062w), tīkā (175¶, 5,545w)
- [x] SN 54 (Ānāpānasaṃyutta) — mūla (20 suttas, 11,648w), att (45¶, 2,018w), tīkā (40¶, 1,393w)

**Aṅguttara Nikāya — numerical lists:**
- [x] AN 3.100 (Loṇakapallasutta) — mūla (1,681w), att (37¶, 1,480w), tīkā (12¶, 333w); Mātikā: seven_awakening_factors, noble_eightfold_path
- [x] AN 4.123–126 (Nānākaraṇasuttāni) — mūla (2,607w), att (22¶, 1,055w), tīkā (10¶, 136w); Mātikā: five_spiritual_faculties, noble_eightfold_path
- [x] AN 5.28 (Pañcaṅgikasutta) — mūla (2,312w), att (31¶, 1,239w), tīkā (35¶, 1,356w); Mātikā: noble_eightfold_path, five_hindrances
- [x] AN 9.36 (Jhānasutta) — mūla (2,177w), att (28¶, 1,249w), tīkā (11¶, 196w); Mātikā: seven_awakening_factors, noble_eightfold_path
- [x] AN 10.2–6 (Ānisaṃsasuttāni) — mūla (2,956w), att (16¶, 326w), tīkā (59¶, 3,062w); Mātikā: noble_eightfold_path, five_spiritual_faculties

### 6. Vinaya Piṭaka — Precepts Study
- [ ] Bhikkhu Pātimokkha (227 rules) — mūla layer: Pali + English (Bhikkhu Thanissaro)
- [ ] Bhikkhunī Pātimokkha (311 rules) — mūla layer
- [ ] Pātimokkha Atthakathā (Kaṅkhāvitaraṇī) — commentary layer
- [ ] Five Precepts (Pañcasīla) — cross-link to matika/five_precepts.md
- [ ] Eight Precepts (Aṭṭhasīla) — cross-link to matika/eight_precepts.md
- [ ] Vinaya INDEX files for Suttavibhaṅga, Khandhaka, Parivāra

### 7. Expansion of Other Nikāyas (Future Phases)
- [ ] **Dīgha Nikāya** — expand beyond DN 2; scaffold full INDEX with all 34 suttas
- [ ] **Saṃyutta Nikāya** — scaffold full INDEX (2,889 suttas in 56 saṃyuttas); priority: SN 12, 35 (SN 46 + 54 done)
- [ ] **Aṅguttara Nikāya** — scaffold full INDEX (2,308 suttas in 11 nipātas); priority: AN 4, 5, 9, 10
- [ ] **Khuddaka Nikāya** — beyond Dhammapada: Udāna, Itivuttaka, Sutta Nipāta, Thera/Therīgāthā
- [ ] **Abhidhamma Piṭaka** — Dhammasaṅgaṇī, Vibhaṅga (mātikā cross-links)

### 8. Abhidhamma & Mātikā Integration
- [ ] Add Abhidhammatthasaṅgaha mūla (English: Bhikkhu Bodhi's "Comprehensive Manual")
- [ ] Cross-link Five Aggregates mātikā to Abhidhamma Khandhavibhaṅga (deferred — awaiting Abhidhamma phase)
- [ ] Cross-link Dependent Origination mātikā to DN 15 and Paṭṭhāna (deferred — DN 15 not yet migrated)
- [x] Cross-link Seven Awakening Factors → sn46, mn10, dn22, mn118, an3_100, an9_36 (done)
- [x] Cross-link Noble Eightfold Path → dn22§4.5.4, mn118, an3_100, an4_123_126, an5_28, an9_36, an10_2_6 (done; MN 141 deferred — not yet migrated)

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
- [x] Link lists to corresponding canonical occurrences — Phase 1 complete (see below)
      - seven_awakening_factors → sn46, mn10§4.4, dn22§4.4, mn118, an3_100, an9_36
      - four_foundations_of_mindfulness → mn10, dn22, mn118, sn54
      - noble_eightfold_path → dn22§4.5.4, mn118, an3_100, an4_123_126, an5_28, an9_36, an10_2_6
      - five_hindrances → mn10§4.1, dn22§4.1, dn2§4.3.2.4, sn46, mn118, an5_28
      - five_spiritual_faculties → sn46, mn118, an4_123_126, an10_2_6
      - four_noble_truths → dn22§4.5, mn10§4.5, mn118
      - four_right_exertions → mn20, mn118
      - five_aggregates → mn10§4.2, dn22§4.2, mn43, mn118
      - Reverse (Mātikā:) lines added to: mn10, dn22, mn118, dn2, sn46, sn54, an3_100, an4_123_126, an5_28, an9_36, an10_2_6
- [ ] Continue linking as new suttas are added (dependent_origination → DN 15 when migrated; five_aggregates → Abhidhamma)

