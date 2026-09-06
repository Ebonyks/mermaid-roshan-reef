"""Register C14 packet rasters and Markdown without changing unrelated ledger text.

Normal mode replaces only the two C14-owned marker blocks.  ``--check`` computes
the same deterministic blocks and compares them with the files on disk without
writing anything.  This helper intentionally records unresolved provenance as a
finding; it never invents a license or source authority.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACKET_REL = Path("assets_src/cinematics/d1_c14_castle_team_cleanup_v1")
LICENSES = ROOT / "ASSET_LICENSES.md"
LEDGER = ROOT / "design/05_DOC_LEDGER.md"
RASTER = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
LICENSE_START = "C14_CLEANUP_ASSETS_START"
LICENSE_END = "C14_CLEANUP_ASSETS_END"
DOC_START = "C14_CLEANUP_DOCS_START"
DOC_END = "C14_CLEANUP_DOCS_END"


def digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def dimensions(path: Path) -> str:
	try:
		with Image.open(path) as image:
			return f"{image.width}x{image.height}"
	except Exception:
		return "unknown"


def read_json(path: Path):
	return json.loads(path.read_text(encoding="utf-8-sig"))


def walk(value):
	if isinstance(value, dict):
		yield value
		for child in value.values():
			yield from walk(child)
	elif isinstance(value, list):
		for child in value:
			yield from walk(child)


def norm_path(value: str, packet: Path) -> str:
	value = value.replace("\\", "/")
	path = Path(value)
	packet_prefix = packet.name + "/"
	packet_rel_prefix = PACKET_REL.as_posix().rstrip("/") + "/"
	if value.startswith(packet_rel_prefix):
		return value[len(packet_rel_prefix):]
	if value.startswith(packet_prefix):
		return value[len(packet_prefix):]
	if path.is_absolute():
		try:
			return path.resolve().relative_to(packet.resolve()).as_posix()
		except ValueError:
			return path.as_posix()
	return path.as_posix().lstrip("./")


def source_rows(packet: Path) -> dict[str, dict]:
	path = packet / "SOURCE_ASSETS.json"
	if not path.is_file():
		return {}
	data = read_json(path)
	return {str(row.get("id")): row for row in data.get("assets", []) if row.get("id")}


def generation_rows(packet: Path) -> dict[str, dict]:
	result = {}
	for path in sorted((packet / "generation_records").glob("*.json")):
		try:
			data = read_json(path)
		except (OSError, ValueError, json.JSONDecodeError):
			continue
		for row in walk(data):
			if not isinstance(row, dict):
				continue
			output = row.get("output_path") or row.get("output") or row.get("path")
			prompt = row.get("prompt") or row.get("exact_tool_prompt") or row.get("full_prompt")
			method = row.get("method") or row.get("generation_method")
			native = row.get("native_output_path")
			if not isinstance(output, str) or not isinstance(prompt, str) or not prompt.strip() or not isinstance(method, str) or not method.strip() or not isinstance(native, str) or not native.strip():
				continue
			result[norm_path(output, packet)] = {
				"record": path.relative_to(packet).as_posix(),
				"row": row,
			}
	return result


def audit_frame_rows(packet: Path) -> dict[str, dict]:
	"""Map decoded audit frame paths to their full source MP4 evidence."""
	path = packet / "audit" / "DOWNLOADS_REUSE_REVIEW.json"
	if not path.is_file():
		return {}
	data = read_json(path)
	clips = {str(row.get("prefix")): row for row in data.get("clips", []) if row.get("prefix")}
	result = {}
	for frame in sorted((packet / "audit" / "frames").glob("*")):
		if not frame.is_file() or frame.suffix.lower() not in RASTER:
			continue
		name = frame.stem
		match = re.match(r"(?P<prefix>[0-9a-f]+)_t(?P<seconds>[0-9_]+)$", name, re.I)
		if not match or match.group("prefix") not in clips:
			continue
		clip = clips[match.group("prefix")]
		result[frame.relative_to(packet).as_posix()] = {
			"source": clip.get("path", "UNRESOLVED source MP4"),
			"source_sha256": clip.get("sha256", "UNRESOLVED source MP4 hash"),
			"frame_path": str(frame),
			"timestamp_s": match.group("seconds").replace("_", "."),
			"provenance": "FFmpeg-decoded diagnostic frame from Downloads motion-reference evidence; inherits source restrictions; no blanket rights granted; not delivery art.",
		}
	return result


def reference_row(path: Path, packet: Path, sources: dict[str, dict]) -> dict | None:
	try:
		rel = path.relative_to(packet / "references")
	except ValueError:
		return None
	for row in sources.values():
		if Path(str(row.get("id", "")) + path.suffix.lower()).as_posix() == rel.as_posix():
			return row
	return None


def planned_assets(root: Path, packet: Path) -> tuple[list[str], list[str]]:
	sources = source_rows(packet)
	generation = generation_rows(packet)
	audit_frames = audit_frame_rows(packet)
	rows = []
	warnings = []
	for path in sorted(packet.rglob("*"), key=lambda p: p.relative_to(packet).as_posix()):
		if not path.is_file() or path.suffix.lower() not in RASTER:
			continue
		rel = path.relative_to(root).as_posix()
		packet_rel = path.relative_to(packet).as_posix()
		gen = generation.get(packet_rel)
		ref = reference_row(path, packet, sources)
		audit = audit_frames.get(packet_rel)
		if gen:
			row = gen["row"]
			source = row.get("native_output_path") or row.get("source_path") or "unresolved native output path"
			provenance = "Project-requested built-in image generation; inherits project ASSET_LICENSES.md restrictions; no blanket rights granted; human approval pending."
			mods = f"complete flattened candidate preserved non-destructively; generation record `{PACKET_REL.as_posix()}/{gen['record']}`"
		elif ref:
			source = ref.get("path", "unresolved SOURCE_ASSETS path")
			provenance = ref.get("license_provenance") or "SOURCE_ASSETS provenance present; inherits project restrictions; no blanket rights granted."
			mods = "byte-identical non-destructive packet reference copy"
		elif audit:
			source = audit["source"]
			provenance = f"{audit['provenance']} Full source MP4 SHA-256 `{audit['source_sha256']}`; decoded frame `{audit['frame_path']}` at {audit['timestamp_s']}s."
			mods = "FFmpeg decode only; no pixel repair or destructive modification"
		else:
			source = "UNRESOLVED: no matching generation record or SOURCE_ASSETS reference"
			provenance = "UNRESOLVED provenance; no license or rights claim made; audit/supporting artifact only."
			mods = "preserved as found; not runtime delivery"
			warnings.append(f"missing provenance: {rel}")
		role = "CANDIDATE/non-runtime raster" if not packet_rel.startswith("audit/") else "AUDIT_SUPPORTING/non-runtime raster"
		rows.append(f"- `{rel}` — {role}; source/native origin `{source}`; dimensions `{dimensions(path)}`; SHA-256 `{digest(path)}`; {provenance} Modifications: {mods}.")
	return rows, warnings


def planned_docs(packet: Path) -> list[str]:
	rows = ["## C14 castle team cleanup — scoped document records", "", "| Document | | Authority note |", "|---|---|---|"]
	for path in sorted(packet.rglob("*.md"), key=lambda p: p.relative_to(packet).as_posix()):
		rel = path.relative_to(ROOT).as_posix()
		if path.relative_to(packet).parts[0] == "audit":
			marker = "🔵"
			note = "`SUPPORTING_CURRENT`; current supporting audit; not a design or runtime authority"
		else:
			marker = "🟣"
			note = "`PROPOSED_CANONICAL`; scoped C14 draft; human approval pending; no runtime or delivery authority"
		rows.append(f"| `{rel}` | {marker} | {note}. |")
	return rows


def block(text: str, start: str, end: str) -> str:
	return f"<!-- {start} -->\n{text.rstrip()}\n<!-- {end} -->"


def existing_block(path: Path, start: str, end: str) -> str:
	text = path.read_text(encoding="utf-8-sig")
	match = re.search(re.escape(f"<!-- {start} -->") + r".*?" + re.escape(f"<!-- {end} -->"), text, re.S)
	return match.group(0) if match else ""


def replace_owned_block(path: Path, start: str, end: str, replacement: str) -> None:
	text = path.read_text(encoding="utf-8-sig")
	pattern = re.escape(f"<!-- {start} -->") + r".*?" + re.escape(f"<!-- {end} -->")
	if re.search(pattern, text, re.S):
		text = re.sub(pattern, lambda _match: replacement, text, count=1, flags=re.S)
	else:
		text = text.rstrip() + "\n\n" + replacement + "\n"
	path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--root", type=Path, default=ROOT)
	parser.add_argument("--packet", type=Path, default=None)
	parser.add_argument("--check", action="store_true", help="compare owned blocks without mutation")
	args = parser.parse_args()
	root = args.root.resolve()
	packet = (args.packet or (root / PACKET_REL)).resolve()
	licenses = root / "ASSET_LICENSES.md"
	ledger = root / "design/05_DOC_LEDGER.md"
	asset_rows, warnings = planned_assets(root, packet)
	license_text = block("\n".join(["## C14 cleanup packet — raster provenance", ""] + asset_rows), LICENSE_START, LICENSE_END)
	doc_text = block("\n".join(planned_docs(packet)), DOC_START, DOC_END)
	if warnings:
		print("PROVENANCE_WARNINGS:")
		print("\n".join(f"- {item}" for item in warnings))
	if args.check:
		failed = False
		if warnings:
			failed = True
			print("CHECK_FAILED: unresolved provenance is not acceptable")
		for path, start, end, expected in ((licenses, LICENSE_START, LICENSE_END, license_text), (ledger, DOC_START, DOC_END, doc_text)):
			actual = existing_block(path, start, end)
			if actual != expected:
				failed = True
				print(f"MISMATCH: {path}")
				print("".join(difflib.unified_diff(actual.splitlines(True), expected.splitlines(True), fromfile="actual", tofile="planned")))
		return 1 if failed else 0
	replace_owned_block(licenses, LICENSE_START, LICENSE_END, license_text)
	replace_owned_block(ledger, DOC_START, DOC_END, doc_text)
	print(f"Registered {len(asset_rows)} C14 raster assets and {len(doc_text.splitlines()) - 5} C14 Markdown records.")
	return 0


if __name__ == "__main__":
	sys.exit(main())
