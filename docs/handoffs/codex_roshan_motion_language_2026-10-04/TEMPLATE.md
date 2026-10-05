# Roshan animation template — V1

**Status:** `PROPOSED / CANDIDATE` template, 2026-10-04, written by Claude at
the owner's direction. Codex runs it; the owner accepts motion. It becomes the
standing template for every future Roshan animation after the Phase A test
animations validate it (README package RM4).

**What it does:** for any scene in the game, analyse the context and every
interaction Roshan takes part in, decide for each one whether an animation
should be generated, and hand it to the right model with a complete card.

## 0. Owner direction this template implements (2026-10-04)

- "The final goal of this is to provide a template for developing all future
  animations for roshan, based on the game and context. The handoff should
  analyze the scene and interactions with mermaid roshan, determine if an
  animation should be generated, and hand it off to the appropriate model if so."
- Production: "The actual workflow will be through ltx locally, through a
  script run by codex, transferring frames through aesprite for ingame use."
- Grok handoffs and shot cards "are not final references, but test documents
  that will be used in the process of forming our final animation, and will be
  digested to examine our workflow."
- Scope: "our role is to make a rich, comprehensive set of animations for
  mermaid roshan. Once we develop our test animations, workflow and style, we
  will be analyzing every room, every game, to derermine what animations are
  right and wrong, and polish/refine overall product."
- Orientation: "sprites don't need a up/down orientation, only left/right."
- Sky Lagoon: "Swimming still, different animation than in sea though,
  slower, more modest travel."

Quotes keep the owner's spelling. The three phases are therefore **A** test
animations, workflow and style; **B** every room and game analysed with this
template; **C** polish.

## 1. The pipeline

```text
scene sheet ──► interaction table ──► decision per interaction
                                         │
      ┌──────────────┬───────────────────┼──────────────────┬──────────────┐
    NONE        CINEMATIC         REUSE / CODE_FIX     VARIANT / GENERATE   KEYS_THEN_GENERATE
  (no Roshan   (story clip      (Godot integration    (LTX locally via     (ImageGen for the
   animation)   lane, gates)      or fix, probes)      Codex's runner)      named missing keys,
                                                              │              then LTX)
                                                              ▼
                                    Aseprite: transfer, clean, register, time, tag,
                                    sockets, lossless atlas + JSON, round-trip check
                                                              ▼
                                    Godot Canvas sprite: playback, events owned by
                                    gameplay, mirror for left, per-scene residency
                                                              ▼
                                    review: machine checks, owner at normal speed on
                                    the tablet, device budget ──► accept or iterate
```

Test lane: Grok shot cards (V2, see [SHOT_CARD_AUDIT.md](SHOT_CARD_AUDIT.md))
and local study packets produce test documents. Their lessons feed this
template; their pixels are never final references.

## 2. Step 1 — analyse the scene

Fill one scene sheet per room, game or route. Take every fact from code and
committed art; mark anything unknown `TO_MEASURE` or `OWNER_QUESTION`.

| Field | Record | Where to find it |
|---|---|---|
| Scene | Room, game or route ID; code entry points with line numbers | `scripts/`, `scenes/` |
| Context | Medium and tempo variant (section 6, M10), costume, other characters present, camera (fixed or follow) | Layout JSON, owner decisions |
| Roshan on screen | Displayed figure height in base-canvas pixels, layer and occlusion, shadow or contact rule | Node scale times cell size; layout contract |
| States | Every state Roshan can be in here (listening idle, travel, arrive, each work verb, react, celebrate, ride, carried) and the transitions between them | The scene's state machine |
| Interactions | Each child input or game event and what Roshan should visibly do: intention, travel, contact, consequence, settle | Input handlers, objective voice lines |
| Current presentation | Which atlas and cells, and how they play (authored frames, cross-fade, pose loop, equal-time slideshow, still cutout sliding, whole-sprite rotation) | Code, plus `tools/measure_roshan_motion.py` |
| Story and voice | Lines and story beats tied to her actions | Voice manifest, story clips |

**Output: the interaction table**, one row per Roshan action:
`id | trigger | what she must visibly do | current presentation | problem`.

## 3. Step 2 — decide for each interaction

Ask in order; the first "yes" is the decision.

| # | Question | Decision |
|---|---|---|
| 1 | Is Roshan absent or passive (only an object or effect changes)? | `NONE` for Roshan; route the object to the object-animation lane if needed |
| 2 | Is it a story moment between scenes that the child does not perform? | `CINEMATIC` (story-clip lane; the Day One selected-cut clips stay untouched) |
| 3 | Does an accepted clip already perform this verb in this context, orientation and scale? | `REUSE` (integration only) |
| 4 | Does suitable art exist but the playback is wrong (cross-fade ghosting, fin flipping sides, pose keys looping, equal-time slideshow, whole-sprite rotation)? | `CODE_FIX` by Codex, then review again |
| 5 | Does an accepted clip perform the action in another context, tempo or costume (for example water swim to Sky Lagoon swim)? | `VARIANT`: generate from that clip's registered keys at the new tempo |
| 6 | Do all needed key poses exist in approved art (home pose, contact pose, end pose) for this orientation? | `GENERATE` with LTX |
| 7 | Is a key pose missing (a new view, a grip on a prop, a contact pose)? | `KEYS_THEN_GENERATE`: ImageGen draws only the named missing keys, identity-bound to `roshan_base.png`, then LTX |

A still cutout that slides because no travel clip exists is not a `CODE_FIX`;
it needs the travel clip first. Record the reason for every decision in one
sentence.

**Priority** orders the backlog: how often the child sees it (every session,
most sessions, rare), story weight (required action or optional), and defect
severity (identity or anatomy break, then snap or ghost, then stiffness).
Record dependencies: a work clip that starts with travel depends on the travel
clip.

**Merge across scenes:** one clip serves every scene with the same verb,
context and orientation. The backlog is a list of clips, each naming the
scenes that use it.

## 4. Step 3 — hand it to the right model

| Decision | Model or tool | Run by | Input | Output |
|---|---|---|---|---|
| `GENERATE`, `VARIANT` | LTX locally in ComfyUI through Codex's runner script. Measured pilot settings: LTX-Video 2B 0.9.8 distilled, 896×512, 24 fps, 41 or 81 frames, registered whole-figure guide keys. LTX-2.3 temporal retake (448×256 measured on the 8 GB card) repairs a defective window | Codex | The card's `generation` and `locks` blocks; registered keys; prompt | Native frames and a receipt |
| `KEYS_THEN_GENERATE` | ImageGen for the named missing keys only, bound to `roshan_base.png` (and prop art), then as above | Codex | The card's `keys` block | Key PNGs into the Aseprite master |
| Every generated clip | Aseprite bridge | Codex | Native frames | Editable master, cleaned frames, tags, pivot, sockets, lossless atlas and JSON |
| `CODE_FIX`, `REUSE` | Godot code | Codex | The card's `runtime` block | Code change and probes |
| `CINEMATIC` | Story-clip lane (Grok or API with a V2 shot card and visual packet) | Codex | Shot card | Video under the cinematic gates |
| Test study | Grok (V2 card) or LTX study packet | Codex | Study brief | Reference only; lessons digested here |

Route by role, not by brand: a better local model replaces LTX-Video 2B by
changing the runner's model entry, not the template.

## 5. Step 4 — fill the card

One card per clip: [`templates/ROSHAN_ANIMATION_CARD_V1.json`](templates/ROSHAN_ANIMATION_CARD_V1.json).
Its blocks:

| Block | Holds |
|---|---|
| `scene`, `interaction`, `decision` | Steps 1–2: where, what she does and why this decision |
| `orientation` | Authored facing (right), mirror rule, home pose with fin and ponytail sides |
| `performance` | Intention sentence, register, phases with seconds, loop or one-shot, follow-through, contact window, end state |
| `keys`, `props` | Existing key poses with hashes; named missing keys; each held prop and whether it is baked into the frames or a separate card on a hand socket |
| `generation` | Route, runner, model, size, fps, frame count, seed, guide frames and strengths, registration landmark, extraction background, prompt, caps |
| `locks` | Generator-independent identity and continuity locks taken from the V2 shot card: exact cast, identity and anatomy invariants, forbidden changes, required prompt phrases (each must appear in the prompt), causal chain, continuity |
| `aseprite` | Master path, layers, tags, pivot, socket tracks, export, round-trip check |
| `runtime` | Target script and node, playback rate, events and their owners, interruptions, mirroring, per-scene loading |
| `review`, `evidence` | Checks in section 7, attempts and receipts, and the three separate claims |

**Props.** A prop that stays in her hand for the whole clip may be drawn into
the frames, with a per-frame tool-point track exported from Aseprite. A prop
that changes owner (picked up, put down, handed over) stays its own card
attached to a per-frame hand socket, so it owns its pixels once
(`DL-LAY-05`) and contact is measured on the tool art (gold-star `GS-02`).

## 6. Style rules every card meets (motion locks, revision 2)

| Lock | Rule |
|---|---|
| M1 Orientation | Left and right only; sprites have no up or down orientation (owner). Author facing right; mirror the whole sprite for left. Moving up or down the screen keeps the current horizontal facing. |
| M2 The tail drives | One connected wave from hip to fin; fin root continuous, broad lobes, gentle membrane curve. Arms scull or balance near the chest. Shoulders, torso, bodice and hair answer each stroke (owner 2026-10-04). |
| M3 Home pose and fin side | Each clip starts and ends on its home pose, with the fin and ponytail on the home pose's sides. The fin changes side only through a drawn swish or turn. |
| M4 Follow-through | Ponytail and curls trail the head and settle with a buoyant curl; the fin tip trails the tail root; the tiara stays rigid; sleeves settle. |
| M5 Rich motion | Full, smooth motion: keep the native generated frame sequence (24 fps in the current runner) and choose each clip's playback rate from review and the device budget. No limited-animation style and no frame-thinning to hide defects (owner). |
| M6 Crisp contours | No motion blur, smear or cross-fade between frames unless a brief asks for it. A smeared frame is repaired (Aseprite repaint or a temporal retake window), not removed. |
| M7 Listening idle | Idle is attentive and alive with authored breath, hair and fin motion; no whole-sprite rotation or squash. |
| M8 Action shape | Notice, travel, contact, the visible finish of the task, settle, show the result, then celebrate once. Gameplay commits progress; animation only reports events. |
| M9 Delight | The livelier Playful Dolphin register only for a real discovery, greeting or earned success, once per event. |
| M10 One Roshan, context variants | The same identity and swim grammar everywhere; tempo follows context. Water: standard swim. Sky Lagoon: swimming, slower and more modest travel (owner). Castle rooms: `OWNER_QUESTION` (README Q7). Costumes change props and verbs, not the swim. |

The 2026-09-11 [movement language](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md)
remains the acting direction under these locks.

## 7. Step 5 — produce, review, iterate

1. **Keys.** Register every key to one root landmark (waist or bodice tip) on
   a fixed canvas; check fin and ponytail sides against the home pose.
2. **Generate.** At most two generated takes per brief and backend; task caps
   never reset when switching backend or splitting the action (`DL-MOT-16`).
3. **Inspect native frames before anything else:** identity against
   `roshan_base.png`, whole-figure response, crisp hands and fingers, one
   tail, fin and ponytail sides. A failed source goes back to generation with
   a diagnosed change; it is never salvaged in Aseprite (owner rule recorded
   with RSW-FLOW-01). A passing source is cleaned in Aseprite.
4. **Aseprite.** Keep native frames on a hidden layer; clean mattes and local
   defects; register the pivot; tag phases; export a lossless atlas and timing
   JSON; reopen and compare the export.
5. **In game.** Wire the clip behind a switch for an A/B against the current
   presentation; gameplay validates targets and commits progress; run the
   probes; measure memory and frame time; load each scene's clips only in that
   scene. Power-of-two atlases may use VRAM compression on the device.
6. **Review.** Machine checks (measure tool: fin side at entry and exit,
   neighbouring-frame change; crisp-frame review; probes), then the owner at
   normal speed on the tablet. Child and device sessions are separate claims.
7. **Record** attempts, time, cleanup minutes and cost per accepted second;
   add lessons to the card and the impact record.

## 8. Using it across the game (Phases B and C)

1. List every room, game and route where Roshan appears (start from
   [ANALYSIS.md section 4](ANALYSIS.md#4-what-roshan-actually-does-on-screen-today)).
2. Fill a scene sheet and interaction table for each.
3. Judge every existing animation right or wrong against the locks and the
   scene's intention; record the verdict per interaction.
4. Make the decisions, merge clips across scenes, and order the backlog by
   priority.
5. Produce and polish in that order; re-measure after every change.

## 9. Worked examples

Three cards built from real code facts at `dev 8a2f30cb`:

| Card | Scene | Decision |
|---|---|---|
| [`RAC-WATER-SWIM-STANDARD`](examples/RAC-WATER-SWIM-STANDARD.json) | Travel in water scenes (first user: the Day One Pool) | `KEYS_THEN_GENERATE` — no approved right-facing side-view swim key exists |
| [`RAC-SKY-LAGOON-SWIM-GENTLE`](examples/RAC-SKY-LAGOON-SWIM-GENTLE.json) | Sky Lagoon promenade travel | `VARIANT` of the water swim: slower, more modest |
| [`RAC-POOL-SKIMMER-SCOOP`](examples/RAC-POOL-SKIMMER-SCOOP.json) | Day One Pool: scoop trash with the skimmer | `KEYS_THEN_GENERATE` for the grip and scoop keys; travel reuses the water swim |

## 10. Checks to build (README RM1)

- A card validator: schema, required fields, hashes, right-facing
  orientation, home pose sides, every required prompt phrase present in the
  prompt, caps declared.
- A general LTX runner that reads the card instead of per-study scripts.
- An Aseprite bridge that turns native frames into a tagged master and a
  lossless atlas with pivot and socket JSON, and proves the round trip.
