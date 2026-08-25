"""Frame-accurate plan for the owner-requested otter-wing revision."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
DOWNLOADS = Path.home() / "Downloads"
PROJECT_NAME = "Mermaid Roshan - Otter Wing Recut 2026-08-23 v1"
TIMELINE_NAME = "MERMAID_ROSHAN_OTTER_WING_RECUT_V2_24FPS"
FPS = 24


@dataclass(frozen=True)
class Shot:
	beat: str
	file: str
	start_frame: int
	duration_frames: int
	transition_in: str = "hard_cut"

	@property
	def path(self) -> Path:
		return DOWNLOADS / self.file


# The previous 72-frame play_resolution shot is intentionally absent.  The
# cabin return begins at source frame 612, after the 60-frame open-palm/wave
# gesture, on the settled two-shot.
SHOTS = (
	Shot("flight_departure", "grok-0502fb4c-eef6-4016-b0a9-043bd2b566b5.mp4", 0, 48),
	Shot("cabin_connection", "grok-0d7c3f2a-78e1-4c92-afb4-250d1a4a7f37-720p.mp4", 6, 96),
	Shot("island_and_castle_approach", "grok-a8018b14-ef72-4e1d-9ae8-b3f287b32dd4.mp4", 12, 36, "cross_dissolve_24f"),
	Shot("castle_reveal_and_forest_breath", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 204, 168),
	Shot("otter_discovery", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 372, 36),
	Shot("otter_jump_retained", "grok-b313bcb5-6577-46b0-80f6-b383830c786d-720p.mp4", 12, 121),
	Shot("cabin_return_after_wave", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 612, 60),
	Shot("exterior_reunion", "grok-bcbfb2e3-7801-4883-af10-8a2d2d34607e-720p.mp4", 12, 121, "cross_dissolve_24f"),
	Shot("castle_bridge_arrival", "grok-ef4539b3-2854-43b4-af2e-870f09a6d0d8-720p.mp4", 12, 121, "cross_dissolve_24f"),
)


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def write_plan() -> Path:
	record_frame = 0
	rows = []
	for shot in SHOTS:
		if not shot.path.is_file():
			raise FileNotFoundError(shot.path)
		row = asdict(shot)
		row.update({
			"source_path": str(shot.path),
			"source_sha256": sha256(shot.path),
			"record_start_frame": record_frame,
			"record_end_frame_exclusive": record_frame + shot.duration_frames,
			"record_start_seconds": record_frame / FPS,
			"record_end_seconds": (record_frame + shot.duration_frames) / FPS,
		})
		rows.append(row)
		record_frame += shot.duration_frames
	destination = PACKAGE / "edit_decision_list_v2.json"
	destination.write_text(json.dumps({
		"project": PROJECT_NAME,
		"timeline": TIMELINE_NAME,
		"fps": FPS,
		"duration_frames": record_frame,
		"duration_seconds": record_frame / FPS,
		"removed": [
			{"beat": "duplicate_play_resolution", "old_record_frames": [505, 577], "old_record_seconds": [21.0416667, 24.0416667], "source_frames": [480, 552]},
			{"beat": "wave_to_otter_on_wing", "old_record_frames": [577, 637], "old_record_seconds": [24.0416667, 26.5416667], "source_frames": [552, 612]},
		],
		"retained_jump_source_audio": {
			"file": str(DOWNLOADS / "grok-b313bcb5-6577-46b0-80f6-b383830c786d-720p.mp4"),
			"source_frames": [12, 133],
			"record_frames": [384, 505],
			"sample_rate": 48000,
			"channels": 2,
		},
		"shots": rows,
	}, indent=2) + "\n", encoding="utf-8")
	return destination


if __name__ == "__main__":
	print(write_plan())
