# Mermaid Roshan — movement and acting language

Version 1.3 · owner commission 2026-09-11; left/right, two-speed/source-frame and short-gameplay timing decisions 2026-09-16 · source baseline
`cdfd937a7db4b3d41e7c469fb8e6a8fe812cd016`.

Authority: `BINDING_DOMAIN` for the commissioned direction and briefing
protocol, subordinate to the [canonical motion rules](../06_COMPREHENSIVE_DESIGN_LANGUAGE.md#9-motion-acting-feedback-and-rewards).
Ribbon Glide with Playful Dolphin accents is the **working creative direction**.
Its numerical targets are pilot starting points, not measured asset facts or
approved footage. The owner has commissioned this language, not selected an
unseen pilot. Refine it through the [production protocol](ANIMATION_PRODUCTION_PROTOCOL.md)
and record evidence in the [animation audit branch](../../audit/animation/README.md).

## Gameplay facing — left/right only

Owner decision 2026-09-16: Roshan gameplay animation has **two display facings,
left and right**, not four-way or eight-way authored coverage. Produce one
canonical **right-facing** source family and derive the left display by a
horizontal mirror of the complete sprite. A readable right-facing three-quarter
view is valid; do not redesign the approved painting into a strict profile.
Apply this to idle, start/cruise/stop swimming, dash, and applicable interactions.
Existing front/rear/turnaround art remains preserved reference, not a requirement
to commission additional direction sets. Cinematic shot direction is unchanged.

This changes presentation, not navigation: vertical/diagonal travel may retain
the appropriate left/right facing. Pure vertical travel and rest retain the last
nonzero horizontal facing; a new actor defaults to right. Future runtime work
must use a small direction dead zone/hysteresis to avoid flicker near zero.
Do not rotate toward/away from the viewer to manufacture cardinal directions.
Keep genuine torso response, sculling arms, tail propulsion, expression and
buoyant hair; reduced view count is not permission for a rigid translated body.

The canonical source retains the rainbow streak on Roshan's anatomical left.
The owner-authorized whole-sprite mirror reverses its apparent screen/anatomical
side in the left-facing gameplay display; that deterministic display reversal
is allowed and is not source-identity drift. Never randomly migrate the streak
within a source take or independently regenerate it to match the display flip.
The exception is for mirrored gameplay presentation, not canonical reference art
or authored cinematic continuity. Do not mirror a whole scene, UI or lettering.

Mirror about the same actor pivot without changing scale, timing or stroke phase.
Reflect local hand/tool sockets, grip offsets and orientation consistently
(`x_local' = -x_local` about that pivot); world targets remain fixed. Review
attached props separately where readable markings or contact prevent blind
mirroring. Do not invent a four-direction set to solve a named contact exception.
A left/right reversal is a discrete presentation flip, not a scale tween through
zero or a fake yaw. Verify silhouette, pivot stability, loop seam, hand/prop
contact and rapid reversals in **both** displayed facings before acceptance.
No runtime flip or mirrored art is implemented or accepted by this document.

## Two swim speeds and performance-led openings

Owner clarification 2026-09-16 commissions **two distinct performances**:
slow, relaxed swimming and a dash. Both retain the right-facing source /
mirrored-left display contract above. A dash is newly performed stronger
propulsion, compact preparation, coordinated arm recovery and readable
deceleration, not the slow clip played faster. Relaxed travel uses softer
effort, longer glides and available attention. Fast need not mean panicked.
Compare both at native normal speed before accepting their distinction.

For this Grok gameplay-source workflow, select a suitable **actual native
frame from existing Grok footage** as the next generation's starting image.
Keep approved artwork as identity/style authority, not a mandatory opening or
resting pose. Grok may choose the frame without another owner opening-approval
step, but must screen face/crown/costume, anatomy, hair attachment, tail/fin,
right-facing readability and full-body margins and record the source video
hash, native frame index/timestamp and extracted PNG hash. A sound frame from
a motion-rejected take may seed a revision; that does not pass the old video.
This lossless frame capture is generation-input preparation, not Aseprite
conversion of failed footage. No new still, composite or deformation seed.

This clarification supersedes earlier fixed-opening instructions for this
pilot, including reuse of a particular locked-front-right still. Preserve
identity, broad framing and camera stability, not pixel equality to that
painting. Give expressive poses room to change. Take start/loop/finish cuts
from observed motion; prompt timestamps are choreography guides, not mandatory
edit indices. Loop joins must match pose, motion direction and speed, including
arms, hair and fin, rather than merely similar endpoint images.

Any small bridge between these performances and the current resting character
is **deferred separate work if needed**. Do not constrain either performance
to the resting sprite's exact pose or add a rest-match rejection gate.
This is not permission to hide defects with morphing, warping, crossfades or
static inserts. The bridge method and slow/dash transition implementation need
their own scoped design and review; neither is implemented here. A mismatch
to the old resting pose alone does not fail a good core performance.

Use the [two-speed handoff](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/START_HERE.txt).
Every new source still requires independent source review; failures go back
to Grok, never Aseprite. At 4.8/5 with no blocking defect, stop for human review.
This direction change accepts no clip, runtime behavior or cinematic delivery.

## Responsive click-to-move timing

The owner approves the A001 motion/acting direction but rejects its long-form
pacing: routine movements often last only **one or two seconds**. Preserve the
soft relaxed swim and brighter dash; do not redesign acting to fix timing. The
[short-gameplay handoff](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/EXCHANGE_07.txt)
supersedes earlier ten-second choreography for new takes, not their history.

Source-video duration is not the duration of a gameplay action. Author a brief
start, a repeatable core cycle and a short stop. Starting pilot targets are
0.10–0.15s for visible commitment, 0.8–1.2s per relaxed cycle, 0.4–0.6s per dash
cycle and roughly 0.15–0.25s for braking. These are unmeasured design targets,
not approved asset timings. Eye/shoulder intention overlaps the first stroke;
never make movement wait for theatrical preparation. Hair and fin overlap
carry personality during travel. Longer generator clips should contain more
genuine cycles, not slower starts or stretched stops.

The future controller must respond immediately to start/release/arrival,
loop only cruise, and allow release mid-stroke without waiting a whole cycle.
Preserve phase-compatible exits; identify missing exit phases as additional
source work rather than snapping, freezing or morphing a pose. One supplied
stop does not prove arbitrary-phase interruption. Restart and left/right
reversal must not queue a whole clip. Validate 1s, 2s and 5s commanded travel,
mid-stroke release and rapid restart/reversal; report whether the short visual
settle is additional to travel duration. These are future timing demonstrations,
not implemented runtime behavior here. Native cadence, continuity, margins and
the 4.8/owner checkpoint remain required. Exact resting-sprite bridges remain
separate; qualitative motion approval is not fabricated numerical acceptance.

Compact slow A002 and dash A003 originals are on the exchange branch for
[independent Codex review](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/reshoots/reviews/PAIR-COMPACT-20260917/START_HERE.txt).
Producer timing/crop notes are inspection flags, not 4.8 scores or accepted
cuts. Dash A002 remains preserved cropped history. No clip is accepted here.

## The character in one sentence

**Roshan notices with her eyes, decides with her hands, and travels with her
tail; she arrives ready to help.**

She feels like a curious child entirely at home in her world: warm, attentive,
resourceful, and pleased to share a discovery. Her calm is confidence, not
solemnity. Her excitement is a moment of delight, not continuous busyness.
These are acting interpretations for this commission, not new biography,
dialogue, relationships, or story events.

The audience should understand what she wants before the effect appears.
The face establishes attention; the hands make the intention specific; the
tail supplies travel and balance. At the important moment, simplify the
performance so the object, friend, or result can be read.

## Two reference styles, one consistent Roshan

These are original motion analogies. A ribbon suggests trailing rhythm; a
dolphin suggests a brief propulsion pulse followed by glide. Neither supplies
anatomy, skin, locomotion permissions, or a different character design.

| Choice | Ribbon Glide — everyday register | Playful Dolphin — excited register |
|---|---|---|
| Emotional impression | Comfortable, curious, considerate | Eager, affectionate, delighted |
| Main phrase | Look → reach → stroke → glide → arrive | Notice → two compact beats → buoyant glide → settle |
| Energy distribution | One soft effort, generous rest | Two short efforts, then a clear rest |
| Line of action | Long, open curve through the approved body and tail | Briefly gathered pose opening into a lifted chest |
| Head and chest | Head leads slightly; chest follows without a snap | Attention and chest commit nearly together |
| Hands | Relaxed balance; one hand makes intention clear | One open greeting or delighted accent, then hands quiet |
| Tail | Readable sweep resolving into fin follow-through | Two contained tail pulses, not a whole-body bounce |
| Path | Smooth and purposeful | Shallow arc only where the established movement mode permits |
| Arrival | Tail catches up once; hands become useful | One small settle, then attentive stillness |
| Use | Explore, approach, carry, listen, careful work | Discover, greet, begin eagerly, celebrate earned success |
| Avoid | Limp drifting, ceremonial slowness, adult glamour | Frantic pumping, leaps on every input, collision comedy |

Default to Ribbon Glide. Choose Playful Dolphin because a meaningful event
changes Roshan's intention, not because a random timer fires. Fast travel is
not automatically excitement; urgent helping can use a compact, focused glide.
Costumes change available gestures and tools, not her underlying personality.

## The motion grammar

### Attention before ornament

A look has a target: the selected object, the working hand, a speaking friend,
or a changed result. Do not scan the room continuously. For a large direction
change, let the face indicate the new heading before the tail finishes its
turn, while navigation responds immediately. In an authored close performance,
allow a small delay between noticing and reaching; do not add it as input lag.

Give one action one leading idea. A wave need not also include a twirl, hair
flick, tail flourish, bouncing camera, and particle burst. Secondary motion
finishes the same gesture. It does not start an unrelated gesture.

### Propulsion and silhouette

Swim effort travels through the approved torso-to-tail connection toward the
fin. Keep the upper body readable instead of making the whole character snake
sideways. A tail pulse is an authored change in pose, not repeated scaling of
the body. Do not split the tail, add knees or legs, stretch the waist, or change
fin topology to make a difficult pose easier.

Use gentle asymmetry: one hand leads a reach while the other balances; one
shoulder turns toward a friend. Both arms may open for a deliberate greeting.
Avoid permanently mirrored paddling. Preserve the approved hair volume,
facial proportions, costume landmarks and outline weight in every heading.

At gameplay size, maintain enough space between a hand, face, carried object
and tail for their roles to remain clear. Judge the actual rendered silhouette;
an attractive enlarged frame does not establish small-screen readability.

### Weight, buoyancy and support

In swimming contexts, buoyancy supports Roshan while the tail propels her.
Her body can settle without dropping like a stone or springing like rubber.
A heavier-looking object encourages closer hands and quieter turns; it never
creates a punitive carrying slowdown or a new control burden by implication.

Respect the environment's established support. A pool, supported floor pose,
seat, ride, flight sequence and minigame station are different staging cases.
This profile authorizes no new hovering ability, land-walking legs, or swimming
through floors. Preserve approved support/transport for non-swimming scenes;
write the specific extension before animating a missing mode.

### Follow-through, rhythm and stillness

The head and intention settle first; tail and hair resolve once afterward,
where accepted frames support that sequence. A fin may trail a turn but cannot
detach, grow or switch side without a readable transition. Prefer a quiet end
pose over a perpetual rebound.

Vary the timing inside a phrase, not the character's design. Do not give every
key equal duration merely because the atlas is a grid. First prove that the
frames are chronological; pose keys are not temporal in-betweens. Do not
manufacture missing motion by looping unrelated poses or presenting static
translation as a newly animated character.

Idle is a listening state. Let the child inspect the world. Sparse authored
glances or relaxed adjustments may occur only when they do not steal focus
from the current instruction. Avoid constant hair-playing, spinning or cheering.

## Emotional registers

| Intention | Face and attention | Hands and body | Tail/rhythm | Return |
|---|---|---|---|---|
| Curious | Look at one specific thing; small interested tilt | Soft reach, open posture | Ribbon Glide | Arrive and inspect |
| Concentrating | Look at the tool's contact point | Compact useful reach; steady supporting hand | Quieter tail, no decorative bounce | Inspect the result |
| Affectionate | Attend to the friend's face | Inviting open hand; approach without crowding | Soft deceleration | Listen in a shared pose |
| Delighted | Look at discovery, then share it | One chest lift or open gesture | Playful Dolphin accent | Calm available for input |
| Proud | Look at the completed work before looking outward | Small satisfied acknowledgement | Brief contained accent | Return to the world |
| Unsure | Look between target and hand; gentle head tilt | Small reset or inviting palm | Pause the flourish, remain supported | Clear retry cue |
| Concerned/helpful | Attend to the friend or obstacle | Purposeful approach; careful hands | Focused glide, reduced flourish | Reassure through the useful act |
| Surprised | Brief widened attention toward the cause | Small opening, not a violent recoil | One contained accent | Curiosity or helping |

Do not express uncertainty through humiliation, collapse, injury, panic, or
lost progress. No-input idle cannot become a celebration. A reward gesture
acknowledges the actual completed event; it is not evidence of completion.
Do not tie these registers to newly invented fear, hostility, romance or lore.

## Timing and spatial starting points

All values below are **tuning proposals** for the first pilot. The renderer
target remains 30 fps; authored frame cadence and rendered fps are different.
Do not retime an accepted special-purpose clip solely to meet this table.

| Parameter | Initial Ribbon Glide target | Excited-register target | Constraint |
|---|---|---|---|
| Travel phrase | 1.6–2.0 s; roughly half glide | 1.0–1.3 s; two pulses then glide | Tail effort must agree with displacement |
| Start accent | 0.10–0.17 s | 0.10–0.17 s | Overlap immediate travel/response; never wait to move |
| Visible turn | 0.25–0.40 s | 0.20–0.30 s | Follow responsive heading; retarget can interrupt |
| Arrival settle | 0.20–0.35 s | 0.25–0.40 s | Keep gameplay position at valid arrival point |
| Notice/inspection | 0.30–0.60 s when authored | 0.20–0.40 s | Optional acting, not required input latency |
| Greeting | 0.8–1.2 s, one clear wave | 0.8–1.2 s, one open greeting | New input can interrupt |
| Celebration | 0.8–1.2 s | 1.0–1.4 s | Once per valid event; do not queue duplicates |
| Decorative idle excursion | At most about 1% of displayed body height | Return to everyday idle | Pilot ceiling only; anchored work/carry may need zero |

`DL-AGE-07` controls input: visible acknowledgement within two rendered frames
at 30 fps. At 30 fps that is about 67 ms; long acting preparation cannot defer
the response. Never extend an existing no-input delay merely to fit a phrase.

Use normalized measures for comparing performances: body height means crown
to fin tip in the neutral approved view; screen coordinates refer to the
entire frame. Record which measure is used. Decorative offsets are separate
from navigation position and cannot loosen contact or hit-target checks.

For slow travel, reduce effort and allow a longer readable glide. For faster
travel, shorten recovery and increase supported stroke cadence within reviewed
art. Keep speed-to-cycle mapping continuous and bounded. Do not rapidly switch
between unrelated sheets, reset to frame zero on every speed change, or replay
full strokes while stationary. Exact thresholds belong to the implementation
brief after observing existing movement speeds and frame coverage.

## Action vocabulary for implementation

| Action | Preparation and main performance | Contact/payoff | Settle and interruption |
|---|---|---|---|
| Idle/listen | Supported neutral pose; attention available | No task progress | Leave immediately for input or a real event |
| Notice/select | Look and small useful reach toward selected target | Visual selection corresponds to that target | Replace cleanly when target changes |
| Start/travel | Lean into route; tail phrase supports movement | No remote work during travel | Preserve phase where possible; arrive through navigation |
| Turn/reverse | Look toward the new left/right heading; preserve authored stroke phase across the whole-sprite flip | Reflect hand/tool anchors with the same pivot transform | No scale-through-zero squeeze, unreviewed contact jump or front/rear turn requirement |
| Arrive | Become ready to work; quiet the travel rhythm | Enter actual approach/contact range | Do not drift out while playing settle |
| Reach/take | Eyes follow working hand; other hand supports if needed | Attach only at the visible grasp event | If canceled before grasp, object remains in prior state |
| Carry | Hands support object; stable torso, restrained tail | Prop remains at correct anchor through headings | Teardown reconciles ownership; no orphaned prop |
| Place/give | Attend to destination; release visibly | Object changes owner/location at visible release | No teleport from hand to a distant target |
| Scoop | Approach, extend held skimmer, sweep through target | Net/target contact precedes removed debris | Return the held tool, then acknowledge result |
| Wipe/scrub | Face working area, brace/hold appropriately | Brush or cloth traverses the marked surface | Release or retarget without stale progress |
| Lift/help | Look at friend/object, establish appropriate support | Show the authorized release/lift cause | Do not invent a rescue or victory in idle footage |
| Greet | Approach without covering friend; one clear hand gesture | Both faces remain readable | Shared attentive end pose |
| Celebrate | Inspect true result; pleased gesture | Effect/sound describe that same result | Once, interruptible, return to available control |
| Recover/retry | Small reset, kind invitation toward target | Preserve completed work | Resume without shame or punishment |

Each work verb requires its own visible meaning. A collect gesture cannot
stand in for scrubbing a bathtub, supporting Baby Eagle, or using a skimmer
unless the actual contact performance supports that reading. Apply the
[approach protocol](../../audit/stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md)
and `MA-PLAY-004` before judging the flourish.

## Performance with another character or object

Stage a triangle of attention: Roshan, the partner/target, and the important
hand or object. Leave breathing room for faces and contact. Her helping should
make the other character visible, not cover them with hair or a large prop.
Look to the partner when listening; look to the contact point while working;
look at the changed result before sharing satisfaction.

Assign ownership of every prop before and after a handoff. Name who holds it,
which hand/anchor, and the release moment. For two-character contact, bind both
performances to the same contact event; independent loops are insufficient.
Match eyelines, relative scale and screen side across shot cuts. A close-up
may enlarge acting detail without making Roshan more frantic or redesigning
her silhouette. Existing shot topology, camera and costume locks still apply.

## Implementation boundary

Navigation owns position/arrival; gameplay owns valid input, targets, object
state and monotonic saved progress; animation owns visible presentation and
named markers. A marker reports that a pose/time was reached. Gameplay still
validates the current action identity, target, range and cancellation state
before changing the world or awarding progress.

Use the existing architecture. The protocol's clip/state names are semantic
brief fields, not shipped APIs or a commission to build another framework.
Keep world/camera travel separate from decorative offsets; use the accepted
2D Canvas path. Never add 3D bodies, skeletons or model fallbacks.

Optional reactions yield to intentional input. Work interruptions specify
whether cancellation occurs before contact, after contact but before visible
completion, or after an already-saved effect. Reconcile to actual world state;
never undo saved work or award twice. Pause/focus loss freezes or cancels
according to the activity contract, and exit prevents late callbacks. Re-entry
does not replay a success merely because an animation had not finished.

The [production protocol](ANIMATION_PRODUCTION_PROTOCOL.md) owns reusable clip
fields, event tests, review records, dependency invalidation, and delivery lanes.

## Reuse inventory and known limitations

This is source inspection at the baseline above, not a fresh visual acceptance
of any frame. Inventory accepted frames before requesting additional art.

| Existing source | Useful vocabulary | Review before reuse |
|---|---|---|
| [Atlas contract](../../assets/characters/roshan_25d/README.md) and `roshan_directional.png` beside it | Eight historical headings, preserved reference | New gameplay coverage is left/right only; static headings do not prove motion |
| `roshan_swim_front.png`, `roshan_swim_back.png` in that family | Sixteen chronological frames per view | Silhouette, phase, source sampling, actual directional fit |
| `roshan_gesture_a.png` through `roshan_gesture_d.png` | Wave/cheer/clap/twirl; look/giggle/sleep/reach; collect and carry vocabulary | Each verb's meaning, contact and continuity in the target scene |
| `roshan_play_a.png`, `roshan_play_b.png` | Existing supported playground actions | Correct seat/support and scenario; not generic locomotion |
| [Career actor](../../scripts/opera_roshan_actor.gd) and `assets/opera/worlds/actors/animation/` | Career-specific costumes and actions | Exact manifest/semantic review and special pose rules |
| [Sampling](../../scripts/roshan_sprite_frames.gd), [anchors](../../scripts/roshan_sprite_anchors.gd), [loop helper](../../scripts/roshan_sprite_loop.gd) | Existing source windows and playback support | Anchor tables cover directional and front/back swim torso anchors; they do not establish hand/tool sockets for gesture/play rows |

The loop helper's 8 fps base and 12 fps maximum are implementation facts at
the source baseline, not approved artistic targets. Its mixed staging and
transition code is not authority to import those methods into cinematic
delivery. Keep `DL-MOT-09`'s accepted Ballerina pose holds and one-shot curtain
call; the known silhouette jumps prohibit treating that row as ordinary
continuous in-betweens.

The current career actor also holds Geologist and Teacher pose keys. Geologist
uses complete idle pose 3 because cells 0/1 omit the full fin. Preserve these
source-specific selections; verify every live caller rather than assuming
one universal playback policy. They are existing constraints, not new repairs
or a claim that all other career motion has been visually reaccepted here.

Likely **questions to test**, not predeclared asset defects: whether a reusable
right-facing cycle expresses both rhythms and mirrors cleanly; whether reversals are
readable; whether every required work verb has a credible hand/tool contact;
whether carry anchors survive turns. Record the exact failed case before any
new frame commission. Protected book art, family voices and friend portraits
remain unchanged. This task produces no new art or visual-reference packet.

## Pilot and selection protocol

First make two separate ten-second studies using the same approved character,
scale, setting, route and fixed camera. Compare style A and style B without
changing travel distance, total duration, costume or music to favor one.

| Time | Shared beat | What the comparison tests |
|---|---|---|
| 0–1 s | Idle, then notice a familiar friend | Attention without idle noise |
| 1–4 s | Start and travel toward the friend | Tail effort, glide spacing, silhouette |
| 4–5 s | Turn slightly and arrive | Heading continuity and control |
| 5–7 s | Greet once | Warmth and hand readability |
| 7–8.5 s | Small pleased reaction | Character's excited register |
| 8.5–10 s | Return to calm | Settle and readiness for new input |

Next test the chosen working direction on one real job, with before/during/
after contact and a carried-object turn. Include near/far targets, reversal,
interruption before contact, interruption after saved effect, and re-entry.
Use normal playback speed and actual Mobile gameplay size before frame-stepping.
The first study proves style; the second tests whether style survives use.

Record A, B, or A with B reserved for delight as a named candidate selection,
the exact clip hashes, reviewer/date, normal-speed observations, and timing
changes. Owner selection and final acceptance remain separately recorded; do
not prefill them. Routine candidate iteration within this commission proceeds
without a new planning permission round.

### Art review questions

1. Can the viewer tell what caught Roshan's attention before the payoff?
2. Does a still silhouette retain her approved identity throughout the phrase?
3. Does the tail plausibly support the visible travel instead of merely cycling?
4. Are reach, contact, release and result legible as distinct events?
5. Does her manner stay recognizable across travel, greeting and useful work?
6. Does the quieter end invite the child's next action?

Identity/anatomy failure, detached contact, wrong state/cause, hidden objective,
stuck control, or false rewards reject a candidate regardless of charm. Timing
and amplitude targets can be tuned with recorded evidence; those invariants
cannot be waived by a high average score.

## Carry the direction into cinematics

Use the same attention, intention, action, contact and settle grammar in an
authored shot. Cinematic scale permits finer acting, not a different Roshan.
Bind the approved profile/version in the archive sidecar and put only the
needed acting sentence in the generation prompt. Preserve existing camera,
room topology, identity, sound instructions and the shot's true cause/end state.

Example acting sentence: “Roshan notices the friend, turns her gaze toward
them, gives one gentle tail stroke, glides to a stop, and offers one relaxed
wave; her tail settles while her attention stays on the friend.” This is a
brief fragment, not an executable shot card or permission to invent a scene.

The full-frame cinematic rules remain controlling, including complete generated
changed frames, per-frame provenance and human review. Runtime atlas playback,
tweening and procedural movement cannot supply cinematic delivery pixels.
External motion reference, archive completeness, generation readiness and
delivery acceptance retain their separate claims. Follow the current
[continuity protocol](../GROK_HANDOFF_2_CONTINUITY_PROTOCOL_2026-09-09.md)
and the applicable shot-card contract for an actual handoff.
