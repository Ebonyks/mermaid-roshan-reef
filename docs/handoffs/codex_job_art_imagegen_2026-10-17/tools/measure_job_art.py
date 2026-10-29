#!/usr/bin/env python3
"""Numbers-only measurement of job-game art wiring. No image is opened or written.

Sections of the JSON report (run from the repository root):

  phase_art      every Opera career phase in scripts/opera_career_world_2d.gd
                 PHASES, the widget art family it resolves to (mirroring
                 _widget_template/_bind_widget) and the painted widget files
                 present for that family; phases that resolve to no family
                 draw their own picture in code.
  code_drawing   primitive draw calls (draw_circle, draw_rect, draw_polygon,
                 draw_line, draw_arc, draw_string, draw_style_box ...),
                 primitive node/style constructions (Polygon2D, Line2D,
                 ColorRect, StyleBoxFlat, gradients, Image.set_pixel) and
                 texture draw calls, per runtime script and per job.
  runtime_svg    vector files under assets/ and the runtime lines that load them.
  asset_wiring   every image under the job asset roots, classified EXACT
                 (full path literal in a runtime file), TEMPLATE (matches a
                 %s/%d path template or a filename-prefix literal), BY_NAME
                 (stem appears as a literal), DIR_PREFIX_ONLY or UNREFERENCED.
                 A static scan: TEMPLATE/DIR_PREFIX_ONLY do not prove use.
  stranded       images added on named unmerged branches and whether the same
                 bytes (git blob) exist anywhere in the base tree.
  program        for --program-branch: non-merge commits ahead of base and how
                 many of them change scripts/, assets/ or scenes/.

Usage:
  python -B tools/measure_job_art.py --base origin/dev \
      --branch origin/codex/job-art-review-v2-20261001 [--branch ...] \
      [--program-branch origin/codex/flat-vector-r6-20261012] \
      [--out report.json] [--summary]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

PRIMITIVE_DRAW = re.compile(
    r"\bdraw_(circle|rect|polygon|colored_polygon|line|polyline|polyline_colors|"
    r"arc|multiline|multiline_colors|primitive|style_box|string|string_outline|"
    r"multiline_string|char|char_outline|dashed_line|ellipse|ellipse_arc)\s*\("
)
TEXTURE_DRAW = re.compile(
    r"\bdraw_(texture|texture_rect|texture_rect_region|lcd_texture_rect_region|"
    r"msdf_texture_rect_region|mesh|multimesh)\s*\("
)
PRIMITIVE_NODE = re.compile(
    r"\b(Polygon2D|Line2D|ColorRect|StyleBoxFlat|StyleBoxLine|GradientTexture2D|"
    r"GradientTexture1D|NoiseTexture2D|CanvasTexture)\.new\s*\(|"
    r"\bImage\.create(_empty)?\s*\(|\.set_pixel\s*\("
)
FUNC = re.compile(r"^\s*(static\s+)?func\s+([A-Za-z0-9_]+)")
STRING = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'')
IMAGE_EXT = (".png", ".webp", ".jpg", ".jpeg", ".svg")
ASSET_ROOTS = (
    "assets/opera", "assets/kart", "assets/castle", "assets/chapter2",
    "assets/flats", "assets/ui", "assets/art35/cards",
)
EXCLUDE_SCRIPT = re.compile(r"(^|/)(probe[^/]*\.gd|[^/]*_test_case\.gd)$")
JOB_SCRIPTS = {
    # Shared by the nine gesture careers and parts of the specialist ones.
    "opera_shared_gesture": ["scripts/opera_gesture_surface.gd"],
    "opera_shared_world": [
        "scripts/opera_career_world_2d.gd", "scripts/opera_world_backdrop_2d.gd",
        "scripts/opera_world_hotspot_2d.gd", "scripts/living_world_canvas.gd",
        "scripts/opera_house_venue_2d.gd",
    ],
    "opera_shared_hud": ["scripts/opera_performance_overlay.gd"],
    "chef": ["scripts/opera_chef_surface.gd"],
    "geologist": ["scripts/opera_geology_surface.gd"],
    "boxer": ["scripts/opera_boxing_surface.gd"],
    "ballerina": ["scripts/opera_ballet_surface.gd"],
    "racer": ["scripts/opera_racer_surface.gd", "scripts/kart_driving.gd"],
    "teacher": ["scripts/opera_teacher_surface.gd", "scripts/teacher_lesson_plan.gd"],
    "nursery": ["scripts/opera_nursery_catch.gd"],
    "arborist_prototype": ["scripts/opera_tree_book_test.gd"],
    "chapter_two_jobs": [
        "scripts/chapter_two_giant_cake_2d.gd", "scripts/chapter_two_rainbow_candle_2d.gd",
        "scripts/chapter_two_lawn_finale_2d.gd", "scripts/chapter_two_party_table_2d.gd",
    ],
    "day_one_jobs": [
        "scripts/arena/day_one_castle_grime.gd", "scripts/games/day_one_bathroom_cleaning.gd",
        "scripts/games/day_one_bathroom_toilet.gd", "scripts/games/day_one_fixture_scrub.gd",
        "scripts/games/day_one_bathroom_cleanup.gd", "scripts/day_one_art_studio.gd",
        "scripts/dust_boss_telegraph_2d.gd",
    ],
}
# Mirrors OperaCareerWorld2D._widget_template at the measured baseline.
NO_FAMILY_MODES = {
    "ballet_pose", "ballet_ribbon", "ballet_twirl", "talk", "boxing_guide",
    "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt", "echo", "pipe",
}
MODE_FAMILY = {
    "pourt": "pour", "oven": "gauge", "circle": "crank", "tap": "target",
    "choice": "lanes", "catch": "catch", "dance_sequence": "lanes",
    "boxer_rhythm": "lanes", "candy_sort": "lanes", "paint_reveal": "trace",
    "farm_lob": "target", "xray_scan": "target",
}


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True,
        text=True, encoding="utf-8",
    ).stdout


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def widget_family(career: str, phase: dict) -> str:
    if "widget" in phase:
        return str(phase["widget"])
    mode, name = phase.get("mode", ""), phase.get("name", "")
    if mode in NO_FAMILY_MODES:
        return ""
    if mode == "timing":
        return "gauge" if career in ("chef", "astronaut", "racer") else "track"
    if mode == "hold":
        if name in ("WASH", "WASH HANDS"):
            return "basin"
        if name in ("POUR", "SYRUP", "FILL", "FEED"):
            return "pour"
        return "charge"
    if mode == "swipe":
        return "push" if name in ("HERD", "DUCK", "STEER", "BEDTIME", "TO THE LINE") else "trace"
    return MODE_FAMILY.get(mode, "")


def phase_art(root: Path) -> dict:
    src = read(root / "scripts/opera_career_world_2d.gd")
    start = src.index("const PHASES := {")
    block = src[start:src.index("\n}\n", start)]
    widgets = sorted(p.name for p in (root / "assets/opera/worlds/widgets").glob("*.png"))
    rows, career, used = [], None, set()
    for line in block.splitlines():
        m = re.match(r'\t"([a-z_]+)": \[', line)
        if m:
            career = m.group(1)
            continue
        m = re.match(r"\t\t(\{.*\}),?$", line)
        if not (m and career):
            continue
        ph = json.loads(m.group(1))
        fam = widget_family(career, ph)
        ctx = f"{fam}_{career}" if fam else ""
        ctx = ph.get("visual_context", ctx)
        ctx = ph.get("widget_context", ctx)
        files = [w for w in widgets if ctx and (w == f"widget_{ctx}.png" or w.startswith(f"widget_{ctx}_"))]
        used.update(files)
        rows.append({
            "career": career, "phase": ph["name"], "mode": ph["mode"],
            "widget_family": fam, "context": ctx, "widget_files": files,
            "draws_own_picture": not files,
        })
    return {
        "phases": len(rows),
        "careers": len({r["career"] for r in rows}),
        "phases_with_widget_art": sum(1 for r in rows if r["widget_files"]),
        "phases_drawing_own_picture": sum(1 for r in rows if r["draws_own_picture"]),
        "widget_png_total": len(widgets),
        "widget_png_matched_by_current_phase": len(used),
        "widget_png_unmatched": sorted(set(widgets) - used),
        "rows": rows,
    }


def runtime_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for base, exts in (
        ("scripts", (".gd", ".json", ".tscn", ".tres")),
        ("scenes", (".tscn", ".tres", ".json")),
        ("assets", (".tscn", ".tres", ".json")),
        ("content", (".json",)),
    ):
        d = root / base
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if p.is_file() and p.suffix in exts:
                rel = p.relative_to(root).as_posix()
                if p.suffix == ".gd" and EXCLUDE_SCRIPT.search(rel):
                    continue
                out.append(p)
    if (root / "project.godot").exists():
        out.append(root / "project.godot")
    return out


def code_drawing(root: Path) -> dict:
    per_file = {}
    for p in sorted((root / "scripts").rglob("*.gd")):
        rel = p.relative_to(root).as_posix()
        if EXCLUDE_SCRIPT.search(rel):
            continue
        text = read(p)
        prim = tex = node = 0
        funcs: Counter = Counter()
        current = "<file>"
        for line in text.splitlines():
            m = FUNC.match(line)
            if m:
                current = m.group(2)
            code = line.split("#", 1)[0]
            n_prim = len(PRIMITIVE_DRAW.findall(code))
            n_node = len(PRIMITIVE_NODE.findall(code))
            prim += n_prim
            node += n_node
            tex += len(TEXTURE_DRAW.findall(code))
            if n_prim or n_node:
                funcs[current] += n_prim + n_node
        if prim or node or tex:
            per_file[rel] = {
                "primitive_draw_calls": prim,
                "primitive_node_constructions": node,
                "texture_draw_calls": tex,
                "lines": text.count("\n") + 1,
                "top_drawing_functions": [[f, n] for f, n in funcs.most_common(15)],
            }
    jobs = {}
    for job, paths in JOB_SCRIPTS.items():
        jobs[job] = {
            "scripts": paths,
            "primitive_draw_calls": sum(per_file.get(p, {}).get("primitive_draw_calls", 0) for p in paths),
            "primitive_node_constructions": sum(per_file.get(p, {}).get("primitive_node_constructions", 0) for p in paths),
            "texture_draw_calls": sum(per_file.get(p, {}).get("texture_draw_calls", 0) for p in paths),
        }
    totals = {
        "files_with_primitive_drawing": sum(
            1 for v in per_file.values() if v["primitive_draw_calls"] or v["primitive_node_constructions"]),
        "primitive_draw_calls": sum(v["primitive_draw_calls"] for v in per_file.values()),
        "primitive_node_constructions": sum(v["primitive_node_constructions"] for v in per_file.values()),
        "texture_draw_calls": sum(v["texture_draw_calls"] for v in per_file.values()),
    }
    job_paths = {p for v in JOB_SCRIPTS.values() for p in v}
    totals["job_scripts_primitive_draw_calls"] = sum(
        v["primitive_draw_calls"] for k, v in per_file.items() if k in job_paths)
    return {"totals": totals, "jobs": jobs, "per_file": per_file}


def runtime_svg(root: Path, files: list[Path]) -> list[dict]:
    svgs = sorted(p.relative_to(root).as_posix() for p in (root / "assets").rglob("*.svg"))
    out = []
    for svg in svgs:
        name = svg.rsplit("/", 1)[-1]
        refs = []
        for f in files:
            if f.suffix != ".gd":
                continue
            for i, line in enumerate(read(f).splitlines(), 1):
                if name in line:
                    refs.append(f"{f.relative_to(root).as_posix()}:{i}")
        out.append({"path": svg, "references": refs})
    return out


def imagegen_rows(root: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    lic = root / "ASSET_LICENSES.md"
    if not lic.exists():
        return rows
    for line in read(lic).splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        path = cells[0].strip("` ")
        if path.lower().endswith(IMAGE_EXT):
            rows[path] = "imagegen" if re.search(r"imagegen|image ?gen|gpt-image", cells[1], re.I) else "other"
    return rows


def asset_wiring(root: Path, files: list[Path]) -> dict:
    literals: set[str] = set()
    templates: list[re.Pattern] = []
    file_prefixes: set[str] = set()
    dir_prefixes: set[str] = set()
    for f in files:
        for m in STRING.finditer(read(f)):
            s = m.group(1) if m.group(1) is not None else m.group(2)
            if not s:
                continue
            s = s.replace("res://", "")
            literals.add(s)
            if not s.startswith("assets/"):
                continue
            if re.search(r"%(0?\d*)[sd]", s):
                pat = re.escape(s)
                pat = re.sub(r"%(0?\d*)d", r"\\d+", pat.replace("\\%", "%"))
                pat = pat.replace("%s", "[^/]+")
                if s.lower().endswith(IMAGE_EXT):
                    templates.append(re.compile("^" + pat + "$"))
                else:
                    templates.append(re.compile("^" + pat))
            elif not s.lower().endswith(IMAGE_EXT):
                if s.endswith("/"):
                    dir_prefixes.add(s)
                else:
                    file_prefixes.add(s)
                    dir_prefixes.add(s.rsplit("/", 1)[0] + "/")
    exact = {s for s in literals if s.lower().endswith(IMAGE_EXT)}
    lic = imagegen_rows(root)
    results = []
    for base in ASSET_ROOTS:
        d = root / base
        if not d.exists():
            continue
        for p in sorted(d.rglob("*")):
            if not (p.is_file() and p.suffix.lower() in IMAGE_EXT):
                continue
            rel = p.relative_to(root).as_posix()
            if rel in exact:
                status = "EXACT"
            elif any(t.search(rel) for t in templates) or any(rel.startswith(fp) for fp in file_prefixes):
                status = "TEMPLATE"
            elif any(p.stem == s or s.endswith("/" + p.name) or s == p.name for s in literals):
                status = "BY_NAME"
            elif any(rel.startswith(dp) for dp in dir_prefixes):
                status = "DIR_PREFIX_ONLY"
            else:
                status = "UNREFERENCED"
            results.append({"path": rel, "status": status, "licence_source": lic.get(rel, "no_row"), "bytes": p.stat().st_size})
    by_folder = defaultdict(Counter)
    for r in results:
        by_folder["/".join(r["path"].split("/")[:4])][r["status"]] += 1
    return {
        "roots": list(ASSET_ROOTS),
        "counts": dict(Counter(r["status"] for r in results)),
        "by_folder": {k: dict(v) for k, v in sorted(by_folder.items())},
        "assets": results,
    }


def cutout_profile(data: bytes) -> dict | None:
    """Alpha profile of PNG bytes: numbers only, nothing is written.

    Needs Pillow and numpy; returns None when they are unavailable.
    """
    try:
        import io
        import numpy as np
        from PIL import Image
    except ImportError:
        return None
    img = Image.open(io.BytesIO(data))
    mode = img.mode
    rgba = np.asarray(img.convert("RGBA"))
    alpha = rgba[:, :, 3]
    total = alpha.size
    h, w = alpha.shape
    corners = [int(alpha[0, 0]), int(alpha[0, w - 1]), int(alpha[h - 1, 0]), int(alpha[h - 1, w - 1])]
    solid = np.argwhere(alpha > 8)
    bbox = None
    if solid.size:
        (y0, x0), (y1, x1) = solid.min(0), solid.max(0)
        bbox = [int(x0), int(y0), int(x1) + 1, int(y1) + 1]
    visible = float((alpha > 0).sum()) or 1.0
    haze = float(((alpha > 0) & (alpha < 16)).sum())
    semi = float(((alpha >= 16) & (alpha < 240)).sum())
    near = float((alpha >= 240).sum())
    if mode in ("RGB", "P", "L") and min(corners) == 255:
        verdict = "NO_ALPHA"
    elif min(corners) == 255:
        verdict = "OPAQUE_BACKGROUND"
    elif near < 0.5 * visible:
        verdict = "TRANSLUCENT_BODY"
    elif haze > 0.05 * total:
        verdict = "FAINT_HAZE"
    else:
        verdict = "CUTOUT_OK"
    return {
        "mode": mode,
        "transparent_pct": round(100.0 * float((alpha == 0).sum()) / total, 1),
        "faint_haze_pct_of_canvas": round(100.0 * haze / total, 1),
        "semi_pct_of_visible": round(100.0 * semi / visible, 1),
        "near_opaque_pct_of_visible": round(100.0 * near / visible, 1),
        "opaque_255_pct": round(100.0 * float((alpha == 255).sum()) / total, 1),
        "corner_alpha": corners,
        "content_bbox": bbox,
        "verdict": verdict,
    }


def stranded(root: Path, base: str, branches: list[str]) -> dict:
    base_blobs: dict[str, list[str]] = defaultdict(list)
    for line in git(root, "ls-tree", "-r", base).splitlines():
        meta, path = line.split("\t", 1)
        base_blobs[meta.split()[2]].append(path)
    out = {}
    for br in branches:
        added = [
            p for p in git(root, "diff", "--name-only", "--diff-filter=A", f"{base}...{br}").splitlines()
            if p.startswith("assets/") and p.lower().endswith(IMAGE_EXT)
        ]
        rows = []
        for p in added:
            blob = git(root, "rev-parse", f"{br}:{p}").strip()
            data = subprocess.run(
                ["git", "-C", str(root), "cat-file", "blob", blob],
                check=True, capture_output=True,
            ).stdout
            rows.append({
                "path": p, "blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                "size": list(struct.unpack(">II", data[16:24])) if data[:8] == b"\x89PNG\r\n\x1a\n" else None,
                "cutout": cutout_profile(data) if p.lower().endswith(".png") else None,
                "same_bytes_in_base": base_blobs.get(blob, []),
            })
        out[br] = {
            "head": git(root, "rev-parse", br).strip(),
            "ahead": int(git(root, "rev-list", "--count", f"{base}..{br}").strip()),
            "behind": int(git(root, "rev-list", "--count", f"{br}..{base}").strip()),
            "added_images": len(rows),
            "not_in_base": sum(1 for r in rows if not r["same_bytes_in_base"]),
            "images": rows,
        }
    return out


def program(root: Path, base: str, branch: str) -> dict:
    commits = git(root, "rev-list", "--no-merges", f"{base}..{branch}").split()
    runtime = []
    for c in commits:
        names = git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", c).splitlines()
        hit = [n for n in names if n.split("/", 1)[0] in ("scripts", "assets", "scenes") and not n.endswith(".import")]
        if hit:
            runtime.append({"commit": c, "subject": git(root, "log", "-1", "--format=%s", c).strip(), "runtime_files": hit})
    return {
        "branch": branch,
        "head": git(root, "rev-parse", branch).strip(),
        "non_merge_commits_ahead": len(commits),
        "commits_changing_scripts_assets_scenes": len(runtime),
        "runtime_commits": runtime,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--base", default="origin/dev")
    ap.add_argument("--branch", action="append", default=[], help="unmerged branch to reconcile (repeatable)")
    ap.add_argument("--program-branch", action="append", default=[], help="branch whose runtime-change ratio to count")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    ap.add_argument("--summary", action="store_true", help="print a short text summary to stderr")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    files = runtime_files(root)
    report = {
        "schema": "reef.job_art_measure/1",
        "head": git(root, "rev-parse", "HEAD").strip(),
        "base": a.base,
        "base_head": git(root, "rev-parse", a.base).strip(),
        "phase_art": phase_art(root),
        "code_drawing": code_drawing(root),
        "runtime_svg": runtime_svg(root, files),
        "asset_wiring": asset_wiring(root, files),
        "stranded": stranded(root, a.base, a.branch) if a.branch else {},
        "program": [program(root, a.base, b) for b in a.program_branch],
    }
    data = (json.dumps(report, indent=1) + "\n").encode("utf-8")
    if a.out:
        Path(a.out).write_bytes(data)
    else:
        sys.stdout.buffer.write(data)
    if a.summary:
        pa, cd = report["phase_art"], report["code_drawing"]
        print(f"phases {pa['phases']} in {pa['careers']} careers: {pa['phases_with_widget_art']} use painted widget art, "
              f"{pa['phases_drawing_own_picture']} draw their own picture; widget pngs {pa['widget_png_total']} "
              f"({pa['widget_png_matched_by_current_phase']} matched by a current phase)", file=sys.stderr)
        print("code drawing totals:", cd["totals"], file=sys.stderr)
        for job, v in cd["jobs"].items():
            print(f"  {job:22s} primitive={v['primitive_draw_calls']:4d} nodes={v['primitive_node_constructions']:3d} "
                  f"texture={v['texture_draw_calls']:3d}", file=sys.stderr)
        print("runtime svg:", len(report["runtime_svg"]), "asset wiring:", report["asset_wiring"]["counts"], file=sys.stderr)
        for br, v in report["stranded"].items():
            print(f"  stranded {br}: added={v['added_images']} not_in_base={v['not_in_base']} "
                  f"ahead={v['ahead']} behind={v['behind']}", file=sys.stderr)
        for p in report["program"]:
            print(f"  program {p['branch']}: {p['commits_changing_scripts_assets_scenes']} of "
                  f"{p['non_merge_commits_ahead']} commits change scripts/assets/scenes", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
