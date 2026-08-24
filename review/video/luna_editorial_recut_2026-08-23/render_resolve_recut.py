"""Render the active recut in Resolve and export a portable project archive."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from edit_plan import PROJECT_NAME
from resolve_bridge_client import ResolveBridgeClient


PACKAGE = Path(__file__).resolve().parent
OUTPUT_STEM = "mermaid_roshan_luna_recut_v1_resolve"


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def main() -> None:
	client = ResolveBridgeClient()
	health = client.request("health")
	if health["current_project"] != PROJECT_NAME:
		raise RuntimeError(f"Wrong active project: {health['current_project']!r}")
	client.call("DeleteAllRenderJobs", target="project")
	if not client.call("SetCurrentRenderFormatAndCodec", "mp4", "H264", target="project"):
		raise RuntimeError("Resolve declined MP4/H.264")
	settings = {
		"TargetDir": str(PACKAGE.resolve()),
		"CustomName": OUTPUT_STEM,
		"SelectAllFrames": True,
		"ExportVideo": True,
		"ExportAudio": True,
		"FormatWidth": 1280,
		"FormatHeight": 720,
		"FrameRate": 24,
		"AudioCodec": "aac",
		"AudioSampleRate": 48_000,
	}
	if not client.call("SetRenderSettings", settings, target="project"):
		raise RuntimeError("Resolve declined render settings")
	job_id = client.call("AddRenderJob", target="project")
	if not job_id:
		raise RuntimeError("Resolve did not add render job")
	if not client.call("StartRendering", job_id, target="project"):
		raise RuntimeError("Resolve did not start rendering")
	deadline = time.monotonic() + 600
	while client.call("IsRenderingInProgress", target="project"):
		if time.monotonic() > deadline:
			raise TimeoutError("Resolve render exceeded ten minutes")
		time.sleep(1.0)
	status = client.call("GetRenderJobStatus", job_id, target="project")
	output = PACKAGE / f"{OUTPUT_STEM}.mp4"
	if status.get("JobStatus") != "Complete" or not output.is_file():
		raise RuntimeError(f"Resolve render failed: {status}")
	client.call("SaveProject", target="project_manager")
	archive = PACKAGE / "Mermaid_Roshan_Luna_Editorial_Recut_2026-08-23.drp"
	if archive.exists():
		raise RuntimeError(f"Refusing to overwrite project archive: {archive}")
	if not client.call("ExportProject", PROJECT_NAME, str(archive), False, target="project_manager"):
		raise RuntimeError("Resolve project export failed")
	result = {
		"render_job": status,
		"video": str(output),
		"video_sha256": sha256(output),
		"project_archive": str(archive),
		"project_archive_sha256": sha256(archive),
	}
	(PACKAGE / "resolve_render_result.json").write_text(
		json.dumps(result, indent=2) + "\n", encoding="utf-8"
	)
	print(json.dumps(result, indent=2))


if __name__ == "__main__":
	main()
