"""Submit a local motion-reference job and preserve its source/output provenance."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

import requests
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_workflows import ROOT, PRESETS, POSITIVE, api_graph

URL = "http://127.0.0.1:8189"
FFMPEG = Path(r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe")
FFPROBE = FFMPEG.with_name("ffprobe.exe")


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=PRESETS, default="quick")
    parser.add_argument("--image", type=Path, default=ROOT / "input" / "neutral_calibration.png")
    parser.add_argument("--prompt", default=POSITIVE)
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--seed", type=int, default=20260930)
    parser.add_argument("--name", default="motion_study")
    parser.add_argument("--wait-for-models", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.name):
        parser.error("Name must use 1–64 letters, numbers, underscores or hyphens")
    if args.wait_for_models:
        deadline = time.monotonic() + 7200
        while not (ROOT / "MODEL_RECEIPT.json").exists():
            if time.monotonic() > deadline:
                raise TimeoutError("Model verification has not completed")
            print("Waiting for verified model downloads...", flush=True)
            time.sleep(30)
    if not (ROOT / "MODEL_RECEIPT.json").exists():
        raise RuntimeError("Run download_models.py first; verified model receipt is missing")
    requests.get(URL + "/system_stats", timeout=10).raise_for_status()
    queue = requests.get(URL + "/queue", timeout=10).json()
    if queue.get("queue_running") or queue.get("queue_pending"):
        raise RuntimeError("ComfyUI has another job; wait until its queue is idle")
    source = args.image.resolve(strict=True)
    if source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        parser.error("Source must be a PNG, JPEG or WebP image")
    with Image.open(source) as source_image:
        source_dimensions = list(source_image.size)
        source_image.verify()
    source_hash = file_hash(source)
    staged_name = f"source_{source_hash[:16]}{source.suffix.lower()}"
    staged = ROOT / "input" / staged_name
    if source != staged:
        if staged.exists() and file_hash(staged) != source_hash:
            raise RuntimeError("Staged source hash conflict")
        if not staged.exists():
            shutil.copyfile(source, staged)
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    job_name = f"{args.name}_{stamp}_{uuid.uuid4().hex[:6]}"
    job = ROOT / "jobs" / job_name
    job.mkdir(parents=True)
    graph = api_graph(args.preset, staged_name, prompt, args.seed, f"local_reference/{job_name}")
    receipt = {
        "status": "SUBMITTING", "acceptance": "LOCAL_MOTION_REFERENCE_ONLY",
        "source": str(source), "source_sha256": source_hash,
        "source_dimensions": source_dimensions,
        "prompt": prompt, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "preset": args.preset, "settings": PRESETS[args.preset], "seed": args.seed,
        "model_receipt": "H:/MermaidReefTools/LocalVideo/MODEL_RECEIPT.json",
        "workflow_sha256": hashlib.sha256(json.dumps(graph, sort_keys=True).encode()).hexdigest(),
        "started_at_utc": stamp,
    }
    manifest = job / "RENDER_RECEIPT.json"
    (job / "workflow.api.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    manifest.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    response = requests.post(URL + "/prompt", json={"prompt": graph, "client_id": job_name}, timeout=30)
    if not response.ok:
        receipt.update(status="VALIDATION_FAILED", error=response.text)
        manifest.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        raise RuntimeError(response.text)
    prompt_id = response.json()["prompt_id"]
    receipt.update(status="RUNNING", prompt_id=prompt_id)
    manifest.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Submitted {args.preset}: {prompt_id}. Receipt: {manifest}", flush=True)
    started = time.monotonic()
    last_report = 0
    while True:
        time.sleep(5)
        history = requests.get(URL + f"/history/{prompt_id}", timeout=30).json()
        if prompt_id in history:
            result = history[prompt_id]
            (job / "COMFY_HISTORY.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            if result.get("status", {}).get("status_str") != "success":
                receipt.update(status="FAILED", result=result.get("status"))
                manifest.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
                raise RuntimeError(f"Render failed; inspect {manifest}")
            files = []
            for output in result.get("outputs", {}).values():
                for key in ("videos", "images", "gifs"):
                    for item in output.get(key, []):
                        candidate = (ROOT / "output" / item.get("subfolder", "") / item["filename"]).resolve()
                        if not candidate.is_relative_to((ROOT / "output").resolve()):
                            raise RuntimeError("Unexpected output path")
                        if candidate.exists():
                            files.append(candidate)
            files = list(dict.fromkeys(files))
            if not files:
                raise RuntimeError("Job reports success but its output file is missing")
            outputs = []
            for path in files:
                outputs.append({"path": str(path), "sha256": file_hash(path), "bytes": path.stat().st_size})
                if path.suffix == ".webm":
                    mp4 = path.with_suffix(".mp4")
                    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-n", "-i", str(path),
                                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", str(mp4)], check=True)
                    outputs.append({"path": str(mp4), "sha256": file_hash(mp4), "bytes": mp4.stat().st_size})
                    probe = subprocess.run([str(FFPROBE), "-v", "error", "-count_frames",
                        "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,codec_name",
                        "-show_entries", "format=duration", "-of", "json", str(mp4)],
                        check=True, capture_output=True, text=True)
                    outputs[-1]["media"] = json.loads(probe.stdout)
                    stream = outputs[-1]["media"]["streams"][0]
                    if (stream["width"], stream["height"], int(stream["nb_read_frames"])) != (
                            PRESETS[args.preset]["width"], PRESETS[args.preset]["height"], PRESETS[args.preset]["frames"]):
                        raise RuntimeError("Encoded video does not preserve expected native dimensions/frame count")
            receipt.update(status="PASS", outputs=outputs, elapsed_seconds=round(time.monotonic()-started, 2),
                           completed_at_utc=datetime.now(timezone.utc).isoformat(),
                           limitation="Machine execution only; no cinematic, game, owner or device acceptance")
            manifest.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
            requests.post(URL + "/free", json={"unload_models": True, "free_memory": True}, timeout=30).raise_for_status()
            print(f"PASS in {receipt['elapsed_seconds']} seconds. Output: {outputs[-1]['path']}", flush=True)
            return
        elapsed = time.monotonic() - started
        if elapsed - last_report >= 30:
            print(f"Rendering {args.preset}: {elapsed:.0f} seconds elapsed", flush=True)
            last_report = elapsed
        if elapsed > 7200:
            raise TimeoutError("Render is still queued/running; its prompt ID is saved in the receipt")


if __name__ == "__main__":
    main()
