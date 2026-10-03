"""Dispatch one connected Candy wrapping study through the existing local video CLI. Derived from the existing Day Two FIFO worker; exact one-job schema and repository root/defaults are the only dispatcher changes.

This worker never posts prompts itself, restarts ComfyUI, cancels other jobs,
or grades outputs. Mutable receipts live in an ignored build directory.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.request import urlopen

from PIL import Image

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "project.godot").is_file())
PACKET = ROOT / "assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a5"


def now():
	return datetime.now(timezone.utc).isoformat(timespec="seconds")


def digest(path):
	return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
	part = path.with_suffix(".part")
	part.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
	part.replace(path)


def validate(packet):
	data = json.loads((packet / "MANIFEST.json").read_text(encoding="utf-8"))
	assert data["acceptance"] == "LOCAL_MOTION_REFERENCE_ONLY"
	assert data["owner_approval"] is None and data["runtime_integration"] is False
	assert len(data["jobs"]) == len({j["id"] for j in data["jobs"]}) == 1
	assert data["renderer"]["server"] == "http://127.0.0.1:8190"
	assert data["renderer"]["preset"] == "quick"
	assert data["renderer"]["settings"] == {"width":896,"height":512,"frames":41,"steps":24,"weight_dtype":"GGUF_Q4_K_S"}
	for binding in data["renderer"]["bindings"]:
		if binding.get("check_installed_bytes",True):
			assert digest(Path(binding["installed_path"])) == binding["sha256"], binding["installed_path"]
		assert digest(packet / binding["packet_path"]) == binding["sha256"]
	for job in data["jobs"]:
		assert digest(ROOT / job["source_path"]) == job["source_sha256"]
		assert digest(packet / job["input_path"]) == job["input_sha256"]
		assert digest(packet / job["prompt_path"]) == job["prompt_sha256"]
		assert job["owner_approval"] is None
		assert (packet / job["prompt_path"]).read_text(encoding="utf-8").rstrip().endswith("Sound: silence.")
		with Image.open(packet / job["input_path"]) as image:
			assert image.mode == "RGB" and image.size == (896, 512)
	assert data["jobs"][0]["id"] == "CANDY-FOLD-A5" and data["source_status"] == "STATIC_SOURCE_DRAFT_4.5_OWNER_UNASSIGNED"
	return data


def native_queue(server):
	with urlopen(server + "/queue", timeout=10) as response:
		return json.load(response)


def matching_benchmark(local_root, settings):
	paths=list((local_root / "jobs").glob("sky_*/RENDER_RECEIPT.json"))
	paths+=list((local_root / "jobs").glob("d2m_b1q_*/RENDER_RECEIPT.json"))
	for path in sorted(paths, reverse=True):
		try:
			receipt = json.loads(path.read_text(encoding="utf-8"))
			graph = json.loads(path.with_name("workflow.api.json").read_text(encoding="utf-8"))
			if (receipt.get("status") == "PASS" and receipt.get("settings") == settings
				and graph["1"]["class_type"] == "UnetLoaderGGUFAdvanced"
				and graph["1"]["inputs"]["unet_name"] == "Wan2.2-TI2V-5B-Q4_K_S.gguf"
				and graph["2"]["inputs"]["clip_name"] == "umt5-xxl-encoder-Q4_K_S.gguf"):
				return str(path)
		except (OSError, ValueError, KeyError):
			continue
	return None


def run(packet, state_dir):
	data = validate(packet)
	state_dir.mkdir(parents=True, exist_ok=True)
	# An OS-held lock prevents duplicate local workers; it releases on process exit.
	import msvcrt
	with (state_dir / "worker.lock").open("a+b") as lock:
		lock.seek(0)
		try:
			if lock.read(1) == b"":
				lock.write(b"0")
				lock.flush()
			lock.seek(0)
			msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
		except OSError:
			raise SystemExit("Day Two worker already active; no prompt submitted.")
		state_path = state_dir / "STATE.json"
		if state_path.exists():
			state = json.loads(state_path.read_text(encoding="utf-8"))
			assert state["manifest_sha256"] == digest(packet / "MANIFEST.json")
		else:
			state = {"queue_id": data["id"], "manifest_sha256": digest(packet / "MANIFEST.json"),
				"created_at_utc": now(), "acceptance": data["acceptance"],
				"jobs": [{"id": j["id"], "name": j["queue_name"], "status": "QUEUED_LOCAL_FIFO"} for j in data["jobs"]]}
		state.update(worker_pid=os.getpid(), worker_started_at_utc=now())
		def save(status, **extra):
			if status != "WAITING_FOR_LOCAL_SERVICE":
				state.pop("service_error",None)
			state.update(status=status, observed_at_utc=now(), **extra)
			write_json(state_path, state)
			print(f'{state["observed_at_utc"]} {status}', flush=True)
		server = data["renderer"]["server"]
		local_root = Path(data["renderer"]["root"])
		deadline = time.monotonic() + 12 * 3600
		for job, item in zip(data["jobs"], state["jobs"]):
			if item["status"] == "MACHINE_RENDER_PASS_PENDING_VISUAL_REVIEW":
				continue
			prior = sorted((local_root / "jobs").glob(job["queue_name"] + "_*/RENDER_RECEIPT.json"))
			if prior:
				# A submitted run is never silently regenerated after a worker restart.
				receipt = json.loads(prior[-1].read_text(encoding="utf-8"))
				item.update(receipt_path=str(prior[-1]), native_prompt_id=receipt.get("prompt_id"))
				if receipt.get("status") == "PASS":
					item.update(status="MACHINE_RENDER_PASS_PENDING_VISUAL_REVIEW", outputs=receipt.get("outputs", []))
					save("DISPATCHING")
					continue
				item["status"] = "PRIOR_SUBMISSION_REQUIRES_RECOVERY"
				save("STOPPED_NO_DUPLICATE_SUBMISSION")
				return 2
			idle_since = None
			while True:
				if time.monotonic() > deadline:
					save("WAIT_TIMEOUT_NO_OTHER_JOB_CANCELLED")
					return 2
				try:
					benchmark = matching_benchmark(local_root, data["renderer"]["settings"])
					if not benchmark and job["id"] != "D2A-0394":
						idle_since = None
						save("WAITING_FOR_MATCHING_QUANTIZED_BENCHMARK")
						time.sleep(30)
						continue
					state["matching_benchmark_receipt"] = benchmark
					state["calibration_first_study"] = not bool(benchmark)
					queue = native_queue(server)
					active = [x[1] for x in queue.get("queue_running", [])]
					pending = [x[1] for x in queue.get("queue_pending", [])]
					if active or pending:
						idle_since = None
						save("WAITING_FOR_EXISTING_COMFY_JOBS", existing_prompt_ids=active + pending)
					elif idle_since is None:
						idle_since = time.monotonic()
						save("WAITING_FOR_QUIET_IDLE_WINDOW", existing_prompt_ids=[])
					elif time.monotonic() - idle_since >= 90:
						break
					else:
						save("WAITING_FOR_QUIET_IDLE_WINDOW", existing_prompt_ids=[])
				except (OSError, ValueError) as error:
					idle_since = None
					save("WAITING_FOR_LOCAL_SERVICE", service_error=str(error))
				time.sleep(30)
			validate(packet)  # Changed installation/inputs block submission.
			command = [data["renderer"]["python"], "-s", "-B", str(packet / data["renderer"]["entrypoint"]),
				"--preset", data["renderer"]["preset"], "--image", str(packet / job["input_path"]),
				"--prompt-file", str(packet / job["prompt_path"]), "--name", job["queue_name"], "--seed", str(job["seed"])]
			with (state_dir / (job["id"] + ".log")).open("ab", buffering=0) as log:
				process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
				item.update(status="LOCAL_RENDERER_STARTING", child_pid=process.pid, started_at_utc=now())
				save("RENDERER_ACTIVE")
				while process.poll() is None:
					receipts = sorted((local_root / "jobs").glob(job["queue_name"] + "_*/RENDER_RECEIPT.json"))
					if receipts:
						try:
							receipt = json.loads(receipts[-1].read_text(encoding="utf-8"))
							item.update(receipt_path=str(receipts[-1]), native_prompt_id=receipt.get("prompt_id"), status=receipt.get("status"))
						except ValueError:
							pass  # Existing CLI writes receipts in place.
						save("RENDERER_ACTIVE")
					time.sleep(10)
				receipts = sorted((local_root / "jobs").glob(job["queue_name"] + "_*/RENDER_RECEIPT.json"))
				if not receipts or process.returncode != 0:
					item.update(status="STOPPED_RENDERER_FAILURE", exit_code=process.returncode)
					save("STOPPED_FOR_REVIEW_NO_AUTOMATIC_REGENERATION")
					return 2
				receipt = json.loads(receipts[-1].read_text(encoding="utf-8"))
				assert receipt["status"] == "PASS"
				assert receipt["source_sha256"] == job["input_sha256"]
				# The deployed CLI hashes read_text() content; Windows CRLF is
				# normalized to LF there. The manifest separately pins file bytes.
				consumed_prompt = (packet / job["prompt_path"]).read_text(encoding="utf-8")
				assert receipt["prompt_sha256"] == hashlib.sha256(consumed_prompt.encode("utf-8")).hexdigest()
				item.update(status="MACHINE_RENDER_PASS_PENDING_VISUAL_REVIEW", finished_at_utc=now(),
					receipt_path=str(receipts[-1]), native_prompt_id=receipt["prompt_id"], outputs=receipt.get("outputs", []))
				save("DISPATCHING")
			save("ALL_MACHINE_RENDERS_DONE_VISUAL_REVIEW_PENDING")
		return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--packet", type=Path, default=PACKET)
	parser.add_argument("--state-dir", type=Path, default=ROOT / "build/candy_local_fold_a5_active_20261003")
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	if args.check:
		validate(args.packet.resolve())
		print("CANDY_LOCAL_MOTION|PASS|1 exact source/input/prompt binding; pinned current installed workflow; candidate static floor4.5; reference-only")
	else:
		raise SystemExit(run(args.packet.resolve(), args.state_dir.resolve()))
