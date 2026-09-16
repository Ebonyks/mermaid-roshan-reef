# Permanent Grok animation handoff profile

Status: `BINDING_DOMAIN`. Owner decision, 2026-09-15: identify the highest-value
animation jobs, use very short clips at Grok's minimum length, deliver through
GitHub, and preserve this workflow as project memory for future animation work.
This governs external Grok motion studies throughout the project, beginning
with Sky Lagoon. It does not replace individual character movement profiles.

## Default workflow

1. Inventory approved source art and current layers. Preserve their shapes,
   palette, geography, camera and contact points. Fix dirty masks or missing
   background surfaces before asking a generator to move them.
2. Spend external generation on difficult material motion, organic articulation
   and genuinely missing action states. Keep color grading, simple transforms,
   touch hit regions, ripples, feedback timing, navigation and saves in Godot.
3. One clip equals one isolated visible action. Default to a locked camera,
   one moving subject/material and a specific starting and ending state.
   No multi-shot movies, camera tours, simultaneous decorative motion or
   whole-world redraws. Separate water surface motion from shoreline contact.
4. Use the shortest duration the selected Grok surface/model actually permits.
   On 2026-09-15 xAI's official generation documentation specifies **1–15 s**;
   the default API micro-study is therefore **1 s**. A GitHub handoff is a
   delivery method, not a generator interface, and does not establish the UI
   minimum. Record the operator's actual interface, model, shortest offered
   duration and observation date before generation. Never silently choose a
   longer setting or stretch a one-second action into slow motion.
5. If the UI cannot generate one second, choose its shortest available setting.
   Use the matching timeline variant. Optional six-second cards in the Sky
   packet are conditional fallbacks, not a claim that six seconds is universal.
   Do not extend clips or add unrelated action to fill time. A declared quiet
   end hold in a motion study can occupy unavoidable remaining time.
6. Build a self-contained packet under versioned `assets_src/cinematics/`:
   actual source images, one shot card and prompt per job, an inspectable beat
   board, source roles/dimensions/hashes/provenance and runtime seam notes.
   Keep archive metadata out of paste-ready prompts. End every prompt with
   `Sound:`; default these visual studies to silence and retain project audio.
7. Commit and push to a durable project branch. Verify the immutable GitHub
   manifest and every image. Provide commit/tree and direct manifest links.
   The remote-verification sidecar is a later record pointing to that content
   commit; never invent a future self-referential commit hash.
8. Keep `ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` separate.
   Source-art approval does not automatically accept a new crop, binding,
   generated action or repaired scene. Draft cards may be fully archived while
   their per-shot review remains pending. Do not generate merely to fill a quota.

Use [the shot-card template](../templates/IMAGINE_SHOT_CARD_V1.md). One-second
micro-studies supersede its previous two-second minimum under this owner
decision. Longer existing accepted cards are historical, not orders to remake
them. The existing eight-second project shot-card ceiling is retained. If a
future interface minimum exceeds that ceiling, revise the documented profile
and validator together before issuing its packet. Every substantive source or
scope change gets a new packet version.

## Source and output boundaries

Bind two to four images, each with one job: clean first-frame/layout, subject,
material, or grade. Never feed the beat board, annotations, HUD captures or a
second conflicting world layout as first-frame pixels. Preserve native aspect;
make an intentional source crop instead of stretching a square scene to 16:9.
Record crop coordinates and native dimensions; enlargement is not native detail.

Grok interface capability must be checked: a single-image I2V endpoint receives
IMAGE_1 only, with other identity/material images retained as operator review
references. A multi-reference endpoint may bind the full declared set if it
also preserves the first-frame contract. Do not fabricate unsupported API
parameters or claim a start-frame lock from a reference-only mode.

Grok output remains motion/editorial reference under the existing full-frame
cinematic evidence contract. Nothing here authorizes direct video-to-atlas,
loop interpolation, composited cinematic delivery or automatic acceptance.
Any eventual runtime texture/animation integration gets its own source and
delivery disposition, masks, contact/occlusion checks and Mobile/device gates.

## Sky Lagoon priority and division of work

| Order | External micro-study | Why it merits Grok | Keep local |
|---|---|---|---|
| 1 | Painted water-surface highlight cycle | Current brightness shimmer lacks coherent material flow across a large visible area | Water mask, fixed shoreline, tiling/seams, time/phase and touch ripples |
| 2 | One gentle lap against shoreline stones | Believable contact makes the lake feel grounded | Stone silhouettes, rope/bridge geometry and occlusion |
| 3 | One large plant's leaf/stem flex and settle | Whole-card bending cannot articulate leaves independently | Root anchors, layer separation, low-cost runtime response |
| 4 | Castle double-door opening a small crack | Reveals hinge behavior and missing interior state | Door approach, collision, trigger, transition, saves and sound |

Defer castle reflection to a second packet after its exact grounded composition
and reflection footprint are accepted. Defer clouds until hidden background
repairs are clean. Skip stained-glass pulses, sparkles and camera parallax as
Grok jobs; they are inexpensive, controllable Godot work. Preserve Meadow.

## Review and budget

First batch: four independent one-second studies, one candidate each, water
first. Review water before spending on the other jobs. No blind retries;
if a clip fails, name one defect and rerun only that job. For each accepted
motion reference record actual duration, native fps/resolution, model, prompt,
input/output hashes, used bindings, reviewer and decision.

Check first/middle/last and every changed frame at full resolution: camera
locked; unchanged object count, topology and contact; no hue pumping, neon
highlights, photoreal water, melted leaves, floating roots, moving stonework,
door-handle duplication or changes to the stained-glass portrait. Inspect a
claimed loop across its join; similarity is not a guarantee of seamless looping.
Do not fix failed movement with interpolation or claim that a passing numerical
score replaces human visual review.

The source for the duration range is [xAI video generation documentation](https://docs.x.ai/developers/model-capabilities/video/generation#duration),
checked 2026-09-15. Recheck capabilities when a future handoff is prepared.
