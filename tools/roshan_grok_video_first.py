"""Video-first dispatch content; never invokes a generator or grants approval."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SOURCE_COMMIT = "ca4dd1963ad36aab420d5f228189231dae924c73"
SOURCE_BASE = "https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/" + SOURCE_COMMIT + "/assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/"
CONTROL_FILES = {"HANDOFF_PACKET.json", "IMAGINE_HANDOFF.json", "PUBLICATION.json"}

START = """ROSHAN: GENERATE ONE SWIMMING VIDEO FIRST

You are directing motion auditions. Imagine makes the video; Codex later reconstructs selected movement in Aseprite. Do not draw storyboards, pose sheets or replacement character art. Do not explain Aseprite. The first deliverable is RSW-01: one playable, continuous eight-second video of the pictured Roshan.

1. Confirm this session can actually invoke image-to-video and return its original video file. Reading GitHub or generating still images does not establish that capability. If video is unavailable here, say VIDEO_TOOL_UNAVAILABLE and supply the RSW-01 prompt and two image links for Imagine's video interface. STOP; no still-board fallback.
2. Use VIDEO_OPERATOR.txt to attach the exact opening as the first frame and the approved painting as identity guidance. URLs in chat are not proof of tool attachment. Reuse an already recorded approval for these exact opening bytes; otherwise show only the RSW-01 opening for approval. Do not ask about the later profile opening yet. Reuse already-recorded generation authorization; ask only about new paid/API spending.
3. Send only shots/RSW-01/PROMPT.txt to the video generator, with those two image roles. Preserve the pictured painted storybook character, not a generic mermaid. Return the actual video plus which inputs/mode were used. Unknown seed/FPS metadata can remain unknown; Codex can inspect the returned file. Do not fabricate tool access, attachment or output.
4. Watch the clip at normal speed: is this Roshan, does she swim rather than fly, and is her curiosity visible? No RSW-02 through RSW-08 until a real RSW-01 video has been returned and reviewed for that purpose. A technically playable file alone is not artistic acceptance. If the pilot is adequate for comparison, proceed with RSW-02, then 03-06, then the 07/08 loop studies.

The full commission remains eight samples with at most two replacement takes (ten generation attempts total, including failed attempts). After two failures with one method, reassess it. No additional paid batch or redesign is implied.

Archive publication is reported in IMAGINE_HANDOFF.json with its committed PUBLICATION.json receipt. That status is separate from input approval, tool readiness and video acceptance. Do not copy old status from commit ca4dd196. Audit records stay outside the pasted motion prompt. Full sample descriptions and combination criteria remain in README.md; they are not instructions to make a montage.
"""

OPERATOR = """VIDEO OPERATOR — NOT THE GENERATION PROMPT

FIRST JOB: RSW-01 only. Deliver a real video, not boards, stills, a slideshow, an animated camera over a still, or a claim that footage exists.

IMAGE INPUTS
RSW-01 through RSW-06:
  IMAGE_1 opening / actual first-frame input: {front_url}
RSW-07 and RSW-08 (later, not a prerequisite for RSW-01):
  IMAGE_1 opening / actual first-frame input: {side_url}
Every job:
  IMAGE_2 subject identity: {identity_url}
These are immutable original-archive URLs. Exact copies are also inside this ZIP under openings/ and references/. If URLs cannot be attached, upload the actual PNG files. Never substitute a GitHub page screenshot, board, newly generated image, or remembered design.

ROUTE TO AN ACTUAL VIDEO TOOL
- Report the available video tool/model and whether it can accept an actual first frame AND a separate identity reference. Do not infer availability from a conversational promise or access to image generation.
- Image-to-video and text-to-image are different operations. Two pictures pasted in chat are not evidence that either reached the video request. Record actual selected/uploaded inputs, IDs or request evidence when exposed. If that evidence is unavailable, say so; do not invent it.
- A supported image-plus-reference video mode is preferred. Official API documentation checked 2026-09-13 distinguishes grok-imagine-video-1.5, which supports a pinned first frame plus references, from classic grok-imagine-video, which rejects that combination. A consumer chat may expose neither mode. Do not silently drop IMAGE_2 or convert the job into text-to-video; report the limitation and route to a compatible video interface.
- If this chat has no video tool: output VIDEO_TOOL_UNAVAILABLE, these image links and the RSW-01 prompt, then stop. Do not generate still boards as a substitute. The owner can carry that small job to Imagine's video interface. A paid API is a separate owner-authorized option, not an automatic fallback.

CONTROLS AND APPROVAL
Request 8 seconds, 16:9, 720p, fixed camera, silent. Camera stability is judged in the resulting video; it is not guaranteed by choosing 720p. Keep native FPS and original audio/provenance tracks if the tool cannot suppress them; report the limitation. No interpolation, frame duplication, watermark removal or auto-enhancement. Unknown seeds and FPS are not a reason to demand a new prompt or invent data; Codex measures the downloaded file.
If a requested duration, resolution or image-input mode is unsupported, disclose the actual supported option before changing the test. Do not mislabel 6 seconds as 8 or stretch it to fit. Generated technical deviations may still be useful inspiration, but are not a passing matched sample or loop study.
Exact new opening approval is still pending in the archive. If the owner has already approved these exact bytes in the current exchange, record that decision once rather than asking again. Character identity approval alone is not new-layout approval. Profile approval is needed only before RSW-07/08. No human decision is prefilled by this update.

CREATIVE PRIORITY
The supplied painted character is the design authority. Preserve the young face, crown/blue gem, pink bodice/lilac frills, pearlescent tail and broad iridescent fin. The loose brown hair has an anatomical-left rainbow streak, not a ponytail. Do not replace the costume with shells, add adult glamour, or flatten the art into a new vector/cel style.
Animate a warm curious child who is comfortable in water. Eyes notice; head/chest decide; tail propels; elbows and wrists articulate; curls and fin follow later. Preserve design and proportions, NOT literal pixel positions or a rigid pose. Video generation cannot promise pixel-identical anatomy in changed poses. No unrelated elaborate finger acting.

RETURN AND CONTINUATION
Return RSW-01_take-01.mp4 (or the disclosed original video format), a playable preview/download and the prompt/input/mode used. A stream-only link is insufficient if the original can be downloaded. Do not start video editing or Aseprite conversion here.
Use CAPABILITY_CHECK.template.json for the short tool/input record. The longer RETURN_MANIFEST.template.json is downstream intake for Codex; missing technical metadata does not justify substituting pictures for footage. Keep original failed videos, name the issue and timecode, and do not inflate ratings.
One returned video proves the tool path; normal-speed identity/motion review determines whether the pilot is adequate to proceed. Keep RSW-02 comparable with 01. The eventual eight studies and two replacement attempts are a total cap, not an instruction to launch ten jobs at once. Loop jobs must perform two genuine three-second cycles with handles, not duplicate or reverse footage. Preferred whole performances and compatible timecoded combinations are evaluated AFTER video returns.

DOCUMENTATION (operator context only)
https://docs.x.ai/developers/model-capabilities/video/image-to-video
https://docs.x.ai/developers/model-capabilities/video/reference-to-video
"""


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def refresh(packet: Path):
    """Revise dispatch without repainting, rescaling, or resetting source approvals."""
    (packet / "START_HERE.txt").write_text(START, encoding="utf-8", newline="\n")
    (packet / "VIDEO_OPERATOR.txt").write_text(OPERATOR.format(front_url=SOURCE_BASE + "openings/front-right.png", side_url=SOURCE_BASE + "openings/right.png", identity_url=SOURCE_BASE + "references/approved-front.png"), encoding="utf-8", newline="\n")
    save(packet / "CAPABILITY_CHECK.template.json", {
        "schema": "roshan-video-capability-check-v1", "session_video_tool": None,
        "model": None, "can_return_original_video": None, "first_frame_plus_identity_supported": None,
        "actual_mode": None, "actual_attached_inputs": [], "request_evidence": None,
        "opening_approval_evidence": None, "account_authorization_evidence": None,
        "unsupported_controls": [], "status": "NOT_CHECKED", "pilot_video_path": None,
        "pilot_video_sha256": None, "normal_speed_review": None, "continue_batch": False,
        "if_unavailable": "VIDEO_TOOL_UNAVAILABLE; provide prompt and image links; no still-board substitution"})
    for card_path in sorted((packet / "shots").glob("*/SHOT_PACKET.json")):
        card = json.loads(card_path.read_text(encoding="utf-8"))
        prompt_path = packet / card["prompt_path"]
        prompt = prompt_path.read_text(encoding="utf-8")
        prompt = prompt.replace("locked camera on IMAGE_1. animate Roshan's", "animate the pictured Roshan in one continuous video, with a locked camera on IMAGE_1. show her")
        style = "preserve the painted storybook finish of the supplied art, including its soft shading and iridescent materials; do not redesign it as vector/cel art, an adult mermaid or a shell-bra costume."
        if style not in prompt:
            prompt = prompt.replace("\n\nend:", "\n\n" + style + "\n\nend:")
        prompt_path.write_text(prompt, encoding="utf-8", newline="\n")
        card["prompt_sha256"] = hashlib.sha256(prompt_path.read_bytes()).hexdigest()
        for ref in card["bound_references"]:
            ref["remote_url"] = SOURCE_BASE + ref["path"]
            ref["input_binding_status"] = "NOT_VERIFIED_IN_VIDEO_TOOL"
        card["execution"] = {"deliverable": "original_continuous_video", "fallback_to_stills": False,
            "stage": "pilot" if card["shot_id"] == "RSW-01" else "after_reviewed_video_pilot",
            "actual_tool_mode": None, "capability_evidence": None}
        card["blocking_findings"] = ["exact IMAGE_1 approval must be recorded", "actual video tool and two input bindings must be verified"]
        save(card_path, card)
    intake_path = packet / "RETURN_MANIFEST.template.json"
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    intake["instructions"] = "Codex downstream intake: preserve original actual videos and fill measurable metadata after receipt. Operator supplies RSW-01 first; unknown values stay null. No still-board substitutes or fabricated reviews."
    intake["pilot_first"] = True
    intake["maximum_generation_attempts"] = 10
    for item in intake["candidates"]:
        item["prompt_sha256"] = hashlib.sha256((packet / f"shots/{item['sample_id']}/PROMPT.txt").read_bytes()).hexdigest()
    save(intake_path, intake)
    handoff_path = packet / "IMAGINE_HANDOFF.json"
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    handoff.update({"archive_status": "incomplete", "archive_remote": None,
        "publication_receipt": "PUBLICATION.json", "publication_receipt_sha256": None,
        "generation_status": "blocked", "delivery_status": "not_accepted",
        "first_job": "RSW-01", "video_capability_status": "NOT_CHECKED",
        "blocking_findings": ["RSW-01 exact opening approval must be recorded; profile approval is deferred until 07/08", "actual image-to-video tool access and two-image attachment are unverified"],
        "claims": {"ARCHIVE_COMPLETE": False, "GENERATION_READY": False, "DELIVERY_ACCEPTED": False}})
    save(handoff_path, handoff)


def publication_errors(packet, archive, handoff):
    """Validate the external control envelope without a self-referential payload hash."""
    if handoff["archive_status"] != "complete":
        return []
    errors = []
    path = packet / "PUBLICATION.json"
    if not path.is_file():
        return ["complete archive missing committed publication receipt"]
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if hashlib.sha256(path.read_bytes()).hexdigest() != handoff.get("publication_receipt_sha256"):
        errors.append("publication receipt hash mismatch")
    if receipt.get("manifest_sha256") != hashlib.sha256((packet / "HANDOFF_PACKET.json").read_bytes()).hexdigest():
        errors.append("publication receipt does not bind current payload manifest")
    expected = {f["path"]: f["sha256"] for f in archive["files"]}
    actual = {f["path"]: f["sha256"] for f in receipt.get("files", [])}
    if actual != expected or len(receipt.get("files", [])) != len(expected) or receipt.get("payload_sha256") != archive["payload_sha256"]:
        errors.append("publication receipt does not bind every current payload file")
    if receipt.get("archive_remote") != handoff.get("archive_remote"):
        errors.append("publication remote mismatch")
    if handoff.get("claims") != {"ARCHIVE_COMPLETE": True, "GENERATION_READY": False, "DELIVERY_ACCEPTED": False}:
        errors.append("publication must not imply generation or delivery acceptance")
    return errors
