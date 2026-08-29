# Owner-run Grok handoff — Day One Bubble Bathroom movies

## Current readiness — do not confuse archive with generation

The committed `HANDOFF_PACKET.json` directories are complete audit archives,
not executable Grok Imagine generation packets. Their 12 and 22 images must
not be uploaded together, the seven/eight-panel boards must not be bound as
pixel references, and the HUD-bearing runtime captures must not be used as
cinematic first frames. The broad Movie A/B prompts below are retained as
direction history; do not paste either one into a single multi-shot job.

Before generating, create one
`design/templates/IMAGINE_SHOT_CARD_V1.md` card for each A0–A6 and B0–B7 shot.
Each job binds only two to four approved, role-labeled images and needs an
accepted clean UI-free first frame. Generate one shot per job, then assemble
the accepted shots in edit. Until those cards and first frames exist and pass
the generator-readiness audit, this handoff is `ARCHIVE_COMPLETE` but
`GENERATION_READY: false` and `DELIVERY_ACCEPTED: false`.

## Use and authority

This is a visual-only storyboard and copy/paste handoff for two optional
cinematics. The owner performs every Grok upload, submission, and download.
Grok does not approve its own output and must not remove, combine, or reorder
the required beats. Codex/Luna review is the primary technical/editorial gate;
owner review is final.

Do not ask Grok for music, ambience, foley, voices, or a final mix. Any returned
audio is disposable sync reference. Never upload, imitate, or synthesize the
protected family voices. Runtime audio is selected only after the picture edit
passes its visual audit.

The runtime seams accept these eventual files:

- `assets/cinematics/day_one_bathroom_entry.ogv`
- `assets/cinematics/day_one_bathroom_cleaned.ogv`

Both are optional. If either file is absent or invalid, the game cuts directly
to the corresponding playable dirty or clean bathroom without a fail state.
When a real movie is present, its phase-specific once-only marker is committed
before playback. The entry movie precedes the basket lesson. The cleaned movie
follows the final tub scrub and precedes the pool-picture route.

## References for the owner to upload

Do **not** run either Grok job from this document alone. Upload the matching
self-contained packet directory and its `HANDOFF_PACKET.json`:

- Entry: `assets_src/cinematics/day_one_bathroom_entry_v1/`
  - exact appearance assets are in `handoff_art/`;
  - `10_entry_shot_board_7_panel_reference.png` gives one visual panel for each
    authored entry shot;
  - `02_entry_storyboard_reference.png` is the compact four-beat overview.
- Cleanup: `assets_src/cinematics/day_one_bathroom_cleaned_v1/`
  - exact appearance assets and dirty/clean anchors are in `handoff_art/`;
  - `14_cleanup_shot_board_8_panel_reference.png` gives one visual panel for
    every authored B0–B7 cleanup shot;
  - `runtime_boundary_sequence/` contains all eight current exact Godot 4.7.1
    gameplay boundary captures;
  - `03_cleanup_storyboard_reference.png` is the compact four-beat overview.

The packet manifest records dimensions, SHA-256, source, role, provenance,
modification status, generation prompt, and a deterministic whole-payload
hash. Appearance authority belongs to the exact copied room, character, bunny,
basket, tool, and grime assets—not to the generated storyboard boards. The
boards communicate narrative order only and are never delivery pixels.

The source paths below remain provenance and authority records; their exact
uploadable copies are already inside the packet:

1. `assets/flats/castle/rooms/room_bubble_bath.png` — approved complete room and
   locked camera/composition authority.
2. `assets/flats/castle/interactions_v4/backgrounds/room_bubble_bath_background.png`
   — approved healed background authority.
3. `assets/characters/roshan_25d/roshan_base.png`
4. `assets/characters/roshan_25d/roshan_directional.png`
5. `assets/characters/roshan_25d/roshan_gestures.png`
6. `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png`
7. `assets/castle/dirty_cleanup_2d/targets/target_sink_grime_v1.png`
8. `assets/castle/dirty_cleanup_2d/targets/target_tub_grime_v1.png`
9. `assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png`
10. `assets/castle/day_one_art_studio/magic_cleaning_brush.png`
11. `assets/castle/day_one_pool/activities/cleanup_basket.png`
12. The current exact 1280×720 Mobile captures produced by
    `scripts/probe_day_one_bathroom_shots.gd`, physically included in the
    cleanup packet's `runtime_boundary_sequence/`.

The runtime capture is composition and state-continuity evidence only. It is
not a delivery frame, background plate, or source of pixels to composite.

## Locked room and character continuity

- Preserve the exact wide room camera: scalloped tub on the left, shell sink in
  the center, pearl toilet on the right, aquarium windows, open warm floor, and
  the two lower-corner foreground shell baskets. Do not mirror or move fixtures.
- Roshan is the approved brown-haired child mermaid with rainbow forelock,
  pink top, and rainbow tail. The requested “walks into the room” beat is
  performed as her established gentle floor glide because she has a mermaid
  tail. Do not invent legs, shoes, or a human walk cycle.
- The bath is already full when first revealed. The existing water remains a
  living, bounded surface with restrained ripple/caustic movement. Its dirty
  state is muted olive-aqua, not horror sludge and not a global colour wash.
- The mermaid dust bunny is the supplied swimming cutout identity: lavender
  spiral ears, pearl accents, cloudlike tapered swimming body, large friendly
  eyes. Keep it small, cheerful, fully inside the basin, and behind the tub lip.
- One action is dominant per shot. No floating cards, text, UI, giant tools,
  overlay boxes, decorative ring fields, sticker halos, or extra characters.
- Polished flattened 2D storybook frames only: rounded readable shapes,
  navy/plum contours, broad painted value bands, aqua/lavender shadows,
  restrained highlights, stable room perspective, no photorealism or 3D render.

## Scene direction brief A — Roshan enters the dirty bathroom

**Scene ID:** `day_one_bathroom_entry_v1`
**Role:** orient the child, make the dirty bath and its friendly occupant the
single problem, then hand control to the pulsing cleaning basket.
**Point of view:** Roshan discovering a room that needs gentle help.
**Start → end:** empty dirty room → Roshan understands the bath needs cleaning.
**Emotional arc:** curiosity → surprise → sympathy → confident decision.
**Audience takeaway:** “The little swimmer needs us; cleaning can help.”

The camera is locked for the entire movie. The room provides orientation and
cause; Roshan’s gaze provides thought; her final turn toward the front-right
basket area provides the cut condition. Dominant motion is Roshan’s entrance,
then the bunny’s tiny paddle, then Roshan’s reaction—never all at once.

Target length: **7.0 seconds at 24 fps (168 frames)**.

| Frames | Beat | Full-frame direction and acceptance |
|---|---|---|
| 000–023 | A0 orientation hold | Exact approved wide bathroom with no Roshan. Tub is full of muted dirty olive-aqua water. The swimming dust bunny is small, fully contained behind the lip. Sink/tub grime is localized and readable. The room holds still except subtle living water. |
| 024–051 | A1 entrance anticipation | Roshan’s head/tail edge appears from the lower-center approach. The bunny and room stay spatially locked. Preserve clear floor space and both foreground occluders. |
| 052–083 | A2 entrance action | Roshan gently floor-glides into her established center-right gameplay position. Her body travels as one coherent mermaid silhouette; no legs, cutout translation, or camera pan. She looks into the room, not at the viewer. |
| 084–107 | A3 observation | Roshan settles. Her gaze shifts first to the dirty sink, then finishes on the full dirty tub and bunny. The bunny gives one tiny paddle only after Roshan is still. |
| 108–135 | A4 sympathetic reaction | Roshan leans slightly toward the tub with one hand at her chest, friendly concern rather than disgust. Keep her clear of the bunny and waterline. The dirty state remains unchanged. |
| 136–155 | A5 decision | Roshan straightens and turns her gaze/one open hand toward the front-right supply-basket location. Do not generate a UI pointer or basket pulse inside the movie. |
| 156–167 | A6 settle/cut | Hold the completed “let’s help” pose long enough to read. End with the room layout matching the first interactive frame so the runtime basket and pointer can appear without a spatial jump. |

### Grok prompt A

Create one complete newly drawn full-frame 1280×720 image for the next frame of
a polished flattened 2D Mermaid Roshan storybook cinematic. Preserve the exact
supplied Bubble Bathroom camera and architecture: scalloped peach shell bathtub
at left, shell sink centered, pink pearl toilet at right, lavender shell-stone
walls, aquarium windows, coral decorations, open warm floor, and both
lower-corner foreground shell baskets. Preserve Roshan’s exact approved brown
hair, rainbow forelock, pink top, rainbow mermaid tail, face, age, proportions,
and costume. She enters with her established gentle mermaid floor glide; never
give her legs or shoes.

CURRENT FRAME / BEAT: [paste exactly one row direction from Movie A].

The tub is already full of bounded muted olive-aqua dirty water with subtle
living ripples. The supplied lavender swimming dust bunny remains small,
friendly, fully inside the water, and naturally occluded behind the tub lip.
Use one dominant action only and preserve all fixed landmarks. Return one
complete flattened frame, never layers, cutouts, a sprite sheet, rig, composite,
or translated plate. No text, UI, pointer, camera drift, photorealism, 3D,
frightening dirt, fumes, mold, extra characters, fixture redesign, global tint,
interpolation, tweening, morphing, optical flow, cross-dissolve, or duplicated
action frame.

## Scene direction brief B — Roshan finishes the clean bathroom

**Scene ID:** `day_one_bathroom_cleaned_v1`
**Role:** pay off the player’s completed sink and tub gestures, let the bunny
leave safely, and hand attention to the actual pool picture.
**Point of view:** Roshan seeing that her work helped.
**Start → end:** final wet brush contact at the nearly clean tub → calm clean
room with Roshan ready to follow the pool route.
**Emotional arc:** focused care → visible consequence → relief → delight.
**Audience takeaway:** “I cleaned it; the bunny is safe; the pool is next.”

This is not a second unrelated cleaning mechanic and does not replay the whole
minigame. It begins on the final player-authored tub stroke, shows the last
visible dirt/water consequence, then holds the clean result. Sink is already
clean at frame B0 because the player completed it first.

Target length: **8.0 seconds at 24 fps (192 frames)**.

| Frames | Beat | Full-frame direction and acceptance |
|---|---|---|
| 000–023 | B0 exact handoff | Match the final interactive tub frame: sink clean, Roshan at center-right, brush making clear contact with the last tub grime, water still partly olive-aqua, bunny visible behind the lip. No continuity jump. |
| 024–055 | B1 last scrub | Roshan completes one readable back-and-forth brush action. Show hand–brush–tub contact and a broad clean stripe beneath the tool. Camera and all fixtures remain locked. |
| 056–083 | B2 water clears | Roshan settles the brush. Dirty colour retreats locally through the living ripples, revealing clear approved aqua water. The final grime leaves the rim. Do not hide contact with bubbles or sparkles. |
| 084–111 | B3 bunny recovery | The clean bunny perks up and paddles toward the near-left safe edge. Roshan watches; she does not move simultaneously. Water stays contained and clean. |
| 112–139 | B4 safe exit | In distinct complete frames, the bunny makes one small buoyant hop out of the basin toward a safe offscreen/foreground exit. Preserve depth over the back water and behind the lip until release; no teleport or body redesign. |
| 140–163 | B5 room consequence | Three restrained sparkles appear at tub, sink, and Roshan—not in a center-floor burst. Warm approved room values return. Roshan’s shoulders and expression relax. |
| 164–179 | B6 next intention | Roshan turns her gaze and one open hand toward the right-side location where the actual pool-room picture will appear after the movie. Do not generate the UI picture inside the cinematic. |
| 180–191 | B7 clean settle/cut | Hold the clean room and completed happy pose. End on the exact clean runtime composition; the pool picture and ghost-hand pointer may then appear without overlap or ambiguity. |

### Grok prompt B

Create one complete newly drawn full-frame 1280×720 image for the next frame of
a polished flattened 2D Mermaid Roshan storybook cinematic. Preserve the exact
supplied Bubble Bathroom camera, architecture, fixture placement, foreground
occluders, Roshan identity/costume/proportions, approved sponge and brush design,
and approved lavender swimming dust-bunny identity.

CURRENT FRAME / BEAT: [paste exactly one row direction from Movie B].

This sequence begins at the final player-authored tub-brush contact. The sink is
already clean. Dirty bath water changes locally from muted olive-aqua to the
approved clear aqua as the final grime leaves; it remains bounded, rippled, and
behind the tub lip. Show action, contact, consequence, reaction, and settle in
that order. Use one dominant action only. Return one complete flattened frame,
never layers, cutouts, a sprite sheet, rig, composite, or translated plate. No
text, UI, pool-route card, camera drift, photorealism, 3D, frightening dirt,
fumes, extra characters, redesigned fixtures, global tint, giant sparkles,
interpolation, tweening, morphing, optical flow, cross-dissolve, or duplicated
action frame.

## Production and audit contract

- Delivery is 1280×720, square pixels, landscape, 24 fps, Theora/Vorbis OGV.
- Treat the frame numbers above as editorial/rhythm ranges, not permission to
  synthesize the intervening motion. Every changed action frame is a separately
  generated and accepted complete flattened frame.
- Intentional holds are allowed only in the declared hold spans and must be
  identified with narrative purpose in each manifest.
- No tween, morph, optical flow, interpolation, cross-dissolve, translated
  layer, sprite/rig animation, procedural warp, or duplicated action frame may
  supply missing motion.
- Keep native candidates, hashes, prompt hashes, attempt records, neighboring
  accepted-frame references, action/hold declarations, subject geometry,
  contact states, character-passport review, and human identity/topology/style
  decisions for every regenerated frame.
- Use separate manifests and audit packets for entry and cleaned movies. Both
  must pass `tools/audit_cinematic.py`, the Scene Direction Brief, silent and
  sounded normal-speed review, half-speed review, and frame-step comparison.
- Do not install an OGV merely because it encodes correctly. Frame integrity,
  scene congruency, rhythm, Roshan identity, contact, and final editorial review
  remain blocking. Owner acceptance is final.

## Exact production packet and manifest skeleton

Create one packet per movie at these stable paths:

- `assets_src/cinematics/day_one_bathroom_entry_v1/`
- `assets_src/cinematics/day_one_bathroom_cleaned_v1/`

Each directory already contains its required uploadable `handoff_art/` and
`HANDOFF_PACKET.json`; preserve them when production begins. Each packet also
contains or later adds `prompts/`, native `candidates/`, `masks/`, optional
neutral-field `position_guides/`, `frame_regeneration_manifest.json`,
`quality_manifest.json`, and `REVIEW.md`. Audit reports go to
`audit/cinematics/day_one_bathroom_{entry,cleaned}_v1/`. Preserve native
candidates; production normalization and the OGV are additional artifacts.

Use this exact validator-facing skeleton for every frame. Replace every
placeholder and repeat the frame object for every timeline index; extras such
as movie/codec/contact metadata are traceability fields and do not replace the
validator-required fields.

```json
{
  "schema": "cinematic-frame-regeneration-v1",
  "movie_id": "day_one_bathroom_entry_v1",
  "frame_index_origin": 0,
  "delivery_size": [1280, 720],
  "delivery_fps": 24,
  "delivery_codec": "Theora/Vorbis OGV",
  "final_ogv": {"path": "../../../assets/cinematics/day_one_bathroom_entry.ogv", "sha256": "<64 hex>"},
  "canvas_policy": "exact_native_size",
  "maximum_native_aspect_error": 0.002,
  "runtime_cut_in": "dirty bathroom before basket lesson",
  "runtime_cut_out": "first interactive dirty-bath frame",
  "reference_assets": [
    {"path": "<approved appearance reference>", "sha256": "<64 hex>", "role": "appearance_authority", "used_as_delivery_pixels": false}
  ],
  "frames": [
    {
      "frame": 0,
      "candidate": {"path": "candidates/frame_000000.png", "sha256": "<64 hex>"},
      "prompt": {"path": "prompts/frame_000000.txt", "sha256": "<64 hex>"},
      "prompt_sha256": "<same 64 hex prompt hash>",
      "generation_method": "full_frame_image_generation",
      "delivery_techniques": [],
      "temporal_derivation": "none",
      "attempt": 1,
      "attempt_id": "entry-f000000-a01",
      "action_state": "hold",
      "hold_reason": "declared orientation hold",
      "generation_references": [
        {"path": "<approved room or identity reference>", "sha256": "<64 hex>", "role": "appearance_authority", "used_as_delivery_pixels": false}
      ],
      "previous_reference": {"path": "<accepted prior frame>", "sha256": "<64 hex>"},
      "next_reference": {"path": "<accepted next/key frame>", "sha256": "<64 hex>"},
      "position_guide": {
        "path": "position_guides/frame_000000_neutral.png",
        "sha256": "<64 hex>",
        "role": "position_only",
        "used_as_delivery_pixels": false,
        "min_mean_pixel_delta": 2.0,
        "max_exact_pixel_ratio": 0.05
      },
      "subjects": [
        {
          "id": "roshan",
          "candidate_mask": {"path": "masks/frame_000000_roshan.png", "sha256": "<64 hex>"},
          "position_guide_mask": {"path": "position_guides/frame_000000_roshan_mask.png", "sha256": "<64 hex>"},
          "position_anchor": "center",
          "position_axis": "xy",
          "max_position_error": 0.015,
          "required_direction": "still",
          "max_step_error": 0.035,
          "max_cross_axis_step": 0.020,
          "max_bbox_height_step": 0.025,
          "normalized_bbox": [0.0, 0.0, 0.0, 0.0],
          "contact_state": "none"
        }
      ],
      "human_review": {
        "identity": 4.9,
        "topology": 4.9,
        "style": 4.9,
        "neighbor_continuity": 4.9,
        "reviewer": "<human name>",
        "reviewed_at": "<ISO-8601>",
        "decision": "accepted"
      }
    }
  ]
}
```

For frame 0, omit `previous_reference`; for the final frame,
`next_reference` may be omitted. Omit the entire `position_guide` and each
`position_guide_mask` when no guide was used. When used, guides stay on a
neutral field and are never delivery pixels. Every appearance and neighbor
reference is also recorded in `generation_references` with its real hash.

The cleaned movie uses the same schema with movie ID
`day_one_bathroom_cleaned_v1`, runtime cut-in “final interactive tub-brush
contact,” and cut-out “clean bathroom before pool-picture reveal.” Bind both
manifests to hashes of their exact dirty/clean Mobile capture references.

### Exact production quality manifests

After each OGV is encoded, bootstrap its validator-owned structure rather than
inventing scene fields:

```text
python tools/audit_cinematic.py assets/cinematics/day_one_bathroom_entry.ogv --bootstrap assets_src/cinematics/day_one_bathroom_entry_v1/quality_manifest.json
python tools/audit_cinematic.py assets/cinematics/day_one_bathroom_cleaned.ogv --bootstrap assets_src/cinematics/day_one_bathroom_cleaned_v1/quality_manifest.json
```

Replace the bootstrap placeholders with the following contracts. `samples`
must contain one object for **every** integer frame in the scene range; the two
objects shown below define the first and last required shapes and are not
permission to leave intervening frames absent. Coordinates are normalized to
the complete 1280×720 frame. Generate the repeated sample rows from accepted
frame measurements, never by interpolating delivery pixels.

Entry `quality_manifest.json` uses `schema: cinematic-quality-v2`,
`frame_index_origin: 0`, video path
`assets/cinematics/day_one_bathroom_entry.ogv`, `fps: 24.0`,
`frame_count: 168`, and one contiguous scene:

```json
{
  "schema": "cinematic-quality-v2",
  "frame_index_origin": 0,
  "video": {
    "path": "assets/cinematics/day_one_bathroom_entry.ogv",
    "fps": 24.0,
    "frame_count": 168,
    "geometry": {"coded_width": 1280, "coded_height": 720, "display_width": 1280, "display_height": 720, "aspect_ratio": "16:9"}
  },
  "character_passports": {
    "roshan": {
      "reference_image": "assets/characters/roshan_25d/roshan_base.png",
      "landmarks": ["face_center", "crown", "left_hand", "right_hand", "tail_tip"],
      "global_review": {"construction": 4.9, "identity": 4.95, "motion": 4.9, "contact": 4.9, "style": 4.95, "performance": 4.9}
    },
    "dust_bunny": {
      "reference_image": "assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png",
      "landmarks": ["eye_center", "ear_pair", "body_center", "tail_tip"],
      "global_review": {"construction": 4.9, "identity": 4.95, "motion": 4.9, "contact": 4.9, "style": 4.95, "performance": 4.9}
    }
  },
  "scenes": [{
    "id": "day_one_bathroom_entry_v1",
    "background_id": "room_bubble_bath_dirty_day_one",
    "start_frame": 0,
    "end_frame": 167,
    "characters": ["roshan", "dust_bunny"],
    "tracks": [
      {"id": "roshan_body_center", "character_id": "roshan", "max_step": 0.035,
       "samples": [{"frame": 0, "x": 0.62, "y": 0.72, "visible": false}, {"frame": 167, "x": 0.62, "y": 0.72, "visible": true}]},
      {"id": "dust_bunny_body_center", "character_id": "dust_bunny", "max_step": 0.02,
       "samples": [{"frame": 0, "x": 0.235, "y": 0.355, "visible": true}, {"frame": 167, "x": 0.235, "y": 0.355, "visible": true}]}
    ],
    "contacts": [
      {"id": "roshan_enters_room", "start_frame": 24, "end_frame": 83},
      {"id": "roshan_observes_bunny", "start_frame": 84, "end_frame": 135},
      {"id": "roshan_chooses_basket", "start_frame": 136, "end_frame": 155}
    ],
    "review": {"construction": 4.9, "identity": 4.95, "motion": 4.9, "contact": 4.9, "style": 4.95, "performance": 4.9}
  }]
}
```

Roshan is invisible only before her authored entrance, glides from the locked
lower-center approach into her established center-right gameplay mark over
frames 24–83, then settles. The bunny remains within the tub-water mask for
all 168 samples; its small paddle occupies frames 84–107.

Cleaned `quality_manifest.json` has the same passports and geometry, video
path `assets/cinematics/day_one_bathroom_cleaned.ogv`, `frame_count: 192`, and
this one-scene body:

```json
{
  "schema": "cinematic-quality-v2",
  "frame_index_origin": 0,
  "video": {
    "path": "assets/cinematics/day_one_bathroom_cleaned.ogv",
    "fps": 24.0,
    "frame_count": 192,
    "geometry": {"coded_width": 1280, "coded_height": 720, "display_width": 1280, "display_height": 720, "aspect_ratio": "16:9"}
  },
  "character_passports": {
    "roshan": {
      "reference_image": "assets/characters/roshan_25d/roshan_base.png",
      "landmarks": ["face_center", "crown", "left_hand", "right_hand", "tail_tip"],
      "global_review": {"construction": 4.9, "identity": 4.95, "motion": 4.9, "contact": 4.9, "style": 4.95, "performance": 4.9}
    },
    "dust_bunny": {
      "reference_image": "assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png",
      "landmarks": ["eye_center", "ear_pair", "body_center", "tail_tip"],
      "global_review": {"construction": 4.9, "identity": 4.95, "motion": 4.9, "contact": 4.9, "style": 4.95, "performance": 4.9}
    }
  },
  "scenes": [{
    "id": "day_one_bathroom_cleaned_v1",
    "background_id": "room_bubble_bath_clean_day_one",
    "start_frame": 0,
    "end_frame": 191,
    "characters": ["roshan", "dust_bunny"],
    "tracks": [
      {"id": "roshan_body_center", "character_id": "roshan", "max_step": 0.035,
       "samples": [{"frame": 0, "x": 0.62, "y": 0.72, "visible": true}, {"frame": 191, "x": 0.62, "y": 0.72, "visible": true}]},
      {"id": "dust_bunny_body_center", "character_id": "dust_bunny", "max_step": 0.02,
       "samples": [{"frame": 0, "x": 0.235, "y": 0.355, "visible": true}, {"frame": 191, "x": 0.12, "y": 0.34, "visible": false}]}
    ],
    "contacts": [
      {"id": "brush_contacts_final_tub_grime", "start_frame": 0, "end_frame": 55},
      {"id": "water_clears_and_grime_releases", "start_frame": 56, "end_frame": 83},
      {"id": "bunny_recovery_paddle", "start_frame": 84, "end_frame": 111},
      {"id": "bunny_safe_exit", "start_frame": 112, "end_frame": 139},
      {"id": "room_sparkle_consequence", "start_frame": 140, "end_frame": 163},
      {"id": "roshan_points_to_pool_route", "start_frame": 164, "end_frame": 179}
    ],
    "review": {"construction": 4.9, "identity": 4.95, "motion": 4.9, "contact": 4.9, "style": 4.95, "performance": 4.9}
  }]
}
```

Expand both cleaned tracks through every frame 0–191. Roshan stays essentially
stationary except for the authored gaze, hand, and settle actions. The bunny
stays inside the tub through frame 111, travels toward the near-left safe exit
over frames 112–139, and is `visible: false` afterward. The validator requires
the six score keys `construction`, `identity`, `motion`, `contact`, `style`,
and `performance`; production floors are 4.85 for every scene score and 4.90
for every passport score. Scores shown here are target values, not automatic
acceptance: the named human reviewer must replace them with measured results.

Run and retain these blocking reports for each movie:

```text
python tools/audit_cinematic.py <movie.ogv> --frame-regeneration-manifest <packet/frame_regeneration_manifest.json> --report <audit-dir/frame_regeneration_report.json>
python tools/audit_cinematic.py <movie.ogv> --manifest <packet/quality_manifest.json> --profile production --report <audit-dir/quality_report.json>
python tools/audit_cinematic.py <movie.ogv> --analyze --report <audit-dir/pixel_transition_evidence.json>
```

`REVIEW.md` records normal-speed review with sound, normal-speed silent review,
half-speed review, frame-step/onion-skin review, and real-device playback on the
target Android tablet/phone. Record reviewer, date, decision, defects, repaired
frame windows, exact OGV SHA-256, and the matching passing report hashes.
