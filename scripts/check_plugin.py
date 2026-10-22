#!/usr/bin/env python3
"""Check that every skill, agent, and command in this plugin can actually be found.

The load check in CI proves the plugin reaches "enabled". It does not prove any
component is reachable: a skill whose frontmatter `name` disagrees with its
directory, or which has no description for the model to match against, installs
cleanly and then never triggers — silently, for everyone who installed it.

ERROR blocks; WARNING does not. Missing `name` is a warning on purpose: Claude Code
falls back to the directory name, so this plugin loads today, but that fallback is
undocumented and other agents' loaders do not all share it.

Usage: python3 scripts/check_plugin.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Components whose directory name must match their frontmatter name.
DIR_NAMED = {"skills"}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str | None]:
    """Return (fields, error). Only top-level `key: value` pairs are read."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing opening --- frontmatter delimiter"
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields, None
        if not line.strip() or line.startswith((" ", "\t", "#")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip("'\"")
    return fields, "missing closing --- frontmatter delimiter"


def check_components(
    kind: str,
    errors: list[str],
    warnings: list[str],
    names: dict[str, list[str]],
) -> int:
    directory = ROOT / kind
    if not directory.is_dir():
        return 0
    paths = (
        sorted(directory.glob("*/SKILL.md"))
        if kind in DIR_NAMED
        else sorted(directory.glob("*.md"))
    )
    if not paths:
        errors.append(f"{kind}/ exists but contains no components")
        return 0
    for path in paths:
        relative = path.relative_to(ROOT)
        fields, error = parse_frontmatter(path)
        if error:
            errors.append(f"{relative}: {error}")
            continue
        if not fields.get("description"):
            errors.append(
                f"{relative}: frontmatter has no non-empty 'description'; "
                "nothing for the model to match on, so it can never be selected"
            )
        expected = path.parent.name if kind in DIR_NAMED else path.stem
        name = fields.get("name")
        if not name:
            warnings.append(
                f"{relative}: no 'name' in frontmatter; loads as {expected!r} by "
                "directory-name fallback, which other agents may not do"
            )
            name = expected
        elif name != expected:
            errors.append(
                f"{relative}: frontmatter name {name!r} does not match {expected!r}; "
                "the component will not be found by that name"
            )
        names.setdefault(name, []).append(str(relative))
    return len(paths)


def check_manifests(errors: list[str]) -> None:
    for relative in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{relative}: missing")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON: {exc.msg} at line {exc.lineno}")
            continue
        if not payload.get("name"):
            errors.append(f"{relative}: missing 'name'")
        if relative.endswith("marketplace.json"):
            plugins = payload.get("plugins")
            if not isinstance(plugins, list) or not plugins:
                errors.append(f"{relative}: 'plugins' must be a non-empty array")
                continue
            for index, entry in enumerate(plugins):
                source = entry.get("source")
                if not source:
                    errors.append(f"{relative}: plugins[{index}] is missing 'source'")
                elif not (ROOT / source).exists():
                    errors.append(
                        f"{relative}: plugins[{index}] source {source!r} does not exist"
                    )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    names: dict[str, list[str]] = {}
    counts = {
        kind: check_components(kind, errors, warnings, names)
        for kind in ("skills", "agents", "commands")
    }
    check_manifests(errors)

    for name, locations in sorted(names.items()):
        if len(locations) > 1:
            errors.append(f"duplicate component name {name!r} in: {', '.join(locations)}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    summary = ", ".join(f"{count} {kind}" for kind, count in counts.items() if count)
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        return 1
    print(f"\nComponents reachable: {summary}. {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
