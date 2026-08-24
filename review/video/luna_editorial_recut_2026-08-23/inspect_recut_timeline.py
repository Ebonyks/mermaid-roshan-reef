"""Print the active recut timeline's clip boundaries."""

from __future__ import annotations

import json

from resolve_bridge_client import ResolveBridgeClient


def main() -> None:
	client = ResolveBridgeClient()
	rows = []
	for track in range(1, 5):
		items = client.call("GetItemListInTrack", "video", track, target="current_timeline") or []
		for item in items:
			rows.append({
				"track": track,
				"name": client.call("GetName", target=item),
				"start": client.call("GetStart", target=item),
				"end": client.call("GetEnd", target=item),
				"duration": client.call("GetDuration", target=item),
			})
	print(json.dumps(rows, indent=2))


if __name__ == "__main__":
	main()
