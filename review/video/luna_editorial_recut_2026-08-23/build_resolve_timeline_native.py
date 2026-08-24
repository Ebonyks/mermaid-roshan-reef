"""Build the recut with Resolve's native MediaPool/Timeline APIs."""

from __future__ import annotations

import json

from edit_plan import PROJECT_NAME, SHOTS, TIMELINE_NAME
from resolve_bridge_client import ResolveBridgeClient


def main() -> None:
	client = ResolveBridgeClient()
	health = client.request("health")
	if health["current_project"] != PROJECT_NAME:
		raise RuntimeError(f"Wrong active project: {health['current_project']!r}")
	# Remove only diagnostic timelines created by failed/importer probes.
	for index in range(client.call("GetTimelineCount", target="project"), 0, -1):
		timeline = client.call("GetTimelineByIndex", index, target="project")
		name = client.call("GetName", target=timeline)
		if name in {"REFERENCE_IMPORT_TEST", TIMELINE_NAME}:
			client.call("DeleteTimelines", [timeline], target="media_pool")
	paths = []
	for shot in SHOTS:
		resolved = str(shot.path.resolve())
		if resolved not in paths:
			paths.append(resolved)
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
	clip_infos = []
	transition_markers = []
	for shot in SHOTS:
		item = by_path[str(shot.path.resolve()).lower()]
		clip_infos.append({
			"mediaPoolItem": item,
			"startFrame": shot.start_frame,
			# Resolve treats endFrame as exclusive for AppendToTimeline. Using
			# duration - 1 creates a one-frame gap at every edit.
			"endFrame": shot.start_frame + shot.duration_frames,
			"recordFrame": record_frame,
			"mediaType": 1,
			"trackIndex": 1,
		})
		if shot.transition_in != "hard_cut":
			transition_markers.append((record_frame, shot.beat, shot.transition_in))
		record_frame += shot.duration_frames
	appended = client.call("AppendToTimeline", clip_infos, target="media_pool") or []
	if len(appended) != len(SHOTS):
		raise RuntimeError(f"Resolve appended {len(appended)} of {len(SHOTS)} shots")
	start_frame = int(client.call("GetStartFrame", target=timeline))
	for absolute_frame, beat, transition in transition_markers:
		client.call(
			"AddMarker",
			absolute_frame - start_frame,
			"Cyan",
			f"TRANSITION: {transition}",
			f"Enter {beat}; apply only at this story/geography change.",
			1,
			"",
			target=timeline,
		)
	client.call("SetCurrentTimeline", timeline, target="project")
	client.call("SaveProject", target="project_manager")
	print(json.dumps({
		"project": PROJECT_NAME,
		"timeline": client.call("GetName", target=timeline),
		"start_frame": start_frame,
		"end_frame": client.call("GetEndFrame", target=timeline),
		"video_items": len(client.call("GetItemListInTrack", "video", 1, target=timeline)),
		"transition_markers": transition_markers,
	}, indent=2))


if __name__ == "__main__":
	main()
