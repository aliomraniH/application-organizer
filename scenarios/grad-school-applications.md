# Scenario: graduate-school applications

This is the campaign the pattern came from. Names are invented.

## The story

Sam has six years in industry and is applying to eight clinical-psychology doctoral programs for one fall intake. Each program wants two statements, a statement of purpose and a diversity or personal statement, each with its own page limit and a named mentor. Northfield University caps the statement of purpose at two pages and asks applicants to name up to two faculty; Sam wants to name Dr. Example and Dr. Sample.

Three recommenders need per-program guidance: which of Sam's projects to stress for which program. Faculty outreach runs over four months: an introductory email, a follow-up, sometimes a call. Through all of it, one research theme has to stay consistent across every document while new papers keep arriving, some of them by the faculty Sam is naming.

Before the pattern, Sam had four copies of each statement (a working doc, a published page, a project file, a pasted draft in chat). The register went through 70 versions in 18 days. Memory recorded two drafted emails as sent, and Sam nearly skipped a follow-up because of it. Questions for Sam sat in sweep reports, in tracker notes and at the end of long chats.

## The setup it implies

### Editable docs
- One per program's statements (sixteen statements in eight docs, or one doc per statement; pick one and keep it)
- Decisions doc ([template](../templates/decisions-doc.md))
- Contact log ([template](../templates/contact-log.md)), one section per program
- Evidence tracker, one tab per research theme
- Approved research summary: the statement of direction every statement must agree with
- Recommender guide, one section per recommender per program
- A two-page plain-language brief for recommenders and family

### Project files (stable names)
- `register.md`: every statement's version, word count, page fit, links, deadline, open gates ([template](../templates/register.md))
- One source file per program: limits, prompts, faculty, AI-use policy
- `sweep-axes.md`: the research theme, axes, faculty watch list with ORCIDs ([template](../templates/sweep-axes.md))
- `ledger.md`, `evidence-tracker.md`, `summary.md`, `summary-PROPOSED.md`
- Skill fallbacks: a README for the tracker and one for the summary, giving format rules

### Skills
All six.
- **document-sync** after any statement edit, and nightly as a scheduled task.
- **weekly-sweep** on Monday mornings.
- **evidence-tracker** and **approved-summary** after the sweep, in a second task later the same day.
- **decisions-queue** at the start of every task.
- **contact-log** whenever an email is mentioned.

### Rules recorded in memory (dated, in Sam's words)
- Voice: "first person, plain, no 'passionate'".
- Exact wording of Sam's role in prior work: "I led the analysis; I did not design the trial."
- Facts that must stay fixed: dates, sample sizes, titles.
- Names never to use: a former employer's client.
- Each program's AI-use policy, and whether Sam must attest sole authorship. Where a program requires it, Claude's text is a suggestion Sam rewrites.

### Scheduled tasks
| Task | When | Model tier | Connectors |
| --- | --- | --- | --- |
| Nightly sync | 02:00 | cheapest | none beyond Claude Docs |
| Weekly sweep | Monday 06:00 | mid-tier, top only for judging A items | none; public APIs |
| Post-sweep update | Monday 14:00 | cheapest | none |

## The record

The ledger lives in the tracker artifact; Sam sees it on the console page. All seven collections are used.

| Collection | Rows at the end of week one |
| --- | --- |
| `programs` | 8, one per program, each with its two statements (`northfield`, ...) |
| `snapshots` | 16, one per statement, written by the first nightly sync |
| `events` | about 40: syncs carried, one conflict, two flags for cited facts without a claims row |
| `tasks` | 12: the setup chat, 7 nightly syncs, the Monday sweep, the post-sweep update, 2 working chats |
| `claims` | 5, forward-only: the cited sentences Sam edited this week, each verified at a primary page |
| `findings` | 866 backfilled from the old prose ledger (`ledger-transcribed`, prompt 08), plus 31 from Monday's sweep |
| `meta` | `config` (sync trigger, lock, last run) and `ledger` (project-ledger v1, counts, the backfill record) |

The first rows written, in order:

    set   · meta/ledger · {schemaVersion: "project-ledger v1", schemaDoc: "ledger-schema.md", collections, counts}
    set   · programs/northfield · {name: "Northfield University", order: 1, statements: [{key: "sop", ...}, {key: "personal", ...}]}
    set   · tasks/2026-10-21-setup · {task: "bootstrap", status: "in_progress", by: "the setup chat"}
    batch · findings/<doc id> × 866 · {verified: "ledger-transcribed"}     (18 batches of 50 or fewer)

## A week in the pattern

Monday's sweep finds a new paper by Dr. Example that complicates a sentence in the Northfield statement. The sweep adds row D-41 to the Decisions doc: "Northfield SOP v1.4, paragraph 3 cites the 2024 finding; a 2026 paper by Dr. Example narrows it to adolescents. Options: (a) add the qualifier, (b) cite both, (c) leave it. Default: leave it." On Tuesday Sam opens a chat to work on Northfield; decisions-queue asks D-41. Sam answers "a", edits the sentence in the doc, and document-sync carries it: published page, `program-files/northfield.md`, one register row, one change-log line. D-41 moves to Closed. Nobody asks again.

## Start here
Run [prompt 01](../prompts/01-bootstrap-project.md), or [prompt 02](../prompts/02-migrate-existing-project.md) if you already have a project full of dated copies.
