import json
from pathlib import Path
import shutil
import tempfile
import subprocess
import unittest
from unittest.mock import patch
from tools import audit_game_2d as audit

ROOT = Path(__file__).resolve().parents[2]

class GodotMCPScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'addons/godot_mcp', self.root / 'addons/godot_mcp', ignore=shutil.ignore_patterns('*.uid', '*.import'))
        (self.root / 'tools/godot_mcp').mkdir(parents=True)
        shutil.copyfile(ROOT / 'tools/godot_mcp/addon_manifest.json', self.root / 'tools/godot_mcp/addon_manifest.json')

    def test_exact_payload_only(self):
        approved = audit._approved_editor_tool_sources(self.root)
        self.assertIn('addons/godot_mcp/plugin.gd', approved)
        self.assertTrue(all(p.endswith('.gd') for p in approved))
        self.assertNotIn('scripts/main.gd', approved)

    def test_changed_payload_fails_closed(self):
        with (self.root / 'addons/godot_mcp/plugin.gd').open('a') as f:
            f.write('\n# changed\n')
        self.assertEqual(set(), audit._approved_editor_tool_sources(self.root))

    def test_new_payload_fails_closed(self):
        (self.root / 'addons/godot_mcp/new.gd').write_text('extends Node3D\n')
        self.assertEqual(set(), audit._approved_editor_tool_sources(self.root))

    def test_missing_payload_fails_closed(self):
        (self.root / 'addons/godot_mcp/plugin.gd').unlink()
        self.assertEqual(set(), audit._approved_editor_tool_sources(self.root))

    def test_rewritten_manifest_fails_closed(self):
        (self.root / 'tools/godot_mcp/addon_manifest.json').write_text('{"files":{}}')
        self.assertEqual(set(), audit._approved_editor_tool_sources(self.root))

    def test_real_inventory_preserves_game_and_model_detection(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        clean = audit.discover(self.root)
        self.assertFalse(clean.production_3d_files)
        self.assertIn('addons/godot_mcp/game_bridge/mcp_game_bridge.gd', clean.reviewed_tooling_3d_files)
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/game.gd').write_text('extends Node3D\n')
        game = audit.discover(self.root)
        self.assertIn('scripts/game.gd', game.production_3d_files)
        (self.root / 'addons/godot_mcp/new_model.gltf').write_text('{"asset":{"version":"2.0"},"nodes":[]}')
        changed = audit.discover(self.root)
        self.assertIn('addons/godot_mcp/new_model.gltf', changed.active_export_model_files)
        self.assertIn('addons/godot_mcp/game_bridge/mcp_game_bridge.gd', changed.production_3d_files)

    def test_game_spatial_code_still_detected(self):
        self.assertTrue(audit._token_counts('extends Node3D\nvar position: Vector3\n'))


    def test_payload_changed_after_approval_is_not_reviewed(self):
        relative = 'addons/godot_mcp/commands/selection_commands.gd'
        victim = self.root / relative
        original = audit._approved_editor_tool_sources

        def change_after_approval(root):
            approved = original(root)
            self.assertIn(relative, approved)
            victim.write_bytes(victim.read_bytes() + b'\n# concurrent mutation\n')
            return approved

        with patch.object(audit, '_approved_editor_tool_sources', side_effect=change_after_approval):
            pinned = audit._reviewed_tooling_hashes(self.root)
        self.assertFalse(audit._is_reviewed_tooling(victim, self.root, pinned))

    def test_manifest_changed_after_approval_is_not_reviewed(self):
        relative = 'addons/godot_mcp/commands/selection_commands.gd'
        original = audit._approved_editor_tool_sources

        def change_after_approval(root):
            approved = original(root)
            self.assertIn(relative, approved)
            (self.root / 'tools/godot_mcp/addon_manifest.json').write_text('{"files":{}}')
            return approved

        with patch.object(audit, '_approved_editor_tool_sources', side_effect=change_after_approval):
            pinned = audit._reviewed_tooling_hashes(self.root)
        self.assertFalse(pinned)
        self.assertFalse(audit._is_reviewed_tooling(self.root / relative, self.root, pinned))

if __name__ == '__main__':
    unittest.main()
