#!/usr/bin/env python3
"""Validate plans separately from execution. Never infer creative approval."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{64}$")
URL = re.compile(r"^https://(?:github\.com/[^/]+/[^/]+/blob|raw\.githubusercontent\.com/[^/]+/[^/]+)/[0-9a-f]{40}/[^?#]+$")
ROLES = {"approved_clean_first_frame", "subject_identity", "object_or_material_identity", "relationship_scale_contact", "lighting_or_grade"}
CAMERAS = {"locked": 0, "slow push-in": 1, "gentle pan right": 1, "gentle pan left": 1, "slow pull-back": 1}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def filehash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value

def inside(root, value):
    if not isinstance(value, str) or not value:
        raise ValueError("missing relative path")
    result = (root / value).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f"path outside packet: {value}")
    return result

def canon_hash(root):
    return digest({p.name: filehash(p) for p in sorted((root / "canon").glob("*.json"))})

def fingerprint(c):
    """Exclude receipts/status to avoid circular hashes; include every creative input."""
    keys = ("shot_id", "revision", "event_id", "exact_cast", "cast_instances",
            "exact_prop_counts", "location_id", "room_state", "end_room_state",
            "camera", "action", "causal_chain", "end_state", "binds", "continuity",
            "must_move", "must_not_move", "negative_constraints", "duration_seconds",
            "aspect_ratio", "delivery_size", "prompt_sha256", "canon_sha256")
    return digest({k: c.get(k) for k in keys})

def load_receipt(root, descriptor, errors, label):
    try:
        p = inside(root, descriptor["path"])
        if not SHA.fullmatch(str(descriptor.get("sha256", ""))) or filehash(p) != descriptor["sha256"]:
            errors.append(f"{label}: file hash mismatch")
        return read(p)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"{label}: invalid/missing receipt: {exc}")
        return {}

def check_request(c, root, errors):
    req = load_receipt(root, c.get("request"), errors, "request")
    if not req:
        return
    expected = digest({k: v for k, v in req.items() if k != "request_sha256"})
    if req.get("request_sha256") != expected:
        errors.append("request: canonical self-hash mismatch")
    for key, value in (("shot_id", c["shot_id"]), ("plan_sha256", fingerprint(c)),
                       ("prompt_sha256", c["prompt_sha256"])):
        if req.get(key) != value:
            errors.append(f"request: stale {key}")
    if req.get("kind") != "MOTION_REQUEST" or not req.get("request_id"):
        errors.append("request: missing motion request identity")
    if not URL.fullmatch(str(req.get("remote_url", ""))):
        errors.append("request: immutable published URL required")
    if req.get("bind_sha256s") != {b["id"]: b.get("sha256") for b in c["binds"]}:
        errors.append("request: image hashes differ")
    attempt = req.get("attempt")
    if type(attempt) is not int or attempt <= c.get("attempts_used", 0):
        errors.append("request: attempt must follow existing lineage")
    elif attempt > c.get("attempt_cap", 3):
        override = load_receipt(root, c.get("attempt_cap_override_receipt"), errors, "attempt override")
        if (override.get("actor") != "owner" or override.get("decision") != "allow_attempt"
                or override.get("shot_id") != c["shot_id"] or override.get("attempt") != attempt
                or override.get("plan_sha256") != fingerprint(c) or not override.get("source_url")):
            errors.append("attempt override: exact owner exception missing")

def readiness(c, root):
    errors = []
    if c.get("blocking_findings") or c.get("blocking_reason") or c.get("hold"):
        errors.append("unresolved blocker or HOLD")
    continuity = c.get("continuity", {})
    if continuity.get("kind") == "continuous_action":
        first_ref = (c.get("binds") or [{}])[0]
        if (first_ref.get("source_kind") != "accepted_previous_end" or
                continuity.get("previous_end_sha256") != first_ref.get("sha256") or
                not SHA.fullmatch(str(continuity.get("previous_end_sha256", "")))):
            errors.append("continuous action needs the exact accepted previous endpoint")
    if c.get("opening_approved") is not True:
        errors.append("opening is not owner-approved")
    opening = c.get("opening_candidate") or {}
    first = (c.get("binds") or [{}])[0]
    if opening.get("sha256") != first.get("sha256") or not SHA.fullmatch(str(opening.get("sha256", ""))):
        errors.append("complete opening hash missing/different from IMAGE_1")
    if opening.get("kind") != "complete_acted_first_frame":
        errors.append("opening is not a complete acted first frame")
    if opening.get("cast_instances") != c.get("cast_instances") or opening.get("room_state") != c.get("room_state"):
        errors.append("opening cast/state differs from card")
    approval = load_receipt(root, c.get("approval_receipt"), errors, "owner approval")
    if (approval.get("actor") != "owner" or approval.get("decision") != "accepted"
            or approval.get("opening_sha256") != first.get("sha256")
            or approval.get("plan_sha256") != fingerprint(c)
            or not approval.get("source_url") or not approval.get("reviewed_at")):
        errors.append("exact owner approval missing or stale")
    for b in c.get("binds", []):
        if b.get("missing_reason") or not SHA.fullmatch(str(b.get("sha256", ""))) or not URL.fullmatch(str(b.get("remote_url", ""))):
            errors.append(f"{b.get('id')}: unresolved binding")
        if b.get("human_decision") != "accepted" or b.get("hud_present") is not False:
            errors.append(f"{b.get('id')}: input acceptance/HUD proof missing")
    access = load_receipt(root, c.get("access_receipt"), errors, "recipient access")
    if (access.get("kind") != "ACCESS_ACK" or access.get("recipient") != "grok"
            or access.get("bind_sha256s") != {b["id"]: b.get("sha256") for b in c.get("binds", [])}
            or not access.get("source_url") or not access.get("checked_at")):
        errors.append("recipient access not established for these inputs")
    check_request(c, root, errors)
    return errors

def check_card(path, errors, root=ROOT):
    try:
        c = read(path)
        sid = c.get("shot_id")
        local = []
        if c.get("schema") != "reef.grok.shot-plan.v2" or sid != path.parent.name:
            local.append("schema or folder ID mismatch")
        chars = read(root / "canon/IDENTITY.json")["characters"]
        refs = read(root / "canon/REFERENCES.json")["references"]
        fixtures = read(root / "canon/FIXTURE_STATES.json")
        dependencies = read(root / "canon/SOURCE_DEPENDENCIES.json")["by_shot"].get(sid, {})
        if c.get("depends_on_events") != dependencies.get("depends_on_events") or not set(dependencies.get("source_shot_dependencies", [])).issubset(c.get("depends_on", [])):
            local.append("source shot/event dependencies lost")
        if dependencies.get("historical_hold") and not c.get("hold"):
            release = load_receipt(root, c.get("hold_release_receipt"), local, "HOLD release")
            if release.get("decision") != "release_hold" or release.get("shot_id") != sid or release.get("plan_sha256") != fingerprint(c) or not release.get("source_url"):
                local.append("source HOLD cannot be silently removed")
        for flag in ("generation_allowed", "opening_approved", "delivery_accepted", "still_attempt_allowed", "hold"):
            if type(c.get(flag)) is not bool:
                local.append(f"{flag}: must be boolean")
        if c.get("delivery_accepted"):
            local.append("motion-reference workflow cannot accept delivery")
        cast = c.get("exact_cast", [])
        if not cast or len(cast) != len(set(cast)) or any(k not in chars for k in cast):
            local.append("cast missing, duplicate, or undefined identity")
        instances = c.get("cast_instances", [])
        instance_ids = [i.get("instance_id") for i in instances]
        if (len(instance_ids) != len(set(instance_ids)) or set(i.get("character_id") for i in instances) != set(cast)
                or any(not i.get("start_visibility") or not i.get("end_visibility") for i in instances)):
            local.append("instance counts/temporal visibility incomplete")
        counts = c.get("exact_prop_counts")
        if not isinstance(counts, dict) or not counts or any(type(v) is not int or v < 0 for v in counts.values()):
            local.append("prop counts must be explicit nonnegative integers")
        for field, source in (("room_state", "by_shot"), ("end_room_state", "end_by_shot")):
            state = c.get(field)
            if not isinstance(state, dict) or not state or "note" in state or state != fixtures[source].get(sid):
                local.append(f"{field}: missing or differs from canon")
        if c.get("canon_sha256") != canon_hash(root):
            local.append("stale canon fingerprint")
        cam = c.get("camera", {})
        if cam.get("verb") not in CAMERAS or type(cam.get("move_count")) is not int or CAMERAS.get(cam.get("verb")) != cam.get("move_count") or not cam.get("address"):
            local.append("one named camera verb/address required")
        duration = c.get("duration_seconds")
        if type(duration) not in (float, int) or not 2 <= duration <= 8:
            local.append("duration outside 2..8")
        if c.get("aspect_ratio") != "16:9" or c.get("delivery_size") != [1280, 720]:
            local.append("wrong delivery aspect/size")
        binds = c.get("binds", [])
        if not 2 <= len(binds) <= 4 or c.get("bind_count") != len(binds):
            local.append("2..4 binding slots required")
        for idx, b in enumerate(binds, 1):
            if b.get("id") != f"IMAGE_{idx}" or b.get("role") not in ROLES:
                local.append("duplicate/out-of-order binding or invalid role")
            if idx == 1 and b.get("role") != "approved_clean_first_frame":
                local.append("IMAGE_1 is not a complete opening")
            if b.get("missing_reason"):
                if any(b.get(k) is not None for k in ("sha256", "remote_url", "path", "reference_id")):
                    local.append("missing binding cannot carry fallback pixels")
            else:
                if not SHA.fullmatch(str(b.get("sha256", ""))) or not URL.fullmatch(str(b.get("remote_url", ""))):
                    local.append("resolved binding needs immutable URL/full hash")
                if not b.get("path") or Path(str(b["path"])).is_absolute() or ".." in Path(str(b["path"])).parts:
                    local.append("invalid packet-relative image path")
                if any(t in str(b.get("path", "")).lower() for t in ("board", "contact_sheet", "montage", "runtime_capture")):
                    local.append("forbidden bound pixels")
                rid = b.get("reference_id")
                if rid in refs and (b.get("sha256") != refs[rid]["sha256"] or b.get("remote_url") != refs[rid]["remote_url"]):
                    local.append("binding differs from registered source")
        for ref in c.get("preparation_references", []):
            r = refs.get(ref.get("reference_id"))
            if r is None or ref.get("sha256") != r["sha256"] or ref.get("remote_url") != r["remote_url"]:
                local.append("preparation reference unresolved/stale")
        prompt_path = inside(path.parent, c.get("prompt_path"))
        prompt = prompt_path.read_text(encoding="utf-8")
        lines = [line.strip() for line in prompt.splitlines() if line.strip()]
        if len(prompt) > 1400 or not lines or not lines[-1].startswith("Sound:") or sum(l.startswith("Sound:") for l in lines) != 1:
            local.append("prompt must be short and end with one Sound: line")
        if c.get("prompt_sha256") != filehash(prompt_path):
            local.append("stale prompt hash")
        if not c.get("end_state") or f"end: {c['end_state']}" not in prompt:
            local.append("prompt endpoint differs from card")
        if any(t in prompt.lower() for t in ("sha256", "database.json", "delivery_accepted")):
            local.append("archive metadata in prompt")
        if c.get("attempts_used", 0) >= c.get("attempt_cap", 3) and not c.get("hold") and not c.get("attempt_cap_override_receipt"):
            local.append("attempt cap exhausted without HOLD/override")
        if c.get("still_attempt_allowed"):
            local.append("still dispatch requires a separate scoped preparation request, not this motion plan flag")
        if c.get("request") and not c.get("generation_allowed"):
            check_request(c, root, local)
        if c.get("generation_allowed") or c.get("opening_approved"):
            local.extend(readiness(c, root))
        elif not c.get("blocking_findings") or not c.get("blocking_reason"):
            local.append("blocked draft must state its blockers")
        errors.extend(f"{sid}: {e}" for e in local)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"{path}: invalid card/data: {exc}")

def check_preparation(path, root):
    errors = []
    try:
        req = read(path)
        c = read(inside(root, f"shots/{req['shot_id']}/CARD.json"))
        refs = read(root / "canon/REFERENCES.json")["references"]
        if req.get("request_sha256") != digest({k: v for k, v in req.items() if k != "request_sha256"}):
            errors.append("preparation request hash mismatch")
        if req.get("plan_sha256") != fingerprint(c) or req.get("required_room_state") != c["room_state"] or req.get("required_cast_instances") != c["cast_instances"]:
            errors.append("preparation plan/state/cast stale")
        if req.get("brief_sha256") != filehash(root / "shots" / c["shot_id"] / "FIRST_FRAME_BRIEF.txt") or req.get("still_prompt_sha256") != filehash(path.parent / "STILL_PROMPT.txt"):
            errors.append("preparation brief/prompt stale")
        if (req.get("kind") != "PREPARATION_REQUEST" or req.get("motion_authorized") is not False
                or req.get("opening_approved") is not False or req.get("delivery_accepted") is not False
                or req.get("maximum_candidates_this_request") != 1 or req.get("stop_after_return") is not True):
            errors.append("preparation scope must be one unapproved still, never motion")
        attempt = req.get("attempt")
        if type(attempt) is not int or not c["attempts_used"] < attempt <= c["attempt_cap"] or c["hold"]:
            errors.append("preparation attempt cap/HOLD violation")
        sources = req.get("source_references", [])
        if not 2 <= len(sources) <= 4:
            errors.append("preparation needs 2..4 role-bound sources")
        for i, source in enumerate(sources, 1):
            expected = refs.get(source.get("reference_id"), {})
            if source.get("slot") != f"SOURCE_{i}" or source.get("sha256") != expected.get("sha256") or source.get("remote_url") != expected.get("remote_url"):
                errors.append("preparation source slot/hash/URL differs")
        if "ACCESS_ACK" not in req.get("dispatch_gate", ""):
            errors.append("preparation recipient access gate missing")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"invalid preparation request: {exc}")
    return errors

def validate(root=ROOT, require_ready=False):
    errors = []
    cards = sorted((root / "shots").glob("SHOT-*/CARD.json"))
    try:
        queue = read(root / "queue.json")["ordered"]
        ids = [row["shot_id"] for row in queue]
        if len(cards) != 36 or len(ids) != len(set(ids)) or sorted(ids) != [p.parent.name for p in cards]:
            errors.append("expected 36 unique matching queue/cards")
        q = {r["shot_id"]: r for r in queue}
        ready = 0
        for path in cards:
            check_card(path, errors, root)
            card = read(path)
            for k in ("generation_allowed", "opening_approved", "hold", "exact_cast", "bind_count", "attempts_used", "blocking_reason"):
                if q.get(card["shot_id"], {}).get(k) != card.get(k):
                    errors.append(f"{card['shot_id']}: queue differs for {k}")
            blockers = readiness(card, root)
            if not blockers:
                ready += 1
            if require_ready:
                errors.extend(f"{card['shot_id']}: NOT_READY: {e}" for e in blockers)
        for request in (root / "preparation").glob("*/REQUEST.json"):
            errors.extend(f"{request.parent.name}: {e}" for e in check_preparation(request, root))
        return errors, len(cards), ready
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return errors + [f"invalid queue/canon: {exc}"], len(cards), 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    errors, count, ready = validate(args.root, args.require_ready)
    print(f"{'FAIL' if errors else 'PASS'} {'READINESS' if args.require_ready else 'PLANNING'}: {count} cards; {ready} ready; {count-ready} blocked")
    for error in errors:
        print(" -", error)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
