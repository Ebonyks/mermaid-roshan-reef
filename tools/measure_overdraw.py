#!/usr/bin/env python3
"""Measure overdraw for the gold-star C7 overdraw checks (numbers only).

Runs scripts/probe_overdraw.gd with the exact approved Godot in a rendering
window (the GPU layer count needs a real frame; nothing is saved or shown as an
image), after its self-test proves the counts exact, and writes
design/reference/overdraw.json for tools/gold_star.py. Each game's measurement
is bound to SHA-256 hashes of the files that produced it, so editing a game or
a drawing script marks its measurement stale instead of silently keeping it.

    python -B tools/measure_overdraw.py                 # self-test, Pool, Opera
    python -B tools/measure_overdraw.py --groups opera  # one group
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from tools import gold_star
    from tools.audit_game_2d import _token_counts as game_2d_token_counts
except ModuleNotFoundError:
    import gold_star  # type: ignore[no-redef]
    from audit_game_2d import _token_counts as game_2d_token_counts  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parents[1]
PROBE = "scripts/probe_overdraw.gd"
OUTPUT = "design/reference/overdraw.json"
GROUPS = ("pool", "opera")
GAME_IDS = {"day_one_pool": "day_one_pool"}
EFFECT_SECONDS_SAMPLED = 2.0


class MeasureError(RuntimeError):
    pass


def safe(text: object) -> str:
    """Keep engine 3D class names out of design JSON (the 2D gate counts them)."""
    value = str(text)
    return "<withheld: engine 3D term>" if game_2d_token_counts(value) else value


def parse_log(text: str) -> dict:
    states, effects, errors, info = [], [], [], []
    done = None
    for line in text.splitlines():
        if not line.startswith("OVERDRAW|"):
            continue
        _, kind, payload = (line.split("|", 2) + [""])[:3]
        if kind == "STATE":
            states.append(json.loads(payload))
        elif kind == "EFFECTS":
            effects.append(json.loads(payload))
        elif kind == "ERROR":
            errors.append(payload)
        elif kind == "INFO":
            info.append(json.loads(payload))
        elif kind == "DONE":
            done = json.loads(payload)
    return {"states": states, "effects": effects, "errors": errors, "info": info, "done": done}


def wasted_layers(state: dict, total_cells: int = 128 * 72) -> list[dict]:
    """Large layers drawn while (almost) entirely hidden under opaque art above them."""
    wasted = []
    for item in state.get("listing", []):
        cells, hidden = int(item.get("cells", 0)), int(item.get("hidden", 0))
        if cells >= total_cells * 0.5 and hidden >= cells * 0.9:
            wasted.append({"name": safe(item.get("name")), "kind": item.get("kind"),
                           "source": safe(item.get("image") or item.get("script") or ""),
                           "screen_share": round(cells / total_cells, 2),
                           "hidden_share": round(hidden / max(cells, 1), 2)})
    return wasted


def compact_state(state: dict) -> dict:
    # A code-drawing script counts as visible unless every cell of its known area
    # sits under opaque art above it; an unknown area (a Node2D) counts as visible.
    hidden_names = {str(item.get("script", "")) for item in state.get("listing", [])
                    if item.get("kind") == "custom" and int(item.get("cells", 0)) > 0
                    and int(item.get("hidden", 0)) >= int(item.get("cells", 0))}
    scripts, hidden = [], []
    for entry in (state.get("custom_draw") or {}).get("items", []):
        path = str(entry.get("script", "")).replace("res://", "")
        if not entry.get("shapes") or not path:
            continue
        (hidden if path.split("/")[-1] in hidden_names else scripts).append(path)
    return {
        "gpu": state.get("gpu_layers") or {},
        "gpu_translucent": state.get("gpu_translucent_layers") or {},
        "gpu_peak": state.get("gpu_peak_layers"),
        "node_depth": state.get("depth") or {},
        "hidden_share": state.get("hidden_share"),
        "duplicates": [{"image": safe(d.get("image")), "names": [safe(n) for n in d.get("names", [])],
                        "overlap": d.get("overlap")} for d in state.get("duplicates", [])],
        "broad_overlays": [{"name": safe(o.get("name")), "kind": o.get("kind"),
                            "screen_share": o.get("screen_share"), "translucent_share": o.get("translucent_share")}
                           for o in state.get("broad_overlays", [])],
        "full_width_alpha_layers": len(state.get("full_width_alpha_layers", [])),
        "code_drawing": sorted(set(scripts)),
        "code_drawing_hidden": sorted(set(hidden) - set(scripts)),
        "wasted_layers": wasted_layers(state),
        "roshan_covered_share": (state.get("roshan") or {}).get("covered_share"),
        "items": state.get("items"),
    }


def compact_effects(record: dict) -> dict:
    def is_guide(entry: dict) -> bool:
        name = str(entry.get("name", "")).lower()
        return "guide" in name or "pointer" in name

    def is_roshan(entry: dict) -> bool:
        return "roshan" in (str(entry.get("name", "")) + " " + str(entry.get("image", ""))).lower()

    transient = [{"name": safe(entry.get("name")), "seconds": entry.get("last"),
                  "screen_share": entry.get("max_screen_share"), "over_roshan_share": entry.get("over_roshan_share")}
                 for entry in record.get("transient", []) if not is_guide(entry) and not is_roshan(entry)]
    lingering = [{"name": safe(entry.get("name")), "screen_share": entry.get("max_screen_share"),
                  "translucent_share": entry.get("translucent_share"),
                  "image": safe(str(entry.get("image", "")).split("/")[-1])}
                 for entry in record.get("persistent", [])
                 if not is_guide(entry) and not is_roshan(entry)
                 and float(entry.get("translucent_share") or 0.0) >= 0.5
                 and float(entry.get("max_screen_share") or 0.0) >= 0.01]
    return {"transient": transient, "lingering_translucent": lingering,
            "sampled_seconds": EFFECT_SECONDS_SAMPLED}


def game_inputs(root: Path, catalogue: dict, game_id: str, scripts: list[str]) -> dict[str, str]:
    paths = {PROBE, "tools/measure_overdraw.py"} | set(scripts)
    for game in catalogue.get("games", []):
        if game.get("id") == game_id:
            paths |= set(game.get("sources", []))
            paths |= {str(anchor.get("path")) for anchor in game.get("evidence", []) if anchor.get("path")}
    hashes = {}
    for path in sorted(paths):
        value = gold_star.anchor_hash(root, {"path": path})
        if value is not None:
            hashes[path] = value
    return hashes


def build(root: Path, catalogue: dict, parsed_groups: dict[str, dict], godot: str, selftest: dict) -> dict:
    games: dict[str, dict] = {}
    for parsed in parsed_groups.values():
        for state in parsed["states"]:
            game_id = GAME_IDS.get(state["game"], state["game"])
            games.setdefault(game_id, {"states": {}, "effects": {}})["states"][state["state"]] = compact_state(state)
        for record in parsed["effects"]:
            game_id = GAME_IDS.get(record["game"], record["game"])
            games.setdefault(game_id, {"states": {}, "effects": {}})["effects"][record["state"]] = compact_effects(record)
    known = {game.get("id") for game in catalogue.get("games", [])}
    for game_id, record in games.items():
        if game_id not in known:
            raise MeasureError(f"measured game is not in the catalogue: {game_id}")
        scripts = sorted({path for state in record["states"].values()
                          for path in (*state["code_drawing"], *state["code_drawing_hidden"])})
        record["inputs"] = game_inputs(root, catalogue, game_id, scripts)
    return {
        "schema": "overdraw_measurements/1",
        "status": "SUPPORTING_CURRENT",
        "note": ("Machine measurement only, never acceptance. Layer counts come from a real Mobile-renderer frame read "
                 "into memory and reduced to numbers; nothing is saved or shown as an image. Node fields come from "
                 "the live Canvas tree. Code-drawing scripts are judged by the classification in gold_star.json."),
        "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head": gold_star.head_sha(root),
        "godot": godot,
        "selftest": selftest,
        "games": dict(sorted(games.items())),
    }


def run_group(godot: str, root: Path, group: str, timeout: int) -> dict:
    with tempfile.TemporaryDirectory() as home:
        env = dict(os.environ)
        for name in ("APPDATA", "LOCALAPPDATA"):
            folder = Path(home) / name.lower()
            folder.mkdir()
            env[name] = str(folder)
        env["XDG_DATA_HOME"] = str(Path(home) / "appdata")
        command = [godot, "--rendering-method", "mobile", "--path", str(root), "-s", PROBE, "--", f"--group={group}"]
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=timeout)
    parsed = parse_log(result.stdout + "\n" + result.stderr)
    script_errors = [line for line in (result.stdout + result.stderr).splitlines() if "SCRIPT ERROR" in line]
    if result.returncode != 0 or parsed["errors"] or script_errors or not parsed["done"]:
        raise MeasureError(f"{group}: exit {result.returncode}; errors {parsed['errors'][:3]}; "
                           f"script errors {script_errors[:3]}")
    return parsed


def resolve_godot(root: Path) -> str:
    result = subprocess.run([sys.executable, "-B", str(root / "tools/resolve_godot.py")], capture_output=True,
                            text=True, check=True)
    return result.stdout.strip().splitlines()[-1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--groups", default=",".join(GROUPS))
    parser.add_argument("--godot")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        godot = args.godot or resolve_godot(root)
        selftest_run = run_group(godot, root, "selftest", args.timeout)
        state = selftest_run["states"][0] if selftest_run["states"] else {}
        selftest = {"result": "PASS", "gpu": state.get("gpu_layers"), "gpu_translucent": state.get("gpu_translucent_layers")}
        version = subprocess.run([godot, "--version"], capture_output=True, text=True).stdout.strip()
        parsed = {group: run_group(godot, root, group, args.timeout)
                  for group in args.groups.split(",") if group}
        catalogue = gold_star.read_json(root, gold_star.CATALOGUE)
        data = build(root, catalogue, parsed, version, selftest)
        output = root / OUTPUT
        if output.is_file() and set(parsed) != set(GROUPS):
            previous = json.loads(output.read_text(encoding="utf-8"))
            merged = previous.get("games", {})
            merged.update(data["games"])
            data["games"] = dict(sorted(merged.items()))
        gold_star.write_json(output, data)
        print(f"OVERDRAW|WROTE|{OUTPUT}|{len(data['games'])} games|godot {version}")
        return 0
    except (MeasureError, subprocess.SubprocessError, OSError, json.JSONDecodeError, IndexError) as error:
        print(f"OVERDRAW|FAIL|{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
