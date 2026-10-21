As of 21 Oct 2026 · artifact runtime contract 0.2.88 · Claude Code plugin schema as documented at code.claude.com/docs/en/plugins

# Capabilities

What the current Claude surfaces offer that this pattern uses, how the pattern uses each, and how each was verified. Every capability fact in this repo comes from this page. When Claude ships something new, this page changes first ([update procedure](#the-update-procedure)).

The Claude Docs and artifact-capabilities guidance is delivered inside a session (the docs guide and the runtime type definitions), not on a public page. It is cited here as "the docs guide and runtime contract 0.2.88 read on 21 Oct 2026".

**Verified how** takes one of three values: *used in the pilot* (a real call was made in the campaign this pattern came from), *documented* (read in the docs guide, the runtime contract or a public page; no call made), or *unverified*.

## Claude Docs (editable docs)

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| Block structure and deltas | Block ids and 8-hex content hashes per block; revision numbers; `sinceRev` (changed blocks only); `atRev` (the doc at a revision); `outline`; `search` (exact text or regex, hits with character ranges; search text limit about 1,024 characters) | document-sync, decisions-queue | used in the pilot |
| Writes | Guarded writes (`ifHash` + `ifRev`); find-and-replace as text; whole-block replace as markdown; insert, move, delete; restore to a revision | document-sync, approved-summary | used in the pilot |
| Comments | Threads anchored to text; a comment sent to Claude arrives as a turn with thread id and anchor; `answering` ties the edit to the thread | document-sync (comment-as-decision), decisions-queue | documented in the docs guide; the pilot exercised reads and edits, not a comment round trip yet |
| Structure | Dropdown enums for status columns; date chips; mention chips; tabs with order and nesting; version history | Decisions doc and Contact log templates | used in the pilot |

## Artifact database (ArtifactData and the `db` capability)

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| Store and queries | Collections and documents; `get`, `list` (cursor, limit 1000, `out_dir` to disk), `query` (`where`, `order_by`, `limit`), `set`, `update` (field delete), `str_replace`, `delete`, `batch` (50 writes, atomic where supported), `if_version` pins; `as_level` to test access rules; a `data/users/<id>` private prefix; `profiles` for display names | project-ledger, document-sync, weekly-sweep, source-check | used in the pilot (866-row backfill in 18 batches; where-query and viewer-level reads checked) |
| Page side | `claude.use("db")`, `onSnapshot` live reads, rules per path (`view` < `interact` < `admin` < `owner`) | [templates/console-page.html](../templates/console-page.html) | used in the pilot (page published); rendering not checked from the build session |

## Artifact runtime capabilities (contract 0.2.88)

The pattern uses `db` and, optionally, `mcp`. The rest are listed so a reader knows what exists.

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| `db` | The artifact database, read and written by the page | console-page.html | used in the pilot |
| `mcp` | Call the viewer's connectors from a page | console-page.html (optional "run sync now" button that fires a scheduled task) | used in the pilot |
| `artifact` | A page republishes itself; for pages that are the record | not yet | documented |
| `assets` | Uploads | not yet | documented |
| `comments` | Page UI to the artifact's comment store | not yet | documented |
| `downloads` | Offer a generated file | not yet | documented |
| `files` | Read a Claude Code project's files as the viewer | not yet | documented |
| `room` | Live presence; nothing persists | not yet | documented |
| `sample` | Ask Claude from the page; no project memory | not yet | documented |
| `user` | Who is viewing | not yet | documented |

## Scheduled tasks

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| Scheduled tasks | Create with a cron or a one-shot time; each run starts a fresh session; connectors included per task; `fire_trigger` starts a run on demand (what the console button calls) | prompts 01, 03, 07; console-page.html | used in the pilot |

Public page: [scheduled tasks](https://code.claude.com/docs/en/routines).

## Projects

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| Project knowledge | Files with stable names; a size cap (2 MB in the pilot); RAG search that returns snippets (not a content recall tool) | every skill; prompts 01, 02 | used in the pilot |
| Project instructions | Pasted by the person | prompt 01 | used in the pilot |
| Project memory | Files with dated lines | prompt 01; decisions-queue | used in the pilot |

## Connectors and MCP

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| Connectors and MCP | As in the v1 chapter ([connectors-and-mcp.md](../extensions/connectors-and-mcp.md)): remote MCP in claude.ai, `.mcp.json` in Claude Code, connectors on scheduled tasks, read-only database servers, security rules | prompts 04, 05, 07; source-check | documented; not re-verified for v2 (facts as of the v1 dates in that chapter) |

## Claude Code plugins and skills

| Capability | What it offers | Used by | Verified how |
| --- | --- | --- | --- |
| Plugins | One marketplace file at `.claude-plugin/marketplace.json`; skills as folders with SKILL.md; `claude plugin validate .` | [plugin/README.md](../plugin/README.md) | verified in v1 (validator passed; local install delivered the skills) |

Public page: [Claude Code plugins](https://code.claude.com/docs/en/plugins).

## Versioning policy

- The repo follows semantic versioning. The plugin `version` in the marketplace entry is the repo version (v1 = 0.2.0; v2 = 0.3.0). [CHANGELOG.md](../CHANGELOG.md) records what changed and which Claude capabilities it depends on.
- This page is dated and names the runtime contract. A change in what Claude offers is a row change here first, then a skill or template change, then a version bump.
- Each skill states, in its first paragraph, the schema version it expects (`project-ledger v1`). `meta/ledger.schemaVersion` in a project says what that project runs. A mismatch is a [prompt 09](../prompts/09-capability-check.md) task, not a silent upgrade.
- A project built from this pattern records its own pattern version in its project instructions (`application-organizer v0.3.0`), so a capability check can tell the person what their project is missing.

## The update procedure

Run by [prompt 09](../prompts/09-capability-check.md) and the [capability-check skill](../skills/capability-check/SKILL.md), on a schedule the person chooses (monthly is the default) and whenever they say a new Claude version is out.

1. Read what the current surfaces offer: the tool descriptions in a fresh session, the runtime contract version, the docs guide, the connector pages.
2. Diff against this page, row by row.
3. Write the new or changed rows with "unverified" until one real call has been made.
4. Propose, as a numbered list with a default of "no change", what in the repo (skills, templates, prompts) and what in the person's own project (instructions, scheduled tasks, console page, schema) should change.
5. Apply only what the person approves; bump versions; add the CHANGELOG entry.
