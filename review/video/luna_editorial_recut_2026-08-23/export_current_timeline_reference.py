"""Export the currently open timeline as FCPXML for schema reference only."""

from __future__ import annotations

import argparse
from pathlib import Path

from resolve_bridge_client import ResolveBridgeClient


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("name", nargs="?", default="existing_timeline_reference.fcpxml")
	args = parser.parse_args()
	client = ResolveBridgeClient()
	constant = client.request(
		"get_attribute", {"target": "resolve", "name": "EXPORT_FCPXML_1_10"}
	)
	if constant.get("kind") != "value":
		raise RuntimeError(f"FCPXML constant unavailable: {constant}")
	destination = Path(__file__).with_name(args.name).resolve()
	result = client.call(
		"Export", str(destination), constant["value"], target="current_timeline"
	)
	if not result:
		raise RuntimeError("Resolve declined FCPXML export")
	print(destination)


if __name__ == "__main__":
	main()
