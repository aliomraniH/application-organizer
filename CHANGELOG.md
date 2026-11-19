# Changelog

All notable changes to this repository. The format follows Keep a Changelog 1.1.0, and the repository follows semantic versioning. The plugin `version` in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) is the repository version.

Each entry names the Claude capabilities it depends on, as listed in [docs/capabilities.md](docs/capabilities.md).

## [0.4.0] - 2026-11-18

What four weeks of finishing and submitting taught: one source with rendered views, gates before "final", phases and requirements, a bounded review loop, and an audit of the project against the pattern. The ledger schema stays **project-ledger v1**: every addition leaves existing rows valid. The gates are named **gates 1** and recorded in `meta/ledger.gates`.

### Changed, and worth reading first
- **document-sync is rewritten around one source.** The editable doc is the only place text is edited; the ledger records it (snapshot, registry row, event); the register and a target's page are views rendered by `templates/render_views.py` and never edited. The four-place sync of 0.2.0 and 0.3.0, which contradicted lesson 1, is gone. A version costs three row writes; views render once per run. A second editable copy must be declared as a mirror. See [docs/views.md](docs/views.md), which includes how to move a 0.3.0 project.
- `templates/register.md` is now the script's output for the synthetic fixtures, and a test keeps it so.

### Added
- **Views.** `docs/views.md`; `templates/render_views.py` (`register`, `page`), with a size budget per view that refuses instead of truncating.
- **Lifecycle.** `docs/lifecycle.md`; `programs/<id>.phase` (`drafting`, `submitted`, `after`, `closed`); sync does not read a frozen document and proposes pausing its own task when nothing is being drafted; the sweep files findings against frozen text as preparation and raises no decision; decisions-queue offers once to close moot rows; prompt 11, Phase change.
- **Requirements.** Skill `requirements` and collection `requirements`: one row per thing a target needs, quoted from the target's page, with owner, due date, lead time and start-by; "submitted is not complete".
- **Contacts.** Collection `contacts`: the record of each Contact log row, with `role` and `nextDue`, never an address. The doc stays the source.
- **Review loop.** `docs/review-loop.md`; skill `review-loop`; `templates/review_verdict.py` (noise band from an A/A calibration, order-effect check, round cap); collection `reviews`.
- **Pattern audit.** Skill `pattern-audit` (nine checks with evidence); `templates/ledger_lint.py` (row shapes, stale counts, rows left open, phases, requirements past their start-by, addresses in rows); prompt 12, Pattern audit; prompt 13, Memory digest.
- The weekly sweep reports coverage per source and calls a week with a refused source PARTIAL COVERAGE.
- Lessons 21 to 28; lesson 1 amended.
- `tests/scripts.test.py` and `tests/fixtures/campaign/`: 25 tests over a synthetic two-target ledger.
- Templates `requirement-row.json`, `contact-row.json`, `review-row.json`; `sweep-axes.md` gains axes for after submission.
- Plugin: thirteen skills.

### Gates (the first part of this version)
- `docs/gates.md`: why a check at the end is not enough, policy modes, spans, claims bound to their words, the detector, waivers, final bound to a hash.
- Skill `final-check`: reads the policy, runs the check, records waivers and the person's answer to the authorship question, sets final, builds the submission file, records submitted on the person's word. Never runs from a scheduled task.
- `templates/final_check.py`: the check as a script, standard library only. `check` (with `--preview`) lists open items; `status` says whether a text is still the text that passed.
- Ledger, inside v1: `programs/<id>.policy` (mode `open`, `own-words`, `feedback-only`, `unknown`) and `.deadline`; per statement `status`, `gateOpen`, `final`, `submitted`; `claims.span`, `.kind`, `.recheckBy` and the statuses `contradicted` and `retired`; collections `spans` and `gates`; event kinds `gate` and `status`.
- Prompt 10, Final check: turns the gates on in an existing project and runs the first check.
- Templates `gate-row.json` and `span-row.json`; `claims-row.json` gains `span` and `kind`.
- Lessons 16 to 20.
- `tests/final_check.test.py` and `tests/fixtures/gates/`: 22 tests over synthetic rows, each named for the failure it stops.
- README worked example: a document becomes final.

### Changed
- document-sync: writes within the target's policy mode (rule 7), records spans (rule 8), never sets final or submitted (rule 9); finds a claims row by its span, not by block and revision; runs the preview on every pass, writes `gateOpen`, returns an edited final document to draft, and adds one Decisions-doc row when open items meet a deadline seven days out.
- project-ledger: claims rows carry `span` and `kind`; a span row is written whenever Claude writes or proposes wording.
- Prompt 01 creates the check script, the deadline and the policy row per target; prompt 06 reports each statement's status and open gate items.
- The claims flag still never blocks a sync. It now blocks final.

### Not in this version
- The console page does not yet show policy modes, statuses, phases, requirements or open gate items; the rendered register and the weekly review carry them.
- Variants (one shared body, per-target differences, a build that joins them) are a stated rule and an audit check; no builder ships.
- Nothing here schedules a reminder from `contacts.nextDue`; the weekly review lists what is due.
- Wording Claude wrote before a project turned the gates on is not in `spans`. For that period the record cannot speak, and prompt 10 says so to the person.

### Depends on
- Nothing new. The four scripts run wherever Python 3 runs; the rows use the same ArtifactData calls as 0.3.0.

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
- `tests/`: synthetic ledger fixtures (every row marked `synthetic`) and an offline Chromium check of the console page. The template was also published as a private demo over those rows: viewer reads, refused writes and the "Run sync now" button (through `mcp` and `fire_trigger`) were each exercised once.

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
