# Racer visual-context reconstruction — 2026-11-05

Status: **PROPOSED / CANDIDATE**, isolated `codex/reef-kart-art-20261104` demo branch. Baseline `7ad71c329c336ddb75c53bef0e38ac73b25f585f`. No dev/master integration or release is included.

The owner requests clear ground boundaries and start/finish representation in all versions, authorizes context-specific new item artwork under the master audit, and requests a review of every visual role in this minigame. [Impact](../../../design/audit_impacts/reef-kart-visual-context-20261105.json). [Exact request](../../../assets_src/imagegen/reef_kart_context_20261105/owner_request.json). This bounded direction supersedes the no-new-content restriction of ODR-TRACK-FIDELITY-20261103 for this Racer object reconstruction; approved room identity and protected originals remain binding.

## Ground readability

The room-course field was allocated at 512×512 but its final byte loop wrote only 128×128 entries. The remaining zeros classified most of the map as road. The loop now writes every texel. The PC regression samples centre-line positions and both shoulders throughout each course, beyond the previously written first 32 rows.

All four PC courses and the original touch-driven Pearl Canal share continuous dark edge contours, broad contrasting curbs, a pale inner line, a gold-framed checker start/finish stripe and large approach chevrons. Wood bridges keep their own surface inside the boundaries. Room finish arches reuse the existing Pearl arch and checker banner. Near-camera span fading clears the starting view before the posts dominate it; independently projected feet remain intact.

The course outlines and collision/handling widths are unchanged. Room palettes distinguish the road from its surroundings. The wall-band crop excludes the painted room floor so the skyline does not suggest a second track.

## Every visual role reviewed

The [project inventory](../../../assets_src/imagegen/reef_kart_context_20261105/project_asset_inventory.json) indexes 2,428 raster assets. The review examines the 78-asset racer family and 408 additional relevant alternative candidates through labelled contact boards. This is a contextual Racer review, not an artistic certification of every project asset. The [per-asset decisions](../../../assets_src/imagegen/reef_kart_context_20261105/visual_decisions.json) record reuse, crop, replacement or retirement without deleting originals.

| Visual role | Result |
|---|---|
| Road, shoulders, rail, bridges, start/finish | Whole-map field repaired; shared ground markings and readable material boundaries. |
| Room walls and Canal background/depth cards | Existing approved compositions reused; room floors cropped out of the skyline. Native background coverage and device acceptance remain open. |
| Context-specific new objects | Shell item capsule, kelp ribbon trap, bend chevron sign, toy block stack, play tent, kitchen teapot, seahorse basin sculpture. |
| Kitchen scenery | Whole existing oven, cake and pitcher reused, with tight non-destructive atlas regions that align the visible base to the ground. |
| Pool scenery | Existing whole shell fountain reused. Complete star/flower motifs retained at reduced width; resizing does not add native detail. |
| Opera scenery | Existing musicbox, microphone and trophy reused. Complete footlights kept at reduced width. |
| Old contaminated room cutouts | Nine retired from this Racer configuration; book/room sources preserved. Seven old role bindings replaced by the new object candidates. |
| Cast, vehicles and selection | Existing identities, portraits and vehicle families preserved. The other cast still uses composite riders rather than bespoke authored rear/turn pose families; that is a future art gap. |
| Item types, currency, buoys and roulette | Capsule distinguishes item rolls from pearl currency. Kelp world art and icon share the same motif. Pearl bundle, sparkle, zoom, gem buoys and pearl sources retained. No new item mechanics. |
| HUD, touch/controller controls and feedback | Existing control geometry, minimap, countdown, position indicator and results retained. Item icons preserve aspect; PC roulette displays the capsule. |
| Motion/effects | Existing separate shadows, spin stars, boost streaks, bubbles and confetti retained. New props contain no baked room backdrop or fake separate animation. |

Props now clear every road section, including neighbouring switchbacks. Reduced density limits overlap. Crops are atlas regions around complete reused objects; no source pixels are destructively edited.

## Seven bounded generation jobs

[Generation packets](../../../assets_src/imagegen/reef_kart_context_20261105/generation_jobs.json) bind references by file-byte SHA-256, prompts, role, world size, support, identity/material/palette limits, placements, attempt limits and runtime review plan. Each object used one built-in ImageGen call. Provider model revision, seed, monetary usage and request identifiers were not exposed; those limits are recorded rather than invented. No separately paid API calls or character redesign were made.

Native RGBA outputs are retained separately from exports. [Export mappings](../../../assets_src/imagegen/reef_kart_context_20261105/runtime_exports.json) record exact source/output hashes, alpha-bound crops, margin, proportional Lanczos fitting and content rectangles. All seven runtime PNGs are 1024-square RGBA with mipmaps. The [runtime texture check](../../../assets_src/imagegen/reef_kart_context_20261105/evidence/runtime-textures.log) measures the imported textures loaded by Godot and confirms ten mip levels for each. Alpha is preserved inside the crop; the alpha threshold only selects bounds. [Structural checks](../../../assets_src/imagegen/reef_kart_context_20261105/structural_validation.json) reject empty, wrong-size, opaque-backdrop and stray-edge controls before checking the shipped candidates. The validator also checks source/reference/prompt hashes and import settings.

The local AI appearance review is limited to still-object silhouette, whole contour, motif, material, palette, isolation and context fit. Applicable dimensions reach the 4.5/5 candidate floor after the recorded placement corrections; no 5/5 owner acceptance is claimed. [Scores and limitations](../../../assets_src/imagegen/reef_kart_context_20261105/local_visual_review.json). Static props have no authored action/loop to certify; runtime bobbing and existing effects remain engine behavior.

## Runtime evidence and limits

[Captures](../../../assets_src/imagegen/reef_kart_context_20261105/review/candidate/captures.json) bind current Godot 4.7.2-stable **Forward Mobile** frames by SHA-256. They cover all four courses in solo and split screen at grid, finish approach and bend; all selected prop families; item/kelp states; mode/garage/course selection/results; 1600×900 scaling; 1280×800 landscape; and the original Canal touch grid/approach/bend. [Baseline captures](../../../assets_src/imagegen/reef_kart_context_20261105/review/baseline/) preserve the pre-repair room views. Labelled review sheets are supporting comparisons, not delivery art.

These are explicitly posed renderer fixtures, including the results layout. They are not fresh canonical QA11 route certification, natural-play or physical-device evidence. One initial capture fixture referenced a nonexistent trap-array name and stopped; the fixture was corrected to the engine's existing `traps` array and rerun with empty stderr. Provenance validation also caught a draft record that hashed a path string; all new records were corrected against file bytes before publication.

Focused checks pass 44 PC and 45 original Canal assertions. The full local suite passes all 82 ordered trusted probes with zero process failures and unchanged classifiers. The [validation receipt](../../../assets_src/imagegen/reef_kart_context_20261105/validation_receipt.json) binds runtime-source and console hashes; final document authority/coverage evidence is tracked there and in the impact. The [GitHub CI receipt](../../../assets_src/imagegen/reef_kart_context_20261105/remote_ci_summary.json) records required pipeline success at runtime revision `b2bd2942`. Advisory reports remain distinct: Chef balance is capped, generic Racer balance does not support `kart_race`, and Sky Lagoon, dust-boss and castle visual receipts fail. Those reports do not establish visual acceptance or measure this Racer.

No master finding is closed: MA-OPERA-014 remains IN_PROGRESS; MA-VIS-008 and game-wide satisfaction retain their existing states. Physical USB/Bluetooth controllers, tablet performance/playback, child comprehension, exact canonical QA11 and owner visual acceptance remain outstanding.
