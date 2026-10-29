# Running Off My Plate in Claude Duet

Written 2026-10-22, the day after Anthropic announced Claude Duet. Everything below about Duet comes from launch coverage and the product page summaries, not from hands-on use, and is labeled accordingly. Verify against support.claude.com before relying on any of it.

## What Duet is (FACT, from coverage dated 2026-10-21/22)

- A proactive agent that runs on its own cloud virtual machine, so it works when your devices are off.
- Sends a morning brief, checks connected apps every few hours, and alerts when something needs attention.
- Asks before sending a message, making a payment, signing, or deleting. Will not trade securities or move money between accounts, even with approval.
- Research preview, waitlist, US Pro and Max accounts only. Join at claude.com/product/claude-duet with your Claude account email. Not on Team or Enterprise yet.
- Built on Opus; picks its own effort level.
- Carries over your Claude memory, skills, and connected apps. Works through connectors or a cloud browser.
- Cannot access local files. Cannot make calls or send texts. Microsoft 365 not yet supported. You cannot watch or take over its browser.
- Background checks use your Claude usage allowance; no separate Duet price announced.

## The mapping

| Off My Plate | In Duet |
|---|---|
| `morning-plate`, scheduled | The daily routine. You ask Duet once: "Every weekday at 7am run my morning plate" and confirm the schedule it created. (INFERENCE: coverage says follow-up instructions can set up repeated work; whether a plugin skill is invoked by name inside a Duet routine is unconfirmed.) |
| `plate/` workspace | A folder in a connected drive, named in `config.md`. Duet cannot read your laptop. (FACT: no local files.) |
| `inbox-sweep` | Duet's mail connector, read plus draft. (ASSUMED: the connected mail tool exposes a drafts tool; if it only exposes send, every reply becomes NEEDS YOUR GO and the text lands in the brief.) |
| `calendar-reality` | Duet's calendar connector, read only. |
| `AUTO` items | Duet does them in the background. |
| `DRAFT` items | Duet writes them into drafts. |
| `NEEDS YOUR GO` items | Duet's approval step. This plugin's gates are designed to line up with Duet's own stop points, so the brief's "Needs your go" block is the same list Duet would pause on. (INFERENCE.) |
| The brief | The morning brief. Phone-sized on purpose. |
| `plate_lint.py` and `plate-reviewer` | Run before the brief goes out when the runtime has a shell and plugin agents. (ASSUMED: nothing in coverage says Duet's cloud machine exposes a shell or runs plugin subagents. With no shell, `morning-plate` runs the RULES §3a lint by hand, date sweep first, and labels the brief UNLINTED, UNREVIEWED. With a shell but no agents, the lint script runs and the brief says UNREVIEWED.) |
| Mid-day alerts | `whats-missing` with a 48-hour deadline filter, on Duet's every-few-hours check (FACT: coverage says it checks every few hours and alerts when something needs attention). Dedupe against the last 7 Plates so it does not nag. (INFERENCE: whether a plugin skill can be the thing it runs on each check is unconfirmed.) |

## What this demonstrates for a Duet application

1. **Proactive, not reactive.** The product is the routine, not the chat. `morning-plate` is built to run with nobody watching.
2. **Approval design that matches Duet's.** Three gates, lint-enforced, so the agent can do real work alone and stop in exactly the right places.
3. **Memory across runs.** The graveyard, waiting-on, projects, and history files are the agent's memory of what it already said, what you already vetoed, and what you already dropped. A proactive agent without that memory is a nag.
4. **A real use case for a real small business.** One person, several brands, an inbox, a calendar, half-finished products, and a brain that is not the same every day. That is most solo operators; the ADHD framing makes the constraints explicit instead of pretending they do not exist.
5. **Verifiable output.** A script decides whether the Plate kept to one next step. The model does not grade itself.

## What Duet cannot do yet, and how the plugin copes

| Gap (FACT unless noted) | Coping |
|---|---|
| No local files | Workspace lives in a connected drive; `config.md` names it. |
| Checks every few hours, not continuously | Deadlines inside 48 hours get flagged a day early; the plugin does not promise same-hour alerts. |
| No texts or calls | Dentist-by-text, vet-by-phone items are always Keep or NEEDS YOUR GO, never AUTO. |
| Unconfirmed whether plugins run inside routines (INFERENCE) | The routine prompt in `morning-plate` is written so it works pasted as plain instructions, with the skill text as the fallback. |
| Uses your usage allowance | `morning-plate` reads only since the last Plate and dedupes against history to keep each run small. |

## Sources

- 9to5Google, "Claude Duet is Anthropic's proactive AI agent", 2026-10-21
- TechCrunch, "Claude Duet app is Anthropic's bet on agents", 2026-10-22
- MacRumors, "Anthropic Launches Claude Duet, a Proactive AI Agent", 2026-10-21
- CNBC, "Anthropic announces preview of Claude Duet", 2026-10-21
- flaviocopes.com, "A deep dive into Claude Duet" (summarizes the product page and getting-started guide)
