---
name: pattern-audit
description: Checks a project against the application-organizer pattern it says it follows - instructions, scheduled tasks, project files, ledger rows, memory, the Decisions doc, views, gates and review loops - and proposes numbered fixes with a default of no change. Use monthly, when a target's phase changes, when the person asks to review or evaluate how the project is set up, or when the weekly review meets the same problem twice.
---

# Pattern audit

Expects schema **project-ledger v1**; the ledger is at <TRACKER_URL>. The script is the project file `ledger_lint.py.txt`. capability-check asks whether the pattern still fits what Claude offers; this skill asks whether the project still follows the pattern. A project drifts from its own rules within weeks, and nobody inside a chat can see it.

The audit changes nothing. A check that could not be run is reported as not checked, never as passed.

## The checks
| # | Read | Passes when |
| --- | --- | --- |
| 1 Instructions | the project instructions | under 500 words; the pattern version is the repo's current one; the skills listed are the skills in use; no status lines |
| 2 Scheduled tasks | each task's prompt, model, connectors and its last three transcripts | the prompt is six lines or fewer and names a skill instead of restating it; the model is the tier `docs/model-and-usage.md` gives; only connectors the task uses are attached; the transcripts show work done, not only a green status; the task is still needed in the current phase |
| 3 Project files | the file list with sizes and dates | at most 40 files and half the knowledge cap; no dated or versioned names except sweep reports; no sweep report older than 8 weeks (its findings are rows); no script copied once per target; no project-file copy of a skill that differs from the saved skill |
| 4 Ledger | every collection, `list · <collection> · out_dir <scratch>`, then `python3 -I ledger_lint.py --ledger <scratch>` | no errors; every warning has an owner |
| 5 Memory | each memory file and its size | under 60 percent of its cap; no status (a send, a version, "currently", "started"); no rule that a later rule replaced; no rule stated twice |
| 6 Decisions doc | its rows and its summary | no Open row older than 30 days without a reason; no Open row about a frozen document; the open count matches the rows; the summary is one short paragraph |
| 7 One source | the registry and each view | no document has two editable places without a declared mirror; each view equals a fresh render; each view is inside its budget |
| 8 Gates | registry rows, `spans`, `gates` | every drafting target has a policy row; every final statement has a gate row with its hash; `spans` is not empty in a project where Claude writes wording |
| 9 Review loops | `reviews` rows and the events of the last 30 days | every loop has a goal and a rubric hash; none ran past the round cap; no document took more than five accepted versions in one day |

## The run
1. Open the tasks row. Read `meta/ledger` and the registry.
2. Run the checks in order. For each, keep the evidence: the number, the file name, the row id.
3. Report in chat as one table: check, result (pass, fail, not checked), evidence.
4. Propose fixes as a numbered list, each with one sentence on what it fixes and one on its risk, default "no change". Group them: do now, do at the next phase change, leave.
5. Apply only what the person approves, through the skill that owns each thing: project-ledger for rows, document-sync for views, the memory digest (prompt 13) for memory. Deleting a file or a scheduled task needs its own yes.
6. `set · events/<id> · {at, kind: "ledger", status: "done", summary: "pattern audit: <n> pass, <n> fail, <n> not checked", by}`. Anything left for the person becomes a Decisions-doc row. Close the tasks row.

## Related skills
capability-check keeps the pattern current with Claude. The weekly review (prompt 06) is the short weekly version of checks 4 and 6. decisions-queue takes what the person must decide.
