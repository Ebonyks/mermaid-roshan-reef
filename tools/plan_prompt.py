#!/usr/bin/env python3
"""Expand a short owner prompt into a reviewable plan, without executing it."""
from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

try:
    from tools.build_study_roadmap import sha256, validate_strengths
except ModuleNotFoundError:  # Direct execution from tools/.
    from build_study_roadmap import sha256, validate_strengths

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = "design/reference/prompt_intents.json"
STRENGTHS = "design/reference/strengths.json"


def load_catalogue(root: Path) -> dict:
    return json.loads((root / CATALOGUE).read_text(encoding="utf-8"))


def validate_catalogue(root: Path, catalogue: dict) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    for intent in catalogue.get("intents", []):
        identifier = intent.get("id", "")
        if not re.fullmatch(r"INT-[A-Z-]+", identifier) or identifier in ids:
            errors.append(f"invalid or duplicate intent: {identifier}")
        ids.add(identifier)
        recipe = intent.get("recipe", {})
        if not recipe.get("id") or not recipe.get("path"):
            errors.append(f"{identifier}: missing recipe")
        elif not (root / recipe["path"]).is_file():
            errors.append(f"{identifier}: missing recipe file {recipe['path']}")
        for key in ("says", "match_patterns", "read_first", "expand", "gates", "write_backs"):
            if not intent.get(key):
                errors.append(f"{identifier}: missing {key}")
        for reference in intent.get("read_first", []):
            path = reference.split("#", 1)[0]
            if not (root / path).is_file():
                errors.append(f"{identifier}: missing reference {path}")
        for pattern in intent.get("match_patterns", []):
            try:
                re.compile(pattern, re.IGNORECASE)
            except re.error as error:
                errors.append(f"{identifier}: bad match pattern: {error}")
    return errors


def infer_intent(prompt: str, catalogue: dict) -> dict:
    matches = [intent for intent in catalogue["intents"] if any(
        re.search(pattern, prompt, re.IGNORECASE) for pattern in intent["match_patterns"])]
    if len(matches) != 1:
        raise ValueError("Prompt must match exactly one intent; use --intent with the catalogue ID.")
    return matches[0]


def save_inventory(root: Path) -> dict:
    """Read allocation sites; the plan never trusts seed counts as live facts."""
    house = (root / "scripts/opera_house.gd").read_text(encoding="utf-8")
    save = (root / "scripts/save_state.gd").read_text(encoding="utf-8")
    bits = sorted({int(value) for value in re.findall(r'"save_bit"\s*:\s*(\d+)', house)})
    if not bits:
        raise ValueError("Cannot allocate: no save_bit records found; inspect the current extension path.")
    next_bit = max(bits) + 1  # Includes retired rows: identities are never reused.
    mask_match = re.search(r"const OPERA_ACTIVE_STAR_MASK\s*(?::[^=\n]+)?[:=]*\s*(0x[0-9A-Fa-f]+|\d+)", save)
    count_match = re.search(r"const OPERA_ACTIVE_ACT_COUNT\s*(?::[^=\n]+)?[:=]*\s*(\d+)", save)
    if not mask_match or not count_match:
        raise ValueError("Cannot read the live save mask/count; no allocation guess is permitted.")
    namespace_bound = (1 << next_bit) - 1
    clamp_sites = [index for index, line in enumerate(save.splitlines(), 1)
                   if re.search(rf"\b{namespace_bound}\b", line)]
    return {
        "next_bit": next_bit, "current_active_mask": hex(int(mask_match.group(1), 0)),
        "proposed_active_mask": hex(int(mask_match.group(1), 0) | (1 << next_bit)),
        "current_active_count": int(count_match.group(1)),
        "proposed_active_count": int(count_match.group(1)) + 1,
        "proposed_namespace_bound": (1 << (next_bit + 1)) - 1,
        "current_namespace_bound": namespace_bound,
        "namespace_clamp_lines": clamp_sites,
        "source": ["scripts/opera_house.gd", "scripts/save_state.gd"],
        "caveat": "Plan only. Re-read load, write and both shared normaliser clamp sites at implementation head; "
                  "the four 262143 clamps at this baseline must all become 524287 for bit 18. Exercise external merge through the shared normaliser. "
                  "Never reuse tombstone bits 4, 9 or 14; retain every existing save key and add new keys with defaults. "
                  "If the platform or namespace changed, derive bounds from its live catalogue instead of this baseline.",
    }



def bakery_background_inventory(root: Path) -> dict:
    """Bind measured composition sources without accepting enlarged delivery art."""
    kitchen_manifest = "audit/interactive_background_ownership_2026-08-29.json"
    chef_manifest = "assets_src/imagegen/opera_codex_2026-08-02/OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json"
    kitchen_path = "assets_src/castle/interactive_background_ownership_2026-08-29/generated_room_kitchen_background_source.png"
    chef_path = "assets_src/imagegen/opera_codex_2026-08-02/native/world_chef_native.png"
    delivery_path = "assets_src/castle/room_backgrounds_2k/room_kitchen_background_2k.png"
    kitchen_doc = json.loads((root / kitchen_manifest).read_text(encoding="utf-8"))
    chef_doc = json.loads((root / chef_manifest).read_text(encoding="utf-8"))
    kitchen = next((item for item in kitchen_doc.get("castle", [])
                    if item.get("room") == "kitchen" and item.get("source") == kitchen_path), {})
    chef = next((item for item in chef_doc.get("accepted", []) if item.get("path") == chef_path), {})

    def measure(path: str, recorded_hash: str | None) -> dict:
        source = root / path
        if not source.is_file():
            return {"path": path, "present": False, "recorded_sha256": recorded_hash,
                    "hash_matches_record": False, "reason": "Source missing; inspect the provenance gap."}
        with source.open("rb") as stream:
            header = stream.read(24)
        if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
            raise ValueError(f"Cannot measure PNG source {path}")
        actual_hash = sha256(source)
        return {"path": path, "present": True, "dimensions": list(struct.unpack(">II", header[16:24])),
                "sha256": actual_hash, "recorded_sha256": recorded_hash,
                "hash_matches_record": bool(recorded_hash) and actual_hash == recorded_hash}

    sources = [measure(kitchen_path, kitchen.get("source_sha256")), measure(chef_path, chef.get("sha256"))]
    delivery = measure(delivery_path, kitchen.get("native_master_sha256")
                       if kitchen.get("native_master") == delivery_path else None)
    intact = all(item["hash_matches_record"] for item in sources + [delivery])
    below_native = all(item.get("dimensions") and min(item["dimensions"]) < 2048 for item in sources)
    return {
        "status": "SOURCE_PROVENANCE_GAP" if not intact else
                  "NATIVE_COVERAGE_GAP" if below_native else "NATIVE_COVERAGE_REVIEW_REQUIRED",
        "native_sources": sources, "kitchen_delivery_master": delivery,
        "recorded_delivery_transform": kitchen.get("normalization", "MISSING"),
        "references": [kitchen_manifest, chef_manifest,
                       "assets_src/castle/room_regenerations/room_kitchen_fullframe_v2_provenance.md",
                       "audit/minigame_art_quality_2026-09-05/opera_native_coverage_followup.md"],
        "acceptance": "Composition/reuse references only. The Kitchen delivery master is documented enlargement; "
                      "its dimensions and tiles do not prove native authored coverage or runtime readiness under DL-LAY-07. "
                      "Recheck the selected route and current source chain, then review at shipping scale before a narrow "
                      "replacement decision. No new art, 5/5 score, owner acceptance or generation budget is granted.",
    }


def build_plan(root: Path, prompt: str, intent_id: str | None = None) -> dict:
    catalogue = load_catalogue(root)
    errors = validate_catalogue(root, catalogue)
    if errors:
        raise ValueError("; ".join(errors))
    if intent_id:
        intent = next((item for item in catalogue["intents"] if item["id"] == intent_id), None)
        if intent is None:
            raise ValueError(f"Unknown intent {intent_id}")
    else:
        intent = infer_intent(prompt, catalogue)
    strengths_document = json.loads((root / STRENGTHS).read_text(encoding="utf-8"))
    strength_errors = validate_strengths(root, strengths_document)
    if strength_errors:
        raise ValueError("Strength evidence invalid: " + "; ".join(strength_errors))
    strengths = strengths_document["strengths"]
    bound = [strength for strength in strengths if strength["id"] in intent.get("strengths", [])]
    bound.sort(key=lambda item: (item["tier"] != "accepted", item["id"]))
    plan = {
        "schema": "prompt_plan/1", "status": "PLAN_ONLY", "prompt": prompt,
        "intent": intent["id"], "recipe": intent["recipe"],
        "defaults": intent["defaults"], "read_first": intent["read_first"],
        "strengths": [{"id": item["id"], "tier": item["tier"], "scope": item["acceptance_scope"]} for item in bound],
        "steps": intent["expand"], "variety_rules": intent["variety_rules"],
        "owner_touchpoints": intent["owner_touchpoints"], "gates": intent["gates"],
        "write_backs": intent["write_backs"],
        "acceptance": "Machine, visual, device, child and owner evidence remain separate; this plan grants none.",
    }
    if intent["id"] == "INT-ADD-JOB":
        plan["save_allocation"] = save_inventory(root)
        if re.search(r"baker|bakery", prompt, re.IGNORECASE):
            plan["job_card"] = {
                "name": "Baker", "premise": "Help Roshan make a pictured bread order; permanent addition pending premise/home decision.",
                "home_default": "Kitchen only if its current story role and reachability fit; otherwise existing Opera freeplay venue.",
                "extension_default": "Opera career row; keep Day One and locked Chapter Two roster unchanged without scope authorization.",
                "beats": [
                    {"act": "Teach", "verb": "pour", "requires": "ingredients_ready", "result_state": "flour_in_bowl", "child_action": "One-finger bag-to-bowl gesture requests Roshan's travel and pour.", "visible_change": "flour fills the same mixing bowl", "voice_key": "opera_baker_pour", "line": "Pour flour into the bowl.", "pointer": "bowl rim and flour bag", "contact": "Roshan carries and tips the bag over the bowl"},
                    {"act": "Play", "verb": "knead", "requires": "flour_in_bowl", "result_state": "kneaded_dough", "child_action": "One-finger presses and folds guide the kneading action.", "visible_change": "rough dough becomes smooth dough along the hand path", "voice_key": "opera_baker_knead", "line": "Press and fold the dough.", "pointer": "dough surface", "contact": "Roshan's hand meets the same dough"},
                    {"act": "Twist", "verb": "shape", "requires": "kneaded_dough", "result_state": "shaped_raw_loaf", "child_action": "One-finger shaping follows the pictured loaf outline with generous tolerance.", "visible_change": "the same raw dough portion takes the pictured loaf shape", "voice_key": "opera_baker_shape", "line": "Make the loaf look like this.", "pointer": "one pictured order and raw dough", "contact": "Roshan shapes and places the same raw dough on its tray"},
                    {"act": "Twist", "verb": "bake", "requires": "shaped_raw_loaf", "result_state": "baked_loaf_in_oven", "child_action": "One finger requests tray placement and oven closure, then guided holds or taps on the pictured oven control advance baking; idle input pauses it.", "visible_change": "Roshan loads the raw loaf, closes the oven and visibly bakes that same loaf in response to intentional input", "voice_key": "opera_baker_bake", "line": "Put the tray in. Help the oven bake.", "pointer": "tray, oven shelf, then pictured oven control", "contact": "Roshan supports the tray at the oven shelf and operates its door/control; no burn or lost loaf"},
                    {"act": "Twist", "verb": "retrieve", "requires": "baked_loaf_in_oven", "result_state": "retrieved_baked_loaf", "child_action": "A deliberate one-finger oven-to-cooling-place gesture requests removal; no automatic retrieval.", "visible_change": "the same visibly baked loaf leaves the oven and rests on the cooling place", "voice_key": "opera_baker_retrieve", "line": "Use the mitt. Take the bread out.", "pointer": "oven mitt, tray handle and cooling place", "contact": "Roshan's mitted hand meets the tray handle and carries it to the supported cooling place"},
                    {"act": "Bow", "verb": "serve", "requires": "retrieved_baked_loaf", "result_state": "served_baked_loaf", "child_action": "A deliberate one-finger loaf-to-plate gesture requests delivery.", "visible_change": "the retrieved baked loaf reaches the matching pictured plate", "voice_key": "opera_baker_serve", "line": "Bring the bread to this plate.", "pointer": "matching plate", "contact": "Roshan carries and places that same baked loaf"},
                ],
                "state_rules": "One finger, voice plus pointer, no fail state. Every result requires the preceding state and the child's intentional action with visible Roshan travel/contact. Idle input cannot finish baking, retrieve, serve or award progress. A timer or demonstration never grants completion. Back/focus loss cancels unfinished action and retains completed checkpoints.",
                "quality_gate": "Target 5/5 only after owner acceptance in runtime context under DL-VIS-07, including all six contact transitions and exact source/derivation provenance. Machine checks grant no score; human/device/child/owner evidence is pending.",
                "background_readiness": bakery_background_inventory(root),
                "imp": "Competitive final job-skill contest under DL-INT-14; an imp win immediately restarts only the contest, with no lost progress.",
                "voice": "Roshan synthetic provisional lines: resolve the current voice-manifest engine authority, exact prefix/folder/category routing, hash and quality ledger; never imitate family recordings.",
                "music": "Propose opera_baker score and EXPECTED_IDS/REQUIRED_AREA_MUSIC entry, or justified byte-identical approved reuse.",
                "help": "Re-say, demonstrate without payout, widen tolerance, assist the next intentional action; no idle win.",
                "save": "Proposed additive checkpoints retain flour, kneaded dough, shaped raw loaf, completed baking, deliberate retrieval and served state with defaults; preserve existing rewards and all previous keys. Partial resume and repeat never downgrade progress; saved baking completion cannot skip retrieval.",
                "art": "Inventory kitchen/chef/candymaker props first, reuse approved Roshan atlas as identity, then name missing raw/baking/baked/retrieved loaf states, tray/mitt/contact frames and costume gap; generation only by Codex with provenance.",
            }
            beats = plan["job_card"]["beats"]
            plan["job_card"]["phase_mapping"] = {
                "phase_count": len(beats),
                "finale_start": next(index for index, beat in enumerate(beats) if beat["act"] == "Bow"),
                "finale_source": "scripts/opera_career_world_2d.gd::FINALE_START / _finale_start (zero-based first contest phase)",
                "phases": [{"index": index, "verb": beat["verb"], "act": beat["act"]}
                           for index, beat in enumerate(beats)],
                "caveat": "Candidate six-step card; Teach/Play/Twist/Bow labels group actions, not four inherited phases. "
                          "Derive PHASES, FINALE_START, stations, hotspot/voice/probe expectations and any checkpoint count "
                          "from the approved card and actual extension contract at implementation head.",
            }
    return plan


def render_plan(plan: dict) -> str:
    rows = [f"# Prompt plan: {plan['prompt']}", "", f"Status: `{plan['status']}`. Recipe: `{plan['recipe']['id']}` ({plan['recipe']['path']}).", "", plan["acceptance"], ""]
    for heading, key in (("Read first", "read_first"), ("Build plan", "steps"), ("Variety", "variety_rules"), ("Gates", "gates"), ("Write back", "write_backs")):
        rows += [f"## {heading}", ""] + [f"- {item}" for item in plan[key]] + [""]
    rows += ["## Owner touchpoints", ""]
    rows += [f"{index}. {item['question']} Default: {item['default']}. Trigger: {item['trigger']}." for index, item in enumerate(plan["owner_touchpoints"], 1)] or ["None for authorized scope."]
    for key in ("strengths", "save_allocation", "job_card"):
        if key in plan:
            rows += ["", f"## {key.replace('_', ' ').title()}", "", "```json", json.dumps(plan[key], indent=2, ensure_ascii=False), "```"]
    return "\n".join(rows) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?")
    parser.add_argument("--intent")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        errors = validate_catalogue(args.root, load_catalogue(args.root))
        print("\n".join(errors) if errors else "PROMPTS: ALL OK")
        return int(bool(errors))
    if not args.prompt:
        parser.error("prompt required unless --check")
    try:
        plan = build_plan(args.root, args.prompt, args.intent)
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))
    print(json.dumps(plan, indent=2, ensure_ascii=False) if args.json else render_plan(plan), end="\n" if args.json else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
