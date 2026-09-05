# Day One draft boundary evidence — 2026-09-04

## Scope and confidence

This is a read-only visual evidence pass over the isolated `d1` worktree. I
inspected the actual PNG/JPG pixels listed below with the image viewer. These
are runtime-boundary references where provenance says so; storyboard/contact
sheet images are labelled as such and are not treated as runtime proof. No
Resolve process was started.

The existing Godot 4.7.2 bathroom probe was attempted with the repository's
official executable:

```text
tmp/godot472_handoff_validation/Godot_v4.7.2-stable_win64_console.exe
--headless --path .worktrees/d1 -s scripts/probe_day_one_bathroom_shots.gd
```

It failed before rendering with parse errors: `ReefMain`,
`DayOneBathroomCleanup`, and `DayOneBathroomCleaning` could not be resolved.
Therefore this pass does not claim a fresh current-runtime render for
bathroom or pool. The existing C09/C10 captures remain the only inspected
current-runtime boundary captures in the v3 packet.

The required `--headless --editor --import` scan completed its filesystem
initialization, but a second isolated capture attempt still failed during
resource loading. The d1 checkout has missing/unsupported imported resources,
including `boot_splash_mermaid_roshan.png` and multiple PNG/JPG textures
(`.godot/imported/*.ctex` absent; “no resource loaders/unrecognized file
extension”). Consequently no new PNGs were produced by the bathroom probe.

## Evidence inspected

| Area | Exact evidence | What the pixels establish | Draft seam disposition |
|---|---|---|---|
| C03 dirty bathroom | `assets_src/cinematics/day_one_bathroom_entry_v1/handoff_art/01_dirty_runtime_anchor.png`; `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C03/audit_evidence/scene_overview.jpg` and contact frames | Runtime anchor shows the actual tub/sink/toilet layout, Roshan scale, basket and pointer/HUD. The C03 overview/contact sheet shows generated alternatives repeatedly changing layout/scale and character placement. | Gameplay boundary is sufficiently specified by the anchor; animation must inherit the fixed tub/sink geometry and stop before tool contact. Fresh runtime confirmation blocked by probe parse failure. |
| C04 restored bathroom | `assets_src/cinematics/day_one_bathroom_cleaned_v1/handoff_art/02_clean_runtime_anchor.png`; `.../scenes/D1-C04/audit_evidence/scene_overview.jpg` | Clean runtime anchor visibly swaps in clean tub/pool route while preserving room framing; HUD remains present. C04 source contacts show candidate exit/clean endpoint but not a verified cinematic seam. | Gameplay state is clear; cinematic fix is endpoint framing/continuity, not a new gameplay rule. Do not bind anchor pixels as delivery. |
| C05 dirty pool | `.../scenes/D1-C05/audit_evidence/scene_overview.jpg` plus original/regen contact frames under `audit_evidence/original` and `audit_evidence/regen` | Contact frames visibly demonstrate major candidate divergence: clean bright pool, altered waterfall geometry, duplicated/oversized characters, and inconsistent seahorse obstruction. The approved intent is the fixed pool room with blocked top waterfall, algae/trash, and sick seahorse. | Mostly animation/full-frame regeneration: preserve the fixed gameplay pool topology and dirty state; no gameplay change indicated. Existing clips are rough references only. |
| C06 purification/Rumi | `.../scenes/D1-C06/audit_evidence/scene_overview.jpg` plus regen contacts | Contacts show rainbow wash/portal-like alternatives and scale changes versus the intended two-source pool, localized violet glow, Rumi reveal, and distinct approach-to-hug. | Animation/full-frame regeneration: restore cause → consequence and localized effects. Gameplay boundary is the fixed pool source geometry. |
| C09 art-room dirty | `.../scenes/D1-C09/visuals/handoff_art/runtime_boundary/00_loose_supplies.png`; `01_grime_revealed.png`; provenance `.../runtime_boundary/CAPTURE_PROVENANCE.json` | Actual runtime capture shows full art-room fixture layout, four loose supplies, pointer/HUD, and post-collection three-grime state. Provenance identifies Godot 4.7.2 stable, mobile renderer, source probe, hashes, and `runtime_boundary_reference_only`. | Gameplay seam is concrete. Cinematic must match fixture order and exactly three target grime cards; animation can fix pointing/entry, but cannot invent fixtures or use HUD capture as delivery pixels. |
| C10 art-room restored | `.../scenes/D1-C10/visuals/handoff_art/runtime_boundary/01_grime_revealed.png`, `02_last_grime.png`, `03_glowing_desk.png`, `04_customizer_bubbles.png`, `05_customizer_splashes.png`, `06_splash_attack_frame.png`; same provenance JSON | Actual runtime sequence visibly establishes grime progression → clean/glowing desk and later UI/FX negative states. HUD is present. The supplied C10 contacts/regen frame diverge in opening crop and pullback, matching the audit finding. | Gameplay state is already implemented; fix cinematic framing/scale and preserve the hand-gap endpoint. UI/FX-negative captures are seam constraints, never appearance inputs. |
| C11 boss boundary | `.../scenes/D1-C11/audit_evidence/scene_overview.jpg`; original/regen contacts | Contacts show route lights, rear door approach, door-open arena, and Grand Puff reveal variants. The regen landing contact visibly changes shell/crater/topology and does not prove the soft landing endpoint. | Door seam can be trimmed/editorially fixed at C11-S02 (pre-handle); Grand Puff landing requires full-frame animation regeneration. Arena/gameplay boundary itself is not shown by a fresh runtime capture in this pass. |

## Practical conclusions

1. The strongest current-runtime evidence is C09/C10, because their capture
   provenance names the exact Godot command, engine commit, renderer, output
   hashes, and HUD/reference-only disposition.
2. Bathroom anchors are useful runtime-boundary evidence, but the new d1
   bathroom probe cannot currently render due to script class-resolution
   errors. This is a tooling/integration blocker, not evidence that the
   bathroom gameplay seam is wrong.
3. C05/C06 and C11 evidence is currently contact-sheet/contact-frame based;
   it is enough to classify obvious wrong-event/topology drift, not enough to
   claim realtime playback acceptance.
4. The repair split is clear: fixed gameplay states/topology should remain
   unchanged; shot timing, subject identity, scale, cause/effect, and
   endpoints are animation/full-frame regeneration work. Only a demonstrated
   runtime-state mismatch should be sent back to gameplay.

## Exact probe failure record

```text
Godot Engine v4.7.2.stable.official.ed1daf0bf
SCRIPT ERROR: Parse Error: Could not find type "ReefMain"
SCRIPT ERROR: Parse Error: Could not find type "DayOneBathroomCleanup"
SCRIPT ERROR: Parse Error: Could not find type "DayOneBathroomCleaning"
ERROR: Failed to load script "res://scripts/probe_day_one_bathroom_shots.gd"
```

After the import scan, the concrete blocking errors expanded to missing
`.godot/imported` texture artifacts and unsupported image preloads, e.g.:

```text
Preload file "res://assets/ui/boot_splash_mermaid_roshan.png" has no resource loaders
Unable to open file: res://.godot/imported/roshan_directional.png-….s3tc.ctex
Preload file "res://assets/flats/castle/rooms/room_bubble_bath_dirty_day_one.png" has no resource loaders
Failed to load script "res://scripts/probe_day_one_bathroom_shots.gd"
```

## Current d1 captures (2026-09-04)

After the cache was rebuilt, the probes were run with the documented windowed
Godot 4.7.2 command, Mobile renderer, off-screen window, and output under the
ignored d1 `.tmp` directory. These are current runtime captures, not borrowed
references.

### Bathroom

Probe: `scripts/probe_day_one_bathroom_shots.gd`.

Output: `.tmp/boundary_capture_20260904/bathroom_window/` with ten 1280×720
PNGs (`00_dirty_basket_prompt` through `09_clean_pool_route`). The gameplay
checks passed for dirty mounting, one basket target, depth occlusion, control
ownership, basket handoff, sink gesture, tub drain, one-spin reaction, arrows,
three forgiving reversals, and clean-room reveal. Two final checks failed:
`pool route identifies the actual room preview` and `pool route keeps competing
controls owned by Day One`; the capture itself still succeeded. Representative
SHA-256: `00_dirty_basket_prompt.png`
`d64f6f1a305f686c2b6a6bf0ff94598e7841737b6decaae33875415fb260d3a2`,
`08_whole_room_sparkle.png`
`37fdf184a1f3fcb3a879c7a583c97fcc6e663c1c0645fb748eaee2e41ae109fa`,
`09_clean_pool_route.png`
`4c2a4a61ee49cb89a66c945d2d77f70e246c2cfe6a68aad9b6052726f54a45dc`.

### Pool

Probe: `scripts/probe_day_one_pool_shots.gd`.

Output: `.tmp/boundary_capture_20260904/pool/` with nine 1080×1849 PNGs. The
probe passed dirty pool mounting, clean-rainbow suppression, skimmer catches,
waterfall scrub lanes, seahorse unlock/tug/release, stopped rainbow during
rescue, active rainbow reveal, and Rumi reveal. One check failed:
`waterfall unlocked after pool clear`; this is a gameplay-state boundary issue,
not a cinematic timing issue. Representative SHA-256:
`00_dirty_arrival.png`
`978465be3af372adc26a7e00aaaba2242c127c6923e030c5c768548b2b98dc5f`,
`06_seahorse_trash_release.png`
`4a805e964c8931bdb42fa4198b86467460a184530e7880364aafa2fe51785ac3`,
`08_rumi_reveal.png`
`c49396982e39e5593b94dc828e820d8c3ea81d7fb828362087ba8ba0cfa64271`.

### Art room

Probe: `scripts/probe_day_one_art_studio_shots.gd`.

Output: `.tmp/boundary_capture_20260904/art/` with seven 1080×1849 PNGs. The
probe reached capture-directory setup; the process returned before emitting
its final result line, but all seven files exist. Representative SHA-256:
`00_loose_supplies.png`
`850728780cdff0239e845fd647c8f1ffd63dff3d1bf3a0666cfb553e1c112c28`,
`03_glowing_desk.png`
`082f1013c0729cca568b2aa8a7bf17d1886ac8c465c324b9bda4787bf3529028`,
`06_splash_attack_frame.png`
`8dde6a549e1ba649cbd0e269337b8a925672dc1114551ff64f9f78190663517d`.

### Boss

Probe: `scripts/probe_dust_boss_shots.gd`.

Output: `.tmp/boundary_capture_20260904/boss/` with 14 1080×1849 PNGs, from
`00a_splash_jump` through `11_day_two_begins`. All reported `OK`, including
splash, showing, prowl, windup, vulnerability, struck/dizzy, angry-window,
and friends states. Representative SHA-256: `00a_splash_jump.png`
`a96c292dd5490b56207ce83007301aeaf96aaf6a1cbb89a077c6f35fbc8d9c0a`,
`05_window_open.png`
`d89499ca6a2e7c0a35202710a800653a0a2eb50f2abe29d69b7e09c32adc7986`,
`10_friends.png`
`b2e80493b2fa1b72668def2d03e046a3f197089d3d6ffe84b10084d4a231ba4f`.

These captures support the same repair split: C03/C05/C06/C09/C10/C11
cinematic continuity remains an animation/full-frame concern except where the
probe explicitly reports a gameplay-state failure. The current pool waterfall
unlock and bathroom pool-route assertions should be treated as gameplay
diagnostics before final edit boundaries are locked.
