#!/usr/bin/env python3
"""Sky Lagoon ambient-animal REALISM audit.

Static, headless companion to `scripts/probe_sky_lagoon_animals.gd`. The probe
proves the animals exist, bind, light, and exit correctly. This tool measures
whether they can read as *live animals in the painting*:

  1. atlas cell geometry  - per-pose subject size, foot-baseline drift, and the
                            source-to-screen oversampling factor;
  2. apparent scale       - each species' on-screen size against Roshan's card
                            and against its real-world body size;
  3. camera reachability  - whether the promenade's pan clamp can ever place the
                            camera on a habitat's page, per device aspect ratio;
  4. mural footing        - what the panorama actually paints under each
                            authored foot baseline (ground, foliage, rail, water);
  5. socket drift         - how far an unlocked animal card slides against its
                            painted footing across its own camera window;
  6. locomotion           - the authored speeds and dwells restated in body
                            lengths per second and exact patrol cycle time.

Everything is derived from the tracked art plus the constants in
scripts/arena/sky_lagoon_promenade.gd. No Godot, display, or capture required.

    python3 tools/audit_sky_lagoon_animal_realism.py \
        --json-out docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02_METRICS.json \
        --sheet-out docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02_FOOTING.jpg
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw

# ---- mirrored from scripts/arena/sky_lagoon_promenade.gd --------------------
CAM_DIST = 47.0
CAM_H = 9.5
CAM_FOV = 38.0
BACKDROP_Z = -18.0
HALF_W = 72.0
SCREEN_HALF_W = 72.0            # BACKDROP_TILE_SIZE.x * BACKDROP_COLUMNS * 0.5
MURAL_TOP_Y = 33.5
MURAL_BOTTOM_Y = -14.5
ROSHAN_CARD_H = 7.8
ROSHAN_CARD_Z = 0.2
ATLAS_COLUMNS = 2
ATLAS_ROWS = 2
PAGE_SPAN = 48.0
ANIMAL_PAGE_CENTERS = [-48.0, 0.0, 48.0]
EDGE_MARGIN = 5.0

MURAL_DIR = "assets/flats/sky_lagoon/main"
MURAL_TILE = "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
MURAL_COLUMNS, MURAL_ROWS, MURAL_TILE_PX = 6, 2, 1024
ANIMAL_DIR = "assets/sprites/sky_lagoon/animals"

# Roshan is a four-year-old; her card is the scene's only human scale reference.
ROSHAN_HEIGHT_CM = 105.0

# id -> authored definition + the reference standing height of the real animal
# (top of head, natural posture) used only for the scale-plausibility column.
ANIMALS = [
    {"id": "otter", "bob": 0.045, "page": 0, "habitat": "arrival_shore",
     "path": [(-62.0, 3.55, -5.8), (-60.0, 3.82, -5.8), (-57.8, 3.58, -5.8)],
     "height": 2.6, "speed": 0.52, "exit_speed": 12.0, "dwell_s": 1.4,
     "real_cm": 30.0, "real_note": "river otter, shoulder height"},
    {"id": "frog", "bob": 0.18, "page": 0, "habitat": "arrival_shore",
     "path": [(-61.7, 3.25, -6.1), (-59.8, 3.48, -6.1), (-58.0, 3.30, -6.1)],
     "height": 1.65, "speed": 0.72, "exit_speed": 10.5, "dwell_s": 1.7,
     "real_cm": 4.5, "real_note": "Pacific tree frog, snout-vent"},
    {"id": "hare", "bob": 0.12, "page": 1, "habitat": "west_meadow_edge",
     "path": [(-20.7, 3.42, -4.8), (-18.9, 3.72, -4.8), (-17.2, 3.50, -4.8)],
     "height": 3.1, "speed": 0.66, "exit_speed": 13.5, "dwell_s": 1.6,
     "real_cm": 32.0, "real_note": "snowshoe hare, sitting"},
    {"id": "squirrel", "bob": 0.055, "page": 1, "habitat": "west_meadow_edge",
     "path": [(-20.7, 4.38, -7.2), (-18.9, 4.70, -7.2), (-17.2, 4.45, -7.2)],
     "height": 2.9, "speed": 0.82, "exit_speed": 14.5, "dwell_s": 1.25,
     "real_cm": 18.0, "real_note": "Douglas squirrel, sitting"},
    {"id": "raccoon", "bob": 0.035, "page": 2, "habitat": "castle_shrub_edge",
     "path": [(29.0, 4.15, -7.0), (31.4, 4.55, -7.0), (34.0, 4.28, -7.0)],
     "height": 3.0, "speed": 0.58, "exit_speed": 13.0, "dwell_s": 1.8,
     "real_cm": 30.0, "real_note": "raccoon, shoulder height"},
]

ASPECTS = [("16:9", 16 / 9), ("18:9", 2.0), ("19:9", 19 / 9),
           ("19.5:9", 19.5 / 9), ("20:9", 20 / 9), ("20.5:9", 20.5 / 9),
           ("21:9", 21 / 9)]


# ---- camera model ----------------------------------------------------------
def frustum_half_h(z: float) -> float:
    return math.tan(math.radians(CAM_FOV * 0.5)) * abs(CAM_DIST - z)


def frustum_half_w(z: float, aspect: float) -> float:
    return frustum_half_h(z) * aspect


def pan_limit(aspect: float) -> float:
    """SideScrollStage.screen_pan_limit for this stage: the mural may never
    leave frame, so the lens can only travel this far from the stage centre."""
    return max(0.0, SCREEN_HALF_W - frustum_half_w(BACKDROP_Z, aspect))


def page_of(camera_x: float) -> int:
    return max(0, min(2, int(math.floor((camera_x + HALF_W) / PAGE_SPAN))))


# ---- mural helpers ---------------------------------------------------------
def load_mural() -> Image.Image:
    width = MURAL_TILE_PX * MURAL_COLUMNS
    height = MURAL_TILE_PX * MURAL_ROWS
    mural = Image.new("RGB", (width, height))
    for row in range(MURAL_ROWS):
        for column in range(MURAL_COLUMNS):
            tile = Image.open(
                os.path.join(MURAL_DIR, MURAL_TILE % (row, column))).convert("RGB")
            mural.paste(tile, (column * MURAL_TILE_PX, row * MURAL_TILE_PX))
    return mural


def mural_px(x: float, y: float, size: tuple[int, int]) -> tuple[float, float]:
    width, height = size
    return ((x + HALF_W) / (HALF_W * 2.0) * width,
            (MURAL_TOP_Y - y) / (MURAL_TOP_Y - MURAL_BOTTOM_Y) * height)


# ROUTE_PAINTED from the promenade: the painted spine Roshan actually walks.
ROUTE_PAINTED = [(-68.0, -2.6), (-58.0, -3.4), (-40.0, -4.0), (-20.0, -3.6),
                 (0.0, -3.4), (20.0, -3.6), (34.0, -4.0), (43.0, -2.6),
                 (52.5, -2.0)]


def point_to_segment(point, start, finish) -> float:
    sx, sy = finish[0] - start[0], finish[1] - start[1]
    length_squared = sx * sx + sy * sy
    if length_squared <= 1e-5:
        return math.dist(point, start)
    amount = max(0.0, min(1.0, ((point[0] - start[0]) * sx
                                + (point[1] - start[1]) * sy) / length_squared))
    return math.dist(point, (start[0] + sx * amount, start[1] + sy * amount))


def classify_footing(patch: np.ndarray) -> str:
    """Name what the panorama paints in a sampled patch. Deliberately coarse:
    the tracked contact sheet is the readable evidence, this is the index."""
    mean = patch.reshape(-1, 3).mean(axis=0) / 255.0
    hue, light, sat = colorsys.rgb_to_hls(*mean)
    hue_deg = hue * 360.0
    if sat < 0.16:
        return "stone/neutral"
    if 150.0 <= hue_deg < 230.0:
        return "water"
    if 60.0 <= hue_deg < 150.0:
        return "vegetation"
    if 260.0 <= hue_deg < 350.0:
        return "painted path"
    return "other"


# ---- measurements ----------------------------------------------------------
def measure_atlases() -> dict:
    result = {}
    for animal in ANIMALS:
        card_h = animal["height"]
        card_z = animal["path"][0][2]
        per_sheet = {}
        for sheet in ("idle", "startle"):
            path = os.path.join(ANIMAL_DIR, "%s_%s_atlas.png" % (animal["id"], sheet))
            image = Image.open(path).convert("RGBA")
            atlas_w, atlas_h = image.size
            cell_w = atlas_w // ATLAS_COLUMNS
            cell_h = atlas_h // ATLAS_ROWS
            cells = []
            for row in range(ATLAS_ROWS):
                for column in range(ATLAS_COLUMNS):
                    cell = image.crop((column * cell_w, row * cell_h,
                                       (column + 1) * cell_w, (row + 1) * cell_h))
                    alpha = np.array(cell)[:, :, 3]
                    ys, xs = np.nonzero(alpha > 24)
                    if len(ys) == 0:
                        cells.append({"frame": row * ATLAS_COLUMNS + column,
                                      "empty": True})
                        continue
                    subject_h = int(ys.max() - ys.min() + 1)
                    world_h = card_h * subject_h / cell_h
                    screen_px = world_h / (frustum_half_h(card_z) * 2.0) * 720.0
                    cells.append({
                        "frame": row * ATLAS_COLUMNS + column,
                        "subject_px_h": subject_h,
                        "subject_px_w": int(xs.max() - xs.min() + 1),
                        "foot_baseline_frac": round(float(ys.max()) / cell_h, 4),
                        "alpha_coverage": round(float((alpha > 24).sum()) / alpha.size, 4),
                        "visible_world_h": round(world_h, 3),
                        "screen_px_h_at_720p": round(screen_px, 1),
                        "source_oversample_x": round(subject_h / max(1e-6, screen_px), 2),
                    })
            baselines = [c["foot_baseline_frac"] for c in cells if not c.get("empty")]
            heights = [c["subject_px_h"] for c in cells if not c.get("empty")]
            per_sheet[sheet] = {
                "cell_px": cell_h,
                "cells": cells,
                "foot_baseline_drift_frac": round(max(baselines) - min(baselines), 4),
                "foot_baseline_drift_world": round(
                    (max(baselines) - min(baselines)) * card_h, 3),
                "subject_height_drift_pct": round(
                    (max(heights) / min(heights) - 1.0) * 100.0, 1),
            }
        result[animal["id"]] = per_sheet
    return result


def measure_scale() -> dict:
    roshan_px = ROSHAN_CARD_H / (frustum_half_h(ROSHAN_CARD_Z) * 2.0) * 720.0
    atlases = measure_atlases()
    rows = {}
    for animal in ANIMALS:
        cells = [c for c in atlases[animal["id"]]["idle"]["cells"] if not c.get("empty")]
        mean_px = sum(c["screen_px_h_at_720p"] for c in cells) / len(cells)
        apparent_cm = mean_px / roshan_px * ROSHAN_HEIGHT_CM
        rows[animal["id"]] = {
            "mean_visible_screen_px": round(mean_px, 1),
            "fraction_of_roshan": round(mean_px / roshan_px, 4),
            "apparent_height_cm": round(apparent_cm, 1),
            "real_height_cm": animal["real_cm"],
            "real_note": animal["real_note"],
            "scale_error_x": round(apparent_cm / animal["real_cm"], 2),
        }
    return {"roshan_card_screen_px": round(roshan_px, 1),
            "roshan_assumed_cm": ROSHAN_HEIGHT_CM, "species": rows}


def measure_reachability() -> dict:
    out = {}
    for label, aspect in ASPECTS:
        limit = pan_limit(aspect)
        species = {}
        for animal in ANIMALS:
            x0 = min(p[0] for p in animal["path"])
            x1 = max(p[0] for p in animal["path"])
            card_z = animal["path"][0][2]
            view = frustum_half_w(card_z, aspect)
            full = partial = False
            window = [None, None]
            steps = 4000
            for i in range(steps + 1):
                camera_x = -limit + 2.0 * limit * i / steps if limit > 0 else 0.0
                if page_of(camera_x) != animal["page"]:
                    continue
                if camera_x - view <= x1 and x0 <= camera_x + view:
                    partial = True
                if camera_x - view <= x0 and x1 <= camera_x + view:
                    full = True
                    window[0] = camera_x if window[0] is None else min(window[0], camera_x)
                    window[1] = camera_x if window[1] is None else max(window[1], camera_x)
            species[animal["id"]] = {
                "page": animal["page"],
                "fully_framed": full,
                "partially_framed": partial,
                "camera_x_window": [round(window[0], 2), round(window[1], 2)]
                if full else None,
                "camera_window_width": round(window[1] - window[0], 2) if full else 0.0,
            }
        out[label] = {
            "aspect": round(aspect, 4),
            "pan_limit": round(limit, 2),
            "pannable_width": round(limit * 2.0, 2),
            "pages_reachable": sorted({page_of(-limit), page_of(0.0), page_of(limit)}),
            "species": species,
        }
    # the exact aspect at which page 0 and page 2 become unreachable
    threshold = (SCREEN_HALF_W - PAGE_SPAN / 2.0) / (
        math.tan(math.radians(CAM_FOV * 0.5)) * abs(CAM_DIST - BACKDROP_Z))
    out["_page_reachability_threshold_aspect"] = round(threshold, 4)
    out["_page_reachability_threshold_label"] = "%.2f:9" % (threshold * 9.0)
    return out


def measure_socket_drift(reach: dict) -> dict:
    """Animal cards are never registered as mural sockets, so the painted point
    behind a card slides as the lens pans. Report units of slide per unit of
    camera pan, and the total across each species' own framing window."""
    out = {}
    backdrop_distance = CAM_DIST - BACKDROP_Z
    for animal in ANIMALS:
        card_distance = CAM_DIST - animal["path"][0][2]
        factor = abs(1.0 - backdrop_distance / card_distance)
        window = reach["16:9"]["species"][animal["id"]]["camera_window_width"]
        body = max(abs(p[0] - q[0]) for p in animal["path"] for q in animal["path"]) or 1.0
        out[animal["id"]] = {
            "slide_per_camera_unit": round(factor, 4),
            "camera_window_16_9": round(window, 2),
            "total_slide_world_units": round(factor * window, 2),
            "slide_vs_own_path_length": round(factor * window / body, 2),
        }
    return out


def measure_locomotion(atlases: dict) -> dict:
    """Express the authored constants in units a body can be judged by: body
    lengths per second, and the exact period of the ping-pong patrol loop."""
    out = {}
    for animal in ANIMALS:
        card_h = animal["height"]
        cells = [c for c in atlases[animal["id"]]["idle"]["cells"] if not c.get("empty")]
        cell_px = atlases[animal["id"]]["idle"]["cell_px"]
        body = max(c["subject_px_w"] for c in cells) / cell_px * card_h
        legs = [abs(animal["path"][i + 1][0] - animal["path"][i][0])
                for i in range(len(animal["path"]) - 1)]
        travel = sum(leg / animal["speed"] for leg in legs)
        # A -> B -> C -> B -> A, dwelling at every arrival.
        period = 2.0 * travel + 2.0 * len(legs) * animal["dwell_s"]
        out[animal["id"]] = {
            "body_length_world": round(body, 3),
            "patrol_length_world": round(sum(legs), 3),
            "patrol_length_in_bodies": round(sum(legs) / body, 2),
            "idle_body_lengths_per_s": round(animal["speed"] / body, 3),
            "exit_body_lengths_per_s": round(animal["exit_speed"] / body, 2),
            "patrol_cycle_s": round(period, 2),
            "authored_bob": animal["bob"],
            "worst_baseline_drift_over_bob": round(max(
                atlases[animal["id"]][sheet]["foot_baseline_drift_world"]
                for sheet in ("idle", "startle")) / animal["bob"], 1),
        }
    return out


def measure_footing(mural: Image.Image) -> dict:
    array = np.asarray(mural)
    out = {}
    for animal in ANIMALS:
        card_h = animal["height"]
        samples = []
        for (x, y, _z) in animal["path"]:
            foot_y = y - card_h * 0.5
            px, py = mural_px(x, foot_y, mural.size)
            half = int(0.55 / (HALF_W * 2.0) * mural.size[0])
            x0 = max(0, int(px) - half)
            x1 = min(mural.size[0], int(px) + half)
            y0 = max(0, int(py) - half // 2)
            y1 = min(mural.size[1], int(py) + half)
            patch = array[y0:y1, x0:x1]
            samples.append({
                "world": [x, round(foot_y, 3)],
                "mural_px": [int(px), int(py)],
                "painted": classify_footing(patch),
                "mean_rgb": [int(v) for v in patch.reshape(-1, 3).mean(axis=0)],
            })
        painted = {s["painted"] for s in samples}
        clearance = min(
            min(point_to_segment((x, y - card_h * 0.5), ROUTE_PAINTED[i],
                                 ROUTE_PAINTED[i + 1])
                for i in range(len(ROUTE_PAINTED) - 1))
            for (x, y, _z) in animal["path"])
        out[animal["id"]] = {
            "foot_world_y": round(animal["path"][0][1] - card_h * 0.5, 3),
            "samples": samples,
            "painted_footing": sorted(painted),
            "route_clearance_world": round(clearance, 2),
        }
    return out


def build_sheet(mural: Image.Image, path: str) -> None:
    """One compact review sheet: each authored habitat, its path box (yellow)
    and its foot baseline (red) drawn on the panorama at native resolution."""
    marked = mural.copy()
    draw = ImageDraw.Draw(marked)
    route = [(-68.0, -2.6), (-58.0, -3.4), (-40.0, -4.0), (-20.0, -3.6),
             (0.0, -3.4), (20.0, -3.6), (34.0, -4.0), (43.0, -2.6), (52.5, -2.0)]
    draw.line([mural_px(x, y, marked.size) for x, y in route],
              fill=(255, 40, 160), width=6)
    crops = []
    for animal in ANIMALS:
        card_h = animal["height"]
        x0 = min(p[0] for p in animal["path"]) - card_h * 0.5
        x1 = max(p[0] for p in animal["path"]) + card_h * 0.5
        top = max(p[1] for p in animal["path"]) + card_h * 0.5
        foot = min(p[1] for p in animal["path"]) - card_h * 0.5
        draw.rectangle([mural_px(x0, top, marked.size), mural_px(x1, foot, marked.size)],
                       outline=(255, 240, 0), width=5)
        draw.line([mural_px(x0, foot, marked.size), mural_px(x1, foot, marked.size)],
                  fill=(255, 0, 0), width=6)
        pad = 11.0
        box = (int(mural_px(x0 - pad, 0, marked.size)[0]),
               int(mural_px(0, top + 6.0, marked.size)[1]),
               int(mural_px(x1 + pad, 0, marked.size)[0]),
               int(mural_px(0, foot - 5.0, marked.size)[1]))
        crop = marked.crop(box)
        crops.append((animal["id"], crop.resize(
            (560, int(crop.height * 560 / crop.width)), Image.LANCZOS)))
    cell_h = max(c.height for _i, c in crops)
    sheet = Image.new("RGB", (560 * 2, cell_h * 3), (12, 14, 22))
    pen = ImageDraw.Draw(sheet)
    for index, (animal_id, crop) in enumerate(crops):
        column, row = index % 2, index // 2
        sheet.paste(crop, (column * 560, row * cell_h))
        pen.text((column * 560 + 10, row * cell_h + 8), animal_id.upper(),
                 fill=(255, 255, 255))
    pen.text((560 + 12, 2 * cell_h + 12),
             "yellow: authored card box   red: foot baseline   magenta: player route",
             fill=(220, 220, 230))
    sheet.save(path, quality=82, optimize=True)


def verify_sheet(path: str, columns: int, rows: int, baseline_tol: float,
                 height_tol_pct: float, airborne: set[int]) -> int:
    """Delivery gate for a new or regenerated pose sheet.

    The defect this exists to catch: `Sprite3D` centres each atlas cell, so a
    subject that sits at a different height inside its cell teleports the animal
    vertically on every frame change. The shipped 2x2 sheets drift up to 21% of
    a cell (0.6 world units, 17x the authored bob). A replacement sheet must
    draw every grounded pose with its feet on one shared canvas baseline.

    Airborne poses are the intended exception: declare them with
    --airborne-frames and they may sit ABOVE the shared baseline (that is the
    hop arc, carried by the art instead of by a runtime sine) but never below.

    Subject height is reported, not gated by default: a crouch really is shorter
    than a stretched bound. Tighten --height-tol only when comparing poses that
    should be the same size.

    Returns a process exit code: 0 pass, 1 fail.
    """
    image = Image.open(path).convert("RGBA")
    cell_w = image.size[0] // columns
    cell_h = image.size[1] // rows
    cells = []
    for row in range(rows):
        for column in range(columns):
            cell = image.crop((column * cell_w, row * cell_h,
                               (column + 1) * cell_w, (row + 1) * cell_h))
            alpha = np.array(cell)[:, :, 3]
            ys, xs = np.nonzero(alpha > 24)
            index = row * columns + column
            if len(ys) == 0:
                cells.append({"frame": index, "empty": True})
                continue
            cells.append({
                "frame": index,
                "baseline": float(ys.max()) / cell_h,
                "height": int(ys.max() - ys.min() + 1),
                "coverage": float((alpha > 24).sum()) / alpha.size,
            })
    filled = [c for c in cells if not c.get("empty")]
    failures = 0
    if len(filled) != columns * rows:
        print("SHEET|cells|FAIL|%d of %d populated" % (len(filled), columns * rows))
        failures += 1
    if not filled:
        return 1
    grounded = [c for c in filled if c["frame"] not in airborne]
    baselines = sorted(c["baseline"] for c in (grounded or filled))
    heights = sorted(c["height"] for c in filled)
    median_baseline = baselines[len(baselines) // 2]
    median_height = heights[len(heights) // 2]
    print("%-6s %-9s %9s %9s %9s" % ("frame", "kind", "baseline", "dBase",
                                     "dHeight%"))
    for cell in cells:
        if cell.get("empty"):
            print("%-6d %-9s %9s" % (cell["frame"], "-", "EMPTY"))
            continue
        is_airborne = cell["frame"] in airborne
        d_base = cell["baseline"] - median_baseline
        d_height = (cell["height"] / median_height - 1.0) * 100.0
        # airborne poses may float above the shared baseline, never below it
        bad = d_base > baseline_tol if is_airborne \
            else abs(d_base) > baseline_tol
        bad = bad or abs(d_height) > height_tol_pct
        failures += 1 if bad else 0
        print("%-6d %-9s %9.4f %+9.4f %+9.1f%s" % (
            cell["frame"], "airborne" if is_airborne else "grounded",
            cell["baseline"], d_base, d_height,
            "   <-- OUT OF TOLERANCE" if bad else ""))
    print("SHEET|%s|%s|baseline_tol=%.4f height_tol=%.1f%% cell=%dx%d" % (
        os.path.basename(path), "PASS" if failures == 0 else "FAIL",
        baseline_tol, height_tol_pct, cell_w, cell_h))
    return 0 if failures == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out")
    parser.add_argument("--sheet-out")
    parser.add_argument("--verify-sheet",
                        help="delivery gate for one pose sheet PNG")
    parser.add_argument("--grid", default="4x4",
                        help="cell grid of the sheet being verified")
    parser.add_argument("--baseline-tol", type=float, default=0.016,
                        help="max foot-baseline deviation, fraction of cell")
    parser.add_argument("--height-tol", type=float, default=40.0,
                        help="max subject-height deviation, percent (coarse "
                             "identity-drift catch; pose-driven change is legal)")
    parser.add_argument("--airborne-frames", default="",
                        help="comma-separated frame indices allowed to sit "
                             "above the shared foot baseline")
    args = parser.parse_args()

    if args.verify_sheet:
        columns, rows = (int(v) for v in args.grid.lower().split("x"))
        airborne = {int(v) for v in args.airborne_frames.split(",") if v.strip()}
        raise SystemExit(verify_sheet(args.verify_sheet, columns, rows,
                                      args.baseline_tol, args.height_tol,
                                      airborne))

    mural = load_mural()
    atlases = measure_atlases()
    reach = measure_reachability()
    report = {
        "target": "Sky Lagoon promenade ambient animals",
        "source": "scripts/arena/sky_lagoon_promenade.gd",
        "canvas": "1280x720 base, canvas_items/expand, Godot Mobile renderer",
        "atlas_geometry": atlases,
        "locomotion": measure_locomotion(atlases),
        "apparent_scale": measure_scale(),
        "camera_reachability": reach,
        "mural_socket_drift": measure_socket_drift(reach),
        "painted_footing": measure_footing(mural),
    }
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
            handle.write("\n")
    if args.sheet_out:
        build_sheet(mural, args.sheet_out)

    scale = report["apparent_scale"]["species"]
    print("species   apparent   real   error  route  footing")
    for animal in ANIMALS:
        row = scale[animal["id"]]
        foot = report["painted_footing"][animal["id"]]
        print("%-9s %5.1fcm %6.1fcm %5.2fx  %4.1fu  %s" % (
            animal["id"], row["apparent_height_cm"], row["real_height_cm"],
            row["scale_error_x"], foot["route_clearance_world"],
            "/".join(foot["painted_footing"])))
    print("\naspect   pan     pages   species never framed")
    for label, _aspect in ASPECTS:
        entry = reach[label]
        missing = [k for k, v in entry["species"].items() if not v["fully_framed"]]
        print("%-8s %5.1f  %-9s %s" % (label, entry["pan_limit"],
                                       entry["pages_reachable"],
                                       ", ".join(missing) or "-"))
    print("\npage 0/2 become unreachable above aspect %s" %
          reach["_page_reachability_threshold_label"])


if __name__ == "__main__":
    main()
