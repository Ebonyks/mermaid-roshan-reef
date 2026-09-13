"""Build and verify a reference-only Grok archive, never generate video or accept art."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BRIEF = ROOT / "design/animation/roshan_grok_auditions_20260912.json"
REL = Path("assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12")
PACKET = ROOT / REL
VIEWS = ("front", "front-right", "right", "back-right", "back", "back-left", "left", "front-left")
LICENSE = "Project-generated derivative of (c) Mermaid Roshan LLC; all rights reserved. Reference use for this owner's commissioned study only."


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dimensions(path):
    with Image.open(path) as im:
        return list(im.size)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build(source, aseprite):
    brief = json.loads(BRIEF.read_text(encoding="utf-8"))
    metadata = {}

    def copy(src, dest, role):
        out = PACKET / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        metadata[dest] = {"source_path": str(src.relative_to(source)) if src.is_relative_to(source) else src.relative_to(ROOT).as_posix(), "source_sha256": sha(src), "role": role, "modification_status": "byte-identical copy", "source_scope": "local eight-view source study" if src.is_relative_to(source) else "current baseline context"}

    copy(source / "references/approved-front.png", "references/approved-front.png", "primary subject identity; explicitly owner-approved prior painting")
    copy(source / "references/approved-head-cleaned.png", "references/approved-head-cleaned.png", "archive face-detail reference; not an extra generator binding")
    for view in VIEWS:
        copy(source / view / "cutout.png", f"references/{view}.png", "turnaround reference; no motion acceptance")
        copy(source / view / "provenance.json", f"provenance/{view}.json", "historical generation provenance; original relative paths are historical, not packet dependencies")
    for name in ("manifest.json", "source-review-summary.json", "verification.json"):
        copy(source / name, "provenance/original-" + name, "historical source evidence; not current motion rating")
    for file in ("design/animation/ROSHAN_MOVEMENT_LANGUAGE.md", "design/animation/ANIMATION_PRODUCTION_PROTOCOL.md", "design/templates/IMAGINE_SHOT_CARD_V1.md"):
        copy(ROOT / file, "context/" + Path(file).stem + ".txt", "bound context snapshot; not generator pixels")
    copy(BRIEF, "context/AUDITION_BRIEF.json", "owner-scoped sample plan")
    for view in ("front-right", "right"):
        out = PACKET / f"openings/{view}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(aseprite), "-b", "--script-param", f"source={PACKET / ('references/' + view + '.png')}", "--script-param", f"output={out}", "--script", str(ROOT / "tools/aseprite/roshan_grok_openings.lua")], check=True, timeout=120)
        metadata[f"openings/{view}.png"] = {"source_path": f"references/{view}.png", "source_sha256": sha(PACKET / f"references/{view}.png"), "role": "proposed clean first-frame layout; human approval pending", "modification_status": "Aseprite uniform 1254-to-640 whole-cutout bilinear resize, placed at (120,40) on 1280x720 solid RGB(17,37,54); no character repaint/warp", "production_script": "tools/aseprite/roshan_grok_openings.lua", "production_script_sha256": sha(ROOT / "tools/aseprite/roshan_grok_openings.lua"), "approval": "pending"}

    common = ("keep the camera, navy observation field and character scale fixed; keep the entire crown, hands and fin inside the frame. "
              "preserve the young rounded face, brown eyes, gold crown with blue gem, loose brown curls, anatomical-left rainbow hair streak, pink bodice with lilac frills, and single pearlescent scaled tail with its broad iridescent fin from IMAGE_2. "
              "the streak is viewer-right in front view and stays attached to her anatomical left through turns, never a ponytail or mirrored near-side stripe. "
              "allow expressive shoulder rotation, bending elbows, following wrists and natural silhouette changes without changing body proportions. "
              "no straight locked flying arms, pinned fingertips, size pulsing, rubber fin, detached parts, extra limbs, legs, extra characters, props, text, hud, camera drift or cuts.")
    shots = []
    for sample in brief["samples"]:
        sid = sample["id"]
        folder = PACKET / "shots" / sid
        folder.mkdir(parents=True, exist_ok=True)
        prompt = "locked camera on IMAGE_1. animate Roshan's " + sample["register"] + " swimming performance.\n\n"
        prompt += "\n".join(f"{start:g}-{end:g}s: {action}." for start, end, action in sample["beats"])
        prompt += "\n\n" + sample["path"] + ". " + common + "\n\nend: " + sample["end"] + "\nSound: silent; no dialogue, voices or music.\n"
        (folder / "PROMPT.txt").write_text(prompt, encoding="utf-8", newline="\n")
        refs = []
        for index, (path, role, approved) in enumerate(((f"openings/{sample['opening']}.png", "approved_clean_first_frame", False), ("references/approved-front.png", "subject_identity", True)), 1):
            refs.append({"id": f"IMAGE_{index}", "role": role, "path": path, "sha256": sha(PACKET / path), "dimensions": dimensions(PACKET / path), "remote_url": None, "hud_present": False, "human_decision": "accepted" if approved else "pending", "approval_scope": "prior owner-approved front identity painting" if approved else "new flattened opening composition has not been human approved"})
        card = {"schema": "imagine-shot-packet-v1", "movie_id": brief["id"], "shot_id": sid, "status": "DRAFT", "mode": "image_to_video", "output_disposition": "motion_reference_only", "duration_seconds": 8, "aspect_ratio": "16:9", "delivery_size": [1280, 720], "bound_references": refs, "non_pixel_references": [{"path": "SHOT_BOARD.html", "used_as_pixel_reference": False, "role": "human timeline and source navigation only"}], "camera": {"verb": "locked", "move_count": 0}, "must_move": ["gaze and expression express the named intention", "shoulders, elbows and wrists articulate rather than translate as one rigid arm", "torso-to-tail propulsion with delayed broad-fin follow-through", "subtle independent curl and colored-strand follow-through"], "must_not_move": ["camera", "neutral navy field", "identity/costume/anatomical ownership; pose itself is not locked"], "end_state": sample["end"], "negative_constraints": ["no HUD", "no text", "no identity drift", "no pinned fingertips", "no rubber fin", "no boomerang or duplicate-video loop"], "prompt_path": f"shots/{sid}/PROMPT.txt", "prompt_sha256": sha(folder / "PROMPT.txt"), "sample_contract": sample, "blocking_findings": ["exact IMAGE_1 human approval pending", "immutable remote input URLs pending publication"]}
        write_json(folder / "SHOT_PACKET.json", card)
        shots.append(f"shots/{sid}/SHOT_PACKET.json")

    write_json(PACKET / "IMAGINE_HANDOFF.json", {"schema": "imagine-handoff-v1", "handoff_id": brief["id"], "archive_status": "incomplete", "generation_status": "blocked", "delivery_status": "not_accepted", "archive_remote": None, "shot_packets": [], "draft_shot_packets": shots, "blocking_findings": ["two exact new opening compositions require human approval", "immutable remote input links require publication and verification"], "scope": brief["scope"], "claims": {"ARCHIVE_COMPLETE": False, "GENERATION_READY": False, "DELIVERY_ACCEPTED": False}})

    intake = {"schema": "roshan-motion-reference-return-v1", "handoff_id": brief["id"], "instructions": "Keep unknown values null. Return original clips, not just a montage or streaming links. Never prefill acceptance.", "candidates": []}
    for sample in brief["samples"]:
        intake["candidates"].append({"sample_id": sample["id"], "take": 1, "video_path": None, "sha256": None, "prompt_sha256": sha(PACKET / f"shots/{sample['id']}/PROMPT.txt"), "input_hashes": [], "service_model": None, "settings": None, "seed": None, "created_at": None, "dimensions": None, "duration_seconds": None, "fps": None, "frame_count": None, "normal_speed_reviewed": False, "reviewer": None, "inferred_intention_before_reading_prompt": None, "knockouts": [], "observations": [], "scores": {axis: None for axis in ("intention", "character_warmth", "buoyancy_propulsion", "rhythm_spacing", "arm_body_integration", "normal_speed_appeal")}, "disposition": "unreviewed", "useful_fragments": [], "loop_candidate": None, "owner_selection": None})
    intake["shortlist"] = []
    intake["assembly_candidates"] = [{"id": "ASSEMBLY-01", "status": "unproposed", "timing_spine_video_sha256": None, "segments": [], "joins": [], "new_output_sha256": None, "normal_speed_review": None, "owner_selection": None}]
    intake["fragment_schema"] = {"source_sha256": None, "in_seconds": None, "out_seconds": None, "in_frame": None, "out_frame_exclusive": None, "use": "inspiration_only | adaptation_reference", "reason": None, "known_defects": [], "facing": None, "pose_phase": None, "pelvis_xy_normalized": None, "incoming_velocity": None, "outgoing_velocity": None}
    write_json(PACKET / "RETURN_MANIFEST.template.json", intake)

    opening_lines = "\n".join(f"- IMAGE_1 {view}: openings/{view}.png; SHA-256 {sha(PACKET / ('openings/' + view + '.png'))}" for view in ("front-right", "right"))
    start = f"""GROK HANDOFF: MERMAID ROSHAN SWIMMING PERFORMANCE AUDITIONS

Please produce EIGHT separate eight-second animation samples, RSW-01 through RSW-08, using the matching short PROMPT.txt files. These are motion/acting references for later sprite development, not final game or cinematic footage. Return the original videos separately so we can analyze them, choose up to three preferred whole performances, or propose an assembly from compatible beats. Up to TWO additional targeted replacement takes are allowed, maximum TEN returned samples. Do not start a paid/API batch without the account owner's normal generation authorization.

FIRST: open README.md, SHOT_BOARD.html and the two opening proposals below. Show these exact files and hashes for human approval. Do not claim the openings were already approved just because the character design was. If the archive cannot be read remotely, use the complete attached ZIP; never substitute remembered art, a screenshot, an old ponytail sprite, or a missing local Windows path.
{opening_lines}

IMAGE_2 for every sample: references/approved-front.png; SHA-256 {sha(PACKET / 'references/approved-front.png')}.
01-06 use the front-right opening; 07-08 use the right-profile opening. Bind only IMAGE_1 and IMAGE_2 to each job. Other views and the board are archive context, never extra image inputs. The board's repeated source thumbnails are NOT drawn action poses or approved video frames.

AFTER opening approval and input-link verification: use one shot per generation, locked camera, 16:9 at 1280x720 if supported. If the service cannot preserve these controls or accept both image roles, report the limitation before changing the test; never silently omit identity guidance. Use native generation FPS; no interpolation, automatic enhancement, camera motion, music, speech or montage. Do not interpret unknown alpha support as transparent delivery.

CREATIVE PRIORITY: a warm curious child at home in water, not a rigid superhero flying. Let eyes notice before head/chest commit; let shoulders, elbows and wrists articulate; a connected body-to-tail wave drives the broad fin, which trails rather than distorts. Preserve face/crown/costume, body proportions and the anatomical-LEFT rainbow hair streak (viewer-right in front view; no ponytail). Short effort followed by a generous glide. Gentle curls and colored strands respond independently. Avoid detailed finger pantomime. Do not freeze the whole body in the name of identity preservation.

Generate 01/02 as a matched A/B first; then 03-06; then 07/08. The final two must PERFORM two genuine continuous three-second cycles at 1-4s and 4-7s, with one second of motion handles at each end. Do not duplicate the first cycle, reverse it, boomerang it or hide a reset. Preserve the complete eight-second original even if a good interior loop can later be sliced out.

RETURN: eight individual native video downloads named RSW-XX_take-01.mp4 (or disclose actual format), plus the completed RETURN_MANIFEST.template.json. Preserve all rejected takes. Report model/settings/seed only if actually available. Give a normal-speed shortlist with specific timecoded reasons. An appealing moment in a flawed take can be labeled inspiration_only, never passed as clean delivery. Leave owner choice and all final-delivery statuses pending.

COMBINATIONS: propose exact source-hash/timecode segments and explain compatible view, scale, line of action, hand pose, tail/fin phase and speed at each join. Prefer one whole performance as the timing spine. A straight-cut assembly is a NEW reference to review, not an accepted animation. Do not combine unrelated moving limbs, crossfade, morph, mirror, use optical flow or conceal joins with holds. If a connecting motion is missing, use an available replacement take or state the gap.

Do not inflate scores to meet a target. After two failing attempts at the same brief/method, reassess the pose/reference/action rather than repeating the same prompt. No generation beyond ten, runtime integration, new character design, protected voice synthesis or final cinematic acceptance is authorized by this handoff.
"""
    (PACKET / "START_HERE.txt").write_text(start, encoding="utf-8", newline="\n")
    render_board(brief)
    for p in sorted(PACKET.rglob("*")):
        if p.is_file() and p.name != "HANDOFF_PACKET.json":
            rel = p.relative_to(PACKET).as_posix()
            meta = metadata.get(rel, {"source_path": "tools/build_roshan_grok_auditions.py and design/animation/roshan_grok_auditions_20260912.json", "role": "project-authored handoff instructions or structured evidence", "modification_status": "new project-authored document; no character delivery pixels"})
            meta.update({"path": rel, "sha256": sha(p), "bytes": p.stat().st_size, "dimensions": dimensions(p) if p.suffix == ".png" else None, "license_provenance": LICENSE if p.suffix == ".png" else "Project-authored instructions/evidence or verbatim project source provenance; original source attribution retained.", "source_url": "project-local source; immutable GitHub archive URL supplied by separate publication receipt"})
            metadata[rel] = meta
    files = [metadata[k] for k in sorted(metadata)]
    payload = "".join(f"{x['path']}\0{x['sha256']}\n" for x in files).encode()
    write_json(PACKET / "HANDOFF_PACKET.json", {"schema": "roshan-motion-audition-archive-v1", "id": brief["id"], "baseline": brief["baseline"], "source_study_branch": "codex/roshan-eight-views-imagegen-20260911", "source_study_base": "cdfd937a7db4b3d41e7c469fb8e6a8fe812cd016", "files": files, "payload_hash_algorithm": "sha256 of UTF-8 concatenation of sorted relative path + NUL + literal SHA256 + LF; excludes HANDOFF_PACKET.json only", "payload_sha256": hashlib.sha256(payload).hexdigest(), "scope": brief["scope"], "runtime_background_and_props": "not applicable: isolated motion-test field, one Roshan, no prop/contact or runtime seam; no room was redesigned", "approval": "opening proposals pending; native video and motion selection not yet produced"})


def render_board(brief):
    esc = html.escape
    head = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Roshan — eight motion auditions</title><style>body{font:16px/1.5 system-ui,sans-serif;background:#f7f5f0;color:#253346;margin:0 auto;padding:24px;max-width:1180px}h1{font-size:30px}h2{font-size:23px;margin-top:32px}a{color:#254cc0}img{max-width:100%;object-fit:contain;background:#112536}figure{margin:0}figcaption{font-size:14px}.openings{display:grid;grid-template-columns:1fr 1fr;gap:20px}.ring{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.ring img{width:100%;height:220px}.sample{padding:22px 0;border-top:1px solid #c9cfd5}.sample-head{display:grid;grid-template-columns:240px 1fr;gap:24px}.beats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:16px}.beat{border-top:4px solid #84acae;padding-top:8px}.beat b{display:block}.note{background:#e8edf0;padding:14px}code{overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}@media(max-width:700px){.openings,.sample-head{grid-template-columns:1fr}.beats{grid-template-columns:1fr 1fr}.ring{grid-template-columns:1fr 1fr}body{padding:16px}}@media print{.sample{break-inside:avoid}a{color:inherit}}</style><h1>Roshan: eight motion auditions</h1><p>Choose a performance worth adapting. These are source references and requested beats — no returned animation or drawn action frames yet.</p><p><a href="START_HERE.txt">Grok start message</a> · <a href="README.md">Operator and review guide</a> · <a href="RETURN_MANIFEST.template.json">Return manifest</a></p><p class="note">Motion-reference only. Exact opening layouts need human approval. Eight native videos requested; no scores or selections prefilled.</p><h2>Two opening proposals</h2><div class="openings">'''
    pieces = [head]
    for view, jobs in (("front-right", "RSW-01–06"), ("right", "RSW-07–08")):
        pieces.append(f'<figure><img src="openings/{view}.png" alt="Proposed {view} opening on neutral field"><figcaption>{jobs} · {view} · pending opening approval<br><code>{sha(PACKET / ("openings/" + view + ".png"))}</code></figcaption></figure>')
    pieces.append('</div><h2>Identity and turnaround context</h2><p>Rainbow streak belongs to her anatomical left. These thumbnails are source views, not temporal frames. Only the named two images are bound to each generation.</p><div class="ring">')
    for view in VIEWS:
        pieces.append(f'<figure><img src="references/{view}.png" alt="Roshan {view} source view"><figcaption>{view}</figcaption></figure>')
    pieces.append('</div><h2>Shot and beat board</h2>')
    for s in brief["samples"]:
        pieces.append(f'<section class="sample" id="{s["id"]}"><div class="sample-head"><img src="openings/{s["opening"]}.png" alt="{s["id"]} proposed opening, not an action pose"><div><h2>{s["id"]} · {esc(s["name"])}</h2><p>{esc(s["question"])}</p><a href="shots/{s["id"]}/PROMPT.txt">Paste-ready prompt</a> · <a href="shots/{s["id"]}/SHOT_PACKET.json">Draft shot card</a><p>{esc(s["path"])}</p></div></div><div class="beats">')
        for start, end, action in s["beats"]:
            pieces.append(f'<div class="beat"><b>{start:g}–{end:g} seconds</b>{esc(action)}.</div>')
        pieces.append('</div><p><b>End:</b> ' + esc(s["end"]) + '</p></section>')
    pieces.append('<p>Board is for human comparison and beat order only. Do not upload it as an image-generation input.</p></html>')
    (PACKET / "SHOT_BOARD.html").write_text("\n".join(pieces), encoding="utf-8", newline="\n")


def verify():
    from audit_imagine_handoff import audit_handoff, audit_shot
    errors = audit_handoff(PACKET)
    archive = json.loads((PACKET / "HANDOFF_PACKET.json").read_text(encoding="utf-8"))
    manifest = json.loads((PACKET / "IMAGINE_HANDOFF.json").read_text(encoding="utf-8"))
    files = archive["files"]
    listed = [x["path"] for x in files]
    actual = sorted(p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file() and p.name != "HANDOFF_PACKET.json")
    if listed != actual:
        errors.append("manifest coverage/order differs from actual packet files")
    for f in files:
        path = (PACKET / f["path"]).resolve()
        if not path.is_relative_to(PACKET.resolve()) or not path.is_file() or sha(path) != f["sha256"]:
            errors.append("file hash/path mismatch: " + f["path"])
        if not f.get("source_path") or not f.get("role") or not f.get("license_provenance") or not f.get("modification_status"):
            errors.append("missing provenance: " + f["path"])
        if path.suffix == ".png":
            with Image.open(path) as im:
                im.verify()
            if dimensions(path) != f["dimensions"]:
                errors.append("dimension mismatch: " + f["path"])
    payload = "".join(f"{x['path']}\0{x['sha256']}\n" for x in files).encode()
    if hashlib.sha256(payload).hexdigest() != archive["payload_sha256"]:
        errors.append("payload hash mismatch")
    if len(manifest["draft_shot_packets"]) != 8 or manifest["generation_status"] != "blocked" or manifest["shot_packets"]:
        errors.append("expected eight explicitly blocked draft jobs")
    expected_pending = []
    for rel in manifest["draft_shot_packets"]:
        card_path = PACKET / rel
        card = json.loads(card_path.read_text(encoding="utf-8"))
        pending = f"{card_path}: IMAGE_1 must be human accepted"
        found = audit_shot(PACKET, card_path, manifest)
        # Report the known gate as pending; never declare these cards ready.
        if found != [pending]:
            errors.extend(found or ["unexpectedly missing pending human gate: " + rel])
        expected_pending.append({"shot": card["shot_id"], "unpassed_gate": pending})
        prompt = (PACKET / card["prompt_path"]).read_text(encoding="utf-8")
        if not prompt.rstrip().endswith("Sound: silent; no dialogue, voices or music.") or "anatomical-left" not in prompt:
            errors.append("prompt direction/sound mismatch: " + rel)
    print(json.dumps({"archive_integrity": "PASS" if not errors else "FAIL", "draft_count": 8, "payload_file_count": len(files), "generation_ready": False, "expected_pending_human_gates": expected_pending, "errors": errors}, indent=2))
    return not errors


def make_zip(destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                archive.write(path, PACKET.name + "/" + path.relative_to(PACKET).as_posix())
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        for info in archive.infolist():
            path = PACKET / Path(info.filename).relative_to(PACKET.name)
            assert hashlib.sha256(archive.read(info)).hexdigest() == sha(path)
    print(json.dumps({"zip": str(destination), "sha256": sha(destination), "bytes": destination.stat().st_size}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path)
    p.add_argument("--aseprite", type=Path)
    p.add_argument("--verify", action="store_true")
    p.add_argument("--zip", type=Path)
    args = p.parse_args()
    if args.source:
        if not args.aseprite:
            p.error("--source requires --aseprite")
        build(args.source.resolve(), args.aseprite.resolve())
    if args.verify and not verify():
        return 1
    if args.zip:
        make_zip(args.zip.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
