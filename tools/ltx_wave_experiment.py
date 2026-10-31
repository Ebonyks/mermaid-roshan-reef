#!/usr/bin/env python3
"""Bounded, independently reviewed Comfy/LTX experiment stages.

Consumes prebuilt workflows; never invents prompts, pixels, a third take or an
acceptance verdict. Every invocation that reaches reservation consumes the
shared campaign budget, including preflight failures and refinement stages.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCHEMA = "reef.ltx-stage-review.v1"
PRIVATE_PARTS = {".secrets", ".git", ".codex", ".aws", ".ssh"}
STAGES = {"first-pass", "refine", "single"}
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$")


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_name(path.name + ".next")
    try:
        staging.write_bytes((json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8"))
        staging.replace(path)
    finally:
        staging.unlink(missing_ok=True)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_name(value: str) -> str:
    if not isinstance(value, str) or not NAME.fullmatch(value) or value in {".", ".."}:
        raise ValueError("Invalid single-component artifact/method name")
    return value


def project_path(root: Path, value: str | Path, output: bool = False) -> Path:
    value = str(value).replace("\\", "/")
    path = (root / value).resolve()
    try:
        relative = path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Path leaves the project") from error
    if any(part.lower() in PRIVATE_PARTS for part in relative.parts) or path.suffix.lower() in {".jks", ".keystore"}:
        raise ValueError("Private/internal paths are forbidden")
    if output and (relative.parts[:2] != ("assets_src", "animation") or len(relative.parts) < 3):
        raise ValueError("Experiment outputs must stay under assets_src/animation/")
    return path


def relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def pin(root: Path, entry: dict) -> Path:
    path = project_path(root, entry["path"])
    expected = entry.get("sha256")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected) or not path.is_file() or sha(path) != expected:
        raise ValueError(f"Missing or changed pinned file: {entry.get('path')}")
    return path


def runtime_path(runtime: Path, value: str, lane: str) -> Path:
    # Comfy returns Windows separators even when the client is on another OS.
    if any(part.lower() in PRIVATE_PARTS for part in runtime.resolve().parts):
        raise ValueError("Private/internal runtime paths are forbidden")
    path = (runtime / value.replace("\\", "/")).resolve()
    anchor = (runtime / lane).resolve()
    try:
        parts = path.relative_to(anchor).parts
    except ValueError as error:
        raise ValueError(f"Runtime path escapes {lane}/") from error
    if not parts or any(part.lower() in PRIVATE_PARTS for part in parts) or path.suffix.lower() in {".jks", ".keystore"}:
        raise ValueError("Private or empty runtime artifact path")
    return path


@contextmanager
def campaign_lock(job_path: Path):
    lock = job_path.with_name(job_path.name + ".lock")
    try:
        with lock.open("x", encoding="utf-8"):
            pass
    except FileExistsError as error:
        raise ValueError("Campaign is in use; no concurrent reservation") from error
    try:
        yield
    finally:
        lock.unlink()


def reserve(root: Path, job_path: Path, method: str, stage: str, output: Path) -> dict:
    safe_name(method)
    if stage not in STAGES:
        raise ValueError("Unknown experiment stage")
    if output.exists():
        raise ValueError("Output already exists; preserve it and choose a new attempt path")
    with campaign_lock(job_path):
        job = read_json(job_path)
        limits = job["limits"]
        per_method = limits["takes_per_changed_method"]
        campaign_max = limits["new_transformer_takes_max"]
        minutes = limits["wall_minutes_per_gpu_take"]
        if any(type(v) is not int or v < 1 for v in (per_method, campaign_max)) or per_method > 2 or campaign_max > 10:
            raise ValueError("Campaign limits exceed two attempts per method or ten per campaign")
        if type(minutes) not in (int, float) or not math.isfinite(minutes) or not 0 < minutes <= 20:
            raise ValueError("Wall cap must be positive and at most twenty minutes")
        if method not in {entry["id"] for entry in job["methods"]}:
            raise ValueError("Method is absent from the commissioned job")
        attempts = job.setdefault("attempts", [])
        if not isinstance(attempts, list):
            raise ValueError("Campaign attempt ledger is invalid")
        # Count every reservation, regardless of failure, pending state or stage.
        if len(attempts) >= campaign_max:
            raise ValueError("Campaign attempt cap exhausted")
        if sum(entry.get("method") == method for entry in attempts) >= per_method:
            raise ValueError("Method attempt cap exhausted; diagnose and change method")
        reservation = {"id": str(uuid.uuid4()), "method": method, "stage": stage,
                       "status": "RESERVED", "reserved_at_utc": utc(),
                       "output": relative(root, output), "wall_seconds_max": minutes * 60,
                       "counted_as_transformer_take": True}
        attempts.append(reservation)
        write_json(job_path, job)
    output.mkdir(parents=True, exist_ok=False)
    return reservation


def update_reservation(job_path: Path, attempt: dict, receipt: dict) -> None:
    with campaign_lock(job_path):
        job = read_json(job_path)
        found = [entry for entry in job["attempts"] if entry["id"] == attempt["id"]]
        if len(found) != 1:
            raise ValueError("Reserved attempt is missing/duplicated")
        found[0].update(status=receipt["status"], ended_at_utc=receipt["ended_at_utc"],
                        prompt_id=receipt.get("prompt_id"), elapsed_seconds=receipt["elapsed_seconds"],
                        receipt_sha256=receipt["receipt_sha256"])
        write_json(job_path, job)


class ComfyClient:
    def __init__(self, endpoint: str):
        parsed = urllib.parse.urlsplit(endpoint)
        if parsed.scheme != "http" or parsed.username or parsed.password or parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
            raise ValueError("Endpoint must be an ordinary localhost HTTP origin")
        host = parsed.hostname
        try:
            local = host == "localhost" or ipaddress.ip_address(host or "").is_loopback
        except ValueError:
            local = False
        if not local:
            raise ValueError("Only localhost Comfy endpoints are allowed")
        self.endpoint = endpoint.rstrip("/")
        # Disable environmental proxies so localhost cannot be routed elsewhere.
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def request(self, path: str, data: dict | None = None) -> dict:
        body = None if data is None else json.dumps(data, allow_nan=False).encode("utf-8")
        request = urllib.request.Request(self.endpoint + path, data=body, headers={"Content-Type": "application/json"})
        with self.opener.open(request, timeout=30) as response:
            return json.load(response)


def assert_idle(client) -> None:
    queue = client.request("/queue")
    if "queue_running" not in queue or "queue_pending" not in queue:
        raise ValueError("Queue snapshot is incomplete")
    if queue["queue_running"] or queue["queue_pending"]:
        raise ValueError("Comfy queue has active/pending work; do not interrupt or share it")


def interrupt_owned(client, prompt_id: str | None) -> bool:
    if not prompt_id:
        return False
    queue = client.request("/queue")
    running = queue.get("queue_running", [])
    # The global interrupt endpoint is used only for our sole known running job.
    if len(running) == 1 and len(running[0]) >= 2 and running[0][1] == prompt_id:
        client.request("/interrupt", {})
        return True
    return False


def validate_graph(workflow: dict, schema: dict, outputs: dict, stage: str = "single") -> None:
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError("Empty Comfy API workflow")
    for node_id, node in workflow.items():
        if not isinstance(node_id, str) or not isinstance(node, dict) or not isinstance(node.get("inputs"), dict):
            raise ValueError("Malformed Comfy API node")
        kind = node.get("class_type")
        if kind not in schema:
            raise ValueError(f"Missing installed node: {kind}")
        needed = set(schema[kind].get("input", {}).get("required", {}))
        missing = needed - set(node["inputs"])
        if missing:
            raise ValueError(f"Node {node_id} missing required inputs: {sorted(missing)}")
        if isinstance(node["inputs"].get("filename_prefix"), str):
            prefix = node["inputs"]["filename_prefix"].replace("\\", "/")
            if prefix.startswith("/") or ":" in prefix or any(part in {"..", "."} or part.lower() in PRIVATE_PARTS for part in prefix.split("/")):
                raise ValueError("Workflow output prefix leaves the runtime output folder")
    seen = set()
    for kind in ("images", "latents"):
        entries = outputs.get(kind, [])
        if not isinstance(entries, list):
            raise ValueError("Output-node specification must use lists")
        for entry in entries:
            name = safe_name(entry["name"])
            if name in seen:
                raise ValueError("Duplicate output artifact name")
            seen.add(name)
            if str(entry["node"]) not in workflow or type(entry["count"]) is not int or entry["count"] < 1:
                raise ValueError("Output node/count is invalid")
            if kind == "images" and (not isinstance(entry.get("canvas"), list) or len(entry["canvas"]) != 2 or any(type(v) is not int or v < 1 for v in entry["canvas"])):
                raise ValueError("Native image output needs exact canvas dimensions")
    if not outputs.get("images"):
        raise ValueError("At least one exact native image output is required")
    if stage == "first-pass":
        samplers = {"SamplerCustom", "SamplerCustomAdvanced", "KSampler", "KSamplerAdvanced", "LTXVTiledFusionSampler"}
        phases = sum(node["class_type"] in samplers for node in workflow.values())
        if phases > 1 or any(node["class_type"] == "LTXVLatentUpsampler" for node in workflow.values()):
            raise ValueError("First-pass workflow must not hide an unreviewed refinement stage")


def bind_sources(root: Path, runtime: Path, manifest: dict) -> list[dict]:
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("A nonempty source manifest is required")
    if not isinstance(manifest.get("model_workflow_pins"), dict) or not manifest["model_workflow_pins"]:
        raise ValueError("Declared model/workflow revision pins are required")
    if not isinstance(manifest.get("settings"), dict) or not manifest["settings"]:
        raise ValueError("Declared method settings are required")
    result, paths = [], set()
    for entry in sources:
        source = pin(root, entry)
        if relative(root, source) in paths:
            raise ValueError("Duplicate source binding")
        paths.add(relative(root, source))
        if not isinstance(entry.get("role"), str) or not entry["role"]:
            raise ValueError("Source role is required")
        item = {**entry, "path": relative(root, source), "sha256": sha(source)}
        if "runtime_path" in entry:
            # The operator stages exact inputs before invoking the runner.
            staged = runtime_path(runtime, entry["runtime_path"], "input")
            if not staged.is_file() or sha(staged) != item["sha256"]:
                raise ValueError(f"Missing/changed actual runtime input: {entry['runtime_path']}")
            item["runtime_sha256"] = sha(staged)
        result.append(item)
    return result


def validate_refine_review(root: Path, review_path: Path | None, sources: list[dict], outputs: dict) -> dict:
    if review_path is None:
        raise ValueError("Refine requires an explicit hash-bound first-pass topology/blur review")
    review_hash = sha(review_path)
    review = read_json(review_path)
    if review.get("schema") != REVIEW_SCHEMA or review.get("reviewer_kind") != "model_observation":
        raise ValueError("Pre-refine review must be explicitly a model observation, not acceptance")
    if not review.get("reviewer") or not review.get("reviewed_at_utc"):
        raise ValueError("Pre-refine reviewer and time are required")
    if any(review.get("checks", {}).get(axis) != "PASS" for axis in ("topology", "blur")):
        raise ValueError("First-pass topology/blur did not pass; preserve it without refinement")
    artifacts = review.get("artifacts", [])
    expected_count = outputs["images"][0]["count"]
    if len(artifacts) != expected_count or [entry.get("index") for entry in artifacts] != list(range(expected_count)):
        raise ValueError("First-pass review must bind every native frame in order")
    paths = set()
    for entry in artifacts:
        path = pin(root, entry)
        if path.suffix.lower() != ".png" or path in paths:
            raise ValueError("Review needs distinct complete native PNG frames")
        paths.add(path)
        with Image.open(path) as image:
            image.verify()
    inputs = review.get("inputs", [])
    current = sorted((entry["path"], entry["sha256"]) for entry in sources)
    recorded = sorted((relative(root, pin(root, entry)), entry["sha256"]) for entry in inputs)
    if recorded != current:
        raise ValueError("Review input bindings are stale/incomplete")
    if review.get("delivery_accepted") or review.get("owner_accepted") or review.get("human_accepted"):
        raise ValueError("Model-stage observations cannot grant creative/human acceptance")
    if sha(review_path) != review_hash:
        raise ValueError("Review record changed while checking its artifacts")
    return {"path": relative(root, review_path), "sha256": review_hash,
            "reviewer_kind": "model_observation", "scope": "pre_refine_gate_only",
            "artifacts": artifacts, "inputs": inputs, "checks": review["checks"]}


def gpu_sample() -> dict:
    try:
        sample = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader,nounits"],
                                capture_output=True, text=True, timeout=10)
        if sample.returncode:
            return {"status": "UNAVAILABLE", "reason": "nvidia-smi returned nonzero"}
        cards = []
        for index, line in enumerate(sample.stdout.strip().splitlines()):
            used, utilization = line.split(",")
            cards.append({"gpu_index": index, "card_used_mib": int(used), "utilization_percent": int(utilization)})
        return {"status": "SAMPLED", "cards": cards}
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        return {"status": "UNAVAILABLE", "reason": type(error).__name__}


def collect_outputs(root: Path, runtime: Path, output: Path, history: dict, spec: dict) -> dict:
    manifest = {"schema": "reef.ltx-native-outputs.v1", "images": [], "latents": [],
                "acceptance": "NOT_REVIEWED", "human_owner_device_child_acceptance": False}
    problems = []
    for kind in ("images", "latents"):
        for entry in spec.get(kind, []):
            rows = history.get("outputs", {}).get(str(entry["node"]), {}).get(kind, [])
            if len(rows) != entry["count"]:
                problems.append(f"Node {entry['node']} {kind}: expected {entry['count']}, got {len(rows)}")
            folder = output / entry["name"]
            folder.mkdir(exist_ok=False)
            for index, row in enumerate(rows):
                try:
                    if row.get("type") != "output" or Path(row["filename"]).name != row["filename"] or "\\" in row["filename"]:
                        raise ValueError("Invalid Comfy output location/name")
                    native = runtime_path(runtime, "output/" + row.get("subfolder", "").replace("\\", "/") + "/" + row["filename"], "output")
                    suffix = ".png" if kind == "images" else ".latent"
                    if native.suffix.lower() != suffix or not native.is_file():
                        raise ValueError("Native output missing or wrong file type")
                    destination = folder / (f"{index:04d}{suffix}" if kind == "images" else f"{entry['name']}_{index:04d}{suffix}")
                    before = sha(native)
                    shutil.copyfile(native, destination)
                    if sha(destination) != before or sha(native) != before:
                        raise ValueError("Native artifact changed during preservation")
                    item = {"index": index, "node": str(entry["node"]), "path": relative(root, destination),
                            "sha256": before, "runtime_subfolder": row.get("subfolder", ""), "runtime_filename": row["filename"]}
                    if kind == "images":
                        with Image.open(destination) as image:
                            item["canvas"] = list(image.size)
                            item["mode"] = image.mode
                            image.verify()
                        if item["canvas"] != entry["canvas"]:
                            problems.append(f"Native canvas mismatch at {destination.name}: {item['canvas']}")
                    manifest[kind].append(item)
                except (KeyError, ValueError, OSError) as error:
                    problems.append(f"Node {entry['node']} artifact {index}: {error}")
    manifest["problems"] = problems
    write_json(output / "native_outputs.json", manifest)
    if problems:
        raise ValueError("; ".join(problems))
    return manifest


def run(root: Path, *, job: str, method: str, stage: str, workflow: str, sources: str,
        outputs: str, output: str, runtime: str | Path, endpoint: str = "http://127.0.0.1:8194",
        review: str | None = None, client=None, clock=time.monotonic, sleep=time.sleep,
        sample_gpu=gpu_sample, progress=print) -> dict:
    root = root.resolve()
    job_path = project_path(root, job, output=True)
    output_path = project_path(root, output, output=True)
    runtime_root = Path(runtime).resolve()
    # Reservation precedes workflow/source/queue/schema/review validation and all
    # submissions. Path/cap checks alone do not contact Comfy or alter old output.
    attempt = reserve(root, job_path, method, stage, output_path)
    start = clock()
    receipt = {"schema": "reef.ltx-stage-receipt.v1", "attempt_id": attempt["id"],
               "method": method, "stage": stage, "status": "PREFLIGHT", "started_at_utc": utc(),
               "endpoint": endpoint, "runtime": str(runtime_root), "wall_seconds_max": attempt["wall_seconds_max"],
               "job_path": relative(root, job_path), "reserved_job_sha256": sha(job_path),
               "model_pins_scope": "declared_in_source_manifest; source/runtime inputs independently byte-verified",
               "acceptance": {"artifact_free_sample": False, "human": False, "owner": False, "device": False,
                              "child": False, "runtime": False, "delivery_accepted": False}}
    memory, prompt_id, connection, history, last_progress = [], None, client, None, -30.0
    receipt_path = output_path / "receipt.json"
    def check_deadline():
        if clock() - start >= attempt["wall_seconds_max"]:
            raise TimeoutError("Twenty-minute/commissioned stage wall cap reached")
    try:
        workflow_path = project_path(root, workflow)
        sources_path = project_path(root, sources)
        outputs_path = project_path(root, outputs)
        graph, source_manifest, output_spec = read_json(workflow_path), read_json(sources_path), read_json(outputs_path)
        receipt.update(workflow_sha256=sha(workflow_path), sources_manifest_sha256=sha(sources_path), outputs_spec_sha256=sha(outputs_path))
        for source, name in ((workflow_path, "workflow.api.json"), (sources_path, "sources.json"), (outputs_path, "outputs.json")):
            shutil.copyfile(source, output_path / name)
            if sha(source) != sha(output_path / name):
                raise ValueError("Recipe changed while copying")
        if not isinstance(source_manifest, dict):
            raise ValueError("Source manifest must be a JSON object")
        receipt.update(declared_model_workflow_pins=source_manifest.get("model_workflow_pins"), settings=source_manifest.get("settings"))
        receipt["source_files"] = bind_sources(root, runtime_root, source_manifest)
        if stage == "refine":
            receipt["first_pass_review"] = validate_refine_review(root, project_path(root, review) if review else None, receipt["source_files"], output_spec)
            shutil.copyfile(project_path(root, review), output_path / "first_pass_review.json")
        connection = connection or ComfyClient(endpoint)
        assert_idle(connection)
        schema = connection.request("/object_info")
        validate_graph(graph, schema, output_spec, stage)
        write_json(output_path / "installed_node_schema.json", {entry["class_type"]: schema[entry["class_type"]] for entry in graph.values()})
        # Recheck actual inputs and idle state immediately before submitting.
        if bind_sources(root, runtime_root, source_manifest) != receipt["source_files"]:
            raise ValueError("Source inputs changed during preflight")
        if sha(workflow_path) != receipt["workflow_sha256"]:
            raise ValueError("Workflow changed during preflight")
        if sha(sources_path) != receipt["sources_manifest_sha256"] or sha(outputs_path) != receipt["outputs_spec_sha256"]:
            raise ValueError("Source/output specification changed during preflight")
        if stage == "refine" and validate_refine_review(root, project_path(root, review), receipt["source_files"], output_spec) != receipt["first_pass_review"]:
            raise ValueError("First-pass review changed during preflight")
        check_deadline()
        assert_idle(connection)
        check_deadline()
        receipt["status"] = "SUBMITTING"
        write_json(receipt_path, receipt)
        submission = connection.request("/prompt", {"prompt": graph, "client_id": attempt["id"]})
        write_json(output_path / "submission.json", submission)
        if not isinstance(submission.get("prompt_id"), str) or not submission["prompt_id"] or submission.get("node_errors"):
            raise ValueError("Comfy submission failed validation")
        prompt_id = submission["prompt_id"]
        receipt.update(status="RUNNING", prompt_id=prompt_id)
        write_json(receipt_path, receipt)
        while clock() - start < attempt["wall_seconds_max"]:
            elapsed = clock() - start
            memory.append({"elapsed_seconds": elapsed, **sample_gpu()})
            response = connection.request("/history/" + urllib.parse.quote(prompt_id, safe=""))
            if prompt_id in response:
                history = response[prompt_id]
                write_json(output_path / "history.json", history)
                check_deadline()
                if history.get("status", {}).get("status_str") != "success":
                    # Preserve any output that exists, even for a failed graph.
                    try:
                        collect_outputs(root, runtime_root, output_path, history, output_spec)
                    except ValueError:
                        pass
                    raise ValueError("Comfy execution failed; exact native history/output evidence preserved")
                collected = collect_outputs(root, runtime_root, output_path, history, output_spec)
                receipt.update(status="EXECUTION_PASS", native_outputs_sha256=sha(output_path / "native_outputs.json"),
                               image_count=len(collected["images"]), latent_count=len(collected["latents"]))
                break
            if elapsed - last_progress >= 30:
                progress(f"LTX_STAGE method={method} stage={stage} seconds={elapsed:.0f} prompt={prompt_id} memory={memory[-1].get('cards', 'unavailable')}", flush=True)
                last_progress = elapsed
            sleep(min(5, max(0, attempt["wall_seconds_max"] - (clock() - start))))
        else:
            raise TimeoutError("Twenty-minute/commissioned stage wall cap reached")
    except (Exception, KeyboardInterrupt) as error:
        status = "EXECUTION_FAIL" if prompt_id else ("SUBMISSION_UNKNOWN" if receipt["status"] == "SUBMITTING" else "PREFLIGHT_FAIL")
        receipt.update(status=status, error=str(error), error_type=type(error).__name__)
        if connection is not None and prompt_id:
            try:
                receipt["owned_job_interrupted"] = interrupt_owned(connection, prompt_id)
            except Exception as interrupt_error:
                receipt["interrupt_status"] = f"UNAVAILABLE: {type(interrupt_error).__name__}"
        raise
    finally:
        receipt.update(ended_at_utc=utc(), elapsed_seconds=clock() - start, memory_sampling_scope="periodic total-card samples; peaks may be missed")
        peaks = [card["card_used_mib"] for item in memory for card in item.get("cards", [])]
        receipt["sampled_card_peak_mib"] = max(peaks) if peaks else None
        write_json(output_path / "memory_samples.json", memory)
        write_json(receipt_path, receipt)
        update_reservation(job_path, attempt, {**receipt, "receipt_sha256": sha(receipt_path)})
        progress(f"LTX_STAGE_RESULT status={receipt['status']} seconds={receipt['elapsed_seconds']:.2f} prompt={prompt_id or 'none'}", flush=True)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["run"])
    for name in ("job", "method", "stage", "workflow", "sources", "outputs", "output"):
        parser.add_argument("--" + name, required=True, **({"choices": sorted(STAGES)} if name == "stage" else {}))
    parser.add_argument("--runtime", default=r"H:\MermaidReefTools\LocalVideo\ltx25")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8194")
    parser.add_argument("--review", help="Explicit native first-pass model-observation gate for --stage refine")
    args = vars(parser.parse_args())
    args.pop("command")
    try:
        run(ROOT, **args)
    except (ValueError, OSError, TimeoutError, KeyError) as error:
        print(f"LTX_STAGE_FAILED {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
