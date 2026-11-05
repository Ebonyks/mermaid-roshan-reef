"""Inspect actual current-rig capture with the seed's unchanged geometry functions."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("seed_audit", ROOT / "tools/seed_audit.py")
seed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)
folder = Path(sys.argv[1])
samples = json.loads((folder / "samples.json").read_text())
rig = json.loads((ROOT / "godot/rig.json").read_text())
reports = {}
for mesh in rig["meshes"]:
    points = np.array(mesh["vertices"])
    triangles = np.array(mesh["triangles"])
    weights = mesh["weights"]
    inverse = np.array([np.linalg.inv(seed.affine(samples[0]["bones"][name])) for name in weights])
    alpha = np.array(Image.open(ROOT / "godot" / mesh["texture"]))[:, :, 3]
    centers = points[triangles].mean(axis=1).astype(int)
    visible = alpha[np.clip(centers[:, 1], 0, 1023), np.clip(centers[:, 0], 0, 1023)] > 192
    low, high, flips = 1.0, 1.0, 0
    failures = []
    for row in samples:
        _, determinant, strain = seed.geometry(points, triangles, weights, inverse, row)
        values = strain[visible]
        local_low, local_high = float(values.min()), float(values.max())
        local_flips = int(np.sum(determinant[visible] <= 0))
        low, high, flips = min(low, local_low), max(high, local_high), flips + local_flips
        if local_low < .80 or local_high > 1.20 or local_flips:
            failures.append(row["frame"])
    reports[mesh["name"]] = {"min_visible_strain": low, "max_visible_strain": high,
                             "inverted_visible_triangles": flips, "failed_frames": failures}
reference = seed.pixel_checks(Image.open(folder / "rgba/0000.png").convert("RGBA"))
alpha_failures, crop_failures = [], []
for row in samples:
    pixels = seed.pixel_checks(Image.open(folder / "rgba" / f"{row['frame']:04d}.png").convert("RGBA"))
    if not seed.seam_pass(pixels, reference):
        alpha_failures.append({"frame": row["frame"], **pixels})
    if pixels["edge_alpha_pixels"]:
        crop_failures.append(row["frame"])
motion = {}
for name in samples[0]["bones"]:
    angles = np.unwrap([np.arctan2(row["bones"][name][1], row["bones"][name][0]) for row in samples])
    speed = np.diff(angles) * 30 * 180 / np.pi
    acceleration = np.diff(speed) * 30
    maximum_speed = float(np.abs(speed).max())
    maximum_acceleration = float(np.abs(acceleration).max())
    motion[name] = {"max_degrees_per_second": maximum_speed,
                    "max_degrees_per_second_squared": maximum_acceleration,
                    "pass": maximum_speed <= 140 and maximum_acceleration <= 650}
reference_scale = samples[0]["actor_scale"]
scale_pass = (all(row["actor_scale"] == reference_scale for row in samples)
              and all(abs(value - .62) <= 1e-7 for value in reference_scale))
report = {
    "lane": "SOURCE_ONLY_NUMERICAL_DIAGNOSTIC",
    "frames": len(samples), "times_seconds": [samples[0]["time"], samples[-1]["time"]],
    "meshes": reports, "alpha_reference": reference, "alpha_failed_frames": alpha_failures,
    "crop_failed_frames": crop_failures, "motion": motion, "constant_actor_scale": scale_pass,
    "floors": {"visible_strain": [.80, 1.20], "flips": 0, "speed_degrees_s": 140,
               "acceleration_degrees_s2": 650, "seed_interior_hole_allowance_pixels": 8},
    "seed_geometry_helper_sha256": hashlib.sha256((ROOT / "tools/seed_audit.py").read_bytes()).hexdigest(),
    "geometry_pass": all(not value["failed_frames"] for value in reports.values()),
    "motion_pass": all(value["pass"] for value in motion.values()),
    "alpha_pass": not alpha_failures and not crop_failures,
    "limits": "30-fps actual source frames only. Does not prove full facing turns, side-view propulsion, natural palm acting, hair follow-through, production integration or device/child/owner acceptance. No thresholds relaxed."
}
(ROOT / "inspection.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({key: report[key] for key in ["frames", "geometry_pass", "motion_pass", "alpha_pass", "constant_actor_scale"]}))
print("geometry failures", {key: len(value["failed_frames"]) for key, value in reports.items()})
print("alpha failures", len(alpha_failures))
