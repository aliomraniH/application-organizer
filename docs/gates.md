# Gates

A gate is a check a controlled document must pass before it is called final. This page describes the two gates the pattern ships, authorship and claims, where each one acts, and what a pass means.

Version: **gates 1**, added in 0.4.0. It adds fields and two collections to the ledger without changing the schema version (**project-ledger v1**); a project turns it on with [prompt 10](../prompts/10-final-check.md).

## Why a check at the end is not enough

A check that runs only when a document is declared final has three weaknesses.

- **It runs on the worst day.** The deadline is close and the text is written. A check that blocks with no way through gets skipped.
- **It sees only what has a row.** A number that nobody recorded passes in silence, and that is the number most likely to be wrong.
- **"Final" is not one moment.** Documents are marked final and edited again the same day. Submission happens outside Claude, so Claude can gate only what it does itself.

So the pattern acts in three places. Most of the control sits at the first two; the final check confirms what the record already shows.

| Where | What happens | Who acts |
| --- | --- | --- |
| Before drafting | The target's AI-use policy is read and stored as a row with a mode | Claude reads; the person confirms the mode |
| At every write | The mode decides what Claude may write; every span Claude writes or suggests is recorded; every cited fact gets a claims row bound to its exact words | Claude |
| At final | A script compares the text with the record and lists every open item; the person answers the authorship question once | The script lists; the person decides |

## Authorship

### The policy row

Each target carries its policy in its registry row:

    programs/<id>.policy · { mode, sourceUrl, quote, readAt, readBy, recheckedAt?, note? }

`quote` is the sentence of the policy that decides the mode, short enough to check against the page. A target with no row is `unknown`, and Claude drafts nothing for it. A target that publishes no policy still gets a row: mode `open`, with a `note` naming the pages that were checked and the date.

### The mode decides what Claude may do

| Mode | The policy says | Claude may | Claude does not |
| --- | --- | --- | --- |
| `open` | nothing, or AI help is allowed | draft and edit in the editable doc | |
| `own-words` | the final wording must be the person's | propose wording as suggestions and in chat | write wording into the doc; accept its own suggestions |
| `feedback-only` | no AI drafting or outlining | comment on what the person wrote: what is unclear, missing, unsupported or over a limit | offer replacement wording or an outline, in the doc or in chat |
| `unknown` | not read yet | read the policy page | draft anything for the target |

Under `own-words`, a suggestion the person accepts unchanged is still Claude's wording, and the final check will say so. The suggestion is there to be read and rewritten.

When a policy is ambiguous, the stricter mode applies until the person says otherwise, and their words are recorded as a dated rule in memory.

### Spans: who wrote what

    spans/<program>-<key>-<nnnn> · { program, key, kind: "written" | "suggested", text, where: "doc" | "chat" | "comment", at, task }

Claude writes a span row whenever it writes wording into a controlled doc (`written`) or proposes wording for one, as a suggestion in the doc or as text in chat (`suggested`). Everything in the doc that no span covers is the person's.

At the final check, the script looks for each sentence of each span in the text. The match ignores case and punctuation, so changing a comma does not make a sentence the person's own. Sentences under eight words are not matched; a short phrase is too common to attribute.

- Under `open`, matches are counted and reported. That count is the authorship record [lesson 10](lessons.md#10-know-each-targets-ai-use-policy-before-drafting) asks for.
- Under `own-words` and `feedback-only`, a match is a failed item. It takes no waiver. The fix is the person's rewrite, or a corrected policy row with its source.

### One question, asked once

Under `own-words` and `feedback-only`, after every other item has passed, Claude shows the person the policy quote and what the record shows, and asks once whether the wording is their own as the policy requires. The answer is stored in their words in the gate row. Anything other than a clear yes leaves the document in draft.

### What this does and does not show

The record shows who typed a sentence. It cannot show who thought of it, and it does not see text the person carried in from somewhere else. The attestation a target asks for is the person's to make. The gate's job is to make sure they make it with the record in front of them, and that Claude never makes it for them.

## Claims

### Bind a claim to its words

A claims row carries a `span`: the exact words in the document that state the fact, usually one sentence.

    claims/<program>-<key>-<nn> · { span, kind, ..., recheckBy? }

A claim holds for as long as its span is in the text. An edit elsewhere in the document changes nothing, so there is nothing to re-point. An edit inside the span removes it from the text; the facts it covered become uncovered, and the row is reported as no longer in the text. `docBlockId` and `docRev` stay in the row as a record of where the sentence stood when it was verified; nothing depends on them.

### The detector

The script scans the text for the shapes a checkable fact takes: figures, number words, years, citations, titled people, organizations, and runs of capitalized words. Every hit must fall inside the span of a claims row. A hit outside every span is reported as uncovered.

The detector over-reports on purpose. A hit costs one row or one waiver; a miss costs a wrong fact in a submitted document. One row can cover a whole sentence of the person's own history, so a personal paragraph costs a few rows, confirmed once. Its known blind spots are single proper nouns ("Medicare") and facts stated without a number or a name. Those still need a reader.

### The level each kind needs

| Kind | What it is | To pass |
| --- | --- | --- |
| `number` | a figure quoted from a source | verified on a page where the number appears (full text, abstract or primary page); a qualifier in the row; if the source is a preprint, the sentence says so |
| `work` | a description of someone's work, role, program or page | verified at a primary page or better, never from metadata alone |
| `account` | the person's own history or experience | the person's confirmation, recorded as theirs |
| `unpublished` | internal or unpublished results | the person's confirmation, and the sentence itself says the result is unpublished |

A row with `recheckBy` covers a fact that can change: who is recruiting, an affiliation, an award status, a policy. Past that date the row fails until someone looks again.

## The final check

The check is a script, [`templates/final_check.py`](../templates/final_check.py), run by the [final-check skill](../skills/final-check/SKILL.md). It needs no model and gives the same answer every time.

### Three outcomes per item

| Outcome | Meaning |
| --- | --- |
| pass | nothing to do |
| fail | the document is not final |
| waived | the person accepted this item, in their words, with a reason |

A waiver belongs to one item. It is never proposed in bulk, never inferred from silence, and never the default of a Decisions-doc row: the default for an open gate item is "not final".

Two kinds of item take no waiver, only a fix:

- a source that is contradicted or retracted for the sentence it supports
- a passage matching Claude's wording under `own-words` or `feedback-only`

A missing policy row and a missing attestation are also fix-only, because the fix is one page read or one question.

### Final is bound to the text

    programs/<id>.statements[].status · "draft" | "final" | "submitted"
    programs/<id>.statements[].final  · { hash, at }
    gates/<program>-<key>             · the script's output for the text that passed

The gate row stores a hash of the text it checked. The document is final only while its text has that hash. Any later edit returns it to draft at the next sync, with an event. `submitted` is set only on the person's word and records the hash that went out.

### One path to a submission file

Only the final check builds the file the person submits, from the same text it hashed. A scheduled run never finalizes, never builds a submission file and never marks anything submitted.

### A preview from the first day

document-sync runs the same script with `--preview` on every pass and writes the open-item count to the registry row, where the register's "Gates open" column shows it. Seven days before a target's deadline, an open count becomes one Decisions-doc row. The last day should hold no surprises.

## Rows added to the ledger

| Row | Written by | Read by |
| --- | --- | --- |
| `programs/<id>.policy`, `.deadline` | final-check, the bootstrap prompt | every skill that writes wording |
| `programs/<id>.statements[].status`, `.gateOpen`, `.final`, `.submitted` | document-sync (preview, return to draft), final-check | the register, the weekly review |
| `claims.span`, `.kind`, `.recheckBy`; statuses `contradicted` and `retired` | whoever writes the claims row | final-check, document-sync |
| `spans/<program>-<key>-<nnnn>` | any skill or chat that writes or proposes wording | final-check |
| `gates/<program>-<key>` | final-check | document-sync, the console |
| `meta/ledger.gates` | project-ledger, when the gates are turned on | every skill |

Field-level shapes are in [templates/ledger-schema.md](../templates/ledger-schema.md); example rows are [templates/gate-row.json](../templates/gate-row.json) and [templates/span-row.json](../templates/span-row.json).

## Tests

[`tests/final_check.test.py`](../tests/final_check.test.py) runs the script over synthetic rows. Each test is named for the failure it stops: a Claude passage under `own-words`, a number with no row, an edit after final, a waiver without a reason, a contradicted source someone tries to waive.

## Limits

- The gate reads the ledger. A span Claude failed to record is invisible to it, so recording spans is a hard rule in every skill that writes wording.
- The detector is a set of text shapes. It is tuned for English prose and for facts that carry a number or a capital letter.
- A pass means the record is complete and the person has answered. It does not mean the document is true, good or admissible.
