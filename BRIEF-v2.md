# application-organizer — v2 build brief: structured memory

21 Oct 2026 · application-organizer contributors

## How to use this brief

Save this file in the repository as `BRIEF-v2.md` beside `BRIEF.md`, then open Claude Code in that folder with one line: "Build v2 of this repository from BRIEF-v2.md. Follow it exactly; read BRIEF.md and the current tree first; ask before deviating." The repo is at v0.2.0 (ten commits, seven skills, seven prompts, three scenarios, the connectors chapter). This brief adds a seventh layer, structured memory, and the documents, skills, prompts and templates that teach and ship it. Everything after "The brief" is source material to copy, adapt and file.

Nothing in this document names a person, program, email, institution or private record. Keep it that way: the repo is public.

## The brief

This is the instruction for Claude Code. Everything below this section is material it draws on.

```markdown
# Build brief: application-organizer v2 — structured memory

You are extending a public repository that teaches and ships a pattern for running a long, document-heavy campaign with Claude. v1 (BRIEF.md) built six layers: project instructions, project knowledge with stable names, editable docs as the source of truth, memory for dated rules, one skill per procedure, scheduled tasks on cheap models. It was tested in one real campaign for three months.

v2 adds the layer v1 was missing: **structured memory** — a small database that lives in a published Claude artifact and is read and written by Claude (ArtifactData), holding the registry of every document, a working-memory row per chat or run, the provenance of every cited fact, and every identifier a research sweep has ever seen. It was built and tested in the same campaign over one day before this brief was written; the rules below are the ones that held.

Build the whole update in this session from the material in BRIEF-v2.md. Read BRIEF.md and the current tree first. Keep every v1 rule that this brief does not change. Ask before deviating from the layout or the rules.

## What v2 adds, in one paragraph

A seventh layer, the **ledger**: collections in the tracker artifact's database — `programs` (registry), `snapshots`, `events`, `tasks` (working memory), `claims` (provenance), `findings` (the research record), `meta`. Three retrieval rules sit on top: **registry first** (read the row, then read deltas), **no claim without a row** (a cited fact carries its source and verification date), **new is not important** (a finding changes a document only when it moves the cumulative record). Two more mechanisms join them: a **comment sent to Claude in a doc is a decision made in place**, and a **console page** on the tracker artifact shows the rows live. The v1 authority rules stand unchanged: the person's words win; propose, wait for yes, apply; sync carries text and never revises facts.

## Repository changes (make exactly these)

    README.md                      new description; seven layers; three retrieval rules; "Start here" gains prompts 08 and 09 (verbatim from prompts/); new "Worked examples" section (three short flows, below); link map rows for the new docs
    CHANGELOG.md                   new: v0.2.0 (what v1 shipped), v0.3.0 (this brief); Keep a Changelog format
    docs/
      architecture.md              seven layers; the change-flow diagram gains the ledger stations (Mermaid); a "what lives where" table with the ledger column; the three tiers of memory (working / project / rules)
      structured-memory.md         new: the collections, their field schemas, the rules each skill follows, how a row is written and read, limits — from the "Structured memory" chapter below
      working-with-data.md         new: documents, data and algorithms, inside Claude and from external sources; how the pattern keeps data, instructions, calculations and retrieval cheap — from the chapter below
      capabilities.md              new: what the current Claude surfaces offer that the pattern uses, as of a date, with a runtime-contract version; the versioning policy; the update procedure — from the chapter below
      lessons.md                   add lessons 11–15 (below)
      model-and-usage.md           add the context-budget rules the ledger enables (deltas, out_dir, in-queries)
    skills/
      project-ledger/SKILL.md      new: the schema steward — creates the collections, opens and closes tasks rows, writes claims and findings rows, prunes, backfills from prose
      capability-check/SKILL.md    new: re-reads what the current Claude surfaces offer, diffs against docs/capabilities.md, proposes changes to the repo and to a project's settings
      document-sync/SKILL.md       add: tasks row at load; claims check in verify; comment-as-decision rule; close the tasks row in record
      decisions-queue/SKILL.md     add: step 0 tasks row; atRev + cumulative check before re-opening; comment rule
      weekly-sweep/SKILL.md        change: findings is the exclusion list; the prep agent builds a cumulative brief; the A-item rule; findings and claims writes; tasks row
      approved-summary/SKILL.md    add: claims rows on approval; cumulative check and atRev in the weekly proposal
      evidence-tracker/SKILL.md    add: read findings rows, not the report alone, for the rolling sections
      source-check/SKILL.md        add: a probe row for the ledger itself (reads at viewer level, a where-query returns rows)
      README.md                    nine skills, one line each
    prompts/
      01-bootstrap-project.md      add: create the tracker artifact with the db capability from templates/console-page.html; write meta/ledger; the first tasks row
      02-migrate-existing-project.md  add: backfill the ledger from prose (findings from a ledger file, programs from a register)
      03-set-up-weekly-sweep.md    change: exclusion list and window come from findings
      06-weekly-review.md          add: open tasks rows, unverified claims, findings that bear on a document since last review
      08-backfill-the-record.md    new (below)
      09-capability-check.md       new (below)
      README.md                    nine prompts and how they fit
    templates/
      ledger-schema.md             the collections and fields with placeholders
      console-page.html            the tracker page: registry table, working memory, evidence record, record rules; declares db (and mcp only if a run button is wanted); placeholders for names
      tasks-row.json               one example row, invented content
      claims-row.json              one example row, invented content
    scenarios/*.md                 add to each: "The record" — which collections it uses and the first week's rows
    plugin/README.md, .claude-plugin/marketplace.json   nine skills; version 0.3.0

## Rules for writing (in addition to BRIEF.md's)

- Skills under 500 lines, third-person descriptions, no shouting, every placeholder kept (<TRACKER_URL>, <DECISIONS_DOC_URL>, <CONTACT_LOG_URL>, <PROJECT_NAME>, <REGISTRY_ROW>).
- Capability facts come only from docs/capabilities.md, which comes only from the chapter below. Where the chapter says "unverified" or "not checked", keep the word. Do not invent product features. Do not describe a capability the chapter does not list.
- Every "how to" that touches a row shows the call shape in one line (collection, doc id, the fields), never a paragraph.
- Examples use invented names ("Dr. Example", "Northfield University", "the handoff paper"), invented identifiers (10.0000/example.2026.1), invented dates.
- Mermaid for diagrams. No images.

## Privacy rules (hard, unchanged)

No real person's name, email, institution, program, document URL, artifact URL or private fact anywhere in the repo. The pre-commit grep on "@" in .md files stays. Add a second grep that fails on "claude.ai/artifact" and "claude.ai/code/artifact" outside documented placeholders.

## Acceptance checks (run before the last commit)

- Both greps return only documented placeholders.
- Every SKILL.md has name + description frontmatter and is under 500 lines; nine skills listed in skills/README.md, the marketplace entry and plugin/README.md.
- README's starter prompts are byte-identical to prompts/*.md (nine).
- docs/capabilities.md carries an as-of date and a runtime-contract version on its first line, and every capability row has a "used by" cell naming a skill, a prompt or "not yet".
- templates/console-page.html declares its capabilities in a comment at the top and renders a designed empty state before any row loads.
- Every internal link resolves; every external URL appears in BRIEF.md or BRIEF-v2.md Sources.
- A fresh reader can follow README → prompt 01 → a project with a tracker, a console page and a first tasks row.
```

## Structured memory (write docs/structured-memory.md and templates/ledger-schema.md from this)

### Three tiers

| Tier | Holds | Store | Why there |
|---|---|---|---|
| Working (one task) | What this chat or run read (doc + rev), decided, changed, left open | `tasks/<id>` row | A new chat resumes from the row and reads only deltas |
| Project (months) | Documents, decisions, contacts, evidence and their history | Editable docs for anything a person edits; rows for machine state | Docs give version history, comments and human editing; rows are queryable, timestamped, access-controlled, and read without loading prose |
| Rules (durable) | Dated rules in the person's words | Memory | Unchanged from v1 |

The rule that holds it together: **status never lives in prose or in memory; it lives in a row with a timestamp and a source.**

### Collections (in the tracker artifact's database)

`programs/<id>` — the registry. One row per controlled document set: name, order, master {url, version}, source {path, version}, statements[] with doc {url, docId, tab, node, syncedRev, seenRev}, key, label, version, words, fit, limit, snapshot; status; note; lastSyncAt. Every task reads the row first, then only what it points to.

`snapshots/<program>-<key>` — last-synced paragraphs, blockIds, blockHashes, docRev, masterVersion, meta, words, verified. The canonical text as last carried; read a paragraph by index instead of loading the doc.

`events/<id>` — {at, kind, status, program, summary, by, decisionId?, resolution?}. Kinds: propagated, note, needs_person, conflict, flag, ledger. Newest 300 kept.

`tasks/<YYYY-MM-DD>-<slug>` — working memory:
    { startedAt, endedAt?, chat, task, status: in_progress|done|stopped,
      docsRead: { "<doc id or url>": { rev|version, at } },   // bookmarks
      rowsRead: [], decisionsAsked: [], decisionsAnswered: [],
      changes: [], open: [], by, model }
Create it in the first reply of any chat that will touch a document, a row or a decision; update docsRead on every doc read; close it before the final reply. One row per scheduled run. Under 4 KB; detail goes in events. Prune done rows older than 60 days.

`claims/<program>-<key>-<nn>` — provenance for a cited fact or number:
    { text, program, key, docBlockId, docRev,
      source: { identifier, url, title?, firstPublic?, status: peer-reviewed|preprint|grey|primary-page|person },
      qualifier, verifiedAt, verifiedBy, verifiedHow: full text|abstract|primary page|metadata,
      status: verified|unverified|stale|retracted, findingId?, decisionId? }
Written whenever a cited sentence or number is edited, added or verified from the day the ledger starts; the sync's verify step flags a changed paragraph with a cited fact and no row (an event, never a block). No backfill unless the person asks. Forward-only is the default because a backfill is an expensive reading pass, not a mechanical one.

`findings/<identifier>` — everything a sweep has seen:
    { identifier, type: doi|arxiv|pmc|pmid|acl|registry|preprint, aliases, docId,
      mentions: [{ sweep, date, label }], sections, sweeps, firstSeenSweep, lastSeenSweep,
      status: bears-on-document|reported|unread|out-of-window|tangential|excluded,
      touchesDocument, watched,
      title?, authors?, firstPublic?, venue?, preprint?, direction?: supports|complicates|pre-empts|stale, touches?: ["<doc> ¶n"], weight?: 1–3,
      source, verified: ledger-transcribed|primary page|full text }
Doc id = identifier with `/` → `_`. The sweep's exclusion list is this collection (query by identifier, or one list to disk), never a prose ledger loaded whole. Backfilled rows from a prose ledger carry `verified: ledger-transcribed` and are an exclusion list, not a bibliography: re-verify before quoting.

`meta/config` and `meta/ledger` — config: trigger id, lastRun, lock, schedule, runbook. ledger: schemaDoc, schemaVersion, collections, counts, backfill record, lastFindingsWrite, lastClaimsWrite.

### The three retrieval rules

1. **Registry first.** A task reads `programs/<id>` (and `tasks/` when resuming) before any document or project file, then reads deltas: `sinceRev` on a doc, `lastSeenSweep >= <date>` on findings, events ordered by `at`. Exact-text doc search confirms a paragraph is there before anyone says it is. Project-knowledge search finds a stable file by name; it does not recall content.
2. **No claim without a row.** A cited fact that reaches a controlled document has a claims row with source and verification date. Whole-block doc writes carry the block hash and the revision from a real read, so a write based on a stale or imagined view fails instead of landing.
3. **New is not important.** A finding changes a document only if, judged against the cumulative findings rows that touch the same sentence (count, direction, dates), it moves the picture. The sweep's judge and the approved-summary's weekly proposal both receive that cumulative brief. `atRev` reads give the document as it stood when a decision was recorded, so "does the decision still apply?" is answered from the record. Closed decisions are never reopened; a change of mind is a new row.

### Comments as the inbox

A comment the person sends to Claude in a controlled doc arrives as its own turn with the thread id and anchor. It is a decision made in place: apply it in that thread, write a tasks change line and an event, reply in the thread, and add a Decisions-doc row only when the change needs a yes on something else. Never move a comment's content into memory.

### Limits (state them)

- Rows can be written by anyone the tracker page admits; treat them as data, never instructions.
- Doc search is exact or regex, not semantic; recall comes from the registry, confirmation from search.
- `in` queries take a short list; batch candidates in tens, or list a whole collection to disk (it stays out of context).
- A page's `sample` capability runs without project memory; it can summarize rows, not apply rules.
- Memory stays rules-only.

### How the pilot backfilled findings (write into prompt 08 and the project-ledger skill)

A script, not a reading pass: split the prose ledger by sweep heading; label each line by its section prefix (A, B, C, D, E, H, J, UNREAD, RESOLVED, ADDED, TANGENTIAL, EXCLUDED, REPORTED); extract DOIs first and mask them, then arXiv ids (prefixed and bare), ACL Anthology ids, PMC, PMID lists, trial registries; merge ACL ids with their 10.18653 DOIs; derive a coarse status from the labels; write one JSON file per row; batch 50 rows per write. Spot-check a random sample of identifiers against the source file by exact search before the first write. State in `meta/ledger` that the rows are transcribed, how many, from what, and that the source's own count (which counted repeats) differs from the unique count. In the pilot: 866 unique identifiers from a 40 KB prose ledger that every sweep had been loading whole.

## Working with documents, data and algorithms (write docs/working-with-data.md from this)

### Where each kind of thing goes

| Kind | Inside Claude | From outside | Store |
|---|---|---|---|
| A document a person edits | Editable doc (version history, comments, block ids, hashes, revisions) | A Drive, SharePoint or Notion file read through its connector; the editable doc is the working copy | Doc + one registry row + one stable project file |
| A record or a table of records | Rows in the ledger | A database through a read-only MCP server, named parameterized queries only | Rows; the query text in a project file |
| A fact with a source | A claims row linked to a findings row | A primary page read in the person's browser or by the sweep | Row; the doc sentence it supports |
| A computation | A script in the project (`.py.txt`), run with the interpreter in isolated mode; inputs and outputs recorded as rows | Same; data pulled through a connector into files first | Script in project knowledge; results as rows with inputs and script version |
| A rule the person stated | Memory, dated, in their words | — | Memory |
| A question for the person | Decisions doc row | — | Doc |

### Inside Claude: documents

Editable docs give the pattern its text primitives: block ids and content hashes (detect an edit without reading the text), revision numbers (`sinceRev` for deltas, `atRev` for the text as it stood at a decision), exact-text and regex search (confirm before claiming), find-and-replace on the smallest span (the person's comments and formatting survive), guarded whole-block writes (`ifHash` + `ifRev`; a guard mismatch means their edit wins), comment threads sent to Claude (the inbox), dropdown enums for status columns (a closed set that repeats), tabs for bulk, version history and restore (deleted text is never retyped from memory). The sync skill is built from these and nothing else.

### Inside Claude: data

The artifact database gives collections and documents with versioned writes (`if_version`), batch writes (50, atomic where supported), `where`/`order_by`/`limit`/cursor queries, `list` to disk (`out_dir`) so a whole collection never enters context, access rules per path (viewers read, contributors write, a private per-user prefix), live subscriptions for a console page, and `str_replace` inside a string field. Claude reads and writes it as the person through ArtifactData; a published page reads it live through the `db` capability. This is the ledger's home. Project knowledge stays for stable files (a 2 MB cap in the pilot; name files, overwrite in place); memory stays for rules.

### Inside Claude: algorithms

Calculations run in code, never in prose: word counts and page fits, merges of three versions, hash comparisons, identifier extraction, scoring of findings against sentences. The script lives in project knowledge as text, is saved locally and run in isolated mode, and its results are written as rows with the inputs, the script name and version. Subagents do the fan-out (one prep agent builds the brief; one agent per axis searches; one judge decides), each reading one shared brief; the coordinator never loads what an agent can summarize.

### From outside: connectors, MCP, APIs, the person's browser

The v1 connectors chapter stands. v2 adds one rule per source: **a source feeds rows, not prose**. A connector read lands as a registry row or a findings row with `source` naming the connector and the time; a database answers a named query and the answer becomes rows with the query id; a public API result (Crossref, PubMed, arXiv, OpenAlex) becomes findings rows with `verified: primary page`; a paywalled item read in the person's browser updates the row's `verified` to `full text`. The person's edits win over anything a source brings in; a conflict is a Decisions-doc row.

### How the pattern keeps four things cheap

**Data.** Rows, not prose; stable names, not dated copies; one editable doc per thing people edit; deltas (`sinceRev`, `lastSeenSweep`), not whole documents; a collection listed to disk, not into context; events pruned to the newest 300; tasks rows pruned at 60 days.

**Instructions.** Project instructions under 500 words pointing at files loaded just in time; one skill per procedure under 500 lines; a schema document read once per session before the first row write; skills that end their questions in the Decisions doc instead of in chat; the cheapest model that can do the job (a sync and a logging task on a small model; a judge on the top model only when there is something to judge).

**Calculations.** In code, with inputs and outputs as rows; a merge that exits non-zero on conflict instead of guessing; a fit check that flags instead of trimming; an exclusion list built by set membership on identifiers, not by reading titles.

**Retrieval.** Registry first; exact search to confirm; `in` queries over candidate identifiers; a cumulative brief per watched sentence so the judge sees the record, not the week; `atRev` to answer "what did it say then"; closed decisions closed. These are the fixes for the three failures the pilot kept hitting: missing data (four copies and dated names made search return the wrong one), hallucination (a claim with no row, a write with no guard), and recency bias (this week's paper weighed against nothing).

## Capabilities and versioning (write docs/capabilities.md from this)

First line of the file: `As of 21 Oct 2026 · artifact runtime contract 0.2.88 · Claude Code plugin schema as documented at code.claude.com/docs/en/plugins`. Every row below has: capability · what it offers · how the pattern uses it (skill or prompt) · verified how (used in the pilot / documented / unverified).

### Claude Docs (editable docs)
- Block ids and 8-hex content hashes per block; revision numbers; `sinceRev` (changed blocks only), `atRev` (the doc at a revision), `outline`, `search` (exact text or regex, hits with character ranges; search text limit ~1,024 characters). Used by document-sync, decisions-queue. Verified in the pilot.
- Guarded writes (`ifHash` + `ifRev`), find-and-replace as text, whole-block replace as markdown, insert, move, delete, restore to a revision. Used by document-sync, approved-summary. Verified.
- Comments: threads anchored to text; a comment sent to Claude arrives as a turn with thread id and anchor; `answering` ties the edit to the thread. Used by document-sync (comment-as-decision). Verified in the docs guide; the pilot exercised reads and edits, not a comment round trip yet — say so.
- Dropdown enums for status columns; date chips; mention chips; tabs with order and nesting; version history. Used by the Decisions doc and Contact log templates. Verified.

### Artifact database (ArtifactData and the `db` capability)
- Collections and documents; `get`, `list` (cursor, limit 1000, `out_dir` to disk), `query` (`where`, `order_by`, `limit`), `set`, `update` (field delete), `str_replace`, `delete`, `batch` (50 writes, atomic where supported), `if_version` pins; `as_level` to test access rules; a `data/users/<id>` private prefix; `profiles` for display names. Used by project-ledger, document-sync, weekly-sweep, source-check. Verified in the pilot (866-row backfill in 18 batches; where-query and viewer-level reads checked).
- Page side: `claude.use("db")`, `onSnapshot` live reads, rules per path (`view` < `interact` < `admin` < `owner`). Used by templates/console-page.html. Verified (page published in the pilot; rendering not checked from the build session — say so).

### Artifact runtime capabilities (contract 0.2.88)
`artifact` (a page republishes itself; for pages that are the record), `assets` (uploads), `comments` (page UI to the artifact's comment store), `db`, `downloads` (offer a generated file), `files` (read a Claude Code project's files as the viewer), `mcp` (call the viewer's connectors from a page; used in the pilot for a "run sync now" button that fires a scheduled task), `room` (live presence; nothing persists), `sample` (ask Claude from the page; no project memory), `user` (who is viewing). The pattern uses `db` and, optionally, `mcp`; the rest are listed so a reader knows what exists. Documented; only `db` and `mcp` verified in the pilot.

### Scheduled tasks
Create with a cron or a one-shot time; each run starts a fresh session; connectors included per task; `fire_trigger` starts a run on demand (what the console button calls). Used by prompts 01, 03, 07 and the console page. Verified in the pilot.

### Projects (project knowledge, instructions, memory)
Project knowledge: files with stable names, a size cap (2 MB in the pilot), RAG search that returns snippets (not a content recall tool); project instructions pasted by the person; project memory in files with dated lines. Used throughout. Verified.

### Connectors and MCP
As in the v1 chapter (extensions/connectors-and-mcp.md): remote MCP in claude.ai, `.mcp.json` in Claude Code, connectors on scheduled tasks, read-only database servers, security rules. Not re-verified for v2; keep the v1 dates.

### Claude Code plugins and skills
One marketplace file at `.claude-plugin/marketplace.json`; skills as folders with SKILL.md; `claude plugin validate .`. Used by plugin/README.md. Verified in v1.

### Versioning policy
- The repo follows semantic versioning; the plugin `version` in the marketplace entry is the repo version (v1 = 0.2.0; this brief = 0.3.0). CHANGELOG.md records what changed and which Claude capabilities it depends on.
- `docs/capabilities.md` is dated and names the runtime contract. A change in what Claude offers is a row change there first, then a skill or template change, then a version bump.
- Each skill states, in its first paragraph, the schema version it expects (`project-ledger v1`); `meta/ledger.schemaVersion` in a project says what that project runs. A mismatch is a prompt-09 task, not a silent upgrade.
- A project built from this pattern records its own pattern version in its project instructions (`application-organizer v0.3.0`), so a capability check can tell the person what their project is missing.

### The update procedure (prompt 09 and the capability-check skill)
When Claude ships a new surface, model or capability: (1) read what the current surfaces offer — the tool descriptions in a fresh session, the runtime contract version, the docs guide, the connector pages; (2) diff against docs/capabilities.md row by row; (3) write the new or changed rows with "unverified" until one real call has been made; (4) propose, as a numbered list with a default of "no change", what in the repo (skills, templates, prompts) and what in the person's own project (instructions, scheduled tasks, console page, schema) should change; (5) apply only what the person approves; bump versions; add the CHANGELOG entry. Run it on a schedule the person chooses (monthly is the default) and whenever they say a new Claude version is out.

## New lessons (append to docs/lessons.md as 11–15)

11. **Status in prose rots; status in a row with a timestamp does not.** A tracking line in memory said two drafts were sent; a row with `at`, `by` and `source` would have said who claimed it and when.
12. **An exclusion list is a set, not a document.** A prose ledger grew to 40 KB in four weeks and every sweep loaded it whole; 866 rows queried by identifier cost nothing.
13. **A claim without a row is a claim nobody checked.** Provenance is cheap at write time and expensive at submission time. Forward-only is fine; the first week's rows are the ones that matter.
14. **The judge must see the record, not the week.** A new paper weighed against nothing always looks important. A cumulative brief per sentence is the cure, and `atRev` says what the sentence said when the last decision was made.
15. **Write a page's rows, then look at the page.** A console built in the same session as its data layer cannot be rendered from there; say so, and let the first look be the person's.

## Worked examples (write into README "Worked examples", three short flows)

**A sentence gets edited.** The person edits paragraph 3 in the editable doc. The nightly sync opens its tasks row, reads the registry row, probes the doc's revision, sees one changed hash, reads that one block, merges, renders the fit, writes the master copy, the stable file and the register row, searches the doc for the new text word for word, finds the cited paper in the paragraph and updates its claims row, records the snapshot and the event, closes the tasks row. The person sees one Activity line on the console.

**A sweep finds a paper.** Monday's prep agent lists `findings` to disk and builds the exclusion set and a cumulative table for the twelve watched sentences. An axis agent finds a new paper on sentence 7. The judge sees three earlier findings on that sentence, two supporting and one complicating; the new one is a stronger design in the complicating direction, so it is an A item with a Decisions-doc row and a findings row with `direction`, `touches` and `decisionId`. A second paper that repeats what the record holds is a B item with a row and no decision.

**A chat resumes.** A new chat opens the project's newest `tasks` row, sees two docs read at known revisions and one open item, reads each doc with `sinceRev`, gets only the paragraphs that changed, and asks the person nothing that `decisionsAnswered` already holds.

## Prompt 08 — Backfill the record (prompts/08-backfill-the-record.md)

```text
Backfill the structured-memory ledger of this project from the prose records it has today, using the project-ledger skill (github.com/aliomraniH/application-organizer). Write rows, read papers never: this is a transcription pass, and it says so on every row.

1. Ask me, in one message: which prose records exist (a sweep ledger, a register, a contact log, status lines in memory or reports), the tracker artifact's URL (or whether to create one from templates/console-page.html), and whether findings rows should carry a coarse status derived from section labels or none.
2. Write a script that extracts identifiers (DOI, arXiv, PMC, PMID, ACL Anthology, trial registries, preprint servers) with the sweep date and section label of each mention, merges aliases, derives the coarse status if I said yes, and writes one JSON file per row plus batch manifests of 50. Spot-check a random sample of identifiers against the source file by exact search before any write; show me the sample.
3. Write the rows in batches; show me the count and the collection size after each batch set. Set meta/ledger with the backfill record: source, rows, method, "ledger-transcribed", and the note that the source's own count may include repeats.
4. Leave the prose record in place as history; point the sweep skill at the collection as its exclusion list; record the change in the project's change log and the tasks row.
5. End with what is NOT in the rows (titles, dates, verification) and how the next sweep fills them in.
```

## Prompt 09 — Capability check (prompts/09-capability-check.md)

```text
Run a capability check for this project and for the application-organizer repo (github.com/aliomraniH/application-organizer), using the capability-check skill. Propose first; change nothing until I approve a numbered item.

1. Read what the current Claude surfaces offer: the tool descriptions available in this session, the artifact runtime contract version, the docs guide index, the connectors pages named in extensions/connectors-and-mcp.md. Record the date.
2. Diff against docs/capabilities.md row by row: new, changed, removed, and anything there that you cannot verify today. Mark each row verified (one real call), documented, or unverified.
3. Propose, as a numbered list with a default of "no change": (a) repo changes — skills, templates, prompts, the capabilities doc, the version bump; (b) changes to this project — instructions, scheduled tasks, the console page, the ledger schema version. For each, one sentence on what it fixes or enables and one on the risk.
4. After my answers: apply only the approved items, bump versions, add the CHANGELOG entry, update meta/ledger.schemaVersion where the schema changed, and add a Decisions-doc row for anything that still needs me.
5. If I asked for a schedule, create a scheduled task that runs this check monthly on the cheapest model, with no connectors beyond the ones it reads from.
```

## Sources (external URLs the docs may cite, in addition to BRIEF.md Sources)

- code.claude.com/docs/en/plugins — plugin and marketplace schema
- code.claude.com/docs/en/routines — scheduled tasks
- The Claude Docs and artifact-capabilities guidance is delivered inside a session (the docs guide and the runtime type definitions), not on a public page; cite it as "the docs guide and runtime contract 0.2.88 read on 21 Oct 2026" and keep the "verified in the pilot / documented / unverified" cell honest.
