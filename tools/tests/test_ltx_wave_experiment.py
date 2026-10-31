"""Failure-first staged experiment contracts; no GPU/model or art acceptance."""
import copy
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from tools import ltx_wave_experiment as runner


class FakeClock:
    def __init__(self):
        self.value = 0.0

    def __call__(self):
        return self.value

    def sleep(self, seconds):
        self.value += seconds


class FakeClient:
    def __init__(self, history=None, busy=None, missing_input=False, fail_submit=False):
        self.history = history
        self.busy = busy
        self.missing_input = missing_input
        self.fail_submit = fail_submit
        self.calls = []
        self.queue_after_submit = {"queue_running": [[0, "owned-prompt"]], "queue_pending": []}

    def request(self, path, data=None):
        self.calls.append((path, data))
        if path == "/queue":
            if self.busy is not None:
                return self.busy
            if any(p == "/prompt" for p, _ in self.calls):
                return self.queue_after_submit
            return {"queue_running": [], "queue_pending": []}
        if path == "/object_info":
            return {"SaveImage": {"input": {"required": {"images": ["IMAGE"]} if self.missing_input else {}}},
                    "SaveLatent": {"input": {"required": {}}}}
        if path == "/prompt":
            if self.fail_submit:
                raise OSError("submission connection closed")
            return {"prompt_id": "owned-prompt", "node_errors": {}}
        if path.startswith("/history/"):
            return {} if self.history is None else {"owned-prompt": self.history}
        if path == "/interrupt":
            return {}
        raise AssertionError(path)


class StageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.packet = self.root / "assets_src/animation/test"
        self.packet.mkdir(parents=True)
        self.runtime = self.root / "runtime"
        (self.runtime / "input").mkdir(parents=True)
        (self.runtime / "output/take").mkdir(parents=True)
        self.source = self.packet / "source.png"
        Image.new("RGBA", (8, 8), "pink").save(self.source)
        (self.runtime / "input/source.png").write_bytes(self.source.read_bytes())
        Image.new("RGBA", (8, 8), "blue").save(self.runtime / "output/take/frame.png")
        (self.runtime / "output/take/video.latent").write_bytes(b"synthetic latent")
        self.job = {"schema": "reef.wave-repair-campaign.v1", "limits": {"takes_per_changed_method": 2,
                    "new_transformer_takes_max": 10, "wall_minutes_per_gpu_take": 0.1},
                    "methods": [{"id": f"method-{i}"} for i in range(6)], "attempts": []}
        self.workflow = {"42": {"class_type": "SaveImage", "inputs": {"filename_prefix": "take/frame"}},
                         "20": {"class_type": "SaveLatent", "inputs": {"filename_prefix": "take/video"}}}
        self.source_manifest = {"sources": [{"path": "assets_src/animation/test/source.png", "sha256": runner.sha(self.source),
                                              "role": "approved_identity", "runtime_path": "input/source.png"}],
                                "model_workflow_pins": {"revision": "synthetic-test-only"}, "settings": {"frames": 1, "fps": 24}}
        self.outputs = {"images": [{"node": "42", "name": "native_frames", "count": 1, "canvas": [8, 8]}],
                        "latents": [{"node": "20", "name": "video", "count": 1}]}
        self.history = {"status": {"status_str": "success"}, "outputs": {
                       "42": {"images": [{"filename": "frame.png", "subfolder": "take", "type": "output"}]},
                       "20": {"latents": [{"filename": "video.latent", "subfolder": "take", "type": "output"}]}}}
        self.clock = FakeClock()
        self.save_inputs()

    def save_inputs(self):
        for name, value in (("job.json", self.job), ("workflow.json", self.workflow),
                            ("sources.json", self.source_manifest), ("outputs.json", self.outputs)):
            runner.write_json(self.packet / name, value)

    def run_stage(self, client=None, **overrides):
        values = {"job": "assets_src/animation/test/job.json", "method": "method-0", "stage": "first-pass",
                  "workflow": "assets_src/animation/test/workflow.json", "sources": "assets_src/animation/test/sources.json",
                  "outputs": "assets_src/animation/test/outputs.json", "output": "assets_src/animation/test/attempt-1",
                  "runtime": self.runtime, "client": client or FakeClient(self.history),
                  "clock": self.clock, "sleep": self.clock.sleep, "sample_gpu": lambda: {"status": "UNAVAILABLE"},
                  "progress": lambda *args, **kwargs: None}
        values.update(overrides)
        return runner.run(self.root, **values)

    def ledger(self):
        return runner.read_json(self.packet / "job.json")["attempts"]

    def receipt(self, folder="attempt-1"):
        return runner.read_json(self.packet / folder / "receipt.json")

    def review(self):
        images = []
        for index in range(1):
            image = self.packet / f"reviewed_{index}.png"
            Image.new("RGBA", (8, 8), "blue").save(image)
            images.append({"index": index, "path": runner.relative(self.root, image), "sha256": runner.sha(image)})
        record = {"schema": runner.REVIEW_SCHEMA, "reviewer_kind": "model_observation", "reviewer": "synthetic tester",
                  "reviewed_at_utc": "2026-10-10T00:00:00Z", "checks": {"topology": "PASS", "blur": "PASS"},
                  "artifacts": images, "inputs": copy.deepcopy(self.source_manifest["sources"])}
        path = self.packet / "review.json"
        runner.write_json(path, record)
        return record, runner.relative(self.root, path)

    def test_success_preserves_native_images_latents_and_never_accepts_art(self):
        receipt = self.run_stage()
        self.assertEqual(receipt["status"], "EXECUTION_PASS")
        self.assertEqual(self.ledger()[0]["status"], "EXECUTION_PASS")
        self.assertEqual((self.packet / "attempt-1/native_frames/0000.png").read_bytes(), (self.runtime / "output/take/frame.png").read_bytes())
        self.assertEqual((self.packet / "attempt-1/video/video_0000.latent").read_bytes(), b"synthetic latent")
        self.assertFalse(any(receipt["acceptance"].values()))
        self.assertEqual(receipt["prompt_id"], "owned-prompt")

    def test_source_preflight_failure_consumes_reserved_attempt(self):
        self.source.write_bytes(b"changed")
        client = FakeClient(self.history)
        with self.assertRaisesRegex(ValueError, "changed pinned"):
            self.run_stage(client)
        self.assertEqual(len(self.ledger()), 1)
        self.assertEqual(self.ledger()[0]["status"], "PREFLIGHT_FAIL")
        self.assertFalse(client.calls)

    def test_staged_runtime_hash_must_match_source(self):
        (self.runtime / "input/source.png").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "runtime input"):
            self.run_stage()
        self.assertEqual(len(self.ledger()), 1)

    def test_failed_and_pending_reservations_count_against_method_cap(self):
        self.job["attempts"] = [{"id": "failed", "method": "method-0", "status": "PREFLIGHT_FAIL"},
                                {"id": "pending", "method": "method-0", "status": "RESERVED"}]
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, "Method attempt cap"):
            self.run_stage()
        self.assertFalse((self.packet / "attempt-1").exists())

    def test_campaign_cap_shared_across_methods(self):
        self.job["attempts"] = [{"id": str(i), "method": f"method-{i // 2}", "status": "EXECUTION_FAIL"} for i in range(10)]
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, "Campaign attempt cap"):
            self.run_stage(method="method-5")

    def test_cap_cannot_be_silently_widened(self):
        self.job["limits"]["takes_per_changed_method"] = 3
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, "two attempts"):
            self.run_stage()

    def test_existing_output_is_never_overwritten(self):
        (self.packet / "attempt-1").mkdir()
        (self.packet / "attempt-1/keep.txt").write_text("preserve")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_stage()
        self.assertEqual((self.packet / "attempt-1/keep.txt").read_text(), "preserve")

    def test_private_and_outside_outputs_rejected_before_submission(self):
        for output in ("../outside", ".secrets/study", "assets_src/animation/.git/attempt", "assets/test"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                self.run_stage(output=output)
        self.assertEqual(len(self.ledger()), 0)

    def test_remote_endpoint_is_forbidden(self):
        for endpoint in ("https://127.0.0.1:8194", "http://example.org:8194", "http://user:pass@localhost:8194", "http://localhost:8194/elsewhere"):
            with self.subTest(endpoint=endpoint), self.assertRaises(ValueError):
                runner.ComfyClient(endpoint)

    def test_busy_queue_failure_is_counted_and_does_not_interrupt(self):
        client = FakeClient(self.history, busy={"queue_running": [[0, "other-prompt"]], "queue_pending": []})
        with self.assertRaisesRegex(ValueError, "active/pending"):
            self.run_stage(client)
        self.assertEqual(self.receipt()["status"], "PREFLIGHT_FAIL")
        self.assertNotIn("/interrupt", [path for path, _ in client.calls])

    def test_pending_queue_is_not_shared(self):
        client = FakeClient(self.history, busy={"queue_running": [], "queue_pending": [[0, "other-prompt"]]})
        with self.assertRaisesRegex(ValueError, "active/pending"):
            self.run_stage(client)
        self.assertNotIn("/prompt", [path for path, _ in client.calls])

    def test_schema_required_input_failure_is_counted_before_prompt(self):
        client = FakeClient(self.history, missing_input=True)
        with self.assertRaisesRegex(ValueError, "required inputs"):
            self.run_stage(client)
        self.assertEqual(len(self.ledger()), 1)
        self.assertNotIn("/prompt", [path for path, _ in client.calls])

    def test_timeout_interrupts_only_sole_owned_running_prompt(self):
        client = FakeClient()
        with self.assertRaises(TimeoutError):
            self.run_stage(client)
        self.assertTrue(self.receipt()["owned_job_interrupted"])
        self.assertEqual(self.receipt()["error_type"], "TimeoutError")

    def test_timeout_never_interrupts_a_shared_or_different_job(self):
        for running in ([[0, "other-prompt"]], [[0, "owned-prompt"], [1, "other-prompt"]], []):
            self.clock = FakeClock()
            client = FakeClient()
            client.queue_after_submit = {"queue_running": running, "queue_pending": []}
            folder = f"attempt-{len(self.ledger()) + 1}"
            with self.subTest(running=running), self.assertRaises(TimeoutError):
                self.run_stage(client, method=f"method-{len(self.ledger())}", output=f"assets_src/animation/test/{folder}")
            self.assertNotIn("/interrupt", [path for path, _ in client.calls])

    def test_submission_disconnect_has_counted_receipt_and_no_unknown_interrupt(self):
        client = FakeClient(fail_submit=True)
        with self.assertRaises(OSError):
            self.run_stage(client)
        self.assertEqual(len(self.ledger()), 1)
        self.assertEqual(self.receipt()["status"], "SUBMISSION_UNKNOWN")
        self.assertNotIn("/interrupt", [path for path, _ in client.calls])

    def test_first_pass_cannot_hide_refinement_in_same_graph(self):
        graph = copy.deepcopy(self.workflow)
        graph["1"] = {"class_type": "SamplerCustom", "inputs": {}}
        graph["2"] = {"class_type": "SamplerCustom", "inputs": {}}
        schema = {node["class_type"]: {"input": {"required": {}}} for node in graph.values()}
        with self.assertRaisesRegex(ValueError, "hide an unreviewed"):
            runner.validate_graph(graph, schema, self.outputs, "first-pass")

    def test_private_sources_cannot_be_read(self):
        self.source_manifest["sources"][0]["path"] = ".secrets/source.png"
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, "Private/internal"):
            self.run_stage()
        self.assertEqual(len(self.ledger()), 1)

    def test_failed_execution_preserves_history_and_returned_native_outputs(self):
        history = copy.deepcopy(self.history)
        history["status"]["status_str"] = "error"
        with self.assertRaisesRegex(ValueError, "execution failed"):
            self.run_stage(FakeClient(history))
        self.assertEqual(runner.read_json(self.packet / "attempt-1/history.json")["status"]["status_str"], "error")
        self.assertTrue((self.packet / "attempt-1/native_frames/0000.png").is_file())

    def test_wrong_dimensions_preserve_failed_native_bytes(self):
        self.outputs["images"][0]["canvas"] = [16, 16]
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, "canvas mismatch"):
            self.run_stage()
        self.assertTrue((self.packet / "attempt-1/native_frames/0000.png").is_file())
        self.assertEqual(self.receipt()["status"], "EXECUTION_FAIL")

    def test_comfy_output_path_escape_is_rejected(self):
        self.history["outputs"]["42"]["images"][0]["subfolder"] = "../../.secrets"
        with self.assertRaisesRegex(ValueError, "escapes"):
            self.run_stage()

    def test_refine_requires_hash_bound_first_pass_review(self):
        client = FakeClient(self.history)
        with self.assertRaisesRegex(ValueError, "explicit hash-bound"):
            self.run_stage(client, stage="refine")
        self.assertNotIn("/prompt", [path for path, _ in client.calls])
        self.assertEqual(len(self.ledger()), 1)

    def test_refine_stale_frame_review_is_rejected(self):
        review, path = self.review()
        (self.packet / "reviewed_0.png").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "changed pinned"):
            self.run_stage(stage="refine", review=path)

    def test_refine_stale_input_review_is_rejected(self):
        review, path = self.review()
        review["inputs"] = []
        runner.write_json(self.packet / "review.json", review)
        with self.assertRaisesRegex(ValueError, "stale/incomplete"):
            self.run_stage(stage="refine", review=path)

    def test_refine_failed_or_incomplete_topology_cannot_be_promoted(self):
        review, path = self.review()
        review["checks"]["topology"] = "FAIL"
        runner.write_json(self.packet / "review.json", review)
        with self.assertRaisesRegex(ValueError, "did not pass"):
            self.run_stage(stage="refine", review=path)

    def test_refine_model_observation_is_never_human_acceptance(self):
        review, path = self.review()
        review["human_accepted"] = True
        runner.write_json(self.packet / "review.json", review)
        with self.assertRaisesRegex(ValueError, "cannot grant"):
            self.run_stage(stage="refine", review=path)

    def test_valid_refine_review_is_recorded_without_acceptance(self):
        review, path = self.review()
        receipt = self.run_stage(stage="refine", review=path)
        self.assertEqual(receipt["status"], "EXECUTION_PASS")
        self.assertEqual(receipt["first_pass_review"]["scope"], "pre_refine_gate_only")
        self.assertFalse(any(receipt["acceptance"].values()))

    def test_atomic_metadata_is_utf8_lf_and_concurrent_lock_refuses(self):
        path = self.packet / "text.json"
        runner.write_json(path, {"name": "Roshan ☀"})
        self.assertNotIn(b"\r", path.read_bytes())
        self.assertEqual(runner.read_json(path)["name"], "Roshan ☀")
        lock = self.packet / "job.json.lock"
        lock.write_bytes(b"")
        with self.assertRaisesRegex(ValueError, "concurrent"):
            self.run_stage()


if __name__ == "__main__":
    unittest.main()
