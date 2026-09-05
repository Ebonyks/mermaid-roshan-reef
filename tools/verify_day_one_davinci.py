"""Verify the delivered editorial packet without calling or changing Resolve."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from assemble_day_one_davinci import ROOT, PACKET, digest, probe, read, require, write


def source_text_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").encode("utf-8")).hexdigest()


def video(path: Path, frames: int, codec: str) -> dict:
    streams = probe(path)["streams"]
    videos = [s for s in streams if s["codec_type"] == "video"]
    require(len(videos) == 1 and all(s["codec_type"] == "video" or (s["codec_type"] == "data" and s.get("codec_tag_string") == "tmcd") for s in streams), f"Unapproved audio/streams: {path}")
    stream = videos[0]
    require(stream["codec_name"] == codec, f"Codec mismatch: {path}")
    require([stream["width"], stream["height"]] == [1280, 720], f"Canvas mismatch: {path}")
    require(stream["r_frame_rate"] == "24/1", f"Frame rate mismatch: {path}")
    counted = subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path),
    ], text=True).strip()
    require(int(counted) == frames, f"Decoded frame count mismatch: {path}: {counted} != {frames}")
    return {"path": path.relative_to(PACKET).as_posix(), "sha256": digest(path), "decoded_frames": int(counted), "codec": codec}


def verify() -> dict:
    assembly = read(PACKET / "ASSEMBLY_MANIFEST.json")
    exports = read(PACKET / "EXPORT_MANIFEST.json")
    runtime = read(PACKET / "runtime_manifest.json")
    readback = read(PACKET / "RESOLVE_READBACK.json")
    require(assembly["plan_sha256"] == digest(ROOT / "design/day_one_davinci_draft_edit.json"), "Edit plan changed after assembly")
    require(assembly["claims"]["delivery_accepted"] is False, "Editorial packet cannot accept delivery")
    integration = read(PACKET / "INTEGRATION_VALIDATION.json")
    for filename, sha in integration["tested_source_sha256"].items():
        require(source_text_sha256(ROOT / filename) == sha, f"Runtime source changed after behavioral evidence: {filename}")
    for run in integration["runs"]:
        log = ROOT / run["log"]
        require(run["exit_code"] == 0 and digest(log) == run["sha256"], f"Probe/log mismatch: {run['name']}")
        require(run["final_pass_line"] in log.read_text(encoding="utf-8"), f"Missing probe PASS: {run['name']}")
    for source in assembly["sources"].values():
        path = PACKET / source["file"]
        require(digest(path) == source["sha256"], f"Source hash mismatch: {path}")
    outputs = {row["id"]: row for row in exports["outputs"]}
    timelines = {row["id"]: row for row in readback["timelines"]}
    results = []
    for movie in assembly["movies"]:
        mid = movie["id"]
        eligible = bool(movie["runtime_preview_eligible"] and movie["shots"])
        row = runtime["movies"][mid]
        require(row["runtime_preview_eligible"] == eligible, f"Runtime eligibility mismatch: {mid}")
        if mid in ["D1-C07", "D1-C08", "D1-C13"]:
            require(not eligible, f"Incomplete event accidentally enabled: {mid}")
        if not movie["shots"]:
            require(mid not in outputs and mid not in timelines, f"Invented missing event: {mid}")
            continue
        output = outputs[mid]
        timeline = timelines[mid]
        require(len(timeline["items"]) == len(movie["shots"]), f"Shot count mismatch: {mid}")
        cursor = 0
        for shot, actual in zip(movie["shots"], timeline["items"]):
            require(shot["record_start"] == cursor, f"Gap/overlap: {mid}")
            cursor = shot["record_end_exclusive"]
            require(actual["source"] == shot["source"], f"Source mismatch: {mid}")
            require(actual["source_start"] == shot["source_start"], f"Wrong source frame: {mid}")
            require(actual["duration"] == shot["source_end_exclusive"] - shot["source_start"], f"Wrong range: {mid}")
        require(cursor == movie["frames"] == timeline["frames"] == output["frames"] == row["frames"], f"Frame accounting mismatch: {mid}")
        for ext, codec in [("mp4", "h264"), ("ogv", "theora")]:
            path = PACKET / output[ext]
            require(digest(path) == output[ext + "_sha256"], f"Export hash mismatch: {mid}/{ext}")
            results.append(video(path, movie["frames"], codec))
        require(row["path"] == output["ogv"] and row["sha256"] == output["ogv_sha256"], f"Wrong runtime file: {mid}")
        require(row["delivery_accepted"] is False, f"False delivery claim: {mid}")
    drp = PACKET / readback["project_export"]
    require(digest(drp) == readback["project_export_sha256"], "Project archive hash mismatch")
    return {"schema": "day-one-draft-validation-v1", "result": "PASS", "source_count": len(assembly["sources"]), "timelines": len(timelines), "runtime_eligible": sum(bool(m["runtime_preview_eligible"]) for m in assembly["movies"]), "total_frames": sum(m["frames"] for m in assembly["movies"]), "outputs": results, "scope": "source hashes, saved Resolve readback, all decoded MP4/OGV frame counts, codec, no audio, eligibility; not full-speed visual/human/device acceptance", "delivery_accepted": False}


def payload_manifest() -> dict:
    rows = []
    # Sort canonical POSIX strings, not platform-specific Path ordering.
    # WindowsPath compares case-insensitively; Linux Path does not.
    for path in sorted(PACKET.rglob("*"), key=lambda item: item.relative_to(PACKET).as_posix()):
        if not path.is_file() or path.name == "PAYLOAD_MANIFEST.json" or path.suffix in [".import", ".uid"]:
            continue
        relative = path.relative_to(PACKET).as_posix()
        row = {"path": relative, "sha256": digest(path), "bytes": path.stat().st_size, "role": relative.split("/")[0] if "/" in relative else "archive_sidecar", "delivery_accepted": False}
        if path.suffix in [".png", ".jpg"]:
            from PIL import Image
            with Image.open(path) as picture:
                row["dimensions"] = list(picture.size)
            row["used_as_delivery_pixels"] = False
            row["used_as_generation_pixels"] = False
        rows.append(row)
    payload = "".join(f'{r["path"]}\t{r["sha256"]}\t{r["bytes"]}\n' for r in rows).encode("utf-8")
    return {"schema": "day-one-editorial-payload-v1", "files": rows, "payload_sha256": hashlib.sha256(payload).hexdigest(), "algorithm": "SHA256 of UTF-8 lines sorted by relative path: path TAB sha256 TAB decimal bytes LF; excludes this manifest and generated Godot import/UID sidecars", "provenance": "ASSET_LICENSES.md plus ASSEMBLY_MANIFEST.json for footage; review/README.md for diagnostic boards; V01 history preserved", "claims": {"editorial_reference_only": True, "delivery_accepted": False}}


def verify_staged(payload: dict) -> None:
    paths = [PACKET / row["path"] for row in payload["files"]]
    paths += [PACKET / "PAYLOAD_MANIFEST.json", ROOT / "design/day_one_davinci_draft_edit.json"]
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        staged = subprocess.check_output(["git", "rev-parse", ":" + relative], cwd=ROOT, text=True).strip()
        literal = subprocess.check_output(["git", "hash-object", "--no-filters", str(path)], cwd=ROOT, text=True).strip()
        require(staged == literal, f"Staged packet bytes are stale/normalized: {relative}")
    for filename, sha in read(PACKET / "INTEGRATION_VALIDATION.json")["tested_source_sha256"].items():
        code = subprocess.check_output(["git", "show", ":" + filename], cwd=ROOT).decode("utf-8-sig").replace("\r\n", "\n")
        require(hashlib.sha256(code.encode("utf-8")).hexdigest() == sha, f"Staged runtime differs from tested source: {filename}")
    for filename in ["tools/verify_day_one_davinci.py", "tools/assemble_day_one_davinci.py"]:
        code = subprocess.check_output(["git", "show", ":" + filename], cwd=ROOT).decode("utf-8-sig").replace("\r\n", "\n")
        require(hashlib.sha256(code.encode("utf-8")).hexdigest() == source_text_sha256(ROOT / filename), f"Staged verification tool differs from working copy: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--staged", action="store_true", help="Also require exact staged packet/recipe bytes and tested runtime source")
    args = parser.parse_args()
    report = verify()
    if args.write_evidence:
        write(PACKET / "VALIDATION.json", report)
        write(PACKET / "PAYLOAD_MANIFEST.json", payload_manifest())
    else:
        require(read(PACKET / "VALIDATION.json") == report, "Stored VALIDATION.json is stale; regenerate deliberately")
        require(read(PACKET / "PAYLOAD_MANIFEST.json") == payload_manifest(), "Stored PAYLOAD_MANIFEST.json is stale; regenerate deliberately")
    if args.staged:
        verify_staged(read(PACKET / "PAYLOAD_MANIFEST.json"))
    print(json.dumps({k: v for k, v in report.items() if k != "outputs"}, indent=2))
