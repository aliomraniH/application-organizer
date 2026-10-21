---
title: Sources (stable)
version: 1.0
description: One row per connector, MCP server, API or database the project reads. Read and updated in place by the source-check skill. Edit this file, not the skill, when a source, its scope or its probes change.
---

# Sources

- Decisions doc: <DECISIONS_DOC_URL>
- Last check: <date>

## Sources and what they may do

| Source | Kind | Configured in | Access | Scope | Secret variables | Used by tasks |
| --- | --- | --- | --- | --- | --- | --- |
| Google Drive | connector | claude.ai | read | folder "Northfield handbook" | none (OAuth) | nightly sync |
| Reporting database | MCP server, read-only role | Claude Code `.mcp.json` | read | schema `reporting`, views only | `PG_READONLY_URL` | weekly sweep |
| Crossref | public API | none | read | works by ORCID on the watch list | none | weekly sweep |

## Probes

| Source | Read probe | Expected shape | Out-of-scope probe | Write-refusal probe |
| --- | --- | --- | --- | --- |
| Google Drive | search "protocol handbook" in the scoped folder | 1 to 5 files, each with title and modified date | search the same term outside the folder | none; confirm write tools are Blocked |
| Reporting database | run `weekly_enrolment_by_site` from `queries.md` with last week's dates | 5 to 40 rows; columns site, week, enrolled | `select 1 from hr.staff limit 1` | `create table reporting.source_check_probe (id int)` inside a transaction, rolled back |
| Crossref | query.author for one watch-list name, from last week | 0 to 50 items, each with DOI and created date | none | none |

## Results (overwritten on each check)

| Source | Last checked | Reachable | Shape | Scope | Tools | Write refusal | Secrets | Task hygiene | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Google Drive | <date> | Pass | Pass | Pass | Unverified | n/a | Pass | Pass | write tool present; person to confirm Blocked |

## Change log (newest first)

| Date | Change |
| --- | --- |
| <date> | Check: 3 rows; 17 Pass, 0 Fail, 1 Unverified |
