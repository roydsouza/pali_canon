# Pali Canon Vault

A personal Obsidian study vault for the Theravāda Buddhist Pali Canon — built for meditation practice and precepts study, not academic coverage.

The vault pairs **root texts** (mūla) with **traditional commentaries** (atthakathā) and **sub-commentaries** (ṭīkā), weaving everything together through a **mātikā web** of 22 doctrinal cross-reference lists. The goal is a practitioner's canonical library: a place to read suttas alongside the classical exegesis, trace doctrines across the canon, and support an active sitting practice — all offline, in plain Markdown.

---

## What Is Here

### Three-Layer Structure

Every sutta has up to three layers, stored in separate directories:

| Layer | Directory | Content | Source |
|---|---|---|---|
| **Mūla** (root text) | `mula/` | Interleaved **bold Pali** / *italic English* segments | SuttaCentral/Bilara (CC0) + Bhikkhu Sujato translations |
| **Aṭṭhakathā** (commentary) | `atthakatha/` | Classical Pali commentary with `§NNN` paragraph anchors | CSCD tipitaka.org XML |
| **Ṭīkā** (sub-commentary) | `tika/` | Classical Pali sub-commentary with `§NNN` paragraph anchors | CSCD tipitaka.org XML |

Each segment in a mūla file looks like this:

```
**Evaṁ me sutaṁ—**
*So I have heard.*
```

The commentaries are anchored to corresponding mūla paragraphs with collapsible callout blocks so you can read commentary in context without breaking the flow of the root text.

### Mātikā Web

Twenty-two canonical Buddhist lists — the Four Noble Truths, the Noble Eightfold Path, the Five Aggregates, the Seven Awakening Factors, and so on — live as standalone notes in `matika/`. Each list note links forward to every sutta in the vault that treats that doctrine, and each sutta links back. This creates a bidirectional doctrinal index: start from any list, navigate to the canonical treatments; start from any sutta, follow its doctrinal threads outward.

### Current Inventory (May 2026)

| Collection | Suttas / Texts | Layers |
|---|---|---|
| Dīgha Nikāya | 8 suttas | Mūla + Aṭṭhakathā + Ṭīkā |
| Majjhima Nikāya | 22 suttas | Mūla + Aṭṭhakathā + Ṭīkā |
| Saṃyutta Nikāya | 11 saṃyuttas (225 suttas) | Mūla + Aṭṭhakathā + Ṭīkā |
| Aṅguttara Nikāya | 35 sutta groups (~662 suttas) | Mūla + Aṭṭhakathā + Ṭīkā |
| Dhammapada | 423 verses (26 vaggas) | Mūla + Aṭṭhakathā |
| Udāna | 80 suttas (8 vaggas) | Mūla + Aṭṭhakathā |
| Itivuttaka | 112 suttas (4 nipātas) | Mūla + Aṭṭhakathā |
| Sutta Nipāta | 73 suttas (5 chapters) | Mūla + Aṭṭhakathā |
| Theragāthā | 203 poems (21 nipātas) | Mūla |
| Therīgāthā | 73 poems (16 nipātas) | Mūla |
| Vinaya Piṭaka | Bhikkhu + Bhikkhunī Pātimokkha | Selected rules |
| **Mātikā lists** | **22 lists** | Pali + English, fully cross-linked |

Total: ~1,162 validated Markdown files, ~14,000 internal wikilinks, 0 broken links.

### Practice Infrastructure

- **`paths/`** — Thematic reading sequences organized by practice domain (entering jhāna, vipassanā, brahmavihāra, gradual training, maraṇasati, anussati, paritta)
- **`paritta/`** — Protective chanting texts in recitation order
- **`practice/`** — Meditation session log, verse memorization tracker, daily practice dashboard
- **`matika/`** — Individual sub-files for all 22 lists and all 8 Noble Eightfold Path factors
- **Obsidian plugins** — Simsapa DPD (double-click Pali word lookup), Dataview (live query tables), Templater, CSS translation toggle (hide English to read Pali only)

---

## Design Principles

**Practice first, study second.** Content decisions are guided by seven practice domains in priority order: Jhāna, Vipassanā, Brahmavihāra, Anussati, Gradual Training, Maraṇasati, and Paritta. A sutta is added because a practitioner working in the Theravāda tradition needs it — not to fill gaps in coverage.

**Three-layer or nothing.** A sutta without its commentary is half a text. The mūla/atthakathā/ṭīkā structure is the unit of work. Commentary paragraphs are cross-linked to root-text paragraphs at the `§NNN` level so study stays in context.

**Markdown-native.** No plugins required to read the texts. No database. No server. An Obsidian vault is a folder of plain `.md` files; this one will be readable by any Markdown editor, even if the cross-links require Obsidian to navigate.

**One canonical translation.** Sujato's SuttaCentral translations (CC0) are the authoritative English text. No AI translation is layered over them.

---

## Repository Layout

```
pali_canon/
├── mula/            # Root texts (interleaved Pali/English)
│   ├── sutta/
│   │   ├── digha_nikaya/
│   │   ├── majjhima_nikaya/
│   │   ├── samyutta_nikaya/
│   │   ├── anguttara_nikaya/
│   │   └── khuddaka_nikaya/
│   └── vinaya/
├── atthakatha/      # Classical commentaries (CSCD Pali, §-anchored)
├── tika/            # Classical sub-commentaries (CSCD Pali, §-anchored)
├── matika/          # Doctrinal cross-reference lists (22 lists + sub-files)
├── paths/           # Thematic reading sequences
├── paritta/         # Protective chanting index
├── practice/        # Meditation log, memorization tracker
├── templates/       # Obsidian Templater templates
├── meta/            # Project coordination (TASKS, ROADMAP, STATUS, SYNC_LOG)
└── scratch/         # Python tooling (generators, validators, crosslinkers)
    ├── generators/
    ├── crosslinkers/
    ├── inspect/
    ├── lib/
    └── tests/
```

---

## Tooling

All scripts live in `scratch/` and require Python 3.10+. Set `PALI_VAULT` to the vault root before running.

```bash
export PALI_VAULT=/path/to/pali_canon
```

| Script | Purpose |
|---|---|
| `scratch/validate_links.py` | Validate all wikilinks and HTML links vault-wide (must be 0 errors before every commit) |
| `scratch/tests/run_all_tests.py` | Run the full unit-test suite (must all pass before every commit) |
| `scratch/generators/generate_sutta.py` | Generate mūla + atthakathā + ṭīkā files for any sutta ID via SuttaCentral API + CSCD XML cache |
| `scratch/crosslinkers/crosslink_generic.py` | Inject paragraph-level cross-links between commentary and root text |
| `scratch/lib/pali_utils.py` | Shared utilities: XML parsing, frontmatter I/O, Pali normalization |

A git pre-commit hook runs the link validator automatically. Never commit with `--no-verify`.

---

## Where This Is Going

### Near-Term: Phase 16 — Study Station Enhancements

These are vault-internal improvements that deepen the reading environment without adding new raw texts:

- **Prosopography** — Manual index notes for key persons (`people/`) and places (`places/`) appearing across the suttas, with links to every sutta they appear in
- **Simile Index** — A cross-referenced catalogue of the canon's major similes (the raft, the blind men, the elephant footprint, the lute strings, …) linking to their source suttas
- **Pericope Concordance** — A map of the canon's repeated stock formulas (jhāna cadences, dependent origination chains, the gradual training sequence) with links to every occurrence
- **Parallel-Texts Layer** — SuttaCentral parallel IDs injected into frontmatter and surfaced via Dataview, so each sutta shows its Chinese/Sanskrit parallels
- **Question-Driven Paths** — New thematic reading paths answering practice questions: *"working with anger"*, *"facing death"*, *"understanding craving"*

### Medium-Term: Phase 17 — Pali NLP Companion (External Repo)

A separate `pali-nlp` repository will treat this vault as its corpus and write reading aids back into it. The vault itself remains plain Markdown; the NLP system produces artifacts — vocabulary concordance tables, spaced-repetition cards, concordance index pages — that are committed back as ordinary notes.

Planned stages:
1. **Graded Reader** — Lemmatize tokens against the Digital Pāli Dictionary (DPD) SQLite database; append per-sutta vocabulary tables; build a reading ladder ordered by lexical difficulty
2. **Linguistic Pipeline** — Offline concordance and collocation search; NER tagger to auto-populate prosopography pages
3. **Semantic Search & RAG** — Local-first vector search with citation links to `§NNN` paragraph anchors; offline LLM generation (MLX/llama.cpp) as the default backend
4. **Performance Porting** — Tokenizer and sandhi-splitting layers rewritten in Rust for the M-series hardware

### Longer-Term: Abhidhamma and Fuller Vinaya

The Abhidhammatthasaṅgaha (Bhikkhu Bodhi's manual) and a fuller Vinaya index are conditional additions — only if the canonical sutta content reaches saturation in actual practice use.

---

## What This Is Not

- **Not a public resource.** The vault is personal; format and density are optimized for one reader.
- **Not an academic database.** No paper annotations, citation management, or research metadata.
- **Not a translation project.** Sujato's translations are the text; this vault adds structure and commentary, not new English renderings.
- **Not mobile-first or cloud-synced.** Designed for a single macOS machine with local storage.

---

## Data Sources and Licenses

| Source | Usage | License |
|---|---|---|
| SuttaCentral / Bilara | Mūla segments + Sujato translations | CC0 |
| CSCD (tipitaka.org) | Commentary and sub-commentary XML | — (personal use; cached in `scratch/xml_cache/`, git-ignored) |
| Digital Pāli Dictionary (DPD) | Lexicon SQLite for the NLP companion | Mixed CC0 / CC BY-NC-SA (git-ignored; verify before redistribution) |

Audio files, the XML cache, and the DPD database are all git-ignored and must not be committed.

---

## Coordination

Active session work is tracked in `meta/`:

- `meta/TASKS.md` — Granular task checklist; never mark done unless verified
- `meta/ROADMAP.md` — Phase sequencing with evaluation checkpoints
- `meta/STATUS.md` — Vault metrics snapshot
- `meta/SYNC_LOG.md` — Timestamped session log (ISO-8601 with UTC offset); entries older than 30 days rotate to `meta/sync_archive/`
