# Pali Canon Vault Index

Welcome to the Obsidian Pali Canon Vault. This vault is organized to host root Canonical Pali texts (Mūla) alongside their respective Commentaries (Atthakathā) and Sub-commentaries (Tīkā), structured symmetrically by Pitaka and Nikaya.

## Directory Structure & Status

The vault is divided into four primary segments. Click on each section below to explore its nested directories:

*   **[[mula/INDEX|Mūla (Canonical Texts)]]**
    *   *Description*: The original discourses, rules, and scholastic treatises of the Tipiṭaka.
    *   *Status*: **Active**. Sutta Piṭaka: MN (10), DN (4), SN (76), AN (14), KN/Dhammapada (423 verses). Vinaya and Abhidhamma scaffolded.
*   **[[atthakatha/INDEX|Atthakathā (Commentaries)]]**
    *   *Description*: Traditional explanations and clarifications of the canonical root texts.
    *   *Status*: **Active**. Commentary for all migrated suttas + Dhammapada-aṭṭhakathā (26 chapters, 294 stories, ~498K words).
*   **[[tika/INDEX|Tīkā (Sub-commentaries)]]**
    *   *Description*: Sub-commentaries explaining the commentary texts.
    *   *Status*: **Active**. Sub-commentary for all migrated suttas (Dhammapada ṭīkā pending).
*   **[[matika/INDEX|Mātika (Buddhist Lists)]]**
    *   *Description*: Systematically cataloged registers of Buddhist lists with Romanized Pali and item-by-item translations.
    *   *Status*: **Active**. 22 lists migrated and cross-linked to canonical sources.
*   **[[practice/INDEX|Practice Dashboard (Meditation & Study)]]**
    *   *Description*: Tools for active practice, meditation logs, templates, and verse memorization logs.
    *   *Status*: **Active**. Templates, memorization log, and practice note dashboard integrated.

---

## Vault-Wide Migration Status

*   **Nikāyas Active**: Majjhima (12), Dīgha (4), Saṃyutta (76), Aṅguttara (52), Khuddaka/Dhammapada (423v)
*   **Total Individual Suttas**: 144 (all three layers where available)
*   **Estimated Total Word Count**: ~900K+ across all layers
*   **Active Piṭakas**: Sutta Piṭaka (Vinaya and Abhidhamma scaffolded)
*   **Last Updated**: 2026-05-23
*   **Excluded Directories**:
    *   `scratch/`: Contains internal XML and JSON raw assets, download scripts, and utility modules. (Not indexed).

---

## Reading Tools

### Translation Toggle — `Cmd+R`

Press **`Cmd+R`** to show or hide the English translations. This lets you read the Pali alone or with the interleaved English.

- **Pali-only mode**: English translations (italic lines) are hidden. Good for reading or reciting Pali directly.
- **Pali + English mode**: Both lines visible side by side. Good for study or when checking meaning.

The toggle remembers its state across notes within the session. Restart Obsidian resets to whatever state was last saved.

### Pali Word Lookup — double-click

**Double-click any Pali word** to open the Digital Pāli Dictionary (DPD) sidebar. It shows the word's definition, grammatical form, root, and sutta references. See [[SIMSAPA-DPD]] for full details and troubleshooting.

The Simsapa desktop app must be running for lookups to work.

---

## 🕒 Recently Modified / Revisited
*This dashboard shows the most recently edited or updated files in the vault, generated using Dataview.*

```dataview
TABLE file.mtime as "Modified Time", type as "Type"
FROM ""
SORT file.mtime DESC
LIMIT 5
```

---
*Created and maintained as a structured database for Buddhist studies.*
