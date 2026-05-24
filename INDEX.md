# Pali Canon Vault Index

Welcome to the Obsidian Pali Canon Vault. This vault is organized to host root Canonical Pali texts (Mūla) alongside their respective Commentaries (Atthakathā) and Sub-commentaries (Tīkā), structured symmetrically by Pitaka and Nikaya.

## Directory Structure & Status

The vault is divided into four primary segments. Click on each section below to explore its nested directories:

*   **[[mula/INDEX|Mūla (Canonical Texts)]]**
    *   *Description*: The original discourses, rules, and scholastic treatises of the Tipiṭaka.
    *   Status: **Active**. Sutta Piṭaka: MN (22), DN (8), SN (11 saṃyuttas / 225 suttas), AN (35 suttas/groups / 662 suttas), KN (6 collections / Dhammapada 423 verses). Vinaya initiated (Bhikkhu & Bhikkhunī Pātimokkha). Abhidhamma scaffolded.
* **[[atthakatha/INDEX|Atthakathā (Commentaries)]]**
    *   Description: Traditional explanations and clarifications of the canonical root texts.
    *   Status: **Active**. Commentary for all migrated suttas + Dhammapada-aṭṭhakathā (26 chapters, 294 stories, ~498K words).
* **[[tika/INDEX|Tīkā (Sub-commentaries)]]**
    *   Description: Sub-commentaries explaining the commentary texts.
    *   Status: **Active**. Sub-commentary for all migrated suttas (Dhammapada ṭīkā pending).
* **[[matika/INDEX|Mātika (Buddhist Lists)]]**
    *   Description: Systematically cataloged registers of Buddhist lists with Romanized Pali and item-by-item translations.
    *   Status: **Active**. 22 lists migrated and cross-linked to canonical sources.
* **[[practice/INDEX|Practice Dashboard (Meditation & Study)]]**
    *   Description: Tools for active practice, meditation logs, templates, and verse memorization logs.
    *   Status: **Active**. Templates, memorization log, and practice note dashboard integrated.

---

## Vault-Wide Migration Status

*   **Nikāyas Active**: Majjhima (22 suttas), Dīgha (8 suttas), Saṃyutta (11 saṃyuttas / 225 selected suttas), Aṅguttara (35 suttas/groups / 662 suttas), Khuddaka (6 collections / Dhammapada 423 verses)
*   **Total Individual Suttas/Poems**: 1,458 (Mūla) / 1,172 (Atthakathā) / 306 (Ṭīkā) where available
*   **Estimated Total Word Count**: ~900K+ across all layers
*   **Active Piṭakas**: Sutta Piṭaka, Vinaya Piṭaka (Abhidhamma scaffolded)
*   **Last Updated**: 2026-05-24
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
