# One source, rendered views

A controlled document has one place where its text is edited. Everything else that shows the text or its status is a view: produced by a script from ledger rows, never edited, never read back as a source. This page says why, what the parts are, and what a version costs.

Added in 0.4.0. It replaces the four-place sync of 0.2.0 and 0.3.0.

## What was wrong with the earlier design

[Lesson 1](lessons.md#1-one-editable-doc-per-thing-people-edit) said one editable doc per document. The sync skill then kept that doc, a published copy, a project file and a register row saying the same thing, and wrote all of them for every version. The lesson and the skill disagreed, and the skill won. In the origin campaign that meant:

- A version cost six or more writes, each a place the copies could part.
- The copies gathered history: change logs, old gates, notes. Published pages passed 90 KB.
- The sync had to read a whole copy before replacing it, so past a certain size a run could no longer finish. The register, at 40 KB, had to be carried forward by a model, word for word.
- On a busy day, most of the work was copying.

## The three kinds of thing

| Kind | What it is | Who writes it | Example |
| --- | --- | --- | --- |
| **Source** | the one place the text is edited | the person, and Claude within the target's policy mode | the editable doc |
| **Record** | what the ledger knows about the source as last seen | document-sync, three row writes per version | `snapshots/<program>-<key>`, the statement entry in `programs/<id>`, one event |
| **View** | a rendering of the record for someone to read | `render_views.py`, and nobody else | `register.md`; a target's page; a project-file export for search |

Rules that follow:

1. **Text moves one way.** Source to record to view. Nothing is ever copied from a view into a source.
2. **A view is a script's output.** A model does not type it, tidy it or carry it forward. If a view looks wrong, a row is wrong, or the script is.
3. **A view holds the present.** History lives in the editable doc's version history and in the ledger's events, where it costs nothing to keep and nothing to skip.
4. **A view has a budget.** The script refuses to write a view over its budget (15 KB for the register, 30 KB for a page) and exits with a code saying so. That becomes a Decisions-doc row. Raising a budget is the person's choice, made once and written down.
5. **A view can be thrown away.** Delete any view and the next render restores it. If deleting something would lose information, it was not a view.

## What a version costs

| | 0.3.0 | 0.4.0 |
| --- | --- | --- |
| Writes when the person accepts an edit | doc, published copy, project file, register row, snapshot, registry row, event | doc, then snapshot, registry row, event |
| Reads before writing | each copy in full | the changed blocks of the doc |
| Views | rewritten every version | rendered once per run, only if a record changed |
| A draft the person has not accepted | often synced | never synced |

In a chat with several accepted edits, the record is written once, before the final reply. Views are rendered at most once per chat, and otherwise by the nightly task.

## The script

[`templates/render_views.py`](../templates/render_views.py), standard library only:

    render_views.py register --ledger <dir> --out register.md
    render_views.py page --ledger <dir> --program <id> --out <id>.md

`<dir>` is the collections listed to disk (`list · programs · out_dir <dir>` and so on). The register has a documents table (target, phase, document, version, status, words, fit, open gate items, deadline, policy mode) and, when the project has requirements rows, a requirements table with what needs attention and what is due in the next 14 days. A page has each of a target's documents as last recorded: the current text and one status line.

The same rows and the same date always give the same bytes, so a view can be compared with a fresh render to find a hand edit.

## Mirrors

Sometimes a second editable copy cannot be avoided: a team drafts in a shared Drive or SharePoint file, or a reviewer will only comment in their own tool. That copy is a **mirror**. It is declared in the registry (`statements[].mirror`), and only a declared mirror gets two-way treatment: a change in the mirror alone is proposed into the source, and a change on both sides is a conflict that goes to the Decisions doc with both versions quoted. A mirror is a cost accepted for a reason; a view is the default.

## Variants

Some documents come in a family: one body shared across targets, with a few lines that differ per target (a CV, a cover letter, a biography). Copying the body once per target is the four-copy problem again, turned sideways: a fix to the shared part has to be made in every copy, and some get missed.

The rule: one source for the shared body, one small source per target holding only what differs, and a build that joins them. 0.4.0 states the rule and the [pattern audit](../skills/pattern-audit/SKILL.md) checks for scripts or files copied once per target. It does not ship a builder; the joining step depends on the file format.

## Registry fields

    programs/<id>.master  · { url }      the target's page view, if it has one
    programs/<id>.source  · { path }     the project-file view, if it has one
    programs/<id>.statements[].mirror · { url, kind }   only for a declared mirror
    meta/config.views     · { register: "register.md", budgets?: { register, page } }

`master` and `source` keep their 0.3.0 names so existing rows stay valid. Their `version` fields are no longer written: a view has no version of its own.

## Moving a 0.3.0 project

1. Render the register with the script and compare it with the hand-kept one. Anything the old file holds that the render lacks is either history (leave it in the events) or a fact that belongs in a row (add the row).
2. For each published copy: move anything that is not current text into the place it belongs (a decision to the Decisions doc, a fact check to a claims row, a note to an event), then replace the copy with the rendered page.
3. Replace the sync task's prompt with the current one. Run [prompt 12](../prompts/12-pattern-audit.md) and check item 7.
