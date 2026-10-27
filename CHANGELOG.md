# Changelog

All notable changes to this plugin. Dates are release dates.

## [0.2.0] - 2026-10-27

### Added
- `scripts/due.py` and `/due`: overdue nudges, graveyard items due back, and later-list deadlines, counted from the workspace tables instead of eyeballed. `whats-missing` and `morning-plate` cite its output.
- `scripts/surfaced.py`: dedupe across the last 7 Plates. Matches reworded repeats by shared words (at least three), so "flea treatment for the dog is still overdue" counts as the same nag as "dog's flea treatment is a month overdue", while "vet appointment Tuesday" and "dentist appointment Tuesday" stay two different errands. `morning-plate` cuts every repeat unless its deadline is inside 48 hours or the Plate says what changed, and the brief says how many it held back; `plate-reviewer` treats a kept repeat as a defect.
- `scripts/init_workspace.py` and `/setup`: the workspace defaults to `~/plate` (or `$OFF_MY_PLATE_DIR`), never the current project folder; never overwrites; adds itself to `.gitignore` when it sits inside a repo.
- `scripts/selftest.py` and a fixture workspace in `examples/workspace/`: 27 checks pin all three scripts, including every break case the independent review found (escaped pipes, non-UTF-8 bytes, impossible dates, a missing `$OFF_MY_PLATE_DIR`, a workspace at a repo root, short look-alike items).
- README "Try it in 2 minutes" and "Schedule it", with `examples/morning.sh` and a launchd example. The unattended recipe allows only reads and writes inside the workspace, reads of the plugin, the three scripts by exact path, and four mail and calendar read tools; every fence was tested on its own, and the whole recipe was run end to end on 2026-10-27.

### Changed
- History files are `plate-YYYY-MM-DD-HHMM.md`, so two runs on one day never overwrite each other.
- Workspace lookup (RULES §2): a location the routine prompt names wins, then `$OFF_MY_PLATE_DIR`, then an existing `./plate`, then `~/plate`. A named path or `$OFF_MY_PLATE_DIR` that does not exist fails instead of falling back to someone's real workspace.
- RULES §2: scripts are called with literal, unquoted absolute paths, one command per call, because unattended `dontAsk` runs deny shell variables, quoted paths, chained commands, and `python3 -c`.

## [0.1.1] - 2026-10-26

### Added
- Directory listing icon: `.claude-plugin/icon.png` (1024 px, one plate, one thing left on it, in the brand palette), editable source at `assets/icon.svg`.
- `LICENSE` (MIT), this changelog, and `homepage` / `repository` / `license` / `icon` in `plugin.json`.
- README install line for the one-step marketplace install.

### Changed
- RULES §3b and `plate-triage` Step 8: present the Plate the moment the lint passes, drafts after. Learned on the first live run (2026-10-22), when the Plate reached the human after the meeting it was meant to prepare.
- Repo rules moved from the plugin root to `.claude/CLAUDE.md` so the plugin validator stops warning; `AGENTS.md` follows it.

## [0.1.0] - 2026-10-22

### Added
- Seven skills (`plate-triage`, `inbox-sweep`, `calendar-reality`, `let-it-go`, `revive-one`, `whats-missing`, `morning-plate`), five commands, the `plate-reviewer` agent, workspace templates, `plate_lint.py`, fixtures with planted defects, and `DUET.md`.
- Three independent review passes to PASS; one live run on a real inbox and calendar, reviewed to PASS.
