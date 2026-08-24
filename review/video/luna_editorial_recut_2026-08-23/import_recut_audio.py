"""Import the bespoke recut mix and place it on A1 in Resolve."""

from __future__ import annotations

import json
from pathlib import Path

from resolve_bridge_client import ResolveBridgeClient


PACKAGE = Path(__file__).resolve().parent


def main() -> None:
	client = ResolveBridgeClient()
	audio = (PACKAGE / "luna_recut_audio_mix_resolve.wav").resolve()
	items = client.call("ImportMedia", [str(audio)], target="media_pool") or []
	if not items:
		root = client.call("GetRootFolder", target="media_pool")
		for item in client.call("GetClipList", target=root) or []:
			path = client.call("GetClipProperty", "File Path", target=item)
			if str(path).lower() == str(audio).lower():
				items = [item]
				break
	if len(items) != 1:
		raise RuntimeError(f"Resolve could not locate one audio item; found {len(items)}")
	timeline = "current_timeline"
	start = int(client.call("GetStartFrame", target=timeline))
	end = int(client.call("GetEndFrame", target=timeline))
	appended = client.call("AppendToTimeline", [{
		"mediaPoolItem": items[0],
		"startFrame": 0,
		"endFrame": end - start,
		"recordFrame": start,
		"mediaType": 2,
		"trackIndex": 1,
	}], target="media_pool") or []
	if len(appended) != 1:
		raise RuntimeError("Resolve declined recut audio placement")
	client.call("SaveProject", target="project_manager")
	print(json.dumps({
		"audio": str(audio),
		"audio_items": len(client.call("GetItemListInTrack", "audio", 1, target=timeline)),
		"start_frame": start,
		"end_frame": end,
	}, indent=2))


if __name__ == "__main__":
	main()
