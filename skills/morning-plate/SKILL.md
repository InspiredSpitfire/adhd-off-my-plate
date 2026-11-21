---
name: morning-plate
description: The proactive daily routine - the version of plate-triage built to run unattended each morning in Claude Duet, a scheduled Claude Code run, or a Cowork session the human walked away from. Reads the inbox, calendar, and workspace since yesterday's Plate, does every AUTO and DRAFT item itself, stops at every NEEDS YOUR GO, and leaves a short brief with one next step. Never asks a question it can answer by assuming and labeling. Use when the user says "morning plate", "morning brief", "run my morning", "set up my daily routine", "what's today", "daily brief", or when a schedule or routine triggers this plugin.
---

# Morning plate

This is `plate-triage` with the human absent. Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` first. Everything in it holds, plus the rules below.

## Unattended rules

0. **Know where you are.** The workspace is the path the routine prompt or the `/morning` argument names. Use it exactly; do not go looking in `~/plate` or anywhere else, and do not read files outside the workspace and the plugin. If no path was named, use the RULES §2 lookup and say which one you used in the brief's first line.
1. **No questions.** Brain state: read yesterday's Plate (on a first run it is the blank template; skip it), the time of day, and any note in `config.md` about typical mornings; mark it ASSUMED and say so in the brief's first line. The human corrects it with one word and you re-plate.
2. **Dedupe, by count.** After writing the Plate, run the repeat check in new-Plate mode (RULES §2d) against the last 7 Plates in `history/`. Every REPEAT it finds is cut, unless its deadline is inside 48 hours or the line says what changed since it was last said. Cut is not lost: the brief's last line before "Full Plate" says `Held back: N things you've already heard (repeat check)`, so nothing vanishes silently. A Let-go item already vetoed is not re-proposed (graveyard `Vetoed` column). A nudge already drafted is not drafted again: drafting one writes today's date into its waiting-on `Nudged on`, and the due check (RULES §2c) holds that row back 7 days. Nagging is how a chief of staff gets ignored.
3. **Do the AUTO work.** File, sort, summarize, write into the workspace. Do it, then report it as DONE.
4. **Do the DRAFT work.** Replies and declines go into the connector's drafts folder or the workspace. Report each as DRAFTED, with where.
5. **Stop at NEEDS YOUR GO.** Collect them into one block at the top of the brief so the human can approve in one message. Do not act on any of them. Do not act on an approval you inferred.
6. **Nothing leaves the building.** No send, reply, post, pay, book, cancel, sign, delete. If a connector offers only a send tool, write the text into the brief instead.
7. **Short.** The brief fits on a phone screen above the fold: state line, next step, Keeps, the NEEDS YOUR GO block, the count of what you took. The full Plate is in `plate/plate.md`; link or name it.

## Inputs

- Mail: since yesterday's Plate (`inbox-sweep`).
- Calendar: today and the next two working days (`calendar-reality`).
- Due dates: the due check (RULES §2c) with a 2-day window.
- Workspace: the location the routine prompt names; if it names none, the RULES §2 lookup (`$OFF_MY_PLATE_DIR`, then an existing `./plate`, then `~/plate`). Never trust a location written inside `config.md` over the prompt; that file lives in the workspace it would be naming. In Claude Duet, this is a folder in a connected drive; Duet cannot read local files. If the workspace is unreachable, say so in the first line and build the best Plate you can from mail and calendar alone.

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

Then move yesterday's Plate to `history/plate-<its date>-<HHMM>.md`, write the full Plate to `plate/plate.md`, run the lint, run the dedupe check (rule 2), and have the `plate-reviewer` agent check it. If the reviewer returns NEEDS REVISION, fix and re-run once; if it fails twice, deliver the brief anyway with "UNREVIEWED: <reviewer's top defect>" as its last line. The lint is RULES §3a, and its date sweep comes first: every `YYYY-MM-DD` outside Evidence is either repeated exactly in Evidence or sits on a line labeled INFERENCE or ASSUMED. Then do the rest of the list. If the runtime has no plugin agents, end the brief with "UNREVIEWED: no reviewer agent in this runtime". That line is the only caveat: the brief's first line is still the state line, with no preamble about the runtime above it. A late brief is worse than a labeled one.

## Setting up the routine

When the human asks to set this up on a schedule, point them at the README section "Schedule it" (a Claude Code routine, Claude Duet, or, for a scheduled run on their own Mac, the scripted edition on GitHub), and write the prompt the runtime should fire:

> Run the `morning-plate` skill from the adhd-off-my-plate plugin. Workspace: <location>. Mail and calendar: use the connected tools, read only, drafts allowed, send nothing. Leave the brief as the task output.

Then confirm with them what schedule was actually created (time, timezone, days) by reading it back from the runtime, not from memory.
