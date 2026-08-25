# Luna candidate audit — Day One Mermaid Pool Video 01

**Review date:** 2026-08-25
**Reviewer:** Luna (independent candidate audit; owner/runtime review is final)
**Film/shot:** `day_one_pool_video_01` / `[shot_id]` / `[timeline_index]`
**Candidate:** `[candidate_path]`
**Status:** `UNREVIEWED` / `REJECT_KNOCKOUT` / `REJECT_SCORE` / `REGEN_REQUIRED` / `AUDIT_PASS_OWNER_PENDING` / `OWNER_ACCEPTED`

This is a review template for fresh Grok full-frame candidates. It is bound by
`AGENTS.md`, `audit/DAY_ONE_DIRTY_POOL_STYLE_AUDIT_2026-08-22.md`,
`audit/DAY_ONE_POOL_NATURAL_INTEGRATION_SPEC_2026-08-23.md`,
`design/HANDOFF_GROK_DAY_ONE_POOL_NEXT_ANIMATION_2026-08-23.md`, and
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (`DL-VIS-01`–`08`,
`DL-READ-01`–`06`, `DL-MOT-01`–`07`, and `DL-CIN-01`–`12`). Grok cannot
approve its own output. Luna scores each candidate
independently; only the owner can grant 5/5 in runtime context.

## Hard decision rule

- A candidate is eligible for `AUDIT_PASS_OWNER_PENDING` only when it has **no
  knockout**, all mandatory evidence is present, and its score is **at least
  4.5/5.0**.
- Never accept a candidate below 4.5. Do not average away a knockout or missing
  provenance with strengths elsewhere.
- Luna's automated/documentary audit score is capped at **4.9/5.0**. A 5.0 is
  impossible in this record until the owner accepts the exact frame in runtime
  context (`DL-VIS-07`); device, child, voice, and owner evidence do not
  transfer from another shot or another build.
- Each shot may receive up to **20 fresh full-frame regeneration attempts**.
  `attempt` is 1–20 and never resets when the prompt changes. If attempt 20
  still fails, mark `REGEN_REQUIRED`/`OWNER_ESCALATION`; never lower the gate,
  reuse a failed frame, or fill a missing action with interpolation or a hold.
- An intentional hold is eligible only when the direction brief explicitly
  calls for stillness and its held span and narrative purpose are recorded.

## Canonical evidence and continuity anchors

Upload/use these as appearance and continuity references, never as delivery
pixels or identity substitutes:

- `assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png`
- `assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_waterfall_rest.png`
- `assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_seahorse_fountain_rest.png`
- `assets/castle/day_one_pool/activities/waterfall_clogged_original_match.png`
- `assets/castle/day_one_pool/activities/pool_skimmer.png`
- `assets/castle/day_one_pool/activities/floating_trash_atlas.png`
- `assets/castle/day_one_pool/activities/seahorse_sick_clear_mouth.png`
- `assets/castle/day_one_pool/activities/seahorse_mouth_trash.png`
- `assets/characters/rumi/rumi_pool_idle_swim_atlas.png`
- `assets/characters/rumi/rumi_eight_pose_runtime.png`
- `assets/characters/roshan_25d/roshan_base.png` and the approved Roshan atlas
  family under `assets/characters/roshan_25d/`
- `assets_src/imagegen/day_one_pool_natural_integration_2026-08-23/room_activity_integration_reference_native.png`
  (layout/material/contact guidance only)

The room remains the same cream pearl coping, lavender shell arches, broad aqua
pool, pearl rainbow fixture at left-center, and long-snouted seahorse fountain
at right-center. The measured 1280x720-stage centers are approximately
waterfall `(461.875, 216.25)` and seahorse `(921.875, 245.625)`; compare in
normalized coordinates when candidate dimensions differ. Roshan remains brown
haired with rainbow forelock/streak, pink top, and rainbow mermaid tail. Rumi
is Violet: enormous violet braid, pointed ears, navy/gold-trimmed sea-jacket
with shell clasp, aqua-to-lavender tail, and coral-pink fins. No other mermaid
belongs in this film.

## Knockout failures — immediate reject

Check every applicable item. A checked knockout makes the candidate
`REJECT_KNOCKOUT`, regardless of numeric score.

- [ ] Wrong Roshan identity, face, hair/forelock, costume, body proportions, or
  tail; identity is not recognizable at phone size.
- [ ] **Pre-finale** waterfall is clean, flowing, sparkling, rainbow-lit,
  glowing, foamy, cyan-streaming, or otherwise healthy before the rescue.
  (A clean rainbow surge is allowed only for the explicit final reward beat.)
- [ ] A canonical fixture is generic, moved, mirrored, enlarged, replaced,
  independently redrawn, or redesigned; the V4 waterfall/seahorse silhouette,
  pivot, and registration are not preserved.
- [ ] The required soggy pink wrapper/seaweed plug is absent from the
  seahorse mouth/nozzle during dirty, effort, or release beats, or the release
  hides the mouth/contact event.
- [ ] Rumi is absent when the beat requires her, has the wrong Violet identity,
  or any extra/substitute mermaid appears.
- [ ] Theater-flat, clip-art, sticker, card, overlay, floating-panel, or
  isolated product-render treatment replaces natural room integration.
- [ ] Photorealism, 3D render/model, PBR look, spatial/mesh character, or any
  medium other than the approved polished 2D storybook generation.
- [ ] The delivery is not one complete flattened full-frame generation (for
  example layers, cutouts, sprite/chroma composite, translated plate, tween,
  morph, optical-flow/interpolated frame, cross-dissolve, procedural warp,
  rig/skeleton, or duplicated action frame).
- [ ] The active subject, action contact, Roshan, mouth obstruction, or required
  prop is illegible in a 3–4-year-old phone-size/squint view with the HUD
  presentation assumed.

Other hard failures: missing candidate hash, missing prompt hash, missing
timeline index, wrong delivery orientation/aspect, forbidden generation method,
guide pixels in delivery, unreviewed identity/topology/style, position drift
without a directed beat, or failed neighboring-frame continuity. Record these
as `REJECT_KNOCKOUT`/`REGEN_REQUIRED` even if the image looks attractive.

## Five-point candidate rubric

Score each dimension in 0.25 increments. The maximum is 5.0 before the
automatic documentary cap; no partial credit can excuse a knockout.

| Dimension | Max | What earns full credit |
|---|---:|---|
| 1. Identity and canonical continuity | 1.25 | Roshan's approved identity is stable; room architecture, pearl coping, shell arches, pool, V4 waterfall and seahorse are exact in silhouette/registration; Rumi is absent until the rise and then unmistakably Violet. No extra mermaid or fixture drift. (`DL-VIS-06`, `DL-MOT-01`) |
| 2. Beat, action, and spatial truth | 1.25 | The declared beat is unmistakable at one active focal action: trash/net contact and wake; scrubber-to-lane contact with remaining sludge; plug visibly stretching from the nozzle; unobscured release into basket; final surge/reaction; or Rumi rise/wave/settle. Anticipation → action → contact/payoff → settle reads without invented shortcuts. (`DL-INT-02`, `DL-INT-03`, `DL-MOT-03`) |
| 3. Natural integration and style congruence | 1.00 | Flat polished 2D storybook language: broad rounded shapes, 2–4 px deep indigo/plum contours, broad painted value bands, aqua/lavender shadows, restrained highlights. Tools/debris are room-scale and locally tinted; contact shadows, waterlines/wakes, occlusion, and perspective make them physically belong. No global teal wash, ring field, white halo, black outline, chrome/PBR, or oversized prop. (`DL-VIS-01`–`05`, natural-integration spec) |
| 4. Child-readable composition | 0.75 | One primary action, quiet support, clear figure/ground, readable face/hands/prop at phone-size squint, Roshan visible, and any pointer points to the live object. No text/UI dependence, competing bright objectives, or thumb-blocked required contact. (`DL-READ-01`–`06`) |
| 5. Cinematic craft and evidence compliance | 0.75 | Complete native-orientation frame with stable camera and neighboring spatial continuity; the image is individually freshly generated with no forbidden temporal method; hashes, dimensions/aspect, prompt/attempt, method, geometry, neighbor refs, and human identity/topology/style review are complete. (`DL-CIN-01`–`12`) |
| **Total** | **5.00** | **Accept for owner/runtime review only at ≥4.50, no knockout. Documentary cap: 4.90.** |

### Score notes

| Dimension | Score | Evidence / defect / repair direction |
|---|---:|---|
| Identity and canonical continuity (1.25) | `[ ]` | `[ ]` |
| Beat, action, and spatial truth (1.25) | `[ ]` | `[ ]` |
| Natural integration and style (1.00) | `[ ]` | `[ ]` |
| Child-readable composition (0.75) | `[ ]` | `[ ]` |
| Cinematic craft/evidence (0.75) | `[ ]` | `[ ]` |
| **Raw total** | `[ ] / 5.00` | `[ ]` |
| **Applied cap** | `max 4.90` | `5.0 reserved for owner runtime acceptance` |

## Beat-specific checklist

Select exactly one declared beat for the candidate. If the frame tries to show
two active beats, score `0` for hierarchy/action and likely reject.

- [ ] **Dirty establishing:** dingy low-energy pool, six readable harmless
  trash pieces, still opaque olive-brown waterfall with embedded leaf/wrapper
  debris and blocked basin, sick seahorse with mouth plug, Rumi absent.
- [ ] **Skimmer:** pearl/aqua net visibly meets one trash item, resistance and
  small wake are readable, nearby shell basket receives litter; other task
  areas stay quiet.
- [ ] **Waterfall scrub:** scrubber contacts one of three vertical sludge lanes,
  broad clean stripe appears beneath it, other lanes remain opaque/stagnant,
  exact fixture architecture remains registered; no rainbow surge yet.
- [ ] **Seahorse effort:** Roshan grips/pulls the plug, plug stretches outward
  across distinct effort frames, seahorse reacts safely/sympathetically, no
  injury or distress.
- [ ] **Release/contact:** plug is visibly free and traveling toward basket,
  mouth is clear, seahorse begins to perk up; hand/sparkle/crop/motion blur do
  not hide contact.
- [ ] **Reward:** only now does the room relight; rainbow waterfall surges from
  top to basin, healthy seahorse water resumes, Roshan reacts with delight.
- [ ] **Rumi rise:** Violet/Rumi rises with approved swim silhouette, thanks or
  introduces herself, waves, then settles into calm idle; no substitute actor.

## Natural-integration and phone pass

- [ ] Activity art is in the room's world/depth hierarchy, not a modal redraw.
- [ ] One active action is emphasized; future tools/targets are quiet or hidden.
- [ ] Skimmer ≤245 px wide / 165 px high at 1280x720; debris approximately
  72–92 px; basket approximately 130–145 px, unless the directed shot calls for
  a measured exception recorded below.
- [ ] Each floating object has a restrained local ripple/contact ellipse only
  8–16 px beyond its silhouette; no shared halo or target-ring field.
- [ ] Skimmer net touches water; basket rests on the front-right promenade;
  mouth plug begins behind the nozzle edge with a tiny local seam shadow.
- [ ] Props use two or three broad value bands, local aqua/lavender shadows,
  15–25% restrained saturation/highlight density, and no white sticker rim.
- [ ] The center water remains open; Roshan's face/body and the required action
  are not covered by foreground, cards, particles, or thumb-risk placement.
- [ ] 16:9 landscape, square pixels, zero rotation metadata; review at phone
  size and with the intended HUD presentation, not desktop-only zoom.

## Candidate audit record (one record per attempt/frame)

Copy this block for every candidate, including rejected attempts. Do not delete
failed attempts; preserve them as evidence and record why they failed.

```yaml
film: day_one_pool_video_01
shot_id: "[shot_id]"
timeline_index: "[exact frame/time index]"
attempt: 1 # integer 1..20; maximum 20 fresh attempts per shot
candidate_path: "[review/build path]"
candidate_sha256: "[full file hash]"
native_dimensions: "[width]x[height]"
delivery_aspect: "[e.g. 16:9]"
orientation: "landscape"
square_pixels: true
rotation_metadata: false
prompt_sha256: "[prompt hash]"
generation_method: "fresh_full_frame_generation"
forbidden_methods_used: []
declared_beat: "[dirty|skimmer|waterfall_scrub|seahorse_effort|release|reward|rumi_rise]"
declared_action_or_hold: "[action description or intentional_hold + purpose]"
position_guide:
  used: false
  path: null
  sha256: null
  role: null # if used: position_only
  used_as_delivery_pixels: false
accepted_neighbor_refs:
  previous:
    path: "[path or null]"
    sha256: "[hash or null]"
  next:
    path: "[path or null]"
    sha256: "[hash or null]"
subject_geometry:
  roshan_bbox_norm: "[x,y,w,h or null]"
  active_prop_bbox_norm: "[x,y,w,h or null]"
  fixture_centers_norm: "[waterfall; seahorse]"
  mouth_plug_bbox_norm: "[bbox or null]"
  rumi_bbox_norm: "[bbox or null]"
  contact_points: "[net/trash; scrubber/lane; plug/nozzle; plug/basket; etc.]"
spatial_continuity:
  room_anchor_match: "[pass/fail + notes]"
  fixture_registration: "[pass/fail + notes]"
  camera_orientation: "[pass/fail + notes]"
  neighboring_motion: "[pass/fail/not_applicable + measured notes]"
identity_topology_style_review:
  roshan_identity: "[pass/fail + reviewer initials/date]"
  rumi_identity: "[pass/not_applicable/fail + reviewer initials/date]"
  fixture_identity: "[pass/fail + reviewer initials/date]"
  anatomy_topology_contact: "[pass/fail + notes]"
  style_material_integration: "[pass/fail + notes]"
phone_readability_review: "[pass/fail + notes]"
knockouts: []
rubric_scores:
  identity_canonical_continuity: 0.0
  beat_action_spatial_truth: 0.0
  natural_integration_style: 0.0
  child_readable_composition: 0.0
  cinematic_craft_evidence: 0.0
raw_total: 0.0
applied_documentary_cap: 4.9
acceptance_status: "[REJECT_KNOCKOUT|REJECT_SCORE|REGEN_REQUIRED|AUDIT_PASS_OWNER_PENDING|OWNER_ACCEPTED]"
reviewer_notes: "[specific evidence and targeted next prompt repair]"
```

## Decision checklist

- [ ] Candidate file is preserved at the recorded path and its full hash was
  computed before any normalization.
- [ ] Prompt and attempt are recorded; generation is a new complete flattened
  frame for this exact timeline index.
- [ ] Native candidate and neighbors are 16:9 landscape evidence; any
  production normalization is a whole-canvas post-acceptance transform only.
- [ ] Neighboring accepted frames are named and hashed; no pixels were blended
  or copied into this candidate.
- [ ] Identity/topology/style review is human-complete, not inferred from a
  green tool or isolated render.
- [ ] Subject geometry, fixture registration, action contact, spatial drift,
  and phone-size legibility are recorded.
- [ ] Every knockout is clear; if not, status is `REJECT_KNOCKOUT`.
- [ ] Score is ≥4.5; if not, status is `REJECT_SCORE` or `REGEN_REQUIRED`.
- [ ] Status is at most `AUDIT_PASS_OWNER_PENDING` unless owner has accepted
  this exact frame in runtime context. Luna does not assign 5.0.
- [ ] Attempt count remains ≤20. At attempt 20, unresolved failure is escalated
  rather than accepted below threshold.

**Luna verdict:** `[REJECT_KNOCKOUT | REJECT_SCORE | REGEN_REQUIRED | AUDIT_PASS_OWNER_PENDING]`
**Score after cap:** `[ ] / 4.90 documentary maximum`
**Targeted regeneration instruction:** `[one exact repair for the next attempt]`
**Reviewer/date:** `[ ]`
