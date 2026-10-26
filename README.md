# ADHD: Off My Plate?

A chief of staff for one ADHD brain, built as a Claude Code plugin and written to be ready for a proactive morning routine in Claude Duet (whether Duet runs plugin skills is unconfirmed; see DUET.md).

Here's the thing about every productivity tool you've ever rage-quit. You hand it forty tasks. It hands you forty tasks back, now with colors. That is not help. That is a mirror with a subscription fee.

A chief of staff does the opposite. You dump everything on the desk, and they hand you back **less**: the three things that matter, the one thing to do next, what they've already taken care of, and what you can stop pretending you're going to do. This plugin is that, for a brain that needs it most and gets it least.

> Status: v0.1.1 (2026-10-26). Built, linted, smoke-tested on the sample dump with no connectors, and independently reviewed through three passes to PASS ([REVIEW.md](REVIEW.md)). First live run on a real inbox and calendar 2026-10-22, reviewed to PASS. Public on GitHub; directory submission pending.

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
| `morning-plate` | The unattended version. No questions, assumptions labeled, AUTO and DRAFT done, NEEDS YOUR GO collected at the top of a phone-sized brief. |

Commands: `/plate`, `/morning`, `/let-go`, `/revive`, `/missing`.

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

Then `/plate` and paste your dump. First run copies `templates/` to `./plate/` and asks the three setup questions that matter.

## Verify

```bash
python3 scripts/check_plugin.py && claude plugin validate . --strict --profile directory
python3 scripts/plate_lint.py examples/sample-plate.md        # PASS
python3 scripts/plate_lint.py examples/sample-plate-bad.md    # FAIL, 13 planted defects
```

## What it will not do

Send, reply, post, pay, book, cancel, sign, or delete. Invent a deadline. Give you five options. Lecture you about consistency. Make a medical claim; brain states are a way to size a day, not a diagnosis.

Author: Inspired Spitfire. The Brain-State System (Feral, Froggy, Foggy, Fried) is her framework. Skill internals are plain so you can run them in your own voice.

She Rebels 🤘
