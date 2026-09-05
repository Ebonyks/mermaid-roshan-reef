"""Build audited Day One editorial drafts in the local DaVinci project.

Source frames are trimmed and joined at straight cuts, at their native rate.
Grok source audio is intentionally excluded; these are editorial references.
No delivery acceptance or full-frame generation provenance is manufactured.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "assets_src/cinematics/day_one_davinci_draft_2026-09-04"
V3 = ROOT / "assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04"
PROJECT = "Mermaid Roshan - Day One Game Cohesion Draft 2026-09-04"
BRIDGE = Path(os.environ.get("DAY_ONE_RESOLVE_BRIDGE", r"C:\Users\Peter\AppData\Local\Temp\davinci-resolve-mcp-v2.103.1"))


def require(value, message):
    if not value:
        raise RuntimeError(message)
    return value


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def connect():
    sys.path.insert(0, str(BRIDGE))
    from src.utils import resolve_bridge_client
    return resolve_bridge_client.connect(require_enabled=False, timeout=30.0)


def movie_stem(movie):
    return movie["id"] + ("_" + movie["edit_version"] if movie.get("edit_version", "V01") != "V01" else "")


def timeline_name(movie):
    return movie["id"] + "_DRAFT_" + movie.get("edit_version", "V01") + "_24FPS"


def picture_edit_identity(movie, sources):
    """Return only the picture-edit fields that make a render reusable."""
    return [
        (
            shot["source"],
            sources.get(shot["source"], {}).get("sha256"),
            shot["source_start"],
            shot["source_end_exclusive"],
        )
        for shot in movie.get("shots", [])
    ]


def guard_existing_render_reuse(previous, movies, sources, exports_root):
    """Refuse silent same-version reuse after a picture edit changes."""
    prior_movies = {movie["id"]: movie for movie in previous.get("movies", [])}
    prior_sources = previous.get("sources", {})
    for movie in movies:
        output = exports_root / (movie_stem(movie) + ".mp4")
        if not output.exists():
            continue
        prior = prior_movies.get(movie["id"])
        if not prior or prior.get("edit_version", "V01") != movie.get("edit_version", "V01"):
            raise RuntimeError(
                "Existing render has no matching prior edit authority for %s; "
                "bump edit_version to an unused version" % movie["id"]
            )
        current_identity = picture_edit_identity(movie, sources)
        prior_identity = picture_edit_identity(prior, prior_sources)
        if current_identity != prior_identity:
            raise RuntimeError(
                "Existing render reuse refused for %s: picture edit identity "
                "changed (source/hash/range/order); bump edit_version before "
                "reusing %s" % (movie["id"], output.name)
            )


def prepare():
    plan = read(ROOT / "design/day_one_davinci_draft_edit.json")
    ledger = read(V3 / "EXHAUSTIVE_159_FILE_LEDGER.json")
    evidence = {item["filename"]: item for item in ledger["entries"]}
    matrix = {item["shot_id"]: item for item in read(V3 / "ALL_SHOT_DECISION_MATRIX.json")["shots"]}
    roots = [Path(path) for path in plan["media_roots"].values()]
    files = {}
    for root in roots:
        for path in root.rglob("*.mp4"):
            files.setdefault(path.name, []).append(path)
    prior_path = PACKET / "ASSEMBLY_MANIFEST.json"
    previous = read(prior_path) if prior_path.exists() else {}
    if previous and previous["plan_sha256"] != digest(ROOT / "design/day_one_davinci_draft_edit.json"):
        history = PACKET / "history" / previous["plan_sha256"][:12]
        history.mkdir(parents=True, exist_ok=True)
        for filename in ["ASSEMBLY_MANIFEST.json", "EXPORT_MANIFEST.json", "RESOLVE_READBACK.json", "runtime_manifest.json"]:
            path = PACKET / filename
            if path.exists() and not (history / filename).exists():
                shutil.copy2(path, history / filename)
    # Keep provenance for the untouched sources behind earlier review cuts too.
    sources = previous.get("sources", {}).copy()
    movies = []
    source_root = PACKET / "sources"
    source_root.mkdir(parents=True, exist_ok=True)
    for movie in plan["timeline_selection"]["movies"]:
        movie_id = "D1-" + movie["movie"].split("_")[0]
        result = {"id": movie_id, "edit_version": movie.get("edit_version", "V01"), "title": movie["movie"], "status": movie["status"], "runtime_preview_eligible": movie.get("runtime_preview_eligible", False), "shots": [], "excluded_shots": []}
        cursor = 0
        for shot in movie["shots"]:
            sid = "D1-" + shot["shot"]
            active = shot.get("active", False)
            if not active:
                result["excluded_shots"].append({"shot": sid, "source": shot.get("source"), "reason": shot.get("reason", shot.get("note", shot.get("status", "not selected")))})
                continue
            selected = require(shot.get("source"), f"Active shot missing source: {sid}")
            name = Path(selected).name
            if shot.get("provenance") == "local_user_supplied":
                source = Path(selected)
                require(source.is_absolute() and source.is_file(), f"Missing explicit local source: {selected}")
                sha = digest(source)
                require(sha == shot.get("sha256"), f"Local source changed after visual audit: {name}")
                provenance = {"kind": "local_user_supplied", "source_url": None, "source_commit": None, "git_blob": None}
            else:
                entry = require(evidence.get(name), f"Source not in exhaustive ledger: {name}")
                matches = require(files.get(name), f"Missing local source: {name}")
                source = matches[0]
                sha = digest(source)
                require(all(digest(p) == sha for p in matches), f"Ambiguous source bytes: {name}")
                expected_path = entry["source_url"].split("/blob/" + entry["commit"] + "/", 1)[1]
                expected_blob = subprocess.check_output(["git", "rev-parse", entry["commit"] + ":" + expected_path], cwd=ROOT, text=True).strip()
                actual_blob = subprocess.check_output(["git", "hash-object", "--no-filters", str(source)], cwd=ROOT, text=True).strip()
                require(actual_blob == expected_blob, f"Clip differs from audited Git source: {name}")
                provenance = {"kind": "audited_git_blob", "source_url": entry["source_url"], "source_commit": entry["commit"], "git_blob": actual_blob}
            media = probe(source)
            video = next(s for s in media["streams"] if s["codec_type"] == "video")
            require(video["r_frame_rate"] == "24/1", f"Unexpected frame rate: {name}")
            require(video["width"] <= 1280 and video["height"] == 720, f"Unreviewed source dimensions: {name}")
            start, end = shot["range"]
            require(0 <= start < end <= int(video["nb_frames"]), f"Invalid source range: {sid}")
            destination = source_root / name
            if destination.exists():
                require(digest(destination) == sha, f"Refusing changed source copy: {destination}")
            else:
                shutil.copy2(source, destination)
            sources[name] = {"file": destination.relative_to(PACKET).as_posix(), "original_local_file": str(source), **provenance, "sha256": sha, "bytes": destination.stat().st_size, "dimensions": [video["width"], video["height"]], "fps": 24, "native_frames": int(video["nb_frames"]), "modifications": "none; byte-identical copy", "normalization": "whole-canvas scale-to-fit with black padding; no crop or subject transform", "role": "grok_editorial_motion_reference", "delivery_accepted": False}
            result["shots"].append({"shot": sid, "source": name, "source_start": start, "source_end_exclusive": end, "record_start": cursor, "record_end_exclusive": cursor + end - start, "strict_disposition": matrix.get(sid, {}).get("strict_disposition", "UNKNOWN"), "edit_note": shot.get("edit_note", shot.get("note", shot.get("trim", "straight cut")))})
            cursor += end - start
        result["frames"] = cursor
        result["seconds"] = cursor / 24
        movies.append(result)
    guard_existing_render_reuse(previous, movies, sources, PACKET / "exports")
    manifest = {"schema": "day-one-davinci-assembly-v1", "project": PROJECT, "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "plan_sha256": digest(ROOT / "design/day_one_davinci_draft_edit.json"), "fps": 24, "resolution": [1280, 720], "audio": "video-only; runtime retains authored score; no generated dialogue", "method": "native-rate source trimming and hard cuts in DaVinci Resolve", "claims": {"editorial_reference_only": True, "delivery_accepted": False}, "sources": sources, "movies": movies}
    write(PACKET / "ASSEMBLY_MANIFEST.json", manifest)
    print(json.dumps({"phase": "prepared", "sources": len(sources), "movies": sum(bool(m["shots"]) for m in movies), "seconds": sum(m["seconds"] for m in movies)}), flush=True)
    return manifest


def assemble(manifest):
    resolve = connect()
    manager = require(resolve.GetProjectManager(), "Project manager unavailable")
    project = require(manager.GetCurrentProject(), "Open the new Day One project in Resolve")
    require(project.GetName() == PROJECT, f"Refusing unexpected current project: {project.GetName()}")
    for key, value in (("timelineFrameRate", "24"), ("timelineResolutionWidth", "1280"), ("timelineResolutionHeight", "720"), ("timelineInputResMismatchBehavior", "scaleToFit"), ("timelineOutputResMismatchBehavior", "scaleToFit"), ("imageRetimeInterpolation", "nearest")):
        require(project.SetSetting(key, value), f"Cannot set {key}")
        actual = project.GetSetting(key)
        matches = float(actual) == float(value) if key == "timelineFrameRate" else str(actual) == value
        require(matches, f"Setting readback mismatch: {key}: {actual!r}")
    pool = project.GetMediaPool()
    root = pool.GetRootFolder()
    bins = {folder.GetName(): folder for folder in root.GetSubFolderList() or []}
    media_bin = bins.get("01_VERIFIED_SOURCES") or pool.AddSubFolder(root, "01_VERIFIED_SOURCES")
    require(pool.SetCurrentFolder(media_bin), "Cannot select verified source bin")
    items = {item.GetClipProperty("File Name"): item for item in media_bin.GetClipList() or []}
    for name, source in manifest["sources"].items():
        if name not in items:
            imported = require(pool.ImportMedia([str(PACKET / source["file"])]), f"Import failed: {name}")
            require(len(imported) == 1, f"Unexpected import count: {name}")
            items[name] = imported[0]
    timelines = {project.GetTimelineByIndex(i).GetName(): project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1)}
    readback = []
    project_dir = PACKET / "project"
    project_dir.mkdir(exist_ok=True)
    for movie in manifest["movies"]:
        if not movie["shots"]:
            continue
        name = timeline_name(movie)
        existing = name in timelines
        pool.SetCurrentFolder(root)
        timeline = timelines.get(name) or require(pool.CreateEmptyTimeline(name), f"Timeline creation failed: {name}")
        require(project.SetCurrentTimeline(timeline), "Cannot select timeline")
        if not existing:
            require(timeline.SetStartTimecode("01:00:00:00"), "Cannot set timeline timecode")
            infos = [{"mediaPoolItem": items[s["source"]], "startFrame": s["source_start"], "endFrame": s["source_end_exclusive"], "mediaType": 1, "trackIndex": 1, "recordFrame": timeline.GetStartFrame() + s["record_start"]} for s in movie["shots"]]
            require(pool.AppendToTimeline(infos), f"Append failed: {name}")
        actual_items = list(timeline.GetItemListInTrack("video", 1) or [])
        require(len(actual_items) == len(movie["shots"]), f"Timeline item count mismatch: {name}")
        rows = []
        for actual, expected in zip(actual_items, movie["shots"]):
            actual_name = actual.GetMediaPoolItem().GetClipProperty("File Name")
            length = actual.GetEnd() - actual.GetStart()
            require(actual_name == expected["source"], f"Wrong source in {name}")
            require(length == expected["source_end_exclusive"] - expected["source_start"], f"Wrong duration in {name}: {actual_name} got {length}")
            require(actual.GetSourceStartFrame() == expected["source_start"], f"Wrong source in-point: {actual_name}")
            require(actual.GetStart() == timeline.GetStartFrame() + expected["record_start"], f"Gap or overlap: {name}")
            color = "Orange" if expected["strict_disposition"] == "REMAKE" else "Green"
            actual.SetClipColor(color)
            if not existing:
                timeline.AddMarker(expected["record_start"], color, expected["shot"], expected["strict_disposition"] + ": " + expected["edit_note"], 1, "day-one-draft-v1")
            rows.append({"source": actual_name, "source_start": actual.GetSourceStartFrame(), "source_end": actual.GetSourceEndFrame(), "record_start": actual.GetStart(), "record_end": actual.GetEnd(), "duration": length})
        require(timeline.GetEndFrame() - timeline.GetStartFrame() == movie["frames"], f"Timeline total mismatch: {name}")
        require(timeline.GetTrackCount("audio") == 0 or not timeline.GetItemListInTrack("audio", 1), f"Unapproved audio entered {name}")
        export_path = project_dir / (movie_stem(movie) + ".drt")
        if not export_path.exists():
            require(timeline.Export(str(export_path), resolve.EXPORT_DRT), f"DRT export failed: {name}")
        readback.append({"id": movie["id"], "timeline": name, "frames": movie["frames"], "items": rows})
        print(json.dumps({"phase": "assembled", "movie": movie["id"], "frames": movie["frames"], "shots": len(rows)}), flush=True)
    require(manager.SaveProject(), "Project save failed")
    version = max(movie.get("edit_version", "V01") for movie in manifest["movies"])
    drp = project_dir / ("Day_One_Game_Cohesion_Draft_" + version + ".drp")
    if not drp.exists():
        require(manager.ExportProject(PROJECT, str(drp)), "DRP export failed")
    report = {"resolve_product": resolve.GetProductName(), "resolve_version": resolve.GetVersionString(), "project": PROJECT, "saved": True, "project_export": drp.relative_to(PACKET).as_posix(), "project_export_sha256": digest(drp), "timelines": readback}
    write(PACKET / "RESOLVE_READBACK.json", report)
    return resolve, project


def render(manifest, resolve, project):
    exports = PACKET / "exports"
    exports.mkdir(exist_ok=True)
    jobs = []
    require(project.SetCurrentRenderMode(1), "Cannot set single-clip rendering")
    require(project.SetCurrentRenderFormatAndCodec("mp4", "H264"), "H264 unavailable")
    timelines = {project.GetTimelineByIndex(i).GetName(): project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1)}
    for movie in manifest["movies"]:
        if not movie["shots"]:
            continue
        output = exports / (movie_stem(movie) + ".mp4")
        if output.exists():
            media = probe(output)
            video = next(s for s in media["streams"] if s["codec_type"] == "video")
            require(int(video["nb_frames"]) == movie["frames"], f"Existing render duration mismatch: {output}")
            continue
        project.SetCurrentTimeline(timelines[timeline_name(movie)])
        require(project.SetRenderSettings({"TargetDir": str(exports), "CustomName": movie_stem(movie), "SelectAllFrames": True, "ExportVideo": True, "ExportAudio": False, "FormatWidth": 1280, "FormatHeight": 720, "FrameRate": 24}), "Render settings failed")
        jobs.append({"id": movie["id"], "job": require(project.AddRenderJob(), "Render job failed")})
    write(PACKET / "RENDER_JOBS.json", jobs)
    if jobs:
        require(project.StartRendering([j["job"] for j in jobs]), "Render start failed")
        while project.IsRenderingInProgress():
            print(json.dumps({"phase": "rendering", "jobs": [{"id": j["id"], "status": project.GetRenderJobStatus(j["job"])} for j in jobs]}), flush=True)
            time.sleep(5)
        for job in jobs:
            job["status"] = project.GetRenderJobStatus(job["job"])
            require(job["status"].get("JobStatus") == "Complete", f"Render not complete: {job}")
        write(PACKET / "RENDER_JOBS.json", jobs)
    runtime_path = PACKET / "runtime_manifest.json"
    runtime = read(runtime_path)
    outputs = []
    for movie in manifest["movies"]:
        row = runtime["movies"].setdefault(movie["id"], {})
        row["runtime_preview_eligible"] = bool(movie["runtime_preview_eligible"] and movie["shots"])
        row["editorial_status"] = movie["status"]
        if not movie["shots"]:
            continue
        mp4 = exports / (movie_stem(movie) + ".mp4")
        video = next(s for s in probe(mp4)["streams"] if s["codec_type"] == "video")
        require(int(video["nb_frames"]) == movie["frames"], f"Rendered frame count mismatch: {mp4}")
        ogv = exports / (movie_stem(movie) + ".ogv")
        if not ogv.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-i", str(mp4), "-map", "0:v:0", "-an", "-c:v", "libtheora", "-q:v", "8", "-pix_fmt", "yuv420p", str(ogv)], check=True)
        row.update({"path": ogv.relative_to(PACKET).as_posix(), "frames": movie["frames"], "fps": 24, "sha256": digest(ogv), "delivery_accepted": False})
        outputs.append({"id": movie["id"], "mp4": mp4.relative_to(PACKET).as_posix(), "mp4_sha256": digest(mp4), "ogv": row["path"], "ogv_sha256": row["sha256"], "frames": movie["frames"], "seconds": movie["seconds"], "runtime_preview_eligible": row["runtime_preview_eligible"]})
        print(json.dumps({"phase": "encoded", "movie": movie["id"], "frames": movie["frames"]}), flush=True)
    write(runtime_path, runtime)
    write(PACKET / "EXPORT_MANIFEST.json", {"outputs": outputs, "source": "DaVinci Resolve rendered MP4; whole-frame Theora encoding only", "delivery_accepted": False})
    require(resolve.GetProjectManager().SaveProject(), "Save after render failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    manifest = prepare()
    if args.prepare_only:
        return
    resolve, project = assemble(manifest)
    if args.render:
        render(manifest, resolve, project)


if __name__ == "__main__":
    main()
