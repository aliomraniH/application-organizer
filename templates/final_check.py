#!/usr/bin/env python3
"""final_check.py: the gate a controlled document passes before it is final.

Part of the application-organizer pattern (gates 1). Standard library only.
Copy into project knowledge as final_check.py.txt and run it in isolated mode.

It reads the document's text and the ledger rows that bear on it, and reports
every item that stands between the document and "final":

  policy       the target's AI-use policy row is missing, unknown or old
  author       a passage matches wording Claude wrote or suggested, under a
               policy that requires the person's own words
  attestation  the person has not yet answered the authorship question
  claim        a claims row whose span is in the text is unverified, below the
               level its kind requires, unlabelled, overdue or contradicted
  uncovered    a number, year, citation or name in the text that no claims
               span covers

Each item is pass, fail or waived. A waiver is the person's, per item, in
their words, with a reason. Two kinds of item take no waiver, only a fix:
a contradicted or retracted source, and a verbatim Claude passage under an
own-words or feedback-only policy.

The script records who wrote a span. It cannot know who thought of it. The
attestation is the person's.

Usage
  final_check.py check --text doc.txt --program programs/northfield.json \
      --key sop --claims claims/ --spans spans/ [--waivers waivers.json] \
      [--attestation attestation.json] [--today 2026-11-30] [--preview] \
      [--out gates/northfield-sop.json]
  final_check.py status --text doc.txt --gate gates/northfield-sop.json

Exit codes: check 0 = pass (or any preview), 1 = fail, 2 = bad input.
            status 0 = final, 1 = draft.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import unicodedata

TOOL = "final_check.py (gates 1)"
MODES = ("open", "own-words", "feedback-only")
RESTRICTIVE = ("own-words", "feedback-only")
POLICY_MAX_AGE_DAYS = 30
MIN_MATCH_WORDS = 8
CONTENT_LEVELS = ("full text", "abstract", "primary page")
UNPUBLISHED_LABELS = ("unpublished", "internal", "in development",
                      "not yet published", "preliminary", "in progress")
ORG_WORDS = ("University", "Institute", "College", "Hospital", "Center",
             "Centre", "Laboratory", "Lab", "School", "Clinic", "Foundation",
             "Journal", "Department", "Program", "Programme", "Society",
             "Association", "Agency", "Company", "Inc", "Award", "Awards",
             "Prize", "Fellowship", "Scholarship")
CALENDAR = {"January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December",
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"}
NUMBER_WORDS = ("two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                "thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
                "nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|"
                "ninety|hundred|thousand|million|billion|dozen")


# ---------------------------------------------------------------- text

def normalize(text):
    """One canonical form of the text: what the hash and every match use."""
    text = unicodedata.normalize("NFKC", text)
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'),
                 ("”", '"'), ("–", "-"), ("—", "-"),
                 (" ", " ")):
        text = text.replace(a, b)
    paragraphs = [re.sub(r"\s+", " ", p).strip()
                  for p in re.split(r"\n\s*\n|\r\n\s*\r\n", text)]
    return "\n".join(p for p in paragraphs if p)


def text_hash(text):
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def sentences(norm):
    """(start, end) of each sentence in normalized text."""
    out = []
    for para in re.finditer(r"[^\n]+", norm):
        start = para.start()
        for m in re.finditer(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])",
                             para.group()):
            out.append((start, para.start() + m.start()))
            start = para.start() + m.end()
        if start < para.end():
            out.append((start, para.end()))
    return out


def sentence_at(norm, sents, pos):
    for s, e in sents:
        if s <= pos < e or pos == e:
            return norm[s:e]
    return ""


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", normalize(text).casefold())


def count_words(text):
    return len(re.findall(r"\S+", normalize(text)))


# ---------------------------------------------------------------- rows

def load_row(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    row_id = os.path.splitext(os.path.basename(path))[0]
    if isinstance(data, dict):
        for wrap in ("row", "data"):
            if isinstance(data.get(wrap), dict):
                ident = data.get("path") or data.get("id") or row_id
                row_id = str(ident).split("/")[-1]
                data = data[wrap]
                break
    return row_id, data


def load_rows(path):
    """Rows from a directory of JSON files, or one JSON file holding a list
    or an {id: row} object. A missing path is an empty collection."""
    if not path or not os.path.exists(path):
        return {}
    if os.path.isdir(path):
        rows = {}
        for name in sorted(os.listdir(path)):
            if name.endswith(".json"):
                row_id, row = load_row(os.path.join(path, name))
                rows[row_id] = row
        return rows
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {str(r.get("id") or i): (r.get("row") or r.get("data") or r)
                for i, r in enumerate(data)}
    return {k: v for k, v in data.items() if isinstance(v, dict)}


def for_document(rows, program, key):
    return {i: r for i, r in rows.items()
            if r.get("program") == program and r.get("key") == key}


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


# ---------------------------------------------------------------- detector

def detect(norm):
    """Every place in the text that states a checkable fact, by shape.
    It over-reports on purpose: a hit costs one claims row or one waiver,
    a miss costs a wrong fact in a submitted document."""
    hits = []

    def add(kind, m_start, m_end):
        hits.append({"kind": kind, "start": m_start, "end": m_end,
                     "text": norm[m_start:m_end]})

    for m in re.finditer(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?:\s?%| percent)?",
                         norm):
        t = m.group().rstrip(",")
        year = re.fullmatch(r"(19|20)\d{2}", t)
        add("year" if year else "number", m.start(), m.start() + len(t))
    for m in re.finditer(r"\b(?:%s)(?:[- ](?:%s))*(?:\s+percent|-fold)?\b"
                         % (NUMBER_WORDS, NUMBER_WORDS), norm, re.I):
        add("number", m.start(), m.end())
    for m in re.finditer(r"\([^()]*\b(?:19|20)\d{2}[a-z]?\b[^()]*\)", norm):
        if re.search(r"[A-Z]", m.group()):
            add("citation", m.start(), m.end())
    for m in re.finditer(r"\b[A-Z][\w'-]+(?: et al\.| (?:and|&) [A-Z][\w'-]+)?"
                         r",? \((?:19|20)\d{2}[a-z]?\)", norm):
        add("citation", m.start(), m.end())
    cap = r"(?!I\b)[A-Z][\w'-]*"
    for m in re.finditer(r"\b(?:Dr|Prof|Professor|Mr|Ms|Mrs)\.? %s(?: %s){0,3}"
                         % (cap, cap), norm):
        add("person", m.start(), m.end())
    starts = {s for s, _ in sentences(norm)}
    link = r"(?: (?:of|for|the|and|in|at|on|de|&))?"
    for m in re.finditer(r"\b%s(?:%s %s)+" % (cap, link, cap), norm):
        words = m.group().split()
        if any(w.strip(".,") in ORG_WORDS for w in words):
            add("organization", m.start(), m.end())
            continue
        start = m.start()
        if start in starts:                      # drop a sentence-first word
            start += len(words[0]) + 1
            words = words[1:]
        kept = [w for w in words if w[0].isupper()]
        if len(kept) >= 2 and not all(w.strip(".,") in CALENDAR for w in kept):
            add("name", start, m.end())
    hits.sort(key=lambda h: (h["start"], -(h["end"] - h["start"])))
    out = []
    for h in hits:                               # drop hits inside a wider hit
        if not any(o["start"] <= h["start"] and h["end"] <= o["end"]
                   for o in out):
            out.append(h)
    return out


# ---------------------------------------------------------------- checks

def item(item_id, check, detail, waivable, **extra):
    row = {"id": item_id, "check": check, "outcome": "fail",
           "waivable": waivable, "detail": detail}
    row.update(extra)
    return row


def check_policy(program, today):
    policy = program.get("policy") or {}
    mode = policy.get("mode")
    if mode not in MODES or not policy.get("readAt") or not (
            policy.get("sourceUrl") or policy.get("note")):
        return mode if mode in MODES else "unknown", [item(
            "policy:missing", "policy",
            "No usable AI-use policy row for this target. Read the target's "
            "policy page and write programs/<id>.policy with mode, sourceUrl, "
            "quote and readAt. A target with no published policy still gets "
            "a row: mode open, with a note naming the pages checked.", False)]
    items = []
    read = parse_date(policy.get("recheckedAt") or policy.get("readAt"))
    if read is None or (today - read).days > POLICY_MAX_AGE_DAYS:
        items.append(item(
            "policy:stale", "policy",
            "The policy page was last read on %s. Re-read it and set "
            "policy.recheckedAt before the document is final."
            % (policy.get("recheckedAt") or policy.get("readAt")), True))
    return mode, items


def check_authorship(norm, spans, mode):
    """Passages in the text that match wording Claude wrote or suggested."""
    haystack = " " + " ".join(tokens(norm)) + " "
    matches = []
    for span_id, span in sorted(spans.items()):
        span_norm = normalize(span.get("text", ""))
        n = 0
        for s, e in sentences(span_norm):
            words = tokens(span_norm[s:e])
            if len(words) < MIN_MATCH_WORDS:
                continue
            n += 1
            if " " + " ".join(words) + " " in haystack:
                matches.append((span_id, n, span.get("kind", "written"),
                                span_norm[s:e]))
    if mode not in RESTRICTIVE:
        return [], matches
    return [item("author:%s:%d" % (span_id, n), "author",
                 "This passage matches wording Claude %s, and the target's "
                 "policy is %s. Fix: the person rewrites it, or the policy "
                 "row is corrected from its source page."
                 % ("suggested" if kind == "suggested" else "wrote", mode),
                 False, passage=passage)
            for span_id, n, kind, passage in matches], matches


def claim_kind(claim, span):
    if claim.get("kind"):
        return claim["kind"]
    if (claim.get("source") or {}).get("status") == "person":
        return "account"
    return "number" if re.search(r"\d", span) else "work"


def check_claims(norm, sents, claims, today):
    items, ranges, absent = [], [], []
    for claim_id, claim in sorted(claims.items()):
        span = normalize(claim.get("span") or claim.get("text") or "")
        if not span or claim.get("status") == "retired":
            continue
        found = [m.start() for m in re.finditer(re.escape(span), norm)]
        if not found:
            absent.append(claim_id)
            continue
        ranges.extend((p, p + len(span)) for p in found)
        sentence = sentence_at(norm, sents, found[0])
        source = claim.get("source") or {}
        status = claim.get("status")
        kind = claim_kind(claim, span)

        def fail(reason, detail, waivable=True):
            items.append(item("claim:%s:%s" % (claim_id, reason), "claim",
                              detail, waivable, span=span))

        if status in ("contradicted", "retracted"):
            fail("contradicted", "The source is %s for this sentence. Fix or "
                 "cut the sentence; a waiver does not apply." % status, False)
            continue
        if status != "verified":
            fail("unverified", "The claims row is %s. Verify it at the "
                 "source, or the person waives it with a reason."
                 % (status or "without a status"))
        if kind in ("number", "work"):
            if claim.get("verifiedHow") not in CONTENT_LEVELS:
                fail("level", "A %s needs the page where it appears (full "
                     "text, abstract or primary page); this row was verified "
                     "by %s." % ("quoted number" if kind == "number"
                                 else "description of someone's work",
                                 claim.get("verifiedHow") or "nothing"))
            if kind == "number" and not claim.get("qualifier"):
                fail("qualifier", "A quoted number keeps its qualifier "
                     "(sample, setting, design). The row has none.")
            if source.get("status") == "preprint" and \
                    "preprint" not in sentence.casefold():
                fail("preprint-label", "The source is a preprint and the "
                     "sentence does not say so.")
        if kind in ("account", "unpublished"):
            if source.get("status") != "person" or not claim.get("verifiedBy"):
                fail("account", "The person's own account needs their "
                     "confirmation: source.status person and verifiedBy.")
        if kind == "unpublished" and not any(
                label in sentence.casefold() for label in UNPUBLISHED_LABELS):
            fail("label", "Unpublished data must be labelled as such in the "
                 "sentence (for example: unpublished, internal, preliminary).")
        due = parse_date(claim.get("recheckBy"))
        if due and due < today:
            fail("recheck", "This fact can change and its re-check date %s "
                 "has passed. Re-verify it and move recheckBy." % due)
    return items, ranges, absent


def check_coverage(norm, sents, ranges):
    items = []
    hits = detect(norm)
    for h in hits:
        if any(s <= h["start"] and h["end"] <= e for s, e in ranges):
            continue
        sentence = sentence_at(norm, sents, h["start"])
        digest = hashlib.sha256((sentence + "|" + h["text"]).encode("utf-8")
                                ).hexdigest()[:8]
        items.append(item(
            "uncovered:%s:%s" % (h["kind"], digest), "uncovered",
            "No claims span covers this %s. Add a claims row whose span "
            "contains it, or the person waives it with a reason." % h["kind"],
            True, hit=h["text"], sentence=sentence))
    return items, len(hits)


def apply_waivers(items, waivers):
    by_id = {i["id"]: i for i in items}
    applied, problems = [], []
    for w in waivers or []:
        target = by_id.get(w.get("item"))
        if target is None:
            problems.append({"item": w.get("item"),
                             "problem": "no open item with this id"})
        elif not target["waivable"]:
            problems.append({"item": w["item"], "problem":
                             "this item takes a fix, not a waiver"})
        elif not (str(w.get("words", "")).strip()
                  and str(w.get("reason", "")).strip()):
            problems.append({"item": w["item"], "problem": "a waiver needs "
                             "the person's words and a reason"})
        else:
            target["outcome"] = "waived"
            applied.append({"item": w["item"], "words": w["words"],
                            "reason": w["reason"], "at": w.get("at")})
    return applied, problems


def run_check(text, program, key, claims, spans, waivers=None,
              attestation=None, today=None, preview=False, program_id=None):
    today = today or datetime.date.today()
    norm = normalize(text)
    sents = sentences(norm)
    program_id = program_id or program.get("id") or ""
    claims = for_document(claims, program_id, key) if program_id else claims
    spans = for_document(spans, program_id, key) if program_id else spans

    mode, items = check_policy(program, today)
    author_items, matches = check_authorship(norm, spans, mode)
    claim_items, ranges, absent = check_claims(norm, sents, claims, today)
    cover_items, hit_count = check_coverage(norm, sents, ranges)
    items += author_items + claim_items + cover_items

    notes = []
    if absent:
        notes.append("Claims rows whose span is no longer in the text (no "
                     "action; retire them when convenient): "
                     + ", ".join(absent))
    if mode == "open" and matches:
        notes.append("%d passage(s) match wording Claude wrote or suggested; "
                     "the policy is open, so this is a record, not a "
                     "failure." % len(matches))
    if mode == "feedback-only" and any(
            s.get("kind") == "suggested" for s in spans.values()):
        notes.append("Suggested wording is on record for a feedback-only "
                     "target. Under this policy Claude comments on the "
                     "person's text and offers no replacement wording.")

    attested = bool(attestation and str(attestation.get("words", "")).strip())
    if mode in RESTRICTIVE and not attested:
        if preview:
            notes.append("The authorship question has not been asked yet; it "
                         "is asked once, at the final check.")
        else:
            items.append(item(
                "attestation:missing", "attestation",
                "The target's policy is %s. Ask the person once, show them "
                "what the record shows, and store their answer in their "
                "words." % mode, False))

    applied, problems = apply_waivers(items, waivers)
    failed = [i for i in items if i["outcome"] == "fail"]
    policy = program.get("policy") or {}
    return {
        "program": program_id, "key": key,
        "hash": text_hash(text), "words": count_words(text),
        "at": today.isoformat(), "preview": bool(preview),
        "policy": {"mode": mode, "readAt": policy.get("readAt"),
                   "recheckedAt": policy.get("recheckedAt"),
                   "sourceUrl": policy.get("sourceUrl")},
        "checked": {"claimsInText": len(claims) - len(absent),
                    "detectorHits": hit_count, "spansOnRecord": len(spans)},
        "items": items, "waivers": applied, "waiverProblems": problems,
        "attestation": attestation if attested else None,
        "notes": notes,
        "open": len(failed),
        "needsFix": len([i for i in failed if not i["waivable"]]),
        "outcome": "pass" if not failed else "fail",
        "tool": TOOL,
    }


def status_of(text, gate):
    """final only while the text is byte-for-byte the text that passed."""
    if not gate or gate.get("preview") or gate.get("outcome") != "pass":
        return "draft", "no passed gate on record"
    if gate.get("hash") != text_hash(text):
        return "draft", "the text changed after the gate passed"
    return "final", "the text matches the gate that passed on %s" % gate["at"]


# ---------------------------------------------------------------- CLI

def report(gate):
    lines = ["%s %s-%s: %s (%d open, %d need a fix, %d waived) · %d words · "
             "policy %s"
             % ("PREVIEW" if gate["preview"] else "FINAL CHECK",
                gate["program"], gate["key"], gate["outcome"].upper(),
                gate["open"], gate["needsFix"], len(gate["waivers"]),
                gate["words"], gate["policy"]["mode"])]
    for i in gate["items"]:
        mark = {"fail": "FAIL ", "waived": "WAIVED"}[i["outcome"]]
        lines.append("  %s %s%s" % (mark, i["id"],
                                    "" if i["waivable"] else "  (fix only)"))
        quoted = i.get("passage") or i.get("hit") or i.get("span")
        if quoted:
            lines.append("         \"%s\"" % quoted)
        lines.append("         " + i["detail"])
    for p in gate["waiverProblems"]:
        lines.append("  WAIVER NOT APPLIED %s: %s" % (p["item"], p["problem"]))
    for n in gate["notes"]:
        lines.append("  note: " + n)
    return "\n".join(lines)


def read_json(path):
    if not path:
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("check")
    c.add_argument("--text", required=True)
    c.add_argument("--program", required=True)
    c.add_argument("--key", required=True)
    c.add_argument("--claims")
    c.add_argument("--spans")
    c.add_argument("--waivers")
    c.add_argument("--attestation")
    c.add_argument("--today")
    c.add_argument("--preview", action="store_true")
    c.add_argument("--out")
    s = sub.add_parser("status")
    s.add_argument("--text", required=True)
    s.add_argument("--gate", required=True)
    args = parser.parse_args(argv)

    try:
        with open(args.text, encoding="utf-8") as f:
            text = f.read()
        if args.command == "status":
            state, why = status_of(text, read_json(args.gate))
            print("%s: %s" % (state, why))
            return 0 if state == "final" else 1
        program_id, program = load_row(args.program)
        today = parse_date(args.today) if args.today else None
        if args.today and today is None:
            raise ValueError("--today must be YYYY-MM-DD")
        gate = run_check(text, program, args.key, load_rows(args.claims),
                         load_rows(args.spans), read_json(args.waivers),
                         read_json(args.attestation), today, args.preview,
                         program_id)
    except (OSError, ValueError) as err:
        print("final_check: %s" % err, file=sys.stderr)
        return 2
    print(report(gate))
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(gate, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return 0 if gate["preview"] or gate["outcome"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
