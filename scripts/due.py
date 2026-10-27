#!/usr/bin/env python3
"""What is due: nudge-by, revive-by, and deadlines from the workspace tables.

Reads waiting-on.md (Nudge-by), graveyard.md (Revive-by), and later.md
(Deadline). Prints rows that are overdue, due today, or due within N days, so
whats-missing and morning-plate cite a list instead of eyeballing three tables.

Skips: template rows, rows with no ISO date, revive-by `never`, graveyard rows
marked Vetoed, and waiting-on rows whose Status is done, closed, or resolved.

Usage: python3 scripts/due.py [WORKSPACE] [--within DAYS] [--today YYYY-MM-DD] [--json]
WORKSPACE defaults to the RULES §2 lookup ($OFF_MY_PLATE_DIR, ./plate, ~/plate).
Exit 0 always (it is a report); 2 if no workspace is found.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from _ws import bad_date, column, find_workspace, first_date, is_blank_template_row, read_table


def iso_day(text: str) -> date:
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not YYYY-MM-DD")

SOURCES = [
    # file, date column prefix, label, item column prefix
    ("waiting-on.md", "nudge-by", "nudge", "what"),
    ("graveyard.md", "revive-by", "revive", "item"),
    ("later.md", "deadline", "deadline", "item"),
]
CLOSED = ("done", "closed", "resolved", "received")
NOT_VETOED = {"", "no", "n", "-", "—", "none"}


def collect(workspace, today: date, within: int, warnings: list[str] | None = None) -> list[dict]:
    hits = []
    warnings = warnings if warnings is not None else []
    for filename, date_col, label, item_col in SOURCES:
        for row in read_table(workspace / filename):
            if is_blank_template_row(row):
                continue
            raw = column(row, date_col)
            if raw.strip().lower().startswith("never"):
                continue
            if filename == "graveyard.md" and column(row, "vetoed").strip().lower() not in NOT_VETOED:
                continue
            if filename == "waiting-on.md" and column(row, "status").strip().lower().startswith(CLOSED):
                continue
            when = first_date(raw)
            if when is None:
                if bad_date(raw):
                    warnings.append(f"{filename} {row.get('id', '?')}: '{bad_date(raw)}' is not a real date; row skipped")
                continue
            days = (when - today).days
            if days > within:
                continue
            item = column(row, item_col)
            if filename == "waiting-on.md":
                item = f"{column(row, 'who')}: {item}"
            hits.append({
                "file": filename,
                "id": row.get("id", ""),
                "kind": label,
                "item": item,
                "date": when.isoformat(),
                "days": days,
            })
    return sorted(hits, key=lambda h: (h["days"], h["file"], h["id"]))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--within", type=int, default=3, help="days ahead to include (default 3)")
    parser.add_argument("--today", type=iso_day, help="override today's date, YYYY-MM-DD (for tests)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    workspace = find_workspace(args.workspace)
    if workspace is None:
        print("No workspace found. A named path or $OFF_MY_PLATE_DIR must hold a config.md; "
              "otherwise ./plate, then ~/plate. Run /setup.", file=sys.stderr)
        return 2
    today = args.today or date.today()
    warnings: list[str] = []
    hits = collect(workspace, today, args.within, warnings)
    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)

    if args.json:
        print(json.dumps({"workspace": str(workspace), "today": today.isoformat(), "within": args.within,
                          "due": hits, "warnings": warnings}, indent=2))
        return 0

    print(f"Due · {workspace} · today {today.isoformat()} · window {args.within} day(s)")
    if not hits:
        print("Nothing overdue or due in the window.")
        return 0
    groups = [
        ("OVERDUE", [h for h in hits if h["days"] < 0]),
        ("TODAY", [h for h in hits if h["days"] == 0]),
        (f"NEXT {args.within} DAYS", [h for h in hits if h["days"] > 0]),
    ]
    for title, group in groups:
        if not group:
            continue
        print(f"\n{title}")
        for h in group:
            when = f"{-h['days']}d late" if h["days"] < 0 else ("today" if h["days"] == 0 else f"in {h['days']}d")
            print(f"- {h['id']} · {h['kind']} {h['date']} ({when}) · {h['item']} · {h['file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
