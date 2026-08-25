"""Create a unique Resolve 21 project and build the revised picture timeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE.parent))

from resolve_bridge_client import ResolveBridgeClient  # noqa: E402
from otter_recut_v2_plan import PROJECT_NAME, SHOTS, TIMELINE_NAME, write_plan  # noqa: E402


def main() -> None:
	write_plan()
	client = ResolveBridgeClient()
	health = client.request("health")
	if health["current_project"] != PROJECT_NAME:
		client.call("SaveProject", target="project_manager")
		projects = client.call("GetProjectListInCurrentFolder", target="project_manager") or []
		if PROJECT_NAME in projects:
			project = client.call("LoadProject", PROJECT_NAME, target="project_manager")
		else:
			project = client.call("CreateProject", PROJECT_NAME, target="project_manager")
		if not project:
			raise RuntimeError("Resolve could not open the unique v2 project")
	for key, value in {
		"timelineFrameRate": "24",
		"timelinePlaybackFrameRate": "24",
		"timelineResolutionWidth": "1280",
		"timelineResolutionHeight": "720",
	}.items():
		client.call("SetSetting", key, value, target="project")
	if client.call("GetTimelineCount", target="project"):
		raise RuntimeError("Refusing to alter a non-empty v2 project")
	paths = list(dict.fromkeys(str(shot.path.resolve()) for shot in SHOTS))
	items = client.call("ImportMedia", paths, target="media_pool") or []
	by_path = {}
	for item in items:
		path = client.call("GetClipProperty", "File Path", target=item)
		by_path[str(path).lower()] = item
	missing = [path for path in paths if path.lower() not in by_path]
	if missing:
		raise RuntimeError(f"Resolve did not import media: {missing}")
	timeline = client.call("CreateEmptyTimeline", TIMELINE_NAME, target="media_pool")
	if not timeline:
		raise RuntimeError("Resolve declined timeline creation")
	client.call("SetStartTimecode", "01:00:00:00", target=timeline)
	record_frame = int(client.call("GetStartFrame", target=timeline))
	start_frame = record_frame
	clip_infos = []
	markers = []
	for shot in SHOTS:
		clip_infos.append({
			"mediaPoolItem": by_path[str(shot.path.resolve()).lower()],
			"startFrame": shot.start_frame,
			"endFrame": shot.start_frame + shot.duration_frames,
			"recordFrame": record_frame,
			"mediaType": 1,
			"trackIndex": 1,
		})
		if shot.transition_in != "hard_cut":
			markers.append((record_frame, shot.beat, shot.transition_in))
		record_frame += shot.duration_frames
	appended = client.call("AppendToTimeline", clip_infos, target="media_pool") or []
	if len(appended) != len(SHOTS):
		raise RuntimeError(f"Resolve appended {len(appended)} of {len(SHOTS)} shots")
	for absolute, beat, transition in markers:
		client.call("AddMarker", absolute - start_frame, "Cyan", f"TRANSITION: {transition}", f"Enter {beat}.", 1, "", target=timeline)
	client.call("SetCurrentTimeline", timeline, target="project")
	client.call("SaveProject", target="project_manager")
	print(json.dumps({
		"project": PROJECT_NAME,
		"timeline": TIMELINE_NAME,
		"start_frame": start_frame,
		"end_frame": client.call("GetEndFrame", target=timeline),
		"video_items": len(client.call("GetItemListInTrack", "video", 1, target=timeline)),
		"transition_markers": markers,
	}, indent=2))


if __name__ == "__main__":
	main()
