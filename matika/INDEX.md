# Mātika (Buddhist Lists Index)

**Navigation**: [[INDEX|Pali Canon Vault]] / [[matika/INDEX|Mātika]]

This directory contains systematic registers of Buddhist lists (*mātika*) compiled from the Pali Canon. Each list is stored in a dedicated file with Romanized Pali and item-by-item English translations, fully cross-referenced.

---

## 📋 Doctrinal Lists

```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

---

## 🏷️ Individual Factors & Mental States

```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND file.name != "INDEX"
  AND !contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

---
*Back to [[INDEX|Vault Home]]*
