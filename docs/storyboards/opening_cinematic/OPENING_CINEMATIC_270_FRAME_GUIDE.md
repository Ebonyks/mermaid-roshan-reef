# Opening cinematic — 270-frame production guide

## Delivery specification

- Duration: **15.000 seconds**
- Storyboard rate: **18 frames per second**
- Published frames: **F001–F270**
- Sheet layout: **30 sheets**, nine consecutive images per 3×3 sheet
- Read order: left-to-right, then top-to-bottom
- Frame time: `(frame number - 1) / 18`
- Final frame: F270 at 14.944 seconds, held through 15.000 seconds
- Gameplay interface: appears only on the game tick after F270
- Retimed storyboard video: all 270 existing panels played at **12 fps** for a
  **22.500-second** silent review master

This is a point-by-point animation and cinematography guide. Every adjacent image
is a distinct micro-beat, not an invitation to jump directly between broad poses.
The written guide specifies the intended camera delta, character performance,
physical follow-through, lighting, prop state, and emotional purpose for every
frame.

## Detailed frame guides

1. [F001–F135: approach, cabin jolt, reassurance, landing, and unbuckling](guide_parts/part_a_F001-F135.md)
2. [F136–F270: rising, aisle, door, stairs, Sky Lagoon reveal, and gameplay handoff](guide_parts/part_b_F136-F270.md)
3. [Binding continuity and visual-QC bible](guide_parts/continuity_and_qc.md)

## Image package

- [Thirty 3×3 storyboard sheets](sheets/)
- [270 individually extracted frame images](frames/)
- [Initial visual-direction proof](opening_cinematic_proof_3x3_v1.png)
- [12 fps storyboard video — 22.5-second H.264 MP4](opening_cinematic_storyboard_12fps_22.5s.mp4)
- [Stabilized V2 sheets, frames, and 12 fps review master](v2/)
- [Animation QC acceptance criteria](ANIMATION_QC_CRITERIA.md)
- [V2 before/after animation audit](ANIMATION_AUDIT_V2.md)
- [External cinematic-gate manifests, report, and scene samples](v2/external_audit/)

Individual image names include the one-based frame number and rounded millisecond
time. For example, `F145_08000ms.png` is frame F145 at 8.000 seconds.

## Sequence architecture

| Act | Frames | Time | Production purpose |
|---|---:|---:|---|
| Exterior arrival | F001–F018 | 0.000–0.944 | Establish the tiny pilotless passenger jet and child-safe approach. |
| Nervousness and reassurance | F019–F090 | 1.000–4.944 | Turn a small cabin jolt into a readable reach, hug, shared sway, and calm smile. |
| Landing and release | F091–F135 | 5.000–7.444 | Give touchdown, settling, safe cue, hug release, and each buckle its own physical beats. |
| Stand and travel | F136–F180 | 7.500–9.944 | Show tail-supported rising, hand contact, aisle glides, and shell-pad activation without pose jumps. |
| Door, stair, and platform | F181–F234 | 10.000–12.944 | Separate the door angles, six-step deployment, threshold transfers, descent, and final platform balance. |
| Discovery and handoff | F235–F270 | 13.000–15.000 | Withhold geography, play the facial reaction, reveal the accepted Sky Lagoon layout, and settle into gameplay. |

## Authority order

If a generated panel drifts from the project design, use this order of authority:

1. The binding continuity/QC bible and per-frame written direction.
2. Canonical character references:
   `gen2/turnarounds/roshan_v2/front.png`,
   `gen2/turnarounds/roshan_v2/side.png`, and
   `assets/characters/friends/daddy.webp`.
3. Accepted Sky Lagoon geography:
   `assets_src/sky_lagoon/runtime_candidate_046fbcf/lagoon_01_arrival_path.png`.
4. The generated storyboard image.

This matters particularly for discrete counts and topology. The production build
must always contain exactly two passenger seats, no visible pilot or cockpit,
exactly six pearl stair treads plus the separate landing, exactly two lavender
rails, intact mer-tails with no legs, and the accepted Sky Lagoon landmark layout.
The storyboard art communicates framing, motion, emotion, color, and timing; it
does not override those locked facts.

## Animation-use notes

- Keep the 18 fps storyboard timing as the editorial rhythm even if animation is
  rendered at a higher rate. Add in-betweens inside these intervals; do not remove
  the listed beats.
- Ease camera motion continuously within a sheet. Cuts are motivated at the sheet
  boundaries identified in the detailed guide.
- Preserve one-finger, non-reader clarity: every intention is legible through
  hands, eye lines, large silhouettes, light cues, and spatial staging.
- Turbulence and landing remain mild. There is no danger, alarm, fail state,
  separation, crying, smoke, lightning, or violent motion.
- Keep the kingdom unrevealed through F252. S27 supplies only edge hints and S28
  stays on faces. The full accepted geography first appears at F253.
- End on a stable, UI-free gameplay composition at F270 so player control can
  begin without a visible camera pop.
