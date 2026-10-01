from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import content_build as compiler
from tools import content_source_refs as source_refs


ROOT = Path(__file__).resolve().parents[2]


class ContentBuildTests(unittest.TestCase):
	"""Contract mutations run over snapshots, never over the project's assets."""

	@classmethod
	def setUpClass(cls):
		cls.snapshot = compiler.load_catalog(ROOT)

	def catalog(self):
		return copy.deepcopy(self.snapshot)

	def job(self, catalog, job_id="teacher"):
		return next(job for job in catalog["jobs"] if job["id"] == job_id)

	def assert_code(self, catalog, code):
		issues = compiler.validate(ROOT, catalog)
		self.assertTrue(any(issue.startswith(code) for issue in issues), issues)
		return issues

	def test_shipping_snapshot_validates(self):
		self.assertEqual([], compiler.validate(ROOT, self.catalog()))

	def test_all_registered_jobs_and_tombstones_are_preserved(self):
		catalog = self.catalog()
		live = {entry["id"] for entry in catalog["ledger"]["entries"] if entry["status"] == "LIVE"}
		self.assertEqual(live, {job["id"] for job in catalog["jobs"] if job["status"] == "LIVE"})
		self.assertEqual({4, 9, 14}, {entry["star_bit"] for entry in catalog["ledger"]["entries"] if entry["status"] == "TOMBSTONE"})

	def test_unregistered_shipping_act_fails(self):
		catalog = self.catalog()
		catalog["jobs"] = [job for job in catalog["jobs"] if job["id"] != "teacher"]
		self.assert_code(catalog, "E02")

	def test_reused_tombstone_bit_fails(self):
		catalog = self.catalog()
		self.job(catalog)["star_bit"] = 4
		self.assert_code(catalog, "E02")

	def test_too_low_star_ceiling_fails(self):
		catalog = self.catalog()
		catalog["ledger"]["star_namespace"]["derived_ceiling"] = (1 << 17) - 1
		self.assert_code(catalog, "E10")

	def test_missing_exact_voice_key_fails(self):
		catalog = self.catalog()
		self.job(catalog)["voice"]["required_keys"].append("__jp0_missing_voice__")
		self.assert_code(catalog, "E05")

	def test_missing_costume_sheet_fails(self):
		catalog = self.catalog()
		self.job(catalog)["art"]["costume_sheet"] = "res://assets/opera/__jp0_missing_sheet__.png"
		self.assert_code(catalog, "E07")

	def test_no_trusted_probe_fails(self):
		for probes in ([], ["scripts/probe_untrusted_jp0.gd"]):
			with self.subTest(probes=probes):
				catalog = self.catalog()
				self.job(catalog)["probes"] = probes
				self.assert_code(catalog, "E13")

	def test_ledger_entry_removal_reorder_and_repoint_fail(self):
		for mutation in ("remove", "reorder", "id", "bit", "status", "aliases"):
			with self.subTest(mutation=mutation):
				catalog = self.catalog()
				entries = catalog["ledger"]["entries"]
				if mutation == "remove":
					entries.pop()
				elif mutation == "reorder":
					entries[0], entries[1] = entries[1], entries[0]
				elif mutation == "id":
					entries[0]["id"] = "repointed_chef"
				elif mutation == "bit":
					entries[0]["star_bit"] = 18
				elif mutation == "status":
					entries[4]["status"] = "LIVE"
					entries[4]["id"] = "revived_boss"
				else:
					entries[3]["aliases"] = ["repointed_candy"]
				self.assert_code(catalog, "E02")

	def test_duplicate_ids_aliases_and_cross_job_aliases_fail(self):
		for mutation in ("duplicate_id", "alias_is_id", "duplicate_alias"):
			with self.subTest(mutation=mutation):
				catalog = self.catalog()
				if mutation == "duplicate_id":
					self.job(catalog)["id"] = "chef"
				elif mutation == "alias_is_id":
					catalog["ledger"]["entries"][-1]["aliases"] = ["chef"]
				else:
					catalog["ledger"]["entries"][-1]["aliases"] = ["candy"]
				self.assert_code(catalog, "E01")

	def test_invalid_room_and_duplicate_room_order_fail(self):
		catalog = self.catalog()
		self.job(catalog)["home"]["room"] = "__jp0_missing_room__"
		self.assert_code(catalog, "E03")
		catalog = self.catalog()
		chef_home = self.job(catalog, "chef")["home"]
		candy_home = self.job(catalog, "candymaker")["home"]
		candy_home["room_order"] = chef_home["room_order"]
		self.assert_code(catalog, "E03")

	def test_invalid_phase_bounds_and_station_fail(self):
		for mutation in ("empty", "finale", "station"):
			with self.subTest(mutation=mutation):
				catalog = self.catalog()
				job = self.job(catalog)
				if mutation == "empty":
					job["phases"] = []
				elif mutation == "finale":
					job["finale_start"] = len(job["phases"])
				else:
					job["phases"][0]["station"] = "__jp0_missing_station__"
				self.assert_code(catalog, "E04")

	def test_missing_surface_and_design_document_fail(self):
		catalog = self.catalog()
		self.job(catalog)["surface"] = "res://scripts/__jp0_missing_surface__.gd"
		self.assert_code(catalog, "E08")
		catalog = self.catalog()
		self.job(catalog)["docs"] = ["design/__jp0_missing_doc__.md"]
		self.assert_code(catalog, "E14")

	def test_unknown_fields_and_invalid_nested_types_fail(self):
		for path, value in ((["schema"], "job_record/999"), (["unknown_field"], True),
				(["phases", 0, "goal"], "many"), (["home", "room_order"], True),
				(["voice", "required_keys"], "not_an_array"), (["capabilities"], ["unknown_capability"])):
			with self.subTest(path=path, value=value):
				catalog = self.catalog()
				container = self.job(catalog)
				for key in path[:-1]:
					container = container[key]
				container[path[-1]] = value
				self.assert_code(catalog, "E01")

	def test_nonfinite_and_bool_numeric_data_are_rejected(self):
		for value in (float("nan"), float("inf"), float("-inf"), True):
			with self.subTest(value=value):
				catalog = self.catalog()
				self.job(catalog)["phases"][0]["goal"] = value
				self.assert_code(catalog, "E01")

	def test_derived_masks_and_bounds_keep_sparse_bits(self):
		data = compiler.derive(self.catalog())
		self.assertEqual(0x3BDEF, data["ACTIVE_STAR_MASK"])
		self.assertEqual(0x4210, data["RETIRED_STAR_MASK"])
		self.assertEqual(15, data["ACTIVE_ACT_COUNT"])
		self.assertEqual(18, data["SLOT_COUNT"])
		self.assertEqual(0x3FFFF, data["STAR_CEILING"])
		self.assertEqual(61, data["SHIPPING_PHASE_TOTAL"])
		self.assertEqual(0x2C4F, data["PARTY_MASK"])
		self.assertEqual(0, data["ACTIVE_STAR_MASK"] & data["RETIRED_STAR_MASK"])

	def test_render_is_byte_deterministic_and_canonicalizes_job_order(self):
		original = self.catalog()
		reversed_catalog = self.catalog()
		reversed_catalog["jobs"].reverse()
		expected = compiler.render(original).encode("utf-8")
		self.assertEqual(expected, compiler.render(original).encode("utf-8"))
		self.assertEqual(expected, compiler.render(reversed_catalog).encode("utf-8"))
		self.assertNotIn(b"\r", expected)
		self.assertTrue(expected.endswith(b"\n"))


	def test_every_compatibility_shape_retains_order_and_json_types(self):
		derived = compiler.derive(self.catalog())
		source = compiler.source_snapshot(ROOT)
		def equal_shape(expected, actual, path):
			self.assertIs(type(expected), type(actual), path)
			if isinstance(expected, dict):
				self.assertEqual(list(expected), list(actual), path)
				for key in expected:
					equal_shape(expected[key], actual[key], path + "." + str(key))
			elif isinstance(expected, list):
				self.assertEqual(len(expected), len(actual), path)
				for index, value in enumerate(expected):
					equal_shape(value, actual[index], path + "[%d]" % index)
			else:
				self.assertEqual(expected, actual, path)
		for name, value in source.items():
			with self.subTest(constant=name):
				self.assertIn(name, derived)
				equal_shape(value, derived[name], name)

	def test_source_registry_change_fails_without_rewriting_any_file(self):
		source = compiler.source_snapshot(ROOT)
		source["ACTS"][0]["name"] = "unexpected registry drift"
		with mock.patch.object(compiler, "source_snapshot", return_value=source):
			self.assert_code(self.catalog(), "E16")

	def test_missing_music_cue_fails(self):
		catalog = self.catalog()
		self.job(catalog)["music"]["cue"] = "__jp0_missing_music__"
		self.assert_code(catalog, "E06")

	def test_costume_hash_mismatch_fails_even_for_deferred_atlas_jobs(self):
		for job_id in ("teacher", "geologist"):
			with self.subTest(job=job_id):
				catalog = self.catalog()
				self.job(catalog, job_id)["art"]["costume_sheet_sha256"] = "0" * 64
				self.assert_code(catalog, "E07")

	def test_stale_or_missing_generated_file_is_detected(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			generated = root / "scripts/generated/job_catalog_data.gd"
			generated.parent.mkdir(parents=True)
			with mock.patch.object(compiler, "load_catalog", return_value=self.catalog()), \
					mock.patch.object(compiler, "validate", return_value=[]):
				self.assertTrue(any(issue.startswith("E15") for issue in compiler.issues(root)))
				generated.write_bytes(compiler.render(self.catalog()).encode("utf-8"))
				self.assertEqual([], compiler.issues(root))
				generated.write_bytes(generated.read_bytes() + b"# stale hand edit\n")
				self.assertTrue(any(issue.startswith("E15") for issue in compiler.issues(root)))

	def test_write_produces_same_bytes_twice_and_check_passes(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			generated = root / "scripts/generated/job_catalog_data.gd"
			with mock.patch.object(compiler, "load_catalog", side_effect=lambda unused: self.catalog()), \
					mock.patch.object(compiler, "validate", return_value=[]):
				self.assertEqual([], compiler.write(root))
				first = generated.read_bytes()
				self.assertEqual([], compiler.write(root))
				self.assertEqual(first, generated.read_bytes())
				self.assertEqual([], compiler.issues(root))
				self.assertEqual(compiler.render(self.catalog()).encode("utf-8"), first)

	def test_failed_validation_preserves_previous_generated_bytes(self):
		catalog = self.catalog()
		self.job(catalog)["voice"]["required_keys"].append("__jp0_missing_voice__")
		failures = compiler.validate(ROOT, catalog)
		self.assertTrue(failures)
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			generated = root / "scripts/generated/job_catalog_data.gd"
			generated.parent.mkdir(parents=True)
			generated.write_bytes(b"previous valid output\n")
			with mock.patch.object(compiler, "load_catalog", return_value=catalog), \
					mock.patch.object(compiler, "validate", return_value=failures):
				self.assertTrue(compiler.write(root))
			self.assertEqual(b"previous valid output\n", generated.read_bytes())



	def test_synthetic_bit18_derives_a_distinct_bit_and_larger_ceiling(self):
		catalog = self.catalog()
		old = compiler.derive(catalog)
		entry = copy.deepcopy(catalog["ledger"]["entries"][-1])
		entry.update(id="synthetic_bit18", star_bit=18, aliases=[])
		catalog["ledger"]["entries"].append(entry)
		job = copy.deepcopy(self.job(catalog))
		job.update(id="synthetic_bit18", star_bit=18)
		catalog["jobs"].append(job)
		data = compiler.derive(catalog)
		self.assertEqual(19, data["SLOT_COUNT"])
		self.assertEqual(0x7FFFF, data["STAR_CEILING"])
		self.assertEqual(old["ACTIVE_STAR_MASK"] | (1 << 18), data["ACTIVE_STAR_MASK"])
		self.assertEqual(old["RETIRED_STAR_MASK"], data["RETIRED_STAR_MASK"])
		self.assertEqual(old["ACTIVE_ACT_COUNT"] + 1, data["ACTIVE_ACT_COUNT"])



	def test_asset_paths_cannot_escape_the_repository(self):
		for path in ("../outside.png", "res://../outside.png", "C:/outside.png", "/outside.png"):
			with self.subTest(path=path):
				catalog = self.catalog()
				self.job(catalog)["art"]["costume_sheet"] = path
				self.assert_code(catalog, "E07")



	def test_baseline_revision_is_pinned_and_missing_history_fails_closed(self):
		catalog = self.catalog()
		catalog["config"]["runtime_baseline"] = "0" * 40
		self.assert_code(catalog, "E02")
		for failure in (OSError("history unavailable"), ValueError("bad historical ledger")):
			with self.subTest(failure=type(failure).__name__):
				with mock.patch.object(compiler, "baseline_entries", side_effect=failure):
					self.assert_code(self.catalog(), "E02")

	def test_only_whitelisted_native_constructors_can_enter_generated_code(self):
		for value in ({"__call__": "OS.execute", "args": ["arbitrary"]},
				{"__call__": "load", "args": ["res://outside.gd"]},
				{"__call__": "Color.new", "args": []},
				{"__ident__": "OS"}, {"__raw__": "arbitrary code"}):
			with self.subTest(value=value):
				catalog = self.catalog()
				self.job(catalog)["presentation"]["colors"]["floor"] = value
				self.assert_code(catalog, "E01")



	def test_only_the_three_measured_jp4_coverage_gaps_are_deferred(self):
		self.assertEqual({
			"JP4_DEFERRED music_catalog:geologist",
			"JP4_DEFERRED atlas_gate:geologist",
			"JP4_DEFERRED atlas_gate:teacher",
		}, set(compiler.diagnostics(ROOT, self.catalog())))
		for area in ("music_catalog", "atlas_gate"):
			with self.subTest(area=area):
				catalog = self.catalog()
				catalog["config"]["deferred_jp4"][area].append("chef")
				self.assert_code(catalog, "E01")

	def test_new_music_or_atlas_coverage_drift_is_not_waived(self):
		original_read = Path.read_text
		for relative, token, code in (("tools/build_area_music.py", '"opera_chef"', "E06"),
				("tools/audit_opera_roshan_animation.py", '"chef"', "E07")):
			with self.subTest(source=relative):
				changed_path = ROOT / relative
				self.assertIn(token, changed_path.read_text(encoding="utf-8"))
				def changed_read(path, *args, **kwargs):
					body = original_read(path, *args, **kwargs)
					if path == changed_path:
						return body.replace(token, '"__jp0_omitted__"', 1)
					return body
				with mock.patch.object(Path, "read_text", changed_read):
					self.assert_code(self.catalog(), code)



	def test_loader_rejects_duplicate_json_keys_and_nonfinite_numbers(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			jobs = root / "content/jobs"
			jobs.mkdir(parents=True)
			(jobs / "_ledger.json").write_text(json.dumps(self.snapshot["ledger"]), encoding="utf-8")
			(root / "content/compatibility.json").write_text(json.dumps(self.snapshot["compatibility"]), encoding="utf-8")
			config_path = root / "content/catalog.json"
			config_path.write_text(json.dumps(self.snapshot["config"]), encoding="utf-8")
			record_path = jobs / "teacher.json"
			for invalid in ('{"id":"teacher","id":"renamed"}', '{"id":"teacher","goal":NaN}',
					'{"id":"teacher","goal":Infinity}', '{"id":"teacher","goal":-Infinity}'):
				with self.subTest(json=invalid):
					record_path.write_text(invalid, encoding="utf-8")
					with self.assertRaises(ValueError):
						compiler.load_catalog(root)



	def test_compatibility_manifest_cannot_remove_proof_or_inject_code(self):
		for field, value in (("generated", "INJECTED\nfunc injected(): pass"),
				("type", "Dictionary = arbitrary()"), ("path", "../outside.gd"),
				("source", "MISSING_CONSTANT"), ("field", "voice.required_keys"), ("kind", "unknown")):
			with self.subTest(field=field):
				catalog = self.catalog()
				catalog["compatibility"]["registries"][0][field] = value
				self.assert_code(catalog, "E01")
		for mutation in ("remove", "reorder", "schema"):
			with self.subTest(mutation=mutation):
				catalog = self.catalog()
				manifest = catalog["compatibility"]
				if mutation == "remove":
					manifest["registries"].pop()
				elif mutation == "reorder":
					manifest["registries"].reverse()
				else:
					manifest["schema"] = "job_compatibility/999"
				self.assert_code(catalog, "E01")

	def test_two_act_flag_agrees_with_enabled_registry_membership(self):
		for mutation in ("flag", "membership"):
			with self.subTest(mutation=mutation):
				catalog = self.catalog()
				job = self.job(catalog)
				self.assertFalse(job["two_act"])
				if mutation == "flag":
					job["two_act"] = True
				else:
					job["compat_order"]["PERFORMANCE_ENABLED"] = 0
				self.assert_code(catalog, "E01")

	def test_source_reader_rejects_trailing_expressions_and_calls(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "fixture.gd"
			for expression in ("1 + 2", "[] + []", "Color(1, 1, 1).lightened(0.2)", "load(\"res://outside.gd\")"):
				with self.subTest(expression=expression):
					path.write_text("const FIXTURE = " + expression + "\n", encoding="utf-8")
					with self.assertRaises(ValueError):
						compiler.read_const(path, "FIXTURE")
			path.write_text("const FIXTURE: Array = [1, Color(0.1, 0.2, 0.3)] # allowed comment\n", encoding="utf-8")
			self.assertEqual([1, {"__call__": "Color", "args": [0.1, 0.2, 0.3]}], compiler.read_const(path, "FIXTURE"))

	def test_native_constructor_arguments_and_dictionary_tags_are_validated(self):
		for value in ({"__call__": "Color", "args": []},
				{"__call__": "Color", "args": [0.1, True, 0.3]},
				{"__call__": "Vector2i", "args": [1.5, 2]},
				{"__call__": "Vector2", "args": [1]},
				{"__dict__": [[1, "a"], [1, "b"]]}, {"__dict__": [[1]]}):
			with self.subTest(value=value):
				catalog = self.catalog()
				self.job(catalog)["presentation"]["colors"]["floor"] = value
				self.assert_code(catalog, "E01")



	def test_allocation_history_evidence_cannot_be_missing_or_fabricated(self):
		for field, replacement in (("allocated", None), ("observed_commit", ""),
				("observed_commit", "0" * 40), ("observed_date", ""),
				("observed_date", "2000-01-01"), ("first_declaration_commit", "0" * 40),
				("first_declaration_date", "2000-01-01"), ("source", "scripts/opera_house.gd:ACTS[18]")):
			with self.subTest(field=field, value=replacement):
				catalog = self.catalog()
				entry = catalog["ledger"]["entries"][0]
				if field == "allocated":
					entry.pop("allocated")
				else:
					entry["allocated"][field] = replacement
				self.assert_code(catalog, "E02")

	def test_packed_native_arrays_reject_bad_element_types_and_bounds(self):
		for constructor, elements in (("PackedStringArray", [1]),
				("PackedInt32Array", [True]), ("PackedInt32Array", [1.5]),
				("PackedInt32Array", [1 << 31]), ("PackedInt32Array", [-(1 << 31) - 1]),
				("PackedFloat32Array", ["1"]), ("PackedFloat32Array", [True]),
				("PackedFloat32Array", [float("nan")]), ("PackedFloat32Array", [float("inf")])):
			with self.subTest(constructor=constructor, elements=elements):
				catalog = self.catalog()
				self.job(catalog)["presentation"]["colors"]["floor"] = {"__call__": constructor, "args": [elements]}
				self.assert_code(catalog, "E01")




	def test_save_resolver_preserves_exact_registration_and_normalization_order(self):
		data = compiler.derive(self.catalog())
		self.assertEqual(["teacher", "geologist"], data["SAVE_CHECKPOINT_JOB_ORDER"])
		self.assertEqual(["teacher_lesson_checkpoint"], data["SAVE_CHECKPOINT_KEY_LISTS"]["DICTIONARY_KEYS"])
		self.assertEqual(["opera_geology_checkpoint"], data["SAVE_CHECKPOINT_KEY_LISTS"]["KNOWN_KEYS"])
		baseline = source_refs._baseline_save(str(ROOT.resolve()), compiler.BASELINE)
		for name in source_refs.REGISTRATION_LISTS:
			with self.subTest(name=name):
				self.assertEqual(baseline[1][name], source_refs.read_save_const(ROOT, name, data, compiler.BASELINE))
		self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], source_refs.read_checkpoint_order(ROOT, data))

	def save_source_fixture(self, directory, source):
		root = Path(directory)
		path = root / source_refs.SAVE_PATH
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(source, encoding="utf-8")
		return root

	def test_save_resolver_rejects_malformed_preload_and_scalar_expressions(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		mutations = [
			('preload("res://scripts/generated/job_catalog_data.gd")', 'load("res://scripts/generated/job_catalog_data.gd")'),
			('preload("res://scripts/generated/job_catalog_data.gd")', 'preload("res://scripts/other.gd")'),
			('const JobData :=', 'const OtherData :='),
			('const JobData :=', 'const JobData := preload("res://scripts/generated/job_catalog_data.gd")\nconst JobData :='),
			('const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK', 'const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK + 1'),
			('const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK', 'const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_ACT_COUNT'),
			('const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK', 'const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK.call()'),
		]
		with tempfile.TemporaryDirectory() as directory:
			for old, new in mutations:
				with self.subTest(replacement=new):
					self.assertIn(old, original)
					root = self.save_source_fixture(directory, original.replace(old, new, 1))
					with self.assertRaises(ValueError):
						source_refs.read_save_const(root, "OPERA_ACTIVE_STAR_MASK", data, compiler.BASELINE)
			with self.assertRaises(ValueError):
				source_refs.read_save_const(ROOT, "SCHEMA_VERSION", data, compiler.BASELINE)

	def test_save_resolver_rejects_registration_fragment_and_slot_drift(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		baseline = source_refs._baseline_save(str(ROOT.resolve()), compiler.BASELINE)
		mutations = [
			('"teacher_learning_progress",\n] +', '"teacher_learning_progress", "extra_prefix",\n] +'),
			('"opera_mastery", "opera_performance_checkpoints",', '"opera_performance_checkpoints", "opera_mastery",'),
			('JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"]', 'JobData.SAVE_CHECKPOINT_KEY_LISTS["KNOWN_KEYS"]'),
			('JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"]', 'JobData.SAVE_CHECKPOINT_KEY_LISTS.get("DICTIONARY_KEYS")'),
			('] + JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"] + [', '] + JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"] + [] + ['),
		]
		with tempfile.TemporaryDirectory() as directory, mock.patch.object(source_refs, "_baseline_save", return_value=baseline):
			for old, new in mutations:
				with self.subTest(replacement=new):
					self.assertIn(old, original)
					root = self.save_source_fixture(directory, original.replace(old, new, 1))
					with self.assertRaises(ValueError):
						source_refs.read_save_const(root, "DICTIONARY_KEYS", data, compiler.BASELINE)
			collision = copy.deepcopy(data)
			collision["SAVE_CHECKPOINT_KEY_LISTS"]["DICTIONARY_KEYS"].append("won")
			root = self.save_source_fixture(directory, original)
			with self.assertRaises(ValueError):
				source_refs.read_save_const(root, "DICTIONARY_KEYS", collision, compiler.BASELINE)

	def test_save_resolver_rejects_range_and_clamp_expressions_or_missing_bounds(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		mutations = [
			('range(JobData.SLOT_COUNT)', 'range(JobData.SLOT_COUNT + 1)'),
			('range(JobData.SLOT_COUNT)', 'range(JobData.ACTIVE_ACT_COUNT)'),
			('JobData.STAR_CEILING)', 'JobData.STAR_CEILING + 1)'),
			('JobData.STAR_CEILING)', 'JobData.ACTIVE_STAR_MASK)'),
			('JobData.STAR_CEILING)', '262142)'),
			('m.opera_stars = clampi(m.opera_stars, 0, JobData.STAR_CEILING)', 'm.opera_stars = m.opera_stars'),
		]
		with tempfile.TemporaryDirectory() as directory:
			for old, new in mutations:
				with self.subTest(replacement=new):
					self.assertIn(old, original)
					root = self.save_source_fixture(directory, original.replace(old, new, 1))
					with self.assertRaises(ValueError):
						source_refs.read_save_bounds(root, data)

	def test_save_resolver_rejects_normalization_loop_tampering(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		mutations = [
			('in JobData.SAVE_CHECKPOINT_JOB_ORDER:', 'in JobData.SAVE_CHECKPOINTS:'),
			('String(checkpoint_spec["key"])', 'String(checkpoint_spec["other"])'),
			('_normalise_job_checkpoint(raw, checkpoint_job_id)', '_normalise_job_checkpoint(raw, "teacher")'),
			('func _normalise_save(', 'func _normalise_save_unused('),
			('\tfor checkpoint_job_id: String in JobData.SAVE_CHECKPOINT_JOB_ORDER:', '\tdata["teacher_lesson_checkpoint"] = _teacher_lesson_checkpoint_or_default(raw)\n\tfor checkpoint_job_id: String in JobData.SAVE_CHECKPOINT_JOB_ORDER:'),
		]
		with tempfile.TemporaryDirectory() as directory:
			for old, new in mutations:
				with self.subTest(replacement=new):
					self.assertIn(old, original)
					root = self.save_source_fixture(directory, original.replace(old, new, 1))
					with self.assertRaises(ValueError):
						source_refs.read_checkpoint_order(root, data)

	def test_checkpoint_legacy_order_is_immutable(self):
		for prefix in (["geologist", "teacher"], ["teacher"], ["teacher", "geologist", "teacher"]):
			with self.subTest(prefix=prefix):
				catalog = self.catalog()
				catalog["config"]["save_checkpoint_normalization_prefix"] = prefix
				self.assert_code(catalog, "E09")

	def test_future_checkpoint_jobs_append_automatically_by_stable_bit(self):
		catalog = self.catalog()
		for bit, job_id in ((19, "future_b"), (18, "future_a")):
			entry = copy.deepcopy(catalog["ledger"]["entries"][-1])
			entry.update(id=job_id, star_bit=bit, aliases=[])
			catalog["ledger"]["entries"].append(entry)
			job = copy.deepcopy(self.job(catalog))
			job.update(id=job_id, star_bit=bit)
			job["phases"] = [copy.deepcopy(job["phases"][0]) for _ in range(7)]
			job["save"]["checkpoint"] = {"key": job_id + "_checkpoint", "schema_version": 2, "registration_lists": ["DICTIONARY_KEYS", "KNOWN_KEYS"]}
			catalog["jobs"].append(job)
		data = compiler.derive(catalog)
		self.assertEqual(["teacher", "geologist", "future_a", "future_b"], data["SAVE_CHECKPOINT_JOB_ORDER"])
		self.assertEqual(["teacher_lesson_checkpoint", "future_a_checkpoint", "future_b_checkpoint"], data["SAVE_CHECKPOINT_KEY_LISTS"]["DICTIONARY_KEYS"])
		self.assertEqual(["opera_geology_checkpoint", "future_a_checkpoint", "future_b_checkpoint"], data["SAVE_CHECKPOINT_KEY_LISTS"]["KNOWN_KEYS"])
		self.assertEqual(7, data["SAVE_CHECKPOINTS"]["future_a"]["phase_index_max"])
		self.assertEqual(2, data["SAVE_CHECKPOINTS"]["future_a"]["schema_version"])
		catalog["jobs"].reverse()
		self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], compiler.derive(catalog)["SAVE_CHECKPOINT_JOB_ORDER"])
		self.assertEqual({"SLOT_COUNT": 20, "STAR_CEILING": (1 << 20) - 1}, source_refs.read_save_bounds(ROOT, data))

	def test_source_snapshot_derives_fresh_data_without_reading_generated_output(self):
		catalog = self.catalog()
		data = compiler.derive(catalog)
		generated = (ROOT / compiler.GENERATED).resolve()
		read_text = Path.read_text
		read_bytes = Path.read_bytes
		def guarded_text(path, *args, **kwargs):
			self.assertNotEqual(generated, path.resolve(), "source proof must not trust generated output")
			return read_text(path, *args, **kwargs)
		def guarded_bytes(path, *args, **kwargs):
			self.assertNotEqual(generated, path.resolve(), "source proof must not trust generated output")
			return read_bytes(path, *args, **kwargs)
		with mock.patch.object(Path, "read_text", guarded_text), mock.patch.object(Path, "read_bytes", guarded_bytes):
			source = compiler.source_snapshot(ROOT, catalog)
		self.assertEqual(data["OPERA_ACTIVE_STAR_MASK"], source["OPERA_ACTIVE_STAR_MASK"])
		self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], source["SAVE_CHECKPOINT_JOB_ORDER"])
		catalog["ledger"]["entries"].append({"id": "fresh_derivation_test", "status": "LIVE", "star_bit": 18, "aliases": []})
		job = copy.deepcopy(self.job(catalog))
		job.update(id="fresh_derivation_test", star_bit=18)
		job["save"]["checkpoint"]["key"] = "fresh_derivation_checkpoint"
		catalog["jobs"].append(job)
		with mock.patch.object(Path, "read_text", guarded_text), mock.patch.object(Path, "read_bytes", guarded_bytes):
			changed = compiler.source_snapshot(ROOT, catalog)
		self.assertEqual(19, changed["SLOT_COUNT"])
		self.assertEqual(0x7FFFF, changed["STAR_CEILING"])
		self.assertEqual(source["STAR_CEILING"], data["STAR_CEILING"])



	def test_save_bound_proof_cannot_be_relocated_to_unrelated_scope(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		loop = "for bit_index in range(JobData.SLOT_COUNT):"
		load_clamp = 'm.opera_stars = clampi(int(m.save_data.get("opera_stars", 0)), 0, JobData.STAR_CEILING)'
		mutations = [
			original.replace(loop, "for unrelated_index in range(JobData.SLOT_COUNT):", 1) + "\nfunc _bound_decoy() -> void:\n\t" + loop + "\n\t\tpass\n",
			original.replace(load_clamp, "m.opera_stars = 0", 1) + "\nfunc _bound_decoy() -> void:\n\t" + load_clamp + "\n",
			original.replace('func load_save() -> void:', 'func unrelated_load_save() -> void:', 1),
			original.replace("\t" + load_clamp, "\tif false:\n\t\t" + load_clamp, 1),
			original.replace("\t" + load_clamp, "\t" + load_clamp + "\n\t" + load_clamp, 1),
			original.replace("\t" + loop, "\tif false:\n\t\t" + loop, 1),
			original.replace("\t" + loop, "\t" + loop + "\n\t\tpass\n\t" + loop, 1),
			original + "\nfunc _extra_unrelated_loop() -> void:\n\t" + loop + "\n\t\tpass\n",
			original + "\nfunc _extra_unrelated_clamp() -> void:\n\t" + load_clamp + "\n",
		]
		with tempfile.TemporaryDirectory() as directory:
			for index, source in enumerate(mutations):
				with self.subTest(mutation=index):
					root = self.save_source_fixture(directory, source)
					with self.assertRaises(ValueError):
						source_refs.read_save_bounds(root, data)

	def test_save_normalization_loop_must_be_unconditional_at_legacy_insertion_site(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		block = "\n".join("\t" + line if index == 0 else "\t\t" + line for index, line in enumerate(source_refs.NORMALIZATION_LOOP))
		self.assertIn(block, original)
		conditional = "\tif false:\n" + "\n".join("\t" + line for line in block.splitlines())
		sticker_line = '\tdata["stickers"] = _dictionary_or_default(raw, "stickers")'
		moved = original.replace(block + "\n", "", 1).replace(sticker_line, sticker_line + "\n" + block, 1)
		mutations = [original.replace(block, conditional, 1), moved, original.replace(block, block + "\n" + block, 1)]
		with tempfile.TemporaryDirectory() as directory:
			for index, source in enumerate(mutations):
				with self.subTest(mutation=index):
					root = self.save_source_fixture(directory, source)
					with self.assertRaises(ValueError):
						source_refs.read_checkpoint_order(root, data)

	def test_save_source_proof_ignores_comment_and_string_decoys(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		decoys = '\n# for bit_index in range(1):\n# clampi(opera_stars, 0, 1)\nconst UNUSED_DECOY = "clampi(opera_stars, 0, 2)"\n'
		with tempfile.TemporaryDirectory() as directory:
			root = self.save_source_fixture(directory, original + decoys)
			self.assertEqual({"SLOT_COUNT": 18, "STAR_CEILING": 0x3FFFF}, source_refs.read_save_bounds(root, data))
			self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], source_refs.read_checkpoint_order(root, data))



	def test_legacy_literal_checkpoint_proof_requires_exact_unconditional_order_and_site(self):
		data = compiler.derive(self.catalog())
		original = source_refs._baseline_save(str(ROOT.resolve()), compiler.BASELINE)[0]
		teacher = '\tdata["teacher_lesson_checkpoint"] = _teacher_lesson_checkpoint_or_default(raw)'
		geologist = '\tdata["opera_geology_checkpoint"] = _opera_geology_checkpoint_or_default(raw)'
		block = teacher + "\n" + geologist
		sticker_line = '\tdata["stickers"] = _dictionary_or_default(raw, "stickers")'
		self.assertIn(block, original)
		mutations = [
			original.replace(teacher, "\tif false:\n\t" + teacher, 1),
			original.replace(block, geologist + "\n" + teacher, 1),
			original.replace(block + "\n", "", 1).replace(sticker_line, sticker_line + "\n" + block, 1),
			original.replace('_teacher_lesson_checkpoint_or_default(raw)', '_opera_geology_checkpoint_or_default(raw)', 1),
			original.replace(block, teacher + "\n" + block, 1),
		]
		with tempfile.TemporaryDirectory() as directory:
			root = self.save_source_fixture(directory, original)
			self.assertEqual(["teacher", "geologist"], source_refs.read_checkpoint_order(root, data))
			self.assertEqual(["teacher", "geologist"], source_refs.read_checkpoint_order(ROOT, data))
			for index, source in enumerate(mutations):
				with self.subTest(mutation=index):
					root = self.save_source_fixture(directory, source)
					with self.assertRaises(ValueError):
						source_refs.read_checkpoint_order(root, data)



	def test_save_source_proof_ignores_quoted_code_and_rejects_lexical_spoofs(self):
		data = compiler.derive(self.catalog())
		original = (ROOT / source_refs.SAVE_PATH).read_text(encoding="utf-8")
		preload = 'const JobData := preload("res://scripts/generated/job_catalog_data.gd")'
		scalar = 'const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK'
		clamp = 'm.opera_stars = clampi(int(m.save_data.get("opera_stars", 0)), 0, JobData.STAR_CEILING)'
		start = original.index('func _normalise_save(')
		end = original.index('\nfunc ', start + 1)
		normalizer = original[start:end]
		def scalar_reader(root):
			return source_refs.read_save_const(root, "OPERA_ACTIVE_STAR_MASK", data, compiler.BASELINE)
		readers = [(preload, scalar_reader), (scalar, scalar_reader), (normalizer, lambda root: source_refs.read_checkpoint_order(root, data)), (clamp, lambda root: source_refs.read_save_bounds(root, data))]
		with tempfile.TemporaryDirectory() as directory:
			duplicated_function = self.save_source_fixture(directory, original + "\n" + normalizer)
			with self.assertRaises(ValueError):
				source_refs.read_checkpoint_order(duplicated_function, data)
			for delimiter in ('"' * 3, "'" * 3):
				for index, (real_code, reader) in enumerate(readers):
					with self.subTest(delimiter=delimiter, spoof=index):
						quoted = 'const UNUSED_SPOOF = ' + delimiter + "\n" + real_code + "\n" + delimiter if index != 3 else '\tvar unused_spoof = ' + delimiter + "\n\t" + real_code + "\n" + delimiter
						# The clamp's original tab is outside the replaced substring.
						if index == 3:
							quoted = quoted[1:]
						source = original.replace(real_code, quoted, 1)
						root = self.save_source_fixture(directory, source)
						with self.assertRaises(ValueError):
							reader(root)
				decoy = '\nconst UNUSED_LEXICAL_DECOY = ' + delimiter + "\n" + preload + "\n" + scalar + "\nfunc _normalise_save(raw: Dictionary) -> Dictionary:\n\treturn {}\n" + delimiter + "\n"
				root = self.save_source_fixture(directory, original + decoy)
				self.assertEqual(data["ACTIVE_STAR_MASK"], scalar_reader(root))
				self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], source_refs.read_checkpoint_order(root, data))
				self.assertEqual({"SLOT_COUNT": 18, "STAR_CEILING": 0x3FFFF}, source_refs.read_save_bounds(root, data))
			for delimiter, prefix in (('"', ''), ("'", ''), ('"', '&'), ('"', '^'), ('"', 'r'), ("'", 'r')):
				with self.subTest(delimiter=delimiter, prefix=prefix):
					decoy = '\nconst UNUSED_PREFIX_DECOY = ' + prefix + delimiter + 'fake const JobData and func _normalise_save() and clampi(opera_stars, 0, 1) # quote' + delimiter + "\n"
					root = self.save_source_fixture(directory, original + decoy)
					self.assertEqual(data["ACTIVE_STAR_MASK"], scalar_reader(root))
					self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], source_refs.read_checkpoint_order(root, data))
					self.assertEqual({"SLOT_COUNT": 18, "STAR_CEILING": 0x3FFFF}, source_refs.read_save_bounds(root, data))
			# Quotes in comments and # inside literals must not alter lexical state.
			parity = '\n# comment containing unfinished quotes: " and single quote ' + "'" + '\nconst UNUSED_ESCAPES = "escaped quote: \\\" and escaped slash: \\\\ # inside"\n'
			root = self.save_source_fixture(directory, original + parity)
			self.assertEqual(data["ACTIVE_STAR_MASK"], scalar_reader(root))
			self.assertEqual(data["SAVE_CHECKPOINT_JOB_ORDER"], source_refs.read_checkpoint_order(root, data))
			for delimiter in ('"', "'", '"' * 3, "'" * 3):
				with self.subTest(unterminated=delimiter):
					root = self.save_source_fixture(directory, original + '\nconst UNTERMINATED = ' + delimiter + 'unterminated literal')
					with self.assertRaises(ValueError):
						scalar_reader(root)
		# Phase totals come from the actual commissioned _check producers.
		# A literal-looking prefix is insufficient when the RHS continues.
		catalog = self.catalog()
		original_read_text = Path.read_text
		def snapshot_with_probe(path, replacement):
			def reader(instance, *args, **kwargs):
				return replacement if instance == path else original_read_text(instance, *args, **kwargs)
			with mock.patch.object(Path, "read_text", reader):
				return compiler.source_snapshot(ROOT, catalog)
		for relative, comparator, value, exported in (
				("scripts/probe_chapter2.gd", "count", 29, "CHAPTER2_PHASE_TOTAL"),
				("scripts/probe_opera_2d.gd", "shipping_phase_count", 61, "SHIPPING_PHASE_TOTAL")):
			path = ROOT / relative
			probe = path.read_text(encoding="utf-8")
			expression = comparator + " == " + str(value)
			self.assertEqual(1, probe.count(expression))
			for suffix in (" + 1", ".0", "_0", "suffix"):
				with self.subTest(producer=relative, bad_rhs=suffix):
					with self.assertRaises(ValueError):
						snapshot_with_probe(path, probe.replace(expression, expression + suffix, 1))
			for delimiter in ('"' * 3, "'" * 3):
				with self.subTest(producer=relative, quoted_decoy=delimiter):
					decoy = "\nconst UNUSED_COUNT_DECOY = " + delimiter + "\n\t_check(\"fake producer\", " + expression + ")\n" + delimiter + "\n"
					self.assertEqual(value, snapshot_with_probe(path, probe + decoy)[exported])
			unrelated = "\nfunc _unrelated_count() -> void:\n\tvar other_count = 0\n\tvar ignored = other_count == " + str(value) + " + 1\n"
			self.assertEqual(value, snapshot_with_probe(path, probe + unrelated)[exported])


if __name__ == "__main__":
	unittest.main()
