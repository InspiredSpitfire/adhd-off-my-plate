---
name: straight
description: Straight talk. Every reply opens with the thing to do and ends on one next step, for the rest of the session. on, off, always, never, or status.
argument-hint: '[on | off | always | never | status] [optional: feral | froggy | foggy | fried]'
---

Argument: $ARGUMENTS (empty means `on`).

- `on`, or a brain state alone: run the `straight-talk` skill and apply it to every reply for the rest of this session, sized to the brain state if one was given. Confirm in one line: `Straight talk on. "stop straight talk" turns it off.` Then carry on with whatever was in progress.
- `off`: stop applying it. One line: `Straight talk off.`
- `always`, `never`, `status`: find the plugin root (the directory above `commands/`) and run `python3 <plugin root>/scripts/straight_talk.py <argument>` with the path written as a literal absolute path, unquoted. Show its one line of output as it is. After `always`, also turn it on for this session.

`always` only writes one empty flag file in the Claude config folder; `never` removes it. Nothing else is stored.
