# Changelog

All notable changes to this repository. The format follows Keep a Changelog 1.1.0, and the repository follows semantic versioning. The plugin `version` in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) is the repository version.

Each entry names the Claude capabilities it depends on, as listed in [docs/capabilities.md](docs/capabilities.md).

## [0.3.0] - 2026-10-21

Built from [BRIEF-v2.md](BRIEF-v2.md): structured memory.

### Added
- A seventh layer, **structured memory**: the ledger collections `programs`, `snapshots`, `events`, `tasks`, `claims`, `findings` and `meta` in the tracker artifact's database ([docs/structured-memory.md](docs/structured-memory.md)).
- Three retrieval rules: registry first; no claim without a row; new is not important. Comments sent to Claude as decisions made in place.
- `docs/structured-memory.md`, `docs/working-with-data.md`, `docs/capabilities.md` (dated, with the runtime contract version and a "used by" cell per capability).
- Skills: `project-ledger` (schema steward) and `capability-check` (diffs what Claude offers against `docs/capabilities.md`).
- Prompts: 08 Backfill the record, 09 Capability check.
- Templates: `ledger-schema.md`, `console-page.html` (registry, working memory, evidence record, record rules; declares `db`, optional `mcp`), `tasks-row.json`, `claims-row.json`.
- Lessons 11 to 15; context-budget rules for deltas, `out_dir` and `in` queries.
- README "Worked examples": a sentence gets edited, a sweep finds a paper, a chat resumes.
- A "The record" section in each scenario.
- A second privacy check: no artifact links in Markdown.
- `tests/`: synthetic ledger fixtures (every row marked `synthetic`) and an offline Chromium check of the console page.

### Changed
- document-sync, decisions-queue, weekly-sweep, approved-summary, evidence-tracker and source-check read and write ledger rows (tasks rows, claims checks, findings as the exclusion list, the cumulative brief, the ledger probe).
- Prompts 01, 02, 03 and 06 create, backfill, query or review the ledger.
- `docs/architecture.md`: seven layers, three tiers of memory, the change flow with the ledger stations.
- Plugin: nine skills.

### Depends on
- Claude Docs: block hashes, revisions, `sinceRev`, `atRev`, search, guarded writes, comments sent to Claude (the comment round trip is documented, not yet exercised).
- Artifact database through ArtifactData; the `db` runtime capability, contract 0.2.88; optionally `mcp` and scheduled tasks' `fire_trigger`.

## [0.2.0] - 2026-10-21

Built from [BRIEF.md](BRIEF.md), the v1 pattern.

### Added
- Six layers: project instructions, project knowledge with stable names, editable docs, memory for dated rules, skills, scheduled tasks. Three authority rules.
- Skills: document-sync, decisions-queue, contact-log, weekly-sweep, evidence-tracker, approved-summary, and source-check (the test layer for connectors and MCP).
- Prompts 01 to 07, three scenarios, five templates plus `sources.md`, the connectors and MCP chapter with `.mcp.json` examples, ten lessons.
- The plugin, installable from `.claude-plugin/marketplace.json`.
- The at-sign privacy check.

### Depends on
- Claude Projects, Claude Docs, skills, scheduled tasks, connectors and MCP, Claude Code plugins.
