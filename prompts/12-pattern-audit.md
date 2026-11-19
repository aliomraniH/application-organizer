Audit this project against the application-organizer pattern (github.com/aliomraniH/application-organizer), using the pattern-audit skill. Change nothing. Report first, then propose.

1. Run the nine checks in the skill, in order: instructions, scheduled tasks, project files, ledger (list every collection to disk and run ledger_lint.py), memory, Decisions doc, one source and views, gates, review loops. For each check keep the evidence: a number, a file name, a row id.
2. Report as one table: check, result (pass, fail, not checked), evidence. A check you could not run is "not checked", never "pass". Say which tool or permission was missing.
3. Then tell me, in three short paragraphs: what this project is spending the most on that no longer earns it; what rule it has drifted furthest from; and what is most likely to go wrong next if nothing changes.
4. Propose fixes as a numbered list with a default of "no change", each with one sentence on what it fixes and one on its risk, grouped: do now, do at the next phase change, leave.
5. After my answers: apply only the approved items through the skills that own them. Deleting a file or changing a scheduled task needs its own yes. Record one ledger event with the counts, add a Decisions-doc row for anything left for me, and close the tasks row.
6. If I ask for a schedule, create a monthly task that runs steps 1 to 4 on the cheapest model with no connectors beyond the ones it reads from, and messages me only when a check fails.

You will create nothing until I answer; then only what I approve, one ledger event, and Decisions-doc rows for what remains.
