"""Render and export the unique owner-review v2 Resolve project."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE.parent))

from resolve_bridge_client import ResolveBridgeClient  # noqa: E402
from otter_recut_v2_plan import PROJECT_NAME  # noqa: E402


OUTPUT_STEM = "mermaid_roshan_otter_wing_recut_v2_resolve"


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def main() -> None:
	client = ResolveBridgeClient()
	if client.request("health")["current_project"] != PROJECT_NAME:
		raise RuntimeError("Wrong active project")
	output = PACKAGE / f"{OUTPUT_STEM}.mp4"
	archive = PACKAGE / "Mermaid_Roshan_Otter_Wing_Recut_2026-08-23_v1.drp"
	for path in (output, archive):
		if path.exists():
			raise RuntimeError(f"Refusing to overwrite {path}")
	client.call("DeleteAllRenderJobs", target="project")
	if not client.call("SetCurrentRenderFormatAndCodec", "mp4", "H264", target="project"):
		raise RuntimeError("Resolve declined H.264")
	settings = {"TargetDir": str(PACKAGE), "CustomName": OUTPUT_STEM, "SelectAllFrames": True, "ExportVideo": True, "ExportAudio": True, "FormatWidth": 1280, "FormatHeight": 720, "FrameRate": 24, "AudioCodec": "aac", "AudioSampleRate": 48000}
	if not client.call("SetRenderSettings", settings, target="project"):
		raise RuntimeError("Resolve declined render settings")
	job_id = client.call("AddRenderJob", target="project")
	if not job_id or not client.call("StartRendering", job_id, target="project"):
		raise RuntimeError("Resolve did not start rendering")
	deadline = time.monotonic() + 600
	while client.call("IsRenderingInProgress", target="project"):
		if time.monotonic() > deadline:
			raise TimeoutError("Resolve render exceeded ten minutes")
		time.sleep(1)
	status = client.call("GetRenderJobStatus", job_id, target="project")
	if status.get("JobStatus") != "Complete" or not output.is_file():
		raise RuntimeError(f"Resolve render failed: {status}")
	client.call("SaveProject", target="project_manager")
	if not client.call("ExportProject", PROJECT_NAME, str(archive), False, target="project_manager"):
		raise RuntimeError("Resolve project export failed")
	result = {"render_job": status, "video": str(output), "video_sha256": sha256(output), "project_archive": str(archive), "project_archive_sha256": sha256(archive)}
	(PACKAGE / "resolve_render_result_v2.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(result, indent=2))


if __name__ == "__main__":
	main()
