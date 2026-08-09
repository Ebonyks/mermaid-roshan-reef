from __future__ import annotations

import bz2
import gzip
import io
import json
import lzma
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import audit_game_2d as game_2d  # noqa: E402


class Game2DAuditTests(unittest.TestCase):
	def test_production_initial_ceiling_trust_anchor_is_pinned(self) -> None:
		self.assertEqual(
			game_2d.INITIAL_CEILING_SHA256,
			"2da7db0ed6a3b67c33165a988450d322013f58455d590d3b73783646d59be2e2",
		)

	def fixture(self, *, with_debt: bool = True) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
		temp = tempfile.TemporaryDirectory(prefix="test-game-2d-")
		root = Path(temp.name)
		manifest = game_2d._stress_fixture(root, with_debt=with_debt)
		return temp, root, manifest

	def read_manifest(self, path: Path) -> dict:
		return json.loads(path.read_text(encoding="utf-8"))

	def write_manifest(self, path: Path, document: dict) -> None:
		path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

	def finding_ids(self, result: game_2d.AuditResult) -> set[str]:
		return {finding.check_id for finding in result.findings}

	def test_exact_known_debt_is_unsatisfied_but_regression_safe(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		result = game_2d.audit(root, manifest)
		self.assertTrue(result.exact)
		self.assertFalse(result.satisfied)
		self.assertEqual(result.status, "UNSATISFIED")
		self.assertEqual(game_2d.exit_code(result, "default"), 0)
		self.assertEqual(game_2d.exit_code(result, "regression-gate"), 0)
		self.assertNotEqual(game_2d.exit_code(result, "strict"), 0)
		self.assertIn("NO_REGRESSION", game_2d.render(result, "regression-gate"))
		self.assertNotIn("PASS", game_2d.render(result, "regression-gate"))

	def test_true_empty_inventory_is_the_only_strict_success(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		result = game_2d.audit(root, manifest)
		self.assertTrue(result.satisfied)
		self.assertEqual(game_2d.exit_code(result, "strict"), 0)
		self.assertIn("STATUS| SATISFIED", game_2d.render(result, "strict"))

	def test_new_export_scope_model_fails_regression_gate(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		model = root / "new_world/prop.glb"
		model.parent.mkdir(parents=True)
		model.write_bytes(b"new")
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D101", self.finding_ids(result))
		self.assertNotEqual(game_2d.exit_code(result, "regression-gate"), 0)

	def test_numbered_blender_backup_is_repository_model_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		path = root / "tools/out/character.blend12"
		path.parent.mkdir(parents=True)
		path.write_bytes(b"blender backup")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.model_files, ("tools/out/character.blend12",))
		self.assertEqual(inventory.active_export_model_files, ())
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_orphan_model_import_sidecar_is_strict_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		path = root / "assets/orphan.glb.import"
		path.parent.mkdir(parents=True)
		path.write_text("[remap]\n", encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.model_files, ())
		self.assertEqual(inventory.model_import_sidecars, ("assets/orphan.glb.import",))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))
		game_2d._write_manifest(manifest, inventory)
		result = game_2d.audit(root, manifest)
		self.assertTrue(result.exact)
		self.assertNotEqual(game_2d.exit_code(result, "strict"), 0)

	def test_zip_hidden_models_are_fingerprinted_repository_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		path = root / "backups/source_assets.zip"
		path.parent.mkdir(parents=True)
		with zipfile.ZipFile(path, "w") as archive:
			archive.writestr("kit/hidden.glb", b"glTF model")
			archive.writestr("source/rig.blend1", b"BLENDER backup")
			archive.writestr("notes/readme.txt", b"notes")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.model_files, ())
		self.assertEqual(set(inventory.model_archive_files), {"backups/source_assets.zip"})
		evidence = inventory.model_archive_files["backups/source_assets.zip"]
		self.assertEqual(evidence["model_member_count"], 2)
		self.assertEqual(
			evidence["model_members"], ["kit/hidden.glb", "source/rig.blend1"])
		self.assertRegex(str(evidence["sha256"]), r"^[0-9a-f]{64}$")
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_zip_and_tar_sniff_disguised_models_and_mark_nested_archives(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		backup = root / "backups"
		backup.mkdir()
		nested_bytes = io.BytesIO()
		with zipfile.ZipFile(nested_bytes, "w") as nested:
			nested.writestr("hidden.glb", b"model")
		nested_tar_bytes = io.BytesIO()
		with tarfile.open(fileobj=nested_tar_bytes, mode="w:gz") as nested_tar:
			info = tarfile.TarInfo("hidden.glb")
			info.size = 5
			nested_tar.addfile(info, io.BytesIO(b"model"))
		sfx_bytes = io.BytesIO()
		with zipfile.ZipFile(sfx_bytes, "w") as sfx:
			sfx.writestr("hidden.glb", b"model")
		nested_self_extracting = (
			b"\x7fELF" + (b"stub" * (26 * 1024)) + sfx_bytes.getvalue())
		self_extracting = b"MZ" + (b"stub" * (20 * 1024)) + sfx_bytes.getvalue()
		zip_path = backup / "disguised.zip"
		with zipfile.ZipFile(zip_path, "w") as archive:
			archive.writestr("payload.bin", b"glTF\x02\x00\x00\x00")
			archive.writestr("nested.payload", nested_bytes.getvalue())
			archive.writestr("compressed.payload", nested_tar_bytes.getvalue())
			archive.writestr("self_extracting.payload", nested_self_extracting)
			archive.writestr("nested_7z.payload", game_2d.SEVEN_ZIP_MAGIC + b"opaque")
			archive.writestr("nested_rar.payload", game_2d.RAR_MAGICS[1] + b"opaque")
		tar_path = backup / "disguised.tar"
		payload = b"ply\r\nformat ascii 1.0\r\nend_header\r\n"
		with tarfile.open(tar_path, "w") as archive:
			info = tarfile.TarInfo("payload.cache")
			info.size = len(payload)
			archive.addfile(info, io.BytesIO(payload))
		with zipfile.ZipFile(backup / "zip.bundle", "w") as archive:
			archive.writestr("hidden.glb", b"model")
		with tarfile.open(backup / "tar.bundle", "w") as archive:
			info = tarfile.TarInfo("hidden.blend")
			info.size = 5
			archive.addfile(info, io.BytesIO(b"model"))
		with zipfile.ZipFile(backup / "clean.bundle", "w") as archive:
			archive.writestr("readme.txt", b"ordinary 2D notes")
		(backup / "self_extracting.bundle").write_bytes(self_extracting)
		(backup / "elf_self_extracting.bundle").write_bytes(
			b"\x7fELF" + (b"native-stub" * (7 * 1024)) + sfx_bytes.getvalue())
		clean_sfx_bytes = io.BytesIO()
		with zipfile.ZipFile(clean_sfx_bytes, "w") as clean_sfx:
			clean_sfx.writestr("readme.txt", b"ordinary 2D notes")
		(backup / "clean_self_extracting.bundle").write_bytes(
			b"MZ" + (b"stub" * (20 * 1024)) + clean_sfx_bytes.getvalue())
		(backup / "disguised_7z.payload").write_bytes(
			game_2d.SEVEN_ZIP_MAGIC + b"opaque")
		(backup / "disguised_rar.payload").write_bytes(
			game_2d.RAR_MAGICS[0] + b"opaque")
		inventory = game_2d.discover(root)
		zip_members = inventory.model_archive_files["backups/disguised.zip"][
			"model_members"]
		tar_members = inventory.model_archive_files["backups/disguised.tar"][
			"model_members"]
		self.assertIn("payload.bin::<disguised-model-signature>", zip_members)
		self.assertIn("nested.payload::<nested-archive-review-required>", zip_members)
		self.assertIn("compressed.payload::<nested-archive-review-required>", zip_members)
		self.assertIn(
			"self_extracting.payload::<nested-archive-review-required>", zip_members)
		self.assertIn("nested_7z.payload::<nested-archive-review-required>", zip_members)
		self.assertIn("nested_rar.payload::<nested-archive-review-required>", zip_members)
		self.assertEqual(
			tar_members, ["payload.cache::<disguised-model-signature>"])
		self.assertIn("backups/zip.bundle", inventory.model_archive_files)
		self.assertIn("backups/tar.bundle", inventory.model_archive_files)
		self.assertIn("backups/self_extracting.bundle", inventory.model_archive_files)
		self.assertIn(
			"backups/elf_self_extracting.bundle", inventory.model_archive_files)
		self.assertEqual(
			inventory.model_archive_files["backups/disguised_7z.payload"][
				"model_members"], ["<opaque-review-required>"])
		self.assertEqual(
			inventory.model_archive_files["backups/disguised_rar.payload"][
				"model_members"], ["<opaque-review-required>"])
		self.assertNotIn("backups/clean.bundle", inventory.model_archive_files)
		self.assertNotIn(
			"backups/clean_self_extracting.bundle", inventory.model_archive_files)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_archive_sniff_limits_fail_closed(self) -> None:
		temp, root, _manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		path = root / "backups/bounded.zip"
		path.parent.mkdir()
		with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
			archive.writestr("one.txt", b"abcdefgh")
			archive.writestr("two.txt", b"ijklmnop")
			archive.writestr("compressed.bin", b"0" * 2048)
		with mock.patch.object(game_2d, "ARCHIVE_SNIFF_BUDGET", 4):
			evidence = game_2d._model_archive_evidence(path)
		self.assertIsNotNone(evidence)
		self.assertIn("<archive-sniff-budget-exceeded>", evidence["model_members"])
		with mock.patch.object(game_2d, "ARCHIVE_MEMBER_LIMIT", 1):
			evidence = game_2d._model_archive_evidence(path)
		self.assertIn("<archive-member-limit-exceeded>", evidence["model_members"])
		with mock.patch.object(game_2d, "ARCHIVE_RATIO_MIN_SIZE", 1), \
				mock.patch.object(game_2d, "ARCHIVE_RATIO_LIMIT", 1):
			evidence = game_2d._model_archive_evidence(path)
		self.assertTrue(any(
			member.endswith("::<unsafe-compression-review-required>")
			for member in evidence["model_members"]))

	def test_new_production_3d_file_fails_regression_gate(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/new_world.gd").write_text(
			"extends Node3D\nvar camera: Camera3D\n", encoding="utf-8")
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D101", self.finding_ids(result))

	def test_spatial_shader_is_production_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		shader = root / "assets/shaders/live.gdshader"
		shader.parent.mkdir(parents=True)
		shader.write_text(
			"shader_type spatial;\nvoid fragment() {}\n", encoding="utf-8")
		(root / "assets/shaders/live.tres").write_text(
			'[gd_resource type="ShaderMaterial" format=3]\n'
			'[ext_resource path="res://assets/shaders/live.gdshader" type="Shader" id="1"]\n',
			encoding="utf-8",
		)
		inventory = game_2d.discover(root)
		self.assertIn("assets/shaders/live.gdshader", inventory.production_3d_files)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_sky_and_fog_shaders_are_3d_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "sky.gdshader").write_text("shader_type sky;\n", encoding="utf-8")
		(root / "fog.gdshader").write_text("shader_type fog;\n", encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files), {"sky.gdshader", "fog.gdshader"})
		self.assertEqual(
			inventory.production_3d_files["sky.gdshader"], {"<sky-shader>": 1})
		self.assertEqual(
			inventory.production_3d_files["fog.gdshader"], {"<fog-shader>": 1})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_visual_shader_spatial_mode_is_scoped_and_defaults_to_3d(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "explicit.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nmode = 0\n',
			encoding="utf-8")
		(root / "default.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nflags/light_only = false\n',
			encoding="utf-8")
		(root / "canvas.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nmode = 1\n',
			encoding="utf-8")
		(root / "particles.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nmode = 2\n',
			encoding="utf-8")
		(root / "sky_visual.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nmode = 3\n',
			encoding="utf-8")
		(root / "fog_visual.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nmode = 4\n',
			encoding="utf-8")
		(root / "unknown_visual.tres").write_text(
			'[gd_resource type="VisualShader" format=3]\n[resource]\nmode = 99\n',
			encoding="utf-8")
		(root / "scoped.tres").write_text(
			'[gd_resource type="Resource" format=3]\n'
			'[sub_resource type="VisualShader" id="VisualShader_canvas"]\nmode = 1\n'
			'[sub_resource type="Resource" id="Other"]\nmode = 0\n',
			encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.scene_3d_files), {
				"default.tres", "explicit.tres", "fog_visual.tres",
				"sky_visual.tres", "unknown_visual.tres",
			})
		self.assertNotIn("canvas.tres", inventory.scene_3d_files)
		self.assertNotIn("particles.tres", inventory.scene_3d_files)
		self.assertEqual(
			inventory.scene_3d_files["explicit.tres"],
			{"<spatial-visual-shader>": 1})
		(root / "scripts/visual.gd").write_text(
			"var shader = VisualShader.new()\n"
			"shader.mode = VisualShader.MODE_SPATIAL\n",
			encoding="utf-8",
		)
		inventory = game_2d.discover(root)
		self.assertEqual(
			inventory.production_3d_files["scripts/visual.gd"],
			{"<3d-visual-shader-code>": 1},
		)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_visual_shader_code_modes_track_instances_without_2d_false_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		for name, text in {
			"canvas.gd": (
				"var shader = VisualShader.new()\n"
				"shader.mode = VisualShader.MODE_CANVAS_ITEM\n"),
			"particles.gd": (
				"var shader = VisualShader.new()\n"
				"shader.set_mode(VisualShader.MODE_PARTICLES)\n"
				"var numeric = VisualShader.new()\nnumeric.mode = 2\n"),
			"default.gd": "var shader = VisualShader.new()\n",
			"numeric.gd": (
				"var shader: VisualShader\nshader.mode = 0\n"
				"shader.set_mode(3)\nshader.mode = 4\n"
				"func set_existing(existing: VisualShader): existing.mode = 3\n"),
			"classdb.gd": (
				'var shader = ClassDB.instantiate("VisualShader")\nshader.mode = 3\n'),
			"unrelated.gd": "var settings = RefCounted.new()\nsettings.mode = 3\n",
		}.items():
			(root / name).write_text(text, encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files), {"classdb.gd", "default.gd", "numeric.gd"})
		self.assertEqual(
			inventory.production_3d_files["default.gd"],
			{"<visual-shader-default-spatial>": 1})
		self.assertEqual(
			inventory.production_3d_files["numeric.gd"],
			{"<3d-visual-shader-code>": 4})
		self.assertEqual(
			inventory.production_3d_files["classdb.gd"],
			{"<3d-visual-shader-code>": 1})
		self.assertNotIn("canvas.gd", inventory.production_3d_files)
		self.assertNotIn("particles.gd", inventory.production_3d_files)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_visual_shader_csharp_and_cpp_modes_are_instance_scoped(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		for name, text in {
			"managed_canvas.cs": (
				"var shader = new VisualShader();\n"
				"shader.Mode = Shader.ModeEnum.CanvasItem;\n"),
			"managed_particles.cs": (
				"VisualShader shader = new VisualShader();\n"
				"shader.SetMode(VisualShader.ModeEnum.Particles);\n"),
			"managed_object_canvas.cs": (
				"var shader = new VisualShader() { "
				"Mode = Shader.ModeEnum.CanvasItem };\n"),
			"managed_object_spatial.cs": (
				"var shader = new VisualShader { "
				"Mode = Shader.ModeEnum.Spatial };\n"),
			"managed_spatial.cs": (
				"VisualShader shader;\nshader.Mode = Shader.ModeEnum.Spatial;\n"
				"shader.SetMode(VisualShader.ModeEnum.Fog);\n"),
			"managed_nullable.cs": (
				"VisualShader? shader; shader!.Mode = Shader.ModeEnum.Sky;\n"),
			"managed_array.cs": (
				"VisualShader[] shaders; shaders[0].Mode = Shader.ModeEnum.Fog;\n"),
			"native_canvas.cpp": (
				"Ref<VisualShader> shader; shader.instantiate();\n"
				"shader->set_mode(Shader::MODE_CANVAS_ITEM);\n"),
			"native_particles.cpp": (
				"Ref<VisualShader> &shader;\n"
				"shader->set_mode(VisualShader::MODE_PARTICLES);\n"),
			"native_spatial.cpp": (
				"Ref<VisualShader> &shader;\n"
				"shader->set_mode(Shader::MODE_SKY);\n"),
			"native_default.cpp": (
				"Ref<VisualShader> shader; shader.instantiate();\n"),
			"target_default.cs": "VisualShader shader = new();\n",
			"namespace_default.cs": (
				"Godot.VisualShader shader = new Godot.VisualShader();\n"),
			"later_canvas.cs": (
				"VisualShader shader; shader = new VisualShader();\n"
				"shader.Mode = Shader.ModeEnum.CanvasItem;\n"),
			"inline_canvas.gd": (
				"func make_shader():\n"
				"\tVisualShader.new().set_mode(VisualShader.MODE_CANVAS_ITEM)\n"),
			"duplicate_scope.gd": (
				"func canvas():\n\tvar shader = VisualShader.new()\n\tshader.mode = 1\n"
				"func default_shader():\n\tvar shader = VisualShader.new()\n"),
			"native_namespace.cpp": (
				"Ref<godot::VisualShader> shader; shader.instantiate();\n"
				"shader->set_mode(godot::Shader::MODE_SPATIAL);\n"),
			"unknown.gd": (
				"var shader = VisualShader.new()\n"
				"shader.set_mode(VisualShader.MODE_CANVAS_ITEM + runtime_mode)\n"),
		}.items():
			(root / name).write_text(text, encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {
			"duplicate_scope.gd", "managed_array.cs", "managed_nullable.cs",
			"managed_object_spatial.cs", "managed_spatial.cs",
			"namespace_default.cs", "native_default.cpp", "native_namespace.cpp",
			"native_spatial.cpp", "target_default.cs", "unknown.gd",
		})
		self.assertEqual(
			inventory.production_3d_files["managed_spatial.cs"],
			{"<3d-visual-shader-code>": 2})
		self.assertEqual(
			inventory.production_3d_files["native_spatial.cpp"],
			{"<3d-visual-shader-code>": 1})
		self.assertEqual(
			inventory.production_3d_files["native_default.cpp"],
			{"<visual-shader-default-spatial>": 1})
		self.assertEqual(
			inventory.production_3d_files["unknown.gd"],
			{"<visual-shader-unknown-mode>": 1})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_multimesh_is_allowed_only_with_demonstrable_2d_context(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		for name, text in {
			"bound_2d.gd": (
				"var mesh = MultiMesh.new()\n"
				"var display = MultiMeshInstance2D.new()\n"
				"display.multimesh = mesh\n"),
			"inferred_bound_2d.gd": (
				"var mesh := MultiMesh.new()\n"
				"var display := MultiMeshInstance2D.new()\n"
				"display.multimesh = mesh\n"),
			"typed_2d.gd": (
				"func bind(mesh: MultiMesh, display: MultiMeshInstance2D):\n"
				"\tdisplay.multimesh = mesh\n"),
			"explicit_2d.cs": (
				"var mesh = new MultiMesh();\n"
				"mesh.TransformFormat = MultiMesh.TransformFormatEnum.Transform2D;\n"
				"var display = new MultiMeshInstance2D(); display.Multimesh = mesh;\n"),
			"native_2d.cpp": (
				"Ref<MultiMesh> mesh; MultiMeshInstance2D *display;\n"
				"display->set_multimesh(mesh);\n"),
			"object_2d.cs": (
				"var mesh = new MultiMesh() { TransformFormat = 0 };\n"),
			"object_bound_2d.cs": (
				"var mesh = new MultiMesh { };\n"
				"var display = new MultiMeshInstance2D { Multimesh = mesh };\n"),
			"inline_object_2d.cs": (
				"var display = new MultiMeshInstance2D { "
				"Multimesh = new MultiMesh() };\n"),
			"inline_object_explicit_2d.cs": (
				"var display = new MultiMeshInstance2D { "
				"Multimesh = new MultiMesh { TransformFormat = 0 } };\n"),
			"inline_2d.gd": (
				"var display: MultiMeshInstance2D\n"
				"display.multimesh = MultiMesh.new()\n"),
			"numeric_2d.gd": (
				"var mesh: MultiMesh\nmesh = MultiMesh.new()\n"
				"mesh.transform_format = 0\n"),
			"setter_2d.gd": (
				"var mesh = MultiMesh.new()\n"
				"mesh.set_transform_format(MultiMesh.TRANSFORM_2D)\n"),
			"default.gd": "var mesh = MultiMesh.new()\n",
			"inferred_default.gd": "var mesh := MultiMesh.new()\n",
			"classdb_default.gd": (
				'var mesh = ClassDB.instantiate("MultiMesh")\n'),
			"explicit_3d.gd": (
				"var mesh = MultiMesh.new()\n"
				"mesh.transform_format = MultiMesh.TRANSFORM_3D\n"),
			"inferred_3d.gd": (
				"var mesh := MultiMesh.new()\n"
				"mesh.transform_format = MultiMesh.TRANSFORM_3D\n"),
			"numeric_3d.gd": (
				"var mesh = MultiMesh.new()\nmesh.transform_format = 1\n"),
			"setter_3d.cs": (
				"var mesh = new MultiMesh();\n"
				"mesh.SetTransformFormat(MultiMesh.TransformFormatEnum.Transform3D);\n"),
			"object_3d.cs": (
				"var mesh = new MultiMesh { TransformFormat = 1 };\n"),
			"inline_object_3d.cs": (
				"var display = new MultiMeshInstance2D { "
				"Multimesh = new MultiMesh { TransformFormat = 1 } };\n"),
			"native_classdb.cpp": (
				'auto mesh = ClassDB::instantiate("MultiMesh");\n'),
			"control.gd": (
				"var points = PackedVector2Array()\n"
				"var material = CanvasItemMaterial.new()\n"
				"var display: MultiMeshInstance2D\n"),
		}.items():
			(root / name).write_text(text, encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files), {
				"classdb_default.gd", "default.gd", "explicit_3d.gd",
				"inferred_default.gd", "inferred_3d.gd",
				"inline_object_3d.cs", "native_classdb.cpp", "numeric_3d.gd",
				"object_3d.cs",
				"setter_3d.cs",
			})
		self.assertEqual(
			inventory.production_3d_files["default.gd"],
			{"<multimesh-default-3d-risk>": 1})
		self.assertEqual(
			inventory.production_3d_files["inferred_default.gd"],
			{"<multimesh-default-3d-risk>": 1})
		self.assertGreaterEqual(
			inventory.production_3d_files["inferred_3d.gd"].get(
				"<3d-multimesh>", 0), 1)
		self.assertGreaterEqual(
			inventory.production_3d_files["explicit_3d.gd"].get(
				"<3d-multimesh>", 0), 1)
		self.assertEqual(
			inventory.production_3d_files["classdb_default.gd"],
			{"<multimesh-default-3d-risk>": 1})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_serialized_multimesh_scope_distinguishes_2d_and_3d(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		for name, text in {
			"default.tres": (
				'[gd_resource type="MultiMesh" format=3]\n[resource]\n'),
			"explicit_3d.tres": (
				'[gd_resource type="MultiMesh" format=3]\n[resource]\n'
				"transform_format = 1\n"),
			"explicit_2d.tres": (
				'[gd_resource type="MultiMesh" format=3]\n[resource]\n'
				"transform_format = 0\n"),
			"bound_2d.tscn": (
				'[gd_scene format=3]\n'
				'[sub_resource type="MultiMesh" id="MM"]\n'
				'[node name="Display" type="MultiMeshInstance2D"]\n'
				'multimesh = SubResource("MM")\n'),
			"bound_3d.tscn": (
				'[gd_scene format=3]\n'
				'[sub_resource type="MultiMesh" id="MM"]\ntransform_format = 0\n'
				'[node name="Display" type="MultiMeshInstance3D"]\n'
				'multimesh = SubResource("MM")\n'),
		}.items():
			(root / name).write_text(text, encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.scene_3d_files), {
			"bound_3d.tscn", "default.tres", "explicit_3d.tres",
		})
		self.assertNotIn("explicit_2d.tres", inventory.scene_3d_files)
		self.assertNotIn("bound_2d.tscn", inventory.scene_3d_files)
		self.assertEqual(
			inventory.scene_3d_files["default.tres"],
			{"<3d-multimesh-resource>": 1})
		self.assertGreaterEqual(
			inventory.scene_3d_files["bound_3d.tscn"].get(
				"<3d-multimesh-resource>", 0), 1)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_named_3d_resources_and_csharp_are_production_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "environment.tscn").write_text(
			'[gd_scene format=3]\n[node name="World" type="WorldEnvironment"]\n',
			encoding="utf-8",
		)
		(root / "navigation.tres").write_text(
			'[gd_resource type="NavigationMesh" format=3]\n', encoding="utf-8")
		(root / "live.cs").write_text(
			"public partial class Live : Node3D {}\n", encoding="utf-8")
		(root / "addons/live").mkdir(parents=True)
		(root / "addons/live/live.gdextension").write_text(
			'[configuration]\nentry_symbol="live_init"\n', encoding="utf-8")
		(root / "addons/live/live.cpp").write_text(
			"class NativeWorld : public Node3D {};\n"
			"Ref<Mesh> mesh; Ref<godot::Mesh> godot_mesh;\n"
			"godot::Environment *environment;\n", encoding="utf-8")
		(root / "addons/live/prefix_control.cpp").write_text(
			'const char *words = "Sky Plane Basis Compositor Decal Environment Mesh Projection";\n'
			"SkyLagoonPromenade sky_stage; PlaneTicket ticket; BasisPoints points;\n"
			"CompositorPreview preview; Decalogue tale; Environmentalist guide;\n"
			"MeshyAsset art; Projectionist performer;\n"
			"other::Environment *foreign; notgodot::Mesh *impostor;\n"
			"foo::godot::Mesh *nested_namespace;\n",
			encoding="utf-8")
		(root / "addons/live/live.dll").write_bytes(b"MZ\x00Node3D\x00")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files),
			{"live.cs", "addons/live/live.cpp", "addons/live/live.dll"})
		self.assertNotIn("addons/live/prefix_control.cpp", inventory.production_3d_files)
		self.assertEqual(
			set(inventory.scene_3d_files), {"environment.tscn", "navigation.tres"})
		self.assertEqual(
			inventory.configuration_3d_files["addons/live/live.gdextension"],
			{"<native-extension-descriptor>": 1})
		self.assertEqual(inventory.production_3d_files["addons/live/live.cpp"]["Mesh"], 2)
		self.assertEqual(
			inventory.production_3d_files["addons/live/live.cpp"]["Environment"], 1)
		for source in (
			"godot::Mesh *mesh;", "::godot::Mesh *mesh;",
			"Ref<godot::Mesh> mesh;", "class X : public godot::Mesh {};",
			"godot::Mesh *make_mesh();", "static_cast<godot::Mesh *>(value);",
		):
			with self.subTest(source=source):
				self.assertEqual(game_2d._token_counts(source).get("Mesh"), 1)
		for source in (
			"notgodot::Mesh *mesh;", "other::Mesh *mesh;",
			"foo::godot::Mesh *mesh;",
		):
			with self.subTest(source=source):
				self.assertNotIn("Mesh", game_2d._token_counts(source))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_godot_471_3d_api_taxonomy_and_typed_containers_are_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "api.gd").write_text(
			"var skin = Skin.new()\n"
			"var fog = FogMaterial.new()\n"
			"var voxel: VoxelGIData\n"
			"var xr = XRServer\n"
			"var action = OpenXRAction.new()\n"
			"var settings: MeshConvexDecompositionSettings\n"
			"var meshes: Array[Mesh]\n"
			"var skies: Dictionary[String, Sky]\n"
			"var gizmo: EditorNode3DGizmoPlugin\n"
			"var physics_manager: PhysicsServer3DManager\n"
			"var navigation_manager: NavigationServer3DManager\n"
			"var blend_importer: EditorSceneFormatImporterBlend\n"
			"var fbx_document: FBXDocument\n"
			"var obj_importer: ResourceImporterOBJ\n"
			"var post_import: EditorScenePostImport\n",
			encoding="utf-8",
		)
		(root / "control.gd").write_text(
			'const STORY = "Roshan chooses a gentle skin color under the sky"\n'
			"var textures: Array[Texture2D]\n"
			"var colors: Dictionary[String, Color]\n",
			encoding="utf-8",
		)
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {"api.gd"})
		counts = inventory.production_3d_files["api.gd"]
		for token in (
				"Skin", "FogMaterial", "VoxelGIData", "XRServer", "OpenXRAction",
				"MeshConvexDecompositionSettings", "Mesh", "Sky"):
			with self.subTest(token=token):
				self.assertGreaterEqual(counts.get(token, 0), 1)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))
		for token in (
				"EditorNode3DGizmoPlugin", "PhysicsServer3DManager",
				"NavigationServer3DManager", "EditorSceneFormatImporterBlend",
				"FBXDocument", "ResourceImporterOBJ", "EditorScenePostImport"):
			with self.subTest(pipeline_token=token):
				self.assertEqual(counts.get(token), 1)

	def test_packed_vector_and_3d_texture_material_variants_are_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "variants.gd").write_text(
			"var points = PackedVector3Array()\n"
			"var sky_material = SkyMaterial.new()\n"
			"var volume = ImageTexture3D.new()\n"
			"var noise = NoiseTexture3D.new()\n"
			"var placeholder = PlaceholderTexture3D.new()\n"
			"var cubemap = Cubemap.new()\n",
			encoding="utf-8",
		)
		(root / "two_d_controls.gd").write_text(
			"var points = PackedVector2Array()\n"
			"var material = CanvasItemMaterial.new()\n"
			"var texture = ImageTexture.create_empty(8, 8)\n"
			"var array = Texture2DArray.new()\n",
			encoding="utf-8",
		)
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {"variants.gd"})
		counts = inventory.production_3d_files["variants.gd"]
		for token in (
				"PackedVector3Array", "SkyMaterial", "ImageTexture3D",
				"NoiseTexture3D", "PlaceholderTexture3D", "Cubemap"):
			with self.subTest(token=token):
				self.assertEqual(counts.get(token), 1)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_native_descriptor_and_stripped_binary_are_review_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "addons/live").mkdir(parents=True)
		(root / "addons/live/plugin.gdextension").write_text(
			'[libraries]\nwindows="res://addons/live/plugin.dll"\n', encoding="utf-8")
		(root / "addons/live/plugin.dll").write_bytes(b"MZ\x00\x01stripped")
		(root / "disabled_addons/old").mkdir(parents=True)
		(root / "disabled_addons/old/old.gdextension").write_text(
			"[configuration]\n", encoding="utf-8")
		(root / "disabled_addons/old/old.so.1").write_bytes(b"Node3D")
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {"addons/live/plugin.dll"})
		self.assertEqual(
			set(inventory.configuration_3d_files), {"addons/live/plugin.gdextension"})
		self.assertEqual(
			inventory.production_3d_files["addons/live/plugin.dll"],
			{"<opaque-native-extension-binary>": 1})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_ambiguous_story_words_require_actual_api_context(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "story.gd").write_text(
			'const LABEL = "Sky Lagoon and Pearl Plane"\n'
			'const NOTE = "Basis Compositor Decal Environment Mesh Projection"\n'
			'# Sky Plane Environment Mesh Projection Decal Basis Compositor\n'
			'# VisualShader.new() and ClassDB.instantiate(StringName("Me" + "sh"))\n'
			'const TYPE_PROSE = "type=\\"Sky\\" VisualShader.new()"\n',
			encoding="utf-8")
		self.assertEqual(game_2d.discover(root).production_3d_files, {})

		(root / "actual.gd").write_text(
			"var basis: Basis\nvar compositor: Compositor\nvar decal: Decal\n"
			"var environment: Environment\nvar mesh: Mesh\nvar plane: Plane\n"
			"var projection: Projection\nvar skin = Skin.new()\nvar sky: Sky\n",
			encoding="utf-8")
		(root / "sky_resource.tres").write_text(
			'[gd_resource type="Sky" format=3]\n', encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files["actual.gd"]),
			game_2d.AMBIGUOUS_3D_API_CLASSES)
		self.assertEqual(inventory.scene_3d_files["sky_resource.tres"], {"Sky": 1})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_classdb_simple_concatenation_resolves_3d_but_not_2d(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "runtime.gd").write_text(
			'const PREFIX = "Mesh"\nconst SUFFIX = "Instance" + "3D"\n'
			'const TYPE = PREFIX + SUFFIX\n'
			'const WRAPPED = String("Node" + "3D")\n'
			'var one = ClassDB.instantiate(TYPE)\n'
			'var two = ClassDB.instantiate(StringName("Mesh" + "Instance" + "3D"))\n'
			'var three = ClassDB.instantiate(WRAPPED)\n'
			'var four = ClassDB.instantiate(&"Mesh" + "Instance" + "3D")\n',
			encoding="utf-8")
		(root / "control.gd").write_text(
			'var node = ClassDB.instantiate(StringName("Node" + "2D"))\n'
			'# ClassDB.instantiate(StringName("Mesh" + "Instance" + "3D"))\n',
			encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {"runtime.gd"})
		self.assertEqual(
			inventory.production_3d_files["runtime.gd"], {"<resolved-3d-class>": 4})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_classdb_static_dynamic_cpp_and_csharp_instantiation_are_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "runtime.gd").write_text(
			'static var TYPE = "Node" + "3D"\n'
			"var known = ClassDB.instantiate(TYPE)\n"
			"var dynamic = ClassDB.instantiate(runtime_type)\n",
			encoding="utf-8",
		)
		(root / "native.cpp").write_text(
			'auto node = ClassDB::instantiate("MeshInstance3D");\n',
			encoding="utf-8",
		)
		(root / "managed.cs").write_text(
			'var node = ClassDB.Instantiate("Node3D");\n', encoding="utf-8")
		(root / "control.gd").write_text(
			'var node = ClassDB.instantiate("Node2D")\n', encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files), {"managed.cs", "native.cpp", "runtime.gd"})
		self.assertEqual(
			inventory.production_3d_files["runtime.gd"]["<resolved-3d-class>"], 1)
		self.assertEqual(
			inventory.production_3d_files["runtime.gd"][
				"<dynamic-classdb-instantiation>"], 1)
		self.assertGreaterEqual(
			inventory.production_3d_files["native.cpp"]["<resolved-3d-class>"], 1)
		self.assertGreaterEqual(
			inventory.production_3d_files["managed.cs"]["<resolved-3d-class>"], 1)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_binary_scene_and_override_configuration_are_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "main.scn").write_bytes(b"RSRC opaque Godot binary scene")
		(root / "override.cfg").write_text(
			'[physics]\n3d/physics_engine="Jolt Physics"\n', encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			inventory.scene_3d_files["main.scn"],
			{"<opaque-binary-resource>": 1},
		)
		self.assertIn("override.cfg", inventory.configuration_3d_files)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_disabled_model_import_settings_remain_configuration_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "project.godot").write_text(
			'[filesystem]\nimport/blender/enabled=false\nimport/fbx/importer=0\n',
			encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			inventory.configuration_3d_files["project.godot"],
			{"<3d-configuration>": 2})

	def test_runtime_data_tokens_are_debt_but_provenance_data_is_not(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "catalog.json").write_text('{"type":"Node3D"}\n', encoding="utf-8")
		(root / "assets").mkdir()
		(root / "assets/runtime.json").write_text(
			'{"value":"Sprite3D"}\n', encoding="utf-8")
		(root / "data").mkdir()
		(root / "data/live.xml").write_text("<type>Vector3</type>\n", encoding="utf-8")
		(root / "config").mkdir()
		(root / "config/live.toml").write_text('type="WorldEnvironment"\n', encoding="utf-8")
		(root / "content").mkdir()
		(root / "content/live.yaml").write_text("type: Camera3D\n", encoding="utf-8")
		(root / "assets/provenance").mkdir()
		(root / "assets/provenance/history.json").write_text(
			'{"removed":"Node3D","model":"assets/legacy.glb"}\n', encoding="utf-8")
		(root / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json").write_text(
			'{"review":"Node3D","model":"assets/legacy.glb"}\n', encoding="utf-8")
		(root / "FABLE_RUNTIME.json").write_text(
			'{"runtime":"Node3D"}\n', encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {
			"assets/runtime.json", "catalog.json", "config/live.toml",
			"content/live.yaml", "data/live.xml",
			"FABLE_RUNTIME.json",
		})
		self.assertNotIn(
			"assets/provenance/history.json", inventory.production_3d_files)
		self.assertNotIn(
			"FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json",
			inventory.production_3d_files)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_custom_godot_active_data_roots_are_scanned_and_gdignore_is_respected(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "custom/catalogs").mkdir(parents=True)
		(root / "custom/catalogs/catalog.json").write_text(
			'{"node":"Node3D","model":"res://assets/legacy/prop.glb"}\n',
			encoding="utf-8",
		)
		(root / "ignored/catalogs").mkdir(parents=True)
		(root / "ignored/.gdignore").write_text("", encoding="utf-8")
		(root / "ignored/catalogs/catalog.json").write_text(
			'{"node":"Node3D","model":"res://assets/legacy/prop.glb"}\n',
			encoding="utf-8",
		)
		(root / "custom/provenance").mkdir()
		(root / "custom/provenance/retired.json").write_text(
			'{"node":"Node3D","model":"res://assets/legacy/prop.glb"}\n',
			encoding="utf-8",
		)
		inventory = game_2d.discover(root)
		self.assertIn("custom/catalogs/catalog.json", inventory.production_3d_files)
		self.assertNotIn("ignored/catalogs/catalog.json", inventory.production_3d_files)
		self.assertNotIn(
			"custom/provenance/retired.json", inventory.production_3d_files)
		game_2d._write_manifest(manifest, inventory)
		# Add an archive candidate after the exact inventory is written; dependency
		# proof must still see the custom live catalog.
		(root / "assets/legacy").mkdir(parents=True)
		(root / "assets/legacy/prop.glb").write_bytes(b"model")
		inventory = game_2d.discover(root)
		game_2d._write_manifest(
			manifest, inventory, ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		self.assertTrue(any(
			finding.check_id == "G2D301"
			and "custom/catalogs/catalog.json" in finding.detail
			for finding in result.findings), result.findings)
		self.assertFalse(any(
			"ignored/catalogs" in finding.detail for finding in result.findings))
		self.assertFalse(any(
			"custom/provenance" in finding.detail for finding in result.findings))

	def test_live_code_load_makes_provenance_data_runtime_reachable(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "assets/provenance").mkdir(parents=True)
		(root / "assets/provenance/loaded.json").write_text(
			'{"node":"Node3D","model":"res://assets/legacy/prop.glb"}\n',
			encoding="utf-8",
		)
		(root / "assets/provenance/unreferenced.json").write_text(
			'{"node":"Node3D","model":"res://assets/legacy/prop.glb"}\n',
			encoding="utf-8",
		)
		(root / "assets/provenance/dynamic").mkdir()
		(root / "assets/provenance/dynamic/runtime.json").write_text(
			'{"node":"Camera3D","model":"res://assets/legacy/prop.glb"}\n',
			encoding="utf-8",
		)
		for name in ("managed.json", "native.json"):
			(root / "assets/provenance" / name).write_text(
				'{"node":"Node3D","model":"res://assets/legacy/prop.glb"}\n',
				encoding="utf-8",
			)
		(root / "runtime.gd").write_text(
			'const CATALOG = "res://assets/provenance".path_join("loaded.json")\n'
			'const DYNAMIC_DIR = "res://assets/provenance/dynamic"\n'
			"func read_catalog():\n"
			"\treturn FileAccess.get_file_as_string(CATALOG)\n"
			"func read_named(name: String):\n"
			"\treturn FileAccess.get_file_as_string(DYNAMIC_DIR.path_join(name))\n",
			encoding="utf-8",
		)
		(root / "managed.cs").write_text(
			'var config = new ConfigFile();\n'
			'config.Load("res://assets/provenance/managed.json");\n',
			encoding="utf-8",
		)
		(root / "native.cpp").write_text(
			'FileAccess::get_file_as_string('
			'"res://assets/provenance/native.json");\n', encoding="utf-8")
		(root / "assets/legacy").mkdir(parents=True)
		(root / "assets/legacy/prop.glb").write_bytes(b"model")
		inventory = game_2d.discover(root)
		self.assertIn(
			"assets/provenance/loaded.json", inventory.production_3d_files)
		self.assertIn(
			"assets/provenance/dynamic/runtime.json", inventory.production_3d_files)
		self.assertIn(
			"assets/provenance/managed.json", inventory.production_3d_files)
		self.assertIn(
			"assets/provenance/native.json", inventory.production_3d_files)
		self.assertNotIn(
			"assets/provenance/unreferenced.json", inventory.production_3d_files)
		game_2d._write_manifest(
			manifest, inventory, ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		self.assertTrue(any(
			finding.check_id == "G2D301"
			and "assets/provenance/loaded.json" in finding.detail
			for finding in result.findings), result.findings)
		self.assertFalse(any(
			"assets/provenance/unreferenced.json" in finding.detail
			for finding in result.findings))

	def test_additional_runtime_source_and_opaque_package_formats_are_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "addons/live").mkdir(parents=True)
		for name, text in {
			"shader.gdshaderinc": "Vector3 helper;\n",
			"Plugin.java": "class Plugin extends Node3D {}\n",
			"Plugin.kt": "val point: Vector3\n",
			"plugin.rs": "struct Plugin(Node3D);\n",
		}.items():
			(root / "addons/live" / name).write_text(text, encoding="utf-8")
		with zipfile.ZipFile(root / "addons/live/plugin.jar", "w") as archive:
			archive.writestr("Plugin.class", b"ordinary stripped bytecode")
		(root / "assets").mkdir()
		(root / "assets/content.pck").write_bytes(b"GDPC opaque pack")
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.production_3d_files), {
			"addons/live/Plugin.java", "addons/live/Plugin.kt",
			"addons/live/plugin.jar", "addons/live/plugin.rs",
			"addons/live/shader.gdshaderinc", "assets/content.pck",
		})
		self.assertEqual(
			inventory.production_3d_files["addons/live/plugin.jar"],
			{"<opaque-runtime-binary>": 1})
		self.assertEqual(
			inventory.production_3d_files["assets/content.pck"],
			{"<opaque-runtime-binary>": 1})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_disguised_glb_magic_is_model_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		path = root / "assets/disguised.bin"
		path.parent.mkdir(parents=True)
		path.write_bytes(b"glTF\x02\x00\x00\x00\x20\x00\x00\x00")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.model_files, ("assets/disguised.bin",))
		self.assertEqual(inventory.active_export_model_files, ("assets/disguised.bin",))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_disguised_ascii_obj_requires_vertices_and_face(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		path = root / "assets/disguised.txt"
		path.parent.mkdir(parents=True)
		path.write_text(
			"# renamed OBJ\nv 0.0 0.0 0.0\nv 1.0 0.0 0.0\nv 0.0 1.0 0.0\nf 1 2 3\n",
			encoding="ascii",
		)
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.model_files, ("assets/disguised.txt",))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_obj_words_without_geometry_are_not_a_model_false_positive(self) -> None:
		temp, root, _manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "notes.txt").write_text(
			"v is a letter and f is another letter\n", encoding="utf-8")
		self.assertEqual(game_2d.discover(root).model_files, ())

	def test_disguised_gltf_json_is_model_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		assets = root / "assets"
		assets.mkdir(parents=True)
		(assets / "gltf1.json").write_text(
			'{"asset":{"version":"1.1","generator":"test"},"scenes":[{}]}\n',
			encoding="utf-8")
		(assets / "gltf2.json").write_text(
			'{"asset":{"version":"2.4","generator":"test"},"scenes":[{}]}\n',
			encoding="utf-8")
		(assets / "whitespace_gltf.json").write_text(
			(" " * (70 * 1024)) +
			'{"asset":{"version":"2.0"},"meshes":[]}\n', encoding="utf-8")
		(assets / "bom_gltf.json").write_bytes(
			b"\xef\xbb\xbf" + b'{"asset":{"version":"2.0"},"nodes":[]}\n')
		(assets / "mesh.cache").write_bytes(
			b"ply\r\nformat ascii 1.0\r\nend_header\r\n")
		(assets / "ordinary.json").write_text(
			'{"asset":{"version":"2.4"},"levels":[]}\n', encoding="utf-8")
		(assets / "large_gltf.payload").write_text(
			'{"padding":"' + ("x" * (600 * 1024)) + '","asset":{"version":"2.0"},'
			'"meshes":[]}\n', encoding="utf-8")
		(assets / "namespaced.xml").write_text(
			'<?xml version="1.0"?>\n<!--' + ("x" * (20 * 1024)) + '-->\n'
			'<c:COLLADA xmlns:c="urn:collada"><c:asset/></c:COLLADA>\n',
			encoding="utf-8")
		(assets / "namespaced_x3d.xml").write_text(
			'<x:X3D xmlns:x="urn:x3d"><x:Scene/></x:X3D>\n', encoding="utf-8")
		(assets / "ordinary.xml").write_text(
			'<x:Scene xmlns:x="urn:ordinary">storybook</x:Scene>\n', encoding="utf-8")
		self.assertEqual(
			game_2d.discover(root).model_files,
			(
				"assets/bom_gltf.json", "assets/gltf1.json", "assets/gltf2.json",
				"assets/large_gltf.payload",
				"assets/mesh.cache", "assets/namespaced.xml",
				"assets/namespaced_x3d.xml", "assets/whitespace_gltf.json",
			))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_plausible_model_text_over_safe_cap_is_explicit_coverage_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		assets = root / "assets"
		assets.mkdir()
		(assets / "ordinary.json").write_text(
			'{"storybook":"small and two dimensional"}\n', encoding="utf-8")
		(assets / "unproven.payload").write_text(
			'{"padding":"' + ("x" * 4096) + '","levels":[]}\n',
			encoding="utf-8",
		)
		with mock.patch.object(game_2d, "MODEL_TEXT_SCAN_BYTES", 1024):
			inventory = game_2d.discover(root)
			self.assertIn("assets/unproven.payload", inventory.model_files)
			self.assertIn(
				"assets/unproven.payload", inventory.model_scan_coverage_files)
			self.assertNotIn("assets/ordinary.json", inventory.model_files)
			result = game_2d.audit(root, manifest)
		self.assertIn("G2D101", self.finding_ids(result))

	def test_raw_compressed_models_and_bounded_compression_fail_closed(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		assets = root / "assets"
		assets.mkdir()
		payload = b"glTF\x02\x00\x00\x00\x20\x00\x00\x00"
		(assets / "model.gzip").write_bytes(gzip.compress(payload))
		(assets / "model.bzip").write_bytes(bz2.compress(payload))
		(assets / "model.xzip").write_bytes(lzma.compress(payload))
		(assets / "ordinary.gzip").write_bytes(gzip.compress(b"ordinary 2D notes"))
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.model_archive_files), {
			"assets/model.bzip", "assets/model.gzip", "assets/model.xzip",
		})
		for relative in inventory.model_archive_files:
			self.assertEqual(
				inventory.model_archive_files[relative]["model_members"],
				["<compressed-model-signature>"])
		self.assertNotIn("assets/ordinary.gzip", inventory.model_archive_files)
		oversized = assets / "oversized.gzip"
		oversized.write_bytes(gzip.compress(bytes(range(256)) * 64))
		with mock.patch.object(game_2d, "ARCHIVE_SNIFF_BUDGET", 128):
			evidence = game_2d._model_archive_evidence(oversized)
		self.assertIsNotNone(evidence)
		self.assertTrue(any(
			member in {
				"<compressed-payload-review-required>",
				"<compressed-payload-budget-exceeded>",
			}
			for member in evidence["model_members"]))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_truncated_compression_never_crashes_and_is_review_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		assets = root / "assets"
		assets.mkdir()
		for name, payload in {
			"bad.payload": b"\x1f\x8bBAD",
			"bad.bzip": b"BZhBAD",
			"bad.xzip": b"\xfd7zXZ\x00BAD",
			"bad.tar.gz": b"\x1f\x8bBAD",
			"bad.tgz": b"\x1f\x8b",
		}.items():
			(assets / name).write_bytes(payload)
		inventory = game_2d.discover(root)
		self.assertEqual(set(inventory.model_archive_files), {
			"assets/bad.bzip", "assets/bad.payload", "assets/bad.tar.gz",
			"assets/bad.tgz", "assets/bad.xzip",
		})
		for evidence in inventory.model_archive_files.values():
			self.assertTrue(any(
				"review-required" in member
				for member in evidence["model_members"]))
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_git_worktree_active_untracked_sidecar_and_magic_model_are_debt(self) -> None:
		temp = tempfile.TemporaryDirectory(prefix="test-game-2d-untracked-active-")
		self.addCleanup(temp.cleanup)
		root = Path(temp.name)
		subprocess.run(
			["git", "-C", str(root), "init", "-q"], check=True,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		)
		manifest = root / game_2d.DEFAULT_MANIFEST
		game_2d._write_manifest(manifest, game_2d.discover(root))
		(root / "assets").mkdir()
		(root / "assets/ghost.glb.import").write_text("[remap]\n", encoding="utf-8")
		(root / "assets/disguised.bin").write_bytes(b"glTF\x02\x00\x00\x00")
		(root / "assets/live.json").write_text(
			'{"asset":{"version":"1.0"},"scenes":[]}\n', encoding="utf-8")
		(root / "assets/model.cache").write_bytes(b"BLENDER-v300")
		(root / ".gitignore").write_text("*.payload\n", encoding="utf-8")
		(root / "assets/ignored.payload").write_text(
			'{"asset":{"version":"2.0"},"meshes":[]}\n', encoding="utf-8")
		(root / "review").mkdir()
		(root / "review/.gdignore").write_text("", encoding="utf-8")
		(root / "review/hidden.payload").write_bytes(b"glTF\x02\x00\x00\x00")
		with zipfile.ZipFile(root / "assets/runtime.zip", "w") as archive:
			archive.writestr("payload.bin", b"glTF\x02\x00\x00\x00")
		(root / "assets/content.data.import").write_text(
			'[deps]\nsource_file="res://assets/hidden.glb"\n', encoding="utf-8")
		(root / "gen2").mkdir()
		(root / "gen2/untracked.GLB").write_bytes(b"model")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.model_files, ())
		self.assertEqual(
			inventory.active_export_model_files,
			(
				"assets/disguised.bin", "assets/ignored.payload",
				"assets/live.json", "assets/model.cache",
			))
		self.assertNotIn("review/hidden.payload", inventory.active_export_model_files)
		self.assertEqual(inventory.model_import_sidecars, ())
		self.assertIn("assets/runtime.zip", inventory.model_archive_files)
		self.assertEqual(
			inventory.active_untracked_model_import_sidecars,
			("assets/content.data.import", "assets/ghost.glb.import"),
		)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D101", self.finding_ids(result))
		self.assertNotEqual(game_2d.exit_code(result, "strict"), 0)

	def test_root_and_addon_runtime_files_are_scanned(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "runtime.gd").write_text("extends Node3D\n", encoding="utf-8")
		(root / "root_world.tscn").write_text(
			'[gd_scene format=3]\n[node name="World" type="Node3D"]\n', encoding="utf-8")
		(root / "addons/live").mkdir(parents=True)
		(root / "addons/live/runtime.gd").write_text(
			"var camera: Camera3D\n", encoding="utf-8")
		(root / "addons/live/material.tres").write_text(
			'[gd_resource type="StandardMaterial3D" format=3]\n', encoding="utf-8")
		(root / "review").mkdir()
		(root / "review/.gdignore").write_text("", encoding="utf-8")
		(root / "review/old.gd").write_text("extends Node3D\n", encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(
			set(inventory.production_3d_files),
			{"runtime.gd", "addons/live/runtime.gd"},
		)
		self.assertEqual(
			set(inventory.scene_3d_files),
			{"root_world.tscn", "addons/live/material.tres"},
		)
		self.assertNotIn("review/old.gd", inventory.production_3d_files)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

	def test_existing_debt_file_cannot_gain_more_3d_api(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		path = root / "scripts/legacy.gd"
		path.write_text(
			path.read_text(encoding="utf-8") + "var camera: Camera3D\n",
			encoding="utf-8",
		)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D102", self.finding_ids(result))

	def test_same_path_model_replacement_cannot_be_rebaselined(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		initial_ceiling = document["initial_ceiling"]
		(root / "assets/legacy/prop.glb").write_bytes(b"other")
		changed = game_2d.audit(root, manifest)
		self.assertIn("G2D103", self.finding_ids(changed))
		game_2d._write_manifest(
			manifest, game_2d.discover(root), initial_ceiling=initial_ceiling)
		rebaselined = game_2d.audit(root, manifest)
		self.assertIn("G2D402", self.finding_ids(rebaselined))
		self.assertNotEqual(game_2d.exit_code(rebaselined, "regression-gate"), 0)

	def test_manifest_cannot_expand_to_bless_new_repository_debt(self) -> None:
		temp = tempfile.TemporaryDirectory(prefix="test-game-2d-history-")
		self.addCleanup(temp.cleanup)
		root = Path(temp.name)

		def git(*args: str) -> None:
			subprocess.run(
				["git", "-C", str(root), *args], check=True,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			)

		git("init", "-q")
		git("config", "user.email", "game-2d-test@example.invalid")
		git("config", "user.name", "Game 2D Test")
		(root / "assets/legacy").mkdir(parents=True)
		(root / "scripts").mkdir(parents=True)
		(root / "assets/legacy/prop.glb").write_bytes(b"model")
		(root / "scripts/legacy.gd").write_text("extends Node3D\n", encoding="utf-8")
		git("add", "assets", "scripts")
		manifest = root / game_2d.DEFAULT_MANIFEST
		game_2d._write_manifest(manifest, game_2d.discover(root))
		git("add", game_2d.DEFAULT_MANIFEST)
		git("commit", "-q", "-m", "baseline")

		(root / "gen2/meshy").mkdir(parents=True)
		(root / "gen2/meshy/new_source.glb").write_bytes(b"new model")
		git("add", "gen2/meshy/new_source.glb")
		game_2d._write_manifest(manifest, game_2d.discover(root))
		git("add", game_2d.DEFAULT_MANIFEST)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D401", self.finding_ids(result))
		self.assertNotEqual(game_2d.exit_code(result, "regression-gate"), 0)

	def test_expansion_stays_red_after_an_unrelated_commit(self) -> None:
		temp = tempfile.TemporaryDirectory(prefix="test-game-2d-history-sticky-")
		self.addCleanup(temp.cleanup)
		root = Path(temp.name)

		def git(*args: str) -> None:
			subprocess.run(
				["git", "-C", str(root), *args], check=True,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			)

		git("init", "-q")
		git("config", "user.email", "game-2d-test@example.invalid")
		git("config", "user.name", "Game 2D Test")
		(root / "assets").mkdir()
		(root / "assets/original.glb").write_bytes(b"model")
		git("add", "assets/original.glb")
		manifest = root / game_2d.DEFAULT_MANIFEST
		game_2d._write_manifest(manifest, game_2d.discover(root))
		git("add", game_2d.DEFAULT_MANIFEST)
		git("commit", "-q", "-m", "immutable baseline")

		(root / "assets/expanded.glb").write_bytes(b"model")
		git("add", "assets/expanded.glb")
		game_2d._write_manifest(manifest, game_2d.discover(root))
		git("add", game_2d.DEFAULT_MANIFEST)
		git("commit", "-q", "-m", "invalid expansion")
		(root / "README.txt").write_text("unrelated\n", encoding="utf-8")
		git("add", "README.txt")
		git("commit", "-q", "-m", "unrelated follow-up")

		result = game_2d.audit(root, manifest)
		self.assertIn("G2D401", self.finding_ids(result))
		self.assertNotEqual(game_2d.exit_code(result, "regression-gate"), 0)

	def test_initial_ceiling_hash_detects_tampering(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		document["initial_ceiling"]["model_files"].append("assets/injected.glb")
		document["initial_ceiling"]["declared_counts"]["model_files"] += 1
		self.write_manifest(manifest, document)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D004", self.finding_ids(result))
		self.assertNotEqual(game_2d.exit_code(result, "regression-gate"), 0)

	def test_duplicate_json_keys_are_rejected_and_refresh_cannot_splice_them(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		text = manifest.read_text(encoding="utf-8")
		text = text.replace(
			'"initial_ceiling": {',
			'"initial_ceiling": {},\n  "initial_ceiling": {',
			1,
		)
		manifest.write_text(text, encoding="utf-8")
		before = manifest.read_bytes()
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D001", self.finding_ids(result))
		self.assertTrue(any(
			"duplicate JSON key" in finding.detail for finding in result.findings))
		ok, findings = game_2d.refresh_manifest(root, manifest)
		self.assertFalse(ok)
		self.assertTrue(any("duplicate JSON key" in finding.detail for finding in findings))
		self.assertEqual(manifest.read_bytes(), before)

	def test_initial_ceiling_rejects_expansion_in_depth_one_clone(self) -> None:
		temp = tempfile.TemporaryDirectory(prefix="test-game-2d-shallow-source-")
		clone_temp = tempfile.TemporaryDirectory(prefix="test-game-2d-shallow-clone-")
		self.addCleanup(temp.cleanup)
		self.addCleanup(clone_temp.cleanup)
		root = Path(temp.name)

		def git(repository: Path, *args: str) -> subprocess.CompletedProcess:
			return subprocess.run(
				["git", "-C", str(repository), *args], check=True,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			)

		git(root, "init", "-q")
		git(root, "config", "user.email", "game-2d-test@example.invalid")
		git(root, "config", "user.name", "Game 2D Test")
		(root / "assets").mkdir()
		(root / "assets/original.glb").write_bytes(b"model")
		git(root, "add", "assets/original.glb")
		manifest = root / game_2d.DEFAULT_MANIFEST
		game_2d._write_manifest(manifest, game_2d.discover(root))
		initial_anchor = self.read_manifest(manifest)["initial_ceiling"]["canonical_sha256"]
		git(root, "add", game_2d.DEFAULT_MANIFEST)
		git(root, "commit", "-q", "-m", "initial ceiling")

		(root / "assets/expanded.glb").write_bytes(b"model")
		git(root, "add", "assets/expanded.glb")
		# Simulate laundering both the live inventory and its self-consistent
		# embedded ceiling/hash.  Only the external literal trust anchor survives.
		game_2d._write_manifest(manifest, game_2d.discover(root))
		git(root, "add", game_2d.DEFAULT_MANIFEST)
		git(root, "commit", "-q", "-m", "invalid expansion")
		(root / "README.txt").write_text("unrelated\n", encoding="utf-8")
		git(root, "add", "README.txt")
		git(root, "commit", "-q", "-m", "unrelated follow-up")

		clone = Path(clone_temp.name) / "clone"
		subprocess.run(
			["git", "clone", "-q", "--depth", "1", root.as_uri(), str(clone)],
			check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		)
		self.assertEqual(
			git(clone, "rev-parse", "--is-shallow-repository").stdout.strip(), b"true")
		result = game_2d.audit(
			clone, clone / game_2d.DEFAULT_MANIFEST,
			initial_ceiling_anchor=initial_anchor,
		)
		self.assertIn("G2D005", self.finding_ids(result))
		self.assertIn("G2D403", self.finding_ids(result))
		self.assertNotEqual(game_2d.exit_code(result, "regression-gate"), 0)
		clone_anchor = self.read_manifest(
			clone / game_2d.DEFAULT_MANIFEST)["initial_ceiling"]["canonical_sha256"]
		ok, refresh_findings = game_2d.refresh_manifest(
			clone, clone / game_2d.DEFAULT_MANIFEST,
			initial_ceiling_anchor=clone_anchor,
		)
		self.assertFalse(ok)
		self.assertTrue(any(
			"shallow repository refused" in finding.detail
			for finding in refresh_findings), refresh_findings)

	def test_refresh_manifest_allows_only_shrink_and_preserves_ceiling_bytes(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		before = manifest.read_text(encoding="utf-8")
		start, end = game_2d._json_object_member_span(before, "initial_ceiling")
		ceiling_bytes = before[start:end]
		anchor = self.read_manifest(manifest)["initial_ceiling"]["canonical_sha256"]
		(root / "assets/legacy/prop.glb").unlink()
		(root / "assets/legacy/prop.glb.import").unlink()
		ok, findings = game_2d.refresh_manifest(
			root, manifest, initial_ceiling_anchor=anchor)
		self.assertTrue(ok, findings)
		after = manifest.read_text(encoding="utf-8")
		new_start, new_end = game_2d._json_object_member_span(after, "initial_ceiling")
		self.assertEqual(after[new_start:new_end], ceiling_bytes)
		document = self.read_manifest(manifest)
		self.assertNotIn("assets/legacy/prop.glb", document["model_files"])
		self.assertNotIn("assets/legacy/prop.glb.import", document["model_import_sidecars"])
		self.assertEqual(document["archive_now_model_files"], [])
		self.assertTrue(game_2d.audit(root, manifest).exact)
		self.assertEqual(list(manifest.parent.glob(manifest.name + ".*.tmp")), [])

	def test_refresh_preserves_top_level_ceiling_not_nested_metadata_key(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		document["metadata"]["initial_ceiling"] = {"decoy": True}
		manifest.write_text(
			json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
		before = manifest.read_text(encoding="utf-8")
		start, end = game_2d._json_object_member_span(before, "initial_ceiling")
		ceiling_bytes = before[start:end]
		self.assertNotEqual(json.loads(ceiling_bytes), {"decoy": True})
		anchor = document["initial_ceiling"]["canonical_sha256"]
		(root / "assets/legacy/prop.glb").unlink()
		(root / "assets/legacy/prop.glb.import").unlink()
		ok, findings = game_2d.refresh_manifest(
			root, manifest, initial_ceiling_anchor=anchor)
		self.assertTrue(ok, findings)
		after = manifest.read_text(encoding="utf-8")
		new_start, new_end = game_2d._json_object_member_span(after, "initial_ceiling")
		self.assertEqual(after[new_start:new_end], ceiling_bytes)
		self.assertEqual(self.read_manifest(manifest)["metadata"]["initial_ceiling"], {"decoy": True})

	def test_refresh_cannot_reintroduce_debt_removed_in_git_history(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)

		def git(*args: str) -> None:
			subprocess.run(
				["git", "-C", str(root), *args], check=True,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			)

		git("init", "-q")
		git("config", "user.email", "game-2d-test@example.invalid")
		git("config", "user.name", "Game 2D Test")
		anchor = self.read_manifest(manifest)["initial_ceiling"]["canonical_sha256"]
		old_manifest = manifest.read_bytes()
		old_model = (root / "assets/legacy/prop.glb").read_bytes()
		old_sidecar = (root / "assets/legacy/prop.glb.import").read_bytes()
		git("add", ".")
		git("commit", "-q", "-m", "baseline")
		(root / "assets/legacy/prop.glb").unlink()
		(root / "assets/legacy/prop.glb.import").unlink()
		git("add", "-u")
		ok, findings = game_2d.refresh_manifest(
			root, manifest, initial_ceiling_anchor=anchor)
		self.assertTrue(ok, findings)
		git("add", ".")
		git("commit", "-q", "-m", "shrink")
		manifest.write_bytes(old_manifest)
		(root / "assets/legacy/prop.glb").write_bytes(old_model)
		(root / "assets/legacy/prop.glb.import").write_bytes(old_sidecar)
		git("add", "assets/legacy/prop.glb", "assets/legacy/prop.glb.import")
		before = manifest.read_bytes()
		ok, findings = game_2d.refresh_manifest(
			root, manifest, initial_ceiling_anchor=anchor)
		self.assertFalse(ok)
		self.assertTrue(
			any(finding.check_id == "G2D401" for finding in findings), findings)
		self.assertEqual(manifest.read_bytes(), before)

	def test_refresh_manifest_refuses_path_token_and_fingerprint_growth(self) -> None:
		for mutation in ("path", "token", "fingerprint"):
			with self.subTest(mutation=mutation):
				temp, root, manifest = self.fixture()
				self.addCleanup(temp.cleanup)
				anchor = self.read_manifest(manifest)["initial_ceiling"]["canonical_sha256"]
				if mutation == "path":
					(root / "assets/legacy/new.glb").write_bytes(b"new")
				elif mutation == "token":
					path = root / "scripts/legacy.gd"
					path.write_text(
						path.read_text(encoding="utf-8") + "var camera: Camera3D\n",
						encoding="utf-8")
				else:
					(root / "assets/legacy/prop.glb").write_bytes(b"replacement")
				before = manifest.read_bytes()
				ok, findings = game_2d.refresh_manifest(
					root, manifest, initial_ceiling_anchor=anchor)
				self.assertFalse(ok)
				self.assertTrue(findings)
				self.assertEqual(manifest.read_bytes(), before)

	def test_refresh_manifest_refuses_anchor_or_archive_ceiling_rewrite(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		before = manifest.read_bytes()
		ok, findings = game_2d.refresh_manifest(
			root, manifest, initial_ceiling_anchor="0" * 64)
		self.assertFalse(ok)
		self.assertTrue(findings)
		self.assertEqual(manifest.read_bytes(), before)

		document = self.read_manifest(manifest)
		document["archive_now_model_files"] = ["assets/legacy/prop.glb"]
		document["declared_counts"]["archive_now_model_files"] = 1
		self.write_manifest(manifest, document)
		tampered = manifest.read_bytes()
		anchor = document["initial_ceiling"]["canonical_sha256"]
		ok, findings = game_2d.refresh_manifest(
			root, manifest, initial_ceiling_anchor=anchor)
		self.assertFalse(ok)
		self.assertTrue(any(finding.check_id == "G2D401" for finding in findings))
		self.assertEqual(manifest.read_bytes(), tampered)

	def test_missing_manifest_entry_cannot_create_false_green(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		document["model_files"] = []
		document["declared_counts"]["model_files"] = 0
		self.write_manifest(manifest, document)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D101", self.finding_ids(result))
		self.assertFalse(result.exact)

	def test_false_empty_manifest_fails_when_tree_has_debt(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		game_2d._write_manifest(manifest, game_2d.Inventory())
		result = game_2d.audit(root, manifest)
		self.assertTrue(result.findings)
		self.assertFalse(result.satisfied)
		self.assertNotEqual(game_2d.exit_code(result, "regression-gate"), 0)

	def test_removed_model_requires_manifest_to_shrink_same_change(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "assets/legacy/prop.glb").unlink()
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D201", self.finding_ids(result))

	def test_reduced_token_count_requires_manifest_to_shrink(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/legacy.gd").write_text("extends Node3D\n", encoding="utf-8")
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D202", self.finding_ids(result))

	def test_archive_now_entry_must_be_model_debt_subset(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		document["archive_now_model_files"] = ["assets/not-present.glb"]
		document["declared_counts"]["archive_now_model_files"] = 1
		self.write_manifest(manifest, document)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D002", self.finding_ids(result))

	def test_archive_now_list_cannot_expand_beyond_initial_ceiling(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		game_2d._write_manifest(
			manifest,
			game_2d.discover(root),
			["assets/legacy/prop.glb"],
			initial_ceiling=document["initial_ceiling"],
		)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D401", self.finding_ids(result))

	def test_archive_now_entry_cannot_have_exact_production_reference(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/loader.gd").write_text(
			'var prop = load("res://assets/legacy/prop.glb")\n', encoding="utf-8")
		game_2d._write_manifest(
			manifest,
			game_2d.discover(root),
			["assets/legacy/prop.glb"],
		)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D301", self.finding_ids(result))

	def test_archive_now_entry_cannot_have_exact_scene_reference(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scenes/prop.tscn").write_text(
			'[gd_scene load_steps=2 format=3]\n'
			'[ext_resource type="PackedScene" path="res://assets/legacy/prop.glb" id="1"]\n',
			encoding="utf-8",
		)
		game_2d._write_manifest(
			manifest,
			game_2d.discover(root),
			["assets/legacy/prop.glb"],
		)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D301", self.finding_ids(result))

	def test_archive_now_entry_cannot_hide_behind_concatenated_extension(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/loader.gd").write_text(
			'const DIR = "res://assets/legacy/"\n'
			'const NAME = "prop"\nvar prop = load(DIR + NAME + ".glb")\n',
			encoding="utf-8",
		)
		game_2d._write_manifest(
			manifest,
			game_2d.discover(root),
			["assets/legacy/prop.glb"],
		)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D301", self.finding_ids(result))

	def test_archive_now_cross_file_split_reference_is_rejected(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/loader.gd").write_text(
			'const DIR = "res://assets/legacy/"\nfunc load_named(name): return load(DIR + name)\n',
			encoding="utf-8",
		)
		(root / "scripts/caller.gd").write_text(
			'const MODEL_NAME = "prop.glb"\n', encoding="utf-8")
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		self.assertIn("G2D301", self.finding_ids(game_2d.audit(root, manifest)))

	def test_archive_now_runtime_json_and_data_paths_are_rejected(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "assets/runtime_catalog.json").write_text(
			'{"model":"res://assets/legacy/prop.glb"}\n', encoding="utf-8")
		(root / "assets/runtime_catalog.data").write_text(
			"assets/legacy/prop.glb\n", encoding="utf-8")
		(root / "data").mkdir()
		(root / "data/runtime_catalog.xml").write_text(
			'<model src="res://assets/legacy/prop.glb"/>\n', encoding="utf-8")
		# Provenance/review catalogs are not runtime dependencies.
		(root / "art_library").mkdir()
		(root / "art_library/ART_INVENTORY.csv").write_text(
			"assets/legacy/prop.glb,deprecated\n", encoding="utf-8")
		(root / "assets/provenance").mkdir()
		(root / "assets/provenance/retired.json").write_text(
			'{"retired":"assets/legacy/prop.glb"}\n', encoding="utf-8")
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		details = [finding.detail for finding in result.findings if finding.check_id == "G2D301"]
		self.assertTrue(any("assets/runtime_catalog.json" in detail for detail in details))
		self.assertTrue(any("assets/runtime_catalog.data" in detail for detail in details))
		self.assertTrue(any("data/runtime_catalog.xml" in detail for detail in details))
		self.assertFalse(any("art_library" in detail for detail in details))
		self.assertFalse(any("assets/provenance" in detail for detail in details))

	def test_archive_now_active_archive_data_code_and_nested_content_block(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		nested_bytes = io.BytesIO()
		with zipfile.ZipFile(nested_bytes, "w") as nested:
			nested.writestr(
				"catalog.json", '{"model":"res://assets/legacy/prop.glb"}')
		path = root / "assets/runtime_bundle.zip"
		with zipfile.ZipFile(path, "w") as archive:
			archive.writestr(
				"catalog.json", '{"model":"res://assets/legacy/prop.glb"}')
			archive.writestr(
				"loader.gd", 'var model = load("res://assets/legacy/prop.glb")\n')
			archive.writestr("nested.payload", nested_bytes.getvalue())
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D301", self.finding_ids(result))
		self.assertIn("G2D302", self.finding_ids(result))

	def test_archive_now_directory_iterator_and_dynamic_name_loader_block(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/loader.gd").write_text(
			'const DIR = "res://assets/legacy/"\nconst EXT = ".glb"\n'
			'const GLOBAL_DIR = ProjectSettings.globalize_path(DIR)\n'
			'func load_named(name): return load(DIR + name + EXT)\n'
			'func load_exact(): return ResourceLoader.load('
			'String(DIR + "prop" + EXT), "", ResourceLoader.CACHE_MODE_IGNORE)\n'
			'func list_models(): return DirAccess.get_files_at('
			'ProjectSettings.globalize_path(DIR))\n'
			'func open_models(): return DirAccess.open(GLOBAL_DIR)\n',
			encoding="utf-8")
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		details = [finding.detail for finding in result.findings if finding.check_id == "G2D301"]
		self.assertTrue(any("enumerated dynamically" in detail for detail in details))
		self.assertTrue(any("dynamic directory/name loader" in detail for detail in details))

	def test_archive_now_percent_format_and_path_join_loaders_block(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		text = (
			'const DIR = "res://assets/legacy/"\nconst EXT = ".glb"\n'
			'func percent(name): return load("res://assets/legacy/%s.glb" % name)\n'
			'func formatted(name): return ResourceLoader.load('
			'"res://assets/legacy/{name}.glb".format({"name": name}))\n'
			"func joined(name): return load(DIR.path_join(name + EXT))\n"
		)
		(root / "scripts/loader.gd").write_text(text, encoding="utf-8")
		self.assertEqual(
			game_2d._dynamic_model_load_patterns(
				text, game_2d._simple_string_assignments(text)),
			{("assets/legacy", ".glb")},
		)
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		self.assertTrue(any(
			finding.check_id == "G2D301"
			and "dynamic directory/name loader" in finding.detail
			for finding in result.findings), result.findings)

	def test_archive_now_stem_does_not_match_longer_2d_sibling(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/loader.gd").write_text(
			'var picture = load("res://assets/legacy/propeller.png")\n',
			encoding="utf-8",
		)
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		self.assertFalse(any(
			finding.check_id == "G2D301" for finding in result.findings),
			result.findings)

	def test_archive_now_inspects_and_fails_closed_on_opaque_runtime_packages(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "addons/live").mkdir(parents=True)
		needle = b"res://assets/legacy/prop.glb\x00"
		(root / "addons/live/plugin.so").write_bytes(b"ELF\x00" + needle)
		with zipfile.ZipFile(root / "addons/live/plugin.jar", "w") as archive:
			archive.writestr("Plugin.class", b"bytecode\x00" + needle)
		with zipfile.ZipFile(root / "addons/live/plugin.aar", "w") as archive:
			archive.writestr("classes.dex", b"dex\x00" + needle)
		(root / "assets/content.pck").write_bytes(b"GDPC\x00" + needle)
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		result = game_2d.audit(root, manifest)
		details = [
			finding.detail for finding in result.findings
			if finding.check_id == "G2D301"]
		for source in ("plugin.so", "plugin.jar", "plugin.aar", "content.pck"):
			with self.subTest(source=source):
				self.assertTrue(any(source in detail for detail in details), details)
		self.assertIn("G2D302", self.finding_ids(result))

	def test_archive_now_is_blocked_by_opaque_binary_scene(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scenes/hidden.scn").write_bytes(b"RSRC opaque dependency")
		game_2d._write_manifest(
			manifest, game_2d.discover(root), ["assets/legacy/prop.glb"])
		self.assertIn("G2D302", self.finding_ids(game_2d.audit(root, manifest)))

	def test_non_active_model_sources_remain_repository_wide_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		for relative in (
			"assets_src/blender/source.blend",
			"backups/legacy.glb",
			"gen2/meshy/static.glb",
			"tools/out/rig.glb",
			"assets/_staging/review.glb",
			"tools/out/rig.blend1",
		):
			path = root / relative
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_bytes(b"archive source")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.active_export_model_files, ())
		self.assertEqual(len(inventory.model_files), 6)
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))
		game_2d._write_manifest(manifest, inventory)
		result = game_2d.audit(root, manifest)
		self.assertTrue(result.exact)
		self.assertFalse(result.satisfied)
		self.assertNotEqual(game_2d.exit_code(result, "strict"), 0)

	def test_probe_3d_api_is_separate_strict_debt(self) -> None:
		temp, root, manifest = self.fixture(with_debt=False)
		self.addCleanup(temp.cleanup)
		(root / "scripts/probe_future.gd").write_text(
			"extends Node3D\n", encoding="utf-8")
		inventory = game_2d.discover(root)
		self.assertEqual(inventory.production_3d_files, {})
		self.assertEqual(set(inventory.probe_3d_files), {"scripts/probe_future.gd"})
		self.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))
		game_2d._write_manifest(manifest, inventory)
		self.assertNotEqual(
			game_2d.exit_code(game_2d.audit(root, manifest), "strict"), 0)

	def test_manifest_paths_and_counts_are_canonical(self) -> None:
		temp, root, manifest = self.fixture()
		self.addCleanup(temp.cleanup)
		document = self.read_manifest(manifest)
		document["model_files"] = [
			"assets/z.glb", "assets/legacy/prop.glb", "assets/z.glb",
		]
		document["declared_counts"]["model_files"] = 3
		self.write_manifest(manifest, document)
		result = game_2d.audit(root, manifest)
		self.assertIn("G2D001", self.finding_ids(result))

	def test_stress_harness_is_green(self) -> None:
		self.assertEqual(game_2d.stress(), 0)


if __name__ == "__main__":
	unittest.main()
