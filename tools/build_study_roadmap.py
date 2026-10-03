#!/usr/bin/env python3
"""Generate advisory roadmap, verification batches and history from source evidence."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS = "audit/findings/ACTIVE_FINDINGS_2026-08-13.md"
TERMINAL = {"VERIFIED_FIXED", "DISMISSED_NOT_A_DEFECT", "DISMISSED_NOT_IN_PROJECT", "SUPERSEDED", "DUPLICATE", "WAIVED_WITH_REASON"}
TEXT_EVIDENCE_SUFFIXES = {".md", ".gd", ".json", ".py", ".txt", ".csv", ".tsv", ".yaml", ".yml", ".toml", ".tscn", ".tres", ".gdshader", ".ps1", ".sh"}


def sha256(path: Path, hash_mode: str = "raw") -> str:
    data = path.read_bytes()
    if hash_mode == "git_canonical_lf":
        if path.suffix.lower() not in TEXT_EVIDENCE_SUFFIXES:
            raise ValueError("git_canonical_lf is limited to declared text-source extensions")
        data = data.replace(b"\r\n", b"\n")
    elif hash_mode != "raw":
        raise ValueError(f"unknown evidence hash mode: {hash_mode}")
    return hashlib.sha256(data).hexdigest()


def split_records(text: str) -> dict[str, dict[str, str]]:
    parts = re.split(r"(?m)^## (MA-[A-Z0-9]+-\d{3})\s*$", text)
    result: dict[str, dict[str, str]] = {}
    for index in range(1, len(parts), 2):
        fields: dict[str, str] = {}
        for line in parts[index + 1].splitlines():
            match = re.match(r"^\| ([a-z_ /]+) \| (.*) \|$", line)
            if match:
                fields[match.group(1).strip()] = match.group(2).strip()
        result[parts[index]] = fields
    return result


def validate_strengths(root: Path, document: dict) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for strength in document.get("strengths", []):
        identifier = strength.get("id", "")
        if not re.fullmatch(r"S-\d+", identifier) or identifier in seen:
            errors.append(f"invalid or duplicate strength: {identifier}")
        seen.add(identifier)
        if strength.get("tier") not in {"candidate", "accepted"}:
            errors.append(f"{identifier}: invalid tier")
        if not strength.get("evidence"):
            errors.append(f"{identifier}: evidence required")
        for evidence in strength.get("evidence", []):
            path = root / evidence.get("path", "")
            if not path.is_file():
                errors.append(f"{identifier}: missing evidence {evidence.get('path')}")
            else:
                try:
                    digest = sha256(path, evidence.get("hash_mode", "raw"))
                except ValueError as error:
                    errors.append(f"{identifier}: {error}")
                    continue
                if evidence.get("sha256") != digest:
                    errors.append(f"{identifier}: evidence changed; re-review {evidence['path']}")
        if strength.get("tier") == "accepted":
            authority = strength.get("accepted_evidence")
            if not isinstance(authority, dict) or authority.get("kind") not in {"owner_rule", "owner_note", "child_observation"}:
                errors.append(f"{identifier}: accepted tier needs owner/child evidence")
            elif authority.get("path") not in [item.get("path") for item in strength.get("evidence", [])]:
                errors.append(f"{identifier}: accepted evidence must be hash-bound evidence")
        for reference in strength.get("references", []):
            if not (root / reference.get("path", "")).is_file():
                errors.append(f"{identifier}: missing reference {reference.get('path')}")
        if not strength.get("acceptance_scope") or not strength.get("reuse"):
            errors.append(f"{identifier}: acceptance scope and reuse required")
    return errors


def render_strengths(document: dict) -> str:
    lines = ["# Strengths register", "", "Status: `SUPPORTING_CURRENT`. Generated from [strengths.json](strengths.json); source hashes invalidate a candidate when its evidence changes. Each evidence row declares its hash mode: `git_canonical_lf` normalizes CRLF to LF for text sources; `raw` (also the default when omitted) hashes exact bytes. Binary evidence always retains exact-byte hashes.", "", "Accepted entries preserve their exact owner/child scope. An accepted design constraint does not certify runtime performance, visual quality or child enjoyment. Candidate patterns may guide a recipe with their limits visible. Seed-only proposals remain proposals.", ""]
    for strength in document["strengths"]:
        lines += [f"## {strength['id']} — {strength['strength']}", "", f"Tier: **{strength['tier']}**. Scope: {strength['acceptance_scope']}", "", f"Reuse: {strength['reuse']}", "", "Evidence:", ""]
        lines += [f"- [{item['path']}](../../{item['path']}) — {item['kind']}; SHA-256 `{item['sha256']}`; hash mode `{item.get('hash_mode', 'raw')}`. {item.get('note', '')}" for item in strength["evidence"]]
        lines += ["", "References:", ""]
        lines += [f"- `{item['id']}` — [{item['path']}](../../{item['path']}). {item.get('scope', '')}" for item in strength.get("references", [])] or ["- No accepted exemplar/identity sheet claimed; see the evidence and scope above."]
        lines += ["", f"Exemplar gap: {strength.get('exemplar_gap', 'No promoted exemplar claimed.')}", ""]
    return "\n".join(lines).rstrip() + "\n"


def bare(value: str) -> str:
    return value.replace("`", "").strip()


def rank_child_impact(fields: dict[str, str]) -> tuple[int, str]:
    """Transparent text triage, never a human quality score."""
    text = fields.get("child_impact", "").lower()
    if any(word in text for word in ("lost progress", "lose progress", "punitive", "trap", "corrupt", "save loss", "soft-lock")):
        return 0, "progress/safety language"
    if any(word in text for word in ("non-reader", "unclear", "confus", "cannot", "unreadable", "touch", "comprehension", "stuck")):
        return 1, "access/comprehension language"
    if any(word in text for word in ("meaningful", "job", "action", "reward", "play", "agency")):
        return 2, "play/agency language"
    return 3, "presentation/support or uncategorized language"


def rank_owner_priority(fields: dict[str, str]) -> tuple[int, str]:
    value = fields.get("owner_decision", "").lower()
    if any(word in value for word in ("owner request", "owner directs", "owner requires", "owner decision")):
        return 0, "recorded owner direction (not relative priority)"
    if value and not any(word in value for word in ("none", "pending", "unresolved")):
        return 1, "recorded authority; relative priority unspecified"
    return 2, "owner priority unspecified"


def make_repair_items(records: dict, today: dt.date, overrides: dict | None = None) -> list[dict]:
    overrides = overrides or {}
    items: list[dict] = []
    for identifier, fields in records.items():
        lifecycle = bare(fields.get("lifecycle", ""))
        if lifecycle in TERMINAL:
            continue
        dates = re.findall(r"20\d\d-\d\d-\d\d", fields.get("history", ""))
        last = max(dates) if dates else None
        age = (today - dt.date.fromisoformat(last)).days if last else None
        child_rank, child_reason = rank_child_impact(fields)
        owner_rank, owner_reason = rank_owner_priority(fields)
        override = overrides.get(identifier, {})
        dependencies = override.get("depends_on", [])
        recipe = "REC-REPAIR"
        prompt = f"Collect the missing verification evidence for {identifier}." if lifecycle == "FIXED_PENDING_VERIFICATION" else f"Repair {identifier} with the smallest source-bound change."
        items.append({"id": identifier, "title": fields.get("title", identifier), "lifecycle": lifecycle,
                      "severity": fields.get("severity", "unspecified"), "prompt": prompt, "recipe": recipe,
                      "child_rank": child_rank, "child_reason": child_reason,
                      "owner_rank": override.get("owner_priority", owner_rank), "owner_reason": owner_reason,
                      "depends_on": dependencies, "dependency_reason": "explicit study override" if dependencies else "No directed dependency supplied; relationships are context, not an inferred blocker.",
                      "age_days": age, "last_history": last, "source": f"{FINDINGS}#{identifier.lower()}"})
    ordered = sorted(items, key=lambda item: (item["child_rank"], item["owner_rank"], len(item["depends_on"]), -(item["age_days"] or 0), item["id"]))
    # Only confirmed dependency edges affect order. Cycles stay explicit and never disappear.
    pending = list(ordered)
    result: list[dict] = []
    ids = {item["id"] for item in pending}
    while pending:
        eligible = next((item for item in pending if not (set(item["depends_on"]) & ids)), None)
        if eligible is None:
            for item in pending:
                item["dependency_reason"] += " Dependency cycle/unresolved ordering; owner/agent review needed."
            result.extend(pending)
            break
        result.append(eligible)
        pending.remove(eligible)
        ids.remove(eligible["id"])
    return result


def verification_sweep(records: dict, today: dt.date) -> list[dict]:
    rows: list[dict] = []
    for identifier, fields in records.items():
        if bare(fields.get("lifecycle", "")) != "FIXED_PENDING_VERIFICATION":
            continue
        # Keep the source's missing-evidence wording verbatim. No acceptance is inferred from age or CI.
        gap = fields.get("closure", "") or fields.get("verification", "")
        if not gap:
            gap = "Canonical record supplies no closure evidence list; reviewer must specify it before closure."
        context = " ".join(fields.get(key, "") for key in ("verification", "closure", "acceptance", "surrounding_tests"))
        groups = []
        if re.search(r"owner|art acceptance|accepted.visual|listening|human", context, re.I):
            groups.append("owner")
        if re.search(r"device|phone|M11|native.aspect|touch", context, re.I):
            groups.append("device")
        if re.search(r"child|comprehen", context, re.I):
            groups.append("child")
        if re.search(r"remote|machine|CI|commit|hash|result|closure", context, re.I):
            groups.append("machine/provenance")
        rows.append({"id": identifier, "missing_evidence": gap, "groups": groups or ["reviewer classification needed"],
                     "acceptance": fields.get("acceptance", "Not specified"), "reproduction": fields.get("reproduction", "Not specified"),
                     "source": f"{FINDINGS}#{identifier.lower()}", "lifecycle": "FIXED_PENDING_VERIFICATION"})
    return rows


def table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_scope_families(scope: str, defined_families: set[str]) -> str:
    """Display a historical bare family as a family, never invent a stable rule."""
    return re.sub(r"\bDL-([A-Z]+)\b(?![-A-Za-z0-9])", lambda match:
                  match.group(0) + "-*" if match.group(1) in defined_families else match.group(0), scope)


def render_sweep(rows: list[dict], cycle: str, group: str | None = None) -> str:
    title = {None: "Verification sweep", "owner": "Owner review page", "device": "Device session"}[group]
    selected = [row for row in rows if group is None or group in row["groups"]]
    lines = [f"# {title} — {cycle}", "", "Status: `SUPPORTING_CURRENT / EVIDENCE_PENDING`. Requested monthly batch; **no session is scheduled**. Owner time and device availability need an explicit slot. A generated request is not a booking, review, lifecycle transition or acceptance.", "", f"{len(selected)} findings in this batch. Source: `{FINDINGS}`; missing-evidence text is copied from canonical closure/verification fields, including their historical limits. Re-read current sources before collecting evidence.", "", "Capture exact source commit/APK hash, device/model/OS, renderer and quality tier, date/reviewer, native aspect, actions/results, artifact hashes and owner/child verdict when applicable. Keep child observation private; no device telemetry is read by this tool.", ""]
    for row in selected:
        lines += [f"## {row['id']}", "", f"Source: [{row['id']}](../../findings/ACTIVE_FINDINGS_2026-08-13.md#{row['id'].lower()}). Groups: {', '.join(row['groups'])}.", "", f"Missing: {row['missing_evidence']}", "", f"Reproduction: {row['reproduction']}", "", f"Acceptance criterion: {row['acceptance']}", "", "Result: **PENDING**. Evidence/commit/date/reviewer: **not supplied**. Lifecycle remains `FIXED_PENDING_VERIFICATION`.", ""]
    return "\n".join(lines).rstrip() + "\n"


def impact_history(root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted((root / "design/audit_impacts").glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            rows.append({"path": path.relative_to(root).as_posix(), "id": path.stem, "date": None, "scope": "Unreadable record; needs repair", "results": "UNREADABLE"})
            continue
        # A date in the record is authority; filename date is only a declared fallback.
        date = record.get("date")
        date_source = "record.date" if date else "not supplied"
        if not date:
            match = re.search(r"(20\d{2})-?(\d{2})-?(\d{2})", path.stem)
            if match:
                date = "-".join(match.groups())
                date_source = "filename; not asserted completion date"
        rows.append({"path": path.relative_to(root).as_posix(), "id": record.get("id", path.stem), "date": date,
                     "date_source": date_source, "scope": record.get("scope", "No scope supplied"), "baseline": record.get("baseline", "Not supplied"),
                     "results": ", ".join(str(item.get("result", "UNSPECIFIED")) for item in record.get("validation", [])) or "No validation supplied"})
    return sorted(rows, key=lambda row: (row["date"] is None, row["date"] or "", row["path"]))


def build_outputs(root: Path, study: dict, today: str | None = None) -> dict[str, str]:
    cycle = today or study.get("cycle_date") or study.get("cycle") or dt.date.today().isoformat()
    date = dt.date.fromisoformat(cycle)
    strengths = json.loads((root / "design/reference/strengths.json").read_text(encoding="utf-8"))
    errors = validate_strengths(root, strengths)
    if errors:
        raise ValueError("; ".join(errors))
    catalogue = json.loads((root / "design/reference/prompt_intents.json").read_text(encoding="utf-8"))
    recipes = {item["recipe"]["id"]: item["recipe"]["path"] for item in catalogue["intents"]}
    records = split_records((root / FINDINGS).read_text(encoding="utf-8"))
    repair = make_repair_items(records, date, study.get("roadmap_overrides"))
    grow = [
        {"id": "GROW-JOBS", "title": "Plan the next owner-chosen job using truthful action and distinct verbs.", "prompt": "Plan an owner-chosen job, such as a bakery job.", "recipe": "REC-ADD-JOB", "source": "ODR-LOOP-Q8 operating default; S-02 candidate, S-12 candidate; premise/home reserved."},
        {"id": "GROW-ROOM", "title": "Plan a room activity around a visible, persistent change.", "prompt": "Plan a rainy-day activity inside an approved castle room.", "recipe": "REC-ROOM-ACTIVITY", "source": "ODR-LOOP-Q8 operating default; S-03 candidate, S-08 candidate; new permanent premise reserved."},
    ]
    strengthen: list[dict] = []
    handoffs = study.get("handoffs") or study.get("loop_health", {}).get("handoffs", [])
    for item in handoffs:
        if item.get("status") in {"BUILT", "not tracked by this script"}:
            continue
        name = item.get("handoff") or item.get("id", "unnamed handoff")
        strengthen.append({"id": name, "title": f"Review implementation gaps: {name} ({item.get('status', 'UNKNOWN')}).", "prompt": f"Study and scope the remaining packages in {name}.", "recipe": "REC-STUDY", "source": "File-presence sensor only; implementation/acceptance requires exact review."})
    for name, sensor in sorted(study.get("sensors", {}).items()):
        status = sensor.get("status", "UNKNOWN")
        summary = sensor.get("summary", {})
        summary_status = summary.get("status") if isinstance(summary, dict) else None
        if status not in {"PASS", "ALL_OK", "OK", "MEASURED"} or summary_status in {"FAIL", "UNSATISFIED", "NOT_MEASURED"}:
            detail = f"{status}; measured summary {summary_status}" if summary_status else status
            strengthen.append({"id": f"SENSOR-{name}", "title": f"Resolve sensor evidence gap {name}: {detail}.", "prompt": f"Study and repair the {name} evidence gap.", "recipe": "REC-STUDY", "source": str(sensor.get("reason") or summary or "No result supplied; no passing evidence claimed.")})
    for step in study.get("ci", {}).get("advisory_steps", []):
        if step.get("status") != "MEASURED":
            name = step.get("name", "unnamed CI advisory")
            strengthen.append({"id": f"ADVISORY-{name}", "title": f"Collect valid advisory evidence for {name}: {step.get('status', 'UNKNOWN')}.", "prompt": f"Study and repair the {name} advisory evidence gap.", "recipe": "REC-STUDY", "source": str(step.get("reason") or "No complete advisory evidence supplied; CI success is insufficient.")})
    library = study.get("day_two_library", {})
    if library.get("changed_watched_sources") or library.get("missing_watched_sources") or library.get("stale_items"):
        strengthen.append({"id": "LIBRARY-REFRESH", "title": "Refresh changed or missing Day Two library references.", "prompt": "Study the changed Day Two library sources and refresh their scoped reviews.", "recipe": "REC-STUDY", "source": "Source hashes changed or are missing; previous agent scores do not transfer to new bytes."})
    pending_strengths = [row for row in strengths["strengths"] if row["tier"] == "candidate"]
    strengthen.append({"id": "STRENGTH-REVIEW", "title": f"Review {len(pending_strengths)} source-bound candidate strengths before promoting any exemplar.", "prompt": "Review the candidate strengths and collect the missing acceptance evidence.", "recipe": "REC-STUDY", "source": "Candidate evidence alone does not grant owner/child acceptance."})
    lines = [f"# Improvement roadmap — {cycle}", "", f"Status: `SUPPORTING_CURRENT / GENERATED_ADVISORY`. Studied head: `{study.get('studied_head') or study.get('head', 'not supplied')}`. Generated from canonical findings, strengths and the study; never changes rules, findings, save state or images.", "", "Repair ordering: transparent text triage of child impact, recorded owner direction, explicit directed dependencies supplied by the study, then age since the last dated history entry. This is a planning heuristic, not an owner priority verdict or quality score. Relationships are not silently converted into dependencies; unspecified dependencies remain review work. Grow uses the stated jobs/room-activities operating default; choosing it still requires the recipe's reserved premise decision.", ""]
    for heading, items in (("Repair", repair), ("Grow", grow), ("Strengthen", strengthen)):
        lines += [f"## {heading}", "", "| Item | One-line prompt | Recipe | Evidence / ordering / limits |", "|---|---|---|---|"]
        for item in items:
            recipe = item.get("recipe")
            reason = item.get("reason")
            if not recipe and not reason:
                raise ValueError(f"{item['id']}: recipe or explicit reason required")
            if recipe and (recipe not in recipes or not (root / recipes[recipe]).is_file()):
                raise ValueError(f"{item['id']}: unresolved recipe {recipe}")
            label = f"`{recipe}`: `{recipes[recipe]}`" if recipe else reason
            detail = item.get("source", "")
            if heading == "Repair":
                detail += f"; {item['severity']} / {item['lifecycle']}; {item['child_reason']}; {item['owner_reason']}; age {item['age_days'] if item['age_days'] is not None else 'unknown'} days; dependencies {', '.join(item['depends_on']) or 'unspecified'} ({item['dependency_reason']})"
            lines.append("| " + " | ".join(table_cell(value) for value in (f"{item['id']}: {item['title']}", item["prompt"], label, detail)) + " |")
        lines += [""]
    sweep = verification_sweep(records, date)
    history = [f"# Generated impact history — {cycle}", "", "Status: `SUPPORTING_CURRENT / GENERATED_INDEX`. Canonical impact records and historical master text remain untouched. Order: available record date, explicit filename fallback, path; undated records last. Filename dates are not asserted completion dates. Validation strings are declarations in their original record, not re-run evidence. Bare defined DL family references display with `-*`; the source record retains its exact original scope wording.", "", "| Date / source | Record | Scope | Baseline | Declared validation |", "|---|---|---|---|---|"]
    rule_text = (root / "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md").read_text(encoding="utf-8")
    defined_families = set(re.findall(r"\bDL-([A-Z]+)-\d+\b", rule_text))
    for row in impact_history(root):
        history.append("| " + " | ".join(table_cell(value) for value in (f"{row['date'] or 'undated'} ({row.get('date_source', 'not supplied')})", row["path"], format_scope_families(row["scope"], defined_families), row.get("baseline", "Not supplied"), row["results"])) + " |")
    surfaces = study.get("surfaces") or study.get("live_status", {}).get("surfaces", [])
    scorecard = [f"# Current surface evidence — {cycle}", "", "Status: `SUPPORTING_CURRENT / GENERATED_EVIDENCE_INDEX`. Scores are **not assessed** by file-presence or static sensors. Machine evidence does not establish visual, device, child or owner quality. These current surfaces supplement the sealed August scorecards; historical scores are not copied to today's game.", "", "| Surface | Source / measurement | Machine status | Visual / device / child / owner |", "|---|---|---|---|"]
    if isinstance(surfaces, dict):
        surfaces = [{"id": key, **(value if isinstance(value, dict) else {"source": value})} for key, value in surfaces.items()]
    for surface in surfaces:
        if isinstance(surface, str):
            surface = {"id": surface}
        machine = surface.get("status", "Source present; runtime not assessed" if surface.get("present") else "SOURCE_MISSING" if surface.get("present") is False else "Not assessed")
        scorecard.append("| " + " | ".join(table_cell(value) for value in (surface.get("name") or surface.get("id", "unnamed"), surface.get("source") or surface.get("path") or surface.get("sources", "Not supplied"), machine, "PENDING / not supplied by this study")) + " |")
    if not surfaces:
        scorecard.append("| Current shipping surfaces | Sensor supplied no surface inventory; must be repaired | MISSING | PENDING |")
    return {"ROADMAP.md": "\n".join(lines).rstrip() + "\n", "VERIFICATION_SWEEP.md": render_sweep(sweep, cycle),
            "OWNER_REVIEW.md": render_sweep(sweep, cycle, "owner"), "DEVICE_SESSION.md": render_sweep(sweep, cycle, "device"),
            "GENERATED_CHANGE_HISTORY.md": "\n".join(history).rstrip() + "\n", "CURRENT_SURFACES.md": "\n".join(scorecard).rstrip() + "\n",
            "STRENGTHS.md": render_strengths(strengths)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--study", type=Path)
    parser.add_argument("--today")
    parser.add_argument("--output", type=Path, default=Path("audit/ROADMAP.md"))
    parser.add_argument("--cycle-dir", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--render-strengths", action="store_true")
    args = parser.parse_args(argv)
    try:
        document = json.loads((args.root / "design/reference/strengths.json").read_text(encoding="utf-8"))
        errors = validate_strengths(args.root, document)
        if errors:
            print("\n".join(errors))
            return 1
        if args.check:
            print("STRENGTHS: ALL OK")
            return 0
        if args.render_strengths:
            (args.root / "design/reference/STRENGTHS.md").write_text(render_strengths(document), encoding="utf-8", newline="\n")
            print("Rendered strengths register")
            return 0
        if not args.study:
            parser.error("--study required for roadmap generation")
        study_path = args.study if args.study.is_absolute() else args.root / args.study
        outputs = build_outputs(args.root, json.loads(study_path.read_text(encoding="utf-8")), args.today)
        output_path = args.output if args.output.is_absolute() else args.root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(outputs["ROADMAP.md"], encoding="utf-8", newline="\n")
        if args.cycle_dir:
            cycle_dir = args.cycle_dir if args.cycle_dir.is_absolute() else args.root / args.cycle_dir
            cycle_dir.mkdir(parents=True, exist_ok=True)
            for name, text in outputs.items():
                if name != "STRENGTHS.md":
                    (cycle_dir / name).write_text(text, encoding="utf-8", newline="\n")
        print("ROADMAP: ALL OK (generated advisory only; sessions unscheduled)")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ROADMAP: FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
