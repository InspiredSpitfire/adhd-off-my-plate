---
name: whats-missing
description: The gap finder. Cross-references the brain dump, the inbox, the calendar, the waiting-on list, the graveyard, and the life anchors in config and names what the human is not seeing - commitments with no task, deadlines with no calendar slot, people waiting past their nudge date, money left on the table, dropped items due for revival, and body and life items with no room in the day. Use when the user says "what am I missing", "what am I forgetting", "blind spots", "what's going to bite me", "what fell through the cracks", "did I forget anyone", or when plate-triage reaches its What-you're-missing section.
---

# What's missing

Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` first (§9, evidence labels), then every workspace file. This skill is only as good as the cross-reference, so read all of it.

## Start with the scripts

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/due.py" <workspace> --within 3
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/surfaced.py" <workspace> --threshold 3
```

The first is the evidence for checks 2, 4, and 5; the second for check 8. Cite their lines (`due.py: W-01 nudge 3d late`). Do not re-derive dates from the tables by eye. If there is no shell, read the tables and say so.

## The eight checks

Run every one. Report only the hits, with where each was found.

1. **Commitment with no task.** An "I owe them" row from `inbox-sweep` (or a promise in the dump) that is not in Keep, Off my plate, or `later.md`. Quote it.
2. **Deadline with no slot.** Anything due inside 72 hours, on the Plate or in `later.md`, that has no calendar block and no Keep slot. Say the date and the gap.
3. **Event with no prep.** A calendar event in the next 48 hours that implies presenting, deciding, or bringing something, with nothing on the Plate for it.
4. **Person past nudge-by.** `due.py` OVERDUE and TODAY rows from `waiting-on.md`. Offer the nudge as a DRAFT.
5. **Graveyard due.** `due.py` rows from `graveyard.md` whose revive-by is today or past. Surface each once, then move its revive-by forward 30 days or to `never` on the human's word.
6. **Money.** Unpaid invoices they are owed, bills due, renewals they meant to cancel, a quote they never sent, an offer they never priced. From the sweep and the dump.
7. **Body and life.** Life anchors in `config.md` with no room in today's real hours: meds, food, movement, sleep, appointments overdue (vet, dentist, doctor, school forms), the dog. These outrank work items of equal urgency.
8. **The avoided thing.** The item `surfaced.py --threshold 3` lists (three or more Plates without moving), or that the dump mentions with a sigh. Name it once, plainly, and offer a 5-minute version. Do not lecture.

## Rules

- Every hit cites where it came from: email sender/subject/date, calendar event/time, dump line, workspace file and row.
- Never invent a gap. If a check finds nothing, do not pad; say nothing about it.
- If every check comes up empty, the section's one line is the place you could not look ("No mail connector, so commitments made by email are unchecked").
- Life items first, money second, then the rest in deadline order.

## Output

```
## What you're missing · <date>

- <gap> · found in <source> · <suggested handling: Keep | Off my plate (gate) | Let go | Next step>
...

Checked: dump, inbox (<window> | not connected), calendar (<range> | not connected), waiting-on, graveyard, config anchors.
```

Standing alone, end with the single gap most likely to cost them something this week.
