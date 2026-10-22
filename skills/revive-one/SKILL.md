---
name: revive-one
description: Picks one unfinished project from the registry, diagnoses in one clause why it stalled, and hands over a single step of ten minutes or less that makes it un-stuck. Tracks revival attempts so a project revived and dropped three times gets called out. Use when the user says "revive", "which project should I pick back up", "I have so many unfinished things", "I never finish anything", "what's one small step", "half-done projects", or when plate-triage reaches its Revive section.
---

# Revive one

Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` first (§8, reviving), then `plate/projects.md`, `plate/graveyard.md`, and today's brain state.

## Pick one

Not the most important project. The one most likely to move today, which is usually:

1. a project whose stall reason is a single missing decision or a single missing fact (fast to un-stick), then
2. a project where someone is waiting (the social pull helps), then
3. the project that fits today's brain state (Feral: the hard creative one; Froggy: the one with a novel next move; Foggy: the one with a checklist-shaped step; Fried: none, skip this skill),
4. and never a project whose revival count in `projects.md` is already 3 or more, unless you say so out loud and they choose it anyway.

If `projects.md` is empty, build it: pull every half-finished thing from the dump, the inbox, and the file system or repos the human points you at. One row each: name, bucket, last touched (EVIDENCE if a file date or email exists, else ASSUMED, else `unknown`), what done looks like, why it stalled, revival count.

## Diagnose in one clause

The reason is the step. Pick one:

| Stalled because | The tiny step is |
|---|---|
| The next step is unclear | Write the next three steps on paper; do none of them (10 min) |
| Waiting on someone | Draft the nudge (DRAFT gate) and set a nudge-by (5 min) |
| A decision is missing | Make the decision for them, state it, and give the action that follows (recommended answer labeled INFERENCE) |
| Novelty wore off | Change one thing about how it is done: new tool, new place, new format, a timer (10 min) |
| Fear of the result | Ship the ugliest possible version to one safe person (10 min) |
| No deadline | Pick a date and a witness; write the invite text into the Plate as NEEDS YOUR GO (a calendar event with an attendee sends on creation, so it is never DRAFT) |
| Too big | Cut scope until the whole project is one afternoon; write the new done line (10 min) |

The step makes it un-stuck. It does not finish it. Ten minutes or less. One line. On Foggy, do the first half of the step yourself where you can.

## Honesty about the count

Read the revival count in `projects.md`. When it is already 3 or more, say: "This is revival #N. Keep it dead, or make it a Keep. Both are allowed." Record whatever they choose. Do not re-revive it silently.

## Output

```
## Revive one · <date>

**Project:** <name> · stalled since <date | ASSUMED> · stalled because <one clause> · revival #<N>
**Tiny step:** <action> (N min)     ← N ≤ 10
**Done line for the project:** <what finished looks like, one sentence>
```

Update `plate/projects.md`: revival count +1, "last revived" = today, the step recorded. If they pass on the project, record "declined <date>" instead.
