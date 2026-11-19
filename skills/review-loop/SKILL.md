---
name: review-loop
description: Runs a bounded, judged comparison between a controlled document's current text and one candidate change - the person's goal written down first, a rubric fixed before reading, two independent readers in opposite orders, a noise band, an order-effect check and a round cap - and records the result. Use when the person asks to judge, score, compare or improve a document or a passage, asks which of two versions is better, or when a back-and-forth on one passage has gone three rounds without a clear gain.
---

# Review loop

Expects schema **project-ledger v1**; the ledger is at <TRACKER_URL>. The script is the project file `review_verdict.py.txt`. Design: `docs/review-loop.md` in the application-organizer repo.

Scores compare two versions for two readers. They do not say a document is good, and they do not predict what its real reader will decide. Never report a score as a chance of success.

## Rules
1. **Goal first, in the person's words**: what this pass is for, what must not change, what done looks like. `update · tasks/<id> · {goal}`. Check every candidate against it before judging; a candidate that breaks a constraint is not judged.
2. **The rubric is fixed before any reader sees a text.** Build it from the target's own pages and the goal. Save its text and hash. It does not change inside a loop; a new rubric is a new loop, and scores from different rubrics are never compared.
3. **Two readers, independent.** Each gets the rubric and two unlabelled texts, in opposite orders. No thread history, no version numbers, no hint which is current. Each returns a score per criterion, a total, and the three sentences that cost the most.
4. **Calibrate once per rubric.** Give each reader the same text twice as two documents. The difference is noise, and it sets the band.
5. **The script reads the scores.** `python3 -I review_verdict.py rounds.json`. Never call a win from the table by eye.
6. **A tie keeps the current text.** So does a loss, and so does an order effect.
7. **Three rounds at most.** When the script says stop, stop and report. Offer a fresh reader who gets the goal, the constraints and the text, never the scores or the earlier candidates.
8. **Scores are leads, not instructions.** Never add a fact, a method, a name or a commitment to raise a criterion. A reader's fix is a proposal to the person. Where a criterion and the goal pull apart, the goal wins and the report says so.
9. **A candidate is not a version.** Nothing reaches the editable doc until the person says yes. Then: one edit, one version, one sync, at the end of the loop.
10. **The policy mode holds** (`programs/<REGISTRY_ROW>.policy.mode`). `open`: candidates may be Claude's. `own-words`: Claude's candidates are suggestions the person rewrites, and each is recorded as a span. `feedback-only`: judge only texts the person wrote; return the readers' comments, no candidate wording.
11. **An outside reader** (another model family, a person) is used only when the person asks, and asked for each time.

## The run
1. Open the tasks row. Registry first: the statement's row and its policy mode. Write the goal (rule 1) and read it back to the person once.
2. Write the rubric; show it; fix it on their yes. Record its hash.
3. Calibrate if this rubric has no calibration on record.
4. One round: both readers, opposite orders. Write the scores to `rounds.json` as the script expects and run it.
5. Tell the person the verdict in one line, then the readers' costliest sentences. On `candidate`: offer it. On a tie or a loss: the current text stands; say what the readers agreed on, and ask whether to try one more candidate.
6. Repeat from 4 only while the script says continue.
7. On the person's yes to a candidate: apply it within the mode, then hand to document-sync once.
8. Record: `set · reviews/<program>-<key>-<nn> · {program, key, goal, rubricHash, scale, band, rounds: [{label, diffs, verdict, orderEffect}], outcome: "accepted" | "kept" | "stopped", acceptedBy?, at, task}`. Keep the tasks row short; the readers' full reports go in an event or a scratch file, not the row.

## When a thread has drifted
If the person restates their direction, or the same sentences keep being flagged: stop the loop, re-read the goal with them, and say where the candidates left it. Then rule 7's fresh reader, not another round.

## Related skills
document-sync records the accepted change. final-check decides final; a review never does. decisions-queue takes any choice the readers raise that only the person can make. project-ledger defines the `reviews` row.
