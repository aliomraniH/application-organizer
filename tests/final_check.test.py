#!/usr/bin/env python3
"""Tests for templates/final_check.py. Synthetic fixtures only.

    python3 tests/final_check.test.py

Each test names the failure the gate exists to stop.
"""

import copy
import datetime
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures", "gates")
SCRIPT = os.path.join(ROOT, "templates", "final_check.py")

spec = importlib.util.spec_from_file_location("final_check", SCRIPT)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)

TODAY = datetime.date(2026, 11, 30)
CLAUDE_SENTENCE = ("I want to learn to test these questions with the rigor "
                   "that careful clinical work deserves.")


def load():
    with open(os.path.join(FIX, "document.txt"), encoding="utf-8") as f:
        text = f.read()
    _, program = fc.load_row(os.path.join(FIX, "programs", "northfield.json"))
    claims = fc.load_rows(os.path.join(FIX, "claims"))
    spans = fc.load_rows(os.path.join(FIX, "spans"))
    with open(os.path.join(FIX, "attestation.json"), encoding="utf-8") as f:
        attestation = json.load(f)
    return text, program, claims, spans, attestation


def check(text, program, claims, spans, attestation=None, waivers=None,
          preview=False):
    return fc.run_check(text, copy.deepcopy(program), "sop",
                        copy.deepcopy(claims), copy.deepcopy(spans),
                        waivers, attestation, TODAY, preview, "northfield")


def ids(gate, outcome="fail"):
    return [i["id"] for i in gate["items"] if i["outcome"] == outcome]


class Baseline(unittest.TestCase):
    def test_clean_document_passes_and_is_final(self):
        text, program, claims, spans, att = load()
        gate = check(text, program, claims, spans, att)
        self.assertEqual(gate["outcome"], "pass", gate["items"])
        self.assertEqual(fc.status_of(text, gate)[0], "final")

    def test_every_fixture_row_is_marked_synthetic(self):
        for folder, _, names in os.walk(FIX):
            for name in names:
                if name.endswith(".json"):
                    with open(os.path.join(folder, name)) as f:
                        self.assertIs(json.load(f).get("synthetic"), True,
                                      name)


class Authorship(unittest.TestCase):
    def test_claude_passage_under_own_words_fails_and_takes_no_waiver(self):
        text, program, claims, spans, att = load()
        text = text.replace("I want to learn to test these questions "
                            "properly.", CLAUDE_SENTENCE)
        gate = check(text, program, claims, spans, att)
        failed = ids(gate)
        self.assertEqual(failed, ["author:northfield-sop-0001:1"])
        waiver = [{"item": failed[0], "words": "It is fine.",
                   "reason": "deadline"}]
        gate = check(text, program, claims, spans, att, waiver)
        self.assertEqual(gate["outcome"], "fail")
        self.assertEqual(gate["needsFix"], 1)
        self.assertIn("fix, not a waiver",
                      gate["waiverProblems"][0]["problem"])

    def test_changing_only_punctuation_and_case_still_matches(self):
        text, program, claims, spans, att = load()
        altered = CLAUDE_SENTENCE.replace(" with the rigor",
                                          ", with the rigor").upper()
        gate = check(text + "\n\n" + altered, program, claims, spans, att)
        self.assertIn("author:northfield-sop-0001:1", ids(gate))

    def test_the_persons_rewrite_passes(self):
        text, program, claims, spans, att = load()
        rewrite = "I want to learn how to put these questions to a fair test."
        gate = check(text + "\n\n" + rewrite, program, claims, spans, att)
        self.assertEqual(gate["outcome"], "pass", gate["items"])

    def test_same_passage_under_open_policy_is_a_note_not_a_failure(self):
        text, program, claims, spans, _ = load()
        program["policy"]["mode"] = "open"
        gate = check(text + "\n\n" + CLAUDE_SENTENCE, program, claims, spans)
        self.assertEqual(gate["outcome"], "pass", gate["items"])
        self.assertTrue(any("record, not a failure" in n
                            for n in gate["notes"]))

    def test_restrictive_policy_needs_the_persons_answer(self):
        text, program, claims, spans, _ = load()
        gate = check(text, program, claims, spans)
        self.assertEqual(ids(gate), ["attestation:missing"])
        self.assertEqual(gate["needsFix"], 1)
        preview = check(text, program, claims, spans, preview=True)
        self.assertEqual(preview["open"], 0)
        self.assertTrue(preview["notes"])


class Policy(unittest.TestCase):
    def test_no_policy_row_blocks_and_takes_no_waiver(self):
        text, program, claims, spans, att = load()
        for policy in (None, {"mode": "unknown"}, {"mode": "open"}):
            program["policy"] = policy
            gate = check(text, program, claims, spans, att)
            self.assertIn("policy:missing", ids(gate))
            self.assertFalse(gate["items"][0]["waivable"])

    def test_old_policy_read_must_be_repeated_or_waived(self):
        text, program, claims, spans, att = load()
        program["policy"]["readAt"] = "2026-09-01"
        gate = check(text, program, claims, spans, att)
        self.assertEqual(ids(gate), ["policy:stale"])
        program["policy"]["recheckedAt"] = "2026-11-29"
        gate = check(text, program, claims, spans, att)
        self.assertEqual(gate["outcome"], "pass")


class Claims(unittest.TestCase):
    def test_number_with_no_row_fails_until_covered_or_waived(self):
        text, program, claims, spans, att = load()
        text += "\n\nThe clinic saw 4,000 patients last year."
        gate = check(text, program, claims, spans, att)
        failed = ids(gate)
        self.assertEqual(len(failed), 1)
        self.assertTrue(failed[0].startswith("uncovered:number:"))
        self.assertEqual(gate["items"][0]["hit"], "4,000")

        no_reason = [{"item": failed[0], "words": "Leave it."}]
        gate = check(text, program, claims, spans, att, no_reason)
        self.assertEqual(gate["outcome"], "fail")
        self.assertEqual(len(gate["waiverProblems"]), 1)

        waiver = [{"item": failed[0], "words": "That is our own count.",
                   "reason": "from the clinic's annual report, which I wrote",
                   "at": "2026-11-30T18:00:00Z"}]
        gate = check(text, program, claims, spans, att, waiver)
        self.assertEqual(gate["outcome"], "pass")
        self.assertEqual(gate["waivers"][0]["words"], "That is our own count.")
        self.assertEqual(ids(gate, "waived"), failed)

    def test_claim_survives_an_edit_elsewhere_without_repointing(self):
        text, program, claims, spans, att = load()
        claims["northfield-sop-03"]["docRev"] = 1      # an old revision
        text = text.replace("properly.", "properly, and to teach others.")
        gate = check(text, program, claims, spans, att)
        self.assertEqual(gate["outcome"], "pass", gate["items"])

    def test_editing_inside_a_span_uncovers_its_facts(self):
        text, program, claims, spans, att = load()
        gate = check(text.replace("212 adults", "312 adults"), program,
                     claims, spans, att)
        self.assertTrue(any(i.get("hit") == "312" for i in gate["items"]))
        self.assertIn("northfield-sop-03", " ".join(gate["notes"]))

    def test_contradicted_source_takes_no_waiver(self):
        text, program, claims, spans, att = load()
        claims["northfield-sop-03"]["status"] = "contradicted"
        waiver = [{"item": "claim:northfield-sop-03:contradicted",
                   "words": "Keep it.", "reason": "close enough"}]
        gate = check(text, program, claims, spans, att, waiver)
        self.assertEqual(ids(gate), ["claim:northfield-sop-03:contradicted"])
        self.assertEqual(gate["needsFix"], 1)

    def test_unverified_row_fails_and_can_be_waived(self):
        text, program, claims, spans, att = load()
        claims["northfield-sop-04"]["status"] = "unverified"
        gate = check(text, program, claims, spans, att)
        self.assertEqual(ids(gate), ["claim:northfield-sop-04:unverified"])
        self.assertTrue(gate["items"][0]["waivable"])

    def test_number_verified_from_metadata_is_below_its_level(self):
        text, program, claims, spans, att = load()
        claims["northfield-sop-03"]["verifiedHow"] = "metadata"
        claims["northfield-sop-03"]["qualifier"] = ""
        gate = check(text, program, claims, spans, att)
        self.assertEqual(ids(gate), ["claim:northfield-sop-03:level",
                                     "claim:northfield-sop-03:qualifier"])

    def test_preprint_must_be_labelled_in_the_sentence(self):
        text, program, claims, spans, att = load()
        claims["northfield-sop-03"]["source"]["status"] = "preprint"
        gate = check(text, program, claims, spans, att)
        self.assertEqual(ids(gate), ["claim:northfield-sop-03:preprint-label"])

    def test_unpublished_data_must_say_so(self):
        text, program, claims, spans, att = load()
        bare = "Our pilot suggests nurses read short notes first."
        text = text.replace(claims["northfield-sop-05"]["span"], bare)
        claims["northfield-sop-05"]["span"] = bare
        gate = check(text, program, claims, spans, att)
        self.assertEqual(ids(gate), ["claim:northfield-sop-05:label"])

    def test_fact_that_can_change_is_rechecked_after_its_date(self):
        text, program, claims, spans, att = load()
        claims["northfield-sop-04"]["recheckBy"] = "2026-11-15"
        gate = check(text, program, claims, spans, att)
        self.assertEqual(ids(gate), ["claim:northfield-sop-04:recheck"])


class FinalIsBoundToTheText(unittest.TestCase):
    def test_any_edit_after_the_gate_returns_the_document_to_draft(self):
        text, program, claims, spans, att = load()
        gate = check(text, program, claims, spans, att)
        self.assertEqual(fc.status_of(text + "  \n", gate)[0], "final")
        self.assertEqual(fc.status_of(text.replace("six", "seven"),
                                      gate)[0], "draft")

    def test_a_preview_or_a_failed_gate_is_never_final(self):
        text, program, claims, spans, att = load()
        preview = check(text, program, claims, spans, att, preview=True)
        self.assertEqual(fc.status_of(text, preview)[0], "draft")
        failed = check(text, program, claims, spans)
        self.assertEqual(fc.status_of(text, failed)[0], "draft")
        self.assertEqual(fc.status_of(text, None)[0], "draft")


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-I", SCRIPT, *args],
                              capture_output=True, text=True)

    def test_check_writes_a_gate_row_and_status_reads_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "gates", "northfield-sop.json")
            base = ["check", "--text", os.path.join(FIX, "document.txt"),
                    "--program", os.path.join(FIX, "programs",
                                              "northfield.json"),
                    "--key", "sop", "--claims", os.path.join(FIX, "claims"),
                    "--spans", os.path.join(FIX, "spans"),
                    "--today", "2026-11-30"]
            failed = self.run_cli(*base)
            self.assertEqual(failed.returncode, 1, failed.stdout)
            self.assertIn("attestation:missing", failed.stdout)
            preview = self.run_cli(*base, "--preview")
            self.assertEqual(preview.returncode, 0, preview.stdout)
            passed = self.run_cli(*base, "--attestation",
                                  os.path.join(FIX, "attestation.json"),
                                  "--out", out)
            self.assertEqual(passed.returncode, 0, passed.stdout)
            with open(out) as f:
                self.assertEqual(json.load(f)["outcome"], "pass")
            status = self.run_cli("status", "--text",
                                  os.path.join(FIX, "document.txt"),
                                  "--gate", out)
            self.assertEqual(status.returncode, 0)
            self.assertTrue(status.stdout.startswith("final"))

    def test_bad_input_is_exit_2(self):
        self.assertEqual(self.run_cli("check", "--text", "/nonexistent",
                                      "--program", "/nonexistent",
                                      "--key", "sop").returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
