---
name: requirements
description: Keeps one ledger row per thing each target needs (documents, letters, transcripts, evaluations, tests, fees, forms, steps after submission) with its owner, due date, lead time, status and source page, and says what must be started now. Use when a target is added, when the person asks what is left or what is due, when they say something was requested, sent or received, before a submission, and when a target's phase changes.
---

# Requirements

Expects schema **project-ledger v1**; the ledger is at <TRACKER_URL>. A target is more than its documents. This skill keeps the rest: what each target asks for, who has to produce it, how long that takes, and whether the target has it. Design: `docs/lifecycle.md` in the application-organizer repo.

## Rules
1. A requirement is read from the target's own pages or from the checklist in its application system, never remembered. Every row carries `source: {url, quote, readAt}`.
2. Submitted is not complete. A target is complete when every row is `verified`, `waived` or `na`. `verified` means the target's own system shows the item as received; the person's report of what it shows is the evidence, recorded with its date.
3. Anything another party produces has a lead time. Ask or look up how long it takes (a registrar, an evaluation service, a testing agency, a recommender). Unknown: use 21 days and say that it is an assumption. `startBy` is `due` minus `leadDays`.
4. Status moves only on evidence: the person's word, or a primary page. A drafted request is still `todo`.
5. Never store an address, an account number or an ID number in a row. Point to the Contact log instead (`contact`).
6. The rows are the source. The register's Requirements table is rendered from them and never edited.

## Setting up a target
1. Open the tasks row. `get · programs/<REGISTRY_ROW>`.
2. Read the target's requirements page, the page for the person's situation (an applicant from another country, a degree earned abroad, a career changer), and the application system's checklist if the person can show it. Read every page that the first page points to for a condition. Quote the sentence that sets each requirement.
3. Write one row per item: `set · requirements/<program>-<slug> · {program, item, kind, owner, due, leadDays, status: "todo", source: {url, quote, readAt}, contact?, document?, note, updatedAt, updatedBy}`. `kind`: document, letter, transcript, evaluation, test, fee, form, interview, other. `owner`: person, recommender, institution, target. A row for a controlled document names it: `document: "<program>-<key>"`.
4. Run `ledger_lint.py` over `list · requirements · out_dir <scratch>`. Show the person the table, with every item already past its `startBy` first.
5. A requirement that needs their choice (which service, which recommender, whether an unofficial copy is accepted) becomes a Decisions-doc row. A question only the target can answer becomes a contact row with a due date, through contact-log.

## When something moves
On the person's word, in the same turn: `update · requirements/<id> · {status, evidence, updatedAt, updatedBy: "the person, chat <date>"}`. Statuses: `todo`, `requested`, `sent`, `received`, `verified`, `waived`, `na`. If a linked contact exists, update its row through contact-log.

## What is left
`list · requirements · out_dir <scratch>`, then answer from the rows in this order: late, should have started, due in 14 days, waiting on someone else. Never answer from memory or from an earlier chat.

## Before a submission
List the target's rows. Every `owner: person` document row needs its document final (final-check). Say plainly which rows will still be open after the person submits, and when each is due.

## After a submission
When the person says they submitted, final-check records it. Then, here: set the target's `phase: "submitted"`; read the target's pages for what comes next (verification of materials, interview dates, decision dates, a reply deadline) and add those rows; list what is still open. When every row is done, say that the target is complete and set nothing else.

## Related skills
contact-log holds the people behind `contact` and their due dates. final-check makes a document final. document-sync renders the register. decisions-queue takes the choices. project-ledger defines the row shapes.
