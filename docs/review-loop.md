# The review loop

Having a model judge a draft is cheap, fast and persuasive. It is also noisy, and the noise looks like signal. This page describes the loop the pattern uses to compare a document's current text with a candidate change, and the rules that keep the loop from running the project.

Added in 0.4.0. Skill: [review-loop](../skills/review-loop/SKILL.md). Script: [`templates/review_verdict.py`](../templates/review_verdict.py).

## What goes wrong without rules

- **Margins inside the noise get acted on.** A round is decided by two or three points on a scale of well over a hundred, when the same text read by another reader moves by ten.
- **Order decides a round.** Each reader prefers whichever text it read second. Without opposite orders and a check, that reads as a split, or as a win.
- **The loop has no end.** Each round suggests one more fix, each fix earns one more round, and a document changes many times in a day with every change carried to the record.
- **Scores pull the text.** A rubric rewards something specific, and candidate by candidate the document drifts toward a claim, a plan or a commitment the person never chose. Each step is a reasonable response to a score.
- **Two judges disagree about level and nobody can say who is right.** One reader scores everything higher than another. Neither is tied to how the real reader decides.

## The loop

1. **The goal, in the person's words.** What this pass is for, what must not change, what done looks like. It is written into the tasks row before any text is judged, and every candidate is checked against it first.
2. **A rubric fixed before reading.** Built from the target's own pages and the goal, saved and hashed. A changed rubric is a new loop.
3. **Calibration.** Once per rubric, each reader scores the same text twice, presented as two documents. The difference is pure noise.
4. **A round.** Two readers with no history of the thread, two unlabelled texts, opposite orders. Each returns scores, a total and the three sentences that cost the most.
5. **The verdict, by script.**
   - The **band** is the larger of 3 percent of the scale and the largest calibration difference. A difference inside it is a tie.
   - If each reader preferred the text it read second (or each the first), that is an **order effect** and a tie.
   - A candidate **wins** only when every reader prefers it by more than the band.
6. **A tie keeps the current text.** The person's text has standing; a candidate has to earn its place.
7. **Three rounds at most.** Two rounds in a row without a win also end the loop. Then: report, and offer a fresh reader who sees the goal and the text and none of the scores.
8. **One change, once.** A winning candidate is offered to the person. On their yes it becomes one edit, one version and one sync.

## What a score is

A score here is a comparison between two versions, for two readers, under one rubric. It supports "these readers preferred B to A by more than their own noise". It does not support "B is a strong document", "B is ready" or any statement about what the real reader will do. The skill says so each time it reports, and never turns a score into a chance of success.

Two readers from the same model family agree with each other more than either agrees with the world. An outside reader adds a different bias, not a ground truth. If two readers differ steadily in level, compare each reader's own preference between the two texts and ignore the levels.

## Scores are leads

The most useful thing a reader returns is the list of sentences that cost the most, because two independent readers naming the same sentence is hard to get by chance. The least useful is the total.

A criterion can be satisfied by adding something that is not true, not decided or not the person's: a method, a number, a commitment. The loop never does that. Where the goal and a criterion pull apart, the goal wins and the report names the criterion that was left unmet.

## With the gates

The policy mode of the target holds inside a loop ([gates.md](gates.md#the-mode-decides-what-claude-may-do)). Under `open`, candidates may be Claude's. Under `own-words`, a candidate from Claude is a suggestion the person rewrites, recorded as a span. Under `feedback-only` there are no candidates from Claude at all: the readers comment on the person's text and the person decides what to do with the comments.

A review never makes a document final. Only the final check does.

## The record

    reviews/<program>-<key>-<nn> ·
      { program, key, goal, rubricHash, scale, band,
        rounds: [ { label, diffs, verdict, orderEffect } ],
        outcome: "accepted" | "kept" | "stopped", acceptedBy?, at, task }

One row per loop. The [pattern audit](../skills/pattern-audit/SKILL.md) reads these rows for loops without a goal, loops past the cap, and documents that took more than five accepted versions in a day.
