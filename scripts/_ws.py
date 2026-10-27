"""Shared helpers for the workspace scripts: find the workspace, read its tables.

Not a command. due.py, surfaced.py and init_workspace.py import it.
"""

from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path

ISO_DATE = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")


def read_text(path: Path) -> str:
    """Workspace files are the human's; a stray non-UTF-8 byte must not crash a run."""
    return path.read_text(encoding="utf-8", errors="replace")


def bad_date(text: str) -> str | None:
    """An ISO-shaped date that is not a real date (2026-13-40), for warnings."""
    match = ISO_DATE.search(text or "")
    if match and first_date(text) is None:
        return match.group(0)
    return None
PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def find_workspace(explicit: str | None = None) -> Path | None:
    """RULES §2 lookup order: argument, $OFF_MY_PLATE_DIR, ./plate, ~/plate.

    A path given explicitly is the only one checked: naming a workspace that does
    not exist must fail, never quietly fall back to someone's real ~/plate.
    """
    if explicit:
        path = Path(explicit).expanduser()
        return path.resolve() if (path / "config.md").is_file() else None
    env = os.environ.get("OFF_MY_PLATE_DIR")
    if env:
        # Same rule as an explicit path: a configured workspace that is missing fails.
        path = Path(env).expanduser()
        return path.resolve() if (path / "config.md").is_file() else None
    candidates = [Path.cwd() / "plate", Path.home() / "plate"]
    for path in candidates:
        if (path / "config.md").is_file():
            return path.resolve()
    return None


def first_date(text: str) -> date | None:
    match = ISO_DATE.search(text or "")
    if not match:
        return None
    try:
        return date(int(match[1]), int(match[2]), int(match[3]))
    except ValueError:
        return None


def read_table(path: Path) -> list[dict[str, str]]:
    """Rows of the first markdown table in a file, keyed by lower-cased header."""
    if not path.is_file():
        return []
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in read_text(path).splitlines():
        if not line.lstrip().startswith("|"):
            if header is not None and rows:
                break
            continue
        inner = re.sub(r"^\s*\|", "", line.rstrip())
        inner = re.sub(r"(?<!\\)\|\s*$", "", inner)
        cells = [c.strip().replace("\\|", "|") for c in UNESCAPED_PIPE.split(inner)]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        row = dict(zip(header, cells + [""] * (len(header) - len(cells))))
        rows.append(row)
    return rows


def column(row: dict[str, str], prefix: str) -> str:
    """Value of the first column whose header starts with prefix (case-insensitive)."""
    prefix = prefix.lower()
    for key, value in row.items():
        if key.startswith(prefix):
            return value
    return ""


def is_blank_template_row(row: dict[str, str]) -> bool:
    """A template's pre-filled row (ID only, everything else empty or a default)."""
    values = [v for k, v in row.items() if k != "id"]
    return not any(v and v not in {"open", "0"} for v in values)
