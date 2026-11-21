---
name: due
description: What's due. Overdue nudges, graveyard items due back, and deadlines from your later list, counted step by step, not guessed.
argument-hint: '[days ahead, default 3]'
---

Days ahead: $ARGUMENTS if it is a number, otherwise 3. Find the workspace (RULES §2 lookup) and the plugin root (the directory above `commands/`), read RULES §2c, and run the due check with that many days ahead. Show its result lines and any warnings.

Then one line: the single overdue item most likely to cost something this week, and its handling (a DRAFT nudge, a Keep, or a revive-by moved on the human's word). If nothing is due, say so in one line and stop.
