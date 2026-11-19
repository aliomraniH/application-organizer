#!/usr/bin/env python3
"""review_verdict.py: decide what a round of judged reads actually showed.

Part of the application-organizer pattern (0.4.0). Standard library only.
Copy into project knowledge as review_verdict.py.txt and run it in isolated
mode. Used by the review-loop skill.

Two readers score the current text and a candidate, in opposite orders.
The script answers three questions a tired reader of score tables gets
wrong:

  1. Is the difference larger than noise?   (the band)
  2. Did each reader just prefer whichever text it read second, or first?
     (the order effect)
  3. Should the loop stop?                  (the round cap, repeated ties)

It never says a text is good. Scores compare two versions for these
readers; they do not predict what a real reader will decide.

Input (JSON file)
  { "scale": 180,
    "calibration": [ { "reader": "A", "x": 141, "y": 144 } ],
    "maxRounds": 3,
    "rounds": [
      { "label": "draft B",
        "reads": [
          { "reader": "A", "order": "current-first",
            "current": 146, "candidate": 145 },
          { "reader": "B", "order": "candidate-first",
            "current": 144, "candidate": 145 } ] } ] }

"calibration" is the A/A test: each reader scores the same text twice,
shown as two unlabelled documents. Any difference there is noise.

The band is the larger of 3 percent of the scale and the largest A/A
difference. A difference inside the band is a tie.

Usage
  review_verdict.py rounds.json [--out verdict.json]

Exit codes: 0 always when the input is valid (read the verdict), 2 bad input.
"""

import argparse
import json
import math
import sys

BAND_SHARE = 0.03
MAX_ROUNDS = 3
ORDERS = ("current-first", "candidate-first")


def band_of(scale, calibration):
    floor = int(math.ceil(BAND_SHARE * scale))
    measured = max([abs(c["x"] - c["y"]) for c in calibration or []] or [0])
    return max(floor, measured), floor, measured


def judge_round(rnd, band):
    reads = rnd.get("reads") or []
    if len(reads) < 2:
        raise ValueError("round %r needs two reads" % rnd.get("label"))
    orders = {r.get("order") for r in reads}
    if not orders <= set(ORDERS):
        raise ValueError("order must be one of %s" % (ORDERS,))
    diffs, votes = [], []
    for r in reads:
        d = r["candidate"] - r["current"]
        diffs.append(d)
        votes.append("candidate" if d > band else
                     "current" if d < -band else "tie")
    balanced = orders == set(ORDERS)
    # Which text did each reader lean to, however slightly: second or first?
    leans = []
    for r, d in zip(reads, diffs):
        if d == 0:
            leans.append(None)
        else:
            second = "candidate" if r["order"] == "current-first" \
                else "current"
            leans.append("second" if (d > 0) == (second == "candidate")
                         else "first")
    order_effect = (balanced and None not in leans
                    and len(set(leans)) == 1
                    and len({d > 0 for d in diffs}) > 1)
    if not balanced:
        verdict, why = "tie", ("the reads were not in opposite orders, so "
                               "an order effect cannot be ruled out")
    elif order_effect:
        verdict, why = "tie", ("each reader preferred the text it read %s; "
                               "that is an order effect, not a preference"
                               % leans[0])
    elif all(v == "candidate" for v in votes):
        verdict, why = "candidate", ("every reader preferred the candidate "
                                     "by more than the band")
    elif all(v == "current" for v in votes):
        verdict, why = "current", ("every reader preferred the current text "
                                   "by more than the band")
    else:
        verdict, why = "tie", ("at least one difference is inside the band "
                               "of %d, or the readers disagree" % band)
    return {"label": rnd.get("label"), "diffs": diffs, "votes": votes,
            "orderEffect": bool(order_effect), "verdict": verdict,
            "why": why}


def run(data):
    scale = data.get("scale")
    if not isinstance(scale, (int, float)) or scale <= 0:
        raise ValueError("scale must be a positive number")
    band, floor, measured = band_of(scale, data.get("calibration"))
    max_rounds = int(data.get("maxRounds") or MAX_ROUNDS)
    rounds = [judge_round(r, band) for r in data.get("rounds") or []]
    if not rounds:
        raise ValueError("no rounds")

    last = rounds[-1]
    no_win = 0
    for r in reversed(rounds):
        if r["verdict"] == "candidate":
            break
        no_win += 1
    if last["verdict"] == "candidate":
        stop, action = True, ("Offer the candidate to the person. It becomes "
                              "the text only on their yes.")
    elif len(rounds) >= max_rounds:
        stop, action = True, ("Round cap reached. The current text stands. "
                              "Report what was tried; do not run another "
                              "round in this loop.")
    elif no_win >= 2:
        stop, action = True, ("Two rounds in a row without a win. The "
                              "current text stands. Offer a fresh reader "
                              "with no history of this thread, given the "
                              "goal and the text, not the scores.")
    else:
        stop, action = False, ("The current text stands for now. One more "
                               "round is allowed.")
    notes = []
    if not data.get("calibration"):
        notes.append("No A/A calibration was given, so the band is the "
                     "floor of %d (3 percent of the scale). Run the A/A "
                     "test once per rubric." % floor)
    return {"scale": scale, "band": band,
            "bandFrom": "calibration" if measured > floor else "floor",
            "rounds": rounds, "roundsUsed": len(rounds),
            "maxRounds": max_rounds, "stop": stop,
            "standing": "candidate" if last["verdict"] == "candidate"
            else "current",
            "action": action, "notes": notes,
            "tool": "review_verdict.py (0.4.0)"}


def report(v):
    lines = ["band %d (%s) · %d of %d rounds"
             % (v["band"], v["bandFrom"], v["roundsUsed"], v["maxRounds"])]
    for r in v["rounds"]:
        lines.append("  %-14s %-9s diffs %s · %s"
                     % (r["label"], r["verdict"].upper(), r["diffs"],
                        r["why"]))
    lines.append(("STOP: " if v["stop"] else "CONTINUE: ") + v["action"])
    lines += ["note: " + n for n in v["notes"]]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("rounds")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    try:
        with open(args.rounds, encoding="utf-8") as f:
            verdict = run(json.load(f))
    except (OSError, ValueError, KeyError, TypeError) as err:
        print("review_verdict: %s" % err, file=sys.stderr)
        return 2
    print(report(verdict))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(verdict, f, indent=2)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
