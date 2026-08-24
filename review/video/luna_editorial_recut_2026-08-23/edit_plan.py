"""Authoritative frame-accurate editorial plan for the final recut."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
DOWNLOADS = Path.home() / "Downloads"
PROJECT_NAME = "Mermaid Roshan - Luna Editorial Recut 2026-08-23 v5"
TIMELINE_NAME = "MERMAID_ROSHAN_LUNA_RECUT_V1_24FPS"
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


SHOTS = (
	Shot("flight_departure", "grok-0502fb4c-eef6-4016-b0a9-043bd2b566b5.mp4", 0, 48),
	Shot("cabin_connection", "grok-0d7c3f2a-78e1-4c92-afb4-250d1a4a7f37-720p.mp4", 6, 96),
	Shot("island_and_castle_approach", "grok-a8018b14-ef72-4e1d-9ae8-b3f287b32dd4.mp4", 12, 36, "cross_dissolve_24f"),
	Shot("castle_reveal_and_forest_breath", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 204, 168),
	Shot("otter_discovery", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 372, 36),
	Shot("otter_plane_play", "grok-b313bcb5-6577-46b0-80f6-b383830c786d-720p.mp4", 12, 121),
	Shot("play_resolution", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 480, 72),
	Shot("cabin_return", "GROK_OTTER_PLANE_MASTER_20260823_V02_REVIEW.mp4", 552, 120),
	Shot("exterior_reunion", "grok-bcbfb2e3-7801-4883-af10-8a2d2d34607e-720p.mp4", 12, 121, "cross_dissolve_24f"),
	Shot("castle_bridge_arrival", "grok-ef4539b3-2854-43b4-af2e-870f09a6d0d8-720p.mp4", 12, 121, "cross_dissolve_24f"),
)


def write_plan() -> Path:
	record_frame = 0
	rows = []
	for shot in SHOTS:
		row = asdict(shot)
		row["record_start_frame"] = record_frame
		row["record_end_frame_exclusive"] = record_frame + shot.duration_frames
		row["record_start_seconds"] = record_frame / FPS
		row["record_end_seconds"] = (record_frame + shot.duration_frames) / FPS
		rows.append(row)
		record_frame += shot.duration_frames
	destination = PACKAGE / "edit_decision_list.json"
	destination.write_text(json.dumps({
		"project": PROJECT_NAME,
		"timeline": TIMELINE_NAME,
		"fps": FPS,
		"duration_frames": record_frame,
		"duration_seconds": record_frame / FPS,
		"shots": rows,
	}, indent=2) + "\n", encoding="utf-8")
	return destination


if __name__ == "__main__":
	print(write_plan())
