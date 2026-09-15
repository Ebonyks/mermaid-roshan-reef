# Grand Puff movement profile — review candidate v1

Status: `SUPPORTING_CURRENT`, 2026-09-14. This is an editable asset review,
commissioned by the owner from Grok's signed return. It grants no runtime,
cinematic, device, child or final visual acceptance.

## Owner review update — 2026-09-14

The owner rejected the reconstructed motion as too limited and insufficiently
faithful to Grok's personality. The 105-frame set remains an editable source and
rejected performance baseline; its machine checks do not rehabilitate the acting.
The current corrective work is the [three-pilot Grok handoff](../../assets_src/cinematics/grand_puff_personality_repair_2026-09-14/r01/START_HERE.txt):
laugh, angry windup and friends, followed by timed return/review cycles. Preserve
the expressive poses and emotional beats while repairing anatomy drift. No live
integration or production acceptance has been authorized by this update.

## Identity, scope and sources

Grand Puff is the cloud bunny boss who becomes a small intact friend. The signed
front, profile and back at Grok commit `8d07b0908c39051c2a310caf29fd86a56dc82b40`
lock the painted curls, inward spiral ears, two ear-base pearls, two floor paws,
two pointed upper teeth and pale crest sparkle. Existing game baseline is
`29bd345dd67dbc4ed4bbf2f02527cd53c7482cfc`.
[Source bindings](../../assets_src/characters/grand_puff_aseprite_2026-09-14/SOURCE_BINDINGS.json)
record exact preserved files/hashes. Fifteen MP4s supply editorial intentions only;
none of their pixels enter the reconstruction. The signed stills are isolated,
partitioned and articulated, with harmonic underpainting and newly drawn facial
cels. This method is for interactive Canvas candidates, never cinematic delivery.

[Impact](../audit_impacts/grand-puff-aseprite-20260914.json) records applicable
authority, visual, motion, asset and quality rules by exact IDs. MA-VIS-006 and MA-TOUCH-001
remain open at their existing canonical lifecycle; an asset review repairs neither.

## Acting thesis

Proposed interpretation: Puff wants to seem enormous, puts visible effort into
his attacks, and reveals a cuddly personality when that effort subsides.

| Quality | Visible habit | Avoid |
|---|---|---|
| Proud | Open-eye stare, a held stance before compressing | Cruel or frightening anger |
| Effortful | Broad base compresses before rising; ears follow the effort | Weightless whole-sticker bobbing as the entire performance |
| Playful | Closed-eye laugh, wink recovery, intact small friendly settle | Implosion, distress, extra limbs or anatomy drift |

Listening is a quiet open-eye hold; approach is the proposed alternating-paw prowl.
Error reads as a brief flinch or dizzy eye, then a safe settle. Success softens into
the friends pose. Asking for help and relationships beyond the signed ending are
uncommissioned/unknown, not new canon. Attention returns to the child's action via
quiet idle; the idle itself never advances a battle.

## Movement grammar

Face leads intention; body compression supplies effort; spiral ears trail by small
angles. Ordinary register uses a quiet breath/blink; attentive windup compresses
progressively; excitement contrasts squash with release and laughter; recovery
reduces motion and settles into open eyes or a wink. Four pearl forms, spiral ears,
painted palette and the crest remain constant. Paws are separate editable cels;
all locomotion and full stage travel remain external responsibilities.

Authoring cells are 512×512 RGBA, with a 32px safe border and nominal support pivot
(256,480). The isolated sole ends around y=478, allowing a two-pixel filtering margin.
Coordinates are pixels, +x right, +y down. Local elevation is at most 24px; it is
an acting study, not the stage trajectory. No prop sockets are commissioned. Ear
seams overlap beneath the body. Gold counter, dust, speed, splash and lock-flash
FX must be separate layers/actors in a later integration. The pale crest is anatomy.

The intended diagnostic display is 112px high and full 512px authoring scale.
Aspect-ratio/camera acceptance remains pending in-context Mobile captures. The
body must not obscure the aiming/locked/launching warning sequence; the third
warning's colour change is external to this asset. Three-quarter reconstruction
is not included: only the signed front/profile/back reference views are supplied.

## Clip vocabulary and contracts

[Clip contract](../../assets_src/characters/grand_puff_aseprite_2026-09-14/CLIP_CONTRACT.json)
is the exact ordered state/duration/bounds record for all 105 frames and 15 tags.
Every frame references the shared signed source bindings above. Durations are
proposed interactive phrasing, not a transcription of the six-second MP4 lengths.

| Clip | Intention and sequence | Boundary/contact |
|---|---|---|
| idle | Rest, small inhale, blink, settle | Grounded; proposed loop |
| jump | Anticipate, compress, release, apex, land, recover | Keys 3–6 airborne; key 7 proposed landing |
| laugh_vulnerable | Close eyes, laugh pulses, smile, reopen | Grounded; vulnerability remains gameplay-owned |
| flinch_1 | Surprise, compress, recover | Grounded; no damage event in asset |
| flinch_2 | Compress, dizzy eye oscillation, blink, recover | Grounded; no loss/failure state |
| flinch_3 | Compress, wink, settle | Grounded |
| angry | Puff/huff, hold proud face, soften | Grounded; no straight rabbit ears |
| angry_jump_final | Effort hold, deeper squash, release, land, settle | Keys 4–7 airborne; key 8 proposed landing |
| friends | Close eyes, become small intact friend, wink, hold | Grounded; last frame held, never loop back to large |
| showing | Small intact body swells into proud stance | Grounded; no dust nest or baked props |
| peek | Compress, look, recover, duck pose | External foreground owns occlusion; no hatch pixels |
| windup | Progressive compression and held readiness | Grounded; last frame held until gameplay releases |
| prowl | Alternating paw effort and short local lift | Proposed cycle; stage movement remains external |
| giggle | Close eyes, laugh with small alternating lean, settle | Proposed loop; no passive reward |
| splash | Proud ear cock, wink, soft settle | Presentation pose; no title or FX pixels |

Entry is front-facing, no held prop. Except friends/showing/peek boundaries specified
above, the resting destination is front idle at the existing stage position.
Windup's 1.26s body study does not shorten the full 2.2–2.7s gameplay aim warning:
a later adapter must hold readiness while the attack owner finishes its warning.
No frame directly commits damage, rewards, progression, saves, sound or FX.
Landing/effort markers are proposed presentation labels only and must validate the
current attack request before an at-most-once effect in any future adapter.

Future integration contract, not implemented APIs: navigation owns translation;
retarget/cancel/back/exit must invalidate delayed markers; pause/focus loss freezes
presentation and clears touch ownership; reload restores authoritative progress and
safe idle (or small friends state if already committed), never a remembered frame
reward. Touch feedback must begin within two rendered frames at 30fps independently
of decorative timing. No new state/save/input owner is created in this pass.

## Review and acceptance

The pilot compares idle, jump and laugh with identical front identity, cell, source
paint and support pivot. Controlled contrast is compression/release versus facial
laugh acting. Exact state durations and support offsets are in the clip contract.
Check hard failures first: clipping, extra pearls, lost spiral topology, opaque
background, missing teeth in toothed mouth states, detached support or baked FX.
Then assess intention, personality, weight, rhythm and quietness without averaging
away failures. Contact-sheet inspection checks anatomy and expressions, not full
motion acceptance. Native reopen/export, alpha/bounds and hash evidence live in
[verification](../../assets_src/characters/grand_puff_aseprite_2026-09-14/VERIFICATION.json).

No matched in-game A/B, touch-latency measurement, target-device performance,
child comprehension or owner animation acceptance has occurred for these cels.
The modest part articulation and new facial states are review candidates; a richer
painted in-between pass may still be needed to meet the requested impact. No 4.75/5
score is assigned. Existing live renderer and ending are unchanged.

## Round-one Grok return review

The [round-two correction](../../assets_src/cinematics/grand_puff_personality_repair_2026-09-14/r02/START_HERE.txt) records direct review of Grok return `caec2f39188599b4c94f82e6cdd787d79821b732`: richer movement, but missing sustained friendship shrink, smiling huff, and challenging laugh ending. Four pearl forms are correct in inspected samples; the return's extra-pearl claim is unsupported there. No clip, runtime, owner or finding acceptance is granted.

Round-two return `f55d22365cd7f5380ea8d01abe471fe70399f822` restores the laugh payoff and introduces real shrink. [Round three](../../assets_src/cinematics/grand_puff_personality_repair_2026-09-14/r03/START_HERE.txt) carries P01 as preferred motion reference and limits regeneration to P02 eye/ear continuity and P03 spiral-ear/support/shrink repairs. No production acceptance.
