# Changelog

All notable changes to this plugin. Dates are release dates.

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
