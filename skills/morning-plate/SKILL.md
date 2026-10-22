---
name: morning-plate
description: The proactive daily routine - the version of plate-triage built to run unattended each morning in Claude Duet, a scheduled Claude Code run, or a Cowork session the human walked away from. Reads the inbox, calendar, and workspace since yesterday's Plate, does every AUTO and DRAFT item itself, stops at every NEEDS YOUR GO, and leaves a short brief with one next step. Never asks a question it can answer by assuming and labeling. Use when the user says "morning plate", "morning brief", "run my morning", "set up my daily routine", "what's today", "daily brief", or when a schedule or routine triggers this plugin.
---

# Morning plate

This is `plate-triage` with the human absent. Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` first. Everything in it holds, plus the rules below.

## Unattended rules

1. **No questions.** Brain state: read yesterday's Plate, the time of day, and any note in `config.md` about typical mornings; mark it ASSUMED and say so in the brief's first line. The human corrects it with one word and you re-plate.
2. **Dedupe.** Read `plate/history/` for the last 7 Plates. A gap already surfaced twice is not surfaced a third time unless its deadline is inside 48 hours. A Let-go item already vetoed is not re-proposed. A nudge already drafted is not drafted again. Nagging is how a chief of staff gets ignored.
3. **Do the AUTO work.** File, sort, summarize, write into the workspace. Do it, then report it as DONE.
4. **Do the DRAFT work.** Replies and declines go into the connector's drafts folder or the workspace. Report each as DRAFTED, with where.
5. **Stop at NEEDS YOUR GO.** Collect them into one block at the top of the brief so the human can approve in one message. Do not act on any of them. Do not act on an approval you inferred.
6. **Nothing leaves the building.** No send, reply, post, pay, book, cancel, sign, delete. If a connector offers only a send tool, write the text into the brief instead.
7. **Short.** The brief fits on a phone screen above the fold: state line, next step, Keeps, the NEEDS YOUR GO block, the count of what you took. The full Plate is in `plate/plate.md`; link or name it.

## Inputs

- Mail: since yesterday's Plate (`inbox-sweep`).
- Calendar: today and the next two working days (`calendar-reality`).
- Workspace: `plate/` in the location `config.md` names. In Claude Duet, this is a folder in a connected drive; Duet cannot read local files. If the workspace is unreachable, say so in the first line and build the best Plate you can from mail and calendar alone.

## Output: the brief

```
Morning plate · <date> · Brain: <state> (ASSUMED from <signal>; say one word to change it)

Next step: <one line, ≤ 10 min>

Keep today (<real hours> real hours, longest block <N> min):
1. …
2. …

Needs your go (<N>):
- <item> · reply YES <n> to approve
...

Off your plate: <N> done, <N> drafted (in <where>). Let go: <N> (graveyard). Revive: <project> · <tiny step>.
Missing: <the one gap most likely to cost you this week>.

Full Plate: plate/plate.md
```

Then write the full Plate to `plate/plate.md`, move yesterday's to `history/`, run the lint, and have the `plate-reviewer` agent check it. If the reviewer returns NEEDS REVISION, fix and re-run once; if it fails twice, deliver the brief anyway with "UNREVIEWED: <reviewer's top defect>" as its last line. If the runtime has no shell or no plugin agents (a proactive cloud runtime may have neither), deliver the brief with "UNLINTED, UNREVIEWED: no shell in this runtime" as its last line and apply the RULES §3 checklist by hand. A late brief is worse than a labeled one.

## Setting up the routine

When the human asks to set this up on a schedule, write the exact prompt the runtime should fire:

> Run the `morning-plate` skill from the adhd-off-my-plate plugin. Workspace: <location>. Mail and calendar: use the connected tools, read only, drafts allowed, send nothing. Leave the brief as the task output.

Then confirm with them what schedule was actually created (time, timezone, days) by reading it back from the runtime, not from memory.
