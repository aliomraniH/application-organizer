# Skills

Thirteen skills, one per recurring procedure. Each is short, follows Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and sends its questions to the Decisions doc instead of leaving them in chat.

| Skill | When it triggers | Doc it owns |
| --- | --- | --- |
| [document-sync](document-sync/SKILL.md) | After an accepted edit to a controlled document, on "sync" or "render", or when the sync task fires | The record of each document (`programs`, `snapshots`, sync events in the ledger at `<TRACKER_URL>`) and the rendered views: `register.md`, a target's page |
| [decisions-queue](decisions-queue/SKILL.md) | At the start of any task touching a document, target, research doc or contact; whenever a decision comes up or is answered | The Decisions doc at `<DECISIONS_DOC_URL>` |
| [contact-log](contact-log/SKILL.md) | Before answering about emails, replies or follow-ups; before drafting outreach; when the person says they sent or received something; when they ask what is due | The Contact log at `<CONTACT_LOG_URL>` and its record, the `contacts` rows |
| [weekly-sweep](weekly-sweep/SKILL.md) | When the sweep task fires or the person asks for a sweep | `sweep-<YYYY-MM-DD>.md` reports and the `findings` collection |
| [evidence-tracker](evidence-tracker/SKILL.md) | When the post-sweep task fires or the person dictates a tracker change | The evidence tracker doc and `evidence-tracker.md` |
| [approved-summary](approved-summary/SKILL.md) | When the person says update or approve the summary, dictates a change, or the post-sweep task asks for the weekly proposal | The approved summary doc, `summary.md` and `summary-PROPOSED.md` |
| [project-ledger](project-ledger/SKILL.md) | When a ledger is set up, a chat or run starts or ends work on a document, row or decision, a cited fact or finding needs a row, or the person asks to backfill or prune | The ledger at `<TRACKER_URL>`: `meta`, `tasks` rows, the row shapes of every collection |
| [capability-check](capability-check/SKILL.md) | When the capability-check task fires, the person says a new Claude version is out, or a project's schema version does not match | `docs/capabilities.md` in the repo; `meta/ledger.schemaVersion` in a project (on approval) |
| [final-check](final-check/SKILL.md) | When the person says a document is final, ready or about to be submitted, asks what stands between it and final, asks for the submission file, or says they submitted | `programs/<id>.policy`, each statement's `status`, the `gates` rows, the submission file |
| [requirements](requirements/SKILL.md) | When a target is added, when the person asks what is left or due, when something was requested, sent or received, before a submission, when a phase changes | The `requirements` rows; each target's `phase` |
| [review-loop](review-loop/SKILL.md) | When the person asks to judge, score, compare or improve a document or passage, or a back-and-forth has gone three rounds without a clear gain | The `reviews` rows; the goal in the tasks row |
| [pattern-audit](pattern-audit/SKILL.md) | Monthly, at a phase change, or when the person asks how the project is set up | Nothing; it reports and proposes |
| [source-check](source-check/SKILL.md) | After a source is added or changed, before the first scheduled run that depends on it, when the source-check task fires, or on request | `sources.md` (results and change log) |

## Installing

- **claude.ai**: save each `SKILL.md` as a skill (one folder per skill), then fill the placeholders. The [bootstrap prompt](../prompts/01-bootstrap-project.md) does the filling.
- **Claude Code**: copy the folders into `.claude/skills/` in your project, or install them together as a plugin (see [`plugin/`](../plugin/README.md)).

## Placeholders

Angle-bracketed values are filled per project and never committed back here with real values: `<PROJECT_NAME>`, `<DECISIONS_DOC_URL>`, `<CONTACT_LOG_URL>`, `<TRACKER_URL>`, `<REGISTRY_ROW>`, `<project-files>`.

## Schema version

Every skill that reads or writes the ledger states the schema it expects in its first paragraph: **project-ledger v1** ([docs/structured-memory.md](../docs/structured-memory.md)). A project records the version it runs in `meta/ledger.schemaVersion`; a mismatch is a capability-check task, not a silent upgrade. The gates (`spans`, `gates`, policy rows) are an addition inside v1, recorded as `meta/ledger.gates`; final-check stops and offers prompt 10 when it is missing.

## Keep only what you use

Disable skills that do not belong to the project. Descriptions compete for the same trigger, and a skill that says "always use" over-triggers ([lesson 8](../docs/lessons.md#8-disable-unrelated-skills)).
