# Starter prompts

Thirteen copy-paste prompts. Each is self-contained: paste it into a chat in your Claude Project, answer its numbered questions in one reply, and it says what it will create before creating anything. The files hold only the prompt text, so you can copy a whole file.

| # | Prompt | Use it when | Creates or changes |
| --- | --- | --- | --- |
| 01 | [Bootstrap a project](01-bootstrap-project.md) | Starting a new campaign | Decisions doc, Contact log, one editable doc per document, stable project files, the tracker artifact with its console page and ledger, the first tasks row, project instructions, dated memory rules, scheduled tasks |
| 02 | [Migrate an existing project](02-migrate-existing-project.md) | You already have a project full of dated copies and status in memory | Stable files, the two docs, the ledger (backfilled by script), trimmed memory, shorter task prompts; deletes only after you confirm |
| 03 | [Set up the weekly sweep](03-set-up-weekly-sweep.md) | You want new papers, postings or updates found every week | `sweep-axes.md`, the sweep task, an optional post-sweep task, one test run |
| 04 | [Connect enterprise sources](04-connect-enterprise-sources.md) | Your documents live in Drive, SharePoint, Notion, Confluence or Slack | A sync rule per source, security rules, one read-only test per source |
| 05 | [Add a database](05-add-a-database.md) | Figures for the sweep or a skill live in a database | A read-only role (you run the SQL), an `.mcp.json` entry, named queries, a write-refusal test |
| 06 | [Weekly review](06-weekly-review.md) | Once a week, or before a deadline | Nothing until you answer; then each answer goes through the skill that owns it |
| 07 | [Test connectors and MCP](07-test-connectors-and-mcp.md) | After 04 or 05, after any source changes, or when a sweep comes back thin | `sources.md`, one supervised test run, Decisions-doc rows for failures, an optional scheduled check |
| 08 | [Backfill the record](08-backfill-the-record.md) | A project has prose records (a sweep ledger, a register) and is moving to the ledger | `findings` and `programs` rows by script, marked `ledger-transcribed`; the backfill record in `meta/ledger` |
| 09 | [Capability check](09-capability-check.md) | Monthly, or when a new Claude version or feature is out | A numbered proposal for the repo and the project; nothing until you approve; an optional monthly task |
| 10 | [Final check](10-final-check.md) | A document is nearly ready, or a project built before 0.4.0 needs the gates turned on | The check script as a project file, a policy row per target, claims rows for facts verified, a gate row, and on a pass the submission file; no document text changes |
| 11 | [Phase change](11-phase-change.md) | You submitted, a file became complete, a decision arrived, or you withdrew | Nothing until you answer; then registry phases, requirements and contact rows, closed moot decisions, re-aimed sweep axes, a rendered register, proposals for each scheduled task |
| 12 | [Pattern audit](12-pattern-audit.md) | Monthly, at a phase change, or when the project feels heavy | A table of nine checks with evidence, then numbered fixes; nothing until you approve; an optional monthly task |
| 13 | [Memory digest](13-memory-digest.md) | Memory is past half its cap, or the audit finds status or replaced rules in it | Nothing until you approve; then each current rule once, status moved where it belongs, replaced lines archived |

## How they fit together

```mermaid
flowchart LR
    A[01 Bootstrap] --> C[03 Weekly sweep]
    B[02 Migrate] --> C
    A --> D[04 Enterprise sources]
    B --> D
    D --> E[05 Database]
    C --> F[06 Weekly review]
    D --> F
    E --> F
    D --> G[07 Test sources]
    E --> G
    G -->|before each sweep| C
    G --> F
    B --> H[08 Backfill the record]
    H --> C
    F --> I[09 Capability check]
    I -->|monthly| I
    F -->|every week| F
    F --> J[10 Final check]
    J --> K[11 Phase change]
    K --> L[12 Pattern audit]
    L -->|memory over half its cap| M[13 Memory digest]
    L -->|monthly| L
    J -->|each document, before it is submitted| J
```

- Run **01** or **02**, never both. 01 starts clean and creates the tracker, console page and first tasks row; 02 audits what you have, deletes only what you confirm, and builds the ledger.
- **03**, **04** and **05** extend a project that already has a Decisions doc and Contact log. Each needs the files 01 or 02 created.
- **07** tests what 04 and 05 connected, and keeps testing it on a schedule so a broken source surfaces before a sweep or sync relies on it.
- **08** follows 02 when the old project kept a prose sweep ledger or register: it turns them into ledger rows by script, so the sweep stops loading prose.
- **09** keeps the pattern current: it compares what Claude offers now with [docs/capabilities.md](../docs/capabilities.md) and proposes changes.
- **10** turns on the gates in a project built before 0.4.0 and runs the first final check. After that, the final-check skill runs whenever you say a document is ready; 01 sets the gates up from the start.
- **11** turns the project when a target changes phase, so nothing keeps working on documents that can no longer change. **12** checks the project against the pattern and is the place to start when a project feels heavier than its work. **13** is what 12 sends you to when memory has filled with status and replaced rules.
- **06** is the habit. It reads everything the others built and asks you only what blocks the nearest deadline.

The prompts point at this repository for the templates and skills. If you forked it, change the repository address in each prompt to your fork.
