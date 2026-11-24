# Straight talk eval

One question: are replies better with the straight-talk rules than without them?

## What it does

For each case in `cases.jsonl`, each trial:

1. `claude -p` answers the message, asked for with no tools, no MCP servers, no user settings, and no plugins. That is **without**.
2. It answers the same message again with the straight-talk rules appended to the system prompt. That is **with**.
3. A separate judge call gets both replies as `A` and `B`, in shuffled order, plus the case's criteria and the block of `rubric.md` between the `judge:` markers. It is never told which is which.

`RESULTS.md` in the run folder has the scores per dimension, per case, the blockers, and the release gate from `rubric.md`.

## Run it

```bash
python3 scripts/straight_eval.py validate
```

```bash
python3 scripts/straight_eval.py run
```

That second one only prints the call count. A full run is 20 cases x 3 trials x 3 calls = 180 calls on your own Claude login. To spend them:

```bash
python3 scripts/straight_eval.py run --go
```

Cheaper first look: `--trials 1` (60 calls), or `--cases fried,error-unknown-cause,casual` (either one is reported as PARTIAL, never as a passed gate). `--model` and `--judge-model` pick the models (default `opus` for both). `--max-cost 5` stops the run once the reported cost reaches five dollars; without it there is no cap. The run also stops by itself after 3 failed case-trials in a row. Pass the same `--out` folder to carry on: scored case-trials are skipped, failed ones are tried again. Run folders land in `evals/runs/`, which is not committed.

## Limits, said up front

- **The isolation is unconfirmed.** The harness passes `--tools ""`, `--strict-mcp-config`, `--setting-sources ""`, and `--disable-slash-commands`. Until a real run shows otherwise, assume your own global instructions or connectors could reach both conditions.
- **It partly grades its own homework.** The judge sees each case's criteria, and many of them describe the shape the rules ask for (numbered steps, action first). A higher score partly means "followed the rules". Correctness, honesty, and safety are the columns without that problem.
- The judge is a Claude model grading Claude replies.
- Three trials is few. A single-case change under about 0.5 is noise.
- No tools, so this grades the reply, not the work.
- `persistence`, `off-phrase`, and `still-broken` are transcripts pasted into one message, not real multi-turn sessions. Nothing here tests the mode surviving a real long conversation, or the always-on hook.
- Not covered by any case: the app's own instructions overriding a rule, and a Plate taking over the reply.
- No token or cost comparison between the two conditions, only the total reported cost.
- Brain-state sizing is tested by one case (`fried`). The Plate itself is tested elsewhere (`plate_lint.py`, `sandbox/`).

## Status

Harness self-tested against a fake `claude` (`scripts/selftest_straight.py`). No real run yet, so there are no results to report.
