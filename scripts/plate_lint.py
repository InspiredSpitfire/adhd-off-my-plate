#!/usr/bin/env python3
"""Structural check of a Plate (RULES.md §3).

A Plate is the one deliverable of this plugin. The model that wrote it is the
worst judge of whether it kept to one next step, so a script checks instead.

Exit 0 = PASS, 1 = FAIL (defects listed), 2 = could not read the file.

Usage: python3 scripts/plate_lint.py plate/plate.md [--fried-ok]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SECTIONS = [
    "Off my plate",
    "Keep",
    "Let go",
    "Next step",
    "Revive one",
    "What you're missing",
    "Evidence",
]
STATES = {"Feral", "Froggy", "Foggy", "Fried"}
GATES = {"AUTO", "DRAFT", "NEEDS YOUR GO"}
# Verbs that mean the item leaves the building. Any Off-my-plate line with one
# of these must be gated NEEDS YOUR GO, not AUTO or DRAFT.
OUTWARD = re.compile(
    r"\b(send|sends|sending|sent|reply to|respond to|post|posts|publish|pay|pays|"
    r"book|books|cancel|cancels|sign|signs|delete|deletes|unsubscribe|transfer|"
    r"accept|decline|rsvp)\b",
    re.IGNORECASE,
)
# "draft a reply" is fine at DRAFT; "reply" alone is outward. Strip drafting
# phrasing before testing for outward verbs.
DRAFTING = re.compile(r"\bdraft(s|ed|ing)?\b[^·]*?\b(reply|replies|response|decline|email|message|post)\b", re.IGNORECASE)
MINUTES = re.compile(r"(\d+)\s*(?:min|mins|minutes)\b", re.IGNORECASE)
BANNED = [
    "just try harder",
    "consistency is key",
    "just use a calendar",
    "you've got this",
    "you got this",
    "no excuses",
    "hustle",
    "discipline",
]
ISO_DATE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")


def split_sections(text: str) -> tuple[str, dict[str, str]]:
    lines = text.splitlines()
    header = lines[0] if lines else ""
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []
    for line in lines[1:]:
        match = re.match(r"^##\s+(.*?)\s*$", line)
        if match:
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = match.group(1)
            buffer = []
        else:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return header, sections


def content_lines(block: str) -> list[str]:
    return [line for line in block.splitlines() if line.strip()]


def lint(path: Path, fried_ok: bool = False) -> list[str]:
    defects: list[str] = []
    text = path.read_text(encoding="utf-8")
    header, sections = split_sections(text)

    # Header
    head = re.match(r"^#\s+The Plate\s+·\s+(\S+)\s+·\s+Brain:\s+(\w+)", header)
    state = None
    if not head:
        defects.append("header: first line must be '# The Plate · YYYY-MM-DD · Brain: <state>'")
    else:
        date, state = head.group(1), head.group(2)
        if not ISO_DATE.fullmatch(date):
            defects.append(f"header: date {date!r} is not YYYY-MM-DD")
        if state not in STATES:
            defects.append(f"header: brain state {state!r} is not one of {sorted(STATES)}")

    for name in SECTIONS:
        if name not in sections:
            defects.append(f"missing section '## {name}'")
    if defects and any(d.startswith("missing section") for d in defects):
        return defects  # structure too broken to check further

    # Off my plate
    for line in content_lines(sections["Off my plate"]):
        if not line.lstrip().startswith("- "):
            defects.append(f"Off my plate: not a list item: {line.strip()[:60]!r}")
            continue
        gate = next((g for g in GATES if f"gate: {g}" in line), None)
        if gate is None:
            defects.append(f"Off my plate: no gate tag (AUTO | DRAFT | NEEDS YOUR GO): {line.strip()[:60]!r}")
            continue
        body = line.split("· gate:")[0]
        test_body = DRAFTING.sub("draft", body)
        if OUTWARD.search(test_body) and gate != "NEEDS YOUR GO":
            defects.append(
                f"Off my plate: outward action gated {gate}, must be NEEDS YOUR GO: {line.strip()[:60]!r}"
            )

    # Keep
    keeps = [l for l in content_lines(sections["Keep"]) if re.match(r"^\s*\d+[.)]\s", l)]
    limit = 1 if state == "Fried" else 3
    if not keeps:
        defects.append("Keep: needs at least one numbered item (on Fried, 'rest' counts)")
    elif len(keeps) > limit:
        defects.append(f"Keep: {len(keeps)} items; maximum is {limit} for brain state {state}")

    # Let go
    for line in content_lines(sections["Let go"]):
        if line.strip().lower() in {"- nothing today", "- none"}:
            continue
        if not line.lstrip().startswith("- "):
            defects.append(f"Let go: not a list item: {line.strip()[:60]!r}")
            continue
        if "revive-by:" not in line:
            defects.append(f"Let go: no 'revive-by:' (date or never): {line.strip()[:60]!r}")
        else:
            value = line.split("revive-by:", 1)[1].strip().split("·")[0].strip()
            if value != "never" and not ISO_DATE.fullmatch(value):
                defects.append(f"Let go: revive-by {value!r} is not YYYY-MM-DD or 'never'")

    # Next step
    steps = content_lines(sections["Next step"])
    if len(steps) != 1:
        defects.append(f"Next step: must be exactly one line, found {len(steps)}")
    else:
        step = steps[0]
        if not step.lstrip().startswith(">"):
            defects.append("Next step: line must start with '>'")
        if re.search(r"\b(or|then|and then|either)\b", step, re.IGNORECASE):
            defects.append("Next step: contains 'or' / 'then' / 'either'; that is a menu, not a step")
        if re.search(r"(^|\s)[-*]\s|\d+[.)]\s", step.lstrip(">").strip()):
            defects.append("Next step: contains list markers; one action only")
        mins = MINUTES.search(step)
        cap = 5 if state == "Fried" else 10
        if not mins:
            defects.append(f"Next step: no time box found (write '… (≤ {cap} min)')")
        elif int(mins.group(1)) > cap:
            defects.append(f"Next step: {mins.group(1)} min exceeds the {cap} min cap for {state}")

    # Revive one
    revive = sections["Revive one"]
    if state == "Fried" and re.search(r"not today", revive, re.IGNORECASE):
        pass
    else:
        projects = re.findall(r"\*\*Project:\*\*", revive)
        tiny = re.findall(r"\*\*Tiny step:\*\*(.*)", revive)
        if len(projects) != 1:
            defects.append(f"Revive one: exactly one '**Project:**' line required, found {len(projects)}")
        if len(tiny) != 1:
            defects.append(f"Revive one: exactly one '**Tiny step:**' line required, found {len(tiny)}")
        else:
            mins = MINUTES.search(tiny[0])
            if not mins:
                defects.append("Revive one: tiny step has no time box (≤ 10 min)")
            elif int(mins.group(1)) > 10:
                defects.append(f"Revive one: tiny step is {mins.group(1)} min; cap is 10")
            if re.search(r"\b(or|then)\b", tiny[0], re.IGNORECASE):
                defects.append("Revive one: tiny step contains 'or' / 'then'; one step only")
        if "stalled because" not in revive:
            defects.append("Revive one: missing 'stalled because <one clause>'")

    # What you're missing
    if not content_lines(sections["What you're missing"]):
        defects.append("What you're missing: empty; write the gap, or the place you could not look")

    # Evidence
    evidence = sections["Evidence"]
    if not re.search(r"^EVIDENCE:\s*\S", evidence, re.MULTILINE):
        defects.append("Evidence: needs at least one 'EVIDENCE: <source>' line")
    if not re.search(r"^ASSUMED:\s*\S", evidence, re.MULTILINE):
        defects.append("Evidence: needs an 'ASSUMED: …' line ('ASSUMED: none' is fine)")

    # Dates outside Evidence must be labeled or present in Evidence
    cited = set(ISO_DATE.findall(evidence))
    for name in ("Keep", "Next step", "Let go", "Revive one", "What you're missing"):
        for date in ISO_DATE.findall(sections[name]):
            line = next((l for l in sections[name].splitlines() if date in l), "")
            if name == "Let go" and "revive-by:" in line and date in line.split("revive-by:", 1)[1]:
                continue  # revive-by dates are decisions, not facts
            if date not in cited and not re.search(r"ASSUMED|INFERENCE", line):
                defects.append(f"{name}: date {date} is not in Evidence and not labeled INFERENCE/ASSUMED")

    # Tone
    lowered = text.lower()
    for phrase in BANNED:
        if phrase in lowered:
            defects.append(f"tone: banned phrase {phrase!r}")

    return defects


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    path = Path(args[0])
    if not path.is_file():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 2
    defects = lint(path, fried_ok="--fried-ok" in argv)
    if defects:
        print(f"FAIL: {path} · {len(defects)} defect(s)")
        for d in defects:
            print(f"  - {d}")
        return 1
    print(f"PASS: {path} · one next step, gates present, evidence labeled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
