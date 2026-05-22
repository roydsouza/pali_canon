# Sync Log

This log tracks sync states and key technical context for agent pairs working on the Pali Canon Vault.

## [2026-05-21 23:00:00-07:00] - AN Batch: 5 Suttas All Three Layers + Mātikā Phase 2 (Claude Code)

### Accomplishments
- **AN mūla layer** — 5 files in `mula/sutta/anguttara_nikaya/`:
  - `an3_100.md` — Loṇakapallasutta (1,681w)
  - `an4_123_126.md` — Nānākaraṇasuttāni, 4 suttas grouped (2,607w)
  - `an5_28.md` — Pañcaṅgikasutta (2,312w)
  - `an9_36.md` — Jhānasutta (2,177w)
  - `an10_2_6.md` — Ānisaṃsasuttāni, 5 suttas grouped (2,956w — complete after SSL retry)
- **AN atthakathā layer** — 5 files in `atthakatha/sutta/anguttara_nikaya/`:
  - an3_100_att (37¶, 1,480w) · an4_123_126_att (22¶, 1,055w) · an5_28_att (31¶, 1,239w)
  - an9_36_att (28¶, 1,249w) · an10_2_6_att (16¶, 326w)
- **AN tīkā layer** — 5 files in `tika/sutta/anguttara_nikaya/`:
  - an3_100_tik (12¶, 333w) · an4_123_126_tik (10¶, 136w) · an5_28_tik (35¶, 1,356w)
  - an9_36_tik (11¶, 196w) · an10_2_6_tik (59¶, 3,062w)
- **CSCD file mapping** (non-obvious — discovered by probing):
  - `s0402a` spans AN 2+3+4 (att0-63), `s0403a` spans AN 5 (att0-15+), `s0404a` spans AN 8+9+10
  - Tīkā numbering mirrors att exactly (s040Xt.tikN = s040Xa.attN)
  - Specific mappings: an3_100→att28, an4_123_126→att48, an5_28→att2, an9_36→att13, an10_2_6→att15
- **Mātikā Phase 2** — 4 concept files updated + 5 sutta files with `**Mātikā**:` lines:
  - `seven_awakening_factors.md` += an3_100, an9_36
  - `noble_eightfold_path.md` += an3_100, an4_123_126, an5_28, an9_36, an10_2_6
  - `five_spiritual_faculties.md` += an4_123_126, an10_2_6
  - `five_hindrances.md` += an5_28
  - Reverse lines: an3_100 (seven_awakening_factors · noble_eightfold_path), an4_123_126 (five_spiritual_faculties · noble_eightfold_path), an5_28 (noble_eightfold_path · five_hindrances), an9_36 (seven_awakening_factors · noble_eightfold_path), an10_2_6 (noble_eightfold_path · five_spiritual_faculties)
- **Scripts**: `generate_an_mula.py`, `generate_an_att.py`, `generate_an_tik.py` in `scratch/`

### Technical Note
- AN title extraction bug: AN has 3 metadata keys per sutta (`:0.1` nikāya, `:0.2` vagga, `:0.3` sutta title) vs MN/SN which have 2. Script fixed to prefer `:0.3` with `:0.2` fallback.
- an10.3-6 experienced SSL timeout on first mūla re-run; second re-run succeeded cleanly.

### Current State
- AN 3.100, 4.123–126, 5.28, 9.36, 10.2–6 — all three layers complete, mātikā cross-linked.
- TASKS.md updated: AN batch items marked `[x]`, mātikā inventory updated.
- Next candidates (TASKS.md §5): DN 9, DN 15, SN 35.

## [2026-05-21 22:15:00-07:00] - Mātikā Cross-Links Phase 1 (Claude Code)

### Accomplishments
- **8 mātikā files updated** with canonical sutta references (concept → text direction):
  - `seven_awakening_factors.md` → sn46, mn10§4.4, dn22§4.4, mn118
  - `four_foundations_of_mindfulness.md` → mn10, dn22, mn118, sn54
  - `noble_eightfold_path.md` → dn22§4.5.4, mn118
  - `five_hindrances.md` → mn10§4.1, dn22§4.1, dn2§4.3.2.4, sn46, mn118
  - `five_spiritual_faculties.md` → sn46, mn118
  - `four_noble_truths.md` → dn22§4.5, mn10§4.5, mn118
  - `four_right_exertions.md` → mn20, mn118
  - `five_aggregates.md` → mn10§4.2, dn22§4.2, mn43, mn118
- **6 sutta files updated** with `**Mātikā**:` reverse-link lines (text → concept direction):
  - mn10, dn22, mn118, dn2, sn46, sn54
- All links use heading anchors (e.g., `[[mn10#4.4. The Awakening Factors|...]]`) for direct section navigation
- Also added `**Related Texts**:` lines to mn10 and dn2 (were missing from Phase 1 generation)

### Current State
- Mātikā ↔ sutta web is now connected for all 8 lists that have canonical source suttas in the vault
- Deferred: `dependent_origination.md` → DN 15 (not yet migrated); `five_aggregates.md` → Abhidhamma (future phase)
- TASKS.md mātikā item marked complete

## [2026-05-21 21:30:00-07:00] - SN 46 + SN 54: All Three Layers (Claude Code)

### Accomplishments
- **Saṃyutta Nikāya scaffolded**: new directories in `mula/sutta/samyutta_nikaya/`, `atthakatha/sutta/samyutta_nikaya/`, `tika/sutta/samyutta_nikaya/`
- **SN 46 Bojjhaṅgasaṃyutta** — mūla (56 suttas combined, 23,919w), att (180¶, 6,062w), tīkā (175¶, 5,545w)
- **SN 54 Ānāpānasaṃyutta** — mūla (20 suttas combined, 11,648w), att (45¶, 2,018w), tīkā (40¶, 1,393w)
- Each saṃyutta is one combined file (one file per saṃyutta, each individual sutta as `## SN NN.N:` heading)
- **CSCD file mapping** for SN Mahāvagga: `s0305a.att{N}.xml` / `s0305t.tik{N}.xml` where N=0 → SN 45, N=1 → SN 46, …, N=9 → SN 54
- **Scripts**: `generate_sn_mula.py`, `generate_sn_att.py`, `generate_sn_tik.py`
- All index files updated (mūla/att/tīkā for samyutta_nikaya)
- TASKS.md updated: SN 46 + SN 54 marked complete

### Current State
- SN 46 + SN 54 complete. Cross-links (mūla ↔ att ↔ tīkā) not yet done — awaiting further instruction.
- Next candidates (per TASKS.md): DN 9, DN 15; AN 3.100, AN 4.123–126, AN 5.28, AN 9.36, AN 10.2–6; SN 35.

## [2026-05-21 20:45:00-07:00] - Phase 2 Meditation Suttas: All Three Layers (Claude Code)

### Accomplishments
- **6 Phase 2 suttas** — mūla + atthakathā + tīkā for MN 36, 43, 44, 52, 111 and DN 22:

| Sutta | Mūla | Att (¶+notes) | Tīkā (¶) |
|---|---|---|---|
| MN 36 Mahāsaccakasutta | 9,139w | 34¶+25 notes, 3,365w | 32¶, 1,364w |
| MN 43 Mahāvedallasutta | 3,877w | 60¶+30 notes, 5,181w | 54¶, 4,322w |
| MN 44 Cūḷavedallasutta | 3,096w | 39¶+27 notes, 4,209w | 40¶, 2,404w |
| MN 52 Aṭṭhakanāgarasutta | 1,696w | 14¶+14 notes, 1,155w | 10¶, 528w |
| MN 111 Anupadasutta | 2,272w | 26¶+18 notes, 2,415w | 38¶, 2,158w |
| DN 22 Mahāsatipaṭṭhānasutta | 8,892w | 293¶+78 notes, 14,411w | 236¶, 12,626w |

- **Key discovery**: Gahapativagga att (`s0202a.att0.xml`) and tīkā (`s0202t.tik0.xml`) exist on tipitaka.org but NOT in the siongui/tipitaka-romn GitHub repo — file probing logic now in phase2 scripts
- **CSCD file mapping for DN Mahāvagga**: att8 and tik8 are dedicated DN 22 files
- **Scripts**: `generate_phase2_mula.py`, `generate_phase2_att.py`, `generate_phase2_tik.py`
- Index files updated: MN, DN mūla/att/tīkā indexes

### Current State
- Phase 2 MN + DN 22 complete. SN and AN expansion deferred (requires new scaffolding).
- Next candidates: DN 9, DN 15; or SN 46, SN 54 (bojjhaṅga/ānāpāna saṃyuttas).

## [2026-05-21 19:30:00-07:00] - MN 118 Cross-Links + DhpA Complete (Claude Code)

### Accomplishments

**MN 118 Cross-linking** (`scratch/crosslink_mn118.py`):
- `### §NNN` heading anchors inserted in mn118_att.md and mn118_tik.md at 7 paragraphs (§144, 145, 146, 147, 149, 150, 152)
- Collapsed `> [!info]- Commentary` callouts inserted in mn118.md at 7 key mūla passages, linking to both att and tik anchors
- `> [!abstract]- Tīkā §NNN` links appended after each att paragraph block → direct cross-navigation att↔tik
- Pattern is reusable: same script structure works for any future three-layer sutta

**Dhammapada-aṭṭhakathā — all 26 vaggas complete** (`scratch/generate_dhammapada_att_remaining.py`):
- 20 remaining vaggas fetched from ancient-buddhist-texts.net (Bhante Ānandajoti/Burlingame)
- **233 new stories** across 20 chapters; ~382K words
- Grand total DhpA: **294 origin stories**, ~498K words across all 26 vaggas
- Notable: Ch 1 (Yamaka) 14 stories 52K words; Ch 26 (Brāhmaṇa) 40 stories 38K words
- INDEX.md updated with all 26 chapters in sorted order with word counts
- Source stopped gracefully at 3 consecutive 404s per chapter

### Current State
- Dhammapada commentary layer: **complete** (all 26 vaggas with origin stories)
- Dhammapada tīkā: not yet done
- Dhammapada vagga→mātikā cross-links: not yet done
- Next high-priority: Phase 2 meditation sutta tranche (MN 36, 43, 44, 52, 111; DN 15, 22; SN 46, 54)

## [2026-05-21 18:15:00-07:00] - Meditation Suttas Tīkā Layer (Claude Code)

### Accomplishments
- **6 tīkā (sub-commentary) files** generated from tipitaka.org CSCD (UTF-16 XML):
  - `tika/sutta/majjhima_nikaya/mn10_tik.md` — Papañcasūdanī-ṭīkā, 232 ¶, **11,365 words**
  - `tika/sutta/majjhima_nikaya/mn20_tik.md` — 26 ¶, **1,006 words**
  - `tika/sutta/majjhima_nikaya/mn119_tik.md` — 8 ¶, **358 words**
  - `tika/sutta/majjhima_nikaya/mn121_tik.md` — 11 ¶, **589 words**
  - `tika/sutta/digha_nikaya/dn2_tik.md` — Sumaṅgalavilāsinī-ṭīkā, 259 ¶, **13,655 words**
  - `tika/sutta/anguttara_nikaya/an4_41_tik.md` — Manorathapūraṇī-ṭīkā, 18 ¶, **996 words**
- **Format**: YAML frontmatter → navigation (links to mūla + atthakathā) → Pali tīkā text with `(N)` paragraph numbers
- **Source discovery**: GitHub/siongui/tipitaka-romn has no sutta tīkā; tipitaka.org/romn/cscd/ has full set `s{NNNN}t.tik{N}.xml`
- **Section extraction**: same regex heading approach as atthakathā; stop_pat catches next sutta/vagga boundary
- **Tīkā file mapping**:
  - MN Mūlapaṇṇāsa: `s0201t.tik1.xml` (MN 1-10), `s0201t.tik2.xml` (MN 11-20)
  - MN Uparipaṇṇāsa: `s0203t.tik1.xml` (Anupadavagga/MN 111-120), `s0203t.tik2.xml` (Suññatavagga/MN 121-130)
  - DN 2: `s0101t.tik2.xml` (entire dedicated file)
  - AN 4.41: `s0402t.tik4.xml` (entire Parisavagga tīkā)
- **Index files**: `tika/sutta/INDEX.md`, `tika/sutta/{nikaya}/INDEX.md` created with word-count rows
- **Script**: `scratch/generate_meditation_tik.py` — reusable for future suttas
- **TASKS.md**: tīkā subtask marked complete; comprehensive future roadmap added (Phase 2 suttas, Vinaya, full nikāya expansion, Abhidhamma integration)

### Current State
- All 6 meditation suttas now have **three complete layers**: mūla + atthakathā + tīkā.
- Remaining high-priority work: MN 118 cross-links (mūla↔att↔tīkā), remaining 20 DhpA chapters,
  Phase 2 sutta tranche (MN 36, 43, 44, 52, 111; DN 9, 15, 22; SN 35, 46, 54; AN key suttas).

## [2026-05-21 17:30:00-07:00] - Meditation Suttas Atthakathā Layer (Claude Code)

### Accomplishments
- **6 atthakathā (commentary) files** generated for key meditation suttas, combining two sources:
  1. **Pali commentary text** — CSCD (Chattha Sangayana Tipitaka) XML from siongui/tipitaka-romn on GitHub; UTF-16 decoded, paragraphs numbered, bold terms preserved
  2. **Translator's notes** — Bhikkhu Sujato's segment annotations from SuttaCentral `/comment` API
- **Files** in `atthakatha/sutta/{nikaya}/`:
  - `mn10_att.md` — Papañcasūdanī, 362 ¶, 49 Sujato notes, **15,912 words**
  - `mn20_att.md` — Papañcasūdanī, 40 ¶, 11 notes, **2,159 words**
  - `mn119_att.md` — Papañcasūdanī, 10 ¶, 18 notes, **1,181 words**
  - `mn121_att.md` — Papañcasūdanī, 13 ¶, 15 notes, **1,476 words**
  - `dn2_att.md` — Sumaṅgalavilāsinī, 394 ¶, 141 notes, **22,452 words**
  - `an4_41_att.md` — Manorathapūraṇī, 15 ¶, 0 notes, **952 words**
- **Format**: YAML frontmatter → Translator's Notes section → `---` → Pali commentary with `(N)` paragraph numbers and `**bold**` key terms
- **Index files updated**: MN, DN, AN atthakathā indexes with word counts and sources
- **Fetch script**: `scratch/generate_meditation_att.py` — reusable for future suttas

### Current State
- All 6 meditation sutta mūla + atthakathā layers complete.
- Sub-commentary (tīkā) layer not yet added. CSCD tīkā files follow same `*.tik*.xml` naming pattern.
- Next: tīkā layer, or other phases (remaining DhpA chapters, MN expansion, etc.)

## [2026-05-21 16:30:00-07:00] - Meditation Suttas Mūla Layer (Claude Code)

### Accomplishments
- **6 key meditation suttas** fetched from SuttaCentral (Sujato translation) and generated as interleaved Pali/English mūla files:
  - `mula/sutta/majjhima_nikaya/mn10.md` — Satipaṭṭhānasutta, 5,721 words
  - `mula/sutta/majjhima_nikaya/mn20.md` — Vitakkasaṇṭhānasutta, 1,798 words
  - `mula/sutta/majjhima_nikaya/mn119.md` — Kāyagatāsatisutta, 4,967 words
  - `mula/sutta/majjhima_nikaya/mn121.md` — Cūḷasuññatasutta, 2,760 words
  - `mula/sutta/digha_nikaya/dn2.md` — Sāmaññaphalasutta, 17,701 words
  - `mula/sutta/anguttara_nikaya/an4_41.md` — Samādhibhāvanāsutta, 745 words
- **New nikāya directories** scaffolded with INDEX.md: `digha_nikaya` and `anguttara_nikaya` (all three layers: mula/atthakatha/tika)
- **Format**: YAML frontmatter, `## Section` / `### Sub-section` headings for structural divisions (Pali + English), interleaved `**Pali**` / `*English*` body segments
- **Index files updated**: MN, DN, AN mula indexes + `mula/sutta/INDEX.md`
- **Fetch script**: `scratch/generate_meditation_suttas.py` — reusable for future suttas

### Current State
- All 6 meditation sutta mūla files complete. Commentary (Papañcasūdanī / Sumaṅgalavilāsinī / Manorathapūraṇī) and sub-commentary not yet added.
- Next: commentary layer for these suttas, or continue expanding other phases.

## [2026-05-21 16:05:00-07:00] - Dhammapada Atthakathā — Meditation Chapters (Claude Code)

### Accomplishments
- **Dhammapada-aṭṭhakathā (6 meditation chapters)**: Fetched and generated commentary files from ancient-buddhist-texts.net (Bhante Ānandajoti's revised Burlingame translation). 61 HTML pages fetched across 6 chapters.
- **Files generated** in `atthakatha/sutta/khuddaka_nikaya/dhammapada/`:
  - `dhp_02_appamadavagga_att.md` — 9 stories, ~41,004 words (Heedfulness)
  - `dhp_03_cittavagga_att.md` — 9 stories, ~14,290 words (The Mind)
  - `dhp_07_arahantavagga_att.md` — 10 stories, ~10,384 words (The Arahant)
  - `dhp_14_buddhavagga_att.md` — 9 stories, ~21,573 words (The Buddha)
  - `dhp_20_maggavagga_att.md` — 12 stories, ~10,085 words (The Path)
  - `dhp_25_bhikkhuvagga_att.md` — 12 stories, ~18,494 words (The Monk)
  - `INDEX.md` — chapter listing with wikilinks
- **Format**: Each story has heading (`### N.M Title (*vatthu*)`), verse cross-links to mula files, metadata (Burlingame ref/Compare/Cast/Keywords), narrative prose, verse quote (blockquote with Pali bold + English italic), and closing note.
- **Fetch script**: `scratch/generate_dhammapada_att.py` — reusable for remaining 20 chapters.

### Current State
- All 6 meditation-chapter commentaries complete (~116K words total, 61 origin stories).
- Cross-links from commentary to mūla verse anchors are present (e.g., `[[dhp_07_arahantavagga#90|Dhp 90]]`).
- Remaining Dhammapada-aṭṭhakathā work: 20 non-meditation chapters (can reuse same script with expanded CHAPTERS list).
- Next: MN expansion (MN 10, MN 20, etc.) or remaining DhpA chapters.

## [2026-05-21 14:30:00-07:00] - Dhammapada Mūla Complete (Claude Code)

### Accomplishments
- **Dhammapada mūla**: All 26 vaggas (423 verses, ~17,600 words) fetched from SuttaCentral API and generated as interleaved Pali/English files. Bhikkhu Sujato translation.
- **Files**: `mula/sutta/khuddaka_nikaya/dhammapada/dhp_01_yamakavagga.md` through `dhp_26_brahmanavagga.md` + `INDEX.md`.
- **Format**: Each verse has verse number, optional vatthu (origin story name) as italic subhead, then Pali (bold) / English (italic) line pairs. Vagga-end colophons preserved from canonical tradition.
- **Tags**: Meditation-focused chapters (2, 3, 7, 14, 20, 25) tagged `meditation`; ethics/precepts chapters (1, 9, 10, 17, 18, 19) tagged `precepts`.
- **Fetch script**: `scratch/generate_dhammapada.py` — reusable for re-fetching or adapting to other Khuddaka texts.
- **Khuddaka INDEX**: Updated to list Dhammapada as complete.

### Current State
- Dhammapada mūla layer is complete. Commentary (Dhammapada-aṭṭhakathā) and sub-commentary not yet added.
- Next: Dhammapada commentary (origin stories), then Abhidhamma or MN expansion.

## [2026-05-21 14:00:00-07:00] - Templater Translation Toggle (Claude Code)

### Accomplishments
- **Templater plugin** (v2.20.5) installed and configured. `enabled_templates_hotkeys` in `data.json` registers the command `Templater: Insert toggle_translations` as a hotkey-assignable Obsidian command.
- **Toggle template** at `templates/toggle_translations.md` — executes JS to flip the `pali-translation-toggle` CSS snippet on/off with no content inserted into the active note.
- **Hotkey**: user assigns via Settings → Hotkeys → search `toggle` → `Templater: Insert toggle_translations`.
- **`.gitignore`** updated: Templater's `data.json` is now tracked (holds hotkey config); other plugins' `data.json` remain ignored.

### Current State
- Full infrastructure is operational: Simsapa DPD lookup, Dataview, translation toggle, git, templates, and folder scaffolding for all three piṭakas.

## [2026-05-21 13:30:00-07:00] - Vault Infrastructure Overhaul (Claude Code)

### Accomplishments
- **Simsapa DPD Integration**: Installed Simsapa Dhamma Reader (v0.5.2-alpha.1, arm64) to `/Applications` and Simsapa Obsidian plugin (v0.5.0) to `.obsidian/plugins/simsapa/`. Double-click any Pali word in Obsidian to trigger a DPD lookup window.
- **Dataview Plugin**: Installed Dataview (v0.5.70) to `.obsidian/plugins/dataview/`. Enables SQL-like queries over vault metadata directly in notes.
- **CSS Translation Toggle**: Created `.obsidian/snippets/pali-translation-toggle.css`. Enable in Settings → Appearance → CSS Snippets to hide all English translations and read pure Pali. Assign to a hotkey via Settings → Hotkeys → "Toggle CSS snippet: pali-translation-toggle".
- **Git Repository**: Initialized git repo at vault root with `.gitignore` (excludes workspace.json, plugin data.json, .DS_Store).
- **Templates**: Created `templates/` folder with three starter templates: `mula_sutta.md`, `atthakatha_sutta.md`, `tika_sutta.md`. Configure via Settings → Templates → Template folder location → `templates`.
- **Folder Scaffolding**:
  - `mula/sutta/khuddaka_nikaya/` — ready for Dhammapada and other Khuddaka texts
  - `mula/abhidhamma/`, `atthakatha/abhidhamma/`, `tika/abhidhamma/` — ready for Abhidhamma Piṭaka
  - `mula/vinaya/`, `atthakatha/vinaya/`, `tika/vinaya/` — ready for Vinaya Piṭaka (precepts study)
- **INDEX updates**: Root INDEX.md updated to reflect new pitaka scaffolding.
- **Initial git commit**: Full vault snapshot committed.

### Current State
- Vault has Simsapa DPD lookup (double-click), Dataview queries, translation toggle CSS, and folder structure for all three piṭakas.
- Two one-time manual steps remain in Obsidian: (1) enable Dataview in Community plugins, (2) set Templates folder to `templates` in core Templates plugin settings.

## [2026-05-21 11:00:00-07:00] - Additional Mātika (Buddhist Lists) Expanded

### Accomplishments
- **Expanded Lists**: Generated 7 additional practice-oriented and ethical Buddhist lists with Romanized Pali and item-by-item English translations:
  - [eight_precepts.md](file:///Users/rds/pali_canon/matika/eight_precepts.md) (*Aṭṭhaṅgasīla*)
  - [three_refuges.md](file:///Users/rds/pali_canon/matika/three_refuges.md) (*Tisarana*)
  - [ten_perfections.md](file:///Users/rds/pali_canon/matika/ten_perfections.md) (*Dasa Pāramī*)
  - [four_sublime_states.md](file:///Users/rds/pali_canon/matika/four_sublime_states.md) (*Cattāro Brahmavihārā*)
  - [five_spiritual_faculties.md](file:///Users/rds/pali_canon/matika/five_spiritual_faculties.md) (*Pañcindriya*)
  - [three_unwholesome_roots.md](file:///Users/rds/pali_canon/matika/three_unwholesome_roots.md) (*Akusalamūla*)
  - [four_right_exertions.md](file:///Users/rds/pali_canon/matika/four_right_exertions.md) (*Cattāro Sammappadhānā*)
- **Cross-linking & Validation**: Fully integrated these files with navigation paths, related lists, and references. Verified vault-wide integrity via the wikilink validator (68 total files validated successfully, 0 broken links).
- **Index & Status Sync**: Updated [matika/INDEX.md](file:///Users/rds/pali_canon/matika/INDEX.md), root [INDEX.md](file:///Users/rds/pali_canon/INDEX.md), [STATUS.md](file:///Users/rds/pali_canon/STATUS.md), and [TASKS.md](file:///Users/rds/pali_canon/TASKS.md) to register all 16 active lists.

### Current State
- The Mātika branch contains 16 highly structured lists, fully translated and cross-referenced.
- Link validation is completely clean.

## [2026-05-21 10:55:00-07:00] - Mātika (Buddhist Lists) Creation Complete

### Accomplishments
- **Mātika Directory & Index**: Created the `/Users/rds/pali_canon/matika/` directory and [matika/INDEX.md](file:///Users/rds/pali_canon/matika/INDEX.md) to serve as the master catalog for Buddhist lists.
- **Lists Generation**: Created 9 core Buddhist lists with Romanized Pali and item-by-item English translations, complete with navigation headers and standard YAML metadata:
  - [four_noble_truths.md](file:///Users/rds/pali_canon/matika/four_noble_truths.md) (*Cattāri Ariyasaccāni*)
  - [noble_eightfold_path.md](file:///Users/rds/pali_canon/matika/noble_eightfold_path.md) (*Ariyo Aṭṭhaṅgiko Maggo*)
  - [three_marks.md](file:///Users/rds/pali_canon/matika/three_marks.md) (*Tilakkhaṇa*)
  - [five_aggregates.md](file:///Users/rds/pali_canon/matika/five_aggregates.md) (*Pañcupādānakkhandhā*)
  - [dependent_origination.md](file:///Users/rds/pali_canon/matika/dependent_origination.md) (*Paṭiccasamuppāda*)
  - [five_precepts.md](file:///Users/rds/pali_canon/matika/five_precepts.md) (*Pañcasīla*)
  - [five_hindrances.md](file:///Users/rds/pali_canon/matika/five_hindrances.md) (*Pañca Nīvaraṇāni*)
  - [seven_awakening_factors.md](file:///Users/rds/pali_canon/matika/seven_awakening_factors.md) (*Satta Bojjhaṅgā*)
  - [four_foundations_of_mindfulness.md](file:///Users/rds/pali_canon/matika/four_foundations_of_mindfulness.md) (*Cattāro Satipaṭṭhānā*)
- **Cross-linking & Validation**: Linked all lists with relevant dependencies and to their occurrences/discussions in Majjhima Nikāya 118. Executed the wikilink validator verifying vault integrity.
- **Index and Status Updates**: Updated root [INDEX.md](file:///Users/rds/pali_canon/INDEX.md), [STATUS.md](file:///Users/rds/pali_canon/STATUS.md), and [TASKS.md](file:///Users/rds/pali_canon/TASKS.md) to integrate the new Mātika branch.

### Current State
- The vault is fully updated with the Mātika branch, including all 9 core lists mapped out, fully translated, and linked.
- Link validation returns no broken links.
- Future tasks involve linking these lists to new suttas as they are added, and expanding commentaries/sub-commentaries.

## [2026-05-21 10:46:52-07:00] - MN 118 Interleaving Complete & Vault Tracking Initiated

### Accomplishments
- **Mūla Interleaving**: Interleaved the Romanized Pali of the Ānāpānasati Sutta ([mn118.md](file:///Users/rds/pali_canon/mula/sutta/majjhima_nikaya/mn118.md)) with Bhikkhu Sujato's segment-by-segment English translation.
- **Commentary Translation**: Translated the 18 paragraphs of the Papañcasūdanī commentary on MN 118 and interleaved them sentence-by-sentence with the original Pali ([mn118_att.md](file:///Users/rds/pali_canon/atthakatha/sutta/majjhima_nikaya/mn118_att.md)).
- **Sub-commentary Translation**: Translated the 16 paragraphs of the Majjhima Nikāya Sub-commentary on MN 118 and interleaved them sentence-by-sentence with the original Pali ([mn118_tik.md](file:///Users/rds/pali_canon/tika/sutta/majjhima_nikaya/mn118_tik.md)).
- **Index Updates**: Updated word counts across all Nikāya indexes ([mula index](file:///Users/rds/pali_canon/mula/sutta/majjhima_nikaya/INDEX.md), [atthakatha index](file:///Users/rds/pali_canon/atthakatha/sutta/majjhima_nikaya/INDEX.md), [tika index](file:///Users/rds/pali_canon/tika/sutta/majjhima_nikaya/INDEX.md)).
- **Verification**: Created and ran a wikilink validation script verifying all links across the vault resolve cleanly.
- **Tracking System**: Created vault-level tracking files at the root: [SYNC_LOG.md](file:///Users/rds/pali_canon/SYNC_LOG.md), [TASKS.md](file:///Users/rds/pali_canon/TASKS.md), and [STATUS.md](file:///Users/rds/pali_canon/STATUS.md).

### Current State
- The vault is fully optimized for Obsidian with working indexes, navigation headers, and relative path wikilinks.
- Majjhima Nikāya 118 is completely migrated, translated, and interleaved across all three layers (Mūla, Commentary, Sub-commentary).
- The next step is expanding to other suttas in the Majjhima Nikāya or enhancing the existing files with cross-link references between Commentary, Sub-commentary, and Mūla.
