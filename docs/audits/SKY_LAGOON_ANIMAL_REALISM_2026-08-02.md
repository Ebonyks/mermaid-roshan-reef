# Sky Lagoon animal realism audit

Date: 2026-08-02
Target: `scripts/arena/sky_lagoon_promenade.gd`, the five ambient animals
Question asked: why do they read as animated cartoons instead of live animals,
and what is the best way to make the scene feel inhabited?

This is an audit only. **No runtime behaviour was changed by this commit.** The
tracked evidence is generated from the shipped art and the shipped constants by
`tools/audit_sky_lagoon_animal_realism.py`; the remediation plan at the end is a
proposal for a separate, probe-gated batch.

## What already exists, and what it proves

`docs/audits/SKY_LAGOON_ANIMALS_2026-08-01.md` is a good *implementation* audit:
it proves the five species exist, bind to one pooled card, light correctly by
day and night, keep clear of the route and the props, and exit toward authored
cover. `scripts/probe_sky_lagoon_animals.gd` enforces all of that.

None of those checks ask the question the owner is asking. A card can pass every
one of them and still read as a sticker being slid across a painting — which is
what is happening. The gap is deliberate scope, not oversight: the previous pass
audited *placement and lighting*, this one audits *life*.

## Method

Static analysis of the shipped assets against the shipped camera model. No
Godot, display, or capture is required, so it runs in this environment and in
CI:

```
python3 tools/audit_sky_lagoon_animal_realism.py \
  --json-out  docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02_METRICS.json \
  --sheet-out docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02_FOOTING.jpg
```

It measures, per species: alpha geometry of all four poses in both atlases;
apparent on-screen size against Roshan's card; whether the lens can ever reach
the animal's habitat page on a given device aspect; how far the card slides
against its painted footing; what the panorama actually paints under each
authored foot baseline; and the authored speeds restated in body lengths per
second with the exact patrol cycle time. Behavioural findings below are read directly from
`_tick_animal_idle`, `_tick_animal_startle`, `_tick_animals`, and `_bind_animal`.

## Executive summary — findings ranked by how much they cost the illusion

| # | Finding | Severity | Where |
|---|---|---|---|
| 1 | Above 19.3:9 — most modern phones — three of the five species can never appear at all | Critical | camera pan clamp |
| 2 | Not one animal stands on painted ground — they stand on a rope rail or on shrub canopy | Critical | authored paths |
| 3 | The card slides up to ~9 world units across its own painted footing as the lens pans | High | no mural socket |
| 4 | Uncontrolled per-pose baseline drift in the atlases is up to 17× the authored bob | High | atlas geometry |
| 5 | Every animal runs one fixed, frame-identical patrol loop forever — 13.5 s to 24.4 s | High | idle state machine |
| 6 | Travel is 0.21–0.49 body lengths/s: a fifth of a slow walk, at constant velocity | High | `speed`, `move_toward` |
| 7 | Hopping animals glide: forward motion is continuous, the "hop" is a decoupled sine | High | `bob` |
| 8 | The animals never once acknowledge Roshan, each other, or the wind | High | no awareness model |
| 9 | Absolute stillness while paused — a static bitmap, no breath, no ear, no tail | Medium | pause state |
| 10 | One startle script for five species; a raccoon flees like a hare | Medium | `_tick_animal_startle` |
| 11 | Night is a colour grade only — nocturnal and diurnal species behave identically | Medium | `_animal_tint` |
| 12 | Zero animal audio, and the one sound cue that does fire is a sparkle burst | Medium | `_startle_animal` |
| 13 | Animals pop in and out of existence in the middle of the frame | Medium | `_hide_animal` |
| 14 | Apparent scale is wrong and inverted: the frog is nearly as big as the otter | Medium | `height` |
| 15 | The audit probe validates the animals from a camera position the game cannot produce | High (process) | `probe_sky_lagoon_animals.gd` |

Findings 1, 2, 3 and 15 are the ones to fix first. They are not "polish" — they
are the reason the current animals cannot look alive no matter how good the
behaviour code becomes.

---

## 1. Three of five species never appear on a modern phone

`SideScrollStage.screen_pan_limit` forbids the lens from panning off the mural,
so the camera x is clamped to `±(72 − frustum_half_width_at_backdrop)`. The
frustum width grows with the device aspect ratio (base 1280×720,
`canvas_items`/`expand`), so the wider the phone, the *less* the camera may pan.

`_animal_page_index()` derives the habitat page from the camera x, in 48-unit
pages. Page 0 needs camera x ≤ −24 and page 2 needs camera x ≥ +24.

| Aspect | Pan limit | Pages reachable | Species that can never be framed |
|---|---|---|---|
| 16:9 | ±32.2 | 0, 1, 2 | — |
| 18:9 | ±27.2 | 0, 1, 2 | — |
| 19:9 | ±24.8 | 0, 1, 2 | — |
| **19.5:9** | ±23.5 | **1 only** | **otter, frog, raccoon** |
| **20:9** | ±22.3 | **1 only** | **otter, frog, raccoon** |
| 21:9 | ±19.8 | 1 only | otter, frog, raccoon |

The cutover is exact: **above 19.30:9, pages 0 and 2 become unreachable.**
Most Android phones sold since 2019 are 19.5:9 or 20:9, so the 3–4-year-old
target device is very likely on the wrong side of that line — worth confirming
against the actual handset before anything else, because if it is, the Sky Lagoon
has two animals and not five: a hare and a squirrel, alternating forever on the
same 3.5-unit patch of hedge.

That alone explains a large part of "they feel like a cartoon prop." There is no
variety to observe, because 60% of the roster is unreachable.

Even at 16:9 the shore is nearly unreachable in practice. The camera x window in
which the otter is fully framed *and* page 0 is active is 2.53 units wide out of
64.4 pannable units — Roshan has to be standing in the far-western 4% of her
walkable range. Frog 3.01 units, raccoon 8.20 units, against hare 35.00 and
squirrel 36.46.

**Root cause:** habitat pages are keyed to camera position over a span the camera
cannot cover, and the animals were authored at page centres (±48) that the lens
can never reach.

## 2. No animal stands on the ground

`_animal_path_is_safe()` enforces two things: ≥3.2 units of clearance from the
painted player route, and no waypoint inside a prop/seam exclusion rectangle.
It never asks the only question that matters for grounding — *is there painted
ground under the foot?*

The tracked contact sheet
(`SKY_LAGOON_ANIMAL_REALISM_2026-08-02_FOOTING.jpg`) draws each authored card box
in yellow and its foot baseline in red on the panorama:

- **otter, frog** — the foot baseline lands on the painted rope-and-post railing
  above the stepping stones. The otter walks *along the top of a rope fence*.
- **hare, squirrel** — feet at mid-height of the painted shrub mass, i.e. the
  hare stands on top of the hedge canopy, not on the lawn a few units below.
- **raccoon** — feet on top of the shrub bank beside the lake.

The sampled footing classification agrees: `stone/neutral` for the shore pair
(the rail posts), `vegetation` for the meadow pair, mixed for the raccoon.

An animal that is not in contact with the ground can never read as alive; the
brain rejects it before it evaluates the motion. This is finding #2 only because
finding #1 hides three of the five offenders on the real device.

**Root cause:** the paths were authored against a 2D exclusion mask, not against
the painted terrain. There is no ground-height function for the animal band the
way `_walk_y()` / `ROUTE_PAINTED` exist for Roshan.

## 3. The cards slide against the painting

Every ground-standing card in this stage is registered as a *mural socket*
(`_register_mural_socket`, `GROUND_SOCKET_LOCK`) precisely so it cannot drift
away from the painted spot it stands on as the lens pans: the playground, the
castle, the cabin smoke, the near tree. **The animal pool is never registered.**

An unlocked card at depth `z` slides against the backdrop by
`|1 − (47+18)/(47−z)|` units per unit of camera pan:

| Species | Slide per camera unit | Camera window (16:9) | Total slide | vs its own patrol length |
|---|---|---|---|---|
| hare | 0.255 | 35.00 | 8.92 | 2.55× |
| squirrel | 0.199 | 36.46 | 7.27 | 2.08× |
| raccoon | 0.204 | 8.20 | 1.67 | 0.33× |
| otter | 0.231 | 2.53 | 0.58 | 0.14× |
| frog | 0.224 | 3.01 | 0.67 | 0.18× |

The two species that are actually reachable on a phone are the two worst: the
hare slides nearly nine world units — two and a half times the length of its own
patrol — across the hedge it is nominally standing in, purely as a function of
Roshan walking past. It reads exactly as what it is: a sticker on a nearer sheet
of glass.

## 4. The atlases fight the animation

All ten atlases are 512×512 read as a 2×2 grid, so each pose is a 256 px cell.
`Sprite3D` is centred, so the *subject's* position inside its cell decides where
the feet are. That position is not consistent between poses:

| Species | Idle baseline drift | Startle baseline drift | Authored bob | Worst drift ÷ bob |
|---|---|---|---|---|
| otter | 0.315 u | 0.538 u | 0.045 | **12.0×** |
| raccoon | 0.328 u | 0.598 u | 0.035 | **17.1×** |
| squirrel | 0.317 u | 0.555 u | 0.055 | **10.1×** |
| hare | 0.182 u | 0.581 u | 0.12 | 4.8× |
| frog | 0.180 u | 0.148 u | 0.18 | 1.0× |

Subject height also drifts 9.9%–81.7% between poses of the same sheet. The
generation prompts asked for a consistent baseline and identical scale; the
generator did not deliver it, and the README's "no pose was individually moved"
means the drift went into the game unmeasured.

The consequence: the carefully authored 0.035–0.12 unit bob is invisible noise
under a 0.3–0.6 unit vertical jump that fires on every frame change, while the
contact shadow — correctly pinned to `route_position` — stays put. The animal
visibly detaches from its own shadow twice per second.

There is, however, a large budget hiding here. Displayed at 720p the idle poses
are 18–52 px tall, drawn from 100–211 px source subjects: **4.1× to 7.9× linear
oversampling.** The same 512×512 atlas re-cut as a 4×4 grid would give **16 poses
per sheet at zero VRAM cost** and still be 2–4× oversampled. Behavioural richness
here is a layout decision, not a memory decision.

## 5–7. The motion model

Read straight off `_tick_animal_idle`:

- **The patrol is a metronome.** Three waypoints, ping-ponged, constant speed via
  `move_toward`, and an identical `dwell_s` at every arrival. There is no random
  element anywhere in the loop. Full cycle time is fixed to the frame: otter
  21.8 s, frog 17.1 s, hare 17.0 s, squirrel 13.5 s, raccoon 24.4 s — repeated
  identically for as long as the child watches.
- **Every pause is the same pause.** `frame = 1 if pause_t > dwell*0.45 else 3`:
  sniff for 55% of the dwell, alert-glance for 45%, always, in that order.
- **Speed is a fifth of life.** In body lengths per second: raccoon 0.21, otter
  0.21, hare 0.27, squirrel 0.34, frog 0.49. A relaxed foraging mammal moves
  1–2 BL/s and a Douglas squirrel scampers in 4–8 BL/s bursts. The patrol spans
  1.4–2.5 body lengths total, so each animal is creeping back and forth inside a
  box barely longer than itself. The escape run, by contrast, is well judged at
  4.7–7.1 BL/s — it is the *approach* that is wrong, not the flight.
- **Hoppers glide.** Forward motion is continuous and the "hop" is
  `abs(sin(state_t * 8.5)) * bob` — a sine on its own clock, unrelated to the
  frame cadence (`state_t / frame_s`) and to distance travelled. Real saltatory
  locomotion is ballistic: push-off, airborne arc, landing, *pause*. Forward
  velocity should be zero between hops. As written the hare moonwalks and its
  feet never sync with the ground.
- **Facing snaps.** `flip_h` mirrors instantaneously at each waypoint reversal.
  Nothing turns; it simply becomes its own mirror image.
- **Acceleration does not exist.** Idle travel starts and stops at full speed;
  the escape run goes from 0 to 13.5 u/s in a single frame.

## 8–9. There is no awareness model, and no stillness

The animals have exactly two inputs: a tap within 114 px, and which page the
camera is on. They do not know Roshan exists. Measured against the painted route,
she can stand 5.3–6.5 world units from their feet — two body lengths, the same
frame, plainly visible — and the hare will keep sniffing the same hedge on the
same schedule. Living things track the moving thing in the scene; that single
missing cue probably costs more perceived life than any other behaviour on this
list.

Equally, nothing else in the world reaches them. The stage already runs a wind
model (`_wind_gust_at`, a 24 s cycle that bends the foliage cards); the animals
ignore it. They never react to each other (only one exists at a time), to the
pearl plane departing, to the castle door, or to the time of day.

And when an animal pauses it is a *perfectly static bitmap* — no breathing, no
ear flick, no tail. Absolute stillness is the single strongest "this is a decal"
signal available; real stillness is never still.

## 10. One startle script for five species

`ANIMAL_STARTLE_ALERT_S / SQUASH_S / HOP_S` are global constants: 0.24 / 0.18 /
0.24 for everything, then a flat constant-velocity run at `exit_speed`, always
toward `safe_exit = −1.0` (west) for every species, always at 100% probability,
regardless of how far away the tap was.

Ecologically these five animals have five different escape strategies: a tree
frog makes one large leap and is gone; a squirrel goes *up* and freezes on the
far side of a trunk; a hare explodes into a bounding zigzag then stops at cover
distance and looks back; an otter porpoises into water; a raccoon does not flee
at all — it looks up, holds, and ambles off unhurried. Giving all five the same
0.66 s wind-up and the same flat westward sprint is the most cartoon-like single
behaviour in the system.

The 114 px touch radius puts a 228 px target around a 48 px hare. That generosity is
correct for a four-year-old and should stay — but it means the animal currently
bolts from taps that are visually nowhere near it. Grading the response by tap
distance (far tap → freeze and look; near tap → flee) turns an accessibility
allowance into a realism feature at no cost to the child.

## 11. Night is a colour grade

`is_night` changes `modulate` and the shadow tint. Nothing else. The nocturnal
raccoon is equally likely at noon; the diurnal hare and squirrel are equally
active at midnight; the tree frog — which is essentially only findable at night
in the real Pacific Northwest — is a daytime shore animal here. Night is
reachable in-game (the castle bed calls `_set_night`), so a diel roster is a
real, cheap behavioural win: switch which species the page can bind rather than
only how it is tinted.

## 12. No sound, and the wrong effect

There is no animal audio at all. The only cues on activation are
`m._sparkle_burst(...)` — 36 unshaded cubes exploding upward in gold — and
Roshan's giggle. The giggle is right: the child's reaction is part of the scene.
The sparkle burst is the strongest cartoon signal in the whole feature; it is the
game's *reward* vocabulary, applied to a wild animal. A physical cue in its place
(a dust/leaf puff at the push-off point, and a shake of the cover it disappears
into) says "something living just went in there" instead of "you collected a
thing."

The audio bus already exists (`ambience_lagoon.ogg` via `audio_director`), and
one-shot `AudioStreamPlayer` cues are already used for hops and chimes. Adding a
short rustle, a splash, a frog chirp and a squirrel chatter is small, cheap, and
per byte the highest-yield realism item on this whole list.

## 13. Pop-in, pop-out

`_tick_animals` hides the animal the instant the camera crosses a page boundary,
with no regard for whether it is on screen. At 16:9 the boundary at camera
x = −24 sits with the hare only ~3 units from frame centre: one step west and a
fully visible, centre-frame hare vanishes. Coming back, `_bind_next_animal`
makes it reappear at `path[0]` at full opacity 0.7 s later. Arrivals and
departures are teleports; nothing ever *comes out of* or *goes into* cover
except during the tap escape.

The roster is also strictly round-robin (`cycles[page] % definitions.size()`), so
the order of appearances is fixed forever, and an animal that just fled returns
5.5 s later to the same spot, with the same wariness, having learned nothing.

## 14. Apparent scale

Assuming Roshan's 7.8-unit card is a 105 cm four-year-old:

| Species | Apparent | Real | Error |
|---|---|---|---|
| frog | 12.2 cm | 4.5 cm (tree frog) | **2.72×** |
| squirrel | 23.3 cm | 18 cm | 1.29× |
| hare | 28.7 cm | 32 cm | 0.90× |
| raccoon | 22.5 cm | 30 cm | 0.75× |
| otter | 14.7 cm | 30 cm | **0.49×** |

The absolute errors are survivable in a storybook; the *ordering* is not. In life
the otter and raccoon are the big animals and the frog is a thumbnail. In the
scene the frog is 83% of the otter's height. Relative scale is what a child reads,
and here it is inverted.

## 15. The probe tests a camera the game cannot produce

`probe_sky_lagoon_animals.gd::_move_to_page()` teleports the camera to
`ANIMAL_PAGE_CENTERS` = ±48, then validates binding, idle motion, lighting and
the startle sequence there. The live pan clamp is ±32.2 at best and ±22.3 on the
target phone, so **every page-0 and page-2 assertion is made from a camera
position the game can never reach.** The probe is green — and if the phone is
19.5:9 or wider, the raccoon has never once been on its screen.

Any remediation must fix the probe's framing model first, or it will keep
certifying an unreachable scene.

## What is right, and must survive any change

Do not regress these while chasing realism:

- one pooled `Sprite3D` and one pooled contact shadow, Speedy-tier safe;
- unshaded cards against flattened painted art, per-species day/night modulation
  and habitat-tinted shadows (the 2026-08-01 lighting audit measured this);
- the shadow pinned to `route_position` rather than to the bobbing card;
- clearance from the player route, the props, the seams and the castle approach;
- no fail state, no objective, no save-state consequence, no blocking of travel;
- a generous touch radius for a four-year-old's finger;
- determinism: the living-card gates compare placement/phase signatures across
  cold builds, so any variation added below must be *deterministic* pseudo-random
  (hash of page, cycle index, waypoint index — never `randf()`).

## Remediation plan

Ordered by illusion-per-unit-of-risk. Each item is one mechanical, revertible
commit under the `main.gd` refactor rules; state stays on `ReefMain.g`.

**R1 — Make the habitats reachable (blocks everything else).**
Decouple habitat selection from the 48-unit camera page. Bind on *visibility*:
an animal becomes eligible when its authored path is inside the current frustum
with margin, using `SideScrollStage.view_half_size` rather than a fixed page
width. Move the shore roster inward from x ≈ −62 to inside the reachable window
(≤ −29.7 at 16:9, ≤ −22.3 at 20:9) and the raccoon from x ≈ 29–34 likewise, or
widen `screen_pan_limit` for this stage. Update `_move_to_page` in the probe to
drive the *real* clamped camera and add a regression check across 16:9 / 19.5:9 /
20:9 that every species can be framed. This probe change is the explicit goal of
the task, so it is a permitted probe edit — call it out in the commit message.

**R2 — Ground them.** Add a painted-ground function for the animal band, the
analogue of `ROUTE_PAINTED`/`_walk_y()`: per-habitat ground polylines sampled
from the mural, with `_animal_path_is_safe` extended to reject any waypoint whose
foot is not on painted walkable ground. Re-author the five paths onto real
ground — the shore pair onto the stone/shingle between the rail and the water
(not the rail), the meadow pair onto the lawn *in front of* the hedge with the
hedge behind them as cover, the raccoon onto the shore rocks. Re-run the footing
sheet as the acceptance gate.

**R3 — Socket-lock the animal card.** `_register_mural_socket(card,
GROUND_SOCKET_LOCK)` on bind, and drive the card through
`_mural_anchored_position` each tick with the authored waypoint as the reference
position, exactly like the playground cards. Kills the 9-unit slide.

**R4 — Normalize the atlases.** Measure each cell's alpha bbox once, offline, and
bake a per-frame `offset` table (or re-emit the atlases with a common baseline
and a common subject height). `Sprite3D.offset` is free at runtime. This is a
prerequisite for any believable gait: no locomotion model survives a 0.6-unit
random vertical jitter.

**R5 — Rebuild the gait.** Ballistic hops for frog and hare: forward motion only
during the airborne arc, zero between; the arc, the frame index and the shadow
scale driven by one phase variable. Scamper bursts for the squirrel (0.4–0.9 s
dash at 3–5 BL/s, then a freeze). Continuous but 3–5× faster walk cycles for
otter and raccoon, with ease-in/ease-out at each waypoint and a 0.25–0.4 s body
turn instead of an instant `flip_h`.

**R6 — Give the idle loop a repertoire.** Replace the two-state loop with a small
weighted behaviour set per species — forage, vigilance scan, groom, brief bed —
chosen by a deterministic hash of `(species, cycle, step)`, with dwell times
drawn from a range instead of a constant, and a low-amplitude always-on breathing
(a ±1.5% `scale.y` at 0.25–0.4 Hz) so a paused animal is never a static bitmap.
The 4×4 atlas re-cut described in §4 pays for the extra poses at zero VRAM cost.

**R7 — Add awareness of Roshan.** One distance term drives everything: beyond
~14 units, normal behaviour; 8–14 units, head/body turns toward her and dwell
times lengthen (vigilance); under ~6 units, a deterministic decision to move a
short distance toward cover *without* the tap escape firing. A retreat that
happens because she walked close is the single most convincing thing an ambient
animal can do, and it costs one `absf(player.x − route_position.x)` per tick.

**R8 — Species-specific escapes, graded by distance.** Per-species alert latency
(frog ~0.12 s, squirrel ~0.15 s, hare ~0.2 s, otter ~0.25 s, raccoon ~0.6 s and
no sprint — a look, a hold, then an amble), per-species exit direction and shape
(frog: one leap into water; squirrel: up and out of frame; otter: into the pond
with a ripple; raccoon: unhurried, with a look back), and a graded response to
tap distance: far tap → freeze and look, near tap → flee. Keep the four-pose
alert/squash/hop reading — it is what makes the reaction legible to a
four-year-old — but let the timings differ.

**R9 — Entrances, exits and memory.** Enter from cover with a 0.25 s fade plus a
shake of the bush entered from, never mid-frame at full alpha; suppress the
page/visibility unbind while the animal is on screen (finish the behaviour, then
leave); randomize the return delay deterministically around 5.5 s; and carry a
per-page `startle_count` so a returning animal is warier — longer vigilance,
shorter approach, earlier exit. Habituation is cheap and reads as intelligence.

**R10 — Sound and world coupling.** Four short OGG cues (rustle, splash, chirp,
chatter) with ASSET_LICENSES lines in the same commit; a leaf/dust puff at the
push-off point replacing `_sparkle_burst` on activation; a shake of the cover
card the animal disappears into; and a small wind coupling so a gust
(`lagoon_wind_gust` > 1.2) makes a vigilant animal look up.

**R11 — Diel roster.** Bind by time of day: day → hare, squirrel, otter;
night → raccoon, frog, otter; with slower cadence and longer vigilance at night.
Keeps all five species, doubles the observed variety, and fixes the ecology for
free.

**R12 — Scale pass.** Bring the frog down to ~0.7 units of card height and the
otter up to ~3.4 so the ordering matches life. Re-run the lighting audit
afterwards — the composites in the 2026-08-01 JSON are size-sensitive.

R1–R4 are corrective and should land as one batch; they are what turn the
animals from decals into inhabitants. R5–R9 are the behavioural work the owner
is actually asking about, and they only pay off once R1–R4 are in. R10–R12 are
inexpensive and can land alongside.

## Reproducing the evidence

```
python3 tools/audit_sky_lagoon_animal_realism.py \
  --json-out  docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02_METRICS.json \
  --sheet-out docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02_FOOTING.jpg
```

Requires only Pillow and NumPy. All figures in this document come from that run
against the tracked panorama tiles, the tracked animal atlases, and the constants
in `scripts/arena/sky_lagoon_promenade.gd`; if those constants change, the tool's
mirrored block at the top of the file must be updated with them.

Two observations in this document are *not* covered by the tool and should be
confirmed in a real capture before being acted on: the painted light in the mural
reads as coming from the upper right (the rocks and shrubs carry their shading
low-left), while the pooled contact shadow is centred directly beneath the body,
i.e. lit from overhead; and the in-frame visibility of the page-boundary pop-out
described in §13 was derived from the frustum model rather than observed.
