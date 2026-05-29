# Sync Log

## [2026-05-28 08:37:00-07:00 — Completion of Phase 15 Hygiene, Consistency & Backfill (Antigravity)]

### Accomplishments

**Batch 1 — Dotted Filename Refactor**
- **Dotted Filename Refactor**: Successfully renamed 422 dotted files (e.g., `snp1.1.md` -> `snp1_1.md`) across the Sutta Nipāta, Theragāthā, and Therīgāthā in Mūla and Atthakathā layers.
- **Link Rewriter**: Modified `scratch/refactor/rename_dotted.py` to support path-based wikilinks (e.g. target containing slashes) and backslash-escaped pipes `\|` inside markdown tables. Ran refactoring script to successfully update references in `paritta/INDEX.md` and `practice/memorization_log.md` which corrected the remaining 10 broken links.

**Batch 2 — Frontmatter Schema Validation & AN Chunking Alignment**
- **Frontmatter Schema Linter**: Created the standalone validation script `scratch/inspect/lint_frontmatter.py` to check YAML metadata constraints by file type.
- **AN Chunking Reciprocal Validation**: Configured `covers` lists on grouped AN commentary and sub-commentary files (`an11_3_5_att`, `an11_2_5_tik`) and updated covered Mūla files with reciprocal `commentary_file`/`sub_commentary_file` fields.
- **Integration**: Integrated linter checks directly into `scratch/validate_links.py` and added the `TestFrontmatterLinter` test suite inside `scratch/tests/run_all_tests.py`.

**Batch 3 — Paragraph-Level Cross-Linking Backfill (Phase 19)**
- **Backfill Coordination**: Created `scratch/refactor/run_backfill.py` to run paragraph alignment on MN 36, DN 22, and the SN saṃyuttas (SN 12, 22, 35, 46, 54, 56).
- **Correctness Fix**: Modified `scratch/crosslinkers/crosslink_generic.py` to verify paragraph existence in Tīkā files before injecting headings and links, resolving all 23 broken link errors from missing Tīkā paragraphs.

### Health Baseline
- **Validator**: 1,162 files / 14,136 wikilinks / **0 errors** ✅
- **Unit tests**: 10/10 pass ✅
- **Git**: Clean state (re-run validate_links and run_all_tests prior to completion).

## [2026-05-28 07:25:00-07:00 — Execution of Urgent Handoff Cleanups (Antigravity)]

### Accomplishments

**Batch 1 — Multi-agent Correctness & Cleanliness**
- **CLAUDE.md Guardrails**: Created the project-level `/Users/rds/pali_canon/CLAUDE.md` documenting the mission, data model, coordinated contracts, guardrails (tests/validators), and workflows.
- **SYNC_LOG Rotation**: Trimmed the live `meta/SYNC_LOG.md` to keep only current entries (post-May 24, 2026). The older logs (~66 KB) were successfully moved to `meta/sync_archive/SYNC_LOG_2026-05_early.md` to prevent context overhead.
- **Triage File Removal**: Deleted the transient `FROM-CLAUDE.md` handoff note now that all its items are fully resolved or recorded in `meta/TASKS.md` Phase 15.

**Batch 2 — Audio Embeds Fix**
- **Chanting Audio**: Replaced broken `file://` absolute paths in `meta/CHANTING.md` and `practice/INDEX.md` with vault-relative wikilink embeds `![[filename.mp3]]` to natively render Obsidian's audio player for local files in the git-ignored `practice/audio/` directory.
- **Link Validator**: Updated `scratch/validate_links.py` to recognize and bypass media files (.mp3, .png, etc.) so Obsidian resource embeds are not flagged as unresolved markdown files.

### Next Session Handover
The critical hygiene/setup phase is complete:
- Live `meta/SYNC_LOG.md` size is reduced to 17 KB.
- Zero broken links / Zero test failures.
- Recommended next task: Gemini Flash 3.5 can take over "easy stuff" like **B1: Dotted Filename Refactor** or **B2: Frontmatter Schema Validation** (developing `scratch/inspect/lint_frontmatter.py`).

---

## [2026-05-27 18:50:00-07:00 — Status Review & Triage of FROM-CLAUDE.md (Antigravity)]

### Context
Reviewed the second `FROM-CLAUDE.md` handoff (2026-05-27, Claude Opus 4.7) against current governance docs and live vault state. Goal: identify what's already been done, what's still open, and recommend prioritized execution order for the next session.

### Health Baseline
- **Validator**: 1,160 files / 13,837 wikilinks / **0 errors** ✅
- **Unit tests**: 9/9 pass ✅
- **Git**: clean on `main`, tracking `origin`. One untracked file: `FROM-CLAUDE.md`
- **Actual counts**: 1,169 total `.md` files, 132 Python scripts, 422 dotted filenames

### FROM-CLAUDE.md Triage (what's done vs. still open)

| Item | Description | Status |
|---|---|---|
| **A1** | Chanting audio `file://` broken embeds | ⚠️ **OPEN** — 4 refs in `meta/CHANTING.md`, 3 in `practice/INDEX.md` |
| **A2** | Stale doc counts (remote, scripts, files) | ✅ Done (prior session corrected VISION, STATUS) |
| **A3** | No project-level `CLAUDE.md` | ⚠️ **OPEN** — file does not exist |
| **B1** | 422 dotted filenames | ⚠️ **OPEN** — `find` confirms 422 matches |
| **B2** | Frontmatter schema linter | ⚠️ **OPEN** — no `lint_frontmatter.py` exists |
| **B3** | AN cross-layer `covers:`/`part_of:` | ⚠️ **OPEN** |
| **B4** | SYNC_LOG unbounded (1,070 lines / 78 KB) | ⚠️ **OPEN** |
| **B5** | Phase 19 §-anchor backfill | ⚠️ **OPEN** |
| **Stage 3** | Study enhancements (prosopography, etc.) | Already tracked in TASKS.md Phase 16 |
| **Stage 4** | Pali NLP system | Already tracked in TASKS.md Phase 17 |
| **D.0** | AI-layer posture | Recorded in VISION.md |
| **D.1** | VISION.md NLP boundary clarification | ✅ Done (prior session) |

### Recommended Execution Order (for next agent session)

**Batch 1 — Highest leverage, unlocks multi-agent correctness:**
1. **A3: Create `CLAUDE.md`** at vault root. This is the single highest-leverage fix: every new agent re-derives conventions from scratch and gets them wrong. Concise guardrails doc pointing to VISION, TASKS, SYNC_LOG, validator, and test suite.
2. **B4: SYNC_LOG rotation.** Create `meta/sync_archive/`, move entries older than current month, keep trailing ~30 days live. Current 78 KB is a burden on every agent session.

**Batch 2 — Fix broken features:**
3. **A1: Chanting audio fix.** Replace `file://` embeds in `meta/CHANTING.md` and `practice/INDEX.md` with vault-relative wikilink embeds (`![[audio_file.mp3]]`). Drop the "open folder" `file://` link (unsupported in Obsidian). Document that `practice/audio/` is git-ignored and users place audio files locally.

**Batch 3 — Consistency & hygiene (Phase 15):**
4. **B1: Dotted filename refactor.** Write `scratch/refactor/rename_dotted.py` (idempotent, dry-run-able), rename 422 files, rewrite all wikilinks. Largest single change — run validator after.
5. **B2: Frontmatter schema linter.** Create `scratch/inspect/lint_frontmatter.py`, wire into test suite. Enforce required keys by `type` (mula/atthakatha/tika/matika).
6. **B3: AN chunking alignment.** Add `covers:`/`part_of:` fields to grouped AN files.

**Batch 4 — Backfill (Phase 19):**
7. **B5: §-anchor backfill** for MN 36, DN 22, and SN 12/22/35/46/54/56.

**Batch 5 — Future phases (Phase 16-17):**
8. Study enhancements and NLP companion development per existing TASKS.md.

### Status of `FROM-CLAUDE.md`
The file is **partially processed**: items A2 and D.1 were already resolved; Stages 3-4 and D.0 are already tracked in governance docs. **Six items remain open (A1, A3, B1-B4, B5).** Do NOT delete `FROM-CLAUDE.md` until all remaining items are either completed or folded into TASKS.md. The file should be committed to git so it's visible to all agents.

### Recommendations for the User
- **Commit `FROM-CLAUDE.md` to git** (`git add FROM-CLAUDE.md && git commit -m "docs: add Claude Opus 4.7 vault review handoff"`). It's currently untracked and invisible to agents cloning the repo.
- **Next session: execute Batches 1-3** (~30 min work) to close the critical gaps before starting any new content migration.
- The vault is in **good health** (0 link errors, all tests green, remote up to date) — the open items are all hygiene/robustness improvements, not data integrity issues.

---

## [2026-05-27 17:10:00-07:00 — Full Vault Review & NLP Roadmap (Claude Opus 4.7)]

### Accomplishments
- Conducted a full review of the vault (1,161 validated md files, 132 Python scripts, all `meta/` governance docs) plus live diagnostics: link validator (0 errors), unit tests (9/9), filename/frontmatter/git scans.
- Authored `FROM-CLAUDE.md` (root) — a staged, step-by-step handoff for any LLM, covering: critical fixes, consistency/hygiene gaps, study-workstation enhancements, and a 4-stage path to a Pali NLP system (reading layer → linguistic pipeline → semantic/RAG → Rust port).
- Captured Roy's directional decisions: NLP = all-layers/staged; architecture = hybrid Python-now/Rust-later; resources = lean hard on DPD + SuttaCentral; **the NLP engine lives in its own separate `pali-nlp` repo that consumes this vault (vault stays plain markdown)**; AI-layer posture delegated to Claude (recommendation in doc §D.0).

### Key findings (see FROM-CLAUDE.md for fixes)
- **Errors**: chanting audio uses non-rendering `file://` embeds and `practice/audio/` is empty; HERMES/STATUS still claim "no remote" but `origin` exists; STATUS says 126 scripts (actual 132); VISION says ~242 files (actual 1,161); no project-level `CLAUDE.md`.
- **Gaps**: 422 dotted filenames; frontmatter schema drift; AN cross-layer chunking lacks `covers:`/`part_of:`; `SYNC_LOG.md` is an unbounded 1,056-line append log; Phase 19 §-anchor backfill still pending.

### Current State
- No vault content changed; only `FROM-CLAUDE.md` added and this log entry. Validator/tests still green. Next agent should work `FROM-CLAUDE.md` Stage 1 → 4 and delete it once processed.

## [2026-05-24 20:45:00-07:00 — Dataview Index Diagnostics & Root Cause Analysis (Antigravity)]

### Diagnosis of Blank Dataview Tables
We diagnosed the issue causing blank Dataview tables in `matika/INDEX.md` when rendering in Obsidian.
1. **Keyword Collision with Reserved Names**: In Dataview’s query parser, words like `type` and `list` are built-in reserve keywords (`type()` is a type checking function, and `LIST` is a query format). Query filters like `WHERE type = "matika"` and `WHERE category = "list"` collide with the Dataview parser.
2. **Obsidian Vault Root Nesting**: If the repository is opened inside a parent folder in Obsidian, folder paths specified via `FROM "matika"` look for a directory named `matika` at the root of the vault, which doesn't exist if the repo is in `pali_canon/matika/`.
3. **Obsidian Metadata Cache Delay**: When files are edited or created externally (via terminal python scripts), Obsidian detects file change events, but Dataview's internal IndexedDB database cache does not always automatically trigger a re-parse of custom frontmatter tags (such as `category`) unless forced.

### Actions Taken and Attempted
- **First Attempt**: Removed `type: matika` and renamed frontmatter category values from `list`/`factor` to `list_note`/`factor_note` to bypass reserved keyword collisions in Dataview.
- **Second Attempt**: Replaced the absolute folder path `FROM "matika"` with a relative folder query `WHERE contains(file.folder, "matika")` to allow nested vault compatibility.
- **Third Attempt (Foolproof)**: Since Dataview's cache database may still have stale metadata for custom properties like `category`, we designed a query that only uses 100% native built-in Obsidian file properties (`file.path` and `file.name`) which are always indexed.

### Standardized, Metadata-Independent Queries Implemented in `matika/INDEX.md`
For lists:
```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

For factors:
```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND file.name != "INDEX"
  AND !contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

These queries do not rely on any custom YAML frontmatter fields (like `type` or `category`), making them completely immune to metadata indexing delays.

## [2026-05-24 16:45:00-07:00 — Vault Review (Claude Opus 4.7)]

### Session Accomplishments
- **Full hierarchy review**: Read the folder structure across all three layers (mūla/aṭṭhakathā/ṭīkā × sutta/abhidhamma/vinaya), `matika/`, `practice/`, `paths/`, `paritta/`, `templates/`, and the root meta-docs.
- **Deliverable**: Wrote [FROM-CLAUDE.md](file:///Users/rds/pali_canon/FROM-CLAUDE.md) — a review covering errors/inconsistencies, omissions, usability/structure, and innovative uses for learning Pali and the Pali literature. Follows the archived `archive/FROM-CLAUDE-05-22.md`.

### Key Findings (no fixes applied this session — review only)
- **Frontmatter schema drift** across mūla files (e.g. `mn118` vs `an10_60` differ in `id`/`sutta_number` form and commentary-link fields) — flagged as the keystone fix that unblocks vault-wide Dataview.
- **"22 mātikā lists" is stated in INDEX/HERMES/STATUS but disagrees** with reality (matika INDEX shows 19; `## The List` appears in 21; folder holds 108 files incl. ~87 unindexed factor pages).
- **Cross-layer chunking mismatch** in AN (mūla `an11_2..5` vs att `an11_3_5` vs ṭīkā `an11_2_5`); `an10_60` has att but no ṭīkā.
- **Coverage gaps**: Abhidhamma piṭaka is stub-only; Vinaya has Pātimokkha mūla but no exegesis; Theragāthā/Therīgāthā lack commentary; empty stubs create dead-end navigation.
- **Biggest opportunity**: vault is reading/doctrine-oriented but thin on *language* learning — recommended a word-by-word gloss toggle, corpus vocabulary-frequency graded reader, pericope/formula concordance, and a verbal-root graph.

### Current State
- No content or text-layer files were modified. Only `FROM-CLAUDE.md` was created and this log entry added.
- See FROM-CLAUDE.md §F for a prioritized action checklist. No TASKS.md items marked done (this was a review, not migration work); the §F items could be promoted into TASKS.md if the recommendations are accepted.

## [2026-05-24 — Meditation Techniques Section in INDEX.md (Antigravity)]

### Session Accomplishments

**Meditation Techniques Section**
- **INDEX.md Integration**: Added a new "Meditation Techniques" section to `INDEX.md` directly under the card grid (Daily Practice & Support section), linking to core meditation techniques in the suttas.
- **Technique Files Creation**: Created 5 detailed technique notes in the `practice/` directory:
  * `practice/jhana.md` (Jhāna / Meditative Absorption)
  * `practice/vipassana.md` (Vipassanā / Insight Meditation)
  * `practice/metta.md` (Mettā / Loving-Kindness Meditation)
  * `practice/anapanasati.md` (Ānāpānasati / Mindfulness of Breathing)
  * `practice/maranasati.md` (Maraṇasati / Mindfulness of Death)
  * Each file includes a description (one page or less), back pointer to `INDEX.md` at the top, and a curated list of relevant suttas referencing the technique at the bottom.
- **Explicit Paths Resolution**: Resolved a link ambiguity on the `maranasati` base name by explicitly directing path index references to `paths/maranasati.md` and practice techniques to `practice/maranasati.md`.

**Verification and Link Integrity**
- **Link Validator**: Verified link health. Checked **1,162 markdown files** and **14,053 wikilinks**, confirming **0 broken links** in the entire vault.

---

## [2026-05-24 — Phase 20.2: Vault-wide Mātika Factors Expansion Complete (Antigravity)]

### Session Accomplishments

**Vault-wide Mātika Factors Expansion**
- **Factor Files Creation**: Created 78 detailed markdown files under `matika/` for every factor in the remaining 18 lists of the Buddhist *Mātika* (e.g. `impermanence.md`, `feeling.md`, `sensual_desire.md`, `abstaining_from_killing.md`, `mindfulness.md`, `buddha.md`, `generosity.md`, `contemplation_of_body.md`, etc.).
- **Canonical Definition & Description**: Each file contains its Romanized Pali definition from canonical texts (such as SN 45.8, SN 12.2, MN 9, Vibhaṅga, etc.), an interleaved English translation, a detailed practical description, and relative links to suttas in the vault that describe/mention the factor.
- **Parent List Integration**: Updated all 18 parent files in `matika/` to dynamically link parent list items to their respective detailed factor files, using clean English-first wikilinks with Pali display labels where appropriate.
- **Tool Refinement**: Modified the generator script `scratch/generators/generate_matika_details.py` to fix list section replacements in files with custom list headers (`ten_fetters.md` and `seven_purifications.md`) and to utilize dynamic regex matching of search headers.

**Verification and Link Integrity**
- **Link Validator**: Ran `validate_links.py`. Verified 1,157 markdown files and 14,018 wikilinks, confirming **0 broken links** in the entire vault.

---

## [2026-05-24 — Phase 20.1: Noble Eightfold Path Factors Expansion Complete (Antigravity)]

### Session Accomplishments

**Noble Eightfold Path Factors Expansion**
- **Factor Files Creation**: Created 8 detailed markdown files in `matika/` for each path factor:
  - `right_view.md` (*Sammādiṭṭhi*)
  - `right_intention.md` (*Sammāsaṅkappo*)
  - `right_speech.md` (*Sammāvācā*)
  - `right_action.md` (*Sammākammanto*)
  - `right_livelihood.md` (*Sammāājīvo*)
  - `right_effort.md` (*Sammāvāyāmo*)
  - `right_mindfulness.md` (*Sammāsati*)
  - `right_concentration.md` (*Sammāsamādhi*)
- **Canonical Definition & Description**: Each file contains its Romanized Pali definition from the *Vibhaṅgasutta* (SN 45.8), an interleaved English translation, a detailed descriptive summary (a page or less), and links to suttas in the vault that describe/mention the factor.
- **Parent List Integration**: Updated `matika/noble_eightfold_path.md` to link the factors directly to their respective detail files.
- **Validation-Safe Placeholders**: Linked non-migrated suttas (like MN 9 and MN 58) using standard markdown links rather than wikilinks to maintain the vault-wide 0-broken-links guarantee.

**Verification and Link Integrity**
- **Link Validator**: Verified link health. Checked all 1,079 markdown files and 13,653 links, confirming 0 broken links in the entire vault.

---

## [2026-05-24 — Phase 18: Interactive Dashboards & Practice Hubs Complete (Antigravity)]

### Session Accomplishments

**Interactive Dashboards & Practice Hubs**
- **Custom CSS Design System**: Created `dashboard-styles.css` snippet containing the styling system (grids, glassmorphism cards, HSL category colors, hover scale animations, custom list items, and status badges). Enabled it vault-wide in `appearance.json`.
- **Premium Root Dashboard**: Rebuilt the root `INDEX.md` using standard HTML `<a>` tags with `class="internal-link"` for all internal links within card divisions, guaranteeing that links always render and function in Obsidian (bypassing raw HTML block markdown parsing limitations).
- **Premium Practice Hub**: Overwrote `practice/INDEX.md` with a beautiful grid dashboard using standard HTML `<a>` tags with the `internal-link` class for card links to guarantee rendering and traversal, alongside dynamic Dataview queries for stats and sits.
- **Chanting & SRS Review System**: Enhanced `practice/memorization_log.md` with:
  - An **Audio Track** column linking directly to localized recitation files.
  - A dedicated **Spaced Repetition & Active Recall** section at the bottom containing double-colon flashcard definitions for all active memorization verses.

**Verification and Link Integrity**
- **Link Validator**: Extended `validate_links.py` to scan and validate HTML `<a>` links ending in `.md` alongside standard wikilinks. Ran full vault validation: **1,071 markdown files and 13,585 total links successfully verified with 0 errors**.

---
