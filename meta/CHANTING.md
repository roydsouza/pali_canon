# Audio Chanting Integration Guide

This guide describes how audio chanting recitations are integrated into the Pali Canon Vault to support recitation, memorization, and daily meditation practice.

---

## 1. Overview

Audio chanting integration allows you to play high-quality recitations of Pali verses, suttas, and monastic codes directly from within their respective Obsidian notes. This bridges the gap between scholastic text study and oral recitation practice.

---

## 2. Directory Structure

All chanting audio files are stored in the git-ignored practice directory:
*   Path: `practice/audio/`
*   Format: `.mp3` (recommended for broad system compatibility)

You can open the audio folder on your system directly using this link (Hold `Cmd` and click in Editing Mode, or click directly in Reading Mode):
*   👉 **[Open practice/audio/ Folder in Finder](file:///Users/rds/pali_canon/practice/audio/)**

---

## 3. Difference Between Embeds and Clickable Links

In Markdown and Obsidian, there is an important distinction between embedding a media player and creating a clickable navigation link:

1.  **Audio Player Embed (Starts with `!`)**:
    *   Syntax: `![Player Name](path_to_audio.mp3)`
    *   Behavior: Renders an active audio playback bar in Obsidian. It is **not** a clickable link that opens the file in an external app; it is a player meant for inline listening.
2.  **Clickable Link (No `!`)**:
    *   Syntax: `[Link Name](path_to_audio.mp3)`
    *   Behavior: Clicking this link (or `Cmd`+clicking in Edit Mode) opens or reveals the file/folder in your system's default media player or Finder.

---

## 4. How to Configure Embeds & Links

Here are the standard formats for both audio player embeds and clickable links:

### A. Absolute Path (Vault Standard)
Used by automated generation scripts to ensure link resolution independent of note nesting depth.

*   **Audio Player Embed Syntax**:
    ```markdown
    ![Bhikkhu Pātimokkha Chanting Recitation](file:///Users/rds/pali_canon/practice/audio/bhikkhu_patimokkha.mp3)
    ```
*   **Interactive Test Link** (opens file externally if it exists):
    *   👉 [Open bhikkhu_patimokkha.mp3 (Absolute Link)](file:///Users/rds/pali_canon/practice/audio/bhikkhu_patimokkha.mp3)
    *   👉 [Open bhikkhuni_patimokkha.mp3 (Absolute Link)](file:///Users/rds/pali_canon/practice/audio/bhikkhuni_patimokkha.mp3)

### B. Relative Path (Portable)
A standard markdown relative link. You must adjust the number of `../` directories based on the folder depth of the note.

*   **Audio Player Embed Syntax** (for notes in `mula/vinaya/`):
    ```markdown
    ![Bhikkhu Pātimokkha Chanting Recitation](../../practice/audio/bhikkhu_patimokkha.mp3)
    ```
*   **Interactive Test Link** (relative to vault root/this guide):
    *   👉 [Open bhikkhu_patimokkha.mp3 (Relative Link)](practice/audio/bhikkhu_patimokkha.mp3)
    *   👉 [Open bhikkhuni_patimokkha.mp3 (Relative Link)](practice/audio/bhikkhuni_patimokkha.mp3)

> [!NOTE]
> If the `.mp3` files do not exist yet in your `practice/audio/` folder, clicking the links above will not open anything or may show a "File not found" warning. Once you place the files in the directory, these links will immediately become functional.

---

## 5. Current Audio Integrations

The following files already contain audio player integrations (configured with instructions to place the files in `practice/audio/`):

1.  **Bhikkhu Pātimokkha (227 Rules)**: [[patimokkha_bhikkhu|Bhikkhu Pātimokkha]]
    *   Target File: `bhikkhu_patimokkha.mp3`
2.  **Bhikkhunī Pātimokkha (311 Rules)**: [[patimokkha_bhikkhuni|Bhikkhunī Pātimokkha]]
    *   Target File: `bhikkhuni_patimokkha.mp3`

---

## 6. How to Follow Links in Obsidian

To test or follow these links in Obsidian:
*   **In Reading Mode**: Left-click the link directly.
*   **In Editing Mode (Live Preview/Source)**: Hold down the **`Cmd`** key (on macOS) and click the link.
