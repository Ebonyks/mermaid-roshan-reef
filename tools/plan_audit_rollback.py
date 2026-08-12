#!/usr/bin/env python3
"""Print conservative, branch-based rollback plans for the master audit.

This helper is deliberately read-only.  It does not inspect, switch, restore,
revert, stage, or commit a Git worktree.  ``--emit-script`` only writes a shell
script to stdout, and is available solely for the catalog entries whose inverse
is bounded enough to review mechanically.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from typing import Sequence


AUDIT_BASELINE_COMMIT = "4ba20414a3fdbb771c3635a43cee66c850a49515"
AUDIT_INTEGRATION_COMMIT = "ad36ee9ffe4eae4d5c4183d0546d775de0218213"
AUDIT_INTEGRATION_PARENT = "7b5d1209063a22002118c364767d537b34b3dc6f"
AUDIT_UPSTREAM_PARENT = "245c16137fae82271dabac456d5ab04d843463a8"
AUDIT_CATALOG_COMMIT = "dacef1405b6a8cb470117e824aebac3a8ca500af"
AUDIT_RECONCILIATION_COMMIT = "f3b0de078898a8b4faddb2c738c4403180eff928"
AUDIT_RECONCILIATION_PARENT = "ea6185fdb1a687a20a6d118bdc368400e2c30f60"
AUDIT_RECONCILIATION_AUDIT_PARENT = "5f58ef0a9db7aa9593f85131e1b855e51b84aea8"
GODOT_REQUIREMENT = "exact Godot 4.7.1-stable (not 4.4 or a development build)"
PROTECTED_PATHS = (
	"assets/book/",
	"assets/audio/voices/",
	"assets/characters/friends/",
)

MANUAL = "MANUAL_RECONSTRUCTION_REQUIRED"
REVIEWABLE = "REVIEWABLE_COMMIT_INVERSE"
MERGE_ALL = "ALL_OR_NOTHING_MERGE_INVERSE"


@dataclass(frozen=True)
class ChangeGroup:
	change_id: str
	title: str
	summary: str
	baseline_commit: str
	commits: tuple[str, ...]
	paths: tuple[str, ...]
	dependencies: tuple[str, ...]
	gates: tuple[str, ...]
	rollback_start: str = AUDIT_INTEGRATION_COMMIT
	warnings: tuple[str, ...] = ()
	safety: str = MANUAL
	manual_reason: str = ""
	pending_commit: bool = False
	all_or_nothing: bool = False
	revert_target: str = ""
	revert_mainline: int | None = None
	merge_parents: tuple[str, ...] = ()

	@property
	def branch_name(self) -> str:
		return f"codex/rollback-{self.change_id.lower()}"


def _group(
	change_id: str,
	title: str,
	summary: str,
	baseline_commit: str,
	commits: Sequence[str],
	paths: Sequence[str],
	dependencies: Sequence[str],
	gates: Sequence[str],
	*,
	rollback_start: str = AUDIT_INTEGRATION_COMMIT,
	warnings: Sequence[str] = (),
	safety: str = MANUAL,
	manual_reason: str = "",
	pending_commit: bool = False,
	all_or_nothing: bool = False,
	revert_target: str = "",
	revert_mainline: int | None = None,
	merge_parents: Sequence[str] = (),
) -> ChangeGroup:
	return ChangeGroup(
		change_id=change_id,
		title=title,
		summary=summary,
		baseline_commit=baseline_commit,
		commits=tuple(commits),
		paths=tuple(paths),
		dependencies=tuple(dependencies),
		gates=tuple(gates),
		rollback_start=rollback_start,
		warnings=tuple(warnings),
		safety=safety,
		manual_reason=manual_reason,
		pending_commit=pending_commit,
		all_or_nothing=all_or_nothing,
		revert_target=revert_target,
		revert_mainline=revert_mainline,
		merge_parents=tuple(merge_parents),
	)


# Stable catalog shared with the written change log. Commit ownership is
# intentionally unique: a commit belongs to one partial group only. CHG-022 and
# CHG-024 are separate historical umbrella merge inverses and each owns only its
# exact merge commit.
CATALOG: tuple[ChangeGroup, ...] = (
	_group(
		"CHG-001",
		"Roshan 2D contract and frame repair",
		"Removed active 3D Roshan payload/tooling, enforced the narrow 2D character contract, and repaired clipped playground art/settling.",
		AUDIT_BASELINE_COMMIT,
		(
			"3be5b44bfa196df8d321ac0606472300c1c8d049",
			"a1be9a1ecf0a6fc65396a8dd78ee10c8fbe35fde",
		),
		(
			"assets/characters/roshan_v3.glb",
			"assets/characters/roshan_v4.glb",
			"gen2/meshy/roshan_playable/",
			"gen2/meshy/roshan_v2/",
			"scripts/player.gd",
			"tools/audit_roshan_2d.py",
			"tools/tests/test_audit_roshan_2d.py",
			"assets/lagoon/playground/",
		),
		("CHG-008", "CHG-011"),
		(
			"python tools/audit_roshan_2d.py",
			"python -m unittest tools.tests.test_audit_roshan_2d",
			"\"$GODOT\" --headless -s scripts/probe_l2.gd",
		),
		manual_reason="The inverse would restore prohibited model payloads and obsolete rig tooling while later 2D authority and debt gates assume their absence.",
	),
	_group(
		"CHG-002",
		"Companion no-fail behavior and verification",
		"Removed inactivity loss/removal behavior and added patient waiting, legacy-save, passive, teardown, and re-entry coverage.",
		"3be5b44bfa196df8d321ac0606472300c1c8d049",
		(
			"0522d1faafa6e0ba13741b00187b8a873a1a7ab5",
			"f8efeb0a1a55d6e203e25ef0ee4738ef12bc22be",
		),
		(
			"STUFFIE_COMPANIONS.md",
			"scripts/companion.gd",
			"scripts/stuffie_battle.gd",
			"scripts/save_state.gd",
			"scripts/probe_stuffie.gd",
			"scripts/probe_load.gd",
		),
		(),
		(
			"\"$GODOT\" --headless -s scripts/probe_stuffie.gd",
			"\"$GODOT\" --headless -s scripts/probe_load.gd",
		),
		manual_reason="Reverting this slice can reintroduce a fail state for a four-year-old and therefore requires an explicit owner decision and a replacement no-fail design.",
	),
	_group(
		"CHG-003",
		"Child-access route, snowman targets, and playground visibility",
		"Enlarged snowman touch targets, added a voiced Lagoon-to-Reef route, and kept completion feedback on visible Roshan.",
		"0522d1faafa6e0ba13741b00187b8a873a1a7ab5",
		(
			"82f9828c5a478599668f2b019f53128ff084a73c",
			"986010c0bb3c8a018e774e420c62cccc3737a333",
			"711879ecf10fa7c8871abb1544248a49f38d9078",
			"e6e56f8b8c185b3efbc6583617eaad77c0b2108d",
		),
		(
			"scripts/games/picture_games.gd",
			"scripts/arena/sky_lagoon.gd",
			"scripts/pause_menu.gd",
			"scripts/probe_mg2d.gd",
			"scripts/probe_l2.gd",
			"scripts/probe_audit.gd",
		),
		("CHG-001", "CHG-004"),
		(
			"\"$GODOT\" --headless -s scripts/probe_mg2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_l2.gd",
		),
		manual_reason="This group contains accessibility and navigation repairs on shared gameplay files; an inverse must preserve one-finger reachability and a voiced route.",
	),
	_group(
		"CHG-004",
		"Voice and dialogue integrity",
		"Prevented duplicate or lingering speech, preserved Opera speaker identity on re-prompts, rejected shadowed cue keys, and bound brawl prompts to one voice cue.",
		"b50f2477f87b56ed16f1ca469fbf7b5848ead723",
		(
			"17813082951eefd8552c56cdda1bda61c8d1c87d",
			"c86d3a7d024ecac59900b8b8348c305e3493c10d",
			"8b5ca161a71f9bb7e709e4bc653d81be8445b077",
			"1c6e0c24799ab96a3e632f8202c8b6aa905185a4",
			"e8485d544c785548f855e55124af08dc4f15e277",
		),
		(
			"scripts/audio_director.gd",
			"scripts/main.gd",
			"scripts/opera_career_world_2d.gd",
			"scripts/stuffie_battle.gd",
			"scripts/probe_voice.gd",
			"tools/audit_voice_cues.py",
		),
		("CHG-003", "CHG-016"),
		(
			"\"$GODOT\" --headless -s scripts/probe_voice.gd",
			"\"$GODOT\" --headless -s scripts/probe_audio.gd",
			"\"$GODOT\" --headless -s scripts/probe_opera_2d.gd",
		),
		manual_reason="The commits touch shared dialogue state and protected-recording routing. Selective restoration risks duplicate, stale, or wrong-speaker speech.",
	),
	_group(
		"CHG-005",
		"Trusted probe parity and cross-platform CI",
		"Made local and remote trusted-probe coverage fail closed, kept the Windows grade gate portable, and placed downloaded Godot archives outside project debt scope.",
		"82f9828c5a478599668f2b019f53128ff084a73c",
		(
			"7e6d699dcad4e8e37e0fd8e47583354d77cd1876",
			"5c4b34f0f50693ce79d12fb455936453c324ae0c",
			"7b5d1209063a22002118c364767d537b34b3dc6f",
			"dacef1405b6a8cb470117e824aebac3a8ca500af",
		),
		(
			".github/workflows/probes.yml",
			"audit/MASTER_AUDIT_2026-08-09.md",
			"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",
			"scripts/ci.sh",
			"tools/audit_probe_parity.py",
			"tools/check_grade_headroom.py",
			"tools/tests/test_check_grade_headroom.py",
		),
		("CHG-008", "CHG-022"),
		(
			"python tools/audit_probe_parity.py",
			"python tools/audit_probe_parity.py --stress",
			"python -m unittest tools.tests.test_check_grade_headroom",
		),
		rollback_start=AUDIT_CATALOG_COMMIT,
		manual_reason="This is a high-risk workflow/CI enforcement change. Removing it can silently reduce remote coverage and must be replaced, not simply reverted.",
	),
	_group(
		"CHG-006",
		"Lagoon and visual-evidence measurements",
		"Made unresolved visual states explicit and corrected touch diameter, active-art, scene-congruency, and texture-residency measurements.",
		"711879ecf10fa7c8871abb1544248a49f38d9078",
		(
			"219fe59384d3af5f2b0993fda13054bdf91f6b25",
			"6e04706d686e1abdadd95c80195c5e2bf56c9c22",
			"09027504f2da30897cf219f91728994d0392eb13",
			"76c30a6699de3a8bb2b9699f2ec9aaf89d5c00b6",
		),
		(
			"tools/audit_visual_design.py",
			"tools/visual_audit_spec.json",
			"tools/check_grade_headroom.py",
			"tools/audit_cinematic.py",
			"scripts/probe_visual_audit.gd",
		),
		("CHG-014",),
		(
			"python -m unittest tools.tests.test_audit_visual_design",
			"python tools/audit_visual_design.py --stress",
			"python tools/audit_cinematic.py",
		),
		manual_reason="These commits evolve one evidence contract across shared specs and validators; reverting a subset can make false PASS results possible.",
	),
	_group(
		"CHG-007",
		"Canvas 2D feedback slices",
		"Moved picture-game, wardrobe, and medal feedback to bounded Canvas overlays and retired the medal spatial scoreboard.",
		"76c30a6699de3a8bb2b9699f2ec9aaf89d5c00b6",
		(
			"21ae8391f019a00f740a2433e84532f300b6e109",
			"be3fb490246f3dc21dd1f0246b8f72208e458e3a",
			"fe3616b438b423600a840d5affa59baec8016880",
			"8ed978bec959140c0b100b8eb811ad648da589c1",
		),
		(
			"scripts/games/picture_games.gd",
			"scripts/wardrobe_ui.gd",
			"scripts/medal_system.gd",
			"scripts/probe_mg2d.gd",
			"scripts/probe_ui_system.gd",
			"scripts/probe_rank.gd",
		),
		("CHG-008", "CHG-011"),
		(
			"\"$GODOT\" --headless -s scripts/probe_mg2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_ui_system.gd",
			"\"$GODOT\" --headless -s scripts/probe_rank.gd",
		),
		manual_reason="The inverse would restore Sprite3D feedback and touches shared reward/save paths, so it conflicts with the binding medium direction.",
	),
	_group(
		"CHG-008",
		"GAME2D shrink gate and CI enforcement",
		"Added the canonical whole-game debt classifier, falsification tests, shrink-only manifest, and post-import local/remote enforcement.",
		"fe3616b438b423600a840d5affa59baec8016880",
		(
			"e0877b65cf9e080e70117c995d53624ea3ab9910",
			"d6240be828a841b70fba4742874ef28d34d47011",
			"b3ad384228bda62d33af0e7cc9df099ad63326b8",
			"344d8d5c5d30d773dfc1da5868fa97fbdbf333b6",
			"a3d3bce18dd73d0ac87f2fb4bac397e2b4396180",
		),
		(
			"tools/audit_game_2d.py",
			"tools/game_2d_migration_manifest.json",
			"tools/tests/test_audit_game_2d.py",
			"scripts/ci.sh",
			".github/workflows/probes.yml",
		),
		("CHG-005", "CHG-009", "CHG-010", "CHG-013"),
		(
			"python -m unittest tools.tests.test_audit_game_2d",
			"python tools/audit_game_2d.py --stress",
			"python tools/audit_game_2d.py --regression",
		),
		manual_reason="This group includes a high-risk workflow change and cumulative manifest semantics. Reversion would remove the guard that proves later debt reductions.",
	),
	_group(
		"CHG-009",
		"Archived source and unreachable-model retirement",
		"Removed byte-verified non-runtime source models and unreachable active/export models after preservation on the deprecated-resources branch.",
		"b3ad384228bda62d33af0e7cc9df099ad63326b8",
		(
			"86d0c2434579c1b0e226414a9601dcce4d5b9e22",
			"0b75c60cdd16d670bc8366f7d3aeaaf426f682e9",
		),
		(
			"assets_src/blender/",
			"backups/",
			"gen2/meshy/",
			"tools/out/",
			"assets/art35/",
			"assets/castle/",
			"assets/galaxy/",
			"assets/kits/",
			"tools/game_2d_migration_manifest.json",
		),
		("CHG-008", "CHG-011"),
		(
			"python tools/audit_game_2d.py --regression",
			"\"$GODOT\" --headless --import .",
			"GODOT=\"$GODOT\" scripts/ci.sh",
		),
		manual_reason="This is a large, policy-sensitive deletion set. Any restore must prove archive hashes, dependencies, licensing, import behavior, and a newly approved runtime purpose.",
	),
	_group(
		"CHG-010",
		"Display/device Canvas Racer and exact cue",
		"Made normal display/device production UI and the forced-2D probe route use the Canvas Racer with the exact circle cue; ordinary unforced headless still retains the legacy lobby/Racer path and may load scripts/kart.gd.",
		"0b75c60cdd16d670bc8366f7d3aeaaf426f682e9",
		(
			"82124b3a03426985afa9ff5d03447b8807d37f12",
			"e4528b27e2552f669de2b65c37da0243fb924eac",
		),
		(
			"scripts/opera_career_world_2d.gd",
			"scripts/probe_opera_2d.gd",
			"scripts/audio_director.gd",
		),
		("CHG-004", "CHG-008", "CHG-011", "CHG-016", "CHG-022"),
		(
			"\"$GODOT\" --headless -s scripts/probe_opera_2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_voice.gd",
			"python tools/audit_game_2d.py --regression",
		),
		manual_reason="The current file contains manual reconciliation that protects the display/device Canvas route but does not remove the ordinary-headless legacy lobby/kart source path tracked by MA-OPERA-010. Reverting old commits cannot safely reconstruct the current mixed file or expand that debt into production UI.",
	),
	_group(
		"CHG-011",
		"2D authority and synchronized master documents",
		"Established the central audit/design language, preserved security precedence, superseded game-wide 3D direction, and synchronized the later evidence baseline.",
		"e4528b27e2552f669de2b65c37da0243fb924eac",
		(
			"806ffb95a4c36ca938235bc2e41d4491de2d019a",
			"0e75f3838a439391ff999e2bee9131a81d212fa1",
			"9289dd813439d16cc8178e57abcbd332a8e0fe9d",
			"d1f73a388ad9716a2abdfb6aca751f368abb2ff2",
		),
		(
			"AGENTS.md",
			"CLAUDE.md",
			"audit/MASTER_AUDIT_2026-08-09.md",
			"design/00_MASTER_INDEX.md",
			"design/01_GAME_DESIGN.md",
			"design/02_ART_DIRECTION.md",
			"design/03_TECHNICAL_ARCHITECTURE.md",
			"design/04_OPEN_WORK.md",
			"design/05_DOC_LEDGER.md",
		),
		("CHG-001", "CHG-008", "CHG-009"),
		("git diff --check",),
		manual_reason="Authority files are high-risk and later documents build on them. A rollback needs an explicit replacement authority, not restoration of superseded 3D prescriptions.",
	),
	_group(
		"CHG-012",
		"Dolls Canvas catcher",
		"Converted Faron's catcher to bounded Canvas gameplay with real touch, no-fail behavior, save/replay, teardown, and Mobile capture coverage.",
		"9289dd813439d16cc8178e57abcbd332a8e0fe9d",
		("5df754279a358b475c3e088e9e54f6ad0c1f32dc",),
		(
			"scripts/games/dolls.gd",
			"scripts/main.gd",
			"scripts/player.gd",
			"scripts/probe_audit.gd",
			"scripts/probe_dolls.gd",
		),
		("CHG-008", "CHG-011"),
		(
			"\"$GODOT\" --headless -s scripts/probe_dolls.gd",
			"\"$GODOT\" --headless -s scripts/probe_audit.gd",
		),
		manual_reason="The inverse restores a spatial catcher and overlaps player/main state ownership. It would violate current 2D and child-safety contracts.",
	),
	_group(
		"CHG-013",
		"Animated Seek kit and Canvas meadow",
		"Added governed Evie/Lamb-a' animation, rebuilt Seek with higher-grade Canvas art, and retired four archived meadow GLBs.",
		"5df754279a358b475c3e088e9e54f6ad0c1f32dc",
		(
			"8fa90111fefddd114a7a9ad68f838ba2108ce00e",
			"27bda85d3fc9a7842b05426e6ca846139160b043",
		),
		(
			"assets/minigames/seek/",
			"assets_src/imagegen/seek_animated_2026-08-09/",
			"assets/art35/arena/meadow_bush_0.glb",
			"assets/art35/arena/meadow_bush_1.glb",
			"assets/art35/arena/meadow_bush_2.glb",
			"assets/art35/arena/meadow_bush_3.glb",
			"scripts/games/seek.gd",
			"scripts/probe_seek.gd",
			"tools/build_seek_animation_assets.py",
		),
		("CHG-008", "CHG-011", "CHG-014"),
		(
			"python -m unittest tools.tests.test_build_seek_animation_assets",
			"\"$GODOT\" --headless -s scripts/probe_seek.gd",
			"python tools/audit_game_2d.py --regression",
		),
		manual_reason="This group mixes generated assets, shared main/probe routing, and archived GLB deletion. A revert could restore the rejected vinyl/low-quality presentation or lose archive invariants.",
	),
	_group(
		"CHG-014",
		"Fresh visual attestation and cinematic orientation",
		"Rejected wrong-orientation cinematic delivery, ignored review artifacts, required same-process fresh Canvas evidence, and bound ignored/custom production sources so stale captures cannot renew PASS.",
		"711879ecf10fa7c8871abb1544248a49f38d9078",
		(
			"b50f2477f87b56ed16f1ca469fbf7b5848ead723",
			"96317f8b703f08f171a00a774b8dc546910f57e4",
			"3b7a7e665323bed975b56635cbb6b7e99106c5e5",
			"fea916a81d8ece3df36a568567016a59fecd46a0",
		),
		(
			".gitignore",
			"VISUAL_AUDIT_TOOL.md",
			"scripts/probe_visual_audit.gd",
			"tools/audit_visual_design.py",
			"tools/visual_audit_spec.json",
			"tools/tests/test_audit_visual_design.py",
			"tools/audit_cinematic.py",
			"tools/tests/test_audit_cinematic.py",
		),
		("CHG-006", "CHG-013"),
		(
			"python -m unittest tools.tests.test_audit_visual_design",
			"python tools/audit_visual_design.py --stress",
			"python tools/audit_visual_design.py --fresh-strict",
			"python tools/audit_cinematic.py",
		),
		manual_reason="This is a fail-closed evidence chain. A partial inverse can silently authorize stale or ignored evidence and is therefore unsafe to automate.",
	),
	_group(
		"CHG-015",
		"Castle and Opera cross-platform generated-art stability",
		"Made Castle text provenance and Opera generated-art checks stable across platforms without weakening semantic, scanline, pixel, or delivery-hash controls.",
		"86d0c2434579c1b0e226414a9601dcce4d5b9e22",
		(
			"df5b4cf7f98cd1ce09468b2551cd3bd5bb8ddf4c",
			"5961fd968066e4644e2b77f73c72e990c4bef4ac",
			"fe10ffd2f36606eaad99e1e8881c1c84ffc5fa08",
		),
		(
			"assets/flats/castle/interactions_v4/castle_interactions_v4.json",
			"assets_src/castle/interactions_v4/castle_interaction_frame_approval_ledger.json",
			"assets_src/imagegen/opera_minigame_quality_2026-08-09/REVIEW.md",
			"audit/MASTER_AUDIT_2026-08-09.md",
			"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",
			"tools/build_castle_interaction_v4_delivery.py",
			"tools/build_castle_native_interactions_v4.py",
			"tools/plan_audit_rollback.py",
			"tools/prepare_opera_minigame_art.py",
			"tools/test_build_castle_interaction_v4_delivery.py",
			"tools/tests/test_prepare_opera_minigame_art.py",
		),
		(),
		(
			"python -m unittest tools.test_build_castle_interaction_v4_delivery tools.tests.test_prepare_opera_minigame_art",
			"python tools/build_castle_interaction_v4_delivery.py --check",
			"python tools/prepare_opera_minigame_art.py --check-only",
		),
		rollback_start=AUDIT_CATALOG_COMMIT,
		manual_reason="Although bounded, reverting a portability fix has no safe automatic benefit and could make Windows and CI disagree.",
	),
	_group(
		"CHG-016",
		"General Opera overhaul, 13 atlases, and minigame art",
		"Expanded the Opera career system, added 13 governed Roshan atlases and 208-frame audit evidence, and rebuilt broad minigame interaction/art foundations.",
		AUDIT_INTEGRATION_PARENT,
		(
			"ebd75539f16546752dcea4cbcabd2fea1c9f9cb4",
			"32e1a7e8c50123ec0abf83a291352fecee189ad0",
			"2119ab399ae778530c1f944b4f7414a97d218608",
		),
		(
			"OPERA_QUALITY_OVERHAUL_2026-08-09.md",
			"OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md",
			"assets/opera/worlds/actors/animation/",
			"assets/opera/worlds/ui/crests/",
			"assets/opera/worlds/widgets/",
			"assets_src/imagegen/opera_roshan_animation_2026-08-09/",
			"assets_src/imagegen/opera_minigame_quality_2026-08-09/",
			"scripts/opera_career_world_2d.gd",
			"scripts/opera_gesture_surface.gd",
			"scripts/opera_roshan_actor.gd",
		),
		("CHG-004", "CHG-005", "CHG-010", "CHG-017", "CHG-018", "CHG-019", "CHG-020", "CHG-022"),
		(
			"python tools/prepare_opera_minigame_art.py --check-only",
			"python tools/audit_opera_roshan_animation.py",
			"\"$GODOT\" --headless -s scripts/probe_opera_2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_opera_gesture_quality.gd",
		),
		manual_reason="The source commits are broad and their shared files were manually reconciled in ad36. Reverting them directly would also undo accepted specialist and Canvas-Racer work.",
	),
	_group(
		"CHG-017",
		"Ballerina specialist",
		"Replaced the old Ballerina premise/art with a three-act held-pose recital, one-shot curtain call, teaching assists, and focused quality coverage.",
		AUDIT_INTEGRATION_PARENT,
		(
			"dc48c91a047668dd90f7f794950e8402e0138e08",
			"6ab63aa7c147be395d0d67945a527b5789ccf746",
			"26305338d84791feb85b40927379a7c325947b63",
			"86b6a5b693410c48c4fbcfdb83956ebca6100c44",
			"6369a72adec388e1a4c751fc6a2d2a61458531fb",
			"3dd98fbe5e63374615c64316f353665553d36fcd",
			"7d9e6c5f121ef1245bff96388745fd85d54b16d3",
			"0447188f73b7ca7dadfe782384cc8d1c4da7828f",
		),
		(
			"BALLERINA_PARTY_REBUILD_2026-08-09.md",
			"assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png",
			"assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_ballerina_sheet_a_native.png",
			"scripts/opera_ballet_surface.gd",
			"scripts/opera_career_world_2d.gd",
			"scripts/probe_opera_2d.gd",
		),
		("CHG-016", "CHG-022"),
		(
			"python tools/audit_opera_roshan_animation.py",
			"\"$GODOT\" --headless -s scripts/probe_opera_2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_opera_gesture_quality.gd",
		),
		manual_reason="The Ballerina work spans rescue/final commits and shared Opera files, and the accepted atlas is part of the general 13-atlas pack. Automatic commit reversal is not isolated.",
	),
	_group(
		"CHG-018",
		"Boxer specialist",
		"Added a five-phase, two-glove, one-finger Boxer surface with no-loss contact, passive rejection, teardown, re-entry, and save coverage.",
		AUDIT_INTEGRATION_PARENT,
		("8d67c2bd180b97a0bca6c473892d45aedbd00537",),
		(
			"design/BOXING_GAME_PROJECT_2026-08-09.md",
			"scripts/opera_boxing_surface.gd",
			"scripts/opera_career_world_2d.gd",
			"scripts/probe_opera_2d.gd",
			"scripts/probe_opera_gesture_quality.gd",
		),
		("CHG-016", "CHG-022"),
		(
			"\"$GODOT\" --headless -s scripts/probe_opera_2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_opera_gesture_quality.gd",
		),
		manual_reason="The new surface is isolated, but phase registration, save state, and probes live in shared files. The tempting `-m 2` upstream-merge shortcut is mutually exclusive with other accepted work and is explicitly refused.",
	),
	_group(
		"CHG-019",
		"Candymaker phone-playability fix",
		"Aligned the syrup pitcher drawing, stream, and hit geometry and made filling monotonic and generous on phone screens.",
		AUDIT_INTEGRATION_PARENT,
		("3974675629c45a8a95d41d597205f8110aaa0deb",),
		(
			"scripts/opera_gesture_surface.gd",
			"scripts/probe_opera_2d.gd",
			"scripts/probe_opera_gesture_quality.gd",
		),
		("CHG-016", "CHG-022"),
		(
			"\"$GODOT\" --headless -s scripts/probe_opera_2d.gd",
			"\"$GODOT\" --headless -s scripts/probe_opera_gesture_quality.gd",
		),
		manual_reason="This is a small semantic fix inside very large shared files that were conflict-resolved later; patch reversal must be hand-reviewed against current line geometry.",
	),
	_group(
		"CHG-020",
		"Deterministic area music",
		"Authored, rendered, routed, and deterministically checked 42 unique looped area cues while preserving the Castle visual-approval ledger.",
		AUDIT_INTEGRATION_PARENT,
		(
			"0da07e24c92c56a974635d7a3f3a4967f4695624",
			"27c2c95d7711c5b5ddb36eb46fb5baf1a86e5f96",
			"ddac6b2e17246e6e7247692bc9c61af16d3adbeb",
		),
		(
			"MUSIC_AUDIT_2026-08-09.md",
			"assets/audio/music/area_music_manifest.json",
			"assets/audio/music/",
			"assets_src/audio/music/area_music_scores.json",
			"scripts/audio_director.gd",
			"scripts/probe_audio.gd",
			"tools/build_area_music.py",
		),
		("CHG-004", "CHG-016", "CHG-018", "CHG-022"),
		(
			"python tools/build_area_music.py --check",
			"\"$GODOT\" --headless -s scripts/probe_audio.gd",
			"\"$GODOT\" --headless -s scripts/probe_voice.gd",
		),
		warnings=(
			"CHG-020 uses the parent-1 comparison of 245c1613; never combine it on one rollback branch with CHG-018's opposing parent-2 comparison of that same merge.",
			"The CHG-020 comparison is known to stop on a scripts/games/picture_games.gd conflict at ad36; abort or hand-reconcile it under the coupled CHG-007 and CHG-020 contracts.",
		),
		safety=REVIEWABLE,
		revert_target=AUDIT_UPSTREAM_PARENT,
		revert_mainline=1,
	),
	_group(
		"CHG-021",
		"Saved Castle logo on shell banners",
		"Applied the child's saved Castle color/symbol to registered purple shell banners without stealing room input; this is the catalog's safest bounded partial inverse.",
		AUDIT_INTEGRATION_PARENT,
		("9e75e8e392d34b784b9899e7434cdf954fb0e31d",),
		(
			"scripts/castle_logo_studio.gd",
			"scripts/probe_interaction.gd",
		),
		("CHG-022",),
		(
			"python -m gdtoolkit.parser scripts/castle_logo_studio.gd scripts/probe_interaction.gd",
			"python tools/lint_inference.py scripts/castle_logo_studio.gd scripts/probe_interaction.gd",
			"\"$GODOT\" --headless -s scripts/probe_interaction.gd",
		),
		safety=REVIEWABLE,
	),
	_group(
		"CHG-022",
		"ad36 integration reconciliation and full recovery",
		"Merged current Opera/art/music work while preserving the display/device Canvas Racer, reconciled CI/workflow parity and CRLF checks, and synchronized the central audit; ordinary unforced headless still retained a legacy lobby/kart path. Recovery is the entire merge delta or nothing.",
		AUDIT_INTEGRATION_PARENT,
		(AUDIT_INTEGRATION_COMMIT,),
		(
			".github/workflows/probes.yml",
			"ASSET_LICENSES.md",
			"audit/MASTER_AUDIT_2026-08-09.md",
			"design/",
			"assets/audio/music/",
			"assets/opera/worlds/",
			"assets_src/audio/music/",
			"assets_src/imagegen/opera_minigame_quality_2026-08-09/",
			"assets_src/imagegen/opera_roshan_animation_2026-08-09/",
			"scripts/",
			"tools/",
		),
		("CHG-010", "CHG-016", "CHG-017", "CHG-018", "CHG-019", "CHG-020", "CHG-021"),
		(
			"git diff --cached --exit-code 7b5d1209063a22002118c364767d537b34b3dc6f --",
			"GODOT=\"$GODOT\" scripts/ci.sh",
		),
		safety=MERGE_ALL,
		all_or_nothing=True,
		revert_target=AUDIT_INTEGRATION_COMMIT,
		revert_mainline=1,
		merge_parents=(AUDIT_INTEGRATION_PARENT, AUDIT_UPSTREAM_PARENT),
	),
	_group(
		"CHG-023",
		"Written change log and rollback process",
		"Adds the stable change catalog, conservative planning helper, validation tests, and central written rollback instructions requested after ad36.",
		AUDIT_INTEGRATION_COMMIT,
		("57bc08d1220594fbabcab15362b5685a9f8514e6",),
		(
			".gitignore",
			"audit/MASTER_AUDIT_2026-08-09.md",
			"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",
			"design/00_MASTER_INDEX.md",
			"design/03_TECHNICAL_ARCHITECTURE.md",
			"design/04_OPEN_WORK.md",
			"design/05_DOC_LEDGER.md",
			"design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md",
			"tools/plan_audit_rollback.py",
			"tools/tests/test_plan_audit_rollback.py",
		),
		(),
		(
			"python -m py_compile tools/plan_audit_rollback.py tools/tests/test_plan_audit_rollback.py",
			"python -m unittest tools.tests.test_plan_audit_rollback",
		),
		rollback_start=AUDIT_CATALOG_COMMIT,
		manual_reason="The introduction anchor is known, but the ledger and planner are append-only operational controls. Reverse 57bc only on a dedicated branch after reviewing later CHG-023 maintenance and preserving any still-required rollback evidence.",
	),
	_group(
		"CHG-024",
		"f3b0 current-dev master-audit reconciliation and full recovery",
		"Imported the master audit, toolchain, intentional archive removals, and bounded Canvas conversions onto current dev while preserving newer diegetic Opera, Candy, Ballerina, and Boxer work; preserved the display/device Canvas Racer without removing the ordinary unforced headless legacy kart split, moved V2 Castle logo banners to Canvas, added remote diegetic parity gates, canonicalized CRLF text fingerprints, and corrected truthful Nursery/Racer probe sampling.",
		AUDIT_RECONCILIATION_PARENT,
		(AUDIT_RECONCILIATION_COMMIT,),
		(
			".github/",
			".gitignore",
			"AGENTS.md",
			"art_library/",
			"ASSET_LICENSES.md",
			"assets/",
			"assets_src/",
			"audit/",
			"backups/",
			"CLAUDE.md",
			"CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md",
			"design/",
			"gen2/",
			"ROSHAN_SPRITE_CUTOFF_AUDIT_2026-08-02.md",
			"scripts/",
			"STUFFIE_COMPANIONS.md",
			"tools/",
			"VISUAL_AUDIT_TOOL.md",
		),
		tuple(f"CHG-{number:03d}" for number in range(1, 24)),
		(
			f"git diff --cached --exit-code {AUDIT_RECONCILIATION_PARENT} --",
			"python -B tools/prepare_opera_minigame_art.py --check-only",
			"GODOT=\"$GODOT\" scripts/ci.sh",
		),
		rollback_start=AUDIT_RECONCILIATION_COMMIT,
		warnings=(
			"This all-or-nothing inverse removes the entire f3b0 reconciliation; it is not a per-change rollback.",
			"It reverses intentional archive removals and can restore retired 3D or source resources to active repository paths; restored payloads are not approved production content.",
			"Never combine CHG-024 with any CHG-001 through CHG-023 inverse on the same branch.",
			"The source delta must contain no assets/book/, assets/audio/voices/, or assets/characters/friends/ paths; stop before mutation if the protected-path guard fails.",
			"Run the exact Godot 4.7.1 full gate suite and remote exact-head CI before considering the rollback.",
		),
		safety=MERGE_ALL,
		all_or_nothing=True,
		revert_target=AUDIT_RECONCILIATION_COMMIT,
		revert_mainline=1,
		merge_parents=(AUDIT_RECONCILIATION_PARENT, AUDIT_RECONCILIATION_AUDIT_PARENT),
	),
)


class CatalogError(ValueError):
	"""Raised when the static catalog is internally unsafe."""


class UnknownChangeError(KeyError):
	"""Raised when a requested stable ID is absent."""


class UnsafePlanError(RuntimeError):
	"""Raised when command emission is forbidden for a mixed group."""


_ID_RE = re.compile(r"CHG-[0-9]{3}\Z")
_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")


def _validate_path(path: str) -> None:
	if not path or "\x00" in path or "\\" in path:
		raise CatalogError(f"unsafe catalog path: {path!r}")
	if path.startswith(("/", "-")) or re.match(r"^[A-Za-z]:", path):
		raise CatalogError(f"unsafe catalog path: {path!r}")
	parts = path.rstrip("/").split("/")
	if any(part in ("", ".", "..") for part in parts):
		raise CatalogError(f"unsafe catalog path: {path!r}")


def validate_catalog(groups: Sequence[ChangeGroup] = CATALOG) -> None:
	ids: set[str] = set()
	commit_owners: dict[str, str] = {}
	for group in groups:
		if not _ID_RE.fullmatch(group.change_id):
			raise CatalogError(f"invalid change ID: {group.change_id!r}")
		if group.change_id in ids:
			raise CatalogError(f"duplicate change ID: {group.change_id}")
		ids.add(group.change_id)
		if not _COMMIT_RE.fullmatch(group.baseline_commit):
			raise CatalogError(f"invalid baseline commit for {group.change_id}")
		if not _COMMIT_RE.fullmatch(group.rollback_start):
			raise CatalogError(f"invalid rollback start for {group.change_id}")
		if group.pending_commit:
			if group.commits or group.safety != MANUAL:
				raise CatalogError(f"pending group {group.change_id} must be manual with no commits")
		elif not group.commits:
			raise CatalogError(f"group {group.change_id} has no commits")
		for commit in group.commits:
			if not _COMMIT_RE.fullmatch(commit):
				raise CatalogError(f"invalid commit in {group.change_id}: {commit!r}")
			owner = commit_owners.get(commit)
			if owner is not None:
				raise CatalogError(f"commit {commit} is owned by both {owner} and {group.change_id}")
			commit_owners[commit] = group.change_id
		for path in group.paths:
			_validate_path(path)
		for warning in group.warnings:
			if not warning or "\n" in warning or "\r" in warning:
				raise CatalogError(f"invalid warning in {group.change_id}")
		if group.safety not in (MANUAL, REVIEWABLE, MERGE_ALL):
			raise CatalogError(f"invalid safety for {group.change_id}: {group.safety}")
		if group.safety == MANUAL and not group.manual_reason:
			raise CatalogError(f"manual group {group.change_id} lacks a refusal reason")
		if group.all_or_nothing != (group.safety == MERGE_ALL):
			raise CatalogError(f"merge safety mismatch for {group.change_id}")
		if group.revert_target:
			if not _COMMIT_RE.fullmatch(group.revert_target):
				raise CatalogError(f"invalid revert target in {group.change_id}")
			if group.safety == MERGE_ALL and group.revert_target not in group.commits:
				raise CatalogError(f"merge revert target is not owned by {group.change_id}")
			if group.revert_mainline not in (1, 2):
				raise CatalogError(f"invalid merge mainline for {group.change_id}")
		elif group.revert_mainline is not None:
			raise CatalogError(f"mainline without revert target in {group.change_id}")
		if group.safety == MERGE_ALL:
			if len(group.merge_parents) != 2:
				raise CatalogError(f"whole-merge group {group.change_id} must record exactly two parents")
			for parent in group.merge_parents:
				if not _COMMIT_RE.fullmatch(parent):
					raise CatalogError(f"invalid merge parent in {group.change_id}")
			if group.rollback_start != group.revert_target:
				raise CatalogError(f"whole-merge group {group.change_id} must start at its revert target")
			assert group.revert_mainline is not None
			if group.baseline_commit != group.merge_parents[group.revert_mainline - 1]:
				raise CatalogError(f"whole-merge baseline/mainline mismatch for {group.change_id}")
			exact_tree_gate = f"git diff --cached --exit-code {group.baseline_commit} --"
			if exact_tree_gate not in group.gates:
				raise CatalogError(f"whole-merge group {group.change_id} lacks exact parent-tree gate")
		elif group.merge_parents:
			raise CatalogError(f"non-whole-merge group {group.change_id} records merge parents")

	for group in groups:
		for dependency in group.dependencies:
			if dependency == group.change_id:
				raise CatalogError(f"self dependency in {group.change_id}")
			if dependency not in ids:
				raise CatalogError(f"unknown dependency {dependency} in {group.change_id}")


def select_group(change_id: str, groups: Sequence[ChangeGroup] = CATALOG) -> ChangeGroup:
	if not _ID_RE.fullmatch(change_id):
		raise UnknownChangeError(change_id)
	for group in groups:
		if group.change_id == change_id:
			return group
	raise UnknownChangeError(change_id)


def _bullets(items: Sequence[str], empty: str = "none") -> list[str]:
	if not items:
		return [f"  - {empty}"]
	return [f"  - {item}" for item in items]


def render_plan(group: ChangeGroup) -> str:
	validate_catalog()
	lines = [
		f"Change ID: {group.change_id}",
		f"Title: {group.title}",
		f"Safety: {group.safety}",
		f"Summary: {group.summary}",
		"",
		"Exact baseline requirements:",
		f"  - Audit branch began at {AUDIT_BASELINE_COMMIT}.",
		f"  - This group's comparison baseline is {group.baseline_commit}.",
		f"  - Historical ad36 parent 1 is {AUDIT_INTEGRATION_PARENT}; parent 2 is {AUDIT_UPSTREAM_PARENT}.",
		"  - The inverse must preserve protected originals and all save keys.",
	]
	if group.merge_parents:
		lines.extend((
			f"  - Exact merge source is {group.revert_target}.",
			f"  - Parent 1 is {group.merge_parents[0]}; parent 2 is {group.merge_parents[1]}.",
			f"  - Mainline {group.revert_mainline} selects exact recovery tree {group.baseline_commit}.",
		))
	lines.extend((
		"",
		"Exact current/start requirements:",
		f"  - Use exactly {group.rollback_start} as the rollback branch start.",
		"  - Index, tracked worktree, and untracked set must all be empty before creating the branch.",
		f"  - Use {GODOT_REQUIREMENT} for every Godot gate.",
		f"  - The new branch name is {group.branch_name}; it must not already exist.",
		"",
		"Owned commits (recorded oldest to newest):",
	))
	if group.pending_commit:
		lines.extend(_bullets((), "PENDING: record the final CHG-023 commit before planning an inverse"))
	else:
		lines.extend(_bullets(group.commits))
	lines.extend(("", "Affected path selectors (the owned commits remain the exact file authority):"))
	lines.extend(_bullets(group.paths))
	lines.extend(("", "Coupled change IDs to review:"))
	lines.extend(_bullets(group.dependencies))
	lines.extend(("", "Required gates:"))
	lines.extend(_bullets(group.gates))
	lines.extend(("", "Safety warnings:"))
	lines.extend(_bullets(group.warnings))
	lines.extend(("", "Branch-based plan:"))
	if group.safety == MANUAL:
		lines.extend((
			f"  1. Inspect the owned commits and coupled IDs without changing Git state.",
			f"  2. From a clean tree, create {group.branch_name} at exact start {group.rollback_start}.",
			"  3. Hand-author the smallest inverse; do not bulk-restore the listed selectors.",
			"  4. Review protected assets, save compatibility, child safety, and medium authority before staging.",
			"  5. Run every listed gate, review the staged diff, then commit only with owner approval.",
			f"  REFUSAL: {group.manual_reason}",
			"  --emit-script is disabled for this group.",
		))
	elif group.safety == MERGE_ALL:
		lines.extend((
			f"  1. The emitted script creates {group.branch_name} at {group.rollback_start}.",
			f"  2. It verifies the exact two-parent topology, then stages only `git revert --no-commit -m {group.revert_mainline} {group.revert_target}`.",
			f"  3. It requires the staged result to equal selected-parent baseline {group.baseline_commit} exactly.",
			"  4. It refuses a source delta or staged inverse that touches a protected path.",
			"  5. It runs the complete listed gates and stops with changes staged for human review; it does not commit.",
			"  This is explicit all-or-nothing recovery. Do not copy selected paths from the merge inverse.",
		))
	else:
		inverse = (
			f"`git revert --no-commit -m {group.revert_mainline} {group.revert_target}`"
			if group.revert_target
			else "the owned commits in reverse order with `git revert --no-commit`"
		)
		lines.extend((
			f"  1. The emitted script creates {group.branch_name} at {group.rollback_start}.",
			f"  2. It applies {inverse}.",
			"  3. It runs the listed gates and stops with changes staged for human review; it does not commit.",
			"  4. Inspect all coupled IDs and the complete staged diff before committing.",
		))
	return "\n".join(lines) + "\n"


def render_script(group: ChangeGroup) -> str:
	validate_catalog()
	if group.safety == MANUAL:
		raise UnsafePlanError(f"{group.change_id} is mixed or policy-sensitive: {group.manual_reason}")
	commits = " ".join(reversed(group.commits))
	lines = [
		"#!/usr/bin/env sh",
		"set -eu",
		f"CURRENT='{group.rollback_start}'",
		f"BRANCH='{group.branch_name}'",
		"if [ -n \"$(git status --porcelain=v1 --untracked-files=all)\" ]; then",
		"  echo 'STOP: working tree, index, and untracked set must be clean.' >&2",
		"  exit 1",
		"fi",
		"git cat-file -e \"${CURRENT}^{commit}\"",
	]
	if group.safety == MERGE_ALL:
		protected_paths = " ".join(PROTECTED_PATHS)
		lines.extend((
			f"SOURCE='{group.revert_target}'",
			f"BASELINE='{group.baseline_commit}'",
			f"EXPECTED_PARENTS='{group.merge_parents[0]} {group.merge_parents[1]}'",
			"git cat-file -e \"${SOURCE}^{commit}\"",
			"if [ \"$(git show -s --format=%P \"${SOURCE}\")\" != \"${EXPECTED_PARENTS}\" ]; then",
			"  echo 'STOP: merge topology does not match the catalog.' >&2",
			"  exit 1",
			"fi",
			f"if ! git diff --quiet \"${{BASELINE}}\" \"${{SOURCE}}\" -- {protected_paths}; then",
			"  echo 'STOP: source merge changes a protected asset path.' >&2",
			"  exit 1",
			"fi",
		))
	lines.extend((
		"if git show-ref --verify --quiet \"refs/heads/${BRANCH}\"; then",
		"  echo \"STOP: branch already exists: ${BRANCH}\" >&2",
		"  exit 1",
		"fi",
	))
	for warning in group.warnings:
		lines.append(f"# WARNING: {warning}")
	if group.warnings:
		lines.append("echo 'WARNING: review every catalog warning above before accepting this inverse.' >&2")
	lines.append("git switch -c \"${BRANCH}\" \"${CURRENT}\"")
	if group.revert_target:
		lines.append(f"git revert --no-commit -m {group.revert_mainline} {group.revert_target}")
	else:
		lines.append(f"git revert --no-commit {commits}")
	if group.safety == MERGE_ALL:
		protected_paths = " ".join(PROTECTED_PATHS)
		lines.extend((
			f"if [ -n \"$(git diff --cached --name-only -- {protected_paths})\" ]; then",
			"  echo 'STOP: staged inverse changes a protected asset path.' >&2",
			"  exit 1",
			"fi",
		))
	lines.append("git diff --check")
	lines.append("git diff --cached --check")
	lines.append(": \"${GODOT:?Set GODOT to the exact Godot 4.7.1-stable binary}\"")
	lines.extend(group.gates)
	lines.extend((
		"git status --short",
		"git diff --cached --stat",
		"echo 'STOP: review the complete staged inverse and coupled change IDs; no commit was created.'",
	))
	return "\n".join(lines) + "\n"


def render_catalog(groups: Sequence[ChangeGroup] = CATALOG) -> str:
	validate_catalog(groups)
	lines = ["Stable master-audit rollback catalog:"]
	for group in groups:
		lines.append(f"  {group.change_id}  {group.safety}  {group.title}")
	return "\n".join(lines) + "\n"


def _parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("change_id", nargs="?", help="stable ID such as CHG-013")
	parser.add_argument("--list", action="store_true", help="list stable IDs")
	parser.add_argument(
		"--emit-script",
		action="store_true",
		help="print (never execute) a guarded shell script for an approved reviewable group",
	)
	return parser


def main(argv: Sequence[str] | None = None) -> int:
	args = _parser().parse_args(argv)
	try:
		validate_catalog()
	except CatalogError as exc:
		print(f"catalog error: {exc}", file=sys.stderr)
		return 4
	if args.list:
		if args.change_id or args.emit_script:
			print("error: --list cannot be combined with a change ID or --emit-script", file=sys.stderr)
			return 2
		print(render_catalog(), end="")
		return 0
	if not args.change_id:
		print("error: a stable change ID is required (or use --list)", file=sys.stderr)
		return 2
	try:
		group = select_group(args.change_id)
	except UnknownChangeError:
		print(f"error: unknown change ID: {args.change_id}", file=sys.stderr)
		return 2
	if args.emit_script:
		try:
			print(render_script(group), end="")
		except UnsafePlanError as exc:
			print(f"refused: {exc}", file=sys.stderr)
			return 3
	else:
		print(render_plan(group), end="")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
