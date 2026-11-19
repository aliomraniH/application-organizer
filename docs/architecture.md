# Architecture

The pattern has seven layers. Each has one job, and each job lives in exactly one layer. Three authority rules and three retrieval rules hold them together. This page says what lives where, why, and how a change moves through.

v1 had six layers. v2 adds the seventh, **structured memory**: a ledger of rows in the tracker artifact's database. The full schema is in [structured-memory.md](structured-memory.md).

## The seven layers

```mermaid
flowchart TB
    I["1 Project instructions: where things live, authority rules, which skills"]
    K["2 Project knowledge: stable-named files, overwritten in place"]
    D["3 Editable docs: the single source of truth for anything a person edits"]
    M["4 Memory: dated rules and decisions the person stated"]
    S["5 Skills: one per recurring procedure"]
    T["6 Scheduled tasks: short prompt that invokes a skill"]
    L["7 Structured memory: ledger rows in the tracker database"]
    I -->|points to| K
    I -->|points to| D
    I -->|names| S
    T -->|invokes| S
    S -->|reads and writes| D
    S -->|overwrites| K
    M -->|constrains| S
    S -->|reads registry first, writes rows| L
    L -->|points to| D
```

| Layer | Holds | Changes how often | Owner |
| --- | --- | --- | --- |
| Project instructions | where things live, authority rules, which skills | rarely | the person |
| Project knowledge | stable-named files: register, sweep axes, per-document sources, skill fallbacks | per pass, in place | skills |
| Editable docs | statements, Decisions doc, Contact log, evidence tracker, approved summary | daily | the person and Claude |
| Memory | dated rules and decisions the person stated | when the person decides something | background pass |
| Skills | one per recurring procedure | when a procedure changes | the person, via skill cards |
| Scheduled tasks | short prompt + skill, cheap model, few connectors | weekly or nightly runs | the person |
| Structured memory | registry, snapshots, events, tasks (working memory), claims (provenance), findings (research record), meta | every task and run | skills, through project-ledger |

### 1. Project instructions

Short: under 500 words. They say where things live, state the authority rules, name the skills that apply, and set one task per chat. They point to files instead of copying them, because every chat reads the instructions in full. Start from [templates/project-instructions.md](../templates/project-instructions.md).

Why short: context is a budget. Anthropic's guidance on [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) is to load the smallest set of high-signal tokens and fetch the rest just in time.

### 2. Project knowledge

A small set of files with **stable names**: `sweep-axes.md`, `ledger-schema.md`, `evidence-tracker.md`, `summary.md`, the scripts, and the rendered views (`register.md`, and a file per target if search needs one). Each is overwritten in place. A view is written only by `render_views.py` ([views.md](views.md)); the rest carry their version inside the file, not in the filename.

Why stable: when a project's knowledge grows past what fits in context, Claude searches it ([RAG for Projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)). Ten dated copies of one statement mean search can return the wrong one. History already lives in the editable doc's version history.

The one exception is the weekly sweep report, `sweep-<YYYY-MM-DD>.md`: one report per week is history, not a version of one thing. It is also how a file list grows without anyone deciding it should: a report older than eight weeks has done its work, because its findings are rows. The [pattern audit](../skills/pattern-audit/SKILL.md) holds the project to a file budget.

### 3. Editable docs

One editable doc (a Claude Doc or equivalent, see [Get started with Claude Docs](https://support.claude.com/en/articles/16923645-get-started-with-claude-docs)) per thing a person edits:

- each controlled document (a statement, an essay, a handbook section)
- the **Decisions doc**: every question waiting on the person, with options and a default ([template](../templates/decisions-doc.md))
- the **Contact log**: the only record of outreach ([template](../templates/contact-log.md))
- the **evidence tracker**: one tab per theme, updated after each sweep
- the **approved summary**: the statement of direction every other document must agree with

Why one: copies multiply writes. Edits happen in the doc. The ledger keeps a record of it, and every other copy is a view rendered from that record by script, never edited ([views.md](views.md)).

### 4. Memory

Dated rules and decisions the person stated, in their words: "2026-10-02: never name my previous employer in a statement." Memory never holds status that changes weekly (which email was sent, which version is current). Status lives in the docs, where it is visible and correctable.

### 5. Skills

One per recurring procedure, each short (well under the 500-line ceiling in the [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)). Each ends its open questions as rows in the Decisions doc, never in chat. See [skills/README.md](../skills/README.md).

### 6. Scheduled tasks

Short prompts that invoke a skill. The cheapest model that can do the job. Only the connectors the task needs, because included connectors can use every tool, writes included, without asking during a run ([scheduled tasks](https://code.claude.com/docs/en/routines)). See [model-and-usage.md](model-and-usage.md).

### 7. Structured memory

A small database in the tracker artifact, read and written by Claude as the person, and shown live on a [console page](../templates/console-page.html). It holds machine state the docs should not: the registry of every controlled document, one working-memory row per chat or run, the provenance of every cited fact, and every identifier a sweep has ever seen. The collections are `programs`, `snapshots`, `events`, `tasks`, `claims`, `findings` and `meta`. The project-ledger skill is their steward.

Why rows: status in prose rots. A row has a timestamp, a source and an author, can be queried without loading prose, and can be listed to disk instead of into context. See [structured-memory.md](structured-memory.md) and [working-with-data.md](working-with-data.md).

## Three tiers of memory

| Tier | Holds | Store | Why there |
| --- | --- | --- | --- |
| Working (one task) | what this chat or run read (doc and revision), decided, changed, left open | a `tasks/<id>` row | a new chat resumes from the row and reads only deltas |
| Project (months) | documents, decisions, contacts, evidence and their history | editable docs for anything a person edits; rows for machine state | docs give version history, comments and human editing; rows are queryable, timestamped and read without loading prose |
| Rules (durable) | dated rules in the person's words | memory | unchanged from v1 |

The rule that holds it together: **status never lives in prose or in memory; it lives in a row with a timestamp and a source.**

## The test layer for sources

When a project reads from connectors, MCP servers, APIs or a database, a test layer sits across the seven layers. It adds no new kind of thing; it is built from the same parts:

| Part | Layer it lives in | Job |
| --- | --- | --- |
| `sources.md` | project knowledge (stable file) | what each source may do, and the probes that prove it |
| source-check | skills | runs the probes: reachable, shape, scope, tools, write refusal, secrets, task hygiene |
| the check task | scheduled tasks | runs before the tasks that depend on the sources, on the cheapest model, carrying only the connectors under test |
| failure rows | editable docs (Decisions doc) | each failure, with the default "pause the dependent task" |

```mermaid
flowchart LR
    S["sources.md: expected access, scope, probes"] --> C["source-check runs the probes"]
    C --> R{"Result per check"}
    R -->|Pass| W["Results and change log in sources.md"]
    R -->|Fail or blocking Unverified| D["Decisions doc row, default pause the dependent task"]
    D --> P{"The person answers"}
    P -->|fix the setting| C
    P -->|accept the risk| W
    W --> T["Sweep and sync tasks run"]
```

The authority rules hold here too. The check proposes and never repairs: it does not enable a write, widen a scope or paste a credential to turn a Fail into a Pass. A check that cannot run is Unverified, not Pass, for the same reason a green task status is not success. See [connectors-and-mcp.md](../extensions/connectors-and-mcp.md#testing-sources) and [prompt 07](../prompts/07-test-connectors-and-mcp.md).

## The three authority rules

1. **The person's words win** over any older text: a doc, a file, memory, a source.
2. **Propose, wait for yes, then apply.** Nothing in a controlled document changes without the person's approval.
3. **Sync carries text and never revises facts.** If something looks wrong during sync, it becomes a Decisions-doc row.

## The three retrieval rules

1. **Registry first.** A task reads its `programs/<id>` row (and `tasks/` when resuming) before any document or file, then reads only deltas: `sinceRev` on a doc, `lastSeenSweep` on findings, events by `at`. Exact-text search confirms a paragraph is there before anyone says it is.
2. **No claim without a row.** A cited fact that reaches a controlled document has a claims row with its source and verification date. Whole-block writes carry the block hash and revision from a real read, so a write from a stale view fails instead of landing.
3. **New is not important.** A finding changes a document only if, judged against the cumulative findings that touch the same sentence, it moves the picture. `atRev` gives the document as it stood when a decision was recorded. Closed decisions stay closed; a change of mind is a new row.

## Comments as the inbox

A comment the person sends to Claude in a controlled doc is a decision made in place. Claude applies it in that thread, writes a tasks change line and an event, replies in the thread, and adds a Decisions-doc row only when the change needs a yes on something else. A comment's content never moves into memory.

## Gates before final

A controlled document is not final because someone says so. Two gates stand in front of that word, and both are described in [gates.md](gates.md).

| Gate | Acts before drafting | Acts at every write | Confirms at final |
| --- | --- | --- | --- |
| Authorship | the target's AI-use policy is read into a row with a mode | the mode decides what Claude may write; every span Claude writes or suggests is recorded | no recorded span is in the text under a policy that requires the person's own words; the person answers once |
| Claims | | every cited fact gets a claims row bound to its exact sentence | every number, citation and name sits inside a verified row at the level its kind needs |

The final check is a script, so it gives the same answer every time and costs no model judgment. It lists what is open. The person fixes or waives each item, in their words, with a reason; a contradicted source and a passage of Claude's wording under a restrictive policy can only be fixed. Final is bound to a hash of the text, so an edit returns the document to draft, and only the final check builds the file that is submitted.

The authority rules hold: the person's words win, which is why most items can be waived; propose, wait, apply, which is why a waiver is never a default; and nothing in a document is revised by the check itself.

A comment sent to Claude in a doc is still a decision made in place, within the target's mode: the person's own words are applied as given, and wording Claude supplies is written, suggested or withheld as the mode says.

## Phases

A target is `drafting`, `submitted`, `after` or `closed`, and the skills behave differently in each: sync stops reading a submitted document, the sweep stops proposing changes to it, and its open decisions are closed as moot on one confirmation. What a target still needs after its documents are in (letters, transcripts, verification, what comes next) lives in `requirements` rows with owners, lead times and source quotes. See [lifecycle.md](lifecycle.md).

## Keeping the project honest

Two skills look at the project instead of at a document. [review-loop](../skills/review-loop/SKILL.md) bounds judged comparisons with a noise band, an order-effect check and a round cap ([review-loop.md](review-loop.md)). [pattern-audit](../skills/pattern-audit/SKILL.md) checks the project against these pages and reports where it has drifted.

## How a change flows

Every change, whatever its source, passes through one approval and lands in one editable doc; the ledger records it, and the views are rendered from the record.

```mermaid
flowchart LR
    A["Source: sweep finding, reviewer comment, the person's idea"] --> B["Decisions doc row with options and a default"]
    B --> C{"The person answers"}
    C -->|yes| D["Editable doc updated"]
    C -->|no or silence| E["Default stays; row closed, never asked again"]
    D --> F["document-sync records it: snapshot, registry row, event"]
    F --> G["Views rendered once: register, target page"]
    G --> K["tasks row closed; console shows the activity"]
    C -.->|a durable rule stated| H["Memory: dated rule"]
    X["Comment sent to Claude in the doc"] -->|decision made in place| D
    R["findings rows: cumulative record"] -->|judge sees the record, not the week| A
```

The stations: source, Decisions doc, approval, editable doc, sync, ledger, closed tasks row. Only the approval needs the person. A comment sent to Claude is an approval given in place, so it goes straight to the editable doc. The findings rows feed the source station: a sweep finding becomes a Decisions-doc row only when the cumulative record says it moves the picture.

## What lives where, and why

| Question | Answer lives in | Ledger row | Not in |
| --- | --- | --- | --- |
| What is the current text of the statement? | its editable doc | `snapshots/<program>-<key>` (as last carried) | a dated file, memory |
| Which version is current, how many words, does it fit? | `register.md`, a rendered view | `programs/<id>` | memory, chat, a hand-edited register |
| What does this target still need, and what must I start today? | the register's Requirements table | `requirements/<program>-<slug>` | memory, a checklist in a chat |
| What follow-up is due? | Contact log | `contacts/<slug>.nextDue` | memory |
| Is this target still being drafted? | the register's Phase column | `programs/<id>.phase` | a note, a task prompt |
| Did the last judged round show anything? | the review-loop report | `reviews/<program>-<key>-<nn>` | a score table read by eye |
| Did I email Dr. Example? | Contact log | none | memory, an earlier chat |
| What am I waiting to decide? | Decisions doc | `events` with `decisionId` (pointers only) | a sweep report, a tracker note |
| What did this week's sweep find? | `sweep-<date>.md` | `findings` with `lastSeenSweep` = this week | the evidence tracker (it holds the synthesis) |
| Never name my old employer | memory, as a dated rule | none | the Decisions doc (it is not pending) |
| How to run the sync | `skills/document-sync/SKILL.md` | none | project instructions |
| When the sync runs | a scheduled task | `meta/config` | the skill |
| Does the Drive connector still work, and is it still read-only? | `sources.md` results, written by source-check | none; the ledger probe covers only the ledger itself | memory, an earlier chat |
| Where was this chat up to? | the newest `tasks` row | `tasks/<YYYY-MM-DD>-<slug>` | memory, a long chat |
| Where does this cited number come from? | the doc sentence | `claims/<program>-<key>-<nn>` | memory, the sweep report alone |
| May Claude draft for this target, and how? | the target's policy page | `programs/<id>.policy` (mode, quote, date read) | project instructions, memory alone |
| Which sentences did Claude write or suggest? | nowhere a person edits | `spans/<program>-<key>-<nnnn>` | chat history, memory |
| Is this document final, and for which text? | the register's status and "Gates open" columns | `programs/<id>.statements[].status` and `.final.hash`; `gates/<program>-<key>` | a note, a filename, a chat message saying "final" |
| Has the sweep seen this paper before? | the findings collection | `findings/<identifier>` | a prose ledger loaded whole |
