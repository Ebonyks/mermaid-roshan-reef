"""Measure fixed material patches in existing review captures; never alter art."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent / "whole_scene_revision"
EVIDENCE = BASE / "runtime_evidence"
FILES = ["meadow-boundary-canvas_screen_1_day.png",
         "meadow-boundary-canvas_screen_2_day.png",
         "rosette-canvas_screen_3_day.png", "rosette-canvas_screen_3_night.png"]
images = {name: Image.open(EVIDENCE / name).convert("RGB") for name in FILES}
assert all(im.size == (1280, 720) for im in images.values())

# Coordinates refer to the fixed castle camera, not moving actor positions.
patches = {
    "sky": [530, 25, 650, 75],
    "mountain": [640, 140, 700, 190],
    "rear_hedge": [590, 300, 650, 350],
    "lawn": [370, 530, 450, 545],
    "foreground_leaf_mass": [640, 625, 680, 660],
    "castle_wall": [790, 390, 810, 435],
    "bridge_deck": [825, 499, 850, 514],
    "water": [1035, 525, 1070, 545],
    "path": [945, 635, 975, 655],
    "swing_top_beam": [195, 332, 260, 339],
}

def measure(im, box):
    crop = im.crop(box)
    rgb = np.asarray(crop, dtype=float) / 255
    linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    lum = linear @ np.array([.2126, .7152, .0722])
    hsv = np.asarray(crop.convert("HSV"), dtype=float) / 255
    return {"median_linear_luminance": float(np.median(lum)),
            "median_HSV_saturation": float(np.median(hsv[:, :, 1])),
            "luminance_p10_p90": np.percentile(lum, [10, 90]).tolist()}

rows = []
for material, box in patches.items():
    day = measure(images[FILES[2]], box)
    night = measure(images[FILES[3]], box)
    rows.append({"material": material, "rect_xyxy": box, "day": day, "night": night,
                 "night_day_luminance_ratio": night["median_linear_luminance"] / day["median_linear_luminance"]})

findings = [
    ("P1", "Bellflower leaves", "Yellow-green highlights stand apart from adjacent teal/olive foliage in arrival and castle.", "Trial selective leaf highlight compression and hue alignment; preserve cream petals and leaf detail."),
    ("P1", "Foreground shrub clumps", "Pale rounded foreground leaves contrast strongly with dark fine-grained rear hedges; the repeated border reads as a separate asset family.", "Compare same-species foliage; grade individual clumps and reduce repetitive placement, preserving foreground depth."),
    ("P1", "Castle and bridge at night", "Large opaque surfaces remain nearly day-bright while landscape darkens; the discontinuity is broader than saturation.", "Separate ambient surfaces from windows, gold glints and doorway accents; test an opt-in night grade without painting over approved art."),
    ("P1", "Playground at night", "Swing and slide remain conspicuously bright against the dark lawn.", "Align ambient response with nearby props; retain readable interaction accents."),
    ("P2", "Arrival versus meadow foliage", "Mapped source patches show greater arrival saturation and cooler hue. This is regional evidence, not a whole-stage score.", "Compare matched foliage materials across the transition before applying a local grade."),
    ("P2", "Clouds and mountains", "Some overlay clouds are rounder and higher-contrast than the distant cloud field; pale mountains and clouds still provide useful depth.", "Review cloud edge, opacity and value at rest and maximum drift; do not globally desaturate sky or mountain art."),
    ("P2", "Grass and ground cover", "Broad yellow-green lawn and dark teal planting beds have strong material separation; sparse animated blades can look pasted on.", "Check blade base and highlight colors against their exact underlying lawn at every pose; retain path contrast."),
    ("P2", "Water and ripples", "Water shares the ambient night change, but white interaction ripples attract disproportionate attention in still captures.", "Review the complete alpha/fade cycle and contact feedback before adjusting highlight intensity."),
    ("P2", "Paths and rocks", "Paths remain legible and cooler pink stone separates from grass; no global recolor is justified by this review.", "Preserve clear left castle approach; inspect lighting continuity around healed plant masks and water banks."),
    ("P2", "Flowers, berries and new large plants", "Purple/pink/cream accents provide useful variety. New rosette and berry-fan highlights have already been compressed, but adjacent older assets remain inconsistent.", "Use approved nearby material references for each asset; never force all flower hues or species to match."),
    ("OPEN", "Roshan and animals", "Bright actor colors support visibility, but the actor moves between these day/night captures; fixed pixel differences cannot isolate actor lighting.", "Capture matched actor positions and interactions in all stages; preserve protected source colors."),
    ("OPEN", "HUD and touch feedback", "HUD is intentionally screen-space and bright; it must be evaluated for readability independently from landscape lighting.", "Review focus rings, pointers and feedback across day/night and touch states on the target device."),
]
report = {
    "status": "REVIEWED_CAPTURE_FINDINGS_NOT_VISUAL_ACCEPTANCE",
    "scope": "Three day composites and one castle night composite; all visible material families reviewed. This does not complete all-stage night or interaction-state coverage.",
    "sources": [{"path": str((EVIDENCE / f).relative_to(BASE.parent)).replace("\\", "/"),
                 "sha256": hashlib.sha256((EVIDENCE / f).read_bytes()).hexdigest()} for f in FILES],
    "method": "Fixed rectangular castle-camera patches, unmasked pixels, sRGB decoded to linear luminance. HSV saturation is diagnostic, not perceptual quality. Regions may contain painted shading and mixed pixels; ratios are not target grade values.",
    "castle_day_night_patches": rows,
    "visual_findings": [{"priority": p, "material": m, "observation": o, "next_action": a} for p, m, o, a in findings],
    "correction_order": ["Bellflower and pale foreground foliage trials", "Shared night ambient response with separate emissive accents", "Cross-stage material matching", "Per-cel and camera-boundary checks", "Target-device and owner review"],
    "rollback": "No runtime or artwork changed by this audit. Future corrections must be opt-in derived variants with original sources retained.",
    "remaining": ["Arrival and meadow matched night composites", "Actor/animal and touch-state coverage", "All material corrections and visual comparisons", "Device and owner acceptance"],
}
(BASE / "color_audit/RENDERED_COLOR_REVIEW.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
for row in rows:
    print(row["material"], round(row["night_day_luminance_ratio"], 3))
