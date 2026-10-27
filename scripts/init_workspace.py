#!/usr/bin/env python3
"""Create the Off My Plate workspace, safely.

Default location is ~/plate (or $OFF_MY_PLATE_DIR), not the current folder, so
a brain dump, an inbox ledger, and a list of people who owe you money never land
inside some project repo by accident. Never overwrites: on a second run it only
adds template files that are missing. If the workspace sits inside a git repo,
it adds the workspace to that repo's .gitignore (pass --no-gitignore to skip).

Usage: python3 scripts/init_workspace.py [PATH] [--no-gitignore]
"""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from _ws import PLUGIN_ROOT

TEMPLATES = PLUGIN_ROOT / "templates"


def git(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def ensure_ignored(workspace: Path) -> str:
    top = git("rev-parse", "--show-toplevel", cwd=workspace)
    if top.returncode != 0:
        return "not inside a git repo; nothing to ignore"
    root = Path(top.stdout.strip()).resolve()
    if git("check-ignore", "-q", str(workspace), cwd=root).returncode == 0:
        return f"already ignored by {root}"
    if workspace == root:
        return (f"WARNING: {workspace} is itself the root of a git repo, so nothing here is ignored. "
                "Anything you commit there goes wherever that repo goes. Pick another folder.")
    rel = workspace.relative_to(root).as_posix() + "/"
    ignore = root / ".gitignore"
    existing = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    with ignore.open("a", encoding="utf-8") as fh:
        if existing and not existing.endswith("\n"):
            fh.write("\n")
        fh.write(f"# Off My Plate workspace: personal, never commit\n{rel}\n")
    return f"added {rel} to {ignore}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?")
    parser.add_argument("--no-gitignore", action="store_true")
    args = parser.parse_args(argv)

    target = args.path or os.environ.get("OFF_MY_PLATE_DIR") or str(Path.home() / "plate")
    workspace = Path(target).expanduser().resolve()
    fresh = not (workspace / "config.md").exists()
    workspace.mkdir(parents=True, exist_ok=True)

    created, kept = [], []
    for source in sorted(TEMPLATES.rglob("*")):
        rel = source.relative_to(TEMPLATES)
        dest = workspace / rel
        if source.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue
        if source.name == ".gitkeep":
            dest.parent.mkdir(parents=True, exist_ok=True)
            continue
        if dest.exists():
            kept.append(str(rel))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            created.append(str(rel))

    print(f"Workspace: {workspace} ({'new' if fresh else 'existing, nothing overwritten'})")
    if created:
        print("Created: " + ", ".join(created))
    if kept:
        print(f"Kept as is: {len(kept)} file(s)")
    if not args.no_gitignore:
        print("Git: " + ensure_ignored(workspace))
    if fresh:
        print("\nNext: answer the three ★ questions in config.md (hours, life anchors, buckets).")
    if workspace != (Path.home() / "plate").resolve() and not os.environ.get("OFF_MY_PLATE_DIR"):
        print(f"\nThis is not the default location. Set OFF_MY_PLATE_DIR={shlex.quote(str(workspace))} so scheduled runs find it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
