# ADHD: Off My Plate?

A chief of staff for one ADHD brain, built as a Claude Code plugin and written to be ready for a proactive morning routine in Claude Duet (whether Duet runs plugin skills is unconfirmed; see DUET.md).

Here's the thing about every productivity tool you've ever rage-quit. You hand it forty tasks. It hands you forty tasks back, now with colors. That is not help. That is a mirror with a subscription fee.

A chief of staff does the opposite. You dump everything on the desk, and they hand you back **less**: the three things that matter, the one thing to do next, what they've already taken care of, and what you can stop pretending you're going to do. This plugin is that, for a brain that needs it most and gets it least.

> Status: v0.2.0 (2026-10-27). Built, linted, smoke-tested on the sample dump with no connectors, and independently reviewed through three passes to PASS ([REVIEW.md](REVIEW.md)). First live run on a real inbox and calendar 2026-10-22, reviewed to PASS. Public on GitHub; directory submission pending.

## What you hand it

→ A messy brain dump (paste it; grammar optional)
→ A to-do list that is too long (they all are)
→ Your inbox, through a connected mail tool, or pasted
→ Your calendar, through a connected calendar tool, or pasted
→ The projects you never finished (it will build the list if you don't have one)
→ One word: which brain showed up today

## What you get back: one Plate

| Section | What it answers |
|---|---|
| **Off my plate** | What Claude is taking off you right now, each item tagged `AUTO`, `DRAFT`, or `NEEDS YOUR GO` |
| **Keep** | The 1 to 3 things that actually need your hands today. Fried days get 1. |
| **Let go** | What to drop, with a revive-by date or `never`. Letting go is not deleting. |
| **Next step** | One physical action, ten minutes or less. One. The lint fails a Plate with two. |
| **Revive one** | One unfinished project, why it stalled, one tiny step that un-sticks it |
| **What you're missing** | Commitments with no task, deadlines with no slot, people waiting, money on the table, the dog |

Then it does the AUTO and DRAFT work and stops at every NEEDS YOUR GO: it hands you the final text and tells you exactly where to click. The plugin itself never sends, pays, books, cancels, or deletes; those are your hands, every time.

## Why it isn't a prompt

| A prompt | Off My Plate |
|---|---|
| "Be my assistant" in a chat box | Seven skills that read one shared workspace and one rulebook |
| Gives you a prioritized list | Gives you a **shorter** list and makes the demotions for you |
| "Don't send anything" is a sentence you hope it read | Every item carries a gate; a script fails items whose verb leaves the building but are marked AUTO or DRAFT, and a reviewer agent reads the rest |
| Deletes what you drop | Moves it to a **graveyard** with revival rights; you can let go because it isn't gone |
| Assumes you're the same person every day | Sizes the day to **Feral, Froggy, Foggy, or Fried** you |
| "Here are 5 next steps" | **One** next step. A list of options is a decision, and a decision is the thing this brain can't spare |
| Grades its own work | An independent reviewer agent returns PASS or NEEDS REVISION |
| Nags you about the same thing daily | Reads the last 7 Plates and stays quiet about what it already said |

## The skills

| Skill | What it does |
|---|---|
| `plate-triage` | The whole thing. Dump + inbox + calendar + projects in, one Plate out. |
| `inbox-sweep` | Inbox → what you owe people, what they owe you, decisions, money, archive-unread. Drafts replies. Sends nothing. |
| `calendar-reality` | Calendar → the real hours you have today, as arithmetic, plus conflicts, prep, and declines. |
| `let-it-go` | The drop audit. Three questions per item. Graveyard with revive-by dates. Decline text drafted. |
| `revive-one` | One stalled project, one-clause diagnosis, one ten-minute step that addresses the reason it stalled. |
| `whats-missing` | Eight cross-checks for what fell through the cracks, each hit with its source. |
| `morning-plate` | The unattended version. No questions, assumptions labeled, AUTO and DRAFT done, NEEDS YOUR GO collected at the top of a phone-sized brief. Cuts anything it already told you twice (`scripts/surfaced.py`). |

Commands: `/setup`, `/plate`, `/morning`, `/due`, `/let-go`, `/revive`, `/missing`.

## Written for Claude Duet

Duet is a proactive agent that runs on its own cloud machine, checks your connected apps every few hours, sends a morning brief, and asks before it sends, pays, or deletes (per launch coverage, sources in DUET.md). That is exactly the shape of `morning-plate`. Whether Duet can run a plugin skill inside a routine is not confirmed by anything published; the routine prompt is written so it works pasted as plain instructions either way. See [DUET.md](DUET.md) for the mapping, with every Duet fact labeled by source, and for the parts Duet can't do yet.

## Install

One step, inside Claude Code:

```
/plugin install adhd-off-my-plate --marketplace InspiredSpitfire/adhd-off-my-plate
```

Or from a terminal:

```bash
claude plugin marketplace add InspiredSpitfire/adhd-off-my-plate
claude plugin install adhd-off-my-plate
```

Then `/setup`. It makes your workspace at `~/plate`, never inside whatever project folder you happen to be standing in, keeps it out of git, and asks the three questions that size every Plate. Skip any of them and it guesses, out loud.

## Try it in 2 minutes

No inbox, no calendar, no commitment. Just watch it take a mess and hand back less.

1. `/setup` and say "skip" to all three questions.
2. `/plate foggy`, then paste the fake brain dump from [examples/sample-brain-dump.md](examples/sample-brain-dump.md). It's a stranger's Tuesday: an unsent invoice, a dentist who won't stop texting, a course page stuck at 80% for two months, a dog who needs flea meds.
3. You get one Plate back. Compare it to [examples/sample-plate.md](examples/sample-plate.md): two Keeps (Foggy gets two), one next step under ten minutes, the website rebuild in the graveyard with a revival date, the course page revived with one eight-minute text.
4. `/due` runs `scripts/due.py` on your workspace: overdue nudges, graveyard items due back, deadlines. Empty on day one. That's the point.

When it lands, swap the fake dump for your real one and connect mail and calendar.

## Schedule it

`morning-plate` is built to run with nobody watching: no questions, assumptions labeled, AUTO and DRAFT work done, every NEEDS YOUR GO collected at the top of a phone-sized brief. Three ways to run it, most tested first.

**1. On your own machine.** Tested 2026-10-27 with Claude Code 2.1.310; see "What the test showed" below.

Copy [examples/morning.sh](examples/morning.sh) to `~/plate/morning.sh`. It finds the installed plugin, then runs, in effect:

```bash
claude -p "/adhd-off-my-plate:morning $HOME/plate" --permission-mode dontAsk --allowedTools "Read(/$HOME/plate/**)" "Read(/$PLUGIN/**)" "Edit(/$HOME/plate/**)" "Skill" "Agent" "Bash(python3 $PLUGIN/scripts/plate_lint.py:*)" "Bash(python3 $PLUGIN/scripts/due.py:*)" "Bash(python3 $PLUGIN/scripts/surfaced.py:*)" "mcp__claude_ai_Gmail__search_threads" "mcp__claude_ai_Gmail__get_thread" "mcp__claude_ai_Google_Calendar__list_calendars" "mcp__claude_ai_Google_Calendar__list_events" < /dev/null
```

The safety is in `dontAsk`: anything not on that list is denied, not asked about. No send, delete, RSVP, or pay tool is on it. Reads stay inside your workspace and the plugin; writes stay inside your workspace (`Edit(...)` covers writes; a `Write(...)` rule does nothing). The only commands it can run are the plugin's three read-and-report scripts, by exact path. A `python3 -c` one-liner, a quoted path, or a script call with a second command chained on is denied.

Four things we learned the hard way running it headless, so you don't have to:
- **Name the workspace in the prompt.** An unattended run has no shell to read environment variables, so without the path it goes looking for one.
- **No `$VARIABLES` and no quotes in script commands.** `dontAsk` denies both. The rulebook tells the skills to write literal, unquoted paths.
- **`< /dev/null`**, or `claude -p` waits for input that never comes.
- **Your own hooks still run.** If you gate MCP tools with a PreToolUse hook, headless runs name your connectors `mcp__claude_ai_Gmail__*` and `mcp__claude_ai_Google_Calendar__*`, which can differ from the names the desktop app uses. Allow the read tools under those names too, or the brief says mail and calendar were unreachable.

What the test showed: a full run of `morning.sh` against a fictional test workspace exited cleanly, wrote only inside that workspace, produced a lint-clean Plate and a phone-sized brief, and `surfaced.py` found no repeats on the new Plate. Each fence above was tested on its own. On the test machine its own MCP-gating hook blocked the connector reads, so the mail and calendar path is verified up to the permission layer, not against a live inbox.

Then schedule the script. On a Mac, use launchd, because it runs a missed job when the laptop wakes up and cron just shrugs: edit and load [examples/com.offmyplate.morning.plist](examples/com.offmyplate.morning.plist) (instructions inside). On Linux, cron:

```bash
30 6 * * 1-5 /bin/sh "$HOME/plate/morning.sh"
```

The brief lands in `~/plate/notes/brief-YYYY-MM-DD.md`.

**2. A Claude Code routine in the cloud.** Not tested. A cloud routine cannot read `~/plate` on your machine, so the workspace has to live somewhere it can reach, the same constraint as Claude Duet.

**3. Claude Duet.** Not tested; Duet is a waitlisted preview. Paste the routine prompt from the `morning-plate` skill ("Setting up the routine") and name a connected-drive folder as the workspace. See [DUET.md](DUET.md).

## Verify

```bash
python3 scripts/check_plugin.py && claude plugin validate . --strict --profile directory
python3 scripts/plate_lint.py examples/sample-plate.md        # PASS
python3 scripts/plate_lint.py examples/sample-plate-bad.md    # FAIL, 13 planted defects
python3 scripts/selftest.py                                   # due.py, surfaced.py, init_workspace.py: all checks PASS
```

## What it will not do

Send, reply, post, pay, book, cancel, sign, or delete. Invent a deadline. Give you five options. Lecture you about consistency. Make a medical claim; brain states are a way to size a day, not a diagnosis.

Author: Inspired Spitfire. The Brain-State System (Feral, Froggy, Foggy, Fried) is her framework. Skill internals are plain so you can run them in your own voice.

She Rebels 🤘
