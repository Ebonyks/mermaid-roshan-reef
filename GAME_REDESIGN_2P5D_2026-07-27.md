# Game redesign charter — the 2.5D storybook promenade (2026-07-27)

## Owner decision (2026-07-27, binding)

The game gets a **fundamental redesign to 2.5D**, with a **heavy emphasis on
background sprites**, for three reasons stated by the owner:

1. **Navigation** — free-roam 3D is too easy to get lost in.
2. **Camera** — a chased 3D camera is a problem to manage; a staged side-on
   camera is not.
3. **Accessibility** — the analog-stick design is too ambitious for a
   4-year-old; it is not appropriate for the age group.

And one production decision: **Codex, as the generator of 2D art, takes a
greater role — Codex 2D art is higher quality than our Blender/Meshy 3D
assets and becomes the primary art channel.**

### What this supersedes

- **NPC_3D_WORKORDER_2026-07-19 (gen2 Meshy character migration): PAUSED.**
  No new 3D character conversions. Illustrated cutouts/billboards remain the
  character medium (they were always the shipped fallback; they are now the
  target). Existing landed .glb characters stay until their zone migrates.
- **Analog stick as primary input: demoted.** The virtual stick becomes an
  accessibility *fallback* (and the desktop/pad path), not the thing the
  child is expected to master. Touch-the-world is the primary grammar.
- The free-swim 3D world as the game's spine. Zone by zone it is replaced by
  **2.5D promenade stages** (below); the 3D world remains shipped per zone
  until that zone's promenade passes the device test.

### What this does NOT change (still binding)

- All CLAUDE.md hard rules: mobile renderer everywhere, no fail states,
  voice + pointer objectives, save-key compatibility, texture/audio budgets,
  ASSET_LICENSES.md discipline, protected book art / family voices / friend
  cutouts.
- The MiniGame contract and engine set (MINIGAME_ENGINES.md). This redesign
  *promotes* E2 from minigame engine to world engine; it does not replace
  the engine architecture.
- The Hybrid Touch interaction grammar (TOUCH_CENTRIC_REVERSIBLE_HANDOFF
  _2026-07-25.md): discover ring → gold-ring acknowledge → approach →
  ready → act. That language survives unchanged — it just plays out on a
  plane instead of in a volume, which makes every one of its hard problems
  (occlusion, depth misses, wedged approaches) easier or moot.
- Probe gating and the reversibility culture. Every phase lands behind a
  green CI probe run; the shipped world stays playable throughout.

---

## 1. The target shape of the game

**The world becomes a connected set of 2.5D promenade stages** — think
storybook diorama pages the child walks across — built on the E2
`SideScrollStage` engine's depth-band walk mode (the Castle Crashers rig
that already ships in the toy-castle brawler).

Each promenade is:

- **A parallax flat stack** (the "heavy emphasis on background sprites"):
  4–5 Codex-painted layers — sky, far silhouettes, mid dressing, play-plane
  skirt, sparse foreground vignette — sliding at different rates as the
  camera glides. Specs and per-zone shot lists:
  CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md.
- **A play plane**: the real rigged 3D Roshan (wardrobe intact) walking a
  wide x-band with a shallow z-band, exactly the brawl-mode kinematics. 3D
  is retained ONLY where it pays: Roshan herself, her animation/wardrobe,
  and hand-tuned rail modes (kart). Everything else on the plane is flat
  art: cutout friends, sprite props, painted landmarks.
- **A fixed side-on camera**: E2's `_glide_camera` — gentle follow, slight
  breathing, zero player camera control. The camera problem is deleted, not
  managed.
- **Edge exits and door cards**: stages connect left/right (and via marked
  archway sprites) into a linear-with-branches map. You cannot be lost on a
  line: off-screen objectives get the existing golden pointer plus a
  screen-edge arrow, and every exit is an oversized, wordless picture.

### The layering rule (owner note, 2026-07-27 — binding on all stage art)

The heart of the look is **clear, intentional layering of 2D designs in 3D
space**. A stage set is never one painting. Every design is broken down
into depth-classed pieces, each with a deliberate z home, so that as
Roshan moves through the walk band her occlusion against the world always
makes sense:

1. **Background murals** — behind the band, can never overlap Roshan.
   These are the parallax `layers` (sky/far/mid/skirt).
2. **Play-band standees** — individual cutout sprites standing at a real
   depth inside or around the band (a coral head, a market counter, a
   lamp post, a door card). Roshan passes **in front of or behind** each
   one depending on her z, sorted by the real depth buffer — this is what
   makes her interaction with the stage and its objects read true. Engine
   primitive: `SideScrollStage.flat()` (alpha-scissor, depth-writing,
   contact shadow).
3. **Foreground occluders** — past the band, between her and the camera;
   she always passes behind them. Sparse framing only.

Corollary for all art orders: **anything Roshan can tap, pass, or stand
behind ships as its own sprite with its own depth — never baked into a
mural.** A mural that paints a "prop" at band depth is a layering bug.

### The visual north star (owner decision 2026-07-27)

**A modernized, happy, 4-year-old Curse of Monkey Island.** CMI is the
staging and rendering reference for the promenade world — reference only:
no Monkey Island / LucasArts assets, characters, designs, or music, ever.

What we take from it:

- **Painted light.** Light pools, god rays, glowing windows and lantern
  warmth are painted into the murals — never runtime lights. (This is the
  no-new-OmniLights rule wearing a costume.)
- **Atmospheric recession.** Every layer back gets cooler, hazier, less
  saturated and softer-edged; saturation and contrast peak exactly at the
  walk band. The tappable plane is always the most vivid thing on screen —
  the look rule doubles as the accessibility rule.
- **Cel-vs-background separation.** Crisp outlined standees and characters
  pop off soft-edged painterly murals (already enforced by the
  scissor-vs-alpha split in the layer spec).
- **Theatrical staging.** Big readable silhouettes, oversized props,
  walk-behind foreground pieces, one dominant hue per scene with one
  accent (each Codex batch declares its color script).
- **Stepped motion.** Transform animation samples a ~10 fps clock
  (engine: `dress_tick`) so tweened sway and bob read as hand-drawn cel
  animation instead of screensaver-smooth interpolation. Costs nothing.

What we invert for the four-year-old: grime becomes pastel candy, menace
becomes cozy, night is bioluminescent-magical rather than gloomy, and
nothing at child eye level is ever scary. Modernized means clean crisp
edges at native resolution, generous color, and the existing pastel toy
palette — CMI's composition and light, never its texture of danger.

### The animation ladder (resource law for all stage art)

Codex paintings are the scarce resource; frames are paintings. Every
moving thing uses the cheapest tier that reads:

- **Tier 0 — animate the quad** (default for ALL standees): idle bob,
  pendulum sway, squash-and-stretch on tap. Zero art frames.
- **Tier 1 — shared shaders**: one vertex-sway material for foliage-class
  standees, UV-scroll for bubbles/water, emissive pulse. Zero art frames.
- **Tier 2 — paper-doll parts** (new named characters and hero props):
  one character painted as 4–6 pieces, joints tweened by the engine;
  animations are reusable across any character on the same rig. One
  painting buys unlimited motion. The whole part set fits one 512×512
  sheet.
- **Tier 3 — flipbooks, last resort**: ≤4 frames, ≤256 px per frame, only
  the region that changes (a blink card, a splash) — never a full
  character. One 8-frame 1024² flipbook costs more VRAM than a whole
  zone's murals; that budget mistake is banned by rule.

**The resolution split (owner rule 2026-07-27).** The big canvases belong
to still art only: full mural sizes and the 1024-px standee allowance are
reserved for **unanimated** background art. Anything animated in-game —
paper-doll parts, interactive-prop state cards, flipbook frames — ships
much lower: 256 px is the default, 512 px longest side is the hard
ceiling, and one item's entire animated set (all parts, states and frames
together) must fit a single 512×512 sheet. Transform-only motion (Tier
0/1) doesn't count against this — a swaying kelp standee is still one
still painting, only the quad moves — so it keeps the static allowance.

Protected friend cutouts and book art stay Tier 0 + sparkle overlays
(they may never be cut apart or repainted). Roshan herself remains the
rigged 3D model — the one constant high-quality mover, free of charge.

### The control grammar (replaces the stick)

One finger, two ideas, nothing else:

1. **Touch the world and Roshan goes there.** Tap — she travels to that
   spot and stops (the goal persists to arrival, same assisted-travel
   contract as Hybrid). Hold — she keeps following the finger. The press is
   projected onto the play plane: x free, screen height mapped into the
   depth band. No stick, no dead-zones, no thumb coordination. This is
   `walk_tick` in the E2 engine (shipped this branch, §4).
2. **Tap a thing to use it.** Unchanged Hybrid grammar: rings, second tap
   or the big pictogram button to act. Taps and holds are disambiguated the
   way the touch router already does (a tap on a registered target wins;
   a hold on open ground is travel).
3. **Tap = THE button** inside games, as today.

The virtual stick and pad/keyboard remain functional behind the same
composite reads (Classic toggle keeps its meaning) — fallback, not
curriculum.

---

## 2. Zone migration map

Order chosen so the cheapest, highest-traffic spaces prove the rig first,
and the hardest (most 3D-entangled) go last. Each zone = its own work
branch, its own Codex flat set, its own probe, merged to dev only green.

| # | Zone (today) | Becomes | Notes |
|---|---|---|---|
| 1 | **Reef home** (free-swim) | Reef Promenade — the pilot | Friends, Manta Pearl Shop, wreck cave, den, brawler & race doors as stage targets. Proves the whole rig. |
| 2 | **Castle hall floors** | One promenade per floor; stairs = door cards | Bed, wardrobe, easel, bells, chest, dungeon/opera doors. Interiors are the easiest flats. |
| 3 | **Courtyard** | Promenade; train keeps its rail | courtyard_train.gd already runs a rail — it becomes set dressing + ride target. |
| 4 | **Sky Lagoon** | 2–3 linked promenades (lagoon, alpine route, gates) | Replaces the longest get-lost route in the game. |
| 5 | **Northern kingdom** | Promenade chain | |
| 6 | **Ember Fortress / Butterfly World** | Promenades | Ember already has 2D concept art direction to reuse. |
| 7 | **Galaxy** | LAST, or retired to a picture-game | The one true 3D one-off; owner call when we get there. |

### Minigame inventory under the redesign

Most games already comply — the engine consolidation did the work:

- **Already 2.5D/staged, keep as-is:** dolls (E2 catch), toy-castle brawler
  (E2 brawl), opera acts (staged sets + flat art), dance, picture games ×5
  (K2 canvas), fairy pond (E3 overhead — staged, fixed camera).
- **Rail modes, keep (fixed camera, one verb):** kart/races (E4), penguin &
  rainbow slides, courtyard train ride.
- **Free-swim-dependent, restage onto engines when their zone migrates:**
  fetch → E2 stage (aim/throw on the plane); seek → promenade hide-spots
  (tap the giggling coral); treasure/melody/collection → K1 collect chains
  along promenades; shop → flat shop interior (tap shelves, already
  proximity+tap); combat arena & dungeon rooms → E1 RoomStage as planned
  (overhead octagon is already a fixed-camera stage; unchanged by this
  charter).
- **Stuffie battle:** already an overhead fixed-camera stage with one
  button + QTE — compliant, untouched.

---

## 3. Phases (each probe-gated, each reversible)

- **P0 — this branch.** Charter + Codex work order + CLAUDE.md decision
  record + P1 engine foundations. No behavior change to any shipped mode.
- **P1 — engine foundations (this branch, code).** In `side_scroll.gd`:
  parallax `layers` stack in `open()` + camera-locked layer glide, and
  `walk_tick()` — the touch-the-world promenade mode (press-point-projected
  travel with stick/pad/keys fallback merged in). Additive; dolls and brawl
  tick paths untouched, existing probes must stay green to prove it.
- **P2 — Reef Promenade pilot.** New satellite `scripts/promenade.gd`
  (RefCounted, state on main) hosting zone configs; the reef promenade
  reachable behind an additive save key `world_style` (`"classic"` default
  until sign-off, `"storybook"` = the new world), toggled from the pause
  menu like Hybrid/Classic. Placeholder gradient flats until Codex batch 1
  lands; cutout friends registered as tap targets through the existing
  interaction registry. New trusted probe `probe_promenade.gd`: walk both
  directions, tap-travel, enter/exit one activity and one door, plus a
  passive leg (nothing may be won by watching). ci.sh gains the probe.
- **P3 — Codex batch 1 integration + device test.** Real reef flats in,
  M11 device pass per the mandatory human-test protocol (frame pacing,
  overdraw at Speedy tier, first-tap comprehension by the intended child).
  `world_style` flips default to `storybook` for the reef only after
  sign-off.
- **P4+ — zone-by-zone** per the table above, one zone per branch, each
  with its Codex set, probe, and device pass. Free-swim code for a migrated
  zone is retired (attic'd, not deleted) one full promotion cycle later.
- **P-final — stick demotion.** Once every routine destination is
  reachable by touch-the-world, the virtual stick stops auto-showing
  (remains as the accessibility/pad path and in Classic).

### Success criteria (how we know the redesign worked)

- The child can get from wake-up to any friend and back **unprompted, with
  one finger, no adult, no reading** — the P3/P4 device tests measure
  exactly this, per zone.
- Zero camera management anywhere in the shipped path.
- Passive runs still win nothing (probe_passive extends to promenades).
- Frame pacing on the M11 at Speedy tier is no worse than the 3D reef
  (flats must be mostly opaque; alpha overdraw is the one new perf risk —
  budget in the Codex work order).

## 4. Engine notes (what landed in P1)

`SideScrollStage.open()` now takes an optional `"layers"` array (back-to-
front flat stack; each `{tex, size, y, z, lock}` where `lock` ∈ [0,1] is
the camera-follow factor — 0 pinned to the stage, 1 riding the camera like
a sky). The old single `backdrop` key is unchanged and equivalent to one
layer with `lock: 0`. `_glide_camera` slides locked layers with its follow
point, which is the entire parallax implementation — no per-frame game
code.

`walk_tick(delta)` is the promenade verb: merged composite input
(keys ∥ pad ∥ virtual stick) as a velocity, OR press-and-point — the finger
cast as a camera ray onto the vertical stage plane, with screen height
remapped into the depth band (`band_h`), Roshan moving toward that goal and
stopping inside `arrive_r`. The goal persists after release until arrival
(tap-to-travel); any manual axis input cancels it instantly and steers
directly, matching the Hybrid rule that the stick always overrides assisted
travel. Returns `{px, pz, moved, pointing, arrived}`; no tap semantics — in
the world, tap belongs to the interaction director.

Risks called out honestly: probe rewrites are the largest engineering cost
of P4+ (every navigation bot assumption changes per zone); Mali overdraw
from big transparent quads is the perf risk (mitigated by opaque-first
layer specs); and Codex throughput is the schedule risk — which is why the
work order ships today, before any zone needs it.
