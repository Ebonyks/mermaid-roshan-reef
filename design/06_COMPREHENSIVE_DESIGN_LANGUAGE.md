# Mermaid Roshan: Reef of Light — comprehensive design language

- **Document ID:** CDL-2026-08-09
- **Status:** `PROPOSED_CANONICAL`; direct owner decisions remain controlling
  while the exhaustive ledger, complete finding records, and documentation gate
  remain open
- **Decision baseline:** owner direction through 2026-08-09
- **Runtime baseline:** exactly Godot 4.7.1-stable, Mobile renderer
- **Authority reconciliation checkpoint:** `9289dd813439d16cc8178e57abcbd332a8e0fe9d`
- **Last synchronized audit commit:** `a3d3bce18dd73d0ac87f2fb4bac397e2b4396180`
- **Current audit state:** `IN_PROGRESS` / `UNSATISFIED`
- **Audience:** one specific non-reading four-year-old, using one finger on a
  three-to-four-year-old Android phone; Lenovo Tab M11 is the performance
  reference

This document consolidates the durable rules from the existing master design
documents, `ART_STYLE_GUIDE.md`, `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md`,
`AUDIT_UPGRADE.md`, the touch/combat/menu/castle/Opera audits, the visual-audit
contract, and the owner's final 2026-08-09 game-wide true-2D decision.

It is intentionally a rulebook, not a claim that the current build already
meets every rule. Current compliance, exceptions, dismissed audit items, and
closure evidence live in `audit/MASTER_AUDIT_2026-08-09.md`.

Commit `9289dd81` reconciled `AGENTS.md`, `CLAUDE.md`, `design/00` through
`design/05`, and the named Roshan authority surface to the owner's final 2D
decision. The ledger is still incomplete across the current 299 tracked
Markdown files, so a direct owner decision and binding operational/security
rules remain higher authority. Where an older art or design document conflicts
with a rule here, the dated supersession table in section 15 controls.

At synchronized code commit `a3d3bce1`, this remains an acceptance target, not
a compliance claim. Exact local full CI is green after 1434.3 seconds with
fresh import, all static gates, GAME2D `NO_REGRESSION`, and all 61 trusted
probes under Godot 4.7.1-stable. Repeated nonfatal invalid-UID fallback warnings
for the retained `sponge_tubes.glb` and `starfish.glb` resources remain open 3D
migration/resource-hygiene debt, so the run is not warning-free or
release-clean. GAME2D is exact but strict-unsatisfied at 509 models, 68
production 3D files, and 77 probe 3D files. Fresh-runtime visual strict is also
unsatisfied at 16 failures, 17 reviews, two manual items, and 86 coverage gaps;
no live Canvas capture output was accepted. Commits `3b7a7e66` and `fea916a8`
are the approved visual-evidence implementation baseline for `DL-QA-11`.

---

## 1. How to use these rules

Every normative rule has a stable ID. Audits, work orders, code comments, and
waivers should cite the ID rather than a mutable line number. A finding without
a cited rule is an observation or proposal, not a design failure.

Normative terms:

- **MUST / MUST NOT** — blocking unless an explicit owner decision supersedes
  the rule.
- **SHOULD / SHOULD NOT** — expected; a deviation needs written evidence and a
  reason.
- **MAY** — permitted, not required.
- **Owner acceptance** — an explicit visual, design, or scope decision; passing
  automation alone never implies it.

Rule precedence:

1. Binding `SECURITY.md`, protected-asset/save rules, credential and filesystem
   safeguards, and release requirements. A content or design decision never
   weakens these boundaries.
2. A direct, dated owner product decision within those boundaries.
3. Exact engine requirements and the remaining current operational rules in
   `AGENTS.md`.
4. This design language.
5. A current domain document explicitly named by this document.
6. Historical audits and work orders, used only as evidence.

`DL-AUTH-01` — A later owner decision supersedes an earlier recommendation,
even if the earlier recommendation remains in a file labelled authoritative.

`DL-AUTH-02` — A finding MUST retain its source and history when superseded,
dismissed, or fixed. Closing a finding does not erase why it existed.

`DL-AUTH-03` — Severity, lifecycle state, and verification level are separate.
A severe finding can be superseded; a low-severity fix can remain unverified.

---

## 2. The child is the primary design constraint

`DL-AGE-01` — The game MUST be understandable to a non-reader. Required
objectives use a short spoken line and a moving visual pointer or equally clear
diegetic cue. Text may support an adult but MUST NOT be the child's only route.

`DL-AGE-02` — The primary interaction grammar is one finger. A child-facing
action MUST NOT require simultaneous controls, precision chords, reading a
control legend, or a separate confirm button after a visible object is chosen.

`DL-AGE-03` — There are no punitive fail states, lives, game-over screens,
lost collectibles, or irreversible wrong choices. A mistake receives kind,
immediate feedback and preserves a route to completion.

`DL-AGE-04` — No input and passive demonstration MUST NOT earn a win. Mercy
widens windows, slows cues, magnetizes targets, demonstrates the correct verb,
or eventually assists the correct action; it does not make mindless tapping the
optimal strategy.

`DL-AGE-05` — Correct, intentional play MUST make progress faster than wrong,
random, passive, or repeated input. Wrong input may sparkle, bounce, or sound
kindly, but uncapped wrong-input payouts are forbidden.

`DL-AGE-06` — Sessions are short. Every entered activity MUST have a kind,
obvious route to start, complete, leave, re-enter, pause, and recover after
focus loss.

`DL-AGE-07` — The child MUST see a visible response within two rendered frames
of a valid touch at the 30 fps target. Response may begin before the full action
finishes.

`DL-AGE-08` — Scary imagery, hostile language, dark threat, predatory teeth or
glare, and punishment are softened into playful, child-scale fantasy.

---

## 3. Final medium decision: a 2D game

`DL-MED-01` — This is a 2D game in both authored medium and runtime structure.
Gameplay uses `Node2D`, `CanvasItem`, `Control`, `Sprite2D`, `TextureRect`,
`Camera2D`, 2D particles, 2D collision where collision is needed, and explicit
2D draw/z ordering. A flat image mounted on a 3D node is migration debt, not a
finished 2D implementation.

`DL-MED-02` — Mermaid Roshan's only approved final representation is the RGBA
atlas/cutout family under `assets/characters/roshan_25d/`, staged through
`Node2D`/`Sprite2D` and explicit 2D ordering. The current player still contains
legacy `Node3D`/`Sprite3D` staging, which is measured migration debt rather than
evidence that this target is complete. Her final animation, costumes, contact,
and occlusion MUST use the 2D canvas path; there is no model, skeleton, rig,
skin-weight, bone-driven costume, or model fallback in the accepted runtime.

`DL-MED-03` — No active project, editor, export, source-master, backup, build
tool, or production-test surface may retain 3D model resources or their import
sidecars. This includes GLB/glTF, Blender and numbered Blender backups, FBX,
OBJ, DAE, 3DS, STL, PLY, USD-family, Alembic, X3D, and equivalent disguised
model binaries. Those resources belong only on the out-of-tree deprecated-
resources branch.

`DL-MED-04` — `Node3D`, `Sprite3D`, `Camera3D`, 3D meshes/materials/lights,
spatial shaders, 3D physics/collision, `Vector3`/`Transform3D` world logic, and
3D scene roots are not accepted implementation scaffolding for the final game.
While conversion is in progress they MUST be recorded as exact shrinking debt,
MUST NOT grow, and MUST be removed one tested gameplay slice at a time.

`DL-MED-05` — Character and world cutouts retain their drawn contours, identity
colors, authored light, and stable pivots. They may receive restrained 2D idle
motion, contact shadow, bubbles, sparkles, and `z_index` occlusion, but MUST NOT
be relit, sculpted, or redesigned to imitate a mesh.

`DL-MED-06` — The 2026-07-19 Meshy migration, every real-3D character or world
work order, the Roshan v2/v3/v4 model hierarchy, and the claim that landed GLBs
remain until a zone migrates are superseded. They are historical evidence, not
paused work and not an approved source of new runtime content.

`DL-MED-07` — The old dimensional rollback requirement does not require a path
back to any 3D mode or 3D-first art direction. General feature flags remain
appropriate for risky behavior changes, but the final 2D medium is not an
experiment waiting to be undone.

`DL-MED-08` — The historically named branch
`codex/deprecated-resources-roshan-20260809`, verified at archive head
`9329d9a6`, is the out-of-tree preservation authority for all retired 3D
resources, not only Roshan. It is historical evidence only, not an alternate
production authority, active fallback, runtime dependency, rollback target, or
merge source. The active game removes each archived resource only after its 2D
replacement or non-reachability proof and surrounding tests are verified.

`DL-MED-09` — `tools/audit_game_2d.py` defines the migration inventory. A green
regression result means only that debt did not grow; it MUST say
`NO_REGRESSION`, never `PASS`. Only the strict zero-debt state may say the game
satisfies the 2D medium contract.

`DL-MED-10` — Current-authority documents and work orders MAY mention 3D only
as exact shrinking transition debt or explicitly labelled historical evidence.
They MUST NOT prescribe `Node3D`, `Sprite3D`, `Camera3D`, models, spatial
shaders, 3D physics, Blender, or Meshy as an accepted final implementation.

---

## 4. Visual promise

The game is Mermaid Roshan's illustrated storybook presented as a pastel toy
playset: soft, rounded, legible, specific, warm, and visibly handmade. Wind
Waker is a rendering reference only; no Zelda asset, symbol, interface, music,
character design, or story language may enter the project.

`DL-VIS-01` — Shape language uses broad rounded masses, slight handmade
asymmetry, and one immediately readable silhouette. Small detail is grouped
into two or three calm clusters rather than distributed evenly.

`DL-VIS-02` — Major contours read as clean deep-indigo, plum, or warm-brown
lines at approximately 2–4 screen pixels at 1280×720; interior marks are
approximately 1–2 pixels. Avoid white sticker rims, scratchy hatching, noisy
speed lines, and photographic edge detail.

`DL-VIS-03` — Values remain high-key. Faces, hands, objective props, and touch
targets MUST NOT collapse into a dark mass. Shadows lean aqua, blue-grey, or
lavender rather than neutral black.

`DL-VIS-04` — Cool water and field colors occupy most of an environment; warm
rainbow color identifies characters, rewards, and actions. Saturation peaks are
small and intentional, never a full-screen neon field.

`DL-VIS-05` — Materials read through a few broad painted value bands and
specific silhouettes, not PBR noise. Matte-to-satin is the default, with wet
accents used selectively.

`DL-VIS-06` — The protected book art is the identity authority. Roshan's face,
rainbow forelock, tail, proportions, and costume motifs MUST remain recognizable
at phone size and across every atlas frame.

`DL-VIS-07` — A visual score of 5/5 requires owner acceptance in runtime
context. Source prestige, successful generation, a clean isolated render, or a
green technical gate cannot grant 5/5 by itself.

`DL-VIS-08` — A global average across source files is not evidence that a
rendered gameplay state has a palette or figure/ground defect when it equally
weights mutually exclusive states, decorative files, or art absent from that
frame and ignores compositing, HUD, viewport, and device presentation. Do not
recolor or regenerate approved art merely to satisfy that metric. First measure
the true state-local Canvas composite and review it in runtime and on device.

`DL-VIS-09` — When an accepted frame-animated 2D counterpart exists for a
gameplay character, an older vinyl/sticker card MUST NOT remain that activity's
active actor unless the activity is explicitly a sticker-book interface. Trees,
bushes, and other environment art in the same activity meet the surrounding
game's silhouette, contour, value, and phone-readability quality; preview drafts
do not become production merely because they are already imported.

---

## 5. Composition and child-readable hierarchy

`DL-READ-01` — Backgrounds frame play; they do not compete with the thing a
finger should find. The playable band SHOULD be lower in saturation and detail
than characters and touch targets, with a measurable figure/ground value or
color separation.

`DL-READ-02` — Every interactive object MUST remain identifiable in a phone-size
squint test with the HUD present. Full-resolution desktop inspection is
insufficient.

`DL-READ-03` — A frame has one primary focal action, one supporting context,
and quiet peripheral dressing. Multiple equally bright objectives are a
hierarchy defect.

`DL-READ-04` — World art MUST NOT contain required words, letters, or digits.
Decorative marks that resemble text are rejected if a child can reasonably
read them as an instruction.

`DL-READ-05` — Roshan MUST remain visible during play. Enemies, widget cards,
foreground cards, particles, and overlays MUST NOT fully cover her face and
body during an action that depends on locating her.

`DL-READ-06` — A pointer points at the live actionable object or location, not a
generic screen corner, stale coordinate, decorative duplicate, or passive demo.

---

## 6. 2D canvas living-card world construction

`DL-LAY-01` — World raster art uses unshaded `Sprite2D`/canvas cards at
intentional `z_index` and 2D parallax layers. Background, playable cards, and
foreground framing have named ordering roles. A `Sprite3D` card is transition
debt under `DL-MED-04`, not an accepted implementation of this rule.

`DL-LAY-02` — A panning promenade MUST use at least two independently staged
background layers; the target language is four to five depth classes where the
transparent-overdraw budget permits. Side-by-side tiles from one panorama count
as one layer.

`DL-LAY-03` — Anything Roshan can tap, approach, pass, or stand behind is an
independent owned card, not a painted mural object pretending to be interactive.

`DL-LAY-04` — Occlusion is validated per relevant card. It is not sufficient
for one depth constant in a stage to overlap the walk band while all important
playground or interaction cards remain permanently behind Roshan.

`DL-LAY-05` — An extracted object owns its source pixels exactly once. Remove
the object from the background, heal the background, and reinsert the same
approved object as one 2D card at the correct `z_index`. Never place a sticker
over a second painted copy.

`DL-LAY-06` — A readable object crossing a generated background-tile boundary
MUST NOT be independently regenerated in each tile. Extract it, heal the joined
master, and stage it once at an intentional 2D `z_index`/parallax layer.

`DL-LAY-07` — Multi-screen background resolution is measured per playable
screen. Each screen requires at least 2048×2048 native coverage; a three-screen
horizontal master therefore requires at least 6144×2048 and is reconstructed
as non-overlapping 1024×1024 `Sprite2D` cards without seams.

`DL-LAY-08` — Foreground occluders are sparse physical framing. They MUST NOT
carry broad opaque wall, floor, water, or architecture pixels that hide Roshan.

`DL-LAY-09` — Fixed-camera canvas activities are exempt from promenade
parallax, but not from hierarchy, ownership, cutoff, touch-target, or
figure/ground rules.

---

## 7. Interactions change the world truthfully

`DL-INT-01` — A touch target belongs to the visible object it affects. Invisible
or overlapping controls MUST NOT steal input from a different visible object.

`DL-INT-02` — Meaningful interaction changes a truthful part or state of the
object: a door opens, water pours, a cushion compresses, a lamp lights, a toy
moves as that toy. Generic whole-card bounce, spin, hover, or detached sparkle
is feedback, not the authored action.

`DL-INT-03` — Authored object animation uses 4–12 coherent states where that
contract applies, a stable pivot, fixed ownership, and a clear return or resting
state. Runtime MUST NOT interpolate a broken identity or synthesize missing
contact frames.

`DL-INT-04` — Touch coordinates, visual sockets, collision/selection regions,
and authored object positions MUST share one coordinate transform at every
supported aspect ratio.

`DL-INT-05` — A child can repair a wrong plan. Puzzle pieces are conserved,
liftable or resettable, and cannot duplicate, disappear, or make a round
unrecoverable.

`DL-INT-06` — A demonstration may show a verb but MUST NOT collect, score,
damage, solve, or cross the final completion threshold.

---

## 8. Touch and interface grammar

`DL-UI-01` — Touch-the-world is primary: tap travels or acts; hold follows or
charges when explicitly taught; drag manipulates an object only when the
fiction visibly calls for manipulation.

`DL-UI-02` — The virtual stick, keyboard, gamepad, and accessibility controls
may remain as fallbacks. A visible movement pad is not the primary child-facing
curriculum and MUST NOT silently own a screen region while hidden.

`DL-UI-03` — Required child-facing touch targets SHOULD be at least 110×110
base-canvas pixels or provide an equivalently generous projected hit region,
with separation sufficient to prevent neighboring actions from competing.

`DL-UI-04` — One touch owns one route for its lifetime. A second finger cannot
steal a held action, and motion beyond a threshold cannot retroactively turn a
different control's press into movement.

`DL-UI-05` — Focus loss, pause, back navigation, overlay close, and activity
teardown cancel held input. Cancellation MUST NOT release a charge, deal
damage, confirm a choice, or continue a stale callback.

`DL-UI-06` — Picture-first cards use a shared Storybook UI grammar: paper or
shell surfaces, violet/navy hierarchy, large direct choices, visible
pressed/focus state, and one neutral way back.

`DL-UI-07` — Child-facing HUD copy is short and supplemental. Persistent report
cards, sentence objectives, raw debug controls, and unexplained mode choices do
not belong on the child's play surface.

---

## 9. Motion, acting, feedback, and rewards

`DL-MOT-01` — Every animation preserves identity, anatomy, topology, costume,
outline language, and stable contact. Cropped hair, detached body parts, ghost
neighbors, pose snaps, or shifting pivots fail even when the timing is smooth.

`DL-MOT-02` — Atlas changes require measured cell bounds, anchor tables, and an
engine-side sampling assertion. A mathematically correct source window is not
accepted until the runtime node is proven to sample it correctly.

`DL-MOT-03` — Motion follows anticipation → readable action → contact/payoff →
settle. Avoid continuous idle noise that competes with objectives.

`DL-MOT-04` — Feedback is redundant but coherent: visual change, sound, and
optional haptic all describe the same event. Effects do not obscure the action
they celebrate.

`DL-MOT-05` — Rewards preserve agency. Stars, medals, applause, and celebration
are earned by an intentional or explicitly assisted correct action, never by
zero input or a stale timer.

`DL-MOT-06` — Camera motion is gentle, predictable, and subordinate to the
action. Avoid abrupt lens yaw, pose/camera disagreement, and framing that loses
the active object or Roshan.

`DL-MOT-07` — If a character is described as animated, the runtime MUST visibly
advance accepted authored frames or equivalent approved 2D states. Translating,
scaling, rotating, fading, or wobbling one static sticker is feedback motion,
not a fully animated character replacement. Hide/peek/reveal sequences also
MUST preserve opacity and framing so an actor cannot leak or clip before the
authored reveal.

---

## 10. Voice, music, and non-reader communication

`DL-SND-01` — Every required objective has an exact spoken cue. A generic cheer,
wrong legacy noun, missing recording, or adult-readable caption is not a
complete substitute.

`DL-SND-02` — Captions remain useful for the accompanying adult and for missing
audio diagnosis, but gameplay MUST remain independently understandable to the
child.

`DL-SND-03` — Voice identity remains consistent by speaker. Dialogue queues are
touch-skippable, clear on teardown, and never drain into the next location.

`DL-SND-04` — Music ducks under speech; success, miss, danger-play, and
transition sounds have consistent loudness and meaning across activities.

`DL-SND-05` — Protected family recordings under `assets/audio/voices/` are
irreplaceable. Do not modify, recompress destructively, or substitute them
without explicit owner authorization.

---

## 11. Cinematic exception

`DL-CIN-01` — Authored cinematic delivery frames are complete flattened images
in the current approved polished 2D storybook generation style. This complete
contract incorporates the binding `AGENTS.md` cinematic rules without
relaxation; a short summary elsewhere cannot narrow it. For a defective
cinematic frame, full-frame regeneration supersedes the general art-reuse
budget and cannot be avoided by substituting another production technique.

`DL-CIN-02` — A failed action frame is regenerated at its exact timeline index.
Keep an existing frame only when that exact frame passes. Each replacement uses
the direction brief, continuity data, character/object references, and accepted
adjacent full frames; neighboring pixels are never blended into delivery.

`DL-CIN-03` — Final or review delivery MUST NOT use tweening, morphing, optical
flow or motion interpolation, cross-dissolve, sprite/cutout animation,
chroma-key compositing, skeletal/rig animation, procedural warping, translating
a static layer or camera, or duplicated frames to conceal missing action.

`DL-CIN-04` — An intentional hold is allowed only when the direction brief
calls for stillness and the manifest records the held span and its narrative
purpose. A hold cannot replace motion, acting, contact, or camera action. Every
changed action-span frame is an individually generated and accepted full frame.

`DL-CIN-05` — After acceptance, production may normalize resolution, pad,
convert pixel format, or encode only by applying the same whole-canvas transform
to the complete flattened frame. Preserve the native generation and hash.
Normalization cannot isolate, translate, warp, mask, resize, or otherwise repair
a subject or compensate for failed motion; audit motion in normalized
coordinates before the production transform.

`DL-CIN-06` — The final medium remains the established polished 2D storybook
full-frame generation. Cinematics cannot switch to 3D, sprites, vector or
procedural animation, or another medium to make production easier.

`DL-CIN-07` — A disposable position guide is the sole sprite/chroma exception
and may be created only to show the generator where an object belongs. It may
communicate normalized position, bounding box, scale, and orientation. It has
no authority over design, anatomy, topology, style, lighting, texture, shading,
background, or final pixels.

`DL-CIN-08` — A generator-facing position guide places its flat chroma footprint
and coordinate marks on a neutral field. It contains no scene plate, accepted
background, texture, or appearance-bearing pixels. A neutral-field crosshair
guide with no subject footprint is not presumed superior: the 2026-07-29
opening-plane trial materially overshot. A neutral-field bounding-box guide is
also experimental: one nearer result was followed by scale growth, stalls,
reversals, and overshoots. Every guide mode must earn measured full-frame
acceptance without relaxed gates.

`DL-CIN-09` — Every guide prompt labels the input `POSITION_GUIDE_ONLY` and says
all appearance comes from approved image/style references. No guide pixel may
be copied, composited, keyed, traced, or inserted into delivery. The generator
returns a new complete frame, and that full frame passes the normal audit.

`DL-CIN-10` — Guides stay under an ignored review/build path, never runtime
`assets/`, and never count as production art or accepted keyframes. The manifest
records guide path and hash, `role: "position_only"`, and
`used_as_delivery_pixels: false`.

`DL-CIN-11` — Every regenerated-frame record includes timeline index, full-frame
candidate path and hash, accepted neighboring reference paths and hashes,
prompt hash, attempt number, generation method, declared action/hold state,
subject geometry, any position-guide metadata, and human identity/topology/
style review.

`DL-CIN-12` — `tools/audit_cinematic.py` is blocking. Missing provenance,
forbidden methods, guide-pixel reuse, unreviewed identity, position drift, or a
failed neighboring-frame comparison is a hard failure. A smooth metric cannot
override a failed frame. Production delivery is native 1280×720 landscape with
square pixels, zero rotation metadata, and a 16:9 displayed canvas. Candidates
and neighboring references have delivery orientation/aspect even when pixel
dimensions match; equal-sized wrong-aspect inputs are invalid evidence.

---

## 12. Mobile performance and asset discipline

`DL-PERF-01` — Mobile rendering is authoritative on every platform. The base
canvas is 1280×720, landscape, `canvas_items`/`expand`.

`DL-PERF-02` — The Speedy tier is the default. Normal play targets stable
30 fps: P95 frame time ≤33.3 ms, P99 ≤50 ms, no normal-path hitch over 100 ms,
and no low-memory or thermal kill in a 30-minute target-device session.

`DL-PERF-03` — Transparent overdraw, 2D particles/lights, runtime material
creation, and large decoded textures are hard mobile costs. No large
transparent family or new dynamic 2D light ships without a measured Speedy
cull/budget path. 3D lights are prohibited by `DL-MED-04`.

`DL-PERF-04` — New textures are no more than 1024 pixels on the longest side or
are power-of-two. VRAM compression is used only where legal and where visual or
pixel-contract review accepts it. NPOT plus VRAM compression is forbidden due
to the known importer deadlock.

`DL-PERF-05` — New audio is OGG; music is at least 64 kbps and loop-tagged.

`DL-PERF-06` — Superseded runtime art is removed from export once references,
provenance, rollback needs, and probes prove it is safe. An orphan warning is
not permission for blind deletion.

`DL-PERF-07` — APK size, decoded texture memory, and runtime GPU memory are
separate metrics. Optimize the measured bottleneck and record the tradeoff; do
not claim a disk reduction from a memory-only conversion.

---

## 13. Save, lifecycle, and release safety

`DL-SAVE-01` — Never remove a key from `reef_save.json`. Add keys with defaults,
preserve unknown fields, and migrate legacy aliases forward without losing
progress.

`DL-SAVE-02` — Save writes remain recoverable and preserve the `.bak` path.
Focus loss, pause, and activity exits flush safely without triggering gameplay.

`DL-SAVE-03` — Every activity owns its callbacks, tweens, timers, audio queue,
touch ownership, and temporary nodes. Leaving or suspending it cancels them
before another world becomes active.

`DL-SAVE-04` — An activity acceptance path includes enter → understand → act →
complete → reward → leave → return → re-enter, plus pause/focus-loss and save/
load at meaningful intermediate states.

`DL-SAVE-05` — A release requires exact Godot 4.7.1-stable analysis/import,
trusted probes at the exact commit, save-upgrade evidence, matching APK hash,
and device acceptance. A local green run does not authorize bypassing the
dev-to-master promotion workflow.

---

## 14. Art sourcing, reuse, and provenance

`DL-ASSET-01` — Inventory approved repository art and source masters before
generating or commissioning anything. Reuse, shared components, and
non-destructive derivatives are preferred when they meet identity, readability,
licensing, performance, and purpose.

`DL-ASSET-02` — Generate new art only for a named gap. Record why reuse failed,
the exact prompt/reference/provenance, accepted/rejected candidates, hashes,
and modifications.

`DL-ASSET-03` — Never modify, destructively recompress, or substitute files in
`assets/book/`, `assets/audio/voices/`, or `assets/characters/friends/` without
explicit authorization.

`DL-ASSET-04` — Every new asset receives an `ASSET_LICENSES.md` entry in the
same commit. Retired assets retain historical provenance even when delivery
pixels leave the active tree.

`DL-ASSET-05` — Rejected generations and source-review material stay outside
runtime `assets/` and cannot be counted as shipped art.

`DL-ASSET-06` — Approved art is not regenerated for novelty, stylistic
exploration, or preference. Identity stability outranks variety during
finalization.

`DL-ASSET-07` — Moving retired 3D resources out of the active project preserves
the exact archived bytes, paths, hashes, license/provenance history, and archive
commit. Protected originals are never modified. Archive preservation does not
create a runtime fallback, rollback requirement, or permission to merge those
resources back into the active game.

---

## 15. Explicitly superseded, dismissed, and deferred ideas

These states prevent an old recommendation from silently becoming a new bug.

| Prior idea | Current state | Controlling rule/reason |
|---|---|---|
| Rigged/modelled Roshan; v2/v3/v4 GLB fallback hierarchy | **SUPERSEDED** | Removed from the active project under `DL-MED-01` through `DL-MED-06`; owner 2026-08-09 |
| Gen2 Meshy migration for Roshan, the character roster, or any world zone as current direction | **SUPERSEDED**, not paused | Final game-wide 2D medium |
| `Node3D`, `Sprite3D`, `Camera3D`, meshes, spatial shaders, or 3D physics as the final staging language | **SUPERSEDED** | They are measured transition debt only under `DL-MED-01` and `DL-MED-04` |
| Keep a landed character GLB as a fallback until its zone migrates | **SUPERSEDED** | The archive preserves history; active runtime fallback is forbidden by `DL-MED-02`, `DL-MED-06`, and `DL-MED-08` |
| Restore a dimensional rollback to any 3D mode | **DISMISSED_NOT_IN_PROJECT** | `DL-MED-07` |
| Reuse or merge `codex/deprecated-resources-roshan-20260809` into the active game | **DISMISSED_NOT_IN_PROJECT** | Archive branch is historical evidence only under `DL-MED-08` |
| Meshy keys, Blender/Blender-backup sources, Jolt standees, or physical-prop fleets as active production dependencies | **DISMISSED_NOT_IN_PROJECT** | Those dependencies must become archive-only under `DL-MED-03`, `DL-MED-04`, and `DL-MED-08`; reachable instances remain measured migration debt until retired |
| Gabby content | **DISMISSED_NOT_IN_PROJECT** | IP hold; preserve only under `attic/gabby/`; do not reintroduce without owner-approved redesign |
| Sparkle guide-fish implementation | **DISMISSED_NOT_IN_PROJECT** | Current wayfinding uses landmarks, voice, pointers, and helping-current behavior; the underlying wayfinding need remains valid |
| Visible virtual stick as the primary curriculum | **SUPERSEDED** | Direct touch is primary; stick is fallback under `DL-UI-01` and `DL-UI-02` |
| Whole-card bounce/spin as an object's meaningful action | **DISMISSED_NOT_IN_PROJECT** | It is not an approved interaction solution under `DL-INT-02` |
| Use Seek's vinyl `characters/stickers/pearl_friend.png` pair card or `assets/mg/k_bush2.png` preview art in place of the accepted animated activity | **SUPERSEDED for Seek** | `DL-VIS-09` and `DL-MOT-07`; `8fa90111`/`27bda85d` provide the accepted animated Evie/Lamb-a' actors and high-grade tree cards. Protected/reference originals remain untouched and are not globally reclassified by this bounded runtime decision. |
| Build new 3D construction before or after approved 2D direction | **DISMISSED_NOT_IN_PROJECT** | Final 2D medium; migration work only removes measured debt |
| 3D Opera, companion, path, or `Curve3D` presentation as a retained fallback | **SUPERSEDED** | The 3D prescriptions are superseded; any currently reachable companion/path/Opera implementation remains measured migration debt until a tested 2D replacement owns it |
| Cinematic tween/morph/interpolation shortcuts or portrait/rotated delivery | **DISMISSED_NOT_IN_PROJECT** | `DL-CIN-01` through `DL-CIN-12` |
| Repack Roshan into a smaller runtime atlas during the migration audit | **DEFERRED_WITH_REASON** | It may be a later measured optimization; it is not required to prove true 2D and must not risk protected pixels or identity |
| Add bone-driven or per-costume runtime costume layers to replace the current atlas | **DISMISSED_NOT_A_DEFECT** | The owner chose the approved 2D atlas family; absent costume layering is not a current bug |
| New Chapter 2 plot, daily rhythm, naming, gifting, tending, decorating, additional minigames | **DEFERRED_WITH_REASON** | Design proposals, not current defects; existing-game golden path, device evidence, and confirmed defects come first |
| Dungeon lock-and-key redesign and Zelda-grammar verb roadmap | **DEFERRED_WITH_REASON** | Design proposals, not current defects; no implementation authorization implied |
| Sky Lagoon's historical out-of-order migration | **DISMISSED_NOT_A_DEFECT** | It is not a current product defect and cannot be repaired retroactively; retain only as a process lesson |

---

## 16. Acceptance and audit contract

No feature, art pass, or master audit is accepted from one kind of evidence.

`DL-QA-01` — Static analysis proves files, references, dimensions, hashes, and
source rules. It does not prove runtime presentation.

`DL-QA-02` — Automated probes exercise real state transitions and negative
controls. A probe that writes state directly around the interaction it claims
to test is diagnostic, not closure evidence.

`DL-QA-03` — Runtime capture proves composition, cutoff, coordinate alignment,
animation, hierarchy, and visible feedback at supported aspect ratios only when
its provenance and state transition are bound to the audited build. An image or
facts file detached from that runtime may guide review but cannot prove it.

`DL-QA-04` — Target-device evidence proves frame pacing, latency, thermal/memory
behavior, touch geometry, audio audibility, and the phone-size squint test.

`DL-QA-05` — Observed child evidence proves comprehension, discoverability,
comfort, agency, session length, and absence of adult verbal instruction.

`DL-QA-06` — Owner review decides identity, style, narrative intent, protected
art treatment, and whether a deliberate exception is acceptable.

`DL-QA-07` — `SKIP`, `MANUAL`, missing capture, absent device evidence, or a
waiver is never silently converted into PASS. State the gap and its owner.

`DL-QA-08` — A waiver names the exact rule and scope, reason, owner, date,
expiry/review trigger, and residual child risk. A global “known issue” is not a
waiver.

`DL-QA-09` — The game-wide true-2D contract is satisfied only when
`tools/audit_game_2d.py --strict` reports an exact manifest with no findings and
zero in every reported category: `model_files`, `model_scan_coverage_files`,
`active_export_model_files`, `model_import_sidecars`,
`active_untracked_model_import_sidecars`, `model_archive_files`,
`production_3d_files`, `probe_3d_files`, `scene_3d_files`,
`configuration_3d_files`, and `archive_now_model_files`. Archive hashes,
provenance, dependency proofs, and shrink-only history must also remain valid.
A default-mode exit zero means only that the inventory is exact;
`NO_REGRESSION`, a shrinking count, a green sub-slice probe, or an archive
branch alone is not completion.

`DL-QA-10` — Master-audit satisfaction requires:

1. the strict zero-debt true-2D contract in `DL-QA-09` is satisfied;
2. no P0/P1 finding remains in an unresolved lifecycle:
   `REPORTED_UNCONFIRMED`, `CONFIRMED_OPEN`, `IN_PROGRESS`,
   `FIXED_PENDING_VERIFICATION`, `REGRESSED`, `OWNER_DECISION_REQUIRED`,
   `BLOCKED_EXTERNAL`, or `DEFERRED_WITH_REASON`; a P0/P1 waiver also blocks
   satisfaction unless the owner explicitly accepts its residual risk for this
   exact audit round, and a duplicate is resolved only when its canonical owner
   is resolved;
3. every P2/P3 finding is `VERIFIED_FIXED`, explicitly deferred, waived,
   dismissed, superseded, or a duplicate whose canonical owner is resolved,
   with evidence;
4. exact Godot 4.7.1-stable import/analyzer and all trusted probes green at the
   audited commit;
5. all applicable visual/runtime checks run under `DL-QA-11`, with no
   unresolved failure/review/manual/coverage gap;
6. target-device performance and touch gates met;
7. an observed five-minute golden-path child session completed without adult
   verbal instruction, reading, trapped state, accidental reward, lost
   progress, obvious presentation break, or frame-time breach; and
8. a clean re-audit after repairs finds no new P0/P1 issue.

`DL-QA-11` — Authoritative visual-runtime PASS requires the approved
same-process `--fresh-runtime` contract: a new random one-use challenge, exact
Godot 4.7.1-stable/Mobile/1280×720/stretch binding, clean current Git and full
active source dependency closure, implemented closed state transition, and
immutable visible/hidden/restored capture bytes tied to unique live Canvas
targets. The verifier independently checks decoded layer identity,
source-projected target shape, alpha-aware coverage/occlusion, effective draw
order, and real touch reach. Saved JSON/PNGs, manual facts, copied or re-encoded
layers, renewed hashes, presentation labels, and stale captures are diagnostic
only: they MUST NOT grant PASS, suppress a static risk, or replace missing live
evidence. Active 3D or unresolved dynamic/native reachability is `FAIL` or
`COVERAGE_GAP`, never accepted Canvas evidence. Any absent/invalid challenge,
capture, adapter, source binding, or target proof fails closed, and every such
gap blocks strict satisfaction.

---

## 17. Finding record fields

Every master-audit finding uses these fields:

An abbreviated triage-index row is an audit item, not a canonical finding
record. It may be called a finding only after a stable linked record contains
every field below; unknown values are written explicitly as missing or blocked,
never omitted.

| Field | Requirement |
|---|---|
| `id` | Stable identifier; never reused |
| `title` | One falsifiable problem statement |
| `rule_ids` | One or more rules from this document |
| `domain` / `zone` | Affected system and player-visible location |
| `source` | Audit/report/owner observation that raised it |
| `severity` | P0, P1, P2, or P3 |
| `lifecycle` | One exact value from master-audit section 2.2: `REPORTED_UNCONFIRMED`, `CONFIRMED_OPEN`, `IN_PROGRESS`, `FIXED_PENDING_VERIFICATION`, `VERIFIED_FIXED`, `REGRESSED`, `OWNER_DECISION_REQUIRED`, `BLOCKED_EXTERNAL`, `DEFERRED_WITH_REASON`, `WAIVED_WITH_REASON`, `DISMISSED_NOT_A_DEFECT`, `DISMISSED_NOT_IN_PROJECT`, `SUPERSEDED`, or `DUPLICATE` |
| `verification` | Highest completed evidence level |
| `reproduction` | Exact action, state, aspect ratio, and build |
| `child_impact` | Why it matters to this player |
| `evidence` | Paths, lines, assets, hashes, captures, logs, and device |
| `owner_decision` | Required when intent/scope controls the result |
| `fix` | Minimal intervention and affected files |
| `surrounding_tests` | Positive, negative, save/re-entry, and adjacent-system checks |
| `acceptance` | Observable conditions and required verification levels for closure |
| `closure` | Evidence actually executed: exact command, capture, device/session record, result, commit, and date |
| `relationships` | Duplicate, supersedes, superseded-by, or regression-of IDs |
| `history` | Timestamped state changes; never rewritten away |

The audit-cycle and finding-state vocabularies are defined in
`audit/MASTER_AUDIT_2026-08-09.md` section 2.2 and apply to every subsequent
audit round.
