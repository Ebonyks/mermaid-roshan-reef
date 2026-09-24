#!/usr/bin/env python3
"""Build and verify the Day One story clips (owner exception DL-CIN-16).

Straight cuts at exact recorded frame boundaries from the owner-selected
2026-09-20 Day One cut, plus the 2026-09-04 V03 clean-bathroom endpoint.
Whole-canvas Theora/Vorbis encoding and short audio fades are the only
transforms. No frame is generated, retimed, repeated, cropped or repaired.

  python tools/build_day_one_story_clips.py --source-root <main checkout>
      cuts and encodes every clip, then writes both manifests.
  python tools/build_day_one_story_clips.py --check
      verifies every committed clip against the committed manifests
      (no source media or ffmpeg needed; this is the CI mode).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "assets" / "cinematics" / "day_one_story"
RUNTIME_MANIFEST = RUNTIME_DIR / "story_clips.json"
PROVENANCE_DIR = ROOT / "assets_src" / "cinematics" / "day_one_story_clips_2026-09-23"
PROVENANCE_MANIFEST = PROVENANCE_DIR / "CLIP_MANIFEST.json"

FPS = 24
SELECTED_CUT = "export/movie_selected_cut_20260920/renders/DAY_ONE_SELECTED_CUT.mp4"
SELECTED_CUT_SHA256 = "0698b8119daff5dcab2f0eb998cb69849bf168f5fe3cd06989e9a7629e72a8e7"
SELECTED_CUT_FRAMES = 3394
V03_CLEAN_BATH = ("assets_src/cinematics/day_one_davinci_draft_2026-09-04/sources/"
	"C04_S04_v1_clean_endpoint.mp4")

# id, source key, [start, end) frames, where it plays, picture events it keeps.
CLIPS = [
	("d1_opening", "selected", 0, 733, "New Game: the 30-second introduction to the game",
		"flight with Daddy, landing, walk to the closed castle door"),
	("d1_castle", "selected", 733, 925, "first castle entry (dirty-castle discovery)",
		"castle door opens onto the dirty Main Hall"),
	("d1_bath_arrival", "selected", 925, 1057, "first Bubble Bath arrival",
		"bath threshold and tool"),
	("d1_bath_clean", "v03_clean_bath", 12, 84, "Bubble Bath cleaned",
		"V03 C04-S04 clean endpoint with the happy bath bunny"),
	("d1_pool_arrival", "selected", 1201, 1429, "first Mermaid Pool arrival",
		"dirty pool, blocked waterfall, stuck seahorse"),
	("d1_pool_clean", "selected", 1561, 1969, "Mermaid Pool cleaned",
		"waterfall restored, seahorse flows, Rumi rises and hugs Roshan"),
	("d1_eagle_free", "selected", 1969, 2157, "Playroom rescue complete",
		"Roshan frees Baby Eagle, who flaps his wings"),
	("d1_art_arrival", "selected", 2157, 2253, "first Craft Room arrival",
		"four loose supplies"),
	("d1_art_clean", "selected", 2253, 2445, "Craft Room cleaned",
		"central-table work and the restored room"),
	("d1_rainbow_route", "selected", 2445, 2553, "all four rooms clean (boss door glows)",
		"rainbow trails from the four rooms lead to the royal door"),
	("d1_puff_arrival", "selected", 2553, 2733, "Grand Puff trigger, before Roshan faces him",
		"the attic and the grumpy big dust bunny landing"),
	("d1_puff_transformation", "selected", 2733, 3033, "Grand Puff beaten",
		"family scrub, foam, rainbow dust bunny jumps out as the dusty shell collapses"),
	("d1_epilogue", "selected", 3033, 3394, "after the transformation, before the Day Two card",
		"the new friend helps tidy, room recollections, Daddy's hug"),
]
OMITTED = [
	{"range": [1057, 1201], "reason": "bathroom sink/tub scrubbing: the child performs it in play"},
	{"range": [1429, 1561], "reason": "pool net skimming: the child performs it in play"},
]
VIDEO = {"codec": "libtheora", "quality": 6, "width": 1280, "height": 720,
	"scale_flags": "lanczos", "pixel_format": "yuv420p"}
AUDIO = {"codec": "libvorbis", "quality": 4, "fade_in_s": 0.08, "fade_out_s": 0.12}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def find_tool(name: str) -> str:
	env = os.environ.get(name.upper())
	if env:
		return env
	found = shutil.which(name)
	if found:
		return found
	local = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MermaidReefTools" / "FFmpeg"
	for candidate in sorted(local.glob(f"*/bin/{name}.exe"), reverse=True):
		return str(candidate)
	raise SystemExit(f"STORYCLIPS|FAIL|{name} not found")


def source_path(key: str, source_root: Path) -> Path:
	return source_root / SELECTED_CUT if key == "selected" else ROOT / V03_CLEAN_BATH


def count_frames(ffprobe: str, path: Path) -> int:
	out = subprocess.run([ffprobe, "-v", "error", "-count_frames", "-select_streams", "v:0",
		"-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
		check=True, capture_output=True, text=True).stdout.strip()
	return int(out)


def has_audio(ffprobe: str, path: Path) -> bool:
	out = subprocess.run([ffprobe, "-v", "error", "-select_streams", "a", "-show_entries",
		"stream=index", "-of", "csv=p=0", str(path)], check=True, capture_output=True,
		text=True).stdout.strip()
	return bool(out)


def build(source_root: Path) -> int:
	ffmpeg, ffprobe = find_tool("ffmpeg"), find_tool("ffprobe")
	selected = source_root / SELECTED_CUT
	if not selected.is_file():
		print(f"STORYCLIPS|FAIL|missing source {selected}")
		return 1
	selected_sha = sha256(selected)
	if selected_sha != SELECTED_CUT_SHA256:
		print(f"STORYCLIPS|FAIL|selected cut SHA-256 {selected_sha} != {SELECTED_CUT_SHA256}")
		return 1
	RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
	PROVENANCE_DIR.mkdir(parents=True, exist_ok=True)
	rows, runtime = [], {}
	for clip_id, key, start, end, plays, keeps in CLIPS:
		src = source_path(key, source_root)
		frames = end - start
		seconds = frames / FPS
		out = RUNTIME_DIR / f"{clip_id}.ogv"
		vf = (f"[0:v]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,"
			f"scale={VIDEO['width']}:{VIDEO['height']}:flags={VIDEO['scale_flags']},"
			f"format={VIDEO['pixel_format']}[v]")
		cmd = [ffmpeg, "-v", "error", "-y", "-i", str(src)]
		audio = has_audio(ffprobe, src) and key == "selected"
		if audio:
			fade_out = max(0.0, seconds - AUDIO["fade_out_s"])
			af = (f"[0:a]atrim=start={start / FPS:.6f}:end={end / FPS:.6f},asetpts=PTS-STARTPTS,"
				f"afade=t=in:d={AUDIO['fade_in_s']},afade=t=out:st={fade_out:.6f}:d={AUDIO['fade_out_s']}[a]")
			cmd += ["-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]",
				"-c:a", AUDIO["codec"], "-q:a", str(AUDIO["quality"])]
		else:
			cmd += ["-filter_complex", vf, "-map", "[v]", "-an"]
		cmd += ["-c:v", VIDEO["codec"], "-q:v", str(VIDEO["quality"]), str(out)]
		subprocess.run(cmd, check=True)
		got = count_frames(ffprobe, out)
		if got != frames:
			print(f"STORYCLIPS|FAIL|{clip_id} has {got} frames, expected {frames}")
			return 1
		out_sha = sha256(out)
		rows.append({
			"id": clip_id, "file": f"assets/cinematics/day_one_story/{clip_id}.ogv",
			"plays": plays, "keeps": keeps,
			"source": SELECTED_CUT if key == "selected" else V03_CLEAN_BATH,
			"source_sha256": selected_sha if key == "selected" else sha256(src),
			"source_frames": [start, end], "frames": frames, "seconds": round(seconds, 3),
			"audio": "selected-cut music/ambience/foley mix" if audio else "none (game audio plays)",
			"output_sha256": out_sha, "output_bytes": out.stat().st_size,
			"status": "OWNER_DIRECTED_RUNTIME_CLIP",
		})
		runtime[clip_id] = {"path": f"res://assets/cinematics/day_one_story/{clip_id}.ogv",
			"seconds": round(seconds, 3), "frames": frames}
		print(f"STORYCLIPS|BUILT|{clip_id}|{frames} frames|{out.stat().st_size} bytes")
	manifest = {
		"schema": "day_one_story_clips/1",
		"authority": "Owner decision 2026-09-23, DL-CIN-16 (AGENTS.md): straight cuts from the "
			"owner-selected 2026-09-20 cut between gameplay scenes. OWNER_DIRECTED_RUNTIME_CLIP, "
			"never DELIVERY_ACCEPTED.",
		"fps": FPS,
		"selected_cut": {"path": SELECTED_CUT, "sha256": selected_sha,
			"frames": SELECTED_CUT_FRAMES, "note": "local owner export, not committed (size)"},
		"transforms": {"video": VIDEO, "audio": AUDIO,
			"forbidden": "no generated, retimed, repeated, cropped, warped or repaired frames"},
		"omitted_spans": OMITTED,
		"clips": rows,
	}
	PROVENANCE_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	RUNTIME_MANIFEST.write_text(json.dumps({"schema": "day_one_story_clips/1", "clips": runtime},
		indent=2) + "\n", encoding="utf-8")
	total = sum(r["output_bytes"] for r in rows)
	print(f"STORYCLIPS|RESULT|BUILT {len(rows)} clips|{total} bytes")
	return 0


def check() -> int:
	errors = []
	if not PROVENANCE_MANIFEST.is_file() or not RUNTIME_MANIFEST.is_file():
		print("STORYCLIPS|FAIL|missing manifest")
		return 1
	manifest = json.loads(PROVENANCE_MANIFEST.read_text(encoding="utf-8"))
	runtime = json.loads(RUNTIME_MANIFEST.read_text(encoding="utf-8")).get("clips", {})
	ids = [row["id"] for row in manifest.get("clips", [])]
	if ids != [clip[0] for clip in CLIPS]:
		errors.append("clip list differs from the tool")
	for row, clip in zip(manifest.get("clips", []), CLIPS):
		path = ROOT / row["file"]
		if not path.is_file():
			errors.append(f"{row['id']}: missing {row['file']}")
			continue
		if sha256(path) != row["output_sha256"]:
			errors.append(f"{row['id']}: output hash drift")
		if row["source_frames"] != [clip[2], clip[3]] or row["frames"] != clip[3] - clip[2]:
			errors.append(f"{row['id']}: frame range differs from the tool")
		if row.get("status") != "OWNER_DIRECTED_RUNTIME_CLIP":
			errors.append(f"{row['id']}: wrong status")
		rt = runtime.get(row["id"], {})
		if rt.get("frames") != row["frames"] or not str(rt.get("path", "")).endswith(f"{row['id']}.ogv"):
			errors.append(f"{row['id']}: runtime manifest mismatch")
	extra = sorted(p.name for p in RUNTIME_DIR.glob("*.ogv") if p.stem not in ids)
	if extra:
		errors.append("unmanifested runtime clips: " + ", ".join(extra))
	for error in errors:
		print("STORYCLIPS|FAIL|" + error)
	print("STORYCLIPS|RESULT|" + ("ALL OK" if not errors else f"{len(errors)} ISSUE(S)"),
		f"|{len(ids)} clips")
	return 0 if not errors else 1


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	parser.add_argument("--source-root", type=Path, help="checkout that holds export/")
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	if args.check:
		return check()
	if args.source_root is None:
		parser.error("--source-root is required to build")
	return build(args.source_root.resolve())


if __name__ == "__main__":
	sys.exit(main())
