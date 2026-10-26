# ADHD: Off My Plate? (Claude Code plugin)

A chief of staff for one ADHD brain. Product name: **ADHD: Off My Plate?** (named by Inspired Spitfire 2026-10-22). Slug: `adhd-off-my-plate`. Status: v0.1.1 (2026-10-26). Public at github.com/InspiredSpitfire/adhd-off-my-plate since 2026-10-22 (pushed on the owner's explicit go). First live run on the owner's real inbox and calendar 2026-10-22, reviewed to PASS. Directory submission pending. Built as the demo for the owner's Claude Duet application: the `morning-plate` skill is the routine Duet would run each morning on its own cloud machine.

## Layout
- `RULES.md` — the shared rulebook every skill reads: workspace, the Plate format, approval gates, evidence labels, brain-state sizing, the graveyard. Change rules here, not in seven places.
- `skills/` — seven skills. `plate-triage` is the product; the other six are its organs and also run alone.
- `agents/plate-reviewer.md` — independent PASS / NEEDS REVISION reviewer. Runs `scripts/plate_lint.py` and judges the Plate against the workspace.
- `commands/` — `/plate`, `/morning`, `/let-go`, `/revive`, `/missing`.
- `templates/` — blank workspace files copied on first run.
- `examples/` — a sample brain dump, a passing Plate, and a Plate with planted defects. The lint must keep catching them.
- `scripts/check_plugin.py` — component reachability check. `scripts/plate_lint.py` — structural check of a Plate.
- `DUET.md` — how this runs inside Claude Duet, with every Duet fact labeled by source.

## Rules
- The Plate has exactly one next step. Not a menu. The lint enforces it; do not soften the lint.
- Nothing is sent, paid, booked, cancelled, or deleted by this plugin. Every "off my plate" item carries a gate: `AUTO` (reading, sorting, filing, writing into the workspace), `DRAFT` (text only; the human sends), `NEEDS YOUR GO` (anything that leaves the building). The lint fails outward verbs at AUTO or DRAFT by heuristic; the reviewer agent reads the rest.
- Letting go is a move to the graveyard with a revive-by date or `never`. It is not deletion. Revival rights are the whole reason an ADHD brain can let go.
- The Brain-State System (Feral, Froggy, Foggy, Fried) is Inspired Spitfire's framework: four states, never renamed, definitions in RULES §5 and authoritative in `she-rebels-brand-kit`. Skill internals stay plain so any user can run them in their own voice.
- Never invent a deadline, a sender, a commitment, or a calendar event. Everything in a Plate is EVIDENCE (quoted), INFERENCE (reasoned, stated), or ASSUMED (a guess the human can correct).
- No medical or diagnostic claims anywhere. Brain states are a way to size a day, not treatment.
- After any change run `python3 scripts/check_plugin.py && claude plugin validate . --strict --profile directory` and the three lint commands in README "Verify".
- Publishing, pushing to a public repo, submitting to a marketplace, or listing for sale is an outward action: needs the owner's explicit go.
- Rules live in `.claude/CLAUDE.md` (plugin validator warns on a root CLAUDE.md); `AGENTS.md` symlinks to it. The listing icon is `.claude-plugin/icon.png`, rendered from `assets/icon.svg` with `qlmanage -t -s 1024 -o .claude-plugin assets/icon.svg` (rename the output); the directory keeps the first submitted icon permanently.
- README, DUET.md pitch copy, and launch posts are Inspired Spitfire territory: load `she-rebels-brand-kit` before editing them. Public author name is "Inspired Spitfire", never a legal name.
