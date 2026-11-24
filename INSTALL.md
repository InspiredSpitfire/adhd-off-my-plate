# Install

## Claude Code (tested)

```
/plugin marketplace add InspiredSpitfire/adhd-off-my-plate
/plugin install adhd-off-my-plate@adhd-off-my-plate
```

Then `/setup` for the Plate, and `/straight` for straight talk. `/straight always` keeps it on for every new session; `/straight never` undoes that. The always-on hook needs `python3` on your PATH; there is no PowerShell or `sh` fallback, so on a machine without `python3` always-on does nothing and `/straight` still works per session.

With always-on set, the notice is printed again after a `/clear`, a resume, or a compaction. "stop straight talk" holds for the conversation you said it in.

## Other agents (untested)

The files below follow each agent's published plugin layout. **None of them has been run on its agent yet.** If one fails to load, that is a bug: open an issue with the error.

What carries over: the skills are plain Markdown, so `straight-talk` should work anywhere skills load. What may not: the `/straight` command, the always-on hook, and the Plate scripts are Claude Code features, and the Plate skills expect a shell with `python3` plus mail and calendar connectors.

| Agent | File it reads | What you should get |
|---|---|---|
| Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | All eight skills. Turn straight talk on by asking: "use straight-talk for the rest of this session". |
| Cursor | `.cursor/skills/straight-talk/SKILL.md` | Straight talk only, when the repo is open in Cursor. Or copy that folder into your own project's `.cursor/skills/`. |
| Gemini CLI | `gemini-extension.json`, `GEMINI.md` | Straight talk on for every reply (the context file imports the rules), with a pointer to the Plate rulebook. |
| Qwen Code | `qwen-extension.json` | The skills folder. |
| Kimi Code | `kimi.plugin.json` | The skills folder. |

**Codex note:** `.agents/plugins/marketplace.json` points at this repo's `main` branch, so a Codex install only works once a version with `.codex-plugin/` is pushed there. Its `policy` block copies the layout other Codex plugins use and has not been checked against Codex.

**Not covered:** OpenCode, Pi, OMP, Antigravity, and Grok have no manifest here. No translated install docs.

Any other agent: paste `skills/straight-talk/SKILL.md` (everything under the second `---`) into its custom instructions. That is the whole mode.

## Turning it off

"stop straight talk" or "normal mode" in the conversation. On Claude Code, `/straight never` also removes the always-on flag file (`.off-my-plate-straight-talk` in your Claude config folder).
