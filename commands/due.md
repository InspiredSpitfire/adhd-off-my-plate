---
name: due
description: What's due. Overdue nudges, graveyard items due back, and deadlines from your later list, counted by script, not guessed.
argument-hint: '[days ahead, default 3]'
---

Days ahead: $ARGUMENTS if it is a number, otherwise 3. Find the workspace (RULES §2 lookup) and the plugin root (the directory above `commands/`), then run `python3 <plugin root>/scripts/due.py <workspace> --within <days>` with both written as literal absolute paths, unquoted (RULES §2: unattended runs deny anything else). Show its output as it is, including any WARN lines.

Then one line: the single overdue item most likely to cost something this week, and its handling (a DRAFT nudge, a Keep, or a revive-by moved on the human's word). If nothing is due, say so in one line and stop.
