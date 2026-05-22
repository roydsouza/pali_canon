# Pali Canon Vault Status

This document captures the current status of the Pali Canon Obsidian Vault migration, cataloging what has been completed, what is in progress, and overall progress metrics.

## Overall Progress Metrics

| Layer | Suttas Complete | Nikāyas Active | Notes |
|---|---|---|---|
| **Mūla (Root Texts)** | 104 individual suttas | MN, DN, SN, AN, KN | Interleaved Pali/English (Sujato) |
| **Aṭṭhakathā (Commentaries)** | 104 individual suttas + 26 DhpA chapters | MN, DN, SN, AN, KN | CSCD Pali + Sujato notes |
| **Ṭīkā (Sub-commentaries)** | 104 individual suttas | MN, DN, SN, AN | CSCD Pali |
| **Mātikā (Doctrinal Lists)** | 16 lists | — | Pali/English, cross-linked |

---

## Migrated Texts Catalog

### Majjhima Nikāya (Middle Discourses) — 10 suttas

| Sutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| MN 10 Satipaṭṭhānasutta | ✅ 5,721w | ✅ 362¶ + 49 notes | ✅ 232¶ | Mātikā |
| MN 20 Vitakkasaṇṭhānasutta | ✅ 1,798w | ✅ 40¶ + 11 notes | ✅ 26¶ | Mātikā |
| MN 36 Mahāsaccakasutta | ✅ 9,139w | ✅ 34¶ + 25 notes | ✅ 32¶ | — |
| MN 43 Mahāvedallasutta | ✅ 3,877w | ✅ 60¶ + 30 notes | ✅ 54¶ | — |
| MN 44 Cūḷavedallasutta | ✅ 3,096w | ✅ 39¶ + 27 notes | ✅ 40¶ | — |
| MN 52 Aṭṭhakanāgarasutta | ✅ 1,696w | ✅ 14¶ + 14 notes | ✅ 10¶ | — |
| MN 111 Anupadasutta | ✅ 2,272w | ✅ 26¶ + 18 notes | ✅ 38¶ | — |
| MN 118 Ānāpānasatisutta | ✅ 3,522w | ✅ 18¶ | ✅ 16¶ | ✅ Full §-anchors |
| MN 119 Kāyagatāsatisutta | ✅ 4,967w | ✅ 10¶ + 18 notes | ✅ 8¶ | — |
| MN 121 Cūḷasuññatasutta | ✅ 2,760w | ✅ 13¶ + 15 notes | ✅ 11¶ | — |

### Dīgha Nikāya (Long Discourses) — 4 suttas

| Sutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| DN 2 Sāmaññaphalasutta | ✅ 17,701w | ✅ 394¶ + 141 notes | ✅ 259¶ | Mātikā |
| DN 9 Poṭṭhapādasutta | ✅ 8,837w | ✅ 57¶ + 67 notes | ✅ 72¶ | ✅ Full §-anchors & Mātikā |
| DN 15 Mahānidānasutta | ✅ 6,706w | ✅ 138¶ + 80 notes | ✅ 122¶ | ✅ Full §-anchors & Mātikā |
| DN 22 Mahāsatipaṭṭhānasutta | ✅ 8,892w | ✅ 293¶ + 78 notes | ✅ 236¶ | Mātikā |

### Saṃyutta Nikāya (Connected Discourses) — 76 suttas (2 saṃyuttas)

| Saṃyutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| SN 46 Bojjhaṅgasaṃyutta (56 suttas) | ✅ 23,919w | ✅ 180¶ | ✅ 175¶ | Mātikā |
| SN 54 Ānāpānasaṃyutta (20 suttas) | ✅ 11,648w | ✅ 45¶ | ✅ 40¶ | Mātikā |

### Aṅguttara Nikāya (Numerical Discourses) — 14 suttas

| Sutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| AN 3.100 Loṇakapallasutta | ✅ 1,681w | ✅ 37¶ | ✅ 12¶ | Mātikā |
| AN 4.41 Samādhibhāvanāsutta | ✅ 745w | ✅ 15¶ | ✅ 18¶ | — |
| AN 4.123–126 Nānākaraṇasuttāni (4) | ✅ 2,607w | ✅ 22¶ | ✅ 10¶ | Mātikā |
| AN 5.28 Pañcaṅgikasutta | ✅ 2,312w | ✅ 31¶ | ✅ 35¶ | Mātikā |
| AN 9.36 Jhānasutta | ✅ 2,177w | ✅ 28¶ | ✅ 11¶ | Mātikā |
| AN 10.2–6 Ānisaṃsasuttāni (5) | ✅ 2,956w | ✅ 16¶ | ✅ 59¶ | Mātikā |

### Khuddaka Nikāya — Dhammapada

| Component | Status | Details |
|---|---|---|
| Mūla (26 vaggas, 423 verses) | ✅ ~17,600w | Sujato translation |
| Aṭṭhakathā (26 chapters) | ✅ ~498,000w | 294 origin stories (Ānandajoti/Burlingame) |
| Ṭīkā | ❌ Not started | — |

---

## Vault Infrastructure Status

*   **Vault Index**: [INDEX.md](file:///Users/rds/pali_canon/INDEX.md) (Operational)
*   **Obsidian Plugins**: Simsapa DPD, Dataview, Templater (all configured)
*   **CSS Toggle**: Translation toggle for pure Pali reading
*   **Templates**: Mūla, Atthakathā, Tīkā sutta templates
*   **Git**: Local repository initialized (no remote)
*   **Scripts**: 17 reusable Python scripts in `scratch/`

---

## Mātikā (Buddhist Lists)

*   **Mātika Index**: [matika/INDEX.md](file:///Users/rds/pali_canon/matika/INDEX.md)
    *   *Status*: **Completed** (16 lists total, cross-linked to canonical sources).
*   **Migrated Lists**:
    *   [[four_noble_truths|Four Noble Truths (Cattāri Ariyasaccāni)]]
    *   [[noble_eightfold_path|Noble Eightfold Path (Ariyo Aṭṭhaṅgiko Maggo)]]
    *   [[three_marks|Three Marks of Existence (Tilakkhaṇa)]]
    *   [[five_aggregates|Five Aggregates (Pañcupādānakkhandhā)]]
    *   [[dependent_origination|Dependent Origination (Paṭiccasamuppāda)]]
    *   [[five_precepts|Five Precepts (Pañcasīla)]]
    *   [[five_hindrances|Five Hindrances (Pañca Nīvaraṇāni)]]
    *   [[seven_awakening_factors|Seven Awakening Factors (Satta Bojjhaṅgā)]]
    *   [[four_foundations_of_mindfulness|Four Foundations of Mindfulness (Cattāro Satipaṭṭhānā)]]
    *   [[eight_precepts|Eight Precepts (Aṭṭhaṅgasīla)]]
    *   [[three_refuges|Three Refuges (Tisarana / Tiratana)]]
    *   [[ten_perfections|Ten Perfections (Dasa Pāramī)]]
    *   [[four_sublime_states|Four Sublime States (Cattāro Brahmavihārā)]]
    *   [[five_spiritual_faculties|Five Spiritual Faculties (Pañcindriya)]]
    *   [[three_unwholesome_roots|Three Unwholesome Roots (Akusalamūla)]]
    *   [[four_right_exertions|Four Right Exertions (Cattāro Sammappadhānā)]]
