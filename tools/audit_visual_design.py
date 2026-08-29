#!/usr/bin/env python3
"""Game-wide visual design audit for Mermaid Roshan: Reef of Light.

Why this exists
---------------
The game is authored and shipped as polished fixed-view 2.5D storybook art.
World artwork is raster imagery on Sprite3D/AnimatedSprite3D cards; Canvas is
reserved for UI, safe-band overlays, touch feedback, cinematics, and registered
legacy exceptions. A declared projection is immutable, ordinary cameras are
static, and wide rooms may translate X only inside audited bounds. GLB/model,
mesh, rig, and spatial gameplay physics remain forbidden. The current design
language still contains numeric, checkable promises — independently moving
Canvas layers, alpha-layer overdraw budgets, state-local figure/ground
readability, and texture legality. Written promises rot silently. This tool
turns each of them into a check that fails out loud.

Design contract (read before extending)
---------------------------------------
1.  Every check maps to a named rule in ``tools/visual_audit_spec.json``.
    A check with no rule behind it is an opinion, and opinions do not gate.
2.  Every check is a pure function of (zone, repo, runtime_facts) -> findings.
    No check may mutate the repo.
3.  A check that cannot run (missing runtime facts, missing asset class)
    reports COVERAGE_GAP with a reason. A rule that genuinely does not apply
    reports NOT_APPLICABLE explicitly. Silence is never a pass.
4.  Every check must be provably falsifiable: ``--stress`` builds a synthetic
    zone engineered to violate it and asserts the check fires.  A check that
    survives the stress pass unfired is a broken check and the stress run
    fails.

Usage
-----
    python3 tools/audit_visual_design.py                 # advisory, all zones
    python3 tools/audit_visual_design.py --zone sky_lagoon
    python3 tools/audit_visual_design.py --strict        # saved-facts gaps block
    python3 tools/audit_visual_design.py --fresh-runtime --strict
    python3 tools/audit_visual_design.py --list-checks
    python3 tools/audit_visual_design.py --stress        # self-test the checks
    python3 tools/audit_visual_design.py --format json

Runtime facts (produced by scripts/probe_visual_audit.gd) default to
``audit/visual_runtime_facts.json``; ``--runtime-facts`` accepts an isolated
capture bundle for diagnostics only. Runtime PASS authority requires
``--fresh-runtime``: this process launches the probe with a random one-use
challenge, snapshots verified captures into memory, and removes its temporary
output. Static checks run without facts; scene/capture checks report
COVERAGE_GAP without fresh authority, and strict mode fails.
"""

from __future__ import annotations

import argparse
import glob as globlib
import hashlib
import io
import json
import math
import os
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field, asdict
from functools import lru_cache
from typing import Callable, Iterable, Iterator

try:
    import audit_game_2d as game_2d
except ModuleNotFoundError:  # imported as tools.audit_visual_design in unit tests
    from tools import audit_game_2d as game_2d

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_PATH = os.path.join(REPO, "tools", "visual_audit_spec.json")
RUNTIME_FACTS_PATH = os.path.join(REPO, "audit", "visual_runtime_facts.json")
REPORT_JSON = os.path.join(REPO, "audit", "visual_design_report.json")
REPORT_MD = os.path.join(REPO, "audit", "visual_design_report.md")
LICENSES = os.path.join(REPO, "ASSET_LICENSES.md")

ERROR, WARN, INFO, MANUAL, SKIP = "ERROR", "WARN", "INFO", "MANUAL", "SKIP"
SEVERITY_ORDER = {ERROR: 0, WARN: 1, MANUAL: 2, INFO: 3, SKIP: 4}

# Lifecycle disposition is independent from severity. Severity describes the
# impact; disposition says whether the audit has enough evidence to close it.
PASS = "PASS"
FAIL = "FAIL"
REVIEW_OPEN = "REVIEW_OPEN"
MANUAL_OPEN = "MANUAL_OPEN"
COVERAGE_GAP = "COVERAGE_GAP"
WAIVED = "WAIVED"
NOT_APPLICABLE = "NOT_APPLICABLE"
DISPOSITIONS = (FAIL, REVIEW_OPEN, MANUAL_OPEN, COVERAGE_GAP,
                WAIVED, PASS, NOT_APPLICABLE)
DISPOSITION_ORDER = {state: index for index, state in enumerate(DISPOSITIONS)}
DEFAULT_DISPOSITION = {
    ERROR: FAIL,
    WARN: REVIEW_OPEN,
    MANUAL: MANUAL_OPEN,
    SKIP: COVERAGE_GAP,
    INFO: PASS,
}
STRICT_BLOCKING_DISPOSITIONS = {FAIL, REVIEW_OPEN, MANUAL_OPEN, COVERAGE_GAP}
WAIVABLE_DISPOSITIONS = {FAIL, REVIEW_OPEN}

# Presentations whose source art can be triaged as a painted stack. The legacy
# row remains in this set only so its source images receive risk triage; it is
# not an accepted runtime presentation.
FIXED_VIEW_PRESENTATIONS = {
    "panning_depth_cards", "fixed_depth_cards", "overhead_canvas",
    "legacy_3d_debt",
}
FLAT_PRESENTATIONS = FIXED_VIEW_PRESENTATIONS

# The parallax/occlusion rules are specific to the side-on promenade: it is the
# only presentation where the camera pans across a set and the player moves
# through a depth band. Fixed-camera stages are explicitly exempt from
# parallax, but not readability, touch, ownership, or hierarchy rules.
PARALLAX_PRESENTATIONS = {"panning_depth_cards"}

FORBIDDEN_3D_MODEL_EXTENSIONS = tuple(sorted(game_2d.MODEL_EXTENSIONS))
TRANSITIVE_SOURCE_EXTENSIONS = (
    ".gd", ".gdshader", ".gdshaderinc", ".tscn", ".tres",
)
UNSUPPORTED_EXECUTABLE_SOURCE_EXTENSIONS = (
    ".cs", ".dll", ".dylib", ".gdc", ".gde", ".gdextension", ".gdnlib",
    ".lua", ".so",
)
OPAQUE_RUNTIME_RESOURCE_EXTENSIONS = (
    ".7z", ".mesh", ".pck", ".rar", ".res", ".scn", ".tar",
    ".tar.bz2", ".tar.gz", ".tar.xz", ".tbz", ".tbz2", ".tgz",
    ".txz", ".zip",
)
RUNTIME_RESOURCE_CALL_PATTERN = (
    r"(?:\bload|\bpreload|ResourceLoader\.(?:load|load_interactive|"
    r"load_threaded_get|load_threaded_request)|"
    r"GDExtensionManager\.load_extension|OS\.open_dynamic_library|"
    r"ProjectSettings\.load_resource_pack|"
    r"[A-Za-z_]\w*\.(?:change_scene_to_file|load_scene)|"
    r"\bchange_scene_to_file)"
)
RUNTIME_LITERAL_PREFIX_RE = re.compile(
    r"(?:\b(?:load|preload)\s*\(\s*&?\s*|"
        r"\bResourceLoader\s*\.\s*(?:load|load_interactive|load_threaded_get|"
        r"load_threaded_request)\s*\(\s*&?\s*|"
    r"\bchange_scene_to_file\s*\(\s*&?\s*|\bextends\s+&?\s*|"
    r"\bpath\s*=\s*&?\s*)$"
)
RENDERING_SERVER_3D_METHOD_PREFIXES = (
    "camera", "compositor", "decal", "environment", "fog_volume", "instance",
    "light", "lightmap", "mesh", "occluder", "reflection_probe", "scenario",
    "shadow_atlas", "skeleton", "sky", "voxel_gi",
)
RENDERING_SERVER_CANVAS_METHOD_PREFIXES = (
    "canvas", "canvas_item", "canvas_texture",
)
RENDERING_SERVER_OBSERVATION_METHODS = {
    "frame_post_draw", "frame_pre_draw",
    "get_current_rendering_driver_name", "get_current_rendering_method",
    "get_default_clear_color", "get_rendering_info",
    "get_video_adapter_api_version", "get_video_adapter_driver_info",
    "get_video_adapter_driver_version", "get_video_adapter_name",
    "get_video_adapter_type", "get_video_adapter_vendor", "has_os_feature",
    "is_low_end", "set_default_clear_color",
}
CANVAS_SAFE_ENGINE_SINGLETONS = {
    "AudioServer", "DisplayServer", "NavigationServer2D", "PhysicsServer2D",
    "TextServerManager", "TranslationServer",
}

# Capture adapters are executable probe code, not naming conventions.  Keep
# this allow-list deliberately closed: adding a state to the spec does not make
# the probe capable of entering or asserting that state.  ``fx`` is the exact
# synthetic positive control used by this module's isolated unit fixture.
RENDERED_STATE_ADAPTER_CONTRACTS = {
    ("sky_lagoon", "promenade_idle"): {
        "adapter": "probe_visual_audit:sky_lagoon_promenade_idle",
        "method": "explicit_live_state_assertions_v1",
        "state": {
            "focus": "",
            "game": "level2",
            "intro_active": False,
            "mg_kind": "",
            "phase": "promenade",
            "play_animation_empty": True,
            "tree_paused": False,
            "world_controls_enabled": True,
            "zone": "sky_lagoon",
        },
    },
    ("fx", "idle"): {
        "adapter": "probe_visual_audit:fx_idle",
        "method": "explicit_live_state_assertions_v1",
        "state": {"fixture": "idle", "zone": "fx"},
    },
}
CANVAS_STAGE_TYPES = (
    "CanvasItem", "CanvasLayer", "Node2D", "Sprite2D", "Parallax2D",
    "TextureRect", "Control", "Camera2D",
)
SPRITE3D_STAGE_TYPES = (
    "Node3D", "Sprite3D", "AnimatedSprite3D", "Camera3D",
)

RUNTIME_EVIDENCE_SCHEMA = 2
RUNTIME_EVIDENCE_FILES = {
    "probe": "scripts/probe_visual_audit.gd",
    "spec": "tools/visual_audit_spec.json",
    "scene": "scenes/main.tscn",
    "project": "project.godot",
    "main_script": "scripts/main.gd",
    "player_script": "scripts/player.gd",
    "fixed_view_25d_contract": "tools/audit_fixed_view_25d.py",
    "auditor": "tools/audit_visual_design.py",
}
RENDERED_DIFF_METHOD = "visible_minus_target_hidden_rgba8_exact_v1"
CANVAS_COVERAGE_METHOD = "viewport_grid_effective_canvas_alpha_64x36_v2"
CANVAS_COMPOSITE_SIGNATURE_METHOD = "viewport_grid_effective_canvas_rgba_64x36_v1"
CANVAS_MOTION_METHOD = "viewport_canvas_transform_delta"
CANVAS_DRAW_ORDER_METHOD = \
    "deterministic_effective_canvas_z_verified_descendants_v3"
SOURCE_PROJECTION_METHOD = "independent_source_alpha_inverse_canvas_v1"
CANVAS_OCCLUSION_METHOD = \
    "live_canvas_alpha_overlap_effective_z_groups_v3"
TEMPORAL_FREEZE_METHOD = "engine_time_scale_zero_alternating_visibility_v1"

RUNTIME_MANIFEST_SUFFIXES = (
    ".cs", ".gd", ".gdc", ".gde", ".gdextension", ".gdnlib",
    ".gdshader", ".gdshaderinc", ".json", ".lua", ".tscn", ".tres",
)
RUNTIME_MANIFEST_EXCLUDED_DIRS = {
    ".git", ".godot", "__pycache__", "audit", "tmp",
}


# --------------------------------------------------------------------------
# finding + check registry
# --------------------------------------------------------------------------

@dataclass
class Finding:
    check: str
    zone: str
    severity: str
    message: str
    rule: str = ""
    evidence: dict = field(default_factory=dict)
    disposition: str = ""

    def __post_init__(self) -> None:
        if not self.disposition:
            self.disposition = DEFAULT_DISPOSITION.get(self.severity, FAIL)
        if self.disposition not in DISPOSITIONS:
            raise ValueError(f"unknown audit disposition: {self.disposition}")

    def key(self) -> tuple:
        return (DISPOSITION_ORDER.get(self.disposition, 99),
                SEVERITY_ORDER.get(self.severity, 9), self.check, self.zone)


@dataclass
class Check:
    id: str
    category: str
    rule: str
    doc: str
    fn: Callable
    presentations: set | None = None  # None = every presentation
    stressable: bool = True      # False only for checks with no synthetic form


REGISTRY: dict[str, Check] = {}


def check(check_id: str, category: str, rule: str,
          presentations: Iterable[str] | None = None,
          stressable: bool = True):
    """Register an audit check.  ``rule`` must name a key in spec['rules']."""

    def deco(fn: Callable) -> Callable:
        REGISTRY[check_id] = Check(
            id=check_id, category=category, rule=rule,
            doc=(fn.__doc__ or "").strip().split("\n")[0],
            fn=fn, presentations=set(presentations) if presentations else None,
            stressable=stressable,
        )
        return fn

    return deco


# --------------------------------------------------------------------------
# repo access — everything a check is allowed to look at
# --------------------------------------------------------------------------

class Repo:
    """Read-only, cached view of the repository for the checks."""

    def __init__(self, root: str, spec: dict, runtime_facts: dict | None = None,
                 fresh_attestation: dict | None = None):
        self.root = root
        self.spec = spec
        self.budgets = spec.get("budgets", {})
        self.runtime = runtime_facts or {}
        self.fresh_attestation = fresh_attestation
        self._img_cache: dict[str, dict] = {}
        self._text_cache: dict[str, str] = {}
        self._texture_import_cache: dict[str, dict] = {}
        self._visible_pixel_hash_cache: dict[str, str] = {}
        self._source_closure_cache: dict[tuple[str, ...], tuple] = {}
        self._builder_stage_cache: dict[str, dict] = {}
        self._active_3d_classification_cache: dict[tuple[str, ...], tuple] = {}
        self._global_class_source_cache: dict[str, tuple[str, ...]] | None = None
        self._head_tracked_files_cache: frozenset[str] | None = None
        self._head_tracked_files_loaded = False
        self._all_source: str | None = None

    # -- files ------------------------------------------------------------
    def expand(self, patterns: Iterable[str]) -> list[str]:
        out: list[str] = []
        for pat in patterns:
            hits = sorted(globlib.glob(os.path.join(self.root, pat), recursive=True))
            out.extend(os.path.relpath(h, self.root) for h in hits if os.path.isfile(h))
        return sorted(set(out))

    def read(self, rel: str) -> str:
        if rel not in self._text_cache:
            path = os.path.join(self.root, rel)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    self._text_cache[rel] = fh.read()
            except OSError:
                self._text_cache[rel] = ""
        return self._text_cache[rel]

    def exists(self, rel: str) -> bool:
        return os.path.exists(os.path.join(self.root, rel))

    def size(self, rel: str) -> int:
        try:
            return os.path.getsize(os.path.join(self.root, rel))
        except OSError:
            return 0

    def path(self, rel_or_abs: str) -> str:
        return (rel_or_abs if os.path.isabs(rel_or_abs)
                else os.path.join(self.root, rel_or_abs))

    def sha256(self, rel_or_abs: str) -> str:
        """Hash a current source/capture without trusting a facts-file claim."""
        attested = self.attested_capture_bytes(rel_or_abs)
        if attested is not None:
            return hashlib.sha256(attested).hexdigest()
        try:
            digest = hashlib.sha256()
            with open(self.path(rel_or_abs), "rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()
        except OSError:
            return ""

    def attested_capture_bytes(self, rel_or_abs: str) -> bytes | None:
        """Return the immutable in-process snapshot of a fresh probe capture."""
        if not isinstance(self.fresh_attestation, dict):
            return None
        blobs = self.fresh_attestation.get("capture_bytes")
        if not isinstance(blobs, dict):
            return None
        value = blobs.get(str(rel_or_abs))
        return value if isinstance(value, bytes) else None

    def capture_exists(self, rel_or_abs: str) -> bool:
        """Accept an already-consumed fresh capture snapshot or a diagnostic file."""
        return self.attested_capture_bytes(rel_or_abs) is not None \
            or os.path.isfile(self.path(rel_or_abs))

    def open_image(self, rel_or_abs: str):
        """Open fresh capture bytes from memory, preventing post-probe TOCTOU."""
        from PIL import Image
        blob = self.attested_capture_bytes(rel_or_abs)
        if blob is not None:
            return Image.open(io.BytesIO(blob))
        return Image.open(self.path(rel_or_abs))

    def all_source(self) -> str:
        """Every .gd / .tscn / .py body concatenated — for reference scans."""
        if self._all_source is None:
            chunks = []
            for sub, exts in (("scripts", (".gd",)), ("scenes", (".tscn",)),
                              ("tools", (".py",))):
                base = os.path.join(self.root, sub)
                for dirpath, _dirs, files in os.walk(base):
                    for name in files:
                        if name.endswith(exts):
                            rel = os.path.relpath(os.path.join(dirpath, name), self.root)
                            chunks.append(self.read(rel))
            self._all_source = "\n".join(chunks)
        return self._all_source

    # -- images -----------------------------------------------------------
    def image(self, rel: str) -> dict:
        """Perceptual summary of one PNG.  Cached; returns {} if unreadable."""
        if rel in self._img_cache:
            return self._img_cache[rel]
        info: dict = {}
        try:
            from PIL import Image
            import numpy as np
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(os.path.join(self.root, rel)) as im:
                w, h = im.size
                rgba = np.asarray(im.convert("RGBA"), dtype=np.float32) / 255.0
            alpha = rgba[..., 3]
            rgb = rgba[..., :3]
            opaque = alpha > 0.5
            coverage = float(opaque.mean())
            if opaque.sum() > 0:
                px = rgb[opaque]
                mx = px.max(axis=1)
                mn = px.min(axis=1)
                sat = float(((mx - mn) / np.maximum(mx, 1e-6)).mean())
                lum = float((px @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)).mean())
                # local contrast proxy: stdev of luminance across the opaque art
                lum_std = float((px @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)).std())
            else:
                sat = lum = lum_std = 0.0
            info = {
                "w": w, "h": h, "px": w * h,
                "has_alpha": bool((alpha < 0.999).any()),
                "coverage": coverage,
                "saturation": sat,
                "luminance": lum,
                "contrast": lum_std,
                # uncompressed VRAM cost if the importer cannot block-compress
                "rgba_bytes": w * h * 4,
                "pot": _is_pot(w) and _is_pot(h),
            }
        except Exception as exc:                                  # noqa: BLE001
            info = {"error": f"{type(exc).__name__}: {exc}"}
        self._img_cache[rel] = info
        return info

    def texture_import(self, rel: str) -> dict:
        """Reviewed Godot texture-import settings relevant to GPU residency."""
        if rel in self._texture_import_cache:
            return self._texture_import_cache[rel]
        source = self.read(rel + ".import")
        mode_match = re.search(r"^compress/mode=(\d+)$", source, re.MULTILINE)
        high_match = re.search(
            r"^compress/high_quality=(true|false)$", source, re.MULTILINE)
        mip_match = re.search(
            r"^mipmaps/generate=(true|false)$", source, re.MULTILINE)
        info = {
            "mode": int(mode_match.group(1)) if mode_match else None,
            "high_quality": high_match is not None and high_match.group(1) == "true",
            "mipmaps": mip_match is not None and mip_match.group(1) == "true",
        }
        self._texture_import_cache[rel] = info
        return info

    def texture_vram_bytes(self, rel: str) -> int:
        """Conservative Android GPU bytes from the pinned Godot import mode.

        Godot's VRAM-compressed ETC2 path stores opaque colour as 4-bpp ETC2
        RGB and alpha art as 8-bpp ETC2 RGBA. Lossless/lossy source storage is
        decoded to 32-bpp on upload. Missing sidecars stay conservatively
        uncompressed; the separate sidecar check explains the missing review.
        """
        image = self.image(rel)
        if "error" in image:
            return 0
        settings = self.texture_import(rel)
        width = int(image.get("w", 0))
        height = int(image.get("h", 0))
        mipmaps = bool(settings.get("mipmaps", False))
        mode = settings.get("mode")
        total = 0
        while width > 0 and height > 0:
            if mode == 2:
                # ETC2 is block-compressed in 4x4 blocks. High-quality imports
                # may select an 8-bpp path even for opaque art, so retain the
                # conservative block size there.
                block_bytes = 16 if image.get("has_alpha") \
                    or settings.get("high_quality") else 8
                total += math.ceil(width / 4) * math.ceil(height / 4) * block_bytes
            else:
                total += width * height * 4
            if not mipmaps or (width == 1 and height == 1):
                break
            width = max(1, width // 2)
            height = max(1, height // 2)
        return total

    def license_patterns(self) -> list[str]:
        """Every asset path token in ASSET_LICENSES.md, brace-expanded.

        Rows license families with globs and brace groups, so the raw text is
        not a usable membership test on its own.
        """
        if not hasattr(self, "_lic"):
            doc = self.read("ASSET_LICENSES.md")
            tokens = re.findall(r"[A-Za-z0-9_./*{}\[\],.\-]*\.(?:png|jpg|jpeg|glb|ogg)", doc)
            pats: list[str] = []
            for tok in tokens:
                for expanded in brace_expand(tok):
                    pats.append(expanded.strip("`* "))
                    pats.append(expanded)
            self._lic = sorted(set(p for p in pats if p))
        return self._lic

    # -- gdscript introspection -------------------------------------------
    def const_floats(self, rel: str) -> dict[str, float]:
        """``const NAME := 12.5`` / ``const NAME: float = 12.5`` -> {NAME: 12.5}."""
        out: dict[str, float] = {}
        pat = re.compile(r"^\s*const\s+([A-Z][A-Z0-9_]*)\s*(?::\s*\w+\s*)?:?=\s*(-?\d+\.?\d*)\s*(?:#.*)?$",
                         re.MULTILINE)
        for name, value in pat.findall(self.read(rel)):
            out[name] = float(value)
        return out


def _is_pot(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


_BRACE_LIST = re.compile(r"\{([^{}]*)\}")


def brace_expand(token: str) -> list[str]:
    """Expand shell-style ``{a,b}`` and ``{0..3}`` groups.

    ASSET_LICENSES.md licenses whole families in one row
    (``flat_..._tile_{0..3}.png``).  A matcher that cannot read that notation
    accuses the art of being unlicensed when it is not — so the expansion
    lives here rather than in the check.
    """
    hit = _BRACE_LIST.search(token)
    if not hit:
        return [token]
    body = hit.group(1)
    span = hit.span()
    rng = re.fullmatch(r"(\d+)\.\.(\d+)", body.strip())
    if rng:
        lo, hi = int(rng.group(1)), int(rng.group(2))
        parts = [str(i) for i in range(min(lo, hi), max(lo, hi) + 1)]
    else:
        parts = [p.strip() for p in body.split(",")]
    out: list[str] = []
    for part in parts:
        out.extend(brace_expand(token[:span[0]] + part + token[span[1]:]))
    return out


@lru_cache(maxsize=1024)
def gdscript_without_comments(source: str) -> str:
    """Remove line comments while retaining strings needed for resource scans."""
    token = re.compile(
        r'"""(?:\\.|[\s\S])*?"""|\'\'\'(?:\\.|[\s\S])*?\'\'\'|'
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|(?m:#[^\r\n]*)'
    )
    return token.sub(
        lambda match: "" if match.group(0).startswith("#") else match.group(0),
        source,
    )


@lru_cache(maxsize=1024)
def gdscript_code(source: str) -> str:
    """Return enough executable GDScript text for conservative type scans.

    The audit deliberately does not accept a comment saying ``Sprite3D was
    removed`` as evidence that a Canvas builder still instantiates Sprite3D.
    Strings and line comments are therefore stripped before type-token scans.
    This is not a parser; the Godot analyzer remains the syntax authority.
    """
    without_comments = gdscript_without_comments(source)
    without_strings = re.sub(
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        '""', without_comments,
    )
    return without_strings


@lru_cache(maxsize=1024)
def _string_contexts(source: str) -> tuple[tuple[str, str], ...]:
    """Return literal value/prefix pairs after comments are removed."""
    without_comments = gdscript_without_comments(source)
    token = re.compile(
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    )
    out: list[tuple[str, str]] = []
    for match in token.finditer(without_comments):
        raw = match.group(0)[1:-1]
        value = raw.replace(r"\"", '"').replace(r"\'", "'").replace(r"\\", "\\")
        out.append((value, without_comments[max(0, match.start() - 160):match.start()]))
    return tuple(out)


def _literal_is_runtime_reference(prefix: str) -> bool:
    """True only when a string is in an executable load/extends/resource slot."""
    return RUNTIME_LITERAL_PREFIX_RE.search(prefix) is not None


def _normalize_res_path(value: str) -> str:
    value = value.lstrip("*")
    if not value.startswith("res://"):
        return ""
    normalized = os.path.normpath(value[6:]).replace("\\", "/")
    if normalized == ".." or normalized.startswith("../") or os.path.isabs(normalized):
        return ""
    return normalized


def _strict_string_value(expression: str, assignments: dict[str, str]) -> str | None:
    """Resolve only literal/identifier ``+`` concatenation.

    The canonical multi-language helper is intentionally permissive and can
    treat a conditional containing two quoted strings as one apparent value.
    Security-sensitive singleton/dispatch identity needs a smaller grammar.
    """
    token_re = re.compile(
        r"\s*((?:&|\^)?(?:\"(?:\\.|[^\"\\])*\"|"
        r"'(?:\\.|[^'\\])*')|[A-Za-z_]\w*|\+)"
    )
    tokens: list[str] = []
    position = 0
    while position < len(expression):
        if not expression[position:].strip():
            position = len(expression)
            break
        match = token_re.match(expression, position)
        if match is None:
            return None
        tokens.append(match.group(1))
        position = match.end()
    if expression[position:].strip() or not tokens or len(tokens) % 2 == 0:
        return None
    values: list[str] = []
    for index, token in enumerate(tokens):
        if index % 2 == 1:
            if token != "+":
                return None
            continue
        literal = re.fullmatch(
            r"(?:&|\^)?([\"'])(.*)\1", token, re.DOTALL)
        if literal is not None:
            raw = literal.group(2)
            values.append(raw.replace(r'\"', '"').replace(r"\'", "'")
                          .replace(r"\\", "\\"))
        elif re.fullmatch(r"[A-Za-z_]\w*", token) and token in assignments:
            values.append(assignments[token])
        else:
            return None
    return "".join(values)


def _strict_string_assignments(source: str) -> dict[str, str]:
    expressions = {
        match.group(1): match.group(2).strip()
        for match in re.finditer(
            r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
            r"(?:\s*:[^=\n]+)?\s*(?::=|=)\s*([^\r\n#]+)", source)
    }
    resolved: dict[str, str] = {}
    for _pass in range(len(expressions) + 1):
        changed = False
        for name, expression in expressions.items():
            if name in resolved:
                continue
            value = _strict_string_value(expression, resolved)
            if value is not None:
                resolved[name] = value
                changed = True
        if not changed:
            break
    return resolved


def _top_level_arguments(expression: str) -> list[str]:
    """Split one call body without treating nested commas as separators."""
    out: list[str] = []
    start = 0
    quote = ""
    escaped = False
    depth = 0
    for index, character in enumerate(expression):
        if escaped:
            escaped = False
        elif quote:
            if character == "\\":
                escaped = True
            elif character == quote:
                quote = ""
        elif character in {'"', "'"}:
            quote = character
        elif character in "([{":
            depth += 1
        elif character in ")]}":
            depth = max(0, depth - 1)
        elif character == "," and depth == 0:
            out.append(expression[start:index].strip())
            start = index + 1
    out.append(expression[start:].strip())
    return out


def _callable_arguments(source: str) -> list[list[str]]:
    masked = game_2d._mask_strings_and_comments(source)
    out: list[list[str]] = []
    for match in re.finditer(r"\bCallable\s*\(", masked):
        open_index = match.end() - 1
        close_index = game_2d._matching_parenthesis(masked, open_index)
        if close_index is not None:
            out.append(_top_level_arguments(source[open_index + 1:close_index]))
    return out


@lru_cache(maxsize=1024)
def _runtime_call_references(source: str) -> tuple[tuple[str, ...], int]:
    """Resolve complete first arguments for runtime loader/scene calls.

    The canonical game-wide scanner supplies the expression parser and simple
    constant folding. Partial string prefixes never count as a resolved call;
    an expression the audit cannot close is explicit coverage debt.
    """
    assignments = game_2d._simple_string_assignments(source)
    masked = game_2d._mask_strings_and_comments(source)
    values: list[str] = []
    unresolved = 0
    for expression in game_2d._call_argument_expressions(
            source, RUNTIME_RESOURCE_CALL_PATTERN, masked):
        value = game_2d._simple_string_value(expression, assignments)
        if value is None:
            unresolved += 1
        else:
            values.append(value)
    return tuple(values), unresolved


@lru_cache(maxsize=1024)
def _indirect_runtime_loader_count(source: str) -> int:
    """Count loader capabilities that escape the direct-call closure parser.

    Bound/Callable/aliased loaders can activate code and resource packs while
    hiding the path from the transitive source walk.  Until such dataflow is
    resolved, it is explicit coverage debt rather than a clean-source pass.
    """
    without_comments = gdscript_without_comments(source)
    code = gdscript_code(source)
    assignments = _strict_string_assignments(without_comments)
    aliases = {"ProjectSettings", "ResourceLoader"}
    assignment_pattern = re.compile(
        r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
        r"(?:\s*:[^=\n]+)?\s*(?::=|=)\s*([A-Za-z_]\w*)\s*$"
    )
    for _pass in range(8):
        changed = False
        for match in assignment_pattern.finditer(code):
            if match.group(2) in aliases and match.group(1) not in aliases:
                aliases.add(match.group(1))
                changed = True
        if not changed:
            break
    alias_pattern = "|".join(
        sorted(map(re.escape, aliases), key=len, reverse=True))
    loader_methods = {
        "load", "load_extension", "load_interactive", "load_resource_pack",
        "load_threaded_get", "load_threaded_request",
        "open_dynamic_library",
    }
    scene_loader_methods = {
        "change_scene_to_file", "load_extension", "load_resource_pack",
        "load_scene", "open_dynamic_library",
    }
    unresolved = 0
    member_re = re.compile(
        rf"\b(?:{alias_pattern})\s*\.\s*([A-Za-z_]\w*)\b")
    for match in member_re.finditer(code):
        method = match.group(1)
        if method in {"call", "call_deferred", "callv"}:
            unresolved += 1
            continue
        if method not in loader_methods:
            continue
        tail = code[match.end():]
        # Only an immediate direct call is consumed by
        # _runtime_call_references. A method value, bind or dynamic dispatch
        # severs the path closure and is therefore a gap.
        if re.match(r"\s*\(", tail) is None:
            unresolved += 1

    callable_re = re.compile(
        rf"Callable\s*\(\s*(?:{alias_pattern})\s*,\s*([^\r\n\)]*)\)")
    for match in callable_re.finditer(without_comments):
        method = _strict_string_value(match.group(1), assignments)
        if method is None or method in loader_methods:
            unresolved += 1

    for arguments in _callable_arguments(without_comments):
        if len(arguments) < 2:
            continue
        method = _strict_string_value(arguments[1], assignments)
        if method in scene_loader_methods:
            unresolved += 1

    masked = game_2d._mask_strings_and_comments(without_comments)
    for expression in game_2d._call_argument_expressions(
            without_comments, r"\.\s*(?:call|call_deferred|callv)", masked):
        method = _strict_string_value(expression, assignments)
        if method in scene_loader_methods:
            unresolved += 1
    for match in re.finditer(
            r"\.\s*(change_scene_to_file|load_extension|load_resource_pack|"
            r"load_scene|open_dynamic_library)\b", code):
        if re.match(r"\s*\(", code[match.end():]) is None:
            unresolved += 1

    residual = code
    residual = member_re.sub("", residual)
    residual = re.sub(
        rf"Callable\s*\(\s*(?:{alias_pattern})\s*,[^\r\n\)]*\)", "", residual)
    residual = assignment_pattern.sub("", residual)
    for alias in aliases:
        if re.search(rf"\b{re.escape(alias)}\b", residual):
            unresolved += 1
            break
    return unresolved


@lru_cache(maxsize=1024)
def _dynamic_script_capability_count(source: str) -> int:
    """Count runtime-created executable script text that static closure cannot audit."""
    code = gdscript_code(source)
    return int(re.search(r"\bGDScript\s*\.\s*new\s*\(", code) is not None) \
        + int(re.search(r"\.\s*source_code\s*=", code) is not None)


def _global_class_sources(repo: Repo) -> dict[str, tuple[str, ...]]:
    """Map project ``class_name`` symbols to their active source files.

    Godot exposes a globally registered class without a preload string. A
    res://-only closure therefore misses exactly the factory indirection this
    audit must reject. Review/build output roots are excluded, while a class
    under a deprecated-resource directory is still followed if active code
    names it.
    """
    if repo._global_class_source_cache is not None:
        return repo._global_class_source_cache
    owners: dict[str, list[str]] = {}
    ignored_dirs = {".git", ".godot", "audit", "tmp", "tools", "__pycache__"}
    for dirpath, child_dirs, filenames in os.walk(repo.root):
        if ".gdignore" in filenames and os.path.abspath(dirpath) != os.path.abspath(repo.root):
            child_dirs[:] = []
            continue
        child_dirs[:] = sorted(name for name in child_dirs if name not in ignored_dirs)
        for filename in sorted(filenames):
            if not filename.endswith(".gd"):
                continue
            rel = os.path.relpath(
                os.path.join(dirpath, filename), repo.root).replace("\\", "/")
            code = gdscript_code(repo.read(rel))
            for name in re.findall(
                    r"(?m)^\s*class_name\s+([A-Za-z_]\w*)\b", code):
                owners.setdefault(name, []).append(rel)
    result = {name: tuple(sorted(set(paths))) for name, paths in owners.items()}
    repo._global_class_source_cache = result
    return result


def _head_tracked_files(repo: Repo) -> frozenset[str] | None:
    """Return paths committed at HEAD, or ``None`` when Git cannot prove them."""
    if repo._head_tracked_files_loaded:
        return repo._head_tracked_files_cache
    repo._head_tracked_files_loaded = True
    try:
        result = subprocess.run(
            ["git", "-C", repo.root, "ls-tree", "-r", "--name-only", "-z", "HEAD"],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    repo._head_tracked_files_cache = frozenset(
        value.decode("utf-8", errors="replace").replace("\\", "/")
        for value in result.stdout.split(b"\0") if value
    )
    return repo._head_tracked_files_cache


def _active_source_tracking_gap(repo: Repo, path: str) -> str:
    """Fail closed when executable closure reaches bytes not bound at HEAD."""
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    tracked = _head_tracked_files(repo)
    if tracked is None:
        return "unverifiable-active-source:" + normalized
    if normalized not in tracked:
        return "untracked-active-source:" + normalized
    return ""


def _source_closure(zone: "Zone", root_values: Iterable[str]) \
        -> tuple[dict[str, str], list[str], list[str], int]:
    """Resolve a cycle-safe text-source closure from explicit runtime roots."""
    roots = {str(path).replace("\\", "/") for path in root_values if str(path)}
    cache_key = tuple(sorted(roots))
    cached = zone.repo._source_closure_cache.get(cache_key)
    if cached is not None:
        return cached
    queue = sorted(roots)
    sources: dict[str, str] = {}
    missing: list[str] = []
    unresolved_runtime_references = 0
    global_classes = _global_class_sources(zone.repo)
    global_class_re = re.compile(
        r"\b(?:" + "|".join(
            sorted(map(re.escape, global_classes), key=len, reverse=True)) + r")\b"
    ) if global_classes else None
    while queue:
        path = queue.pop(0)
        if path in sources or path in missing:
            continue
        if not zone.repo.exists(path):
            missing.append(path)
            continue
        tracking_gap = _active_source_tracking_gap(zone.repo, path)
        if tracking_gap:
            missing.append(tracking_gap)
        source = zone.repo.read(path)
        sources[path] = source
        call_values, unresolved_calls = _runtime_call_references(source)
        unresolved_runtime_references += (
            unresolved_calls + _indirect_runtime_loader_count(source)
            + _dynamic_script_capability_count(source))
        for value in call_values:
            raw_value = value.lstrip("*")
            if not raw_value.startswith("res://"):
                missing.append("external:" + raw_value)
                continue
            dependency = _normalize_res_path(value)
            if dependency.lower().endswith(OPAQUE_RUNTIME_RESOURCE_EXTENSIONS):
                missing.append("opaque:" + dependency)
                continue
            if dependency.lower().endswith(UNSUPPORTED_EXECUTABLE_SOURCE_EXTENSIONS):
                missing.append("unsupported-executable:" + dependency)
                continue
            if not dependency or not dependency.lower().endswith(
                    TRANSITIVE_SOURCE_EXTENSIONS):
                continue
            if dependency not in sources and dependency not in queue:
                queue.append(dependency)
        if path.lower().endswith((".gdshader", ".gdshaderinc")):
            for include_value in re.findall(
                    r'(?m)^\s*#include\s+["\']([^"\']+)["\']', source):
                if include_value.startswith("res://"):
                    dependency = _normalize_res_path(include_value)
                elif "://" not in include_value:
                    dependency = os.path.normpath(
                        os.path.join(os.path.dirname(path), include_value)
                    ).replace("\\", "/")
                else:
                    missing.append("external:" + include_value)
                    continue
                if dependency == ".." or dependency.startswith("../") \
                        or os.path.isabs(dependency):
                    missing.append("external:" + include_value)
                    continue
                if dependency.endswith((".gdshader", ".gdshaderinc")) \
                        and dependency not in sources and dependency not in queue:
                    queue.append(dependency)
        for value, prefix in _string_contexts(source):
            raw_value = value.lstrip("*")
            if not _literal_is_runtime_reference(prefix):
                # project.godot autoload/main-scene/plugin bindings are active
                # dependency roots even though they are not function calls.
                if path != RUNTIME_EVIDENCE_FILES["project"] \
                        or not raw_value.startswith("res://"):
                    continue
            if not raw_value.startswith("res://"):
                missing.append("external:" + raw_value)
                continue
            dependency = _normalize_res_path(value)
            if re.search(r"\btype\s*=\s*[\"']Script[\"']", prefix) \
                    and not dependency.lower().endswith(".gd"):
                missing.append("unsupported-script:" + dependency)
                continue
            if dependency.lower().endswith(OPAQUE_RUNTIME_RESOURCE_EXTENSIONS):
                missing.append("opaque:" + dependency)
                continue
            if dependency.lower().endswith(UNSUPPORTED_EXECUTABLE_SOURCE_EXTENSIONS):
                missing.append("unsupported-executable:" + dependency)
                continue
            if not dependency or not dependency.lower().endswith(
                    TRANSITIVE_SOURCE_EXTENSIONS):
                continue
            if dependency not in sources and dependency not in queue:
                queue.append(dependency)
        code = gdscript_code(source)
        referenced_classes = set(global_class_re.findall(code)) \
            if global_class_re is not None else set()
        for class_name in referenced_classes:
            class_paths = global_classes[class_name]
            for dependency in class_paths:
                if dependency not in sources and dependency not in queue:
                    queue.append(dependency)
        queue.sort()
    result = (sources, sorted(roots), sorted(set(missing)),
              unresolved_runtime_references)
    zone.repo._source_closure_cache[cache_key] = result
    return result


def _active_source_closure(zone: "Zone") \
        -> tuple[dict[str, str], list[str], list[str], int]:
    """Resolve the complete game-wide source closure used by active presentation."""
    roots = {
        RUNTIME_EVIDENCE_FILES["scene"],
        RUNTIME_EVIDENCE_FILES["project"],
        RUNTIME_EVIDENCE_FILES["main_script"],
        RUNTIME_EVIDENCE_FILES["player_script"],
        *zone.builders,
    }
    for raw in zone.repo.spec.get("zones", []):
        if isinstance(raw, dict) and raw.get("lifecycle") == "active_shipped":
            builders = raw.get("builders", [])
            if isinstance(builders, list):
                roots.update(str(path).replace("\\", "/") for path in builders)
    return _source_closure(zone, roots)


def _rendering_server_method_counts(source: str) -> Counter[str]:
    """Classify low-level rendering calls, including common indirection.

    ``RenderingServer`` can create a complete spatial world without a single
    scene-tree spatial node.  Direct-call regexes are therefore insufficient:
    aliases, ``Engine.get_singleton`` and ``Callable`` method references must
    be resolved too.  Any executable use that cannot be classified is a
    coverage gap, never proof of a clean Canvas presentation.
    """
    counts: Counter[str] = Counter()
    without_comments = gdscript_without_comments(source)
    code = gdscript_code(source)
    assignments = _strict_string_assignments(without_comments)
    aliases = {"RenderingServer"}

    assignment_pattern = re.compile(
        r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
        r"(?:\s*:[^=\n]+)?\s*(?::=|=)\s*([A-Za-z_]\w*)\s*$"
    )
    for _pass in range(8):
        changed = False
        for match in assignment_pattern.finditer(code):
            if match.group(2) in aliases and match.group(1) not in aliases:
                aliases.add(match.group(1))
                changed = True
        if not changed:
            break

    singleton_assignment = re.compile(
        r"(?m)^\s*(?:(?:static\s+)?var|const)\s+([A-Za-z_]\w*)"
        r"(?:\s*:[^=\n]+)?\s*(?::=|=)\s*Engine\.get_singleton\s*\((.*?)\)\s*$"
    )
    singleton_expressions = game_2d._call_argument_expressions(
        without_comments, r"Engine\.get_singleton",
        game_2d._mask_strings_and_comments(without_comments))
    singleton_values = [
        _strict_string_value(expression, assignments)
        for expression in singleton_expressions
    ]
    rendering_singleton_calls = sum(
        value == "RenderingServer" for value in singleton_values)
    unresolved_singleton_receivers = sum(
        value is None for value in singleton_values)
    unresolved_singleton_receivers += len(re.findall(
        r"\bEngine\s*\.\s*(?:call|call_deferred|callv)\s*\(", code))
    for arguments in _callable_arguments(without_comments):
        if len(arguments) < 2 or arguments[0].strip() != "Engine":
            continue
        method = _strict_string_value(arguments[1], assignments)
        if method is None or method == "get_singleton":
            unresolved_singleton_receivers += 1
    for match in re.finditer(r"\bEngine\s*\.\s*get_singleton\b", code):
        if re.match(r"\s*\(", code[match.end():]) is None:
            unresolved_singleton_receivers += 1
    for singleton in singleton_values:
        if singleton is None or singleton == "RenderingServer" \
                or singleton in CANVAS_SAFE_ENGINE_SINGLETONS:
            continue
        if "3D" in singleton or "XR" in singleton:
            counts[f"Engine.get_singleton:{singleton}"] += 1
        else:
            unresolved_singleton_receivers += 1
    consumed_rendering_singletons = 0
    for match in singleton_assignment.finditer(without_comments):
        singleton = _strict_string_value(match.group(2), assignments)
        if singleton == "RenderingServer":
            aliases.add(match.group(1))
            consumed_rendering_singletons += 1

    def classify(method: str) -> None:
        def in_family(prefixes: Iterable[str]) -> bool:
            return any(method == prefix or method.startswith(prefix + "_")
                       for prefix in prefixes)

        if in_family(RENDERING_SERVER_3D_METHOD_PREFIXES):
            counts[f"RenderingServer.{method}"] += 1
        elif method in RENDERING_SERVER_OBSERVATION_METHODS \
                or in_family(RENDERING_SERVER_CANVAS_METHOD_PREFIXES) \
                or in_family(("texture", "global_shader_parameter")):
            return
        else:
            counts["<unresolved-rendering-server-call>"] += 1

    alias_pattern = "|".join(
        sorted(map(re.escape, aliases), key=len, reverse=True))
    member_re = re.compile(
        rf"\b(?:{alias_pattern})\s*\.\s*([A-Za-z_]\w*)\b")
    for match in member_re.finditer(code):
        if match.group(1) not in {"call", "call_deferred", "callv"}:
            classify(match.group(1))

    dispatch_re = re.compile(
        rf"\b(?:{alias_pattern})\s*\.\s*(?:call|call_deferred|callv)"
        r"\s*\(\s*([^,\r\n\)]*)")
    for match in dispatch_re.finditer(without_comments):
        method = _strict_string_value(match.group(1), assignments)
        if method is None:
            counts["<unresolved-rendering-server-call>"] += 1
        else:
            classify(method)

    # Chained singleton calls have no named alias and the singleton name is a
    # string, so classify them against the unmasked source separately.
    singleton_member = re.compile(
        r"Engine\.get_singleton\s*\((.*?)\)\s*\.\s*([A-Za-z_]\w*)\b")
    for match in singleton_member.finditer(without_comments):
        singleton = _strict_string_value(match.group(1), assignments)
        if singleton == "RenderingServer":
            classify(match.group(2))
            consumed_rendering_singletons += 1

    # A Callable captures a method even if ``call`` occurs elsewhere. Resolve
    # simple literal/constant concatenation for the method name; otherwise gap.
    callable_re = re.compile(
        rf"Callable\s*\(\s*(?:{alias_pattern})\s*,\s*([^\r\n\)]*)\)")
    for match in callable_re.finditer(without_comments):
        method = _strict_string_value(match.group(1), assignments)
        if method is None:
            counts["<unresolved-rendering-server-call>"] += 1
        else:
            classify(method)

    # Remove every classified/safe form, alias declaration, and explicit null
    # observation. Any remaining singleton token or server alias is being
    # passed/stored/invoked in a way this bounded classifier cannot prove.
    residual = code
    residual = member_re.sub("", residual)
    residual = re.sub(
        rf"Callable\s*\(\s*(?:{alias_pattern})\s*,[^\r\n\)]*\)", "", residual)
    residual = assignment_pattern.sub("", residual)
    residual = re.sub(
        r"(?m)^\s*(?:(?:static\s+)?var|const)\s+[A-Za-z_]\w*"
        r"(?:\s*:[^=\n]+)?\s*(?::=|=)\s*Engine\.get_singleton\s*\([^\n]*\)\s*$",
        "", residual)
    for alias in sorted(aliases, key=len, reverse=True):
        escaped = re.escape(alias)
        residual = re.sub(
            rf"(?:\bis_instance_valid\s*\(\s*{escaped}\s*\)|"
            rf"\b{escaped}\s*(?:==|!=)\s*null|"
            rf"\bnull\s*(?:==|!=)\s*{escaped})", "", residual)
    if any(re.search(rf"\b{re.escape(alias)}\b", residual) for alias in aliases):
        counts["<unresolved-rendering-server-call>"] += 1
    counts["<unresolved-rendering-server-call>"] += (
        unresolved_singleton_receivers
        + max(0, rendering_singleton_calls - consumed_rendering_singletons))
    return counts


def _canonical_game_2d_counts(path: str, source: str) -> Counter[str]:
    """Apply the canonical game-wide 2D taxonomy to one reachable source.

    GDScript prose is removed before raw token classification so comments and
    messages do not become executable visual debt. Canonical ClassDB parsing
    still receives the original source and therefore resolves complete string
    expressions and marks unresolved dynamic instantiation conservatively.
    """
    suffix = os.path.splitext(path)[1].lower()
    if suffix == ".gd":
        counts = Counter(game_2d._token_counts(gdscript_code(source)))
        counts.update(game_2d._classdb_counts(source))
        # Canonical inventory intentionally tracks broad 3D-named constants;
        # this executable gate excludes all-caps configuration symbols unless
        # the canonical contextual classifier found an actual class use.
        for token in list(counts):
            if re.fullmatch(r"[A-Z][A-Z0-9_]*3D[A-Z0-9_]*", token):
                del counts[token]
    else:
        counts = Counter(game_2d._token_counts(
            source,
            configuration=path == RUNTIME_EVIDENCE_FILES["project"],
            scene_resource=suffix in {".tscn", ".tres"},
        ))
    if re.search(r"\bSideScrollStage\b", gdscript_code(source)):
        counts["SideScrollStage"] += 1
    if suffix == ".gd":
        counts.update(_rendering_server_method_counts(source))
    return counts


def builder_stage_evidence(zone: "Zone") -> dict:
    """Classify declared builder source without treating 3D as 2D evidence."""
    cached = zone.repo._builder_stage_cache.get(zone.id)
    if cached is not None:
        return cached
    sources, roots, missing, unresolved_references = _active_source_closure(zone)
    zone_sources, zone_roots, zone_missing, zone_unresolved_references = \
        _source_closure(zone, zone.builders)
    source = "\n".join(sources[path] for path in sorted(sources))
    if not source.strip() and missing:
        result = {"backend": "missing", "builders": zone.builders}
        zone.repo._builder_stage_cache[zone.id] = result
        return result
    classification_key = tuple(sorted(sources))
    classified = zone.repo._active_3d_classification_cache.get(classification_key)
    if classified is None:
        classified_counts: Counter[str] = Counter()
        classified_resources: set[str] = set()
        classified_dynamic = 0
        for path, body in sources.items():
            counts = _canonical_game_2d_counts(path, body)
            classified_dynamic += counts.pop("<dynamic-classdb-instantiation>", 0)
            classified_dynamic += counts.pop("<unresolved-rendering-server-call>", 0)
            classified_counts.update(counts)
            for match in game_2d.MODEL_REFERENCE_RE.finditer(
                    gdscript_without_comments(body)):
                classified_resources.add(match.group(0))
            call_values, _unresolved_calls = _runtime_call_references(body)
            for value in call_values:
                dependency = _normalize_res_path(value)
                if dependency.lower().endswith(FORBIDDEN_3D_MODEL_EXTENSIONS):
                    classified_resources.add(dependency)
            for value, prefix in _string_contexts(body):
                dependency = _normalize_res_path(value)
                if _literal_is_runtime_reference(prefix) \
                        and dependency.lower().endswith(FORBIDDEN_3D_MODEL_EXTENSIONS):
                    classified_resources.add(dependency)
        classified = (
            dict(classified_counts), tuple(sorted(classified_resources)),
            classified_dynamic,
        )
        zone.repo._active_3d_classification_cache[classification_key] = classified
    forbidden_counts = Counter(classified[0])
    forbidden_resources = set(classified[1])
    unresolved_dynamic_types = int(classified[2])
    zone_code = gdscript_code("\n".join(
        zone_sources[path] for path in sorted(zone_sources)))
    canvas: set[str] = {
        token for token in CANVAS_STAGE_TYPES
        if re.search(rf"\b{re.escape(token)}\b", zone_code)
    }
    for path, body in zone_sources.items():
        for value, prefix in _string_contexts(body):
            if re.search(r"\btype\s*=\s*&?\s*$", prefix) \
                    and path in zone_sources and value in CANVAS_STAGE_TYPES:
                canvas.add(value)
    forbidden = sorted(forbidden_counts)
    forbidden_resources = sorted(forbidden_resources)
    if forbidden or forbidden_resources:
        backend = "legacy_3d"
    elif missing or zone_missing or unresolved_dynamic_types \
            or unresolved_references or zone_unresolved_references:
        backend = "unknown"
    elif re.search(r"\b(?:Sprite3D|AnimatedSprite3D)\b", zone_code):
        backend = "sprite3d_25d"
    elif canvas:
        backend = "canvas_2d"
    else:
        backend = "unknown"
    result = {
        "backend": backend,
        "forbidden_types": forbidden,
        "forbidden_token_counts": dict(sorted(forbidden_counts.items())),
        "forbidden_resources": forbidden_resources,
        "canvas_types": sorted(canvas),
        "builders": zone.builders,
        "active_source_roots": roots,
        "source_dependencies": sorted(sources),
        "dependency_gaps": missing,
        "zone_source_roots": zone_roots,
        "zone_source_dependencies": sorted(zone_sources),
        "zone_dependency_gaps": zone_missing,
        "unresolved_dynamic_types": unresolved_dynamic_types,
        "unresolved_runtime_references": unresolved_references,
        "zone_unresolved_runtime_references": zone_unresolved_references,
    }
    zone.repo._builder_stage_cache[zone.id] = result
    return result


def canonical_visible_pixel_signature(repo: Repo, path: str) -> str:
    """Hash decoded RGBA, ignoring encoding metadata and RGB under zero alpha."""
    if path in repo._visible_pixel_hash_cache:
        return repo._visible_pixel_hash_cache[path]
    digest = ""
    try:
        from PIL import Image
        with Image.open(repo.path(path)) as source:
            image = source.convert("RGBA")
            width, height = image.size
            pixels = bytearray(image.tobytes())
        has_visible_pixel = False
        for index in range(0, len(pixels), 4):
            if pixels[index + 3] == 0:
                pixels[index:index + 3] = b"\x00\x00\x00"
            else:
                has_visible_pixel = True
        if not has_visible_pixel:
            repo._visible_pixel_hash_cache[path] = ""
            return ""
        hasher = hashlib.sha256()
        hasher.update(f"{width}x{height}:".encode("ascii"))
        hasher.update(pixels)
        digest = hasher.hexdigest()
    except Exception:  # noqa: BLE001
        digest = ""
    repo._visible_pixel_hash_cache[path] = digest
    return digest


def asset_content_signature(repo: Repo, paths: Iterable[str]) -> str:
    """Stable signature of canonical decoded visible pixels, not PNG encoding."""
    normalized = sorted(set(path.replace("\\", "/") for path in paths))
    if not normalized:
        return ""
    pixel_hashes: list[str] = []
    for path in normalized:
        pixel_hash = canonical_visible_pixel_signature(repo, path)
        if not pixel_hash:
            continue
        if re.fullmatch(r"[0-9a-f]{64}", pixel_hash) is None:
            return ""
        pixel_hashes.append(pixel_hash)
    if not pixel_hashes:
        return ""
    return hashlib.sha256(
        "|".join(sorted(pixel_hashes)).encode("ascii")).hexdigest()


def source_manifest_signature(repo: Repo) -> dict:
    """Hash every project runtime-source candidate, including ignored paths.

    A reachable helper may live outside the conventional source roots or be
    Git-ignored.  Whole-worktree cleanliness does not see ignored files, so the
    challenged probe and verifier independently bind the complete project-wide
    code/scene/resource/shader/data candidate set.
    """
    entries: list[str] = []
    for dirpath, child_dirs, filenames in os.walk(repo.root):
        child_dirs[:] = sorted(
            name for name in child_dirs
            if name not in RUNTIME_MANIFEST_EXCLUDED_DIRS)
        for filename in sorted(filenames):
            if not filename.endswith(RUNTIME_MANIFEST_SUFFIXES):
                continue
            rel = os.path.relpath(
                os.path.join(dirpath, filename), repo.root).replace("\\", "/")
            entries.append(f"{rel}:{repo.sha256(rel)}")
    entries.sort()
    payload = "\n".join(entries).encode("utf-8")
    return {"algorithm": "sha256_project_runtime_candidates_v2",
            "file_count": len(entries),
            "sha256": hashlib.sha256(payload).hexdigest()}


def source_revision_signature(repo: Repo) -> str:
    """Recomputable revision of every bound file plus the runtime source manifest."""
    manifest = source_manifest_signature(repo)
    paths = sorted(set(RUNTIME_EVIDENCE_FILES.values()))
    entries = [f"{path}:{repo.sha256(path)}" for path in paths]
    payload = "|".join([manifest["sha256"], *entries]).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def git_source_identity(repo: Repo) -> dict:
    """Return the independently verifiable checked-out source revision.

    Runtime evidence is intentionally generated outside the dependency roots.
    The code, scenes, art/shaders, project settings, and audit specification are
    required to be a clean checkout of one Git commit.  That makes a source
    edit invalidate an old capture even if somebody rewrites every renewable
    SHA field in the JSON facts file.
    """
    dependency_paths = ["<entire_worktree>"]

    def git(*args: str) -> tuple[int, str]:
        try:
            result = subprocess.run(
                ["git", "-C", repo.root, *args], check=False,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, encoding="utf-8", errors="replace",
            )
        except OSError:
            return 127, ""
        return result.returncode, result.stdout.strip()

    head_code, head = git("rev-parse", "--verify", "HEAD")
    tree_code, tree = git("rev-parse", "HEAD^{tree}")
    status_code, status = git(
        "status", "--porcelain=v1", "--untracked-files=all")
    valid_head = head_code == 0 and re.fullmatch(r"[0-9a-f]{40,64}", head) is not None
    valid_tree = tree_code == 0 and re.fullmatch(r"[0-9a-f]{40,64}", tree) is not None
    return {
        "revision": head if valid_head else "",
        "tree": tree if valid_tree else "",
        "dependencies_clean": status_code == 0 and status == "",
        "status": status,
        "dependency_paths": dependency_paths,
    }


def _runtime_png_paths(runtime: dict) -> set[str]:
    """Return every PNG path asserted anywhere in the runtime response."""
    paths: set[str] = set()

    def visit(value: object, key: str = "") -> None:
        if isinstance(value, dict):
            for child_key, child in value.items():
                visit(child, str(child_key))
        elif isinstance(value, list):
            for child in value:
                visit(child, key)
        elif isinstance(value, str) and key.endswith("path") \
                and value.lower().endswith(".png"):
            paths.add(value)

    visit(runtime)
    return paths


def _runtime_capture_paths(runtime: dict) -> set[str]:
    """Return output images whose bytes must come from the challenged process."""
    paths: set[str] = set()
    named_keys = {
        "capture_path", "target_hidden_capture_path",
        "target_restored_capture_path", "mask_path",
    }

    def visit(value: object) -> None:
        if isinstance(value, dict):
            for key in named_keys:
                path = value.get(key)
                if isinstance(path, str) and path.lower().endswith(".png"):
                    paths.add(path)
            # Stability bindings intentionally use the compact {path, sha256}
            # form. No live-instance/source-art dictionary has that shape.
            path = value.get("path")
            if isinstance(path, str) and path.lower().endswith(".png") \
                    and isinstance(value.get("sha256"), str):
                paths.add(path)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(runtime)
    return paths


def runtime_bundle_signature(repo: Repo, runtime: dict,
                             capture_hashes: dict[str, str] | None = None) -> str:
    """Seal canonical facts plus every referenced PNG byte digest."""
    supplied = capture_hashes if isinstance(capture_hashes, dict) else {}
    capture_entries = [
        f"{path}:{supplied.get(path, repo.sha256(path))}"
        for path in sorted(_runtime_png_paths(runtime))
    ]
    canonical = json.dumps(
        runtime, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(
        (canonical + "\n" + "\n".join(capture_entries)).encode("utf-8")
    ).hexdigest()


def fresh_runtime_attestation(repo: Repo, runtime: dict, challenge: str,
                              capture_root: str | None = None,
                              executable_path: str | None = None) -> dict:
    """Snapshot challenged output into a private, immutable process capability."""
    if re.fullmatch(r"[0-9a-f]{64}", challenge) is None:
        raise ValueError("fresh runtime challenge is malformed")
    capture_paths = _runtime_capture_paths(runtime)
    if not capture_paths:
        raise ValueError("fresh runtime response contains no rendered capture outputs")
    resolved_root = os.path.realpath(capture_root) if capture_root else ""
    blobs: dict[str, bytes] = {}
    hashes: dict[str, str] = {}
    for path in sorted(capture_paths):
        resolved = os.path.realpath(repo.path(path))
        if resolved_root:
            try:
                inside = os.path.commonpath([resolved_root, resolved]) == resolved_root
            except ValueError:
                inside = False
            if not inside:
                raise ValueError(
                    f"fresh capture escaped its private output directory: {path}")
        try:
            with open(resolved, "rb") as handle:
                blob = handle.read()
        except OSError as exc:
            raise ValueError(f"fresh capture is missing: {path}") from exc
        if not blob:
            raise ValueError(f"fresh capture is empty: {path}")
        blobs[path] = blob
        hashes[path] = hashlib.sha256(blob).hexdigest()
    executable = os.path.realpath(executable_path) if executable_path else ""
    executable_sha256 = repo.sha256(executable) if executable else ""
    if executable and not executable_sha256:
        raise ValueError("configured Godot executable cannot be bound")
    return {
        "challenge": challenge,
        "bundle_sha256": runtime_bundle_signature(repo, runtime, hashes),
        "capture_root": resolved_root,
        "capture_paths": sorted(capture_paths),
        "capture_sha256": hashes,
        "capture_bytes": blobs,
        "godot_executable": executable,
        "godot_executable_sha256": executable_sha256,
    }


class Zone:
    """One audited zone, resolved against the repo."""

    def __init__(self, raw: dict, repo: Repo):
        self.raw = raw
        self.repo = repo
        self.id = raw["id"]
        self.name = raw.get("name", raw["id"])
        self.art_medium = raw.get("art_medium", "unknown")
        self.presentation = raw.get("presentation", "unknown")
        self.lifecycle = raw.get("lifecycle", "unknown")
        self.builders = raw.get("builders", [])
        self.probes = raw.get("probes", [])
        self.murals = repo.expand(raw.get("murals", []))
        self.standees = repo.expand(raw.get("standees", []))
        self.characters = repo.expand(raw.get("characters", []))
        self.runtime_auxiliary = repo.expand(raw.get("runtime_auxiliary", []))
        self.texture_peak_alternatives = raw.get("texture_peak_alternatives", [])
        self.canvas_layers = raw.get("canvas_layers", [])
        self.rendered_readability_states = raw.get("rendered_readability_states", [])
        self.asset_roots = raw.get("asset_roots", [])

    @property
    def foreground(self) -> list[str]:
        return self.standees + self.characters

    @property
    def runtime_art(self) -> list[str]:
        return sorted(set(
            self.murals + self.standees + self.characters + self.runtime_auxiliary))

    def budget(self, name: str, default=None):
        return self.raw.get("budgets", {}).get(name, self.repo.budgets.get(name, default))

    def runtime_facts(self) -> dict | None:
        return (self.repo.runtime.get("zones") or {}).get(self.id)

    def resolved_canvas_layers(self) -> list[dict]:
        out: list[dict] = []
        if not isinstance(self.canvas_layers, list):
            return out
        for value in self.canvas_layers:
            row = value if isinstance(value, dict) else {}
            patterns = row.get("assets", [])
            if not isinstance(patterns, list):
                patterns = []
            out.append({
                "id": str(row.get("id", "")),
                "role": str(row.get("role", "")),
                "patterns": patterns,
                "assets": [path.replace("\\", "/")
                           for path in self.repo.expand(patterns)],
                "asset_match": str(row.get("asset_match", "exact")),
                "required_content": bool(row.get("required_content", True)),
                "stack_evidence": bool(row.get("stack_evidence", True)),
                "minimum_coverage_ratio": row.get("minimum_coverage_ratio"),
                "parallax_factor": row.get("parallax_factor"),
                "relative_z_range": row.get("relative_z_range", [0, 0]),
            })
            out[-1]["content_signature"] = asset_content_signature(
                self.repo, out[-1]["assets"])
        return out


def _project_contract_issues(repo: Repo) -> list[str]:
    """Reject capture evidence made under a different project presentation."""
    source = repo.read("project.godot")
    expected_patterns = {
        "main scene": r'^run/main_scene="res://scenes/main\.tscn"$',
        "base width": r"^window/size/viewport_width=1280$",
        "base height": r"^window/size/viewport_height=720$",
        "Canvas stretch mode": r'^window/stretch/mode="canvas_items"$',
        "expand stretch aspect": r'^window/stretch/aspect="expand"$',
        "Mobile renderer": r'^renderer/rendering_method="mobile"$',
    }
    return [f"project.godot does not declare the required {label}"
            for label, pattern in expected_patterns.items()
            if re.search(pattern, source, re.MULTILINE) is None]


def _runtime_contract_issues(zone: Zone, block: dict | None = None) -> list[str]:
    """Bind runtime claims to the exact harness, engine, project, and builder bytes."""
    contract = zone.repo.runtime.get("evidence_contract")
    if not isinstance(contract, dict):
        return ["runtime facts have no evidence_contract provenance"]
    issues: list[str] = []
    if contract.get("schema_version") != RUNTIME_EVIDENCE_SCHEMA:
        issues.append(
            f"runtime evidence schema is {contract.get('schema_version')!r}; "
            f"requires {RUNTIME_EVIDENCE_SCHEMA}")
    fresh_challenge = str(contract.get("fresh_challenge", ""))
    attestation = zone.repo.fresh_attestation
    if not isinstance(attestation, dict):
        issues.append(
            "saved runtime facts have no current one-use fresh-capture attestation")
    else:
        expected_challenge = str(attestation.get("challenge", ""))
        expected_bundle = str(attestation.get("bundle_sha256", ""))
        if re.fullmatch(r"[0-9a-f]{64}", fresh_challenge) is None \
                or re.fullmatch(r"[0-9a-f]{64}", expected_challenge) is None \
                or not secrets.compare_digest(fresh_challenge, expected_challenge):
            issues.append("runtime evidence challenge is missing, stale, or replayed")
        capture_hashes = attestation.get("capture_sha256")
        capture_paths = attestation.get("capture_paths")
        capture_blobs = attestation.get("capture_bytes")
        discovered_paths = sorted(_runtime_capture_paths(zone.repo.runtime))
        if not isinstance(capture_paths, list) \
                or capture_paths != discovered_paths \
                or not isinstance(capture_hashes, dict) \
                or set(capture_hashes) != set(discovered_paths) \
                or not isinstance(capture_blobs, dict) \
                or set(capture_blobs) != set(discovered_paths):
            issues.append("fresh runtime capture snapshot scope is incomplete or changed")
            capture_hashes = {}
        else:
            for path in discovered_paths:
                blob = capture_blobs.get(path)
                digest = capture_hashes.get(path)
                if not isinstance(blob, bytes) \
                        or re.fullmatch(r"[0-9a-f]{64}", str(digest)) is None \
                        or hashlib.sha256(blob).hexdigest() != digest:
                    issues.append(
                        "fresh runtime capture snapshot bytes are missing or changed")
                    break
        current_bundle = runtime_bundle_signature(
            zone.repo, zone.repo.runtime,
            capture_hashes if isinstance(capture_hashes, dict) else None)
        if re.fullmatch(r"[0-9a-f]{64}", expected_bundle) is None \
                or not secrets.compare_digest(current_bundle, expected_bundle):
            issues.append(
                "runtime evidence changed after the one-use fresh capture was attested")
        executable = str(attestation.get("godot_executable", ""))
        executable_sha = str(attestation.get("godot_executable_sha256", ""))
        if executable or executable_sha:
            if not executable or re.fullmatch(r"[0-9a-f]{64}", executable_sha) is None:
                issues.append("fresh runtime has no complete Godot executable binding")
            else:
                current_executable_sha = zone.repo.sha256(executable)
                if current_executable_sha != executable_sha:
                    issues.append("configured Godot executable changed after probe launch")

    files = contract.get("files")
    if not isinstance(files, dict):
        issues.append("runtime evidence has no bound file-hash map")
    else:
        if set(files) != set(RUNTIME_EVIDENCE_FILES):
            issues.append("runtime evidence file-hash scope is incomplete or unexpected")
        for role, expected_path in RUNTIME_EVIDENCE_FILES.items():
            value = files.get(role)
            if not isinstance(value, dict):
                issues.append(f"runtime evidence has no {role} file binding")
                continue
            path = str(value.get("path", "")).replace("\\", "/")
            recorded = str(value.get("sha256", ""))
            if path != expected_path:
                issues.append(
                    f"runtime evidence {role} path is {path!r}; expected {expected_path}")
            elif re.fullmatch(r"[0-9a-f]{64}", recorded) is None:
                issues.append(f"runtime evidence {role} SHA-256 is malformed")
            elif zone.repo.sha256(path) != recorded:
                issues.append(f"runtime evidence is stale: {path} changed")

    manifest = contract.get("source_manifest")
    current_manifest = source_manifest_signature(zone.repo)
    if not isinstance(manifest, dict) or manifest != current_manifest:
        issues.append(
            "runtime evidence source manifest is missing or stale; a script/scene changed")
    source_revision = str(contract.get("source_revision", ""))
    current_revision = source_revision_signature(zone.repo)
    if source_revision != current_revision:
        issues.append("runtime evidence source_revision is missing or stale")
    git_identity = git_source_identity(zone.repo)
    git_revision = str(contract.get("git_revision", ""))
    git_tree = str(contract.get("git_tree", ""))
    if not git_identity["revision"] or not git_identity["tree"]:
        issues.append("runtime evidence cannot be verified against a Git source revision")
    elif git_revision != git_identity["revision"] or git_tree != git_identity["tree"]:
        issues.append("runtime evidence was captured from a different Git source revision")
    if contract.get("git_dependencies_clean") is not True \
            or not git_identity["dependencies_clean"]:
        issues.append(
            "runtime evidence dependencies are not a clean checkout of the bound Git revision")
    run_nonce = str(contract.get("run_nonce", ""))
    run_started_utc = str(contract.get("run_started_utc", ""))
    if re.fullmatch(r"[0-9a-f]{64}", run_nonce) is None:
        issues.append("runtime evidence has no valid run nonce")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
                    run_started_utc) is None:
        issues.append("runtime evidence has no valid UTC run start")
    version_for_identity = str((contract.get("engine") or {}).get(
        "version_string", "")) if isinstance(contract.get("engine"), dict) else ""
    renderer_for_identity = str((contract.get("renderer") or {}).get(
        "actual", "")) if isinstance(contract.get("renderer"), dict) else ""
    expected_identity = hashlib.sha256("|".join([
        git_revision, git_tree, fresh_challenge, source_revision,
        run_nonce, run_started_utc,
        version_for_identity, renderer_for_identity,
    ]).encode("utf-8")).hexdigest()
    run_identity = str(contract.get("run_identity", ""))
    if run_identity != expected_identity:
        issues.append("runtime evidence run identity is not derivable from its revision/run")

    engine = contract.get("engine")
    if not isinstance(engine, dict):
        issues.append("runtime evidence has no Godot engine identity")
    else:
        exact = (engine.get("major"), engine.get("minor"), engine.get("patch"),
                 str(engine.get("status", "")))
        if exact != (4, 7, 1, "stable"):
            issues.append(
                "runtime evidence was not captured by exactly Godot 4.7.1-stable")
        version_string = str(engine.get("version_string", ""))
        if re.match(r"^4\.7\.1(?:[.-])stable(?:\b|\s|\()", version_string) is None:
            issues.append("runtime evidence Godot version string is not 4.7.1-stable")

    renderer = contract.get("renderer")
    if not isinstance(renderer, dict) \
            or renderer.get("actual") != "mobile" \
            or renderer.get("project_setting") != "mobile":
        issues.append("runtime evidence was not rendered with the Mobile renderer")

    capture = contract.get("capture_context")
    if not isinstance(capture, dict) \
            or capture.get("viewport") != [1280, 720] \
            or capture.get("stretch_mode") != "canvas_items" \
            or capture.get("stretch_aspect") != "expand":
        issues.append("runtime evidence has the wrong viewport/stretch capture context")
    issues.extend(_project_contract_issues(zone.repo))

    if block is not None:
        if block.get("run_identity") != run_identity:
            issues.append("runtime evidence block came from a different probe run")
        if block.get("zone_id") != zone.id:
            issues.append("runtime evidence block is bound to a different zone")
        builders = block.get("builder_sha256")
        if not isinstance(builders, dict):
            issues.append("runtime evidence block has no builder SHA-256 map")
        else:
            normalized = {str(path).replace("\\", "/"): str(value)
                          for path, value in builders.items()}
            expected = sorted(set(zone.builders))
            if set(normalized) != set(expected):
                issues.append("runtime builder SHA-256 scope is incomplete or unexpected")
            else:
                for path in expected:
                    recorded = normalized[path]
                    if re.fullmatch(r"[0-9a-f]{64}", recorded) is None \
                            or zone.repo.sha256(path) != recorded:
                        issues.append(f"runtime evidence is stale: {path} changed")
        root_path = str(block.get("root_instance_path", ""))
        if not root_path.startswith("/root/"):
            issues.append("runtime evidence has no live scene-root instance path")
    return issues


def attest_fresh_runtime_response(repo: Repo, spec: dict, runtime: dict,
                                  challenge: str, capture_root: str,
                                  executable_path: str | None = None) -> dict:
    """Verify and snapshot one challenged probe response before deleting output."""
    attestation = fresh_runtime_attestation(
        repo, runtime, challenge, capture_root, executable_path)
    runtime_zones = runtime.get("zones") if isinstance(runtime, dict) else None
    if not isinstance(runtime_zones, dict):
        raise ValueError("fresh runtime response has no zone facts")
    raw_zone = next((
        value for value in spec.get("zones", [])
        if isinstance(value, dict) and value.get("id") in runtime_zones
    ), None)
    if not isinstance(raw_zone, dict):
        raise ValueError("fresh runtime response does not match an audited zone")
    candidate = Repo(repo.root, spec, runtime, attestation)
    issues = _runtime_contract_issues(Zone(raw_zone, candidate))
    if issues:
        raise ValueError("fresh runtime contract rejected: " + "; ".join(issues))
    return attestation


# --------------------------------------------------------------------------
# CHECKS — texture legality and cost
# --------------------------------------------------------------------------

@check("texture.pot_or_small", "texture", "texture_max_side_or_pot")
def _texture_pot(zone: Zone) -> Iterator[Finding]:
    """Every runtime texture is power-of-two or <=1024px on its longest side."""
    art = zone.runtime_art
    if not art:
        yield Finding("texture.pot_or_small", zone.id, SKIP,
                      "zone declares no runtime PNG art")
        return
    cap = zone.budget("texture_max_side", 1024)
    bad = []
    for rel in art:
        info = zone.repo.image(rel)
        if "error" in info:
            yield Finding("texture.pot_or_small", zone.id, WARN,
                          f"unreadable image {rel}: {info['error']}", evidence={"file": rel})
            continue
        if not info["pot"] and max(info["w"], info["h"]) > cap:
            bad.append((rel, info["w"], info["h"]))
    for rel, w, h in bad:
        yield Finding("texture.pot_or_small", zone.id, ERROR,
                      f"{rel} is {w}x{h}: not power-of-two and over {cap}px",
                      evidence={"file": rel, "w": w, "h": h})
    if not bad:
        yield Finding("texture.pot_or_small", zone.id, INFO,
                      f"{len(art)} runtime textures legal", evidence={"count": len(art)})


@check("texture.vram_compressible", "texture", "texture_max_side_or_pot")
def _texture_vram(zone: Zone) -> Iterator[Finding]:
    """Non-power-of-two art is legal but cannot VRAM-compress; track the cost."""
    art = zone.runtime_art
    if not art:
        yield Finding("texture.vram_compressible", zone.id, SKIP, "no runtime PNG art")
        return
    npot = [(r, zone.repo.image(r)) for r in art if not zone.repo.image(r).get("pot", True)]
    uncompressed = sum(i.get("rgba_bytes", 0) for _r, i in npot)
    if not npot:
        yield Finding("texture.vram_compressible", zone.id, INFO,
                      "all runtime textures are power-of-two")
        return
    mb = uncompressed / 1048576.0
    sev = WARN if mb >= 4.0 else INFO
    yield Finding("texture.vram_compressible", zone.id, sev,
                  f"{len(npot)}/{len(art)} textures are non-power-of-two: "
                  f"{mb:.1f} MB that must ship uncompressed on the Mali GPU",
                  evidence={"npot": [r for r, _ in npot], "uncompressed_mb": round(mb, 2)})


@check("texture.import_sidecar", "texture", "texture_max_side_or_pot")
def _texture_sidecar(zone: Zone) -> Iterator[Finding]:
    """Runtime art without a tracked .import has unreviewable compression settings."""
    art = zone.runtime_art
    if not art:
        yield Finding("texture.import_sidecar", zone.id, SKIP, "no runtime PNG art")
        return
    missing = [r for r in art if not zone.repo.exists(r + ".import")]
    if not missing:
        yield Finding("texture.import_sidecar", zone.id, INFO,
                      "every runtime texture pins its import settings")
        return
    yield Finding("texture.import_sidecar", zone.id, WARN,
                  f"{len(missing)}/{len(art)} textures have no tracked .import: compression "
                  f"mode, mipmaps and the NPOT-deadlock setting are unreviewable in-repo",
                  evidence={"missing": missing[:12], "missing_count": len(missing)})


@check("texture.zone_budget", "texture", "texture_max_side_or_pot")
def _texture_budget(zone: Zone) -> Iterator[Finding]:
    """A zone's simultaneous imported texture peak stays inside budget."""
    art = zone.runtime_art
    if not art:
        yield Finding("texture.zone_budget", zone.id, SKIP, "no runtime PNG art")
        return
    declared = set(art)
    base = set(art)
    grouped: set[str] = set()
    choices = []
    for group in zone.texture_peak_alternatives:
        group_id = str(group.get("id", "unnamed"))
        alternatives = []
        group_paths: set[str] = set()
        for alternative in group.get("alternatives", []):
            alternative_id = str(alternative.get("id", "unnamed"))
            paths = zone.repo.expand(alternative.get("files", []))
            expected = int(alternative.get("expected_count", len(paths)))
            if not paths or len(paths) != expected:
                yield Finding("texture.zone_budget", zone.id, ERROR,
                              f"texture peak group '{group_id}/{alternative_id}' resolved "
                              f"{len(paths)} files (expected {expected})",
                              evidence={"group": group_id, "alternative": alternative_id,
                                        "files": paths, "expected_count": expected})
                return
            unknown = set(paths) - declared
            overlap = set(paths) & (grouped | group_paths)
            if unknown or overlap:
                yield Finding("texture.zone_budget", zone.id, ERROR,
                              f"texture peak group '{group_id}/{alternative_id}' has "
                              "undeclared or multiply-grouped files",
                              evidence={"unknown": sorted(unknown),
                                        "overlap": sorted(overlap)})
                return
            alternatives.append({"id": alternative_id, "paths": paths})
            group_paths.update(paths)
        if not alternatives:
            yield Finding("texture.zone_budget", zone.id, ERROR,
                          f"texture peak group '{group_id}' declares no alternatives")
            return
        grouped.update(group_paths)
        base.difference_update(group_paths)
        selected = max(
            alternatives,
            key=lambda alternative: sum(
                zone.repo.texture_vram_bytes(path) for path in alternative["paths"]),
        )
        choices.append({"group": group_id, **selected})

    peak_paths = set(base)
    for choice in choices:
        peak_paths.update(choice["paths"])
    decoded_bytes = sum(
        int(zone.repo.image(rel).get("rgba_bytes", 0)) for rel in peak_paths)
    vram_bytes = sum(zone.repo.texture_vram_bytes(rel) for rel in peak_paths)
    decoded = decoded_bytes / 1048576.0
    vram = vram_bytes / 1048576.0
    cap = float(zone.budget("zone_runtime_texture_mb", 24.0))
    sev = ERROR if vram > cap * 1.5 else (WARN if vram > cap else INFO)
    yield Finding("texture.zone_budget", zone.id, sev,
                  f"simultaneous runtime art peaks at ~{vram:.1f} MB of VRAM on the M11 "
                  f"({decoded:.1f} MB decoded, budget {cap:.0f} MB)",
                  evidence={"vram_mb": round(vram, 2), "decoded_mb": round(decoded, 2),
                            "budget_mb": cap, "files": len(art),
                            "peak_files": len(peak_paths),
                            "alternatives": [{"group": choice["group"],
                                              "selected": choice["id"],
                                              "files": choice["paths"]}
                                             for choice in choices]})


# --------------------------------------------------------------------------
# CHECKS — the layering rule (the heart of the redesign)
# --------------------------------------------------------------------------

@check("layering.legacy_3d_debt", "layering", "layering_rule")
def _legacy_3d_debt(zone: Zone) -> Iterator[Finding]:
    """Require the declared fixed-view medium, preserving legacy inventory."""
    if zone.lifecycle != "active_shipped":
        yield Finding(
            "layering.legacy_3d_debt", zone.id, INFO,
            "fixed-view staging is outside the active shipped lifecycle",
            disposition=NOT_APPLICABLE,
        )
        return
    source = builder_stage_evidence(zone)
    if source["backend"] == "missing":
        yield Finding(
            "layering.legacy_3d_debt", zone.id, SKIP,
            "active surface has no readable declared builder source, so game-wide "
            "fixed-view staging cannot be confirmed",
            evidence=source,
        )
        return
    if source["backend"] == "unknown":
        yield Finding(
            "layering.legacy_3d_debt", zone.id, SKIP,
            "active builder has neither Sprite3D nor registered Canvas exception "
            "evidence; the fixed-view source gate cannot confirm it",
            evidence=source,
        )
        return
    if source["backend"] == "sprite3d_25d":
        yield Finding(
            "layering.legacy_3d_debt", zone.id, INFO,
            "active builder source contains fixed-view Sprite3D staging",
            evidence=source,
        )
        return
    if source["backend"] == "canvas_2d":
        yield Finding(
            "layering.legacy_3d_debt", zone.id, WARN,
            "active builder still uses Canvas staging; migrate world cards to "
            "Sprite3D or register a scoped Canvas exception",
            evidence=source,
            disposition=REVIEW_OPEN,
        )
        return
    yield Finding(
        "layering.legacy_3d_debt", zone.id, ERROR,
        "active surface contains forbidden model/mesh/physics staging; remove it "
        "before the fixed-view 2.5D audit can close",
        evidence={"presentation": zone.presentation, "source": source,
                  "target_presentation": zone.raw.get("target_presentation", "canvas")},
    )


@check("layering.mural_is_a_stack", "layering", "mural_layer_stack",
       presentations=PARALLAX_PRESENTATIONS)
def _mural_stack(zone: Zone) -> Iterator[Finding]:
    """A promenade proves distinct, instantiated Canvas layers in motion."""
    need = int(zone.budget("mural_min_layers", 2))
    if not isinstance(zone.canvas_layers, list) or not zone.canvas_layers:
        yield Finding(
            "layering.mural_is_a_stack", zone.id, SKIP,
            "zone declares no canvas_layers contract; filenames and tile counts "
            "cannot prove independent runtime layers",
        )
        return
    declared = zone.resolved_canvas_layers()
    ids = [row["id"] for row in declared]
    declaration_issues: list[str] = []
    stack_declared = [row for row in declared if row["stack_evidence"]]
    if len(stack_declared) < need:
        declaration_issues.append(
            f"declares {len(stack_declared)} Canvas stack-evidence layer(s); "
            f"requires at least {need}")
    if any(not layer_id for layer_id in ids):
        declaration_issues.append("every Canvas layer needs a non-empty stable id")
    duplicate_ids = sorted({layer_id for layer_id in ids if ids.count(layer_id) > 1})
    if duplicate_ids:
        declaration_issues.append(f"duplicate layer ids: {duplicate_ids}")
    invalid_asset_match = [row["id"] or "<unnamed>" for row in declared
                           if row["asset_match"] not in {"exact", "contains", "dynamic"}]
    if invalid_asset_match:
        declaration_issues.append(
            f"declared layers use an invalid asset_match: {invalid_asset_match}")
    invalid_z_ranges = [
        row["id"] or "<unnamed>" for row in declared
        if not isinstance(row["relative_z_range"], list)
        or len(row["relative_z_range"]) != 2
        or any(not isinstance(value, int) or isinstance(value, bool)
               for value in row["relative_z_range"])
        or (isinstance(row["relative_z_range"], list)
            and len(row["relative_z_range"]) == 2
            and all(isinstance(value, int) and not isinstance(value, bool)
                    for value in row["relative_z_range"])
            and row["relative_z_range"][0] > row["relative_z_range"][1])
    ]
    if invalid_z_ranges:
        declaration_issues.append(
            f"declared layers use an invalid relative_z_range: {invalid_z_ranges}")
    missing_assets = [row["id"] or "<unnamed>" for row in declared
                      if row["required_content"] and not row["assets"]
                      and row["asset_match"] != "dynamic"]
    if missing_assets:
        declaration_issues.append(
            f"declared layers resolve no source assets: {missing_assets}")
    asset_owners: dict[str, list[str]] = {}
    for row in declared:
        for path in row["assets"]:
            asset_owners.setdefault(path, []).append(row["id"] or "<unnamed>")
    shared_assets = {
        path: owners for path, owners in asset_owners.items() if len(set(owners)) > 1
    }
    if shared_assets:
        declaration_issues.append(
            "multiple declared layers reuse the same source pixels")
    declared_signatures = [row["content_signature"] for row in declared
                           if row["content_signature"]]
    duplicate_declared_signatures = sorted({
        signature for signature in declared_signatures
        if declared_signatures.count(signature) > 1
    })
    if duplicate_declared_signatures:
        declaration_issues.append(
            "multiple declared layers have canonically identical decoded visible pixels")
    if declaration_issues:
        yield Finding(
            "layering.mural_is_a_stack", zone.id, ERROR,
            "; ".join(declaration_issues),
            evidence={
                "evidence_class": "declared_canvas_layer_contract",
                "declared_layers": declared,
                "shared_assets": shared_assets,
                "duplicate_content_signatures": duplicate_declared_signatures,
                "minimum_layers": need,
            },
        )
        return

    facts = zone.runtime_facts()
    runtime = facts.get("canvas_parallax") if isinstance(facts, dict) else None
    if not isinstance(runtime, dict):
        if isinstance(facts, dict) and int(facts.get("sprite3d_visible", 0)) > 0:
            yield Finding(
                "layering.mural_is_a_stack", zone.id, ERROR,
                "runtime facts contain visible Sprite3D staging and no Canvas layer "
                "capture; 3D depth cannot satisfy the 2D layer contract",
                evidence={"evidence_class": "legacy_runtime_debt",
                          "sprite3d_visible": facts.get("sprite3d_visible")},
            )
        else:
            yield Finding(
                "layering.mural_is_a_stack", zone.id, SKIP,
                "declared layers need runtime Canvas evidence; run "
                "scripts/probe_visual_audit.gd",
                evidence={"declared_layers": ids},
            )
        return

    provenance_issues = _runtime_contract_issues(zone, runtime)
    if provenance_issues:
        yield Finding(
            "layering.mural_is_a_stack", zone.id, SKIP,
            "; ".join(provenance_issues),
            evidence={"evidence_class": "bound_live_canvas_capture",
                      "runtime": runtime},
        )
        return

    if runtime.get("backend") != "canvas_2d":
        yield Finding(
            "layering.mural_is_a_stack", zone.id, ERROR,
            f"runtime layer backend is '{runtime.get('backend', 'unknown')}', not "
            "Canvas 2D; SideScrollStage/Sprite3D evidence is rejected",
            evidence=runtime,
        )
        return
    if runtime.get("root_canvas_item") is not True \
            or int(runtime.get("non_canvas_spatial_nodes", 0)) > 0:
        yield Finding(
            "layering.mural_is_a_stack", zone.id, ERROR,
            "runtime layer capture is not a pure Canvas subtree",
            evidence=runtime,
        )
        return
    runtime_layers = runtime.get("layers")
    if not isinstance(runtime_layers, list):
        yield Finding(
            "layering.mural_is_a_stack", zone.id, SKIP,
            "runtime Canvas capture has no auditable layers list",
            evidence=runtime,
        )
        return

    runtime_ids = [str(row.get("id", "")) for row in runtime_layers
                   if isinstance(row, dict)]
    issues: list[str] = []
    evidence_gaps: list[str] = []
    duplicate_runtime_ids = sorted({layer_id for layer_id in runtime_ids
                                    if runtime_ids.count(layer_id) > 1})
    if duplicate_runtime_ids:
        issues.append(f"runtime duplicated ids: {duplicate_runtime_ids}")
    missing_ids = sorted(set(ids) - set(runtime_ids))
    extra_ids = sorted(set(runtime_ids) - set(ids))
    if missing_ids:
        issues.append(f"declared layers not instantiated: {missing_ids}")
    if extra_ids:
        issues.append(f"runtime layers lack declarations: {extra_ids}")
    instance_paths: list[str] = []
    signatures: list[str] = []
    painted_signatures: list[str] = []
    movements: list[float] = []
    draw_orders: list[float] = []
    default_min_coverage = float(
        zone.budget("canvas_layer_min_coverage_ratio", 0.50))
    by_id = {row["id"]: row for row in declared}
    for value in runtime_layers:
        if not isinstance(value, dict):
            issues.append("runtime layers list contains a non-object entry")
            continue
        layer_id = str(value.get("id", ""))
        instance_path = str(value.get("instance_path", ""))
        signature = str(value.get("content_signature", ""))
        painted_signature = str(value.get("painted_composite_signature", ""))
        instance_paths.append(instance_path)
        node_type = str(value.get("node_type", ""))
        if value.get("instantiated") is not True or value.get("visible") is not True:
            issues.append(f"{layer_id or '<unnamed>'} is not visibly instantiated")
        if value.get("canvas_item") is not True or "3D" in node_type \
                or int(value.get("non_canvas_spatial_descendants", 0)) > 0:
            issues.append(f"{layer_id or '<unnamed>'} is not a pure Canvas layer")
        if not instance_path:
            issues.append(f"{layer_id or '<unnamed>'} has no runtime instance path")
        declared_row = by_id.get(layer_id)
        required_content = bool(declared_row.get("required_content", True)) \
            if declared_row is not None else True
        stack_evidence = bool(declared_row.get("stack_evidence", True)) \
            if declared_row is not None else True
        if required_content and not signature:
            issues.append(f"{layer_id or '<unnamed>'} has no content signature")
        if value.get("painted_composite_method") != CANVAS_COMPOSITE_SIGNATURE_METHOD \
                or re.fullmatch(r"[0-9a-f]{64}", painted_signature) is None:
            issues.append(
                f"{layer_id or '<unnamed>'} has no canonical painted-composite signature")
        runtime_assets = sorted(set(str(path) for path in value.get("assets", [])
                                    if isinstance(path, str)))
        if declared_row is not None:
            asset_match = declared_row["asset_match"]
            if asset_match == "exact" and runtime_assets != declared_row["assets"]:
                issues.append(f"{layer_id} runtime assets do not match its declaration")
            elif asset_match == "contains" \
                    and not set(declared_row["assets"]).issubset(runtime_assets):
                issues.append(f"{layer_id} runtime assets omit required declared assets")
            if asset_match == "exact" \
                    and signature != declared_row["content_signature"]:
                issues.append(f"{layer_id} runtime content signature is not reproducible")
            expected_factor = declared_row.get("parallax_factor")
            runtime_factor = value.get("parallax_factor")
            if expected_factor is not None and (
                    not isinstance(runtime_factor, (int, float))
                    or isinstance(runtime_factor, bool)
                    or not math.isfinite(float(runtime_factor))
                    or not math.isclose(float(runtime_factor),
                                        float(expected_factor), abs_tol=0.0001)):
                issues.append(f"{layer_id} has the wrong runtime parallax factor")
            expected_z_range = declared_row["relative_z_range"]
            allowed_z_min = value.get("allowed_relative_z_min")
            allowed_z_max = value.get("allowed_relative_z_max")
            relative_z_min = value.get("relative_z_min")
            relative_z_max = value.get("relative_z_max")
            z_values = (allowed_z_min, allowed_z_max,
                        relative_z_min, relative_z_max)
            if any(not isinstance(item, int) or isinstance(item, bool)
                   for item in z_values):
                issues.append(f"{layer_id} lacks an exact descendant z-band audit")
            elif [allowed_z_min, allowed_z_max] != expected_z_range:
                issues.append(f"{layer_id} runtime z band differs from its declaration")
            elif relative_z_min < expected_z_range[0] \
                    or relative_z_max > expected_z_range[1]:
                issues.append(f"{layer_id} has a visual outside its declared z band")
        if value.get("coverage_method") != CANVAS_COVERAGE_METHOD:
            issues.append(f"{layer_id or '<unnamed>'} lacks painted-pixel coverage evidence")
        unresolved = value.get("unresolved_alpha_effects")
        if not isinstance(unresolved, int) or isinstance(unresolved, bool) \
                or unresolved < 0:
            evidence_gaps.append(
                f"{layer_id or '<unnamed>'} lacks an effective-alpha effects audit")
        elif unresolved > 0:
            evidence_gaps.append(
                f"{layer_id or '<unnamed>'} has {unresolved} material, CanvasGroup, "
                "or unresolved clip effect(s); source alpha cannot prove rendered coverage")
        unresolved_draw = value.get("unresolved_draw_order_effects")
        if not isinstance(unresolved_draw, int) or isinstance(unresolved_draw, bool) \
                or unresolved_draw < 0:
            evidence_gaps.append(
                f"{layer_id or '<unnamed>'} lacks a descendant draw-order audit")
        elif unresolved_draw > 0:
            evidence_gaps.append(
                f"{layer_id or '<unnamed>'} has {unresolved_draw} contributing visual(s) "
                "whose effective order differs from the tagged layer or uses ambiguous "
                "Canvas ordering")
        coverage = value.get("screen_coverage_ratio")
        configured_min = declared_row.get("minimum_coverage_ratio") \
            if declared_row is not None else None
        min_coverage = default_min_coverage if configured_min is None \
            else float(configured_min)
        if not isinstance(coverage, (int, float)) or not math.isfinite(float(coverage)):
            issues.append(f"{layer_id or '<unnamed>'} has no measured screen coverage")
        elif float(coverage) < min_coverage:
            issues.append(
                f"{layer_id or '<unnamed>'} covers {float(coverage):.1%}; "
                f"requires at least {min_coverage:.0%}")
        movement = value.get("screen_delta_px")
        if not isinstance(movement, (int, float)) or not math.isfinite(float(movement)):
            issues.append(f"{layer_id or '<unnamed>'} has no measured camera response")
        else:
            if stack_evidence:
                movements.append(float(movement))
        draw_order = value.get("draw_order")
        if value.get("draw_order_method") != CANVAS_DRAW_ORDER_METHOD \
                or not isinstance(draw_order, (int, float)) \
                or isinstance(draw_order, bool) \
                or not math.isfinite(float(draw_order)):
            issues.append(f"{layer_id or '<unnamed>'} has no measured Canvas draw order")
        else:
            if stack_evidence:
                draw_orders.append(float(draw_order))
        if signature:
            signatures.append(signature)
        if stack_evidence and painted_signature:
            painted_signatures.append(painted_signature)
    duplicate_paths = sorted({path for path in instance_paths
                              if path and instance_paths.count(path) > 1})
    duplicate_signatures = sorted({sig for sig in signatures
                                   if sig and signatures.count(sig) > 1})
    duplicate_painted_signatures = sorted({sig for sig in painted_signatures
                                           if sig and painted_signatures.count(sig) > 1})
    if duplicate_paths:
        issues.append(f"layers share runtime instances: {duplicate_paths}")
    if duplicate_signatures:
        issues.append("layers duplicate the same runtime content signature")
    if duplicate_painted_signatures:
        issues.append("layers paint the same canonical viewport composite")

    camera_sample = runtime.get("camera_sample_px")
    min_sample = float(zone.budget("canvas_layer_min_camera_sample_px", 120.0))
    evidence_gap = None
    if runtime.get("motion_method") != CANVAS_MOTION_METHOD:
        evidence_gap = "camera response is not measured from the viewport Canvas transform"
    elif not isinstance(camera_sample, (int, float)) \
            or not math.isfinite(float(camera_sample)) \
            or abs(float(camera_sample)) < min_sample:
        evidence_gap = (
            f"camera sample is too small or missing (need at least {min_sample:.0f}px)")
    if evidence_gap is not None:
        evidence_gaps.append(evidence_gap)
    differential = max(movements) - min(movements) if len(movements) >= 2 else 0.0
    min_differential = float(zone.budget("canvas_layer_min_differential_px", 8.0))
    if len(movements) >= need and differential < min_differential:
        issues.append(
            f"layer motion differs by only {differential:.1f}px; requires at least "
            f"{min_differential:.1f}px over the camera sample")
    draw_spread = max(draw_orders) - min(draw_orders) if len(draw_orders) >= 2 else 0.0
    min_draw_spread = float(zone.budget("canvas_layer_min_z_index_spread", 1.0))
    if len(draw_orders) >= need and draw_spread < min_draw_spread:
        issues.append(
            f"Canvas draw order differs by only {draw_spread:.1f}; requires at least "
            f"{min_draw_spread:.1f} so layers do not collapse into equal z_index")

    if evidence_gaps:
        yield Finding(
            "layering.mural_is_a_stack", zone.id, SKIP,
            "; ".join(dict.fromkeys(evidence_gaps)),
            evidence=runtime,
        )
        return
    if issues:
        yield Finding(
            "layering.mural_is_a_stack", zone.id, ERROR,
            "; ".join(issues),
            evidence={"runtime": runtime, "differential_px": differential,
                      "minimum_differential_px": min_differential,
                      "draw_order_spread": draw_spread,
                      "minimum_draw_order_spread": min_draw_spread},
        )
        return
    yield Finding(
        "layering.mural_is_a_stack", zone.id, INFO,
        f"{len(runtime_layers)} registered Canvas holders include "
        f"{len(stack_declared)} stack-evidence layers and differ "
        f"by {differential:.1f}px over a {abs(float(camera_sample)):.0f}px effective "
        f"camera sample with {draw_spread:.1f} draw-order spread",
        evidence={"runtime": runtime, "differential_px": differential,
                  "draw_order_spread": draw_spread},
    )


@check("layering.engine_layer_api", "layering", "mural_layer_stack",
       presentations=PARALLAX_PRESENTATIONS)
def _engine_layers(zone: Zone) -> Iterator[Finding]:
    """A panning stage's builder is Canvas-based and contains no 3D staging."""
    if not zone.builders:
        yield Finding("layering.engine_layer_api", zone.id, SKIP, "zone declares no builder")
        return
    evidence = builder_stage_evidence(zone)
    if evidence["backend"] == "missing":
        yield Finding("layering.engine_layer_api", zone.id, SKIP, "builder sources unreadable")
        return
    if evidence["backend"] == "legacy_3d":
        yield Finding(
            "layering.engine_layer_api", zone.id, ERROR,
            "builder still reaches canonical spatial stage/resource/API debt; it "
            "cannot satisfy the Canvas 2D contract",
            evidence=evidence,
        )
        return
    # A Node2D/CanvasItem token can live in a never-called branch. Source-token
    # presence is therefore only a rejection aid, never positive evidence. A
    # pass requires the current, hash-bound harness to observe the tagged live
    # Canvas instances and satisfy the complete layer contract.
    live_rows = list(_mural_stack(zone))
    live = live_rows[0] if len(live_rows) == 1 else None
    if live is not None and live.disposition == PASS:
        yield Finding(
            "layering.engine_layer_api", zone.id, INFO,
            "current hash-bound runtime facts prove the declared live Canvas layer "
            "instances; source contains no forbidden 3D stage types",
            evidence={"source": evidence, "runtime": live.evidence},
        )
        return
    if live is not None and live.disposition == FAIL:
        yield Finding(
            "layering.engine_layer_api", zone.id, ERROR,
            "source has no forbidden 3D type, but current live Canvas layer evidence "
            f"fails: {live.message}",
            evidence={"source": evidence, "runtime": live.evidence},
        )
        return
    yield Finding(
        "layering.engine_layer_api", zone.id, SKIP,
        "Canvas-looking source tokens cannot prove that the current builder "
        "instantiated the declared layers; current bound runtime evidence is missing",
        evidence={"source": evidence,
                  "runtime": live.evidence if live is not None else {}},
    )


@check("layering.depth_spread", "layering", "layering_rule",
       presentations=PARALLAX_PRESENTATIONS)
def _depth_spread(zone: Zone) -> Iterator[Finding]:
    """A panning stage has distinct current live Canvas draw orders."""
    source = builder_stage_evidence(zone)
    if source["backend"] == "legacy_3d":
        yield Finding(
            "layering.depth_spread", zone.id, ERROR,
            "builder exposes 3D stage types; 3D depth is rejected rather than "
            "credited as Canvas draw-order evidence",
            evidence=source,
        )
        return
    facts = zone.runtime_facts()
    runtime = facts.get("canvas_parallax") if isinstance(facts, dict) else None
    if not isinstance(runtime, dict):
        yield Finding("layering.depth_spread", zone.id, SKIP,
                      "needs current live Canvas draw-order facts")
        return
    provenance_issues = _runtime_contract_issues(zone, runtime)
    if provenance_issues:
        yield Finding("layering.depth_spread", zone.id, SKIP,
                      "; ".join(provenance_issues), evidence={"runtime": runtime})
        return
    if runtime.get("backend") != "canvas_2d" \
            or int(runtime.get("non_canvas_spatial_nodes", 0)) != 0:
        yield Finding("layering.depth_spread", zone.id, ERROR,
                      "runtime staging is not a pure Canvas presentation",
                      evidence={"runtime": runtime})
        return
    layers = runtime.get("layers")
    draw_orders: list[float] = []
    if isinstance(layers, list):
        for value in layers:
            if not isinstance(value, dict) \
                    or value.get("draw_order_method") != CANVAS_DRAW_ORDER_METHOD:
                continue
            order = value.get("draw_order")
            if isinstance(order, (int, float)) and not isinstance(order, bool) \
                    and math.isfinite(float(order)):
                draw_orders.append(float(order))
    if len(draw_orders) < 2:
        yield Finding("layering.depth_spread", zone.id, SKIP,
                      "fewer than two bound live Canvas draw orders were measured",
                      evidence={"runtime": runtime})
        return
    spread = max(draw_orders) - min(draw_orders)
    need = float(zone.budget("canvas_layer_min_z_index_spread", 1.0))
    if spread < need:
        yield Finding("layering.depth_spread", zone.id, ERROR,
                      f"live Canvas draw-order spread is {spread:.1f}; requires at "
                      f"least {need:.1f}", evidence={"draw_orders": draw_orders})
        return
    yield Finding("layering.depth_spread", zone.id, INFO,
                  f"live Canvas layers span {spread:.1f} draw-order units",
                  evidence={"draw_orders": draw_orders, "spread": spread})


@check("layering.occlusion_band", "layering", "layering_rule",
       presentations=PARALLAX_PRESENTATIONS)
def _occlusion(zone: Zone) -> Iterator[Finding]:
    """Live Canvas overlap samples put the target both behind and in front."""
    source = builder_stage_evidence(zone)
    if source["backend"] == "legacy_3d":
        yield Finding(
            "layering.occlusion_band", zone.id, ERROR,
            "builder implements occlusion with Node3D/Sprite3D; only Canvas "
            "draw-order evidence can satisfy the 2D contract",
            evidence=source,
        )
        return
    facts = zone.runtime_facts()
    runtime = facts.get("canvas_occlusion") if isinstance(facts, dict) else None
    if not isinstance(runtime, dict):
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "needs live Canvas overlap/draw-order samples")
        return
    provenance_issues = _runtime_contract_issues(zone, runtime)
    if provenance_issues:
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "; ".join(provenance_issues), evidence={"runtime": runtime})
        return
    if runtime.get("backend") != "canvas_2d" \
            or int(runtime.get("non_canvas_spatial_nodes", 0)) != 0:
        yield Finding("layering.occlusion_band", zone.id, ERROR,
                      "runtime occlusion evidence is not from a pure Canvas stage",
                      evidence={"runtime": runtime})
        return
    if runtime.get("method") != CANVAS_OCCLUSION_METHOD:
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "runtime facts lack the live Canvas draw-order sample method",
                      evidence={"runtime": runtime})
        return
    unresolved = runtime.get("unresolved_alpha_effects")
    if not isinstance(unresolved, int) or isinstance(unresolved, bool) \
            or unresolved < 0:
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "runtime facts lack an effective-alpha effects audit",
                      evidence={"runtime": runtime})
        return
    if unresolved > 0:
        yield Finding(
            "layering.occlusion_band", zone.id, SKIP,
            f"{unresolved} Canvas visual(s) use a material, CanvasGroup, or "
            "unresolved clip effect; source alpha cannot prove rendered occlusion",
            evidence={"runtime": runtime},
        )
        return
    unresolved_draw = runtime.get("unresolved_draw_order_effects")
    if not isinstance(unresolved_draw, int) or isinstance(unresolved_draw, bool) \
            or unresolved_draw < 0:
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "runtime facts lack a contributing-visual draw-order audit",
                      evidence={"runtime": runtime})
        return
    if unresolved_draw > 0:
        yield Finding(
            "layering.occlusion_band", zone.id, SKIP,
            f"{unresolved_draw} contributing Canvas visual(s) have unresolved or "
            "mismatched effective draw order",
            evidence={"runtime": runtime},
        )
        return
    samples = runtime.get("samples")
    if not isinstance(samples, list) or not samples:
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "no target has a current live Canvas behind/front overlap sample",
                      evidence={"runtime": runtime})
        return
    root_path = str(runtime.get("root_instance_path", ""))
    issues: list[str] = []
    min_alpha = float(zone.budget("canvas_occlusion_min_effective_alpha", 0.50))
    min_ratio = float(zone.budget("canvas_occlusion_min_target_overlap_ratio", 0.05))
    min_samples = int(zone.budget("canvas_occlusion_min_painted_samples", 4))
    for index, value in enumerate(samples):
        if not isinstance(value, dict):
            issues.append(f"sample {index} is malformed")
            continue
        target_path = str(value.get("target_instance_path", ""))
        target_order = value.get("target_draw_order")
        if not target_path.startswith(root_path + "/"):
            issues.append(f"sample {index} target is outside the live zone root")
        if value.get("target_canvas_item") is not True \
                or value.get("target_visible") is not True:
            issues.append(f"sample {index} target is not a visible Canvas item")
        if not isinstance(target_order, (int, float)) \
                or isinstance(target_order, bool) \
                or not math.isfinite(float(target_order)):
            issues.append(f"sample {index} has no measured target draw order")
            continue
        for side, comparison in (("behind", lambda order: order < float(target_order)),
                                 ("front", lambda order: order > float(target_order))):
            rows = value.get(side)
            if not isinstance(rows, list) or not rows:
                issues.append(f"sample {index} has no overlapping Canvas layer {side}")
                continue
            for row in rows:
                path = str(row.get("instance_path", "")) if isinstance(row, dict) else ""
                order = row.get("draw_order") if isinstance(row, dict) else None
                overlap = row.get("overlap_px2") if isinstance(row, dict) else None
                painted_samples = row.get(
                    "painted_sample_count") if isinstance(row, dict) else None
                target_samples = row.get(
                    "target_painted_sample_count") if isinstance(row, dict) else None
                overlap_ratio = row.get(
                    "target_overlap_ratio") if isinstance(row, dict) else None
                alpha_threshold = row.get(
                    "alpha_threshold") if isinstance(row, dict) else None
                sample_step = row.get("sample_step_px") if isinstance(row, dict) else None
                if not path.startswith(root_path + "/") \
                        or not isinstance(order, (int, float)) \
                        or isinstance(order, bool) \
                        or not comparison(float(order)) \
                        or not isinstance(overlap, (int, float)) \
                        or isinstance(overlap, bool) or float(overlap) <= 0.0 \
                        or row.get("overlap_method") != CANVAS_OCCLUSION_METHOD \
                        or not isinstance(painted_samples, int) \
                        or isinstance(painted_samples, bool) \
                        or painted_samples < min_samples \
                        or not isinstance(target_samples, int) \
                        or isinstance(target_samples, bool) or target_samples < painted_samples \
                        or not isinstance(overlap_ratio, (int, float)) \
                        or isinstance(overlap_ratio, bool) \
                        or not math.isfinite(float(overlap_ratio)) \
                        or float(overlap_ratio) < min_ratio \
                        or not isinstance(alpha_threshold, (int, float)) \
                        or isinstance(alpha_threshold, bool) \
                        or float(alpha_threshold) < min_alpha \
                        or row.get("unresolved_alpha_effects") != 0 \
                        or not isinstance(sample_step, (int, float)) \
                        or isinstance(sample_step, bool) \
                        or not 0.0 < float(sample_step) <= 8.0:
                    issues.append(f"sample {index} has invalid {side} Canvas overlap evidence")
                    break
    if issues:
        yield Finding("layering.occlusion_band", zone.id, ERROR,
                      "; ".join(issues), evidence={"runtime": runtime})
        return
    yield Finding("layering.occlusion_band", zone.id, INFO,
                  f"{len(samples)} live target sample(s) overlap Canvas layers both "
                  "behind and in front", evidence={"runtime": runtime})


@check("layering.standee_alpha", "layering", "standee_not_mural",
       presentations=FLAT_PRESENTATIONS)
def _standee_alpha(zone: Zone) -> Iterator[Finding]:
    """Standees are cutouts: mostly transparent frames, never full-bleed rectangles."""
    if not zone.standees:
        yield Finding("layering.standee_alpha", zone.id, SKIP, "zone declares no standees")
        return
    lo = float(zone.budget("standee_alpha_coverage_min", 0.05))
    hi = float(zone.budget("standee_alpha_coverage_max", 0.90))
    bad = []
    for rel in zone.standees:
        info = zone.repo.image(rel)
        cov = info.get("coverage")
        if cov is None:
            continue
        if cov > hi:
            bad.append((rel, cov, "opaque rectangle — this is a mural, not a standee"))
        elif cov < lo:
            bad.append((rel, cov, "almost nothing painted — will not read at M11 size"))
    for rel, cov, why in bad:
        yield Finding("layering.standee_alpha", zone.id, WARN,
                      f"{os.path.basename(rel)} alpha coverage {cov:.0%}: {why}",
                      evidence={"file": rel, "coverage": round(cov, 3)})
    if not bad:
        yield Finding("layering.standee_alpha", zone.id, INFO,
                      f"{len(zone.standees)} standees inside the {lo:.0%}-{hi:.0%} coverage band")


# --------------------------------------------------------------------------
# CHECKS — palette and readability
# --------------------------------------------------------------------------

def _rendered_provenance_issues(zone: Zone, state: dict) -> list[str]:
    """Validate capture bytes and invalidate evidence after code/art changes."""
    state_id = str(state.get("id", "<unnamed>"))
    issues: list[str] = _runtime_contract_issues(zone, state)
    capture_path = str(state.get("capture_path", ""))
    capture_hash = str(state.get("capture_sha256", ""))
    if not capture_path or not capture_path.lower().endswith(".png"):
        issues.append(f"state '{state_id}' has no flattened PNG capture path")
    elif not zone.repo.capture_exists(capture_path):
        issues.append(f"state '{state_id}' capture does not exist: {capture_path}")
    elif re.fullmatch(r"[0-9a-f]{64}", capture_hash) is None:
        issues.append(f"state '{state_id}' has no valid capture SHA-256")
    elif zone.repo.sha256(capture_path) != capture_hash:
        issues.append(f"state '{state_id}' capture SHA-256 does not match its bytes")

    provenance = state.get("provenance")
    if not isinstance(provenance, dict):
        issues.append(f"state '{state_id}' has no code/art provenance")
        return issues
    for label, expected_paths in (
        ("builder_sha256", sorted(set(zone.builders))),
        ("art_sha256", sorted(set(
            path.replace("\\", "/") for path in zone.murals + zone.foreground))),
    ):
        declared = provenance.get(label)
        if not isinstance(declared, dict):
            issues.append(f"state '{state_id}' has no {label} map")
            continue
        normalized = {str(path).replace("\\", "/"): str(value)
                      for path, value in declared.items()}
        if set(normalized) != set(expected_paths):
            missing = sorted(set(expected_paths) - set(normalized))
            extra = sorted(set(normalized) - set(expected_paths))
            issues.append(
                f"state '{state_id}' {label} scope mismatch "
                f"(missing={missing}, extra={extra})")
            continue
        for path in expected_paths:
            recorded = normalized[path]
            current = zone.repo.sha256(path)
            if re.fullmatch(r"[0-9a-f]{64}", recorded) is None or not current:
                issues.append(f"state '{state_id}' has invalid {label} for {path}")
            elif recorded != current:
                issues.append(f"state '{state_id}' is stale: {path} changed")
    return issues


def _source_alpha_projection(zone: Zone, visual: dict,
                             width: int, height: int) -> tuple[object, dict]:
    """Independently project current source alpha through a strict Canvas binding.

    The probe records live instance metadata, but it does not get to declare the
    silhouette.  This function loads the current source texture and recomputes
    which 1280x720 pixel centres the exact Sprite2D/TextureRect geometry can
    paint.  Singular/offscreen transforms, impossible frame/region coordinates,
    and non-boolean flags are rejected before any capture pixels are considered.
    """
    from PIL import Image
    import numpy as np

    def numbers(raw: object, count: int, label: str,
                *, positive_size: bool = False) -> list[float]:
        if not isinstance(raw, list) or len(raw) != count \
                or any(not isinstance(value, (int, float))
                       or isinstance(value, bool)
                       or not math.isfinite(float(value)) for value in raw):
            raise ValueError(f"{label} is not a finite {count}-value array")
        values = [float(value) for value in raw]
        if positive_size and (values[-2] <= 0.0 or values[-1] <= 0.0):
            raise ValueError(f"{label} has no positive size")
        return values

    def strict_bool(value: object, label: str) -> bool:
        if type(value) is not bool:
            raise ValueError(f"{label} is not boolean")
        return value

    texture_path = str(visual.get("texture_path", "")).replace("\\", "/")
    try:
        with Image.open(zone.repo.path(texture_path)) as image:
            source_rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"source texture is not a readable raster: {texture_path}: {exc}") \
            from exc
    source_h, source_w = source_rgba.shape[:2]
    if source_w <= 0 or source_h <= 0:
        raise ValueError("source texture has no pixels")
    source_alpha = source_rgba[..., 3] >= 128

    local_x, local_y, local_w, local_h = numbers(
        visual.get("local_rect"), 4, "local_rect", positive_size=True)
    a, b, c, d, tx, ty = numbers(
        visual.get("canvas_transform"), 6, "canvas_transform")
    determinant = a * d - b * c
    if abs(determinant) <= 1.0e-8:
        raise ValueError("canvas_transform is singular")
    if max(abs(a), abs(b), abs(c), abs(d)) > 10000.0:
        raise ValueError("canvas_transform scale is implausible")
    corners = [
        (a * x + c * y + tx, b * x + d * y + ty)
        for x, y in ((local_x, local_y), (local_x + local_w, local_y),
                     (local_x + local_w, local_y + local_h),
                     (local_x, local_y + local_h))
    ]
    min_x, max_x = min(x for x, _y in corners), max(x for x, _y in corners)
    min_y, max_y = min(y for _x, y in corners), max(y for _x, y in corners)
    if max_x <= 0.0 or max_y <= 0.0 or min_x >= width or min_y >= height:
        raise ValueError("canvas_transform projects the visual offscreen")
    if max_x - min_x > width * 16.0 or max_y - min_y > height * 16.0:
        raise ValueError("canvas_transform projects an implausibly large visual")

    screen_y, screen_x = np.mgrid[0:height, 0:width].astype(np.float32)
    screen_x += 0.5
    screen_y += 0.5
    relative_x = screen_x - tx
    relative_y = screen_y - ty
    local_px = (d * relative_x - c * relative_y) / determinant
    local_py = (-b * relative_x + a * relative_y) / determinant
    inside_local = ((local_px >= local_x) & (local_px < local_x + local_w)
                    & (local_py >= local_y) & (local_py < local_y + local_h))
    projection = visual.get("projection")
    node_type = str(visual.get("node_type", ""))
    if not isinstance(projection, dict) or projection.get("kind") != node_type:
        raise ValueError("visual projection metadata is missing or has the wrong type")

    source_x = np.zeros((height, width), dtype=np.float32)
    source_y = np.zeros((height, width), dtype=np.float32)
    drawable = inside_local.copy()
    if node_type == "Sprite2D":
        region_enabled = strict_bool(
            projection.get("region_enabled"), "Sprite2D region_enabled")
        flip_h = strict_bool(projection.get("flip_h"), "Sprite2D flip_h")
        flip_v = strict_bool(projection.get("flip_v"), "Sprite2D flip_v")
        centered = strict_bool(projection.get("centered"), "Sprite2D centered")
        region_x, region_y, region_w, region_h = numbers(
            projection.get("region_rect"), 4, "Sprite2D region_rect")
        hframes = projection.get("hframes")
        vframes = projection.get("vframes")
        if not isinstance(hframes, int) or isinstance(hframes, bool) \
                or not isinstance(vframes, int) or isinstance(vframes, bool) \
                or hframes <= 0 or vframes <= 0:
            raise ValueError("Sprite2D frame-grid metadata is invalid")
        frame_values = numbers(
            projection.get("frame_coords"), 2, "Sprite2D frame_coords")
        frame_x, frame_y = (int(round(value)) for value in frame_values)
        if any(abs(raw - rounded) > 1.0e-6
               for raw, rounded in zip(frame_values, (frame_x, frame_y))) \
                or not 0 <= frame_x < hframes or not 0 <= frame_y < vframes:
            raise ValueError("Sprite2D frame coordinates are impossible")
        offset_x, offset_y = numbers(
            projection.get("offset"), 2, "Sprite2D offset")
        if region_enabled:
            if region_w <= 0.0 or region_h <= 0.0 \
                    or region_x < 0.0 or region_y < 0.0 \
                    or region_x + region_w > source_w + 1.0e-6 \
                    or region_y + region_h > source_h + 1.0e-6:
                raise ValueError("Sprite2D region is outside the source texture")
            base_x, base_y, base_w, base_h = (
                region_x, region_y, region_w, region_h)
        else:
            base_x, base_y, base_w, base_h = 0.0, 0.0, float(source_w), float(source_h)
        frame_w, frame_h = base_w / hframes, base_h / vframes
        expected_x = offset_x - frame_w * 0.5 if centered else offset_x
        expected_y = offset_y - frame_h * 0.5 if centered else offset_y
        if max(abs(local_x - expected_x), abs(local_y - expected_y),
               abs(local_w - frame_w), abs(local_h - frame_h)) > 1.0e-4:
            raise ValueError("Sprite2D local_rect does not match source frame geometry")
        u = (local_px - local_x) / local_w
        v = (local_py - local_y) / local_h
        if flip_h:
            u = 1.0 - u
        if flip_v:
            v = 1.0 - v
        source_x = base_x + frame_x * frame_w + u * frame_w
        source_y = base_y + frame_y * frame_h + v * frame_h
    elif node_type == "TextureRect":
        flip_h = strict_bool(projection.get("flip_h"), "TextureRect flip_h")
        flip_v = strict_bool(projection.get("flip_v"), "TextureRect flip_v")
        strict_bool(projection.get("clip_contents"), "TextureRect clip_contents")
        control_w, control_h = numbers(
            projection.get("control_size"), 2, "TextureRect control_size")
        if control_w <= 0.0 or control_h <= 0.0 \
                or max(abs(local_x), abs(local_y), abs(local_w - control_w),
                       abs(local_h - control_h)) > 1.0e-4:
            raise ValueError("TextureRect local_rect does not match its control size")
        stretch = projection.get("stretch_mode")
        expand = projection.get("expand_mode")
        if not isinstance(stretch, int) or isinstance(stretch, bool) \
                or not 0 <= stretch <= 6:
            raise ValueError("TextureRect stretch mode is invalid")
        if not isinstance(expand, int) or isinstance(expand, bool) \
                or not 0 <= expand <= 3:
            raise ValueError("TextureRect expand mode is invalid")
        px = local_px
        py = local_py
        if stretch == 1:  # TILE
            source_x = np.mod(px, float(source_w))
            source_y = np.mod(py, float(source_h))
        else:
            if stretch == 0:  # SCALE
                draw_w, draw_h = control_w, control_h
                draw_x = draw_y = 0.0
            elif stretch in (2, 3):  # KEEP / KEEP_CENTERED
                draw_w, draw_h = float(source_w), float(source_h)
                draw_x = (control_w - draw_w) * 0.5 if stretch == 3 else 0.0
                draw_y = (control_h - draw_h) * 0.5 if stretch == 3 else 0.0
            else:
                scale = (max(control_w / source_w, control_h / source_h)
                         if stretch == 6 else
                         min(control_w / source_w, control_h / source_h))
                draw_w, draw_h = source_w * scale, source_h * scale
                centered_aspect = stretch in (5, 6)
                draw_x = (control_w - draw_w) * 0.5 if centered_aspect else 0.0
                draw_y = (control_h - draw_h) * 0.5 if centered_aspect else 0.0
            drawable &= ((px >= draw_x) & (px < draw_x + draw_w)
                         & (py >= draw_y) & (py < draw_y + draw_h))
            u = (px - draw_x) / draw_w
            v = (py - draw_y) / draw_h
            source_x = u * source_w
            source_y = v * source_h
        if flip_h:
            source_x = source_w - source_x
        if flip_v:
            source_y = source_h - source_y
    else:
        raise ValueError(f"{node_type or 'unknown visual'} is not an accepted Canvas visual")

    sample_x = np.floor(source_x).astype(np.int64)
    sample_y = np.floor(source_y).astype(np.int64)
    drawable &= ((sample_x >= 0) & (sample_x < source_w)
                 & (sample_y >= 0) & (sample_y < source_h))
    out = np.zeros((height, width), dtype=bool)
    indices_y, indices_x = np.nonzero(drawable)
    out[indices_y, indices_x] = source_alpha[
        sample_y[indices_y, indices_x], sample_x[indices_y, indices_x]]
    return out, {
        "instance_path": str(visual.get("instance_path", "")),
        "texture_path": texture_path,
        "source_size": [source_w, source_h],
        "projected_pixels": int(np.count_nonzero(out)),
        "screen_bounds": [round(min_x, 3), round(min_y, 3),
                          round(max_x - min_x, 3), round(max_y - min_y, 3)],
    }


def _rendered_sample_metrics(zone: Zone, state: dict, sample: dict) -> tuple[dict, str]:
    """Recompute the target silhouette from full and target-hidden captures."""
    try:
        from PIL import Image
        import numpy as np

        def png_bytes(path_value: object, hash_value: object,
                      label: str) -> tuple[object, str]:
            path = str(path_value)
            recorded = str(hash_value)
            if not path or not path.lower().endswith(".png"):
                raise ValueError(f"{label} has no PNG path")
            if not zone.repo.capture_exists(path):
                raise ValueError(f"{label} does not exist: {path}")
            if re.fullmatch(r"[0-9a-f]{64}", recorded) is None \
                    or zone.repo.sha256(path) != recorded:
                raise ValueError(f"{label} SHA-256 does not match its bytes")
            with zone.repo.open_image(path) as image:
                return np.asarray(image.convert("RGBA"), dtype=np.uint8), path

        capture_rgba, _capture_path = png_bytes(
            state.get("capture_path"), state.get("capture_sha256"),
            "flattened capture")
        hidden_rgba, hidden_path = png_bytes(
            sample.get("target_hidden_capture_path"),
            sample.get("target_hidden_capture_sha256"),
            "target-hidden capture")
        restored_rgba, restored_path = png_bytes(
            sample.get("target_restored_capture_path"),
            sample.get("target_restored_capture_sha256"),
            "target-restored capture")
        def stability_captures(raw: object, label: str) -> list[object]:
            if not isinstance(raw, list) or len(raw) != 2:
                raise ValueError(f"{label} needs exactly two asymmetric-cadence captures")
            images: list[object] = []
            for index, value in enumerate(raw):
                if not isinstance(value, dict):
                    raise ValueError(f"{label} capture {index} is malformed")
                image, _path = png_bytes(
                    value.get("path"), value.get("sha256"),
                    f"{label} capture {index}")
                images.append(image)
            return images
        hidden_stability = stability_captures(
            sample.get("target_hidden_stability_captures"), "target-hidden stability")
        visible_stability = stability_captures(
            sample.get("target_visible_stability_captures"), "target-visible stability")
        mask_rgba, mask_path = png_bytes(
            sample.get("mask_path"), sample.get("mask_sha256"), "target mask")
        all_captures = [hidden_rgba, restored_rgba, mask_rgba,
                        *hidden_stability, *visible_stability]
        if any(capture_rgba.shape != image.shape for image in all_captures):
            raise ValueError(
                "flattened, temporal target, and mask captures have "
                "different dimensions")
        height, width = capture_rgba.shape[:2]

        if sample.get("mask_source") != RENDERED_DIFF_METHOD:
            raise ValueError(
                "target mask is not derived from an exact target-hidden viewport capture")
        if sample.get("target_hidden_source") != "viewport_composite_target_hidden":
            raise ValueError("target-hidden pixels are not declared as a viewport composite")
        if sample.get("target_restored_source") != "viewport_composite_target_restored":
            raise ValueError("target-restored pixels are not declared as a viewport composite")
        if sample.get("temporal_schedule_frames") != [1, 2, 1, 3, 2, 1]:
            raise ValueError("target capture lacks the required asymmetric temporal schedule")
        if sample.get("temporal_freeze_method") != TEMPORAL_FREEZE_METHOD \
                or sample.get("shader_time_scale") != 0.0:
            raise ValueError("target capture did not freeze shader TIME during alternation")
        if not all(np.array_equal(capture_rgba, value)
                   for value in [restored_rgba, *visible_stability]):
            mismatch = max(int(np.count_nonzero(np.any(
                capture_rgba != value, axis=2)))
                for value in [restored_rgba, *visible_stability])
            raise ValueError(
                f"visible frames are temporally unstable at up to {mismatch} pixel(s)")
        if not all(np.array_equal(hidden_rgba, value) for value in hidden_stability):
            mismatch = max(int(np.count_nonzero(np.any(
                hidden_rgba != value, axis=2))) for value in hidden_stability)
            raise ValueError(
                f"target-hidden frames are temporally unstable at up to {mismatch} pixel(s)")
        target_path = str(sample.get("target_instance_path", ""))
        root_path = str(state.get("root_instance_path", ""))
        if not root_path.startswith("/root/") \
                or not target_path.startswith(root_path + "/"):
            raise ValueError("sample target instance is outside its bound live zone root")
        if sample.get("projection_method") != SOURCE_PROJECTION_METHOD:
            raise ValueError("sample lacks independent source-alpha projection evidence")

        visuals = sample.get("visuals")
        if not isinstance(visuals, list) or not visuals:
            raise ValueError("sample has no bound live visual instances")
        visual_paths: list[str] = []
        visual_art: list[str] = []
        projected_mask = np.zeros((height, width), dtype=bool)
        projection_evidence: list[dict] = []
        allowed_art = {path.replace("\\", "/") for path in zone.foreground}

        def numeric_list(raw: object, count: int, label: str,
                         *, positive_size: bool = False) -> list[float]:
            if not isinstance(raw, list) or len(raw) != count \
                    or any(not isinstance(value, (int, float))
                           or isinstance(value, bool)
                           or not math.isfinite(float(value)) for value in raw):
                raise ValueError(f"{label} is not a finite {count}-value array")
            values = [float(value) for value in raw]
            if positive_size and (values[-2] <= 0.0 or values[-1] <= 0.0):
                raise ValueError(f"{label} has no positive size")
            return values

        for visual in visuals:
            if not isinstance(visual, dict):
                raise ValueError("visual binding contains a non-object entry")
            instance_path = str(visual.get("instance_path", ""))
            if not instance_path or not (instance_path == target_path
                                         or instance_path.startswith(target_path + "/")):
                raise ValueError("visual instance is not bound beneath its target instance")
            if instance_path in visual_paths:
                raise ValueError("visual instance path is duplicated")
            visual_paths.append(instance_path)
            node_type = str(visual.get("node_type", ""))
            if node_type not in {"Sprite2D", "TextureRect"}:
                raise ValueError(f"{node_type or 'unknown visual'} is not an accepted Canvas visual")
            if visual.get("visible_in_tree") is not True:
                raise ValueError("hidden visual instance cannot establish a target silhouette")
            texture_path = str(visual.get("texture_path", "")).replace("\\", "/")
            texture_hash = str(visual.get("texture_sha256", ""))
            if texture_path not in allowed_art:
                raise ValueError("visual texture is outside the declared foreground")
            if re.fullmatch(r"[0-9a-f]{64}", texture_hash) is None \
                    or zone.repo.sha256(texture_path) != texture_hash:
                raise ValueError("visual texture hash is missing or stale")
            visual_art.append(texture_path)
            numeric_list(visual.get("canvas_transform"), 6, "canvas_transform")
            numeric_list(visual.get("local_rect"), 4, "local_rect", positive_size=True)
            projection = visual.get("projection")
            if not isinstance(projection, dict) or projection.get("kind") != node_type:
                raise ValueError("visual projection metadata is missing or has the wrong type")
            if node_type == "Sprite2D":
                required_projection = {
                    "kind", "region_enabled", "region_rect", "hframes", "vframes",
                    "frame_coords", "flip_h", "flip_v", "centered", "offset",
                }
                if not required_projection.issubset(projection):
                    raise ValueError("Sprite2D region/frame/flip projection metadata is incomplete")
                numeric_list(projection.get("region_rect"), 4, "Sprite2D region_rect")
                numeric_list(projection.get("frame_coords"), 2, "Sprite2D frame_coords")
                numeric_list(projection.get("offset"), 2, "Sprite2D offset")
                if not isinstance(projection.get("hframes"), int) \
                        or not isinstance(projection.get("vframes"), int) \
                        or int(projection["hframes"]) <= 0 \
                        or int(projection["vframes"]) <= 0:
                    raise ValueError("Sprite2D frame-grid metadata is invalid")
            else:
                required_projection = {
                    "kind", "stretch_mode", "expand_mode", "flip_h", "flip_v",
                    "control_size", "clip_contents",
                }
                if not required_projection.issubset(projection):
                    raise ValueError("TextureRect stretch/crop projection metadata is incomplete")
                numeric_list(projection.get("control_size"), 2, "TextureRect control_size")
                if not isinstance(projection.get("stretch_mode"), int) \
                        or not 0 <= int(projection["stretch_mode"]) <= 6:
                    raise ValueError("TextureRect stretch mode is invalid")
            visual_projection, visual_projection_evidence = _source_alpha_projection(
                zone, visual, width, height)
            projected_mask |= visual_projection
            projection_evidence.append(visual_projection_evidence)

        source_value = sample.get("mask_source_art", [])
        if isinstance(source_value, str):
            source_art = [source_value.replace("\\", "/")]
        elif isinstance(source_value, list):
            source_art = sorted(set(
                str(path).replace("\\", "/") for path in source_value if str(path)))
        else:
            source_art = []
        if source_art != sorted(set(visual_art)):
            raise ValueError("target-mask art does not match its bound live visual textures")
        source_hash_value = sample.get("mask_source_sha256", {})
        if not isinstance(source_hash_value, dict):
            raise ValueError("target mask source-art hash scope is incomplete")
        source_hashes = {str(path).replace("\\", "/"): str(value)
                         for path, value in source_hash_value.items()}
        if set(source_hashes) != set(source_art):
            raise ValueError("target mask source-art hash scope is incomplete")
        for path in source_art:
            if re.fullmatch(r"[0-9a-f]{64}", source_hashes[path]) is None \
                    or zone.repo.sha256(path) != source_hashes[path]:
                raise ValueError("target mask source-art hash is missing or stale")

        # This is the authoritative silhouette: the exact pixels changed when
        # the bound live target visuals alone were hidden in a frozen scene.
        expected_mask = np.any(capture_rgba != hidden_rgba, axis=2)
        alpha = mask_rgba[..., 3]
        if int(alpha.min()) != int(alpha.max()):
            target_mask = alpha >= 128
        else:
            target_mask = np.any(mask_rgba[..., :3] >= 128, axis=2)
        if not np.array_equal(target_mask, expected_mask):
            mismatch = int(np.count_nonzero(target_mask != expected_mask))
            raise ValueError(
                f"target mask differs from the bound target-hidden composite at "
                f"{mismatch} pixel(s)")
        ys, xs = np.nonzero(target_mask)
        if xs.size == 0:
            raise ValueError("hiding the bound target changes no rendered pixels")
        if xs.size >= width * height * 0.80:
            raise ValueError("target mask implausibly selects most of the viewport")
        projected_pixels = int(np.count_nonzero(projected_mask))
        if projected_pixels == 0:
            raise ValueError("current source alpha projects no visible target pixels")

        def shifted(mask: object, dy: int, dx: int) -> object:
            out = np.zeros_like(mask)
            src_y0, src_y1 = max(0, -dy), min(height, height - dy)
            src_x0, src_x1 = max(0, -dx), min(width, width - dx)
            dst_y0, dst_y1 = max(0, dy), min(height, height + dy)
            dst_x0, dst_x1 = max(0, dx), min(width, width + dx)
            out[dst_y0:dst_y1, dst_x0:dst_x1] = mask[src_y0:src_y1,
                                                             src_x0:src_x1]
            return out

        def dilated_by(mask: object, radius: int) -> object:
            out = mask.copy()
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy > radius * radius:
                        continue
                    src_y0, src_y1 = max(0, -dy), min(height, height - dy)
                    src_x0, src_x1 = max(0, -dx), min(width, width - dx)
                    dst_y0, dst_y1 = max(0, dy), min(height, height + dy)
                    dst_x0, dst_x1 = max(0, dx), min(width, width + dx)
                    out[dst_y0:dst_y1, dst_x0:dst_x1] |= mask[
                        src_y0:src_y1, src_x0:src_x1]
            return out

        projection_tolerance = 2
        projected_near = dilated_by(projected_mask, projection_tolerance)
        difference_near = dilated_by(target_mask, projection_tolerance)
        projection_precision = float(np.count_nonzero(target_mask & projected_near)) \
            / float(xs.size)
        projection_visible_fraction = float(np.count_nonzero(
            projected_mask & difference_near)) / float(projected_pixels)
        def boundary_of(mask: object) -> object:
            eroded_mask = mask.copy()
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1),
                           (-1, -1), (-1, 1), (1, -1), (1, 1)):
                eroded_mask &= shifted(mask, dy, dx)
            return mask & ~eroded_mask

        projected_boundary = boundary_of(projected_mask)
        difference_boundary = boundary_of(target_mask)
        projected_boundary_near = dilated_by(projected_boundary, projection_tolerance)
        difference_boundary_near = dilated_by(difference_boundary, projection_tolerance)
        difference_boundary_pixels = int(np.count_nonzero(difference_boundary))
        projected_boundary_pixels = int(np.count_nonzero(projected_boundary))
        projection_contour_precision = float(np.count_nonzero(
            difference_boundary & projected_boundary_near)) \
            / float(max(1, difference_boundary_pixels))
        projection_contour_recall = float(np.count_nonzero(
            projected_boundary & difference_boundary_near)) \
            / float(max(1, projected_boundary_pixels))
        precision_need = float(zone.budget(
            "rendered_projection_precision_min", 0.90))
        visible_need = float(zone.budget(
            "rendered_projection_visible_fraction_min", 0.35))
        contour_precision_need = float(zone.budget(
            "rendered_projection_contour_precision_min", 0.20))
        contour_recall_need = float(zone.budget(
            "rendered_projection_contour_recall_min", 0.20))
        if projection_precision < precision_need:
            raise ValueError(
                f"target-hidden difference precision against current source-alpha "
                f"projection is {projection_precision:.3f}; requires {precision_need:.3f}")
        if projection_visible_fraction < visible_need:
            raise ValueError(
                f"only {projection_visible_fraction:.3f} of the current source-alpha "
                f"projection is causally visible; requires {visible_need:.3f}")
        if projection_contour_precision < contour_precision_need \
                or projection_contour_recall < contour_recall_need:
            raise ValueError(
                "target-hidden difference does not preserve enough of the current "
                "source-alpha silhouette contour "
                f"(precision={projection_contour_precision:.3f}, "
                f"recall={projection_contour_recall:.3f}; requires "
                f"{contour_precision_need:.3f}/{contour_recall_need:.3f})")

        def bounds(raw: object, label: str) -> tuple[int, int, int, int]:
            values = numeric_list(raw, 4, label, positive_size=True)
            x, y, rect_w, rect_h = (int(round(value)) for value in values)
            if x < 0 or y < 0 or x + rect_w > width or y + rect_h > height:
                raise ValueError(f"{label} is outside the {width}x{height} capture")
            return x, y, rect_w, rect_h

        measured_rect = [int(xs.min()), int(ys.min()),
                         int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]
        declared_rect = list(bounds(sample.get("figure_rect"), "figure_rect"))
        if measured_rect != declared_rect:
            raise ValueError(
                f"target-difference bbox {measured_rect} does not equal figure_rect "
                f"{declared_rect}")

        dilation_radius = 6
        dilated = target_mask.copy()
        for dy in range(-dilation_radius, dilation_radius + 1):
            for dx in range(-dilation_radius, dilation_radius + 1):
                if dx * dx + dy * dy <= dilation_radius * dilation_radius:
                    dilated |= shifted(target_mask, dy, dx)
        background_mask = dilated & ~target_mask
        eroded = target_mask.copy()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)):
            eroded &= shifted(target_mask, dy, dx)
        inner_boundary = target_mask & ~eroded
        outer_boundary = np.zeros_like(target_mask)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)):
            outer_boundary |= shifted(target_mask, dy, dx)
        outer_boundary &= ~target_mask
        rgb = capture_rgba[..., :3].astype(np.float32) / 255.0
        figure_px = rgb[target_mask]
        background_px = rgb[background_mask]
        inner = rgb[inner_boundary]
        outer = rgb[outer_boundary]
        if figure_px.size == 0 or background_px.size == 0 \
                or inner.size == 0 or outer.size == 0:
            raise ValueError("target mask has no usable figure, annulus, or boundary pixels")
        lum_weights = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
        figure_l = float((figure_px @ lum_weights).mean())
        background_l = float((background_px @ lum_weights).mean())
        figure_rgb = figure_px.mean(axis=0)
        background_rgb = background_px.mean(axis=0)
        color_distance = float(np.linalg.norm(figure_rgb - background_rgb) / math.sqrt(3.0))
        boundary_distance = float(np.linalg.norm(
            inner.reshape(-1, 3).mean(axis=0)
            - outer.reshape(-1, 3).mean(axis=0)) / math.sqrt(3.0))
        return ({
            "figure_pixels": int(figure_px.shape[0]),
            "background_pixels": int(background_px.shape[0]),
            "figure_luminance": round(figure_l, 6),
            "background_luminance": round(background_l, 6),
            "luminance_delta": round(abs(figure_l - background_l), 6),
            "color_distance": round(color_distance, 6),
            "boundary_contrast": round(boundary_distance, 6),
            "figure_rect": measured_rect,
            "mask_path": mask_path,
            "target_hidden_capture_path": hidden_path,
            "target_restored_capture_path": restored_path,
            "target_instance_path": target_path,
            "visual_instance_paths": visual_paths,
            "mask_source_art": source_art,
            "projection_method": SOURCE_PROJECTION_METHOD,
            "projection_precision": round(projection_precision, 6),
            "projection_visible_fraction": round(projection_visible_fraction, 6),
            "projection_contour_precision": round(projection_contour_precision, 6),
            "projection_contour_recall": round(projection_contour_recall, 6),
            "projection_visuals": projection_evidence,
        }, "")
    except Exception as exc:  # noqa: BLE001
        return ({}, f"{type(exc).__name__}: {exc}")


def _complete_rendered_readability_pass(zone: Zone) -> bool:
    """True only for current rendered evidence from a pure live Canvas stage."""
    if builder_stage_evidence(zone).get("backend") not in {"canvas_2d", "sprite3d_25d"} \
            or zone.presentation == "legacy_3d_debt":
        return False
    facts = zone.runtime_facts()
    canvas = facts.get("canvas_parallax") if isinstance(facts, dict) else None
    if not isinstance(canvas, dict) or _runtime_contract_issues(zone, canvas):
        return False
    if canvas.get("backend") != "canvas_2d" \
            or canvas.get("root_canvas_item") is not True \
            or int(canvas.get("non_canvas_spatial_nodes", 0)) != 0:
        return False
    layers = canvas.get("layers")
    if not isinstance(layers, list) or not layers:
        return False
    for value in layers:
        if not isinstance(value, dict) \
                or value.get("instantiated") is not True \
                or value.get("visible") is not True \
                or value.get("canvas_item") is not True \
                or int(value.get("non_canvas_spatial_descendants", 0)) != 0:
            return False
    rows = list(_rendered_readability(zone))
    return len(rows) == 1 and rows[0].disposition == PASS

@check("palette.background_recessive", "palette", "background_recessive",
       presentations=FLAT_PRESENTATIONS)
def _background_recessive(zone: Zone) -> Iterator[Finding]:
    """Source-image saturation averages flag review risk, never gameplay failure."""
    if not zone.murals or not zone.foreground:
        yield Finding("palette.background_recessive", zone.id, SKIP,
                      "needs both murals and foreground art declared")
        return
    bg = [zone.repo.image(r).get("saturation") for r in zone.murals]
    fg = [zone.repo.image(r).get("saturation") for r in zone.foreground]
    bg = [v for v in bg if v is not None]
    fg = [v for v in fg if v is not None]
    if not bg or not fg:
        yield Finding("palette.background_recessive", zone.id, SKIP, "no readable art")
        return
    bg_s = sum(bg) / len(bg)
    fg_s = sum(fg) / len(fg)
    ratio = bg_s / fg_s if fg_s > 0 else math.inf
    cap = float(zone.budget("background_saturation_ratio_max", 0.90))
    if ratio <= cap:
        yield Finding("palette.background_recessive", zone.id, INFO,
                      f"source-average saturation ratio is {ratio:.2f} (cap {cap:.2f}); "
                      "state-local rendered evidence remains authoritative",
                      evidence={"evidence_class": "static_source_average",
                                "can_fail_gameplay_readability": False,
                                "background_saturation": round(bg_s, 4),
                                "foreground_saturation": round(fg_s, 4),
                                "ratio": round(ratio, 3), "cap": cap})
        return
    evidence = {"background_saturation": round(bg_s, 4),
                "foreground_saturation": round(fg_s, 4),
                "ratio": round(ratio, 3), "cap": cap,
                "murals": zone.murals, "foreground": zone.foreground,
                "evidence_class": "static_source_average",
                "can_fail_gameplay_readability": False}
    if _complete_rendered_readability_pass(zone):
        evidence["superseded_by"] = "palette.rendered_composite_readability"
        yield Finding(
            "palette.background_recessive", zone.id, INFO,
            f"source-average saturation ratio {ratio:.2f} flags a static risk, but "
            "complete current state-local composites clear an approved separation "
            "channel; the heuristic is superseded",
            evidence=evidence,
        )
        return
    yield Finding(
        "palette.background_recessive", zone.id, WARN,
        f"source-average background saturation {bg_s:.3f} vs foreground {fg_s:.3f} "
        f"(ratio {ratio:.2f}, cap {cap:.2f}) is a review risk. These files may "
        "represent mutually exclusive states or transparent decorations, so this "
        "heuristic cannot establish an in-game failure",
        evidence=evidence,
    )


@check("palette.figure_ground_luminance", "palette", "background_recessive",
       presentations=FLAT_PRESENTATIONS)
def _luminance(zone: Zone) -> Iterator[Finding]:
    """Source-image luminance averages flag review risk, never gameplay failure."""
    if not zone.murals or not zone.foreground:
        yield Finding("palette.figure_ground_luminance", zone.id, SKIP,
                      "needs both murals and foreground art declared")
        return
    bg = [zone.repo.image(r).get("luminance") for r in zone.murals]
    fg = [zone.repo.image(r).get("luminance") for r in zone.foreground]
    bg = [v for v in bg if v is not None]
    fg = [v for v in fg if v is not None]
    if not bg or not fg:
        yield Finding("palette.figure_ground_luminance", zone.id, SKIP, "no readable art")
        return
    bg_l = sum(bg) / len(bg)
    fg_l = sum(fg) / len(fg)
    delta = abs(bg_l - fg_l)
    need = float(zone.budget("foreground_luminance_delta_min", 0.04))
    if delta >= need:
        yield Finding("palette.figure_ground_luminance", zone.id, INFO,
                      f"source-average figure/ground luminance delta {delta:.3f}; "
                      "state-local rendered evidence remains authoritative",
                      evidence={"evidence_class": "static_source_average",
                                "can_fail_gameplay_readability": False,
                                "delta": round(delta, 4)})
        return
    evidence = {"background_luminance": round(bg_l, 4),
                "foreground_luminance": round(fg_l, 4),
                "delta": round(delta, 4),
                "evidence_class": "static_source_average",
                "can_fail_gameplay_readability": False}
    if _complete_rendered_readability_pass(zone):
        evidence["superseded_by"] = "palette.rendered_composite_readability"
        yield Finding(
            "palette.figure_ground_luminance", zone.id, INFO,
            f"source-average luminance delta {delta:.3f} flags a static risk, but "
            "complete current state-local composites clear value, colour, or boundary "
            "separation; the heuristic is superseded",
            evidence=evidence,
        )
        return
    yield Finding(
        "palette.figure_ground_luminance", zone.id, WARN,
        f"source-average figure/ground luminance delta is {delta:.3f} "
        f"(review threshold {need:.3f}); only a complete current state-local "
        "rendered composite can close or confirm this risk",
        evidence=evidence,
    )


@check("palette.rendered_composite_readability", "palette", "background_recessive",
       presentations=FLAT_PRESENTATIONS)
def _rendered_readability(zone: Zone) -> Iterator[Finding]:
    """Only current captured pixels failing every separation channel hard-fail."""
    if not zone.murals or not zone.foreground:
        yield Finding(
            "palette.rendered_composite_readability", zone.id, INFO,
            "zone has no declared mural/foreground pair to compare",
            disposition=NOT_APPLICABLE,
        )
        return
    required = zone.rendered_readability_states
    if not isinstance(required, list) or not required:
        yield Finding(
            "palette.rendered_composite_readability", zone.id, SKIP,
            "zone declares no required rendered_readability_states; source averages "
            "cannot substitute for state-local evidence",
        )
        return
    adapter_gaps: list[str] = []
    for requirement in required:
        if not isinstance(requirement, dict):
            adapter_gaps.append("rendered state declaration is malformed")
            continue
        state_id = str(requirement.get("id", "<unnamed>"))
        adapter = str(requirement.get("capture_adapter", ""))
        contract = RENDERED_STATE_ADAPTER_CONTRACTS.get((zone.id, state_id))
        if contract is None or adapter != contract["adapter"]:
            reason = str(requirement.get(
                "coverage_gap_reason", "no implemented state capture adapter"))
            adapter_gaps.append(
                f"state '{state_id}' remains COVERAGE_GAP: {reason}; "
                "an adapter-shaped string is not an implemented state transition")
    if adapter_gaps:
        yield Finding(
            "palette.rendered_composite_readability", zone.id, SKIP,
            "; ".join(adapter_gaps),
            evidence={"evidence_class": "declared_capture_adapter_gap",
                      "required_states": required},
        )
        return
    facts = zone.runtime_facts()
    captured = facts.get("rendered_composites") if isinstance(facts, dict) else None
    if not isinstance(captured, list) or not captured:
        yield Finding(
            "palette.rendered_composite_readability", zone.id, SKIP,
            "needs state-local viewport-composite evidence from "
            "scripts/probe_visual_audit.gd",
            evidence={"required_states": required},
        )
        return

    gaps: list[str] = []
    failed_all_channels: list[dict] = []
    passing_channels: list[dict] = []
    accepted_samples = 0
    min_pixels = int(zone.budget("rendered_readability_min_sample_pixels", 64))
    need_luminance = float(zone.budget("foreground_luminance_delta_min", 0.04))
    need_color = float(zone.budget("rendered_color_distance_min", 0.10))
    need_boundary = float(zone.budget("rendered_boundary_contrast_min", 0.08))
    captured_by_id: dict[str, dict] = {}
    capture_hash_owners: dict[str, str] = {}
    state_signature_owners: dict[str, str] = {}
    for value in captured:
        if not isinstance(value, dict):
            gaps.append("rendered_composites contains a non-object state")
            continue
        state_id = str(value.get("id", ""))
        if not state_id:
            gaps.append("captured state has no id")
        elif state_id in captured_by_id:
            gaps.append(f"captured state '{state_id}' is duplicated")
        else:
            captured_by_id[state_id] = value
        capture_hash = str(value.get("capture_sha256", ""))
        if capture_hash:
            owner = capture_hash_owners.get(capture_hash)
            if owner is not None and owner != state_id:
                gaps.append(
                    f"states '{owner}' and '{state_id}' reuse one flattened capture")
            else:
                capture_hash_owners[capture_hash] = state_id
        state_signature = str(value.get("adapter_state_signature", ""))
        if state_signature:
            owner = state_signature_owners.get(state_signature)
            if owner is not None and owner != state_id:
                gaps.append(
                    f"states '{owner}' and '{state_id}' reuse one asserted live state")
            else:
                state_signature_owners[state_signature] = state_id

    for requirement in required:
        if not isinstance(requirement, dict) or not str(requirement.get("id", "")):
            gaps.append("required rendered state declaration is malformed")
            continue
        state_id = str(requirement["id"])
        state = captured_by_id.get(state_id)
        if state is None:
            gaps.append(f"required state '{state_id}' was not captured")
            continue
        if state.get("capture_adapter") != requirement.get("capture_adapter"):
            gaps.append(f"state '{state_id}' was captured by the wrong adapter")
        adapter_contract = RENDERED_STATE_ADAPTER_CONTRACTS.get((zone.id, state_id))
        if adapter_contract is None:
            gaps.append(f"state '{state_id}' has no implemented capture adapter")
        else:
            expected_state = adapter_contract["state"]
            expected_signature = hashlib.sha256(json.dumps(
                expected_state, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8")).hexdigest()
            if state.get("adapter_method") != adapter_contract["method"]:
                gaps.append(
                    f"state '{state_id}' lacks the implemented adapter assertion method")
            if state.get("adapter_state") != expected_state:
                gaps.append(
                    f"state '{state_id}' does not match its asserted live state")
            if state.get("adapter_state_signature") != expected_signature:
                gaps.append(
                    f"state '{state_id}' asserted-state signature is invalid")
        if state.get("source") != "viewport_composite":
            gaps.append(f"state '{state_id}' is not sourced from a viewport composite")
        gaps.extend(_rendered_provenance_issues(zone, state))
        viewport = state.get("viewport")
        if viewport != [1280, 720]:
            gaps.append(
                f"state '{state_id}' viewport is {viewport!r}; requires the exact "
                "1280x720 base Canvas")
        else:
            try:
                from PIL import Image
                with zone.repo.open_image(str(state.get("capture_path", ""))) as image:
                    if list(image.size) != [int(viewport[0]), int(viewport[1])]:
                        gaps.append(
                            f"state '{state_id}' viewport does not match capture pixels")
            except Exception as exc:  # noqa: BLE001
                gaps.append(f"state '{state_id}' capture is unreadable: {exc}")
        samples = state.get("samples")
        if not isinstance(samples, list) or not samples:
            gaps.append(f"state '{state_id}' contains no local target samples")
            continue
        required_targets = requirement.get("required_targets", [])
        if not isinstance(required_targets, list):
            gaps.append(f"state '{state_id}' required_targets declaration is malformed")
            required_targets = []
        min_samples = int(requirement.get("min_samples", len(required_targets) or 1))
        sample_by_id: dict[str, dict] = {}
        target_instance_owners: dict[str, str] = {}
        visual_instance_owners: dict[str, str] = {}
        for sample in samples:
            if not isinstance(sample, dict):
                gaps.append(f"state '{state_id}' contains a non-object sample")
                continue
            target_id = str(sample.get("id", ""))
            if not target_id:
                gaps.append(f"state '{state_id}' contains an unnamed sample")
                continue
            if target_id in sample_by_id:
                gaps.append(f"state '{state_id}' duplicates target '{target_id}'")
                continue
            sample_by_id[target_id] = sample
            target_path = str(sample.get("target_instance_path", ""))
            conflicting_target = next((
                (path, owner) for path, owner in target_instance_owners.items()
                if target_path == path or target_path.startswith(path + "/")
                or path.startswith(target_path + "/")
            ), None) if target_path else None
            if conflicting_target is not None:
                gaps.append(
                    f"state '{state_id}' target '{target_id}' reuses live target "
                    f"instance ownership with '{conflicting_target[1]}'")
            elif target_path:
                target_instance_owners[target_path] = target_id
            visuals = sample.get("visuals")
            if isinstance(visuals, list):
                for visual in visuals:
                    visual_path = str(visual.get("instance_path", "")) \
                        if isinstance(visual, dict) else ""
                    if not visual_path:
                        continue
                    owner = visual_instance_owners.get(visual_path)
                    if owner is not None and owner != target_id:
                        gaps.append(
                            f"state '{state_id}' target '{target_id}' reuses live "
                            f"visual instance owned by '{owner}'")
                    else:
                        visual_instance_owners[visual_path] = target_id
            metrics, metric_error = _rendered_sample_metrics(zone, state, sample)
            if metric_error:
                gaps.append(
                    f"state '{state_id}' target '{target_id}' cannot be recomputed: "
                    f"{metric_error}")
                continue
            if metrics["figure_pixels"] < min_pixels \
                    or metrics["background_pixels"] < min_pixels:
                gaps.append(
                    f"state '{state_id}' target '{target_id}' has too few sampled pixels")
                continue
            accepted_samples += 1
            channels = {
                "luminance": metrics["luminance_delta"] >= need_luminance,
                "color": metrics["color_distance"] >= need_color,
                "boundary": metrics["boundary_contrast"] >= need_boundary,
            }
            row = {"state": state_id, "target": target_id,
                   "channels": channels, "metrics": metrics,
                   "minimums": {"luminance_delta": need_luminance,
                                "color_distance": need_color,
                                "boundary_contrast": need_boundary}}
            if any(channels.values()):
                passing_channels.append(row)
            else:
                failed_all_channels.append(row)
        missing_targets = sorted(set(str(value) for value in required_targets)
                                 - set(sample_by_id))
        if missing_targets:
            gaps.append(f"state '{state_id}' is missing targets {missing_targets}")
        if len(sample_by_id) < min_samples:
            gaps.append(
                f"state '{state_id}' has {len(sample_by_id)} sample(s); needs {min_samples}")

    if gaps:
        yield Finding(
            "palette.rendered_composite_readability", zone.id, SKIP,
            "; ".join(gaps),
            evidence={"evidence_class": "state_local_rendered_composite",
                      "required_states": required, "captured_states": captured},
        )
        return
    if failed_all_channels:
        yield Finding(
            "palette.rendered_composite_readability", zone.id, ERROR,
            f"{len(failed_all_channels)}/{accepted_samples} state-local target "
            "sample(s) fail value, perceptual-colour, and outline/boundary "
            "separation together",
            evidence={"evidence_class": "state_local_rendered_composite",
                      "failed_all_channels": failed_all_channels,
                      "passing_samples": passing_channels,
                      "captured_states": captured},
        )
        return
    yield Finding(
        "palette.rendered_composite_readability", zone.id, INFO,
        f"{accepted_samples} current state-local viewport-composite target samples "
        "clear at least one approved separation channel",
        evidence={"evidence_class": "state_local_rendered_composite",
                  "passing_samples": passing_channels,
                  "captured_states": captured},
    )


@check("overdraw.alpha_layers", "overdraw", "alpha_layer_budget",
       presentations=FLAT_PRESENTATIONS)
def _alpha_layers(zone: Zone) -> Iterator[Finding]:
    """At most two alpha-carrying full-width layers per stage (Mali overdraw)."""
    if not zone.murals:
        yield Finding("overdraw.alpha_layers", zone.id, SKIP, "zone declares no murals")
        return
    alpha_layers = sorted({os.path.basename(r) for r in zone.murals
                           if zone.repo.image(r).get("has_alpha")})
    cap = int(zone.budget("alpha_layers_max", 2))
    if len(alpha_layers) <= cap:
        yield Finding("overdraw.alpha_layers", zone.id, INFO,
                      f"{len(alpha_layers)} alpha mural layer(s) (cap {cap})")
        return
    yield Finding("overdraw.alpha_layers", zone.id, ERROR,
                  f"{len(alpha_layers)} alpha-carrying mural files exceed the hard Mali "
                  f"overdraw budget of {cap}",
                  evidence={"alpha_layers": alpha_layers, "cap": cap})


@check("readability.tap_target_size", "readability", "tap_target_size", stressable=False)
def _tap_targets(zone: Zone) -> Iterator[Finding]:
    """Every tap target clears the 110px minimum touch size at 1280x720 base."""
    facts = zone.runtime_facts()
    if not facts or "targets" not in facts:
        yield Finding("readability.tap_target_size", zone.id, SKIP,
                      "needs runtime facts — run scripts/probe_visual_audit.gd "
                      f"to produce {os.path.relpath(RUNTIME_FACTS_PATH, REPO)}")
        return
    provenance_issues = _runtime_contract_issues(zone, facts)
    if provenance_issues:
        yield Finding("readability.tap_target_size", zone.id, SKIP,
                      "; ".join(provenance_issues), evidence={"runtime": facts})
        return
    targets = facts["targets"]
    if not isinstance(targets, list) or not targets:
        yield Finding("readability.tap_target_size", zone.id, SKIP,
                      "runtime facts contain no tap targets; empty evidence cannot prove "
                      "the 110px touch contract")
        return
    target_ids = [str(value.get("id", "")) if isinstance(value, dict) else ""
                  for value in targets]
    target_paths = [str(value.get("instance_path", ""))
                    if isinstance(value, dict) else "" for value in targets]
    root_path = str(facts.get("root_instance_path", ""))
    if any(not target_id for target_id in target_ids) \
            or len(set(target_ids)) != len(target_ids) \
            or any(not path.startswith(root_path + "/") for path in target_paths) \
            or len(set(target_paths)) != len(target_paths) \
            or any(not isinstance(value, dict)
                   or value.get("audited_viewport") is not True
                   or value.get("interaction_registry")
                   != "lagoon_promenade_targets_v1"
                   or value.get("resolver_method")
                   != "production_target_at_radial_reach_v2"
                   or value.get("resolver_hit_confirmed") is not True
                   or value.get("resolver_center_in_viewport") is not True
                   or str(value.get("resolver_returned_id", ""))
                   != str(value.get("id", ""))
                   or not isinstance(value.get("visible_canvas_visual_count"), int)
                   or isinstance(value.get("visible_canvas_visual_count"), bool)
                   or int(value.get("visible_canvas_visual_count", 0)) <= 0
                   for value in targets):
        yield Finding(
            "readability.tap_target_size", zone.id, SKIP,
            "tap-target facts do not bind unique IDs to unique visible instances "
            "in the audited root viewport",
            evidence={"targets": targets},
        )
        return
    fact_issues: list[str] = []
    rendered_rects: dict[str, list[list[float]]] = {}
    rendered_states = facts.get("rendered_composites", [])
    if isinstance(rendered_states, list):
        for state in rendered_states:
            if not isinstance(state, dict) or not isinstance(state.get("samples"), list):
                continue
            for sample in state["samples"]:
                if not isinstance(sample, dict):
                    continue
                sample_id = str(sample.get("id", ""))
                rect = sample.get("figure_rect")
                if sample_id and isinstance(rect, list) and len(rect) == 4 \
                        and all(isinstance(value, (int, float))
                                and not isinstance(value, bool)
                                and math.isfinite(float(value)) for value in rect):
                    rendered_rects.setdefault(sample_id, []).append(
                        [float(value) for value in rect])
    for target in targets:
        target_id = str(target.get("id", "<unnamed>"))
        screen = target.get("screen_px")
        hit = target.get("hit_diameter_px")
        visual_height = target.get("visual_screen_px")
        visual_width = target.get("visual_width_px")
        nearest_painted = target.get("resolver_nearest_painted_px")
        reach_radius = target.get("resolver_reach_radius_px")
        numbers = (screen, hit, visual_height, visual_width, nearest_painted,
                   reach_radius)
        if any(not isinstance(value, (int, float)) or isinstance(value, bool)
               or not math.isfinite(float(value)) or float(value) < 0.0
               for value in numbers):
            fact_issues.append(f"target '{target_id}' has malformed size evidence")
            continue
        if abs(float(screen) - float(hit)) > 0.11:
            fact_issues.append(
                f"target '{target_id}' screen_px disagrees with hit_diameter_px")
        if target.get("meets_min_touch") is not (float(hit) >= 110.0):
            fact_issues.append(
                f"target '{target_id}' has an inconsistent meets_min_touch result")
        hit_point = target.get("resolver_hit_screen_px")
        visual_rect = target.get("visual_screen_rect")
        if not isinstance(hit_point, list) or len(hit_point) != 2 \
                or any(not isinstance(value, (int, float)) or isinstance(value, bool)
                       or not math.isfinite(float(value)) for value in hit_point):
            fact_issues.append(
                f"target '{target_id}' has a malformed resolver hit centre")
            continue
        expected_reach = min(float(hit) * 0.5, 55.0)
        if abs(float(reach_radius) - expected_reach) > 0.11:
            fact_issues.append(
                f"target '{target_id}' resolver reach disagrees with its measured hit size")
        reach_samples = target.get("resolver_reach_samples")
        if not isinstance(reach_samples, list) or len(reach_samples) != 9:
            fact_issues.append(
                f"target '{target_id}' lacks centre/cardinal/diagonal resolver samples")
        else:
            seen_offsets: set[tuple[float, float]] = set()
            center_samples = 0
            radial_samples = 0
            for sample in reach_samples:
                if not isinstance(sample, dict):
                    fact_issues.append(
                        f"target '{target_id}' has a malformed resolver sample")
                    continue
                offset = sample.get("offset_px")
                point = sample.get("screen_px")
                if not isinstance(offset, list) or len(offset) != 2 \
                        or not isinstance(point, list) or len(point) != 2 \
                        or any(not isinstance(value, (int, float))
                               or isinstance(value, bool)
                               or not math.isfinite(float(value))
                               for value in [*offset, *point]):
                    fact_issues.append(
                        f"target '{target_id}' has a malformed resolver sample geometry")
                    continue
                offset_key = (round(float(offset[0]), 1),
                              round(float(offset[1]), 1))
                if offset_key in seen_offsets:
                    fact_issues.append(
                        f"target '{target_id}' duplicates a resolver reach sample")
                seen_offsets.add(offset_key)
                distance = math.hypot(float(offset[0]), float(offset[1]))
                if distance <= 0.11:
                    center_samples += 1
                elif abs(distance - expected_reach) <= 0.2:
                    radial_samples += 1
                else:
                    fact_issues.append(
                        f"target '{target_id}' resolver sample is not on its proved boundary")
                if abs(float(point[0]) - (float(hit_point[0])
                                          + float(offset[0]))) > 0.11 \
                        or abs(float(point[1]) - (float(hit_point[1])
                                                 + float(offset[1]))) > 0.11:
                    fact_issues.append(
                        f"target '{target_id}' resolver sample is not bound to its centre")
                if sample.get("inside_viewport") is not True \
                        or sample.get("matches_target") is not True \
                        or str(sample.get("returned_id", "")) != target_id:
                    fact_issues.append(
                        f"target '{target_id}' production resolver misses its 55px reach")
            if center_samples != 1 or radial_samples != 8:
                fact_issues.append(
                    f"target '{target_id}' resolver samples do not cover one centre "
                    "and eight radial directions")
            reach_key = round(expected_reach, 1)
            diagonal = round(expected_reach / math.sqrt(2.0), 1)
            expected_offsets = {
                (0.0, 0.0), (reach_key, 0.0), (-reach_key, 0.0),
                (0.0, reach_key), (0.0, -reach_key),
                (diagonal, diagonal), (diagonal, -diagonal),
                (-diagonal, diagonal), (-diagonal, -diagonal),
            }
            if seen_offsets != expected_offsets:
                fact_issues.append(
                    f"target '{target_id}' resolver samples omit required directions")
        if not (0.0 <= float(hit_point[0]) < 1280.0
                and 0.0 <= float(hit_point[1]) < 720.0):
            fact_issues.append(
                f"target '{target_id}' resolver hit centre is outside the viewport")
        if not isinstance(visual_rect, list) or len(visual_rect) != 4 \
                or any(not isinstance(value, (int, float)) or isinstance(value, bool)
                       or not math.isfinite(float(value)) for value in visual_rect) \
                or float(visual_rect[2]) <= 0.0 or float(visual_rect[3]) <= 0.0:
            fact_issues.append(
                f"target '{target_id}' has a malformed visible-art rectangle")
            continue
        causal_rects = rendered_rects.get(target_id, [])
        if not causal_rects:
            fact_issues.append(
                f"target '{target_id}' has no bound rendered-difference silhouette")
        elif any(rect[2] <= 0.0 or rect[3] <= 0.0
                 or abs(rect[2] - float(visual_rect[2])) > 4.0
                 or abs(rect[3] - float(visual_rect[3])) > 4.0
                 for rect in causal_rects):
            fact_issues.append(
                f"target '{target_id}' visible size disagrees with its rendered silhouette")
        left, top, width, height = (float(value) for value in visual_rect)
        right, bottom = left + width, top + height
        dx = max(left - float(hit_point[0]), 0.0, float(hit_point[0]) - right)
        dy = max(top - float(hit_point[1]), 0.0, float(hit_point[1]) - bottom)
        rect_distance = math.hypot(dx, dy)
        near_limit = min(float(hit) * 0.5, max(16.0,
                         min(float(visual_width), float(visual_height)) * 0.5))
        if rect_distance > near_limit + 0.11 \
                or float(nearest_painted) > near_limit + 0.11:
            fact_issues.append(
                f"target '{target_id}' production hit centre is not near visible art")
    if fact_issues:
        yield Finding(
            "readability.tap_target_size", zone.id, SKIP,
            "; ".join(fact_issues), evidence={"targets": targets},
        )
        return
    min_visible = float(zone.budget("tap_target_min_visible_px", 64.0))
    small = [
        (target, [
            *( [f"hit diameter {float(target['hit_diameter_px']):.0f}px < 110px"]
               if float(target["hit_diameter_px"]) < 110.0 else []),
            *( [f"visible size {float(target['visual_width_px']):.0f}x"
                f"{float(target['visual_screen_px']):.0f}px < {min_visible:.0f}px"]
               if min(float(target["visual_width_px"]),
                      float(target["visual_screen_px"])) < min_visible else []),
        ])
        for target in targets
    ]
    small = [(target, reasons) for target, reasons in small if reasons]
    for t, reasons in small:
        yield Finding("readability.tap_target_size", zone.id, WARN,
                      f"target '{t.get('id')}' is undersized for a 4-year-old: "
                      + "; ".join(reasons),
                      evidence=t)
    if not small:
        yield Finding("readability.tap_target_size", zone.id, INFO,
                      f"{len(targets)} tap targets clear 110px")


# --------------------------------------------------------------------------
# CHECKS — current release evidence
# --------------------------------------------------------------------------

@check("charter.probe_gated", "charter", "probe_gate")
def _probe_gated(zone: Zone) -> Iterator[Finding]:
    """Every shipped zone has at least one probe in the trusted CI list."""
    if zone.lifecycle != "active_shipped":
        yield Finding("charter.probe_gated", zone.id, INFO,
                      f"lifecycle '{zone.lifecycle}' does not ship",
                      disposition=NOT_APPLICABLE)
        return
    if not zone.probes:
        yield Finding("charter.probe_gated", zone.id, ERROR,
                      "shipped zone declares no probe")
        return
    ci = zone.repo.read("scripts/ci.sh")
    trusted = [p for p in zone.probes
               if os.path.basename(p).removesuffix(".gd") in ci]
    if trusted:
        yield Finding("charter.probe_gated", zone.id, INFO,
                      f"gated by {', '.join(os.path.basename(p) for p in trusted)}")
        return
    yield Finding("charter.probe_gated", zone.id, WARN,
                  f"none of this zone's probes ({', '.join(zone.probes)}) appear in the "
                  f"trusted list in scripts/ci.sh — the zone ships ungated",
                  evidence={"probes": zone.probes})


# --------------------------------------------------------------------------
# CHECKS — asset hygiene
# --------------------------------------------------------------------------

@check("hygiene.orphan_art", "hygiene", "orphan_art")
def _orphans(zone: Zone) -> Iterator[Finding]:
    """Shipped PNGs under a zone's roots are referenced by something."""
    if not zone.asset_roots:
        yield Finding("hygiene.orphan_art", zone.id, SKIP, "zone declares no asset roots")
        return
    pngs = zone.repo.expand([os.path.join(r, "**", "*.png") for r in zone.asset_roots])
    if not pngs:
        yield Finding("hygiene.orphan_art", zone.id, SKIP, "no PNGs under the zone roots")
        return
    src = zone.repo.all_source()
    orphans = [p for p in pngs if os.path.basename(p) not in src]
    total = sum(zone.repo.size(p) for p in orphans)
    if not orphans:
        yield Finding("hygiene.orphan_art", zone.id, INFO, f"all {len(pngs)} PNGs referenced")
        return
    warn_at = int(zone.budget("orphan_bytes_warn", 1048576))
    sev = WARN if total >= warn_at else INFO
    yield Finding("hygiene.orphan_art", zone.id, sev,
                  f"{len(orphans)}/{len(pngs)} PNGs are referenced by no script or scene "
                  f"({total / 1048576.0:.1f} MB of superseded art still shipping in the APK)",
                  evidence={"orphans": orphans, "bytes": total})


@check("hygiene.superseded_generations", "hygiene", "asset_generations")
def _generations(zone: Zone) -> Iterator[Finding]:
    """Only one generation of each named asset ships."""
    if not zone.asset_roots:
        yield Finding("hygiene.superseded_generations", zone.id, SKIP, "no asset roots")
        return
    pngs = zone.repo.expand([os.path.join(r, "**", "*.png") for r in zone.asset_roots])
    if not pngs:
        yield Finding("hygiene.superseded_generations", zone.id, SKIP, "no PNGs")
        return
    families: dict[str, list[tuple[str, str]]] = {}
    for p in pngs:
        stem = os.path.basename(p).removesuffix(".png")
        # Only an explicit _vN token denotes a generation. Numeric animation
        # frame suffixes are identity: slide_0/slide_1/slide_2_v2 are three
        # poses, not three competing versions of one file.
        match = re.match(
            r"^(.*)_v(\d+)(?:_(?:compact|audited(?:_\d+)?|drift|sway))*$",
            stem,
        )
        base, generation = (match.group(1), match.group(2)) if match else (stem, "0")
        families.setdefault(base, []).append((p, generation))
    multi = {
        key: [path for path, _generation in values]
        for key, values in families.items()
        if len({generation for _path, generation in values}) > 1
    }
    if not multi:
        yield Finding("hygiene.superseded_generations", zone.id, INFO,
                      "one generation per asset family")
        return
    for base, files in sorted(multi.items()):
        yield Finding("hygiene.superseded_generations", zone.id, WARN,
                      f"'{base}' ships {len(files)} generations: "
                      f"{', '.join(os.path.basename(f) for f in sorted(files))}",
                      evidence={"family": base, "files": sorted(files)})


def _licensed(rel: str, doc: str, patterns: list[str]) -> bool:
    """True if ASSET_LICENSES.md covers this asset by path, name, or family glob."""
    import fnmatch
    if rel in doc:
        return True
    base = os.path.basename(rel)
    for pat in patterns:
        if pat.endswith(base) or fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(base, pat):
            return True
        # a row may license a directory family: assets/fairy/sprites/*.png
        if "*" in pat and fnmatch.fnmatch(rel, pat.lstrip("./")):
            return True
    return base in doc


@check("hygiene.license_line", "hygiene", "licenses")
def _licenses(zone: Zone) -> Iterator[Finding]:
    """Every runtime asset has a line in ASSET_LICENSES.md."""
    art = zone.runtime_art
    if not art:
        yield Finding("hygiene.license_line", zone.id, SKIP, "no runtime PNG art")
        return
    doc = zone.repo.read("ASSET_LICENSES.md")
    if not doc:
        yield Finding("hygiene.license_line", zone.id, SKIP, "ASSET_LICENSES.md unreadable")
        return
    patterns = zone.repo.license_patterns()
    missing = [r for r in art if not _licensed(r, doc, patterns)]
    if not missing:
        yield Finding("hygiene.license_line", zone.id, INFO,
                      f"all {len(art)} runtime assets licensed")
        return
    yield Finding("hygiene.license_line", zone.id, ERROR,
                  f"{len(missing)} runtime asset(s) have no ASSET_LICENSES.md line",
                  evidence={"missing": missing})


@check("hygiene.manual_squint_test", "hygiene", "no_text_in_art",
       presentations=FLAT_PRESENTATIONS,
       stressable=False)
def _manual(zone: Zone) -> Iterator[Finding]:
    """Flags what only a human can judge: no text, nothing scary, squint test."""
    art = zone.murals + zone.standees
    if not art:
        yield Finding("hygiene.manual_squint_test", zone.id, SKIP, "no flat art")
        return
    yield Finding("hygiene.manual_squint_test", zone.id, MANUAL,
                  f"{len(art)} flats need the human pass this tool cannot do: no words/"
                  f"letters/digits, nothing scary at child eye level, and the M11 squint "
                  f"test (every socket still findable)",
                  evidence={"files": art})


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------

def load_spec(path: str = SPEC_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


WAIVER_REQUIRED_FIELDS = {
    "check", "zone", "rule", "scope", "reason", "owner", "date",
    "review_trigger", "residual_risk",
}


def waiver_contract_issues(spec: dict) -> list[str]:
    """Return owner-actionable errors for incomplete or dangling waivers."""
    issues: list[str] = []
    zone_ids = {z.get("id") for z in spec.get("zones", [])}
    seen: set[tuple[str, str]] = set()
    for index, waiver in enumerate(spec.get("waivers", [])):
        missing = sorted(field for field in WAIVER_REQUIRED_FIELDS
                         if not str(waiver.get(field, "")).strip())
        if missing:
            issues.append(f"waiver #{index + 1} missing required fields: {', '.join(missing)}")
        check_id = waiver.get("check")
        zone_id = waiver.get("zone")
        if check_id not in REGISTRY:
            issues.append(f"waiver #{index + 1} references unknown check '{waiver.get('check')}'")
        elif waiver.get("rule") != REGISTRY[check_id].rule:
            issues.append(
                f"waiver #{index + 1} rule '{waiver.get('rule')}' does not match "
                f"{check_id}'s rule '{REGISTRY[check_id].rule}'"
            )
        if zone_id not in zone_ids:
            issues.append(f"waiver #{index + 1} references unknown zone '{waiver.get('zone')}'")
        pair = (str(check_id), str(zone_id))
        if pair in seen:
            issues.append(f"waiver #{index + 1} duplicates {pair[0]}/{pair[1]}")
        seen.add(pair)
        if waiver.get("date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(waiver["date"])):
            issues.append(f"waiver #{index + 1} date must use YYYY-MM-DD")
    return issues


def strict_blockers(findings: Iterable[Finding]) -> list[Finding]:
    """Find unresolved results that prevent a complete audit from passing."""
    return [f for f in findings if f.disposition in STRICT_BLOCKING_DISPOSITIONS]


def strict_passes(findings: Iterable[Finding]) -> bool:
    """True only when the requested audit produced evidence and closed it all."""
    rows = list(findings)
    return bool(rows) and not strict_blockers(rows)


def satisfaction(findings: Iterable[Finding]) -> str:
    """Return the audit-level lifecycle state represented by the findings."""
    rows = list(findings)
    if not strict_passes(rows):
        return "UNSATISFIED"
    if any(f.disposition == WAIVED for f in rows):
        return "SATISFIED_WITH_WAIVERS"
    return "SATISFIED"


def run(repo: Repo, zone_ids: list[str] | None = None,
        check_ids: list[str] | None = None) -> list[Finding]:
    waiver_issues = waiver_contract_issues(repo.spec)
    waivers = {} if waiver_issues else {
        (w["check"], w["zone"]): w for w in repo.spec.get("waivers", [])
    }
    findings: list[Finding] = []
    for issue in waiver_issues:
        findings.append(Finding(
            "audit.waiver_contract", "_audit", ERROR, issue,
            rule=repo.spec.get("rules", {}).get("waiver_contract", "waiver_contract"),
        ))
    for raw in repo.spec["zones"]:
        if zone_ids and raw["id"] not in zone_ids:
            continue
        zone = Zone(raw, repo)
        for cid, chk in REGISTRY.items():
            if check_ids and cid not in check_ids:
                continue
            if (chk.presentations is not None
                    and zone.presentation not in chk.presentations):
                findings.append(Finding(
                    cid, zone.id, INFO,
                    f"presentation '{zone.presentation}' is outside this check's scope",
                    rule=repo.spec.get("rules", {}).get(chk.rule, chk.rule),
                    evidence={"presentation": zone.presentation,
                              "applies_to": sorted(chk.presentations)},
                    disposition=NOT_APPLICABLE,
                ))
                continue
            try:
                produced = list(chk.fn(zone))
            except Exception as exc:                              # noqa: BLE001
                produced = [Finding(cid, zone.id, ERROR,
                                    f"check crashed: {type(exc).__name__}: {exc}")]
            for f in produced:
                f.rule = f.rule or repo.spec.get("rules", {}).get(chk.rule, chk.rule)
                waiver = waivers.get((cid, zone.id))
                if waiver is not None and f.disposition in WAIVABLE_DISPOSITIONS:
                    f.disposition = WAIVED
                    f.message = f"[WAIVED: {waiver['reason']}] " + f.message
                    f.evidence = dict(f.evidence)
                    f.evidence["waiver"] = waiver
                elif waiver is not None and f.disposition in (MANUAL_OPEN, COVERAGE_GAP):
                    f.message = (f"[WAIVER CANNOT REPLACE {f.disposition} EVIDENCE] "
                                 + f.message)
                    f.evidence = dict(f.evidence)
                    f.evidence["rejected_waiver"] = waiver
                findings.append(f)
    findings.sort(key=Finding.key)
    return findings


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

COLORS = {ERROR: "\033[31m", WARN: "\033[33m", MANUAL: "\033[35m",
          INFO: "\033[32m", SKIP: "\033[90m"}
RESET = "\033[0m"


def configure_console() -> None:
    """Keep direct Windows runs usable when stdout is strict cp1252."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(errors="backslashreplace")
        except (OSError, ValueError):
            pass


def _tint(sev: str, text: str, use_color: bool) -> str:
    return f"{COLORS.get(sev, '')}{text}{RESET}" if use_color else text


def print_console(findings: list[Finding], verbose: bool) -> None:
    use_color = sys.stdout.isatty()
    shown = [f for f in findings
             if verbose or f.disposition not in (PASS, NOT_APPLICABLE)]
    by_zone: dict[str, list[Finding]] = {}
    for f in shown:
        by_zone.setdefault(f.zone, []).append(f)
    for zone_id in sorted(by_zone):
        print(f"\n-- {zone_id} " + "-" * max(0, 60 - len(zone_id)))
        for f in by_zone[zone_id]:
            label = f"{f.severity}/{f.disposition}"
            print(f"  {_tint(f.severity, label.ljust(22), use_color)} "
                  f"{f.check}\n                         {f.message}")
    counts = {s: sum(1 for f in findings if f.severity == s)
              for s in (ERROR, WARN, MANUAL, INFO, SKIP)}
    print("\n" + "=" * 62)
    print("VISUALAUDIT| " + "  ".join(
        f"{s}={counts[s]}" for s in (ERROR, WARN, MANUAL, INFO, SKIP)))
    states = {state: sum(1 for f in findings if f.disposition == state)
              for state in DISPOSITIONS}
    print("VISUALAUDIT| STATE " + "  ".join(
        f"{state}={states[state]}" for state in DISPOSITIONS)
        + f"  RESULT={satisfaction(findings)}")


def write_reports(findings: list[Finding], repo: Repo) -> None:
    os.makedirs(os.path.dirname(REPORT_JSON), exist_ok=True)
    payload = {
        "spec_version": repo.spec.get("version"),
        "checks": {c.id: {"category": c.category, "rule": c.rule, "doc": c.doc}
                   for c in REGISTRY.values()},
        "findings": [asdict(f) for f in findings],
        "summary": {s: sum(1 for f in findings if f.severity == s)
                     for s in (ERROR, WARN, MANUAL, INFO, SKIP)},
        "dispositions": {state: sum(1 for f in findings if f.disposition == state)
                         for state in DISPOSITIONS},
        "satisfaction": satisfaction(findings),
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    lines = ["# Visual design audit — generated report", "",
             "Generated by `tools/audit_visual_design.py`. Do not hand-edit;",
             "adjust `tools/visual_audit_spec.json` and re-run.", ""]
    summary = payload["summary"]
    lines += ["| Severity | Count |", "|---|---:|"]
    lines += [f"| {s} | {summary[s]} |" for s in (ERROR, WARN, MANUAL, INFO, SKIP)]
    lines.append("")
    lines += ["| Disposition | Count |", "|---|---:|"]
    lines += [f"| {state} | {payload['dispositions'][state]} |" for state in DISPOSITIONS]
    lines += ["", f"**Result:** `{payload['satisfaction']}`", ""]
    for state in (FAIL, REVIEW_OPEN, MANUAL_OPEN, COVERAGE_GAP, WAIVED):
        rows = [f for f in findings if f.disposition == state]
        if not rows:
            continue
        lines += [f"## {state}", "",
                  "| Severity | Zone | Check | Finding |", "|---|---|---|---|"]
        for f in rows:
            msg = f.message.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {f.severity} | `{f.zone}` | `{f.check}` | {msg} |")
        lines.append("")
    with open(REPORT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------
# stress mode — prove every check can actually fail
# --------------------------------------------------------------------------

def _write_png(path: str, w: int, h: int, rgb: tuple, alpha_coverage: float = 1.0) -> None:
    from PIL import Image
    import numpy as np
    os.makedirs(os.path.dirname(path), exist_ok=True)
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = rgb
    cut = int(h * min(max(alpha_coverage, 0.0), 1.0))
    arr[:cut, :, 3] = 255
    Image.fromarray(arr, "RGBA").save(path)


def _write_rendered_fixture(path: str, hidden_path: str, restored_path: str,
                            mask_path: str,
                            mode: str) -> tuple[list[int], list[int]]:
    """Write a full/target-hidden pair and their exact difference mask."""
    from PIL import Image, ImageDraw
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if mode in ("low_all_channels", "irregular_bbox_lie"):
        background, figure = (128, 128, 128), (130, 130, 130)
    elif mode == "same_luminance_color":
        # Rec.709 luminance is ~0.213 for both, while hue separation is strong.
        background, figure = (0, 76, 0), (255, 0, 0)
    else:
        background, figure = (64, 64, 76), (224, 224, 236)
    hidden = Image.new("RGB", (1280, 720), background)
    figure_rect = [592, 328, 96, 64]
    background_rect = [576, 312, 128, 96]
    mask = Image.new("L", hidden.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    if mode == "irregular_bbox_lie":
        # High-contrast decoration in the transparent corners makes a naïve
        # rectangle average look separated. The actual masked subject and its
        # local annulus remain nearly identical grey.
        mask_draw.rectangle((636, 328, 643, 391), fill=255)
        mask_draw.rectangle((592, 356, 687, 363), fill=255)
        draw = ImageDraw.Draw(hidden)
        for rect in ((592, 328, 625, 345), (654, 328, 687, 345),
                     (592, 374, 625, 391), (654, 374, 687, 391)):
            draw.rectangle(rect, fill=(250, 250, 250))
    else:
        mask_draw.ellipse((figure_rect[0], figure_rect[1],
                           figure_rect[0] + figure_rect[2] - 1,
                           figure_rect[1] + figure_rect[3] - 1), fill=255)
    image = hidden.copy()
    fill = Image.new("RGB", image.size, figure)
    image.paste(fill, mask=mask)
    image.save(path)
    hidden.save(hidden_path)
    image.save(restored_path)
    mask.save(mask_path)
    return figure_rect, background_rect


def _write_target_source_fixture(path: str, rgb: tuple, mode: str,
                                 alpha_coverage: float) -> None:
    """Write source alpha that truthfully projects to the rendered fixture target."""
    from PIL import Image, ImageDraw
    if abs(alpha_coverage - 0.4) > 1.0e-9:
        _write_png(path, 256, 256, rgb, alpha_coverage)
        return
    image = Image.new("RGBA", (256, 256), (*rgb, 0))
    draw = ImageDraw.Draw(image)
    if mode == "irregular_bbox_lie":
        draw.rectangle((117, 0, 138, 255), fill=(*rgb, 255))
        draw.rectangle((0, 112, 255, 143), fill=(*rgb, 255))
    else:
        draw.ellipse((0, 0, 255, 255), fill=(*rgb, 255))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)


def _fixture(root: str, *, presentation="panning_depth_cards", murals=1,
             mural_rgb=(60, 200, 255),
             fg_rgb=(150, 170, 190),
             depths=(("BACKDROP_Z", -18.0), ("DRESS_Z", -6.0), ("PLAY_Z", 0.5)),
             band=True, layers_api=False,
             lifecycle="active_shipped",
             licensed=True, extra_generation=False, alpha_murals=0,
             fg_coverage=0.4, mural_layer_names=("L0",), huge_texture=False,
             zone_budgets=None, canvas_layer_count=1,
             duplicate_canvas_assets=False, rendered_mode="luminance_pass") -> dict:
    """Build a synthetic repo that violates exactly what the caller asks for."""
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(root, "scenes"), exist_ok=True)
    os.makedirs(os.path.join(root, "tools"), exist_ok=True)
    with open(os.path.join(root, ".gitignore"), "w", encoding="utf-8") as fh:
        fh.write("/audit/\n")
    with open(os.path.join(root, "project.godot"), "w", encoding="utf-8") as fh:
        fh.write(
            '[application]\nrun/main_scene="res://scenes/main.tscn"\n'
            '[display]\nwindow/size/viewport_width=1280\n'
            'window/size/viewport_height=720\n'
            'window/stretch/mode="canvas_items"\nwindow/stretch/aspect="expand"\n'
            '[rendering]\nrenderer/rendering_method="mobile"\n')
    with open(os.path.join(root, "scenes", "main.tscn"), "w", encoding="utf-8") as fh:
        fh.write('[gd_scene format=3]\n[node name="Fixture" type="Node2D"]\n')
    with open(os.path.join(root, "scripts", "probe_visual_audit.gd"),
              "w", encoding="utf-8") as fh:
        fh.write("extends SceneTree\n# fixture evidence harness\n")
    with open(os.path.join(root, "scripts", "main.gd"),
              "w", encoding="utf-8") as fh:
        fh.write("extends Node2D\n# fixture main state owner\n")
    with open(os.path.join(root, "scripts", "player.gd"),
              "w", encoding="utf-8") as fh:
        fh.write("extends Node2D\n# fixture player controller\n")
    with open(os.path.join(root, "tools", "visual_audit_spec.json"),
              "w", encoding="utf-8") as fh:
        json.dump({"version": 6, "fixture": True}, fh, sort_keys=True)
    with open(os.path.join(root, "tools", "audit_game_2d.py"),
              "w", encoding="utf-8") as fh:
        fh.write("# fixture binding for canonical game-wide 2D taxonomy\n")
    with open(os.path.join(root, "tools", "audit_visual_design.py"),
              "w", encoding="utf-8") as fh:
        fh.write("# fixture binding for the PASS-producing verifier\n")

    mural_files, standee_files = [], []
    for i in range(murals):
        name = mural_layer_names[i % len(mural_layer_names)]
        rel = f"assets/flats/fx/stage/flat_fx_stage_{name}_bg{i}.png"
        size = (1500, 700) if huge_texture else (512, 512)
        layer_rgb = tuple(
            int(channel) + i * 3 if int(channel) + i * 3 <= 255
            else int(channel) - i * 3
            for channel in mural_rgb)
        _write_png(os.path.join(root, rel), size[0], size[1], layer_rgb,
                   1.0 if i >= alpha_murals else 0.5)
        mural_files.append(rel)
    rel = "assets/sprites/fx/standee_thing.png"
    _write_target_source_fixture(
        os.path.join(root, rel), fg_rgb, rendered_mode, fg_coverage)
    standee_files.append(rel)
    if extra_generation:
        old = "assets/sprites/fx/standee_thing_v2.png"
        _write_png(os.path.join(root, old), 256, 256, fg_rgb, fg_coverage)

    depth_src = "\n".join(f"const {n} := {v}" for n, v in depths) if depths else ""
    band_src = "const HALF_D := 2.6\nconst BAND_Y := -5.0\nconst BAND_H := 10.0\n" if band else ""
    if layers_api:
        stage_src = """\tvar root := Node2D.new()
\tvar camera := Camera2D.new()
\troot.add_child(camera)
\tvar layer := Sprite2D.new()
\troot.add_child(layer)
"""
    else:
        stage_src = """\tstage = SideScrollStage.new(m)
\tstage.open({
\t\t"layers": [],
\t\t"half_w": 72.0,
\t})
\tvar legacy_card := Sprite3D.new()
"""
    builder = f"""class_name FxStage
extends RefCounted
{band_src}{depth_src}

func build() -> void:
{stage_src}
	var fixture_shader := load("res://assets/shaders/fixture.gdshader")
	if fixture_shader == null:
		return
\t_add("res://{standee_files[0]}")
"""
    for m_rel in mural_files:
        builder += f'\t_add("res://{m_rel}")\n'
    with open(os.path.join(root, "scripts", "fx_stage.gd"), "w", encoding="utf-8") as fh:
        fh.write(builder)
    with open(os.path.join(root, "scripts", "ci.sh"), "w", encoding="utf-8") as fh:
        fh.write("for p in probe_fx; do :; done\n")
    with open(os.path.join(root, "scripts", "probe_fx.gd"), "w", encoding="utf-8") as fh:
        fh.write("extends SceneTree\n")
    shader_path = os.path.join(root, "assets", "shaders", "fixture.gdshader")
    os.makedirs(os.path.dirname(shader_path), exist_ok=True)
    with open(shader_path, "w", encoding="utf-8") as fh:
        fh.write("shader_type canvas_item;\nvoid fragment() { COLOR = texture(TEXTURE, UV); }\n")
    with open(os.path.join(root, "ASSET_LICENSES.md"), "w", encoding="utf-8") as fh:
        if licensed:
            for r in mural_files + standee_files:
                fh.write(f"- `{os.path.basename(r)}` — Codex original, CC0.\n")
        else:
            fh.write("(intentionally empty)\n")

    capture_rel = "audit/fixture_idle.png"
    hidden_rel = "audit/fixture_idle_target_hidden.png"
    restored_rel = "audit/fixture_idle_target_restored.png"
    mask_rel = "audit/fixture_idle_mask.png"
    hidden_stable_rels = [
        "audit/fixture_idle_target_hidden_stable.png",
        "audit/fixture_idle_target_hidden_repeat.png",
    ]
    visible_stable_rels = [
        "audit/fixture_idle_target_restored_stable.png",
        "audit/fixture_idle_target_restored_repeat.png",
    ]
    figure_rect, background_rect = _write_rendered_fixture(
        os.path.join(root, capture_rel), os.path.join(root, hidden_rel),
        os.path.join(root, restored_rel), os.path.join(root, mask_rel), rendered_mode)
    from PIL import Image
    for rel_path in hidden_stable_rels:
        with Image.open(os.path.join(root, hidden_rel)) as image:
            image.save(os.path.join(root, rel_path))
    for rel_path in visible_stable_rels:
        with Image.open(os.path.join(root, capture_rel)) as image:
            image.save(os.path.join(root, rel_path))
    builder_paths = ["scripts/fx_stage.gd"]
    art_paths = sorted(mural_files + standee_files)
    fixture_repo = Repo(root, {"budgets": {}, "rules": {}, "waivers": []})

    declared_layers = []
    for index in range(canvas_layer_count):
        if mural_files:
            asset_index = 0 if duplicate_canvas_assets else min(index, len(mural_files) - 1)
            assets = [mural_files[asset_index]]
        else:
            assets = []
        declared_layers.append({
            "id": f"L{index}", "role": f"fixture_{index}", "assets": assets,
        })
    runtime_layers = []
    for index, layer in enumerate(declared_layers):
        assets = sorted(layer["assets"])
        runtime_layers.append({
            "id": layer["id"],
            "instance_path": f"/root/Fx/L{index}",
            "node_type": "Node2D" if layers_api else "Sprite3D",
            "instantiated": True,
            "visible": True,
            "canvas_item": layers_api,
            "non_canvas_spatial_descendants": 0 if layers_api else 1,
            "assets": assets,
            "content_signature": asset_content_signature(fixture_repo, assets),
            "painted_composite_method": CANVAS_COMPOSITE_SIGNATURE_METHOD,
            "painted_composite_signature": asset_content_signature(
                fixture_repo, assets),
            "coverage_method": CANVAS_COVERAGE_METHOD,
            "screen_coverage_ratio": 0.85,
            "unresolved_alpha_effects": 0,
            "screen_delta_px": float(index * 12),
            "z_index": index,
            "draw_order": index,
            "draw_order_method": CANVAS_DRAW_ORDER_METHOD,
            "visual_draw_order_min": index,
            "visual_draw_order_max": index,
            "relative_z_min": 0,
            "relative_z_max": 0,
            "allowed_relative_z_min": 0,
            "allowed_relative_z_max": 0,
            "unresolved_draw_order_effects": 0,
        })
    subprocess.run(["git", "init", "-q", root], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "-C", root, "config", "user.name", "Visual Audit Fixture"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "-C", root, "config", "user.email", "fixture@example.invalid"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        "git", "-C", root, "add", "--", "scripts", "scenes", "assets",
        "project.godot", "tools/visual_audit_spec.json", "tools/audit_game_2d.py",
        "tools/audit_visual_design.py", "ASSET_LICENSES.md", ".gitignore",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", "fixture source"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    git_identity = git_source_identity(fixture_repo)
    builder_hashes = {path: fixture_repo.sha256(path) for path in builder_paths}
    source_revision = source_revision_signature(fixture_repo)
    run_nonce = "b" * 64
    fresh_challenge = "c" * 64
    run_started_utc = "2026-08-09T12:00:00Z"
    engine_string = "4.7.1-stable (official fixture)"
    run_identity = hashlib.sha256("|".join([
        git_identity["revision"], git_identity["tree"], fresh_challenge,
        source_revision, run_nonce, run_started_utc, engine_string, "mobile",
    ]).encode("utf-8")).hexdigest()
    runtime_contract = {
        "schema_version": RUNTIME_EVIDENCE_SCHEMA,
        "run_identity": run_identity,
        "run_nonce": run_nonce,
        "run_started_utc": run_started_utc,
        "fresh_challenge": fresh_challenge,
        "source_revision": source_revision,
        "git_revision": git_identity["revision"],
        "git_tree": git_identity["tree"],
        "git_dependencies_clean": git_identity["dependencies_clean"],
        "source_manifest": source_manifest_signature(fixture_repo),
        "files": {
            role: {"path": path, "sha256": fixture_repo.sha256(path)}
            for role, path in RUNTIME_EVIDENCE_FILES.items()
        },
        "engine": {
            "major": 4, "minor": 7, "patch": 1, "status": "stable",
            "version_string": engine_string,
        },
        "renderer": {"actual": "mobile", "project_setting": "mobile"},
        "capture_context": {
            "viewport": [1280, 720], "stretch_mode": "canvas_items",
            "stretch_aspect": "expand",
        },
    }
    occlusion_samples = []
    if layers_api and len(runtime_layers) >= 2:
        occlusion_samples = [{
            "id": "standee",
            "target_instance_path": "/root/Fx/StandeeTarget/Visual",
            "target_canvas_item": True,
            "target_visible": True,
            "target_draw_order": 0.5,
            "behind": [{"instance_path": runtime_layers[0]["instance_path"],
                        "draw_order": runtime_layers[0]["draw_order"],
                        "overlap_px2": 6144.0,
                        "painted_sample_count": 384,
                        "target_painted_sample_count": 512,
                        "target_overlap_ratio": 0.75,
                        "alpha_threshold": 0.5,
                        "unresolved_alpha_effects": 0,
                        "overlap_method": CANVAS_OCCLUSION_METHOD,
                        "sample_step_px": 4.0}],
            "front": [{"instance_path": runtime_layers[1]["instance_path"],
                       "draw_order": runtime_layers[1]["draw_order"],
                       "overlap_px2": 6144.0,
                       "painted_sample_count": 384,
                       "target_painted_sample_count": 512,
                       "target_overlap_ratio": 0.75,
                       "alpha_threshold": 0.5,
                       "unresolved_alpha_effects": 0,
                       "overlap_method": CANVAS_OCCLUSION_METHOD,
                       "sample_step_px": 4.0}],
        }]
    touch_radius = 55.0
    touch_diagonal = round(touch_radius / math.sqrt(2.0), 1)
    touch_offsets = [
        (0.0, 0.0), (touch_radius, 0.0), (-touch_radius, 0.0),
        (0.0, touch_radius), (0.0, -touch_radius),
        (touch_diagonal, touch_diagonal), (touch_diagonal, -touch_diagonal),
        (-touch_diagonal, touch_diagonal), (-touch_diagonal, -touch_diagonal),
    ]
    touch_reach_samples = [{
        "offset_px": [offset_x, offset_y],
        "screen_px": [round(640.0 + offset_x, 1), round(360.0 + offset_y, 1)],
        "returned_id": "standee",
        "inside_viewport": True,
        "matches_target": True,
    } for offset_x, offset_y in touch_offsets]
    runtime_facts = {
        "evidence_contract": runtime_contract,
        "zones": {"fx": {
            "zone_id": "fx",
            "root_instance_path": "/root/Fx",
            "builder_sha256": builder_hashes,
            "run_identity": run_identity,
            "targets": [{"id": "standee", "screen_px": 120.0,
                         "hit_diameter_px": 120.0,
                         "visual_screen_px": 64.0,
                         "visual_width_px": 96.0,
                         "visual_screen_rect": [592.0, 328.0, 96.0, 64.0],
                         "instance_path": "/root/Fx/StandeeTarget",
                         "audited_viewport": True,
                         "visible_canvas_visual_count": 1,
                         "interaction_registry": "lagoon_promenade_targets_v1",
                         "resolver_method": "production_target_at_radial_reach_v2",
                         "resolver_hit_screen_px": [640.0, 360.0],
                         "resolver_returned_id": "standee",
                         "resolver_hit_confirmed": True,
                         "resolver_reach_radius_px": touch_radius,
                         "resolver_reach_samples": touch_reach_samples,
                         "resolver_center_in_viewport": True,
                         "resolver_nearest_painted_px": 0.0,
                         "meets_min_touch": True}],
            "canvas_parallax": {
                "backend": "canvas_2d" if layers_api else "legacy_spatial",
                "root_canvas_item": layers_api,
                "non_canvas_spatial_nodes": 0 if layers_api else 1,
                "camera_sample_px": 240.0,
                "motion_method": CANVAS_MOTION_METHOD,
                "zone_id": "fx",
                "root_instance_path": "/root/Fx",
                "builder_sha256": builder_hashes,
                "run_identity": run_identity,
                "layers": runtime_layers,
            },
            "canvas_occlusion": {
                "backend": "canvas_2d" if layers_api else "legacy_spatial",
                "non_canvas_spatial_nodes": 0 if layers_api else 1,
                "method": CANVAS_OCCLUSION_METHOD,
                "zone_id": "fx",
                "root_instance_path": "/root/Fx",
                "builder_sha256": builder_hashes,
                "run_identity": run_identity,
                "unresolved_alpha_effects": 0,
                "unresolved_draw_order_effects": 0,
                "samples": occlusion_samples,
            },
            "rendered_composites": [{
                "id": "idle",
                "capture_adapter": "probe_visual_audit:fx_idle",
                "adapter_method": "explicit_live_state_assertions_v1",
                "adapter_state": {"fixture": "idle", "zone": "fx"},
                "adapter_state_signature": hashlib.sha256(json.dumps(
                    {"fixture": "idle", "zone": "fx"}, sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")).hexdigest(),
                "source": "viewport_composite",
                "capture_path": capture_rel,
                "capture_sha256": fixture_repo.sha256(capture_rel),
                "viewport": [1280, 720],
                "zone_id": "fx",
                "root_instance_path": "/root/Fx",
                "builder_sha256": builder_hashes,
                "run_identity": run_identity,
                "provenance": {
                    "builder_sha256": builder_hashes,
                    "art_sha256": {path: fixture_repo.sha256(path)
                                   for path in art_paths},
                },
                "samples": [{
                    "id": "standee",
                    "target_instance_path": "/root/Fx/StandeeTarget",
                    "visuals": [{
                        "instance_path": "/root/Fx/StandeeTarget/Visual",
                        "node_type": "Sprite2D",
                        "visible_in_tree": True,
                        "texture_path": standee_files[0],
                        "texture_sha256": fixture_repo.sha256(standee_files[0]),
                        "canvas_transform": [0.375, 0.0, 0.0, 0.25, 640.0, 360.0],
                        "local_rect": [-128.0, -128.0, 256.0, 256.0],
                        "projection": {
                            "kind": "Sprite2D", "region_enabled": False,
                            "region_rect": [0.0, 0.0, 256.0, 256.0],
                            "hframes": 1, "vframes": 1, "frame_coords": [0, 0],
                            "flip_h": False, "flip_v": False, "centered": True,
                            "offset": [0.0, 0.0],
                        },
                    }],
                    "figure_rect": figure_rect,
                    "background_rect": background_rect,
                    "target_hidden_source": "viewport_composite_target_hidden",
                    "target_hidden_capture_path": hidden_rel,
                    "target_hidden_capture_sha256": fixture_repo.sha256(hidden_rel),
                    "target_hidden_stability_captures": [
                        {"path": path, "sha256": fixture_repo.sha256(path)}
                        for path in hidden_stable_rels
                    ],
                    "target_restored_source": "viewport_composite_target_restored",
                    "target_restored_capture_path": restored_rel,
                    "target_restored_capture_sha256": fixture_repo.sha256(restored_rel),
                    "target_visible_stability_captures": [
                        {"path": path, "sha256": fixture_repo.sha256(path)}
                        for path in visible_stable_rels
                    ],
                    "temporal_schedule_frames": [1, 2, 1, 3, 2, 1],
                    "temporal_freeze_method": TEMPORAL_FREEZE_METHOD,
                    "shader_time_scale": 0.0,
                    "mask_path": mask_rel,
                    "mask_sha256": fixture_repo.sha256(mask_rel),
                    "mask_source": RENDERED_DIFF_METHOD,
                    "projection_method": SOURCE_PROJECTION_METHOD,
                    "mask_source_art": [standee_files[0]],
                    "mask_source_sha256": {
                        standee_files[0]: fixture_repo.sha256(standee_files[0]),
                    },
                }],
            }],
        }},
    }

    fixture_result = {
        "version": 6,
        "rules": load_spec().get("rules", {}),
        "budgets": load_spec().get("budgets", {}),
        "zones": [{
            "id": "fx", "name": "Fixture", "art_medium": "flattened_2d",
            "presentation": presentation, "lifecycle": lifecycle,
            "builders": ["scripts/fx_stage.gd"], "probes": ["scripts/probe_fx.gd"],
            "murals": mural_files, "standees": standee_files, "characters": [],
            "canvas_layers": declared_layers,
            "rendered_readability_states": [{
                "id": "idle", "capture_adapter": "probe_visual_audit:fx_idle",
                "required_targets": ["standee"],
            }],
            "asset_roots": ["assets/flats/fx", "assets/sprites/fx"],
            "budgets": zone_budgets or {},
        }],
        "waivers": [],
        "_runtime_facts": runtime_facts,
    }
    attestation_repo = Repo(root, fixture_result, runtime_facts)
    fixture_result["_fresh_attestation"] = attest_fresh_runtime_response(
        attestation_repo, fixture_result, runtime_facts, fresh_challenge,
        os.path.join(root, "audit"))
    return fixture_result


# (check_id, fixture kwargs, expected severity) — each row must make the named
# check fire.  Adding a check without adding a row here fails the stress run.
STRESS_CASES: list[tuple[str, dict, str]] = [
    ("texture.pot_or_small", {"huge_texture": True}, ERROR),
    ("texture.vram_compressible", {"murals": 2, "huge_texture": True}, WARN),
    ("texture.zone_budget", {"zone_budgets": {"zone_runtime_texture_mb": 0.05}}, ERROR),
    ("texture.import_sidecar", {}, WARN),
    ("layering.legacy_3d_debt", {"presentation": "legacy_3d_debt"}, ERROR),
    ("layering.mural_is_a_stack", {"murals": 4, "canvas_layer_count": 1}, ERROR),
    ("layering.engine_layer_api", {"layers_api": False}, ERROR),
    ("layering.depth_spread", {"depths": (("DRESS_Z", -17.9), ("PLAY_Z", -17.8))}, ERROR),
    ("layering.occlusion_band", {"depths": (("DRESS_Z", -17.9), ("PLAY_Z", -17.8))}, ERROR),
    ("layering.standee_alpha", {"fg_coverage": 1.0}, WARN),
    ("palette.background_recessive", {"mural_rgb": (0, 255, 255),
                                      "fg_rgb": (150, 150, 155),
                                      "rendered_mode": "low_all_channels"}, WARN),
    ("palette.figure_ground_luminance", {"mural_rgb": (128, 128, 128),
                                         "fg_rgb": (128, 128, 128),
                                         "rendered_mode": "low_all_channels"}, WARN),
    ("palette.rendered_composite_readability", {"rendered_mode": "low_all_channels"}, ERROR),
    ("overdraw.alpha_layers", {"murals": 4, "alpha_murals": 4,
                               "mural_layer_names": ("L0", "L1", "L2", "L3")}, ERROR),
    ("charter.probe_gated", {}, WARN),
    ("hygiene.orphan_art", {"extra_generation": True}, INFO),
    ("hygiene.superseded_generations", {"extra_generation": True}, WARN),
    ("hygiene.license_line", {"licensed": False}, ERROR),
]


def stress(fuzz: int = 0, verbose: bool = False) -> int:
    """Prove each check fires on a fixture built to violate it. Returns exit code."""
    failures: list[str] = []
    stressable = {cid for cid, c in REGISTRY.items() if c.stressable}
    covered = {cid for cid, _kw, _sev in STRESS_CASES}
    for missing in sorted(stressable - covered):
        failures.append(f"STRESS GAP: {missing} has no case in STRESS_CASES — "
                        f"a check nobody proved can fail")

    for cid, kwargs, expect in STRESS_CASES:
        if cid not in REGISTRY:
            failures.append(f"STRESS STALE: {cid} is no longer a registered check")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            spec = _fixture(tmp, **kwargs)
            if cid == "charter.probe_gated":
                with open(os.path.join(tmp, "scripts", "ci.sh"), "w", encoding="utf-8") as fh:
                    fh.write("for p in probe_other; do :; done\n")
            repo = Repo(tmp, spec, spec.get("_runtime_facts"),
                        spec.get("_fresh_attestation"))
            got = [f for f in run(repo, check_ids=[cid]) if f.check == cid]
            sevs = {f.severity for f in got}
            if expect not in sevs:
                failures.append(f"STRESS FAIL: {cid} expected {expect}, got "
                                f"{sorted(sevs) or ['nothing']}")
            elif verbose:
                print(f"  ok  {cid} -> {expect}")

        # negative control: a clean fixture must not raise this check above INFO
        if cid in ("texture.import_sidecar", "hygiene.orphan_art", "charter.probe_gated",
                   "layering.engine_layer_api"):
            continue        # these fire on any minimal fixture by construction
        with tempfile.TemporaryDirectory() as tmp:
            clean = _fixture(tmp, murals=3, mural_layer_names=("L0", "L1", "L2"),
                             mural_rgb=(180, 190, 200), fg_rgb=(255, 90, 60),
                             depths=(("BACKDROP_Z", -18.0), ("DRESS_Z", -6.0),
                                     ("PLAY_Z", 0.5), ("NEAR_Z", 2.0)),
                             layers_api=True, alpha_murals=1, fg_coverage=0.4,
                             canvas_layer_count=3)
            repo = Repo(tmp, clean, clean.get("_runtime_facts"),
                        clean.get("_fresh_attestation"))
            noisy = [f for f in run(repo, check_ids=[cid])
                     if f.check == cid and f.severity in (ERROR, WARN)]
            if noisy:
                failures.append(f"STRESS FALSE-POSITIVE: {cid} fired on a clean fixture: "
                                f"{noisy[0].message[:120]}")

    for i in range(fuzz):
        rng = random.Random(1000 + i)
        with tempfile.TemporaryDirectory() as tmp:
            spec = _fixture(
                tmp,
                murals=rng.randint(0, 5),
                mural_rgb=(rng.randrange(256), rng.randrange(256), rng.randrange(256)),
                fg_rgb=(rng.randrange(256), rng.randrange(256), rng.randrange(256)),
                depths=tuple((f"L{j}_Z", round(rng.uniform(-20, 5), 2))
                             for j in range(rng.randint(0, 4))),
                band=rng.random() < 0.8,
                fg_coverage=rng.random(),
                alpha_murals=rng.randint(0, 5),
                presentation=rng.choice(sorted(FLAT_PRESENTATIONS) + ["free_swim", "ui"]),
            )
            try:
                crashes = [f for f in run(Repo(
                    tmp, spec, spec.get("_runtime_facts"),
                    spec.get("_fresh_attestation")))
                           if "check crashed" in f.message]
            except Exception as exc:                              # noqa: BLE001
                failures.append(f"FUZZ CRASH seed {1000 + i}: {type(exc).__name__}: {exc}")
                continue
            for c in crashes:
                failures.append(f"FUZZ CRASH seed {1000 + i}: {c.check}: {c.message}")

    print(f"VISUALAUDIT| stress: {len(STRESS_CASES)} cases, "
          f"{len(stressable)} stressable checks, {fuzz} fuzz rounds")
    for msg in failures:
        print(f"  {msg}")
    if failures:
        print("VISUALAUDIT| stress: FAIL")
        return 1
    print("VISUALAUDIT| stress: ALL OK")
    return 0


# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    configure_console()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", default=SPEC_PATH)
    ap.add_argument("--zone", action="append", help="limit to zone id (repeatable)")
    ap.add_argument("--check", action="append", help="limit to check id (repeatable)")
    ap.add_argument("--category", action="append", help="limit to a check category")
    ap.add_argument(
        "--strict", action="store_true",
        help="require a complete audit: no fail, review, manual-open, or coverage-gap result",
    )
    ap.add_argument("--max-warn", type=int, default=None,
                    help="exit nonzero above this many WARNs")
    ap.add_argument("--format", choices=("console", "json", "md"), default="console")
    ap.add_argument(
        "--runtime-facts", default=RUNTIME_FACTS_PATH,
        help="saved runtime-facts JSON for diagnostics only; it has no PASS authority",
    )
    ap.add_argument(
        "--fresh-runtime", action="store_true",
        help="launch the exact Godot probe with a random one-use challenge; required "
             "for runtime/capture PASS authority",
    )
    ap.add_argument(
        "--godot", default=None,
        help="Godot executable for --fresh-runtime (else $GODOT, godot, or godot4)",
    )
    ap.add_argument("--verbose", "-v", action="store_true", help="show INFO and SKIP too")
    ap.add_argument("--list-checks", action="store_true")
    ap.add_argument("--stress", action="store_true", help="self-test every check")
    ap.add_argument("--fuzz", type=int, default=24, help="fuzz rounds during --stress")
    ap.add_argument("--no-report", action="store_true", help="skip writing audit/ files")
    args = ap.parse_args(argv)

    if args.list_checks:
        for cid in sorted(REGISTRY):
            c = REGISTRY[cid]
            presentations = (",".join(sorted(c.presentations))
                             if c.presentations else "all")
            print(f"{cid:38s} [{c.category:10s}] "
                  f"presentations={presentations:38s} {c.doc}")
        return 0

    if args.stress:
        return stress(fuzz=args.fuzz, verbose=args.verbose)

    spec = load_spec(args.spec)
    runtime = {}
    fresh_attestation = None
    fresh_tmp = None
    if args.fresh_runtime:
        godot = args.godot or os.environ.get("GODOT") \
            or shutil.which("godot") or shutil.which("godot4")
        if not godot:
            print("warning: --fresh-runtime cannot find Godot; runtime checks will "
                  "report COVERAGE_GAP", file=sys.stderr)
        else:
            godot = shutil.which(godot) or os.path.abspath(godot)
            console_candidate = os.path.join(
                os.path.dirname(os.path.abspath(godot)), "godot_console.exe")
            if os.name == "nt" and os.path.isfile(console_candidate):
                godot = console_candidate
            try:
                version_check = subprocess.run(
                    [godot, "--version"], cwd=REPO, check=False,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                    encoding="utf-8", errors="replace", timeout=30,
                )
                version_text = version_check.stdout.strip()
                if version_check.returncode != 0 or re.match(
                        r"^4\.7\.1(?:[.-])stable(?:[.-]official)?(?:\b|\s|\()",
                        version_text) is None:
                    raise ValueError(
                        f"configured Godot is not exactly 4.7.1-stable: {version_text!r}")
                challenge = secrets.token_hex(32)
                fresh_tmp = tempfile.TemporaryDirectory(prefix="reef-visual-audit-")
                facts_path = os.path.join(fresh_tmp.name, "visual_runtime_facts.json")
                command = [
                    godot, "--path", REPO, "--rendering-method", "mobile",
                    "--windowed", "--resolution", "1280x720",
                    "-s", "scripts/probe_visual_audit.gd", "--",
                    f"--visual-facts-out={facts_path.replace(os.sep, '/')}",
                    f"--visual-audit-challenge={challenge}",
                ]
                completed = subprocess.run(
                    command, cwd=REPO, check=False, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                    errors="replace", timeout=180,
                )
                if args.verbose and completed.stdout:
                    print(completed.stdout.rstrip(), file=sys.stderr)
                if completed.returncode != 0 or not os.path.isfile(facts_path):
                    print(
                        f"warning: fresh Godot probe failed ({completed.returncode}); "
                        "runtime checks will report COVERAGE_GAP", file=sys.stderr)
                else:
                    with open(facts_path, "r", encoding="utf-8") as fh:
                        runtime = json.load(fh)
                    probe_challenge = str(
                        (runtime.get("evidence_contract") or {}).get(
                            "fresh_challenge", ""))
                    if not secrets.compare_digest(probe_challenge, challenge):
                        print("warning: fresh Godot probe returned the wrong one-use "
                              "challenge", file=sys.stderr)
                    else:
                        attestation_repo = Repo(REPO, spec, runtime)
                        fresh_attestation = attest_fresh_runtime_response(
                            attestation_repo, spec, runtime, challenge,
                            os.path.join(fresh_tmp.name, "visual_runtime_captures"),
                            godot)
            except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError,
                    ValueError) as exc:
                print(f"warning: fresh Godot probe unavailable ({exc}); runtime checks "
                      "will report COVERAGE_GAP", file=sys.stderr)
        # Captures with PASS authority now live only in immutable process memory.
        # Deleting the challenged response closes path substitution and TOCTOU.
        if fresh_tmp is not None:
            fresh_tmp.cleanup()
            fresh_tmp = None
    elif os.path.exists(args.runtime_facts):
        try:
            with open(args.runtime_facts, "r", encoding="utf-8") as fh:
                runtime = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"warning: runtime facts unreadable ({exc}); "
                  "scene checks will report COVERAGE_GAP",
                  file=sys.stderr)

    repo = Repo(REPO, spec, runtime, fresh_attestation)
    check_ids = list(args.check or [])
    if args.category:
        check_ids += [cid for cid, c in REGISTRY.items() if c.category in args.category]
    findings = run(repo, zone_ids=args.zone, check_ids=check_ids or None)

    if args.format == "console":
        print_console(findings, args.verbose)
    elif args.format == "json":
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        for f in findings:
            if f.disposition not in (PASS, NOT_APPLICABLE) or args.verbose:
                print(f"- **{f.severity}/{f.disposition}** `{f.zone}` "
                      f"`{f.check}` — {f.message}")

    if not args.no_report:
        write_reports(findings, repo)

    warns = sum(1 for f in findings
                if f.severity == WARN and f.disposition == REVIEW_OPEN)
    exit_code = 0
    if args.strict and not strict_passes(findings):
        exit_code = 1
    if args.max_warn is not None and warns > args.max_warn:
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
