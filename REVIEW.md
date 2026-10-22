# Review history

Independent reviews by a separate agent that did not build the plugin, against written acceptance criteria. PASS requires zero MAJOR defects.

| Date | Pass | Verdict | What it found |
|---|---|---|---|
| 2026-10-22 | 1 | NEEDS REVISION | 5 MAJOR: Fried rules disagreed across files; lint missed email/text/share/schedule/order/submit; a "not today" substring disabled Revive checks; revive-one drafted a calendar invite (which sends); some Duet claims unsourced. 12 MINOR. Plus a separate smoke test of `plate-triage` on the sample dump: lint PASS first try, 14 ambiguities in the skill text. |
| 2026-10-22 | 2 | NEEDS REVISION | Original 5 fixed. 2 new MAJOR, both in the lint: Fried sentinel not enforced when a full Revive block is written; "draft it and email it" passed at DRAFT. 11 MINOR. |
| 2026-10-22 | 3 | NEEDS REVISION | Lint only. Both wave-2 MAJORs fixed. 1 new MAJOR: the sticky-note noun exception also swallowed the verb phrase "post it". 3 MINOR (verb-list gaps, hyphenated noun collisions). |
| 2026-10-22 | 3b | PASS | Same reviewer re-ran its full test set (lint-tests t01–t10, r3 a00–a08, b01, c01–c06, d01–d22, both examples): every file matched its expectation, zero MAJOR. |

**Status:** every MAJOR from passes 1–3 is closed and the lint holds PASS on the reviewer-authored test set. Known MINOR limits: the outward-verb check is a heuristic (RULES §3 says so; the `plate-reviewer` agent covers the rest), and the plugin has not yet run against a live inbox or calendar. First live run is the next verification step.
