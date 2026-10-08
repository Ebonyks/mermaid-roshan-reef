#!/usr/bin/env python3
"""Reusable whole-sprite preparation, review and bounded repair requests.

Never edits character pixels or starts a model job. Aseprite imports complete
drawings; generation is explicitly dispatched by Codex from the saved request.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "reef.whole-sprite-pipeline.v1"
MEASURER = "docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py"
PIXEL_ROLES = {"identity", "outfit", "pose"}
REVIEW_AXES = ("identity", "outfit", "topology", "motion")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(data, indent=2, allow_nan=False) + "\n"
    staging = path.with_name(path.name + ".next")
    try:
        staging.write_bytes(encoded.encode("utf-8"))
        staging.replace(path)
    finally:
        staging.unlink(missing_ok=True)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@contextmanager
def ledger_lock(path: Path):
    lock = path.with_suffix(path.suffix + ".lock")
    try:
        with lock.open("x", encoding="utf-8"):
            pass
    except FileExistsError as error:
        raise ValueError("Campaign ledger is in use; retry after the other operation finishes") from error
    try:
        yield
    finally:
        lock.unlink()


def inside(root: Path, value: str, output: bool = False) -> Path:
    path = (root / value).resolve()
    try:
        relative = path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"Path leaves project: {value}") from error
    if any(part.lower() in {".secrets", ".git", ".codex", ".aws"} for part in relative.parts):
        raise ValueError(f"Private/internal path: {value}")
    if path.suffix.lower() in {".jks", ".keystore"}:
        raise ValueError("Keystore paths are forbidden")
    if output and (not relative.parts or relative.parts[0] not in {"assets_src", "tmp"}):
        raise ValueError("Candidate output must stay in assets_src/ or tmp/")
    return path


def pinned(root: Path, entry: dict) -> Path:
    path = inside(root, entry["path"])
    actual = None
    if path.is_file():
        mode = entry.get("hash_normalization")
        if mode is None:
            actual = sha(path)
        elif mode == "git_text_lf" and path.suffix.lower() in {".json", ".md", ".txt", ".log", ".py", ".lua"}:
            actual = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        else:
            raise ValueError("Unsupported metadata hash normalization; image/native binary hashes stay byte-exact")
    if actual != entry["sha256"]:
        raise ValueError(f"Missing or changed pinned source: {entry['path']}")
    return path


def image_pixels(path: Path, cell: list | None = None) -> bytes:
    with Image.open(path) as source:
        image = source.convert("RGBA")
        if cell:
            x, y, w, h = cell
            if min(x, y) < 0 or min(w, h) < 1 or x + w > image.width or y + h > image.height:
                raise ValueError(f"Invalid cell in {path.name}")
            image = image.crop((x, y, x + w, y + h))
        return image.tobytes()


def frame_clock(count: int, fps: int) -> list[int]:
    # Aseprite uses integer milliseconds: distributed rounding, never 41ms x41.
    tick = lambda n: (n * 1000 + fps // 2) // fps
    return [tick(i + 1) - tick(i) for i in range(count)]


def alpha_islands(path: Path, minimum_area: int) -> dict:
    try:
        import cv2
        import numpy as np
    except ModuleNotFoundError as error:
        return check("PENDING", f"Alpha component dependency unavailable: {error.name}")
    with Image.open(path) as image:
        alpha = np.array(image.convert("RGBA"))[:, :, 3]
    count, _, stats, _ = cv2.connectedComponentsWithStats((alpha > 16).astype(np.uint8), 8)
    parts = [{"box": [int(v) for v in row[:4]], "area": int(row[4])} for row in stats[1:]]
    parts.sort(key=lambda row: row["area"], reverse=True)
    detached = [part for part in parts[1:] if part["area"] >= minimum_area]
    return check("FAIL" if detached else "PASS", {"detached": detached, "minimum_area": minimum_area,
                                                   "scope": "Disconnected alpha islands are diagnostic; no pixels are deleted"})


def source_id(job: dict, token: str) -> str:
    if not isinstance(token, str):
        raise ValueError("Source bindings must be strings")
    if not token.startswith("@"):
        return token
    aliases = {**job["character"].get("source_aliases", {}), **job["outfit"].get("source_aliases", {}), **job.get("source_aliases", {})}
    value = aliases.get(token[1:])
    if not isinstance(value, str) or not value or value.startswith("@"):
        raise ValueError(f"Unbound or recursive source alias: {token}")
    return value


def load_job(root: Path, catalog_path: Path, job_id: str) -> dict:
    catalog = read_json(catalog_path)
    if catalog.get("schema") != SCHEMA:
        raise ValueError("Unsupported pipeline schema")
    job = dict(catalog["jobs"][job_id])
    job.update(id=job_id, catalog=catalog, catalog_sha256=sha(catalog_path))
    job["character"] = catalog["characters"][job["character_id"]]
    job["outfit"] = catalog["outfits"][job["outfit_id"]]
    job["action"] = catalog["actions"][job["action_id"]]
    if job["outfit"]["character_id"] != job["character_id"]:
        raise ValueError("Outfit belongs to another character")
    action = job["action"]
    if type(action["count"]) is not int or type(action["fps"]) is not int or not 1 <= action["count"] <= 10000 or not 1 <= action["fps"] <= 120:
        raise ValueError("Invalid frame count/rate")
    if "delivery_cell" in action and (len(action["delivery_cell"]) != 2 or any(type(v) is not int or v < 1 for v in action["delivery_cell"])):
        raise ValueError("Invalid delivery cell")
    frames = read_json(inside(root, job["frames_manifest"]))
    if not isinstance(frames, list) or len(frames) != action["count"] or [r["index"] for r in frames] != list(range(action["count"])):
        raise ValueError("Frame inventory must cover every index exactly once, in order")
    job["frames"] = frames
    job["frame_paths"] = [pinned(root, row) for row in frames]
    job["sources"] = {key: catalog["sources"][key] for key in {source_id(job, token) for token in job["character"]["sources"] + job["outfit"]["sources"] + action["sources"]}}
    for source in job["sources"].values():
        pinned(root, source)
        if not source.get("license") or not source.get("acceptance_scope"):
            raise ValueError("Every source needs license and acceptance scope")
    for phase in action["phases"]:
        if not 0 <= phase["from"] <= phase["to"] < action["count"]:
            raise ValueError("Phase lies outside timeline")
    if not math.isfinite(job["mapping"]["scale"]) or job["mapping"]["scale"] <= 0:
        raise ValueError("Invalid geometry scale")
    profile = job["character"]["geometry"]
    if len(profile["landmarks"]) < 3 or any(len(p) != 2 or not all(math.isfinite(v) for v in p) for p in profile["landmarks"].values()):
        raise ValueError("At least three finite geometry landmarks are required")
    for segment in profile["segments"].values():
        if not math.isfinite(segment["length_px"]) or segment["length_px"] <= 0 or not math.isfinite(segment["tolerance_pct"]) or segment["tolerance_pct"] < 0:
            raise ValueError("Segment lengths/tolerances must be finite and valid")
    job["ledger_path"] = inside(root, job["attempt_ledger"])
    job["ledger"] = read_json(job["ledger_path"])
    if job["ledger"]["campaign_id"] != job["campaign_id"]:
        raise ValueError("Attempt ledger belongs to another campaign")
    limits = job["ledger"]["limits"]
    if not 0 <= limits["imagegen_calls_max"] <= 2:
        raise ValueError("This V1 supports at most two corrective key calls per campaign")
    if len(job["ledger"]["attempts"]) > limits["imagegen_calls_max"]:
        raise ValueError("Campaign already exceeded its call cap")
    if min(limits["wall_minutes_max"], limits["cleanup_minutes_max"]) < 0:
        raise ValueError("Time caps must be nonnegative")
    return job


def check(status: str, evidence: object) -> dict:
    return {"status": status, "evidence": evidence}


def group_spans(defects: list[dict], count: int, context: int) -> list[dict]:
    indices = sorted({d["index"] for d in defects})
    groups: list[list[int]] = []
    for index in indices:
        if groups and index == groups[-1][-1] + 1:
            groups[-1].append(index)
        else:
            groups.append([index])
    return [{"from": g[0], "to": g[-1], "context_from": max(0, g[0] - context),
             "context_to": min(count - 1, g[-1] + context),
             "categories": sorted({d["category"] for d in defects if d["index"] in g}),
             "replacement_unit": "complete_figure_frame"} for g in groups]


def geometry(root: Path, job: dict) -> tuple[dict, list[dict]]:
    """Use the handoff's actual measurement implementation, with profile data.

    Historical checker is left unchanged. Its permissive missing-data behavior
    is tightened here: every required track/joint must exist and be finite.
    """
    profile = job["character"]["geometry"]
    spec = importlib.util.spec_from_file_location("wave_measurement", root / MEASURER)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ModuleNotFoundError as error:
        return {"geometry": check("PENDING", f"Dependency unavailable: {error.name}")}, []
    module.FEATURES = {key: tuple(value) for key, value in profile["landmarks"].items()}
    module.FACE_BOX = tuple(profile["head_box"])
    paths = job["frame_paths"]

    class Paths:
        def __mod__(self, index):
            return paths[index]

    scale, offset = job["mapping"]["scale"], job["mapping"]["offset"]
    _, tracks = module.track(Paths(), len(paths), scale, offset)
    figure = []
    for found in tracks:
        keys = [key for key in found if key in tracks[0]]
        figure.append(module.fit_scale([tracks[0][key] for key in keys], [found[key] for key in keys]))
    head = module.ecc_scale(Paths(), len(paths), scale, offset)
    checks, defects = {}, []
    missing = [i for i, row in enumerate(tracks) if set(row) != set(profile["landmarks"])]
    checks["landmark_coverage"] = check("PENDING" if missing else "PASS", {"missing_indices": missing})
    for name, series, limit in (("figure_scale", figure, job["action"]["limits"]["figure_scale_pp_pct"]),
                                ("head_scale", head, job["action"]["limits"]["head_scale_pp_pct"])):
        finite = all(math.isfinite(value) for value in series)
        value = 100 * (max(series) - min(series)) if finite else None
        status = "PENDING" if not finite or (name == "figure_scale" and missing) else ("PASS" if value <= limit else "FAIL")
        checks[name] = check(status, {"peak_to_peak_pct": value, "limit_pct": limit,
                                     "per_frame_pct": [100 * (v - 1) if math.isfinite(v) else None for v in series]})
        if status == "FAIL":
            # Range failure has two extrema, rather than an arbitrary blame threshold.
            for index in {series.index(min(series)), series.index(max(series))}:
                defects.append({"index": index, "category": name, "source": "measurement"})
    if job.get("master"):
        master = pinned(root, job["master"])
        count = module.aseprite_layers(master)
        checks["single_layer"] = check("PASS" if count == 1 else "FAIL", {"layers": count})
    else:
        checks["single_layer"] = check("PENDING", "No pinned editable master")
    return checks, defects


def inspect(root: Path, job: dict) -> dict:
    checks, defects = geometry(root, job)
    dimensions, matte_failures, border_failures = [], [], []
    island_rows = []
    for i, path in enumerate(job["frame_paths"]):
        with Image.open(path) as image:
            dimensions.append(list(image.size))
            alpha = image.convert("RGBA").getchannel("A")
            if alpha.getextrema()[0] == 255:
                matte_failures.append(i)
            box = alpha.getbbox()
            margin = job["action"]["limits"]["border_px"]
            if box is None or min(box[0], box[1], image.width - box[2], image.height - box[3]) < margin:
                border_failures.append(i)
        island_rows.append({"index": i, **alpha_islands(path, max(1, round(job["action"]["limits"].get("detached_component_min_cell_px", 4) * job["mapping"]["scale"] ** 2)))})
    checks["canvas"] = check("PASS" if all(d == job["native_canvas"] for d in dimensions) else "FAIL", dimensions)
    checks["sprite_alpha"] = check("FAIL" if matte_failures else "PASS", {"opaque_indices": matte_failures, "scope": "export/matte defect; not a request to redraw every frame"})
    checks["border"] = check("FAIL" if border_failures else "PASS", {"failed_indices": border_failures})
    checks["alpha_islands"] = check("FAIL" if any(row["status"] == "FAIL" for row in island_rows) else ("PENDING" if any(row["status"] == "PENDING" for row in island_rows) else "PASS"), island_rows)
    for index in border_failures:
        defects.append({"index": index, "category": "border_or_matte", "source": "measurement"})
    endpoints = []
    for boundary in job["action"]["boundaries"]:
        resolved = source_id(job, boundary["source_id"])
        source = job["sources"][resolved]
        path = pinned(root, source)
        cell = source.get("cell")
        with Image.open(path) as image:
            size = cell[2:] if cell else list(image.size)
        index = boundary["index"]
        same = dimensions[index] == size and image_pixels(job["frame_paths"][index]) == image_pixels(path, cell)
        endpoints.append({"index": index, "source_id": resolved, "source_binding": boundary["source_id"], "decoded_rgba_byte_exact": same})
        if not same:
            defects.append({"index": index, "category": "endpoint", "source": "measurement"})
    checks["endpoints"] = check("PASS" if endpoints and all(row["decoded_rgba_byte_exact"] for row in endpoints) else "FAIL", endpoints)
    if not job.get("derivation"):
        checks["whole_frame_provenance"] = check("PENDING", "A one-layer file does not prove how its pixels were made; exact per-frame derivation is required")
    else:
        provenance = read_json(pinned(root, job["derivation"]))
        entries = provenance["frames"]
        if [entry["index"] for entry in entries] != list(range(len(job["frames"]))):
            raise ValueError("Derivation must cover every frame once")
        failed = []
        for entry, frame in zip(entries, job["frames"]):
            if entry["sha256"] != frame["sha256"]:
                raise ValueError("Derivation frame hash is stale")
            if entry["method"] not in {"whole_frame_generated", "whole_frame_drawn", "approved_whole_frame_reuse"} or entry["pixel_assembly"] != "NONE":
                failed.append(entry["index"])
            if not entry.get("parents") or not entry.get("edits"):
                raise ValueError("Derivation needs pinned parents and an edit declaration")
            for parent in entry["parents"]:
                pinned(root, parent)
        checks["whole_frame_provenance"] = check("FAIL" if failed else "PASS", {"failed_indices": failed, "scope": "Pinned declaration/ancestry check; method and pixels still require human review"})
    segments = job["character"]["geometry"]["segments"]
    joint_data = read_json(inside(root, job["joints"])) if job.get("joints") else {"frames": []}
    joints = {row["index"]: row for row in joint_data["frames"]}
    if len(joints) != len(joint_data["frames"]) or any(i not in range(len(job["frames"])) for i in joints):
        raise ValueError("Duplicate or out-of-range joint annotations")
    missing, lengths = [], []
    for frame in job["frames"]:
        index = frame["index"]
        row = joints.get(index)
        if not row or row.get("sha256") != frame["sha256"]:
            missing.append(index)
            continue
        for name, segment in segments.items():
            flag = segment.get("required_when")
            if flag and flag not in row.get("flags", {}):
                missing.append(index)
                continue
            if flag and type(row["flags"][flag]) is not bool:
                raise ValueError("Joint condition flags must be explicit booleans")
            if flag and row["flags"][flag] is False:
                continue
            a, b = (row["points"].get(p) for p in segment["points"])
            if a is None or b is None or not all(math.isfinite(v) for v in a + b):
                missing.append(index)
                continue
            if len(a) != 2 or len(b) != 2:
                raise ValueError("Joint coordinates must be 2D canvas points")
            deviation = 100 * (math.dist(a, b) / (segment["length_px"] * job["mapping"]["scale"]) - 1)
            lengths.append({"index": index, "segment": name, "deviation_pct": deviation})
            if abs(deviation) > segment["tolerance_pct"]:
                defects.append({"index": index, "category": "proportions", "source": "joint_annotation"})
    joint_fails = any(d["category"] == "proportions" for d in defects)
    checks["proportions"] = check("FAIL" if joint_fails else ("PENDING" if missing else "PASS"), {"missing_indices": sorted(set(missing)), "lengths": lengths})
    reviews = read_json(inside(root, job["review"])) if job.get("review") else {"frames": []}
    reviewed = {}
    for row in reviews["frames"]:
        index = row["index"]
        if index in reviewed or index not in range(len(job["frames"])):
            raise ValueError("Duplicate or out-of-range review index")
        if row["sha256"] != job["frames"][index]["sha256"]:
            raise ValueError(f"Review is stale at frame {index}")
        if not row.get("reviewer") or not row.get("date"):
            raise ValueError("Human observations need reviewer and date")
        reviewed[index] = row
        for category, state in row["checks"].items():
            if state not in {"PASS", "FAIL", "PENDING"}:
                raise ValueError("Unknown review state")
            if state == "FAIL":
                defects.append({"index": index, "category": category, "source": "human_observation", "note": row.get("note", "")})
    human_pass = all(index in reviewed and reviewed[index].get("reviewer_kind") == "human" and all(reviewed[index]["checks"].get(axis) == "PASS" for axis in REVIEW_AXES) for index in range(len(job["frames"])))
    full_speed = reviews.get("full_speed", {})
    bound_hashes = [row["sha256"] for row in job["frames"]]
    speed_pass = full_speed.get("status") == "PASS" and full_speed.get("reviewer_kind") == "human" and full_speed.get("frame_hashes") == bound_hashes and bool(full_speed.get("reviewer")) and bool(full_speed.get("date"))
    human_fail = any(d["source"] == "human_observation" for d in defects)
    checks["human_frame_review"] = check("FAIL" if human_fail else ("PASS" if human_pass else "PENDING"), "Exact-hash identity/outfit/topology/motion review by a declared human on every frame required; model observations may block but cannot accept")
    checks["full_speed_review"] = check("FAIL" if full_speed.get("status") == "FAIL" else ("PASS" if speed_pass else "PENDING"), "Declared human review of exact sequence and repaired boundaries at normal speed; static/model observations do not fill this lane")
    blocked = [key for key, entry in checks.items() if entry["status"] != "PASS"]
    return {"schema": SCHEMA, "job_id": job["id"], "catalog_sha256": job["catalog_sha256"],
            "frame_hashes": bound_hashes, "checks": checks, "defects": defects,
            "repair_spans": group_spans([d for d in defects if d["category"] != "border_or_matte"], len(job["frames"]), job["action"]["context_frames"]),
            "durations_ms": frame_clock(len(job["frames"]), job["action"]["fps"]),
            "candidate_ready": not blocked, "blockers": blocked,
            "claims": {"ARCHIVE_COMPLETE": "PENDING_REMOTE_VERIFICATION", "GENERATION_READY": "PENDING_KEY_REVIEW", "DELIVERY_ACCEPTED": False,
                       "runtime": "NOT_INTEGRATED", "device_child_owner": "PENDING"}}


def repair_requests(root: Path, job: dict, report: dict) -> dict:
    if report["job_id"] != job["id"] or report["catalog_sha256"] != job["catalog_sha256"] or report["frame_hashes"] != [row["sha256"] for row in job["frames"]]:
        raise ValueError("Report belongs to a different revision/job")
    ledger = job["ledger"]
    remaining = max(0, ledger["limits"]["imagegen_calls_max"] - len(ledger["attempts"]))
    requests, scheduled = [], 0
    locks = job["character"]["identity_locks"] + job["outfit"]["locks"] + job["action"]["motion_locks"]
    for gap in job["action"]["key_gaps"]:
        bindings = []
        for token in gap["source_ids"]:
            resolved = source_id(job, token)
            source = job["sources"][resolved]
            if source["role"] not in PIXEL_ROLES or source["acceptance_scope"] != "APPROVED_SOURCE" or not source.get("pixel_input_allowed", False):
                raise ValueError(f"Source cannot be bound as generation pixels: {resolved}")
            bindings.append({"source_id": resolved, **source})
        if not 1 <= len(bindings) <= 4:
            raise ValueError("Bind one to four purpose-specific source images")
        index = gap["index"]
        if not 0 <= index < job["action"]["count"]:
            raise ValueError("Key gap lies outside action")
        prior = [row for row in ledger["attempts"] if row["key_id"] == gap["id"]]
        if prior and prior[-1]["disposition"] in {"CANDIDATE", "RESERVED"}:
            state = "PENDING_CANDIDATE_REVIEW"
        elif prior and prior[-1]["disposition"] in {"REJECTED", "FAILED"}:
            state = "DIAGNOSE_REJECTED_KEY"
        elif scheduled >= remaining:
            state = "TASK_CAP_BLOCKED"
        else:
            state = "READY_TO_REQUEST_KEY"
            scheduled += 1
        phase = next((p["description"] for p in job["action"]["phases"] if p["from"] <= index <= p["to"]), "transition")
        prompt = ("Use case: identity-preserve\nAsset type: complete RGBA storybook sprite key\n"
                  f"Primary request: {gap['description']}\nAction: {job['action']['verb']}; phase: {phase}; intended frame {index}.\n"
                  f"Outfit: {job['outfit']['description']}\n"
                  "Input roles: " + "; ".join(f"Image {n+1}: {b['role']}, {b.get('binding_note', b['source_id'])}" for n, b in enumerate(bindings)) + "\n"
                  "Constraints: one complete newly painted figure; one flattened drawing; coordinated body response. "
                  + "; ".join(locks) + "\n"
                  f"Requested canvas: {job['action']['key_canvas'][0]}x{job['action']['key_canvas'][1]}; preserve the normalized full-canvas framing of Image1.\n"
                  "Transparent background, full figure with motion margin, no copied/pasted limbs, no duplicate figure, no text, no sparkle dots, no detached specks or colored matte noise.\n")
        requests.append({"id": gap["id"], "index": index, "state": state,
                         "campaign_id": job["campaign_id"], "bindings": bindings, "prompt": prompt,
                         "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                         "replacement_unit": "complete_figure_frame", "review_context": report["repair_spans"],
                         "expected_canvas": job["action"]["key_canvas"]})
    return {"schema": SCHEMA, "job_id": job["id"], "catalog_sha256": job["catalog_sha256"],
            "calls_used": len(ledger["attempts"]), "calls_remaining": remaining,
            "limits": ledger["limits"], "prior_campaigns": ledger.get("prior_campaigns", []),
            "requests": requests, "dispatch": "Codex built-in imagegen; never automatically executed by this CLI",
            "next_animation": job["action"]["backend"], "generation_ready": False}


def validate_plan(job: dict, plan: dict, key_id: str) -> dict:
    if plan["catalog_sha256"] != job["catalog_sha256"] or plan["job_id"] != job["id"]:
        raise ValueError("Plan is stale or belongs to another job")
    request = next(row for row in plan["requests"] if row["id"] == key_id)
    if request["state"] != "READY_TO_REQUEST_KEY":
        raise ValueError("Request is blocked")
    return request


def reserve_key(job: dict, plan: dict, key_id: str) -> dict:
    request = validate_plan(job, plan, key_id)
    with ledger_lock(job["ledger_path"]):
        ledger = read_json(job["ledger_path"])
        if len(ledger["attempts"]) >= ledger["limits"]["imagegen_calls_max"]:
            raise ValueError("Aggregate campaign call cap reached")
        if any(row.get("time_cap_exceeded") for row in ledger["attempts"]):
            raise ValueError("A prior call exceeded the task time cap; diagnose before changing the brief")
        if any(row["key_id"] == key_id and row["disposition"] in {"RESERVED", "CANDIDATE"} for row in ledger["attempts"]):
            raise ValueError("Existing key request must be reviewed before another call")
        if sum(row.get("cleanup_minutes", 0) for row in ledger["attempts"]) >= ledger["limits"]["cleanup_minutes_max"]:
            raise ValueError("Aggregate cleanup cap reached")
        attempt = {"attempt_id": f"{job['campaign_id']}-{len(ledger['attempts'])+1}",
                   "key_id": key_id, "job_id": job["id"], "index": request["index"],
                   "campaign_id": job["campaign_id"], "disposition": "RESERVED", "cleanup_minutes": 0,
                   "prompt_sha256": request["prompt_sha256"], "binding_hashes": [b["sha256"] for b in request["bindings"]]}
        ledger["attempts"].append(attempt)
        write_json(job["ledger_path"], ledger)
    return attempt


def record_key(root: Path, job: dict, plan: dict, key_id: str, image_path: Path | None, receipt: dict, output: Path) -> dict:
    request = validate_plan(job, plan, key_id)
    for field in ("provider", "request_id", "provider_revision", "elapsed_seconds", "cleanup_minutes", "usage", "disposition"):
        if field not in receipt:
            raise ValueError(f"Missing generation receipt field: {field}")
    if receipt.get("prompt_sha256") != request["prompt_sha256"] or receipt.get("binding_hashes") != [b["sha256"] for b in request["bindings"]]:
        raise ValueError("Receipt prompt/bindings differ from the planned job")
    if receipt["disposition"] not in {"CANDIDATE", "REJECTED", "FAILED"}:
        raise ValueError("Generated output may only enter as candidate, rejected or failed")
    if not all(isinstance(receipt[k], (int, float)) and math.isfinite(receipt[k]) and receipt[k] >= 0 for k in ("elapsed_seconds", "cleanup_minutes")):
        raise ValueError("Invalid measured times")
    if image_path is None and receipt["disposition"] != "FAILED":
        raise ValueError("Candidate/rejected calls require native output")
    output = inside(root, str(output), output=True)
    if output.exists():
        raise ValueError("Never overwrite an existing native candidate")
    with ledger_lock(job["ledger_path"]):
        ledger = read_json(job["ledger_path"])
        slot = next((i for i, row in enumerate(ledger["attempts"]) if row["key_id"] == key_id and row["disposition"] == "RESERVED"), None)
        if slot is None:
            raise ValueError("Reserve the key call before dispatch; no call can disappear from its budget")
        reserved = ledger["attempts"][slot]
        if reserved["prompt_sha256"] != request["prompt_sha256"] or reserved["binding_hashes"] != receipt["binding_hashes"]:
            raise ValueError("Reservation differs from this request")
        attempt = {**reserved, **receipt, "expected_canvas": request["expected_canvas"],
                   "geometry_review": "PENDING", "owner_acceptance": "PENDING"}
        output.mkdir(parents=True)
        if image_path:
            with Image.open(image_path) as image:
                attempt["dimensions"] = list(image.size)
                attempt["alpha_extrema"] = list(image.convert("RGBA").getchannel("A").getextrema())
            native = output / "native.png"
            shutil.copyfile(image_path, native)
            attempt.update(native_path=native.relative_to(root).as_posix(), native_sha256=sha(native))
            attempt["canvas_check"] = check("PASS" if attempt["dimensions"] == request["expected_canvas"] else "FAIL", attempt["dimensions"])
            attempt["alpha_islands"] = alpha_islands(native, max(1, round(job["action"]["limits"].get("detached_component_min_cell_px", 4) * (max(attempt["dimensions"]) / 256) ** 2)))
        total_cleanup = sum(a.get("cleanup_minutes", 0) for i, a in enumerate(ledger["attempts"]) if i != slot) + receipt["cleanup_minutes"]
        attempt["time_cap_exceeded"] = receipt["elapsed_seconds"] > ledger["limits"]["wall_minutes_max"] * 60 or total_cleanup > ledger["limits"]["cleanup_minutes_max"]
        write_json(output / "receipt.json", attempt)
        (output / "prompt.txt").write_bytes(request["prompt"].encode("utf-8"))
        ledger["attempts"][slot] = attempt
        write_json(job["ledger_path"], ledger)
    return attempt


def export_master(root: Path, job: dict, output: Path, aseprite: str) -> dict:
    output = inside(root, str(output), output=True)
    if output.exists():
        raise ValueError("Use a fresh export directory; originals are never overwritten")
    output.mkdir(parents=True)
    versions = subprocess.run([aseprite, "--version"], capture_output=True, text=True, check=True, timeout=30)
    bridge = {"canvas": job["native_canvas"], "frames": [str(p) for p in job["frame_paths"]],
              "durations_ms": frame_clock(len(job["frames"]), job["action"]["fps"]),
              "phases": job["action"]["phases"], "output": str(output)}
    write_json(output / "bridge_input.json", bridge)
    process = subprocess.run([aseprite, "--batch", "--script-param", "input=" + str(output / "bridge_input.json"),
                              "--script", str(root / "tools/sprite_pipeline_bridge.lua")], capture_output=True, text=True, timeout=120)
    (output / "aseprite.log").write_text(process.stdout + process.stderr, encoding="utf-8")
    if process.returncode:
        raise ValueError("Aseprite export failed; inspect saved log")
    for i, path in enumerate(job["frame_paths"]):
        target = output / "frames" / f"{i:04d}.png"
        with Image.open(target) as image:
            if list(image.size) != job["native_canvas"]:
                raise ValueError("Export changed the native canvas")
        if image_pixels(path) != image_pixels(target):
            raise ValueError(f"Export changed pixels at frame {i}")
    proof = read_json(output / "master_proof.json")
    if proof["layers"] != 1 or proof["count"] != len(job["frames"]) or proof["durations_ms"] != bridge["durations_ms"]:
        raise ValueError("Reopened master changes layers/count/timing")
    result = {"status": "SOURCE_EXPORT_PASS", "job_id": job["id"], "aseprite_version": versions.stdout.strip(),
              "master_sha256": sha(output / "whole_sprite.aseprite"), "rgba_byte_exact_frames": len(job["frames"]),
              "total_ms": sum(bridge["durations_ms"]), "layers": 1,
              "pixel_transform": "none; one complete native frame per cel", "runtime_ready": False,
              "acceptance": "Source/export equality only; anatomy, alpha, motion, device and owner remain independent"}
    write_json(output / "export_report.json", result)
    return result


def normalize_key(root: Path, job: dict, image_path: Path, output: Path, aseprite: str) -> dict:
    """Declared uniform whole-canvas export, never internal proportion repair."""
    image_path = inside(root, str(image_path))
    output = inside(root, str(output), output=True)
    if output.exists():
        raise ValueError("Use a fresh normalization directory")
    with Image.open(image_path) as image:
        native = list(image.size)
    target = job["action"]["delivery_cell"]
    if native[0] * target[1] != native[1] * target[0]:
        raise ValueError("Normalization may not stretch axes independently; canvas aspect must match")
    output.mkdir(parents=True)
    bridge = {"canvas": native, "delivery_canvas": target, "frames": [str(image_path)],
              "durations_ms": [frame_clock(1, job["action"]["fps"])[0]], "phases": [], "output": str(output)}
    write_json(output / "bridge_input.json", bridge)
    process = subprocess.run([aseprite, "--batch", "--script-param", "input=" + str(output / "bridge_input.json"),
                              "--script", str(root / "tools/sprite_pipeline_bridge.lua")], capture_output=True, text=True, timeout=120)
    (output / "aseprite.log").write_text(process.stdout + process.stderr, encoding="utf-8")
    if process.returncode:
        raise ValueError("Aseprite normalization failed; inspect saved log")
    normalized = output / "frames/0000.png"
    with Image.open(normalized) as image:
        if list(image.size) != target:
            raise ValueError("Normalization changed the delivery canvas")
    proof = read_json(output / "master_proof.json")
    if proof["layers"] != 1 or proof["count"] != 1:
        raise ValueError("Normalized master is not a single complete frame/layer")
    result = {"status": "NORMALIZED_CANDIDATE", "source_path": image_path.relative_to(root).as_posix(), "source_sha256": sha(image_path),
              "source_canvas": native, "delivery_canvas": target, "uniform_scale": target[0] / native[0],
              "transform": "Aseprite bilinear uniform whole-canvas resize only; no crop, reposition or per-part edit",
              "normalized_path": normalized.relative_to(root).as_posix(), "normalized_sha256": sha(normalized),
              "master_sha256": sha(output / "whole_sprite.aseprite"), "alpha_islands": alpha_islands(normalized, 4),
              "geometry": "PENDING_REMEASUREMENT", "runtime_ready": False}
    write_json(output / "normalization.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "plan", "reserve-key", "record-key", "normalize-key", "export"))
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--job", required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--key")
    parser.add_argument("--image", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--aseprite", default=r"C:\Program Files\Aseprite\Aseprite.exe")
    args = parser.parse_args()
    try:
        job = load_job(args.root, args.catalog, args.job)
        output = inside(args.root, args.out, output=True)
        if args.command == "inspect":
            result = inspect(args.root, job)
            write_json(output, result)
            print("CANDIDATE_READY" if result["candidate_ready"] else "REVIEW_BLOCKED", ", ".join(result["blockers"]))
            return 0 if result["candidate_ready"] else 1
        if args.command == "plan":
            if args.report is None:
                raise ValueError("plan requires --report")
            result = repair_requests(args.root, job, read_json(args.report))
            write_json(output, result)
            print("REPAIR_PLAN", len(result["requests"]), "named keys; remaining calls", result["calls_remaining"])
        elif args.command == "reserve-key":
            if args.plan is None or args.key is None:
                raise ValueError("reserve-key requires --plan --key")
            result = reserve_key(job, read_json(args.plan), args.key)
            write_json(output, result)
            print("KEY_CALL_RESERVED", result["attempt_id"])
        elif args.command == "record-key":
            if None in (args.plan, args.key, args.receipt):
                raise ValueError("record-key requires --plan --key --receipt; --image for native output")
            result = record_key(args.root, job, read_json(args.plan), args.key, args.image, read_json(args.receipt), output)
            print("KEY_CALL_RECORDED", result["disposition"])
        elif args.command == "normalize-key":
            if args.image is None:
                raise ValueError("normalize-key requires --image")
            result = normalize_key(args.root, job, args.image, output, args.aseprite)
            print(result["status"], result["uniform_scale"])
        else:
            result = export_master(args.root, job, output, args.aseprite)
            print(result["status"], result["rgba_byte_exact_frames"], "whole frames")
        return 0
    except (ValueError, KeyError, TypeError, IndexError, StopIteration, OSError, subprocess.SubprocessError) as error:
        print("SPRITE_PIPELINE_ERROR:", error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
