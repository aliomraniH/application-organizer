# Tests

Everything under `tests/` is **synthetic**. No row, name, identifier or date here comes from a real campaign. Every fixture row carries `"synthetic": true` so it can never be mistaken for, or merged into, a real ledger.

## fixtures/ledger/

One JSON file per ledger row, `<collection>/<doc id>.json`, following `templates/ledger-schema.md` (project-ledger v1). Two targets (Northfield University, Eastbrook Institute), one snapshot, four events, three tasks rows (one still `in_progress`), one claims row, four findings rows (one `ledger-transcribed`). Invented identifiers only (`10.0000/example.*`, `arxiv:2610.00001`).

They are used two ways:

1. **Seeding a demo tracker.** Publish `templates/console-page.html` as a private artifact with the `db` capability, then write each file as a row (`set · <collection>/<doc id> · file`) in one batch. The console page should then show two registry rows, one open tasks row, four activity lines and four findings.
2. **Checking the page offline.** `console-page.check.js` opens the template in a local Chromium with a fake `db` built from these files and reports console errors, horizontal scroll and whether each section rendered.

A demo tracker seeded from these rows is a throwaway: delete it, or clear its rows, before pointing a real project at the page. The `synthetic` field and the `meta/ledger.backfill.source` text both say so.

## console-page.check.js

    node tests/console-page.check.js            # needs playwright and a Chromium

Prints one line per viewport (`wide`, `phone`) and `seeded`, with the error count and whether the registry, tasks, events and findings sections rendered rows.

## fixtures/gates/ and final_check.test.py

    python3 tests/final_check.test.py           # standard library only

Tests for [`templates/final_check.py`](../templates/final_check.py), the script behind the final-check skill ([docs/gates.md](../docs/gates.md)). The fixtures are one short invented statement, one registry row with an `own-words` policy, four claims rows (one of each kind), one span of suggested wording and one attestation. Every row carries `"synthetic": true`.

Each test is named for the failure the gate stops:

- a passage matching Claude's wording under `own-words` fails, takes no waiver, and still matches after a change of punctuation or case; the person's rewrite passes; under `open` the same passage is a note
- a restrictive policy needs the person's answer; a missing policy row blocks; an old policy read must be repeated or waived
- a number with no claims row fails until it is covered or waived, and a waiver without a reason is not applied
- a claim survives an edit elsewhere with no re-pointing; an edit inside its span uncovers its facts
- a contradicted source takes no waiver; an unverified row, a number verified from metadata, an unlabelled preprint, unlabelled unpublished data and an overdue re-check each fail
- any edit after the gate returns the document to draft; a preview or a failed gate is never final
