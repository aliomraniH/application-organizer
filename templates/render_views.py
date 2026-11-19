#!/usr/bin/env python3
"""render_views.py: render a project's read-only views from its ledger rows.

Part of the application-organizer pattern (0.4.0). Standard library only.
Copy into project knowledge as render_views.py.txt and run it in isolated mode.

A view is a copy nobody edits: the register, a target's published page.
It is rendered by this script from rows listed to disk. A model never
retypes a view, and a view is never read back as a source.

Every view has a size budget. A view over its budget is not written; the
script exits 3 and says by how much. The fix is to take history out of the
view (it lives in events and in the doc's version history), never to let
the view grow.

Usage
  render_views.py register --ledger <dir> [--today 2026-11-18] \
      [--out register.md] [--budget 15000]
  render_views.py page --ledger <dir> --program northfield \
      [--out northfield.md] [--budget 30000]

<dir> holds one folder per collection (programs, snapshots, requirements),
one JSON file per row, as `list · <collection> · out_dir <dir>` writes them.

Exit codes: 0 written, 2 bad input, 3 over budget (nothing written).
"""

import argparse
import datetime
import json
import os
import sys

REGISTER_BUDGET = 15000
PAGE_BUDGET = 30000
DONE = ("received", "verified", "waived", "na")
SOON_DAYS = 14


def load_rows(folder):
    rows = {}
    if not os.path.isdir(folder):
        return rows
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            data = json.load(f)
        row_id = name[:-5]
        for wrap in ("row", "data"):
            if isinstance(data, dict) and isinstance(data.get(wrap), dict):
                row_id = str(data.get("path") or data.get("id")
                             or row_id).split("/")[-1]
                data = data[wrap]
                break
        rows[row_id] = data
    return rows


def parse_date(value):
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def cell(value):
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip() or "-"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "| " + " | ".join("---" for _ in header) + " |"]
    out += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def ordered(programs):
    return sorted(programs.items(),
                  key=lambda kv: (kv[1].get("order", 999),
                                  str(kv[1].get("name", kv[0]))))


def start_by(req):
    due = parse_date(req.get("due"))
    if due is None:
        return None
    return due - datetime.timedelta(days=int(req.get("leadDays") or 0))


def render_register(programs, requirements, today):
    lines = ["---", "title: Register (rendered view)",
             "rendered: %s" % today.isoformat(),
             "description: Rendered from the ledger by render_views.py. "
             "Do not edit; change the rows or the editable docs instead.",
             "---", "", "# Register", "", "## Documents", ""]
    doc_rows = []
    for pid, p in ordered(programs):
        policy = (p.get("policy") or {}).get("mode", "unknown")
        statements = p.get("statements") or [{}]
        for s in statements:
            doc = s.get("doc") or {}
            link = "[doc](%s)" % doc["url"] if doc.get("url") else "-"
            doc_rows.append([
                p.get("name", pid), p.get("phase", "drafting"),
                s.get("label", "-"), s.get("version"),
                s.get("status", "draft"), s.get("words"), s.get("fit"),
                s.get("gateOpen"), p.get("deadline"), policy, link])
    lines.append(table(["Target", "Phase", "Document", "Version", "Status",
                        "Words", "Limit and fit", "Gates open", "Deadline",
                        "Policy", "Editable doc"], doc_rows))

    if requirements:
        names = {pid: p.get("name", pid) for pid, p in programs.items()}
        order = {pid: i for i, (pid, _) in enumerate(ordered(programs))}
        reqs = sorted(requirements.values(), key=lambda r: (
            order.get(r.get("program"), 999), str(r.get("due") or "9999"),
            str(r.get("item"))))
        lines += ["", "## Requirements", "", table(
            ["Target", "Item", "Owner", "Status", "Start by", "Due"],
            [[names.get(r.get("program"), r.get("program")), r.get("item"),
              r.get("owner"), r.get("status"),
              start_by(r).isoformat() if start_by(r) else None,
              r.get("due")] for r in reqs])]
        soon, late = [], []
        horizon = today + datetime.timedelta(days=SOON_DAYS)
        for r in reqs:
            if r.get("status") in DONE:
                continue
            due, begin = parse_date(r.get("due")), start_by(r)
            label = "%s: %s" % (names.get(r.get("program"), r.get("program")),
                                r.get("item"))
            if due and due < today:
                late.append("- %s (was due %s, status %s)"
                            % (label, due, r.get("status")))
            elif begin and begin <= today and r.get("status") == "todo":
                late.append("- %s (should have started by %s to make %s)"
                            % (label, begin, due))
            elif due and due <= horizon:
                soon.append("- %s (due %s, status %s)"
                            % (label, due, r.get("status")))
        lines += ["", "## Needs attention", ""]
        lines += late or ["- nothing is late"]
        lines += ["", "## Due in the next %d days" % SOON_DAYS, ""]
        lines += soon or ["- nothing"]
    return "\n".join(lines) + "\n"


def render_page(pid, program, snapshots, today):
    lines = ["---", "title: %s (rendered view)" % program.get("name", pid),
             "rendered: %s" % today.isoformat(),
             "description: Current text only, rendered from the ledger by "
             "render_views.py. Do not edit. History is in the editable "
             "doc's version history and the ledger events.",
             "---", "", "# %s" % program.get("name", pid), "",
             "Phase: %s · Deadline: %s · Policy: %s"
             % (program.get("phase", "drafting"),
                program.get("deadline") or "-",
                (program.get("policy") or {}).get("mode", "unknown"))]
    for s in program.get("statements") or []:
        snap_id = str(s.get("snapshot") or "%s-%s" % (pid, s.get("key"))
                      ).split("/")[-1]
        snap = snapshots.get(snap_id) or {}
        lines += ["", "## %s" % s.get("label", s.get("key", "Document")), "",
                  "Version %s · %s · %s words · %s"
                  % (s.get("version", "-"), s.get("status", "draft"),
                     s.get("words", snap.get("words", "-")),
                     s.get("fit") or "no limit recorded"), ""]
        paragraphs = snap.get("paragraphs") or []
        if not paragraphs:
            lines.append("_No snapshot yet. The text is in the editable "
                         "doc._")
        for para in paragraphs:
            lines += [str(para), ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def emit(text, out, budget):
    size = len(text.encode("utf-8"))
    if size > budget:
        print("render_views: over budget by %d bytes (%d of %d). Nothing "
              "written. Take history out of the view or split it."
              % (size - budget, size, budget), file=sys.stderr)
        return 3
    if out:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("render_views: wrote %s (%d of %d bytes)" % (out, size, budget))
    else:
        sys.stdout.write(text)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name, budget in (("register", REGISTER_BUDGET), ("page", PAGE_BUDGET)):
        p = sub.add_parser(name)
        p.add_argument("--ledger", required=True)
        p.add_argument("--today")
        p.add_argument("--out")
        p.add_argument("--budget", type=int, default=budget)
        if name == "page":
            p.add_argument("--program", required=True)
    args = parser.parse_args(argv)

    today = parse_date(args.today) if args.today else datetime.date.today()
    if today is None:
        print("render_views: --today must be YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        programs = load_rows(os.path.join(args.ledger, "programs"))
        if not programs:
            raise ValueError("no programs rows under %s" % args.ledger)
        if args.command == "register":
            text = render_register(
                programs, load_rows(os.path.join(args.ledger,
                                                 "requirements")), today)
        else:
            if args.program not in programs:
                raise ValueError("no programs row %r" % args.program)
            text = render_page(
                args.program, programs[args.program],
                load_rows(os.path.join(args.ledger, "snapshots")), today)
    except (OSError, ValueError) as err:
        print("render_views: %s" % err, file=sys.stderr)
        return 2
    return emit(text, args.out, args.budget)


if __name__ == "__main__":
    sys.exit(main())
