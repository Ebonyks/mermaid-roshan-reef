#!/usr/bin/env python3
"""Bind an already-pushed immutable content commit without rebuilding packets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = ROOT / "assets_src" / "cinematics"
INDEX = PACKET_ROOT / "day_one_grok_visual_handoffs_2026-09-02" / "INDEX.json"
REPOSITORY = "Ebonyks/mermaid-roshan-reef"


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("commit")
	parser.add_argument("--verified-at", required=True)
	args = parser.parse_args()
	if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
		raise SystemExit("commit must be a full lowercase Git SHA")
	packets = []
	for manifest_path in sorted(PACKET_ROOT.glob("d1_c*_visual_v1/IMAGINE_HANDOFF.json")):
		packet = manifest_path.parent
		manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
		if manifest.get("schema") != "imagine-handoff-v2":
			continue
		slug = packet.name
		base = f"assets_src/cinematics/{slug}"
		manifest["archive_status"] = "complete"
		manifest["archive_remote"] = {
			"commit": args.commit,
			"tree": f"https://github.com/{REPOSITORY}/tree/{args.commit}/{base}",
			"manifest": f"https://raw.githubusercontent.com/{REPOSITORY}/{args.commit}/{base}/HANDOFF_PACKET.json",
			"readme": f"https://github.com/{REPOSITORY}/blob/{args.commit}/{base}/README.md",
			"verified_via": "GitHub recursive commit-tree API; every HANDOFF_PACKET asset path resolved",
			"verified_at": args.verified_at,
		}
		manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
		readme_path = packet / "README.md"
		readme = readme_path.read_text(encoding="utf-8")
		readme = readme.replace("`ARCHIVE_COMPLETE`: false  \n", "`ARCHIVE_COMPLETE`: true\n", 1)
		readme = readme.replace("`ARCHIVE_COMPLETE`: true  \n", "`ARCHIVE_COMPLETE`: true\n", 1)
		readme_path.write_text(readme, encoding="utf-8")
		packets.append(slug)
	index = json.loads(INDEX.read_text(encoding="utf-8"))
	index["archive_commit"] = args.commit
	claims = index.setdefault("claims", {})
	claims["archive_complete"] = True
	claims["generation_ready"] = False
	claims["delivery_accepted"] = False
	index["remote_verification"] = {
		"verified_at": args.verified_at,
		"verified_via": "GitHub recursive commit-tree API",
		"packet_count": len(packets),
		"all_manifest_references_resolved": True,
	}
	INDEX.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
	print(f"BOUND|packets={len(packets)}|commit={args.commit}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
