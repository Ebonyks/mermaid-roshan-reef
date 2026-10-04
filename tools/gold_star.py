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
    from tools.audit_probe_parity import _loop_names
    from tools.build_study_roadmap import SEVERITY_RANK, TEXT_EVIDENCE_SUFFIXES, sha256, split_records
except ModuleNotFoundError:
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


def derive_rating(scores: dict[str, int], p0_open: bool = False) -> tuple[int, str]:
    """Turn twelve 0-2 scores into the master audit's 1-5 scale, deterministically.

    An open game-specific P0 blocker caps the rating at 2 (master audit 2.3:
    a primary path is unavailable).
    """
    assessed = [scores[key] for key in ASSESSED]
    zeros = [key for key in ASSESSED[1:] if scores[key] == 0]
    partial = [key for key in ASSESSED if scores[key] == 1]
    if all(scores[key] == 2 for key in CRITERIA) and not p0_open:
        return 5, "Every criterion meets the gold star, including device, child and owner acceptance"
    if scores["C1"] == 0:
        return 1, "A child cannot reach it in normal play"
    if len(zeros) >= 2:
        return 2, "Fails " + ", ".join(zeros) + ("; an open P0 blocker" if p0_open else "")
    if p0_open:
        return 2, "An open P0 blocker" + (f"; fails {zeros[0]}" if zeros else "")
    if zeros or scores["C11"] == 0 or len(partial) > 2:
        reasons = [f"fails {zeros[0]}"] if zeros else []
        if scores["C11"] == 0:
            reasons.append("an open P0/P1 defect")
        if len(partial) > 2:
            reasons.append(f"{len(partial)} criteria only partly met")
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
    rows = []
    for game in catalogue.get("games", []):
        scores, notes = game_scores(game, findings)
        p0_open = any(findings.get(identifier, {}).get("lifecycle") in DEFECT
                      and findings.get(identifier, {}).get("severity") == "P0"
                      for identifier in game.get("findings", []))
        rating, reason = derive_rating(scores, p0_open)
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
            "open_defects": open_defects, "stale_evidence": stale,
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
    for path in uncovered_files(root, catalogue, rubric):
        errors.append(f"{path}: game file is not in the catalogue; catalogue and assess it, or list it under coverage.not_games with a reason")
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
    return {"game": game, "name": target["name"], "rating": target["rating"], "points": target["points"],
            "reference": reference, "gaps": gaps,
            "prompt": f"Bring {target['name']} up to the gold star" if gaps else f"{target['name']} meets every criterion"}


def render_compare(result: dict) -> str:
    lines = [f"# {result['name']} against the gold star", "",
             f"Rating {result['rating']}/5, {result['points']}/24 points. Reference: `{result['reference']}`.", ""]
    if not result["gaps"]:
        return "\n".join(lines + ["Every criterion meets the gold star.", ""])
    for gap in result["gaps"]:
        lines += [f"## {gap['criterion']} {gap['title']} — {gap['score']}/2 (reference {gap['reference_score']}/2)", "",
                  f"Rules: {', '.join(f'`{rule}`' for rule in gap['rules'])}.", "",
                  f"Now: {gap['note']}", "", f"Gold star: {gap['meets']}", ""]
        for pattern in gap["patterns"]:
            lines += [f"- Copy {pattern['id']} {pattern['title']}: {pattern['copy']} ({'; '.join(pattern['anchors'])})"]
        if gap["patterns"]:
            lines.append("")
    lines += [f"Planner prompt: \"{result['prompt']}\" (`python -B tools/plan_prompt.py \"{result['prompt']}\"`).", ""]
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
    lines += ["", "## Rubric", "", "| Criterion | Rules | Gold star means |", "|---|---|---|"]
    for entry in rubric.get("criteria", []):
        rules = ", ".join(f"`{rule}`" for rule in entry.get("rules", []))
        lines.append(f"| {entry['id']} {table_cell(entry['title'])} | {rules} | {table_cell(entry['meets'])} |")
    lines += ["", "Rating rule: " + table_cell(rubric.get("rating_rule", "")), "",
              "## Using it", "",
              "- `python -B tools/gold_star.py --rank` lists the games, strongest first.",
              "- `python -B tools/gold_star.py --compare GAME` prints what GAME needs to reach the gold star and which reference pattern to copy.",
              "- `python -B tools/gold_star.py --check` fails on schema errors, unknown rules or findings, unresolved evidence, and any new game file that is not catalogued; `--strict` also fails on stale assessments or a stale page.",
              "- After re-assessing a game, `python -B tools/gold_star.py --rebind GAME` records the hashes of the evidence that was judged.", ""]
    return "\n".join(lines)


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
        if page_stale:
            print(f"GOLDSTAR|STALE_PAGE|{PAGE}|run --render")
        failed = bool(errors) or (args.strict and bool(stale or patterns or page_stale))
        print(f"GOLDSTAR|RESULT|{'FAIL' if failed else 'OK'}|{len(rows)} games, {len(errors)} errors, {len(stale)} stale")
        return 1 if failed else 0
    except GoldStarError as error:
        print(f"GOLDSTAR|ERROR|{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
