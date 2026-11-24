#!/usr/bin/env python3
"""SessionStart hook: turn straight talk on for a new session, if the human opted in.

Opt-in is one empty flag file, written by `/straight always`:
    $CLAUDE_CONFIG_DIR/.off-my-plate-straight-talk   (default ~/.claude/)

No flag, no output. With the flag, the straight-talk rules are printed, and Claude
Code adds what a SessionStart hook prints to the session's context. This never
blocks a session from starting: every failure exits 0.
It is printed again after a resume, a /clear, or a compaction, so the notice tells
the model to leave it off if the human already turned it off in that conversation.
It reads two files and opens no network connection.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

FLAG_NAME = ".off-my-plate-straight-talk"
FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)


def flag_path() -> Path:
    base = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(base) / FLAG_NAME


def rules() -> str:
    skill = Path(__file__).resolve().parents[1] / "skills" / "straight-talk" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    return FRONTMATTER.sub("", text, count=1).strip()


def main() -> int:
    try:
        flag = flag_path()
        if not flag.is_file():
            return 0
        body = rules()
        if not body:
            return 0
        sys.stdout.write(
            "STRAIGHT TALK ON (always-on, from ADHD: Off My Plate). The rules below shape every "
            "reply in this session. This notice is printed again after a resume, a /clear, or a "
            "compaction: if the conversation so far shows the human saying \"stop straight talk\" "
            "or \"normal mode\" and not turning it back on since, leave it off and ignore the rules below. To stop the notice "
            f"itself: /straight never, or delete {flag}.\n\n"
            f"{body}\n"
        )
        sys.stdout.flush()
    except Exception:
        pass
    try:
        # A closed pipe must not turn into an error at interpreter exit.
        sys.stdout = open(os.devnull, "w")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
