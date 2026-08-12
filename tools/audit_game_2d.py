#!/usr/bin/env python3
"""Migration contract for the owner's game-wide 2D-only decision.

This is intentionally not a waiver system.  Every tracked model binary or
model-import sidecar -- including source masters and backups -- and every
active project, probe, scene/resource, shader, or configuration file that
still bears a 3D API is migration debt.  The active/export model subset is
reported separately only to prioritise runtime migration.  The manifest is an
exact, shrinking snapshot so a large conversion can land in small reviewable
slices without allowing the old architecture to grow.

Modes
-----
``default``
	Advisory inventory.  Known debt prints ``UNSATISFIED`` but returns zero when
	the manifest exactly matches the tree.  Inventory drift is an error.
``--regression-gate``
	Returns zero only when the manifest is complete, exact, and a subset of the
	preceding checked-in baseline.  A green exit is reported as
	``NO_REGRESSION`` -- never PASS -- while any debt remains.
``--strict``
	Returns zero only after every debt inventory is empty.
``--stress``
	Builds disposable projects and proves that expansion, incomplete manifests,
	stale entries, and false empty baselines are rejected.

The audit modes are read-only outside disposable stress directories.
``--refresh-manifest`` is the sole write mode: it atomically records exact
debt removal while preserving the immutable initial ceiling byte-for-byte and
refusing any path, token, fingerprint, archive, or archive-now expansion.
"""

from __future__ import annotations

import argparse
import bz2
import gzip
import hashlib
import io
import json
import lzma
import os
import re
import subprocess
import tarfile
import tempfile
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping


SCHEMA_VERSION = 4
DEFAULT_MANIFEST = "tools/game_2d_migration_manifest.json"
# Trust anchor for this repository's first full debt ceiling.  Updating this
# literal is an explicit contract change, not a normal manifest regeneration.
INITIAL_CEILING_SHA256 = "2da7db0ed6a3b67c33165a988450d322013f58455d590d3b73783646d59be2e2"
MODEL_EXTENSIONS = {
	".3ds", ".abc", ".blend", ".dae", ".escn", ".fbx", ".glb", ".gltf",
	".obj", ".ply", ".stl", ".usd", ".usda", ".usdc", ".usdz", ".x3d",
}
MODEL_EXTENSION_PATTERN = (
	r"(?:3ds|abc|blend(?:\d+)?|dae|escn|fbx|glb|gltf|obj|ply|stl|usd|usda|usdc|usdz|x3d)"
)
NUMBERED_BLEND_RE = re.compile(r"(?i)\.blend\d+$")
MODEL_IMPORT_SIDECAR_RE = re.compile(
	r"(?i)\." + MODEL_EXTENSION_PATTERN + r"\.import$"
)
MODEL_MAGIC_PREFIXES = (
	b"glTF", b"BLENDER", b"Kaydara FBX Binary", b"PXR-USDC",
)
OBJ_VERTEX_RE = re.compile(
	br"(?m)^\s*v\s+[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?\s+"
	br"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?\s+"
	br"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?(?:\s|$)"
)
OBJ_FACE_RE = re.compile(br"(?m)^\s*f\s+\d+(?:/\d*)?(?:/\d+)?(?:\s+\d+(?:/\d*)?(?:/\d+)?){2,}\s*$")
ASCII_STL_RE = re.compile(br"(?is)^\s*solid\b.*\bfacet\s+normal\b.*\bvertex\s+")
GLTF_JSON_RE = re.compile(
	br"(?is)^\s*\{.*?\"asset\"\s*:\s*\{.{0,2048}"
	br"\"version\"\s*:\s*\"[12](?:\.\d+)?\""
)
GLTF_CONTENT_RE = re.compile(
	br"(?i)\"(?:accessors|animations|buffers|bufferViews|cameras|images|materials|"
	br"meshes|nodes|samplers|scenes|skins|textures)\"\s*:")
PLY_HEADER_RE = re.compile(br"^ply\r?\n")
COLLADA_XML_RE = re.compile(
	br"(?i)<(?:[A-Za-z_][A-Za-z0-9_.-]*:)?COLLADA\b")
X3D_XML_RE = re.compile(
	br"(?i)<(?:[A-Za-z_][A-Za-z0-9_.-]*:)?X3D\b")
MAGIC_SNIFF_ACTIVE_EXTENSIONS = {
	"", ".bin", ".blob", ".dat", ".json", ".txt", ".xml",
}
PRODUCTION_SOURCE_EXTENSIONS = {
	".c", ".cc", ".cpp", ".cs", ".cxx", ".gd", ".gdshader",
	".gdshaderinc", ".h", ".hh", ".hpp", ".hxx", ".java", ".kt", ".rs",
}
SOURCE_TEXT_EXTENSIONS = PRODUCTION_SOURCE_EXTENSIONS | {".py", ".pyi"}
NATIVE_BINARY_EXTENSIONS = {".a", ".dll", ".dylib", ".lib", ".so", ".wasm"}
OPAQUE_RUNTIME_BINARY_EXTENSIONS = {".aar", ".jar", ".pck"}
ACTIVE_DATA_EXTENSIONS = {
	".csv", ".dat", ".data", ".json", ".jsonl", ".toml", ".tsv",
	".txt", ".xml", ".yaml", ".yml",
}
DEPENDENCY_TEXT_EXTENSIONS = (
	ACTIVE_DATA_EXTENSIONS | PRODUCTION_SOURCE_EXTENSIONS |
	{".cfg", ".gdextension", ".tscn", ".tres"}
)
OPAQUE_DEPENDENCY_MEMBER_EXTENSIONS = (
	NATIVE_BINARY_EXTENSIONS | OPAQUE_RUNTIME_BINARY_EXTENSIONS |
	{".class", ".dex", ".res", ".scn"}
)
MODEL_SAMPLE_BYTES = 65536
# Plausible regular JSON/XML is inspected completely up to this generous cap.
# Larger candidates become explicit scan-coverage debt instead of silently
# passing because a model signature happened to occur after a finite prefix.
MODEL_TEXT_SCAN_BYTES = 4 * 1024 * 1024
NATIVE_SYMBOL_SCAN_BYTES = 8 * 1024 * 1024
ARCHIVE_MEMBER_LIMIT = 10000
ARCHIVE_SNIFF_BUDGET = 8 * 1024 * 1024
ARCHIVE_RATIO_LIMIT = 1000
ARCHIVE_RATIO_MIN_SIZE = 1024 * 1024
ARCHIVE_MAGIC_BYTES = 64 * 1024
ZIP_ARCHIVE_EXTENSIONS = (".zip",)
TAR_ARCHIVE_EXTENSIONS = (
	".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz", ".tbz2",
	".tar.xz", ".txz",
)
OPAQUE_ARCHIVE_EXTENSIONS = (".7z", ".rar")
SEVEN_ZIP_MAGIC = b"7z\xbc\xaf\x27\x1c"
RAR_MAGICS = (b"Rar!\x1a\x07\x00", b"Rar!\x1a\x07\x01\x00")
ZIP_MAGIC_RE = re.compile(br"PK(?:\x03\x04|\x05\x06|\x07\x08)")

# These roots are not part of the live Godot project/export.  They remain in
# the repository-wide model inventory and must ultimately move to an out-of-
# tree deprecated-resources worktree; this list only separates migration
# priority from the strict owner contract.
NON_ACTIVE_TOP_LEVEL = {
	".git", ".godot", ".venv", "__pycache__", "assets_src", "audit",
	"art_library", "backups", "build", "decommissioned", "deprecated-resources", "docs",
	"disabled_addons", "example", "gen2", "tmp", "tools",
}
NON_ACTIVE_PREFIXES = {"assets/_staging"}
# These are review/provenance ledgers, not live game data.  Every other
# Godot-active data directory is scanned, including future custom roots; a
# directory needs .gdignore (or an explicit reviewed provenance entry here)
# to leave the runtime contract.
NON_RUNTIME_DATA_PREFIXES = {
	".claude", ".codex", ".github", "art_library", "docs",
	"assets/provenance", "assets/_provenance",
	"FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03",
}
NON_RUNTIME_ROOT_DATA_FILES = {"FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"}

# A suffix of 3D catches the Godot class family without maintaining a brittle
# hand list.  Unambiguous named tokens remain raw debt.  Short class names that
# are also ordinary story words are counted only in API/type syntax, so labels
# such as "Sky Lagoon" and "Pearl Plane" do not become destructive cleanup work.
AMBIGUOUS_3D_API_CLASSES = {
	"Basis", "Compositor", "Decal", "Environment", "Mesh", "Plane",
	"Projection", "Skin", "Sky",
}
AMBIGUOUS_CLASS_ALTERNATION = "|".join(
	sorted(map(re.escape, AMBIGUOUS_3D_API_CLASSES), key=len, reverse=True))
AMBIGUOUS_CLASS_SEARCH_RE = re.compile(
	r"\b(?:" + AMBIGUOUS_CLASS_ALTERNATION + r")\b")
AMBIGUOUS_API_RES = tuple(re.compile(pattern) for pattern in (
	r"\b(?P<class>" + AMBIGUOUS_CLASS_ALTERNATION +
		r")\s*\.\s*(?:new|create_[A-Za-z0-9_]+|[A-Z][A-Z0-9_]*)\b",
	r"\b(?P<class>" + AMBIGUOUS_CLASS_ALTERNATION + r")\s*\(",
	r"(?:(?<!:):(?!:)|->)\s*(?P<class>" + AMBIGUOUS_CLASS_ALTERNATION + r")\b",
	r"\b(?:extends|as|is|new)\s+(?P<class>" +
		AMBIGUOUS_CLASS_ALTERNATION + r")\b",
	r"\b(?:class|struct)\s+[A-Za-z_]\w*\s*:\s*(?:public\s+)?(?P<class>" +
		AMBIGUOUS_CLASS_ALTERNATION + r")\b",
	r"<[^>\r\n]*\b(?P<class>" + AMBIGUOUS_CLASS_ALTERNATION +
		r")\b[^>\r\n]*>",
	r"\b(?:Array|Dictionary)\s*\[[^\]\r\n]*\b(?P<class>" +
		AMBIGUOUS_CLASS_ALTERNATION + r")\b[^\]\r\n]*\]",
	r"(?<!::)\b(?P<class>" + AMBIGUOUS_CLASS_ALTERNATION +
		r")\b\s*[*&]?\s*[A-Za-z_]\w*\s*[;=,)]",
	r"(?<![\w:])(?:::)?godot::(?P<class>" +
		AMBIGUOUS_CLASS_ALTERNATION + r")\b",
))
AMBIGUOUS_SCENE_TYPE_RE = re.compile(
	r"\b(?:type|base_type)\s*=\s*[\"'](?P<class>" +
	AMBIGUOUS_CLASS_ALTERNATION + r")[\"']")
# Authoritative Godot 4.7.1 taxonomy, grouped from the exact extension API
# dump.  Names ending in 3D are covered generically below; these sets cover
# the 3D-only resources, import pipeline, and XR APIs whose names do not.
MESH_3D_API_CLASSES = {
	"ArrayMesh", "BoxMesh", "CapsuleMesh", "CylinderMesh", "ImmediateMesh",
	"ImporterMesh", "MeshConvexDecompositionSettings", "MeshDataTool",
	"MeshLibrary", "PanoramaSkyMaterial", "PhysicalSkyMaterial",
	"PlaceholderMesh", "PlaneMesh", "PointMesh", "PrimitiveMesh", "PrismMesh",
	"ProceduralSkyMaterial", "QuadMesh", "RibbonTrailMesh", "SphereMesh",
	"SurfaceTool", "TextMesh", "TorusMesh", "TriangleMesh", "TubeTrailMesh",
}
TEXTURE_3D_API_CLASSES = {
	"CompressedCubemap", "CompressedCubemapArray", "CompressedTexture3D",
	"Cubemap", "CubemapArray", "ImageTexture3D", "NoiseTexture3D",
	"PlaceholderCubemap", "PlaceholderCubemapArray", "SkyMaterial",
	"PlaceholderTexture3D", "Texture3D", "Texture3DRD",
	"TextureCubemapArrayRD", "TextureCubemapRD",
	"VisualShaderNodeCubemap", "VisualShaderNodeCubemapParameter",
	"VisualShaderNodeTexture3D", "VisualShaderNodeTexture3DParameter",
}
RENDER_3D_API_CLASSES = {
	"CameraAttributes", "CameraAttributesPhysical", "CameraAttributesPractical",
	"CompositorEffect", "FogMaterial", "FogVolume", "GridMap", "LightmapGI",
	"LightmapGIData", "LightmapProbe", "NavigationMesh",
	"NavigationMeshGenerator", "ReflectionProbe", "RootMotionView",
	"VoxelGI", "VoxelGIData", "WorldEnvironment",
}
SKELETAL_3D_API_CLASSES = {
	"BoneMap", "SkeletonProfile", "SkeletonProfileHumanoid", "SkinReference",
}
GLTF_3D_API_CLASSES = {
	"EditorSceneFormatImporter", "EditorSceneFormatImporterBlend",
	"EditorSceneFormatImporterFBX2GLTF", "EditorSceneFormatImporterGLTF",
	"EditorSceneFormatImporterUFBX", "EditorScenePostImport",
	"EditorScenePostImportPlugin", "FBXDocument", "FBXState",
	"GLTFAccessor", "GLTFAnimation", "GLTFBufferView", "GLTFCamera",
	"GLTFDocument", "GLTFDocumentExtension",
	"GLTFDocumentExtensionConvertImporterMesh", "GLTFLight", "GLTFMesh",
	"GLTFNode", "GLTFObjectModelProperty", "GLTFPhysicsBody",
	"GLTFPhysicsShape", "GLTFSkeleton", "GLTFSkin", "GLTFSpecGloss",
	"GLTFState", "GLTFTexture", "GLTFTextureSampler", "ResourceImporterOBJ",
	"ResourceImporterScene",
}
XR_3D_API_CLASSES = {
	"MobileVRInterface", "OpenXRAPIExtension", "OpenXRAction",
	"OpenXRActionBindingModifier", "OpenXRActionMap", "OpenXRActionSet",
	"OpenXRAnalogThresholdModifier", "OpenXRAnchorTracker",
	"OpenXRAndroidThreadSettingsExtension", "OpenXRBindingModifier",
	"OpenXRBindingModifierEditor", "OpenXRCompositionLayer",
	"OpenXRCompositionLayerCylinder", "OpenXRCompositionLayerEquirect",
	"OpenXRCompositionLayerQuad", "OpenXRDpadBindingModifier",
	"OpenXRExtensionWrapper", "OpenXRExtensionWrapperExtension",
	"OpenXRFrameSynthesisExtension", "OpenXRFutureExtension",
	"OpenXRFutureResult", "OpenXRHand", "OpenXRHapticBase",
	"OpenXRHapticVibration", "OpenXRIPBinding", "OpenXRIPBindingModifier",
	"OpenXRInteractionProfile", "OpenXRInteractionProfileEditor",
	"OpenXRInteractionProfileEditorBase", "OpenXRInteractionProfileMetadata",
	"OpenXRInterface", "OpenXRMarkerTracker", "OpenXRPlaneTracker",
	"OpenXRRenderModel", "OpenXRRenderModelExtension",
	"OpenXRRenderModelManager", "OpenXRSpatialAnchorCapability",
	"OpenXRSpatialCapabilityConfigurationAnchor",
	"OpenXRSpatialCapabilityConfigurationAprilTag",
	"OpenXRSpatialCapabilityConfigurationAruco",
	"OpenXRSpatialCapabilityConfigurationBaseHeader",
	"OpenXRSpatialCapabilityConfigurationMicroQrCode",
	"OpenXRSpatialCapabilityConfigurationPlaneTracking",
	"OpenXRSpatialCapabilityConfigurationQrCode",
	"OpenXRSpatialComponentAnchorList", "OpenXRSpatialComponentBounded2DList",
	"OpenXRSpatialComponentBounded3DList", "OpenXRSpatialComponentData",
	"OpenXRSpatialComponentMarkerList", "OpenXRSpatialComponentMesh2DList",
	"OpenXRSpatialComponentMesh3DList", "OpenXRSpatialComponentParentList",
	"OpenXRSpatialComponentPersistenceList",
	"OpenXRSpatialComponentPlaneAlignmentList",
	"OpenXRSpatialComponentPlaneSemanticLabelList",
	"OpenXRSpatialComponentPolygon2DList", "OpenXRSpatialContextPersistenceConfig",
	"OpenXRSpatialEntityExtension", "OpenXRSpatialEntityTracker",
	"OpenXRSpatialMarkerTrackingCapability", "OpenXRSpatialPlaneTrackingCapability",
	"OpenXRSpatialQueryResultData", "OpenXRStructureBase", "OpenXRVisibilityMask",
	"WebXRInterface", "XRBodyTracker", "XRControllerTracker", "XRFaceTracker",
	"XRHandTracker", "XRInterface", "XRInterfaceExtension", "XRPose",
	"XRPositionalTracker", "XRServer", "XRTracker", "XRVRS",
}
FORBIDDEN_NAMED_TOKENS = (
	{
		"AABB", "PackedVector3Array", "Quaternion", "Transform3D", "Vector3",
		"Vector3i", "VisualShaderNodeParticleMeshEmitter",
	}
	| MESH_3D_API_CLASSES | TEXTURE_3D_API_CLASSES | RENDER_3D_API_CLASSES
	| SKELETAL_3D_API_CLASSES | GLTF_3D_API_CLASSES | XR_3D_API_CLASSES
)
FORBIDDEN_TOKEN_RE = re.compile(
	r"\b(?:[A-Za-z_][A-Za-z0-9_]*3D[A-Za-z0-9_]*|" +
	"|".join(sorted(map(re.escape, FORBIDDEN_NAMED_TOKENS), key=len, reverse=True)) +
	r")\b"
)
LOWER_3D_MARKER_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*_3d(?:_[A-Za-z0-9_]+)*\b")
MODEL_REFERENCE_RE = re.compile(
	r"(?i)(?<![A-Za-z0-9_./%+@~\-])(?:res://|assets/)?[^\s\"']+\." +
	MODEL_EXTENSION_PATTERN + r"\b"
)
CONFIG_3D_RE = re.compile(
	r"(?i)(?:\b3d/|_3d\b|\bjolt\s+physics\b|\bphysics_engine\s*=\s*\"jolt|"
	r"\bimport/(?:blender/enabled|fbx/importer)\s*=)"
)
THREE_D_SHADER_RE = re.compile(r"(?i)\bshader_type\s+(spatial|sky|fog)\b")
VISUAL_SHADER_3D_MODE_RE = re.compile(
	r"^(?:(?:(?:(?:Godot\.|godot::)?(?:VisualShader|Shader))\s*(?:\.|::)\s*)?"
	r"MODE_(?:SPATIAL|SKY|FOG)|"
	r"(?:Godot\.)?(?:VisualShader|Shader)\s*\.\s*ModeEnum\s*\.\s*"
	r"(?:Spatial|Sky|Fog)|"
	r"(?:0|3|4))$")
VISUAL_SHADER_2D_MODE_RE = re.compile(
	r"^(?:(?:(?:(?:Godot\.|godot::)?(?:VisualShader|Shader))\s*(?:\.|::)\s*)?"
	r"MODE_(?:CANVAS_ITEM|PARTICLES)|"
	r"(?:Godot\.)?(?:VisualShader|Shader)\s*\.\s*ModeEnum\s*\.\s*"
	r"(?:CanvasItem|Particles)|"
	r"(?:1|2))$")
CLASSDB_ANY_CALL_PATTERN = (
	r"\bClassDB\s*(?:::|\.)\s*(?:can_instantiate|class_exists|instantiate|"
	r"CanInstantiate|ClassExists|Instantiate)"
)
CLASSDB_INSTANTIATE_CALL_PATTERN = (
	r"\bClassDB\s*(?:::|\.)\s*(?:instantiate|Instantiate)"
)
RUNTIME_DATA_CALL_PATTERN = (
	r"(?:\bload|\bpreload|ResourceLoader(?:::|\.)(?:load|exists|Load|Exists)|"
	r"ConfigFile(?:::|\.)(?:load|Load)|"
	r"FileAccess(?:::|\.)(?:open|get_file_as_string|get_file_as_bytes|Open|"
	r"GetFileAsString|GetFileAsBytes)|"
	r"[A-Za-z_]\w*\.(?:Load|Open|GetFileAsString|GetFileAsBytes))"
)
STRING_COMMENT_RE = re.compile(
	r'''(?sx)
		"(?:\\.|[^"\\])*(?:"|$)
		|'(?:\\.|[^'\\])*(?:'|$)
		|//[^\r\n]*
		|\#[^\r\n]*
		|/\*.*?(?:\*/|$)
	''')
NON_NEWLINE_RE = re.compile(r"[^\r\n]")

CATEGORY_FIELDS = (
	"model_files",
	"model_scan_coverage_files",
	"active_export_model_files",
	"model_import_sidecars",
	"active_untracked_model_import_sidecars",
	"model_archive_files",
	"production_3d_files",
	"probe_3d_files",
	"scene_3d_files",
	"configuration_3d_files",
)
TOKEN_CATEGORIES = {
	"production_3d_files",
	"probe_3d_files",
	"scene_3d_files",
	"configuration_3d_files",
}


@dataclass(frozen=True)
class Finding:
	check_id: str
	path: str
	detail: str


class DuplicateJSONKeyError(ValueError):
	pass


@dataclass
class Inventory:
	model_files: tuple[str, ...] = ()
	model_file_fingerprints: dict[str, dict[str, int | str]] = field(default_factory=dict)
	model_scan_coverage_files: tuple[str, ...] = ()
	active_export_model_files: tuple[str, ...] = ()
	model_import_sidecars: tuple[str, ...] = ()
	active_untracked_model_import_sidecars: tuple[str, ...] = ()
	model_import_sidecar_fingerprints: dict[str, dict[str, int | str]] = field(
		default_factory=dict)
	model_archive_files: dict[str, dict[str, object]] = field(default_factory=dict)
	production_3d_files: dict[str, dict[str, int]] = field(default_factory=dict)
	probe_3d_files: dict[str, dict[str, int]] = field(default_factory=dict)
	scene_3d_files: dict[str, dict[str, int]] = field(default_factory=dict)
	configuration_3d_files: dict[str, dict[str, int]] = field(default_factory=dict)

	def debt_count(self) -> int:
		# Active/export and scan-coverage lists are explanatory subsets of model
		# debt, not additional debt, so do not double-count them.
		return (
			len(self.model_files) + len(self.model_import_sidecars) +
			len(self.active_untracked_model_import_sidecars) +
			len(self.model_archive_files) +
			len(self.production_3d_files) +
			len(self.probe_3d_files) +
			len(self.scene_3d_files) + len(self.configuration_3d_files)
		)

	def counts(self) -> dict[str, int]:
		return {
			"model_files": len(self.model_files),
			"model_scan_coverage_files": len(self.model_scan_coverage_files),
			"active_export_model_files": len(self.active_export_model_files),
			"model_import_sidecars": len(self.model_import_sidecars),
			"active_untracked_model_import_sidecars": len(
				self.active_untracked_model_import_sidecars),
			"model_archive_files": len(self.model_archive_files),
			"production_3d_files": len(self.production_3d_files),
			"probe_3d_files": len(self.probe_3d_files),
			"scene_3d_files": len(self.scene_3d_files),
			"configuration_3d_files": len(self.configuration_3d_files),
		}


@dataclass
class InitialCeiling:
	model_files: tuple[str, ...]
	model_file_fingerprints: dict[str, dict[str, int | str]]
	model_scan_coverage_files: tuple[str, ...]
	active_export_model_files: tuple[str, ...]
	model_import_sidecars: tuple[str, ...]
	active_untracked_model_import_sidecars: tuple[str, ...]
	model_import_sidecar_fingerprints: dict[str, dict[str, int | str]]
	model_archive_files: dict[str, dict[str, object]]
	production_3d_files: dict[str, dict[str, int]]
	probe_3d_files: dict[str, dict[str, int]]
	scene_3d_files: dict[str, dict[str, int]]
	configuration_3d_files: dict[str, dict[str, int]]
	archive_now_model_files: tuple[str, ...]
	canonical_sha256: str

	def inventory(self) -> Inventory:
		return Inventory(
			model_files=self.model_files,
			model_file_fingerprints=self.model_file_fingerprints,
			model_scan_coverage_files=self.model_scan_coverage_files,
			active_export_model_files=self.active_export_model_files,
			model_import_sidecars=self.model_import_sidecars,
			active_untracked_model_import_sidecars=(
				self.active_untracked_model_import_sidecars),
			model_import_sidecar_fingerprints=self.model_import_sidecar_fingerprints,
			model_archive_files=self.model_archive_files,
			production_3d_files=self.production_3d_files,
			probe_3d_files=self.probe_3d_files,
			scene_3d_files=self.scene_3d_files,
			configuration_3d_files=self.configuration_3d_files,
		)


@dataclass
class Manifest:
	model_files: tuple[str, ...]
	model_file_fingerprints: dict[str, dict[str, int | str]]
	model_scan_coverage_files: tuple[str, ...]
	active_export_model_files: tuple[str, ...]
	model_import_sidecars: tuple[str, ...]
	active_untracked_model_import_sidecars: tuple[str, ...]
	model_import_sidecar_fingerprints: dict[str, dict[str, int | str]]
	model_archive_files: dict[str, dict[str, object]]
	production_3d_files: dict[str, dict[str, int]]
	probe_3d_files: dict[str, dict[str, int]]
	scene_3d_files: dict[str, dict[str, int]]
	configuration_3d_files: dict[str, dict[str, int]]
	archive_now_model_files: tuple[str, ...]
	declared_counts: dict[str, int]
	initial_ceiling: InitialCeiling | None
	metadata: dict = field(default_factory=dict)

	def inventory(self) -> Inventory:
		return Inventory(
			model_files=self.model_files,
			model_file_fingerprints=self.model_file_fingerprints,
			model_scan_coverage_files=self.model_scan_coverage_files,
			active_export_model_files=self.active_export_model_files,
			model_import_sidecars=self.model_import_sidecars,
			active_untracked_model_import_sidecars=(
				self.active_untracked_model_import_sidecars),
			model_import_sidecar_fingerprints=self.model_import_sidecar_fingerprints,
			model_archive_files=self.model_archive_files,
			production_3d_files=self.production_3d_files,
			probe_3d_files=self.probe_3d_files,
			scene_3d_files=self.scene_3d_files,
			configuration_3d_files=self.configuration_3d_files,
		)


@dataclass
class AuditResult:
	inventory: Inventory
	manifest: Manifest | None
	findings: list[Finding]

	@property
	def exact(self) -> bool:
		return self.manifest is not None and not self.findings

	@property
	def satisfied(self) -> bool:
		return self.exact and self.inventory.debt_count() == 0

	@property
	def status(self) -> str:
		return "SATISFIED" if self.satisfied else "UNSATISFIED"


def _relative(path: Path, root: Path) -> str:
	return path.relative_to(root).as_posix()


def _normalise_relative(value: str) -> str:
	normalised = value.replace("\\", "/").strip("/")
	if not normalised or normalised.startswith("../") or "/../" in normalised:
		raise ValueError(f"path is not a safe project-relative path: {value!r}")
	return normalised


def _json_loads_unique(text: str) -> object:
	"""Parse JSON while rejecting shadowed security/contract fields."""
	def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
		result: dict[str, object] = {}
		for key, value in pairs:
			if key in result:
				raise DuplicateJSONKeyError(f"duplicate JSON key: {key!r}")
			result[key] = value
		return result

	return json.loads(text, object_pairs_hook=unique_object)


def _is_active_path(path: Path, root: Path) -> bool:
	relative = _relative(path, root)
	parts = relative.split("/")
	if not parts or parts[0] in NON_ACTIVE_TOP_LEVEL or parts[0].startswith("."):
		return False
	return not any(relative == prefix or relative.startswith(prefix + "/")
		for prefix in NON_ACTIVE_PREFIXES)


def _is_godot_ignored_path(path: Path, root: Path,
		cache: dict[Path, bool] | None = None) -> bool:
	current = path.parent
	visited: list[Path] = []
	while current != root and root in current.parents:
		if cache is not None and current in cache:
			result = cache[current]
			for directory in visited:
				cache[directory] = result
			return result
		visited.append(current)
		if (current / ".gdignore").is_file():
			if cache is not None:
				for directory in visited:
					cache[directory] = True
			return True
		current = current.parent
	if cache is not None:
		for directory in visited:
			cache[directory] = False
	return False


def _is_model_path(path: Path) -> bool:
	return path.suffix.lower() in MODEL_EXTENSIONS or bool(NUMBERED_BLEND_RE.search(path.name))


def _sample_is_model(sample: bytes) -> bool:
	"""Recognise a model from a bounded, format-aware byte sample."""
	if any(sample.startswith(prefix) for prefix in MODEL_MAGIC_PREFIXES):
		return True
	if PLY_HEADER_RE.match(sample):
		return True
	stripped = sample.lstrip(b"\xef\xbb\xbf\t\r\n ")
	if stripped.startswith(b"#usda 1.0") or stripped.startswith(b"Ogawa"):
		return True
	if COLLADA_XML_RE.search(sample) or X3D_XML_RE.search(sample):
		return True
	if stripped.startswith(b"{"):
		# A complete plausible JSON candidate is normally available here.  Parse
		# it so legal key ordering and long extras cannot evade the glTF check;
		# retain the byte-pattern fallback for bounded/corrupt evidence.
		try:
			document = json.loads(stripped.decode("utf-8-sig"))
		except (UnicodeDecodeError, json.JSONDecodeError):
			document = None
		if isinstance(document, dict):
			asset = document.get("asset")
			version = asset.get("version") if isinstance(asset, dict) else None
			content_keys = {
				"accessors", "animations", "buffers", "bufferViews", "cameras",
				"images", "materials", "meshes", "nodes", "samplers", "scenes",
				"skins", "textures",
			}
			if (isinstance(version, str) and re.fullmatch(r"[12](?:\.\d+)?", version)
					and any(key in document for key in content_keys)):
				return True
		if GLTF_JSON_RE.search(sample) and GLTF_CONTENT_RE.search(sample):
			return True
	# Require both a syntactically credible vertex and triangular-or-larger face
	# so ordinary prose/source files mentioning OBJ terms are not classified.
	if b"\0" not in sample and OBJ_VERTEX_RE.search(sample) and OBJ_FACE_RE.search(sample):
		return True
	return bool(b"\0" not in sample and ASCII_STL_RE.search(sample))


def _sample_is_declared_source_text(path: Path, sample: bytes) -> bool:
	"""Distinguish source containing model fixtures from a model payload.

	A source suffix is not a directory waiver: named model extensions are handled
	before this check, and binary or document-level disguised models remain debt.
	Only credible UTF-8 program text whose *document* is not itself a known model
	format is protected from signatures embedded in literals and test fixtures.
	"""
	if path.suffix.lower() not in SOURCE_TEXT_EXTENSIONS or b"\0" in sample:
		return False
	if any(sample.startswith(prefix) for prefix in MODEL_MAGIC_PREFIXES):
		return False
	try:
		sample.decode("utf-8")
	except UnicodeDecodeError as error:
		# A bounded prefix may end between bytes of one otherwise-valid UTF-8
		# codepoint.  Accept only that terminal truncation; malformed bytes inside
		# the sample still prove this is not credible source text.
		if error.reason != "unexpected end of data" or error.end != len(sample):
			return False
	stripped = sample.lstrip(b"\xef\xbb\xbf\t\r\n ")
	if not stripped:
		return True
	if stripped.startswith((
			b"{", b"<", b"#usda 1.0", b"Ogawa", b"ply\n", b"ply\r\n",
			b"solid ", b"solid\t", b"solid\r", b"solid\n")):
		return False
	# Preserve disguised OBJ detection when the first non-comment record is
	# model syntax, while allowing fixture records inside ordinary source code.
	first_record = next((
		line.lstrip() for line in stripped.splitlines()
		if line.strip() and not line.lstrip().startswith(b"#")
	), b"")
	if (first_record.startswith((
			b"v ", b"v\t", b"mtllib ", b"mtllib\t", b"o ", b"o\t",
			b"g ", b"g\t", b"usemtl ", b"usemtl\t", b"s ", b"s\t"))
			and OBJ_VERTEX_RE.search(sample) and OBJ_FACE_RE.search(sample)):
		return False
	return True


def _sample_is_model_for_path(path: Path, sample: bytes) -> bool:
	return (not _sample_is_declared_source_text(path, sample)
		and _sample_is_model(sample))


def _plausible_model_text(sample: bytes) -> bool:
	stripped = sample.lstrip(b"\xef\xbb\xbf\t\r\n ")
	return stripped.startswith((b"{", b"<"))


def _read_model_sample_with_coverage(stream, budget: int,
		declared_size: int | None = None) -> tuple[bytes, bool]:
	"""Read signatures within ``budget`` and report incomplete text coverage.

	Binary formats need only their bounded leading signature.  Plausible JSON
	or XML is read completely up to the caller's cap.  A candidate longer than
	the cap is never silently accepted as 2D: the boolean becomes explicit
	coverage debt.
	"""
	budget = max(0, budget)
	first_limit = min(budget, MODEL_SAMPLE_BYTES)
	first = stream.read(first_limit)
	chunks = [first]
	# JSON permits arbitrarily long leading whitespace.  Continue within the
	# same cap until a format-significant byte is available; if the cap ends
	# first, report coverage debt rather than silently clearing the file.
	while (first and not first.lstrip(b"\xef\xbb\xbf\t\r\n ")
			and sum(map(len, chunks)) < budget):
		chunk = stream.read(min(
			MODEL_SAMPLE_BYTES, budget - sum(map(len, chunks))))
		if not chunk:
			break
		chunks.append(chunk)
		first = b"".join(chunks)
	if not _plausible_model_text(first):
		total = sum(map(len, chunks))
		all_whitespace = not first.lstrip(b"\xef\xbb\xbf\t\r\n ")
		if declared_size is not None:
			truncated = bool(declared_size > total and all_whitespace)
		else:
			truncated = bool(
				all_whitespace and total >= budget and budget > 0 and stream.read(1))
		return b"".join(chunks), truncated
	first = b"".join(chunks)
	chunks = [first]
	total = len(first)
	while total < budget:
		chunk = stream.read(min(MODEL_SAMPLE_BYTES, budget - total))
		if not chunk:
			break
		chunks.append(chunk)
		total += len(chunk)
	if declared_size is not None:
		truncated = declared_size > total
	elif total >= budget and budget > 0:
		truncated = bool(stream.read(1))
	else:
		truncated = False
	return b"".join(chunks), truncated


def _read_model_sample(stream, budget: int) -> bytes:
	return _read_model_sample_with_coverage(stream, budget)[0]


def _path_model_scan_details(path: Path,
		detect_zip: bool = False) -> tuple[bytes, bool, bool]:
	try:
		size = path.stat().st_size
		with path.open("rb") as stream:
			sample, coverage = _read_model_sample_with_coverage(
				stream, MODEL_TEXT_SCAN_BYTES, declared_size=size)
			is_zip = bool(detect_zip and size >= 22 and zipfile.is_zipfile(stream))
			return sample, coverage, is_zip
	except OSError:
		return b"", False, False


def _path_model_scan(path: Path) -> tuple[bytes, bool]:
	sample, coverage, _is_zip = _path_model_scan_details(path)
	return sample, coverage


def _path_model_sample(path: Path) -> bytes:
	return _path_model_scan(path)[0]


def _has_model_magic(path: Path) -> bool:
	"""Recognise credible model signatures even when the extension is disguised."""
	return _sample_is_model_for_path(path, _path_model_sample(path))


def _is_model_or_scan_coverage(path: Path) -> bool:
	sample, coverage = _path_model_scan(path)
	return coverage or _sample_is_model_for_path(path, sample)


def _is_model_resource(path: Path) -> bool:
	return _is_model_path(path) or _is_model_or_scan_coverage(path)


def _fingerprint(path: Path) -> dict[str, int | str] | None:
	try:
		digest = hashlib.sha256()
		size = 0
		with path.open("rb") as stream:
			for chunk in iter(lambda: stream.read(1024 * 1024), b""):
				digest.update(chunk)
				size += len(chunk)
	except OSError:
		return None
	return {"size": size, "sha256": digest.hexdigest()}


def _text_fingerprint(path: Path) -> dict[str, int | str] | None:
	"""Fingerprint repository text using Git's LF-canonical byte form."""
	try:
		data = path.read_bytes().replace(b"\r\n", b"\n")
	except OSError:
		return None
	return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def _is_model_import_sidecar(path: Path) -> bool:
	return bool(MODEL_IMPORT_SIDECAR_RE.search(path.name))


def _is_model_import_sidecar_resource(path: Path) -> bool:
	if _is_model_import_sidecar(path):
		return True
	if path.suffix.lower() != ".import" or not path.is_file():
		return False
	try:
		text = path.read_text(encoding="utf-8", errors="replace")[:MODEL_SAMPLE_BYTES]
	except OSError:
		return False
	return bool(MODEL_REFERENCE_RE.search(text))


def _archive_sample_kind(sample: bytes) -> str | None:
	# ZIP permits a prepended executable stub.  Search only the bounded leading
	# sample here; top-level candidates are subsequently validated by zipfile.
	if ZIP_MAGIC_RE.search(sample) is not None:
		return "zip"
	if len(sample) >= 262 and sample[257:262] == b"ustar":
		return "tar"
	if SEVEN_ZIP_MAGIC in sample or any(magic in sample for magic in RAR_MAGICS):
		return "opaque"
	if sample.startswith((b"\x1f\x8b", b"BZh", b"\xfd7zXZ\x00")):
		return "compressed"
	return None


def _archive_suffix_kind(path: Path) -> str | None:
	name = path.name.lower()
	if name.endswith(ZIP_ARCHIVE_EXTENSIONS):
		return "zip"
	if name.endswith(TAR_ARCHIVE_EXTENSIONS):
		return "tar"
	if name.endswith(OPAQUE_ARCHIVE_EXTENSIONS):
		return "opaque"
	return None


def _archive_kind(path: Path, sample: bytes | None = None) -> str | None:
	suffix_kind = _archive_suffix_kind(path)
	if suffix_kind is not None:
		return suffix_kind
	if sample is None:
		try:
			with path.open("rb") as stream:
				sample = stream.read(ARCHIVE_MAGIC_BYTES)
		except OSError:
			return None
	sample = sample[:ARCHIVE_MAGIC_BYTES]
	kind = _archive_sample_kind(sample)
	# A valid ZIP may carry an arbitrarily long native/self-extracting prefix.
	# zipfile validates from the bounded central-directory tail, independently
	# of the outer suffix and without decompressing members.
	if kind is None:
		try:
			if path.stat().st_size >= 22 and zipfile.is_zipfile(path):
				return "zip"
		except OSError:
			return None
	if kind == "zip":
		try:
			return "zip" if zipfile.is_zipfile(path) else None
		except OSError:
			return None
	if kind in {"opaque", "tar"}:
		return kind
	# A compressed tar has no raw ustar marker.  Only ask tarfile to validate
	# recognised compression containers so ordinary arbitrary files stay cheap
	# and never become archive debt merely because of their suffix.
	if kind == "compressed":
		try:
			if tarfile.is_tarfile(path):
				return "tar"
		except (OSError, EOFError, tarfile.TarError, lzma.LZMAError):
			pass
		return "compressed"
	return None


def _compressed_stream(sample: bytes):
	if sample.startswith(b"\x1f\x8b"):
		return gzip.GzipFile(fileobj=io.BytesIO(sample), mode="rb")
	if sample.startswith(b"BZh"):
		return bz2.BZ2File(io.BytesIO(sample), mode="rb")
	if sample.startswith(b"\xfd7zXZ\x00"):
		return lzma.LZMAFile(io.BytesIO(sample), mode="rb")
	return None


def _read_path_bytes_bounded(path: Path, limit: int) -> tuple[bytes, bool]:
	try:
		with path.open("rb") as stream:
			chunks: list[bytes] = []
			total = 0
			while total < limit:
				chunk = stream.read(min(MODEL_SAMPLE_BYTES, limit - total))
				if not chunk:
					break
				chunks.append(chunk)
				total += len(chunk)
			return b"".join(chunks), bool(stream.read(1)) if total >= limit else False
	except OSError:
		return b"", True


def _decompress_bytes_bounded(payload: bytes, budget: int,
		depth: int = 0) -> tuple[bytes, bool, bool]:
	"""Return bounded recursively decompressed bytes, overflow, and error."""
	if depth >= 3:
		return payload[:budget], True, False
	stream = _compressed_stream(payload)
	if stream is None:
		return payload[:budget], len(payload) > budget, False
	chunks: list[bytes] = []
	total = 0
	try:
		with stream:
			while total < budget:
				chunk = stream.read(min(MODEL_SAMPLE_BYTES, budget - total))
				if not chunk:
					break
				chunks.append(chunk)
				total += len(chunk)
			overflow = bool(stream.read(1)) if total >= budget else False
	except (OSError, EOFError, ValueError, lzma.LZMAError):
		return b"".join(chunks), False, True
	result = b"".join(chunks)
	if _archive_sample_kind(result) == "compressed":
		return _decompress_bytes_bounded(result, budget, depth + 1)
	return result, overflow, False


def _member_is_model_resource(member: str) -> bool:
	member_path = Path(member.replace("\\", "/"))
	return _is_model_path(member_path) or _is_model_import_sidecar(member_path)


def _archive_member_marker(member: str, reason: str) -> str:
	return f"{member.replace(chr(92), '/')}::<{reason}>"


def _read_stream_bounded(stream, limit: int) -> tuple[bytes, bool]:
	chunks: list[bytes] = []
	total = 0
	while total < limit:
		chunk = stream.read(min(MODEL_SAMPLE_BYTES, limit - total))
		if not chunk:
			break
		chunks.append(chunk)
		total += len(chunk)
	return b"".join(chunks), bool(stream.read(1)) if total >= limit else False


def _is_long_sfx_candidate(sample: bytes) -> bool:
	return sample.startswith((b"MZ", b"\x7fELF", b"#!"))


def _model_archive_evidence(path: Path) -> dict[str, object] | None:
	kind = _archive_kind(path)
	if kind is None:
		return None
	members: list[str] = []
	sniff_budget = ARCHIVE_SNIFF_BUDGET
	try:
		if kind == "zip":
			with zipfile.ZipFile(path) as archive:
				infos = archive.infolist()
				if len(infos) > ARCHIVE_MEMBER_LIMIT:
					members.append("<archive-member-limit-exceeded>")
				for info in infos[:ARCHIVE_MEMBER_LIMIT]:
					if info.is_dir():
						continue
					name = info.filename.replace("\\", "/")
					member_path = Path(name)
					if _archive_suffix_kind(member_path) is not None:
						members.append(_archive_member_marker(
							name, "nested-archive-review-required"))
						continue
					if _member_is_model_resource(name):
						members.append(name)
						continue
					ratio = info.file_size / max(info.compress_size, 1)
					if info.file_size >= ARCHIVE_RATIO_MIN_SIZE and ratio > ARCHIVE_RATIO_LIMIT:
						members.append(_archive_member_marker(
							name, "unsafe-compression-review-required"))
						continue
					if sniff_budget <= 0:
						members.append("<archive-sniff-budget-exceeded>")
						break
					try:
						with archive.open(info) as member_stream:
							sample, coverage = _read_model_sample_with_coverage(
								member_stream, sniff_budget, declared_size=info.file_size)
					except (OSError, RuntimeError, zipfile.BadZipFile, EOFError):
						members.append(_archive_member_marker(
							name, "unreadable-member-review-required"))
						continue
					sniff_budget -= len(sample)
					if coverage:
						members.append(_archive_member_marker(
							name, "model-signature-scan-limit-exceeded"))
						continue
					if _archive_sample_kind(sample) is not None:
						members.append(_archive_member_marker(
							name, "nested-archive-review-required"))
						continue
					if _is_long_sfx_candidate(sample) and info.file_size > len(sample):
						if info.file_size > sniff_budget + len(sample):
							members.append(_archive_member_marker(
								name, "archive-member-tail-review-required"))
							continue
						try:
							with archive.open(info) as member_stream:
								full_member, overflow = _read_stream_bounded(
									member_stream, info.file_size)
						except (OSError, RuntimeError, zipfile.BadZipFile, EOFError):
							members.append(_archive_member_marker(
								name, "unreadable-member-review-required"))
							continue
						sniff_budget -= max(0, len(full_member) - len(sample))
						if overflow:
							members.append(_archive_member_marker(
								name, "archive-member-tail-review-required"))
							continue
						if zipfile.is_zipfile(io.BytesIO(full_member)):
							members.append(_archive_member_marker(
								name, "nested-archive-review-required"))
							continue
					if _sample_is_model(sample):
						members.append(_archive_member_marker(
							name, "disguised-model-signature"))
		elif kind == "tar":
			with tarfile.open(path, mode="r:*") as archive:
				for index, member in enumerate(archive):
					if index >= ARCHIVE_MEMBER_LIMIT:
						members.append("<archive-member-limit-exceeded>")
						break
					if not member.isfile():
						continue
					name = member.name.replace("\\", "/")
					member_path = Path(name)
					if _archive_suffix_kind(member_path) is not None:
						members.append(_archive_member_marker(
							name, "nested-archive-review-required"))
						continue
					if _member_is_model_resource(name):
						members.append(name)
						continue
					if sniff_budget <= 0:
						members.append("<archive-sniff-budget-exceeded>")
						break
					try:
						member_stream = archive.extractfile(member)
						coverage = False
						if member_stream is None:
							sample = b""
						else:
							with member_stream:
								sample, coverage = _read_model_sample_with_coverage(
									member_stream, sniff_budget, declared_size=member.size)
					except (OSError, tarfile.TarError, EOFError):
						members.append(_archive_member_marker(
							name, "unreadable-member-review-required"))
						continue
					sniff_budget -= len(sample)
					if coverage:
						members.append(_archive_member_marker(
							name, "model-signature-scan-limit-exceeded"))
						continue
					if _archive_sample_kind(sample) is not None:
						members.append(_archive_member_marker(
							name, "nested-archive-review-required"))
						continue
					if _is_long_sfx_candidate(sample) and member.size > len(sample):
						if member.size > sniff_budget + len(sample):
							members.append(_archive_member_marker(
								name, "archive-member-tail-review-required"))
							continue
						try:
							member_stream = archive.extractfile(member)
							if member_stream is None:
								full_member, overflow = b"", False
							else:
								with member_stream:
									full_member, overflow = _read_stream_bounded(
										member_stream, member.size)
						except (OSError, EOFError, tarfile.TarError):
							members.append(_archive_member_marker(
								name, "unreadable-member-review-required"))
							continue
						sniff_budget -= max(0, len(full_member) - len(sample))
						if overflow:
							members.append(_archive_member_marker(
								name, "archive-member-tail-review-required"))
							continue
						if zipfile.is_zipfile(io.BytesIO(full_member)):
							members.append(_archive_member_marker(
								name, "nested-archive-review-required"))
							continue
					if _sample_is_model(sample):
						members.append(_archive_member_marker(
							name, "disguised-model-signature"))
		elif kind == "compressed":
			raw, raw_overflow = _read_path_bytes_bounded(path, ARCHIVE_SNIFF_BUDGET)
			payload, payload_overflow, failed = _decompress_bytes_bounded(
				raw, ARCHIVE_SNIFF_BUDGET)
			if failed or raw_overflow:
				members = ["<compressed-payload-review-required>"]
			elif payload_overflow:
				members = ["<compressed-payload-budget-exceeded>"]
			elif _sample_is_model(payload):
				members = ["<compressed-model-signature>"]
			elif _archive_sample_kind(payload) is not None:
				members = ["<nested-archive-review-required>"]
		else:
			# Python's standard library cannot safely inspect RAR/7z.  Keep an
			# explicit review debt instead of silently declaring the archive 2D.
			members = ["<opaque-review-required>"]
	except (OSError, EOFError, ValueError, lzma.LZMAError,
			tarfile.TarError, zipfile.BadZipFile):
		members = ["<opaque-review-required>"]
	if not members:
		return None
	fingerprint = _fingerprint(path)
	if fingerprint is None:
		return None
	unique_members = sorted(set(members))
	return {
		"model_member_count": len(unique_members),
		"model_members": unique_members,
		"size": fingerprint["size"],
		"sha256": fingerprint["sha256"],
	}


def _split_simple_concat(expression: str) -> list[str]:
	parts: list[str] = []
	start = 0
	quote = ""
	escaped = False
	depth = 0
	for index, character in enumerate(expression):
		if escaped:
			escaped = False
			continue
		if character == "\\" and quote:
			escaped = True
			continue
		if quote:
			if character == quote:
				quote = ""
			continue
		if character in {"\"", "'"}:
			quote = character
		elif character in "([{":
			depth += 1
		elif character in ")]}":
			depth = max(0, depth - 1)
		elif character == "+" and depth == 0:
			parts.append(expression[start:index].strip())
			start = index + 1
	parts.append(expression[start:].strip())
	return parts


def _matching_parenthesis(text: str, open_index: int) -> int | None:
	depth = 0
	quote = ""
	escaped = False
	for index in range(open_index, len(text)):
		character = text[index]
		if escaped:
			escaped = False
			continue
		if quote:
			if character == "\\":
				escaped = True
			elif character == quote:
				quote = ""
			continue
		if character in {"\"", "'"}:
			quote = character
		elif character == "(":
			depth += 1
		elif character == ")":
			depth -= 1
			if depth == 0:
				return index
	return None


def _whole_call_argument(expression: str, call_names: Iterable[str]) -> str | None:
	for call_name in call_names:
		match = re.match(rf"^{re.escape(call_name)}\s*\(", expression)
		if match is None:
			continue
		open_index = expression.find("(", match.start())
		close_index = _matching_parenthesis(expression, open_index)
		if close_index == len(expression) - 1:
			return expression[open_index + 1:close_index]
	return None


def _simple_string_value(expression: str, assignments: Mapping[str, str]) -> str | None:
	expression = expression.strip()
	while expression.startswith("("):
		close_index = _matching_parenthesis(expression, 0)
		if close_index != len(expression) - 1:
			break
		expression = expression[1:-1].strip()
	wrapper_argument = _whole_call_argument(
		expression, ("String", "StringName", "ProjectSettings.globalize_path"))
	if wrapper_argument is not None:
		return _simple_string_value(wrapper_argument, assignments)
	path_join = re.fullmatch(r"(.+)\.path_join\s*\((.*)\)", expression)
	if path_join is not None:
		base = _simple_string_value(path_join.group(1), assignments)
		child = _simple_string_value(path_join.group(2), assignments)
		if base is not None and child is not None:
			return base.rstrip("/\\") + "/" + child.lstrip("/\\")
	parts = _split_simple_concat(expression)
	values: list[str] = []
	for part in parts:
		literal = re.fullmatch(r"(?:&|\^)?([\"'])(.*?)\1", part)
		if literal:
			values.append(literal.group(2))
		elif re.fullmatch(r"[A-Za-z_]\w*", part) and part in assignments:
			values.append(assignments[part])
		elif part != expression and (
				value := _simple_string_value(part, assignments)) is not None:
			values.append(value)
		else:
			return None
	return "".join(values)


def _simple_string_assignments(text: str) -> dict[str, str]:
	expressions: dict[str, str] = {}
	assignment_res = (
		re.compile(
			r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
			r"(?:\s*:[^=\n]+)?\s*(?::=|=)\s*([^\r\n#]+)"),
		re.compile(
			r"(?m)^\s*(?:(?:public|private|protected|internal|static|readonly|const)\s+)*"
			r"(?:std::)?(?:string|String|StringName|auto|char\s*(?:const\s*)?\*+)"
			r"\s+([A-Za-z_]\w*)\s*=\s*([^;\r\n]+)"),
	)
	for assignment_re in assignment_res:
		for match in assignment_re.finditer(text):
			expressions[match.group(1)] = match.group(2).strip()
	resolved: dict[str, str] = {}
	for _pass in range(len(expressions) + 1):
		changed = False
		for name, expression in expressions.items():
			if name in resolved:
				continue
			value = _simple_string_value(expression, resolved)
			if value is not None:
				resolved[name] = value
				changed = True
		if not changed:
			break
	return resolved


def _call_argument_expressions(text: str, call_pattern: str,
		masked: str | None = None) -> list[str]:
	expressions: list[str] = []
	if masked is None:
		masked = _mask_strings_and_comments(text)
	for match in re.finditer(call_pattern + r"\s*\(", masked):
		open_index = match.end() - 1
		close_index = _matching_parenthesis(masked, open_index)
		if close_index is not None:
			expression = text[open_index + 1:close_index]
			parts: list[str] = []
			start = 0
			quote = ""
			escaped = False
			depth = 0
			for index, character in enumerate(expression):
				if escaped:
					escaped = False
					continue
				if quote:
					if character == "\\":
						escaped = True
					elif character == quote:
						quote = ""
					continue
				if character in {"\"", "'"}:
					quote = character
				elif character in "([{":
					depth += 1
				elif character in ")]}":
					depth = max(0, depth - 1)
				elif character == "," and depth == 0:
					parts.append(expression[start:index])
					break
			expressions.append((parts[0] if parts else expression).strip())
	return expressions


def _resolved_call_strings(text: str, call_pattern: str,
		assignments: Mapping[str, str] | None = None,
		masked: str | None = None) -> list[str]:
	if assignments is None:
		assignments = _simple_string_assignments(text)
	resolved: list[str] = []
	for expression in _call_argument_expressions(text, call_pattern, masked):
		value = _simple_string_value(expression, assignments)
		if value is not None:
			resolved.append(value)
	return resolved


def _mask_strings_and_comments(text: str) -> str:
	"""Preserve layout while hiding prose from ambiguous API matching."""
	return STRING_COMMENT_RE.sub(
		lambda match: NON_NEWLINE_RE.sub(" ", match.group(0)), text)


def _contextual_3d_api_counts(text: str, *, scene_resource: bool = False) -> Counter[str]:
	counts: Counter[str] = Counter()
	if AMBIGUOUS_CLASS_SEARCH_RE.search(text) is None:
		return counts
	code = _mask_strings_and_comments(text)
	spans: dict[str, set[tuple[int, int]]] = {
		class_name: set() for class_name in AMBIGUOUS_3D_API_CLASSES
	}
	for pattern in AMBIGUOUS_API_RES:
		for match in pattern.finditer(code):
			spans[match.group("class")].add(match.span("class"))
	for container in re.finditer(
			r"\b(?:Array|Dictionary)\s*\[([^\]\r\n]*)\]|<([^>\r\n]*)>", code):
		body_group = 1 if container.group(1) is not None else 2
		body = container.group(body_group)
		body_start = container.start(body_group)
		for match in AMBIGUOUS_CLASS_SEARCH_RE.finditer(body):
			spans[match.group(0)].add((
				body_start + match.start(), body_start + match.end()))
	if scene_resource:
		# Text Godot resources declare class names inside quoted type fields.
		for match in AMBIGUOUS_SCENE_TYPE_RE.finditer(text):
			spans[match.group("class")].add(match.span("class"))
	for class_name, class_spans in spans.items():
		if class_spans:
			counts[class_name] += len(class_spans)
	return counts


def _is_3d_class_name(value: str) -> bool:
	classes = AMBIGUOUS_3D_API_CLASSES | FORBIDDEN_NAMED_TOKENS
	return value.endswith("3D") or value in classes


def _classdb_counts(text: str) -> Counter[str]:
	"""Resolve simple cross-language ClassDB calls and fail closed on loaders."""
	counts: Counter[str] = Counter()
	assignments = _simple_string_assignments(text)
	masked = _mask_strings_and_comments(text)
	for value in _resolved_call_strings(
			text, CLASSDB_ANY_CALL_PATTERN, assignments, masked):
		if _is_3d_class_name(value):
			counts["<resolved-3d-class>"] += 1
	for expression in _call_argument_expressions(
			text, CLASSDB_INSTANTIATE_CALL_PATTERN, masked):
		if _simple_string_value(expression, assignments) is None:
			counts["<dynamic-classdb-instantiation>"] += 1
	return counts


def _visual_shader_code_counts(text: str) -> Counter[str]:
	"""Track VisualShader instances so genuine 2D modes remain allowed."""
	counts: Counter[str] = Counter()
	masked = _mask_strings_and_comments(text)
	known_variables: set[str] = set()
	new_variables: Counter[str] = Counter()
	configured_variables: Counter[str] = Counter()

	gdscript_new_re = re.compile(
		r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
		r"(?:\s*:\s*VisualShader)?\s*(?::=|=)\s*"
		r"VisualShader\s*\.\s*new\s*\(\s*\)")
	gdscript_new_matches = tuple(gdscript_new_re.finditer(masked))
	for match in gdscript_new_matches:
		known_variables.add(match.group(1))
	csharp_new_re = re.compile(
		r"\b(?:var|(?:Godot\.)?VisualShader)\s+([A-Za-z_]\w*)\s*=\s*"
		r"new\s+(?:Godot\.)?VisualShader\s*\(\s*\)")
	csharp_new_matches = tuple(csharp_new_re.finditer(masked))
	for match in csharp_new_matches:
		known_variables.add(match.group(1))
	for match in re.finditer(
			r"\b(?:Godot\.)?VisualShader\s+([A-Za-z_]\w*)\s*=\s*new\s*\(\s*\)",
			masked):
		known_variables.add(match.group(1))
	csharp_object_initializers: list[tuple[str, str]] = []
	object_initializer_res = (
		re.compile(
			r"\b(?:var|(?:Godot\.)?VisualShader)\s+([A-Za-z_]\w*)\s*=\s*"
			r"new\s+(?:Godot\.)?VisualShader\b(?:\s*\(\s*\))?\s*"
			r"\{([^{}]*)\}"),
		re.compile(
			r"\b(?:Godot\.)?VisualShader\s+([A-Za-z_]\w*)\s*=\s*"
			r"new\s*\(\s*\)\s*\{([^{}]*)\}"),
	)
	for initializer_re in object_initializer_res:
		for match in initializer_re.finditer(masked):
			known_variables.add(match.group(1))
			csharp_object_initializers.append((
				match.group(1), text[match.start(2):match.end(2)]))

	for match in re.finditer(
			r"\b(?:([A-Za-z_]\w*)\s*:\s*VisualShader|"
			r"(?:Godot\.|godot::)?VisualShader\s*(?:\?|\[\])?\s*[*&]?\s+"
			r"([A-Za-z_]\w*)|"
			r"Ref\s*<\s*(?:godot::)?VisualShader\s*>\s*[*&]?\s*([A-Za-z_]\w*))",
			masked):
		known_variables.add(next(group for group in match.groups() if group))

	# ClassDB-created VisualShaders need the same numeric-mode scrutiny even
	# though VisualShader itself is not intrinsically 3D.
	assignment_re = re.compile(
		r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
		r"(?:\s*:[^=\r\n]+)?\s*(?::=|=)\s*([^\r\n#]+)")
	classdb_assignment_res = (
		assignment_re,
		re.compile(
			r"(?m)^\s*(?:auto|var|VisualShader\s*[*&]?)\s+([A-Za-z_]\w*)"
			r"\s*=\s*([^;\r\n]+)"),
	)
	classdb_constructions: set[tuple[str, int]] = set()
	for classdb_assignment_re in classdb_assignment_res:
		for match in classdb_assignment_re.finditer(masked):
			rhs = text[match.start(2):match.end(2)]
			if "VisualShader" in _resolved_call_strings(
					rhs, CLASSDB_INSTANTIATE_CALL_PATTERN):
				known_variables.add(match.group(1))
				classdb_constructions.add((match.group(1), match.start(1)))
	for variable, _position in classdb_constructions:
		new_variables[variable] += 1

	# Count direct construction assignments, including target-typed C# new().
	assigned_explicit_constructors = 0
	for variable in tuple(known_variables):
		explicit = len(re.findall(
			rf"\b{re.escape(variable)}\s*(?::=|=)\s*(?:"
			r"VisualShader\s*\.\s*new\s*\(\s*\)|"
			r"new\s+(?:Godot\.)?VisualShader\b(?:\s*\(\s*\))?)", masked))
		target_typed = len(re.findall(
			rf"\b{re.escape(variable)}\s*=\s*new\s*\(\s*\)", masked))
		new_variables[variable] += explicit + target_typed
		assigned_explicit_constructors += explicit

	# C++ Ref<T>.instantiate() is the native equivalent of VisualShader.new().
	for variable in tuple(known_variables):
		new_variables[variable] += len(re.findall(
			rf"\b{re.escape(variable)}\s*(?:\.|->)\s*instantiate\s*\(\s*\)",
			masked))

	mode_assignment_re = re.compile(
		r"(?m)\b([A-Za-z_]\w*)\s*!?\s*(?:\[[^\]\r\n]+\]\s*)?"
		r"(?:\.|->)\s*(?:mode|Mode)\s*=\s*"
		r"([^;\r\n#]+)")
	for match in mode_assignment_re.finditer(masked):
		variable = match.group(1)
		if variable not in known_variables:
			continue
		configured_variables[variable] += 1
		mode = re.sub(r"\s+", "", match.group(2))
		if VISUAL_SHADER_3D_MODE_RE.fullmatch(mode):
			counts["<3d-visual-shader-code>"] += 1
		elif not (VISUAL_SHADER_3D_MODE_RE.fullmatch(mode)
				or VISUAL_SHADER_2D_MODE_RE.fullmatch(mode)):
			counts["<visual-shader-unknown-mode>"] += 1

	if known_variables:
		set_mode_re = re.compile(
			r"\b(" + "|".join(sorted(map(re.escape, known_variables))) +
			r")\s*!?\s*(?:\[[^\]\r\n]+\]\s*)?(?:\.|->)\s*"
			r"(?:set_mode|SetMode)\s*\(")
		for match in set_mode_re.finditer(masked):
			open_index = match.end() - 1
			close_index = _matching_parenthesis(masked, open_index)
			if close_index is None:
				continue
			variable = match.group(1)
			configured_variables[variable] += 1
			argument = text[open_index + 1:close_index]
			mode = re.sub(r"\s+", "", argument)
			if VISUAL_SHADER_3D_MODE_RE.fullmatch(mode):
				counts["<3d-visual-shader-code>"] += 1
			elif not (VISUAL_SHADER_3D_MODE_RE.fullmatch(mode)
					or VISUAL_SHADER_2D_MODE_RE.fullmatch(mode)):
				counts["<visual-shader-unknown-mode>"] += 1

	for variable, body in csharp_object_initializers:
		mode_match = re.search(r"\bMode\s*=\s*([^,}]+)", body)
		if mode_match is None:
			continue
		configured_variables[variable] += 1
		mode = re.sub(r"\s+", "", mode_match.group(1))
		if VISUAL_SHADER_3D_MODE_RE.fullmatch(mode):
			counts["<3d-visual-shader-code>"] += 1
		elif not (VISUAL_SHADER_3D_MODE_RE.fullmatch(mode)
				or VISUAL_SHADER_2D_MODE_RE.fullmatch(mode)):
			counts["<visual-shader-unknown-mode>"] += 1

	# Inline construction/configuration is one instance and must not be mistaken
	# for an unconfigured default merely because it has no variable name.
	inline_configured = 0
	inline_re = re.compile(
		r"(?:(?:VisualShader\s*\.\s*new|new\s+(?:Godot\.)?VisualShader)"
		r"\s*\(\s*\))\s*(?:\.|->)\s*(?:set_mode|SetMode)\s*\(")
	for match in inline_re.finditer(masked):
		close_index = _matching_parenthesis(masked, match.end() - 1)
		if close_index is None:
			continue
		inline_configured += 1
		mode = re.sub(r"\s+", "", text[match.end():close_index])
		if VISUAL_SHADER_3D_MODE_RE.fullmatch(mode):
			counts["<3d-visual-shader-code>"] += 1
		elif not (VISUAL_SHADER_3D_MODE_RE.fullmatch(mode)
				or VISUAL_SHADER_2D_MODE_RE.fullmatch(mode)):
			counts["<visual-shader-unknown-mode>"] += 1

	for variable, instance_count in sorted(new_variables.items()):
		unconfigured = instance_count - configured_variables[variable]
		if unconfigured > 0:
			counts["<visual-shader-default-spatial>"] += unconfigured
	all_constructor_count = len(re.findall(
		r"\bVisualShader\s*\.\s*new\s*\(\s*\)", masked))
	all_constructor_count += len(re.findall(
		r"\bnew\s+(?:Godot\.)?VisualShader\b(?:\s*\(\s*\))?", masked))
	standalone = all_constructor_count - assigned_explicit_constructors - inline_configured
	if standalone > 0:
		counts["<visual-shader-default-spatial>"] += (
			standalone)
	return counts


def _multimesh_counts(text: str) -> Counter[str]:
	"""Count shared MultiMesh only when its use is not demonstrably 2D."""
	counts: Counter[str] = Counter()
	masked = _mask_strings_and_comments(text)
	known: set[str] = set()
	constructor_counts: Counter[str] = Counter()
	instances_2d: set[str] = set()
	multimesh_object_initializers: list[tuple[str, str]] = []
	instance_2d_object_initializers: list[tuple[str, str]] = []

	for match in re.finditer(
			r"\b(?:(?:var|const)\s+([A-Za-z_]\w*)(?:\s*:\s*MultiMesh\b)?|"
			r"(?:Godot\.|godot::)?MultiMesh\s*[*&]?\s+([A-Za-z_]\w*)|"
			r"Ref\s*<\s*(?:godot::)?MultiMesh\s*>\s*[*&]?\s*([A-Za-z_]\w*))"
			r"\s*(?::=|=)\s*(?:(?:(?:Godot\.|godot::)?MultiMesh\s*\.\s*new|"
			r"new\s+(?:Godot\.)?MultiMesh)\s*\(\s*\))",
			masked):
		variable = next(group for group in match.groups() if group)
		known.add(variable)
	for match in re.finditer(
			r"\b(?:Godot\.)?MultiMesh\s+([A-Za-z_]\w*)\s*=\s*new\s*\(\s*\)",
			masked):
		known.add(match.group(1))
	for initializer_re in (
		re.compile(
			r"\b(?:var|(?:Godot\.)?MultiMesh)\s+([A-Za-z_]\w*)\s*=\s*"
			r"new\s+(?:Godot\.)?MultiMesh\b(?:\s*\(\s*\))?\s*\{([^{}]*)\}"),
		re.compile(
			r"\b(?:Godot\.)?MultiMesh\s+([A-Za-z_]\w*)\s*=\s*"
			r"new\s*\(\s*\)\s*\{([^{}]*)\}"),
	):
		for match in initializer_re.finditer(masked):
			known.add(match.group(1))
			multimesh_object_initializers.append((
				match.group(1), text[match.start(2):match.end(2)]))
	for match in re.finditer(
			r"\b(?:([A-Za-z_]\w*)\s*:\s*MultiMesh\b|"
			r"(?:Godot\.|godot::)?MultiMesh\s*[*&]?\s+([A-Za-z_]\w*)|"
			r"Ref\s*<\s*(?:godot::)?MultiMesh\s*>\s*[*&]?\s*([A-Za-z_]\w*))",
			masked):
		known.add(next(group for group in match.groups() if group))
	# Fields/parameters may be constructed on a later statement.
	assigned_explicit_constructors = 0
	for variable in tuple(known):
		created = len(re.findall(
			rf"\b{re.escape(variable)}\s*(?::=|=)\s*(?:(?:MultiMesh\s*\.\s*new|"
			r"new\s+(?:Godot\.)?MultiMesh\b)\s*(?:\(\s*\))?|new\s*\(\s*\))",
			masked))
		constructor_counts[variable] += created
		assigned_explicit_constructors += len(re.findall(
			rf"\b{re.escape(variable)}\s*(?::=|=)\s*(?:MultiMesh\s*\.\s*new|"
			r"new\s+(?:Godot\.)?MultiMesh\b)\s*(?:\(\s*\))?", masked))
	# ClassDB creation is a default-format MultiMesh until proven otherwise.
	classdb_constructions: set[tuple[str, int]] = set()
	for assignment_re in (
		re.compile(
			r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
			r"(?:\s*:[^=\r\n]+)?\s*(?::=|=)\s*([^\r\n#]+)"),
		re.compile(
			r"(?m)^\s*(?:auto|Ref\s*<[^>]+>|(?:godot::)?MultiMesh\s*[*&]?)"
			r"\s+([A-Za-z_]\w*)\s*=\s*([^;\r\n]+)"),
	):
		for match in assignment_re.finditer(masked):
			rhs = text[match.start(2):match.end(2)]
			if "MultiMesh" in _resolved_call_strings(
					rhs, CLASSDB_INSTANTIATE_CALL_PATTERN):
				known.add(match.group(1))
				classdb_constructions.add((match.group(1), match.start(1)))
	for variable, _position in classdb_constructions:
		constructor_counts[variable] += 1
	for variable in tuple(known):
		constructor_counts[variable] += len(re.findall(
			rf"\b{re.escape(variable)}\s*(?:\.|->)\s*instantiate\s*\(\s*\)",
			masked))
	for match in re.finditer(
			r"\b(?:([A-Za-z_]\w*)\s*:\s*MultiMeshInstance2D\b|"
			r"(?:var|const)\s+([A-Za-z_]\w*)\s*(?::=|=)\s*"
			r"(?:MultiMeshInstance2D\s*\.\s*new|new\s+MultiMeshInstance2D)\s*\(\s*\)|"
			r"MultiMeshInstance2D\s*[*&]?\s*([A-Za-z_]\w*)(?:\s*=\s*new\s+"
			r"MultiMeshInstance2D\s*\(\s*\))?)", masked):
		instances_2d.add(next(group for group in match.groups() if group))
	for match in re.finditer(
			r"\b(?:var|MultiMeshInstance2D)\s+([A-Za-z_]\w*)\s*=\s*"
			r"new\s+MultiMeshInstance2D\b(?:\s*\(\s*\))?\s*\{([^{}]*)\}",
			masked):
		instances_2d.add(match.group(1))
		instance_2d_object_initializers.append((
			match.group(1), text[match.start(2):match.end(2)]))

	mode_2d: set[str] = set()
	mode_3d: set[str] = set()
	for variable in known:
		access = rf"\b{re.escape(variable)}\s*(?:\.|->)\s*"
		for match in re.finditer(
				access + r"(?:transform_format|TransformFormat)\s*=\s*"
				r"(?:(?:MultiMesh|Godot\.MultiMesh|godot::MultiMesh)\s*"
				r"(?:(?:\.|::)\s*(?:TransformFormatEnum\s*\.\s*)?)?)?"
				r"(?:TRANSFORM_(2D|3D)|Transform(2D|3D)|([01]))", masked):
			mode = match.group(1) or match.group(2) or (
				"2D" if match.group(3) == "0" else "3D")
			(mode_2d if mode == "2D" else mode_3d).add(variable)
		for match in re.finditer(
				access + r"(?:set_transform_format|SetTransformFormat)\s*\(\s*"
				r"(?:(?:MultiMesh|Godot\.MultiMesh|godot::MultiMesh)\s*"
				r"(?:(?:\.|::)\s*(?:TransformFormatEnum\s*\.\s*)?)?)?"
				r"(?:TRANSFORM_(2D|3D)|Transform(2D|3D)|([01]))", masked):
			mode = match.group(1) or match.group(2) or (
				"2D" if match.group(3) == "0" else "3D")
			(mode_2d if mode == "2D" else mode_3d).add(variable)
	for variable, body in multimesh_object_initializers:
		mode_match = re.search(r"\bTransformFormat\s*=\s*([^,}]+)", body)
		if mode_match is None:
			continue
		mode = re.sub(r"\s+", "", mode_match.group(1))
		if re.fullmatch(r"(?:(?:Godot\.)?MultiMesh\.TransformFormatEnum\.)?"
				r"(?:Transform2D|TRANSFORM_2D|0)", mode):
			mode_2d.add(variable)
		elif re.fullmatch(r"(?:(?:Godot\.)?MultiMesh\.TransformFormatEnum\.)?"
				r"(?:Transform3D|TRANSFORM_3D|1)", mode):
			mode_3d.add(variable)

	bound_2d: set[str] = set()
	for instance in instances_2d:
		for match in re.finditer(
				rf"\b{re.escape(instance)}\s*(?:\.|->)\s*(?:multimesh\s*=|"
				r"set_multimesh\s*\()\s*([A-Za-z_]\w*)", masked,
				re.IGNORECASE):
			if match.group(1) in known:
				bound_2d.add(match.group(1))
	for _instance, body in instance_2d_object_initializers:
		for match in re.finditer(r"\bMultimesh\s*=\s*([A-Za-z_]\w*)", body):
			if match.group(1) in known:
				bound_2d.add(match.group(1))

	inline_2d_constructors = 0
	for instance in instances_2d:
		inline_2d_constructors += len(re.findall(
			rf"\b{re.escape(instance)}\s*(?:\.|->)\s*(?:multimesh\s*=|"
			r"set_multimesh\s*\()\s*(?:(?:MultiMesh\s*\.\s*new|"
			r"new\s+(?:Godot\.)?MultiMesh)\s*\(\s*\)|new\s*\(\s*\))",
			masked, re.IGNORECASE))
	inline_object_3d = 0
	inline_object_risk = 0
	inline_object_count = 0
	inline_object_re = re.compile(
		r"\bnew\s+MultiMeshInstance2D\b(?:\s*\(\s*\))?\s*\{"
		r"(?:(?!\}).)*?\bMultimesh\s*=\s*new\s+(?:Godot\.)?MultiMesh\b"
		r"(?:\s*\(\s*\))?(?:\s*\{([^{}]*)\})?", re.IGNORECASE)
	for match in inline_object_re.finditer(masked):
		inline_object_count += 1
		body = text[match.start(1):match.end(1)] if match.group(1) is not None else ""
		mode_match = re.search(r"\bTransformFormat\s*=\s*([^,}]+)", body)
		if mode_match is None:
			continue
		mode = re.sub(r"\s+", "", mode_match.group(1))
		if re.fullmatch(r"(?:(?:Godot\.)?MultiMesh\.TransformFormatEnum\.)?"
				r"(?:Transform3D|TRANSFORM_3D|1)", mode):
			inline_object_3d += 1
		elif not re.fullmatch(
				r"(?:(?:Godot\.)?MultiMesh\.TransformFormatEnum\.)?"
				r"(?:Transform2D|TRANSFORM_2D|0)", mode):
			inline_object_risk += 1
	if inline_object_3d:
		counts["<3d-multimesh>"] += inline_object_3d
	if inline_object_risk:
		counts["<multimesh-default-3d-risk>"] += inline_object_risk

	for variable in sorted(known):
		instance_count = max(1, constructor_counts[variable])
		if variable in mode_3d:
			counts["<3d-multimesh>"] += instance_count
		elif variable not in mode_2d and variable not in bound_2d:
			counts["<multimesh-default-3d-risk>"] += instance_count
		elif constructor_counts[variable] > 1:
			# One observed 2D configuration cannot prove multiple separately-created
			# instances all use the safe format.
			counts["<multimesh-default-3d-risk>"] += constructor_counts[variable] - 1

	all_constructors = len(re.findall(
		r"\b(?:MultiMesh\s*\.\s*new|new\s+(?:Godot\.)?MultiMesh\b)\s*"
		r"(?:\(\s*\))?", masked))
	unassigned = (
		all_constructors - assigned_explicit_constructors - inline_2d_constructors
		- inline_object_count)
	if unassigned > 0:
		counts["<multimesh-default-3d-risk>"] += unassigned
	return counts


def _spatial_visual_shader_count(text: str) -> int:
	"""Count VisualShader resources whose scoped mode is 3D (default/zero)."""
	sections = re.split(r"(?m)(?=^\[)", text)
	root_is_visual = any(
		section.startswith("[gd_resource")
		and re.search(r"\btype\s*=\s*[\"']VisualShader[\"']", section.split("\n", 1)[0])
		for section in sections
	)
	count = 0
	for section in sections:
		header = section.split("\n", 1)[0]
		is_visual_subresource = (
			header.startswith("[sub_resource")
			and re.search(r"\btype\s*=\s*[\"']VisualShader[\"']", header) is not None)
		is_root_resource = root_is_visual and header.startswith("[resource")
		if not (is_visual_subresource or is_root_resource):
			continue
		mode_match = re.search(r"(?m)^\s*mode\s*=\s*(\d+)\s*$", section)
		# Godot modes: spatial=0, canvas=1, particles=2, sky=3, fog=4.
		# Particle-process visual shaders are shared by 2D and 3D emitters, so
		# mode 2 is not intrinsically 3D.  Unknown modes fail closed.
		if mode_match is None or int(mode_match.group(1)) not in {1, 2}:
			count += 1
	return count


def _spatial_multimesh_resource_count(text: str) -> int:
	"""Count serialized MultiMeshes not proven to use a 2D transform/binding."""
	sections = re.split(r"(?m)(?=^\[)", text)
	root_is_multimesh = any(
		section.startswith("[gd_resource")
		and re.search(
			r"\btype\s*=\s*[\"']MultiMesh[\"']", section.split("\n", 1)[0])
			is not None
		for section in sections)
	resources: dict[str, int | None] = {}
	for section in sections:
		header = section.split("\n", 1)[0]
		resource_id: str | None = None
		if root_is_multimesh and header.startswith("[resource"):
			resource_id = "<root>"
		elif (header.startswith("[sub_resource") and re.search(
				r"\btype\s*=\s*[\"']MultiMesh[\"']", header) is not None):
			id_match = re.search(r"\bid\s*=\s*[\"']([^\"']+)[\"']", header)
			resource_id = id_match.group(1) if id_match is not None else "<unknown>"
		if resource_id is None:
			continue
		mode_match = re.search(
			r"(?m)^\s*transform_format\s*=\s*(-?\d+)\s*$", section)
		resources[resource_id] = (
			int(mode_match.group(1)) if mode_match is not None else None)

	bound_2d: set[str] = set()
	bound_3d: set[str] = set()
	for section in sections:
		header = section.split("\n", 1)[0]
		type_match = re.search(r"\btype\s*=\s*[\"']([^\"']+)[\"']", header)
		if type_match is None or type_match.group(1) not in {
				"MultiMeshInstance2D", "MultiMeshInstance3D"}:
			continue
		for reference in re.finditer(
				r"(?m)^\s*multimesh\s*=\s*SubResource\s*\(\s*[\"']([^\"']+)[\"']\s*\)",
				section):
			(bound_2d if type_match.group(1) == "MultiMeshInstance2D"
				else bound_3d).add(reference.group(1))

	count = 0
	for resource_id, mode in resources.items():
		if resource_id in bound_3d:
			count += 1
		elif mode == 0:
			continue
		elif mode is None and resource_id in bound_2d:
			continue
		else:
			# Explicit TRANSFORM_3D=1, defaults outside a known 2D binding,
			# and unknown future values are migration debt.
			count += 1
	return count


def _token_counts(text: str, *, configuration: bool = False,
		scene_resource: bool = False) -> dict[str, int]:
	counts: Counter[str] = Counter(match.group(0) for match in FORBIDDEN_TOKEN_RE.finditer(text))
	counts.update(_contextual_3d_api_counts(text, scene_resource=scene_resource))
	for _match in LOWER_3D_MARKER_RE.finditer(text):
		counts["<lowercase-3d-marker>"] += 1
	for _match in MODEL_REFERENCE_RE.finditer(text):
		counts["<model-reference>"] += 1
	for match in THREE_D_SHADER_RE.finditer(text):
		counts[f"<{match.group(1).lower()}-shader>"] += 1
	if "VisualShader" in text:
		counts.update(_visual_shader_code_counts(text))
	if "MultiMesh" in text:
		counts.update(_multimesh_counts(text))
	if "ClassDB" in text:
		counts.update(_classdb_counts(text))
	if scene_resource:
		visual_shader_count = _spatial_visual_shader_count(text)
		if visual_shader_count:
			counts["<spatial-visual-shader>"] += visual_shader_count
		multimesh_count = _spatial_multimesh_resource_count(text)
		if multimesh_count:
			counts["<3d-multimesh-resource>"] += multimesh_count
	if configuration:
		for _match in CONFIG_3D_RE.finditer(text):
			counts["<3d-configuration>"] += 1
	return dict(sorted(counts.items()))


def _active_files(root: Path) -> Iterable[Path]:
	"""Walk live project paths without descending into declared inactive roots."""
	for directory, child_dirs, filenames in os.walk(root):
		current = Path(directory)
		if current != root and ".gdignore" in filenames:
			child_dirs[:] = []
			continue
		child_dirs[:] = sorted(
			name for name in child_dirs
			if _is_active_path(current / name, root)
		)
		for filename in sorted(filenames):
			yield current / filename


def _production_files(root: Path) -> Iterable[Path]:
	return (
		path for path in _active_files(root)
		if path.suffix.lower() in PRODUCTION_SOURCE_EXTENSIONS
		and not (path.suffix.lower() == ".gd" and path.name.startswith("probe_"))
	)


def _native_binary_files(root: Path) -> Iterable[Path]:
	return (
		path for path in _active_files(root)
		if path.suffix.lower() in NATIVE_BINARY_EXTENSIONS
		or re.search(r"(?i)\.so(?:\.\d+)+$", path.name) is not None
	)


def _opaque_runtime_binary_files(root: Path) -> Iterable[Path]:
	return (
		path for path in _active_files(root)
		if path.suffix.lower() in OPAQUE_RUNTIME_BINARY_EXTENSIONS
	)


def _read_text_cached(path: Path,
		cache: dict[Path, str] | None = None) -> str:
	if cache is not None and path in cache:
		return cache[path]
	text = path.read_text(encoding="utf-8", errors="replace")
	if cache is not None:
		cache[path] = text
	return text


def _runtime_dependency_scope(root: Path,
		active_files: Iterable[Path] | None = None,
		text_cache: dict[Path, str] | None = None) -> tuple[set[str], set[str]]:
	"""Resolve data paths/directories explicitly reached by live game code."""
	paths: set[str] = set()
	directories: set[str] = set()
	active = tuple(_active_files(root) if active_files is None else active_files)
	sources = {
		path for path in active
		if ((path.suffix.lower() in PRODUCTION_SOURCE_EXTENSIONS
			and not (path.suffix.lower() == ".gd" and path.name.startswith("probe_")))
			or path.suffix.lower() in {".tscn", ".tres", ".cfg", ".gdextension"})
	}
	project = root / "project.godot"
	if project.is_file():
		sources.add(project)
	for source in sorted(sources):
		try:
			text = _read_text_cached(source, text_cache)
		except OSError:
			continue
		masked = _mask_strings_and_comments(text)
		assignments = _simple_string_assignments(text)
		for value in _resolved_call_strings(
				text, RUNTIME_DATA_CALL_PATTERN, assignments, masked):
			normalised = _normalise_resource_directory(value)
			if normalised:
				paths.add(normalised)
		directories.update(_directory_iterator_paths(text, assignments, masked))
		for expression in _call_argument_expressions(
				text, RUNTIME_DATA_CALL_PATTERN, masked):
			if _simple_string_value(expression, assignments) is not None:
				continue
			known_values = {
				match.group(2)
				for match in re.finditer(r"(?:&|\^)?([\"'])(.*?)\1", expression)
			}
			known_values.update(
				assignments[name]
				for name in re.findall(r"\b[A-Za-z_]\w*\b", expression)
				if name in assignments)
			for value in known_values:
				normalised = _normalise_resource_directory(value)
				if not normalised or not (
						value.startswith("res://") or "/" in value):
					continue
				if Path(normalised).suffix.lower() in ACTIVE_DATA_EXTENSIONS:
					normalised = normalised.rsplit("/", 1)[0]
				directories.add(normalised.rstrip("/"))
	return paths, directories


def _is_runtime_dependency_path(path: Path, root: Path,
		scope: tuple[set[str], set[str]]) -> bool:
	relative = _relative(path, root)
	paths, directories = scope
	return (_is_runtime_data_path(path, root) or relative in paths or any(
		relative == directory or relative.startswith(directory.rstrip("/") + "/")
		for directory in directories if directory))


def _runtime_data_files(root: Path,
		scope: tuple[set[str], set[str]] | None = None,
		active_files: Iterable[Path] | None = None) -> Iterable[Path]:
	active = tuple(_active_files(root) if active_files is None else active_files)
	if scope is None:
		scope = _runtime_dependency_scope(root, active)
	return (
		path for path in active
		if path.suffix.lower() in ACTIVE_DATA_EXTENSIONS
		and _is_runtime_dependency_path(path, root, scope)
	)


def _native_binary_counts(path: Path) -> dict[str, int]:
	counts: Counter[str] = Counter({"<opaque-native-extension-binary>": 1})
	try:
		with path.open("rb") as stream:
			sample = stream.read(NATIVE_SYMBOL_SCAN_BYTES + 1)
	except OSError:
		counts["<unreadable-native-extension-binary>"] += 1
		return dict(sorted(counts.items()))
	if len(sample) > NATIVE_SYMBOL_SCAN_BYTES:
		counts["<native-symbol-scan-truncated>"] += 1
		sample = sample[:NATIVE_SYMBOL_SCAN_BYTES]
	text = sample.decode("latin-1", errors="ignore")
	for match in FORBIDDEN_TOKEN_RE.finditer(text):
		counts[match.group(0)] += 1
	return dict(sorted(counts.items()))


def _probe_scripts(root: Path) -> Iterable[Path]:
	return (
		path for path in _active_files(root)
		if path.suffix.lower() == ".gd" and path.name.startswith("probe_")
	)


def _scene_text_files(root: Path) -> Iterable[Path]:
	return (
		path for path in _active_files(root)
		if path.suffix.lower() in {".tscn", ".tres"}
	)


def _binary_scene_resource_files(root: Path) -> Iterable[Path]:
	return (
		path for path in _active_files(root)
		if path.suffix.lower() in {".res", ".scn"}
	)


def _configuration_files(root: Path) -> Iterable[Path]:
	paths = {
		path for path in _active_files(root)
		if path.suffix.lower() in {".cfg", ".gdextension"}
	}
	project = root / "project.godot"
	if project.is_file():
		paths.add(project)
	return iter(sorted(paths))


def _repository_model_resources(root: Path,
		archive_kind_cache: dict[str, str | None] | None = None) -> tuple[
		tuple[str, ...], tuple[str, ...], tuple[str, ...],
		dict[str, dict[str, object]]]:
	"""Return tracked models, sidecars and model-bearing archives."""
	try:
		top_level = subprocess.run(
			["git", "-C", str(root), "rev-parse", "--show-toplevel"],
			check=False,
			capture_output=True,
		)
	except OSError:
		top_level = None
	is_repo_root = False
	if top_level is not None and top_level.returncode == 0:
		reported = top_level.stdout.decode("utf-8", errors="replace").strip()
		is_repo_root = Path(reported).resolve() == root
	completed = None
	if is_repo_root:
		completed = subprocess.run(
			["git", "-C", str(root), "ls-files", "-z"],
			check=False,
			capture_output=True,
		)
	if completed is not None and completed.returncode == 0:
		tracked = completed.stdout.decode("utf-8", errors="surrogateescape").split("\0")
		models_list: list[str] = []
		coverage_list: list[str] = []
		sidecars_list: list[str] = []
		archives: dict[str, dict[str, object]] = {}
		for relative in tracked:
			if not relative:
				continue
			normalised = _normalise_relative(relative)
			path = root / relative
			is_named_model = _is_model_path(path)
			if is_named_model:
				sample, coverage, is_zip = b"", False, False
			else:
				sample, coverage, is_zip = _path_model_scan_details(
					path, detect_zip=True)
			if is_named_model or coverage or _sample_is_model_for_path(path, sample):
				models_list.append(normalised)
			if coverage:
				coverage_list.append(normalised)
			if _is_model_import_sidecar_resource(path):
				sidecars_list.append(normalised)
			kind = _archive_suffix_kind(path)
			if kind is None and not is_named_model and is_zip:
				kind = "zip"
			elif (kind is None and not is_named_model
					and _archive_sample_kind(sample) is not None):
				kind = _archive_kind(path, sample)
			if archive_kind_cache is not None:
				archive_kind_cache[normalised] = kind
			if kind is not None:
				evidence = _model_archive_evidence(path)
				if evidence is not None:
					archives[normalised] = evidence
		models = tuple(sorted(models_list))
		coverage_models = tuple(sorted(coverage_list))
		sidecars = tuple(sorted(sidecars_list))
		return models, coverage_models, sidecars, dict(sorted(archives.items()))
	# Disposable unit/stress fixtures are intentionally not Git repositories.
	# There, every on-disk model/sidecar represents what a future commit would
	# track, including content held under a non-runtime source directory.
	files = tuple(
		path for path in root.rglob("*")
		if path.is_file() and not any(
			part in {".git", ".godot", ".venv", "__pycache__"}
			for part in path.relative_to(root).parts)
	)
	models_list: list[str] = []
	coverage_list: list[str] = []
	for path in files:
		if _is_model_path(path):
			models_list.append(_relative(path, root))
			continue
		sample, coverage = _path_model_scan(path)
		if coverage or _sample_is_model_for_path(path, sample):
			models_list.append(_relative(path, root))
		if coverage:
			coverage_list.append(_relative(path, root))
	models = tuple(sorted(models_list))
	coverage_models = tuple(sorted(coverage_list))
	sidecars = tuple(sorted(
		_relative(path, root) for path in files if _is_model_import_sidecar_resource(path)))
	archives = {
		_relative(path, root): evidence
		for path in files
		if (evidence := _model_archive_evidence(path)) is not None
	}
	return models, coverage_models, sidecars, dict(sorted(archives.items()))


def _git_untracked_active_files(root: Path) -> Iterable[Path]:
	relatives: set[str] = set()
	for arguments in (
		("--others", "--exclude-standard", "-z"),
		("--others", "--ignored", "--exclude-standard", "-z"),
	):
		try:
			completed = subprocess.run(
				["git", "-C", str(root), "ls-files", *arguments],
				check=False, capture_output=True,
			)
		except OSError:
			continue
		if completed.returncode == 0:
			relatives.update(
				relative for relative in completed.stdout.decode(
					"utf-8", errors="surrogateescape").split("\0")
				if relative)
	paths: list[Path] = []
	ignore_cache: dict[Path, bool] = {}
	for relative in sorted(relatives):
		path = root / _normalise_relative(relative)
		if (_is_active_path(path, root)
				and not _is_godot_ignored_path(path, root, ignore_cache)):
			paths.append(path)
	return tuple(paths)


def discover(root: Path,
		archive_kind_cache: dict[str, str | None] | None = None,
		text_cache: dict[Path, str] | None = None,
		active_files_cache: list[Path] | None = None) -> Inventory:
	"""Return the complete active 3D/model debt inventory for ``root``."""
	root = root.resolve()
	models, coverage_models, sidecars, model_archives = _repository_model_resources(
		root, archive_kind_cache)
	worktree_only_files = tuple(_git_untracked_active_files(root))
	active_files = tuple(_active_files(root))
	if active_files_cache is not None:
		active_files_cache.extend(active_files)
	# Repository-wide archive debt is tracked-only, but an untracked archive in
	# a live/export path is already runtime debt and must not wait for a commit
	# before the regression gate sees it.
	model_archives = dict(model_archives)
	for path in worktree_only_files:
		relative = _relative(path, root)
		kind = _archive_kind(path)
		if archive_kind_cache is not None:
			archive_kind_cache[relative] = kind
		if relative in model_archives or kind is None:
			continue
		evidence = _model_archive_evidence(path)
		if evidence is not None:
			model_archives[relative] = evidence
	model_archives = dict(sorted(model_archives.items()))
	active_sidecars = {
		_relative(path, root)
		for path in active_files
		if _is_model_import_sidecar_resource(path)
	}
	active_untracked_sidecars = tuple(sorted(active_sidecars - set(sidecars)))
	model_fingerprints = {
		relative: fingerprint
		for relative in models
		if (fingerprint := _fingerprint(root / relative)) is not None
	}
	sidecar_fingerprints = {
		relative: fingerprint
		for relative in sidecars
		if (fingerprint := _text_fingerprint(root / relative)) is not None
	}
	# Repository discovery has already performed binary magic sniffing.  Reuse
	# that result for disguised tracked models, then add ordinary-extension
	# untracked files without reopening every image/audio file in the project.
	active_ignore_cache: dict[Path, bool] = {}
	active_model_set = {
		relative for relative in models
		if (root / relative).is_file() and _is_active_path(root / relative, root)
		and not _is_godot_ignored_path(
			root / relative, root, active_ignore_cache)
	}
	active_model_set.update(
		_relative(path, root)
		for path in active_files
		if _is_model_path(path) or (
			path.suffix.lower() in MAGIC_SNIFF_ACTIVE_EXTENSIONS
			and _is_model_or_scan_coverage(path))
	)
	active_model_set.update(
		_relative(path, root)
		for path in worktree_only_files
		if _is_model_or_scan_coverage(path)
	)
	active_models = tuple(sorted(active_model_set))

	production: dict[str, dict[str, int]] = {}
	for path in (
			candidate for candidate in active_files
			if candidate.suffix.lower() in PRODUCTION_SOURCE_EXTENSIONS
			and not (candidate.suffix.lower() == ".gd"
				and candidate.name.startswith("probe_"))):
		counts = _token_counts(_read_text_cached(path, text_cache))
		if counts:
			production[_relative(path, root)] = counts
	for path in (
			candidate for candidate in active_files
			if candidate.suffix.lower() in NATIVE_BINARY_EXTENSIONS
			or re.search(r"(?i)\.so(?:\.\d+)+$", candidate.name) is not None):
		production[_relative(path, root)] = _native_binary_counts(path)
	for path in (
			candidate for candidate in active_files
			if candidate.suffix.lower() in OPAQUE_RUNTIME_BINARY_EXTENSIONS):
		production[_relative(path, root)] = {"<opaque-runtime-binary>": 1}
	runtime_scope = _runtime_dependency_scope(root, active_files, text_cache)
	for path in _runtime_data_files(root, runtime_scope, active_files):
		counts = _token_counts(_read_text_cached(path, text_cache))
		if counts:
			production[_relative(path, root)] = counts

	probes: dict[str, dict[str, int]] = {}
	for path in (
			candidate for candidate in active_files
			if candidate.suffix.lower() == ".gd"
			and candidate.name.startswith("probe_")):
		counts = _token_counts(_read_text_cached(path, text_cache))
		if counts:
			probes[_relative(path, root)] = counts

	scenes: dict[str, dict[str, int]] = {}
	for path in (
			candidate for candidate in active_files
			if candidate.suffix.lower() in {".tscn", ".tres"}):
		counts = _token_counts(
			_read_text_cached(path, text_cache), scene_resource=True)
		if counts:
			scenes[_relative(path, root)] = counts
	for path in (
			candidate for candidate in active_files
			if candidate.suffix.lower() in {".res", ".scn"}):
		scenes[_relative(path, root)] = {"<opaque-binary-resource>": 1}

	configuration: dict[str, dict[str, int]] = {}
	configuration_paths = {
		candidate for candidate in active_files
		if candidate.suffix.lower() in {".cfg", ".gdextension"}
	}
	project = root / "project.godot"
	if project.is_file():
		configuration_paths.add(project)
	for path in sorted(configuration_paths):
		counts = _token_counts(
			_read_text_cached(path, text_cache), configuration=True)
		if path.suffix.lower() == ".gdextension":
			counts["<native-extension-descriptor>"] = (
				counts.get("<native-extension-descriptor>", 0) + 1)
		if counts:
			configuration[_relative(path, root)] = counts

	return Inventory(
		model_files=models,
		model_file_fingerprints=dict(sorted(model_fingerprints.items())),
		model_scan_coverage_files=coverage_models,
		active_export_model_files=active_models,
		model_import_sidecars=sidecars,
		active_untracked_model_import_sidecars=active_untracked_sidecars,
		model_import_sidecar_fingerprints=dict(sorted(sidecar_fingerprints.items())),
		model_archive_files=model_archives,
		production_3d_files=dict(sorted(production.items())),
		probe_3d_files=dict(sorted(probes.items())),
		scene_3d_files=dict(sorted(scenes.items())),
		configuration_3d_files=dict(sorted(configuration.items())),
	)


def _initial_ceiling_payload(inventory: Inventory,
		archive_now: Iterable[str] = ()) -> dict:
	archive = sorted({_normalise_relative(path) for path in archive_now})
	counts = inventory.counts()
	counts["archive_now_model_files"] = len(archive)
	return {
		"declared_counts": counts,
		"model_files": list(inventory.model_files),
		"model_file_fingerprints": inventory.model_file_fingerprints,
		"model_scan_coverage_files": list(inventory.model_scan_coverage_files),
		"active_export_model_files": list(inventory.active_export_model_files),
		"model_import_sidecars": list(inventory.model_import_sidecars),
		"active_untracked_model_import_sidecars": list(
			inventory.active_untracked_model_import_sidecars),
		"model_import_sidecar_fingerprints": inventory.model_import_sidecar_fingerprints,
		"model_archive_files": inventory.model_archive_files,
		"production_3d_files": inventory.production_3d_files,
		"probe_3d_files": inventory.probe_3d_files,
		"scene_3d_files": inventory.scene_3d_files,
		"configuration_3d_files": inventory.configuration_3d_files,
		"archive_now_model_files": archive,
	}


def _canonical_sha256(document: Mapping) -> str:
	encoded = json.dumps(
		document, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
	).encode("utf-8")
	return hashlib.sha256(encoded).hexdigest()


def _new_initial_ceiling(inventory: Inventory,
		archive_now: Iterable[str] = ()) -> dict:
	payload = _initial_ceiling_payload(inventory, archive_now)
	return {"canonical_sha256": _canonical_sha256(payload), **payload}


def manifest_dict(inventory: Inventory, archive_now: Iterable[str] = (),
		metadata: Mapping | None = None,
		initial_ceiling: Mapping | None = None) -> dict:
	"""Build a canonical manifest document; useful to tests and maintainers."""
	archive = sorted({_normalise_relative(path) for path in archive_now})
	counts = inventory.counts()
	counts["archive_now_model_files"] = len(archive)
	ceiling = dict(initial_ceiling) if initial_ceiling is not None else (
		_new_initial_ceiling(inventory, archive))
	return {
		"schema_version": SCHEMA_VERSION,
		"policy": "Known entries are migration debt, not waivers. Lists may only shrink.",
		"metadata": dict(metadata or {}),
		"initial_ceiling": ceiling,
		"declared_counts": counts,
		"model_files": list(inventory.model_files),
		"model_file_fingerprints": inventory.model_file_fingerprints,
		"model_scan_coverage_files": list(inventory.model_scan_coverage_files),
		"active_export_model_files": list(inventory.active_export_model_files),
		"model_import_sidecars": list(inventory.model_import_sidecars),
		"active_untracked_model_import_sidecars": list(
			inventory.active_untracked_model_import_sidecars),
		"model_import_sidecar_fingerprints": inventory.model_import_sidecar_fingerprints,
		"model_archive_files": inventory.model_archive_files,
		"production_3d_files": inventory.production_3d_files,
		"probe_3d_files": inventory.probe_3d_files,
		"scene_3d_files": inventory.scene_3d_files,
		"configuration_3d_files": inventory.configuration_3d_files,
		"archive_now_model_files": archive,
	}


def _validate_path_list(raw: object, field_name: str) -> tuple[tuple[str, ...], list[Finding]]:
	findings: list[Finding] = []
	if not isinstance(raw, list):
		return (), [Finding("G2D001", field_name, "manifest field must be a list")]
	values: list[str] = []
	for index, item in enumerate(raw):
		if not isinstance(item, str):
			findings.append(Finding(
				"G2D001", f"{field_name}[{index}]", "manifest path must be a string"))
			continue
		try:
			values.append(_normalise_relative(item))
		except ValueError as error:
			findings.append(Finding("G2D001", f"{field_name}[{index}]", str(error)))
	if values != sorted(set(values)):
		findings.append(Finding(
			"G2D001", field_name, "manifest paths must be sorted and unique"))
	return tuple(values), findings


def _validate_token_map(raw: object, field_name: str) -> tuple[dict[str, dict[str, int]], list[Finding]]:
	findings: list[Finding] = []
	if not isinstance(raw, dict):
		return {}, [Finding("G2D001", field_name, "manifest field must be an object")]
	result: dict[str, dict[str, int]] = {}
	keys = list(raw)
	if keys != sorted(keys):
		findings.append(Finding(
			"G2D001", field_name, "manifest file keys must be sorted"))
	for path_value, counts_raw in raw.items():
		if not isinstance(path_value, str):
			findings.append(Finding("G2D001", field_name, "manifest file key must be a string"))
			continue
		try:
			path = _normalise_relative(path_value)
		except ValueError as error:
			findings.append(Finding("G2D001", path_value, str(error)))
			continue
		if not isinstance(counts_raw, dict) or not counts_raw:
			findings.append(Finding(
				"G2D001", path, "token inventory must be a non-empty object"))
			continue
		if list(counts_raw) != sorted(counts_raw):
			findings.append(Finding(
				"G2D001", path, "token keys must be sorted"))
		counts: dict[str, int] = {}
		for token, count in counts_raw.items():
			if not isinstance(token, str) or not isinstance(count, int) or isinstance(count, bool) or count <= 0:
				findings.append(Finding(
					"G2D001", path, f"invalid token count {token!r}: {count!r}"))
				continue
			counts[token] = count
		if counts:
			result[path] = dict(sorted(counts.items()))
	return dict(sorted(result.items())), findings


def _validate_fingerprint_map(raw: object, field_name: str) -> tuple[
		dict[str, dict[str, int | str]], list[Finding]]:
	findings: list[Finding] = []
	if not isinstance(raw, dict):
		return {}, [Finding("G2D001", field_name, "fingerprint field must be an object")]
	if list(raw) != sorted(raw):
		findings.append(Finding(
			"G2D001", field_name, "fingerprint paths must be sorted"))
	result: dict[str, dict[str, int | str]] = {}
	for path_value, fingerprint in raw.items():
		if not isinstance(path_value, str):
			findings.append(Finding(
				"G2D001", field_name, "fingerprint path must be a string"))
			continue
		try:
			path = _normalise_relative(path_value)
		except ValueError as error:
			findings.append(Finding("G2D001", path_value, str(error)))
			continue
		if not isinstance(fingerprint, dict) or set(fingerprint) != {"size", "sha256"}:
			findings.append(Finding(
				"G2D001", path, "fingerprint must contain exactly size and sha256"))
			continue
		size = fingerprint.get("size")
		digest = fingerprint.get("sha256")
		if not isinstance(size, int) or isinstance(size, bool) or size < 0:
			findings.append(Finding("G2D001", path, "fingerprint size must be non-negative"))
			continue
		if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
			findings.append(Finding(
				"G2D001", path, "fingerprint sha256 must be lowercase hexadecimal"))
			continue
		result[path] = {"size": size, "sha256": digest}
	return dict(sorted(result.items())), findings


def _validate_model_archive_map(raw: object, field_name: str) -> tuple[
		dict[str, dict[str, object]], list[Finding]]:
	findings: list[Finding] = []
	if not isinstance(raw, dict):
		return {}, [Finding("G2D001", field_name, "archive evidence must be an object")]
	if list(raw) != sorted(raw):
		findings.append(Finding("G2D001", field_name, "archive paths must be sorted"))
	result: dict[str, dict[str, object]] = {}
	for path_value, evidence in raw.items():
		if not isinstance(path_value, str):
			findings.append(Finding("G2D001", field_name, "archive path must be a string"))
			continue
		try:
			path = _normalise_relative(path_value)
		except ValueError as error:
			findings.append(Finding("G2D001", path_value, str(error)))
			continue
		expected_keys = {"model_member_count", "model_members", "size", "sha256"}
		if not isinstance(evidence, dict) or set(evidence) != expected_keys:
			findings.append(Finding(
				"G2D001", path,
				"archive evidence must contain member count/list, size and sha256"))
			continue
		members = evidence.get("model_members")
		count = evidence.get("model_member_count")
		size = evidence.get("size")
		digest = evidence.get("sha256")
		valid_members = (
			isinstance(members, list) and bool(members)
			and all(isinstance(member, str) and bool(member) for member in members)
			and members == sorted(set(members))
		)
		if not valid_members or count != len(members):
			findings.append(Finding(
				"G2D001", path, "archive model members/count must be non-empty and canonical"))
			continue
		if not isinstance(size, int) or isinstance(size, bool) or size < 0:
			findings.append(Finding("G2D001", path, "archive size must be non-negative"))
			continue
		if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
			findings.append(Finding("G2D001", path, "archive sha256 must be lowercase hex"))
			continue
		result[path] = {
			"model_member_count": count,
			"model_members": list(members),
			"size": size,
			"sha256": digest,
		}
	return dict(sorted(result.items())), findings


def _parse_initial_ceiling(raw: object) -> tuple[InitialCeiling | None, list[Finding]]:
	label = "initial_ceiling"
	if not isinstance(raw, dict):
		return None, [Finding("G2D004", label, "immutable initial ceiling must be an object")]
	expected_keys = {
		"canonical_sha256", "declared_counts", "model_files",
		"model_file_fingerprints",
		"model_scan_coverage_files",
		"active_export_model_files", "model_import_sidecars",
		"active_untracked_model_import_sidecars",
		"model_import_sidecar_fingerprints",
		"model_archive_files",
		"production_3d_files", "probe_3d_files", "scene_3d_files",
		"configuration_3d_files", "archive_now_model_files",
	}
	findings: list[Finding] = []
	if set(raw) != expected_keys:
		findings.append(Finding(
			"G2D004", label,
			f"ceiling keys must be exact; expected {sorted(expected_keys)!r}"))
	payload = {key: value for key, value in raw.items() if key != "canonical_sha256"}
	declared_hash = raw.get("canonical_sha256")
	computed_hash = _canonical_sha256(payload)
	if not isinstance(declared_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
		findings.append(Finding(
			"G2D004", f"{label}.canonical_sha256",
			"canonical ceiling hash must be 64 lowercase hexadecimal characters"))
	elif declared_hash != computed_hash:
		findings.append(Finding(
			"G2D004", f"{label}.canonical_sha256",
			f"ceiling hash mismatch: declared {declared_hash}, computed {computed_hash}"))

	models, errors = _validate_path_list(raw.get("model_files"), f"{label}.model_files")
	findings.extend(errors)
	model_fingerprints, errors = _validate_fingerprint_map(
		raw.get("model_file_fingerprints"), f"{label}.model_file_fingerprints")
	findings.extend(errors)
	model_coverage, errors = _validate_path_list(
		raw.get("model_scan_coverage_files"),
		f"{label}.model_scan_coverage_files")
	findings.extend(errors)
	active_models, errors = _validate_path_list(
		raw.get("active_export_model_files"), f"{label}.active_export_model_files")
	findings.extend(errors)
	sidecars, errors = _validate_path_list(
		raw.get("model_import_sidecars"), f"{label}.model_import_sidecars")
	findings.extend(errors)
	active_untracked_sidecars, errors = _validate_path_list(
		raw.get("active_untracked_model_import_sidecars"),
		f"{label}.active_untracked_model_import_sidecars")
	findings.extend(errors)
	sidecar_fingerprints, errors = _validate_fingerprint_map(
		raw.get("model_import_sidecar_fingerprints"),
		f"{label}.model_import_sidecar_fingerprints")
	findings.extend(errors)
	model_archives, errors = _validate_model_archive_map(
		raw.get("model_archive_files"), f"{label}.model_archive_files")
	findings.extend(errors)
	archive, errors = _validate_path_list(
		raw.get("archive_now_model_files"), f"{label}.archive_now_model_files")
	findings.extend(errors)
	production, errors = _validate_token_map(
		raw.get("production_3d_files"), f"{label}.production_3d_files")
	findings.extend(errors)
	probes, errors = _validate_token_map(
		raw.get("probe_3d_files"), f"{label}.probe_3d_files")
	findings.extend(errors)
	scenes, errors = _validate_token_map(
		raw.get("scene_3d_files"), f"{label}.scene_3d_files")
	findings.extend(errors)
	configuration, errors = _validate_token_map(
		raw.get("configuration_3d_files"), f"{label}.configuration_3d_files")
	findings.extend(errors)

	if not set(active_models).issubset(models):
		for relative in sorted(set(active_models) - set(models)):
			findings.append(Finding(
				"G2D004", relative,
				"initial active/export model ceiling is absent from repository model ceiling"))
	if not set(model_coverage).issubset(models):
		for relative in sorted(set(model_coverage) - set(models)):
			findings.append(Finding(
				"G2D004", relative,
				"initial model scan-coverage ceiling is absent from model debt"))
	if not set(archive).issubset(active_models):
		for relative in sorted(set(archive) - set(active_models)):
			findings.append(Finding(
				"G2D004", relative,
				"initial archive-now ceiling is absent from active/export model ceiling"))
	if set(model_fingerprints) != set(models):
		findings.append(Finding(
			"G2D004", f"{label}.model_file_fingerprints",
			"initial model fingerprints must exactly cover initial model files"))
	if set(sidecar_fingerprints) != set(sidecars):
		findings.append(Finding(
			"G2D004", f"{label}.model_import_sidecar_fingerprints",
			"initial sidecar fingerprints must exactly cover initial sidecars"))

	expected_counts = {
		"model_files": len(models),
		"model_scan_coverage_files": len(model_coverage),
		"active_export_model_files": len(active_models),
		"model_import_sidecars": len(sidecars),
		"active_untracked_model_import_sidecars": len(active_untracked_sidecars),
		"model_archive_files": len(model_archives),
		"production_3d_files": len(production),
		"probe_3d_files": len(probes),
		"scene_3d_files": len(scenes),
		"configuration_3d_files": len(configuration),
		"archive_now_model_files": len(archive),
	}
	if raw.get("declared_counts") != expected_counts:
		findings.append(Finding(
			"G2D004", f"{label}.declared_counts",
			"initial ceiling counts do not match its canonical inventories"))
	return InitialCeiling(
		model_files=models,
		model_file_fingerprints=model_fingerprints,
		model_scan_coverage_files=model_coverage,
		active_export_model_files=active_models,
		model_import_sidecars=sidecars,
		active_untracked_model_import_sidecars=active_untracked_sidecars,
		model_import_sidecar_fingerprints=sidecar_fingerprints,
		model_archive_files=model_archives,
		production_3d_files=production,
		probe_3d_files=probes,
		scene_3d_files=scenes,
		configuration_3d_files=configuration,
		archive_now_model_files=archive,
		canonical_sha256=declared_hash if isinstance(declared_hash, str) else "",
	), findings


def _parse_manifest_document(raw: object, label: str) -> tuple[Manifest | None, list[Finding]]:
	if not isinstance(raw, dict):
		return None, [Finding("G2D001", label, "manifest root must be an object")]
	findings: list[Finding] = []
	if raw.get("schema_version") != SCHEMA_VERSION:
		findings.append(Finding(
			"G2D001", label,
			f"schema_version must be {SCHEMA_VERSION}"))
	initial_ceiling, ceiling_findings = _parse_initial_ceiling(raw.get("initial_ceiling"))
	findings.extend(ceiling_findings)

	models, model_findings = _validate_path_list(raw.get("model_files"), "model_files")
	model_fingerprints, model_fingerprint_findings = _validate_fingerprint_map(
		raw.get("model_file_fingerprints"), "model_file_fingerprints")
	model_coverage, model_coverage_findings = _validate_path_list(
		raw.get("model_scan_coverage_files"), "model_scan_coverage_files")
	active_models, active_model_findings = _validate_path_list(
		raw.get("active_export_model_files"), "active_export_model_files")
	sidecars, sidecar_findings = _validate_path_list(
		raw.get("model_import_sidecars"), "model_import_sidecars")
	active_untracked_sidecars, active_untracked_sidecar_findings = _validate_path_list(
		raw.get("active_untracked_model_import_sidecars"),
		"active_untracked_model_import_sidecars")
	sidecar_fingerprints, sidecar_fingerprint_findings = _validate_fingerprint_map(
		raw.get("model_import_sidecar_fingerprints"),
		"model_import_sidecar_fingerprints")
	model_archives, model_archive_findings = _validate_model_archive_map(
		raw.get("model_archive_files"), "model_archive_files")
	archive, archive_findings = _validate_path_list(
		raw.get("archive_now_model_files"), "archive_now_model_files")
	production, production_findings = _validate_token_map(
		raw.get("production_3d_files"), "production_3d_files")
	probes, probe_findings = _validate_token_map(
		raw.get("probe_3d_files"), "probe_3d_files")
	scenes, scene_findings = _validate_token_map(raw.get("scene_3d_files"), "scene_3d_files")
	configuration, config_findings = _validate_token_map(
		raw.get("configuration_3d_files"), "configuration_3d_files")
	findings.extend(model_findings + model_fingerprint_findings + model_coverage_findings +
		active_model_findings + sidecar_findings + active_untracked_sidecar_findings +
		sidecar_fingerprint_findings +
		model_archive_findings +
		archive_findings + production_findings + probe_findings +
		scene_findings + config_findings)

	if not set(active_models).issubset(models):
		for relative in sorted(set(active_models) - set(models)):
			findings.append(Finding(
				"G2D002", relative,
				"active/export model is missing from repository-wide model debt"))
	if not set(model_coverage).issubset(models):
		for relative in sorted(set(model_coverage) - set(models)):
			findings.append(Finding(
				"G2D002", relative,
				"model scan-coverage debt is missing from repository-wide model debt"))
	if not set(archive).issubset(active_models):
		for relative in sorted(set(archive) - set(active_models)):
			findings.append(Finding(
				"G2D002", relative,
				"archive-now model is not present in active/export model debt"))
	if set(model_fingerprints) != set(models):
		findings.append(Finding(
			"G2D002", "model_file_fingerprints",
			"model fingerprints must exactly cover model_files"))
	if set(sidecar_fingerprints) != set(sidecars):
		findings.append(Finding(
			"G2D002", "model_import_sidecar_fingerprints",
			"sidecar fingerprints must exactly cover model_import_sidecars"))

	declared = raw.get("declared_counts")
	expected_counts = {
		"model_files": len(models),
		"model_scan_coverage_files": len(model_coverage),
		"active_export_model_files": len(active_models),
		"model_import_sidecars": len(sidecars),
		"active_untracked_model_import_sidecars": len(active_untracked_sidecars),
		"model_archive_files": len(model_archives),
		"production_3d_files": len(production),
		"probe_3d_files": len(probes),
		"scene_3d_files": len(scenes),
		"configuration_3d_files": len(configuration),
		"archive_now_model_files": len(archive),
	}
	if declared != expected_counts:
		findings.append(Finding(
			"G2D003", "declared_counts",
			f"declared counts {declared!r} do not match inventory {expected_counts!r}"))

	manifest = Manifest(
		model_files=models,
		model_file_fingerprints=model_fingerprints,
		model_scan_coverage_files=model_coverage,
		active_export_model_files=active_models,
		model_import_sidecars=sidecars,
		active_untracked_model_import_sidecars=active_untracked_sidecars,
		model_import_sidecar_fingerprints=sidecar_fingerprints,
		model_archive_files=model_archives,
		production_3d_files=production,
		probe_3d_files=probes,
		scene_3d_files=scenes,
		configuration_3d_files=configuration,
		archive_now_model_files=archive,
		declared_counts=expected_counts,
		initial_ceiling=initial_ceiling,
		metadata=raw.get("metadata", {}) if isinstance(raw.get("metadata", {}), dict) else {},
	)
	return manifest, findings


def load_manifest(path: Path) -> tuple[Manifest | None, list[Finding]]:
	if not path.is_file():
		return None, [Finding("G2D001", path.as_posix(), "migration manifest is missing")]
	try:
		raw = _json_loads_unique(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError, DuplicateJSONKeyError) as error:
		return None, [Finding("G2D001", path.as_posix(), f"cannot read manifest: {error}")]
	if not isinstance(raw, dict):
		return None, [Finding("G2D001", path.as_posix(), "manifest root must be an object")]
	return _parse_manifest_document(raw, path.as_posix())


def _git_manifest_history(root: Path, manifest_path: Path) -> tuple[list[Manifest], list[Finding]]:
	"""Load every reachable checked-in baseline to prove monotonic shrinkage.

	Comparing only with ``HEAD^`` lets an expansion become green after one
	unrelated commit.  Requiring the current inventory to be a subset of every
	reachable snapshot makes the first baseline immutable and also prevents a
	previously removed entry from being reintroduced later.
	"""
	try:
		relative = manifest_path.resolve().relative_to(root).as_posix()
	except ValueError:
		return [], []
	try:
		top = subprocess.run(
			["git", "-C", str(root), "rev-parse", "--show-toplevel"],
			check=False, capture_output=True,
		)
		if top.returncode != 0 or Path(
				top.stdout.decode("utf-8", errors="replace").strip()).resolve() != root:
			return [], []
		logged = subprocess.run(
			["git", "-C", str(root), "log", "--reverse", "--format=%H",
				"HEAD", "--", relative],
			check=False, capture_output=True,
		)
	except OSError:
		return [], []
	if logged.returncode != 0:
		return [], []
	manifests: list[Manifest] = []
	findings: list[Finding] = []
	for commit in logged.stdout.decode("ascii", errors="ignore").splitlines():
		shown = subprocess.run(
			["git", "-C", str(root), "show", f"{commit}:{relative}"],
			check=False, capture_output=True,
		)
		# A commit which deleted the manifest has no blob; earlier snapshots still
		# remain authoritative if the contract is later restored.
		if shown.returncode != 0:
			continue
		label = f"{commit}:{relative}"
		try:
			raw = _json_loads_unique(shown.stdout.decode("utf-8"))
		except (UnicodeDecodeError, json.JSONDecodeError, DuplicateJSONKeyError) as error:
			findings.append(Finding(
				"G2D401", label,
				f"cannot validate historical shrinking manifest: {error}"))
			continue
		if not isinstance(raw, dict):
			findings.append(Finding(
				"G2D401", label,
				"cannot validate historical shrinking manifest: root is not an object"))
			continue
		manifest, parse_findings = _parse_manifest_document(raw, label)
		for finding in parse_findings:
			findings.append(Finding(
				"G2D401", label,
				f"invalid historical manifest ({finding.path}): {finding.detail}"))
		if manifest is not None and not parse_findings:
			manifests.append(manifest)
	return manifests, findings


def _compare_manifest_history(current: Manifest, previous: Manifest | InitialCeiling,
		findings: list[Finding]) -> None:
	"""Reject any debt entry/count not contained by the preceding baseline."""
	for category, current_paths, previous_paths in (
		("tracked repository model", current.model_files, previous.model_files),
		("model signature scan-coverage", current.model_scan_coverage_files,
			previous.model_scan_coverage_files),
		("active/export model", current.active_export_model_files,
			previous.active_export_model_files),
		("tracked model import sidecar", current.model_import_sidecars,
			previous.model_import_sidecars),
		("active untracked model import sidecar",
			current.active_untracked_model_import_sidecars,
			previous.active_untracked_model_import_sidecars),
		("tracked model archive", current.model_archive_files,
			previous.model_archive_files),
		("archive-now model", current.archive_now_model_files,
			previous.archive_now_model_files),
	):
		for relative in sorted(set(current_paths) - set(previous_paths)):
			findings.append(Finding(
				"G2D401", relative,
				f"{category} debt was added to the shrinking manifest"))
	for category, current_map, previous_map in (
		("production 3D API", current.production_3d_files,
			previous.production_3d_files),
		("probe 3D API", current.probe_3d_files,
			previous.probe_3d_files),
		("scene 3D API", current.scene_3d_files, previous.scene_3d_files),
		("configuration 3D", current.configuration_3d_files,
			previous.configuration_3d_files),
	):
		for relative in sorted(set(current_map) - set(previous_map)):
			findings.append(Finding(
				"G2D401", relative,
				f"{category} file was added to the shrinking manifest"))
		for relative in sorted(set(current_map) & set(previous_map)):
			for token, count in current_map[relative].items():
				previous_count = previous_map[relative].get(token, 0)
				if count > previous_count:
					findings.append(Finding(
						"G2D401", relative,
						f"{category} debt for {token} grew in manifest: "
						f"{previous_count} -> {count}"))
	for category, current_map, previous_map in (
		("model binary", current.model_file_fingerprints,
			previous.model_file_fingerprints),
		("model import sidecar", current.model_import_sidecar_fingerprints,
			previous.model_import_sidecar_fingerprints),
		("model-bearing archive", current.model_archive_files,
			previous.model_archive_files),
	):
		for relative in sorted(set(current_map) & set(previous_map)):
			if current_map[relative] != previous_map[relative]:
				findings.append(Finding(
					"G2D402", relative,
					f"retained {category} fingerprint differs from immutable baseline"))


def _compare_path_inventory(current: Iterable[str], baseline: Iterable[str],
		category: str, findings: list[Finding]) -> None:
	current_set = set(current)
	baseline_set = set(baseline)
	for relative in sorted(current_set - baseline_set):
		findings.append(Finding(
			"G2D101", relative,
			f"current {category} debt is missing from the shrinking manifest"))
	for relative in sorted(baseline_set - current_set):
		findings.append(Finding(
			"G2D201", relative,
			f"stale {category} manifest entry; remove it in the same debt-reduction change"))


def _compare_token_inventory(current: Mapping[str, Mapping[str, int]],
		baseline: Mapping[str, Mapping[str, int]], category: str,
		findings: list[Finding]) -> None:
	_compare_path_inventory(current, baseline, category, findings)
	for relative in sorted(set(current) & set(baseline)):
		current_counts = dict(current[relative])
		baseline_counts = dict(baseline[relative])
		if current_counts == baseline_counts:
			continue
		all_tokens = sorted(set(current_counts) | set(baseline_counts))
		for token in all_tokens:
			current_count = current_counts.get(token, 0)
			baseline_count = baseline_counts.get(token, 0)
			if current_count > baseline_count:
				findings.append(Finding(
					"G2D102", relative,
					f"{category} debt expanded for {token}: {baseline_count} -> {current_count}"))
			elif current_count < baseline_count:
				findings.append(Finding(
					"G2D202", relative,
					f"stale {category} token baseline for {token}: "
					f"manifest {baseline_count}, current {current_count}; shrink the manifest"))


def _compare_fingerprint_inventory(
		current: Mapping[str, Mapping[str, int | str]],
		baseline: Mapping[str, Mapping[str, int | str]],
		category: str, findings: list[Finding]) -> None:
	_compare_path_inventory(current, baseline, f"{category} fingerprint", findings)
	for relative in sorted(set(current) & set(baseline)):
		if dict(current[relative]) != dict(baseline[relative]):
			findings.append(Finding(
				"G2D103", relative,
				f"retained {category} bytes changed at the same path"))


def _resolved_resource_strings(text: str, assignments: Mapping[str, str] | None = None,
		masked: str | None = None) -> set[str]:
	"""Fold simple constant string concatenations used by load/exists calls."""
	return set(_resolved_call_strings(
		text, r"(?:\bload|\bpreload|ResourceLoader\.(?:load|exists))",
		assignments, masked))


def _normalise_resource_directory(value: str) -> str:
	normalised = value.replace("\\", "/").strip()
	if normalised.startswith("res://"):
		normalised = normalised[6:]
	return normalised.strip("/")


def _is_runtime_data_path(path: Path, root: Path) -> bool:
	relative = _relative(path, root)
	if any(relative == prefix or relative.startswith(prefix + "/")
			for prefix in NON_RUNTIME_DATA_PREFIXES):
		return False
	parts = relative.split("/")
	if any(part.lower() in {"provenance", "_provenance"} for part in parts[:-1]):
		return False
	if len(parts) == 1:
		return path.name not in NON_RUNTIME_ROOT_DATA_FILES
	# _active_files already enforces Godot-active roots and .gdignore.  Do not
	# maintain a second allowlist here: custom live catalogs are equally capable
	# of carrying 3D API names and model dependencies.
	return True


def _directory_iterator_paths(text: str, assignments: Mapping[str, str] | None = None,
		masked: str | None = None) -> set[str]:
	paths = _resolved_call_strings(
		text,
		r"(?:DirAccess\.(?:get_directories_at|get_files_at|open)|"
		r"ResourceLoader\.list_directory)", assignments, masked,
	)
	return {_normalise_resource_directory(path) for path in paths if path}


def _dynamic_model_load_patterns(text: str,
		assignments: Mapping[str, str] | None = None,
		masked: str | None = None) -> set[tuple[str, str]]:
	if assignments is None:
		assignments = _simple_string_assignments(text)
	patterns: set[tuple[str, str]] = set()
	for expression in _call_argument_expressions(
			text, r"(?:\bload|\bpreload|ResourceLoader\.(?:load|exists))", masked):
		if _simple_string_value(expression, assignments) is not None:
			continue
		known_values: set[str] = {
			match.group(2)
			for match in re.finditer(r"(?:&|\^)?([\"'])(.*?)\1", expression)
		}
		known_values.update(
			assignments[name]
			for name in re.findall(r"\b[A-Za-z_]\w*\b", expression)
			if name in assignments)
		directories: set[str] = set()
		for value in known_values:
			normalised = _normalise_resource_directory(value)
			model_match = re.search(
				r"(?i)\." + MODEL_EXTENSION_PATTERN + r"\b", normalised)
			if model_match is not None:
				prefix = normalised[:model_match.start()]
				if "/" in prefix:
					directories.add(prefix.rsplit("/", 1)[0])
			elif value.startswith("res://") or "/" in value:
				directories.add(normalised)
		extensions = {
			match.group(0).lower()
			for value in known_values
			for match in re.finditer(r"(?i)\." + MODEL_EXTENSION_PATTERN + r"\b", value)
		}
		for directory in directories:
			for extension in extensions:
				patterns.add((directory, extension))
	return patterns


def _path_or_stem_reference(text: str, relative: str) -> bool:
	"""Match an exact resource path/stem, never a longer sibling basename."""
	def token_character(character: str) -> bool:
		return character.isalnum() or character in "_.-"

	stem = relative.rsplit(".", 1)[0]
	for candidate in ("res://" + relative, relative, "res://" + stem, stem):
		start = 0
		while (index := text.find(candidate, start)) >= 0:
			end = index + len(candidate)
			before_ok = index == 0 or not token_character(text[index - 1])
			after_ok = end == len(text) or not token_character(text[end])
			if before_ok and after_ok:
				return True
			start = index + 1
	return False


def _active_archive_dependency_texts(path: Path,
		kind: str | None = None) -> tuple[list[tuple[str, str]], bool]:
	"""Read bounded JSON/data members used by archive-safety proof."""
	if kind is None:
		kind = _archive_kind(path)
	if kind is None:
		return [], False
	if kind == "opaque":
		return [], True
	texts: list[tuple[str, str]] = []
	remaining = ARCHIVE_SNIFF_BUDGET
	opaque = False
	try:
		if kind == "zip":
			with zipfile.ZipFile(path) as packed:
				infos = packed.infolist()
				if len(infos) > ARCHIVE_MEMBER_LIMIT:
					return [], True
				for info in infos:
					if info.is_dir():
						continue
					member_path = Path(info.filename)
					if _archive_suffix_kind(member_path) is not None:
						opaque = True
						continue
					is_opaque_binary = (
						member_path.suffix.lower() in OPAQUE_DEPENDENCY_MEMBER_EXTENSIONS)
					if is_opaque_binary:
						opaque = True
					is_dependency_text = (
						member_path.suffix.lower() in DEPENDENCY_TEXT_EXTENSIONS)
					if is_dependency_text:
						read_size = info.file_size
					elif is_opaque_binary:
						read_size = min(info.file_size, NATIVE_SYMBOL_SCAN_BYTES)
					else:
						read_size = min(info.file_size, ARCHIVE_MAGIC_BYTES)
					if read_size > remaining:
						return texts, True
					with packed.open(info) as stream:
						data = stream.read(
							read_size + (1 if is_dependency_text or is_opaque_binary else 0))
					if (is_dependency_text or is_opaque_binary) and len(data) > read_size:
						opaque = True
						data = data[:read_size]
					if is_dependency_text and len(data) > read_size:
						return texts, True
					remaining -= len(data)
					if _archive_sample_kind(data) is not None:
						opaque = True
						continue
					if not (is_dependency_text or is_opaque_binary):
						continue
					texts.append((
						f"{path.name}!{info.filename.replace(chr(92), '/')}",
						data.decode("utf-8", errors="replace"),
					))
		else:
			with tarfile.open(path, mode="r:*") as packed:
				for index, member in enumerate(packed):
					if index >= ARCHIVE_MEMBER_LIMIT:
						return texts, True
					if not member.isfile():
						continue
					member_path = Path(member.name)
					if _archive_suffix_kind(member_path) is not None:
						opaque = True
						continue
					is_opaque_binary = (
						member_path.suffix.lower() in OPAQUE_DEPENDENCY_MEMBER_EXTENSIONS)
					if is_opaque_binary:
						opaque = True
					is_dependency_text = (
						member_path.suffix.lower() in DEPENDENCY_TEXT_EXTENSIONS)
					if is_dependency_text:
						read_size = member.size
					elif is_opaque_binary:
						read_size = min(member.size, NATIVE_SYMBOL_SCAN_BYTES)
					else:
						read_size = min(member.size, ARCHIVE_MAGIC_BYTES)
					if read_size > remaining:
						return texts, True
					stream = packed.extractfile(member)
					if stream is None:
						data = b""
					else:
						with stream:
							data = stream.read(read_size + (
								1 if is_dependency_text or is_opaque_binary else 0))
					if (is_dependency_text or is_opaque_binary) and len(data) > read_size:
						opaque = True
						data = data[:read_size]
					if is_dependency_text and len(data) > read_size:
						return texts, True
					remaining -= len(data)
					if _archive_sample_kind(data) is not None:
						opaque = True
						continue
					if not (is_dependency_text or is_opaque_binary):
						continue
					texts.append((
						f"{path.name}!{member.name.replace(chr(92), '/')}",
						data.decode("utf-8", errors="replace"),
					))
	except (OSError, RuntimeError, tarfile.TarError, zipfile.BadZipFile, EOFError):
		return texts, True
	return texts, opaque


def _active_dependency_texts(root: Path,
		archive_kind_cache: Mapping[str, str | None] | None = None,
		text_cache: dict[Path, str] | None = None,
		active_files: Iterable[Path] | None = None) -> tuple[
		list[tuple[str, str]], list[str]]:
	active = tuple(_active_files(root) if active_files is None else active_files)
	runtime_scope = _runtime_dependency_scope(root, active, text_cache)
	paths = {
		path for path in active
		if (path.suffix.lower() in PRODUCTION_SOURCE_EXTENSIONS
			or path.suffix.lower() in {".tscn", ".tres", ".cfg", ".gdextension"})
	}
	project = root / "project.godot"
	if project.is_file():
		paths.add(project)
	paths.update(_runtime_data_files(root, runtime_scope, active))
	texts: list[tuple[str, str]] = []
	opaque_sources: list[str] = []
	for path in sorted(paths):
		try:
			text = _read_text_cached(path, text_cache)
		except OSError:
			opaque_sources.append(_relative(path, root))
			continue
		texts.append((_relative(path, root), text))
	# Native libraries and packed runtime containers can hold resource strings
	# outside source files.  Inspect a bounded prefix for exact evidence and keep
	# them opaque/fail-closed because absence from that prefix is not proof.
	binary_paths = {
		path for path in active
		if (path.suffix.lower() in NATIVE_BINARY_EXTENSIONS
			or re.search(r"(?i)\.so(?:\.\d+)+$", path.name) is not None
			or path.suffix.lower() in OPAQUE_RUNTIME_BINARY_EXTENSIONS)
	}
	for path in sorted(binary_paths):
		relative = _relative(path, root)
		try:
			with path.open("rb") as stream:
				data = stream.read(NATIVE_SYMBOL_SCAN_BYTES + 1)
		except OSError:
			opaque_sources.append(relative)
			continue
		texts.append((relative, data[:NATIVE_SYMBOL_SCAN_BYTES].decode(
			"latin-1", errors="ignore")))
		opaque_sources.append(relative)
	for path in active:
		relative = _relative(path, root)
		if archive_kind_cache is not None and relative in archive_kind_cache:
			kind = archive_kind_cache[relative]
		else:
			kind = _archive_kind(path)
		if kind is None or not _is_runtime_dependency_path(
				path, root, runtime_scope):
			continue
		archive_texts, opaque = _active_archive_dependency_texts(path, kind)
		for member, text in archive_texts:
			source = f"{_relative(path, root)}!{member.split('!', 1)[-1]}"
			texts.append((source, text))
		if opaque:
			opaque_sources.append(_relative(path, root))
	return texts, sorted(set(opaque_sources))


def _archive_reference_findings(root: Path, archive: Iterable[str],
		archive_kind_cache: Mapping[str, str | None] | None = None,
		text_cache: dict[Path, str] | None = None,
		active_files: Iterable[Path] | None = None) -> list[Finding]:
	texts, opaque_dependency_sources = _active_dependency_texts(
		root, archive_kind_cache, text_cache, active_files)
	prepared_texts: list[
		tuple[str, str, set[str], set[str], set[tuple[str, str]]]] = []
	for source, source_text in texts:
		needs_resolution = any(marker in source_text for marker in (
			"load", "preload", "ResourceLoader", "DirAccess", "path_join"))
		masked = _mask_strings_and_comments(source_text) if needs_resolution else ""
		assignments = (
			_simple_string_assignments(source_text) if needs_resolution else {})
		prepared_texts.append((
			source,
			source_text,
			(_resolved_resource_strings(source_text, assignments, masked)
				if needs_resolution else set()),
			(_directory_iterator_paths(source_text, assignments, masked)
				if needs_resolution else set()),
			(_dynamic_model_load_patterns(source_text, assignments, masked)
				if needs_resolution else set()),
		))
	string_literals = {
		match.group(2)
		for _source, text in texts
		for match in re.finditer(r"([\"'])(.*?)\1", text)
	}
	binary_sources = [_relative(path, root) for path in _binary_scene_resource_files(root)]
	findings: list[Finding] = []
	for relative in archive:
		stem = relative.rsplit(".", 1)[0]
		directory = stem.rsplit("/", 1)[0] if "/" in stem else ""
		filename = relative.rsplit("/", 1)[-1]
		for source, text, resolved, iterator_paths, dynamic_patterns in prepared_texts:
			direct = _path_or_stem_reference(text, relative)
			split_path = "res://" + relative in resolved or relative in resolved
			if direct or split_path:
				findings.append(Finding(
					"G2D301", relative,
					f"archive-now model path or stem has a production reference in {source}"))
			iterator_match = any(
				directory == iterator or directory.startswith(iterator + "/")
				for iterator in iterator_paths if iterator)
			if iterator_match:
				findings.append(Finding(
					"G2D301", relative,
					f"archive-now model directory is enumerated dynamically in {source}"))
			extension = "." + relative.rsplit(".", 1)[-1].lower()
			dynamic_match = any(
				(extension == dynamic_extension and (
					directory == dynamic_directory
					or directory.startswith(dynamic_directory + "/")))
				for dynamic_directory, dynamic_extension in dynamic_patterns
				if dynamic_directory)
			if dynamic_match:
				findings.append(Finding(
					"G2D301", relative,
					f"archive-now model matches a dynamic directory/name loader in {source}"))
		cross_file_split = bool(
			directory and filename in string_literals and (
				"res://" + directory + "/" in string_literals
				or directory + "/" in string_literals))
		if cross_file_split:
			findings.append(Finding(
				"G2D301", relative,
				f"archive-now model directory and filename are split across production sources"))
		for source in binary_sources:
			findings.append(Finding(
				"G2D302", relative,
				f"cannot prove archive safety while opaque binary resource {source} exists"))
		for source in opaque_dependency_sources:
			findings.append(Finding(
				"G2D302", relative,
				f"cannot prove archive safety while dependency data {source} is opaque"))
	return findings


def audit(root: Path, manifest_path: Path | None = None,
		initial_ceiling_anchor: str | None = None) -> AuditResult:
	root = root.resolve()
	if manifest_path is None:
		manifest_path = root / DEFAULT_MANIFEST
	elif not manifest_path.is_absolute():
		manifest_path = root / manifest_path
	archive_kind_cache: dict[str, str | None] = {}
	text_cache: dict[Path, str] = {}
	active_files_cache: list[Path] = []
	inventory = discover(
		root, archive_kind_cache, text_cache, active_files_cache)
	manifest, findings = load_manifest(manifest_path)
	if manifest is not None:
		if _git_path_is_tracked(root, manifest_path) and _git_repository_is_shallow(root):
			findings.append(Finding(
				"G2D403", manifest_path.as_posix(),
				"full Git history is required for shrinking-baseline validation; "
				"shallow repository refused"))
		if initial_ceiling_anchor is not None and (
				manifest.initial_ceiling is None or
				manifest.initial_ceiling.canonical_sha256 != initial_ceiling_anchor):
			actual = (manifest.initial_ceiling.canonical_sha256
				if manifest.initial_ceiling is not None else "<missing>")
			findings.append(Finding(
				"G2D005", "initial_ceiling.canonical_sha256",
				f"immutable trust anchor is {initial_ceiling_anchor}, manifest has {actual}"))
		if manifest.initial_ceiling is not None:
			_compare_manifest_history(manifest, manifest.initial_ceiling, findings)
		historical_manifests, history_findings = _git_manifest_history(root, manifest_path)
		findings.extend(history_findings)
		if not history_findings:
			for previous_manifest in historical_manifests:
				_compare_manifest_history(manifest, previous_manifest, findings)
		_compare_path_inventory(
			inventory.model_files, manifest.model_files,
			"tracked repository model file", findings)
		_compare_fingerprint_inventory(
			inventory.model_file_fingerprints, manifest.model_file_fingerprints,
			"model binary", findings)
		_compare_path_inventory(
			inventory.model_scan_coverage_files, manifest.model_scan_coverage_files,
			"model signature scan-coverage", findings)
		_compare_path_inventory(
			inventory.active_export_model_files, manifest.active_export_model_files,
			"active/export model file", findings)
		_compare_path_inventory(
			inventory.model_import_sidecars, manifest.model_import_sidecars,
			"tracked model import sidecar", findings)
		_compare_path_inventory(
			inventory.active_untracked_model_import_sidecars,
			manifest.active_untracked_model_import_sidecars,
			"active untracked model import sidecar", findings)
		_compare_fingerprint_inventory(
			inventory.model_import_sidecar_fingerprints,
			manifest.model_import_sidecar_fingerprints,
			"model import sidecar", findings)
		_compare_fingerprint_inventory(
			inventory.model_archive_files, manifest.model_archive_files,
			"model-bearing archive", findings)
		_compare_token_inventory(
			inventory.production_3d_files, manifest.production_3d_files,
			"production 3D API", findings)
		_compare_token_inventory(
			inventory.probe_3d_files, manifest.probe_3d_files,
			"probe 3D API", findings)
		_compare_token_inventory(
			inventory.scene_3d_files, manifest.scene_3d_files,
			"scene 3D API", findings)
		_compare_token_inventory(
			inventory.configuration_3d_files, manifest.configuration_3d_files,
			"configuration 3D", findings)
		findings.extend(_archive_reference_findings(
			root, manifest.archive_now_model_files, archive_kind_cache, text_cache,
			active_files_cache))
	return AuditResult(
		inventory=inventory,
		manifest=manifest,
		findings=sorted(findings, key=lambda item: (item.check_id, item.path, item.detail)),
	)


def _json_object_member_span(text: str, key: str) -> tuple[int, int]:
	"""Locate an object-valued member of the top-level JSON object only."""
	def string_end(start: int) -> int:
		escaped = False
		for index in range(start + 1, len(text)):
			character = text[index]
			if escaped:
				escaped = False
			elif character == "\\":
				escaped = True
			elif character == '"':
				return index + 1
		raise ValueError("JSON string is unterminated")

	def object_end(start: int) -> int:
		depth = 0
		index = start
		while index < len(text):
			character = text[index]
			if character == '"':
				index = string_end(index)
				continue
			if character == "{":
				depth += 1
			elif character == "}":
				depth -= 1
				if depth == 0:
					return index + 1
			index += 1
		raise ValueError(f"JSON object member {key!r} is unterminated")

	index = 0
	while index < len(text) and text[index].isspace():
		index += 1
	if index >= len(text) or text[index] != "{":
		raise ValueError("manifest root is not a JSON object")
	depth = 1
	index += 1
	while index < len(text) and depth:
		character = text[index]
		if character == '"':
			end = string_end(index)
			if depth == 1:
				try:
					member_name = json.loads(text[index:end])
				except json.JSONDecodeError:
					member_name = None
				cursor = end
				while cursor < len(text) and text[cursor].isspace():
					cursor += 1
				if cursor < len(text) and text[cursor] == ":":
					cursor += 1
					while cursor < len(text) and text[cursor].isspace():
						cursor += 1
					if member_name == key:
						if cursor >= len(text) or text[cursor] != "{":
							raise ValueError(
								f"JSON object member {key!r} is not an object")
						return cursor, object_end(cursor)
			index = end
			continue
		if character in "[{":
			depth += 1
		elif character in "]}":
			depth -= 1
		index += 1
	raise ValueError(f"JSON object member {key!r} is missing or not an object")


def _git_short_head(root: Path) -> str:
	try:
		completed = subprocess.run(
			["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
			check=False, capture_output=True, text=True,
		)
	except OSError:
		return "unversioned"
	return completed.stdout.strip() if completed.returncode == 0 else "unversioned"


def _git_path_is_tracked(root: Path, path: Path) -> bool:
	try:
		relative = path.resolve().relative_to(root).as_posix()
		completed = subprocess.run(
			["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
			check=False, capture_output=True,
		)
	except (OSError, ValueError):
		return False
	return completed.returncode == 0


def _git_repository_is_shallow(root: Path) -> bool:
	try:
		completed = subprocess.run(
			["git", "-C", str(root), "rev-parse", "--is-shallow-repository"],
			check=False, capture_output=True, text=True,
		)
	except OSError:
		return False
	return completed.returncode == 0 and completed.stdout.strip().lower() == "true"


def refresh_manifest(root: Path, manifest_path: Path | None = None,
		initial_ceiling_anchor: str | None = None) -> tuple[bool, list[Finding]]:
	"""Atomically refresh a manifest after debt removal, never after growth."""
	root = root.resolve()
	if manifest_path is None:
		manifest_path = root / DEFAULT_MANIFEST
	elif not manifest_path.is_absolute():
		manifest_path = root / manifest_path
	try:
		original_text = manifest_path.read_text(encoding="utf-8")
	except OSError as error:
		return False, [Finding("G2D501", manifest_path.as_posix(), str(error))]
	current, findings = load_manifest(manifest_path)
	if current is None or findings:
		return False, sorted(findings or [Finding(
			"G2D501", manifest_path.as_posix(), "current manifest is invalid")],
			key=lambda item: (item.check_id, item.path, item.detail))
	if current.initial_ceiling is None:
		return False, [Finding("G2D501", "initial_ceiling", "initial ceiling is missing")]
	if initial_ceiling_anchor is not None and (
			current.initial_ceiling.canonical_sha256 != initial_ceiling_anchor):
		return False, [Finding(
			"G2D501", "initial_ceiling.canonical_sha256",
			"manifest does not match the pinned immutable trust anchor")]
	if _git_path_is_tracked(root, manifest_path) and _git_repository_is_shallow(root):
		return False, [Finding(
			"G2D501", manifest_path.as_posix(),
			"shrink-only refresh requires full Git history; shallow repository refused")]
	historical_manifests, history_findings = _git_manifest_history(root, manifest_path)
	if history_findings:
		return False, sorted(
			history_findings, key=lambda item: (item.check_id, item.path, item.detail))
	try:
		ceiling_start, ceiling_end = _json_object_member_span(
			original_text, "initial_ceiling")
	except ValueError as error:
		return False, [Finding("G2D501", "initial_ceiling", str(error))]
	original_ceiling_bytes = original_text[ceiling_start:ceiling_end]

	archive_kind_cache: dict[str, str | None] = {}
	text_cache: dict[Path, str] = {}
	active_files_cache: list[Path] = []
	inventory = discover(
		root, archive_kind_cache, text_cache, active_files_cache)
	archive_now = tuple(
		relative for relative in current.archive_now_model_files
		if relative in inventory.active_export_model_files
		and relative in inventory.model_files)
	metadata = dict(current.metadata)
	metadata.update({
		"inventory_head": _git_short_head(root),
		"inventory_date": date.today().isoformat(),
		"refresh_contract": "shrink-only; immutable initial ceiling preserved",
	})
	document = manifest_dict(
		inventory, archive_now, metadata,
		initial_ceiling=_json_loads_unique(original_ceiling_bytes),
	)
	proposed, parse_findings = _parse_manifest_document(document, "refreshed manifest")
	if proposed is None or parse_findings:
		return False, sorted(parse_findings or [Finding(
			"G2D501", "refreshed manifest", "generated manifest is invalid")],
			key=lambda item: (item.check_id, item.path, item.detail))
	growth_findings: list[Finding] = []
	_compare_manifest_history(proposed, current, growth_findings)
	_compare_manifest_history(proposed, current.initial_ceiling, growth_findings)
	for previous_manifest in historical_manifests:
		_compare_manifest_history(proposed, previous_manifest, growth_findings)
	growth_findings.extend(_archive_reference_findings(
		root, archive_now, archive_kind_cache, text_cache, active_files_cache))
	if growth_findings:
		return False, sorted(
			growth_findings, key=lambda item: (item.check_id, item.path, item.detail))

	new_text = json.dumps(document, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
	try:
		new_start, new_end = _json_object_member_span(new_text, "initial_ceiling")
	except ValueError as error:
		return False, [Finding("G2D501", "initial_ceiling", str(error))]
	new_text = new_text[:new_start] + original_ceiling_bytes + new_text[new_end:]
	try:
		validated_raw = _json_loads_unique(new_text)
	except (json.JSONDecodeError, DuplicateJSONKeyError) as error:
		return False, [Finding("G2D501", "refreshed manifest", str(error))]
	if not isinstance(validated_raw, dict):
		return False, [Finding(
			"G2D501", "refreshed manifest", "manifest root is not an object")]
	validated_manifest, validated_findings = _parse_manifest_document(
		validated_raw, "refreshed manifest after ceiling splice")
	if validated_manifest is None or validated_findings:
		return False, sorted(validated_findings or [Finding(
			"G2D501", "refreshed manifest", "post-splice manifest is invalid")],
			key=lambda item: (item.check_id, item.path, item.detail))
	if (initial_ceiling_anchor is not None and (
			validated_manifest.initial_ceiling is None or
			validated_manifest.initial_ceiling.canonical_sha256 != initial_ceiling_anchor)):
		return False, [Finding(
			"G2D501", "initial_ceiling.canonical_sha256",
			"post-splice manifest does not match the pinned immutable trust anchor")]
	if new_text[new_start:new_start + len(original_ceiling_bytes)] != original_ceiling_bytes:
		return False, [Finding(
			"G2D501", "initial_ceiling", "initial ceiling bytes were not preserved")]

	temporary_path: Path | None = None
	try:
		manifest_path.parent.mkdir(parents=True, exist_ok=True)
		with tempfile.NamedTemporaryFile(
				"w", encoding="utf-8", newline="\n", delete=False,
				dir=manifest_path.parent, prefix=manifest_path.name + ".",
				suffix=".tmp") as stream:
			temporary_path = Path(stream.name)
			stream.write(new_text)
			stream.flush()
			os.fsync(stream.fileno())
		os.replace(temporary_path, manifest_path)
	except OSError as error:
		if temporary_path is not None:
			try:
				temporary_path.unlink(missing_ok=True)
			except OSError:
				pass
		return False, [Finding("G2D501", manifest_path.as_posix(), str(error))]
	return True, []


def exit_code(result: AuditResult, mode: str = "default") -> int:
	if result.findings:
		return 1
	if mode == "strict":
		return 0 if result.satisfied else 1
	return 0


def render(result: AuditResult, mode: str = "default") -> str:
	lines: list[str] = []
	for finding in result.findings:
		lines.append(
			f"GAME2D| FAIL| {finding.check_id}| {finding.path}| {finding.detail}")
	counts = result.inventory.counts()
	archive_count = len(result.manifest.archive_now_model_files) if result.manifest else 0
	lines.append(
		"GAME2D| DEBT| " + "| ".join(
			f"{field}={counts[field]}" for field in CATEGORY_FIELDS) +
		f"| archive_now_model_files={archive_count}")
	lines.append(f"GAME2D| STATUS| {result.status}")
	if result.satisfied:
		lines.append("GAME2D| RESULT| SATISFIED - active game is fully 2D")
	elif result.findings:
		lines.append(
			f"GAME2D| RESULT| FAIL - manifest drift ({len(result.findings)} finding(s)); "
			"2D contract remains UNSATISFIED")
	elif mode == "regression-gate":
		lines.append(
			"GAME2D| RESULT| NO_REGRESSION - exact shrinking baseline; "
			"migration debt remains UNSATISFIED")
	elif mode == "strict":
		lines.append(
			"GAME2D| RESULT| STRICT FAIL - migration debt remains; "
			"known debt is not a waiver")
	else:
		lines.append(
			"GAME2D| RESULT| UNSATISFIED - inventory is exact, but tracked/active 3D/model "
			"debt remains")
	return "\n".join(lines)


def _write_manifest(path: Path, inventory: Inventory,
		archive_now: Iterable[str] = (),
		initial_ceiling: Mapping | None = None) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(
		json.dumps(
			manifest_dict(inventory, archive_now, initial_ceiling=initial_ceiling),
			indent=2, sort_keys=False,
		) + "\n",
		encoding="utf-8",
	)


def _stress_fixture(root: Path, *, with_debt: bool = True) -> Path:
	(root / "tools").mkdir(parents=True, exist_ok=True)
	(root / "scripts").mkdir(parents=True, exist_ok=True)
	(root / "scenes").mkdir(parents=True, exist_ok=True)
	if with_debt:
		(root / "assets/legacy").mkdir(parents=True, exist_ok=True)
		(root / "assets/legacy/prop.glb").write_bytes(b"model")
		(root / "assets/legacy/prop.glb.import").write_text("[remap]\n", encoding="utf-8")
		(root / "scripts/legacy.gd").write_text(
			"extends Node3D\nvar point := Vector3.ZERO\n", encoding="utf-8")
		(root / "scenes/main.tscn").write_text(
			'[gd_scene format=3]\n[node name="Main" type="Node3D"]\n', encoding="utf-8")
		(root / "project.godot").write_text(
			'[physics]\n3d/physics_engine="Jolt Physics"\n', encoding="utf-8")
	manifest_path = root / DEFAULT_MANIFEST
	_write_manifest(manifest_path, discover(root))
	return manifest_path


def stress() -> int:
	failures: list[str] = []
	assertion_count = 0

	def expect(name: str, predicate) -> None:
		nonlocal assertion_count
		assertion_count += 1
		try:
			if not predicate():
				failures.append(name)
		except Exception as error:  # pragma: no cover - diagnostic safety net
			failures.append(f"{name}: {error}")

	with tempfile.TemporaryDirectory(prefix="game-2d-stress-") as temp:
		root = Path(temp)
		manifest_path = _stress_fixture(root)
		known = audit(root, manifest_path)
		expect("known debt must be exact", lambda: known.exact)
		expect("known debt must remain unsatisfied", lambda: known.status == "UNSATISFIED")
		expect("regression gate accepts exact debt inventory",
			lambda: exit_code(known, "regression-gate") == 0)
		expect("strict rejects known debt", lambda: exit_code(known, "strict") != 0)

		(root / "assets/legacy/new.glb").write_bytes(b"new model")
		new_model = audit(root, manifest_path)
		expect("new model must fail",
			lambda: any(item.check_id == "G2D101" for item in new_model.findings))
		(root / "assets/legacy/new.glb").unlink()
		(root / "assets/legacy/new.glb.import").write_text("[remap]\n", encoding="utf-8")
		new_sidecar = audit(root, manifest_path)
		expect("new model import sidecar must fail",
			lambda: any(item.check_id == "G2D101" for item in new_sidecar.findings))
		(root / "assets/legacy/new.glb.import").unlink()

		(root / "gen2/meshy").mkdir(parents=True, exist_ok=True)
		(root / "gen2/meshy/source.blend1").write_bytes(b"new source model backup")
		new_source = audit(root, manifest_path)
		expect("new repository/source model must fail",
			lambda: any(item.check_id == "G2D101" for item in new_source.findings))
		(root / "gen2/meshy/source.blend1").unlink()

		(root / "scripts/new_3d.gd").write_text("var camera: Camera3D\n", encoding="utf-8")
		new_code = audit(root, manifest_path)
		expect("new 3D code file must fail",
			lambda: any(item.check_id == "G2D101" for item in new_code.findings))
		(root / "scripts/new_3d.gd").unlink()

		legacy = root / "scripts/legacy.gd"
		original = legacy.read_text(encoding="utf-8")
		legacy.write_text(original + "var camera: Camera3D\n", encoding="utf-8")
		expanded = audit(root, manifest_path)
		expect("existing 3D file expansion must fail",
			lambda: any(item.check_id == "G2D102" for item in expanded.findings))
		legacy.write_text(original, encoding="utf-8")

		raw = json.loads(manifest_path.read_text(encoding="utf-8"))
		raw["model_files"] = []
		raw["declared_counts"]["model_files"] = 0
		manifest_path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
		missing = audit(root, manifest_path)
		expect("missing manifest entry must fail",
			lambda: any(item.check_id == "G2D101" for item in missing.findings))

		_write_manifest(manifest_path, discover(root))
		(root / "assets/legacy/prop.glb").unlink()
		stale = audit(root, manifest_path)
		expect("stale model entry must fail",
			lambda: any(item.check_id == "G2D201" for item in stale.findings))

		(root / "assets/legacy/prop.glb").write_bytes(b"model")
		empty = Inventory()
		_write_manifest(manifest_path, empty)
		false_empty = audit(root, manifest_path)
		expect("false empty baseline must fail",
			lambda: exit_code(false_empty, "regression-gate") != 0 and bool(false_empty.findings))

	empty_fingerprint: dict[str, int | str] = {
		"size": 0, "sha256": hashlib.sha256(b"").hexdigest(),
	}
	previous, previous_errors = _parse_manifest_document(
		manifest_dict(Inventory(
			model_files=("assets/old.glb",),
			model_file_fingerprints={"assets/old.glb": empty_fingerprint},
		)), "previous")
	current, current_errors = _parse_manifest_document(
		manifest_dict(Inventory(
			model_files=("assets/new.glb", "assets/old.glb"),
			model_file_fingerprints={
				"assets/new.glb": empty_fingerprint,
				"assets/old.glb": empty_fingerprint,
			},
		)), "current")
	history_findings: list[Finding] = []
	if previous is not None and current is not None:
		_compare_manifest_history(current, previous, history_findings)
	expect("updated manifest cannot bless expanded debt",
		lambda: not previous_errors and not current_errors and
			any(item.check_id == "G2D401" for item in history_findings))

	with tempfile.TemporaryDirectory(prefix="game-2d-stress-clean-") as temp:
		root = Path(temp)
		manifest_path = _stress_fixture(root, with_debt=False)
		clean = audit(root, manifest_path)
		expect("true empty strict state must satisfy",
			lambda: clean.satisfied and exit_code(clean, "strict") == 0)

	if failures:
		for failure in failures:
			print(f"GAME2D| STRESS FAIL| {failure}")
		return 1
	print(f"GAME2D| stress: {assertion_count} falsification/control assertions ALL OK")
	return 0


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
	parser.add_argument("--manifest", type=Path, default=None)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--regression-gate", action="store_true")
	mode.add_argument("--strict", action="store_true")
	mode.add_argument("--stress", action="store_true")
	mode.add_argument("--refresh-manifest", action="store_true")
	args = parser.parse_args(argv)
	if args.stress:
		return stress()
	if args.refresh_manifest:
		ok, findings = refresh_manifest(
			args.root, args.manifest,
			initial_ceiling_anchor=INITIAL_CEILING_SHA256,
		)
		for finding in findings:
			print(f"GAME2D| REFRESH FAIL| {finding.check_id}| {finding.path}| {finding.detail}")
		if ok:
			print("GAME2D| REFRESH| OK - exact debt inventory shrank; initial ceiling preserved")
		return 0 if ok else 1
	mode_name = "strict" if args.strict else (
		"regression-gate" if args.regression_gate else "default")
	result = audit(
		args.root, args.manifest,
		initial_ceiling_anchor=INITIAL_CEILING_SHA256,
	)
	print(render(result, mode_name))
	return exit_code(result, mode_name)


if __name__ == "__main__":
	raise SystemExit(main())
