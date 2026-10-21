# Working with documents, data and algorithms

A campaign handles four kinds of material: text people edit, records, facts with sources, and calculations. Each has one home. This page says where each goes, what Claude offers for it, how outside sources join, and how the pattern keeps data, instructions, calculations and retrieval cheap.

What each Claude feature offers, and how it was verified, is in [capabilities.md](capabilities.md).

## Where each kind of thing goes

| Kind | Inside Claude | From outside | Store |
| --- | --- | --- | --- |
| A document a person edits | Editable doc (version history, comments, block ids, hashes, revisions) | A Drive, SharePoint or Notion file read through its connector; the editable doc is the working copy | Doc + one registry row + one stable project file |
| A record or a table of records | Rows in the ledger | A database through a read-only MCP server, named parameterized queries only | Rows; the query text in a project file |
| A fact with a source | A claims row linked to a findings row | A primary page read in the person's browser or by the sweep | Row; the doc sentence it supports |
| A computation | A script in the project (`.py.txt`), run with the interpreter in isolated mode; inputs and outputs recorded as rows | Same; data pulled through a connector into files first | Script in project knowledge; results as rows with inputs and script version |
| A rule the person stated | Memory, dated, in their words | — | Memory |
| A question for the person | Decisions doc row | — | Doc |

## Inside Claude: documents

Editable docs give the pattern its text primitives:

- **Block ids and content hashes.** Detect an edit without reading the text.
- **Revision numbers.** `sinceRev` returns only what changed; `atRev` returns the text as it stood at a decision.
- **Exact-text and regex search.** Confirm a sentence is there before claiming it is.
- **Find-and-replace on the smallest span.** The person's comments and formatting survive.
- **Guarded whole-block writes** (`ifHash` + `ifRev`). A guard mismatch means the person's edit wins.
- **Comment threads sent to Claude.** The inbox: a comment is a decision made in place.
- **Dropdown enums.** A closed set for status columns that repeat.
- **Tabs** for bulk; **version history and restore**, so deleted text is never retyped from memory.

The [document-sync skill](../skills/document-sync/SKILL.md) is built from these and nothing else.

## Inside Claude: data

The artifact database gives:

- collections and documents with versioned writes (`if_version`)
- batch writes (50, atomic where supported)
- `where`, `order_by`, `limit` and cursor queries
- `list` to disk (`out_dir`), so a whole collection never enters context
- access rules per path (viewers read, contributors write, a private per-user prefix)
- live subscriptions for a console page
- `str_replace` inside a string field

Claude reads and writes it as the person through ArtifactData; a published page reads it live through the `db` capability. This is the ledger's home ([structured-memory.md](structured-memory.md)).

Project knowledge stays for stable files (a 2 MB cap in the pilot; name files, overwrite in place). Memory stays for rules.

## Inside Claude: algorithms

Calculations run in code, never in prose: word counts and page fits, merges of three versions, hash comparisons, identifier extraction, scoring of findings against sentences.

1. The script lives in project knowledge as text (`merge.py.txt`).
2. It is saved locally and run in isolated mode.
3. Its results are written as rows with the inputs, the script name and its version.

Subagents do the fan-out: one prep agent builds the brief, one agent per axis searches, one judge decides. Each reads one shared brief. The coordinator never loads what an agent can summarize.

## From outside: connectors, MCP, APIs, the person's browser

The v1 [connectors chapter](../extensions/connectors-and-mcp.md) stands. v2 adds one rule per source: **a source feeds rows, not prose.**

| Source | Lands as |
| --- | --- |
| A connector read | a registry row or findings row, with `source` naming the connector and the time |
| A database | the answer to a named query, as rows carrying the query id |
| A public API (Crossref, PubMed, arXiv, OpenAlex) | findings rows with `verified: "primary page"` |
| A paywalled item read in the person's browser | the row's `verified` updated to `"full text"` |

The person's edits win over anything a source brings in. A conflict is a Decisions-doc row.

## How the pattern keeps four things cheap

**Data.** Rows, not prose. Stable names, not dated copies. One editable doc per thing people edit. Deltas (`sinceRev`, `lastSeenSweep`), not whole documents. A collection listed to disk, not into context. Events pruned to the newest 300; tasks rows pruned at 60 days.

**Instructions.** Project instructions under 500 words, pointing at files loaded just in time. One skill per procedure, under 500 lines. A schema document read once per session, before the first row write. Skills that end their questions in the Decisions doc instead of in chat. The cheapest model that can do the job: a sync and a logging task on a small model; a judge on the top model only when there is something to judge.

**Calculations.** In code, with inputs and outputs as rows. A merge that exits non-zero on conflict instead of guessing. A fit check that flags instead of trimming. An exclusion list built by set membership on identifiers, not by reading titles.

**Retrieval.** Registry first. Exact search to confirm. `in` queries over candidate identifiers. A cumulative brief per watched sentence, so the judge sees the record, not the week. `atRev` to answer "what did it say then". Closed decisions stay closed.

These are the fixes for the three failures the pilot kept hitting:

| Failure | What it looked like | The fix |
| --- | --- | --- |
| Missing data | four copies and dated names made search return the wrong one | stable names; registry first |
| Hallucination | a claim with no row; a write with no guard | claims rows; guarded writes from a real read |
| Recency bias | this week's paper weighed against nothing | the cumulative brief; new is not important |
