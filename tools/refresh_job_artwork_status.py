"""Refresh review freshness without changing art, scores, or the sealed library."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "audit/day2_job_contexts_2026-09-30/inventory.json"
OUT = ROOT / "audit/job_artwork_refinement_live/STATUS.json"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def revision(ref: str) -> str:
    return subprocess.check_output(["git", "rev-parse", ref], cwd=ROOT, text=True).strip()


def status() -> dict:
    inventory = json.loads(BASE.read_text(encoding="utf-8"))
    supplemental = json.loads((BASE.parent / "reviews.json").read_text(encoding="utf-8"))["assets"]
    changed = []
    formatting_only = []
    unavailable = []
    for item in inventory["items"]:
        path = ROOT / item["path"]
        if not path.is_file():
            unavailable.append(item["path"])
        elif digest(path.read_bytes()) != item["sha256"]:
            raw = path.read_bytes()
            record = {"id": item["id"], "path": item["path"],
                      "baseline_sha256": item["sha256"], "current_sha256": digest(raw)}
            # Preserve exact byte provenance, but do not label Windows checkout
            # line-ending conversions as newly changed artwork.
            original = subprocess.check_output(
                ["git", "show", "9038246cf9b34005afb8bc28a2f81396930988b6:" + item["path"]], cwd=ROOT)
            if path.suffix == ".svg" and raw.replace(b"\r\n", b"\n") == original.replace(b"\r\n", b"\n"):
                record["qualification"] = "Only CRLF/LF checkout formatting differs; SVG content is unchanged."
                formatting_only.append(record)
            else:
                changed.append(record)
    source_deltas = []
    literal_art = set()
    known = {item["path"] for item in inventory["items"]}
    for name in inventory["sources"]:
        path = ROOT / name
        if not path.is_file():
            unavailable.append(name)
            continue
        raw = path.read_bytes()
        expected = inventory["source_text_fingerprints"][name]["normalized_lf_sha256"]
        actual = digest(raw.replace(b"\r\n", b"\n"))
        if actual != expected:
            source_deltas.append({"path": name, "baseline_normalized_sha256": expected,
                                  "current_normalized_sha256": actual})
        if name.endswith(".gd"):
            literal_art.update(re.findall(r'res://(assets/[^"\s]+\.(?:png|webp|jpg|svg))', raw.decode("utf-8")))
    # Also watch the shared state owner, launch seams, Dolls and Day One code,
    # even where the earlier Day Two capture inventory did not list them.
    tree = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", inventory["production_revision"], "scripts"], cwd=ROOT)
    baseline_scripts = {}
    for row in tree.split(b"\0"):
        if not row:
            continue
        header, path = row.split(b"\t", 1)
        name = path.decode("utf-8")
        if name.endswith(".gd"):
            baseline_scripts[name] = header.split()[2].decode("ascii")
    script_changes = []
    current_scripts = {p.relative_to(ROOT).as_posix() for p in (ROOT / "scripts").rglob("*.gd")}
    for name in sorted(set(baseline_scripts) | current_scripts):
        path = ROOT / name
        raw = path.read_bytes().replace(b"\r\n", b"\n") if path.is_file() else None
        oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() if raw is not None else None
        if oid != baseline_scripts.get(name):
            script_changes.append({"path": name, "baseline_git_blob": baseline_scripts.get(name),
                                   "current_normalized_git_blob": oid})
    care_bindings = []
    care_data = ROOT / "assets/opera/worlds/nursery/refinement_v2/care_keys.json"
    if care_data.is_file():
        for pose in json.loads(care_data.read_text(encoding="utf-8"))["poses"]:
            path = ROOT / pose["path"]
            care_bindings.append({"path": pose["path"], "declared_sha256": pose["sha256"],
                                  "current_sha256": digest(path.read_bytes()) if path.is_file() else None,
                                  "role": "Nursery connected-body candidate; creative/action acceptance remains open."})
    day_one = {"inventory_present": False, "watched_assets": 0, "changed_assets": [],
               "unavailable_assets": [], "reused_source_opinions": 0, "new_source_reviews_pending": 0,
               "new_source_opinions_completed": 0, "source_cells_reviewed": 0}
    day_one_path = ROOT / "audit/day_one_job_art_census_20261001/inventory.json"
    if day_one_path.is_file():
        census = json.loads(day_one_path.read_text(encoding="utf-8"))
        day_one.update(inventory_present=True, watched_assets=len(census["items"]),
                       reused_source_opinions=census["prior_exact_source_opinions_reused"],
                       new_source_reviews_pending=census["remaining_source_review_pending"],
                       new_source_opinions_completed=census.get("new_source_opinions_completed", 0),
                       source_cells_reviewed=census.get("individual_source_cells_reviewed", 0))
        for item in census["items"]:
            path = ROOT / item["path"]
            if path.is_file():
                raw = path.read_bytes()
            else:
                # Sparse checkout is not a deleted asset. Read the current
                # committed object without restoring or modifying its pixels.
                result = subprocess.run(["git", "show", "HEAD:" + item["path"]],
                                        cwd=ROOT, capture_output=True)
                if result.returncode:
                    day_one["unavailable_assets"].append(item["path"])
                    continue
                raw = result.stdout
            current_hash = digest(raw)
            if current_hash != item["sha256"]:
                day_one["changed_assets"].append({"id": item["id"], "path": item["path"],
                                                 "baseline_sha256": item["sha256"],
                                                 "current_sha256": current_hash})
    return {
        "schema": "reef.job-artwork-freshness.v1",
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sealed_library_revision": "9038246cf9b34005afb8bc28a2f81396930988b6",
        "captured_production_revision": inventory["production_revision"],
        "working_head": revision("HEAD"), "cached_origin_dev": revision("origin/dev"),
        "baseline_sources": len(inventory["items"]),
        "baseline_inclusive_source_priorities": sum(
            float(i["draft_source_score"] if "draft_source_score" in i else supplemental[i["id"]]["score"]) <= 4.5
            for i in inventory["items"]),
        "changed_source_art": changed, "source_byte_formatting_only": formatting_only,
        "changed_capture_dependencies": source_deltas,
        "watched_game_scripts": len(set(baseline_scripts) | current_scripts),
        "changed_game_scripts": script_changes,
        "new_care_pose_bindings": care_bindings,
        "day_one_discovery_freshness": day_one,
        "existing_literal_job_art_not_in_baseline_inventory": sorted(
            p for p in literal_art - known if "%" not in p and (ROOT / p).is_file()),
        "unresolved_literal_paths": sorted(p for p in literal_art - known if "%" not in p and not (ROOT / p).is_file()),
        "dynamic_binding_templates": sorted(p for p in literal_art if "%" in p),
        "unavailable_in_checkout": sorted(set(unavailable)),
        "capture_freshness": "REVIEW_REFRESH_REQUIRED" if changed or source_deltas or script_changes or unavailable or day_one["changed_assets"] or day_one["unavailable_assets"] else "BASELINE_BYTES_MATCH",
        "qualification": "Literal references supplement the existing dynamic census; they do not establish every loaded/drawn image. A changed hash is a review trigger, not a defect or automatic score. The sealed report is preserved.",
        "coverage": {
            "day_two_training_story_shared_outputs": "Sealed777-source first pass plus unfinished nursery supplements; normal traversal and all played actions remain open.",
            "day_one_cleaning": f"Additional{day_one['watched_assets']}-file/179-drawing-function discovery census: {day_one['reused_source_opinions']} earlier byte-identical opinions, {day_one['new_source_opinions_completed']} new source opinions, {day_one['source_cells_reviewed']} source cells and{day_one['new_source_reviews_pending']} discovered-source reviews pending. Main helpers, dynamic bindings, remaining atlas cells and complete played-context review remain open; no complete census or acceptance is claimed.",
            "all_weak_live_items": "INCOMPLETE: no global4.5 pass is claimed.",
            "owner_final_report": "PENDING_APPROVAL_AFTER_COMPLETE_REPORT",
        },
        "refresh_command": "python -B tools/refresh_job_artwork_status.py --output audit/job_artwork_refinement_live/STATUS.json",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare saved status with current sources without writing.")
    parser.add_argument("--output", default=OUT.relative_to(ROOT).as_posix(),
                        help="Mutable live status or a new review snapshot; sealed earlier packets are preserved.")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to((ROOT / "audit").resolve()):
        raise SystemExit("Status output must remain inside this project's audit directory")
    if not args.check and output.is_relative_to((ROOT / "audit/job_artwork_refinement_20261001").resolve()):
        raise SystemExit("The earlier published status packet is sealed; use a new snapshot or the mutable live status")
    current = status()
    if args.check:
        saved = json.loads(output.read_text(encoding="utf-8"))
        current.pop("checked_utc")
        saved.pop("checked_utc")
        # A documentation-only commit or remote ref move does not stale captures.
        for key in ["working_head", "cached_origin_dev"]:
            current.pop(key)
            saved.pop(key)
        if saved != current:
            raise SystemExit("JOB_ART_STATUS|STALE|Run the refresh command; no scores were changed")
        print("JOB_ART_STATUS|CURRENT|Source fingerprints match saved status; acceptance remains open")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print("JOB_ART_STATUS|REFRESHED|", current["capture_freshness"], "|changed_dependencies=", len(current["changed_capture_dependencies"]))


if __name__ == "__main__":
    main()
