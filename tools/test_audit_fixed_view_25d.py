#!/usr/bin/env python3
"""Mutation tests for the fixed-view audit contract."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


class FixedViewAuditMutations(unittest.TestCase):
	def run_audit(self, source: str, mutation: str = "") -> int:
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			(root / "scripts").mkdir()
			(root / "scripts" / "authority.gd").write_text(source + mutation, encoding="utf-8")
			manifest = {
				"legacy_2d_paths": [],
				"strict_25d_paths": ["scripts/authority.gd"],
				"legacy_baseline": {
					"camera_mutation": {"count": 0, "paths_sha256": EMPTY_SHA},
					"model_resource": {"count": 0, "paths_sha256": EMPTY_SHA},
					"spatial_physics": {"count": 0, "paths_sha256": EMPTY_SHA},
					"sprite2d_world": {"count": 0, "paths_sha256": EMPTY_SHA},
					"camera2d_world": {"count": 0, "paths_sha256": EMPTY_SHA},
				},
				"strict_authority_groups": [{
					"id": "test",
					"paths": ["scripts/authority.gd"],
					"required_constructors": ["Node3D.new()", "Camera3D.new()", "Sprite3D.new()"],
					"required_touch_tokens": ["camera_ray", "Plane", "screen_position"],
					"forbidden_runtime_mutations": [r"func\s+_(?:process|physics_process|input|unhandled_input)[\s\S]{0,1200}?(?:camera|cam)\.(?:rotation|rotation_degrees|fov|size|projection)\s*="]
				}],
				"rooms": {},
			}
			manifest_path = root / "manifest.json"
			manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
			tool = Path(__file__).with_name("audit_fixed_view_25d.py")
			return subprocess.run([sys.executable, str(tool), "--root", str(root), "--manifest", str(manifest_path)], capture_output=True, text=True).returncode

	def test_valid_fixed_projection_passes(self) -> None:
		source = "Node3D.new() Camera3D.new() Sprite3D.new() camera_ray Plane screen_position"
		self.assertEqual(self.run_audit(source), 0)

	def test_unused_sprite2d_factory_fails_missing_sprite3d(self) -> None:
		source = "Node3D.new() Camera3D.new() Sprite2D.new() camera_ray Plane screen_position"
		self.assertNotEqual(self.run_audit(source), 0)

	def test_mesh_in_strict_stage_fails(self) -> None:
		source = "Node3D.new() Camera3D.new() Sprite3D.new() MeshInstance3D.new() camera_ray Plane screen_position"
		self.assertNotEqual(self.run_audit(source), 0)

	def test_camera_mutation_in_tick_fails(self) -> None:
		source = "Node3D.new() Camera3D.new() Sprite3D.new() camera_ray Plane screen_position\nfunc _process(_delta):\n\tcamera.fov = 60.0"
		self.assertNotEqual(self.run_audit(source), 0)


if __name__ == "__main__":
	unittest.main()
