#!/usr/bin/env python3
"""Structural check of a Plate (RULES.md §3).

A Plate is the one deliverable of this plugin. The model that wrote it is the
worst judge of whether it kept to one next step, so a script checks instead.

What it enforces: the seven sections; Keep limits per brain state (Feral 3,
Froggy 3, Foggy 2, Fried 1); exactly one next step with a time box (≤ 10 min,
Fried ≤ 5, "(0 min)" allowed); gates on every Off-my-plate item, with outward
verbs at AUTO or DRAFT failing; revive-by on every Let-go item; one project and
one ≤ 10 min step in Revive (Fried: the exact sentinel); a non-empty Missing
section; Evidence with EVIDENCE and ASSUMED lines; dates outside Evidence
labeled; banned tone phrases outside quoted evidence.

The outward-verb check is a heuristic on the item's leading verb plus a list of
execution verbs. It catches the common cases; it is not a proof. The
plate-reviewer agent reads the items too.

Exit 0 = PASS, 1 = FAIL (defects listed), 2 = could not read the file.

Usage: python3 scripts/plate_lint.py plate/plate.md
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
KEEP_LIMIT = {"Feral": 3, "Froggy": 3, "Foggy": 2, "Fried": 1}
STEP_CAP = {"Feral": 10, "Froggy": 10, "Foggy": 10, "Fried": 5}
GATES = ("NEEDS YOUR GO", "DRAFT", "AUTO")
FRIED_REVIVE = "Revive: not today, on purpose."

# Verbs that, as the item's leading verb, mean the item acts in the world.
OUTWARD_VERBS = (
    "send|email|e-mail|text|message|dm|call|phone|reply|respond|share|forward|post|publish|"
    "schedule|book|reserve|order|buy|purchase|pay|submit|sign|cancel|delete|remove|"
    "unsubscribe|transfer|accept|decline|rsvp|invite|confirm|approve|notify|tell|ask|ping|nudge"
)
# Verbs that, anywhere in the item, mean something is executed, not prepared.
EXECUTE = re.compile(
    r"\b(send|sends|sending|submit|submits|pay|pays|cancel|cancels|delete|deletes|book|books|"
    r"sign|signs|transfer|transfers|publish|publishes|unsubscribe|buy|buys|order|orders|purchase|"
    r"forward|forwards|hit send|press send|email it|text it|message it|post it|share it|schedule it|"
    r"rsvp|archive|archives|label|labels|move|moves|mark as)\b",
    re.IGNORECASE,
)
# Noun and idiom collisions that are not actions; stripped before the verb checks.
NOT_ACTIONS = re.compile(
    r"\b(purchase orders?|sign[- ]?ups?|sign[- ]up sheets?|book clubs?|pay schedules?|pay stubs?|"
    r"call(?:s|ed|ing)? out|order (?:oldest|newest|by|of)|confirm(?:s|ed|ing)? (?:from|against|that)|"
    r"post[- ]?its?|the (?:email|text|message|post|order|call|invoice|book|sign))\b",
    re.IGNORECASE,
)
# A second verb after a coordinator: "pull the thread and email Jordan".
COORDINATED = re.compile(
    rf"(?:\band\b|\bthen\b|;|,)\s+(?:{OUTWARD_VERBS})\b", re.IGNORECASE
)
LEADING = re.compile(rf"^\s*-\s*\[.\]\s*(?:{OUTWARD_VERBS}|archive|label|move|mark)(?:s|ed|ing)?\b", re.IGNORECASE)
DRAFTING_START = re.compile(
    r"^\s*-\s*\[.\]\s*(?:draft|write|prepare|compose|pre-write|put together|pull together|outline)\b",
    re.IGNORECASE,
)
TIMEBOX = re.compile(r"\((\d+)\s*(?:min|mins|minutes)\)\s*$", re.IGNORECASE)
MENU = re.compile(
    r"\b(or|then|either|whichever|and also|alternatively|instead|otherwise|pick one|if that)\b|\s/\s|:\s*\w[^,]*,\s*\w[^,]*,",
    re.IGNORECASE,
)
BANNED = [
    r"just try harder",
    r"consistency is key",
    r"just use a calendar",
    r"you'?ve got this",
    r"you got this",
    r"no excuses",
    r"\bhustle\b",
    r"\bdiscipline\b",
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
            current = re.sub(r"\s*\(.*\)\s*$", "", match.group(1))  # "Keep (2 real hours)" → "Keep"
            buffer = []
        else:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return header, sections


def content_lines(block: str) -> list[str]:
    return [line for line in block.splitlines() if line.strip()]


def is_none_line(line: str) -> bool:
    return re.fullmatch(r"-?\s*(nothing today|none|nothing)[.!]?\s*(·.*)?", line.strip(), re.IGNORECASE) is not None


def lint(path: Path) -> list[str]:
    defects: list[str] = []
    text = path.read_text(encoding="utf-8").replace("\u2019", "'").replace("\u2018", "'")
    header, sections = split_sections(text)

    head = re.match(r"^#\s+The Plate\s+·\s+(\S+)\s+·\s+Brain:\s+(\w+)", header)
    state = "Feral"
    if not head:
        defects.append("header: first line must be '# The Plate · YYYY-MM-DD · Brain: <state>'")
    else:
        date, state = head.group(1), head.group(2)
        if not ISO_DATE.fullmatch(date):
            defects.append(f"header: date {date!r} is not YYYY-MM-DD")
        if state not in STATES:
            defects.append(f"header: brain state {state!r} is not one of {sorted(STATES)}")
            state = "Feral"

    missing = [name for name in SECTIONS if name not in sections]
    for name in missing:
        defects.append(f"missing section '## {name}'")
    if missing:
        return defects

    # Off my plate
    for line in content_lines(sections["Off my plate"]):
        if is_none_line(line):
            continue
        if not line.lstrip().startswith("- "):
            defects.append(f"Off my plate: not a list item: {line.strip()[:60]!r}")
            continue
        gate = next((g for g in GATES if f"gate: {g}" in line), None)
        if gate is None:
            defects.append(f"Off my plate: no gate tag (AUTO | DRAFT | NEEDS YOUR GO): {line.strip()[:60]!r}")
            continue
        body = NOT_ACTIONS.sub("", line.split("· gate:")[0])
        short = line.strip()[:60]
        if gate == "NEEDS YOUR GO":
            continue
        if gate == "DRAFT":
            if not DRAFTING_START.match(body):
                defects.append(f"Off my plate: DRAFT item must start with a drafting verb (draft, write, prepare…): {short!r}")
            elif EXECUTE.search(body) or COORDINATED.search(body):
                defects.append(f"Off my plate: DRAFT item also acts (\"draft it and send it\"); must be NEEDS YOUR GO: {short!r}")
        else:  # AUTO
            if LEADING.match(body) or EXECUTE.search(body) or COORDINATED.search(body):
                defects.append(f"Off my plate: outward action gated AUTO, must be NEEDS YOUR GO: {short!r}")

    # Keep
    keeps = [l for l in content_lines(sections["Keep"]) if re.match(r"^\s*\d+[.)]\s", l)]
    limit = KEEP_LIMIT[state]
    if not keeps:
        defects.append("Keep: needs at least one numbered item (on Fried, '1. Rest.' counts)")
    elif len(keeps) > limit:
        defects.append(f"Keep: {len(keeps)} items; maximum is {limit} for brain state {state}")

    # Let go
    for line in content_lines(sections["Let go"]):
        if is_none_line(line):
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
    cap = STEP_CAP[state]
    if len(steps) != 1:
        defects.append(f"Next step: must be exactly one line, found {len(steps)}")
    else:
        step = steps[0]
        if not step.lstrip().startswith(">"):
            defects.append("Next step: line must start with '>'")
        body = step.lstrip(">").strip()
        if MENU.search(body):
            defects.append("Next step: contains 'or' / 'then' / 'either' / 'whichever' / '/'; that is a menu, not a step")
        if re.match(r"^(?:[-*]\s|\d+[.)]\s)", body):
            defects.append("Next step: starts with a list marker; one action, as a sentence")
        mins = TIMEBOX.search(body)
        if not mins:
            defects.append(f"Next step: must end with a time box like '(≤ {cap} min)' → write '(N min)'; '(0 min)' is allowed for nothing-on-purpose")
        elif int(mins.group(1)) > cap:
            defects.append(f"Next step: {mins.group(1)} min exceeds the {cap} min cap for {state}")

    # Revive one
    revive = sections["Revive one"].strip()
    if state == "Fried":
        if revive != FRIED_REVIVE:
            defects.append(f"Revive one: on Fried the section is exactly {FRIED_REVIVE!r}, nothing else")
    else:
        projects = re.findall(r"\*\*Project:\*\*", revive)
        tiny = re.findall(r"\*\*Tiny step:\*\*(.*)", revive)
        if len(projects) != 1:
            defects.append(f"Revive one: exactly one '**Project:**' line required, found {len(projects)}")
        if len(tiny) != 1:
            defects.append(f"Revive one: exactly one '**Tiny step:**' line required, found {len(tiny)}")
        else:
            mins = TIMEBOX.search(tiny[0].strip())
            if not mins:
                defects.append("Revive one: tiny step must end with a time box '(N min)', N ≤ 10")
            elif int(mins.group(1)) > 10:
                defects.append(f"Revive one: tiny step is {mins.group(1)} min; cap is 10")
            if MENU.search(tiny[0]):
                defects.append("Revive one: tiny step contains 'or' / 'then'; one step only")
        if "stalled because" not in revive:
            defects.append("Revive one: missing 'stalled because <one clause>'")
        if not re.search(r"revival #\d+", revive):
            defects.append("Revive one: missing 'revival #N' (read it from projects.md; 0 for a first revival)")

    # What you're missing
    if not content_lines(sections["What you're missing"]):
        defects.append("What you're missing: empty; write the gap, or the place you could not look")

    # Evidence
    evidence = sections["Evidence"]
    if not re.search(r"^EVIDENCE:\s*\S", evidence, re.MULTILINE):
        defects.append("Evidence: needs at least one 'EVIDENCE: <source>' line")
    if not re.search(r"^ASSUMED:\s*\S", evidence, re.MULTILINE):
        defects.append("Evidence: needs an 'ASSUMED: …' line ('ASSUMED: none' is fine)")

    # Dates outside Evidence must be cited there or labeled on their own line
    cited = set(ISO_DATE.findall(evidence))
    for name in ("Off my plate", "Keep", "Next step", "Let go", "Revive one", "What you're missing"):
        for line in sections[name].splitlines():
            labeled = re.search(r"ASSUMED|INFERENCE", line)
            for date in ISO_DATE.findall(line):
                if name == "Let go" and "revive-by:" in line and date in line.split("revive-by:", 1)[1]:
                    continue  # revive-by dates are decisions, not facts
                if date not in cited and not labeled:
                    defects.append(f"{name}: date {date} is not in Evidence and not labeled INFERENCE/ASSUMED")

    # Tone, outside the Evidence section (quotes of the human's own words live there)
    prose = "\n".join(v for k, v in sections.items() if k != "Evidence").lower()
    for pattern in BANNED:
        if re.search(pattern, prose):
            defects.append(f"tone: banned phrase {pattern.strip(chr(92)+'b')!r}")

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
    defects = lint(path)
    if defects:
        print(f"FAIL: {path} · {len(defects)} defect(s)")
        for d in defects:
            print(f"  - {d}")
        return 1
    print(f"PASS: {path} · one next step, gates present, evidence labeled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
