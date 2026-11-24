#!/usr/bin/env python3
"""Turn always-on straight talk on or off, or report which it is.

    python3 scripts/straight_talk.py always    write the flag file
    python3 scripts/straight_talk.py never     remove it
    python3 scripts/straight_talk.py status    say which

The flag is one empty file: $CLAUDE_CONFIG_DIR/.off-my-plate-straight-talk
(default ~/.claude/). hooks/always_on.py reads it when a session starts.
Exit 0 on success, 2 on a bad argument or a folder that cannot be written.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from always_on import flag_path  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in {"always", "never", "status"}:
        print(__doc__)
        return 2
    flag = flag_path()
    action = argv[0]
    try:
        if action == "always":
            flag.parent.mkdir(parents=True, exist_ok=True)
            flag.touch()
            print(f"Straight talk: ALWAYS ON for new sessions. Flag: {flag}")
        elif action == "never":
            flag.unlink(missing_ok=True)
            print(f"Straight talk: always-on is OFF. /straight still turns it on per session. Flag removed: {flag}")
        else:
            state = "ALWAYS ON for new sessions" if flag.is_file() else "per session only (always-on is off)"
            print(f"Straight talk: {state}. Flag: {flag}")
    except OSError as exc:
        print(f"Straight talk: could not change {flag}: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
