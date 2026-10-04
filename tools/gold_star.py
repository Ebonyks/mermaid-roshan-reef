#!/usr/bin/env python3
"""Gold star: rate every child-facing game against one rubric and one reference.

`design/reference/games.json` catalogues each game: its own runtime sources,
host, route, trusted probes, game-specific findings, and Claude's assessed
scores for criteria C1-C10, bound to hashes of the code they judged. C11 (open
defects) and C12 (device, child and owner acceptance) are computed here from the
finding register, the owner-decision register and recorded acceptance evidence.
`design/reference/gold_star.json` holds the rubric, the rating rule, the
reference game whose patterns new work copies, and the coverage globs that keep
every new game file inside the rubric.

Machine signals never raise a score. They only mark an assessment stale, so a
person or agent re-assesses it (DL-QA-01, DL-QA-07). A rating of 5 needs every
criterion at 2, which includes recorded device, child and owner acceptance.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    from tools.audit_game_2d import _token_counts as game_2d_token_counts
    from tools.audit_probe_parity import _loop_names
    from tools.build_study_roadmap import SEVERITY_RANK, TEXT_EVIDENCE_SUFFIXES, sha256, split_records
except ModuleNotFoundError:
    from audit_game_2d import _token_counts as game_2d_token_counts
    from audit_probe_parity import _loop_names
    from build_study_roadmap import SEVERITY_RANK, TEXT_EVIDENCE_SUFFIXES, sha256, split_records

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = "design/reference/games.json"
RUBRIC = "design/reference/gold_star.json"
PAGE = "design/reference/GOLD_STAR.md"
FINDINGS = "audit/findings/ACTIVE_FINDINGS_2026-08-13.md"
DESIGN = "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md"
DECISIONS = "design/reference/owner_decisions.json"
MANIFEST = "tools/game_2d_migration_manifest.json"
CI = "scripts/ci.sh"
OVERDRAW = "design/reference/overdraw.json"
OD_CHECKS = ("OD1", "OD2", "OD3", "OD4", "OD5", "OD6")
OD_RESULTS = ("pass", "fail", "not_measured")
OD_REVIEWED = ("OD1", "OD2")
DRAWING_ROLES = ("wash", "ambient", "stand_in", "guide", "effect", "child_mark", "ui")
DEFAULT_CORE = ("C1", "C3", "C4", "C5", "C6")

ASSESSED = tuple(f"C{number}" for number in range(1, 11))
COMPUTED = ("C11", "C12")
CRITERIA = ASSESSED + COMPUTED
ACCEPTANCE_LANES = ("device", "child", "owner")
FAMILIES = ("opera_career", "day_one", "chapter_two", "picture_game", "minigame", "world", "action", "system")
STATES = ("live", "dormant", "debug_only", "retired")
# Lifecycles that still describe a defect the child can meet. A fix awaiting
# device, child or owner evidence belongs to C12 instead; a decision, a block
# or an unconfirmed report caps C11 at 1 without counting as a confirmed defect.
DEFECT = {"CONFIRMED_OPEN", "IN_PROGRESS", "REGRESSED"}
UNSETTLED = {"REPORTED_UNCONFIRMED", "OWNER_DECISION_REQUIRED", "BLOCKED_EXTERNAL", "DEFERRED_WITH_REASON"}
PENDING = {"FIXED_PENDING_VERIFICATION"}
RULE_RE = re.compile(r"`(DL-[A-Z0-9]+-\d{2})`")
SCORE_VALUES = (0, 1, 2)
RATING_WORDS = {5: "gold star", 4: "strong", 3: "workable", 2: "major repair", 1: "absent or unsuitable"}


class GoldStarError(ValueError):
    """The catalogue or rubric cannot be read."""


def read_json(root: Path, relative: str) -> dict:
    path = root / relative
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise GoldStarError(f"{relative}: {error}") from error
    if not isinstance(data, dict):
        raise GoldStarError(f"{relative}: top level is not an object")
    return data


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*]", "", value or "")).strip()


def first_word(value: str | None) -> str:
    text = clean(value)
    return text.split(" ")[0] if text else ""


def declaration_text(text: str, name: str, kind: str = "func") -> str | None:
    """Return one top-level GDScript function or constant, up to the next top-level declaration.

    Comment lines stay with the declaration above them, so editing the comment
    that introduces the next one also marks this one for re-review: a
    conservative choice for evidence binding.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    if kind == "func":
        signature = re.compile(rf"^(?:static\s+)?func\s+{re.escape(name)}\s*\(")
    else:
        signature = re.compile(rf"^const\s+{re.escape(name)}\b")
    start = None
    for index, line in enumerate(lines):
        if start is None:
            if signature.match(line):
                start = index
        elif line and not line[0].isspace() and not line.startswith("#") and not line.startswith(("]", "}", ")")):
            return "\n".join(lines[start:index]).rstrip() + "\n"
    return "\n".join(lines[start:]).rstrip() + "\n" if start is not None else None


def func_text(text: str, name: str) -> str | None:
    return declaration_text(text, name, "func")


def entry_text(block: str, key: str) -> str | None:
    """Return `"key": value` from a dictionary literal, matching brackets outside strings."""
    match = re.search(rf'"{re.escape(key)}"\s*:\s*', block)
    if not match:
        return None
    start = index = match.end()
    if index >= len(block) or block[index] not in "[{":
        end = block.find("\n", index)
        return block[match.start():end if end >= 0 else len(block)].rstrip().rstrip(",")
    depth, quote = 0, ""
    while index < len(block):
        char = block[index]
        if quote:
            if char == "\\":
                index += 1
            elif char == quote:
                quote = ""
        elif char in "\"'":
            quote = char
        elif char in "[{(":
            depth += 1
        elif char in "]})":
            depth -= 1
            if depth == 0:
                return block[match.start():index + 1]
        index += 1
    return None if start == index else None


def anchor_text(text: str, anchor: dict) -> str | None:
    if anchor.get("func"):
        return func_text(text, str(anchor["func"]))
    if anchor.get("const"):
        block = declaration_text(text, str(anchor["const"]), "const")
        if block is None or not anchor.get("key"):
            return block
        return entry_text(block, str(anchor["key"]))
    return None


def anchor_hash(root: Path, anchor: dict) -> str | None:
    """Hash one evidence anchor: a whole file, a function, a constant, or one entry of a constant."""
    path = root / str(anchor.get("path", ""))
    if not path.is_file():
        return None
    if anchor.get("func") or anchor.get("const"):
        body = anchor_text(path.read_text(encoding="utf-8", errors="replace"), anchor)
        return hashlib.sha256(body.encode("utf-8")).hexdigest() if body is not None else None
    mode = "git_canonical_lf" if path.suffix.lower() in TEXT_EVIDENCE_SUFFIXES else "raw"
    return sha256(path, mode)


def anchor_label(anchor: dict) -> str:
    if anchor.get("func"):
        return f"{anchor.get('path')}::{anchor['func']}"
    if anchor.get("const"):
        return f"{anchor.get('path')}::{anchor['const']}" + (f"[{anchor['key']}]" if anchor.get("key") else "")
    return str(anchor.get("path"))


def defined_rules(root: Path) -> set[str]:
    path = root / DESIGN
    return set(RULE_RE.findall(path.read_text(encoding="utf-8"))) if path.is_file() else set()


def trusted_probes(root: Path) -> set[str]:
    path = root / CI
    names = _loop_names(path.read_text(encoding="utf-8")) if path.is_file() else None
    return set(names or [])


def debt_by_file(root: Path) -> dict[str, int]:
    manifest = read_json(root, MANIFEST)
    debt: dict[str, int] = {}
    for path, tokens in (manifest.get("production_3d_files") or {}).items():
        debt[path] = sum(value for value in tokens.values() if isinstance(value, int)) if isinstance(tokens, dict) else 0
    return debt


def finding_states(root: Path) -> dict[str, dict]:
    path = root / FINDINGS
    records = split_records(path.read_text(encoding="utf-8")) if path.is_file() else {}
    return {identifier: {"severity": first_word(fields.get("severity")),
                         "lifecycle": first_word(fields.get("lifecycle")),
                         "title": clean(fields.get("title"))}
            for identifier, fields in records.items()}


def owner_verdicts(root: Path) -> list[dict]:
    path = root / DECISIONS
    if not path.is_file():
        return []
    return list(read_json(root, DECISIONS).get("decisions", []))


def compute_c11(game: dict, findings: dict[str, dict]) -> tuple[int, str]:
    """2 = no open defect; 1 = only P2/P3 defects or unsettled items; 0 = an open P0/P1 defect."""
    worst, notes = 2, []
    for identifier in game.get("findings", []):
        state = findings.get(identifier)
        if not state:
            continue
        lifecycle, severity = state["lifecycle"], state["severity"]
        if lifecycle in DEFECT:
            level = 0 if SEVERITY_RANK.get(severity, 9) <= 1 else 1
        elif lifecycle in UNSETTLED:
            level = 1
        else:
            continue
        worst = min(worst, level)
        notes.append(f"{identifier} {severity} {lifecycle}")
    return worst, "; ".join(notes) or "No open game-specific defect in the finding register"


def compute_c12(game: dict, findings: dict[str, dict]) -> tuple[int, str]:
    """2 = device, child and owner acceptance recorded; 1 = some; 0 = none, or a lane did not accept."""
    acceptance = game.get("acceptance") or {}
    pending = [identifier for identifier in game.get("findings", [])
               if findings.get(identifier, {}).get("lifecycle") in PENDING]
    suffix = f"; pending verification: {', '.join(pending)}" if pending else ""
    refused = [f"{lane} ({acceptance[lane].get('evidence')})" for lane in ACCEPTANCE_LANES
               if isinstance(acceptance.get(lane), dict) and acceptance[lane].get("result") == "not_accepted"]
    if refused:
        return 0, "Not accepted by " + ", ".join(refused) + suffix
    recorded = [lane for lane in ACCEPTANCE_LANES
                if isinstance(acceptance.get(lane), dict) and acceptance[lane].get("result") == "accepted"]
    if len(recorded) == len(ACCEPTANCE_LANES):
        return 2, "Device, child and owner acceptance recorded" + suffix
    if recorded:
        missing = ", ".join(lane for lane in ACCEPTANCE_LANES if lane not in recorded)
        return 1, f"Accepted by {', '.join(recorded)}; still needed: {missing}" + suffix
    return 0, "No device, child or owner acceptance recorded" + suffix


def load_measurements(root: Path) -> dict:
    path = root / OVERDRAW
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise GoldStarError(f"{OVERDRAW}: invalid JSON: {error}") from error


def stale_inputs(root: Path, record: dict) -> list[str]:
    """Files whose content changed since the overdraw measurement was taken."""
    return sorted(path for path, digest in (record.get("inputs") or {}).items()
                  if anchor_hash(root, {"path": path}) != digest)


def stale_drawing(root: Path, rubric: dict) -> list[str]:
    return [entry["path"] for entry in (rubric.get("overdraw") or {}).get("code_drawing", [])
            if anchor_hash(root, {"path": entry.get("path", "")}) != entry.get("sha256")]


def overdraw_results(root: Path, rubric: dict, measurements: dict, game: dict) -> dict[str, dict]:
    """Derive OD1-OD6 for one game from measurements, the drawing classification and reviews.

    A missing, stale or unclassified measurement is `not_measured`, never a pass.
    """
    spec = rubric.get("overdraw") or {}
    budgets = spec.get("budgets") or {}
    results = {check: {"result": "not_measured", "detail": "No overdraw measurement for this game."} for check in OD_CHECKS}
    reviews = game.get("overdraw_review") or {}
    record = (measurements.get("games") or {}).get(game.get("id"))
    if record:
        changed = stale_inputs(root, record)
        if changed:
            detail = "Measurement is stale; re-measure after: " + ", ".join(changed[:4])
            results = {check: {"result": "not_measured", "detail": detail} for check in OD_CHECKS}
            record = None
    if record:
        skip = set(spec.get("states_not_budgeted", []))
        states = {name: state for name, state in (record.get("states") or {}).items() if name not in skip}
        classified = {entry["path"]: entry for entry in spec.get("code_drawing", [])}
        unreliable = set(stale_drawing(root, rubric))
        duplicates = [f"{name}: {' and '.join(d.get('names', []))}" for name, state in states.items()
                      for d in state.get("duplicates", [])]
        results["OD1"] = ({"result": "fail", "detail": "Drawn twice over itself: " + "; ".join(duplicates[:4])} if duplicates
                          else {"result": "not_measured", "detail": "No on-screen duplicate; the painted-copy review is still needed."})
        drawn = sorted({path for state in states.values() for path in state.get("code_drawing", [])})
        unknown = [path for path in drawn if path not in classified or path in unreliable]
        refused = [path for path in drawn if path in classified and path not in unreliable and not classified[path].get("allowed")]
        if refused:
            results["OD3"] = {"result": "fail", "detail": "; ".join(
                f"{path.split('/')[-1]}: {classified[path]['draws'].rstrip('.')}" for path in refused) + "."}
        elif unknown:
            results["OD3"] = {"result": "not_measured", "detail": "Classify what these scripts draw: " + ", ".join(unknown)}
        else:
            results["OD3"] = {"result": "pass", "detail": "No code-drawn shapes on screen outside allowed child marks."}
        slow, covering, lingering = [], [], []
        for name, effect in (record.get("effects") or {}).items():
            for item in effect.get("transient", []):
                if float(item.get("seconds") or 0.0) > float(budgets.get("effect_seconds", 1.0)):
                    slow.append(f"{item['name']} ({name}, {item['seconds']} s)")
                if float(item.get("over_roshan_share") or 0.0) > float(budgets.get("effect_over_roshan", 0.25)):
                    covering.append(f"{item['name']} ({name})")
            lingering += [f"{item['name']} ({name})" for item in effect.get("lingering_translucent", [])]
        problems = ([f"slow: {', '.join(slow)}"] if slow else []) + ([f"over Roshan: {', '.join(covering)}"] if covering else []) \
            + ([f"left over finished work: {', '.join(lingering)}"] if lingering else [])
        results["OD4"] = ({"result": "fail", "detail": "; ".join(problems)} if problems
                          else {"result": "pass", "detail": "Effects clear within the budget and stay off Roshan."}
                          if record.get("effects") else {"result": "not_measured", "detail": "No action effects measured."})
        has_gpu = bool(states) and all(state.get("gpu") for state in states.values())
        washed = [name for name, state in states.items()
                  if has_gpu and int(state["gpu_translucent"].get("p50", 0)) > int(budgets.get("translucent_p50", 0))]
        washes = [f"a translucent layer lies under at least half the screen in {', '.join(washed)}"] if washed else []
        washes += [f"{overlay['name']} covers {overlay.get('screen_share')} of the screen in {name}"
                   for name, state in states.items() for overlay in state.get("broad_overlays", [])]
        results["OD5"] = ({"result": "fail", "detail": sentence("; ".join(washes[:4]))} if washes
                          else {"result": "pass", "detail": "No broad translucent layer."} if has_gpu
                          else {"result": "not_measured", "detail": "No GPU layer count."})
        heavy = []
        for name, state in states.items():
            gpu = state.get("gpu") or {}
            over = [label for label, value, limit in (
                ("mean", gpu.get("mean"), budgets.get("mean_layers", 2.5)),
                ("4+ layers", gpu.get("share_ge4"), budgets.get("share_ge4", 0.10)),
                ("max", gpu.get("max"), budgets.get("max_layers", 8)),
                ("peak", state.get("gpu_peak"), budgets.get("peak_layers", 32)))
                if value is not None and float(value) > float(limit)]
            if over:
                heavy.append((float(gpu.get("mean") or 0.0),
                              f"{name} (mean {gpu.get('mean')} layers, {round(100 * float(gpu.get('share_ge4') or 0))}% with 4+, "
                              f"max {gpu.get('max')}, peak {state.get('gpu_peak')})"))
        wasted = sorted({layer["name"] for state in states.values() for layer in state.get("wasted_layers", [])})
        problems = ([f"over budget in {len(heavy)} play state(s), worst {max(heavy)[1]}"] if heavy else []) \
            + (["drawn while hidden under opaque art: " + ", ".join(wasted)] if wasted else [])
        results["OD6"] = ({"result": "fail", "detail": sentence("; ".join(problems))} if problems
                          else {"result": "pass", "detail": "Within the fill budget with no wasted layers."} if has_gpu
                          else {"result": "not_measured", "detail": "No GPU layer count."})
        results["OD2"] = {"result": "not_measured", "detail": "Look-alike review not recorded."}
    # OD1 needs both the machine count and the painted-copy review; OD2 is review only.
    for check in OD_REVIEWED:
        review = reviews.get(check)
        if not isinstance(review, dict) or results[check]["result"] == "fail":
            continue
        if review.get("result") == "fail":
            results[check] = {"result": "fail", "detail": f"Review: {review.get('evidence')}"}
        elif review.get("result") == "pass" and (check == "OD2" or record):
            results[check] = {"result": "pass", "detail": f"Reviewed: {review.get('evidence')}"}
    return results


def sentence(text: str) -> str:
    return (text[:1].upper() + text[1:]).rstrip(".") + "."


def overdraw_ok(results: dict[str, dict]) -> bool:
    return bool(results) and all(entry["result"] == "pass" for entry in results.values())


def derive_rating(scores: dict[str, int], p0_open: bool = False, overdraw_passed: bool = True,
                  core: tuple[str, ...] = ()) -> tuple[int, str]:
    """Turn twelve 0-2 scores into the master audit's 1-5 scale, deterministically.

    An open game-specific P0 blocker caps the rating at 2 (master audit 2.3:
    a primary path is unavailable). A 4 also needs every core criterion at 2
    and every overdraw check passed (refined 2026-10-04).
    """
    assessed = [scores[key] for key in ASSESSED]
    zeros = [key for key in ASSESSED[1:] if scores[key] == 0]
    partial = [key for key in ASSESSED if scores[key] == 1]
    short_core = [key for key in core if scores.get(key, 0) < 2]
    if all(scores[key] == 2 for key in CRITERIA) and not p0_open and overdraw_passed:
        return 5, "Every criterion meets the gold star, including device, child and owner acceptance"
    if scores["C1"] == 0:
        return 1, "A child cannot reach it in normal play"
    if len(zeros) >= 2:
        return 2, "Fails " + ", ".join(zeros) + ("; an open P0 blocker" if p0_open else "")
    if p0_open:
        return 2, "An open P0 blocker" + (f"; fails {zeros[0]}" if zeros else "")
    if zeros or scores["C11"] == 0 or len(partial) > 2 or short_core or not overdraw_passed:
        reasons = [f"fails {zeros[0]}"] if zeros else []
        if scores["C11"] == 0:
            reasons.append("an open P0/P1 defect")
        if len(partial) > 2:
            reasons.append(f"{len(partial)} criteria only partly met")
        if short_core and not zeros:
            reasons.append("core " + ", ".join(short_core) + " below the gold star")
        if not overdraw_passed:
            reasons.append("overdraw checks not all passed")
        return 3, "Workable: " + "; ".join(reasons)
    if min(assessed) >= 1:
        return 4, "Strong: what remains is " + (", ".join(partial) + " and " if partial else "") + "device, child and owner gates"
    return 3, "Workable"


def game_scores(game: dict, findings: dict[str, dict]) -> tuple[dict[str, int], dict[str, str]]:
    scores, notes = {}, {}
    for key in ASSESSED:
        entry = (game.get("scores") or {}).get(key) or {}
        scores[key] = int(entry.get("score", 0)) if entry.get("score") in SCORE_VALUES else 0
        notes[key] = str(entry.get("note", ""))
    scores["C11"], notes["C11"] = compute_c11(game, findings)
    scores["C12"], notes["C12"] = compute_c12(game, findings)
    return scores, notes


def evaluate(root: Path, catalogue: dict, rubric: dict) -> list[dict]:
    findings = finding_states(root)
    debt = debt_by_file(root)
    trusted = trusted_probes(root)
    measurements = load_measurements(root) if rubric.get("overdraw") else {}
    core = tuple(rubric.get("core") or ()) if rubric.get("overdraw") else ()
    rows = []
    for game in catalogue.get("games", []):
        scores, notes = game_scores(game, findings)
        p0_open = any(findings.get(identifier, {}).get("lifecycle") in DEFECT
                      and findings.get(identifier, {}).get("severity") == "P0"
                      for identifier in game.get("findings", []))
        overdraw = overdraw_results(root, rubric, measurements, game) if rubric.get("overdraw") else {}
        passed = overdraw_ok(overdraw) if overdraw else True
        if overdraw and not passed and scores["C7"] > 1:
            scores["C7"] = 1
            notes["C7"] += " Capped at 1: the overdraw checks are not all passed."
        rating, reason = derive_rating(scores, p0_open, passed, core)
        stale = [anchor_label(anchor) for anchor in game.get("evidence", [])
                 if anchor_hash(root, anchor) != anchor.get("sha256")]
        open_defects = [identifier for identifier in game.get("findings", [])
                        if findings.get(identifier, {}).get("lifecycle") in DEFECT]
        rows.append({
            "id": game["id"], "name": game.get("name", game["id"]), "family": game.get("family"),
            "state": game.get("state"), "scores": scores, "notes": notes,
            "points": sum(scores.values()), "rating": rating, "rating_reason": reason,
            "debt_3d": sum(debt.get(path, 0) for path in game.get("sources", [])),
            "probes": [probe for probe in game.get("probes", []) if probe in trusted],
            "untrusted_probes": [probe for probe in game.get("probes", []) if probe not in trusted],
            "open_defects": open_defects, "stale_evidence": stale, "overdraw": overdraw,
        })
    return rows


def ranked(rows: list[dict]) -> list[dict]:
    live = [row for row in rows if row["state"] == "live"]
    return sorted(live, key=lambda row: (-row["rating"], -row["points"], len(row["open_defects"]), row["id"]))


def uncovered_files(root: Path, catalogue: dict, rubric: dict) -> list[str]:
    claimed = {path for game in catalogue.get("games", []) for path in (*game.get("sources", []), *game.get("host", []))}
    claimed |= {str(entry.get("path")) for entry in (rubric.get("coverage") or {}).get("not_games", [])}
    tracked = git_files(root)
    missing = []
    for pattern in (rubric.get("coverage") or {}).get("globs", []):
        for path in tracked:
            if fnmatch.fnmatchcase(path, pattern) and path not in claimed:
                missing.append(path)
    return sorted(set(missing))


def git_files(root: Path) -> list[str]:
    """Tracked and new unignored files, so a game file is caught before its first commit."""
    try:
        output = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
                                capture_output=True, text=True, check=True).stdout
        return [line for line in output.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def validate(root: Path, catalogue: dict, rubric: dict) -> list[str]:
    errors: list[str] = []
    rules = defined_rules(root)
    findings = finding_states(root)
    decisions = {str(entry.get("id")) for entry in owner_verdicts(root)}
    if catalogue.get("schema") != "game_catalogue/1":
        errors.append(f"{CATALOGUE}: schema must be game_catalogue/1")
    if rubric.get("schema") != "gold_star/1":
        errors.append(f"{RUBRIC}: schema must be gold_star/1")
    criteria = {entry.get("id"): entry for entry in rubric.get("criteria", [])}
    if tuple(criteria) != CRITERIA:
        errors.append(f"{RUBRIC}: criteria must be exactly {', '.join(CRITERIA)} in order")
    for identifier, entry in criteria.items():
        if not entry.get("title") or not entry.get("meets"):
            errors.append(f"{RUBRIC}: {identifier} needs a title and a 'meets' definition")
        for rule in entry.get("rules", []):
            if rule not in rules:
                errors.append(f"{RUBRIC}: {identifier} cites undefined rule {rule}")
    games = catalogue.get("games", [])
    ids = [game.get("id") for game in games]
    duplicates = sorted({identifier for identifier in ids if ids.count(identifier) > 1})
    if duplicates:
        errors.append(f"{CATALOGUE}: duplicate ids {', '.join(map(str, duplicates))}")
    for game in games:
        label = f"{CATALOGUE}: {game.get('id')}"
        if game.get("family") not in FAMILIES:
            errors.append(f"{label}: family must be one of {', '.join(FAMILIES)}")
        if game.get("state") not in STATES:
            errors.append(f"{label}: state must be one of {', '.join(STATES)}")
        if not game.get("name") or not game.get("route"):
            errors.append(f"{label}: needs a name and a route")
        for path in (*game.get("sources", []), *game.get("host", [])):
            if not (root / path).is_file():
                errors.append(f"{label}: source does not exist: {path}")
        if not game.get("sources"):
            errors.append(f"{label}: needs at least one source file")
        for probe in game.get("probes", []):
            if not (root / "scripts" / f"{probe}.gd").is_file():
                errors.append(f"{label}: probe does not exist: {probe}")
        for identifier in game.get("findings", []):
            if identifier not in findings:
                errors.append(f"{label}: finding is not in the register: {identifier}")
        scores = game.get("scores") or {}
        for key in ASSESSED:
            entry = scores.get(key)
            if not isinstance(entry, dict) or entry.get("score") not in SCORE_VALUES or not str(entry.get("note", "")).strip():
                errors.append(f"{label}: {key} needs a score of 0, 1 or 2 and a note")
        extra = sorted(set(scores) - set(ASSESSED))
        if extra:
            errors.append(f"{label}: computed or unknown criteria cannot be assessed by hand: {', '.join(extra)}")
        for lane in ACCEPTANCE_LANES:
            entry = (game.get("acceptance") or {}).get(lane)
            if entry is None:
                continue
            evidence = str(entry.get("evidence", "")) if isinstance(entry, dict) else ""
            if not isinstance(entry, dict) or entry.get("result") not in ("accepted", "not_accepted") or not evidence:
                errors.append(f"{label}: {lane} acceptance needs a result of accepted or not_accepted and evidence")
            elif evidence.startswith("ODR-"):
                if evidence not in decisions:
                    errors.append(f"{label}: {lane} acceptance cites an unknown owner decision: {evidence}")
            elif not (root / evidence.split("#")[0]).is_file():
                errors.append(f"{label}: {lane} acceptance evidence does not exist: {evidence}")
        if not game.get("evidence"):
            errors.append(f"{label}: needs hashed evidence anchors for the assessment")
        for anchor in game.get("evidence", []):
            if anchor_hash(root, anchor) is None:
                errors.append(f"{label}: evidence anchor does not resolve: {anchor_label(anchor)}")
            if not re.fullmatch(r"[0-9a-f]{64}", str(anchor.get("sha256", ""))):
                errors.append(f"{label}: evidence anchor needs a sha256: {anchor_label(anchor)}")
    reference = (rubric.get("reference") or {}).get("game")
    live = {game.get("id") for game in games if game.get("state") == "live"}
    if reference not in live:
        errors.append(f"{RUBRIC}: reference game must be a live catalogue entry: {reference}")
    pattern_ids = [pattern.get("id") for pattern in rubric.get("patterns", [])]
    if len(pattern_ids) != len(set(pattern_ids)):
        errors.append(f"{RUBRIC}: pattern ids must be unique")
    for pattern in rubric.get("patterns", []):
        label = f"{RUBRIC}: {pattern.get('id')}"
        if pattern.get("criterion") not in ASSESSED:
            errors.append(f"{label}: criterion must be one of C1-C10")
        if pattern.get("game") is not None and pattern.get("game") not in set(ids):
            errors.append(f"{label}: source game is not in the catalogue: {pattern.get('game')}")
        if not pattern.get("title") or not pattern.get("copy") or not pattern.get("anchors"):
            errors.append(f"{label}: needs a title, what to copy and at least one anchor")
        for anchor in pattern.get("anchors", []):
            if anchor_hash(root, anchor) is None:
                errors.append(f"{label}: anchor does not resolve: {anchor_label(anchor)}")
            if not re.fullmatch(r"[0-9a-f]{64}", str(anchor.get("sha256", ""))):
                errors.append(f"{label}: anchor needs a sha256: {anchor_label(anchor)}")
    for entry in (rubric.get("coverage") or {}).get("not_games", []):
        if not (root / str(entry.get("path"))).is_file() or not entry.get("reason"):
            errors.append(f"{RUBRIC}: not_games entry needs an existing path and a reason: {entry.get('path')}")
    errors += validate_overdraw(root, catalogue, rubric)
    for path in uncovered_files(root, catalogue, rubric):
        errors.append(f"{path}: game file is not in the catalogue; catalogue and assess it, or list it under coverage.not_games with a reason")
    # design/ JSON is live project data to tools/audit_game_2d.py, so an engine
    # class name in a note would count as new 3D debt and fail the 2D gate.
    for name in (CATALOGUE, RUBRIC, OVERDRAW):
        path = root / name
        words = game_2d_token_counts(path.read_text(encoding="utf-8")) if path.is_file() else {}
        if words:
            listed = ", ".join(f"{word} x{count}" for word, count in words.items())
            errors.append(f"{name}: {listed} would count as 3D debt in tools/audit_game_2d.py; "
                          "write plain words such as '3D nodes' instead of engine class names")
    return errors


def validate_overdraw(root: Path, catalogue: dict, rubric: dict) -> list[str]:
    errors: list[str] = []
    for game in catalogue.get("games", []):
        for check, review in (game.get("overdraw_review") or {}).items():
            if check not in OD_REVIEWED or not isinstance(review, dict) \
                    or review.get("result") not in ("pass", "fail") or not review.get("evidence"):
                errors.append(f"{CATALOGUE}: {game.get('id')}: overdraw_review {check} needs a result of pass or fail and evidence")
    spec = rubric.get("overdraw")
    if spec is None:
        return errors
    if tuple(check.get("id") for check in spec.get("checks", [])) != OD_CHECKS:
        errors.append(f"{RUBRIC}: overdraw checks must be exactly {', '.join(OD_CHECKS)} in order")
    for check in spec.get("checks", []):
        if not (check.get("title") and check.get("means") and check.get("method")):
            errors.append(f"{RUBRIC}: overdraw {check.get('id')} needs a title, what it means and how it is measured")
    for key, value in (spec.get("budgets") or {}).items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            errors.append(f"{RUBRIC}: overdraw budget {key} must be a non-negative number")
    for entry in spec.get("code_drawing", []):
        label = f"{RUBRIC}: code_drawing {entry.get('path')}"
        if not (root / str(entry.get("path", ""))).is_file():
            errors.append(f"{label}: file does not exist")
        if entry.get("role") not in DRAWING_ROLES:
            errors.append(f"{label}: role must be one of {', '.join(DRAWING_ROLES)}")
        if not isinstance(entry.get("allowed"), bool) or not entry.get("draws"):
            errors.append(f"{label}: needs allowed (true or false) and what it draws")
        if entry.get("allowed") and entry.get("role") != "child_mark":
            errors.append(f"{label}: only the child's own marks may be allowed")
        if not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", ""))):
            errors.append(f"{label}: needs a sha256")
    if any(key not in ASSESSED for key in rubric.get("core") or []):
        errors.append(f"{RUBRIC}: core criteria must be assessed criteria (C1-C10)")
    measurements = load_measurements(root)
    if measurements:
        if measurements.get("schema") != "overdraw_measurements/1":
            errors.append(f"{OVERDRAW}: schema must be overdraw_measurements/1")
        known = {game.get("id") for game in catalogue.get("games", [])}
        for game_id, record in (measurements.get("games") or {}).items():
            if game_id not in known:
                errors.append(f"{OVERDRAW}: measured game is not in the catalogue: {game_id}")
            if not record.get("inputs") or not record.get("states"):
                errors.append(f"{OVERDRAW}: {game_id} needs hashed inputs and measured states")
    return errors


def stale_patterns(root: Path, rubric: dict) -> list[str]:
    return [f"{pattern['id']} {anchor_label(anchor)}" for pattern in rubric.get("patterns", [])
            for anchor in pattern.get("anchors", []) if anchor_hash(root, anchor) != anchor.get("sha256")]


def compare(rows: list[dict], rubric: dict, game: str, reference: str | None = None) -> dict:
    by_id = {row["id"]: row for row in rows}
    if game not in by_id:
        raise GoldStarError(f"unknown game: {game}")
    reference = reference or (rubric.get("reference") or {}).get("game")
    target, model = by_id[game], by_id.get(reference)
    criteria = {entry["id"]: entry for entry in rubric.get("criteria", [])}
    gaps = []
    for key in CRITERIA:
        if target["scores"][key] >= 2:
            continue
        patterns = [pattern for pattern in rubric.get("patterns", []) if pattern.get("criterion") == key]
        gaps.append({"criterion": key, "title": criteria.get(key, {}).get("title", key),
                     "score": target["scores"][key], "rules": criteria.get(key, {}).get("rules", []),
                     "note": target["notes"][key], "meets": criteria.get(key, {}).get("meets", ""),
                     "reference_score": model["scores"][key] if model else None,
                     "patterns": [{"id": p["id"], "title": p["title"], "copy": p["copy"],
                                   "anchors": [anchor_label(a) for a in p.get("anchors", [])]} for p in patterns]})
    overdraw = target.get("overdraw") or {}
    return {"game": game, "name": target["name"], "rating": target["rating"], "points": target["points"],
            "reference": reference, "gaps": gaps, "overdraw": overdraw,
            "to_four": next_steps(target, rubric, gaps, overdraw) if target["rating"] < 4 else [],
            "to_five": final_steps(target, gaps),
            "prompt": f"Bring {target['name']} up to the gold star" if gaps else f"{target['name']} meets every criterion"}


def next_steps(row: dict, rubric: dict, gaps: list[dict], overdraw: dict) -> list[str]:
    """The ordered work that lifts a game to 4/5 under the rating rule."""
    core = tuple(rubric.get("core") or DEFAULT_CORE)
    checks = {check["id"]: check for check in (rubric.get("overdraw") or {}).get("checks", [])}
    by_key = {gap["criterion"]: gap for gap in gaps}

    def hint(key: str) -> str:
        names = [pattern["id"] for pattern in by_key[key]["patterns"]]
        return f" Copy {', '.join(names)}." if names else ""

    steps = []
    if row["scores"]["C1"] < 2:
        steps.append(f"Make it reachable from a fresh save by touch (C1, now {row['scores']['C1']}/2): {by_key['C1']['note']}")
    if row["open_defects"]:
        steps.append(f"Close its open defects first: {', '.join(row['open_defects'])} (C11).")
    for key in core:
        if key != "C1" and key in by_key:
            steps.append(f"Raise core {key} {by_key[key]['title']} to 2 (now {by_key[key]['score']}/2): {by_key[key]['note']}{hint(key)}")
    for check, entry in overdraw.items():
        if entry["result"] == "fail":
            steps.append(f"Fix overdraw {check} {checks.get(check, {}).get('title', '')}: {entry['detail']}")
    open_checks = [check for check, entry in overdraw.items() if entry["result"] == "not_measured"]
    unmeasured = [check for check in open_checks if check not in OD_REVIEWED or "No overdraw measurement" in overdraw[check]["detail"]
                  or "stale" in overdraw[check]["detail"]]
    unreviewed = [check for check in open_checks if check not in unmeasured]
    if unmeasured:
        steps.append(f"Measure overdraw ({', '.join(unmeasured)}): add the game's states to `scripts/probe_overdraw.gd` if needed, "
                     "then run `python -B tools/measure_overdraw.py`.")
    if unreviewed:
        steps.append(f"Review overdraw ({', '.join(unreviewed)}) at phone size and record it in the game's `overdraw_review`: "
                     + "; ".join({"OD1": "no live object over a painted copy of itself",
                                  "OD2": "no painted look-alike beside the action"}[check] for check in unreviewed) + ".")
    for key in ASSESSED:
        if key not in core and key in by_key and by_key[key]["score"] == 0:
            steps.append(f"Raise {key} {by_key[key]['title']} from 0: {by_key[key]['note']}{hint(key)}")
    partial = [key for key in ASSESSED if key not in core and key in by_key and by_key[key]["score"] == 1]
    if len(partial) > 2:
        steps.append(f"Raise {len(partial) - 2} of these partly met criteria to 2: "
                     + "; ".join(f"{key} {by_key[key]['title']}{hint(key)}" for key in partial))
    return steps


def final_steps(row: dict, gaps: list[dict]) -> list[str]:
    remaining = [f"{gap['criterion']} {gap['title']}" for gap in gaps if gap["criterion"] != "C12"]
    steps = [f"Fully meet the remaining criteria: {'; '.join(remaining)}."] if remaining else []
    if row["scores"]["C12"] < 2:
        steps.append("Record a phone session, an observed child session and the owner's verdict in the game's acceptance lanes (C12).")
    return steps


def render_compare(result: dict) -> str:
    lines = [f"# {result['name']} against the gold star", "",
             f"Rating {result['rating']}/5, {result['points']}/24 points. Reference: `{result['reference']}`.", ""]
    for gap in result["gaps"]:
        lines += [f"## {gap['criterion']} {gap['title']} — {gap['score']}/2 (reference {gap['reference_score']}/2)", "",
                  f"Rules: {', '.join(f'`{rule}`' for rule in gap['rules'])}.", "",
                  f"Now: {gap['note']}", "", f"Gold star: {gap['meets']}", ""]
        for pattern in gap["patterns"]:
            lines += [f"- Copy {pattern['id']} {pattern['title']}: {pattern['copy']} ({'; '.join(pattern['anchors'])})"]
        if gap["patterns"]:
            lines.append("")
    if result["overdraw"]:
        lines += ["## Overdraw (C7)", ""]
        lines += [f"- {check} {entry['result'].replace('_', ' ')}: {entry['detail']}" for check, entry in result["overdraw"].items()]
        lines.append("")
    lines += [f"Planner prompt: \"{result['prompt']}\" (`python -B tools/plan_prompt.py \"{result['prompt']}\"`).", ""]
    lines += ["## To reach 4/5", ""]
    lines += [f"{index}. {step}" for index, step in enumerate(result["to_four"], start=1)] or ["Already 4/5 or better."]
    lines += ["", "## Then for 5/5", ""]
    lines += [f"{index}. {step}" for index, step in enumerate(result["to_five"], start=1)] or ["Every criterion meets the gold star."]
    lines.append("")
    return "\n".join(lines)


def table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_page(root: Path, catalogue: dict, rubric: dict, rows: list[dict]) -> str:
    reference = (rubric.get("reference") or {})
    by_id = {row["id"]: row for row in rows}
    model = by_id.get(reference.get("game"))
    order = ranked(rows)
    lines = ["# Gold star — game scorecard and reference model", "",
             f"Status: `{catalogue.get('status', 'SUPPORTING_CURRENT')}`. Generated by `python -B tools/gold_star.py --render` "
             f"from [the catalogue](games.json) and [the rubric](gold_star.json); edit those, not this page. "
             f"Assessed by {catalogue.get('author', 'Claude')} on {catalogue.get('assessed')} at "
             f"`{str(catalogue.get('assessed_head', ''))[:12]}`.", "",
             "Scores are evidence for development choices, not acceptance. A machine signal never raises a score; "
             "C12 stays at 0 until device, child and owner results are recorded (`DL-QA-04`, `DL-QA-05`, `DL-QA-06`, `DL-QA-07`).", ""]
    if model:
        lines += ["## Reference model", "",
                  f"**{model['name']}** (`{model['id']}`), rating {model['rating']}/5, {model['points']}/24 points. "
                  f"{reference.get('why', '')}", "",
                  f"Status: {reference.get('status', '')}", ""]
        gaps = compare(rows, rubric, model["id"])["gaps"]
        if gaps:
            lines += ["What still separates it from a gold star:", ""]
            lines += [f"- {gap['criterion']} {gap['title']} ({gap['score']}/2): {gap['note']}" for gap in gaps]
            lines.append("")
        lines += ["Patterns to copy:", ""]
        for pattern in rubric.get("patterns", []):
            anchors = ", ".join(f"`{anchor_label(anchor)}`" for anchor in pattern.get("anchors", []))
            source = by_id.get(pattern.get("game", ""))
            origin = f" From {source['name']}." if source and source["id"] != model["id"] else ""
            lines.append(f"- **{pattern['id']} {pattern['title']}** ({pattern['criterion']}): {pattern['copy']}{origin} {anchors}")
        lines.append("")
    lines += ["## Ranking of live games", "",
              "| Rank | Game | Family | Rating | Points | " + " | ".join(CRITERIA) + " | 3D debt | Open defects |",
              "|---:|---|---|---:|---:|" + "---:|" * len(CRITERIA) + "---:|---|"]
    for index, row in enumerate(order, start=1):
        cells = " | ".join(str(row["scores"][key]) for key in CRITERIA)
        defects = ", ".join(row["open_defects"]) or "none"
        lines.append(f"| {index} | {table_cell(row['name'])} | {row['family']} | {row['rating']} | {row['points']} | {cells} | "
                     f"{row['debt_3d']} | {defects} |")
    others = [row for row in rows if row["state"] != "live"]
    if others:
        lines += ["", "Not reachable as a live game: " + "; ".join(f"{row['name']} (`{row['state']}`)" for row in others) + "."]
    lines += render_overdraw(root, rubric, rows)
    lines += ["", "## Rubric", "", "| Criterion | Rules | Gold star means |", "|---|---|---|"]
    for entry in rubric.get("criteria", []):
        rules = ", ".join(f"`{rule}`" for rule in entry.get("rules", []))
        lines.append(f"| {entry['id']} {table_cell(entry['title'])} | {rules} | {table_cell(entry['meets'])} |")
    lines += ["", "Rating rule: " + table_cell(rubric.get("rating_rule", "")), "",
              "## Using it", "",
              "- `python -B tools/gold_star.py --rank` lists the games, strongest first.",
              "- `python -B tools/gold_star.py --compare GAME` prints what GAME needs to reach the gold star and which reference pattern to copy, "
              "and ends with the ordered list of what lifts it to 4/5, then 5/5.",
              "- `python -B tools/measure_overdraw.py` re-measures overdraw (needs a display; numbers only, never an image).",
              "- `python -B tools/gold_star.py --check` fails on schema errors, unknown rules or findings, unresolved evidence, and any new game file that is not catalogued; `--strict` also fails on stale assessments or a stale page.",
              "- After re-assessing a game, `python -B tools/gold_star.py --rebind GAME` records the hashes of the evidence that was judged.", ""]
    return "\n".join(lines)


def render_overdraw(root: Path, rubric: dict, rows: list[dict]) -> list[str]:
    spec = rubric.get("overdraw")
    if not spec:
        return []
    measurements = load_measurements(root)
    measured = (measurements.get("games") or {})
    budgets = spec.get("budgets") or {}
    skip = set(spec.get("states_not_budgeted", []))
    lines = ["", "## Overdraw (C7)", "", table_cell(spec.get("meaning", "")), "",
             f"Status: {spec.get('status', '')} Measured by {spec.get('measured_by', '')}"
             + (f" at `{str(measurements.get('head', ''))[:12]}` on {measurements.get('measured_at', '')}, "
                f"Godot {measurements.get('godot', '')}, self-test {(measurements.get('selftest') or {}).get('result', 'not run')}."
                if measurements else "; no measurement recorded yet."), "",
             f"Budgets per play state: mean layers at most {budgets.get('mean_layers')}, four or more layers on at most "
             f"{budgets.get('share_ge4')} of the screen, max {budgets.get('max_layers')} (peak frame {budgets.get('peak_layers')}); "
             f"effects clear within {budgets.get('effect_seconds')} s and cover at most {budgets.get('effect_over_roshan')} of Roshan.", "",
             "| Check | Means | How it is measured |", "|---|---|---|"]
    for check in spec.get("checks", []):
        lines.append(f"| {check['id']} {table_cell(check['title'])} | {table_cell(check['means'])} | {table_cell(check['method'])} |")
    lines += ["", "| Game | Rating | Busiest play state (mean, share with 4+ layers, max, peak) | " + " | ".join(OD_CHECKS) + " |",
              "|---|---:|---|" + "---|" * len(OD_CHECKS)]
    word = {"pass": "pass", "fail": "fail", "not_measured": "—"}
    for row in ranked(rows):
        record = measured.get(row["id"])
        if not record:
            continue
        states = {name: state for name, state in record.get("states", {}).items() if name not in skip and state.get("gpu")}
        busiest = max(states.items(), key=lambda item: float(item[1]["gpu"].get("mean", 0)), default=None)
        numbers = (f"{busiest[0]}: {busiest[1]['gpu'].get('mean')}, {busiest[1]['gpu'].get('share_ge4')}, "
                   f"{busiest[1]['gpu'].get('max')}, {busiest[1].get('gpu_peak')}") if busiest else "—"
        results = " | ".join(word[row["overdraw"].get(check, {}).get("result", "not_measured")] for check in OD_CHECKS)
        lines.append(f"| {table_cell(row['name'])} | {row['rating']} | {numbers} | {results} |")
    unmeasured = [row["name"] for row in ranked(rows) if row["id"] not in measured]
    if unmeasured:
        lines += ["", f"Not yet measured ({len(unmeasured)} live games): " + "; ".join(unmeasured) + "."]
    lines += ["", "Code-drawing scripts seen on screen:", "", "| Script | Role | What it draws | Allowed |", "|---|---|---|---|"]
    stale = set(stale_drawing(root, rubric))
    for entry in spec.get("code_drawing", []):
        flag = " (changed since classified)" if entry["path"] in stale else ""
        lines.append(f"| `{entry['path']}`{flag} | {entry['role']} | {table_cell(entry['draws'])} | {'yes' if entry['allowed'] else 'no'} |")
    return lines


def bind_anchors(root: Path, anchors: list[dict]) -> None:
    for anchor in anchors:
        value = anchor_hash(root, anchor)
        if value is None:
            raise GoldStarError(f"anchor does not resolve: {anchor_label(anchor)}")
        anchor["sha256"] = value


def rebind(root: Path, catalogue: dict, game_id: str, head: str) -> dict:
    for game in catalogue.get("games", []):
        if game.get("id") == game_id:
            bind_anchors(root, game.get("evidence", []))
            game["assessed_head"] = head
            return catalogue
    raise GoldStarError(f"unknown game: {game_id}")


def rebind_patterns(root: Path, rubric: dict, head: str) -> dict:
    for pattern in rubric.get("patterns", []):
        bind_anchors(root, pattern.get("anchors", []))
    rubric.setdefault("reference", {})["patterns_reviewed_head"] = head
    return rubric


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def head_sha(root: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def summary(root: Path) -> dict:
    """Compact gold-star state for the study loop; never raises on a damaged catalogue."""
    if not (root / CATALOGUE).is_file() and not (root / RUBRIC).is_file():
        return {"status": "ABSENT", "errors": []}
    try:
        catalogue, rubric = read_json(root, CATALOGUE), read_json(root, RUBRIC)
        rows = evaluate(root, catalogue, rubric)
        errors = validate(root, catalogue, rubric)
    except (GoldStarError, OSError) as error:
        return {"status": "ERROR", "errors": [str(error)]}
    order = ranked(rows)
    reference = (rubric.get("reference") or {}).get("game")
    model = next((row for row in rows if row["id"] == reference), None)
    def brief(row: dict) -> dict:
        return {"id": row["id"], "name": row["name"], "rating": row["rating"], "points": row["points"]}

    return {
        "status": "ERROR" if errors else ("STALE" if any(row["stale_evidence"] for row in rows) else "CURRENT"),
        "errors": errors[:20],
        "reference": {"game": reference, "name": model["name"] if model else None, "rating": model["rating"] if model else None,
                      "gaps": [gap["criterion"] for gap in compare(rows, rubric, reference)["gaps"]] if model else []},
        "strongest": [brief(row) for row in order[:5]],
        "weakest": [brief(row) for row in order[-5:][::-1]],
        "stale": sorted(row["id"] for row in rows if row["stale_evidence"]),
        "stale_patterns": stale_patterns(root, rubric),
        "ratings": {str(value): sum(row["rating"] == value for row in order) for value in range(5, 0, -1)},
        "overdraw": {
            "measured": sorted(row["id"] for row in rows if any(entry["result"] != "not_measured"
                                                                 for entry in (row.get("overdraw") or {}).values())),
            "passing": sorted(row["id"] for row in rows if row.get("overdraw") and overdraw_ok(row["overdraw"])),
            "failing": {row["id"]: [check for check, entry in row["overdraw"].items() if entry["result"] == "fail"]
                        for row in rows if any(entry["result"] == "fail" for entry in (row.get("overdraw") or {}).values())},
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="validate the catalogue and rubric (default)")
    action.add_argument("--rank", action="store_true", help="list live games, strongest first")
    action.add_argument("--compare", metavar="GAME", help="print what GAME needs to reach the gold star")
    action.add_argument("--render", action="store_true", help=f"write {PAGE}")
    action.add_argument("--rebind", metavar="GAME", help="record current evidence hashes after re-assessing GAME")
    action.add_argument("--rebind-patterns", action="store_true", help="record current pattern hashes after re-reviewing them")
    parser.add_argument("--to", metavar="GAME", help="compare against this game instead of the reference")
    parser.add_argument("--strict", action="store_true", help="with --check, also fail on stale assessments or a stale page")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        catalogue, rubric = read_json(root, CATALOGUE), read_json(root, RUBRIC)
        if args.rebind:
            updated = rebind(root, catalogue, args.rebind, head_sha(root))
            write_json(root / CATALOGUE, updated)
            print(f"GOLDSTAR|REBIND|{args.rebind}|{head_sha(root)[:12]}")
            return 0
        if args.rebind_patterns:
            write_json(root / RUBRIC, rebind_patterns(root, rubric, head_sha(root)))
            print(f"GOLDSTAR|REBIND|patterns|{head_sha(root)[:12]}")
            return 0
        rows = evaluate(root, catalogue, rubric)
        if args.compare:
            result = compare(rows, rubric, args.compare, args.to)
            print(json.dumps(result, indent=1) if args.json else render_compare(result))
            return 0
        if args.rank:
            order = ranked(rows)
            if args.json:
                print(json.dumps(order, indent=1))
            else:
                for index, row in enumerate(order, start=1):
                    flag = " STALE" if row["stale_evidence"] else ""
                    print(f"{index:2}. {row['rating']}/5 {row['points']:2}/24  {row['name']} ({row['family']}){flag} — {row['rating_reason']}")
            return 0
        if args.render:
            (root / PAGE).write_text(render_page(root, catalogue, rubric, rows), encoding="utf-8", newline="\n")
            print(f"GOLDSTAR|RENDER|{PAGE}")
            return 0
        errors = validate(root, catalogue, rubric)
        stale = {row["id"]: row["stale_evidence"] for row in rows if row["stale_evidence"]}
        patterns = stale_patterns(root, rubric)
        page = root / PAGE
        page_stale = not page.is_file() or page.read_text(encoding="utf-8").replace("\r\n", "\n") != render_page(root, catalogue, rubric, rows)
        for error in errors:
            print(f"GOLDSTAR|ERROR|{error}")
        for game, anchors in sorted(stale.items()):
            print(f"GOLDSTAR|STALE|{game}|re-assess, then --rebind: {', '.join(anchors)}")
        for pattern in patterns:
            print(f"GOLDSTAR|STALE_PATTERN|{pattern}")
        drawing = stale_drawing(root, rubric)
        for path in drawing:
            print(f"GOLDSTAR|STALE_DRAWING|{path}|re-read what it draws, update the classification and its sha256")
        measurements = load_measurements(root)
        for game_id, record in sorted((measurements.get("games") or {}).items()):
            changed = stale_inputs(root, record)
            if changed:
                # Fail-closed already: a stale measurement scores as not measured.
                print(f"GOLDSTAR|STALE_OVERDRAW|{game_id}|re-measure: {', '.join(changed[:4])}")
        if page_stale:
            print(f"GOLDSTAR|STALE_PAGE|{PAGE}|run --render")
        failed = bool(errors) or (args.strict and bool(stale or patterns or drawing or page_stale))
        print(f"GOLDSTAR|RESULT|{'FAIL' if failed else 'OK'}|{len(rows)} games, {len(errors)} errors, {len(stale)} stale")
        return 1 if failed else 0
    except GoldStarError as error:
        print(f"GOLDSTAR|ERROR|{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
