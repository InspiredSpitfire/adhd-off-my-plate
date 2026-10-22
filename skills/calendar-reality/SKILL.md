---
name: calendar-reality
description: Turns a calendar into the number of real working hours the human actually has, then names the conflicts, the events that need prep, the events to decline, and the life anchors with no slot. Reads today plus the next two working days through a connected calendar tool or pasted agenda. Use when the user says "what's my day look like", "how much time do I actually have", "am I double-booked", "what do I need to prep", "which meetings can I skip", "calendar check", or when plate-triage calls it.
---

# Calendar reality

Read `../../RULES.md` first (especially §6, capacity is arithmetic), then `plate/config.md` for waking hours, life anchors, and the standing-no list.

## The arithmetic

For today and each of the next two working days:

```
waking window (config.md)
− calendar events (busy, accepted or unanswered)
− life anchors with no calendar event (meds, meals, kids, dog, commute, sleep debt noted in the dump)
− 20% buffer (ADHD transitions are not free)
= real hours
```

Say each number. Then say the real-hours figure in plain words: "You have about 2 hours and 40 minutes of actual work time today, and it is split into three pieces, the longest being 75 minutes." The shape of the time matters as much as the total: a Feral brain needs one long block; a Foggy brain is fine with pieces.

## What you flag

1. **Conflicts.** Overlapping events, events during a life anchor, back-to-backs with no travel or reset time.
2. **Needs prep.** Any event whose title or description implies the human presents, decides, or brings something. Say what the prep is and how long, as a Keep candidate or an Off-my-plate item (you can draft the agenda, pull the notes, build the one-pager).
3. **Decline or skip.** Events that match a standing no in `config.md`, recurring meetings with no agenda, optional invites unanswered for more than a week. For each, give the one-line decline text as a DRAFT or NEEDS YOUR GO item. Never decline for them.
4. **Unanswered invites.** Yes/no decisions due today.
5. **Life anchors with no slot.** Meds, food, movement, the dog, the kid pickup. If the day has no gap for them, that is the first conflict, not a footnote.

## Output

```
## Calendar reality · <date range>

| Day | Waking | Events | Life anchors | Buffer | Real hours | Longest block |

### Conflicts
### Needs prep  (→ Keep candidates / Off-my-plate items with gates)
### Decline or skip  (→ DRAFT / NEEDS YOUR GO, with the text)
### Unanswered invites
### Life anchors with no slot

EVIDENCE: <events cited with time>
ASSUMED: <waking window if config.md is blank, anchors if not listed>
```

Standing alone, end with the single calendar move that buys the most time today.
