# Skills

Six skills, one per recurring procedure. Each is short, follows Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and sends its questions to the Decisions doc instead of leaving them in chat.

| Skill | When it triggers | Doc it owns |
| --- | --- | --- |
| [document-sync](document-sync/SKILL.md) | After any edit to a controlled document, on "sync" or "propagate", or when the sync task fires | The published copies, the stable project files, `register.md` and the tracker at `<TRACKER_URL>` |
| [decisions-queue](decisions-queue/SKILL.md) | At the start of any task touching a document, target, research doc or contact; whenever a decision comes up or is answered | The Decisions doc at `<DECISIONS_DOC_URL>` |
| [contact-log](contact-log/SKILL.md) | Before answering about emails, replies or follow-ups; before drafting outreach; when the person says they sent or received something | The Contact log at `<CONTACT_LOG_URL>` |
| [weekly-sweep](weekly-sweep/SKILL.md) | When the sweep task fires or the person asks for a sweep | `sweep-<YYYY-MM-DD>.md` reports and `ledger.md` |
| [evidence-tracker](evidence-tracker/SKILL.md) | When the post-sweep task fires or the person dictates a tracker change | The evidence tracker doc and `evidence-tracker.md` |
| [approved-summary](approved-summary/SKILL.md) | When the person says update or approve the summary, dictates a change, or the post-sweep task asks for the weekly proposal | The approved summary doc, `summary.md` and `summary-PROPOSED.md` |

## Installing

- **claude.ai**: save each `SKILL.md` as a skill (one folder per skill), then fill the placeholders. The [bootstrap prompt](../prompts/01-bootstrap-project.md) does the filling.
- **Claude Code**: copy the folders into `.claude/skills/` in your project, or install them together as a plugin (see [`plugin/`](../plugin/README.md)).

## Placeholders

Angle-bracketed values are filled per project and never committed back here with real values: `<PROJECT_NAME>`, `<DECISIONS_DOC_URL>`, `<CONTACT_LOG_URL>`, `<TRACKER_URL>`, `<project-files>`.

## Keep only what you use

Disable skills that do not belong to the project. Descriptions compete for the same trigger, and a skill that says "always use" over-triggers ([lesson 8](../docs/lessons.md#8-disable-unrelated-skills)).
