---
name: inbox-sweep
description: Turns an inbox into commitments, requests, decisions, deadlines, and money, with drafts prepared and nothing sent. Reads the last 48 hours (or since the last Plate) through a connected mail tool or pasted email text and returns a short ledger - what the human owes people, what people owe them, what needs a decision, what can be archived unread - plus reply drafts gated for approval. Use when the user says "sweep my inbox", "what's in my email", "who am I ignoring", "what did I promise people", "draft replies", "triage my email", or when plate-triage calls it.
---

# Inbox sweep

Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` first, then `plate/config.md` (people who matter, standing no's) and `plate/waiting-on.md`.

## What you read

The last 48 hours, or everything since the date on the last Plate, whichever is longer. Use the mail connector's search and read tools. If there is no connector, work from pasted text and say so. Skip newsletters, receipts, and notifications unless a `config.md` rule names them (a receipt for a subscription they meant to cancel is money, not noise).

## What you extract

One ledger, five tables. Every row cites sender, subject, and date. Quote the sentence that makes it a commitment or a request; do not paraphrase a promise into something bigger.

1. **I owe them.** They said they would do something, or someone asked and is waiting. Columns: who, what (quoted), since, deadline (EVIDENCE if written, INFERENCE with a range if implied, blank if none).
2. **They owe me.** Something was promised to the human and has not arrived. Goes to `waiting-on.md` with a nudge-by date 5 working days out unless the mail says otherwise.
3. **Decisions.** Yes/no or pick-one questions the human alone can answer. State the question in one line and, where the workspace supports it, your recommended answer, labeled INFERENCE.
4. **Money.** Invoices to send, invoices unpaid, bills, renewals, refunds, anything with a dollar sign. Dates and amounts quoted.
5. **Archive unread.** Threads that need nothing. Count them; do not list them unless asked.

## What you draft

For every "I owe them" row that can be closed with a reply of under 150 words, write the reply in the human's voice from `config.md`. Put it in the connector's drafts folder if there is a draft tool, otherwise in `plate/drafts/<slug>.md`; both are `DRAFT` gate. Never send. Never reply-all. Never promise a date the human did not give you; write "by [DATE?]" and flag it.

For a "no" (declining a request), write the no plainly, with one reason or none, no apology spiral. Offer a redirect only if one is real.

## Output

```
## Inbox sweep · <window> · <N> threads read, <N> archive-unread

### I owe them
| Who | What (quoted) | Since | Deadline | Draft |

### They owe me  → appended to plate/waiting-on.md
| Who | What | Since | Nudge-by |

### Decisions
- <question> · recommended: <answer> (INFERENCE: <why>)

### Money
| What | Amount | Due | Action · gate |

### Drafts ready: <N> in <where> · Need your go: <N>
```

Feed the ledger back to `plate-triage` when called from it. Standing alone, end with the one reply the human should send first and why.
