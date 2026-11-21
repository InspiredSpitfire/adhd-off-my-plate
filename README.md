# ADHD: Off My Plate

A chief of staff for one ADHD brain, built as a Claude Code plugin and written to be ready for a proactive morning routine in Claude Duet (whether Duet runs plugin skills is unconfirmed; see DUET.md).

Here's the thing about every productivity tool you've ever rage-quit. You hand it forty tasks. It hands you forty tasks back, now with colors. That is not help. That is a mirror with a subscription fee.

A chief of staff does the opposite. You dump everything on the desk, and they hand you back **less**: the three things that matter, the one thing to do next, what they've already taken care of, and what you can stop pretending you're going to do. This plugin is that, for a brain that needs it most and gets it least.

> Status: v0.2.4 (2026-11-21), the directory edition. Built, linted, smoke-tested on the sample dump with no connectors, and independently reviewed through three passes to PASS ([REVIEW.md](REVIEW.md)). First live run on a real inbox and calendar 2026-10-22, reviewed to PASS.
>
> **Two editions.** This one is all Markdown: no scripts, so it runs anywhere Claude does, Cowork and Duet included, and it is the one in the Claude plugin directory. Every check is a written procedure Claude follows step by step. The [scripted edition](https://github.com/InspiredSpitfire/adhd-off-my-plate) on GitHub's main branch does the same counting in code (a lint script, a due-date counter, a repeat finder) and adds a scheduler example and a Duet sandbox. Same skills, same Plate.

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

Here's the middle of a real one, from a Foggy Tuesday ([the whole Plate](examples/sample-plate.md)):

```markdown
## Keep (2 real hours, longest block 75 min)
1. Send the agency invoice once the draft is in your inbox: $1,200 outstanding,
   and money outranks everything else on the list today.
2. Text the dentist back with one of the two offered times.

## Let go
- Redo the whole website → graveyard · revive-by: 2026-12-01 · Nobody is waiting,
  and "redo everything" is what a Foggy brain reaches for instead of the invoice.

## Next step
> Go to the car and get the permission slip. Put it in your bag. (3 min)
```

Seventeen things went into that dump. Two made Keep, plus a permission slip.

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
| `morning-plate` | The unattended version. No questions, assumptions labeled, AUTO and DRAFT done, NEEDS YOUR GO collected at the top of a phone-sized brief. Cuts anything it already told you twice (the repeat check). |

Commands: `/setup`, `/plate`, `/morning`, `/due`, `/let-go`, `/revive`, `/missing`.

## Written for Claude Duet

Duet is a proactive agent that runs on its own cloud machine, checks your connected apps every few hours, sends a morning brief, and asks before it sends, pays, or deletes (per launch coverage, sources in DUET.md). That is exactly the shape of `morning-plate`. Whether Duet can run a plugin skill inside a routine is not confirmed by anything published; the routine prompt is written so it works pasted as plain instructions either way. See [DUET.md](DUET.md) for the mapping, with every Duet fact labeled by source, and for the parts Duet can't do yet.

**No Duet invite yet? Same.** So the scripted edition has a [sandbox](https://github.com/InspiredSpitfire/adhd-off-my-plate/tree/main/sandbox) that fakes Duet's working conditions:
- nobody watching
- no local files
- no shell
- a fake inbox with send, trash, and forward buttons that answer like the real thing, and pressing one fails the run
- a second check-in after new mail lands

It grades every run. Two Duet-profile runs on Opus (2026-10-28, four check-ins in all) went like this. The first ran on an earlier version of the sandbox that loaded the plugin in place, so re-grading it today also fails the newer isolation checks. Its behavior below still stands: it had only the fake connectors, no shell, and it read nothing but the plugin's public rulebook.
- zero outward calls
- the scam email flagged every time, never obeyed
- the triple-booking caught
- the previous Plate moved to history
- one real gap, twice: with no shell to lint itself, two of the four check-ins shipped a Plate with a single date that was neither quoted in Evidence nor labeled as reasoning

The local scheduled-run profile, which can lint itself, passed clean.

**Then we fixed the gap and ran it again.** RULES §3a now spells out the lint as a by-hand checklist for runtimes with no shell, with the date sweep first. In this edition that checklist is the lint everywhere. It took three rounds of runs to get the wording right:

| Wording | Check-ins | Lint passed | What still slipped |
|---|---|---|---|
| Before the fix | 4 | 2 | two unlabeled dates |
| First draft | 4 | 1 | no dates; three draft items described an action ("a request to move the sync"), and one brief opened with a preamble |
| Final checklist | 4 | 4 | two briefs opened with a preamble instead of the state line |
| Final, with the draft and first-line rules | 4 | 4 | nothing: every hard check passed, zero warnings |

Four clean check-ins is evidence, not proof. The sandbox is in the scripted edition if you want to add your own.

## Install

From the Claude plugin directory, once it is listed: search for ADHD: Off My Plate.

The scripted edition, from GitHub, inside Claude Code:

```
/plugin marketplace add InspiredSpitfire/adhd-off-my-plate
/plugin install adhd-off-my-plate@adhd-off-my-plate
```

Or from a terminal:

```bash
claude plugin marketplace add InspiredSpitfire/adhd-off-my-plate
claude plugin install adhd-off-my-plate@adhd-off-my-plate
```

Then `/setup`. It makes your workspace at `~/plate`, never inside whatever project folder you happen to be standing in, keeps it out of git, and asks the three questions that size every Plate. Skip any of them and it guesses, out loud.

## Try it in 2 minutes

No inbox, no calendar, no commitment. Just watch it take a mess and hand back less.

1. `/setup` and say "skip" to all three questions.
2. `/plate foggy`, then paste the fake brain dump from [examples/sample-brain-dump.md](examples/sample-brain-dump.md). It's a stranger's Tuesday: an unsent invoice, a dentist who won't stop texting, a course page stuck at 80% for two months, a dog who needs flea meds.
3. You get one Plate back. Compare it to [examples/sample-plate.md](examples/sample-plate.md): two Keeps (Foggy gets two), one next step under ten minutes, the website rebuild in the graveyard with a revival date, the course page revived with one eight-minute text.
4. `/due` counts the dates in your workspace, step by step: overdue nudges, graveyard items due back, deadlines. Empty on day one. That's the point.

When it lands, swap the fake dump for your real one and connect mail and calendar.

## Schedule it

`morning-plate` is built to run with nobody watching: no questions, assumptions labeled, AUTO and DRAFT work done, every NEEDS YOUR GO collected at the top of a phone-sized brief. Three ways to run it, most tested first.

**1. On your own machine.** Use the [scripted edition](https://github.com/InspiredSpitfire/adhd-off-my-plate#schedule-it): it ships `morning.sh` and a launchd example, tested 2026-10-27 with Claude Code 2.1.310. A scheduled run on your own Mac needs a script to start it, and this edition ships none.

**2. A Claude Code routine in the cloud.** Not tested. A cloud routine cannot read `~/plate` on your machine, so the workspace has to live somewhere it can reach, the same constraint as Claude Duet.

**3. Claude Duet.** Not tested; Duet is a waitlisted preview. Paste the routine prompt from the `morning-plate` skill ("Setting up the routine") and name a connected-drive folder as the workspace. See [DUET.md](DUET.md).

## Verify

```bash
claude plugin validate . --strict --profile directory
```

The scripted edition's lint and self-tests run against the same `examples/`: `sample-plate.md` passes, `sample-plate-bad.md` fails with 13 planted defects. Run RULES §3a on either by hand and you should get the same answers.

## Privacy

What it reads: what you paste into a Claude Code session, the plugin's own files, your workspace (`~/plate` unless you name another folder, including its history, notes, and drafts), any other folder or repo you point it at, and, only if you have connected them in Claude yourself, your mail and calendar through your own connectors. It reads mail and calendar; it never sends, replies, RSVPs, trashes, or deletes. Reply and decline drafts go into your mail connector's drafts folder or your workspace, and you send them.

What it stores: the Plate, its history, notes, drafts, and tables, as plain Markdown in your workspace on your own disk (or the connected-drive folder you name for Claude Duet). Setup adds the workspace path to the `.gitignore` of a git repo that contains the workspace. Nothing else.

What leaves your machine: only what Claude itself processes under your Claude account, and the drafts your connectors save in your own accounts. Nothing goes to the plugin's author. No telemetry, no analytics, no accounts. It ships no scripts, so nothing in it opens a network connection.

## What it will not do

Send, reply, post, pay, book, cancel, sign, or delete. Invent a deadline. Give you five options. Lecture you about consistency. Make a medical claim; brain states are a way to size a day, not a diagnosis.

Author: Inspired Spitfire. The Brain-State System (Feral, Froggy, Foggy, Fried) is her framework. Skill internals are plain so you can run them in your own voice.

She Rebels 🤘
