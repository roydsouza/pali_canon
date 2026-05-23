---
id: practice_dashboard
title: Practice Dashboard
type: practice-index
tags:
  - practice/index
---

# Practice Dashboard

**Navigation**: [[INDEX|Pali Canon Vault]] / [[practice/INDEX|Practice Dashboard]]

Welcome to your active Buddhist practice dashboard. This space aggregates your meditation sessions, verse memorization tracking, and links to your personal logs.

---

## Core Practice Tools

- 📖 **[[memorization_log|Verse Memorization Log]]**: Keep track of the Pali verses and chants you are actively memorizing.
- 📝 **[Meditation Session Template](../templates/practice_note.md)**: The standardized template for creating new practice notes.

---

## 🧘 Recent Meditation Sessions

*This list is generated automatically via Dataview using the `#practice/session` tag.*

```dataview
LIST
FROM #practice/session
SORT date DESC
LIMIT 10
```

---

## 📈 Sutta Integration Log

*The table below tracks your focus suttas across recent practice sessions, enabling you to see how your canonical study integrates with your actual practice.*

```dataview
TABLE duration_minutes as "Duration (min)", associated_suttas as "Focus Suttas", hindrances as "Hindrances encountered"
FROM #practice/session
SORT date DESC
LIMIT 10
```

---

## Getting Started

1. **Create a Note**: When you sit, create a new note in your Obsidian vault and apply the `practice_note` template.
2. **Log Details**: Log the duration, meditation type (e.g. *Anāpānasati* or *Jhāna*), and any suttas you are studying or reflecting on.
3. **Check the Dashboard**: Revisit this dashboard to see your practice history and see which suttas you have been practicing with.
