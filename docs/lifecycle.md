# Lifecycle: phases, requirements and contacts

A campaign is not one activity. It drafts, it submits, it waits and prepares for what comes next, and it ends. The machinery that helps in one phase is waste, or a hazard, in the next. This page describes the phases, what each skill does in each, and the two record types that carry a target from "documents ready" to "complete": requirements and contacts.

Added in 0.4.0.

## Phases

Each target has a phase in its registry row:

    programs/<id>.phase · "drafting" | "submitted" | "after" | "closed"
    programs/<id>.submittedAt?, .outcome?

| Phase | Means | Ends when |
| --- | --- | --- |
| `drafting` | documents are being written | the person says they submitted |
| `submitted` | the documents went in; other items may still be open | every requirement is done (the target is complete) |
| `after` | complete; what follows is interviews, visits, questions, waiting | the target decides, or the person withdraws |
| `closed` | over, with an `outcome` in the person's words | never |

A phase changes only on the person's word or on the rows (the move from `submitted` to `after` is every requirement being done). The campaign has no phase of its own; it is whatever its targets are.

### What each skill does in each phase

| Skill | `drafting` | `submitted` and `after` | `closed` |
| --- | --- | --- | --- |
| document-sync | records and renders | does not read the documents; a nightly task with no drafting target proposes pausing itself | nothing |
| final-check | previews and checks | records what was submitted | nothing |
| weekly-sweep | A items: what touches a current document | no A items against submitted text; the same findings are filed for preparation instead | drops the target from the watch list on the person's yes |
| decisions-queue | asks what bears on the task | offers, once, to close rows about frozen documents as moot | |
| requirements | what must be started now | what is still open; then what comes next | |
| contact-log | outreach | offices, recommenders, schedulers; follow-ups by due date | |
| review-loop | runs | does not run on submitted text | |

The principle: **nothing proposes a change to a document that can no longer change.** A finding that would have altered a submitted sentence is still worth knowing, as something to be ready to talk about. It is filed that way and raises no decision.

### When a phase changes

[Prompt 11](../prompts/11-phase-change.md) does the turn in one pass: records the submission, sets the phase, closes moot decisions on one confirmation, adds the requirements that come next, re-aims the sweep axes, and proposes which scheduled tasks to pause. Scheduled tasks are the person's; the prompt proposes and they decide.

## Requirements

    requirements/<program>-<slug> ·
      { program, item,
        kind: "document" | "letter" | "transcript" | "evaluation" | "test" | "fee" | "form" | "interview" | "other",
        owner: "person" | "recommender" | "institution" | "target",
        due, leadDays,
        status: "todo" | "requested" | "sent" | "received" | "verified" | "waived" | "na",
        source: { url, quote, readAt },
        contact?, document?, evidence?, note, updatedAt, updatedBy }

One row per thing a target needs. Four ideas carry the design.

**Read, do not remember.** Every row quotes the sentence on the target's own page that sets the requirement, with the date it was read. Requirements differ by target and by the person's situation, and the conditions that bite are on the second page, not the first: the page for degrees earned abroad, the page saying which evaluation services count, the line saying a file is not reviewed until it is complete.

**Submitted is not complete.** Pressing submit sends the documents. A target is complete when every row is `verified`, `waived` or `na`, and `verified` means the target's own system shows the item as received. Many targets do not review an incomplete file, and some do not say so loudly.

**Lead time.** A document the person writes can be finished the night before. A transcript sent by a registrar, a credential evaluation, a test score or a letter cannot. Each such row carries `leadDays`, and `startBy` is `due` minus `leadDays`. The register and the weekly review put anything past its `startBy` at the top. Without a row and a lead time, a requirement of this kind is found on the day of submission, when nothing can be done about it in time.

**Evidence moves status.** A row moves on the person's word or a primary page, and records which. A drafted request is still `todo`.

Requirements rows are the source; nobody edits a requirements doc. The register's second table is rendered from them.

## Contacts

The Contact log stays what it was: an editable doc, the only record of outreach, read before anything is said about who was written to. 0.4.0 adds an index of it in the ledger:

    contacts/<slug> ·
      { name, organization, program?,
        role: "prospect" | "recommender" | "office" | "scheduler" | "reviewer" | "other",
        status, sent: [], lastReplyAt?, nextStep, nextDue,
        requirement?, closed?, logRev, updatedAt }

- **The doc is the source; the row is its record**, in the same relation as a statement and its snapshot. contact-log writes the row in the same turn it changes the doc. If they differ, the doc wins and the row is rewritten. If the doc's revision is ahead of `meta/config.contactLogRev`, the person edited it by hand, and the changed rows are read again first.
- **No address in a row.** Addresses stay in the doc. `ledger_lint.py` treats an address in any row as an error.
- **`nextDue` is the point.** A follow-up date in a doc table cannot be queried or scheduled. In a row it can: `query · contacts · where nextDue <= "<date>"` answers "what is due" without loading the log, and the weekly review lists what has passed. A due date is a reminder to the person. It is never permission for Claude to send or to draft unasked.
- **Roles.** The log was built for one kind of contact, someone being asked for something. After submission most contacts are offices, recommenders and schedulers. `role` says which, and `requirement` links a contact to the row it serves, so "has the letter arrived" and "who do I ask" are one lookup.

## What the register shows

One page, rendered: every document with its status and open gate items; every requirement with its owner, status, start-by and due date; what needs attention; what is due in the next 14 days. See [views.md](views.md).
