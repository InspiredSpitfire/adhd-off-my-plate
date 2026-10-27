#!/usr/bin/env python3
"""Self-test for the workspace scripts. Pins due.py, surfaced.py, and
init_workspace.py to the fixture workspace in examples/workspace/.

Run from anywhere: python3 scripts/selftest.py
Exit 0 = every check passed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "examples" / "workspace"
PY = sys.executable
results: list[tuple[bool, str]] = []


def run(script: str, *args: str, cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    full_env = {k: v for k, v in os.environ.items() if k != "OFF_MY_PLATE_DIR"}
    full_env.update(env or {})
    return subprocess.run([PY, str(ROOT / "scripts" / script), *args], cwd=cwd or ROOT,
                          capture_output=True, text=True, env=full_env)


def check(ok: bool, label: str) -> None:
    results.append((ok, label))


# due.py
out = run("due.py", str(FIX), "--today", "2026-10-20", "--json")
due = json.loads(out.stdout)["due"] if out.returncode == 0 else []
ids = [d["id"] for d in due]
check(ids == ["W-01", "W-02", "G-01", "L-01"], f"due.py window 3: expected W-01 W-02 G-01 L-01, got {ids}")
check(due and due[0]["days"] == -3, "due.py: W-01 is 3 days late")
wide = json.loads(run("due.py", str(FIX), "--today", "2026-10-20", "--within", "60", "--json").stdout)["due"]
wide_ids = {d["id"] for d in wide}
check({"W-04", "G-04"} <= wide_ids, "due.py window 60 adds W-04 and G-04")
check(not ({"W-03", "G-02", "G-03", "L-02", "L-03"} & wide_ids), "due.py skips done, never, vetoed, none, and blank rows")
check(run("due.py", "/nonexistent/workspace").returncode == 2, "due.py: a named workspace that does not exist fails, no fallback")

# surfaced.py
report = run("surfaced.py", str(FIX))
check(report.returncode == 0 and report.stdout.count("2x") == 2, "surfaced.py report: two items surfaced twice")
cand = run("surfaced.py", str(FIX), "--candidate", str(FIX / "plate.md"))
check(cand.returncode == 1 and cand.stdout.count("- REPEAT") == 2, "surfaced.py candidate: flea treatment and website flagged, exit 1")
check("tax" not in cand.stdout.lower(), "surfaced.py candidate: the new tax gap is not flagged")
high = run("surfaced.py", str(FIX), "--candidate", str(FIX / "plate.md"), "--threshold", "3")
check(high.returncode == 0, "surfaced.py candidate with threshold 3: nothing flagged")

# init_workspace.py
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    ws = tmp / "home-plate"
    first = run("init_workspace.py", str(ws), "--no-gitignore")
    expected = {"config.md", "plate.md", "later.md", "projects.md", "graveyard.md", "waiting-on.md", "parking-lot.md"}
    check(first.returncode == 0 and expected <= {p.name for p in ws.iterdir()}, "init: creates every template file")
    check(all((ws / d).is_dir() for d in ("history", "drafts", "notes")), "init: creates history, drafts, notes")
    check(not list(ws.rglob(".gitkeep")), "init: does not copy .gitkeep files")
    (ws / "config.md").write_text("MINE\n")
    (ws / "later.md").unlink()
    second = run("init_workspace.py", str(ws), "--no-gitignore")
    check((ws / "config.md").read_text() == "MINE\n", "init: second run never overwrites")
    check((ws / "later.md").exists() and "later.md" in second.stdout, "init: second run restores a missing file")

    repo = tmp / "some-project"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    run("init_workspace.py", str(repo / "plate"))
    ignore = (repo / ".gitignore").read_text() if (repo / ".gitignore").exists() else ""
    check("plate/" in ignore, "init: workspace inside a git repo is added to its .gitignore")
    again = run("init_workspace.py", str(repo / "plate"))
    check((repo / ".gitignore").read_text().count("plate/") == 1 and "already ignored" in again.stdout,
          "init: .gitignore line is added once")

# find_workspace honours $OFF_MY_PLATE_DIR
env_run = subprocess.run([PY, str(ROOT / "scripts" / "due.py"), "--today", "2026-10-20", "--json"],
                         cwd="/", capture_output=True, text=True,
                         env={**os.environ, "OFF_MY_PLATE_DIR": str(FIX)})
check(env_run.returncode == 0 and json.loads(env_run.stdout)["workspace"] == str(FIX.resolve()),
      "OFF_MY_PLATE_DIR is honoured")

# Regressions from the 0.2.0 review: each of these once failed.
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    ws = tmp / "reg"
    (ws / "history").mkdir(parents=True)
    (ws / "config.md").write_text("fixture\n")
    (ws / "waiting-on.md").write_bytes(
        "| ID | Who | What | Since | Nudge-by | Nudged on | Status |\n|---|---|---|---|---|---|---|\n"
        "| W-01 | Ana | Reply on A\\|B pricing | 2026-09-01 | 2026-12-30 |  | open |\n"
        "| W-02 | Bo | Contract | 2026-10-01 | 2026-10-18 |  | done 10/22 |\n".encode()
        + b"| W-03 | Caf\xe9 owner | Invoice | 2026-10-01 | 2026-10-19 |  | open |\n"
        + "| W-04 | Dee | Deck | 2026-10-01 | 2026-13-40 |  | open |\n".encode())
    (ws / "graveyard.md").write_text(
        "| ID | Item | Let go on | Revive-by (date or never) | Why | Who was told | Vetoed |\n|---|---|---|---|---|---|---|\n"
        "| G-01 | Old course | 2026-10-01 | 2026-10-19 | meh | nobody | no |\n")
    reg = run("due.py", str(ws), "--today", "2026-10-20", "--json")
    data = json.loads(reg.stdout) if reg.returncode == 0 else {"due": [], "warnings": []}
    reg_ids = [d["id"] for d in data["due"]]
    check("W-01" not in reg_ids, "due.py: an escaped \\| inside a cell does not shift columns")
    check("W-02" not in reg_ids, "due.py: status 'done 10/22' counts as closed")
    check("W-03" in reg_ids, "due.py: a non-UTF-8 byte does not crash the run")
    check(any("2026-13-40" in w for w in data["warnings"]), "due.py: an impossible date is warned about, not silently dropped")
    check("G-01" in reg_ids, "due.py: Vetoed 'no' is not a veto")
    bad_today = run("due.py", str(ws), "--today", "yesterday")
    check(bad_today.returncode == 2 and "Traceback" not in bad_today.stderr, "due.py: a bad --today is a clean usage error")
    missing_env = run("due.py", env={"OFF_MY_PLATE_DIR": str(tmp / "nope")})
    check(missing_env.returncode == 2, "OFF_MY_PLATE_DIR pointing nowhere fails instead of falling back")

    # Different errands that share two words are not repeats; a real rewording is.
    for name, items in [("plate-2026-10-01-0700.md", ["Dentist appointment Tuesday", "Pay car registration", "Electric bill overdue", "Jordan never replied about the workshop outline"]),
                        ("plate-2026-10-02-0700.md", ["Dentist appointment Tuesday", "Pay car registration", "Electric bill overdue", "Jordan still has not replied about the outline for the workshop"])]:
        (ws / "history" / name).write_text("# The Plate · " + name[6:16] + " · Brain: Feral\n\n## What you're missing\n" + "".join(f"- {i} · found in dump\n" for i in items))
    cand = ws / "candidate.md"
    cand.write_text("# The Plate · 2026-10-03 · Brain: Feral\n\n## What you're missing\n- Vet appointment Tuesday\n- Pay car insurance\n- Water bill overdue\n- Jordan has not replied about the workshop outline\n")
    dedupe = run("surfaced.py", str(ws), "--candidate", str(cand))
    flagged = dedupe.stdout
    check("Vet" not in flagged and "insurance" not in flagged and "Water" not in flagged,
          "surfaced.py: vet vs dentist, insurance vs registration, water vs electric are not repeats")
    check("Jordan" in flagged and dedupe.returncode == 1, "surfaced.py: the reworded Jordan nag is still a repeat")

    root_repo = tmp / "rootrepo"
    root_repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root_repo, check=True)
    at_root = run("init_workspace.py", str(root_repo))
    check("WARNING" in at_root.stdout and not (root_repo / ".gitignore").exists(),
          "init: a workspace at a repo root warns instead of writing a useless ./ ignore line")

failed = [label for ok, label in results if not ok]
for ok, label in results:
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
raise SystemExit(1 if failed else 0)
