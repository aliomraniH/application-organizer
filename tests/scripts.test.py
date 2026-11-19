#!/usr/bin/env python3
"""Tests for templates/render_views.py, review_verdict.py and ledger_lint.py.
Synthetic fixtures only (tests/fixtures/two-targets).

    python3 tests/scripts.test.py
"""

import copy
import datetime
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures", "two-targets")
TODAY = datetime.date(2026, 11, 18)


def module(name):
    path = os.path.join(ROOT, "templates", name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


rv, RV = module("render_views")
vd, VD = module("review_verdict")
ll, LL = module("ledger_lint")


def cli(script, *args):
    return subprocess.run([sys.executable, "-I", script, *args],
                          capture_output=True, text=True)


def reads(a_cur, a_cand, b_cur, b_cand):
    return [{"reader": "A", "order": "current-first",
             "current": a_cur, "candidate": a_cand},
            {"reader": "B", "order": "candidate-first",
             "current": b_cur, "candidate": b_cand}]


class Views(unittest.TestCase):
    def rows(self, name):
        return rv.load_rows(os.path.join(FIX, name))

    def test_register_is_rendered_from_rows_and_is_stable(self):
        a = rv.render_register(self.rows("programs"),
                               self.rows("requirements"), TODAY)
        b = rv.render_register(self.rows("programs"),
                               self.rows("requirements"), TODAY)
        self.assertEqual(a, b)
        self.assertIn("Do not edit", a)
        self.assertLess(a.index("Northfield University"),
                        a.index("Eastbrook Institute"))
        self.assertIn("| own-words |", a)

    def test_register_names_the_item_that_should_have_started(self):
        text = rv.render_register(self.rows("programs"),
                                  self.rows("requirements"), TODAY)
        late = text.split("## Needs attention")[1].split("##")[0]
        self.assertIn("Official transcript", late)
        self.assertIn("should have started by 2026-11-10", late)
        self.assertNotIn("Credential evaluation", late)   # received

    def test_page_holds_current_text_only(self):
        programs = self.rows("programs")
        text = rv.render_page("northfield", programs["northfield"],
                              self.rows("snapshots"), TODAY)
        self.assertIn("I want to learn to test these questions properly.",
                      text)
        self.assertNotIn("change log", text.lower())

    def test_view_over_budget_is_refused_not_truncated(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "register.md")
            r = cli(RV, "register", "--ledger", FIX, "--today", "2026-11-18",
                    "--out", out, "--budget", "500")
            self.assertEqual(r.returncode, 3)
            self.assertFalse(os.path.exists(out))
            self.assertIn("over budget", r.stderr)
            r = cli(RV, "register", "--ledger", FIX, "--today", "2026-11-18",
                    "--out", out)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(out))

    def test_register_template_is_a_fresh_render_of_the_fixtures(self):
        with open(os.path.join(ROOT, "templates", "register.md"),
                  encoding="utf-8") as f:
            self.assertEqual(f.read(), rv.render_register(
                self.rows("programs"), self.rows("requirements"), TODAY))

    def test_no_programs_is_bad_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cli(RV, "register", "--ledger", tmp).returncode,
                             2)


class Verdict(unittest.TestCase):
    def run_rounds(self, rounds, calibration=None, scale=180):
        return vd.run({"scale": scale, "calibration": calibration,
                       "rounds": [{"label": "r%d" % i, "reads": r}
                                  for i, r in enumerate(rounds, 1)]})

    def test_difference_inside_the_band_is_a_tie(self):
        v = self.run_rounds([reads(140, 143, 141, 144)])
        self.assertEqual(v["band"], 6)
        self.assertEqual(v["rounds"][0]["verdict"], "tie")
        self.assertFalse(v["stop"])

    def test_each_reader_preferring_what_it_read_second_is_not_a_win(self):
        v = self.run_rounds([reads(145, 147, 147, 148)])   # same direction
        self.assertFalse(v["rounds"][0]["orderEffect"])
        v = self.run_rounds([reads(138, 150, 152, 139)])   # big, opposite
        self.assertTrue(v["rounds"][0]["orderEffect"])
        self.assertEqual(v["rounds"][0]["verdict"], "tie")
        self.assertIn("read second", v["rounds"][0]["why"])

    def test_a_win_needs_every_reader_beyond_the_band(self):
        v = self.run_rounds([reads(130, 142, 128, 141)])
        self.assertEqual(v["rounds"][0]["verdict"], "candidate")
        self.assertTrue(v["stop"])
        self.assertIn("only on their yes", v["action"])
        v = self.run_rounds([reads(130, 142, 128, 131)])
        self.assertEqual(v["rounds"][0]["verdict"], "tie")

    def test_calibration_widens_the_band(self):
        cal = [{"reader": "A", "x": 140, "y": 151}]
        v = self.run_rounds([reads(130, 140, 128, 138)], cal)
        self.assertEqual(v["band"], 11)
        self.assertEqual(v["bandFrom"], "calibration")
        self.assertEqual(v["rounds"][0]["verdict"], "tie")

    def test_two_rounds_without_a_win_stop_the_loop(self):
        tie = reads(140, 142, 141, 143)
        v = self.run_rounds([tie, tie])
        self.assertTrue(v["stop"])
        self.assertEqual(v["standing"], "current")
        self.assertIn("fresh reader", v["action"])

    def test_round_cap_stops_the_loop(self):
        tie, lose = reads(140, 142, 141, 143), reads(150, 130, 149, 131)
        v = vd.run({"scale": 180, "maxRounds": 1,
                    "rounds": [{"label": "r1", "reads": lose}]})
        self.assertTrue(v["stop"])
        self.assertIn("Round cap", v["action"])
        self.assertEqual(v["rounds"][0]["verdict"], "current")

    def test_reads_in_the_same_order_cannot_show_a_win(self):
        same = reads(130, 145, 128, 144)
        same[1]["order"] = "current-first"
        v = self.run_rounds([same])
        self.assertEqual(v["rounds"][0]["verdict"], "tie")

    def test_cli_on_the_fixture(self):
        r = cli(VD, os.path.join(FIX, "rounds.json"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("order effect", r.stdout)
        self.assertEqual(cli(VD, "/nonexistent").returncode, 2)


class Lint(unittest.TestCase):
    def setUp(self):
        self.data = ll.load(FIX)

    def checks(self, data=None, level=None):
        return [(i["collection"], i["id"], i["check"])
                for i in ll.lint(data or self.data, TODAY)
                if level is None or i["level"] == level]

    def edit(self, col, row_id, **fields):
        data = copy.deepcopy(self.data)
        row, size = data[col][row_id]
        row.update(fields)
        data[col][row_id] = (row, len(json.dumps(row)))
        return data

    def test_fixture_has_no_errors_and_names_what_is_late(self):
        self.assertEqual(self.checks(level="error"), [])
        warns = self.checks(level="warn")
        self.assertIn(("requirements", "northfield-transcript", "start-by"),
                      warns)
        self.assertIn(("contacts", "registrar", "next-due"), warns)

    def test_every_fixture_row_is_marked_synthetic(self):
        for col, rows in self.data.items():
            for row_id, (row, _) in rows.items():
                self.assertIs(row.get("synthetic"), True, row_id)

    def test_task_row_shape_drift_is_an_error(self):
        data = self.edit("tasks", "2026-11-17-sync", status="done_partial",
                         docsRead=[{"node": "x", "rev": 1}])
        errors = self.checks(data, "error")
        self.assertIn(("tasks", "2026-11-17-sync", "status"), errors)
        self.assertIn(("tasks", "2026-11-17-sync", "docsRead"), errors)

    def test_oversized_and_abandoned_task_rows_are_flagged(self):
        data = self.edit("tasks", "2026-11-17-sync", changes=["x" * 5000])
        self.assertIn(("tasks", "2026-11-17-sync", "size"),
                      self.checks(data, "warn"))
        data = self.edit("tasks", "2026-11-18-northfield-sop",
                         startedAt="2026-11-01T10:00:00Z")
        self.assertIn(("tasks", "2026-11-18-northfield-sop", "left-open"),
                      self.checks(data, "warn"))

    def test_stale_counts_and_old_open_events_are_flagged(self):
        data = self.edit("meta", "ledger",
                         counts={"tasks": 28, "contacts": 3})
        self.assertIn(("meta", "ledger", "counts"), self.checks(data, "warn"))
        data = self.edit("events", "e-2026-11-17-001", status="queued",
                         at="2026-10-14T00:00:00Z")
        self.assertIn(("events", "e-2026-11-17-001", "stale-open"),
                      self.checks(data, "warn"))

    def test_target_without_policy_or_deadline_is_flagged(self):
        data = self.edit("programs", "northfield", policy=None, deadline=None)
        warns = self.checks(data, "warn")
        self.assertIn(("programs", "northfield", "policy"), warns)
        self.assertIn(("programs", "northfield", "deadline"), warns)

    def test_phase_and_statement_status_must_agree(self):
        data = self.edit("programs", "eastbrook", phase="drafting")
        self.assertIn(("programs", "eastbrook/sop", "phase-behind"),
                      self.checks(data, "warn"))
        data = self.edit("programs", "northfield", phase="submitted")
        self.assertIn(("programs", "northfield/sop", "status-behind"),
                      self.checks(data, "warn"))

    def test_overdue_requirement_is_an_error(self):
        data = self.edit("requirements", "northfield-letter-1",
                         due="2026-11-15")
        self.assertIn(("requirements", "northfield-letter-1", "overdue"),
                      self.checks(data, "error"))

    def test_requirement_needs_a_source_page(self):
        data = self.edit("requirements", "northfield-sop", source={})
        self.assertIn(("requirements", "northfield-sop", "source"),
                      self.checks(data, "warn"))

    def test_an_address_in_any_row_is_an_error(self):
        address = "dr.example" + chr(64) + "northfield.example"
        data = self.edit("contacts", "dr-example", note=address)
        self.assertIn(("contacts", "dr-example", "address"),
                      self.checks(data, "error"))

    def test_cli_exit_codes(self):
        self.assertEqual(cli(LL, "--ledger", FIX, "--today",
                             "2026-11-18").returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "ledger")
            shutil.copytree(FIX, bad)
            os.remove(os.path.join(bad, "meta", "ledger.json"))
            self.assertEqual(cli(LL, "--ledger", bad, "--today",
                                 "2026-11-18").returncode, 1)
        self.assertEqual(cli(LL, "--ledger", "/nonexistent").returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
