#!/usr/bin/env python3
"""Read-only chapter story-binding gate. Static reachability is not route acceptance."""
from __future__ import annotations
import argparse
import ast
import re
from pathlib import Path
try:
    from tools.audit_castle_static_depth_cards import _without_hash_comments, _dictionary, _array, AuditInputError
except ModuleNotFoundError:
    from audit_castle_static_depth_cards import _without_hash_comments, _dictionary, _array, AuditInputError

ADAPTER = "scripts/chapter_two_career_scene_adapter.gd"
WORLD = "scripts/opera_career_world_2d.gd"
PATHS = "scripts/opera_stage_paths.gd"
PLAN = "scripts/chapter_two_party_plan.gd"

def literal(text: str, start: int) -> str:
    pairs = {"[": "]", "{": "}", "(": ")"}
    stack, quote, escaped = [], "", False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escaped: escaped = False
            elif char == chr(92): escaped = True
            elif char == quote: quote = ""
            continue
        if char in (chr(34), chr(39)): quote = char
        elif char in pairs: stack.append(pairs[char])
        elif char in "]})":
            if not stack or stack.pop() != char: raise ValueError("unbalanced chapter data")
            if not stack: return text[start:index + 1]
    raise ValueError("unterminated chapter data")

def value(text: str):
    text = text.strip()
    if text.startswith("{"): return {key: value(raw) for key, raw in _dictionary(text, "chapter data").items()}
    if text.startswith("["): return [value(raw) for raw in _array(text, "chapter data")]
    if text in {"true", "false", "null"}: return {"true": True, "false": False, "null": None}[text]
    if re.fullmatch(r'Vector2\([^()]+\)', text): return text
    return ast.literal_eval(text)

def constant(text: str, name: str):
    text = _without_hash_comments(text)
    match = re.search(r"(?m)^const " + re.escape(name) + r"(?:\s*:[^=\n]*)?\s*:?=\s*([\[{])", text)
    if not match: raise ValueError("missing literal constant " + name)
    return value(literal(text, match.start(1)))

def function(text: str, name: str) -> str:
    match = re.search(r"(?ms)^(?:static )?func " + re.escape(name) + r"\(.*?(?=^(?:static )?func |\Z)", _without_hash_comments(text))
    if not match: raise ValueError("missing function " + name)
    return match.group(0)

def station_ids(world: str, paths: dict, career: str) -> set[str]:
    config = function(world, "_configure_stage_paths")
    branches = re.split(r"(?m)^\t(?=if |elif |else:)", config)[1:]
    selected = next((part for part in branches if ('career_id == "' + career + '"') in part.split("\n", 1)[0]
                     or (career == "ballerina" and "_is_chapter2_stuffie_scene()" in part.split("\n", 1)[0])), None)
    if selected is None:
        selected = next((part for part in branches if part.startswith("else:")), "")
    if "station_list = _chapter2_stuffie_ballet_stations()" in selected:
        body = function(world, "_chapter2_stuffie_ballet_stations")
        begin = re.search(r"\breturn\s*(\[)", body)
        if not begin: raise ValueError("missing Stuffie room stations")
        return {item["id"] for item in value(literal(body, begin.start(1)))}
    authored = re.findall(r'_story_station\("([^"\n]+)"', selected)
    if authored: return set(authored)
    call = re.search(r'station_list = StagePaths.stations\(("[^"\n]+"|career_id)\)', selected)
    if not call: raise ValueError("unrecognized station construction for " + career)
    owner = career if call.group(1) == "career_id" else ast.literal_eval(call.group(1))
    result = {item["id"] for item in paths.get(owner, {}).get("stations", [])}
    if career == "popstar":
        match = re.search(r'if _is_chapter2_story_scene\(\) and career_id == "popstar":(.*)', selected, re.S)
        if not match: raise ValueError("missing Pop Star story socket")
        source = re.search(r'_station_index_for_id\("([^"\n]+)"\)', match.group(1))
        target = re.search(r'rumi_socket\["id"\] = "([^"\n]+)"', match.group(1))
        if not source or not target or source.group(1) not in result: raise ValueError("unreachable Pop Star story socket")
        result.add(target.group(1))
    return result

def binding_issues(phases: dict, bindings: dict, stations: dict[str, set[str]], careers: list[str]) -> list[str]:
    issues = []
    for career in careers:
        steps = phases.get(career, {}).get("phases", [])
        if not steps: issues.append(career + ": missing story phases")
        for step in steps:
            name = step.get("name", "")
            station = bindings.get(career, {}).get(name, {}).get("station_id", "")
            if not station: issues.append(career + "/" + name + ": unbound story step")
            elif station not in stations.get(career, set()): issues.append(career + "/" + name + ": object outside its own room: " + station)
    return issues

def audit(root: Path) -> list[str]:
    try:
        adapter = (root / ADAPTER).read_text(encoding="utf-8")
        world = (root / WORLD).read_text(encoding="utf-8")
        phases, bindings = constant(adapter, "PHASE_SETS"), constant(adapter, "PHASE_BINDINGS")
        plan = constant((root / PLAN).read_text(encoding="utf-8"), "LIVE_CAREERS")
        careers = [row["career"].replace("candy_maker", "candymaker") for row in plan]
        paths = constant((root / PATHS).read_text(encoding="utf-8"), "PATHS")
        stations = {career: station_ids(world, paths, career) for career in careers}
        return binding_issues(phases, bindings, stations, careers)
    except (OSError, ValueError, SyntaxError, KeyError, TypeError, AuditInputError) as exc:
        return ["chapter contract could not be read: " + str(exc)]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    issues = audit(args.root)
    for issue in issues: print("CHAPTER|FAIL|" + issue)
    print("CHAPTER|RESULT|" + ("FAIL" if issues else "ALL OK (static bindings only)"))
    return int(bool(issues))

if __name__ == "__main__": raise SystemExit(main())
