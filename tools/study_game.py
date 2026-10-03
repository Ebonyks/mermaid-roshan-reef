#!/usr/bin/env python3
"""Collect advisory game-study evidence and render a reproducible report from JSON.

Never launches a capture, writes art, changes finding lifecycles, or reads child
device data. Sensor failures are evidence; a successful collection is not game
acceptance. Remote CI is read at the exact studied head; --offline names the gap.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

try:
    from tools import measure_loop_health as health
except ModuleNotFoundError:
    import measure_loop_health as health

SCHEMA_VERSION = 1
SAFE_ROOTS = {"scripts", "scenes", "design", "audit", "docs", "tools", "assets", "assets_src", ".github"}
RESULT_RE = re.compile(r"(?:RESULT\s*\|\s*|result:\s*)(PASS|FAIL(?:ED)?|MEASURED|EMPTY|CAPPED|NOT_MEASURED|ALL OK|\d+ FAILED)", re.I)
BAD_RE = re.compile(r"\b(?:FAIL(?:ED)?|CAPPED|NOT_MEASURED|timeout|timed out)\b|verdict=capped|no files (?:were )?found|no files to upload", re.I)
SENSORS = {
    "game_2d": ["tools/audit_game_2d.py"],
    "typography": ["tools/audit_typography.py", "--json", "--check"],
    "visual_profile": ["tools/audit_visual_design.py", "--format", "json", "--no-report"],
    "document_authority": ["tools/audit_document_authority.py"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def safe_relative(root: Path, value: str) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    value = value.removeprefix("res://").replace("\\", "/")
    relative = Path(value)
    if relative.is_absolute() or ":" in value or ".." in relative.parts:
        return None
    if any(p.lower() in {".secrets", ".git"} for p in relative.parts) or relative.suffix.lower() in {".keystore", ".jks"}:
        return None
    try:
        path = (root / relative).resolve()
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def execute(root: Path, command: list[str], timeout: float = 60, max_output: int = 200_000,
            input_text: str | None = None) -> dict:
    """Disk-backed output, timeout, exact hash, and bounded display; shell never used."""
    result: dict[str, Any] = {"command": command, "status": "NOT_MEASURED", "exit_code": None}
    with tempfile.TemporaryFile() as output:
        try:
            process = subprocess.run(command, cwd=root, input=input_text.encode() if input_text is not None else None,
                                     stdout=output, stderr=subprocess.STDOUT, check=False, timeout=timeout)
            result["exit_code"] = process.returncode
        except subprocess.TimeoutExpired:
            result["reason"] = f"Sensor exceeded {timeout:g}-second cap"
            result["status"] = "TIMEOUT"
        except OSError as error:
            result["reason"] = str(error)
            result["status"] = "UNAVAILABLE"
        output.seek(0)
        digest = hashlib.sha256()
        chunks = []
        size = 0
        kept = 0
        while chunk := output.read(65536):
            digest.update(chunk)
            size += len(chunk)
            if kept < max_output:
                piece = chunk[:max_output - kept]
                chunks.append(piece)
                kept += len(piece)
        text = b"".join(chunks).decode("utf-8", errors="replace")
        result.update(output=text, output_sha256=digest.hexdigest(), output_bytes=size,
                      truncated=size > max_output)
        # Preserve every explicit advisory result line even beyond the display cap.
        output.seek(0)
        lines = []
        omitted = 0
        for raw in output:
            line = raw.decode("utf-8", errors="replace").strip()
            if RESULT_RE.search(line) or "verdict=" in line or "if-no-files-found" not in line and BAD_RE.search(line):
                if len(lines) < 2000:
                    lines.append(line[:2000])
                else:
                    omitted += 1
        result.update(result_lines=lines, omitted_result_lines=omitted)
    if result["exit_code"] is not None:
        if result["exit_code"] != 0:
            result["status"] = "FAIL"
            result["reason"] = "Nonzero sensor exit"
        elif not text.strip():
            result["status"] = "EMPTY"
            result["reason"] = "Sensor produced no output"
        elif result["truncated"]:
            result["status"] = "TRUNCATED"
            result["reason"] = "Display output cap reached; no complete JSON summary inferred"
        else:
            result["status"] = "MEASURED"
    return result


def git_result(root: Path, *args: str, timeout: float = 30) -> dict:
    return execute(root, ["git", *args], timeout)


def git_text(root: Path, *args: str, timeout: float = 30) -> str:
    result = git_result(root, *args, timeout=timeout)
    if result["exit_code"] != 0 or result["truncated"]:
        raise ValueError(f"Git measurement unavailable: {' '.join(args)}; {result.get('reason', '')}")
    return result["output"]


def advisory_status(text: str, conclusion: str | None = None) -> tuple[str, str]:
    if re.search(r"\bCAPPED\b|verdict=capped", text, re.I):
        return "CAPPED", "At least one simulation reached its cap"
    if re.search(r"RESULT\s*\|\s*(?:NOT_MEASURED|EMPTY)\b", text, re.I):
        return "NOT_MEASURED", "Advisory explicitly reports empty or unmeasured evidence"
    if BAD_RE.search(text):
        return "FAIL", "Failure, timeout, empty artifact or NOT_MEASURED appears in advisory output"
    if conclusion and conclusion not in {"success", "neutral", "skipped"}:
        return "FAIL", f"CI step conclusion: {conclusion}"
    if conclusion == "skipped":
        return "NOT_MEASURED", "CI skipped the advisory step"
    terminal = RESULT_RE.findall(text)
    if terminal and all(t.upper() in {"PASS", "MEASURED", "ALL OK"} for t in terminal):
        return "MEASURED", "Explicit terminal result recorded; no human acceptance inferred"
    return "NOT_MEASURED", "No explicit terminal result in the advisory log"


def sensor_summary(name: str, result: dict) -> dict:
    if result["truncated"]:
        return {}
    text = result["output"]
    if name == "game_2d":
        return {"counts": {k: int(v) for k, v in re.findall(r"\b([a-z0-9_]+)=(\d+)", text)},
                "status": next(iter(re.findall(r"GAME2D\| STATUS\|\s*(\S+)", text)), "NOT_MEASURED")}
    try:
        data = json.loads(text)
    except ValueError:
        if name in {"typography", "visual_profile"}:
            result["status"] = "FAIL"
            result["reason"] = "Expected JSON sensor output was not valid JSON"
        return {"result_lines": result["result_lines"]}
    if name == "visual_profile" and isinstance(data, list):
        counts = dict(sorted(collections.Counter(str(row.get("severity", "UNCLASSIFIED"))
                                                for row in data if isinstance(row, dict)).items()))
        return {"status": "FINDINGS_RECORDED" if data else "NO_FINDINGS_RECORDED",
                "findings": len(data), "severity_counts": counts,
                "limit": "Static/saved diagnostic facts only; no fresh captures or visual/device acceptance"}
    if not isinstance(data, dict):
        result["status"] = "FAIL"
        result["reason"] = "Sensor output has unsupported JSON shape"
        return {}
    if name == "typography":
        return {"status": data.get("status"), "label3d": data.get("label3d"),
                "glyph_classification_counts": data.get("glyphs", {}).get("classification_counts"),
                "unclassified_glyphs": data.get("glyphs", {}).get("unclassified"),
                "font_coverage_status": data.get("font", {}).get("coverage_status"),
                "machine_errors": data.get("machine_errors", [])}
    return data


def run_sensors(root: Path, timeout: float, skip: bool, max_output: int) -> dict:
    def run_one(name: str, arguments: list[str]) -> dict:
        command = [sys.executable, "-B", str(root / arguments[0]), *arguments[1:]]
        if skip:
            return {"status": "NOT_MEASURED", "command": command,
                    "reason": "Explicit --skip-sensors", "summary": {}}
        if not (root / arguments[0]).is_file():
            return {"status": "UNAVAILABLE", "command": command,
                    "reason": "Sensor script missing", "summary": {}}
        result = execute(root, command, timeout, max_output)
        result["summary"] = sensor_summary(name, result)
        return result

    # Independent read-only sensors share no outputs and have individual caps.
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = {name: pool.submit(run_one, name, arguments) for name, arguments in SENSORS.items()}
        return {name: future.result() for name, future in pending.items()}


def live_status(root: Path) -> dict:
    scripts = sorted((root / "scripts").rglob("*.gd"))
    result: dict[str, Any] = {"production_scripts": sum(not p.name.startswith("probe") for p in scripts),
                              "probe_scripts": sum(p.name.startswith("probe") for p in scripts), "sources": []}
    for filename, key in (("tools/godot_baseline.json", "engine"),):
        try:
            data = json.loads(read_text(root / filename))
            result[key] = {k: data.get(k) for k in ("version", "release", "official_build")}
            result["sources"].append(filename)
        except (OSError, ValueError):
            result[key] = {"status": "NOT_MEASURED", "reason": "Baseline absent or invalid"}
    opera = root / "scripts/opera_house.gd"
    if opera.exists():
        text = read_text(opera)
        match = re.search(r"const LIVE_ACT_INDICES[^=]*=\s*\[([^]]+)\]", text)
        result["opera_live_act_indices"] = [int(n) for n in re.findall(r"\d+", match[1])] if match else None
        result["opera_active_careers"] = len(result["opera_live_act_indices"]) if match else None
        result["sources"].append("scripts/opera_house.gd")
    world = root / "scripts/opera_career_world_2d.gd"
    if world.exists():
        text = read_text(world)
        match = re.search(r"const PHASES\s*:=\s*\{(.*?)\n\}", text, re.S)
        if match:
            rows = re.findall(r'"mode"\s*:\s*"([^"]+)"', match[1])
            result.update(opera_declared_phases=len(rows), opera_declared_modes=sorted(set(rows)))
            result["phase_count_scope"] = "Literal PHASES entries, not dynamic specialist lesson expansion"
        else:
            result["phase_count_scope"] = "NOT_MEASURED: PHASES source layout not recognized"
        result["sources"].append("scripts/opera_career_world_2d.gd")
    result["surfaces"] = [{"id": name, "source": source, "present": (root / source).is_file(),
                            "acceptance": "NOT_MEASURED", "reason": "Source inventory is not runtime/device/child review"}
                           for name, source in (("Day One", "scripts/day_one_director.gd"),
                                                ("Grand Puff", "scripts/games/dust_boss.gd"),
                                                ("Day Two", "scripts/chapter_two_director.gd"),
                                                ("Opera careers", "scripts/opera_career_world_2d.gd"),
                                                ("Sky Lagoon", "scripts/arena/sky_lagoon_promenade.gd"),
                                                ("Castle rooms", "scripts/arena/castle_rooms_25d.gd"),
                                                ("Roshan movement", "scripts/player.gd"),
                                                ("Companions", "scripts/companion.gd"),
                                                ("Touch controls", "scripts/touch_ui.gd"),
                                                ("Pause and settings", "scripts/pause_menu.gd"),
                                                ("Wardrobe", "scripts/wardrobe_ui.gd"),
                                                ("Craft studio", "scripts/craft_studio.gd"),
                                                ("Teacher", "scripts/opera_teacher_surface.gd"),
                                                ("Geologist", "scripts/opera_geology_surface.gd"))]
    return result


def collect_impacts(root: Path, timeout: float) -> dict:
    result = {key: [] for key in ("records", "lessons", "pending", "failed", "strengths_observed", "owner_corrections", "references_used", "errors")}
    last_changes = {}
    current_sha = None
    for line in git_text(root, "log", "--format=COMMIT:%H", "--name-only", "--", "design/audit_impacts", timeout=timeout).splitlines():
        if line.startswith("COMMIT:"):
            current_sha = line[7:]
        elif line.startswith("design/audit_impacts/") and line not in last_changes:
            last_changes[line] = current_sha
    for path in sorted((root / "design/audit_impacts").glob("*.json")):
        relative = path.relative_to(root).as_posix()
        try:
            record = json.loads(read_text(path))
            if not isinstance(record, dict):
                raise ValueError("Impact record is not an object")
        except (OSError, ValueError) as error:
            result["errors"].append({"path": relative, "reason": str(error)})
            continue
        base = {"record": relative, "id": record.get("id"), "last_changed_head": last_changes.get(relative)}
        result["records"].append({**base, "scope": record.get("scope"), "baseline": record.get("baseline"),
                                  "files": record.get("files", []), "findings": record.get("findings", []),
                                  "acceptance_gaps": record.get("acceptance_gaps"), "validation": record.get("validation", []),
                                  "lessons": record.get("lessons", [])})
        for key in ("lessons", "strengths_observed", "owner_corrections", "references_used"):
            values = record.get(key, [])
            if not isinstance(values, list):
                result["errors"].append({**base, "reason": f"{key} is not an array"})
                continue
            for value in values:
                row = {**base, "value": value}
                if key == "lessons":
                    row["write_back_missing"] = not isinstance(value, dict) or not value.get("write_back")
                result[key].append(row)
        for validation in record.get("validation", []):
            if isinstance(validation, dict) and validation.get("result") in {"PENDING", "FAIL"}:
                result["pending" if validation["result"] == "PENDING" else "failed"].append({**base, **validation})
    return result


def changed_findings(root: Path, records: dict, dirty_paths: list[str], timeout: float) -> list[dict]:
    history = {}
    current_date = None
    dates = [d for fields in records.values() for d in health.DATE.findall(fields.get("history", ""))]
    if not dates:
        return [{"status": "NOT_MEASURED", "reason": "No finding history dates"}]
    path_re = re.compile(r"(?:res://)?(?:scripts|scenes|tools|design|audit|assets|assets_src|docs|\.github)/[A-Za-z0-9_. /-]+?\.[A-Za-z0-9]+")
    referenced = sorted(set(value.removeprefix("res://") for fields in records.values()
                            for value in path_re.findall(" ".join(fields.get(k, "") for k in ("evidence", "reproduction", "source", "fix")))
                            if safe_relative(root, value) is not None))
    if not referenced:
        return []
    for line in git_text(root, "log", f"--since={min(dates)}T00:00:00", "--format=DATE:%cs", "--name-only", "--", *referenced, timeout=timeout).splitlines():
        if line.startswith("DATE:"):
            current_date = line[5:]
        elif line and current_date and line not in history:
            history[line] = current_date
    rows = []
    for finding_id, fields in records.items():
        if any(f"`{s}`" in fields.get("lifecycle", "") for s in health.TERMINAL):
            continue
        last = max(health.DATE.findall(fields.get("history", "")), default=None)
        paths = set(path_re.findall(" ".join(fields.get(k, "") for k in ("evidence", "reproduction", "source", "fix"))))
        changed = []
        for value in sorted(paths):
            path = safe_relative(root, value)
            if path is None:
                continue
            relative = path.relative_to(root.resolve()).as_posix()
            date = history.get(relative)
            if relative in dirty_paths or date and last and date > last:
                changed.append({"path": relative, "latest_change_date": date, "working_tree_change": relative in dirty_paths})
        if changed:
            rows.append({"id": finding_id, "last_history": last, "files": changed,
                         "action": "Recheck finding; source change alone does not establish repair or regression"})
    return rows


def motion_studies(root: Path, impacts: dict) -> list[dict]:
    rows = []
    for record in impacts["records"]:
        text = str(record.get("scope", ""))
        files = record.get("files", [])
        candidate_files = [str(p) for p in files if str(p).startswith("assets_src/cinematics/")]
        if not candidate_files or not re.search(r"motion|animation|audition|swing|scull", text + " ".join(candidate_files), re.I):
            continue
        kind = "object" if re.search(r"swing|seesaw|object.motion|ten.object", text + " ".join(candidate_files), re.I) else "character"
        verdicts = [v for v in record.get("validation", []) if isinstance(v, dict) and re.search(r"owner|child|human", str(v.get("command", "")), re.I)]
        rows.append({"id": record["id"], "kind": kind, "record": record["record"],
                     "scope": text, "owner_verdicts": verdicts,
                     "verdict_scope": "Only the referenced candidate/action; missing review is not acceptance",
                     "acceptance_gaps": record.get("acceptance_gaps")})
    return rows


def library_delta(root: Path) -> dict:
    folder = root / "audit/day2_art_library_2026-09-30"
    try:
        inventory = json.loads(read_text(folder / "inventory.json"))
        recorded_delta = json.loads(read_text(folder / "refresh_delta.json"))
    except (OSError, ValueError) as error:
        return {"status": "NOT_MEASURED", "reason": str(error)}
    changed = []
    missing = []
    for relative, expected in inventory.get("watched_sources", {}).items():
        path = safe_relative(root, relative)
        if path is None or not path.is_file():
            missing.append(relative)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            changed.append(relative)
    items = inventory.get("items", [])
    stale = []
    for item in items:
        if not isinstance(item, dict):
            continue
        relative = item.get("path", "")
        path = safe_relative(root, relative)
        if path is None or not path.is_file():
            stale.append({"path": relative, "reason": "missing"})
        elif item.get("sha256") and hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            stale.append({"path": relative, "reason": "hash changed"})
    return {"status": "MEASURED", "inventory": "audit/day2_art_library_2026-09-30/inventory.json",
            "source_revision": inventory.get("source_revision"), "items": len(items),
            "recorded_refresh_delta": recorded_delta, "changed_watched_sources": changed,
            "missing_watched_sources": missing, "stale_items": stale,
            "limit": "Existing inventory checked without generating previews; newly added art requires the library refresh workflow"}


def advisory_step_names(root: Path) -> list[str]:
    path = root / ".github/workflows/probes.yml"
    if not path.exists():
        return []
    names = []
    for block in re.split(r"(?m)^\s+- name:\s*", read_text(path))[1:]:
        if re.search(r"(?m)^\s+continue-on-error:\s*true\s*$", block):
            names.append(block.splitlines()[0].strip().strip('"\''))
    return names


def artifact_names_by_step(root: Path) -> dict[str, str]:
    path = root / ".github/workflows/probes.yml"
    if not path.exists():
        return {}
    names = {}
    for block in re.split(r"(?m)^\s+- name:\s*", read_text(path))[1:]:
        if "actions/upload-artifact@" not in block or "continue-on-error: true" not in block:
            continue
        match = re.search(r"(?m)^\s+name:\s*([^\n]+)$", block)
        if match:
            names[block.splitlines()[0].strip().strip('"\'')] = match[1].strip().strip('"\'')
    return names


def advisory_ids_by_step(root: Path) -> dict[str, str]:
    """Only uniquely declared wrapper IDs can identify an UNKNOWN STEP result."""
    path = root / ".github/workflows/probes.yml"
    if not path.exists():
        return {}
    identifiers = collections.defaultdict(set)
    for block in re.split(r"(?m)^\s+- name:\s*", read_text(path))[1:]:
        if not re.search(r"(?m)^\s+continue-on-error:\s*true\s*$", block):
            continue
        name = block.splitlines()[0].strip().strip("\"'")
        for match in re.finditer(r"run_advisory_sensor\.py[^\n]*?\s--name\s+([\"']?)([A-Za-z0-9_.-]+)\1(?:\s|$)", block):
            identifiers[match[2]].add(name)
    return {identifier: next(iter(names)) for identifier, names in identifiers.items() if len(names) == 1}


def advisory_protocols_by_step(root: Path) -> dict[str, str]:
    """Bind legacy protocol prefixes only to uniquely registered probe commands."""
    scripts = {"BALANCE|": "scripts/probe_opera_balance.gd",
               "DUSTBAL|": "scripts/probe_dust_boss_balance.gd",
               "LAGOONSHOT|": "scripts/probe_sky_lagoon_art.gd",
               "CASTLESHOT|": "scripts/probe_castle_shots_2d.gd",
               "ARTMANIFEST|": "scripts/probe_art_manifest.gd",
               "NORTHSHOT|": "scripts/probe_northern_art.gd",
               "DUSTSHOT|": "scripts/probe_dust_boss_shots.gd",
               "ART_AUDIT|": "scripts/probe_human_art_audit.gd"}
    path = root / ".github/workflows/probes.yml"
    if not path.exists():
        return {}
    owners = collections.defaultdict(set)
    advisory = set(advisory_step_names(root))
    for block in re.split(r"(?m)^\s+- name:\s*", read_text(path))[1:]:
        name = block.splitlines()[0].strip().strip("\"'")
        for prefix, script in scripts.items():
            if re.search(r"(?:^|\s)(?:-s|--script)\s+[\"']?" + re.escape(script) + r"(?:[\"']?(?:\s|$))", block):
                owners[prefix].add(name)
    return {prefix: next(iter(names)) for prefix, names in owners.items()
            if len(names) == 1 and next(iter(names)) in advisory}


def ci_timestamp(value: str) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return result.astimezone(dt.timezone.utc) if result.tzinfo else None


def ci_advisory_lines(root: Path, logs: str, jobs: list, names: list[str]) -> tuple[dict, dict, list[str]]:
    """Attribute named steps, unique wrapper IDs, or unambiguous job time windows.

    GitHub jobs API times have second precision while gh log times have fractions.
    Include the entire recorded completion second in candidate windows: adjacent
    steps then overlap at their boundary and cannot steal each other's verdicts.
    Missing/invalid metadata and overlapping windows remain unattributed.
    """
    observed = {name: [] for name in names}
    methods = {name: collections.Counter() for name in names}
    wrapper_ids = advisory_ids_by_step(root)
    protocols = advisory_protocols_by_step(root)
    unattributed = []
    job_records = collections.defaultdict(list)
    for job in jobs:
        if isinstance(job, dict):
            job_records[job.get("name")].append(job)
    windows = {}
    for job_name, records in job_records.items():
        if len(records) != 1:
            continue
        steps = records[0].get("steps")
        if not isinstance(steps, list) or not steps:
            continue
        candidates = []
        for step in steps:
            if not isinstance(step, dict):
                break
            if step.get("conclusion") == "skipped":
                continue
            start, end = ci_timestamp(step.get("started_at")), ci_timestamp(step.get("completed_at"))
            if start is None or end is None or end < start or not isinstance(step.get("name"), str):
                break
            # The API truncates fractional times. An exact-time fixture can still
            # use its precise completion instant without widening the interval.
            coarse_end = bool(re.search(r"T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})$", step["completed_at"]))
            candidates.append((step["name"], start, end + dt.timedelta(seconds=1) if coarse_end else end, coarse_end))
        else:
            windows[job_name] = candidates
    for line in logs.splitlines():
        fields = line.split("\t", 2)
        if len(fields) != 3:
            if RESULT_RE.search(line) or BAD_RE.search(line) or "verdict=" in line:
                unattributed.append(line)
            continue
        job_name, step_name, body = fields
        method = "named_step"
        name = step_name if step_name in observed else None
        if step_name == "UNKNOWN STEP":
            timestamp, separator, message = body.partition(" ")
            moment = ci_timestamp(timestamp) if separator else None
            wrapper = re.match(r"^ADVISORY\|([^|\s]+)\|RESULT\|", message) if moment else None
            name = wrapper_ids.get(wrapper[1]) if wrapper else None
            if name is not None:
                method = "wrapper_id"
            elif moment is not None:
                matches = [entry[0] for entry in windows.get(job_name, [])
                           if entry[1] <= moment and (moment < entry[2] if entry[3] else moment <= entry[2])]
                name = matches[0] if len(matches) == 1 and matches[0] in observed else None
                method = "job_time_window"
                if len(matches) > 1:
                    owners = {owner for prefix, owner in protocols.items() if message.startswith(prefix) and owner in matches}
                    if len(owners) == 1:
                        name, method = next(iter(owners)), "registered_protocol"
        if name is not None:
            observed[name].append(line)
            methods[name][method] += 1
        elif step_name == "UNKNOWN STEP" and (RESULT_RE.search(line) or BAD_RE.search(line) or "verdict=" in line):
            unattributed.append(line)
    return observed, {name: dict(counts) for name, counts in methods.items()}, unattributed


def analyze_ci(root: Path, head: str, data: dict) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("run"), dict):
        raise ValueError("CI observation must be an object with an object run")
    run = data.get("run", {})
    actual = run.get("head_sha", run.get("headSha"))
    if actual != head:
        return {"status": "HEAD_MISMATCH", "head": head, "reason": "CI fixture/run belongs to a different head", "run": run, "advisory_steps": []}
    logs = data.get("log", "")
    if not isinstance(logs, str) or not isinstance(data.get("jobs", []), list):
        raise ValueError("CI observation log must be text and jobs must be an array")
    rows = []
    artifacts_by_name = {a.get("name"): a for a in data.get("artifacts", []) if not a.get("expired", False)}
    expected_artifacts = artifact_names_by_step(root)
    step_conclusions = {s.get("name"): s.get("conclusion") for j in data.get("jobs", []) if isinstance(j, dict)
                        for s in j.get("steps", []) if isinstance(s, dict)}
    names = advisory_step_names(root)
    attributed, methods, unattributed = ci_advisory_lines(root, logs, data.get("jobs", []), names)
    for name in names:
        lines = attributed[name]
        text = "\n".join(lines)
        status, reason = advisory_status(text, step_conclusions.get(name))
        result_lines = [line for line in lines if RESULT_RE.search(line) or BAD_RE.search(line) or "verdict=" in line]
        if name in expected_artifacts:
            artifact = artifacts_by_name.get(expected_artifacts[name])
            if artifact and artifact.get("size_in_bytes", 0) > 0 and status != "FAIL":
                status, reason = "MEASURED", "Exact-run nonempty artifact exists; upload does not prove capture quality"
                result_lines.append(f"ARTIFACT|{expected_artifacts[name]}|bytes={artifact['size_in_bytes']}")
            elif data.get("artifacts_complete", True):
                status, reason = "NOT_MEASURED", "Expected nonempty upload artifact is absent or expired"
        rows.append({"name": name, "status": status, "reason": reason,
                     "conclusion": step_conclusions.get(name), "result_lines": result_lines,
                     "log_lines": len(lines), "log_attribution": methods[name]})
    return {"status": "MEASURED" if data.get("log_complete", True) else "PARTIAL", "head": head, "run": run, "advisory_steps": rows,
            "artifacts": data.get("artifacts", []), "log_complete": data.get("log_complete", True),
            "recent_runs": data.get("recent_runs", [run]),
            "unattributed_result_lines": unattributed,
            "attribution_limit": "UNKNOWN STEP requires complete, unique job windows or a unique declared wrapper ID; boundary seconds require uniquely registered probe protocol ownership. Unattributed verdicts are evidence gaps, never passes.",
            "limit": "Overall CI success and advisory measurements are independent of device/child/owner acceptance"}


def collect_ci(root: Path, head: str, offline: bool, timeout: float, fixture: Path | None) -> dict:
    if fixture:
        return analyze_ci(root, head, json.loads(read_text(fixture)))
    if offline:
        return {"status": "NOT_MEASURED", "head": head, "reason": "Explicit offline run; no remote CI claim", "advisory_steps": []}
    repo = execute(root, ["gh", "repo", "view", "--json", "nameWithOwner"], timeout)
    if repo["status"] != "MEASURED":
        return {"status": "UNAVAILABLE", "head": head, "reason": "GitHub repository lookup failed", "measurement": repo, "advisory_steps": []}
    try:
        name = json.loads(repo["output"])["nameWithOwner"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name):
            raise ValueError("Invalid repository identity")
        runs = execute(root, ["gh", "api", f"repos/{name}/actions/runs?head_sha={head}&per_page=100"], timeout)
        if runs["status"] != "MEASURED":
            raise ValueError("Run lookup unavailable")
        choices = [r for r in json.loads(runs["output"]).get("workflow_runs", [])
                   if r.get("head_sha") == head and (r.get("name") == "Probe Suite" or str(r.get("path", "")).endswith("probes.yml"))]
        if not choices:
            return {"status": "NOT_MEASURED", "head": head, "reason": "No Probe Suite run at exact studied head", "advisory_steps": []}
        run = max(choices, key=lambda r: r.get("id", 0))
        run_id = run["id"]
        log = execute(root, ["gh", "run", "view", str(run_id), "--repo", name, "--log"], timeout, 15_000_000)
        jobs = execute(root, ["gh", "api", f"repos/{name}/actions/runs/{run_id}/jobs?per_page=100"], timeout, 2_000_000)
        artifacts = execute(root, ["gh", "api", f"repos/{name}/actions/runs/{run_id}/artifacts?per_page=100"], timeout, 2_000_000)
        recent = execute(root, ["gh", "api", f"repos/{name}/actions/runs?per_page=100"], timeout, 2_000_000)
        recent_runs = [r for r in json.loads(recent["output"]).get("workflow_runs", [])
                       if r.get("name") == "Probe Suite" or str(r.get("path", "")).endswith("probes.yml")] if recent["status"] == "MEASURED" else []
        result = analyze_ci(root, head, {"run": {k: run.get(k) for k in ("id", "head_sha", "status", "conclusion", "html_url", "updated_at")},
                                       "log": log["output"], "log_complete": log["status"] == "MEASURED",
                                       "jobs": json.loads(jobs["output"]).get("jobs", []) if jobs["status"] == "MEASURED" else [],
                                       "artifacts": json.loads(artifacts["output"]).get("artifacts", []) if artifacts["status"] == "MEASURED" else [],
                                       "artifacts_complete": artifacts["status"] == "MEASURED",
                                       "recent_runs": [{k: r.get(k) for k in ("id", "head_sha", "status", "conclusion", "html_url", "updated_at")} for r in recent_runs]})
        result["lookup_status"] = {"log": log["status"], "jobs": jobs["status"], "artifacts": artifacts["status"]}
        return result
    except (ValueError, KeyError, TypeError) as error:
        return {"status": "UNAVAILABLE", "head": head, "reason": str(error), "advisory_steps": []}


def branch_inventory(root: Path, timeout: float) -> dict:
    reference = "origin/dev"
    exists = git_result(root, "rev-parse", "--verify", reference, timeout=timeout)
    if exists["exit_code"] != 0:
        return {"status": "NOT_MEASURED", "reason": "origin/dev unavailable; no substitute integration authority"}
    result = git_result(root, "for-each-ref", f"--no-merged={reference}", "--format=%(refname:short)|%(objectname)|%(committerdate:iso-strict)", "refs/remotes/origin", timeout=timeout)
    return {"status": result["status"], "integration_head": exists["output"].strip(),
            "unmerged": [{"branch": parts[0], "head": parts[1], "last_commit": parts[2]}
                         for line in result["output"].splitlines() if len(parts := line.split("|")) == 3],
            "limit": "Local fetched refs only; study never fetches or deletes branches"}


def decision_inventory(root: Path) -> dict:
    path = root / "design/reference/owner_decisions.json"
    if not path.exists():
        return {"status": "NOT_MEASURED", "recorded_owner": [], "operating_default": [],
                "reason": "Decision register absent"}
    try:
        data = json.loads(read_text(path))
        rows = data.get("decisions", data.get("entries", [])) if isinstance(data, dict) else data
        if not isinstance(rows, list):
            raise ValueError("Decision register entries must be an array")
    except (OSError, ValueError) as error:
        return {"status": "FAIL", "reason": str(error), "recorded_owner": [], "operating_default": []}
    observed = {"recorded_owner": [], "operating_default": [], "unclassified": []}
    for row in rows:
        if not isinstance(row, dict):
            observed["unclassified"].append(row)
            continue
        classification = row.get("authority", row.get("decision_type", row.get("status", "")))
        key = str(classification).lower()
        observed[key if key in observed else "unclassified"].append(row)
    return {"status": "MEASURED", "source": "design/reference/owner_decisions.json", **observed,
            "limit": "Operating defaults are not owner answers or acceptance"}


def recurrence_proposals(impacts: dict, paths: list[str]) -> list[dict]:
    groups = collections.defaultdict(list)
    for row in impacts["lessons"]:
        if row["record"] not in paths or not isinstance(row["value"], dict):
            continue
        value = row["value"]
        key = value.get("recurrence_key") or value.get("lesson")
        if isinstance(key, str) and key.strip():
            groups[key.strip()].append({"record": row["record"], "lesson": value.get("lesson"),
                                        "write_back": value.get("write_back")})
    return [{"key": key, "count": len(rows), "evidence": rows,
             "proposal": "Propose a named rule or check; owner/rule authority remains unchanged"}
            for key, rows in sorted(groups.items()) if len(rows) >= 3]


def cycle_evidence(root: Path, cycle: str) -> dict:
    path = root / "audit/cycles" / cycle / "CYCLE_EVIDENCE.json"
    answer_path = path.with_name("owner_answers.json")
    try:
        data = json.loads(read_text(path)) if path.exists() else {}
        if not isinstance(data, dict):
            raise ValueError("Cycle evidence must be an object")
        intake = json.loads(read_text(answer_path)) if answer_path.exists() else []
        if not isinstance(intake, list):
            raise ValueError("Saved owner answers must be an array")
        for row in intake:
            if not isinstance(row, dict) or row.get("authority") != "recorded_owner" or row.get("cycle") != cycle:
                raise ValueError("Saved owner answers require recorded_owner authority and this exact cycle")
    except (OSError, ValueError) as error:
        return {"status": "FAIL", "complete": False, "reason": str(error)}
    missing = []
    owner_answers = data.get("owner_answers", [])
    if not isinstance(owner_answers, list):
        owner_answers = []
    answers_by_id = {}
    for answer in [*owner_answers, *intake]:
        if not isinstance(answer, dict) or answer.get("authority") != "recorded_owner":
            continue
        if answer.get("cycle") != cycle or not isinstance(answer.get("id"), str) or not answer["id"].strip():
            return {"status": "FAIL", "complete": False, "reason": "Actual owner answer needs an ID and this exact cycle"}
        if not answer.get("question") or not (answer.get("answer") or answer.get("decision")):
            return {"status": "FAIL", "complete": False, "reason": "Actual owner answer needs its question and answer/decision"}
        if answer["id"] in answers_by_id and answer != answers_by_id[answer["id"]]:
            return {"status": "FAIL", "complete": False, "reason": f"Conflicting owner answer ID {answer['id']}"}
        answers_by_id[answer["id"]] = answer
    answers = list(answers_by_id.values())
    if not answers:
        missing.append("actual_owner_answers")
    for key, values in [("owner_answers", answers)] + [(k, data.get(k, [])) for k in ("build", "check", "learn")]:
        if not isinstance(values, list) or not values:
            if key != "owner_answers":
                missing.append(key)
            continue
        for value in values:
            refs = value.get("evidence", value.get("source", [])) if isinstance(value, dict) else []
            refs = [refs] if isinstance(refs, str) else refs
            # Evidence is required, never a mere PASS/default flag.
            if not refs or not all(isinstance(r, str) and (p := safe_relative(root, r.split("#", 1)[0])) is not None and p.is_file() for r in refs):
                missing.append(f"{key}_evidence")
                break
    status = "EVIDENCE_RECORDED_REQUIRES_REVIEW" if not missing else ("INCOMPLETE" if path.exists() or answer_path.exists() else "AWAITING_OWNER_ANSWERS")
    return {"status": status,
            "complete": False, "recorded_lanes_complete": not missing, "missing": sorted(set(missing)),
            "source": path.relative_to(root).as_posix() if path.exists() else None,
            "owner_answers_source": answer_path.relative_to(root).as_posix() if answer_path.exists() else None,
            "actual_owner_answers": answers,
            "limit": "Tool verifies referenced evidence exists; actual owner/build/check/learn review decides completion"}


def document_sha_references(root: Path, paths: list[str], timeout: float) -> dict:
    references = collections.defaultdict(list)
    for relative in paths:
        if not relative.endswith(".md"):
            continue
        path = safe_relative(root, relative)
        if path is None or not path.is_file():
            continue
        for sha in sorted(set(re.findall(r"\b[0-9a-fA-F]{40}\b", read_text(path)))):
            references[sha.lower()].append(relative)
    if not references:
        return {"status": "MEASURED", "checked": 0, "unresolved": []}
    values = sorted(references)
    result = execute(root, ["git", "cat-file", "--batch-check"], timeout,
                     input_text="\n".join(values) + "\n")
    if result["status"] != "MEASURED":
        return {"status": "NOT_MEASURED", "reason": result.get("reason", "Git object lookup incomplete"),
                "checked": 0, "unresolved": []}
    missing = [line.split()[0] for line in result["output"].splitlines() if line.endswith(" missing")]
    return {"status": "MEASURED", "checked": len(values),
            "unresolved": [{"sha": sha, "documents": references[sha]} for sha in missing],
            "limit": "Unresolved local objects need source review; external-repository references are not fabricated defects"}


def loop_delta(current: dict, previous: dict) -> dict:
    prior = previous.get("loop_health", previous if previous.get("measure") == "loop_health" else {})
    kind = "baseline_measurement" if previous.get("measure") == "loop_health" else ("study_cycle" if prior else "none")
    metrics = {}
    def values(value: dict) -> dict:
        findings = value.get("findings", {})
        impacts = value.get("impact_records", {})
        count = impacts.get("records")
        return {"stale_open": findings.get("open_without_history_entry_for", {}).get("30_days"),
                "fixed_pending_verification": len(findings["fixed_pending_verification"]) if "fixed_pending_verification" in findings else None,
                "structured_lessons_fraction": impacts.get("with_structured_lessons", 0) / count
                if count and "with_structured_lessons" in impacts else None}
    before, after = values(prior), values(current)
    for name in after:
        comparable = before[name] is not None and after[name] is not None
        metrics[name] = {"previous": before[name], "current": after[name],
                         "delta": after[name] - before[name] if comparable else None,
                         "status": "COMPARABLE" if comparable else "NOT_COMPARABLE"}
    old_handoffs = {r["handoff"]: r.get("status") for r in prior.get("handoffs", [])}
    rows = [{"handoff": r["handoff"], "previous": old_handoffs.get(r["handoff"]), "current": r["status"],
             "status": "COMPARABLE" if r["handoff"] in old_handoffs else "NOT_COMPARABLE"}
            for r in current.get("handoffs", [])]
    return {"baseline_kind": kind, "metrics": metrics, "handoffs": rows,
            "limit": "Measurements do not constitute completed owner/build/check/learn cycles"}


def library_comparison(current: dict, prior: dict) -> dict:
    if current.get("status") != "MEASURED" or prior.get("status") != "MEASURED":
        return {"status": "NOT_COMPARABLE", "reason": "Both cycles require a library hash observation"}
    old = {r["path"]: r["reason"] for r in prior.get("stale_items", [])}
    new = {r["path"]: r["reason"] for r in current.get("stale_items", [])}
    return {"status": "COMPARABLE", "previous_source_revision": prior.get("source_revision"),
            "current_source_revision": current.get("source_revision"),
            "new_stale_items": sorted(set(new) - set(old)), "no_longer_stale_items": sorted(set(old) - set(new)),
            "new_changed_watched_sources": sorted(set(current.get("changed_watched_sources", [])) - set(prior.get("changed_watched_sources", []))),
            "no_longer_changed_watched_sources": sorted(set(prior.get("changed_watched_sources", [])) - set(current.get("changed_watched_sources", []))),
            "limit": "Hash/source changes only; review scores and acceptance are not inferred"}


def roadmap_observation(root: Path, study: dict) -> dict:
    """Read current roadmap and compare to the same-cycle/source deterministic render."""
    path = root / "audit/ROADMAP.md"
    context = {"source": "audit/ROADMAP.md", "cycle": study.get("cycle_date", study.get("cycle")),
               "studied_head": study.get("studied_head", study.get("head"))}
    if not path.is_file():
        return {**context, "status": "NOT_MEASURED", "current": None, "reason": "Current roadmap is absent"}
    try:
        try:
            from tools.build_study_roadmap import build_outputs
        except ModuleNotFoundError:
            from build_study_roadmap import build_outputs
        expected = build_outputs(root, study)["ROADMAP.md"].encode("utf-8")
        raw = path.read_bytes()
        # Git may checkout generated Markdown with CRLF on Windows. Compare the
        # exact canonical LF render and retain both canonical and raw byte hashes.
        observed = raw.replace(b"\r\n", b"\n")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ImportError) as error:
        return {**context, "status": "NOT_MEASURED", "current": None,
                "reason": f"Cannot validate same-cycle/source roadmap: {error}"}
    current = observed == expected
    return {**context, "status": "MEASURED", "current": current, "hash_mode": "git_canonical_lf",
            "observed_sha256": hashlib.sha256(observed).hexdigest(),
            "observed_raw_sha256": hashlib.sha256(raw).hexdigest(),
            "expected_sha256": hashlib.sha256(expected).hexdigest(),
            "reason": "Exact deterministic same-cycle/source canonical LF render matches" if current else "Roadmap is stale or differs from the deterministic same-cycle/source render",
            "limit": "A current advisory plan is not finding closure or owner acceptance"}


def health_targets(study: dict) -> list[dict]:
    loop = study["loop_health"]
    findings = loop.get("findings", {})
    impacts = study["impacts"]
    opened = findings.get("open", 0)
    stale = findings.get("open_without_history_entry_for", {}).get("30_days", 0) + findings.get("open_missing_history", 0)
    fraction = stale / opened if opened else 0.0
    old_fixes = sum((r.get("days_since") or 0) > 30 for r in findings.get("fixed_pending_verification", []))
    records = impacts["records"]
    # The LP4 starting boundary is explicit metadata, not inferred from file dates.
    start = study.get("lessons_since")
    lessons_fraction = None
    if start:
        eligible = [r for r in records if r.get("last_changed_head") in study.get("lesson_commits", [])]
        lessons_fraction = sum(bool(r.get("lessons")) for r in eligible) / len(eligible) if eligible else None
    corrections = [json.dumps(r["value"], sort_keys=True) for r in impacts["owner_corrections"]]
    repeated = sum(n - 1 for n in collections.Counter(corrections).values() if n > 1)
    roadmap = study.get("roadmap_observation", {})
    roadmap_status = "NOT_MEASURED" if roadmap.get("status") != "MEASURED" else ("ON_TARGET" if roadmap.get("current") else "NEEDS_ATTENTION")
    return [{"id": "stale_open_fraction", "value": fraction, "target": "<=0.10", "status": "ON_TARGET" if fraction <= .10 else "NEEDS_ATTENTION"},
            {"id": "old_unverified_fixes", "value": old_fixes, "target": "0", "status": "ON_TARGET" if old_fixes == 0 else "NEEDS_ATTENTION"},
            {"id": "lessons_fraction_since_lp4", "value": lessons_fraction, "target": ">=0.50", "status": "NOT_MEASURED" if lessons_fraction is None else ("ON_TARGET" if lessons_fraction >= .5 else "NEEDS_ATTENTION"), "reason": "Set --lessons-since to a real LP4 commit boundary; no fabricated retrospective lessons"},
            {"id": "repeated_owner_corrections", "value": repeated, "target": "0", "status": "NEEDS_ATTENTION" if repeated else "NOT_MEASURED", "reason": "Only structured correction entries; historical prose and semantic repetitions require review"},
            {"id": "roadmap_current_cycle", "value": roadmap.get("current"), "target": "regenerated this cycle", "status": roadmap_status, "measurement_status": roadmap.get("status", "NOT_MEASURED"), "reason": roadmap.get("reason", "Roadmap has not been observed")},
            {"id": "handoffs_waiting_two_cycles", "value": None, "target": "all listed", "status": "NOT_MEASURED", "reason": "Requires three retained cycle observations; path inventory alone cannot establish age in cycles"}]


def report_value(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)


def render_report(study: dict) -> str:
    """Every displayed number and fact comes only from the saved study object."""
    loop = study["loop_health"]
    findings = loop.get("findings", {})
    impacts = study["impacts"]
    lines = [f"# Game study — {study['cycle']}", "", "Status: `SUPPORTING_CURRENT` advisory draft. Machine evidence, owner review, device and child acceptance remain separate.", "",
             "## 0. Cycle header", "", f"- Studied head: `{study['head']}`; as of {study['as_of']}.",
             f"- Working tree: {'changed; measurements include listed uncommitted changes' if study['working_tree']['paths'] else 'clean'}.",
             f"- Previous cycle: {study.get('previous_cycle') or 'none'}. Changes: {len(study['changes']['commits'])} commits, {len(study['changes']['paths'])} paths.",
             f"- CI: {study['ci']['status']}; {study['ci'].get('reason', study['ci'].get('run', {}).get('html_url', 'exact-head run recorded'))}.", "",
             "## 1. What changed since the last cycle", ""]
    changed_records = [r for r in impacts["records"] if r["record"] in study["changes"]["paths"]]
    lines += [f"- `{r['id']}`: {r['scope']} ({r['record']})." for r in changed_records] or ["No previous-cycle range is available; current records are retained in study.json."]
    lines += ["", "## 2. Strengths observed", ""]
    lines += [f"- `{r['id']}`: {json.dumps(r['value'], sort_keys=True, ensure_ascii=False)}; {r['record']}." for r in impacts["strengths_observed"]] or ["No structured strengths observations recorded. Candidate register evidence is reviewed through the roadmap/recipe workflow."]
    lines += ["", "## 3. Weaknesses and sensor coverage", "", "| Sensor | Collection | Evidence status / gap |", "|---|---|---|"]
    for name, sensor in sorted(study["sensors"].items()):
        status = sensor.get("summary", {}).get("status", "")
        lines.append(f"| {name} | {sensor['status']} | {str(status or sensor.get('reason', 'Read measured summary in study.json')).replace('|', '/')} |")
    lines += [f"- Advisory `{r['name']}`: {r['status']} — {r['reason']}." for r in study["ci"].get("advisory_steps", [])]
    unattributed = study["ci"].get("unattributed_result_lines", [])
    if unattributed:
        lines += [f"- CI attribution gap: {len(unattributed)} result/verdict lines have no proven advisory owner; retained in study.json and excluded from passing measurements."]
        lines += [f"  - {line.replace('`', '').replace(chr(9), ' / ')}" for line in unattributed[:20]]
        if len(unattributed) > 20:
            lines += [f"  - Report excerpt capped at 20 lines; all {len(unattributed)} lines remain in study.json."]
    lines += [f"- `{r.get('id', 'finding coverage')}` needs source recheck: {', '.join(f['path'] for f in r.get('files', [])) or r.get('reason', '')}." for r in study["findings_changed_since_history"]]
    lines += [f"- Motion `{r['id']}` ({r['kind']}): {len(r['owner_verdicts'])} recorded human/owner verdict entries; {r['acceptance_gaps']}." for r in study["motion_studies"]]
    lines += ["", "## 4. Loop health", "", f"Open findings: {findings.get('open', 'NOT_MEASURED')}; without a history entry for 30 days: {findings.get('open_without_history_entry_for', {}).get('30_days', 'NOT_MEASURED')}; fixed pending verification: {len(findings.get('fixed_pending_verification', []))}.",
              f"Impact records: {len(impacts['records'])}; structured lessons: {len(impacts['lessons'])}; pending validations: {len(impacts['pending'])}; failed validations retained: {len(impacts['failed'])}.", "",
              "| Health target | Value | Target | Status |", "|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['value'] if r['value'] is not None else 'NOT_MEASURED'} | {r['target']} | {r['status']} |" for r in study["health_targets"]]
    lines += ["", "| Metric since previous observation | Previous | Current | Delta |", "|---|---|---|---|"]
    lines += [f"| {name} | {report_value(row['previous'])} | {report_value(row['current'])} | {report_value(row['delta']) if row['status'] == 'COMPARABLE' else 'NOT_COMPARABLE'} |"
              for name, row in sorted(study.get("loop_health_delta", {}).get("metrics", {}).items())]
    library = study.get("day_two_library", {})
    lines += ["", f"Day Two library: {library.get('status', 'NOT_MEASURED')}; {len(library.get('changed_watched_sources', []))} changed watched sources, {len(library.get('stale_items', []))} stale art hashes. Previous observation comparison: {library.get('previous_observation_delta', {}).get('status', 'NOT_COMPARABLE')}."]
    lines += ["", "## 5. Roadmap delta", "", f"Handoffs inventoried: {len(study['handoffs'])}. Unmerged fetched branches: {len(study['branches'].get('unmerged', []))}. Target presence is not implementation or acceptance.",
              "Run tools/build_study_roadmap.py with this study.json to generate Repair, Grow and Strengthen lanes.", "",
              "## 6. Next prompts", "", '1. "Repair the reported advisory sensor gaps" — `INT-REPAIR`; use exact results and preserve acceptance gaps.',
              '2. "Study the game" — `INT-STUDY`; retain this cycle as the previous observation.', "",
              "## 7. Owner questions and external evidence", "", "The handoff defaults apply. Scheduled automation remains deferred until two complete manual cycles and owner agreement. No telemetry collected. Owner/device/child sessions need actual evidence; this generated draft cannot supply it.", "",
              "## 8. Lessons recorded", ""]
    lines += [f"Cycle evidence: {study.get('cycle_evidence', {}).get('status', 'NOT_MEASURED')}. Recorded owner decisions: {len(study.get('owner_decisions', {}).get('recorded_owner', []))}; operating defaults: {len(study.get('owner_decisions', {}).get('operating_default', []))}.", ""]
    lines += [f"- `{r['id']}`: {json.dumps(r['value'], sort_keys=True, ensure_ascii=False)}; write-back {'MISSING' if r['write_back_missing'] else 'named'}; {r['record']}." for r in impacts["lessons"]] or ["No structured lessons recorded; historical prose remains evidence and is not rewritten."]
    lines += ["", "PENDING entries with matching finished CI are proposed for record reconciliation only; source records remain unchanged."]
    lines += [f"- `{r['id']}`: {report_value(r.get('ci_reconciliation', 'No exact matching CI result collected'))}." for r in impacts["pending"]]
    lines += [f"- Recurrence proposal: {r['key']} occurred {r['count']} times in this cycle; {r['proposal']}." for r in study.get("recurrence_proposals", [])]
    return "\n".join(lines) + "\n"


def collect(root: Path, cycle: str, as_of: str, previous: Path | None = None, offline: bool = False,
            timeout: float = 60, skip_sensors: bool = False, ci_fixture: Path | None = None,
            max_output: int = 1_000_000, lessons_since: str | None = None) -> dict:
    dt.date.fromisoformat(as_of)
    head = git_text(root, "rev-parse", "HEAD", timeout=timeout).strip()
    dirty = git_text(root, "status", "--porcelain=v1", "--untracked-files=all", timeout=timeout)
    dirty_paths = [line[3:].strip('"').replace("\\", "/") for line in dirty.splitlines() if len(line) > 3]
    prior = json.loads(read_text(previous)) if previous else {}
    if not isinstance(prior, dict):
        raise ValueError("Previous observation must be a JSON object")
    if "loop_health" in prior and not isinstance(prior["loop_health"], dict):
        raise ValueError("Previous observation loop_health must be an object")
    previous_head = prior.get("head", prior.get("studied_head"))
    commits = []
    paths = []
    if previous_head:
        if not re.fullmatch(r"[0-9a-fA-F]{40}", previous_head):
            raise ValueError("Previous cycle head must be a full commit SHA")
        ancestor = git_result(root, "merge-base", "--is-ancestor", previous_head, head, timeout=timeout)
        if ancestor["exit_code"] != 0:
            raise ValueError("Previous cycle head is unavailable or not in studied ancestry")
        commits = git_text(root, "rev-list", f"{previous_head}..{head}", timeout=timeout).splitlines()
        paths = git_text(root, "diff", "--name-only", previous_head, head, timeout=timeout).splitlines()
    paths = sorted(set(paths + dirty_paths))
    if lessons_since:
        if not re.fullmatch(r"[0-9a-fA-F]{40}", lessons_since):
            raise ValueError("--lessons-since requires a full LP4 commit SHA")
        if git_result(root, "merge-base", "--is-ancestor", lessons_since, head, timeout=timeout)["exit_code"] != 0:
            raise ValueError("LP4 boundary is unavailable or not in studied ancestry")
        commits_since = [lessons_since, *git_text(root, "rev-list", f"{lessons_since}..{head}", timeout=timeout).splitlines()]
    else:
        commits_since = []
    loop = health.measure(root, dt.date.fromisoformat(as_of), timeout)
    impacts = collect_impacts(root, timeout)
    ci = collect_ci(root, head, offline, timeout, ci_fixture)
    for pending in impacts["pending"]:
        if pending["record"] in dirty_paths:
            pending["ci_reconciliation"] = "Impact has working-tree edits; earlier CI does not verify this record version"
            continue
        candidates = [r for r in ci.get("recent_runs", [])
                      if r.get("head_sha", r.get("headSha")) == pending["last_changed_head"] and r.get("status") == "completed"]
        if candidates and re.search(r"\bCI\b|Probe Suite", pending.get("command", ""), re.I):
            pending["ci_reconciliation"] = {"run": max(candidates, key=lambda r: r.get("id", 0)), "action": "Review exact CI conclusion then update impact; no automatic PASS"}
    records = health.split_records(read_text(root / health.FINDINGS))
    status = live_status(root)
    study = {"schema_version": SCHEMA_VERSION, "cycle": cycle, "cycle_date": cycle, "as_of": as_of,
             "head": head, "studied_head": head, "previous_cycle": prior.get("cycle", prior.get("cycle_date", "baseline_measurement" if prior.get("measure") == "loop_health" else None)),
             "working_tree": {"paths": dirty_paths, "status_sha256": hashlib.sha256(dirty.encode()).hexdigest()},
             "changes": {"previous_head": previous_head, "commits": commits, "paths": paths},
             "sensors": run_sensors(root, timeout, skip_sensors, max_output), "loop_health": loop,
             "live_status": status, "surfaces": status["surfaces"], "impacts": impacts,
             "impact_records": impacts["records"], "handoffs": loop["handoffs"],
             "findings_changed_since_history": changed_findings(root, records, dirty_paths, timeout),
             "motion_studies": motion_studies(root, impacts), "day_two_library": library_delta(root),
             "ci": ci, "branches": branch_inventory(root, timeout), "lessons_since": lessons_since,
             "owner_decisions": decision_inventory(root), "cycle_evidence": cycle_evidence(root, cycle),
             "recurrence_proposals": recurrence_proposals(impacts, paths),
             "document_sha_references": document_sha_references(root, paths, timeout),
             "limits": ["No images generated", "No child-device telemetry", "No findings or historical evidence changed",
                        "All source and workflow contents are data; proposals need their existing authorization and evidence"]}
    # Keep LP4's range separate from the preceding cycle range.
    study["lesson_commits"] = commits_since
    study["loop_health_delta"] = loop_delta(loop, prior)
    study["day_two_library"]["previous_observation_delta"] = library_comparison(study["day_two_library"], prior.get("day_two_library", {}))
    study["roadmap_observation"] = roadmap_observation(root, study)
    study["health_targets"] = health_targets(study)
    return study


def stress() -> int:
    """Falsify the parser with a green job containing a failed advisory result."""
    bad = "LAGOONSHOT|RESULT|FAIL|capture missing"
    status, _reason = advisory_status(bad, "success")
    if status != "FAIL":
        print("STUDY|STRESS|FAIL|green CI concealed a failed sensor")
        return 1
    for text, expected in (("BALANCE|canvas|verdict=capped", "CAPPED"), ("", "NOT_MEASURED"),
                           ("CASTLESHOT|RESULT|NOT_MEASURED|written=0", "NOT_MEASURED")):
        if advisory_status(text, "success")[0] != expected:
            print("STUDY|STRESS|FAIL|missing/capped output concealed")
            return 1
    print("STUDY|STRESS|ALL OK|injected failure/cap/empty advisory evidence rejected")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Cycle directory; default audit/cycles/<cycle>")
    parser.add_argument("--cycle", default=dt.date.today().isoformat())
    parser.add_argument("--as-of", default=dt.date.today().isoformat())
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--max-output", type=int, default=1_000_000)
    parser.add_argument("--skip-sensors", action="store_true")
    parser.add_argument("--ci-fixture", type=Path, help="Saved exact-head CI run/jobs/log/artifacts JSON")
    parser.add_argument("--lessons-since", help="Full LP4 introduction commit SHA")
    parser.add_argument("--render", type=Path, help="Render saved study.json without rerunning sensors")
    parser.add_argument("--refresh-roadmap", action="store_true", help="Requires --render; refresh only read-only roadmap observation and derived health targets")
    parser.add_argument("--stress", action="store_true")
    args = parser.parse_args(argv)
    if args.refresh_roadmap and not args.render:
        parser.error("--refresh-roadmap requires --render")
    if args.stress:
        return stress()
    if args.timeout <= 0 or args.max_output < 1024 or not re.fullmatch(r"[A-Za-z0-9_.-]+", args.cycle):
        parser.error("positive timeout, output cap >=1024 and safe cycle identifier required")
    root = args.root.resolve()
    try:
        study = json.loads(read_text(args.render)) if args.render else collect(
            root, args.cycle, args.as_of, args.previous, args.offline, args.timeout,
            args.skip_sensors, args.ci_fixture, args.max_output, args.lessons_since)
        if not isinstance(study, dict):
            raise ValueError("Saved study must be a JSON object")
        for key, kind in (("cycle", str), ("head", str), ("as_of", str), ("sensors", dict),
                          ("loop_health", dict), ("working_tree", dict), ("changes", dict),
                          ("ci", dict), ("impacts", dict), ("branches", dict),
                          ("handoffs", list), ("health_targets", list),
                          ("findings_changed_since_history", list), ("motion_studies", list)):
            if not isinstance(study.get(key), kind):
                raise ValueError(f"Saved study has missing/invalid {key}")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", study["cycle"]):
            raise ValueError("Saved study cycle identifier is unsafe")
        if args.refresh_roadmap:
            study["roadmap_observation"] = roadmap_observation(root, study)
            study["health_targets"] = health_targets(study)
        # Render before writing so malformed nested data leaves no partial artifact.
        report = render_report(study)
        output = args.output or root / "audit/cycles" / study["cycle"]
        if not output.is_absolute():
            output = root / output
        output.mkdir(parents=True, exist_ok=True)
        (output / "study.json").write_text(json.dumps(study, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        (output / "STUDY_REPORT.md").write_text(report, encoding="utf-8", newline="\n")
        print(f"STUDY|COLLECTED|{study['head']}|{output}")
        print("STUDY|ACCEPTANCE|NOT_MEASURED|device/child/owner gates remain separate")
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as error:
        print(f"STUDY|RESULT|FAIL|{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
