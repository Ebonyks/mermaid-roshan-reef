#!/usr/bin/env python3
"""Game-wide visual design audit for Mermaid Roshan: Reef of Light.

Why this exists
---------------
The 2026-07-27 redesign charter turned the game into a set of 2.5D promenade
stages whose look is carried by Codex-painted flats.  That charter and its
work order contain a dozen numeric, checkable promises — parallax layer
counts, depth spread, alpha-layer overdraw budgets, the contrast rule that
keeps backgrounds recessive, texture legality, reversibility toggles.  Written
promises rot silently.  This tool turns each of them into a check that fails
out loud.

Design contract (read before extending)
---------------------------------------
1.  Every check maps to a named rule in ``tools/visual_audit_spec.json``.
    A check with no rule behind it is an opinion, and opinions do not gate.
2.  Every check is a pure function of (zone, repo, runtime_facts) -> findings.
    No check may mutate the repo.
3.  A check that cannot run (missing runtime facts, missing asset class)
    reports SKIP with a reason.  Silence is never a pass.
4.  Every check must be provably falsifiable: ``--stress`` builds a synthetic
    zone engineered to violate it and asserts the check fires.  A check that
    survives the stress pass unfired is a broken check and the stress run
    fails.

Usage
-----
    python3 tools/audit_visual_design.py                 # advisory, all zones
    python3 tools/audit_visual_design.py --zone sky_lagoon
    python3 tools/audit_visual_design.py --strict        # nonzero on ERROR
    python3 tools/audit_visual_design.py --list-checks
    python3 tools/audit_visual_design.py --stress        # self-test the checks
    python3 tools/audit_visual_design.py --format json

Runtime facts (optional, produced by scripts/probe_visual_audit.gd) are read
from ``audit/visual_runtime_facts.json``.  Static checks run without them;
scene-graph checks SKIP without them.
"""

from __future__ import annotations

import argparse
import glob as globlib
import json
import math
import os
import random
import re
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from typing import Callable, Iterable, Iterator

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_PATH = os.path.join(REPO, "tools", "visual_audit_spec.json")
RUNTIME_FACTS_PATH = os.path.join(REPO, "audit", "visual_runtime_facts.json")
REPORT_JSON = os.path.join(REPO, "audit", "visual_design_report.json")
REPORT_MD = os.path.join(REPO, "audit", "visual_design_report.md")
LICENSES = os.path.join(REPO, "ASSET_LICENSES.md")

ERROR, WARN, INFO, MANUAL, SKIP = "ERROR", "WARN", "INFO", "MANUAL", "SKIP"
SEVERITY_ORDER = {ERROR: 0, WARN: 1, MANUAL: 2, INFO: 3, SKIP: 4}

# Media that are expected to carry a painted flat stack.  Layering and palette
# checks only mean something for these; a free-swim 3D zone is not failing the
# mural rules, it simply has not migrated yet.
FLAT_MEDIA = {"promenade_2p5d", "staged_2d", "overhead_2d"}

# The parallax/occlusion rules are specific to the side-on promenade: it is the
# only medium where the camera pans across a set and the player moves through a
# depth band.  The charter (§2 'Minigame inventory') declares overhead and
# staged fixed-camera modes already compliant, so holding them to a layer stack
# would be the tool inventing a rule nobody wrote.
PARALLAX_MEDIA = {"promenade_2p5d"}


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

    def key(self) -> tuple:
        return (SEVERITY_ORDER.get(self.severity, 9), self.check, self.zone)


@dataclass
class Check:
    id: str
    category: str
    rule: str
    doc: str
    fn: Callable
    media: set | None = None     # None = every medium
    stressable: bool = True      # False only for checks with no synthetic form


REGISTRY: dict[str, Check] = {}


def check(check_id: str, category: str, rule: str, media: Iterable[str] | None = None,
          stressable: bool = True):
    """Register an audit check.  ``rule`` must name a key in spec['rules']."""

    def deco(fn: Callable) -> Callable:
        REGISTRY[check_id] = Check(
            id=check_id, category=category, rule=rule,
            doc=(fn.__doc__ or "").strip().split("\n")[0],
            fn=fn, media=set(media) if media else None, stressable=stressable,
        )
        return fn

    return deco


# --------------------------------------------------------------------------
# repo access — everything a check is allowed to look at
# --------------------------------------------------------------------------

class Repo:
    """Read-only, cached view of the repository for the checks."""

    def __init__(self, root: str, spec: dict, runtime_facts: dict | None = None):
        self.root = root
        self.spec = spec
        self.budgets = spec.get("budgets", {})
        self.runtime = runtime_facts or {}
        self._img_cache: dict[str, dict] = {}
        self._text_cache: dict[str, str] = {}
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


class Zone:
    """One audited zone, resolved against the repo."""

    def __init__(self, raw: dict, repo: Repo):
        self.raw = raw
        self.repo = repo
        self.id = raw["id"]
        self.name = raw.get("name", raw["id"])
        self.medium = raw.get("medium", "unknown")
        self.status = raw.get("status", "unknown")
        self.charter_order = raw.get("charter_order")
        self.supersedes = raw.get("supersedes")
        self.reversibility_key = raw.get("reversibility_key")
        self.builders = raw.get("builders", [])
        self.probes = raw.get("probes", [])
        self.murals = repo.expand(raw.get("murals", []))
        self.standees = repo.expand(raw.get("standees", []))
        self.characters = repo.expand(raw.get("characters", []))
        self.asset_roots = raw.get("asset_roots", [])

    @property
    def foreground(self) -> list[str]:
        return self.standees + self.characters

    @property
    def runtime_art(self) -> list[str]:
        return self.murals + self.standees + self.characters

    def budget(self, name: str, default=None):
        return self.raw.get("budgets", {}).get(name, self.repo.budgets.get(name, default))

    def runtime_facts(self) -> dict | None:
        return (self.repo.runtime.get("zones") or {}).get(self.id)


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
    """A zone's runtime art stays inside its uncompressed-texture budget."""
    art = zone.runtime_art
    if not art:
        yield Finding("texture.zone_budget", zone.id, SKIP, "no runtime PNG art")
        return
    # On the Mali GPU a power-of-two texture block-compresses to ~8 bpp
    # (ETC2/ASTC 4x4); a non-power-of-two one cannot compress and costs the
    # full 32 bpp.  Budget against the realistic on-device cost, not the
    # decoded size, or every zone looks over budget and the check gets ignored.
    decoded = 0
    vram = 0
    for rel in art:
        info = zone.repo.image(rel)
        b = info.get("rgba_bytes", 0)
        decoded += b
        vram += b // 4 if info.get("pot") else b
    decoded /= 1048576.0
    vram /= 1048576.0
    cap = float(zone.budget("zone_runtime_texture_mb", 24.0))
    sev = ERROR if vram > cap * 1.5 else (WARN if vram > cap else INFO)
    yield Finding("texture.zone_budget", zone.id, sev,
                  f"runtime art costs ~{vram:.1f} MB of VRAM on the M11 "
                  f"({decoded:.1f} MB decoded, budget {cap:.0f} MB)",
                  evidence={"vram_mb": round(vram, 2), "decoded_mb": round(decoded, 2),
                            "budget_mb": cap, "files": len(art)})


# --------------------------------------------------------------------------
# CHECKS — the layering rule (the heart of the redesign)
# --------------------------------------------------------------------------

@check("layering.mural_is_a_stack", "layering", "mural_layer_stack", media=PARALLAX_MEDIA)
def _mural_stack(zone: Zone) -> Iterator[Finding]:
    """A promenade's background is a parallax stack, never a single painting."""
    if not zone.murals:
        yield Finding("layering.mural_is_a_stack", zone.id, SKIP,
                      "zone declares no murals")
        return
    need = int(zone.budget("mural_min_layers", 2))
    # Layers are distinguished by their L-index in the work order naming, not by
    # tile count: four side-by-side tiles of one panorama are ONE layer.
    layers = set()
    for rel in zone.murals:
        base = os.path.basename(rel)
        hit = re.search(r"_(L\d)_", base)
        layers.add(hit.group(1) if hit else "L?")
    if len(layers) >= need:
        yield Finding("layering.mural_is_a_stack", zone.id, INFO,
                      f"{len(layers)} distinct mural layers: {sorted(layers)}")
        return
    yield Finding("layering.mural_is_a_stack", zone.id, ERROR,
                  f"background is {len(layers)} layer(s) across {len(zone.murals)} file(s) — "
                  f"the charter requires >={need} parallax layers. Side-by-side tiles of one "
                  f"panorama are one layer, so this stage has no parallax at all",
                  evidence={"layers": sorted(layers), "files": zone.murals})


@check("layering.engine_layer_api", "layering", "mural_layer_stack", media=PARALLAX_MEDIA)
def _engine_layers(zone: Zone) -> Iterator[Finding]:
    """A flat-medium zone feeds its murals through SideScrollStage's layers stack."""
    if not zone.builders:
        yield Finding("layering.engine_layer_api", zone.id, SKIP, "zone declares no builder")
        return
    src = "\n".join(zone.repo.read(b) for b in zone.builders)
    if not src.strip():
        yield Finding("layering.engine_layer_api", zone.id, SKIP, "builder sources unreadable")
        return
    uses_stage = "SideScrollStage" in src or "stage.open(" in src
    uses_layers = re.search(r'"layers"\s*:', src) is not None
    if not uses_stage:
        yield Finding("layering.engine_layer_api", zone.id, INFO,
                      "zone does not build on SideScrollStage")
        return
    if uses_layers:
        yield Finding("layering.engine_layer_api", zone.id, INFO,
                      "murals go through the engine layer stack")
        return
    yield Finding("layering.engine_layer_api", zone.id, WARN,
                  "builds on SideScrollStage but never passes \"layers\": the engine's "
                  "camera-locked parallax stack is bypassed by hand-placed backdrop cards, "
                  "so lock factors and per-layer glide are unavailable to this zone",
                  evidence={"builders": zone.builders})


@check("layering.depth_spread", "layering", "layering_rule", media=PARALLAX_MEDIA)
def _depth_spread(zone: Zone) -> Iterator[Finding]:
    """World cards occupy distinct depths, not one welded plane."""
    if not zone.builders:
        yield Finding("layering.depth_spread", zone.id, SKIP, "zone declares no builder")
        return
    depths: dict[str, float] = {}
    for b in zone.builders:
        for name, value in zone.repo.const_floats(b).items():
            if name.endswith("_Z") or name == "BACKDROP_Z":
                depths[f"{os.path.basename(b)}:{name}"] = value
    if len(depths) < 2:
        yield Finding("layering.depth_spread", zone.id, SKIP,
                      "fewer than two *_Z depth constants found in the builder "
                      "(static parse only sees `const NAME := <float>`)")
        return
    values = sorted(depths.values())
    # the backdrop's own plane is the reference; the spread that matters is
    # among the CARDS that stand in front of it
    spread = values[-1] - values[0]
    need = float(zone.budget("world_card_min_depth_spread", 2.0))
    if spread >= need:
        yield Finding("layering.depth_spread", zone.id, INFO,
                      f"world card depths span {spread:.2f} units",
                      evidence={"depths": depths})
        return
    yield Finding("layering.depth_spread", zone.id, ERROR,
                  f"every world card sits within {spread:.2f} units of depth "
                  f"(need >={need:.1f}): the cards are welded to one plane, so the stage "
                  f"parallaxes as a single painting and reads flat when the lens pans",
                  evidence={"depths": depths, "spread": round(spread, 3)})


@check("layering.occlusion_band", "layering", "layering_rule", media=PARALLAX_MEDIA)
def _occlusion(zone: Zone) -> Iterator[Finding]:
    """The walk band overlaps the standee depths so Roshan can pass BEHIND things."""
    if not zone.builders:
        yield Finding("layering.occlusion_band", zone.id, SKIP, "zone declares no builder")
        return
    consts: dict[str, float] = {}
    for b in zone.builders:
        consts.update(zone.repo.const_floats(b))
    card_z = [v for k, v in consts.items() if k.endswith("_Z") and k != "BACKDROP_Z"]
    band_y = consts.get("BAND_Y")
    band_h = consts.get("BAND_H")
    hover = consts.get("HALF_D")
    if not card_z or band_h is None:
        yield Finding("layering.occlusion_band", zone.id, SKIP,
                      "builder does not declare both card depths and a BAND_H")
        return
    # Roshan's band is centred on the stage origin with half-depth HALF_D; the
    # cards are at *_Z.  If every card is deeper than the band's far edge she
    # can only ever walk in front of the scenery.
    far_edge = -(hover if hover is not None else band_h * 0.5)
    behind = [z for z in card_z if z < far_edge]
    if len(behind) < len(card_z):
        yield Finding("layering.occlusion_band", zone.id, INFO,
                      f"{len(card_z) - len(behind)}/{len(card_z)} card depths sit inside or "
                      f"in front of the walk band")
        return
    yield Finding("layering.occlusion_band", zone.id, ERROR,
                  f"all {len(card_z)} world-card depths are behind the walk band "
                  f"(deepest band edge {far_edge:.2f}): Roshan passes in front of every "
                  f"object in the stage and can never be occluded — the depth-sorted "
                  f"'2D designs at real depth' rule is not being exercised",
                  evidence={"card_depths": sorted(card_z), "band_far_edge": far_edge,
                            "band_y": band_y, "band_h": band_h})


@check("layering.standee_alpha", "layering", "standee_not_mural", media=FLAT_MEDIA)
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

@check("palette.background_recessive", "palette", "background_recessive", media=FLAT_MEDIA)
def _background_recessive(zone: Zone) -> Iterator[Finding]:
    """Backgrounds frame; they never out-saturate the things a finger should find."""
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
                      f"background saturation {bg_s:.3f} vs foreground {fg_s:.3f} "
                      f"(ratio {ratio:.2f}, cap {cap:.2f})")
        return
    sev = ERROR if ratio > 1.0 else WARN
    yield Finding("palette.background_recessive", zone.id, sev,
                  f"background saturation {bg_s:.3f} vs foreground {fg_s:.3f} — the painted "
                  f"scenery is {ratio:.2f}x the saturation of the characters and tap targets "
                  f"standing on it. The contrast rule is inverted: the eye is pulled to the "
                  f"mural, not to the things the child is supposed to touch",
                  evidence={"background_saturation": round(bg_s, 4),
                            "foreground_saturation": round(fg_s, 4),
                            "ratio": round(ratio, 3), "cap": cap,
                            "murals": zone.murals, "foreground": zone.foreground})


@check("palette.figure_ground_luminance", "palette", "background_recessive", media=FLAT_MEDIA)
def _luminance(zone: Zone) -> Iterator[Finding]:
    """Foreground art separates from the mural in luminance, not just in hue."""
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
                      f"figure/ground luminance delta {delta:.3f}")
        return
    yield Finding("palette.figure_ground_luminance", zone.id, WARN,
                  f"figure/ground luminance delta is only {delta:.3f} (need {need:.3f}): "
                  f"standees sit at the same brightness as the painting behind them, so a "
                  f"squint test at M11 size loses their silhouettes",
                  evidence={"background_luminance": round(bg_l, 4),
                            "foreground_luminance": round(fg_l, 4),
                            "delta": round(delta, 4)})


@check("overdraw.alpha_layers", "overdraw", "alpha_layer_budget", media=FLAT_MEDIA)
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


@check("readability.tap_target_size", "readability", "layering_rule", stressable=False)
def _tap_targets(zone: Zone) -> Iterator[Finding]:
    """Every tap target clears the 110px minimum touch size at 1280x720 base."""
    facts = zone.runtime_facts()
    if not facts or "targets" not in facts:
        yield Finding("readability.tap_target_size", zone.id, SKIP,
                      "needs runtime facts — run scripts/probe_visual_audit.gd "
                      f"to produce {os.path.relpath(RUNTIME_FACTS_PATH, REPO)}")
        return
    small = [t for t in facts["targets"] if float(t.get("screen_px", 0)) < 110.0]
    for t in small:
        yield Finding("readability.tap_target_size", zone.id, WARN,
                      f"target '{t.get('id')}' projects to {float(t.get('screen_px', 0)):.0f}px "
                      f"— under the 110px storybook minimum",
                      evidence=t)
    if not small:
        yield Finding("readability.tap_target_size", zone.id, INFO,
                      f"{len(facts['targets'])} tap targets clear 110px")


# --------------------------------------------------------------------------
# CHECKS — charter compliance
# --------------------------------------------------------------------------

@check("charter.reversibility_toggle", "charter", "reversibility")
def _reversibility(zone: Zone) -> Iterator[Finding]:
    """A zone that replaced a shipped mode is reachable behind a save-key toggle."""
    if not zone.supersedes:
        yield Finding("charter.reversibility_toggle", zone.id, SKIP,
                      "zone supersedes nothing")
        return
    key = zone.reversibility_key
    if key and re.search(rf'["\']{re.escape(key)}["\']', zone.repo.all_source()):
        yield Finding("charter.reversibility_toggle", zone.id, INFO,
                      f"gated behind save key '{key}'")
        return
    still_there = zone.repo.exists(zone.supersedes)
    yield Finding("charter.reversibility_toggle", zone.id, ERROR,
                  f"replaced {zone.supersedes} with no reversibility save key. The charter "
                  f"requires the new world behind an additive key defaulting to classic until "
                  f"device sign-off; there is no runtime way back to the superseded mode"
                  + ("" if still_there else " and the superseded builder is gone"),
                  evidence={"supersedes": zone.supersedes,
                            "superseded_file_present": still_there,
                            "declared_key": key})


@check("charter.migration_order", "charter", "pilot_first")
def _migration_order(zone: Zone) -> Iterator[Finding]:
    """Zones migrate in charter order; the pilot proves the rig before the rest."""
    if zone.medium not in FLAT_MEDIA or zone.charter_order is None:
        yield Finding("charter.migration_order", zone.id, SKIP,
                      "zone is not a charter-ordered migration")
        return
    earlier = [z for z in zone.repo.spec["zones"]
               if z.get("charter_order") is not None
               and z["charter_order"] < zone.charter_order
               and z.get("status") == "not_migrated"]
    if not earlier:
        yield Finding("charter.migration_order", zone.id, INFO, "migrated in charter order")
        return
    names = ", ".join(f"#{z['charter_order']} {z['id']}" for z in earlier)
    yield Finding("charter.migration_order", zone.id, WARN,
                  f"zone #{zone.charter_order} shipped while {names} have not migrated — "
                  f"the layer spec was meant to be revised by the pilot's device test before "
                  f"later zones committed to it",
                  evidence={"zone_order": zone.charter_order,
                            "unmigrated_earlier": [z["id"] for z in earlier]})


@check("charter.probe_gated", "charter", "reversibility")
def _probe_gated(zone: Zone) -> Iterator[Finding]:
    """Every shipped zone has at least one probe in the trusted CI list."""
    if zone.status != "shipped":
        yield Finding("charter.probe_gated", zone.id, SKIP, "zone is not shipped")
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

@check("hygiene.orphan_art", "hygiene", "licenses")
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


@check("hygiene.superseded_generations", "hygiene", "licenses")
def _generations(zone: Zone) -> Iterator[Finding]:
    """Only one generation of each named asset ships."""
    if not zone.asset_roots:
        yield Finding("hygiene.superseded_generations", zone.id, SKIP, "no asset roots")
        return
    pngs = zone.repo.expand([os.path.join(r, "**", "*.png") for r in zone.asset_roots])
    if not pngs:
        yield Finding("hygiene.superseded_generations", zone.id, SKIP, "no PNGs")
        return
    families: dict[str, list[str]] = {}
    for p in pngs:
        stem = os.path.basename(p).removesuffix(".png")
        # strip trailing generation/qualifier suffixes: _v3, _v4_compact, _audited
        base = re.sub(r"(_v\d+)?(_compact|_audited(_\d+)?|_drift|_sway)*$", "", stem)
        base = re.sub(r"_\d+$", "", base)            # frame numbers
        families.setdefault(base, []).append(p)
    multi = {k: v for k, v in families.items() if len(v) > 1
             and len({re.search(r"_v(\d+)", os.path.basename(x)).group(1)
                      if re.search(r"_v(\d+)", os.path.basename(x)) else "0" for x in v}) > 1}
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


@check("hygiene.manual_squint_test", "hygiene", "no_text_in_art", media=FLAT_MEDIA,
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


def run(repo: Repo, zone_ids: list[str] | None = None,
        check_ids: list[str] | None = None) -> list[Finding]:
    waivers = {(w["check"], w["zone"]): w.get("reason", "")
               for w in repo.spec.get("waivers", [])}
    findings: list[Finding] = []
    for raw in repo.spec["zones"]:
        if zone_ids and raw["id"] not in zone_ids:
            continue
        zone = Zone(raw, repo)
        for cid, chk in REGISTRY.items():
            if check_ids and cid not in check_ids:
                continue
            if chk.media is not None and zone.medium not in chk.media:
                continue
            try:
                produced = list(chk.fn(zone))
            except Exception as exc:                              # noqa: BLE001
                produced = [Finding(cid, zone.id, ERROR,
                                    f"check crashed: {type(exc).__name__}: {exc}")]
            for f in produced:
                f.rule = f.rule or repo.spec.get("rules", {}).get(chk.rule, chk.rule)
                if (cid, zone.id) in waivers and f.severity in (ERROR, WARN):
                    f.severity = INFO
                    f.message = f"[WAIVED: {waivers[(cid, zone.id)]}] " + f.message
                findings.append(f)
    findings.sort(key=Finding.key)
    return findings


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

COLORS = {ERROR: "\033[31m", WARN: "\033[33m", MANUAL: "\033[35m",
          INFO: "\033[32m", SKIP: "\033[90m"}
RESET = "\033[0m"


def _tint(sev: str, text: str, use_color: bool) -> str:
    return f"{COLORS.get(sev, '')}{text}{RESET}" if use_color else text


def print_console(findings: list[Finding], verbose: bool) -> None:
    use_color = sys.stdout.isatty()
    shown = [f for f in findings
             if verbose or f.severity in (ERROR, WARN, MANUAL)]
    by_zone: dict[str, list[Finding]] = {}
    for f in shown:
        by_zone.setdefault(f.zone, []).append(f)
    for zone_id in sorted(by_zone):
        print(f"\n── {zone_id} " + "─" * max(0, 60 - len(zone_id)))
        for f in by_zone[zone_id]:
            print(f"  {_tint(f.severity, f.severity.ljust(6), use_color)} "
                  f"{f.check}\n         {f.message}")
    counts = {s: sum(1 for f in findings if f.severity == s)
              for s in (ERROR, WARN, MANUAL, INFO, SKIP)}
    print("\n" + "═" * 62)
    print("VISUALAUDIT| " + "  ".join(
        f"{s}={counts[s]}" for s in (ERROR, WARN, MANUAL, INFO, SKIP)))


def write_reports(findings: list[Finding], repo: Repo) -> None:
    os.makedirs(os.path.dirname(REPORT_JSON), exist_ok=True)
    payload = {
        "spec_version": repo.spec.get("version"),
        "checks": {c.id: {"category": c.category, "rule": c.rule, "doc": c.doc}
                   for c in REGISTRY.values()},
        "findings": [asdict(f) for f in findings],
        "summary": {s: sum(1 for f in findings if f.severity == s)
                    for s in (ERROR, WARN, MANUAL, INFO, SKIP)},
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
    for sev in (ERROR, WARN, MANUAL):
        rows = [f for f in findings if f.severity == sev]
        if not rows:
            continue
        lines += [f"## {sev}", "", "| Zone | Check | Finding |", "|---|---|---|"]
        for f in rows:
            msg = f.message.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| `{f.zone}` | `{f.check}` | {msg} |")
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


def _fixture(root: str, *, medium="promenade_2p5d", murals=1, mural_rgb=(60, 200, 255),
             fg_rgb=(150, 170, 190),
             depths=(("BACKDROP_Z", -18.0), ("DRESS_Z", -6.0), ("PLAY_Z", 0.5)),
             band=True, layers_api=False,
             supersedes=None, key=None, status="shipped", order=1,
             licensed=True, extra_generation=False, alpha_murals=0,
             fg_coverage=0.4, mural_layer_names=("L0",), huge_texture=False,
             zone_budgets=None) -> dict:
    """Build a synthetic repo that violates exactly what the caller asks for."""
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(root, "scenes"), exist_ok=True)
    os.makedirs(os.path.join(root, "tools"), exist_ok=True)

    mural_files, standee_files = [], []
    for i in range(murals):
        name = mural_layer_names[i % len(mural_layer_names)]
        rel = f"assets/flats/fx/stage/flat_fx_stage_{name}_bg{i}.png"
        size = (1500, 700) if huge_texture else (512, 512)
        _write_png(os.path.join(root, rel), size[0], size[1], mural_rgb,
                   1.0 if i >= alpha_murals else 0.5)
        mural_files.append(rel)
    rel = "assets/sprites/fx/standee_thing.png"
    _write_png(os.path.join(root, rel), 256, 256, fg_rgb, fg_coverage)
    standee_files.append(rel)
    if extra_generation:
        old = "assets/sprites/fx/standee_thing_v2.png"
        _write_png(os.path.join(root, old), 256, 256, fg_rgb, fg_coverage)

    depth_src = "\n".join(f"const {n} := {v}" for n, v in depths) if depths else ""
    band_src = "const HALF_D := 2.6\nconst BAND_Y := -5.0\nconst BAND_H := 10.0\n" if band else ""
    layers_src = '\t\t"layers": [],\n' if layers_api else ""
    builder = f"""class_name FxStage
extends RefCounted
{band_src}{depth_src}

func build() -> void:
\tstage = SideScrollStage.new(m)
\tstage.open({{
{layers_src}\t\t"half_w": 72.0,
\t}})
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
    with open(os.path.join(root, "ASSET_LICENSES.md"), "w", encoding="utf-8") as fh:
        if licensed:
            for r in mural_files + standee_files:
                fh.write(f"- `{os.path.basename(r)}` — Codex original, CC0.\n")
        else:
            fh.write("(intentionally empty)\n")

    return {
        "version": 2,
        "rules": load_spec().get("rules", {}),
        "budgets": load_spec().get("budgets", {}),
        "zones": [{
            "id": "fx", "name": "Fixture", "medium": medium, "status": status,
            "charter_order": order, "supersedes": supersedes,
            "reversibility_key": key,
            "builders": ["scripts/fx_stage.gd"], "probes": ["scripts/probe_fx.gd"],
            "murals": mural_files, "standees": standee_files, "characters": [],
            "asset_roots": ["assets/flats/fx", "assets/sprites/fx"],
            "budgets": zone_budgets or {},
        }],
        "waivers": [],
    }


# (check_id, fixture kwargs, expected severity) — each row must make the named
# check fire.  Adding a check without adding a row here fails the stress run.
STRESS_CASES: list[tuple[str, dict, str]] = [
    ("texture.pot_or_small", {"huge_texture": True}, ERROR),
    ("texture.vram_compressible", {"murals": 2, "huge_texture": True}, WARN),
    ("texture.zone_budget", {"zone_budgets": {"zone_runtime_texture_mb": 0.05}}, ERROR),
    ("texture.import_sidecar", {}, WARN),
    ("layering.mural_is_a_stack", {"murals": 4, "mural_layer_names": ("L0",)}, ERROR),
    ("layering.engine_layer_api", {"layers_api": False}, WARN),
    ("layering.depth_spread", {"depths": (("DRESS_Z", -17.9), ("PLAY_Z", -17.8))}, ERROR),
    ("layering.occlusion_band", {"depths": (("DRESS_Z", -17.9), ("PLAY_Z", -17.8))}, ERROR),
    ("layering.standee_alpha", {"fg_coverage": 1.0}, WARN),
    ("palette.background_recessive", {"mural_rgb": (0, 255, 255), "fg_rgb": (150, 150, 155)}, ERROR),
    ("palette.figure_ground_luminance", {"mural_rgb": (128, 128, 128), "fg_rgb": (128, 128, 128)}, WARN),
    ("overdraw.alpha_layers", {"murals": 4, "alpha_murals": 4,
                               "mural_layer_names": ("L0", "L1", "L2", "L3")}, ERROR),
    ("charter.reversibility_toggle", {"supersedes": "scripts/old_stage.gd", "key": None}, ERROR),
    ("charter.migration_order", {"order": 4}, WARN),
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
            # the migration-order case needs an unmigrated earlier zone to point at
            if cid == "charter.migration_order":
                spec["zones"].append({"id": "pilot", "name": "Pilot", "medium": "free_swim_3d",
                                      "status": "not_migrated", "charter_order": 1,
                                      "supersedes": None, "reversibility_key": None,
                                      "builders": [], "probes": [], "murals": [],
                                      "standees": [], "characters": [], "asset_roots": []})
            if cid == "charter.probe_gated":
                with open(os.path.join(tmp, "scripts", "ci.sh"), "w", encoding="utf-8") as fh:
                    fh.write("for p in probe_other; do :; done\n")
            repo = Repo(tmp, spec)
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
                             layers_api=True, alpha_murals=1, fg_coverage=0.4)
            repo = Repo(tmp, clean)
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
                medium=rng.choice(sorted(FLAT_MEDIA) + ["free_swim_3d", "ui"]),
            )
            try:
                crashes = [f for f in run(Repo(tmp, spec)) if "check crashed" in f.message]
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
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", default=SPEC_PATH)
    ap.add_argument("--zone", action="append", help="limit to zone id (repeatable)")
    ap.add_argument("--check", action="append", help="limit to check id (repeatable)")
    ap.add_argument("--category", action="append", help="limit to a check category")
    ap.add_argument("--strict", action="store_true", help="exit nonzero on any ERROR")
    ap.add_argument("--max-warn", type=int, default=None,
                    help="exit nonzero above this many WARNs")
    ap.add_argument("--format", choices=("console", "json", "md"), default="console")
    ap.add_argument("--verbose", "-v", action="store_true", help="show INFO and SKIP too")
    ap.add_argument("--list-checks", action="store_true")
    ap.add_argument("--stress", action="store_true", help="self-test every check")
    ap.add_argument("--fuzz", type=int, default=24, help="fuzz rounds during --stress")
    ap.add_argument("--no-report", action="store_true", help="skip writing audit/ files")
    args = ap.parse_args(argv)

    if args.list_checks:
        for cid in sorted(REGISTRY):
            c = REGISTRY[cid]
            media = ",".join(sorted(c.media)) if c.media else "all"
            print(f"{cid:38s} [{c.category:10s}] media={media:34s} {c.doc}")
        return 0

    if args.stress:
        return stress(fuzz=args.fuzz, verbose=args.verbose)

    spec = load_spec(args.spec)
    runtime = {}
    if os.path.exists(RUNTIME_FACTS_PATH):
        try:
            with open(RUNTIME_FACTS_PATH, "r", encoding="utf-8") as fh:
                runtime = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"warning: runtime facts unreadable ({exc}); scene checks will SKIP",
                  file=sys.stderr)

    repo = Repo(REPO, spec, runtime)
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
            if f.severity in (ERROR, WARN, MANUAL) or args.verbose:
                print(f"- **{f.severity}** `{f.zone}` `{f.check}` — {f.message}")

    if not args.no_report:
        write_reports(findings, repo)

    errors = sum(1 for f in findings if f.severity == ERROR)
    warns = sum(1 for f in findings if f.severity == WARN)
    if args.strict and errors:
        return 1
    if args.max_warn is not None and warns > args.max_warn:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
