from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import audit_roshan_2d as audit_2d  # noqa: E402


class Roshan2DAuditTests(unittest.TestCase):
	def fixture(self) -> tuple[tempfile.TemporaryDirectory, Path]:
		temp = tempfile.TemporaryDirectory(prefix="test-roshan-2d-")
		root = Path(temp.name)
		audit_2d._write_fixture(root)
		return temp, root

	def test_clean_fixture_passes(self) -> None:
		temp, root = self.fixture()
		self.addCleanup(temp.cleanup)
		self.assertEqual(audit_2d.audit(root), [])

	def test_model_in_roshan_directory_fails_even_with_generic_filename(self) -> None:
		temp, root = self.fixture()
		self.addCleanup(temp.cleanup)
		model = root / "gen2/meshy/roshan_candidate/static.glb"
		model.parent.mkdir(parents=True)
		model.write_bytes(b"model")
		self.assertIn("R2D001", {issue.check_id for issue in audit_2d.audit(root)})

	def test_runtime_load_without_file_still_fails(self) -> None:
		temp, root = self.fixture()
		self.addCleanup(temp.cleanup)
		(root / "scripts/load_old.gd").write_text(
			'var model = load("res://assets/characters/roshan_v9.glb")\n',
			encoding="utf-8",
		)
		self.assertIn("R2D002", {issue.check_id for issue in audit_2d.audit(root)})

	def test_decommissioned_branch_layout_is_outside_active_scope(self) -> None:
		temp, root = self.fixture()
		self.addCleanup(temp.cleanup)
		model = root / "decommissioned/data/roshan-3d-character/roshan_v4.glb"
		model.parent.mkdir(parents=True)
		model.write_bytes(b"archived")
		self.assertEqual(audit_2d.audit(root), [])

	def test_linked_worktree_is_outside_active_checkout_scope(self) -> None:
		temp, root = self.fixture()
		self.addCleanup(temp.cleanup)
		gitdir = root / ".git/worktrees/other"
		gitdir.mkdir(parents=True)
		worktree = root / ".worktrees/other"
		worktree.mkdir(parents=True)
		(worktree / ".git").write_text(f"gitdir: {gitdir}\n", encoding="utf-8")
		model = worktree / "assets/characters/roshan_v4.glb"
		model.parent.mkdir(parents=True)
		model.write_bytes(b"other checkout")
		self.assertEqual(audit_2d.audit(root), [])

	def test_decoy_worktree_marker_cannot_hide_active_model(self) -> None:
		temp, root = self.fixture()
		self.addCleanup(temp.cleanup)
		worktree = root / ".worktrees/decoy"
		worktree.mkdir(parents=True)
		(worktree / ".git").write_text("gitdir: C:/unrelated/repository\n", encoding="utf-8")
		model = worktree / "assets/characters/roshan_v4.glb"
		model.parent.mkdir(parents=True)
		model.write_bytes(b"active decoy")
		self.assertIn("R2D001", {issue.check_id for issue in audit_2d.audit(root)})

	def test_stress_harness_is_green(self) -> None:
		self.assertEqual(audit_2d.stress(), 0)


if __name__ == "__main__":
	unittest.main()
