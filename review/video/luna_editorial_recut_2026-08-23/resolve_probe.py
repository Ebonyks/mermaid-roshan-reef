"""Read-only smoke test for the active in-app Resolve bridge."""

from __future__ import annotations

import json

from resolve_bridge_client import ResolveBridgeClient


def main() -> None:
	client = ResolveBridgeClient()
	health = client.request("health")
	print(json.dumps({
		"connected": health["connected"],
		"edition": health["edition"],
		"version": health["version"],
		"current_project": health["current_project"],
		"current_page": health["current_page"],
	}, indent=2))


if __name__ == "__main__":
	main()
