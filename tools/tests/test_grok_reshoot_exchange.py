import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.grok_reshoot_exchange import (
	blob_hash,
	export_request,
	ingest_return,
	record_review,
	status,
	supersede,
)


class GrokReshootExchangeTests(unittest.TestCase):
	def test_return_rejects_signed_credential_and_fragment_urls(self):
		request = export_request(self.packet, "SHOT-A")
		for bad_url in (
			"https://example.invalid/clip.mp4?sig=temporary-token",
			"https://user:password@example.invalid/clip.mp4",
			"https://example.invalid/clip.mp4#token",
			"https:///clip.mp4",
		):
			with self.subTest(url=bad_url):
				payload = self._return_payload(request)
				payload["artifacts"][0]["source_url"] = bad_url
				incoming = self.packet / "bad-url.json"
				self._write_json(incoming, payload)
				with self.assertRaises(ValueError):
					ingest_return(self.packet, incoming)
				self.assertFalse((request.parent / "RETURN.json").exists())

	def test_career_phase_change_stales_its_scene_request(self):
		jobs = {
			"jobs": [{"id": "JOB-CHEF", "freeplay_phases": [{"action": "stir"}]}],
			"chapter2_variants": [{"id": "JOBVAR-C2-CHEF", "base_job_id": "JOB-CHEF", "event_id": "EV-A", "phases": [{"action": "frost"}]}],
		}
		self._write_json(self.packet / "JOBS.json", jobs)
		export_request(self.packet, "SHOT-A")
		jobs["chapter2_variants"][0]["phases"][0]["action"] = "place one strawberry"
		self._write_json(self.packet / "JOBS.json", jobs)
		self.assertEqual(status(self.packet)[0]["state"], "STALE")

	def setUp(self):
		self.tmp = tempfile.TemporaryDirectory()
		self.packet = Path(self.tmp.name)
		self.database = {
			"entities": [
				{"id": "CHAR-A", "reference_ids": ["REF-CHAR"]},
				{"id": "LOC-A", "reference_ids": ["REF-LOC"]},
				{"id": "PROP-A", "reference_ids": ["REF-PROP"]},
			],
			"events": [
				{
					"id": "EV-A",
					"prop_ids": ["PROP-A"],
					"before_state": "quiet room",
					"action": "Roshan reaches for the prop",
					"after_state": "prop is in Roshan's hand",
				}
			],
			"shots": [
				{
					"id": "SHOT-A",
					"event_id": "EV-A",
					"location_id": "LOC-A",
					"character_ids": ["CHAR-A"],
					"reference_pool_ids": [],
					"depends_on": [],
					"prompt": (
						"Locked camera. Roshan reaches for the prop.\n"
						"Sound: gentle room tone; no synthesized family voices.\n"
					),
				}
			],
			"references": [
				{"id": "REF-CHAR", "sha256": "1" * 64},
				{"id": "REF-LOC", "sha256": "2" * 64},
				{"id": "REF-PROP", "sha256": "3" * 64},
			],
		}
		self._write_json(self.packet / "DATABASE.json", self.database)
		self._write_json(
			self.packet / "CONFLICT_RESOLUTIONS.json",
			[{"id": "CONFLICT-A", "resolution": "Keep the room fixed."}],
		)
		self.media_path = self.packet / "reshoots" / "inbox" / "SHOT-A.mp4"
		self.media_path.parent.mkdir(parents=True)
		self.media_path.write_bytes(b"fixture motion-reference clip")

	def tearDown(self):
		self.tmp.cleanup()

	@staticmethod
	def _write_json(path, value):
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

	def _return_payload(self, request_path, attempt=None):
		request = json.loads(request_path.read_text(encoding="utf-8"))
		return {
			"shot_id": request["shot_id"],
			"attempt": request["attempt"] if attempt is None else attempt,
			"request_sha256": blob_hash(request_path),
			"generator": "fixture-generator",
			"generation_ready": False,
			"delivery_accepted": False,
			"artifacts": [
				{
					"role": "clip",
					"path": "reshoots/inbox/SHOT-A.mp4",
					"sha256": hashlib.sha256(self.media_path.read_bytes()).hexdigest(),
					"bytes": self.media_path.stat().st_size,
					"fps": 24,
					"frames": 24,
					"source_url": "https://example.invalid/SHOT-A.mp4",
				}
			],
		}

	def _ingest(self, request_path):
		payload = self._return_payload(request_path)
		incoming = self.packet / f"incoming-return-{payload['attempt']}.json"
		self._write_json(incoming, payload)
		return ingest_return(self.packet, incoming)

	def _review_payload(self, return_path, decision="REGENERATE"):
		returned = json.loads(return_path.read_text(encoding="utf-8"))
		artifact_sha = returned["artifacts"][0]["sha256"]
		issues = []
		if decision == "REGENERATE":
			issues = [
				{
					"category": "contact",
					"artifact_sha256": artifact_sha,
					"start_frame": 8,
					"end_frame_exclusive": 12,
					"observation": "The hand stops short of the prop.",
					"expected": "Visible fingertip contact before the prop moves.",
					"reconstruction": "Show fingertip contact, then move the prop.",
				}
			]
		return {
			"shot_id": "SHOT-A",
			"attempt": returned["attempt"],
			"return_sha256": blob_hash(return_path),
			"decision": decision,
			"reviewer": "fixture-reviewer",
			"delivery_accepted": False,
			"issues": issues,
		}

	def _record_regeneration(self, return_path):
		payload = self._review_payload(return_path)
		incoming = self.packet / f"incoming-review-{payload['attempt']}.json"
		self._write_json(incoming, payload)
		return record_review(self.packet, incoming)

	def test_round_trip_exports_ingests_reviews_and_requests_next_attempt(self):
		request_one = export_request(self.packet, "SHOT-A")
		returned_one = self._ingest(request_one)
		review_one = self._record_regeneration(returned_one)
		request_two = export_request(self.packet, "SHOT-A")

		request = json.loads(request_two.read_text(encoding="utf-8"))
		self.assertEqual(request["attempt"], 2)
		self.assertEqual(request["parent_review_sha256"], blob_hash(review_one))
		self.assertIn("Show fingertip contact, then move the prop.", request["prompt"])
		self.assertFalse(request["generation_ready"])
		self.assertFalse(request["delivery_accepted"])
		self.assertEqual(status(self.packet)[0]["state"], "AWAITING_RETURN")

	def test_changed_source_makes_open_request_stale(self):
		request = export_request(self.packet, "SHOT-A")
		self.database["shots"][0]["prompt"] = "Changed authoritative prompt."
		self._write_json(self.packet / "DATABASE.json", self.database)
		incoming = self.packet / "stale-return.json"
		self._write_json(incoming, self._return_payload(request))

		with self.assertRaisesRegex(ValueError, "STALE"):
			ingest_return(self.packet, incoming)
		self.assertEqual(status(self.packet)[0]["state"], "STALE")

	def test_superseded_stale_request_can_recover_with_next_attempt(self):
		request_one = export_request(self.packet, "SHOT-A")
		self.database["shots"][0]["prompt"] = (
			"Changed authoritative prompt.\n"
			"Sound: gentle room tone; no synthesized family voices.\n"
		)
		self._write_json(self.packet / "DATABASE.json", self.database)

		superseded = supersede(self.packet, "SHOT-A", 1)
		request_two = export_request(self.packet, "SHOT-A")
		payload = json.loads(request_two.read_text(encoding="utf-8"))

		self.assertTrue(superseded.is_file())
		self.assertEqual(payload["attempt"], 2)
		self.assertEqual(payload["supersedes_request_sha256"], blob_hash(request_one))
		self.assertIsNone(payload["parent_review_sha256"])
		self.assertIn("Changed authoritative prompt.", payload["prompt"])
		self._ingest(request_two)
		self.assertEqual(status(self.packet)[0]["state"], "AWAITING_QC")

	def test_forged_superseded_marker_cannot_bypass_review_gate(self):
		export_request(self.packet, "SHOT-A")
		marker = self.packet / "reshoots/attempts/SHOT-A/A001/SUPERSEDED.json"
		self._write_json(
			marker,
			{
				"reason": "SOURCE_CONTRACT_CHANGED",
				"request_sha256": "0" * 64,
				"old_contract_sha256": "1" * 64,
				"new_contract_sha256": "2" * 64,
				"generation_ready": False,
				"delivery_accepted": False,
			},
		)

		with self.assertRaises(ValueError):
			export_request(self.packet, "SHOT-A")

	def test_mismatched_superseded_marker_cannot_unlock_stale_request(self):
		request = export_request(self.packet, "SHOT-A")
		request_payload = json.loads(request.read_text(encoding="utf-8"))
		self.database["shots"][0]["prompt"] = "Changed authoritative prompt."
		self._write_json(self.packet / "DATABASE.json", self.database)
		marker = self.packet / "reshoots/attempts/SHOT-A/A001/SUPERSEDED.json"
		self._write_json(
			marker,
			{
				"reason": "SOURCE_CONTRACT_CHANGED",
				"request_sha256": "0" * 64,
				"old_contract_sha256": request_payload["contract_sha256"],
				"new_contract_sha256": "f" * 64,
				"generation_ready": False,
				"delivery_accepted": False,
			},
		)

		with self.assertRaises(ValueError):
			export_request(self.packet, "SHOT-A")

	def test_changed_returned_media_is_rejected_before_qc_is_recorded(self):
		request = export_request(self.packet, "SHOT-A")
		returned = self._ingest(request)
		review = self._review_payload(returned)
		incoming = self.packet / "changed-media-review.json"
		self._write_json(incoming, review)
		self.media_path.write_bytes(b"mutated after immutable return ingestion")

		with self.assertRaisesRegex(ValueError, "changed after ingest"):
			record_review(self.packet, incoming)
		self.assertFalse(
			(self.packet / "reshoots/attempts/SHOT-A/A001/REVIEW.json").exists()
		)

	def test_status_becomes_stale_when_reviewed_media_changes(self):
		request = export_request(self.packet, "SHOT-A")
		returned = self._ingest(request)
		self._record_regeneration(returned)
		self.assertEqual(status(self.packet)[0]["state"], "REGENERATE")

		self.media_path.write_bytes(b"mutated after QC was recorded")

		self.assertEqual(status(self.packet)[0]["state"], "STALE")

	def test_transitive_dependency_change_invalidates_successor_request(self):
		self.database["shots"].extend(
			[
				{
					"id": "SHOT-B",
					"event_id": "EV-A",
					"location_id": "LOC-A",
					"character_ids": ["CHAR-A"],
					"reference_pool_ids": [],
					"depends_on": ["SHOT-A"],
					"prompt": "Middle dependency.\nSound: gentle room tone.\n",
				},
				{
					"id": "SHOT-C",
					"event_id": "EV-A",
					"location_id": "LOC-A",
					"character_ids": ["CHAR-A"],
					"reference_pool_ids": [],
					"depends_on": ["SHOT-B"],
					"prompt": "Successor shot.\nSound: gentle room tone.\n",
				},
			]
		)
		self._write_json(self.packet / "DATABASE.json", self.database)
		request = export_request(self.packet, "SHOT-C")

		self.database["shots"][0]["prompt"] = "Changed transitive ancestor."
		self._write_json(self.packet / "DATABASE.json", self.database)
		incoming = self.packet / "transitive-stale-return.json"
		self._write_json(incoming, self._return_payload(request))

		with self.assertRaisesRegex(ValueError, "STALE"):
			ingest_return(self.packet, incoming)
		states = {row["shot_id"]: row["state"] for row in status(self.packet)}
		self.assertEqual(states["SHOT-C"], "STALE")

	def test_transitive_dependency_authority_changes_invalidate_descendants(self):
		ancestor_reference_path = self.packet / "references" / "ancestor.bin"
		ancestor_reference_path.parent.mkdir(parents=True)
		ancestor_reference_path.write_bytes(b"ancestor reference v1")
		self.database["entities"].extend(
			[
				{
					"id": "LOC-ANCESTOR",
					"reference_ids": [],
					"description": "ancestor-only location v1",
				},
				{"id": "CHAR-REFERENCE", "reference_ids": ["REF-ANCESTOR"]},
			]
		)
		self.database["events"].append(
			{
				"id": "EV-ANCESTOR",
				"prop_ids": [],
				"before_state": "ancestor event before",
				"action": "ancestor-only event v1",
				"after_state": "ancestor event after",
			}
		)
		self.database["references"].append(
			{
				"id": "REF-ANCESTOR",
				"path": "references/ancestor.bin",
				"sha256": blob_hash(ancestor_reference_path),
			}
		)

		def shot(shot_id, event_id="EV-A", location_id="LOC-A",
				character_id="CHAR-A", depends_on=None):
			return {
				"id": shot_id,
				"event_id": event_id,
				"location_id": location_id,
				"character_ids": [character_id],
				"reference_pool_ids": [],
				"depends_on": depends_on or [],
				"prompt": f"{shot_id} action.\nSound: gentle room tone.\n",
			}

		self.database["shots"].extend(
			[
				shot("SHOT-EVENT-A", event_id="EV-ANCESTOR"),
				shot("SHOT-EVENT-B", depends_on=["SHOT-EVENT-A"]),
				shot("SHOT-EVENT-C", depends_on=["SHOT-EVENT-B"]),
				shot("SHOT-ENTITY-A", location_id="LOC-ANCESTOR"),
				shot("SHOT-ENTITY-B", depends_on=["SHOT-ENTITY-A"]),
				shot("SHOT-ENTITY-C", depends_on=["SHOT-ENTITY-B"]),
				shot("SHOT-REFERENCE-A", character_id="CHAR-REFERENCE"),
				shot("SHOT-REFERENCE-B", depends_on=["SHOT-REFERENCE-A"]),
				shot("SHOT-REFERENCE-C", depends_on=["SHOT-REFERENCE-B"]),
			]
		)
		self._write_json(self.packet / "DATABASE.json", self.database)
		requests = {
			"event": export_request(self.packet, "SHOT-EVENT-C"),
			"entity": export_request(self.packet, "SHOT-ENTITY-C"),
			"reference": export_request(self.packet, "SHOT-REFERENCE-C"),
		}

		self.database["events"][-1]["action"] = "ancestor-only event v2"
		self.database["entities"][-2]["description"] = "ancestor-only location v2"
		ancestor_reference_path.write_bytes(b"ancestor reference v2")
		self.database["references"][-1]["sha256"] = blob_hash(ancestor_reference_path)
		self._write_json(self.packet / "DATABASE.json", self.database)

		for authority, request in requests.items():
			with self.subTest(authority=authority):
				incoming = self.packet / f"ancestor-{authority}-return.json"
				self._write_json(incoming, self._return_payload(request))
				with self.assertRaisesRegex(ValueError, "STALE"):
					ingest_return(self.packet, incoming)

	def test_changed_reference_bytes_block_export_even_when_metadata_is_unchanged(self):
		reference_path = self.packet / "references" / "character.bin"
		reference_path.parent.mkdir(parents=True)
		reference_path.write_bytes(b"approved character bytes")
		self.database["references"][0]["path"] = "references/character.bin"
		self.database["references"][0]["sha256"] = blob_hash(reference_path)
		self._write_json(self.packet / "DATABASE.json", self.database)
		reference_path.write_bytes(b"changed character bytes")

		with self.assertRaisesRegex(ValueError, "Reference media missing or hash changed"):
			export_request(self.packet, "SHOT-A")

	def test_returned_artifact_path_must_not_escape_or_use_nonportable_syntax(self):
		request = export_request(self.packet, "SHOT-A")
		for index, bad_path in enumerate(
			("../outside.mp4", "reshoots\\inbox\\SHOT-A.mp4", "C:/SHOT-A.mp4")
		):
			with self.subTest(path=bad_path):
				payload = self._return_payload(request)
				payload["artifacts"][0]["path"] = bad_path
				incoming = self.packet / f"bad-path-{index}.json"
				self._write_json(incoming, payload)
				with self.assertRaises(ValueError):
					ingest_return(self.packet, incoming)

	def test_duplicate_attempt_and_duplicate_return_are_rejected(self):
		request = export_request(self.packet, "SHOT-A")
		with self.assertRaisesRegex(ValueError, "Only reviewed regeneration"):
			export_request(self.packet, "SHOT-A")

		incoming = self.packet / "duplicate-return.json"
		self._write_json(incoming, self._return_payload(request))
		ingest_return(self.packet, incoming)
		with self.assertRaises(FileExistsError):
			ingest_return(self.packet, incoming)

	def test_mismatched_request_and_artifact_hashes_are_rejected(self):
		request = export_request(self.packet, "SHOT-A")
		bad_request = self._return_payload(request)
		bad_request["request_sha256"] = "0" * 64
		incoming = self.packet / "bad-request-hash.json"
		self._write_json(incoming, bad_request)
		with self.assertRaisesRegex(ValueError, "exact request"):
			ingest_return(self.packet, incoming)

		bad_artifact = self._return_payload(request)
		bad_artifact["artifacts"][0]["sha256"] = "0" * 64
		incoming = self.packet / "bad-artifact-hash.json"
		self._write_json(incoming, bad_artifact)
		with self.assertRaisesRegex(ValueError, "hash-mismatched"):
			ingest_return(self.packet, incoming)

	def test_generator_and_qc_cannot_set_acceptance_flags(self):
		request = export_request(self.packet, "SHOT-A")
		for field in ("generation_ready", "delivery_accepted"):
			with self.subTest(return_flag=field):
				payload = self._return_payload(request)
				payload[field] = True
				incoming = self.packet / f"false-return-approval-{field}.json"
				self._write_json(incoming, payload)
				with self.assertRaisesRegex(ValueError, "cannot grant approval"):
					ingest_return(self.packet, incoming)

		returned = self._ingest(request)
		review = self._review_payload(returned)
		review["delivery_accepted"] = True
		incoming = self.packet / "false-review-approval.json"
		self._write_json(incoming, review)
		with self.assertRaisesRegex(ValueError, "cannot be set here"):
			record_review(self.packet, incoming)

	def test_qc_finding_span_must_be_exact_and_inside_clip(self):
		request = export_request(self.packet, "SHOT-A")
		returned = self._ingest(request)
		base = self._review_payload(returned)
		bad_spans = [(-1, 1), (0, 0), (12, 8), (0, 25), ("0", 1)]
		for index, (start, end) in enumerate(bad_spans):
			with self.subTest(start=start, end=end):
				review = copy.deepcopy(base)
				review["issues"][0]["start_frame"] = start
				review["issues"][0]["end_frame_exclusive"] = end
				incoming = self.packet / f"bad-span-{index}.json"
				self._write_json(incoming, review)
				with self.assertRaisesRegex(ValueError, "Invalid exact finding span"):
					record_review(self.packet, incoming)

	def test_three_regenerations_reach_retry_cap(self):
		for expected_attempt in range(1, 4):
			request = export_request(self.packet, "SHOT-A")
			self.assertEqual(
				json.loads(request.read_text(encoding="utf-8"))["attempt"],
				expected_attempt,
			)
			returned = self._ingest(request)
			self._record_regeneration(returned)

		with self.assertRaisesRegex(ValueError, "Three-attempt cap reached"):
			export_request(self.packet, "SHOT-A")


if __name__ == "__main__":
	unittest.main()
