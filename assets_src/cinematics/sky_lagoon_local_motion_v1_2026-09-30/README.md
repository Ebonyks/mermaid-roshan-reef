# Sky Lagoon â€” ten object motion studies and local Wan evaluation

Owner commission: 2026-09-30. Source baseline: `7f068cb80766edd52a110cc1cb3958158f829822`.
Status: `OWNER_REJECTED_AS_ANIMATION_REPLACEMENT / MOTION_REFERENCE_ONLY`. No game or runtime source changes.

Open [the animated review gallery](index.html), [ten-object overview](overview.gif),
or an individual editable Aseprite master under `objects/`.
The set covers fir, huckleberry, hydrangea, bellflower, cloud, smoke,
single-seat swing, seesaw, castle gate and stained-glass glint.

## Owner correction and new swing pose trial

The owner rejected this set as the requested animation replacement: it transforms
existing items, and the swing moves on the wrong axis. “Some are better than
others” grants no individual acceptance. The former lateral swing is rejected.
Its masters, previews and machine checks remain historical evidence.

The corrected swing rotates about the **horizontal suspension beam**. The seat
moves toward and away from the camera, changing inclination, visible surfaces
and occlusion; the frame and hooks stay fixed. That requires new drawn poses.
[The exact review and corrected brief](qc/OWNER_REVIEW.json) record this distinction.

[The new swing trial](pilots/swing_pose_v2/preview.gif) uses eight newly generated
seat drawings, local rope-removal inpainting, and explicitly raster-painted
suspension in [an editable Aseprite master](pilots/swing_pose_v2/swing_pose_v2.aseprite).
The original approved frame stays fixed. Every output pixel is painted in
Aseprite. A uniform 5/16 sampling step and per-pose horizontal registration fit
the new drawings into the reference canvas; the old seat supplies identity only.
This is a built-in ImageGen pose-reference pilot, not a Chinese video API result
or human hand drawing. [Prompts](pilots/swing_pose_v2/PROMPTS.json), native outputs,
the Lua recipe and [raster evidence](pilots/swing_pose_v2/PILOT_RECEIPT.json) are preserved.

The pilot is **unaccepted**. Native cells 6–8 touch their boundaries; seat detail
varies, socket/contact and constant-length perspective need review, and fresh
in-between drawings are missing. Eight rough keys do not finish the requested
ten-object redraw set. The original byte checks prove integrity, not animation
quality or the correct axis. All runtime/cinematic/device/child gates stay open.

## What these files actually are

The original studies are **scripted source-based transformations in Aseprite**, with 32
timed RGBA states at nominal 12 fps. The Lua authoring tool paints each output
pixel into a blank image using `Image.drawPixel`. It samples the existing art
through explicit bends, rigid articulation/projection or a traveling light band.
This is spatial resampling/source reuse, not fresh hand-painted frame redraws,
AI-generated action poses or full-frame cinematic regeneration. The hidden
source layer remains available in each master. Symmetric return motion revisits
the same pose; 32 timed states are not claimed to be 32 unique generated poses.

The source originals are preserved byte-for-byte. Each object includes an
isolated identity card, actual source copy, inspectable beat board, animated
preview, editable master, POT 2048x1024 atlas and timing JSON. The single-seat
swing reuses an existing project source; two-seat trials with incomplete part
isolation are retained as rejected evidence. No source gap is passed off as new
approved art. The gate's study opening is transparent; it invents no room beyond.
The stained-glass source is a complete castle card, with only its window glinting.

## Local AI result

Wan 2.2 TI2V 5B completed the neutral-background hydrangea take in 561.49 seconds
and the stronger-prompt fir take in 481.00 seconds on the RTX 3060 Ti. Both upper
silhouettes moved less than one pixel at the 256px review scale. **Both are
rejected as static/flickering motion references.** Earlier FP8 and low-resolution
geometry failures and the compact-model performance interruption are retained
in the attempt records. Machine encoding success never grants motion acceptance.

The supported `--disable-mmap` native safetensors copy-loading option resolved
the observed Windows model-loading access violation for the completed fir run.
The 1280x704, 41-frame native recipe executed successfully; its motion quality
did not pass. Compact-model completion or quality is not claimed from the
interrupted 1280x704 attempt. A busy renderer must be left to its active client.

## Evidence and acceptance

[manifest.json](manifest.json) lists every payload file, bytes, hashes, roles,
dimensions, source path, modification and inherited license/provenance. Its
deterministic payload hash is the SHA-256 of sorted `path + tab + file hash +
newline` records. Operational remote-verification receipts are outside that
payload. The original `REMOTE_VERIFICATION_RECEIPT.json` verifies the historical
`29e59b1c` packet only. The owner-QC revision requires
`qc/REMOTE_VERIFICATION_QC_RECEIPT.json` after its own immutable publication.

[Machine verification](MACHINE_VERIFICATION.json) checks unchanged source
hashes, all 320 timed states, exact Aseprite pixel round trips, transparent RGB,
POT sheets, fixed roots/fixtures, silhouette displacement and traveling glint.
The manifest also records the raw RGBA SHA-256 of every atlas state. Original
source coordinates, declared root locks and geometric limitations stay explicit.

`ARCHIVE_COMPLETE` depends on anonymous remote verification at an immutable
GitHub revision. `GENERATION_READY` is **false** for external cinematic jobs:
backend credentials, applicable IMAGE_1 layout approval and a useful motion
pilot are still missing. `DELIVERY_ACCEPTED` is **false**. These source-based
warps/articulations are forbidden as authored cinematic delivery; reference-only
labeling supplies no exception. Fresh frame redraws have not been completed.
Owner selection, production topology/contact/loop review, runtime sampling,
Mobile/Speedy performance, phone and child acceptance remain open.

This archive changes no finding lifecycle and closes neither MA-VIS-002 nor
MA-VIS-006. Consult the [production protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md)
and the [master planning entry](../../../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry).

The unchanged game-source baseline has green [Linux CI](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/36791771742).
Native official Godot 4.7.2 import and all 82 existing trusted probes also have
passing results, using the original assertions and recorded normal/fixed clock
retries. [The combined summary](validation/BASELINE_NATIVE_GATES.json) preserves
the limits; the failed Windows Dust Boss timing and Castle transient-layout logs
remain alongside their passing retries. Exact whole Bash-on-Windows CI success
is not claimed. These baseline checks confer no creative acceptance.

## API alternatives for a new motion pilot

For a paid comparison, first test one five-second mechanical-object shot,
then select a backend from the observed motion and identity result. Fal lists
[Kling 2.5 Turbo Pro](https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video)
at $0.35 per five-second clip; its [I2V model overview](https://fal.ai/explore/image-to-video-apis)
lists Kling 3.0 Pro at $0.112/second without audio. MiniMax's
[H3 price page](https://platform.minimax.io/subscribe/token-plan?tab=api-enterprise)
lists $0.08/second at 768p and $0.13/second at 2K. These are checked list prices,
not a quality verdict for this artwork or permission to incur charges. Provider
accounts/credentials and the selected generation route are unresolved. No paid
job was submitted. Neither API tier bypasses the project's cinematic frame rules.

## Verify or rebuild without changing the archive

With Python/Pillow and Aseprite installed, run
`python production/verify_packet.py --aseprite "C:/Program Files/Aseprite/Aseprite.exe"`.
It checks every payload byte, all atlas states and an independent reopen/export
of all ten editable masters. To rebuild one separate derivative, run
`python production/rebuild_reference.py 03_hydrangea --output-directory C:/your-new-output`.
The output directory must be new and outside this archive. Source-based spatial
resampling is explicit; rebuilding does not create accepted cinematic frames.
The other production files retain the original local working-method source;
their old staging paths are historical, not the archive's runnable interface.
