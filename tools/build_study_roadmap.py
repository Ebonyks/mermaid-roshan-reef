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
DECISIONS = "design/reference/owner_decisions.json"
CHECKS = "design/reference/verification_checks.json"
TERMINAL = {"VERIFIED_FIXED", "DISMISSED_NOT_A_DEFECT", "DISMISSED_NOT_IN_PROJECT", "SUPERSEDED", "DUPLICATE", "WAIVED_WITH_REASON"}
TEXT_EVIDENCE_SUFFIXES = {".md", ".gd", ".json", ".py", ".txt", ".csv", ".tsv", ".yaml", ".yml", ".toml", ".tscn", ".tres", ".gdshader", ".ps1", ".sh"}
SEVERITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
# Process findings improve how the project is built and checked; the rest are
# defects or gaps the child can meet. The owner's 2026-09-30 priority keeps the
# two orders separate.
PROCESS_PREFIXES = ("MA-DOC-", "MA-CI-", "MA-CODE-")
LIFECYCLE_LANE = {"FIXED_PENDING_VERIFICATION": "Verify", "BLOCKED_EXTERNAL": "Waiting",
                  "OWNER_DECISION_REQUIRED": "Decide", "DEFERRED_WITH_REASON": "Parked"}
PROMPT_VERBS = {"CONFIRMED_OPEN": "Fix", "IN_PROGRESS": "Finish", "REPORTED_UNCONFIRMED": "Confirm or dismiss",
                "FIXED_PENDING_VERIFICATION": "Check the fix for"}
LANE_REASONS = {"Waiting": "Waiting on evidence or people outside the project; a source change cannot close it",
                "Decide": "Owner decision required (DL-PLAN-01); asked in the cycle report, never assumed",
                "Parked": "Deferred with a recorded reason; reopen only when that reason changes"}
GROW_INTENTS = (("INT-ADD-JOB", "A new job the owner names: the recipe plans the room, distinct verbs, voice, save and checks."),
                ("INT-ROOM-ACTIVITY", "Something to do inside an approved castle room, with a visible change that stays."),
                ("INT-COMPANION", "A friend who follows Roshan, built from an identity sheet and a movement profile."),
                ("INT-EVENT", "A time-limited event that reuses rooms and art and adds its own save key."))
DISPLAY_LIMIT = 10


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


def cycle_date(cycle: str) -> dt.date:
    """Cycle IDs are a date with an optional suffix, for example 2026-10-03b."""
    return dt.date.fromisoformat(str(cycle)[:10])


def validate_strengths(root: Path, document: dict, check_hashes: bool = True) -> list[str]:
    """Structural errors always; hash drift only when check_hashes is set.

    Evidence files are live project documents that change often. Drift means
    "re-review this strength", reported by stale_strength_evidence() in every
    study, not a reason to fail unrelated builds.
    """
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
                if check_hashes and evidence.get("sha256") != digest:
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


def stale_strength_evidence(root: Path, document: dict) -> list[dict]:
    """Strengths whose bound evidence changed since review: re-review, never auto-trust."""
    rows: list[dict] = []
    for strength in document.get("strengths", []):
        for evidence in strength.get("evidence", []):
            path = root / evidence.get("path", "")
            if not path.is_file():
                continue
            try:
                digest = sha256(path, evidence.get("hash_mode", "raw"))
            except ValueError:
                continue
            if evidence.get("sha256") != digest:
                rows.append({"id": strength.get("id"), "tier": strength.get("tier"), "path": evidence.get("path"),
                             "reason": "evidence changed since the strength was recorded; re-review before relying on it"})
    return rows


def render_strengths(document: dict) -> str:
    lines = ["# Strengths register", "", "Status: `SUPPORTING_CURRENT`. Generated from [strengths.json](strengths.json); source hashes invalidate a candidate when its evidence changes. Each evidence row declares its hash mode: `git_canonical_lf` normalizes CRLF to LF for text sources; `raw` (also the default when omitted) hashes exact bytes. Binary evidence always retains exact-byte hashes. Changed evidence is reported by each study for re-review; it does not fail unrelated builds.", "", "Accepted entries preserve their exact owner/child scope. An accepted design constraint does not certify runtime performance, visual quality or child enjoyment. Candidate patterns may guide a recipe with their limits visible. Seed-only proposals remain proposals.", ""]
    for strength in document["strengths"]:
        lines += [f"## {strength['id']} — {strength['strength']}", "", f"Tier: **{strength['tier']}**. Scope: {strength['acceptance_scope']}", "", f"Reuse: {strength['reuse']}", "", "Evidence:", ""]
        lines += [f"- [{item['path']}](../../{item['path']}) — {item['kind']}; SHA-256 `{item['sha256']}`; hash mode `{item.get('hash_mode', 'raw')}`. {item.get('note', '')}" for item in strength["evidence"]]
        lines += ["", "References:", ""]
        lines += [f"- `{item['id']}` — [{item['path']}](../../{item['path']}). {item.get('scope', '')}" for item in strength.get("references", [])] or ["- No accepted exemplar/identity sheet claimed; see the evidence and scope above."]
        lines += ["", f"Exemplar gap: {strength.get('exemplar_gap', 'No promoted exemplar claimed.')}", ""]
    return "\n".join(lines).rstrip() + "\n"


def bare(value: str) -> str:
    return value.replace("`", "").strip()


def short_title(title: str, limit: int = 90) -> str:
    """A sayable handle for a finding: its first clause, cut at a word boundary."""
    text = bare(title).rstrip(".")
    for separator in (". ", "; ", " — ", ", but ", ", so "):
        head = text.split(separator, 1)[0]
        if 25 <= len(head) < len(text):
            text = head
            break
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text


def rank_child_impact(fields: dict[str, str]) -> tuple[int, str]:
    """Transparent text triage, never a human quality score."""
    text = fields.get("child_impact", "").lower()
    if any(word in text for word in ("lost progress", "lose progress", "punitive", "trap", "corrupt", "save loss", "soft-lock")):
        return 0, "progress/safety wording"
    if any(word in text for word in ("non-reader", "unclear", "confus", "cannot", "unreadable", "touch", "comprehension", "stuck")):
        return 1, "access/comprehension wording"
    if any(word in text for word in ("meaningful", "job", "action", "reward", "play", "agency")):
        return 2, "play/agency wording"
    return 3, "presentation/support wording"


def owner_priorities(root: Path) -> dict[str, dict]:
    """Explicit recorded owner priorities from the decision register.

    Only recorded_owner entries with priority "first" and applies_to finding IDs
    count; operating defaults and prose never reorder work.
    """
    path = root / DECISIONS
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    result: dict[str, dict] = {}
    rows = data.get("decisions", []) if isinstance(data, dict) else []
    for row in rows:
        if not isinstance(row, dict) or row.get("authority") != "recorded_owner" or row.get("priority") != "first":
            continue
        for finding in row.get("applies_to") or []:
            if isinstance(finding, str):
                result[finding] = {"decision": row.get("id"), "date": row.get("date"),
                                   "reason": f"owner priority {row.get('id')} ({row.get('date')})"}
    return result


def item_lane(identifier: str, lifecycle: str) -> str:
    if lifecycle in LIFECYCLE_LANE:
        return LIFECYCLE_LANE[lifecycle]
    return "Strengthen" if identifier.startswith(PROCESS_PREFIXES) else "Repair"


def item_prompt(identifier: str, lifecycle: str, title: str) -> str:
    handle = short_title(title)
    lane = LIFECYCLE_LANE.get(lifecycle)
    if lane == "Decide":
        return f"Decide {identifier}: {handle}"
    if lane == "Waiting":
        return f"Unblock {identifier}: {handle}"
    if lane == "Parked":
        return f"Leave {identifier} parked: {handle}"
    return f"{PROMPT_VERBS.get(lifecycle, 'Fix')} {identifier}: {handle}"


def make_repair_items(records: dict, today: dt.date, overrides: dict | None = None,
                      priorities: dict | None = None) -> list[dict]:
    """Every non-terminal finding, laned by lifecycle and ranked transparently.

    Order: recorded owner priority, then severity, then child-impact wording,
    then directed dependencies, then age since the last dated history entry.
    """
    overrides = overrides or {}
    priorities = priorities or {}
    items: list[dict] = []
    for identifier, fields in records.items():
        lifecycle = bare(fields.get("lifecycle", ""))
        if lifecycle in TERMINAL:
            continue
        dates = re.findall(r"20\d\d-\d\d-\d\d", fields.get("history", ""))
        last = max(dates) if dates else None
        age = (today - dt.date.fromisoformat(last)).days if last else None
        child_rank, child_reason = rank_child_impact(fields)
        priority = priorities.get(identifier)
        override = overrides.get(identifier, {})
        dependencies = override.get("depends_on", [])
        severity = bare(fields.get("severity", "")).split(" ", 1)[0] or "unspecified"
        lane = item_lane(identifier, lifecycle)
        item = {"id": identifier, "title": fields.get("title", identifier), "lifecycle": lifecycle,
                "severity": severity, "lane": lane, "prompt": item_prompt(identifier, lifecycle, fields.get("title", identifier)),
                "child_rank": child_rank, "child_reason": child_reason,
                "owner_rank": override.get("owner_priority", 0 if priority else 1),
                "owner_reason": priority["reason"] if priority else "no recorded owner priority",
                "depends_on": dependencies, "dependency_reason": "explicit study override" if dependencies else "No directed dependency supplied; relationships are context, not an inferred blocker.",
                "age_days": age, "last_history": last, "source": f"{FINDINGS}#{identifier.lower()}"}
        if lane in LANE_REASONS:
            item["reason"] = LANE_REASONS[lane]
        else:
            item["recipe"] = "REC-REPAIR"
        items.append(item)
    ordered = sorted(items, key=lambda item: (item["owner_rank"], SEVERITY_RANK.get(item["severity"], 9), item["child_rank"],
                                              len(item["depends_on"]), -(item["age_days"] or 0), item["id"]))
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
        dates = re.findall(r"20\d\d-\d\d-\d\d", fields.get("history", ""))
        last = max(dates) if dates else None
        rows.append({"id": identifier, "title": fields.get("title", identifier), "missing_evidence": gap,
                     "groups": groups or ["reviewer classification needed"],
                     "acceptance": fields.get("acceptance", "Not specified"), "reproduction": fields.get("reproduction", "Not specified"),
                     "age_days": (today - dt.date.fromisoformat(last)).days if last else None,
                     "source": f"{FINDINGS}#{identifier.lower()}", "lifecycle": "FIXED_PENDING_VERIFICATION"})
    return rows


def table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_scope_families(scope: str, defined_families: set[str]) -> str:
    """Display a historical bare family as a family, never invent a stable rule."""
    return re.sub(r"\bDL-([A-Z]+)\b(?![-A-Za-z0-9])", lambda match:
                  match.group(0) + "-*" if match.group(1) in defined_families else match.group(0), scope)


def load_checks(root: Path) -> dict:
    """Plain-language checks written for people; absent entries stay visible gaps."""
    path = root / CHECKS
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    checks = data.get("checks", {}) if isinstance(data, dict) else {}
    return checks if isinstance(checks, dict) else {}


def render_sweep(rows: list[dict], cycle: str, group: str | None = None, checks: dict | None = None) -> str:
    """The technical sweep keeps canonical wording; owner and device pages use plain checks."""
    checks = checks or {}
    if group is None:
        lines = [f"# Verification sweep — {cycle}", "", "Status: `SUPPORTING_CURRENT / EVIDENCE_PENDING`. Technical list for agents. **No session is scheduled**; a generated request is not a booking, review, lifecycle transition or acceptance. The plain-language pages are [OWNER_REVIEW.md](OWNER_REVIEW.md) and [DEVICE_SESSION.md](DEVICE_SESSION.md).", "", f"{len(rows)} findings wait for evidence. Missing-evidence, reproduction and acceptance text is copied verbatim from `{FINDINGS}`, including historical limits; re-read current sources before collecting evidence.", ""]
        for row in rows:
            lines += [f"## {row['id']}", "", f"Source: [{row['id']}](../../findings/ACTIVE_FINDINGS_2026-08-13.md#{row['id'].lower()}). Groups: {', '.join(row['groups'])}.", "", f"Missing: {row['missing_evidence']}", "", f"Reproduction: {row['reproduction']}", "", f"Acceptance criterion: {row['acceptance']}", "", "Result: **PENDING**. Evidence/commit/date/reviewer: **not supplied**. Lifecycle remains `FIXED_PENDING_VERIFICATION`.", ""]
        return "\n".join(lines).rstrip() + "\n"
    if group == "owner":
        selected = [row for row in rows if (checks.get(row["id"]) or {}).get("owner") or "owner" in row["groups"]]
        lines = [f"# Owner review page — {cycle}", "", "Status: `SUPPORTING_CURRENT / EVIDENCE_PENDING`. **No session is scheduled.** Pick a time in the cycle report's questions; a generated request is not a booking, and nothing is accepted until you answer. Each finding's lifecycle remains unchanged until all its required evidence exists.", "",
                 "Play the newest dev build on the family phone (bookmark: `android-dev` release). Never install an older build over a newer one. For each line, note yes, no or what you saw; a short note is enough.", ""]
        for row in selected:
            text = (checks.get(row["id"]) or {}).get("owner")
            link = f"[{row['id']}](../../findings/ACTIVE_FINDINGS_2026-08-13.md#{row['id'].lower()})"
            lines.append(f"- [ ] **{link}** — {text}" if text else
                         f"- [ ] **{link}** — {short_title(row['title'])}. No plain check written yet; Claude writes one in `{CHECKS}` before the session.")
        lines += ["", f"{len(selected)} items. Technical details: [VERIFICATION_SWEEP.md](VERIFICATION_SWEEP.md). A yes moves nothing by itself; the finding records your note and its lifecycle changes only with all its required evidence."]
        return "\n".join(lines).rstrip() + "\n"
    selected = [row for row in rows if (checks.get(row["id"]) or {}).get("device") or "device" in row["groups"]]
    lines = [f"# Device session — {cycle}", "", "Status: `SUPPORTING_CURRENT / EVIDENCE_PENDING`. **No session is scheduled**; a generated request is not a booking. About 30 minutes on the family phone and, if available, the older Android phone.", "",
             "Setup: install the newest dev build from the `android-dev` release (never an older build over a newer one); note the phone model and the build number on the start screen; play at normal brightness with sound on.", ""]
    for index, row in enumerate(selected, 1):
        check = checks.get(row["id"]) or {}
        text = check.get("device")
        if text and check.get("child"):
            text += f" With your child: {check['child']}"
        link = f"[{row['id']}](../../findings/ACTIVE_FINDINGS_2026-08-13.md#{row['id'].lower()})"
        lines.append(f"{index}. **{link}** — {text}" if text else
                     f"{index}. **{link}** — {short_title(row['title'])}. No device step written yet; see the technical sweep.")
    lines += ["", "Record for each step: works / does not work / unsure, plus anything surprising. Keep any child observation private and in words only; no recordings of the child are needed.", "",
              f"{len(selected)} steps. Technical details: [VERIFICATION_SWEEP.md](VERIFICATION_SWEEP.md)."]
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


def grow_items(catalogue: dict) -> list[dict]:
    intents = {item.get("id"): item for item in catalogue.get("intents", []) if isinstance(item, dict)}
    rows = []
    for index, (intent_id, title) in enumerate(GROW_INTENTS):
        intent = intents.get(intent_id)
        if not intent or not intent.get("says") or not intent.get("recipe", {}).get("id"):
            continue
        source = ("ODR-LOOP-Q8 operating default: jobs and room activities first" if index < 2 else "prompt catalogue")
        strengths = ", ".join(intent.get("strengths", [])) or "none bound"
        rows.append({"id": f"GROW-{intent_id[4:]}", "title": title, "prompt": intent["says"][0], "recipe": intent["recipe"]["id"],
                     "source": f"{source}; strengths {strengths}; new permanent content still needs the owner's premise (DL-PLAN-01)."})
    return rows


def advisory_gap(step: dict) -> bool:
    """Retired steps are declared states, not gaps; everything else not MEASURED is a gap."""
    if step.get("status") == "MEASURED":
        return False
    return not step.get("retired")


def strengthen_items(study: dict, process: list[dict], stale: list[dict], candidates: int) -> list[dict]:
    """Owner-priority process findings, then live sensor gaps, then the remaining work."""
    rows = [item for item in process if item.get("owner_rank") == 0]
    ci = study.get("ci", {})
    if ci.get("status") not in {"MEASURED", "PARTIAL"}:
        rows.append({"id": "CI-UNMEASURED", "title": f"CI evidence for the studied head is {ci.get('status', 'NOT_MEASURED')}: {ci.get('reason', 'no exact-head run read')}.",
                     "prompt": "Study the game again once CI has finished for this head", "recipe": "REC-STUDY",
                     "source": "Advisory sensors cannot be reported without the exact-head run; nothing is assumed to pass."})
    for step in ci.get("advisory_steps", []):
        if advisory_gap(step):
            name = step.get("name", "unnamed CI advisory")
            rows.append({"id": f"ADVISORY-{name}", "title": f"{name}: {step.get('status', 'UNKNOWN')} — {step.get('reason', 'no reason recorded')}.",
                         "prompt": f"Fix the advisory check {name}", "recipe": "REC-REPAIR",
                         "source": "Exact-head CI advisory result; CI success alone is insufficient."})
    for name, sensor in sorted(study.get("sensors", {}).items()):
        status = sensor.get("status", "UNKNOWN")
        summary = sensor.get("summary", {})
        summary_status = summary.get("status") if isinstance(summary, dict) else None
        if status not in {"PASS", "ALL_OK", "OK", "MEASURED"} or summary_status in {"FAIL", "UNSATISFIED", "NOT_MEASURED"}:
            detail = f"{status}; measured summary {summary_status}" if summary_status else status
            rows.append({"id": f"SENSOR-{name}", "title": f"Sensor {name}: {detail}.", "prompt": f"Study the {name} sensor gap", "recipe": "REC-STUDY",
                         "source": str(sensor.get("reason") or "Measured summary reports open work; no passing evidence claimed.")})
    rows += [item for item in process if item.get("owner_rank") != 0]
    for item in study.get("handoffs") or study.get("loop_health", {}).get("handoffs", []):
        if item.get("status") not in {"NOT_STARTED", "PARTLY_BUILT"}:
            continue
        name = item.get("handoff") or item.get("id", "unnamed handoff")
        rows.append({"id": name, "title": f"Handoff {name} is {item.get('status')}.", "prompt": f"Study what is left in {name}",
                     "recipe": "REC-STUDY", "source": "File-presence sensor only; implementation/acceptance requires exact review."})
    library = study.get("day_two_library", {})
    if library.get("changed_watched_sources") or library.get("missing_watched_sources") or library.get("stale_items"):
        rows.append({"id": "LIBRARY-REFRESH", "title": "Day Two library sources changed since their review.", "prompt": "Study the changed Day Two library art",
                     "recipe": "REC-STUDY", "source": "Source hashes changed or are missing; previous agent scores do not transfer to new bytes."})
    for row in stale:
        rows.append({"id": f"STRENGTH-{row['id']}", "title": f"Strength {row['id']} ({row['tier']}): {row['path']} changed.",
                     "prompt": f"Study strength {row['id']} again: its evidence changed", "recipe": "REC-STUDY", "source": row["reason"]})
    rows.append({"id": "STRENGTH-REVIEW", "title": f"{candidates} candidate strengths wait for owner or child evidence.",
                 "prompt": "Review the candidate strengths", "recipe": "REC-STUDY", "source": "Candidate evidence alone does not grant owner/child acceptance."})
    return rows


def render_lane(lines: list[str], heading: str, intro: str, items: list[dict], recipes: dict, root: Path, limit: int | None) -> None:
    lines += [f"## {heading} — {len(items)}", "", intro, ""]
    if not items:
        lines += ["Nothing in this lane.", ""]
        return
    lines += ["| Item | Say | Recipe or reason | Why here |", "|---|---|---|---|"]
    shown = items if limit is None else items[:limit]
    for item in items:
        recipe = item.get("recipe")
        reason = item.get("reason")
        if not recipe and not reason:
            raise ValueError(f"{item['id']}: recipe or explicit reason required")
        if recipe and (recipe not in recipes or not (root / recipes[recipe]).is_file()):
            raise ValueError(f"{item['id']}: unresolved recipe {recipe}")
    for item in shown:
        recipe = item.get("recipe")
        label = f"`{recipe}`: `{recipes[recipe]}`" if recipe else item["reason"]
        if "lifecycle" in item:
            age = f"{item['age_days']} days since last entry" if item.get("age_days") is not None else "no dated entry"
            why = f"{item['owner_reason']}; {item['severity']} {item['lifecycle']}; {item['child_reason']}; {age}"
            if item.get("depends_on"):
                why += f"; after {', '.join(item['depends_on'])}"
            title = f"{item['id']}: {short_title(item['title'])}"
        else:
            why = item.get("source", "")
            title = f"{item['id']}: {item['title']}"
        lines.append("| " + " | ".join(table_cell(value) for value in (title, item["prompt"], label, why)) + " |")
    if limit is not None and len(items) > limit:
        rest = ", ".join(f"`{item['id']}`" for item in items[limit:])
        lines += ["", f"Also open, in order ({len(items) - limit} more): {rest}."]
    lines.append("")


def surface_table(study: dict) -> list[str]:
    surfaces = study.get("surfaces") or study.get("live_status", {}).get("surfaces", [])
    if isinstance(surfaces, dict):
        surfaces = [{"id": key, **(value if isinstance(value, dict) else {"source": value})} for key, value in surfaces.items()]
    rows = ["| Surface | Last source change | Trusted probes at the studied head | Review captures | Open findings | Visual / device / child / owner |", "|---|---|---|---|---|---|"]
    for surface in surfaces:
        if isinstance(surface, str):
            surface = {"id": surface}
        probes = surface.get("probes")
        if isinstance(probes, dict):
            probe_text = f"{probes.get('passed', 0)} of {probes.get('ran', 0)} ran clean" if probes.get("ran") else probes.get("reason", "none mapped")
        else:
            probe_text = "not measured"
        captures = surface.get("captures")
        capture_text = ", ".join(captures) if captures else "none"
        findings = surface.get("open_findings")
        finding_text = (", ".join(f"{count} {severity}" for severity, count in sorted(findings.items())) or "none") if isinstance(findings, dict) else "not measured"
        changed = surface.get("last_changed") or ("present" if surface.get("present") else "SOURCE_MISSING" if surface.get("present") is False else "not measured")
        rows.append("| " + " | ".join(table_cell(value) for value in (surface.get("name") or surface.get("id", "unnamed"), changed, probe_text, capture_text, finding_text, "PENDING; not supplied by machines")) + " |")
    if not surfaces:
        rows.append("| Current shipping surfaces | Sensor supplied no surface inventory; must be repaired | MISSING | MISSING | MISSING | PENDING |")
    return rows


def build_outputs(root: Path, study: dict, today: str | None = None) -> dict[str, str]:
    cycle = today or study.get("cycle_date") or study.get("cycle") or dt.date.today().isoformat()
    date = cycle_date(cycle)
    strengths = json.loads((root / "design/reference/strengths.json").read_text(encoding="utf-8"))
    errors = validate_strengths(root, strengths, check_hashes=False)
    if errors:
        raise ValueError("; ".join(errors))
    stale = stale_strength_evidence(root, strengths)
    catalogue = json.loads((root / "design/reference/prompt_intents.json").read_text(encoding="utf-8"))
    recipes = {item["recipe"]["id"]: item["recipe"]["path"] for item in catalogue["intents"]}
    records = split_records((root / FINDINGS).read_text(encoding="utf-8"))
    items = make_repair_items(records, date, study.get("roadmap_overrides"), owner_priorities(root))
    lanes = {lane: [item for item in items if item["lane"] == lane] for lane in ("Repair", "Verify", "Decide", "Waiting", "Parked", "Strengthen")}
    candidates = sum(row["tier"] == "candidate" for row in strengths["strengths"])
    strengthen = strengthen_items(study, lanes["Strengthen"], stale, candidates)
    grow = grow_items(catalogue)
    lines = [f"# Improvement roadmap — {cycle}", "", f"Status: `SUPPORTING_CURRENT / GENERATED_ADVISORY`. Studied head: `{study.get('studied_head') or study.get('head', 'not supplied')}`. Generated from canonical findings, the decision register, strengths and the study; never changes rules, findings, save state or images.", "",
             "Order inside each lane: recorded owner priority first, then severity (P0 to P3), then child-impact wording, then directed dependencies, then age since the last dated history entry. This is a planning aid, not an owner verdict or a quality score. Every \"Say\" line is ready to give to Claude or Codex as written.", ""]
    render_lane(lines, "Repair", "Child-facing defects that a change to the game can fix.", lanes["Repair"], recipes, root, DISPLAY_LIMIT)
    render_lane(lines, "Verify", "Fixed, waiting for a phone, owner or child check. Batched into [OWNER_REVIEW.md](OWNER_REVIEW.md) and [DEVICE_SESSION.md](DEVICE_SESSION.md).", lanes["Verify"], recipes, root, None)
    render_lane(lines, "Decide", "Waiting for an owner decision; each one is asked as a numbered question with a default.", lanes["Decide"], recipes, root, None)
    render_lane(lines, "Waiting", "Blocked by evidence or people outside the project.", lanes["Waiting"], recipes, root, None)
    render_lane(lines, "Parked", "Deferred with a recorded reason.", lanes["Parked"], recipes, root, None)
    render_lane(lines, "Strengthen", "How the project is built, checked and studied: process findings, sensors, handoffs and references.", strengthen, recipes, root, DISPLAY_LIMIT)
    render_lane(lines, "Grow", "New content. Choosing one still needs the owner's premise for anything permanent.", grow, recipes, root, None)
    sweep = verification_sweep(records, date)
    checks = load_checks(root)
    history = [f"# Generated impact history — {cycle}", "", "Status: `SUPPORTING_CURRENT / GENERATED_INDEX`. Canonical impact records and historical master text remain untouched. Order: available record date, explicit filename fallback, path; undated records last. Filename dates are not asserted completion dates. Validation strings are declarations in their original record, not re-run evidence. Bare defined DL family references display with `-*`; the source record retains its exact original scope wording.", "", "| Date / source | Record | Scope | Baseline | Declared validation |", "|---|---|---|---|---|"]
    rule_text = (root / "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md").read_text(encoding="utf-8")
    defined_families = set(re.findall(r"\bDL-([A-Z]+)-\d+\b", rule_text))
    for row in impact_history(root):
        history.append("| " + " | ".join(table_cell(value) for value in (f"{row['date'] or 'undated'} ({row.get('date_source', 'not supplied')})", row["path"], format_scope_families(row["scope"], defined_families), row.get("baseline", "Not supplied"), row["results"])) + " |")
    scorecard = [f"# Current surface evidence — {cycle}", "", "Status: `SUPPORTING_CURRENT / GENERATED_EVIDENCE_INDEX`. Machine evidence per shipping surface at the studied head. Scores are **not assessed** by file-presence or static sensors; machine evidence does not establish visual, device, child or owner quality. The sealed August scorecards keep their own build scope; historical scores are not copied to today's game.", ""]
    scorecard += surface_table(study)
    return {"ROADMAP.md": "\n".join(lines).rstrip() + "\n", "VERIFICATION_SWEEP.md": render_sweep(sweep, cycle),
            "OWNER_REVIEW.md": render_sweep(sweep, cycle, "owner", checks), "DEVICE_SESSION.md": render_sweep(sweep, cycle, "device", checks),
            "GENERATED_CHANGE_HISTORY.md": "\n".join(history).rstrip() + "\n", "CURRENT_SURFACES.md": "\n".join(scorecard).rstrip() + "\n",
            "STRENGTHS.md": render_strengths(strengths)}


def roadmap_summary(root: Path, study: dict) -> dict:
    """Lane counts and the top items, saved into study.json for the owner report."""
    records = split_records((root / FINDINGS).read_text(encoding="utf-8"))
    cycle = study.get("cycle_date") or study.get("cycle") or dt.date.today().isoformat()
    items = make_repair_items(records, cycle_date(cycle), study.get("roadmap_overrides"), owner_priorities(root))
    counts = {lane: sum(item["lane"] == lane for item in items) for lane in ("Repair", "Verify", "Decide", "Waiting", "Parked", "Strengthen")}
    top = {lane: [{"id": item["id"], "prompt": item["prompt"], "recipe": item.get("recipe"), "severity": item["severity"],
                   "owner_priority": item["owner_rank"] == 0, "reason": item.get("reason")}
                  for item in items if item["lane"] == lane][:3] for lane in ("Repair", "Verify", "Decide", "Strengthen")}
    return {"counts": counts, "top": top, "priorities": owner_priorities(root)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--study", type=Path)
    parser.add_argument("--today")
    parser.add_argument("--output", type=Path, default=Path("audit/ROADMAP.md"))
    parser.add_argument("--cycle-dir", type=Path)
    parser.add_argument("--check", action="store_true", help="Validate the strengths register; changed evidence is reported, not failed")
    parser.add_argument("--strict", action="store_true", help="With --check, also fail on changed strength evidence")
    parser.add_argument("--render-strengths", action="store_true")
    args = parser.parse_args(argv)
    try:
        document = json.loads((args.root / "design/reference/strengths.json").read_text(encoding="utf-8"))
        errors = validate_strengths(args.root, document, check_hashes=False)
        if errors:
            print("\n".join(errors))
            return 1
        if args.check:
            stale = stale_strength_evidence(args.root, document)
            for row in stale:
                print(f"STRENGTHS|STALE|{row['id']}|{row['path']}|re-review")
            if stale and args.strict:
                return 1
            print("STRENGTHS: ALL OK" if not stale else f"STRENGTHS: STRUCTURE OK; {len(stale)} evidence changes need re-review")
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
