---
id: practice_dashboard
title: Practice Dashboard
type: practice-index
tags:
  - practice/index
---

<div class="db-header">
  <h1>Pali Canon Practice Hub</h1>
  <p>Daily recollection, chanting recitation, and meditation logging</p>
</div>

<div class="db-grid-wide">

  <div class="db-card practice">
    <div>
      <span class="db-badge practice">Statistics</span>
      <h3>🧘 Meditation Overview</h3>
      <p>Live summary of your meditation practice aggregated via Dataview.</p>
      
```dataview
TABLE WITHOUT ID length(rows) as "Total Sessions", sum(rows.duration_minutes) as "Total Minutes", round(sum(rows.duration_minutes)/60, 1) as "Total Hours"
FROM #practice/session
GROUP BY true
```

```dataview
TABLE WITHOUT ID meditation_type as "Meditation Type", length(rows) as "Sessions", sum(duration_minutes) as "Total Min"
FROM #practice/session
GROUP BY meditation_type
```
    </div>
  </div>

  <div class="db-card jhana">
    <div>
      <span class="db-badge jhana">Memorization</span>
      <h3>📖 Active Recitation Log</h3>
      <p>Key Pali verses selected for memorization and daily chanting practice.</p>

- [[../mula/sutta/anguttara_nikaya/an11_15|AN 11.15 / Snp 1.8: Karaṇīyamettāsutta]] <span class="db-badge jhana">Reviewing</span>
- [[../mula/sutta/khuddaka_nikaya/dhammapada/dhp_01_yamakavagga|Dhammapada: Dhp 1 (Manopubbaṅgamā)]] <span class="db-badge jhana">Reviewing</span>
- [[../mula/sutta/khuddaka_nikaya/dhammapada/dhp_14_buddhavagga|Dhammapada: Dhp 183 (Sabbapāpassa)]] <span class="db-badge jhana">Reviewing</span>
- [[../matika/three_refuges|Tisarana (Refuges)]] <span class="db-badge jhana">Reviewing</span>
- [[../mula/sutta/majjhima_nikaya/mn19|MN 19: Dvedhāvitakkasutta Verse]] <span class="db-badge jhana">Reviewing</span>

      <p style="margin-top: 15px; font-size: 0.9em;">👉 Go to full [[memorization_log|Verse Memorization Log]]</p>
    </div>
  </div>

  <div class="db-card vipassana">
    <div>
      <span class="db-badge vipassana">Chanting</span>
      <h3>🎧 Monastic Chanting Playlists</h3>
      <p>Listen to Pali recitations directly within the vault using local files.</p>
      
      <div class="db-playlist-item">
        <span>Bhikkhu Pātimokkha (227 Rules)</span>
        <span><a class="internal-link" href="audio/bhikkhu_patimokkha.mp3">Play (Relative)</a> | <a href="file:///Users/rds/pali_canon/practice/audio/bhikkhu_patimokkha.mp3">Play (Absolute)</a></span>
      </div>
      
      <div class="db-playlist-item">
        <span>Bhikkhunī Pātimokkha (311 Rules)</span>
        <span><a class="internal-link" href="audio/bhikkhuni_patimokkha.mp3">Play (Relative)</a> | <a href="file:///Users/rds/pali_canon/practice/audio/bhikkhuni_patimokkha.mp3">Play (Absolute)</a></span>
      </div>

      <p style="margin-top: 15px; font-size: 0.9em;">📖 Refer to [[../CHANTING|Audio Chanting Integration Guide]] for setup instructions, or [Open audio/ Folder in Finder](file:///Users/rds/pali_canon/practice/audio/).</p>
    </div>
  </div>

  <div class="db-card matika">
    <div>
      <span class="db-badge matika">Logs & Templates</span>
      <h3>📝 Practice Logs & Navigation</h3>
      <p>Log a session or create customized practice notes.</p>

- [[../templates/practice_note|Meditation Session Template]]
- [[../INDEX|Return to Root Vault Index]]

      <p style="margin-top: 15px; font-size: 0.85em; opacity: 0.8;">
        <strong>How to log a sit:</strong><br>
        1. Create a new note using the session template.<br>
        2. Apply the `#practice/session` tag.<br>
        3. Log your duration, type, and associated suttas to dynamically update this dashboard.
      </p>
    </div>
  </div>

</div>

---

## 🧘 Recent Meditation Sessions

*This list is generated automatically via Dataview using the `#practice/session` tag.*

```dataview
TABLE duration_minutes as "Duration (min)", associated_suttas as "Focus Suttas", hindrances as "Hindrances encountered"
FROM #practice/session
SORT date DESC
LIMIT 10
```

---
*Created and maintained as a structured database for Buddhist studies and daily monastic practice.*
