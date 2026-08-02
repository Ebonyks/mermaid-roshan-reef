# Fable handoff — Pearl Castle animation & interactivity design brief

**Date:** 2026-07-29
**Author:** Fable (audit of `origin/dev` @ `223bfe82`)
**Audience:** Codex — design + implementation
**Scope:** the 2.5D Pearl Castle hub (`scripts/arena/castle_rooms_25d.gd`) — Main Hall
plus the seven destination rooms. Nothing outside the castle.
**Goal:** make the castle dramatically more interactive and alive for the player —
one specific 4-year-old, non-reader, one finger, short sessions, 3–4-year-old
Android phone (see AGENTS.md). More things to touch, and gentle ambient motion
that invites touching, without breaking the picture-first art rules or the
performance envelope.

---

## 1. Current state (verified against code, screenshots, and probes)

### 1.1 Architecture snapshot

- Everything is `Sprite3D` cards in front of one perspective `Camera3D`
  (`WORLD_ORIGIN` y=2000, camera z=18, FOV 58.109). No meshes, no models.
  Main Hall background tiles are the only shaded receivers (touch-lit hall);
  all other cards are unshaded (`castle_rooms_25d.gd:1-8`).
- **Main Hall** is one logical 3344×941 art space (two 1672×941 screens, 8
  native tiles). Roshan's foot X pans the camera. Depth Z bands: background 0,
  items 0.55, player 1.25–3.15, midground 2.0, foreground 4.0, effects 4.35.
- **Seven destination rooms** each: 2×2 background tiles (from 2K masters),
  optional midground (only `mermaid_pool` has one — the pool water card), two
  foreground occluder cards, three touch-prop cards, Roshan + contact shadow.
  Steady-state visible world cards per room ≈ 10–14 (probe-enforced in the
  hall at 14).
- **Touch input is castle-local.** A full-rect Control on CanvasLayer 14
  consumes taps (`_on_room_input` → walk). Items and doors are invisible
  `Button` hotspots, re-projected from the 3D cards every frame
  (`_update_touch_hotspot`), minimum size 112×112 stage px. The world systems
  (InteractionDirector, tap_move, hit_engines, verbs) are all disabled/dormant
  inside the castle — do not re-enable them; extend the local pattern.
- **Navigation:** tap-to-walk (walk Rect2 per room); 8 hall door/throne
  portals with walk-then-enter choreography; Storybook elevator (↕, bottom
  right) opens a 3×3 icon grid (8 rooms + disabled "Bedrooms are dreaming"
  moon tile); back button exits to the Sky Lagoon promenade
  (`_return_to_courtyard`). Entry is the promenade castle gate (tap-confirm or
  doorstep walk) → `_enter_castle_interior` → `open("main_hall")`.
- **Lighting toy (the current crown jewel):** 6 hall sconces toggle 4
  SpotLight3D clusters + ambient fill + glow/bloom sync
  (`_sync_hall_lighting`, `_sync_castle_environment`). Tapping sconces
  genuinely darkens/relights the hall. `quality == "speedy"` reduces glow and
  allows only one shadow-casting spot.
- **Audio:** items play pitched one-shots through one `AudioStreamPlayer`
  (`CastleRoomPropSfx`, SFX bus, −10 dB). Available SFX palette:
  `chime, ui_tap, purr, hop_boing, penguin_giggle, buzz, buy, fart` (+
  `ambience_*` beds, music `castle_open` stinger + `hall`/`home` tracks).
  Every `Button` auto-plays `ui_tap` via `_hook_button_taps` unless it sets
  meta `uses_own_sfx` (item/door hotspots opt out).

### 1.2 Complete interactivity inventory (what a child can touch today)

**Main Hall (wide) — 11 touch items + 8 portals:**

| Item | Reaction (one-shot) | Sound |
|---|---|---|
| 6× Pearl shell sconce | light toggle + scale blip, hall relights | chime (pitch 1.65–1.78) |
| Royal shell tapestry | sway | chime 1.55 |
| Sleepy dust bunny | hover | purr 1.8 |
| Shell-hide dust bunny | wiggle | hop_boing 1.45 |
| Hopping dust bunny | bounce | hop_boing 1.7 |
| Dust bunny family | pulse | penguin_giggle 1.55 |
| 7 door portals + Huluu's throne | Roshan walks there, then enters / crown moment | ui_tap |

**Destination rooms — exactly 3 touch items each (21 total):**

| Room | Items (anim / sound) |
|---|---|
| Opera Hall | curtains (sway/purr) · chandelier (sway/chime) · stage star (pulse/chime) |
| Royal Kitchen | shell sink (splash/ui_tap) · bubbling soup (bounce/buzz) · royal teapot (wiggle/chime) |
| Royal Library | magic storybook (hover/chime) · reading pearl (pulse/purr) · pearl lamp (pulse/chime) |
| Stuffie Playroom | stuffie friends (bounce/penguin_giggle) · stacking toy (wiggle/hop_boing) · toy blocks (bounce/hop_boing) |
| Craft Room | idea board (pulse/chime) · paint jars (bounce/buy) · rainbow palette (wiggle/buzz) |
| Mermaid Pool | rainbow waterfall (splash/ui_tap) · flower float (spin/chime) · bubble fountain (splash/ui_tap) |
| Bubble Bath | bubble bathtub (splash/penguin_giggle) · shell sink (splash/ui_tap) · royal toilet (wiggle/**fart 1.15** — keep forever) |

**Per-room action button** (gold, bottom-left): opera → real opera minigame;
craft → real craft studio; stuffies → companion picker; throne → Crown Star
award (first time) / royal wave. **kitchen, library, pool, bath → text
message + sparkle burst only** — and the player cannot read.

**Animation verb vocabulary** (`_animate_item`): `pulse, wiggle, bounce,
hover, spin, sway, splash, light` — all 0.3–0.7 s single tweens, `busy` meta
swallows taps during playback. Tap feedback = 6 star motes (`assets/mg/star.png`)
tinted per item + pitched SFX.

### 1.3 What is missing (the audit's core finding)

1. **Zero idle motion.** Outside the player's idle sway and the elevator's ▼
   bob, every room is a static painting. Water doesn't fall, soup doesn't
   bubble, bubbles don't rise, stuffies don't breathe, stars don't twinkle.
   For a toddler, motion is the invitation to touch; still frames read as
   "done."
2. **Touch density is thin.** 3 touchables per room vs. dozens of painted
   invitations (hanging pans, toy bins full of stuffies, bookshelves, rubber
   duck, towels, ribbons, audience seats, wall niches, the entire pool
   surface). A toddler *will* tap these; today ~80% of taps land on nothing
   (walk instead — which reads as "the game ignored me").
3. **No reaction variety.** Every repeat tap replays the identical 0.5 s
   micro-tween; rapid taps are swallowed by the `busy` flag. Toddlers tap in
   bursts of 3–10; the game should reward the burst, not eat it.
4. **Four rooms' action buttons are text-only payoffs** — unusable by a
   non-reader (kitchen, library, pool, bath).
5. **No discoverability affordance.** Item dicts carry `symbol`+`color`
   fields, but symbols are dead data (bursts always use star.png). Nothing
   shimmers to say "touch me."
6. **Dead data:** `ROOM_ITEMS["main_hall"]` (throne + fountain_left/right_v2)
   is never spawned — the wide-hall path uses `HALL_ITEMS` only. The v2
   fountain cards (item-style audit 4.7/5) are orphaned art.
7. **Roshan slides** between foots (position/scale tween) with no travel bob;
   fine, but a cheap sin-bob would add life.
8. Nits: elevator/menu/action buttons double-play `ui_tap` (auto-hook + explicit
   `_ui_tap()`); `castle_hall.gd.uid` orphan; `living_world_catalog.gd:124-204`
   still documents the deleted 3D hall rooms.

---

## 2. Design principles for this pass (binding)

1. **One finger, no reading, no failure.** Every new interaction: single tap,
   instant visible+audible reaction, self-resetting, no state to lose. Text
   (`show_msg`) may accompany but must never carry the payoff.
2. **Hotspots ≥ 112×112 stage px** (existing floor). Nothing tappable smaller.
3. **Idle motion invites, tap motion rewards.** Idle = slow, small, silent
   (≤ ~2 px sway, 4–9 s periods, phase-staggered). Tap = fast, big, loud.
   Never let ambient motion drown the tap reward.
4. **Picture-first rules stand.** Only `Sprite3D` cards at authored Z. No
   meshes, no `CanvasItem` world art, no billboards. New cards must respect
   the room's Z bands and never occlude door signage or the walk lane
   readability.
5. **Art-reuse budget (owner decision 2026-07-28).** Inventory existing art
   first; prefer reuse and non-destructive derived variants (new paths,
   source attribution). Generate new art only for recorded gaps (§6 lists
   them). The old "wishing-star/fountain/chime pickup row" was explicitly
   rejected — interactivity must live *inside* the painting, not float on it.
6. **Performance envelope (old Android):** one shared ambient tick (model:
   `sky_lagoon_promenade.gd _tick_ambient_life`) — per-card meta + sin waves,
   **no** long-lived looping Tween per card, no per-frame allocation, capped
   live mote count, no new `Light3D` outside the hall, translucent overdraw
   discipline (promenade lesson: one cloud, thin wisps). `speedy` quality
   halves ambient card counts and disables ambient motes.
7. **Audio: reuse-first.** Pitch families on the existing 8 SFX cover almost
   everything. Genuine gaps (duck squeak, water droplet, page flip) are
   listed in §6 as owner-approval options — do not block on them.
8. **Protected assets untouched:** `assets/book/`, `assets/audio/voices/`,
   `assets/characters/friends/`. (Optional idea in §5.6 uses voices read-only
   and needs explicit owner approval.)

---

## 3. Room-by-room audit and animation design

Format per room: painted-but-inert inventory (from the runtime screenshots in
`audit/castle_sprite3d/`), then recommendations. **[IDLE]** = ambient tick
loop, **[TAP]** = new/updated touch reaction, **[ART]** = needs a card that
does not exist yet (all listed again in §6). Priority ★ = do first.

### 3.1 Main Hall (both screens) — priority ★★ (already strongest; polish + reuse wins)

Painted-inert today: pearl fountain with sculpted drips (screen A, lower
left), 3+ wall-niche pearls, 6 door pictogram signs, hanging banner + royal
tapestry, underwater window slivers (far left), coral wall clusters (screen
B), gem ceiling pendants, the shell throne + rainbow arch (portal only), red
carpet.

- ★ **Bunny idle life [IDLE].** The four dust bunnies are the hall's mascots
  and sit right in the walk lane where the child looks. Sleepy: slow breath
  (scale y 1.00→1.03, 4 s) + a drifting "z" mote every ~9 s (reuse star.png,
  tinted lavender, slow rise). Hop bunny: small real hop (position y +14 px,
  BOUNCE ease) every 6–8 s. Shell-hide: shell lifts 2 px, eyes peek, drops
  (peek-a-boo teaser of its tap reaction). Family: gentle huddle wiggle.
  Phase-stagger so at most one moves at a time.
- ★ **Re-home the orphaned fountain cards [TAP].** Spawn `fountain_left_v2`
  (and mirror) as a HALL_ITEM over the painted screen-A fountain; anim
  `splash` + 8 aqua droplet motes falling back down; idle: one droplet mote
  every ~5 s. Turns dead 4.7-rated art into the hall's water toy and fixes
  finding #6. (If the painted fountain's silhouette fights the card, this is
  a derived-variant extraction, not new art.)
- **Sconce flame flicker [IDLE].** Sconces that are ON get a ±4% modulate
  shimmer (sin, per-sconce phase). Sells the light toggle; zero new nodes.
- **Door-sign wayfinding pulse [IDLE].** When Roshan's foot is within ~260 art
  px of a portal, that door's approach is already known
  (`_update_hall_portals`) — add a gentle 1.06× scale pulse on that door's
  painted sign region via a small overlay card, or simplest: a slow sparkle
  mote loop at the sign. A non-reader learns "glowy sign = I can go in."
  [ART: six ~200 px sign cutout cards — derived extractions from the masters,
  only if the overlay route is chosen; the mote route needs none.]
- **Tapestry + banner sway [IDLE]** (rotation ±0.5°, 7 s, offset phases) —
  tapestry already sways on tap; give it the idle version too.
- **Throne moment upgrade [TAP].** Post-crown taps currently show text + burst.
  Add: rainbow arch shimmer (modulate sweep) + a slow crown-star mote spiral
  above the throne. Wordless royalty.

### 3.2 Mermaid Pool — priority ★★★ (biggest expectation gap: painted water, zero motion)

Painted-inert: the entire pool surface (separate mid card — already isolated!),
rainbow waterfall column, 5 floating shell-flowers, clamshell fountain-throne,
gold star on the rim, towel shelf, coral clusters, big underwater vista window,
entry steps.

- ★ **Waterfall lives [IDLE].** The waterfall is its own item card. Loop:
  scale y 0.99↔1.03 + modulate brightness ±6% (1.6 s), plus 2 staggered
  translucent wisp cards sliding down its column and fading (exact smoke-wisp
  pattern from the promenade, vertical; reuse
  `assets/sprites/sky_lagoon` smoke wisp texture tinted aqua — zero new art,
  3 cards total, matches the "thin airy wisps" owner taste).
- ★ **Pool surface shimmer [IDLE].** `room_mermaid_pool_mid_pool.png` gets a
  slow brightness/saturation sin cycle (±5%, 5 s). One property on one
  existing card — the whole room starts breathing.
- ★ **Tap the water anywhere [TAP].** New full-pool hotspot (behind item
  hotspots in priority): tap → droplet burst at tap point (6 aqua motes up,
  gravity down) + soft `ui_tap` pitch 2.3 + a one-shot expanding ripple
  (scale+fade on a thin ring card). The player is a mermaid; water must
  answer. [ART: one 128 px soft ripple-ring png — trivial, or reuse star.png
  scaled/flattened if acceptable.]
- **Floats bob [IDLE]** (position y ±3 px sin, per-float phase) — flower_float
  keeps its spin tap. Bobbing floats are the classic "alive water" tell.
- **Bubble fountain idle [IDLE].** One bubble mote rising every ~3 s from each
  painted fountain jet (cap 3 live). Reuse star.png tinted white-blue at low
  alpha, or bubble card from §6.
- **Vista window fish [IDLE].** One small fish silhouette card drifting across
  the window arch every ~14 s (wrap, promenade-cloud pattern). [ART: reuse an
  existing 2D fish sprite if one exists in `assets/sprites/` /
  `gen2`; else record gap — one ~180 px side-view fish card.]
- ★ **Fix the 💦 action button [TAP].** Replace text with a 3 s wordless
  splash party: Roshan hop-tween, 14 droplet motes, 3 ripple rings across the
  pool, `penguin_giggle` + pitched `ui_tap` cascade. No state, self-ends.

### 3.3 Royal Kitchen — priority ★★★ (cooking = steam, fire, clatter)

Painted-inert: 4 hanging copper pans + ladles, shell range hood, stove fire
glow, second copper kettle, shelf jars ×3, pink tureen in alcove, round table
with shell bowl + cake stand, seaweed plant, green dish cabinet, two soft-focus
window zones.

- ★ **Soup pot steams [IDLE].** 3 staggered thin steam wisps rising from the
  soup pot on a fposmod life cycle — direct port of the promenade chimney
  smoke (same texture, white-tinted). The single highest thematic win in the
  castle: the pot is painted mid-boil.
- ★ **Soup pot boil-bounce [IDLE].** Tiny scale pulse (1.00↔1.02, 0.9 s) on
  the pot card so the steam has a source rhythm. Tap keeps `bounce` + buzz,
  add 2 extra steam wisps burst on tap.
- **Stove fire flicker [IDLE].** Warm modulate shimmer on a small glow-zone
  card over the painted firebox (±8% orange, noise-phase). [ART: one soft
  ~160 px glow blob card — or reuse an existing glow/spark asset if
  inventoried.]
- ★ **Hanging pans [TAP ×4].** Each pan = its own hotspot (they're large and
  head-height in art). Tap → pendulum swing (rotation ±9° decaying, 1.2 s) +
  `chime` at a per-pan pitch (1.2 / 1.4 / 1.6 / 1.8 — a playable pan
  glockenspiel). [ART: 4 pan cutout cards, derived extractions from the
  background master; vacated silhouettes repaired per the fountain-v2
  precedent — this is the established non-destructive pattern.]
- **Teapot pour [TAP].** Upgrade teapot from `wiggle` to new `pour` verb:
  rotate −35° toward spout, 3 droplet motes arc out, return. Sound stays
  chime.
- **Kettle whistle [TAP].** If pan extraction goes well, same treatment: tap
  kettle → one steam wisp + `buzz` pitch 2.2 jiggle.
- **🍲 action button [TAP].** Replace text with boil-over party: pot rocks,
  6 steam wisps, lid-hop (if lid is part of pot card, scale-y squash sells
  it), `penguin_giggle`. 3 s, wordless.

### 3.4 Bubble Bath — priority ★★★ (bubbles must rise; comedy room)

Painted-inert: foam in the tub, **rubber duck in the tub art**, gold taps,
towel + rail, vanity mirror, potion/perfume shelves, toilet-paper roll, two
underwater windows, coral, bath caddy, shell basket.

- ★ **Bubbles rise [IDLE].** 1 bubble mote every ~2.5 s from the tub foam
  (drift up 60 px, wobble x, pop-fade; cap 4 live). Same pattern over the
  bubble-fountain in the pool room. [ART: one ~64 px bubble card with
  highlight — or star.png at low alpha if the owner accepts sparkle-bubbles;
  inventory reef/minigame assets first, a bubble sprite likely exists.]
- ★ **Duck peek-a-boo [TAP].** Extract the painted duck as its own card
  (derived variant; repair the vacated pixels — fountain-v2 precedent). Idle:
  slow 2 px bob with the "water line" fixed. Tap: duck dives (drops 12 px,
  squash), then pops up with `hop_boing` pitch 2.0 + 3 bubble motes.
  Peek-a-boo is *the* toddler mechanic and the duck is already painted.
- **Tub tap upgrade [TAP].** Keep splash anim; add 4 foam motes + one duck
  hop (once extracted, tub and duck react together).
- **Toilet comedy pack [TAP].** Keep wiggle+fart (pitch-vary 1.0/1.15/1.3 on
  repeat taps). Add: TP roll spin — separate hotspot, rotation 360°
  `hop_boing` (derived cutout, small). Bubbles from the bowl on every third
  tap. This room is allowed to be silly; it's the fart room.
- **Mirror sparkle [TAP].** Tap mirror → diagonal glint mote sweep + chime
  2.4. (No reflection tricks — one mote pass.)
- **Potion bottles [TAP].** One shared hotspot over the shelf: tap → bottles
  wiggle in sequence (3 sub-tweens, staggered 80 ms) + colored puff mote per
  bottle. Teaches colors, needs no new art (motion on a shelf cutout).
  [ART: one shelf cutout card.]
- **🫧 action button [TAP].** Bubble party: screen-wide rising bubbles (12
  motes, 3 s), Roshan giggle-hop, `penguin_giggle` + chime cascade. Wordless.

### 3.5 Stuffie Playroom — priority ★★ (the emotional core; ties into companions)

Painted-inert: TWO toy bins overflowing with stuffies, navy play tent with
crescent flag, striped play tunnel, toy sailboat, 3 wheel chandeliers,
mezzanine rail, wall banners, scattered alphabet blocks, big scallop stage
behind the nook.

- ★ **Stuffie nook — individual friends [TAP].** The nook card shows ~7
  stuffies in a row. Split the hotspot into 3 zones (left/middle/right, each
  ≥112 px). Each zone: that region's stuffies hop (offset sub-tween) with a
  distinct `penguin_giggle` pitch (1.2 / 1.45 / 1.7). Sequential tapping
  becomes a giggle melody. No new art (zones over the existing card).
- ★ **Toy-bin peek-a-boo [IDLE + TAP].** Idle: every ~8 s one bin jiggles and
  a stuffie ear/head rises 6 px then hides (derived cutout of one painted
  stuffie per bin). Tap bin: full pop-up + giggle + 3 heart-tinted motes.
  [ART: 2 small stuffie-peek cutouts — derived.]
- **Tent flap [TAP].** Tap tent → flap wiggle + one dust-bunny card (reuse
  `dust_bunny_hop`) peeks out and hides. Cross-links the hall mascots. [No
  new art — reuse bunny card at 0.3 scale.]
- **Stacking toy count-up [TAP].** Upgrade from `wiggle`: each tap makes the
  rings hop in sequence bottom→top (5 sub-tweens, 90 ms stagger, per-ring
  pitch chime 1.2→2.0). A counting toy with zero text.
- **Blocks topple-restack [TAP].** Tap: tower squash-tips 8° with
  `hop_boing`, springs back with TRANS_BACK overshoot. (True topple needs
  per-block cards — not worth the art; the tip-and-spring reads as physics
  comedy at this age.)
- **Sailboat rock + chandelier sway [IDLE].** Boat: ±3° rock, 5 s. The three
  wheel chandeliers: ±1.5° sway, phases offset. Quiet background life.
- **Mobile idle for the nook [IDLE].** One stuffie in the nook breathes
  (scale 1.00↔1.02) at a time, rotating which one every ~6 s — the shelf
  looks asleep-but-alive.

### 3.6 Opera Hall — priority ★★ (theatre = anticipation; feeds the real opera minigame)

Painted-inert: two curved balconies of shell audience seats, bunting swags,
starry dome (dozens of painted stars), side arch doors, stage floor glow.

- ★ **Curtain reveal [TAP].** Upgrade curtains from `sway`: tap → both
  curtain halves part 10% outward + brighten (scale x on split halves), star
  mote burst on stage, then close. [ART: split the existing curtains card
  into L/R halves — derived, no new pixels.] This is the theatre's promise:
  "something happens behind these."
- ★ **Chandelier real swing [IDLE + TAP].** Idle: pendulum ±1.2°, 4 s. Tap:
  bigger swing (±6°, decaying) + crystal glints (3 white motes falling) +
  chime. The chandelier hangs from the dome — motion here fills the top
  third of the frame.
- **Dome star twinkle [IDLE].** 4–5 tiny glint motes cycling among painted
  star positions (one visible at a time, 2 s fade cycle). Zero new art,
  huge "magic ceiling" payoff for a child staring up.
- **Stage star spotlight [TAP].** Keep pulse; add a brief warm modulate lift
  on the stage floor zone beneath it (0.6 s) — tap the star, the stage
  "lights up" for you.
- **Audience wave [TAP].** One hotspot per balcony: tap → seat-row shimmy
  (scale-y ripple across the balcony card, 3 staggered sub-tweens) + soft
  `purr` applause. [ART: 2 balcony cutout cards — derived extractions; if
  budget says no, skip — lowest priority here.]
- The 🎭 action button already launches the real opera minigame — leave it.

### 3.7 Royal Library — priority ★ (calm room by design — quiet magic, one big toy)

Painted-inert: four bookcases of pastel books, two shell reading chairs, book
stacks, wheel chandelier, arched windows.

- ★ **Pearl lamp becomes a real light [TAP].** Generalize the hall-sconce
  mechanic: lamp toggles `ambient_light_energy` + a small warm SpotLight-free
  modulate lift on the room background tiles (rooms must NOT gain Light3D —
  fake it with tile modulate + glow tweak, which `_sync_castle_environment`
  already varies per room). Lights-on/off is the proven best toy in the
  castle; the library is the natural second home. Dim state should stay
  cozy-readable, never scary-dark.
- ★ **Magic storybook glow-breath [IDLE].** The book is the game's soul
  (family book art lives elsewhere in the app). Idle: hover ±3 px + glow
  modulate breath (5 s). Tap upgrade: `hover` + 3 page-corner flutter
  sub-tweens (skew via tiny rotation wobble) + sparkle spiral.
- **Tappable book spines [TAP].** One hotspot per side bookcase: tap → three
  books nudge out and back in sequence (stagger 90 ms) + chime scale
  (1.3/1.5/1.7). [ART: 2 small spine-trio cutouts — derived; skip if budget
  tight and use whole-case wiggle instead, no art.]
- **Dust motes in window light [IDLE].** 2 slow star motes drifting down the
  window shafts, 10 s loop, alpha 0.25. Library atmosphere in two nodes.
- **Chair boing [TAP].** Cushion squash (scale y 0.94 spring back) + purr.
  [ART: chair cutouts derived — optional.]
- **📚 action button [TAP].** Replace text with: the magic book floats up,
  opens (flip to open-book card), 5 picture motes (tiny star variants) orbit
  it 2 s, closes and settles. [ART gap: ONE open-book card, new art —
  recorded in §6. If not approved, do the float+orbit without the open frame.]

### 3.8 Craft Room — priority ★ (has a real studio already; add color play)

Painted-inert: hanging ribbon wall, two supply shelves of jars, brush pots,
paper rolls + washi rolls on the cart, chandelier, shell basin, pinned cards
on the idea board.

- ★ **Ribbon wall sway [IDLE].** The painted ribbon curtain is the room's
  natural motion: 3 overlapping ribbon-strip cutouts swaying at offset
  phases (±2°, 5–7 s). [ART: 3 strip cutouts — derived from background.]
- ★ **Paint jars teach colors [TAP].** Upgrade paint_table from single
  `bounce`: 3 sub-hotspot zones; each tap bounces that jar cluster and
  bursts motes in THAT cluster's painted color (pink/teal/gold) + `buy`
  pitch per color. Color-cause-effect with zero new art.
- **Idea-board flutter [IDLE + TAP].** Idle: one pinned card corner-flutters
  every ~7 s (tiny rotation wobble). Tap: all pinned cards flutter in a wave
  + chime.
- **Palette rainbow moment [TAP].** Upgrade from `wiggle`: tap → 6 motes in
  rainbow sequence (red→violet, 60 ms stagger) arc over the palette +
  ascending chime pitches. The room's signature firework.
- **Brush pot bounce [TAP].** Cart hotspot: brushes hop in sequence.
  [ART: brush cutout — optional, skip if tight.]
- The 🎨 action button already opens the real craft studio — leave it.

---

## 4. New shared systems (build once, all rooms benefit)

### 4.1 `_tick_castle_ambient(delta)` — the idle engine ★ build first

Port the promenade's `_tick_ambient_life` architecture wholesale
(`sky_lagoon_promenade.gd:334-460`):

- One `castle_ambient_t` accumulator; per-card meta: `ambient_kind`,
  `ambient_base` (pos/scale/rotation), `ambient_phase`, `ambient_speed`,
  `ambient_amplitude`, `intensity_class`.
- Kinds needed: `sway` (rotation sin), `bob` (position-y sin), `breath`
  (scale sin), `shimmer` (modulate sin), `drip`/`bubble`/`wisp` (fposmod
  life-cycle cards, promenade smoke pattern), `twinkle` (cycling glint
  among fixed points), `pendulum` (decaying unless refreshed).
- Data-driven: add optional `"idle": {kind, speed, amp}` keys to
  `HALL_ITEMS`/`ROOM_ITEMS` entries and a per-room `AMBIENT_CARDS` table for
  non-touchable life (wisps, motes, fish). Rebuild on `show_room`, free on
  leave — mirrors `_rebuild_touch_items`.
- Budgets: ≤ 6 ambient-animated cards + ≤ 4 live transient motes per
  destination room; hall ≤ 10 (bunnies + sconce shimmer + fountain drip).
  `speedy`: halve counts, disable transient motes, keep item idles.
- Idle motion must pause on a card while its tap tween runs (`busy` meta
  already exists — the tick skips busy cards) and must restore
  `ambient_base` exactly (promenade already solves this).

### 4.2 Invitation glints — discoverability ★

Every touchable gets a slow glint: one star mote at the item's top edge,
tinted `item.color`, 0.6 s fade, every 6–9 s (per-item phase; ≤ 2 visible
per room at once — schedule round-robin, don't randomize into clumps). This
is the "you can touch this" language across the whole game; the toddler
learns it once. Finally puts the dormant `color` field to work (drop the
dead `symbol` field or start rendering it as the glint glyph via a Label3D —
recommend: drop).

### 4.3 Repeat-tap escalation — reward the burst ★

Replace the busy-swallow: while `busy`, taps increment `combo` (cap 3).
`_finish_item_animation` checks combo > 0 → immediately replays the anim at
1.15× amplitude, +0.12 pitch, +4 motes per level, decrementing. Three fast
taps on the soup pot = big rolling boil with double steam. No new assets,
transforms every existing item, ~20 lines.

### 4.4 Wordless action moments

Shared helper `play_room_moment(room_id)` implementing the four §3 parties
(pool splash, kitchen boil-over, bath bubbles, library book) as 3–4 s
choreographed tween+mote sequences that disable the action button while
running. Opera/craft/stuffies/throne keep their real destinations.

### 4.5 Roshan travel life (cheap, optional)

During walk tweens add a parallel sin bob (±4 stage px, 3.2 Hz, amplitude
scaled by tween duration) and a single landing squash (scale y 0.97→1.0) on
arrival. Transform-only — no frame art, so the full-frame cinematic rule is
not triggered.

### 4.6 Sound families

Stay inside the existing palette via pitch ladders (pan glockenspiel on
`chime`, giggle ladder on `penguin_giggle`, comedy ladder on `fart`).
`ambience_hall.ogg` exists — consider a low-volume bed in the hall only
(music `castle_open`/`hall` already covers melody). Recorded gaps (§6):
duck squeak, droplet, page flip — nice-to-have, all faked acceptably today
(`hop_boing` 2.2 / `ui_tap` 2.4 / `purr` 2.0).

---

## 5. Priority order (recommended build sequence)

| Phase | Work | New art needed |
|---|---|---|
| **1 — systems** | §4.1 ambient tick · §4.2 glints · §4.3 escalation · fix double `ui_tap` · delete dead `ROOM_ITEMS["main_hall"]` after §3.1 fountain re-home | none |
| **2 — water & steam rooms** | Mermaid Pool pack (§3.2) · Kitchen pack (§3.3) · Bubble Bath pack (§3.4) | small: ripple ring, bubble mote, duck cutout, pan cutouts, steam = reuse |
| **3 — friends & theatre** | Playroom pack (§3.5) · Opera pack (§3.6) · Hall bunny life + fountain (§3.1) | stuffie peeks, curtain split, balcony cutouts (optional) |
| **4 — quiet rooms + moments** | Library pack (§3.7) · Craft pack (§3.8) · §4.4 wordless action moments · §4.5 Roshan bob | open-book card (the one real generation), ribbon strips, spine trios |

Rationale: Phase 1 multiplies everything after it. Phases 2 > 3 > 4 by
thematic gap: water/steam rooms are where stillness most contradicts what
the painting promises; playroom/opera are emotional favorites; library/craft
are intentionally calmer.

---

## 6. Art & audio gap register (per the reuse-budget rule)

**Reuse directly (no generation):** promenade smoke wisp texture (steam,
waterfall wisps, tinted), `star.png` motes (glints, droplets, dust, "z",
twinkle), dust-bunny cards (tent peek), fountain_left/right_v2 (hall
fountain), existing SFX pitch families, `ambience_hall.ogg`.

**Derived variants (extract from approved masters, repair vacated pixels,
new paths — fountain-v2 precedent):** duck, TP roll, 4 pans, kettle, potion
shelf, 2 toy-bin stuffie peeks, curtain L/R split, 2 balcony rows, ribbon
strips ×3, spine trios ×2, chair cushions, brush pot, stove glow zone, door
sign cutouts ×6 (only if overlay route), fish silhouette (check
`assets/sprites/` + `gen2/` first).

**Genuine new generation (record + get approval):** ① open magic-book card
(library moment — the only must-ask), ② soft ripple-ring png (trivial,
arguably procedural), ③ optional 64 px bubble card (inventory first — a
bubble sprite very likely already exists in reef/minigame assets).

**Audio gaps (optional, owner call):** duck squeak, water droplet, page
flip. Everything ships without them.

---

## 7. Guardrails & verification (do not skip)

- **Branch workflow:** fresh `claude/`- or `codex/`-topic branch off
  `origin/dev`; never commit to local dev/master; `python -m
  gdtoolkit.parser` + `python tools/lint_inference.py` on touched `.gd`;
  explicit types (CI `--check-only` fails `var x := <expr>` on untyped
  receivers).
- **Keep green:** `probe_castle_pearl_art` (CI runs it headless AND in a
  dedicated mobile-renderer pass — it asserts per-room prop animation + audio
  and hall card counts), `probe_crown` (crown flow, legacy-hall-absent),
  `probe_interaction` (asserts the 3D touch registry stays EMPTY in the
  castle — don't register anything there), `probe_touch_adversary`,
  `probe_audit`.
- **Extend the probe** with the new contract: after Phase 1, assert (a) ≥ N
  cards moved by the ambient tick in each room over 2 s, (b) a second tap
  during `busy` escalates (combo path), (c) mote count never exceeds budget,
  (d) hotspot minimum 112 px holds for every new hotspot, (e) speedy mode
  halves ambient counts.
- **Windows probe runs need an isolated `APPDATA`** or they pollute the real
  save (`%APPDATA%\Godot\app_userdata\Mermaid Roshan Reef of Light\`).
- **Screenshot gate:** refresh `audit/castle_sprite3d/` contact sheets per
  phase (pattern: `probe_castle_shots.gd`, non-headless). Idle motion can't
  be screenshot-verified — capture 3 frames 0.5 s apart and diff, or log the
  tick's per-card displacement in the probe.
- **Never:** meshes/3D models (owner rule 2026-07-26), pickup rows (rejected
  2026-07-28), new `Light3D` outside the hall, per-card looping Tweens for
  ambience, hotspots < 112 px, text-dependent payoffs, edits to protected
  asset dirs, overwriting approved masters (derived variants at new paths
  only).
- **Cleanup while in there (small, optional):** orphaned
  `scripts/arena/castle_hall.gd.uid`; stale castle entries in
  `living_world_catalog.gd:124-204`; the unused `symbol` fields.

---

## 8. Summary for the owner

Today the castle is a beautiful, navigable picture book with 32 touchable
props, a genuinely great hall-lighting toy, four comedy bunnies, and three
real minigame doors — but the pictures don't move until touched, only ~3
things per room respond, repeated taps are ignored, and four rooms' "big
button" pays off in text the player can't read. This brief turns every room
gently alive (steam, waterfalls, bubbles, twinkles — all within the existing
card/tick architecture and performance budget), roughly doubles the
touchable count per room using cutouts derived from art that already exists,
rewards toddler tap-bursts instead of swallowing them, and replaces the four
text payoffs with wordless 3-second spectacle moments. One genuinely new
image is requested (the open storybook); everything else is reuse.
