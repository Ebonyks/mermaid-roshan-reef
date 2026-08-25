"""Place the revised full-length mix on A1 of the active v2 Resolve timeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE.parent))

from resolve_bridge_client import ResolveBridgeClient  # noqa: E402
from otter_recut_v2_plan import PROJECT_NAME  # noqa: E402


def main() -> None:
	client = ResolveBridgeClient()
	if client.request("health")["current_project"] != PROJECT_NAME:
		raise RuntimeError("Wrong active project")
	audio = (PACKAGE / "otter_recut_v2_audio_mix_resolve.wav").resolve()
	items = client.call("ImportMedia", [str(audio)], target="media_pool") or []
	if len(items) != 1:
		raise RuntimeError(f"Resolve imported {len(items)} audio items")
	start = int(client.call("GetStartFrame", target="current_timeline"))
	end = int(client.call("GetEndFrame", target="current_timeline"))
	appended = client.call("AppendToTimeline", [{
		"mediaPoolItem": items[0], "startFrame": 0, "endFrame": end - start,
		"recordFrame": start, "mediaType": 2, "trackIndex": 1,
	}], target="media_pool") or []
	if len(appended) != 1:
		raise RuntimeError("Resolve declined A1 placement")
	client.call("SaveProject", target="project_manager")
	print(json.dumps({"audio": str(audio), "start_frame": start, "end_frame": end}, indent=2))


if __name__ == "__main__":
	main()
