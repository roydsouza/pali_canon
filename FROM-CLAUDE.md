# FROM-CLAUDE — Vault Review

*Review by Claude (Opus 4.7), 2026-05-24.*
*Follows the archived review at `archive/FROM-CLAUDE-05-22.md` (Sonnet 4.6). Where that review's "Ongoing Issues" recur, they are noted below.*

**Scope reviewed:** full folder hierarchy (excluding `.git`, `.obsidian`, `.claude`), the three text layers (mūla/aṭṭhakathā/ṭīkā × sutta/abhidhamma/vinaya), `matika/`, `practice/`, `paths/`, `paritta/`, `templates/`, and the root meta-docs. Sample files were read from each layer and type; counts were taken from the working tree on the review date.

---

## Verdict at a glance

The vault is in genuinely good shape: high-quality interleaved Pali/English, dense and accurate mātikā cross-linking, a clean three-layer model, and real reading tools (translation toggle, DPD lookup, Dataview). The content work is strong. **The weaknesses are almost entirely about consistency, navigability, and metadata discipline — not about the texts themselves.** The single highest-leverage improvement is normalizing YAML frontmatter so the vault becomes queryable as a database. The biggest *opportunity* is that the vault is currently a **reading/doctrine** tool but barely a **language-learning** tool — and the user explicitly wants the latter (see §D).

---

## A. Errors & inconsistencies (concrete, verifiable)

### A1 — Frontmatter schema drift `[HIGH]`
Different migration phases used different YAML schemas for the same kind of file. Compare two mūla suttas:

- `mula/sutta/majjhima_nikaya/mn118.md`: `id: MN118`, `sutta_number: 118`, has `commentary_file` / `sub_commentary_file`, **no** `translator` / `source` / `title_en`.
- `mula/sutta/anguttara_nikaya/an10_60.md`: `id: AN10.60`, `sutta_number: an10.60` (string, dotted), has `translator` / `source` / `title_en` / `tags`, **no** `commentary_file` / `sub_commentary_file`.

So `sutta_number` is sometimes an integer (`118`), sometimes a dotted string (`an10.60`); the commentary cross-reference fields exist in some files and not others. **Consequence:** you cannot reliably write a single Dataview query across the corpus (sort by number, list orphaned commentaries, etc.). This is the root cause that makes several "utility" ideas in §C/§D harder than they should be.
**Fix:** define one canonical schema per `type` (mula / atthakatha / tika / matika / practice / path / index), write it into `templates/`, then run a one-pass normalizer (the `scratch/` tooling already does this kind of sweep).

### A2 — "22 mātikā lists" is asserted in four places but isn't true `[MEDIUM]`
The number 22 is hard-coded in `INDEX.md:42`, `HERMES.md:11`, `HERMES.md:36`, `STATUS.md:12`, and `STATUS.md:165`. But `matika/INDEX.md` actually surfaces **19** lists, `grep '## The List' matika/*.md` finds **21** list-files, and the folder holds **108** files total. None of these agree. This is the same class of bug the 05-22 review caught (18-vs-19) — it has simply drifted further. See C4 for the structural fix (stop hard-coding counts).

### A3 — Cross-layer grouping boundaries don't line up `[MEDIUM]`
The three layers chunk AN differently, which breaks the clean 1-mūla→1-commentary→1-subcommentary mapping:

- mūla: `an11_2.md`, `an11_3.md`, `an11_4.md`, `an11_5.md` (four files)
- aṭṭhakathā: `an11_3_5_att.md` (+ `an11_2_att.md`)
- ṭīkā: `an11_2_5_tik.md` (one file covering 2–5)

Also a likely genuine gap: `an10_60_att.md` exists but there is **no `an10_60_tik.md`** (AN does have a Manorathapūraṇī-ṭīkā, so this isn't a "no ancient ṭīkā" case like Udāna/Snp). And `an10_60.md`'s frontmatter has no `sub_commentary_file`, so nothing flags the omission. Worth a deliberate decision: either align the chunking across layers, or add an explicit `covers:`/`part_of:` field so anchored links survive the mismatch.

### A4 — Filename convention is mixed: dots vs underscores `[LOW]`
`snp1.1`, `thag1.1`, `thig1.1` use dotted decimals; everything else (`an1_1_10`, `mn118`, `sn45`) uses underscores. Dots-in-filenames are also read as extensions by some tools and shells. Not urgent, but a vault-wide convention (prefer `snp1_1`) would remove a class of future friction.

### A5 — `INDEX.md` undersells the Khuddaka Nikāya `[LOW–MED]`
The front-page card badges KN as "**Dhp & Udāna**" (`INDEX.md:20`), but the vault actually has Dhammapada, Udāna, **Itivuttaka (112)**, **Sutta Nipāta (~70)**, **Theragāthā** and **Therīgāthā** under mūla. The front door undercounts your own work by four whole books.

### A6 — Template no longer matches the files it generates `[LOW–MED]`
`templates/mula_sutta.md` has no `**Mātikā**:` line and a minimal frontmatter, but real files like `mn118.md` carry a Mātikā line, commentary callouts, and a different frontmatter shape. New suttas built from the template will silently regress to the older structure. Update templates to match the evolved format (and add the missing ones: a `path` template, a mātikā-**list** vs mātikā-**factor** template, a paritta template).

### A7 — `matika/INDEX.md` only indexes ~18% of the folder `[MEDIUM]`
It lists 19 lists; the folder has 108 files. The other ~87 are **factor pages** (`right_view.md`, `contemplation_of_body.md`, `abstaining_from_killing.md`, …) that are reachable only by following a link from inside a list — there's no index of them and no Dataview that enumerates them. See C2.

---

## B. Omissions & coverage gaps

### B1 — The Abhidhamma Piṭaka is effectively absent
`mula/abhidhamma/`, `atthakatha/abhidhamma/`, `tika/abhidhamma/` each contain **only `INDEX.md`** (stubs of ~450–760 bytes). The vault's stated structure is "three layers × three piṭakas," but one piṭaka is empty scaffolding. This is acknowledged as future work in `HERMES.md`, and that's a defensible priority call (meditation-first). But see B5 — the empty scaffolding shouldn't masquerade as navigable.

### B2 — Vinaya is two Pātimokkha files with no exegesis
`mula/vinaya/` has `patimokkha_bhikkhu.md` + `patimokkha_bhikkhuni.md`; `atthakatha/vinaya/` and `tika/vinaya/` are index-only. Given the user's stated **secondary** goal of precepts study, the Pātimokkha mūla is the right beachhead, but it currently has no commentary layer at all and no cross-links to the `five_precepts` / `eight_precepts` mātikā.

### B3 — Theragāthā / Therīgāthā have mūla only
There is no `atthakatha/sutta/khuddaka_nikaya/theragatha|therigatha/` folder, so the verses of the elders have no commentary layer — even though the Paramatthadīpanī (Thag-a/Thig-a) exists and is rich in the biographical backstories that make those verses meaningful. A genuine future-content gap (distinct from Udāna/Snp/Iti, where the "no ancient ṭīkā" note is legitimate).

### B4 — `paritta/` is index-only
`paritta/INDEX.md` is a well-made curated table pointing at existing snp/an files (links verified valid). That's fine as far as it goes, but there's no recitation-formatted artifact (continuous Pali, no English, with the sequence) for actual chanting — which is what a paritta collection is *for*. See D8.

### B5 — Empty stubs create dead-end navigation
`INDEX.md`'s "Traditional Exegesis" card links to `atthakatha/INDEX` and `tika/INDEX`, and the Abhidhamma/Vinaya index stubs are reachable from there. A first-time user clicks into a confident-looking card and lands on a near-empty page. Either label these clearly as **"planned — not yet migrated"** at the link site, or gate them out of the main index until populated. False affordances erode trust in the index.

### B6 — No language-learning scaffolding
There is no glossary, no grammar reference, no vocabulary list, no morphology aids — nothing that teaches **Pali the language** as opposed to presenting Pali **texts**. DPD double-click lookup is excellent for ad-hoc queries, but the vault has no structured on-ramp for someone building reading competence. This is the gap §D is built around, and it's the one the user's request foregrounds.

---

## C. Structure & usability

### C1 — `practice/` and `paths/` overlap confusingly
The two folders encode a real and useful distinction — `practice/*` = *what the technique is*, `paths/*` = *a curated reading sequence through suttas* — but nothing signposts it, and the names collide: there is a `maranasati.md` in **both** folders, plus `practice/jhana` vs `paths/entering_jhana`, `practice/vipassana` vs `paths/vipassana_practice`, `practice/metta` vs `paths/brahmavihara_cultivation`. A newcomer can't tell which to open.
**Fix (cheap):** add a one-line header to each file stating the axis ("This is the *technique* note — for a guided reading sequence see [[…]]") and cross-link each pair. **Fix (cleaner):** rename path files with a `_path` suffix so the two axes are unambiguous in any link/search.

### C2 — `matika/` is a flat 108-file folder mixing two kinds of note
Lists (`noble_eightfold_path`) and their constituent factors (`right_view`) live at the same level with no separation and no complete index. As this grows it becomes unbrowseable.
**Recommendation:** keep files where they are (to preserve link stability) but add a `category: list | factor` frontmatter field and a Dataview-driven Map-of-Content in `matika/INDEX.md` that auto-lists both groups. This fixes A7 and A2 at once and never goes stale.

### C3 — Root meta-doc sprawl (10 files; `SYNC_LOG.md` is 71 KB)
The root holds `CHANTING`, `HERMES`, `INDEX`, `ROADMAP`, `SIMSAPA-DPD`, `START`, `STATUS`, `SYNC_LOG`, `TASKS`, `VISION` — ten meta-docs competing with the actual entry points (`START`, `INDEX`) for attention, with overlapping content (HERMES, STATUS, ROADMAP, VISION all describe "what's done / what's next"). It's not obvious which is authoritative.
**Recommendation:** keep `START.md` and `INDEX.md` at root as the front door; move process/agent docs into a `meta/` (or `docs/`) folder — `STATUS`, `ROADMAP`, `VISION`, `HERMES`, `SYNC_LOG`, `CHANTING`, `SIMSAPA-DPD`. Designate **one** live status doc and let the others be archival. (`TASKS.md` + `SYNC_LOG.md` are the agent-coordination contract and should stay easy to find, just not at the expense of the reader's front door.)

### C4 — Replace hard-coded counts with live Dataview
Every metric in `INDEX.md` / `STATUS.md` / `HERMES.md` is a hand-maintained number, and they've all drifted (A2; and the 05-22 review's "STATUS script count is stale"). `INDEX.md` already runs Dataview for "Recently Modified." Extend that: `LENGTH(...)`-style counts for suttas-by-nikāya, mātikā lists, files-by-type. Numbers that compute themselves can't drift.

### C5 — Normalize frontmatter (the keystone)
This is A1 restated as a structural priority: a single, documented schema per type turns the whole vault into a queryable database and unlocks C2, C4, and most of §D/§E. Worth doing before the corpus gets larger.

---

## D. Higher utility — innovative uses for **learning Pali (the language)**

This is where the vault can grow the most, and it's the explicit ask. Every idea below is grounded in assets already present: segment-aligned Pali/English, §-anchors, the DPD/Simsapa integration, Dataview, and the `scratch/` tooling.

### D1 — A word-by-word morphological gloss as a third toggle layer ⭐
You already toggle English on/off with `Cmd+R`. Add a **third** interlinear layer: under each Pali line, a word-by-word gloss with lemma + grammatical parse (case/number/gender for nominals, tense/person/voice for verbs, root). This is the classic "trot" that turns opaque Pali into learnable Pali, and it's the single highest-value language feature. DPD already holds the morphological data; a generator can pre-compute the gloss line per segment and a CSS class can hide/show it. Three states: Pali-only → Pali+English → Pali+gloss+English.

### D2 — Corpus vocabulary-frequency engine → a graded reader
Run a lemmatizing pass (DPD) over all mūla text to produce a frequency-ranked vocabulary. From it, generate **per-sutta "new words" lists** in your chosen reading order — i.e., the words that first appear in this sutta given what you've read before. That converts the canon into a graded reader and tells you exactly which ~50 words unlock the most text. (Pali is extremely formulaic, so the frequency curve is steep — a few hundred lemmas cover a huge fraction of the suttas.)

### D3 — Spaced-repetition vocabulary, generated from the corpus
`practice/memorization_log.md` already does spaced review for **verses**. Extend the same mechanism to **vocabulary**: mark a word while reading, and a generator emits a review card (lemma → gloss → an example sentence drawn from a sutta you've read, deep-linked back to the §-anchor). Export to Anki, or use an Obsidian spaced-repetition plugin so it stays inside the vault.

### D4 — A Pāli reading ladder ordered by *linguistic* difficulty
The `paths/` are organized by doctrine. Add one path ordered by **reading difficulty**: short formulaic texts first (Itivuttaka, Dhammapada verses, the highly repetitive Saṃyutta), graduating to Majjhima then the long, syntactically complex Dīgha. A `paths/pali_reading_ladder.md` would be the natural "where do I start reading actual Pali" answer the vault currently lacks.

### D5 — A pericope / stock-formula concordance ⭐
The canon is built from repeated stock phrases (the jhāna formula, the gradual-training formula, *evaṁ me sutaṁ*, the perception-of-impermanence refrain). Recognizing formulas is *the* skill that turns slow decoding into fluent reading. Build a concordance: one page per formula, with the Pali, a gloss, and deep-links to every occurrence across the corpus. Your segment-aligned data makes this uniquely feasible — detect repeated n-grams across files and auto-generate the cross-reference pages.

### D6 — A verbal-root (dhātu) graph — a second knowledge graph
Alongside the doctrinal mātikā graph, build a **linguistic** graph: pages for verbal roots (√gam, √ñā, √dhā, √kar) linking every derived word across the corpus. Obsidian's graph view would then show two complementary webs — one of *meaning*, one of *form*. This is a genuinely novel use of the platform and directly serves language acquisition (learning families of words by root is far more efficient than word-by-word).

### D7 — A grammar reference hub linked to live examples
A small `grammar/` set of reference pages — the eight cases, declension paradigms, verb conjugation classes, sandhi rules, the compound (samāsa) types — where **each grammar point links to real occurrences in your suttas** ("locative absolute → see [[mn118#§…]]"). This is the inverse of D1: instead of glossing a text, you start from a grammar concept and jump to it in context. Mātikā-style hubs, but for grammar.

### D8 — Chanting ↔ text alignment for aural learning
`CHANTING.md` and the audio infrastructure exist. Pair audio with the Pali segments for **shadowing**: hear a line, see it, repeat it. This couples pronunciation/prosody (which silent reading never teaches) with the written form, and turns the paritta collection (B4) into a real recitation tool — a continuous Pali-only recitation file per chant, segment-aligned to audio.

---

## E. Innovative uses for the **literature**

- **E1 — Prosopography graph.** Named-entity pages (Sāriputta, Anāthapiṇḍika, Sāvatthī, Jeta's Grove) that link every sutta mentioning them. The interleaved text already contains the names; this turns the vault into a who's-who/where's-where of the canon and makes the Theragāthā/Therīgāthā backstories navigable.
- **E2 — Simile (upamā) index.** A cross-referenced catalogue of the canon's famous similes (the raft, the saw, the elephant's footprint, the lute). Superb for teaching, recall, and seeing how one image recurs across discourses.
- **E3 — Parallels layer.** Store SuttaCentral parallel IDs (Chinese Āgama, etc.) in frontmatter and surface them via Dataview, enabling comparative study of where the Pali and Āgama versions diverge.
- **E4 — Question-driven reading paths.** Beyond technique-based paths: "working with anger," "facing death," "the factors of stream-entry." (The 05-22 review/HERMES suggested this too — still open and high-value.)
- **E5 — A study dashboard.** A Dataview page tracking what you've read, what's memorized, vocabulary learned, most-revisited texts — the vault as a self-quantified study companion. (All local, consistent with the privacy-first design.)

---

## F. Suggested priority order

**Do first (foundational, unblock everything else):**
1. Normalize frontmatter to one schema per type, recorded in `templates/` (A1, A6, C5).
2. Convert front-page counts to Dataview; stop hand-maintaining numbers (A2, C4).
3. Add `category: list|factor` to mātikā files + a Dataview MoC in `matika/INDEX.md` (A7, C2).

**High-value, low-effort:**
4. Fix `INDEX.md` KN badge and the "22 lists" wording (A5, A2).
5. Label or gate the empty Abhidhamma/Vinaya stubs so they're not dead ends (B5).
6. Add cross-links + clarifying headers between `practice/` and `paths/` pairs (C1).
7. Decide the `an10_60` ṭīkā question and the AN cross-layer chunking policy (A3).

**Bigger bets (the language-learning leap):**
8. Word-by-word gloss toggle (D1) — highest single payoff.
9. Vocabulary frequency engine + graded "new words" lists (D2), feeding spaced repetition (D3).
10. Pericope/formula concordance (D5) and the root graph (D6).

**Housekeeping when convenient:**
11. Move process docs into `meta/`; keep `START`/`INDEX` as the front door (C3).
12. Unify the dot/underscore filename convention (A4).

---

*Net: the corpus and cross-linking are excellent. Invest next in metadata normalization (so the vault becomes a database) and in the language-learning layer (gloss, vocabulary frequency, formula concordance, root graph) — that's where the vault goes from a fine reading library to a genuine tool for learning Pali.*
