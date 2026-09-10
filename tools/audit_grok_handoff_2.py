#!/usr/bin/env python3
"""Check Handoff 2 archive integrity and fail closed on unfinished repair jobs.

This supplements, never replaces, the Imagine and full-frame cinematic gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root: Path, value: str) -> Path:
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes packet: {value}")
    return path


def check_card(root: Path, card: dict, shot_ids: set[str], ready: bool = False) -> list[str]:
    errors = []
    sid = card.get("shot_id", "unknown")
    bindings = card.get("bindings", [])
    if not 2 <= len(bindings) <= 4:
        errors.append("requires 2-4 bindings")
    if [b.get("id") for b in bindings] != [f"IMAGE_{i+1}" for i in range(len(bindings))]:
        errors.append("binding IDs must be ordered and unique")
    if not bindings or bindings[0].get("role") != "approved_clean_first_frame":
        errors.append("IMAGE_1 must be a complete approved opening")
    for b in bindings:
        value = b.get("path")
        if value is None:
            if b.get("id") != "IMAGE_1" or not card.get("blocking_findings"):
                errors.append("missing binding without explicit opening blocker")
            continue
        if b.get("id") == "IMAGE_1":
            review = b.get("human_review")
            if not isinstance(review, dict) or review.get("decision") != "approved" or review.get("sha256") != b.get("sha256"):
                errors.append("non-null opening requires human approval of its exact hash; no fallback plate")
        if any(token in value.lower() for token in ("evidence/", "boards/", "storyboard", "runtime_boundary")):
            errors.append("review/board pixels cannot be bound")
        try:
            p = local(root, value)
            if not p.is_file() or digest(p) != b.get("sha256"):
                errors.append(f"binding hash mismatch: {value}")
        except ValueError as exc:
            errors.append(str(exc))
    deps = card.get("depends_on", [])
    if sid in deps or any(d not in shot_ids for d in deps):
        errors.append("invalid shot dependency")
    camera = card.get("camera", {})
    if camera.get("move_count") not in (0, 1) or not camera.get("verb"):
        errors.append("requires one named camera setup and at most one move")
    if (camera.get("verb") == "locked") != (camera.get("move_count") == 0):
        errors.append("camera verb/count disagree")
    states = {b.get("path") for b in bindings}
    if any(p and p.endswith("/objects/seahorse_sick.png") for p in states) and any(p and p.endswith("/handoff_art/seahorse_sick.png") for p in states):
        errors.append("conflicting plugged/unplugged seahorse state bindings")
    prompt = root / "shots" / sid / "PROMPT.txt"
    if not prompt.is_file() or digest(prompt) != card.get("prompt_sha256"):
        errors.append("prompt missing or changed")
    elif not prompt.read_text(encoding="utf-8").strip().splitlines()[-1].startswith("Sound:"):
        errors.append("prompt must end with Sound:")
    if card.get("delivery_accepted") is not False:
        errors.append("repair queue cannot grant delivery acceptance")
    if card.get("output_disposition") != "motion_reference_only":
        errors.append("Grok output must remain motion reference")
    if card.get("generation_ready") or ready:
        # This draft queue deliberately cannot self-promote. A separately audited
        # V1/V2 execution packet supplies accepted openings and actual reviews.
        errors.append("draft repair queue is not an executable Imagine packet; run the independent V1/V2 readiness gate after binding approved openings")
    if card.get("status") != "DRAFT":
        errors.append("unsupported repair queue status")
    return [f"{sid}: {e}" for e in errors]


def audit(root: Path, ready: bool = False) -> list[str]:
    errors = []
    try:
        manifest = json.loads((root / "HANDOFF_PACKET.json").read_text(encoding="utf-8"))
        paths = []
        for row in manifest["files"]:
            value = row["path"]
            p = local(root, value)
            paths.append(value)
            if not p.is_file() or digest(p) != row["sha256"]:
                errors.append(f"payload hash mismatch: {value}")
            for key in ("source_path", "role", "license_provenance", "modifications"):
                if not row.get(key):
                    errors.append(f"missing {key}: {value}")
        if len(paths) != len(set(paths)):
            errors.append("duplicate manifest path")
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name not in ("HANDOFF_PACKET.json", "REMOTE_VERIFICATION.json")}
        if actual != set(paths):
            errors.append("manifest does not cover exact packet payload")
        joined = "".join(f'{r["path"]}|{r["sha256"]}\n' for r in sorted(manifest["files"], key=lambda x: x["path"]))
        if hashlib.sha256(joined.encode()).hexdigest() != manifest.get("payload_sha256"):
            errors.append("sorted payload digest mismatch")
        queue = json.loads((root / "SHOT_REPAIR_QUEUE.json").read_text())
        historical = json.loads((root / "history/THIRD_PASS_DECISIONS.json").read_text())
        ids = {s["shot_id"] for s in queue["shots"]}
        if len(ids) != len(queue["shots"]) or ids != {s["shot_id"] for s in historical["shots"]}:
            errors.append("shot coverage differs from historical inventory")
        locks = json.loads((root / "CONTINUITY_LOCKS.json").read_text())
        graph = {}
        for shot in queue["shots"]:
            if shot["disposition"] == "REPAIR":
                card = json.loads(local(root, shot["card"]).read_text())
                if card["shot_id"] != shot["shot_id"]:
                    errors.append("card/queue identity mismatch")
                if card.get("location_id") not in locks:
                    errors.append("unknown shared location lock")
                errors.extend(check_card(root, card, ids, ready))
                graph[card["shot_id"]] = card["depends_on"]
        def visit(node: str, stack: set[str]) -> None:
            if node in stack:
                raise ValueError("cyclic shot dependency")
            for dep in graph.get(node, []):
                visit(dep, stack | {node})
        for node in graph:
            visit(node, set())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"invalid packet: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    errors = audit(args.packet, args.require_ready)
    for error in errors:
        print(f"GH2|FAIL|{error}")
    print(f"GH2|{'FAIL' if errors else 'PASS'}|archive integrity and draft consistency; no visual/delivery acceptance")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
