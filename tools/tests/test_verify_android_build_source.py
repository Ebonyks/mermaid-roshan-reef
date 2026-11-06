from __future__ import annotations
import copy
import io
import os
import unittest
import urllib.error
from contextlib import redirect_stdout
from unittest.mock import patch
from tools import verify_android_build_source as gate

SHA = "a" * 40
REPO = gate.REPOSITORY


class SourceGateTests(unittest.TestCase):
    def setUp(self):
        self.run = {"id": 123, "run_number": 42, "event": "push", "head_branch": "dev", "head_sha": SHA,
                    "status": "completed", "conclusion": "success", "path": ".github/workflows/probes.yml",
                    "name": "Probe suite (graphics fork)", "repository": {"full_name": REPO},
                    "head_repository": {"full_name": REPO}}
        self.env = {"GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/dev",
                    "GITHUB_REPOSITORY": REPO, "ANDROID_SOURCE_SHA": SHA, "GH_TOKEN": "test-token-never-print"}
        self.branch = {"ref": "refs/heads/dev", "object": {"sha": SHA}}

    def invoke(self, responses, overrides=None):
        out = io.StringIO()
        with patch.dict(os.environ, {**self.env, **(overrides or {})}, clear=True), patch.object(gate, "fetch_json", side_effect=responses), redirect_stdout(out):
            code = gate.main()
        self.assertNotIn("test-token-never-print", out.getvalue())
        return code, out.getvalue()

    def test_matching_success(self):
        self.assertEqual(123, gate.verify_runs({"workflow_runs": [self.run]}, REPO, SHA))
        code, out = self.invoke([self.branch, {"workflow_runs": [self.run]}])
        self.assertEqual(0, code)
        self.assertIn("probe_run=123", out)

    def test_each_wrong_source_status_or_workflow_fails(self):
        wrong = {"event": "pull_request", "head_branch": "master", "head_sha": "b" * 40,
                 "status": "in_progress", "conclusion": "failure", "path": ".github/workflows/android.yml",
                 "name": "unrelated", "id": True, "run_number": True}
        for key, value in wrong.items():
            with self.subTest(key=key), self.assertRaises(ValueError):
                gate.verify_runs({"workflow_runs": [{**self.run, key: value}]}, REPO, SHA)

    def test_foreign_and_fork_green_rejected(self):
        for key in ("repository", "head_repository"):
            for value in ({}, None, {"full_name": "attacker/fork"}):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    gate.verify_runs({"workflow_runs": [{**self.run, key: value}]}, REPO, SHA)

    def test_missing_fields_and_malformed_responses_fail_closed(self):
        for payload in (None, [], {}, {"workflow_runs": {}}, {"workflow_runs": []}, {"workflow_runs": [None, "success", {}]}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                gate.verify_runs(payload, REPO, SHA)
        for key in self.run:
            run = copy.deepcopy(self.run)
            del run[key]
            with self.subTest(missing=key), self.assertRaises(ValueError):
                gate.verify_runs({"workflow_runs": [run]}, REPO, SHA)

    def test_old_green_and_other_branch_cannot_mask_red_head(self):
        runs = [{**self.run, "head_sha": "b" * 40}, {**self.run, "head_branch": "master"}, {**self.run, "conclusion": "failure"}]
        with self.assertRaises(ValueError):
            gate.verify_runs({"workflow_runs": runs}, REPO, SHA)

    def test_successful_exact_retry_allowed(self):
        self.assertEqual(123, gate.verify_runs({"workflow_runs": [{**self.run, "conclusion": "failure", "id": 122, "run_number": 41}, self.run]}, REPO, SHA))

    def test_newer_red_or_running_exact_head_blocks_older_green(self):
        for fields in ({"conclusion": "failure"}, {"status": "in_progress", "conclusion": None}):
            newer = {**self.run, "id": 124, "run_number": 43, **fields}
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                gate.verify_runs({"workflow_runs": [self.run, newer]}, REPO, SHA)

    def test_manual_master_topic_foreign_repo_and_missing_auth_rejected(self):
        cases = [("GITHUB_EVENT_NAME", "workflow_run"), ("GITHUB_REF", "refs/heads/master"),
                 ("GITHUB_REF", "refs/heads/codex/topic"), ("GITHUB_REPOSITORY", "attacker/fork"),
                 ("GH_TOKEN", ""), ("ANDROID_SOURCE_SHA", SHA + "&branch=master")]
        for key, value in cases:
            with self.subTest(key=key):
                self.assertEqual(1, self.invoke([], {key: value})[0])

    def test_dev_advance_and_wrong_ref_rejected_before_publish(self):
        for branch in ({"ref": "refs/heads/dev", "object": {"sha": "b" * 40}}, {"ref": "refs/heads/master", "object": {"sha": SHA}}, {}, None):
            with self.subTest(branch=branch):
                self.assertEqual(1, self.invoke([branch])[0])

    def test_network_error_hides_token_and_response(self):
        error = urllib.error.HTTPError("https://api.github.com", 403, "test-token-never-print", {}, None)
        self.assertEqual(1, self.invoke([error])[0])


if __name__ == "__main__":
    unittest.main()
