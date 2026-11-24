#!/usr/bin/env python3
"""Self-test for straight talk: the always-on hook, the on/off script, the eval
harness (against a fake `claude`, so it is free), and the copies other agents read.

Run from anywhere: python3 scripts/selftest_straight.py
Exit 0 = every check passed.
"""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
results: list[tuple[bool, str]] = []

FAKE_CLAUDE = r'''#!/usr/bin/env python3
"""Stand-in for `claude -p`. Replies WITH or WITHOUT; as judge, prefers WITH
unless FAKE_MODE says otherwise. Counts every call in $FAKE_COUNT."""
import json, os, re, sys
prompt = sys.stdin.read()
args = sys.argv[1:]
with open(os.environ["FAKE_COUNT"], "a") as fh:
    fh.write("x")
mode = os.environ.get("FAKE_MODE", "good")
if mode == "crash":
    sys.exit(3)
if "## Reply A" in prompt:
    a = re.search(r"## Reply A\s+<reply>\n(.*?)\n</reply>", prompt, re.S).group(1)
    hi = {"correctness": 5, "actionability": 5, "honesty": 5, "safety": 5, "concision": 5, "blocker": False, "note": "fine"}
    lo = {"correctness": 4, "actionability": 3, "honesty": 4, "safety": 4, "concision": 2, "blocker": False, "note": "buried"}
    if mode == "blocker":
        hi = dict(hi, blocker=True, note="invented a cause")
    if mode == "worse":
        hi, lo = lo, hi
    scores = {"A": hi, "B": lo} if a.startswith("WITH ") else {"A": lo, "B": hi}
    text = "garbage, no json" if mode == "badjudge" else "Here you go:\n" + json.dumps(scores)
elif "--append-system-prompt" in args:
    text = "WITH skill reply"
else:
    text = "WITHOUT skill reply"
print(json.dumps({"type": "result", "result": text, "total_cost_usd": 0.01, "is_error": False}))
'''


def check(ok: bool, label: str) -> None:
    results.append((bool(ok), label))


def run(*cmd: str, env: dict | None = None) -> subprocess.CompletedProcess:
    full = dict(os.environ)
    full.update(env or {})
    return subprocess.run([PY, *cmd], capture_output=True, text=True, env=full, cwd=ROOT)


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    cfg = tmp / "claude-config"
    env = {"CLAUDE_CONFIG_DIR": str(cfg)}
    hook = str(ROOT / "hooks" / "always_on.py")
    toggle = str(ROOT / "scripts" / "straight_talk.py")
    flag = cfg / ".off-my-plate-straight-talk"

    # hook + toggle
    quiet = run(hook, env=env)
    check(quiet.returncode == 0 and quiet.stdout == "", "hook: no flag, no output, exit 0")
    status = run(toggle, "status", env=env)
    check(status.returncode == 0 and "always-on is off" in status.stdout, "toggle status: off before opt-in")
    on = run(toggle, "always", env=env)
    check(on.returncode == 0 and flag.is_file() and flag.stat().st_size == 0, "toggle always: writes one empty flag file")
    loud = run(hook, env=env)
    check(loud.returncode == 0 and loud.stdout.startswith("STRAIGHT TALK ON"), "hook: flag present, notice printed")
    check("## The rules" in loud.stdout and "\nname: straight-talk" not in loud.stdout,
          "hook: prints the rules without the frontmatter")
    check("stop straight talk" in loud.stdout and str(flag) in loud.stdout, "hook: says how to turn it off, and where the flag is")
    check("leave it off" in loud.stdout and "printed again" in loud.stdout,
          "hook: notice says it is printed again, and to honor an earlier off")
    check(len(loud.stdout) < 9000, f"hook: output stays under 9,000 characters ({len(loud.stdout)})")
    piped = subprocess.run(f'"{PY}" "{hook}" | true', shell=True, capture_output=True, text=True,
                           env={**os.environ, **env})
    check(piped.returncode == 0 and "Error" not in piped.stderr, "hook: a reader that hangs up early causes no error")
    check(run(toggle, "always", env=env).returncode == 0, "toggle always: safe to run twice")
    off = run(toggle, "never", env=env)
    check(off.returncode == 0 and not flag.exists(), "toggle never: removes the flag")
    check(run(toggle, "never", env=env).returncode == 0, "toggle never: safe when already off")
    check(run(hook, env=env).stdout == "", "hook: quiet again after never")
    check(run(toggle, "sometimes", env=env).returncode == 2, "toggle: unknown argument exits 2")
    blocked = tmp / "a-file"
    blocked.write_text("x")
    check(run(hook, env={"CLAUDE_CONFIG_DIR": str(blocked)}).returncode == 0, "hook: a broken config path still exits 0")
    hooks_json = json.loads((ROOT / "hooks" / "hooks.json").read_text())
    command = hooks_json["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    check("hooks/always_on.py" in command and "${CLAUDE_PLUGIN_ROOT}" in command, "hooks.json: SessionStart runs always_on.py from the plugin root")

    # eval harness, on a fake claude
    ev = str(ROOT / "scripts" / "straight_eval.py")
    fake = tmp / "claude"
    fake.write_text(FAKE_CLAUDE)
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    count = tmp / "count"

    def calls() -> int:
        return len(count.read_text()) if count.exists() else 0

    def eval_run(name: str, mode: str, *extra: str) -> subprocess.CompletedProcess:
        return run(ev, "run", "--claude", str(fake), "--trials", "2", "--cases", "direct-answer,fried",
                   "--out", str(tmp / name), *extra, env={"FAKE_COUNT": str(count), "FAKE_MODE": mode})

    val = run(ev, "validate")
    check(val.returncode == 0 and val.stdout.startswith("OK:"), "eval validate: cases and rubric are well formed")
    dry = eval_run("dry", "good")
    check(dry.returncode == 0 and calls() == 0 and not (tmp / "dry").exists() and "Nothing was run" in dry.stdout,
          "eval run without --go: makes no calls and writes nothing")
    good = eval_run("good", "good", "--go")
    check(good.returncode == 0 and calls() == 12, f"eval run --go: 2 cases x 2 trials = 12 calls, got {calls()}")
    report = (tmp / "good" / "RESULTS.md").read_text() if (tmp / "good" / "RESULTS.md").exists() else ""
    check("rules held" in report and "| **weighted** | | **3.550** | **5.000** | **+1.450** |" in report,
          "eval report: weighted scores are computed right and the rules held")
    check("PARTIAL RUN (2 of 20 cases, 2 trial(s))" in report and "Release gate: PASSED" not in report,
          "eval report: a run on some cases is labeled PARTIAL, never a passed release gate")
    rows = [json.loads(l) for l in (tmp / "good" / "rows.jsonl").read_text().splitlines()]
    orders = {r["order"]["A"] for r in rows}
    check(orders == {"with", "without"}, "eval: the judge sees the two conditions in shuffled order")
    check(all(r["scores"]["with"]["concision"] == 5 and r["scores"]["without"]["concision"] == 2 for r in rows),
          "eval: scores are mapped back to the right condition after the shuffle")
    before = calls()
    again = eval_run("good", "good", "--go")
    check(again.returncode == 0 and calls() == before, "eval: rerunning a finished run folder makes no new calls")
    rep = run(ev, "report", str(tmp / "good"))
    check(rep.returncode == 0, "eval report: rebuilds from a finished run")
    blk = eval_run("blocker", "blocker", "--go")
    check(blk.returncode == 1 and "rule 1" in blk.stdout, "eval gate: a new blocker with the skill fails rule 1")
    worse = eval_run("worse", "worse", "--go")
    check(worse.returncode == 1 and "rule 2" in worse.stdout and "rule 3" in worse.stdout,
          "eval gate: lower scores with the skill fail rules 2 and 3")
    before = calls()
    crash = eval_run("crash", "crash", "--go")
    check(crash.returncode == 1 and "INCOMPLETE" in crash.stdout, "eval gate: failed calls make the run INCOMPLETE, not a pass")
    check("Stopped early: 3 case-trials failed in a row" in crash.stdout and calls() - before == 6,
          "eval: stops after 3 failed case-trials in a row instead of burning the rest")
    with (tmp / "crash" / "rows.jsonl").open("a") as fh:
        fh.write('{"case": "direct-answer", "tri')  # a killed run's half-written line
    healed = eval_run("crash", "good", "--go")
    check(healed.returncode == 0 and "rules held" in healed.stdout and "INCOMPLETE" not in healed.stdout,
          "eval: rerunning the same folder retries the failed case-trials and survives a half-written line")
    before = calls()
    capped = eval_run("capped", "good", "--go", "--max-cost", "0.05")
    check("--max-cost $0.05 reached" in capped.stdout and calls() - before == 6 and capped.returncode == 1,
          "eval: --max-cost stops the run once the reported cost reaches it")
    full = run(ev, "run", "--claude", str(fake), "--trials", "3", "--out", str(tmp / "full"), "--go",
               env={"FAKE_COUNT": str(count), "FAKE_MODE": "good"})
    full_report = (tmp / "full" / "RESULTS.md").read_text() if (tmp / "full" / "RESULTS.md").exists() else ""
    check(full.returncode == 0 and "Release gate: PASSED" in full_report, "eval: a run on every case can pass the release gate")
    src = Path(ev).read_text()
    check(all(f in src for f in ('"--strict-mcp-config"', '"--tools", ""', '"--setting-sources", ""', '"--disable-slash-commands"')),
          "eval: asks claude for no tools, no MCP servers, no user settings, no slash commands")
    badj = eval_run("badjudge", "badjudge", "--go")
    check(badj.returncode == 1 and "INCOMPLETE" in badj.stdout, "eval gate: a judge reply that is not JSON is not scored")
    check(run(ev, "run", "--cases", "nope").returncode == 2, "eval: an unknown case id exits 2")
    check(run(ev, "report", str(tmp / "nothing-here")).returncode == 2, "eval report: a folder with no run exits 2")

# copies for other agents stay in step with the skill
skill = (ROOT / "skills" / "straight-talk" / "SKILL.md").read_bytes()
mirror = ROOT / ".cursor" / "skills" / "straight-talk" / "SKILL.md"
check(mirror.is_file() and mirror.read_bytes() == skill, "Cursor copy of straight-talk matches the skill byte for byte")
version = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]
for relative in (".codex-plugin/plugin.json", "gemini-extension.json", "qwen-extension.json", "kimi.plugin.json"):
    path = ROOT / relative
    try:
        other = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        other = {}
    check(other.get("name") == "adhd-off-my-plate" and other.get("version") == version,
          f"{relative}: name and version match the Claude manifest ({version})")
check("@./skills/straight-talk/SKILL.md" in (ROOT / "GEMINI.md").read_text() if (ROOT / "GEMINI.md").is_file() else False,
      "GEMINI.md imports the straight-talk skill")

failed = [label for ok, label in results if not ok]
for ok, label in results:
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
print(f"\n{len(results) - len(failed)} of {len(results)} checks passed.")
raise SystemExit(1 if failed else 0)
