#!/usr/bin/env python3
"""Build and check the text data of the Opera imp-contest Codex handoff.

Run from the repository root:

    python3 -B docs/handoffs/codex_opera_imp_contest_2026-09-30/tools/build_packet_data.py
    python3 -B docs/handoffs/codex_opera_imp_contest_2026-09-30/tools/build_packet_data.py --manifest
    python3 -B docs/handoffs/codex_opera_imp_contest_2026-09-30/tools/build_packet_data.py --check

The default run regenerates two text inventories from data/contest_spec.json
and the repository, which it reads and never modifies:

    data/imp_art_inventory.json     every imp pose file: path, bytes, SHA-256,
                                    pixel size, whether the shipping game shows
                                    it today, and its planned contest roles
    data/imp_voice_inventory.json   every imp line: text, hashes, routing today
                                    and planned use, plus the new lines needed

--manifest rewrites MANIFEST.json from the committed (LF) bytes of every
packet file. --check verifies MANIFEST.json against the files and confirms the
inventories regenerate byte-identically.

The packet is written material only (CLAUDE.md, "Codex handoffs: Claude
writes, Codex builds images"). This script reads files and writes JSON; it
never creates or edits an image.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
REPO = PACKET.parents[2]
HANDOFF = PACKET.name
SPEC_PATH = PACKET / "data" / "contest_spec.json"
ACTORS = "assets/opera/worlds/actors"
VOICES = "assets/audio/voices"
FILLER = "assets/audio/voices/filler_v1"

STATES = ["idle", "windup", "charge", "slash", "recover", "guard", "stagger",
          "flee", "bopped", "bow", "hop_a", "hop_b", "taunt"]
COSTUMED = ["chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
            "boxer", "magician", "painter", "astronaut", "racer", "popstar"]
FAMILIES = ["rival_" + career for career in COSTUMED] + ["imp_mischief", "imp_captain"]

# What the shipping game at the baseline puts on screen. Every entry cites the
# code that draws it. The dormant bop-crew code (LEGACY_PHASES) is reachable
# from no shipping phase, so the plain mischief and captain imps show nothing.
_WORLD_SHOWN = {
    "idle": "scripts/opera_career_world_2d.gd:1220-1230 (rival actor base texture)",
    "taunt": "scripts/opera_career_world_2d.gd:3689-3693 (rival_step)",
    "bow": "scripts/opera_career_world_2d.gd:3815-3816 and :5045-5046 (curtain call, Hall bow)",
}
SHOWN_TODAY = {"rival_" + c: dict(_WORLD_SHOWN) for c in COSTUMED if c not in ("boxer", "racer")}
SHOWN_TODAY["rival_boxer"] = {
    state: "scripts/opera_boxing_surface.gd:260-262 (boxing surface state set)"
    for state in ["idle", "windup", "charge", "recover", "guard", "stagger",
                  "taunt", "bopped", "bow"]}
SHOWN_TODAY["rival_racer"] = {
    "idle": "scripts/opera_racer_surface.gd:85 (rival kart driver)",
    "bow": _WORLD_SHOWN["bow"],
}
SHOWN_TODAY["imp_mischief"] = {}
SHOWN_TODAY["imp_captain"] = {}

# Imp voice keys the running game routes at the baseline.
ROUTED_TODAY = {
    "imp_op_detective_steal": "scripts/opera_career_world_2d.gd:67 (detective intro lines)",
    "imp_op_retry": "scripts/opera_career_world_2d.gd:3710 (detective guided retry; retired by this design)",
}

# Pose roles shared by every contest (see CONTEST_DESIGN.md, "Pose meanings").
BASE_ROLES = {
    "flee": ["entrance run-in"],
    "hop_a": ["entrance crouch"],
    "hop_b": ["entrance jump", "his win jump"],
    "idle": ["rest between beats"],
    "taunt": ["challenge", "ahead of her", "his win beat", "idle-pause freeze"],
    "windup": ["ready before the contest"],
    "charge": ["working (reach)"],
    "slash": ["working (place)"],
    "stagger": ["she overtakes him", "defeat (1)"],
    "guard": ["worried near her finish", "idle-pause freeze"],
    "bopped": ["defeat (2)"],
    "recover": ["defeat (3)", "after his flub"],
    "bow": ["curtain call"],
}

# Extra pose roles in the defense contests (Chef and Nursery, OD-E).
DEFENSE_ROLES = {
    "windup": ["hazard telegraph"],
    "slash": ["hazard toss or noise"],
}
PLAIN_IMPS = ("imp_mischief", "imp_captain")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def committed_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in {".md", ".json", ".py", ".gd", ".txt", ""}:
        data = data.replace(b"\r\n", b"\n")
    return data


def dump_json(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def png_size(path: Path) -> list:
    """Read width and height from the PNG header (no image library)."""
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return []
    return list(struct.unpack(">II", header[16:24]))


def imp_pose_path(family: str, state: str) -> str | None:
    slug = family if state == "idle" else f"{family}_{state}"
    path = f"{ACTORS}/{slug}.png"
    return path if (REPO / path).exists() else None


def contest_poses(spec: dict) -> dict:
    """Map family -> {state: [roles]} for the poses the contest design uses."""
    entrance = [pose[0] for pose in spec["shared"]["imp_entrance"]["poses"]]
    assert entrance[:3] == ["flee", "hop_a", "hop_b"], entrance
    result: dict = {}
    for career, entry in spec["careers"].items():
        contest = entry.get("contest")
        if not contest:
            continue
        imp = contest["imp"]
        families = imp.get("families") or [imp["family"]]
        substitutions = imp.get("pose_substitutions", {})
        roles_for_state = {state: list(labels) for state, labels in BASE_ROLES.items()}
        if contest.get("archetype") == "defense":
            for state, labels in DEFENSE_ROLES.items():
                roles_for_state[state] += labels
        for family in families:
            roles = result.setdefault(family, {})
            # The plain imps serve more than one career (the Teacher's interim
            # imp and the Nursery wave), so their roles name the career.
            tag = f" [{career}]" if family in PLAIN_IMPS else ""
            for state, labels in roles_for_state.items():
                state = substitutions.get(state, state)
                if imp_pose_path(family, state) is None:
                    continue
                for label in labels:
                    if label + tag not in roles.setdefault(state, []):
                        roles[state].append(label + tag)
            flub_poses = (contest.get("flub") or {}).get("poses", [])
            for state, _seconds in flub_poses:
                state = substitutions.get(state, state)
                if imp_pose_path(family, state) is not None:
                    label = f"flub [{career}]"
                    if label not in roles.setdefault(state, []):
                        roles[state].append(label)
    return result


def build_art_inventory(spec: dict) -> dict:
    planned = contest_poses(spec)
    families = []
    total = shown_total = planned_total = 0
    for family in FAMILIES:
        states = []
        for state in STATES:
            path = imp_pose_path(family, state)
            if path is None:
                states.append({"state": state, "path": None, "note": "no file in this family"})
                continue
            shown = SHOWN_TODAY[family].get(state)
            roles = planned.get(family, {}).get(state, [])
            total += 1
            shown_total += 1 if shown else 0
            planned_total += 1 if (shown or roles) else 0
            states.append({
                "state": state,
                "path": path,
                "bytes": (REPO / path).stat().st_size,
                "sha256": sha256_file(REPO / path),
                "size": png_size(REPO / path),
                "shown_today": shown is not None,
                "shown_today_evidence": shown,
                "contest_roles": roles,
            })
        families.append({"family": family, "states": states})
    return {
        "schema": "opera_imp_art_inventory/1",
        "generated_by": f"docs/handoffs/{HANDOFF}/tools/build_packet_data.py",
        "baseline": spec["baseline"],
        "rule": "Reuse only. No imp art is modified, recoloured, re-cut or regenerated by this design.",
        "totals": {
            "files": total,
            "shown_today": shown_total,
            "shown_after_specified_contests": planned_total,
            "note": "shown_after_specified_contests counts files the shipping game would show once every specified contest ships: the twelve costumed careers, the Teacher on the plain mischief imp (interim), the Nursery wave on the plain mischief and captain imps, and the Geologist on the detective family (interim). If the recommended rival_teacher family replaces the Teacher's interim imp, the mischief imp's 11 files are still used by the Nursery.",
        },
        "families": families,
    }


def voice_texts() -> dict:
    source = (REPO / "tools/make_voices.py").read_text(encoding="utf-8")
    return {match.group(1): match.group(2) for match in re.finditer(
        r'"(imp_op_\w+)": \("imp", "((?:[^"\\]|\\.)*)"\)', source)}


def build_voice_inventory(spec: dict) -> dict:
    manifest = json.loads((REPO / FILLER / "FILLER_MANIFEST.json").read_text(encoding="utf-8"))
    entries = {entry["key"]: entry for entry in manifest["entries"]}
    texts = voice_texts()
    keys = sorted({p.stem for p in (REPO / VOICES).glob("imp_op_*.ogg")}
                  | {p.stem for p in (REPO / FILLER).glob("imp_op_*.ogg")})
    planned: dict = {}
    for career, entry in spec["careers"].items():
        for role, key in entry.get("voice", {}).items():
            if isinstance(key, str) and key.startswith("op_"):
                planned.setdefault("imp_" + key.split(" ", 1)[0], []).append(f"{career} {role}")
    lines = []
    for key in keys:
        legacy = REPO / VOICES / f"{key}.ogg"
        filler = REPO / FILLER / f"{key}.ogg"
        entry = entries.get(key, {})
        uses = planned.get(key, [])
        if key.endswith("_steal"):
            uses = uses or ["unchanged: the steal story beat is outside the contest"]
        lines.append({
            "key": key,
            "text": entry.get("text") or texts.get(key),
            "legacy_path": f"{VOICES}/{key}.ogg" if legacy.exists() else None,
            "legacy_sha256": sha256_file(legacy) if legacy.exists() else None,
            "filler_path": f"{FILLER}/{key}.ogg" if filler.exists() else None,
            "filler_sha256": sha256_file(filler) if filler.exists() else None,
            "filler_status": entry.get("status"),
            "speaker_preset": entry.get("speaker_preset"),
            "routed_today": key in ROUTED_TODAY,
            "routed_today_evidence": ROUTED_TODAY.get(key),
            "planned_use": uses,
        })
    new_lines = []
    for career, entry in spec["careers"].items():
        voice = entry.get("voice", {})
        wanted = []
        for role, speaker in (("new_imp_challenge", "imp"), ("new_roshan_contest", "roshan")):
            if voice.get(role):
                wanted.append((speaker, voice[role]))
        wanted.extend((line["speaker"], line) for line in voice.get("new_lines", []))
        for speaker, line in wanted:
            path = f"{FILLER}/{speaker}_{line['key']}.ogg"
            state = "EXISTS (reuse)" if (REPO / path).exists() else "TO_GENERATE"
            new_lines.append({"career": career, "speaker": speaker, "key": line["key"],
                              "file": path, "text": line["text"], "state": state})
    for line in spec["new_shared_voice"]:
        path = f"{FILLER}/{line['speaker']}_{line['key']}.ogg"
        new_lines.append({"career": "all", "speaker": line["speaker"], "key": line["key"],
                          "file": path, "text": line["text"],
                          "state": "EXISTS (reuse)" if (REPO / path).exists() else "TO_GENERATE"})
    return {
        "schema": "opera_imp_voice_inventory/1",
        "generated_by": f"docs/handoffs/{HANDOFF}/tools/build_packet_data.py",
        "baseline": spec["baseline"],
        "routing_rule": "show_msg(who, text, vo) plays <speaker>_<vo>.ogg, preferring filler_v1 (scripts/audio_director.gd:15-16, :220-231); in the Opera the caption is hidden whenever an exact clip exists (scripts/audio_director.gd:493)",
        "generation_rule": "New lines are appended through the existing filler pipeline (tools/make_parler_voice_trials.py, tools/select_filler_voices.py, tools/master_filler_voices.py) with the imp 'Mike' and Roshan 'Joy' presets as PROVISIONAL_SYNTHETIC_FILLER. Nothing existing is modified or replaced; protected family recordings stay byte-identical (DL-SND-05, DL-SND-11); every new file gets its audio-ledger row (DL-SND-10) and meets DL-SND-12.",
        "totals": {
            "imp_keys": len(lines),
            "routed_today": sum(1 for line in lines if line["routed_today"]),
            "planned_contest_use": sum(1 for line in lines if any(
                not use.startswith("unchanged") for use in line["planned_use"])),
            "new_lines": sum(1 for line in new_lines if line["state"] == "TO_GENERATE"),
            "new_lines_reused": sum(1 for line in new_lines if line["state"] == "EXISTS (reuse)"),
        },
        "imp_lines": lines,
        "new_lines": new_lines,
    }


ROLES = {
    ".gdignore": "keeps Godot from importing this folder",
    "README.md": "handoff entry point",
    "CONTEST_DESIGN.md": "contest design and implementation specification",
    "CURRENT_STATE_ANALYSIS.md": "current-state analysis with code anchors",
    "data/contest_spec.json": "machine-readable contest specification (hand-authored)",
    "data/imp_art_inventory.json": "generated imp art inventory (text)",
    "data/imp_voice_inventory.json": "generated imp voice inventory and new-line list (text)",
    "tools/build_packet_data.py": "text-only generator and checker for the inventories and manifest",
}


def packet_files() -> list:
    return [path for path in sorted(PACKET.rglob("*"))
            if path.is_file() and path.name != "MANIFEST.json" and "__pycache__" not in path.parts]


def build_manifest(spec: dict) -> dict:
    entries = []
    total = 0
    for path in packet_files():
        key = path.relative_to(PACKET).as_posix()
        data = committed_bytes(path)
        total += len(data)
        entries.append({"path": key, "bytes": len(data), "sha256": sha256_bytes(data),
                        "role": ROLES.get(key, "packet file")})
    return {
        "schema": "codex_handoff_manifest/1",
        "handoff": HANDOFF,
        "status": "PROPOSED / CANDIDATE",
        "prepared_by": "Claude (written design, analysis and specification only; no game changes and no images)",
        "recipient": "Codex",
        "evidence_baseline": f"dev {spec['baseline']}",
        "entry": "README.md",
        "file_count": len(entries),
        "total_bytes": total,
        "hash_basis": "SHA-256 of the committed Git blob bytes (LF line endings), identical to what raw.githubusercontent.com serves",
        "revision": "5 (2026-10-04): adds OD-E: the Teacher game cannot be lost and is always silly, the Chef's YUCKY RECIPE, the Geologist's GEODE RACE, the Nursery's QUIET TIME, and a radical slowdown after two failures; revision 4 (OD-D) was 1fbcc9db, revision 3 (art-reuse and imp-contact corrections) was 86732a47, revision 2 (OD-C) was df01b7ce, revision 1 was 7ec82d46",
        "files": entries,
    }


def generated(spec: dict) -> dict:
    return {
        "data/imp_art_inventory.json": dump_json(build_art_inventory(spec)),
        "data/imp_voice_inventory.json": dump_json(build_voice_inventory(spec)),
    }


def check(spec: dict) -> int:
    failures = 0
    manifest = json.loads((PACKET / "MANIFEST.json").read_text(encoding="utf-8"))
    listed = {entry["path"]: entry for entry in manifest["files"]}
    present = {path.relative_to(PACKET).as_posix(): path for path in packet_files()}
    for key in sorted(set(listed) | set(present)):
        if key not in present:
            print(f"FAIL missing file {key}")
            failures += 1
        elif key not in listed:
            print(f"FAIL unlisted file {key}")
            failures += 1
        else:
            data = committed_bytes(present[key])
            if sha256_bytes(data) != listed[key]["sha256"] or len(data) != listed[key]["bytes"]:
                print(f"FAIL hash {key}")
                failures += 1
    for key, data in generated(spec).items():
        if (PACKET / key).read_bytes() != data:
            print(f"FAIL stale generated output {key}")
            failures += 1
    images = [key for key in present if key.lower().endswith(
        (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp"))]
    for key in images:
        print(f"FAIL image in a written handoff {key}")
        failures += 1
    print("PACKET_CHECK|" + ("OK" if failures == 0 else f"FAIL={failures}") + f"|FILES={len(present)}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--manifest", action="store_true", help="rewrite MANIFEST.json")
    parser.add_argument("--check", action="store_true", help="verify the manifest and generated inventories")
    args = parser.parse_args()
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    if args.check:
        return check(spec)
    if args.manifest:
        (PACKET / "MANIFEST.json").write_bytes(dump_json(build_manifest(spec)))
        print("wrote MANIFEST.json")
        return 0
    for key, data in generated(spec).items():
        (PACKET / key).write_bytes(data)
        print(f"wrote {key} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
