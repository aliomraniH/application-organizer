---
name: decisions-queue
description: Checks, asks, records and adds items in the person's Decisions doc, and records what was asked and answered in the chat's working-memory row. Use at the start of any task that touches a controlled document, a target, a research doc or a contact, whenever a decision for the person comes up, and when the person answers one in chat, in the doc, or in a comment sent to Claude.
---

# Decisions queue

Expects schema **project-ledger v1**. One editable doc holds every decision waiting on the person: <DECISIONS_DOC_URL>. Sections by category; each row: ID, decision (one sentence), options and default, what it affects, status (Open, Answered, Applied, Closed), the person's answer, source. The rule: review the doc when a related task comes up, ask once, record the answer, act, never ask that item again. The ledger at <TRACKER_URL> records what each chat asked and was told.

## At the start of a task
0. Open the tasks row (project-ledger), or, when resuming, read the newest one: `query · tasks · order_by startedAt desc, limit 5`. Anything in its `decisionsAnswered` is not asked again.
1. Search the doc for the task's target, document or topic; read only matching rows.
2. If an Open row bears on the task, ask before doing the task: one question block, at most three items, each naming its ID and the options with the default marked. Do not ask rows that do not bear on the task. Record them: `update · tasks/<id> · {decisionsAsked: [...]}`.
3. If none bears on it, say nothing about the doc.
4. Never ask a row that is Answered, Applied or Closed, and never ask the same row twice in one conversation. A skipped row stays Open.

## When the person answers (in a question, in chat, or by typing in the doc)
1. Re-read the row; the person's edits in the doc win.
2. Write the answer with the date in the person's words; set status Answered. `update · tasks/<id> · {decisionsAnswered: [...]}`.
3. Act through the skill that owns the work. "No" or "leave it" changes nothing.
4. When done, set Applied, move the row to Closed items with what was done. Closed rows are never reopened; a change of mind is a new row.
5. If a ledger event points at this ID, mark it done: `update · events/<id> · {status: "done", resolution}`.

## A comment sent to Claude
A comment the person sends to Claude in a controlled doc is a decision made in place. The skill that owns the document applies it in the thread (document-sync for controlled documents). Add a row here only when the change needs a yes on something else, with source "comment, <doc>, <date>".

## Before re-opening a question
A new question that resembles a Closed row is checked against the record first:
1. Read the Closed row and its date. Read the document as it stood then: `atRev` at the revision named in the row or its event.
2. Read the cumulative record since: findings rows that touch the same sentence (`query · findings · where touches array-contains "<doc> ¶n"`), with count, direction and dates.
3. Add a new row only if the sentence changed since the decision or the cumulative record moved; say which, and cite the Closed row's ID. Otherwise do nothing: the decision still applies.

## Adding an item
Any skill or session that would otherwise leave a question in a report, a tracker note or a chat aside adds a row here instead.
1. Search first. An Open row that covers it is updated, not duplicated. A Closed row that covers it is acted on, not re-added, unless the check above says the record moved.
2. Otherwise add a row with the next free ID: a one-sentence question in plain words; options with the default (what stays in place on silence); what it affects; status Open; empty answer; source.
3. Update the open-item count at the top of the doc. Log a pointer: `set · events/<id> · {at, kind: "needs_person", status: "open", program, summary, decisionId}`.

Never put a pending decision into memory or into a row's prose; the doc is the record and rows only point at it by `decisionId`. Durable facts the person states while answering belong in memory as dated rules.

## Related skills
Every other skill in this set adds its questions here instead of leaving them in a report or a chat aside. The skill that owns the work applies the answer: document-sync for controlled documents, contact-log for outreach, approved-summary for the summary. project-ledger defines the tasks and events rows.
