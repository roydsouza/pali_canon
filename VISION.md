# Vision: Pali Canon Vault

*Written 2026-05-22 by Claude Sonnet 4.6, informed by conversation with Roy Peter.*

---

## Where We Are

The vault is a **practitioner's reading station**: a structured environment for reading Pali suttas alongside their commentaries, with doctrinal cross-referencing via the mātikā web. It supports serious study without requiring external reference books.

Current inventory: ~242 files, 7 DN suttas, 11 MN suttas, 10 SN saṃyuttas (222 suttas), 14 AN suttas, Dhammapada, Udāna, Sutta Nipāta Uragavagga, 19 mātikā lists — all with three-layer structure (mūla / atthakathā / tīkā).

---

## Guiding Principles

These principles should constrain what gets added. Not every good idea belongs here.

1. **Practice first, study second.** Add content and tools that deepen meditation or clarify practice decisions. Resist the pull toward exhaustive coverage for its own sake.
2. **Lean over large.** A vault you can navigate comfortably beats one with complete coverage you never fully use. Measure adoption before expanding.
3. **Quality over quantity.** Better to have fewer suttas with full three-layer structure and strong mātikā links than to race to complete coverage.
4. **Evaluate before the next phase.** After each tranche of new content, spend time actually reading it in Obsidian before commissioning more. The vault should drive the practice, not the reverse.

---

## Near-Term: Deepen the Foundation (Phases 6–8)

These are the highest-value additions for a meditator working in the Theravāda tradition.

### Phase 6 — Remaining Sutta Nipāta Chapters
*The Aṭṭhakavagga is among the oldest strata of the Pali canon; the Metta Sutta (1.8) is already present.*

- Snp Chapter 2 (Cūḷavagga, 14 suttas) — includes Ratana Sutta (protective verse chanting), Maṅgala Sutta (blessings)
- Snp Chapter 4 (Aṭṭhakavagga, 16 suttas) — early poems on non-clinging; highly regarded by scholars and practitioners
- Snp Chapter 5 (Pārāyanavagga, 16 questions) — the Buddha's answers to 16 students; dense and terse
- CSCD: `s0503a.att0.xml` (Niddesa commentary for Atthakavagga/Parāyanavagga)

### Phase 7 — Itivuttaka (112 short discourses)
*Brief, self-contained utterances, each introduced with "This was said by the Blessed One." Ideal for daily reading practice.*

- SuttaCentral IDs: `iti1`–`iti112`; Sujato translation available
- Grouped into 4 nipātas (1–3 factors, 4 factors)
- Cross-links to: four_noble_truths, three_marks, noble_eightfold_path naturally

### Phase 8 — Theragāthā / Therīgāthā (exclamation verses)
*The monks' and nuns' verses of liberation: highly personal, poetic, practice-oriented.*

- Thag: ~264 verses in 21 chapters (Sujato translation)
- Thig: ~73 verses (Sujato translation)
- No formal commentary required; mātikā links to four_sublime_states, nibbāna themes

---

## Medium-Term: Practice Support Tools

These are tools that make the vault actively useful *during* practice, not just for study before or after.

### Personal Practice Notes (Per Sutta)
A simple template for recording reflections when you read a sutta. Not a commentary — your own notes:
- What landed? What was unclear?
- Which passage do you want to memorize or return to?
- Any connection to your sitting practice?

Implementation: a `practice/` folder with one note per sutta (or per mātikā), using a minimal template. Dataview can then surface notes you've revisited most recently or flagged as important.

### Thematic Reading Sequences
Rather than browsing by nikāya, curated reading paths organized by practice question:

- *"Working with the hindrances"* → MN 20, SN 46.51, AN 5.28, DN 2 sections
- *"Understanding the aggregates"* → SN 22 selection, MN 44, MN 43
- *"Ānāpānasati practice arc"* → MN 118, SN 54, AN 10.60, SN 46 (bojjhaṅgas)
- *"Path to stream-entry"* → SN 55 selection, DN 2, SN 48.9-10

These would live in a `paths/` or `sequences/` folder as simple Obsidian notes with embedded links.

### Verse Memorization Log
A note that tracks which verses or passages you're working on committing to memory — sutta reference, the Pali and translation, and a date field for spaced review.

---

## Longer-Term: The Study Environment Matures

These are worth considering only after the near-term content is in place and actually being used.

### Deeper MN Coverage
The suttas most valuable for meditation are largely complete (MN 10, 20, 36, 43, 44, 52, 111, 118, 119, 121). Remaining candidates:
- MN 2 (Sabbāsavasutta — removing taints; the 7-method framework)
- MN 117 (Mahācattārīsakasutta — right view in full, with mundane/supramundane distinction)
- MN 22 (snake simile, non-clinging to views)
- MN 140 (Dhātuvibhaṅga — 6 elements, equanimity instruction)

### Vinaya Pātimokkha (Selected Rules)
Not all 227 rules — but the rules with direct bearing on lay or monastic practice context:
- The Bhikkhu Pātimokkha preamble and categories
- Cross-link to five_precepts, eight_precepts
- Thanissaro's translation is freely available

### AN Nipāta Gaps
AN 7, 8, 11 currently have no coverage. Higher priority within them:
- AN 7.65 (Dutiya-aññatitthiya — seven factors of awakening)
- AN 11.1-5 (Gradual training sequence — Ānāpānasatisutta series)
- AN 8.53 (Dāna, sīla, bhāvanā sequence)

---

## What This Vault Is Not For

Keeping these off the roadmap unless something specific changes:

- **Academic paper ingestion or annotation** — this is a canonical-text reading environment, not a research database
- **NLP or corpus analysis** — Pali Language Society / DPD cover this far better
- **Sharing or publishing** — the vault is personal; format and density optimized for one reader
- **Automated translation** — Sujato's Suttacentral translations are the authoritative source; don't layer AI translation over them
- **Mobile sync / remote hosting** — complexity cost outweighs benefit for solo use

---

## Evaluation Points

Suggested pauses before commissioning more content:

1. **After Phase 6**: Can you navigate from a mātikā list to a relevant Snp sutta and find the cross-connection useful? If the Snp material doesn't feel integrated, fix that before adding Itivuttaka.
2. **After Phase 7**: Is the three-layer structure still manageable with ~300+ files? Run the link validator; check if INDEX navigation is still quick.
3. **Before any practice-support tools**: What actual friction have you noticed while using the vault for practice? Tools should solve observed problems, not anticipated ones.
