#!/usr/bin/env python3
"""Fail-closed structural check for Grok handoff v2. Does not inspect pixels."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROLES = {
    "empty_dirty_plate",
    "approved_first_frame",
    "subject_identity",
    "object_or_material_identity",
    "relationship_scale_contact",
}


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def check_card(path: Path, errors: list[str]) -> None:
    card = json.loads(path.read_text())
    sid = card.get("shot_id") or path.parent.name
    if card.get("schema") != "imagine-shot-packet-v2-reef":
        fail(f"{sid}: bad schema", errors)
    if sid != path.parent.name:
        fail(f"{sid}: folder mismatch {path.parent.name}", errors)
    binds = card.get("binds") or []
    n = len(binds)
    if n < 2 or n > 4:
        fail(f"{sid}: bind count {n} not in 2..4", errors)
    ids = [b.get("id") for b in binds]
    if ids and ids[0] != "IMAGE_1":
        fail(f"{sid}: IMAGE_1 must be first", errors)
    for b in binds:
        if b.get("role") not in ALLOWED_ROLES:
            fail(f"{sid}: bad role {b.get('role')}", errors)
    img1 = binds[0] if binds else {}
    if not card.get("opening_approved") and img1.get("people_in_plate") is True:
        fail(f"{sid}: IMAGE_1 has people but opening is not approved", errors)
    if card.get("generation_allowed") and not card.get("opening_approved"):
        fail(f"{sid}: generation_allowed without opening_approved", errors)
    if card.get("delivery_accepted"):
        fail(f"{sid}: delivery_accepted must stay false until owner yes", errors)
    cam = card.get("camera") or {}
    if cam.get("move_count") not in (0, 1):
        fail(f"{sid}: camera.move_count must be 0 or 1", errors)
    dur = card.get("duration_seconds")
    if not isinstance(dur, int) or dur < 3 or dur > 6:
        fail(f"{sid}: duration {dur} not in 3..6", errors)
    prompt = path.parent / "PROMPT.txt"
    if not prompt.is_file():
        fail(f"{sid}: missing PROMPT.txt", errors)
    else:
        text = prompt.read_text()
        if len(text) > 1200:
            fail(f"{sid}: PROMPT.txt {len(text)} chars > 1200", errors)
        if "Sound:" not in text:
            fail(f"{sid}: PROMPT.txt must end with Sound:", errors)
        if "sha256" in text.lower() or "DATABASE" in text:
            fail(f"{sid}: PROMPT.txt contains archive noise", errors)


def main() -> int:
    errors: list[str] = []
    shots = sorted((ROOT / "shots").glob("SHOT-*/CARD.json"))
    if len(shots) != 36:
        errors.append(f"expected 36 cards, found {len(shots)}")
    for p in shots:
        check_card(p, errors)
    queue = json.loads((ROOT / "queue.json").read_text())
    qids = [r["shot_id"] for r in queue["ordered"]]
    cids = [p.parent.name for p in shots]
    if sorted(qids) != sorted(cids):
        errors.append("queue ids do not match shot folders")
    if len(qids) != len(set(qids)):
        errors.append("queue has duplicate shot ids")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK {len(shots)} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
