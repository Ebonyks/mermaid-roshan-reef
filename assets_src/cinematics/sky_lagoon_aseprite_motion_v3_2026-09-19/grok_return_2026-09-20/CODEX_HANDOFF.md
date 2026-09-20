# Codex handoff — Sky Lagoon Aseprite motion

**Date:** 2026-09-20  
**From:** Grok Build (`MODULE-SKY-ENV-MOTION` import + I2V capture)  
**To:** Codex (Aseprite authorship, Godot playback, Krita plant lane)  
**Source packet:** `assets_src/cinematics/sky_lagoon_aseprite_motion_v3_2026-09-19` @ `b19de3a0df30c0951fae0c1d87f8fc42a9560f44`  
**Parent:** `LOC-SKY` — do not replace. Gameplay candidates only.

`GENERATION_READY=false`  
`DELIVERY_ACCEPTED=false`  
`ARCHIVE_COMPLETE=false`  
All five MP4s are **reference-only**. Do not auto-promote video to a runtime atlas.

---

## 1. What Grok did

Owner continued after the import report. Grok captured five independent environment-motion references on `imagine_image_to_video`.

| Fact | Value |
|---|---|
| Requested duration | 1s native-aspect phrase |
| Actual surface minimum | **6.04s** · 24fps · 720p-class |
| Hold policy | Action in ~first second; 1–6s holds rest. Do not slow the action to fill. |
| IMAGE_1 binding | still **null** in the module; proposed crops were used as I2V stills |
| Actor | none |
| Shader bridge trial | remains **rejected** |

Native files live with the Grok review desk under `output/G0x/native.mp4` plus first / max / settled / last stills and an action contact sheet (0–1.2s @ 10fps).

---

## 2. Job order (do not reshuffle)

1. **G01 castle bridge deck** — author now.
2. **G02 near-side chain** — same `.aseprite` file, only after G01 timing is useful.
3. **K01 huckleberry** — independent Krita lane. Do not wait on Grok.
4. **G03 / G04 / G05 water** — hold until G01 Aseprite is accepted in the castle/arrival scene.
5. Meadow has **no** water work.

---

## 3. G01 — Codex Aseprite job (required)

**Intent:** one local load, a small mid-span board flex, release, settle. Supports and both landings pinned. No whole-bridge bounce, no rubber deck, no bending posts.

**Grok capture defects you must correct by drawing:**

- Flex is **below readable amplitude**. Author a clearer local mid-span deflection, still very small.
- Rest is **not pixel-identical** (first→last mae 3.23). Rest frame must composite into the accepted v16 castle scene.
- Output is a 1296×704 upscale of a 372×202 crop. Draw on the crop / scene pixels, not the video pixels.
- 6s hold is interface fill. Authored timing target remains **0.8–1.2s** (8–12 frames), adjusted after you watch the reference.

**File:** one RGBA `.aseprite`

**Layers (named, required):**

- `reference_locked` (Grok frames / stills, hidden on export)
- `rear_chain`
- `supports_fixed`
- `deck_boards`
- `front_chain`
- `front_posts`
- `contact_shadow`

Paint complete overlap under moving boards. Paint a clean world plate behind the bridge; never leave a painted duplicate under exported moving parts.

**Landmarks to pin across all frames:** board seams, four landing corners, post caps, chain sockets. Supports/landings at identical coordinates.

**Tags:** `rest`; add `step_near` / `step_mid` / `step_far` only after each variant exists. One-shot: contact → compression → release → diminishing settle → exact rest. No autonomous looping of footsteps.

**Godot:** `AnimatedSprite2D` / `SpriteFrames` or `AnimationPlayer`. Select contact variant from Roshan’s real footfall later; fire at most once per contact. Pause freezes clocks. Scene exit cancels transients. Return starts at rest. Ambient motion never writes save data.

**Export:** PNG atlas + JSON (names, rects, durations, tags). Stable canvas/origin. Trim off initially. Export only delivery layers, never `reference_locked`. Keep the `.aseprite` and a reproducible CLI command beside outputs.

**Reject if:** invented links, changing post count, melting wood, camera drift, or foot contact that cannot be reproduced.

---

## 4. G02 — same file, later

One existing near-side gold chain span, tiny delayed swing, settle to original hanging curve.

- Preserve **link count** and **both attachment sockets**.
- 6–10 authored states.
- Offset **approximately 60–120ms** after G01 contact — test, do not canonize.
- Do **not** commission a separate chain clip until G01 timing is useful.
- Grok swing is at or below authorship threshold; draw the secondary action, do not rotoscope the MP4.

Independent endpoint. Timing-review dependency on G01 only.

---

## 5. G03–G05 — hold

Captured as water studies. **Do not author yet.**

| Shot | Useful note | Defect to remember later |
|---|---|---|
| G03 painted highlights | Bands do travel | Rest did not return; possible gloss; not a loop; not a 256×128 tile |
| G04 shoreline lap | No ocean surf; stones hold | Lap too faint; needs rock occlusion mask |
| G05 touch ripple | Thin expanding disturbance | Did not fade; may couple to G03; clip behind bridge/rocks |

When unblocked: author alpha sequences, not full-scene video atlases. Castle water first for G03/G05; arrival pool first for G04.

---

## 6. K01 — independent (Codex built-in image gen + Krita)

No Grok plant commission unless a specific motion problem survives local drawing review.

- Start with **one three-branch huckleberry**.
- Preserve berry count, root and leaf attachment.
- Draw rest, soft bend, strongest bend, return. Animate one branch group at a time.
- Use Codex **built-in** image generation, no API keys, no invented model pin. Record the actual tool.
- One candidate pose per call. Inspect and reject drift before spending further frames.
- Bellflower native has green edge spill — K02 must clean the matte before motion.
- Current v16 ORAs have only four broad foreground-review layers. Do not call them animation-ready.

---

## 7. Performance / engine

- Godot **4.7.2**, mobile renderer, **30fps** on Lenovo Tab M11.
- Source art is 1254² review art, below 2048 production coverage.
- Small local crops. Power-of-two atlas pages or ≤1024 longest edge.
- Example: 384×256 × 10 frames ≈ 3.75MiB RGBA before padding/mips. Measure the packed result.
- Water, bridge, plants independently switchable.
- Static original is a reversible fallback.

---

## 8. Explicit non-goals

- Do not replace `LOC-SKY` or narrative events.
- Do not put an actor on these material jobs.
- Do not treat Grok MP4 / contact sheets as delivery pixels.
- Do not weaken the inherited 2–8s/16:9 validator; scoped 1s native-aspect cards remain draft.
- Do not award progress or write saves from ambient motion.
- Door opening is later functional work, not garnish.

---

## 9. Return to owner

For each authored shot: `.aseprite` path, layer inventory, frame tags, PNG atlas + JSON, first/last authored frames, contact sheet of authored cels, gameplay-contact note, and a decision (`accepted_runtime` / `rejected` / `needs_revision`). Do not send only a movie.
