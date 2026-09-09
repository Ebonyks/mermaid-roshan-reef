#!/usr/bin/env python3
"""Deterministic Opera artwork inventory and review-sheet builder.

This is audit support only. It reads source/runtime files, records hashes and
dimensions, and writes review copies under ignored tmp/; it never edits runtime
art or scripts.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(os.environ.get("OPERA_AUDIT_ROOT", str(Path(__file__).resolve().parents[2]))).resolve()
OUT = ROOT / "assets_src" / "minigame_art_audit_2026-09-06"
TMP = ROOT / "tmp" / "opera_art_audit_2026-09-06"
CAREERS = ["chef", "detective", "ballerina", "candymaker", "doctor", "farmer", "boxer", "magician", "painter", "astronaut", "racer", "popstar", "nursery", "geologist", "teacher"]

REPRESENTATIVE_PATHS = {
    "chef": ["assets/opera/worlds/backdrops/world_chef.png", "assets/opera/worlds/actors/roshan_chef.png", "assets/opera/worlds/widgets/widget_pour_chef_mover.png"],
    "detective": ["assets/opera/worlds/backdrops/world_detective.png", "assets/opera/worlds/actors/roshan_detective.png", "assets/opera/worlds/widgets/widget_clue_board_tokens.png"],
    "ballerina": ["assets/opera/worlds/backdrops/world_ballerina.png", "assets/opera/worlds/actors/roshan_ballerina.png", "assets/opera/worlds/widgets/widget_lanes_ballerina_lit.png"],
    "candymaker": ["assets/opera/worlds/backdrops/world_candymaker.png", "assets/opera/worlds/actors/roshan_candymaker.png", "assets/opera/worlds/widgets/widget_pour_candymaker_mover.png"],
    "doctor": ["assets/opera/worlds/backdrops/world_doctor.png", "assets/opera/worlds/actors/roshan_doctor.png", "assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png"],
    "farmer": ["assets/opera/worlds/backdrops/world_farmer.png", "assets/opera/worlds/actors/roshan_farmer.png", "assets/opera/worlds/widgets/widget_target_farmer_piece_2.png"],
    "boxer": ["assets/opera/worlds/backdrops/world_boxer.png", "assets/opera/worlds/actors/roshan_boxer.png", "assets/opera/worlds/widgets/widget_track_boxer_mover.png"],
    "magician": ["assets/opera/worlds/backdrops/world_magician.png", "assets/opera/worlds/actors/roshan_magician.png", "assets/opera/worlds/widgets/widget_magic_vanish_wand.png"],
    "painter": ["assets/opera/worlds/backdrops/world_painter.png", "assets/opera/worlds/actors/roshan_painter.png", "assets/opera/worlds/widgets/widget_pour_painter_mover.png"],
    "astronaut": ["assets/opera/worlds/backdrops/world_astronaut.png", "assets/opera/worlds/actors/roshan_astronaut.png", "assets/opera/worlds/widgets/widget_crank_astronaut_mover.png"],
    "racer": ["assets/opera/worlds/backdrops/world_racer.png", "assets/opera/worlds/actors/roshan_racer.png", "assets/opera/worlds/widgets/widget_push_racer_mover.png"],
    "popstar": ["assets/opera/worlds/backdrops/world_popstar.png", "assets/opera/worlds/actors/roshan_popstar.png", "assets/opera/worlds/widgets/widget_track_popstar_mover.png"],
    "nursery": ["assets/opera/worlds/backdrops/world_nursery_c0r0.png", "assets/opera/worlds/actors/faron_nursery.png", "assets/opera/worlds/nursery/baby_0.png"],
    "geologist": ["assets_src/geologist_rebuild_2026-09-05/geology_grotto_candidate.png", "assets/opera/worlds/actors/animation/roshan_geologist_sheet_a.png", "assets/opera/worlds/hotspots/geologist_fossil.svg"],
    "teacher": ["assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c0.png", "assets/opera/worlds/actors/roshan_teacher.png", "assets/opera/worlds/hotspots/teacher_lesson_board.svg"],
}

DISPOSITIONS = {
    "chef": ("PASS", [], [], ["No repair job; preserve approved room, actor and painted cookware."], "World master, actor and MIX mover inspected native and in whole-room contact sheet."),
    "detective": ("PASS", [], [], ["No repair job; preserve approved storybook, actor and clue-board tokens."], "World master, actor and CASE BOARD tokens inspected native and in whole-room contact sheet."),
    "ballerina": ("PASS", [], [], ["No repair job; preserve approved room, actor and lane pads."], "World master, actor and PHRASE lane group inspected native and in whole-room contact sheet."),
    "candymaker": ("PASS", [], [], ["No repair job; preserve approved workshop, actor and syrup pan."], "World master, actor and SYRUP mover inspected native and in whole-room contact sheet."),
    "doctor": ("PASS", [], [], ["No repair job; preserve approved room, actor and basin effect role."], "World master, actor and WASH effect inspected native and in whole-room contact sheet."),
    "farmer": ("PASS", [], [], ["No repair job; preserve approved field, actor and pumpkin target."], "World master, actor and PLANT target inspected native and in whole-room contact sheet."),
    "boxer": ("PASS", [], [], ["No repair job; preserve approved ring, actor and mitt group."], "World master, actor and COMBO mitt group inspected native and in whole-room contact sheet."),
    "magician": ("PASS", [], [], ["No repair job; preserve approved theatre, actor and wand."], "World master, actor and VANISH wand inspected native and in whole-room contact sheet."),
    "painter": ("PASS", [], [], ["No repair job; preserve approved studio, actor and canvas mover."], "World master, actor and PAINT canvas inspected native and in whole-room contact sheet."),
    "astronaut": ("PASS", [], [], ["No repair job; preserve approved rocket room, actor and valve wheel."], "World master, actor and PIPES wheel inspected native and in whole-room contact sheet."),
    "racer": ("PASS", [], [], ["No repair job; preserve approved circuit, actor and kart mover."], "World master, actor and TO THE LINE kart inspected native and in whole-room contact sheet."),
    "popstar": ("PASS", [], [], ["No repair job; preserve approved stage, actor and note-track effect."], "World master, actor and DANCE track effect inspected native and in whole-room contact sheet."),
    "nursery": ("PASS", [], ["assets/opera/worlds/widgets/widget_catch_nursery.png is retained legacy art; OperaNurseryCatch explicitly sets backdrop_texture=null and uses cradle/pillows/babies."], ["No repair job; keep retired framed card out of runtime."], "Nursery tile, Faron actor and baby_0 inspected native and in whole-room contact sheet; live CATCH surface source inspected."),
    "geologist": ("FAIL", ["No world_geologist.png or complete geologist tile set exists; backdrop setup reaches _draw_geologist() fallback with five polyline bands, rectangle slab/trays and polygon crystals."], ["geology_fossil.svg, geologist_layered_rock.svg and goal_geologist.svg are active approved vectors but SVG pixels were not raster-viewed in this audit."], ["Bounded repair G-01: review existing geology_grotto_candidate.png only as a source candidate; it is 1672x941 REFERENCE_ONLY and cannot ship. Reuse only after native coverage and no-watercolor/cel review. Reassess the rejected checkerboard props candidates; if no suitable reusable source passes, record the exact gap before any new generation."], "Whole Geologist route capture and source fallback inspected; atlas/vector native pixels remain SVG/atlas evidence gaps."),
    "teacher": ("PASS", [], ["teacher_lesson_board.svg was source/hash inspected but not raster-viewed in this environment."], ["No repair job; retain intentional lesson shape stimuli and approved library room."], "Library room, Roshan teacher and teacher lesson route inspected native/whole-room; lesson shapes are intentional role stimuli."),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dims(path: Path) -> list[int] | None:
    try:
        with Image.open(path) as im:
            return [int(im.width), int(im.height)]
    except Exception:
        return None


def all_asset_files() -> list[Path]:
    roots = [
        ROOT / "assets" / "opera" / "worlds" / "backdrops",
        ROOT / "assets" / "opera" / "worlds" / "widgets",
        ROOT / "assets" / "opera" / "worlds" / "actors",
        ROOT / "assets" / "opera" / "worlds" / "props",
        ROOT / "assets" / "opera" / "worlds" / "hotspots",
        ROOT / "assets" / "opera" / "worlds" / "nursery",
    ]
    result: list[Path] = []
    for base in roots:
        if base.is_dir():
            result.extend(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in {".png", ".svg"})
    return sorted(result)


def source_paths() -> list[str]:
    files = [
        "scripts/opera_house.gd", "scripts/opera_act.gd", "scripts/opera_career_world_2d.gd",
        "scripts/opera_hotspot_catalog.gd", "scripts/opera_gesture_surface.gd",
        "scripts/opera_boxing_surface.gd", "scripts/opera_ballet_surface.gd",
        "scripts/opera_teacher_surface.gd", "scripts/opera_geology_surface.gd",
        "scripts/opera_nursery_catch.gd", "scripts/opera_racer_surface.gd",
        "scripts/teacher_lesson_plan.gd", "scripts/chapter_two_career_scene_adapter.gd",
    ]
    return files


def phase_catalog(path: Path) -> dict[str, list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8")
    start = text.index("const PHASES := {")
    end = text.index("\n\nfunc _ballet_voice_length_seconds", start)
    block = text[start:end]
    result: dict[str, list[dict[str, str]]] = {}
    current = None
    for line in block.splitlines():
        m = re.match(r'\t"([a-z]+)": \[$', line)
        if m:
            current = m.group(1)
            result[current] = []
            continue
        if current and line.startswith("\t],"):
            current = None
            continue
        m = re.search(r'\{"name": "([^"]+)".*?"mode": "([^"]+)"', line)
        if m and current:
            result[current].append({"name": m.group(1), "mode": m.group(2)})
    return result


def chapter_catalog(path: Path) -> dict[str, list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8")
    start = text.index("const PHASE_SETS := {")
    end = text.index("\nstatic func phase_set", start)
    block = text[start:end]
    result: dict[str, list[dict[str, str]]] = {}
    for career in CAREERS:
        marker = f'\t"{career}":'
        at = block.find(marker)
        if at < 0:
            continue
        next_at = min([x for x in (block.find(f'\n\t"{c}":', at + 1) for c in CAREERS) if x >= 0] or [len(block)])
        part = block[at:next_at]
        result[career] = [{"name": n, "mode": m} for n, m in re.findall(r'\{"name": "([^"]+)".*?"mode": "([^"]+)"', part)]
    return result


def hotspot_catalog(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    start = text.index("const SPECS: Dictionary = {")
    end = text.index("\n\n## Exact imported", start)
    block = text[start:end]
    result: dict[str, dict[str, str]] = {}
    career = None
    for line in block.splitlines():
        m = re.match(r'\t"([a-z]+)": \{$', line)
        if m:
            career = m.group(1)
            continue
        if career and line.startswith("\t},"):
            career = None
            continue
        m = re.search(r'"([A-Z][A-Z0-9 ?-]+)": \{"path": "([^"]+)".*?"presentation": "([^"]+)"', line)
        if m:
            result[f"{career}/{m.group(1)}"] = {"path": m.group(2), "presentation": m.group(3)}
    return result


def path_refs() -> set[str]:
    refs: set[str] = set()
    for rel in source_paths():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        refs.update(re.findall(r"res://assets/[A-Za-z0-9_./-]+", text))
    return refs


def record(path: Path) -> dict:
    rel = path.relative_to(ROOT).as_posix()
    return {"path": rel, "sha256": sha(path), "dimensions": dims(path)}


def contact_sheet(paths: list[Path], out: Path, title: str, thumb=(180, 120), cols=5) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cell_w, cell_h = thumb[0], thumb[1] + 24
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + 30), (37, 35, 62))
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 8), title, fill=(240, 240, 240))
    for i, path in enumerate(paths):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h + 30
        try:
            im = Image.open(path).convert("RGBA")
            bg = Image.new("RGBA", thumb, (26, 24, 45, 255))
            im.thumbnail(thumb, Image.Resampling.LANCZOS)
            bg.alpha_composite(im, ((thumb[0] - im.width) // 2, (thumb[1] - im.height) // 2))
            sheet.paste(bg.convert("RGB"), (x, y))
        except Exception:
            draw.rectangle((x, y, x + thumb[0], y + thumb[1]), fill=(90, 50, 95))
        draw.text((x + 3, y + thumb[1] + 3), path.stem[:27], fill=(235, 235, 235))
    sheet.save(out, quality=92)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    files = all_asset_files()
    refs = path_refs()
    ref_files = {ROOT / p.removeprefix("res://") for p in refs if p.startswith("res://")}
    catalog = {
        "inventory_date": "2026-09-06",
        "checkout_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "checkout_branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
        "sources": source_paths(),
        "careers": CAREERS,
        "legacy_phase_catalog": phase_catalog(ROOT / "scripts/opera_career_world_2d.gd"),
        "chapter2_phase_catalog": chapter_catalog(ROOT / "scripts/chapter_two_career_scene_adapter.gd"),
        "hotspot_catalog": hotspot_catalog(ROOT / "scripts/opera_hotspot_catalog.gd"),
        "dynamic_asset_refs": sorted(refs),
        "asset_counts": {},
        "all_runtime_assets": [record(p) for p in files],
        "exact_literal_ref_assets": [record(p) for p in files if p in ref_files],
        "retained_or_unreferenced_assets": [record(p) for p in files if p not in ref_files],
    }
    legacy = catalog["legacy_phase_catalog"]
    chapter = catalog["chapter2_phase_catalog"]
    hotspot = catalog["hotspot_catalog"]
    groups = []
    for career in CAREERS:
        phases = legacy.get(career, [])
        chapter_phases = chapter.get(career, [])
        mode_set = sorted({item["mode"] for item in phases + chapter_phases})
        refs_for_career = sorted({spec["path"] for key, spec in hotspot.items() if key.startswith(career + "/")})
        reps = []
        for rel in REPRESENTATIVE_PATHS.get(career, []):
            path = ROOT / rel
            reps.append(record(path) if path.is_file() else {"path": rel, "missing": True})
        groups.append({
            "id": career,
            "entry": "scripts/opera_career_world_2d.gd::_bind_widget/_open_task",
            "reachable": bool(phases),
            "legacy_phases": phases,
            "chapter2_phases": chapter_phases,
            "modes": mode_set,
            "hotspot_refs": refs_for_career,
            "representatives": reps,
            "quality_verdict": DISPOSITIONS[career][0],
            "specific_failures": DISPOSITIONS[career][1],
            "evidence_gaps": DISPOSITIONS[career][2],
            "bounded_repair_jobs": DISPOSITIONS[career][3],
            "inspection_evidence": DISPOSITIONS[career][4],
            "protected_provenance": "Runtime assets under assets/opera are retained approved sources; assets_src candidates are non-runtime review material. Protected originals are not modified.",
        })
    catalog["career_groups"] = groups
    for prefix in ["backdrops", "widgets", "actors", "props", "hotspots", "nursery"]:
        catalog["asset_counts"][prefix] = sum(1 for p in files if f"/worlds/{prefix}/" in p.as_posix())
    (OUT / "opera_inventory.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    widget_paths = sorted((ROOT / "assets/opera/worlds/widgets").glob("*.png"))
    actor_paths = sorted((ROOT / "assets/opera/worlds/actors").glob("*.png"))
    world_paths = sorted((ROOT / "assets/opera/worlds/backdrops").glob("world_*.png"))
    contact_sheet(widget_paths, TMP / "widgets_all_contact.jpg", "Opera widgets: all runtime PNGs")
    contact_sheet(actor_paths, TMP / "actors_all_contact.jpg", "Opera actors: all runtime PNGs", thumb=(220, 180), cols=5)
    contact_sheet(world_paths, TMP / "worlds_all_contact.jpg", "Opera world and stage key paintings", thumb=(220, 140), cols=5)


if __name__ == "__main__":
    main()
