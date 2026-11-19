---
name: contact-log
description: Keeps and consults the Contact log, the only record of who was contacted, when, who replied and what is due, and keeps a ledger row per contact with its role and next due date so follow-ups can be queried. Use before answering anything about emails, replies or follow-ups, before drafting outreach, whenever the person says they sent or received a message, and when they ask what is due.
---

# Contact log

The editable doc at <CONTACT_LOG_URL> is the only record of outreach. Memory keeps no outreach status: the failure this prevents is a draft recorded as sent, or a send the person made themselves never recorded. Sections: how the log works; contacts by target (one row each: person, organization, role sought, address, sent dates, reply gist, status, next step); other contacts; to confirm; event log (newest first); closed or dropped. Status comes only from the dropdown: Not contacted, Drafted, Sent awaiting, Follow-up due, Replied closed, No reply closed.

## Answering a question about outreach
1. Search the doc for the surname or the target; read that row and its event rows.
2. Answer from the doc only, with its dates. If the row says not confirmed, say so and ask the to-confirm question once.
3. Never answer from memory or from an earlier chat. If the person's statement now differs from the doc, the person wins: update the doc and say what changed.

## When the person says they sent or received something
In the same turn: re-read the row; add an event row (date, person, event, source "the person, chat <date>"); update the row's sent or reply cell (append, keep earlier dates), status and next step; delete the to-confirm row it resolves; confirm in one line.

Only the person's word makes a send real. A draft Claude wrote is Drafted with its date until the person says it went out. Every draft handed over ends with: "Tell me when it's sent and I'll log it."

## Before drafting outreach
Read the person's row and the target's other rows. Do not draft to anyone marked do-not-contact or write-only-after-offer unless told to. Follow the outreach rules in project memory. Log the accepted draft as Drafted.

## The ledger row
The doc is the source; `contacts/<slug>` in the ledger at <TRACKER_URL> is its record. In the same turn the doc changes: `set · contacts/<slug> · {name, organization, program?, role, status, sent: [], lastReplyAt?, nextStep, nextDue, requirement?, closed?, logRev, updatedAt}`, then `update · meta/config · {contactLogRev}`.
- `role`: prospect, recommender, office, scheduler, reviewer, other. `requirement` links the contact to the requirements row it serves.
- No address in a row, ever. Addresses stay in the doc.
- Every row that is waiting on someone has a `nextDue`: the date the person gave, or 14 days after the send. A due date reminds the person. It is never a reason to draft or send unasked.
- If the doc's revision is ahead of `meta/config.contactLogRev`, the person edited it by hand: read the changed rows and rewrite their ledger rows first. Where doc and row differ, the doc wins.
- "What is due?": `query · contacts · where nextDue <= "<date>"`, then read those rows in the doc before answering.

## Rules
Never send anything; the person sends. Never put the person's own address anywhere new. Keep cells short; detail goes in the event log. Hygiene only when asked: rows past their next-step date, rows Drafted over a week, rows to confirm, in one message.

## Related skills
requirements holds what each contact's letter, transcript or reply is for. A question about a contact that only the person can settle (a send date nobody recorded, whether to follow up) becomes a row in the Decisions doc at <DECISIONS_DOC_URL> through decisions-queue, unless it is a to-confirm row that belongs in this log.
