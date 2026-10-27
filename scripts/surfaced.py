#!/usr/bin/env python3
"""Dedupe: what has the Plate already told you, and how many times.

A proactive chief of staff that repeats itself every morning gets ignored.
This reads the last N Plates in history/ (default 7), pulls the "What you're
missing" and "Let go" bullets, and matches them by meaning-ish (shared
content words, not exact text) so a reworded nag still counts as a repeat.

Two modes:
  report      list every item surfaced on 2+ past Plates
  --candidate FILE
              check a new Plate before it ships: flag each Missing / Let-go
              bullet already surfaced on THRESHOLD or more past Plates.
              RULES: drop it unless its deadline is inside 48 hours, or the
              Plate says why it is back.

Usage:
  python3 scripts/surfaced.py [WORKSPACE] [--last 7] [--threshold 2]
  python3 scripts/surfaced.py [WORKSPACE] --candidate plate/plate.md
Exit 0 = nothing flagged, 1 = repeats flagged (candidate mode), 2 = no workspace.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _ws import find_workspace, first_date, read_text

SECTIONS = ("What you're missing", "Let go")
STOP = set("""
a an the and or but if then than that this these those to of in on at by for with from as is are was
were be been being it its it's your you you're yours i me my we our they them their he she his her
not no nothing none has have had do does did done will would can could should may might must
there here what which who whom when where why how all any each every some more most other such
only own same so too very just about into over after before again once one two three today tomorrow
yesterday found plate gate auto draft needs go keep let graveyard revive-by never
""".split())


def bullets(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {name: [] for name in SECTIONS}
    current = None
    for line in text.replace("’", "'").splitlines():
        heading = re.match(r"^##\s+(.*?)\s*(?:\(.*\))?\s*$", line)
        if heading:
            current = heading.group(1) if heading.group(1) in SECTIONS else None
            continue
        if current and line.lstrip().startswith("- "):
            body = line.lstrip()[2:]
            if body.strip().lower().rstrip(".") in {"none", "nothing today", "nothing"}:
                continue
            out[current].append(body.strip())
    return out


def tokens(text: str) -> frozenset[str]:
    # Judge an item by its head: what comes before the first " · " source tag.
    head = text.split(" · ")[0].split(" → ")[0]
    out = set()
    for word in re.findall(r"[a-z][a-z0-9'-]+", head.lower()):
        word = re.sub(r"'s$", "", word).strip("'-")
        if len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        if len(word) > 2 and word not in STOP:
            out.add(word)
    return frozenset(out)


MIN_SHARED = 3


def similar(a: frozenset[str], b: frozenset[str]) -> float:
    """Word-overlap ratio, but only once at least MIN_SHARED content words match.

    Two short items that share two words ("vet appointment tuesday" and
    "dentist appointment tuesday") are different errands; cutting one as a
    repeat would quietly drop a real thing from the Plate. A false repeat is the
    expensive mistake here, so the bar is high.
    """
    if not a or not b:
        return 0.0
    shared = len(a & b)
    if shared < min(MIN_SHARED, len(a), len(b)) or (shared < MIN_SHARED and a != b):
        return 0.0
    return shared / len(a | b)


def best(seen: list[dict], section: str, key: frozenset[str], floor: float) -> dict | None:
    scored = [(max(similar(k, key) for k in s["keys"]), s) for s in seen if s["section"] == section]
    scored = [pair for pair in scored if pair[0] >= floor]
    return max(scored, key=lambda pair: pair[0])[1] if scored else None


def plate_date(path: Path) -> str:
    when = first_date(path.name) or first_date(read_text(path).splitlines()[0] if path.stat().st_size else "")
    return when.isoformat() if when else path.stem


def history(workspace: Path, last: int) -> list[Path]:
    files = sorted((workspace / "history").glob("plate-*.md"))
    return files[-last:]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--last", type=int, default=7, help="past Plates to read (default 7)")
    parser.add_argument("--threshold", type=int, default=2, help="past appearances that count as a repeat (default 2)")
    parser.add_argument("--match", type=float, default=0.5, help="word-overlap ratio that counts as the same item (default 0.5)")
    parser.add_argument("--candidate", help="a new Plate to check against history")
    args = parser.parse_args(argv)

    workspace = find_workspace(args.workspace)
    if workspace is None:
        print("No workspace found. Run /setup.", file=sys.stderr)
        return 2
    past = history(workspace, args.last)

    # Each distinct item, with the dates of the past Plates it appeared on.
    seen: list[dict] = []
    for path in past:
        when = plate_date(path)
        for section, items in bullets(read_text(path)).items():
            for item in items:
                key = tokens(item)
                match = best(seen, section, key, args.match)
                if match is None:
                    seen.append({"section": section, "keys": [key], "text": item, "dates": [when]})
                else:
                    match["keys"].append(key)
                    if when not in match["dates"]:
                        match["dates"].append(when)

    if args.candidate:
        candidate = Path(args.candidate)
        if not candidate.is_file():
            print(f"ERROR: {candidate} not found", file=sys.stderr)
            return 2
        flagged = []
        for section, items in bullets(read_text(candidate)).items():
            for item in items:
                key = tokens(item)
                match = best(seen, section, key, args.match)
                if match and len(match["dates"]) >= args.threshold:
                    flagged.append((section, item, match["dates"]))
        print(f"Dedupe check · {candidate} against {len(past)} past Plate(s)")
        if not flagged:
            print("No repeats. Ship it.")
            return 0
        for section, item, dates in flagged:
            print(f"- REPEAT ({len(dates)}x: {', '.join(dates)}) · {section} · {item[:110]}")
        print("Drop each REPEAT unless its deadline is inside 48 hours or the Plate says what changed.")
        return 1

    repeats = [s for s in seen if len(s["dates"]) >= args.threshold]
    print(f"Surfaced · {workspace} · last {len(past)} Plate(s)")
    if not repeats:
        print("Nothing has been surfaced twice. No nagging yet.")
        return 0
    for s in sorted(repeats, key=lambda s: -len(s["dates"])):
        print(f"- {len(s['dates'])}x ({', '.join(s['dates'])}) · {s['section']} · {s['text'][:110]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
