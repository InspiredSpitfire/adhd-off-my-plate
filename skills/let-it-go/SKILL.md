---
name: let-it-go
description: The guilt-free drop audit. Walks a to-do list or project list and names what to let go of, what to defer with a date, and what to hand off, then moves each dropped item to the graveyard with a revive-by date or never, plus the decline text for anyone who needs telling. Use when the user says "what can I drop", "let go", "my list is too long", "I can't do all this", "I said yes to too much", "help me quit things", "what am I keeping out of guilt", "sunk cost", or when plate-triage has more than 3 Keeps.
---

# Let it go

Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` first (§7, letting go), then `plate/config.md`, `plate/graveyard.md`, and `plate/projects.md`.

## The three questions, per item

Ask them in order; the first "no" decides.

1. **Is anyone actually waiting?** A named person, a real deadline, money attached. Not "people might". If no one is waiting, it is a candidate.
2. **Would they start it today if it were new?** If the only reason it is on the list is that it is already on the list, it is a candidate.
3. **Does it serve a bucket in `config.md`?** Brands, roles, life. An item that serves none is a candidate.

Then sort the candidates:

| Verdict | Means | Goes to |
|---|---|---|
| **Drop** | Nobody is waiting, they would not start it today | graveyard, `revive-by: never` |
| **Defer** | Real, but it should not be looked at again until a date | graveyard, `revive-by: <date>` (whats-missing resurfaces it once, on that day). Real and simply not today goes to `later.md` instead, no verdict needed. |
| **Hand off** | Someone else can do it, or Claude can | Off-my-plate item with a gate, or a DRAFT asking the person |
| **Shrink** | The ambition is the problem; the 10-minute version still counts | Stays, rewritten smaller |

## The guilt handling

Sunk cost, "but I told them", and "I'll feel bad" are written into the graveyard row's "why" column, in their words. They are reasons to record, not reasons to keep. Where a person needs to be told, write the telling as a DRAFT (connector draft tool) or NEEDS YOUR GO item: short, plain, one reason or none, no apology spiral, no "I'm so sorry for the delay" opener.

Do not argue them into dropping something. Present the verdicts, the reasoning in one line each, and let them veto. Vetoed items go back to Keep or Later, and `graveyard.md` records "vetoed <date>" so the next audit does not re-litigate it.

## Output

```
## Let it go · <date> · <N> items audited

### Drop (→ graveyard, never)
- <item> · <why, their words>

### Defer (→ graveyard, revive-by)
- <item> · revive-by <date> · <why>

### Hand off (→ Off my plate / DRAFT)
- <item> · to <Claude | person> · gate

### Shrink (stays)
- <item> → <10-minute version>

### Needs telling
- <person> · DRAFT | NEEDS YOUR GO · "<text>"

Kept as is: <N>. List went from <N> to <N>.
```

Append every Drop and Defer to `plate/graveyard.md` in the template's columns. End with the single item whose removal frees the most attention.
