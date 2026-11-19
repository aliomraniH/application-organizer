#!/usr/bin/env python3
"""ledger_lint.py: check a project's ledger rows against the pattern.

Part of the application-organizer pattern (0.4.0). Standard library only.
Copy into project knowledge as ledger_lint.py.txt and run it in isolated
mode. Used by the pattern-audit skill and the weekly review.

Rows drift. A field changes shape, a count goes stale, a row stays open for
a month, a requirement passes the day it should have been started. None of
that shows from inside a chat, and a model asked to "check the ledger" reads
a sample. This script reads every row and says exactly which ones are off.

Usage
  ledger_lint.py --ledger <dir> [--today 2026-11-18] [--out lint.json]

<dir> holds one folder per collection, one JSON file per row, as
`list · <collection> · out_dir <dir>` writes them.

Levels: error (the row breaks a rule), warn (needs a decision or a fix
soon), info (worth knowing). Exit codes: 0 no errors, 1 errors, 2 bad input.
"""

import argparse
import datetime
import json
import os
import re
import sys

TASK_STATUS = ("in_progress", "done", "stopped")
TASK_REQUIRED = ("startedAt", "task", "status", "by")
TASK_MAX_BYTES = 4096
TASK_OPEN_DAYS = 2
EVENT_KINDS = ("propagated", "note", "needs_person", "conflict", "flag",
               "ledger", "gate", "status")
EVENT_OPEN = ("open", "queued", "in_progress", "needs_person")
EVENT_OPEN_DAYS = 14
PHASES = ("drafting", "submitted", "after", "closed")
STATEMENT_STATUS = ("draft", "final", "submitted")
MODES = ("open", "own-words", "feedback-only")
CLAIM_STATUS = ("verified", "unverified", "stale", "retracted",
                "contradicted", "retired")
REQ_STATUS = ("todo", "requested", "sent", "received", "verified", "waived",
              "na")
REQ_DONE = ("received", "verified", "waived", "na")
REQ_OWNER = ("person", "recommender", "institution", "target")
CONTACT_ROLES = ("prospect", "recommender", "office", "scheduler",
                 "reviewer", "other")
ADDRESS = re.compile(r"[\w.+-]+\x40[\w-]+\.[\w.-]+")
COUNTED = ("programs", "snapshots", "events", "tasks", "claims", "findings",
           "spans", "gates", "requirements", "contacts", "reviews")


def load(ledger):
    data = {}
    for col in sorted(os.listdir(ledger)):
        folder = os.path.join(ledger, col)
        if not os.path.isdir(folder):
            continue
        rows = {}
        for name in sorted(os.listdir(folder)):
            if not name.endswith(".json"):
                continue
            path = os.path.join(folder, name)
            with open(path, encoding="utf-8") as f:
                raw = f.read()
            row = json.loads(raw)
            row_id = name[:-5]
            for wrap in ("row", "data"):
                if isinstance(row, dict) and isinstance(row.get(wrap), dict):
                    row_id = str(row.get("path") or row.get("id")
                                 or row_id).split("/")[-1]
                    row = row[wrap]
                    raw = json.dumps(row)
                    break
            rows[row_id] = (row, len(raw.encode("utf-8")))
        data[col] = rows
    return data


def parse_date(value):
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def lint(data, today):
    out = []

    def add(level, col, row_id, check, detail):
        out.append({"level": level, "collection": col, "id": row_id,
                    "check": check, "detail": detail})

    def age(value):
        d = parse_date(value)
        return None if d is None else (today - d).days

    # ---- every row: no addresses
    for col, rows in data.items():
        for row_id, (row, _) in rows.items():
            if ADDRESS.search(json.dumps(row)):
                add("error", col, row_id, "address",
                    "An email address is stored in a row. Addresses live "
                    "in the Contact log, never in the ledger.")

    # ---- meta
    meta = data.get("meta", {})
    ledger = (meta.get("ledger") or ({}, 0))[0]
    if not ledger:
        add("error", "meta", "ledger", "missing", "No meta/ledger row.")
    else:
        if not ledger.get("schemaVersion"):
            add("error", "meta", "ledger", "schema",
                "meta/ledger has no schemaVersion.")
        for col, n in (ledger.get("counts") or {}).items():
            if col in data and len(data[col]) != n:
                add("warn", "meta", "ledger", "counts",
                    "counts.%s says %d; the collection holds %d rows."
                    % (col, n, len(data[col])))
        listed = set(ledger.get("collections") or [])
        for col in COUNTED:
            if data.get(col) and listed and col not in listed:
                add("warn", "meta", "ledger", "collections",
                    "Collection %s has rows but is not listed in "
                    "meta/ledger.collections." % col)

    # ---- tasks
    for row_id, (t, size) in data.get("tasks", {}).items():
        missing = [f for f in TASK_REQUIRED if not t.get(f)]
        if missing:
            add("error", "tasks", row_id, "fields",
                "Missing %s." % ", ".join(missing))
        if t.get("status") not in TASK_STATUS:
            add("error", "tasks", row_id, "status",
                "status is %r; allowed: %s."
                % (t.get("status"), ", ".join(TASK_STATUS)))
        if "docsRead" in t and not isinstance(t["docsRead"], dict):
            add("error", "tasks", row_id, "docsRead",
                "docsRead must be an object keyed by doc id, so a resuming "
                "chat can read its bookmark.")
        if size > TASK_MAX_BYTES:
            add("warn", "tasks", row_id, "size",
                "%d bytes; the limit is %d. Move detail to events."
                % (size, TASK_MAX_BYTES))
        if t.get("status") == "in_progress" and \
                (age(t.get("startedAt")) or 0) > TASK_OPEN_DAYS:
            add("warn", "tasks", row_id, "left-open",
                "in_progress since %s. Close it as done or stopped."
                % t.get("startedAt"))
        if t.get("status") in ("done", "stopped") and not t.get("endedAt"):
            add("warn", "tasks", row_id, "endedAt",
                "Closed without endedAt.")

    # ---- events
    for row_id, (e, _) in data.get("events", {}).items():
        if e.get("kind") not in EVENT_KINDS:
            add("warn", "events", row_id, "kind",
                "kind is %r; allowed: %s."
                % (e.get("kind"), ", ".join(EVENT_KINDS)))
        if e.get("status") in EVENT_OPEN and \
                (age(e.get("at")) or 0) > EVENT_OPEN_DAYS:
            add("warn", "events", row_id, "stale-open",
                "%s since %s. Resolve it, or close it as moot with a "
                "resolution." % (e.get("status"), e.get("at")))

    # ---- programs
    frozen = set()
    for row_id, (p, _) in data.get("programs", {}).items():
        phase = p.get("phase", "drafting")
        if phase not in PHASES:
            add("error", "programs", row_id, "phase",
                "phase is %r; allowed: %s." % (phase, ", ".join(PHASES)))
        if phase != "drafting":
            frozen.add(row_id)
        if phase == "closed" and not p.get("outcome"):
            add("warn", "programs", row_id, "outcome",
                "phase is closed with no outcome.")
        mode = (p.get("policy") or {}).get("mode")
        if phase == "drafting" and mode not in MODES:
            add("warn", "programs", row_id, "policy",
                "No AI-use policy row (mode %r). Nothing should be drafted "
                "for this target until its policy is read." % mode)
        if phase == "drafting" and not parse_date(p.get("deadline")):
            add("warn", "programs", row_id, "deadline",
                "No deadline on a target still being drafted.")
        for s in p.get("statements") or []:
            status = s.get("status", "draft")
            key = "%s/%s" % (row_id, s.get("key"))
            if status not in STATEMENT_STATUS:
                add("error", "programs", key, "statement-status",
                    "status is %r." % status)
            if status == "final" and not (s.get("final") or {}).get("hash"):
                add("error", "programs", key, "final-hash",
                    "final without the hash of the text that passed.")
            if status == "submitted" and phase == "drafting":
                add("warn", "programs", key, "phase-behind",
                    "A statement is submitted but the target's phase is "
                    "still drafting.")
            if status != "submitted" and phase in ("submitted", "after"):
                add("warn", "programs", key, "status-behind",
                    "The target's phase is %s but this statement is %s."
                    % (phase, status))

    # ---- claims
    for row_id, (c, _) in data.get("claims", {}).items():
        if c.get("status") not in CLAIM_STATUS:
            add("error", "claims", row_id, "status",
                "status is %r." % c.get("status"))
        if c.get("status") in ("unverified", "stale"):
            add("info", "claims", row_id, "unverified",
                "%s; it will fail the final check." % c.get("status"))
        due = parse_date(c.get("recheckBy"))
        if due and due < today and c.get("status") == "verified":
            add("warn", "claims", row_id, "recheck",
                "Re-check date %s has passed." % due)
        if not c.get("span") and c.get("status") != "retired":
            add("info", "claims", row_id, "span",
                "No span; the final check will match on text.")

    # ---- requirements
    for row_id, (r, _) in data.get("requirements", {}).items():
        if r.get("status") not in REQ_STATUS:
            add("error", "requirements", row_id, "status",
                "status is %r; allowed: %s."
                % (r.get("status"), ", ".join(REQ_STATUS)))
        if r.get("owner") not in REQ_OWNER:
            add("warn", "requirements", row_id, "owner",
                "owner is %r; allowed: %s."
                % (r.get("owner"), ", ".join(REQ_OWNER)))
        src = r.get("source") or {}
        if not (src.get("url") and src.get("readAt")):
            add("warn", "requirements", row_id, "source",
                "No source page and date. A requirement is read from the "
                "target's own page, not remembered.")
        if r.get("status") in REQ_DONE:
            continue
        due = parse_date(r.get("due"))
        if due is None:
            add("warn", "requirements", row_id, "due", "No due date.")
            continue
        begin = due - datetime.timedelta(days=int(r.get("leadDays") or 0))
        if due < today:
            add("error", "requirements", row_id, "overdue",
                "Due %s, status %s." % (due, r.get("status")))
        elif begin <= today and r.get("status") == "todo":
            add("warn", "requirements", row_id, "start-by",
                "Needs %s days and is due %s: it should have been started "
                "by %s." % (r.get("leadDays"), due, begin))

    # ---- contacts
    for row_id, (c, _) in data.get("contacts", {}).items():
        if c.get("role") not in CONTACT_ROLES:
            add("warn", "contacts", row_id, "role",
                "role is %r; allowed: %s."
                % (c.get("role"), ", ".join(CONTACT_ROLES)))
        due = parse_date(c.get("nextDue"))
        if due and due < today and not c.get("closed"):
            add("warn", "contacts", row_id, "next-due",
                "Next step was due %s: %s" % (due, c.get("nextStep") or ""))

    order = {"error": 0, "warn": 1, "info": 2}
    out.sort(key=lambda i: (order[i["level"]], i["collection"], i["id"]))
    return out


def report(items):
    counts = {lvl: sum(1 for i in items if i["level"] == lvl)
              for lvl in ("error", "warn", "info")}
    lines = ["ledger lint: %(error)d errors, %(warn)d warnings, %(info)d "
             "notes" % counts]
    for i in items:
        lines.append("  %-5s %s/%s · %s · %s"
                     % (i["level"].upper(), i["collection"], i["id"],
                        i["check"], i["detail"]))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--today")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    today = parse_date(args.today) if args.today else datetime.date.today()
    try:
        if today is None:
            raise ValueError("--today must be YYYY-MM-DD")
        items = lint(load(args.ledger), today)
    except (OSError, ValueError) as err:
        print("ledger_lint: %s" % err, file=sys.stderr)
        return 2
    print(report(items))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
            f.write("\n")
    return 1 if any(i["level"] == "error" for i in items) else 0


if __name__ == "__main__":
    sys.exit(main())
