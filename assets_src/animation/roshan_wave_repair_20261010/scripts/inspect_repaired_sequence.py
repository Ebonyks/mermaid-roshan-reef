#!/usr/bin/env python3
"""Read-only repair inspection adapter. Writes JSON metadata, never pixels/jobs.

Uses tools.sprite_pipeline geometry/inspect guards. Hidden authored shoulders
remain outside validated pixel points. A successful run does not accept artwork.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path("assets_src/animation/roshan_wave_repair_20261010")
CATALOG = Path("assets_src/animation/whole_sprite_pipeline_20261007/catalog.json")
COUNT = 41
K0_JOINTS = {"shoulder": [120, 103], "elbow": [115, 127],
             "wrist": [104, 150], "tip": [98, 165]}

sys.path.insert(0, str(ROOT))
from tools import sprite_pipeline as engine


def relative(root: Path, value: str, output: bool = False) -> Path:
    if Path(value).is_absolute():
        raise ValueError("Inputs/outputs must be project-relative paths")
    return engine.inside(root, value, output=output)


def pin(root: Path, path: Path, role: str) -> dict:
    path = engine.inside(root, path.relative_to(root).as_posix())
    if not path.is_file():
        raise ValueError(f"Required completed input is missing: {path}")
    return {"path": path.relative_to(root).as_posix(), "sha256": engine.sha(path),
            "bytes": path.stat().st_size, "role": role}


def ordered(rows: list[dict], key: str) -> dict[int, dict]:
    if len(rows) != COUNT or [row[key] for row in rows] != list(range(COUNT)):
        raise ValueError("Every input must cover all41 indices once, in order")
    return {row[key]: row for row in rows}


def frame_records(root: Path, directory: Path, role: str) -> list[dict]:
    actual = sorted(p.name for p in directory.glob("*.png") if p.stem.isdecimal())
    expected = [f"{i:04}.png" for i in range(COUNT)]
    if actual != expected:
        raise ValueError(f"Missing/extra numeric native frame files: {directory}")
    return [{"index": i, **pin(root, directory / name, role)}
            for i, name in enumerate(expected)]


def transform(point, scale: float, offset: list[float]):
    return None if point is None else [point[0] * scale + offset[0],
                                      point[1] * scale + offset[1]]


def joint_records(frames: list[dict], observed: dict[int, dict],
                  authored: dict[int, dict], sprite: bool) -> dict:
    records = []
    for frame in frames:
        i = frame["index"]
        if i in (0, COUNT - 1):
            scale, offset = (1, [0, 0]) if sprite else (819 / 256, [-48, 32])
            points = {name: transform(p, scale, offset) for name, p in K0_JOINTS.items()}
            row = {"index": i, "sha256": frame["sha256"], "points": points,
                   "flags": {"hand_open": False},
                   "point_authority": "Exact approved complete K0 source calibration under known whole-image mapping; no generated joint inference",
                   "canonical_source_landmarks": K0_JOINTS,
                   "canonical_to_this_canvas": {"scale": scale, "offset": offset}}
        else:
            source, target = observed[i], authored[i]
            scale, offset = (0.3125, [15, -10]) if sprite else (1, [0, 0])
            points = {"shoulder": None,
                      "elbow": source.get("raster_elbow_axis_intersection"),
                      "wrist": source.get("raster_wrist_cross_section_center"),
                      "tip": source.get("raster_longest_tip")}
            authored_points = {"shoulder": target.get("shoulder"), "elbow": target.get("elbow"),
                               "wrist": target.get("wrist"), "tip": target.get("longest_fingertip_target")}
            row = {"index": i, "sha256": frame["sha256"],
                   "points": {name: transform(p, scale, offset) for name, p in points.items()},
                   "authored_points": {name: transform(p, scale, offset) for name, p in authored_points.items()},
                   "flags": {"hand_open": source.get("hand_open")},
                   "point_authority": {"shoulder": "AUTHORED_HIDDEN_UNDER_FRILL; deliberately missing from validated points",
                                       "elbow": "RASTER_AXIS_ESTIMATE", "wrist": "RASTER_SKIN_CENTER",
                                       "tip": "RASTER_COLOR_ENVELOPE"},
                   "measurement_uncertainty_native_px": source.get("measurement_uncertainty_native_px"),
                   "observation_source_native_sha256": source["native_sha256"],
                   "transfer_to_this_canvas": {"scale": scale, "offset": offset},
                   "actual_final_rgba_landmarks_remeasured": False,
                   "limitation": "Transferred native RGB estimates; boundary-alpha edits remain separately reviewed. Hidden shoulder is authored, so complete exact W3 must stay PENDING."}
        records.append(row)
    return {"schema": "reef.repaired-sequence-partial-joints.v1", "frames": records,
            "all41_indices_present": True, "complete_actual_joint_coverage": False,
            "missing_measured_shoulder_indices": list(range(1, COUNT - 1)),
            "human_acceptance": False}


def build(root: Path, paint: Path, matte: Path, out: Path) -> dict:
    # A new output directory preserves previous exact-hash inspection revisions.
    if out.exists() and any(out.iterdir()):
        raise ValueError("Inspection output is already populated; choose a new revision path")
    catalog = engine.read_json(root / CATALOG)
    character = deepcopy(catalog["characters"]["roshan"])
    outfit = deepcopy(catalog["outfits"]["pink_base"])
    action = deepcopy(catalog["actions"]["wave"])
    if action["count"] != COUNT or action["fps"] != 24:
        raise ValueError("Canonical Roshan wave must be41 frames at24fps")
    action["key_gaps"] = []
    action["backend"] = {"auto_dispatch": False, "route": "INSPECTION_ONLY_GENERATION_DISABLED"}
    originals = ordered(engine.read_json(paint / "source_and_recipe_binding.json")["sources"], "frame")
    seed_plan = engine.read_json(matte / "source_and_seed_plan.json")
    if engine.inside(root, seed_plan["source_packet"]) != paint:
        raise ValueError("Matte source packet differs from --paint")
    copied = ordered(seed_plan["sources"], "index")
    matte_profile = seed_plan.get("matte_profile")
    if not matte_profile:
        matte_profile = engine.read_json(matte / "pixel_processing_stats.json")["parameters"]
    boundary_band = matte_profile.get("boundary_radius")
    if not isinstance(boundary_band, int) or boundary_band < 1:
        raise ValueError("Exact executed matte boundary profile must be declared")
    authored_data = engine.read_json(paint / "joint_geometry.json")
    authored = ordered(authored_data["frames"], "source_index")
    observed_data = engine.read_json(paint / "native_raster_geometry_observation.json")
    observed = ordered(observed_data["frames"], "frame")
    paint_frames = frame_records(root, paint, "complete_native_RGB_paint_output")
    native_frames = frame_records(root, matte / "native_rgba", "actual_complete_final_native_RGBA")
    sprite_frames = frame_records(root, matte / "frames", "actual_complete_final_256_RGBA")
    recipe = pin(root, paint / "paint_connected.lua", "actual_direct_whole_cel_pixel_writer")
    profile = pin(root, paint / "recipe_profile.json", "actual_authored_paint_profile")
    mask = pin(root, paint / "head_boundary_masks.json", "actual_source_preservation_mask")
    binding = engine.read_json(paint / "source_and_recipe_binding.json")
    for field, item in [("recipe_sha256", recipe), ("profile_sha256", profile), ("mask_sha256", mask)]:
        if binding[field] != item["sha256"]:
            raise ValueError(f"Paint binding is stale: {field}")
    if observed_data["source_master_sha256"] != engine.sha(paint / "wave_native_rgb.aseprite") or observed_data["authored_geometry_sha256"] != engine.sha(paint / "joint_geometry.json"):
        raise ValueError("Raster observation master/authored source is stale")
    common = [recipe, profile, mask,
              pin(root, paint / "source_and_recipe_binding.json", "paint_source_hash_binding"),
              pin(root, paint / "joint_geometry.json", "authored_targets_not_actual_joints"),
              pin(root, paint / "native_raster_geometry_observation.json", "partial_actual_pixel_observations"),
              pin(root, matte / "source_and_seed_plan.json", "per_frame_matte_seed_review_and_sources"),
              pin(root, matte / "recover_full_edges.lua", "actual_matte_whole_cel_pixel_writer"),
              pin(root, matte / "receipt.json", "completed_matte_processing_receipt"),
              pin(root, matte / "verification.json", "completed_matte_preservation_master_verification")]
    for entry in seed_plan["source_workflow_references"]:
        engine.pinned(root, entry)
    parent_profile = engine.read_json(paint / "recipe_profile.json").get("profile_parent")
    if parent_profile:
        common.append(pin(root, engine.pinned(root, parent_profile), "exact_authoring_profile_parent"))
    preparer = paint.parent / "prepare_full_draft.py"
    preparation_gap = not preparer.is_file() or engine.sha(preparer) != binding.get("preparation_script_sha256")
    if not preparation_gap:
        common.append(pin(root, preparer, "exact_preparation_script_recorded_by_paint_receipt"))
    for directory in (paint, matte):
        for p in sorted(directory.iterdir()):
            if p.is_file() and p.suffix.lower() in {".lua", ".py", ".json", ".md"} and p.name != "packet_manifest.json":
                if not any(e["path"] == p.relative_to(root).as_posix() for e in common):
                    common.append(pin(root, p, "source_workflow_metadata_or_review_reference"))
    k0 = deepcopy(catalog["sources"]["K0"])
    engine.pinned(root, k0)
    native_master = pin(root, matte / "native_final_wave.aseprite", "actual_final_native_editable_master")
    sprite_master = pin(root, matte / "wave.aseprite", "actual_final_256_editable_master")
    inventory = common + [native_master, sprite_master, pin(root, root / CATALOG, "canonical_Roshan_geometry_catalog")]
    derivations = {"native": [], "sprite": []}
    for i in range(COUNT):
        original = originals[i]; engine.pinned(root, original)
        row = copied[i]
        if engine.inside(root, row["source_path"]) != paint / f"{i:04}.png" or row["source_sha256"] != paint_frames[i]["sha256"]:
            raise ValueError(f"Matte paint source changed at{i}")
        preserved = {"path": row["preserved_source_path"], "sha256": row["preserved_source_sha256"]}
        engine.pinned(root, preserved)
        if preserved["sha256"] != paint_frames[i]["sha256"] or observed[i]["native_sha256"] != paint_frames[i]["sha256"]:
            raise ValueError(f"Copied/raster source hash mismatch at{i}")
        inventory.extend([original, paint_frames[i], preserved, native_frames[i], sprite_frames[i]])
        for lane, frame in (("native", native_frames[i]), ("sprite", sprite_frames[i])):
            endpoint = i in (0, COUNT - 1)
            parents = [k0] + common if endpoint else [original, paint_frames[i], preserved] + common
            edits = [{"operation": "approved_complete_K0_reuse", "foreign_part_pixels": False,
                      "mapping": {"native_size": [819, 819], "native_offset": [-48, 32], "actual_native_scale": 819 / 256,
                                  "sprite": "entire exact256px K0 source loaded directly"}}] if endpoint else [
                      {"operation": "local_arm_hand_paint_into_single_complete_native_cel", "source_padding_left": 128,
                       "appearance_part_copy": False, "limb_transform": False},
                      {"operation": "boundary_only_alpha_color_recovery", "boundary_band_native_px": boundary_band,
                       "exact_matte_profile": matte_profile,
                       "per_frame_holes": {k: v for k, v in row.items() if k.endswith("component") or k.endswith("components")}}]
            if lane == "sprite" and not endpoint:
                parents.append(native_frames[i])
                edits.append({"operation": "uniform_complete_frame_bilinear_mapping", "scale": 0.3125,
                              "whole_size": [240, 280], "translation": [15, -10], "canvas": [256, 256]})
            unused_endpoint_history = [original, paint_frames[i], preserved] if endpoint else []
            upstream = matte / "upstream_endpoint_matte" / f"{i:04}.png"
            if endpoint and upstream.is_file():
                history = pin(root, upstream, "unused_preserved_upstream_endpoint_matte")
                inventory.append(history)
                unused_endpoint_history.append(history)
            derivations[lane].append({"index": i, "sha256": frame["sha256"],
                "method": "approved_whole_frame_reuse" if endpoint else "whole_frame_drawn",
                "pixel_assembly": "NONE", "parents": parents, "edits": edits,
                "unused_endpoint_RGB_history": unused_endpoint_history,
                "scope": "Pinned declaration and ancestry only; actual method, pixels, identity and motion require exact review"})
    out.mkdir(parents=True, exist_ok=True)
    campaign_source = root / PACKET / "job.json"
    campaign_bytes = campaign_source.read_bytes()
    engine.read_json(campaign_source)  # Known project job only; no credentials/service logs.
    campaign_snapshot = out / "parent_campaign_snapshot.json"
    campaign_snapshot.write_bytes(campaign_bytes)
    generation = {"enabled": False, "generator_calls": 0, "gpu_calls": 0, "paid_calls": 0,
                  "budget_reset": False,
                  "parent_campaign_origin_at_capture": {"historical_path": campaign_source.relative_to(root).as_posix(),
                      "sha256_at_capture": engine.sha(campaign_snapshot),
                      "scope": "Original campaign may continue changing; literal snapshot is the immutable budget/provenance reference"},
                  "literal_parent_snapshot": pin(root, campaign_snapshot, "immutable_parent_campaign_snapshot")}
    jobs = {}
    for lane, frames, mapping, master in [("native", native_frames, {"scale": 3.2, "offset": [-48, 32]}, native_master),
                                          ("sprite", sprite_frames, {"scale": 1, "offset": [0, 0]}, sprite_master)]:
        frames_file = out / f"{lane}_frames.json"
        derivation_file = out / f"{lane}_derivation.json"
        joints_file = out / f"{lane}_joints.json"
        engine.write_json(frames_file, frames)
        engine.write_json(derivation_file, {"schema": "reef.whole-cel-repair-derivation.v1", "frames": derivations[lane]})
        engine.write_json(joints_file, joint_records(frames, observed, authored, lane == "sprite"))
        jobs[lane] = {"id": f"roshan_repaired_{matte.name}_{lane}", "character": character, "outfit": outfit,
                      "action": action, "sources": {"K0": k0}, "frames": frames,
                      "frames_manifest": frames_file.relative_to(root).as_posix(),
                      "mapping": mapping, "native_canvas": [768, 896] if lane == "native" else [256, 256],
                      "master": master, "derivation": pin(root, derivation_file, "whole_cel_derivation_declaration"),
                      "joints": joints_file.relative_to(root).as_posix(), "generation": generation}
    config = {"schema": "reef.repaired-sequence-inspection-adapter.v1", "paint": paint.relative_to(root).as_posix(),
              "matte": matte.relative_to(root).as_posix(), "all41_coverage": True, "exact_matte_profile": matte_profile,
              "canonical_catalog": pin(root, root / CATALOG, "reused_Roshan_geometry"), "generation": generation,
              "missing_archived_preparation_script": preparation_gap,
              "actual_K0_native_raster_scale": 819 / 256, "native_geometry_reference_scale": 3.2,
              "joint_policy": "Hidden authored shoulder excluded from validated points; projected native RGB observations remain partial. No fabricated W3 PASS.",
              "human_policy": "No model record is submitted as human review; exact human frame/full-speed lanes remain pending", "jobs": jobs}
    config_path = out / "inspection_config.json"
    engine.write_json(config_path, config)
    for job in jobs.values():
        job["frame_paths"] = [engine.pinned(root, row) for row in job["frames"]]
        job["catalog_sha256"] = engine.sha(config_path)
    native_checks, native_defects = engine.geometry(root, jobs["native"])
    native_report = {"schema": engine.SCHEMA, "job_id": jobs["native"]["id"], "checks": native_checks,
                     "defects": native_defects, "frame_hashes": [r["sha256"] for r in native_frames],
                     "W3_complete_actual_joint_coverage": "PENDING_AUTHORED_HIDDEN_SHOULDERS_AND_FINAL_RGBA_REVIEW",
                     "DELIVERY_ACCEPTED": False}
    sprite_report = engine.inspect(root, jobs["sprite"])
    sprite_report["adapter_scope"] = "Source-bound machine inspection only; hidden shoulders and human/full-speed lanes remain pending"
    sprite_report["exact_K0_export_file_bytes"] = [{"index": i, "same": sprite_frames[i]["sha256"] == k0["sha256"]} for i in (0, COUNT - 1)]
    sprite_report["derivation_archive_complete"] = not preparation_gap
    # All writes are strict JSON metadata; the engine owns finite and joint guards.
    engine.write_json(out / "native_geometry.json", native_report)
    engine.write_json(out / "sprite_inspection.json", sprite_report)
    unique = {entry["path"]: entry for entry in inventory}
    engine.write_json(out / "provenance_inventory.json", {"schema": "reef.repaired-sequence-inspection-provenance.v1",
        "files": [unique[key] for key in sorted(unique)], "generation": generation,
        "complete_actual_joint_coverage": False, "human_acceptance": False})
    return {"output": out.relative_to(root).as_posix(),
            "native_checks": {k: v["status"] for k, v in native_checks.items()},
            "sprite_checks": {k: v["status"] for k, v in sprite_report["checks"].items()},
            "candidate_ready": sprite_report["candidate_ready"],
            "generation_enabled": False, "DELIVERY_ACCEPTED": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--paint", required=True, help="Project-relative immutable full paint draft")
    parser.add_argument("--matte", required=True, help="Project-relative completed full matte candidate")
    parser.add_argument("--output", help="New project-relative metadata revision directory")
    args = parser.parse_args()
    root = args.root.resolve()
    paint, matte = relative(root, args.paint), relative(root, args.matte)
    out = relative(root, args.output or (PACKET / "provenance" / f"inspection_{matte.name}").as_posix(), output=True)
    result = build(root, paint, matte, out)
    print(__import__("json").dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
