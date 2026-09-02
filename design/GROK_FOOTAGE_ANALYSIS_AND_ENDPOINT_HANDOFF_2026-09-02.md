# Grok footage analysis and endpoint handoff — Day One

**Date:** 2026-09-02  
**Scope:** D1-C00 through D1-C12 (13 movies, 70 shot jobs)  
**Status:** bridge specification; no footage or endpoint is accepted by this document

This document closes the continuity gap between a generated Grok clip and the
next Grok shot. A prior clip is sent to Grok for motion/editorial analysis:
timing, action cause, camera behavior, screen side, scale, contact, geography,
and the final settled state. The clip is never silently promoted to appearance
authority.

The machine-readable record is
`design/templates/GROK_CONTINUITY_ANALYSIS_V1.json`.

## Current repository finding

The 13 current visual packets under
`assets_src/cinematics/d1_c00_opening_flight_visual_v1/` through
`assets_src/cinematics/d1_c12_restored_castle_finale_visual_v1/` contain no
video files, no `shots/` directories, and no shot-level `FIRST_FRAME.png`
files. The repository-wide search found no `.mp4`, `.mov`, `.webm`, `.mkv`, or
`.ogv` Day One footage. The available media is still art, perspective sheets,
storyboards, gameplay-boundary captures, and generation/review records.

The older bathroom packets may contain PNG runtime-boundary captures. Those are
seam and topology evidence only. They are not a video source, appearance plate,
or `IMAGE_1` unless a new complete flattened frame is separately authored and
human-approved.

All 13 current `IMAGINE_HANDOFF.json` contracts report:

```text
archive_status: incomplete
generation_status: blocked
delivery_status: not_accepted
shot_packets: []
```

The current generated perspective and storyboard sheets have narrative value,
but their manifests explicitly set `appearance_authority: false`,
`bound_reference_eligible: false`, and `used_as_delivery_pixels: false`.

## Authority and promotion rules

The following terms are used in the mapping below:

- `E(Cxx-Syy)` means the last stable full frame extracted from that accepted
  clip. It is only a candidate until human review passes.
- `M` means a new complete, flattened, UI-free, human-approved first-frame
  master for the target shot.
- `G` means the gameplay endpoint that supplies the causal start state. A HUD
  or gameplay capture remains non-pixel evidence; it must be recreated or
  approved as a complete cinematic frame before it can bind as `IMAGE_1`.
- `PG` means a separate accepted post-gameplay clip/endpoint. A reveal clip
  that merely ends ready for gameplay is not a post-gameplay friendship state.

For every generated clip:

1. Inspect the native clip and its lossless frame extraction. Record the clip
   hash, native dimensions, frame rate, duration, and exact timecodes.
2. Record action onset, physical trigger/contact, first visible consequence,
   reaction, and last stable frame. Measure subject boxes and fixed landmarks
   in normalized 0–1 canvas coordinates.
3. Extract the proposed terminal frame without cropping, compositing, masking,
   interpolating, or repairing it. Hash the exact extracted file.
4. Human-review identity, anatomy, cast/object count, topology, contact, state,
   lighting, UI absence, and endpoint stability. Retain rejected candidates.
5. Only an accepted complete endpoint may be promoted to the target
   `shots/<shot_id>/FIRST_FRAME.png` with
   `source_kind: "accepted_previous_end"` and the same SHA-256 in the
   continuity contract.
6. If the next shot changes setup or camera address, use a new `M`; the prior
   clip is still analyzed for editorial and geography continuity but does not
   become its pixels.
7. Generate one shot, then repeat this bridge before the next dependent shot.

No storyboard, perspective sheet, contact sheet, HUD capture, or gameplay
capture may be bound as an appearance image. They belong in
`non_pixel_references` with `appearance_authority: false` and
`used_as_delivery_pixels: false`.

## Required measurements

Each `GROK_CONTINUITY_ANALYSIS_V1.json` record should contain:

- exact native `first_frame`, `action_onset`, `contact_or_trigger`,
  `visible_consequence`, `reaction_or_settle`, and `last_stable_frame`
  timecodes in milliseconds and frame indices;
- normalized bounding boxes for every visible subject at first frame, action
  onset, contact, and endpoint;
- normalized anchor points for doors, seams, coping, tub rims, fixtures,
  basket zones, desks, route lights, arena walls, and other scene landmarks;
- declared versus observed camera verb, move count, translation, and scale
  ratio;
- screen side, facing, relative scale, cast count, object count, and contact
  graph;
- fixed topology invariants and grade/lighting observations;
- knockout, continuity, causality, style/readability, and technical findings;
- endpoint candidate path/hash, human decision, and whether it is eligible for
  `IMAGE_1`.

The first repository pass will correctly record `null` timecodes until actual
native footage is supplied. Missing footage is a blocked input, not permission
to infer timing from a storyboard.

## Day One dependency map

The table identifies the footage that must be analyzed before each scene and
the exact endpoint/master policy for its shots. “Analyze” does not mean “bind
the clip.” Within a scene, the immediate prior accepted clip is analyzed before
every dependent shot, even when the next shot needs a new master because its
camera setup changes.

| Scene | Analyze before scene/shot work | `IMAGE_1` promotion map | Full-frame authority still missing |
|---|---|---|---|
| **D1-C00** Opening Flight | No predecessor at scene entry. Then analyze each accepted prior C00 shot before any true continuation. | Authored opening: `M(S01–S06)`. Camera changes make these separate setup masters unless a later card explicitly declares a matching accepted endpoint. | Six complete cabin/exterior opening masters; no accepted opening clip exists. |
| **D1-C01** Lagoon Landing and Castle Approach | Analyze `C00-S06` for descent, plane scale, lagoon direction, and editorial handoff. | New dock/approach setups: `M(S01–S04)`. S04 must settle the exact closed-door geometry. | Four complete dock/route/door masters. |
| **D1-C02** First Dirty Castle Discovery | Analyze `C01-S04` for door seam, hinge side, handle, screen side, and Daddy/Roshan placement. | `S01 = E(C01-S04)` after acceptance. `S02–S04 = M` for reverse interior, evidence close-up, and route map. | Human-approved dirty Main Hall perspective packet plus four shot-level masters. Current generated sheets are narrative-only. |
| **D1-C03** Bubble Bathroom — Dirty Entry | Analyze `C02-S04` for route attention only. | `S01 = M` dirty empty bathroom. `S02` may use `E(C03-S01)` only if the layout/camera truly matches; `S03–S04 = M` close/medium setups. | V2 dirty reboard/packet and four complete shot masters. |
| **D1-C04** Bubble Bathroom — Restored | Analyze `C03-S04` for discovery context; use the actual gameplay final brush contact as the causal source. | `S01 = G` converted to a human-approved complete cinematic contact master. `S02–S04 = M`. | Approved gameplay-to-cinematic contact frame, V2 packet, and three further masters. |
| **D1-C05** Sparkle Pool — Dirty Discovery | Analyze `C04-S04` for clean-room route/attention only. | New dirty Pool setup masters `M(S01–S06)`. | Six dirty Pool discovery masters; historical boards do not qualify. |
| **D1-C06** Sparkle Pool — Purification, Rumi and Hug | Analyze `C05-S06` for the giant-pool map and dirty state. | `S01 = M` catalyst close-up; `S02 = E(C06-S01)`; `S03 = M` waterfall top source; `S04 = E(C06-S03)` only if the close opening matches; `S05–S09 = M`. | Nine shot cards/masters and the V2 Pool packet; no accepted C05 endpoint exists. |
| **D1-C07** Stuffie Room — Dirty Discovery | Analyze `C06-S09` for sequence context only; this is an authored room cut. | New dirty Stuffie setup masters `M(S01–S06)`. | Six complete dirty-room shot masters; final packet validation/publication remains required. |
| **D1-C08** Stuffie Room — Restoration | Analyze `C07-S06`; gameplay supplies the actual recovered-Baby-Eagle dirty endpoint. | `S01 = G` converted to an approved full-frame seam master; `S02–S07 = M`, including clean endpoint S07. | Approved gameplay seam and six further masters; final packet validation/publication. |
| **D1-C09** Art Room — Spilled Supplies Discovery | Analyze `C08-S07` for clean-room sequence context only. | New dirty Art Room setup masters `M(S01–S05)`. | Human-approved six-view clean/dirty topology packet plus five masters. Incidental floor marks in the current board are not targets. |
| **D1-C10** Art Room — Clean Desk Awakening | Analyze `C09-S05`; gameplay supplies the final brush-contact start. | `S01 = G` converted to an approved full-frame contact master; `S02–S05 = M`. | Gameplay seam, owner-approved six-view topology, and four further masters. |
| **D1-C11** Boss Door and Grand Puff Reveal | Analyze `C10-S05` for restored-route context. | `S01 = M` four-route Main Hall; `S02 = M` rear door; `S03 = E(C11-S02)` if the door endpoint matches; `S04 = M` arena reveal. | Owner-approved circular shell-arena topology card and four shot masters. The current arena sheet is narrative-only. |
| **D1-C12** Restored-Castle Finale | Analyze accepted terminal clips `C04-S04`, `C06-S09`, `C08-S07`, `C10-S05`, plus a separate accepted `PG` Grand Puff friendship clip. | `S01 = E(C04-S04)`, `S02 = E(C06-S09)`, `S03 = E(C08-S07)`, `S04 = E(C10-S05)`, `S05 = E(PG)`, `S06 = M` clean Main Hall reunion. | All four inherited endpoint stills, the post-gameplay Grand Puff endpoint, six shot cards, and runtime seam packet. |

### Important dependency distinctions

- C00-S06 to C01-S01 is a scene handoff with a changed camera/location, so
  C00-S06 is analyzed for route and descent but does not automatically supply
  C01-S01 pixels.
- C01-S04 to C02-S01 is explicitly an inherited door endpoint. It may supply
  `IMAGE_1` only after the C01 clip and terminal frame pass review.
- C04, C08, and C10 begin from player-authored gameplay states. Their HUD or
  runtime captures document the seam; they do not become cinematic image
  inputs by virtue of being exact gameplay captures.
- C11-S04 ends ready for gameplay. C12-S05 requires the later befriended,
  playful Grand Puff state, so it cannot inherit C11-S04 as though the reveal
  were already a friendship payoff.
- C12 is a straight-cut montage. Each room vignette inherits the accepted
  endpoint from its own room film; the montage storyboard does not replace
  those endpoint stills and does not authorize a multi-location generation.

## Endpoint review and promotion record

The endpoint decision is fail-closed:

```text
native clip
  -> measured analysis record
  -> lossless endpoint candidate + hash
  -> human identity/topology/style/UI review
       rejected -> retain candidate, targeted regeneration
       accepted -> promote exact still as IMAGE_1
```

An accepted endpoint must prove the required cast, anatomy, room topology,
screen-side/scale, contact state, lighting, and stable next-shot setup. An
attractive frame that fails any knockout remains rejected. The extracted still
is not delivery evidence merely because it is accepted for the next Grok
input; delivery remains subject to the independent full-frame cinematic audit.

The target shot card must then repeat the endpoint hash in both:

```json
{
  "bound_references": [{
    "id": "IMAGE_1",
    "source_kind": "accepted_previous_end",
    "path": "shots/D1-Cxx-Sxx/FIRST_FRAME.png",
    "sha256": "<same endpoint hash>",
    "hud_present": false,
    "human_decision": "accepted"
  }],
  "continuity": {
    "kind": "continuous_action",
    "previous_shot_id": "D1-Cxx-Syy",
    "previous_end_sha256": "<same endpoint hash>"
  }
}
```

For an authored setup, set `source_kind: "approved_master"` and keep the
prior clip in the analysis record, not in the pixel-binding list. For gameplay
or storyboard evidence, add it to `non_pixel_references` only.

## Completion claims

This bridge does not award any of the three production claims:

- `ARCHIVE_COMPLETE` requires the complete packet, provenance, hashes, and
  remote verification.
- `GENERATION_READY` requires every shot card to have an opened, human-
  accepted two-to-four-image binding, including a valid `IMAGE_1`.
- `DELIVERY_ACCEPTED` requires independent full-frame identity, topology,
  continuity, method, device, child, and owner review.

Grok footage analysis improves consistency by making continuity measurable and
by promoting only reviewed terminal states into the next shot. It must not be
used to smuggle unreviewed appearance pixels or to let a storyboard/capture
stand in for a missing full-frame master.
