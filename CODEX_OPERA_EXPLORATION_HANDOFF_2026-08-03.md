# Codex handoff — the exploration layer for the Pearl Opera career worlds (2026-08-03)

**Audience:** Codex — image generation + deterministic promotion.
**Purpose:** commission the art that turns thirteen beautiful, inert career
paintings into thirteen places a four-year-old can walk around in. The
engine design that consumes this art is written against shipped code; the
object census that sized it is written against the shipped tiles. This file
specifies **only the art**, and it is deliberately small: **18 shared files
carry 234 career-slots**, and only two families are per-career.

Conventions by reference — the weighted acceptance gate, the
automatic-rejection list, the STYLE-JOBS / STYLE-HOUSE contracts, the P2-09
canonical prop locks, the Path A / Path B rule, the 2048px rule and the
staging protocol are as written in
`OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md`. The two open sibling
handoffs are `CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md` (221-row ledger)
and `CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md` (26 sheets);
section 6 sequences all three.

Companion documents (read for context, do not re-solve):
`OPERA_FRAMING_PACING_ANIMATION_AUDIT_2026-08-03.md`,
`CHAPTER2_PARTY_ROLES_2026-08-03.md`,
`CHAPTER2_BIBLE_ACT_SCRIPTS_2026-08-03.md`.

---

## 1. THE DIRECTION

### The owner's ask, verbatim

> *"We've made these great looking backgrounds, but Mermaid Roshan has no
> real ability to explore them. The gameplay is very fast paced and
> engaging — using the same assets, but applying them in a slower, more
> contemplative way, may be the step for success in the next edition."*

**Audience of one:** a four-year-old non-reader, on a tablet, with one
finger. No fail states, no reading, nothing lost, nothing counted at her.
Target ≈ 2 minutes per career act.

### The spine the whole layer hangs on

**Far touch: the painting answers. Near touch: the painting answers, Roshan
reacts, she speaks, and she keeps something.**

That single asymmetry does all the teaching. A child who never understands
"walk over there" still gets a responsive picture on every touch. A child
who notices the bird only *gives* her something when she is standing under
it has invented walking by herself — no arrow, no words, no instruction.
Proximity threshold: **220 px** from her feet.

### What already shipped this session — do NOT re-solve these

Codex should treat every item below as done and stable. None of them is an
art request, and none of them should reappear in a candidate's rationale.

| Area | State |
|---|---|
| **Framing** | The near-black 1244x124 header is gone (compact storybook title plate). The permanent 10% navy wash over every painting is gone. The six-portrait audience row — which covered **57%** of each painting's richest band — now appears only for the finale performance. The crowd meter no longer overlaps the portraits. Stage spotlights no longer wash over painted districts. Chrome was **50.8%** of the screen; the painting now runs nearly edge to edge. |
| **Character scale** | Roshan renders ~**1.3×** a crew imp (owner rule 2026-08-03: a bit taller, **never >1.5×**). Crew imps 118→180 px, captain 150→200 px. This is a binding contract for every new figure in this package. |
| **Imp pathfinding** | A per-career **ROAM envelope** (`OperaStagePaths.roam_range()`, `opera_stage_paths.gd:178`) keeps crew imps inside the walkable span of each painting's derived route — off entry arches, destination daises, water inlets and foreground ledges. New walking figures inherit it. |
| **Widget feedback** | Seven wiring defects fixed (ink-band progressive reveal, charge-meter fill, completion hold, bounce rate-limit, phase-gap skip, affordance restore) plus an aspect squash. |
| **Audio** | 100 new themed clips; every career's imp apprentice now talks about that job. |

### P0 — one art *decision*, not an art request (read before generating)

The delivered `world_<career>_c{0,1}r{0,1}.png` tiles inset the artwork inside
a blurred bleed margin: sharp content spans **x 0.100 → 0.900** of the
composed 2048x1152 frame. The draw code maps the whole frame — bleed
included — to the full 1280x720 screen, so every recorded coordinate lands
at `screen = 0.10 + 0.80 × recorded`. Error is zero at centre and **±128 px
horizontally, ±72 px vertically** at the edges. The Roshan animation handoff
already flagged the same smear ("~68px on the left and ~121px on the right,
baked into the source art").

**Decision: fix it in code, not in art.** Applying the transform inside
`OperaStagePaths` is four lines and corrects all 13 careers, both clue spots
and stations, at once. **Do not re-render the 52 world tiles + 52 stage tiles
to remove the bleed** — that is a 104-file regeneration to save four lines,
and it would invalidate the widget package's registration work.

Two consequences that bind this package:

1. **Nothing in this ledger is coordinate-anchored.** Every shared file is a
   free-floating effect the engine positions. Generation can start
   immediately and in parallel with the coordinate re-derivation.
2. **Seven careers point at a painting that no longer exists.** farmer,
   boxer, magician, painter, astronaut, racer and popstar were regenerated
   as *different places*, not variations. Their `landmark` strings describe
   furniture that is gone. That is a **data** re-derivation task (ours), and
   it gates only the two placement-sensitive files in this package
   (`explore_sprout`, `explore_curtain_open`).

---

## 2. THE EXPLORATION LAYER

### What is being added, in plain terms

A new **WANDER** state sits between the task cards. Today `_show_phase()`
auto-glides Roshan to a station and opens a card. The split becomes
`_arm_phase()` (light the station, place the helper, say the teaser — do
*not* open the card) and `_open_task()` (today's behaviour, minus the
glide, because she walked here herself). Between them, the painting is live:

- **Free walk (W1–W3).** She walks where the child taps, along the painted
  route, using the identical clamp law the imps already walk by, so she can
  never stand in water or off-screen. The lit station **invites** — it does
  not pull. Arriving somewhere empty makes the nearest untouched painted
  detail twinkle once, unprompted.
- **Touch-the-world (T1–T4).** The 8 `clue_spots` per career are already
  coordinates of specific painted details, and today only two detective
  phases use them — **104 responsive details lying dead in the other eleven
  careers.** Touching one lifts that patch of the painting out of the tile
  set and plays one of five motions (`flutter` / `light` / `sway` / `dart` /
  `bulge`). Near enough, Roshan names it in 3–6 words and reacts. The pocket
  lens — ranked the single best interaction in the project for this age, and
  currently present in 2 of 13 careers — becomes available everywhere.
- **Collecting (C1–C4).** Career-themed **party favours** hidden at painted
  details, picked up by *standing under them*. **No HUD, no counter, no
  strip** — she has three because three are orbiting her. They persist in
  `m.opera_pantry`, a dictionary that already exists, already saves and is
  already asserted by `probe_load.gd`. At the curtain call they fly off and
  lay out in a row beside the returned goal prop.
- **Quiet beats (Q1–Q4).** Sit and watch a long ambient event she could not
  have produced by tapping. A listening spot that holds a *sound* instead of
  a picture. **Breathing room** — 2.5 s of nothing after each job, with the
  thing she just made still on screen. A held shot at the theft with the
  music dropped out.
- **Helpers (H1–H5).** A friend walks the promenade behind her, keeps up,
  stops when she stops. Tap him and he names the nearest undiscovered
  detail — **the pull-back ladder turned into a character**, which is the
  difference between help and correction. He fetches far favours. He sits
  when she sits. At the curtain call he says why the thing she made matters
  to *him*; those thirteen lines are already written in
  `CHAPTER2_PARTY_ROLES_2026-08-03.md` §2.
- **Additions (X1–X3).** Every detail she has touched keeps a faint
  permanent glint, so by the finale the painting is a map of her afternoon.
  A brainless **peekaboo imp** pops out of a landmark every ~12 s so the slow
  beats are never dead air for a fast child — and it plants the imps as
  present-and-playful **before** the theft, which makes the theft a betrayal
  instead of a random event. And she meets the goal prop at its own
  workbench before it is stolen.

### How it changes an act's rhythm

Chef, 7 phases, `steal_index = 4`. Median four-year-old.

| # | Beat | Register | Budget |
|---|---|---|---:|
| 1 | **Arrival** — world fades up, Kareem walks in behind her, three details twinkle in turn, nothing is asked | slow | **12 s** |
| 2 | IMPS! scuffle — crew 5→3 | fast | 8 s |
| 3 | **Wander → mixing_bowl** | slow | **7 s** |
| 4 | POUR (goal 5.0 → 3.8) | fast | 8 s |
| 5 | **Breathing room** on the poured bowl | slow | **2.5 s** |
| 6 | **Wander → hearth_oven** | slow | **6 s** |
| 7 | STIR (4.0 → 3.0) | fast | 8 s |
| 8 | **Breathing room** | slow | **2.5 s** |
| 9 | **Wander → cake_tower** — the long one; sit-and-watch offered here | slow | **8 s** |
| 10 | BAKE (6.0 → 4.5) | fast | 8 s |
| 11 | **THE THEFT** — held shot, music out | slow | **2 s** |
| 12 | CAKE CHASE — crew 8→6 + captain | fast | 16 s |
| 13 | Curtain-rise sting (any touch skips) | slow | 2.6 s |
| 14 | PIPE (7.0 → 5.6) on stage | fast | 10 s |
| 15 | **Breathing room** | slow | **2 s** |
| 16 | TOP (8.0 → 6.4) | fast | 10 s |
| 17 | **Curtain call** — confetti, favours lay out, helper's wish | slow | **11 s** |
| | **TOTAL** | | **≈ 124 s** |

**Self-paced share: 55.6 s of 123.6 s = 45%**, against ~4% today (three
1.3 s auto-glides). The act runs 14 s longer than today's ~109 s and feels
like a different medium. Six-phase careers (boxer, racer, popstar) get two
wander windows instead of three and land at ≈ 112 s — correct, not a defect;
those three are the loud careers.

**The art consequence:** everything that plays during a *slow* beat is
either the painting itself or one of the shared effects below. There is no
per-career response art in this package at all, because the response *is*
the career's own painting.

---

## 3. THE ART REQUEST

### 3.0 Shared delivery contract (binds every request in this section)

- **Target runtime path:** `assets/opera/worlds/explore/` (new directory) for
  every `explore_*` file; `assets/opera/worlds/actors/` for `helper_*` and
  `imp_mischief_*` (matches the shipped actor naming exactly and the helper
  slot the bible already specified).
- **Canvas:** RGBA, transparent, **power-of-two**, subject centred with ≥12 px
  margin. Satisfies the `assets/ART_GENERATION_CONTRACT.md` "≤1024 px longest
  side OR power-of-two" clause. The one non-square multi-cell strip
  (`explore_sprout`, 768x256, three 256x256 cells) follows the precedent the
  widget handoff set for lane-lit strips.
- **Style:** STYLE-JOBS finish, quoted by name, plus the P7 harmonization
  wording — navy/indigo contour lines `#4a4f78`–`#1a1238`, **never black**;
  aqua/lavender shadows, never black; high-key; flat broad colour fields;
  child-readable at 50% scale. Palette anchors: coral `#ffa399`, lavender
  `#a87dd6`, gold `#f5b838`, aqua `#45c4c7`, cream `#f5ebd1`, pearl white
  `#E4F5F6`.
- **GREEN IS RESERVED — hard lock.** The success-zone green (house value
  ≈ RGB 117,240,158) exists in the widget layer's T1/T2 go-zones and nowhere
  else. It is the one channel that tells a pre-reader "wait for THIS", and it
  is what makes waiting beat mashing. **No exploration asset may carry green
  in any quantity.** A mint-green "found it" sparkle would silently break the
  anti-mashing signal across all 60 widget phases. This is the single most
  likely way to fail this package.
- **No baked light, no vignette, no drop shadow** on any shared effect. These
  files land on thirteen paintings with thirteen different baked light
  directions (chef warm from upper-left, detective night moonlight, magician
  daylit water, popstar rainbow). An effect that carries its own shadow will
  fight every one of them. Feathered transparent edges only; zero hard rim.
- **Transparent centres** on every overlay that sits *on* a painted object
  (ring, dwell arc, here-ring, prop mat). The painting is the content; the
  effect is the frame around it.
- **Content locks:** no words, letters or numerals anywhere; no baked
  characters in shared FX (Roshan, helpers, imps are runtime sprites); stars
  only as effects, using the house four-point diamond/star shape; bubbles
  never flame; no invented faces on ordinary props; the automatic-rejection
  list applies in full.
- **Staging:** `assets_src/concepts/opera_exploration_2026-08-03/cards/` +
  `contact_sheets/` + `PROMPTS.md` + `REGENERATION_LEDGER.csv`, weighted gate
  pass ≥4.5 / target ≥4.7, one controlled promotion commit, one
  `ASSET_LICENSES.md` line per accepted asset, QA renders at gameplay scale
  on the Mobile renderer. Candidates without runtime captures cap at 2/5 and
  must not ship (section 7 states what "runtime capture" means for this
  package specifically — it is stricter than usual).

---

### 3.1 FAMILY A — WORLD-RESPONSE FX (7 files, **all shared**, all 13 careers)

This family is the whole touch-the-world layer. **There is no per-career
response art**, because T1 lifts the responding patch out of the career's own
tile set and transforms it — *that* bird, *that* lantern, at 1.6× source-to-
screen ratio so a 160 px screen patch samples 256 source px and scales to
1.10 without softening. These seven files are the grammar drawn around it.

**7 files × 13 careers = 91 career-slots.**

| asset_id | filename | canvas | depicts |
|---|---|---|---|
| `explore_touch_ring` | `explore_touch_ring.png` | 256x256 | An expanding ripple ring: two concentric thin contours in pale aqua and pearl, fully transparent centre, softly feathered outer edge, slightly irregular so it reads hand-painted rather than vector. The universal "your touch registered" mark — engine scales 0.3→1.4 and fades to zero over 0.35 s. Must read on water, sand, tile, sky and fabric. |
| `explore_found_twinkle` | `explore_found_twinkle.png` | 256x256 | A cluster of three four-point diamond sparkles at three sizes (one dominant, two satellites), warm white through pearl-gold, no ring, no enclosing shape. The "you found it" flourish for T1 hits, W3's unprompted twinkle, H2's show-me pointer and X1's permanent glint. **Replaces the current reuse of `fx_dizzy_stars.png`, whose orbiting ring reads as damage** — the wrong sentence for a discovery. |
| `explore_glow_warm` | `explore_glow_warm.png` | 512x512 | A soft circular bloom of warm gold falling to full transparency with no discernible edge or banding; slightly denser at the core, faintly irregular. Additive-safe. This is the `light` motion for **every** lantern, oven, window, lamp post, pearl, heart medallion and lit stage in the set — roughly 40 painted objects served by one file. |
| `explore_glow_cool` | `explore_glow_cool.png` | 512x512 | Identical construction in seafoam-aqua through pale lavender. The night and underwater careers (detective's moonlit district, magician's daylit water, astronaut's habitat pods) reject warm gold — it reads as fire in a place with no fire. Two files cover both lighting worlds; a single "neutral" glow covers neither. |
| `explore_here_ring` | `explore_here_ring.png` | 512x256 | A flat elliptical ground ring seen in perspective (2:1 squash), pale gold, thin double contour, transparent centre, one soft gap in the ring so it does not read as a target or a portal. Two jobs: a quiet pulse at her feet in WANDER, and a 0.4 s mark at the tap destination so a child sees where she is going before she gets there. |
| `explore_dwell_arc` | `explore_dwell_arc.png` | 256x256 | A full 360° ring of evenly spaced small pearls, uniform brightness, transparent centre. The engine crops it by angle to fill clockwise: the lens's 0.45 s reveal dwell and the station's 0.35 s open dwell. Beads rather than a solid arc so partial progress is countable at a glance and reads as jewellery, not as a loading spinner. |
| `explore_breadcrumb` | `explore_breadcrumb.png` | 128x128 | One small pearl step-dot with a soft aqua halo, slightly ovoid. The engine repeats it along the route between her position and the lit station for the 11 s rung of the pull-back ladder. Must read at 24–32 px on screen and must not compete with `explore_found_twinkle` — a breadcrumb says "this way", a twinkle says "here". |

---

### 3.2 FAMILY B — COLLECTIBLES: the party favours (15 files: **2 shared, 13 optional per-career**)

Chapter 2 canon: every career makes one piece for a party that turns out to
be her own birthday. The candy maker's function is literally *"one for every
guest — and one for YOU, Sparkle."* So collecting is **party favours**, and it
is persistent — `m.opera_pantry` already exists (`main.gd:295`), already
saves (`save_state.gd:132/207/465`), already round-trips under `probe_load`,
and the shipped carrot-cake beat (`opera_act.gd:3219`) already proves that a
thing found in one act changes dialogue in a later one.

**Budget:** 1 favour in the arrival beat + 1 per wander window + 1 at the
workbench = 5 on 7-phase careers, 4 on the 6-phase ones. **Never displayed as
X of Y.** She has what she has.

| asset_id | filename | canvas | shared? | depicts |
|---|---|---|---|---|
| `explore_favour_pouch` | `explore_favour_pouch.png` | 256x256 | **SHARED — 13 careers** | A small scallop-shell pouch closed with a pearl clasp and a single coral ribbon tied in a soft bow, cream body with a gold rim, three-quarter view, no contents visible. **This is the object that orbits her** and lays out in a row at the curtain call. One file is the entire collecting layer. Must read at **34 px** — that is its orbit size — so the silhouette is shell + bow and nothing else. |
| `explore_favour_glint` | `explore_favour_glint.png` | 256x256 | **SHARED — 13 careers** | A single fat four-point star with a soft pearl bloom, warm gold, no tail. The orbit sparkle that circles her once a favour is hers. **A real defect fix, not a nicety:** the orbit currently reuses `fx_stolen_sparkle.png`, so the identical star that means "the imp took this from you" would now mean "this is yours." One file separates the two sentences. |
| `explore_favour_<career>` ×13 | e.g. `explore_favour_chef.png` | 256x256 | per-career, **P3, optional** | The career's own tiny keepsake, drawn as a flat storybook token: chef a stemmed cherry; candymaker a wrapped candy from the canonical 7-shape roster (P2-09g); detective a glowing paw-print tile; ballerina a rose bud with ribbon; farmer a coral seedling in a pot; doctor a heart medallion; magician a pearl-tipped wand charm; painter a paint blob token; astronaut a pearl rivet; racer a pennant; popstar a music note; boxer a small sash rosette; nursery a star from the mobile. **The layer ships and is complete without these** — until they land the favour is the painting's own patch lifted out and shrunk to 34 px, exactly as T1 lifts it. |

---

### 3.3 FAMILY C — QUIET-BEAT PROPS (4 files, **all shared**)

What makes stillness rewarding at four is that **something changes slowly,
and it changes because she stopped.** These four files are what a stopped
child looks at. Every one of them is shared, because the ambient event is
built from the painting plus a drifting thing, and the drifting thing is the
same drifting thing in all thirteen underwater districts.

| asset_id | filename | canvas | depicts |
|---|---|---|---|
| `explore_rest_cushion` | `explore_rest_cushion.png` | 256x256 | A small round coral-and-cream sitting cushion with a gold piped edge and a pearl button, slightly squashed, seen from a low three-quarter angle so it beds into the ground plane. Fades in under her when she sits (Q1) and under the helper when he sits with her (H4). **This is the cheapest possible cover for the missing SIT animation** — until Roshan `sheet_c` lands, the cushion is what tells the child she sat down, and the body is an `ActorMotion` squash. |
| `explore_ambient_shoal` | `explore_ambient_shoal.png` | 512x256 | Five small pastel reef fish in flat side profile, facing left, staggered in a loose diagonal shoal, coral/aqua/lavender/cream bodies with simple navy contour and one pearl highlight each — no faces beyond a dot eye, no expressions. **The census's single hardest blocker resolved with one file:** there is no fish, bird, crab or butterfly sprite anywhere in the opera set, which is why nothing can currently dart, cross or drift. Every career painting is now underwater, so one shoal is on-world for all thirteen. Also serves the `dart` motion where the painting has no creature to lift. |
| `explore_ambient_bubbles` | `explore_ambient_bubbles.png` | 256x512 | A vertical column of rising bubbles at mixed sizes, pearl-white rims with transparent centres and a single crescent highlight each, denser at the bottom and thinning upward. The passive drift under Q1's long ambient event and the visual for Q2's water-side listening spot. **Bubbles never flame** (house lock). |
| `explore_listen_bloom` | `explore_listen_bloom.png` | 512x512 | Three concentric open arcs expanding from a common origin, pearl and pale aqua, thinning and fading outward, transparent centre, **not** a closed ring. The visible form of a sound. Q2 gives each career one spot that holds a sound rather than a picture (the oven crackling, the sea under the pier, the empty house applauding) — on a muted tablet, which is most tablets, this file is the entire beat. |

---

### 3.4 FAMILY D — HELPER INTERACTION ART (25 new files + 1 REUSE: **the only genuinely per-career family**)

`rival_actor` already exists as a second stage actor with `_place_on_stage`,
depth, bounce and a nursery override to `faron_nursery.png`, and is hidden
outside the finale. The helper is the same slot used the other way round.
`CHAPTER2_BIBLE_ACT_SCRIPTS_2026-08-03.md` §(d) already specified the engine
ask — *"a `helper_actor` TextureRect loading
`assets/opera/worlds/actors/helper_<career>.png`, hidden when the file is
missing … ~12 lines, mirrors the existing `_actor()` + `_place_on_stage()`
calls, zero risk"* — and this package fills it. **The filename pattern below
is that specification, unchanged.**

The cast is already fixed by `CHAPTER2_PARTY_ROLES_2026-08-03.md` §2, and
`AudioDirector._speaker_key` (`audio_director.gd:95-113`) already routes
every one of these names to a voice — verified: `rosalina`, `huluu`,
`evie`/`lamb`, `harper`/`fiona`, `faron`, `daddy`, `chuck`, `wacky`,
`sparkle`, `mewsha`, and `kareem` → `shop`.

#### PROTECTED-ZONE RULE — read before generating any helper card

`assets/characters/friends/` is a **protected, untouchable zone** under
`assets/ART_GENERATION_CONTRACT.md`, alongside `assets/book/` and
`assets/audio/voices/`. Book-derived friend cutouts are never regenerated.

**This package never writes to that directory.** It commissions *opera-world
stage actor cards* at `assets/opera/worlds/actors/helper_<career>.png`,
using the protected cutout as **binding identity reference only**. The
shipped precedent is exact: `faron_nursery.png` is a staged opera actor card
derived from Faron, generated in
`assets_src/concepts/opera_nursery_2026-08-01/` and promoted to
`assets/opera/worlds/actors/`. Follow that pattern for all twelve. Any
candidate that modifies, overwrites or "improves" a file under
`assets/characters/friends/` is an automatic rejection regardless of score.

#### D1 — Helper stage cards (13 slots: 1 REUSE, 8 Path A, 4 Path B)

**Canvas for all: 512x512 RGBA transparent** — matching every shipped file in
`assets/opera/worlds/actors/` (`imp_mischief*.png`, `rival_*.png`,
`roshan_*.png`, `faron_nursery.png` are all 512x512).

**Scale contract (binding, owner rule 2026-08-03):** the helper renders at
`Vector2(190, 190)` — the rival's existing number. Roshan must read as ~1.3×
a helper and **never >1.5×**. Author the figure to the same body proportion
as `rival_<career>.png` so the runtime ratio holds without per-file tuning.

**Pose contract:** full figure, standing or floating, three-quarter view
turned slightly toward frame-left (she walks left-to-right and he trails her
by 140 px at 0.8× speed); arms relaxed and empty; feet-or-tail contact on a
**common baseline** so `_place_on_stage`'s depth term does not make him
bob relative to Roshan; silhouette legible at **190 px**; no ground shadow
baked in.

| Career | Helper | Path | Status | Source of identity |
|---|---|---|---|---|
| nursery | Faron | — | **REUSE** | `assets/opera/worlds/actors/faron_nursery.png` — already shipped and already runtime-wired. Zero cost. |
| chef | Kareem | A | NEW | `assets/characters/friends/kareem.png` (443x640) |
| detective | Princess Huluu | A | NEW | `assets/characters/friends/huluu.png` (640x1039). Bible note: *tiara already off, hands empty — the act is about an absence on her head, so her bare hair is the story.* |
| painter | Flower Friend | A | NEW | `assets/characters/friends/flower_friend.png` (389x460) |
| farmer | Chuck | A | NEW | `assets/characters/friends/wacky_chuck.png` (339x500) — isolate Chuck |
| boxer | Wacky | A | NEW | `assets/characters/friends/wacky_chuck.png` — isolate Wacky |
| racer | Harper & Fiona | A | NEW | `assets/characters/friends/two_friends.png` (480x460) — the pair reads as one card, matching the cast entry |
| popstar | Daddy | A | NEW | `assets/characters/friends/daddy.webp` (727x1024) |
| doctor | Evie | A | NEW | `assets/characters/friends/mama_baby.png` (393x479) — isolate Evie |
| candymaker | **Sparkle** | **B** | NEW | **No art exists anywhere in the repo.** Voice only (`assets/audio/voices/sparkle.ogg`), chirps by design. |
| astronaut | **Mewsha** | **B** | NEW | **No art exists anywhere in the repo.** The bible already flags this as **BLOCKING** and specifies the design: *Mewsha in a round fishbowl helmet, floating* — she is the ship's cat and the act's leak-detector. |
| ballerina | **Rosalina** | **B** | NEW | **No art exists anywhere in the repo.** Voice only (`rosalina.ogg`, `_greet`, `_locked`, `_open`, `_win`). |
| magician | **Lamba** | **B** | NEW | Identity ref `assets/characters/lamb_0.png` (owner-directed, per `FABLE_OPERA_LAMBA_TAKEOVER_HANDOFF_2026-08-01.md`). **SPECIES LOCK: Lamba is the round white lamb** — the owner-directed replacement for the rabbit-fish. Never a rabbit, never a bunny-fish, in this or any card. |

> **Consequence if the four Path-B cards are deferred:** those four careers
> simply ship with no walking helper. Acceptable, not ideal — the act plays,
> the VO plays, H2's show-me falls back to the marker ladder. This is why
> they sit at **P2** and not P1: they block four careers, not the layer.

#### D2 — Helper pointing pose (13 files, **P3, optional**)

`helper_<career>_point.png`, 512x512, same identity and baseline as D1, one
arm raised and extended pointing up-and-away from the body, head following
the hand, expression bright. Serves H2 ("Look UP at the flags!"). **H2 ships
without these** on `_bounce_actor` plus an `explore_found_twinkle` at the
named detail; the pose is the upgrade that makes a hint feel like a friend
rather than a system.

---

### 3.5 FAMILY E — FILL THE EMPTY THING (2 files, **both shared**)

The object census found that the seven regenerated paintings contain
**ready-made empty interaction sets, painted and waiting**: farmer has a
clean 3×3 grid of nine empty planting beds; painter has three blank white
easel canvases; magician has three curtained booths with drawn curtains and
empty lit stages. Each of those is one small sprite away from being the best
moment in its career. Two shared files cover all of it.

| asset_id | filename | canvas | depicts |
|---|---|---|---|
| `explore_sprout` | `explore_sprout.png` | **768x256, three 256x256 cells, left→right** | One coral-flower sprout in three growth stages: (1) a pale green-free seedling — two small aqua-tipped fronds just clear of the soil; (2) budding — taller, a closed coral bud; (3) bloomed — an open coral-and-cream flower with a pearl centre. Bottom-anchored in every cell so the base stays fixed as it grows. **Fills all nine farmer beds, and doubles as the ballerina rose bloom and the painter splat garden.** Note the green lock: use coral/cream/aqua foliage, which is also correct for a coral farm. |
| `explore_curtain_open` | `explore_curtain_open.png` | 512x512 | A pair of swagged theatre curtains parted to the sides with a pearl tie-back on each, drawn in **flat white/pearl greyscale with contour only, so the engine tints it per object**. Transparent centre — whatever is behind shows through. **Serves six careers from one file:** magician's three booths, chef's domed cake, detective's evidence lockboxes and treasure chest, candymaker's cottage doors, farmer's barn doors, ballerina's dressing alcove. The census's finding was that every openable object in the set is painted in exactly one state; this is the second state, once. |

> **Do not commission the three painter easel pictures.** Drop the shipped
> `goal_<career>.png` cards into the frames — thirteen finished hero objects
> in the correct style already exist in `assets/opera/worlds/props/`.

---

### 3.6 FAMILY F — PEEKABOO IMP (2 files, **both shared**)

X2 spawns a single brainless imp every ~12 s that pops out of a painted
landmark, waves and ducks back; tapping it gives a kind fizzle, a giggle and
a dropped favour. It uses `_spawn_stage_imp` with **no `ImpAI`** — no windup,
no contact, no combat state — and the shipped `imp_mischief_taunt.png` /
`imp_mischief_flee.png` already read as playful. So this family is an
upgrade, not a requirement.

**IMP-IDENTITY lock applies in full:** purple humanoid imp, curled **striped**
horns (both visible), amber eyes, pointed ears, friendly fangs, small hair
tuft, curled tail. **Absolutely no shell, pearl, scallop, marine badge,
crest, medallion or target motif on any imp, ever.** Friendly mischief,
never scary.

| asset_id | filename | canvas | depicts |
|---|---|---|---|
| `imp_mischief_peek` | `imp_mischief_peek.png` | 512x512 | The imp peeking out from behind something: head, one shoulder and one gripping hand only, body cut off by a **flat horizontal bottom edge across the lower third** so the sprite reads as "behind an object" wherever the engine places it, eyes wide and delighted, one finger to the mouth. **This is the pose that makes X2 land** — today's `taunt` pose is a whole standing figure, so an imp "hiding behind the oven" currently floats in front of it. |
| `imp_mischief_wave` | `imp_mischief_wave.png` | 512x512 | **P3.** Same peek framing, arm raised mid-wave, other hand still gripping the edge. Gives the pop-out a two-frame beat instead of a single pose. |

---

### 3.7 FAMILY G — THE PROP HAS A HOME (1 file, **shared**)

X3 gives the goal prop a workbench she can visit and touch *before* it is
stolen — meeting the thing before it is taken is what makes the theft land at
all. Today `prop_rect.position` is a hardcoded `Vector2(890, 330)` for all
thirteen careers, landing on whatever the painting happens to have there;
the fix is a `WORKBENCH` data row per career (already asked for by the
framing audit §16), not art. One shared file makes it read.

| asset_id | filename | canvas | depicts |
|---|---|---|---|
| `explore_prop_mat` | `explore_prop_mat.png` | 512x256 | A shallow display mat seen in perspective (2:1 squash): a pale pearl-cream oval top with a thin brushed-gold rim and a soft coral under-edge, no legs, no pattern in the centre. It sits under the goal prop at its workbench. **The beat this buys is the empty mat after the theft** — the prop is gone and its place is still there, which states the theft with no words, no card and no VO. One file, thirteen careers, and it is the cheapest emotional payoff in the package. |

---

### 3.8 Out of scope for this handoff (recorded so it is not lost)

Not art, not codex's gate, but requested by the same design:

- **13 ambient loops, 2–3 s** for Q2's listening spots. Ships without them on
  the existing `_fanfare()` pitch-scaled chime trick.
- **~130 short VO lines** — 104 detail names (T2), 13 show-me lines (H2), 13
  helper wishes (H5, **already written** in `CHAPTER2_PARTY_ROLES` §2). All
  optional: `AudioDirector._say` falls back to the speaker's generic clip and
  then to the pitched "yay", so the layer ships silent-safe.

---

## 4. THE REQUEST LEDGER

Schema mirrors `assets_src/concepts/OPERA_WIDGET_ASSET_LEDGER_2026-08-03.csv`,
adapted for a layer with no template/beat axis. Written to
`assets_src/concepts/OPERA_EXPLORATION_ASSET_LEDGER_2026-08-03.csv`.

`asset_id,filename,target_path,family,serves,canvas,shared,priority,status,depicts`

| asset_id | filename | canvas | shared | pri | status | depicts |
|---|---|---|---|---|---|---|
| explore_touch_ring | explore_touch_ring.png | 256x256 | SHARED-13 | P1 | NEW | Expanding pale-aqua/pearl double ripple ring, transparent centre — universal touch-registered mark |
| explore_found_twinkle | explore_found_twinkle.png | 256x256 | SHARED-13 | P1 | NEW | Three four-point diamond sparkles at three sizes, warm white to pearl-gold — the you-found-it flourish |
| explore_glow_warm | explore_glow_warm.png | 512x512 | SHARED-13 | P1 | NEW | Soft warm-gold radial bloom, edgeless, additive-safe — the light motion for every lantern, oven and window |
| explore_glow_cool | explore_glow_cool.png | 512x512 | SHARED-13 | P1 | NEW | Same bloom in seafoam-aqua to lavender — for night and underwater districts where warm gold reads as fire |
| explore_here_ring | explore_here_ring.png | 512x256 | SHARED-13 | P1 | NEW | Flat perspective ground ring in pale gold with one soft gap — her standing mark and the walk destination |
| explore_favour_pouch | explore_favour_pouch.png | 256x256 | SHARED-13 | P1 | NEW | Scallop-shell pouch, pearl clasp, coral ribbon bow — the party favour that orbits her; must read at 34px |
| explore_dwell_arc | explore_dwell_arc.png | 256x256 | SHARED-13 | P2 | NEW | 360-degree ring of evenly spaced pearls, engine crops by angle — the lens and station dwell timers |
| explore_breadcrumb | explore_breadcrumb.png | 128x128 | SHARED-13 | P2 | NEW | One pearl step-dot with soft aqua halo, repeated along the route for the pull-back ladder |
| explore_favour_glint | explore_favour_glint.png | 256x256 | SHARED-13 | P2 | NEW | Single fat four-point star with pearl bloom — the orbit sparkle; separates yours from the theft sparkle |
| explore_rest_cushion | explore_rest_cushion.png | 256x256 | SHARED-13 | P2 | NEW | Round coral-and-cream cushion, gold piping, pearl button — fades in when she sits, covers the missing SIT pose |
| explore_ambient_shoal | explore_ambient_shoal.png | 512x256 | SHARED-13 | P2 | NEW | Five pastel reef fish in flat left-facing side profile — the only crossing creature in the whole opera set |
| explore_listen_bloom | explore_listen_bloom.png | 512x512 | SHARED-13 | P2 | NEW | Three concentric open arcs in pearl and aqua — the visible form of a sound for the listening spots |
| explore_sprout | explore_sprout.png | 768x256 (3 cells) | SHARED-13 | P2 | NEW | Coral-flower sprout in three growth stages, bottom-anchored — fills the nine farmer beds |
| explore_curtain_open | explore_curtain_open.png | 512x512 | SHARED-13 | P2 | NEW | Parted theatre curtains with pearl tie-backs in tintable white, transparent centre — the missing open state |
| explore_prop_mat | explore_prop_mat.png | 512x256 | SHARED-13 | P2 | NEW | Pearl-cream display mat in perspective with gold rim — the prop's home, and its absence after the theft |
| imp_mischief_peek | imp_mischief_peek.png | 512x512 | SHARED-13 | P2 | NEW | Imp peeking with flat bottom crop so it reads as behind an object, finger to lips — makes X2 land |
| helper_candymaker | helper_candymaker.png | 512x512 | per-career | P2 | NEW | Sparkle as a walking stage helper — no art exists anywhere; voice-only character (Path B) |
| helper_astronaut | helper_astronaut.png | 512x512 | per-career | P2 | NEW | Mewsha the ship's cat in a round fishbowl helmet, floating — bible-BLOCKING, no art exists (Path B) |
| helper_ballerina | helper_ballerina.png | 512x512 | per-career | P2 | NEW | Rosalina as a walking stage helper — no art exists anywhere; voice-only character (Path B) |
| helper_magician | helper_magician.png | 512x512 | per-career | P2 | NEW | Lamba the round white lamb as a walking stage helper; SPECIES LOCK lamb, never bunny-fish (Path B) |
| helper_nursery | faron_nursery.png | 512x512 | per-career | P2 | **REUSE** | Already shipped and runtime-wired; zero cost, listed so the 13-slot table is complete |
| helper_chef | helper_chef.png | 512x512 | per-career | P3 | NEW | Kareem restaged as a full-figure walking helper (Path A from the protected cutout) |
| helper_detective | helper_detective.png | 512x512 | per-career | P3 | NEW | Princess Huluu, tiara off and hands empty — her bare hair is the act's story (Path A) |
| helper_painter | helper_painter.png | 512x512 | per-career | P3 | NEW | Flower Friend restaged as a full-figure walking helper (Path A) |
| helper_farmer | helper_farmer.png | 512x512 | per-career | P3 | NEW | Chuck isolated from the Wacky-and-Chuck cutout, standing (Path A) |
| helper_boxer | helper_boxer.png | 512x512 | per-career | P3 | NEW | Wacky isolated from the Wacky-and-Chuck cutout, standing (Path A) |
| helper_racer | helper_racer.png | 512x512 | per-career | P3 | NEW | Harper and Fiona as one paired card, matching the cast entry (Path A) |
| helper_popstar | helper_popstar.png | 512x512 | per-career | P3 | NEW | Daddy restaged as a full-figure walking helper (Path A) |
| helper_doctor | helper_doctor.png | 512x512 | per-career | P3 | NEW | Evie isolated from the mama-and-baby cutout, standing (Path A) |
| helper_chef_point … helper_nursery_point | helper_<career>_point.png ×13 | 512x512 | per-career | P3 | NEW | Same identity, one arm raised pointing up-and-away, head following the hand — the show-me hint pose |
| explore_favour_chef … explore_favour_nursery | explore_favour_<career>.png ×13 | 256x256 | per-career | P3 | NEW | The career's own tiny keepsake token; the layer is complete without them |
| explore_ambient_bubbles | explore_ambient_bubbles.png | 256x512 | SHARED-13 | P3 | NEW | Vertical column of mixed-size pearl-rimmed bubbles — passive drift and the water listening spot |
| imp_mischief_wave | imp_mischief_wave.png | 512x512 | SHARED-13 | P3 | NEW | Peek framing with the arm raised mid-wave — the second frame of the pop-out beat |

### Ledger totals

| | files |
|---|---:|
| **NEW files requested** | **56** |
| REUSE rows (no generation) | 1 |
| **Total ledger rows** | **57** |
| Shared files (1 file serves 13 careers) | **18** |
| Per-career files | 38 |
| **Career-slots covered by the 18 shared files** | **234** |

| Priority | files | what it unlocks |
|---|---:|---|
| **P1** | **6** | The exploration layer does not ship without these. All six are shared. Six files light up 104 painted details across 13 careers. |
| **P2** | **14** | The quiet beats, the peekaboo imp, the prop's home, the two fill-the-empty overlays, and the four careers that otherwise have no walking helper. (15 ledger rows at P2 — the fifteenth is the `helper_nursery` REUSE row, which generates nothing.) |
| **P3** | **36** | The long tail: 8 Path-A helper restages, 13 point poses, 13 favour tokens, ambient bubbles, imp wave. Every one is an upgrade to something that already works. |

Verified against the generated CSV: 57 rows, 56 NEW + 1 REUSE; 18 shared and
38 per-career among the NEW files; P1 6 / P2 14 / P3 36. Family split:
A-world-response 7, B-collectibles 15, C-quiet-beats 4, D-helpers 26,
E-fill-the-empty 2, F-peekaboo-imp 2, G-prop-home 1.

---

## 5. WHAT NEEDS NO ART

**19 of the 22 exploration tasks need nothing commissioned.** This section
exists so nobody generates art for them. If a candidate appears whose
justification is any row below, it is out of scope.

| Task | What it is | Built from |
|---|---|---|
| **W1** Walk the promenade | She walks where the child taps | `_stage_feet_at_x()` (the identical clamp law the imps already walk by), `_lens_input`'s event shape, `_place_on_stage`'s depth term, `move_toward` in `_process`. **Zero art.** |
| **W2** The station invites | Lit marker breathes; 0.35 s dwell opens the job | `_draw_station_marker` given three states instead of two. `station_marker.png` **already ships** (512x1024). |
| **W3** Stop and look | Arriving somewhere empty twinkles the nearest detail | `ActorMotion` breath + `explore_found_twinkle`. No new subject art. |
| **T1** The painting answers | The touched patch of the painting moves — flutter / light / sway / dart / bulge | **The painting is the sprite.** The patch is cropped live from `world_<career>_c*r*.png` at a uniform 1.6× source-to-screen ratio and transformed. **This is why there is no per-career response art in this package, and there must not be.** |
| **T2** She says what it is | Roshan names the detail in 3–6 words | `show_msg` → `AudioDirector._say` with its existing three-step fallback. Text + optional VO. **Zero art.** |
| **T3** She reacts | Lean, hop, squash-settle toward the touched spot | `ActorMotion` transforms today; Roshan `sheet_c` later (section 6). **Explicitly not** the existing `roshan_25d` gesture atlases — those are uncostumed, and the animation audit §5 is right that a costume swap mid-act is a worse defect than stiffness. |
| **T4** The pocket lens | Magnifier draggable over the whole stage, 0.45 s dwell reveals | The entire lens stack unmodified. `magnifier.png` **already ships** (512x512). Giving 11 more careers the best mechanic in the suite costs **zero assets**. |
| **C2** Curtain-call lay-out | Favours fly off her and land in a row | `celebrate()` + the shipped prop-comes-home bounce + `_bounce_actor`. **Zero art.** |
| **C3** The favours matter next time | A later career's content changes because of an earlier find | The `gift`/`uses` chain that already ships (`opera_act.gd:1558`, read at `:3219` where farmers' carrots turn the chef's cake into a carrot cake). **Zero art.** |
| **C4** The one left over | Racer ends with one favour still in her hand | **One line of dialogue.** |
| **Q1** Sit and watch | A long ambient event she could not have produced by tapping | Chained T1 patch events along `point_along()` + `explore_rest_cushion` + `explore_ambient_shoal`. No per-career art. |
| **Q2** The listening spot | One spot per career holding a sound, not a picture | `_set_ambience` + the ambience duck + the `_fanfare()` pitch-scaled chime trick. `explore_listen_bloom` is the only visual. |
| **Q3** Breathing room | 2.5 s of nothing after each job, with her work still on screen | Extend the completion hold already added this session from 0.9 s to 2.5 s; delete the blank 1.0 s `phase_gap`. **Zero art, and the cheapest win in the design.** |
| **Q4** The held shot at the theft | 1.5 s hold, music out, before the chase arms | The existing theft-flee tween. **Zero art.** |
| **H2** Show me | Tap the helper, he names the nearest undiscovered detail | `_bounce_actor` + `show_msg` + `explore_found_twinkle`. The optional point pose is P3. |
| **H3** Carry it together | Helper fetches a far favour and hands it over | The shipped gift-flight tween + the helper's own walk + two bounces. **Zero art.** |
| **H4** Sit with me | He sits when she sits; nothing happens; nothing is asked | Q1 + the helper's `ActorMotion` + `explore_rest_cushion`. **The beat the owner is actually asking for, made of two existing TextureRects and a timer.** |
| **H5** The helper's wish | At the curtain call he says why it matters to him | `celebrate()` + `show_msg` + one bounce. **The thirteen lines are already written.** |
| **X1** The world remembers | Touched details keep a faint permanent glint | The lens found-state draw, verbatim, moved to `discovery_layer` + `explore_found_twinkle`. **Zero art.** |

### Do not commission — explicit exclusions

1. **Per-career response sprites for the 104 clue spots.** The painting is
   the sprite. 13 × 8 = 104 responsive details for **zero new assets** is the
   central economy of this design; commissioning sprites for them would
   replace the child's own painting with a sticker.
2. **The three painter easel pictures.** Drop the shipped
   `goal_<career>.png` cards into the frames.
3. **A re-render of the 104 world/stage tiles to remove the bleed margin.**
   Four lines of code. See §1 P0.
4. **Any HUD, counter, collection strip, badge or progress bar.** Favours
   orbit her body. This session's entire framing effort was spent removing
   chrome from 50.8% of the screen; adding a collection UI would spend it
   back.
5. **A magnifier, a station marker, a task-card frame, a bop puff, a dust
   puff, dizzy stars, a stolen sparkle, a telegraph ring, a slash arc, a
   telegraph bang, or any `goal_<career>` prop.** All thirteen goal props and
   all seven FX **already ship** in `assets/opera/worlds/props/` and
   `assets/opera/worlds/ui/`.
6. **Costumed Roshan gesture atlases for T3.** The correct ask is `sheet_c`
   in the animation package (section 6), not a variant here.
7. **Anything under `assets/characters/friends/`, `assets/book/` or
   `assets/audio/voices/`.** Protected zones.

---

## 6. INTEGRATION WITH THE TWO OPEN HANDOFFS

### The three packages, and why they do not collide

| Package | Files | Where it draws | State it plays in |
|---|---|---:|---|
| **Widget art** (`CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`) | **221 ledger rows** — 151 REPLACE, 70 NEW; P1 8 / P2 27 / P3 180 / P4 6 | Inside the task card (the gesture surface rect) | **TASK** only |
| **Roshan animation** (`CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md`) | **26 sheets** — 13 × `sheet_a` 2048x2048 4x4, 13 × `sheet_b` 2048x1024 4x2 | The player actor, everywhere | all states |
| **Exploration** (this file) | **56 new files** (57 rows) | The painting, the actors' layer, the discovery layer | **WANDER** and curtain call |

**The widget and exploration packages occupy disjoint screen regions and
disjoint engine states, and neither blocks the other. Run them in parallel.**
The exploration layer is live only while no card is open; the widget art is
visible only while one is. The one shared constraint between them is the
**green lock** (§3.0) — the exploration package must stay off green so the
widget layer's go-zone signal survives.

**The animation package is the one true shared dependency**, in one
direction only: exploration ships without it and gets visibly better with it.

### One new item this design adds to the animation package

`CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md` already predicted it:
*"if the slow-exploration direction lands, add a `sheet_c`."* It has landed.

- **`roshan_<career>_sheet_c.png` — 2048x1024, 4x2 grid of 512x512 cells, 13 files, ~1.5 MB each.**
  - Row 0: **LOOK / POINT** — four chronological keyframes of her turning toward and indicating a painted detail (serves **T3**, and H2 when she is the one who spots it).
  - Row 1: **SIT / REST** — four keyframes of settling down and breathing (serves **Q1** and **H4**).
  - Same content locks as sheets a and b: identity per the accepted
    `roshan_<career>.png` costume portraits, rainbow tail always, **never
    legs**, consistent cell anchor with feet-or-tail contact on a common
    baseline, transparent background, POT canvas, `compress/mode=0`.

**T3 and Q1 ship without `sheet_c`** on `ActorMotion` transforms — a 0.07 rad
lean, a 10 px hop, a 1.06 squash-settle, plus `explore_rest_cushion` for the
sit. That is why `sheet_c` is last in the build order.

### Generation order across all three packages

| # | Do | Package | Why here |
|---|---|---|---|
| 0 | **Coordinate re-derivation** (7 replaced careers' paths/stations/clue spots; the 0.10+0.80× transform; `WORKBENCH` and nursery `PATHS` rows) | *engine/data, ours* | Not art, but it gates *placement* of everything in §3.5. Runs in parallel with all generation below. |
| 1 | **Widget P1** (8 rows) | widget | 151 files are on disk and wrong; these eight are the ones the owner playtested. |
| 2 | **Exploration P1** (6 files) | **this** | Smallest file count in the whole programme, largest coverage: 6 shared files unlock 104 painted details across 13 careers. Nothing else in this package is blocked by anything. |
| 3 | **`roshan_chef_sheet_a`** (1 file) | animation | The style proof for the 26-sheet set, on the beat the owner playtested. |
| 4 | **Exploration P2** (14 files) | **this** | Includes the 4 Path-B helper cards — the only rows in this package that block whole careers. |
| 5 | **Widget P2** (27 rows) | widget | |
| 6 | **Animation sheets a + b** (remaining 25) | animation | |
| 7 | **Exploration P3** (36 files) | **this** | Upgrades to things that already work. |
| 8 | **Widget P3 + P4** (186 rows) | widget | The long tail. |
| 9 | **`roshan_<career>_sheet_c`** (13 files) | animation | T3/Q1/H4 already play without it. Last. |

### Dependencies, stated explicitly

- `helper_<career>.png` **depends on** the `helper_actor` engine slot
  (~12 lines, already specified in `CHAPTER2_BIBLE_ACT_SCRIPTS` §(d)). The
  art may be generated before the slot exists — the engine hides the actor
  when the file is missing, so a promoted card with no slot is inert, not
  broken. It is **not** an orphan under the no-orphans rule provided the slot
  lands in the same workstream.
- `explore_sprout` and `explore_curtain_open` **depend on** step 0 for the
  seven replaced careers — they anchor to specific painted beds, booths and
  doors. Generate freely; promote after the re-derivation.
- `explore_favour_<career>.png` **depends on** the `FAVOUR` data table and its
  `opera_pantry` keys. Data, ours, trivial.
- **Nothing in Family A depends on anything.** Six files, no coordinates, no
  tables, no engine slot beyond a draw call.
- `roshan_<career>_sheet_c` depends on nothing; it improves T3, Q1 and H4.

### Total outstanding across all three packages

| Package | Files |
|---|---:|
| Widget art (221 rows, 1 per file) | **221** |
| Roshan animation, sheets a + b | **26** |
| Roshan animation, sheet c (**newly requested here**) | **13** |
| Exploration layer (this file, new files only) | **56** |
| **TOTAL OUTSTANDING** | **316** |
| (+ REUSE rows requiring no generation) | 1 |

**Of the 316, this package is 56 — 17.7% of the remaining programme — and it
is the one that answers the owner's actual note.** Its 18 shared files carry
234 career-slots, which is the highest coverage-per-file ratio of the three.

---

## 7. ACCEPTANCE

### 7.1 The house gate (unchanged, binding)

Computer ceiling 4.9/5; **pass ≥ 4.5, target ≥ 4.7**.

| Criterion | Weight |
|---|---|
| Style/palette | 25% |
| Child-readable silhouette | 20% |
| Job/mechanic continuity | 20% |
| Roshan identity / prop cohesion | 15% |
| Modelability / mobile practicality | 10% |
| Completeness / uniqueness | 10% |

**Automatic-rejection list (verbatim):** wrong job/mechanic, boss content out
of scope, realistic rendering, human legs on Roshan, wrong species/order/
state, text-heavy signage, copied third-party imagery, clipped cells,
repeated filler, off-palette dominance, micro-detail unmodelable on Mobile.

**Staging protocol:** candidates to
`assets_src/concepts/opera_exploration_2026-08-03/cards/` under the same
asset_id filenames, contact sheets, `PROMPTS.md` with exact prompts and
provenance, one ledger row per candidate (asset_id, family, reference path,
prompt revision, generation id, native dimensions, score, status, rejection
reason). Rejected candidates stay in the ledger; rejected files never enter
the repo proper. One controlled promotion commit. One `ASSET_LICENSES.md`
line per accepted asset. No `final2`/`better` filenames.

**Delivery report:** branch + SHA, reuse/regen/reject/accept counts, native
resolution confirmation, per-family counts, min/max/mean scores, promoted
paths, deferred assets, license updates, CI run URL.

### 7.2 Gates specific to world-response art

These are additional and **any one of them failing is a rejection**, whatever
the weighted score says. They exist because this package is the first one in
the programme whose art is drawn **on top of finished paintings** rather than
inside a card, and the failure modes are different.

**G1 — The thirteen-painting sweep (replaces the usual single QA render).**
"Candidates without runtime captures cap at 2/5" is a house rule; for this
package a runtime capture on a neutral field is worth **nothing**. Every
shared file must be captured **on at least three real career paintings**,
drawn at a real clue-spot coordinate, on the Mobile renderer, at 1280x720:
- **chef** — the warm, busy, high-detail baseline
- **detective** — the night district; the hardest place for a pale effect
- **magician** or **popstar** — daylit water / rainbow; the hardest place for
  a saturated effect

**G2 — Reads at the painted scale.** The effect must be unambiguous at its
real on-screen size and must not become a featureless white blob when the
engine scales it up. Specific sizes to check: `explore_favour_pouch` at
**34 px** (its orbit size); `explore_breadcrumb` at **24–32 px**; helper
cards at **190 px**; `explore_found_twinkle` from **96 px to 256 px**;
`explore_touch_ring` across its full **0.3 → 1.4** scale sweep.

**G3 — Does not fight the painting's own light.** No baked shadow, no
vignette, no directional highlight, no hard rim on any shared effect. The
thirteen paintings carry thirteen different baked light directions; an
effect that brings its own will be wrong on at least ten of them. Warm and
cool glow variants are **both** required for exactly this reason — a single
"neutral" glow that satisfies neither is a rejection, not a compromise.

**G4 — The green lock.** No exploration asset carries green in any quantity.
Verify by sampling: no accepted file may contain pixels in the reserved
success-green family (≈ RGB 117,240,158 ± a generous radius) above trace
level. This protects the anti-mashing signal across all 60 widget phases and
is non-negotiable.

**G5 — Transparent where the painting shows through.** Every overlay that
sits on a painted object — `explore_touch_ring`, `explore_dwell_arc`,
`explore_here_ring`, `explore_curtain_open`, `explore_prop_mat`,
`explore_listen_bloom` — must have a genuinely transparent centre with a
feathered inner falloff. A translucent-but-filled centre greys out the
painted detail the child touched, which inverts the entire point of the
layer.

**G6 — Survives the stage swap.** `backdrop_node.set_stage()` replaces the
district tiles with `stage_<career>_c*r*.png` at the theft. Anything that
plays at the curtain call — `explore_favour_pouch`, `explore_favour_glint`,
`explore_found_twinkle`, `explore_prop_mat`, the helper cards — must be
captured on **both** tile sets. The stage palette is a different world.

**G7 — Actor contract (helpers and the peeking imp).** Silhouette legible at
190 px; feet-or-tail contact on a **common baseline** across the whole family
so `_place_on_stage`'s depth term does not make figures bob relative to one
another; no baked ground shadow; body proportion matched to
`rival_<career>.png` so the runtime holds Roshan at ~1.3× a helper and never
above 1.5×; `imp_mischief_peek`'s bottom crop must be a **flat horizontal
edge** so it reads as occluded wherever it is placed.

**G8 — Protected zones untouched.** No candidate, at any stage, writes to,
overwrites or "improves" anything in `assets/characters/friends/`,
`assets/book/` or `assets/audio/voices/`. Helper identity is taken **from**
the protected cutout **as reference**; the output lands only at
`assets/opera/worlds/actors/helper_<career>.png`. The shipped precedent is
`faron_nursery.png`. Violation is an automatic rejection regardless of score.

**G9 — Species and identity locks.** Lamba is the **round white lamb**
(`assets/characters/lamb_0.png`), never a rabbit or bunny-fish. Mewsha is a
**cat in a round fishbowl helmet**. IMP-IDENTITY applies to both imp poses in
full: striped curled horns both visible, amber eyes, friendly fangs, and
**absolutely no shell, pearl, scallop, marine badge, crest, medallion or
target motif on any imp, ever.**

---

## 8. FILES REFERENCED (absolute)

Repo root: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/`

**Design and audit**
- `.../CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`
- `.../CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md`
- `.../OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md`
- `.../OPERA_FRAMING_PACING_ANIMATION_AUDIT_2026-08-03.md`
- `.../CHAPTER2_PARTY_ROLES_2026-08-03.md`
- `.../CHAPTER2_BIBLE_ACT_SCRIPTS_2026-08-03.md`
- `.../assets/ART_GENERATION_CONTRACT.md`

**Code the design binds to**
- `.../scripts/opera_career_world_2d.gd` (1755 lines)
- `.../scripts/opera_stage_paths.gd` (279 lines — `PATHS`, `roam_range:178`, `path_points:190`, `stations:198`, `clue_spots:220`, `point_along:245`, `nearest_t:261`)
- `.../scripts/opera_world_backdrop_2d.gd` (420 lines — `_load_tile_set:50`, `_draw:98`)
- `.../scripts/audio_director.gd` (`_speaker_key:95-113` — all 13 helper names verified routed)
- `.../scripts/main.gd:295` (`opera_pantry`), `.../scripts/save_state.gd`, `.../scripts/opera_act.gd:1558/3219`
- `.../scripts/arena/castle_rooms_25d.gd:1445-1465` (the hit-test-before-walk order this layer mirrors)

**Ledgers**
- `.../assets_src/concepts/OPERA_WIDGET_ASSET_LEDGER_2026-08-03.csv` (221 rows)
- `.../assets_src/concepts/OPERA_EXPLORATION_ASSET_LEDGER_2026-08-03.csv` (57 rows — this package)

**Assets that already ship and must not be re-commissioned**
- `.../assets/opera/worlds/props/` — `fx_bop_puff.png` (512²), `fx_dust_puff.png` (256²), `fx_dizzy_stars.png` (256²), `fx_stolen_sparkle.png` (128²), `fx_telegraph_ring.png` (512²), `fx_telegraph_bang.png` (128x256), `fx_slash_arc.png` (512x256), `goal_<career>.png` ×13 (512²)
- `.../assets/opera/worlds/ui/` — `magnifier.png` (512²), `station_marker.png` (512x1024), `task_card_frame.png` (1024²)
- `.../assets/opera/worlds/actors/` — `imp_mischief_taunt.png`, `imp_mischief_flee.png` and 9 more imp poses, `imp_captain_*` ×11, `rival_<career>_*` ×13 careers, `roshan_<career>.png` ×13, `faron_nursery.png` (all 512²)
- `.../assets/opera/worlds/backdrops/` — 52 `world_<career>_c*r*.png` + 52 `stage_<career>_c*r*.png`
- `.../assets/opera/worlds/widgets/` — 154 files already promoted from the widget package
