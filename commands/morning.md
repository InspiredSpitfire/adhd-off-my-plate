---
name: morning
description: The unattended morning routine. Reads mail, calendar, and the workspace since yesterday, does the AUTO and DRAFT work, stops at every NEEDS YOUR GO, leaves a phone-sized brief.
argument-hint: [optional: brain state, or "setup" to write the routine prompt]
---

Run the `morning-plate` skill. Arguments: $ARGUMENTS

If the argument is `setup`, skip the run and write the exact routine prompt plus the schedule confirmation step, and point at README "Schedule it". If the argument contains a path (starts with `/` or `~`), that path is the workspace: it wins over every other lookup, and nothing outside it and the plugin is read or written. A brain state may come with it (`/morning ~/plate foggy`). Otherwise run it unattended: no questions, assumptions labeled.
