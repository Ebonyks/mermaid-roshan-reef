"""Block Sky Lagoon composition/contact regressions against independent art facts."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "scripts/arena/sky_lagoon_layout.json"
RUNTIME_PATH = ROOT / "scripts/arena/sky_lagoon_promenade.gd"
PREVIEW_PATH = ROOT / "tools/build_sky_lagoon_preview.py"


def project_path(value: str) -> Path:
	return ROOT / value.removeprefix("res://")


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def point_in_polygon(point: tuple[float, float], polygon: list[list[float]]) -> bool:
	x, y = point
	inside = False
	previous = polygon[-1]
	for current in polygon:
		x1, y1 = previous
		x2, y2 = current
		if (y1 > y) != (y2 > y):
			crossing_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
			if x < crossing_x:
				inside = not inside
		previous = current
	return inside


def validate(manifest: dict[str, object]) -> list[str]:
	errors: list[str] = []
	plate = manifest["plate"]
	cards = manifest["cards"]
	regions = manifest["protected_regions"]
	roshan = manifest["roshan_route"]

	for contract in (plate, cards["castle"], cards["tall_tree"], roshan):
		path = project_path(str(contract["path"]))
		if not path.is_file():
			errors.append(f"missing bound asset: {path.relative_to(ROOT)}")
		elif sha256(path) != contract["sha256"]:
			errors.append(f"stale asset hash: {path.relative_to(ROOT)}")

	castle = cards["castle"]
	anchor_pixel = tuple(float(value) for value in castle["anchor_pixel"])
	anchor_master = tuple(float(value) for value in castle["anchor_master"])
	with Image.open(project_path(str(castle["path"]))) as source:
		image = source.convert("RGBA")
		alpha = image.getchannel("A")
		bounds = alpha.point(lambda value: 255 if value >= 26 else 0).getbbox()
		pixel_alpha = alpha.getpixel((round(anchor_pixel[0]), round(anchor_pixel[1])))
		if bounds is None or pixel_alpha < 26:
			errors.append("bridge landing anchor is not on visible castle-card artwork")
		elif anchor_pixel[1] < bounds[3] - 6:
			errors.append("bridge landing anchor is not at the visible card tip")
	if castle.get("anchor_id") != "bridge_landing_tip":
		errors.append("castle is not owned by the visible bridge-tip anchor")
	if castle.get("terrain_class") != "foreground_stone_landing" or not point_in_polygon(
		anchor_master, regions["foreground_stone_landing"]
	):
		errors.append("bridge landing anchor is outside the reviewed stone socket")

	tall_tree = cards["tall_tree"]
	if tall_tree.get("enabled") is not False or tall_tree.get("role") != "unsupported_new_dressing":
		errors.append("unsupported tall tree was re-enabled or mislabeled as extracted art")
	# The rejected runtime footprint intersects the independently reviewed scenic
	# path. This is a mutation witness: reviving the old coordinate must fail.
	legacy_tree_samples = [
		(x, y)
		for x in range(4040, 4321, 20)
		for y in range(720, 1186, 20)
	]
	if not any(point_in_polygon(point, regions["mountain_path_keep_clear"])
		for point in legacy_tree_samples):
		errors.append("mountain-path mask no longer catches the rejected tree placement")

	with Image.open(project_path(str(roshan["path"]))) as source:
		image = source.convert("RGBA")
		frame_width = int(roshan["frame_size"][0])
		frame_height = int(roshan["frame_size"][1])
		frame = int(roshan["frame"])
		columns = int(roshan["columns"])
		left = (frame % columns) * frame_width
		top = (frame // columns) * frame_height
		alpha = image.crop((left, top, left + frame_width, top + frame_height)).getchannel("A")
		bounds = alpha.point(lambda value: 255 if value >= 26 else 0).getbbox()
		contact = tuple(float(value) for value in roshan["contact_anchor_pixel"])
		pixel_alpha = alpha.getpixel((int(contact[0]), int(contact[1])))
		if bounds is None or pixel_alpha < 26 or contact[1] < bounds[3] - 1.5:
			errors.append("Roshan land contact anchor is not on the visible silhouette bottom")
	if roshan.get("medium") != "land" or roshan.get("shadow_contract") != "contact_anchor":
		errors.append("Roshan route medium/contact contract is not grounded land travel")

	runtime = RUNTIME_PATH.read_text(encoding="utf-8")
	preview = PREVIEW_PATH.read_text(encoding="utf-8")
	for forbidden in (
		"Vector2(4180, 1185)",
		"ROSHAN_SWIM_FRONT",
		"PLAYER_HEIGHT_PX * 0.47",
		"background_socket_healed",
	):
		if forbidden in runtime:
			errors.append(f"runtime revived rejected literal/attestation: {forbidden}")
	if "sky_lagoon_layout.json" not in runtime or "sky_lagoon_layout.json" not in preview:
		errors.append("runtime and preview do not share the canonical layout manifest")
	if "place_master_anchor(canvas, LAYOUT[\"cards\"][\"castle\"])" not in preview:
		errors.append("preview does not place the castle from its bridge-tip contract")

	return errors


def mutation_tests(manifest: dict[str, object]) -> list[str]:
	errors: list[str] = []
	mutated = copy.deepcopy(manifest)
	mutated["cards"]["castle"]["anchor_master"][1] = 1120.0
	if not validate(mutated):
		errors.append("bridge-in-water anchor mutation was accepted")
	mutated = copy.deepcopy(manifest)
	mutated["cards"]["tall_tree"]["enabled"] = True
	if not validate(mutated):
		errors.append("path-blocking tall-tree mutation was accepted")
	mutated = copy.deepcopy(manifest)
	mutated["roshan_route"]["medium"] = "water"
	if not validate(mutated):
		errors.append("land-to-water locomotion mutation was accepted")
	mutated = copy.deepcopy(manifest)
	mutated["roshan_route"]["contact_anchor_pixel"][1] -= 20.0
	if not validate(mutated):
		errors.append("airborne Roshan contact mutation was accepted")
	return errors


def main() -> int:
	manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
	errors = validate(manifest) + mutation_tests(manifest)
	if errors:
		for error in errors:
			print(f"SKY_LAGOON_LAYOUT_AUDIT|FAIL|{error}")
		return 1
	print("SKY_LAGOON_LAYOUT_AUDIT|ALL OK")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
