# Review history

Independent reviews by a separate agent that did not build the plugin, against written acceptance criteria. PASS requires zero MAJOR defects.

| Date | Pass | Verdict | What it found |
|---|---|---|---|
| 2026-10-22 | 1 | NEEDS REVISION | 5 MAJOR: Fried rules disagreed across files; lint missed email/text/share/schedule/order/submit; a "not today" substring disabled Revive checks; revive-one drafted a calendar invite (which sends); some Duet claims unsourced. 12 MINOR. Plus a separate smoke test of `plate-triage` on the sample dump: lint PASS first try, 14 ambiguities in the skill text. |
| 2026-10-22 | 2 | NEEDS REVISION | Original 5 fixed. 2 new MAJOR, both in the lint: Fried sentinel not enforced when a full Revive block is written; "draft it and email it" passed at DRAFT. 11 MINOR. |
| 2026-10-22 | 3 | NEEDS REVISION | Lint only. Both wave-2 MAJORs fixed. 1 new MAJOR: the sticky-note noun exception also swallowed the verb phrase "post it". 3 MINOR (verb-list gaps, hyphenated noun collisions). |
| 2026-10-22 | 3b | PASS | Same reviewer re-ran its full test set (lint-tests t01–t10, r3 a00–a08, b01, c01–c06, d01–d22, both examples): every file matched its expectation, zero MAJOR. |
| 2026-10-22 | live | PASS (after one revision) | First live run on the owner's real Gmail, Google Calendar, school tracker, and dump. `plate-reviewer` returned NEEDS REVISION (6 MAJOR: an unsourced URL, an overreaching money bullet, an unlabeled assumption, an unsupported attendee, drafts claimed before they existed, an embellished line in a draft), all fixed, then PASS. Lesson written into RULES §3b: present before you draft. |
| 2026-10-26 | 0.1.1 | NEEDS REVISION → fixes applied | Submission readiness: validator, icon, version consistency, public hygiene all PASS. 2 MAJOR doc fixes: this table was stale, and the listing copy stated Duet compatibility as fact. Re-check: PASS. |
| 2026-10-27 | 0.2.0 | NEEDS REVISION | Five new pieces (dedupe, due dates, /setup, walkthrough, schedule recipe). 6 MAJOR: dedupe flagged different errands as repeats, an escaped pipe shifted columns, the schedule recipe allowed any `python3` command despite claiming sends and deletes could never run, a lookup-order contradiction, a missing `$OFF_MY_PLATE_DIR` silently fell back to another workspace, a stray byte crashed `due.py`. |
| 2026-10-27 | 0.2.0 re-check | PASS | All six fixed and pinned in `selftest.py` (27 checks). The reviewer reran its full break table. The allow-list now permits three scripts by exact path; denial of quoted paths, `python3 -c`, and chained commands was tested separately, and the whole recipe was run end to end. |

**Status:** every MAJOR from every pass is closed. Known MINOR limits: the outward-verb check is a heuristic (RULES §3 says so; the `plate-reviewer` agent covers the rest), and whether Claude Duet runs plugin skills inside a routine is unconfirmed (DUET.md).
