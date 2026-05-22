# Project Tasks Checklist

This file tracks the roadmap and pending tasks for the Pali Canon Vault.
**Last updated**: 2026-05-22 (Claude Code session — SN 12, 22, 35, 56 completed)

---

## Recommended Next Order (for incoming agent)

Priority is based on: (1) meditation-practice relevance, (2) strong mātikā connections not yet filled, (3) CSCD files already confirmed available.

1. **SN 45 (Maggasaṃyutta)** — Noble Eightfold Path saṃyutta; CSCD `s0305a.att0.xml` (92KB) / `s0305t.tik0.xml` (93KB); mātikā: `noble_eightfold_path`
2. **SN 55 (Sotāpattisaṃyutta)** — Stream entry; CSCD `s0305a.att10.xml` (68KB) / `s0305t.tik10.xml` (55KB); adds stream-entry doctrinal coverage not yet in vault
3. **Udāna (KN)** — 80 short inspired utterances; available on SuttaCentral (`ud1.1`–`ud8.10`); Pali poetic, high density of key teachings; no CSCD needed for mūla
4. **Sutta Nipāta (KN)** — Classic early poetry: Metta Sutta (Snp 1.8), Rhinoceros (Snp 1.3), Aṭṭhakavagga; SuttaCentral `snp1.1`–`snp5.19`
5. **SN 48 (Indriyasaṃyutta)** — Five Spiritual Faculties as a saṃyutta; CSCD `s0305a.att3.xml` (73KB) / `s0305t.tik3.xml` (73KB); mātikā: `five_spiritual_faculties`
6. **DN expansion** — DN 16 (Mahāparinibbāna, large — 6 chapters), DN 21 (Sakkapañha), DN 1 (Brahmajāla); scripts already exist for DN layer generation
7. **AN expansion** — AN 7, 8, 11 nipātas have nothing; AN 1 (one-thing suttas, very short); consult `scratch/generate_an_mula.py` pattern
8. **Vinaya Piṭaka** — Bhikkhu Pātimokkha (227 rules); Bhikkhu Thanissaro translation freely available; cross-link to `matika/five_precepts.md`
9. **New mātikā lists** — Ten fetters (dasa saṃyojanā), seven purifications (satta visuddhi); would connect naturally to SN 55 (sotāpatti) and path material
10. **§-anchor cross-links** — paragraph-level mūla↔att↔tīkā for remaining suttas; pattern established in `scratch/crosslink_mn118.py`; 20+ suttas still lack this

---

## Completed Work

### Phase 1 — Core Meditation Suttas (all three layers)
- [x] MN 10: Satipaṭṭhānasutta — 5,721w / 362¶+49 notes / 232¶
- [x] MN 20: Vitakkasaṇṭhānasutta — 1,798w / 40¶+11 notes / 26¶
- [x] MN 119: Kāyagatāsatisutta — 4,967w / 10¶+18 notes / 8¶
- [x] MN 121: Cūḷasuññatasutta — 2,760w / 13¶+15 notes / 11¶
- [x] DN 2: Sāmaññaphalasutta — 17,701w / 394¶+141 notes / 259¶
- [x] AN 4.41: Samādhibhāvanāsutta — 745w / 15¶ / 18¶

### Phase 2 — Meditation Sutta Expansion (all three layers)
- [x] MN 36: Mahāsaccakasutta — 9,139w / 34¶+25 notes / 32¶
- [x] MN 43: Mahāvedallasutta — 3,877w / 60¶+30 notes / 54¶
- [x] MN 44: Cūḷavedallasutta — 3,096w / 39¶+27 notes / 40¶
- [x] MN 52: Aṭṭhakanāgarasutta — 1,696w / 14¶+14 notes / 10¶
- [x] MN 111: Anupadasutta — 2,272w / 26¶+18 notes / 38¶
- [x] MN 118: Ānāpānasatisutta — 3,522w / 18¶ / 16¶; §-anchors + callouts done
- [x] DN 9: Poṭṭhapādasutta — 8,837w / 57¶+67 notes / 72¶; §-anchors done
- [x] DN 15: Mahānidānasutta — 6,706w / 138¶+80 notes / 122¶; §-anchors done
- [x] DN 22: Mahāsatipaṭṭhānasutta — 8,892w / 293¶+78 notes / 236¶
- [x] AN 3.100: Loṇakapallasutta — 1,681w / 37¶ / 12¶
- [x] AN 4.123–126: Nānākaraṇasuttāni — 2,607w / 22¶ / 10¶
- [x] AN 5.28: Pañcaṅgikasutta — 2,312w / 31¶ / 35¶
- [x] AN 9.36: Jhānasutta — 2,177w / 28¶ / 11¶
- [x] AN 10.2–6: Ānisaṃsasuttāni — 2,956w / 16¶ / 59¶

### Phase 3 — SN Expansion (this session, 2026-05-22)
- [x] SN 12 (Nidānasaṃyutta) — 18 suttas (20,504w) / 475¶ (22,013w) / 463¶ (21,458w); Mātikā: dependent_origination, four_noble_truths
- [x] SN 22 (Khandhasaṃyutta) — 18 suttas (23,613w) / 400¶ (13,968w) / 408¶ (8,841w); Mātikā: five_aggregates, three_marks
- [x] SN 35 (Saḷāyatanasaṃyutta) — 23 suttas (10,082w) / 590¶ (20,030w) / 484¶ (10,316w); Mātikā: five_spiritual_faculties, dependent_origination
- [x] SN 46 (Bojjhaṅgasaṃyutta) — 56 suttas (23,919w) / 180¶ (6,062w) / 175¶ (5,545w); Mātikā: seven_awakening_factors
- [x] SN 47 (Satipaṭṭhānasaṃyutta) — 16 suttas (9,504w) / 220¶ (9,325w) / 149¶ (6,123w); §-anchors + callouts done; Mātikā: four_foundations_of_mindfulness
- [x] SN 54 (Ānāpānasaṃyutta) — 20 suttas (11,648w) / 45¶ (2,018w) / 40¶ (1,393w); Mātikā: four_foundations_of_mindfulness
- [x] SN 56 (Saccasaṃyutta) — 16 suttas (6,469w) / 153¶ (2,413w) / 100¶ (1,689w); Mātikā: four_noble_truths, noble_eightfold_path

### Dhammapada (Khuddaka Nikāya)
- [x] Mūla — all 26 vaggas (423 verses, ~17,600w); Bhikkhu Sujato translation
- [x] Atthakathā — all 26 chapters, 294 origin stories (~498K words); Ānandajoti/Burlingame
- [x] Mātikā cross-links — 6 vaggas linked: dhp_02, 10, 14, 17, 20, 24
- [ ] Ṭīkā — **BLOCKED**: `s0502t.tik*.xml` all 404 on tipitaka.org; CSCD does not publish the Dhammapada-ṭīkā online

### Vault Infrastructure
- [x] CSS translation toggle (`pali-translation-toggle.css`)
- [x] Simsapa DPD plugin (double-click Pali word lookup)
- [x] Dataview plugin
- [x] Templater plugin with translation toggle
- [x] Templates folder (mūla / atthakathā / tīkā sutta templates)
- [x] Git repository with `.gitignore`
- [x] Folder scaffolding for KN, Abhidhamma, Vinaya
- [x] Link validator (`scratch/validate_links.py`) — currently 124 files, 1,144 wikilinks, 0 errors

### Mātikā (16 lists — all complete)
- [x] four_noble_truths, noble_eightfold_path, three_marks, five_aggregates
- [x] dependent_origination, five_precepts, five_hindrances, seven_awakening_factors
- [x] four_foundations_of_mindfulness, eight_precepts, three_refuges, ten_perfections
- [x] four_sublime_states, five_spiritual_faculties, three_unwholesome_roots, four_right_exertions
- [x] All 16 lists cross-linked to canonical vault sources (reverse links in every sutta)

---

## Pending Work

### SN — Remaining High-Value Saṃyuttas
- [ ] **SN 45 (Maggasaṃyutta)** — CSCD: `s0305a.att0.xml` / `s0305t.tik0.xml` — **Recommended #1**
- [ ] **SN 55 (Sotāpattisaṃyutta)** — CSCD: `s0305a.att10.xml` / `s0305t.tik10.xml` — **Recommended #2**
- [ ] **SN 48 (Indriyasaṃyutta)** — CSCD: `s0305a.att3.xml` / `s0305t.tik3.xml` — **Recommended #5**
- [ ] SN 51 (Iddhipādasaṃyutta) — CSCD: `s0305a.att6.xml` / `s0305t.tik6.xml` — lower priority

### Khuddaka Nikāya — Beyond Dhammapada
- [ ] **Udāna** — 80 suttas; SuttaCentral IDs: `ud1.1`–`ud8.10`; no CSCD needed for mūla — **Recommended #4**
- [ ] **Sutta Nipāta** — SuttaCentral IDs: `snp1.1`–`snp5.19`; especially Snp 1.8 (Metta), 1.3 (Khaggavisāṇa) — **Recommended #5**
- [ ] Itivuttaka — SuttaCentral IDs: `iti1`–`iti112`
- [ ] Thera/Therīgāthā — short verses, SuttaCentral available

### Dīgha Nikāya — Expansion
- [ ] DN 16 (Mahāparinibbāna) — CSCD: `s0102a.att0.xml` (large, 6 chapters); important but big
- [ ] DN 21 (Sakkapañha) — CSCD: `s0102a.att4.xml` (approx)
- [ ] DN 1 (Brahmajāla) — 62 views on self and world; CSCD: `s0101a.att0.xml`

### Aṅguttara Nikāya — Expansion
- [ ] AN 1 (Ekakanipāta) — very short single-factor suttas; CSCD: `s0401a.att*.xml`
- [ ] AN 7, 8, 11 nipātas — no coverage yet; CSCD: `s0403a` / `s0404a` range
- [ ] Consult `scratch/generate_an_mula.py` for the established pattern

### Vinaya Piṭaka
- [ ] Bhikkhu Pātimokkha (227 rules) — Thanissaro translation; cross-link to `matika/five_precepts.md`
- [ ] Bhikkhunī Pātimokkha (311 rules)
- [ ] Kaṅkhāvitaraṇī (Pātimokkha commentary)
- [ ] Vinaya INDEX files for Suttavibhaṅga, Khandhaka, Parivāra

### Abhidhamma Piṭaka
- [ ] Abhidhammatthasaṅgaha mūla (Bhikkhu Bodhi's "Comprehensive Manual")
- [ ] Dhammasaṅgaṇī, Vibhaṅga (mātikā cross-links for five aggregates)

### Mātikā — New Lists to Add
- [ ] Ten fetters (dasa saṃyojanā) — connects to SN 55 / stream-entry material
- [ ] Seven purifications (satta visuddhi) — connects to MN 24 (Rathavinīta) if migrated
- [ ] Five powers (pañcabala) — parallel to five_spiritual_faculties

### Cross-linking — Paragraph Level
- [ ] §-anchor cross-links (mūla ↔ att ↔ ṭīkā) for 20+ suttas — pattern in `scratch/crosslink_mn118.py`
      Currently done: MN 118, DN 9, DN 15 only
      Candidates: MN 10, MN 36, DN 22, SN 46, all SN saṃyuttas

### Infrastructure
- [ ] Dataview query blocks in nikaya INDEX files for live sutta lists
- [ ] VRI XML parser script for batch commentary extraction
- [ ] Link validator maintenance as vault grows

