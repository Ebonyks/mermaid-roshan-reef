# Day One — the dirty-castle introduction level

_Written 2026-08-03 on `claude/day-one-castle-intro-u77vnf`. Owner brief:
"the game starts with Daddy Mermaid and Mermaid Roshan arriving on an airplane
to their new Castle. Upon walking in they find a dirty castle full of dust
bunnies. This is the introduction level, where you explore the whole castle in
the process of cleaning it, and each room teaches you the mechanics of that
part of the house as part of the encounter in it."_

This document is the **plan**. Two pieces of it have shipped on owner decision
(2026-08-03): the dated Huluu storybook opener is **cut** (§1.2), and the
control guide that replaces it is **built** (§1.3). The promenade was also
pinned flat (§1.4). Everything else here is still design. The Codex Day One art is in the tree **deactivated** (§9).

Precedence: this sits under `CLAUDE.md`, `AGENTS.md` and `design/01_GAME_DESIGN.md`.
Where it proposes something new it says so; where it records what is already
built it cites the file and line.

---

## 1. What already exists — verified against `dev` @ `6596f637`

Day One is not a blank page. Roughly half of it is already shipped and
probe-gated; the missing half is the *spine* that connects the pieces.

### 1.1 Built and live

| Piece | Where | Status |
|---|---|---|
| The pearl plane, landed at the lagoon dock | `arena/sky_lagoon_promenade.gd:524`, save key `lagoon_plane_departed` | live, tappable |
| The castle gate, tappable, leads inside | `sky_lagoon_promenade.gd:642` (`castle_gate`) | live |
| The 2.5D Pearl Castle: 2-screen Main Hall + 12 rooms | `arena/castle_rooms_25d.gd` (3,573 lines) | live |
| **Three dust bunnies in the Grand Hall**, cleared by walking into them | `castle_rooms_25d.gd:211` `HALL_DUST_BUNNY_SPAWNS`, `CASTLE_DUST_BUNNY_SPAWN_GUIDE_2026-07-29.md` | live, probe-gated |
| **Baby Eagle rescue → the stuffie collection opens** | `castle_rooms_25d.gd:241` `PLAYROOM_RESCUE_ITEMS`, `STUFFIE_PLAYROOM_RESCUE_GUIDE_2026-07-29.md`, `probe_stuffie.gd` | live, probe-gated |
| Princess Huluu offers a companion at the throne | `castle_rooms_25d.gd:_offer_companion_at_throne` | live |
| Royal Kitchen: fridge → recipe → cooking act | `castle_rooms_25d.gd:_launch_kitchen_recipe` | live |
| Craft Room → craft studio | `main.gd:_open_craft_studio` | live |
| Opera Hall → the career arc | `main.gd:_start_opera` | live |
| Dream House Wing: dining / royal bedroom / sleepover / movie lounge, with roleplay verbs (eat, serve, sleep, dress up, watch) | `castle_rooms_25d.gd:540–710` | live |
| Dust Bunny Boss with vulnerability-window AI | `games/dust_boss.gd`, `DUST_BUNNY_BOSS_2026-08-02.md` | live, reached from a **reef** portal |

**The single most important existing fact:** the owner's example — *"rescuing
baby eagle opens up the stuffie collection"* — is already built exactly that
way, wordlessly, with no fail state, and covered by `probe_stuffie.gd`. It is
the template every other room encounter in this plan copies.

### 1.2 The old opener — CUT (owner decision 2026-08-03)

`scripts/intro_overlay.gd` used to play the **old** four-panel premise: *Huluu
lives in the sky, a storm swept her down, find the pearls, open the sky river.*
It fired on first session over the lagoon. It was not the airplane arrival,
Daddy Mermaid was not in it, and there was no dirty castle.

**Owner cut it on 2026-08-03.** In its place:

- `IntroOverlay` is now a movie player and nothing else. A film of Mermaid
  Roshan and Daddy Mermaid flying to the castle together will be added
  eventually; drop it at `assets/cinematics/opening/roshan_daddy_flight.ogv`
  and it plays on the first session with no code change.
- **While that file is absent there is no overlay at all** — no black frame, no
  poster, no placeholder panel. An opener that exists and shows nothing is
  worse than no opener. `probe_day_one_guide` asserts the absence so a blank
  placeholder cannot creep back.
- `_build_intro` / `_intro_next` / `_skip_intro` stay on `ReefMain` as safe
  no-ops, because ~40 probes call `_skip_intro()` defensively at boot.
- The controls the storybook never taught are now taught in the world, by the
  Day One guide (§1.3).

### 1.3 The Day One guide — BUILT (owner decision 2026-08-03)

`scripts/day_one_guide.gd`, a `SkyLagoonPromenade` satellite, teaches the three
controls the game had never taught (D1-11), in the world, using the promenade's
own equipment and animals rather than a slideshow:

| Step | Teaches | Anchor | Completes on |
|---|---|---|---|
| 1 | **Touch-the-world travel** | a spot nine paces along the shore, always toward open ground | arriving there — drifting past does not count |
| 2 | **Two-press activation** | the pearl plane she just landed in (the slide, once the plane has flown) | a real second press |
| 3 | **Tap a thing** | the live animal; while none is on camera the pointer leads her along the promenade, past the slide, swing and seesaw | startling an animal |

It is a pulsing gold `Sprite3D` pointer and one voiced line per step — no
`Control`, no modal, nothing that can eat a tap. There is no timer and no
failure; a step that has been up for 22 s re-voices its line once and then
waits indefinitely. Progress persists under the additive key
`day_one_guide_done`, written true and never false, so a taught child is never
taught twice. Gate: `scripts/probe_day_one_guide.gd`.

Step 2 uses the plane rather than the slide deliberately: the arrival shore's
otter and frog carry `requires_plane_departed`, so on Day One there is no
animal at the spawn point, and the slide is 40 painted units away. The plane is
under her feet, is a registered two-press target, and is the thing she arrived
in.

### 1.4 The promenade reads flat — FIXED (owner decision 2026-08-03)

Owner report: *"the background should load flatly; there's a 3D card effect at
load presently."*

Cause, in `sky_lagoon_promenade.gd`: every world card is a `Sprite3D` at real
depth under a 38° perspective lens 47 units back — mural at z −18, landmarks at
−11, playground at −6, Roshan at 0. `_mural_anchored_position` re-projects each
card onto its authored painted socket every frame, weighted by that card's
`mural_socket_lock`. Playground equipment, the castle, trees and smoke were
already pinned at 1.0. **Landmarks were not** — `DEFAULT_MURAL_SOCKET_LOCK` was
`0.65`, leaving 35% raw parallax.

The largest landmark is the **pearl plane**, which is the first thing on screen
at spawn (painted x −60) and which the camera immediately pans away from, since
the lens clamps to the mural's pan limit while Roshan stands at the painted
edge. So the child met the promenade with its one unpinned prop visibly sliding
off the painted dock. That is the 3D-card read.

Fix: `DEFAULT_MURAL_SOCKET_LOCK := 1.0`. Every card now compensates the whole
camera-depth offset, so the stage reads as one flat picture from any camera
position. The cards stay `Sprite3D` at real depth, so occlusion still works —
this pins the socket, it does not flatten the scene into a single quad. Ambient
motion (cloud drift, smoke, the plane's idle bob) rides on top of the pinned
base and is unchanged. `probe_l2` now asserts the constant is 1.0, so partial
parallax cannot return by accident.

Reversible in one constant if the depth findings
([OW-3](design/04_OPEN_WORK.md#ow-3), [OW-4](design/04_OPEN_WORK.md#ow-4)) are
ever addressed properly, which is where real parallax belongs.

### 1.5 Not built at all

- No arrival. The plane is *already parked* when the child first sees the world;
  nobody flies in and nobody gets out.
- **Daddy Mermaid is absent from the playable game.** He exists as protected art
  (`assets/characters/friends/daddy.webp`), as three **sacred family voice
  recordings** (`daddy1/2/3.ogg`), and as a cutout in one minigame
  (`main.gd:618`, melody). He is in the owner's premise as a co-lead and appears
  in 30 of the 36 Codex storyboard frames — and he is in none of the rooms.
- No cleaning progression. The five existing bunnies are **visit-scoped** and
  reset when the castle closes; nothing persists, nothing counts, nothing
  finishes.
- No day boundary. Nothing in the save says "Day One is done".
- Two rooms in the Codex design do not exist: the **Undercroft** and the hidden
  **Royal Loo**.

---

## 2. What Codex already made for Day One

Codex did substantial Day One work across four branches. It was never merged to
`dev` and its runtime code is built on a stale base (it deletes the living-world
director, the boot splash, and the whole `castle_room_*` 2.5D state block — a
merge would be a large regression). **The art is excellent and the narrative
design is better than anything else in the repo. The runtime shell should be
discarded.**

### 2.1 The branches

| Branch | Contains | Verdict |
|---|---|---|
| `codex/dirty-castle-2d` | 96 runtime cutouts, 36-frame cinematic, prompt records, `DIRTY_CASTLE_CINEMATIC_36_2026-07-23.md` | **art: take it all.** Landed here (§9) |
| `codex/day-one-opening` / `codex/day-one-opening-final` | `arena/dirty_castle_stage.gd`, `cinematic_overlay.gd`, rewritten `intro_overlay.gd`, `probe_story_day_one.gd`, `arrival_imp.png` | **code: do not merge** (§2.3). Art and probe ideas taken |
| `codex/castle-dust-bunny-spawn` | the hall bunnies | already on `dev` |

### 2.2 The 36-frame storyboard — the best artefact of the lot

`DIRTY_CASTLE_CINEMATIC_36_2026-07-23.md` (on `codex/dirty-castle-2d`, brought
forward as `assets_src/concepts/dirty_castle_cleanup_2026-07-22/STORYBOARD_36_PROMPTS.md`)
is a complete, art-finished Day One narrative in 36 illustrated beats, at
1024×576, showing **Roshan, Daddy Mermaid and Baby Eagle cleaning the castle
together, room by room**. Its stated room rhythm is exactly the owner's brief:

> 1. discover the room and its large object groups;
> 2. assign one readable job to Roshan, Daddy, and Baby Eagle;
> 3. show an action with immediate progress;
> 4. show an unmistakably clean room and move forward.

And its treatment of the dust bunnies is a design decision worth adopting
wholesale:

> Dust bunnies become helpers and neighbours. They are **housed comfortably at
> the end rather than defeated or discarded.**

The frame order is: Grand Hall (01–08) → Playroom (09–13) → Library (14–18) →
descent (19) → Pantry (20) → Kitchen (21–25) → Bubble Bath (26–29) → **Royal
Loo (30–32)** → **Undercroft (33–34)** → inspection and finale (35–36).

### 2.3 Why the Codex *runtime* is rejected

`scripts/arena/dirty_castle_stage.gd` (404 lines) builds Day One as a
**full-screen `Control` minigame**: a flat `ColorRect` background, seven rooms
of three tap-three-times targets, a next-room button. Its own header states the
constraint it was built under: *"a genuine full-screen Control minigame, not a
navigable world… its background is code-native Control colour."*

That was a reasonable answer to a background-resolution rule, but it means Day
One would not take place in the castle — it would be a menu that looks like the
castle. It bypasses `castle_rooms_25d.gd` entirely, so nothing the child learns
in it transfers, and the rooms it names (`grand_hall`, `royal_loo`,
`undercroft`) do not match the rooms she can walk into afterwards.

It also depends on two `.ogv` movies that **do not exist and were never made**
(`assets/cinematics/{opening,dirty_castle}/*.ogv`), falling back to a black
screen — while 36 finished frames sit unused one branch over.

**Decision: keep the art and the narrative, rebuild the encounters inside the
existing 2.5D rooms.** Play the 36 frames as a tap-advanced storybook flipbook,
not as video (§5, Phase 2).

---

## 3. The Day One spine

Four stages. Each is skippable-by-hold, replayable, and saves at every seam.

### Stage 1 — Arrival (storybook flipbook)

Frames 01–02 of the flipbook, preceded by two new arrival beats. Daddy Mermaid
and Roshan fly the pearl plane to their new kingdom. **This replaces the
Huluu-storm intro** (`intro_overlay.gd`), which moves to the Library's story
shelf as a re-readable book rather than being deleted.

Daddy's three sacred recordings carry the first lines a child hears in the game.

### Stage 2 — The landing

The lagoon promenade, as it ships today, with three additions:
- Roshan and Daddy walk out of the plane instead of being pre-placed.
- The imp (`assets/sprites/story/arrival_imp.png`) is seen once, fleeing toward
  the castle. He is the reason the castle is dirty. He is never a threat.
- The castle gate is the only lit target until it is entered — Day One is a
  **line**, per the charter's "you cannot be lost on a line".

### Stage 3 — The dirty castle, room by room

The Grand Hall is dirty (dirty skins, §4). Daddy hands out tools. Each room is
one *encounter* that teaches one *mechanic* (§4). Cleaning a room lights its
door on the hub and voices the next one.

### Stage 4 — The day closes

Final inspection (frames 35–36), the dust bunnies get their basket home in the
Undercroft, dinner in the Family Dining Room, and bed in the Royal Bedroom.
Sleeping writes `day_one_done` and voices tomorrow's objective. **This gives the
game its first day boundary**, which it has never had.

---

## 4. Room-by-room — the encounter table

The rule from the brief: *each room teaches the mechanics of that part of the
house, as part of the encounter in it.* One room, one verb, one wordless
discovery, no fail state.

| # | Room | Encounter | Mechanic it teaches | Unlocks | Build status |
|---|---|---|---|---|---|
| 1 | **Grand Hall** | Three dust bunnies hop across the hall; walking into one poofs it | **Touch-the-world travel** — the single most important control in the game | The hall's doors light one at a time | **BUILT** — needs Day One framing + a tool hand-off from Daddy |
| 2 | **Grand Hall — throne** | Princess Huluu greets her, awards the crown, offers a friend | **Two-press activation** (approach → ready → act) | The companion picker | **BUILT** |
| 3 | **Stuffie Playroom** | Two bunnies pin Baby Eagle; free him | **The stuffie collection + companion care** | Companion follows her everywhere | **BUILT & probe-gated** — the model encounter |
| 4 | **Royal Library** | Fallen books, ribbons and picture cards; sort them onto the shelf | **Picture games (K2) and the wordless-book grammar** | The story shelf and the album (§6.1) | **STUB** — one line of dialogue, no gameplay |
| 5 | **Royal Kitchen** | Flour, plates and a crooked pan; wipe up, then Daddy suggests a first recipe | **The gesture-widget grammar** shared with every Opera act | The fridge recipe loop (already built) | **HALF** — the cooking act exists; nothing introduces it |
| 6 | **Craft Room** | Spilled paint and craft scraps | **Make-and-keep** — a crafted fish spawns in the world and stays | The craft studio | **HALF** — studio exists, unframed |
| 7 | **Bubble Bath** | Foggy mirror, soap ring, tipped toy basket | **Care** — the same wipe/scrub verbs that heal a bruised stuffie | The care loop gets a *place* instead of a menu (§6.3) | **STUB** |
| 8 | **Mermaid Pool** | The pool is cloudy; clear it and the water comes alive | **Swimming** — the one honest home left for the legacy swim controller | The way down to the reef (§6.2) | **STUB** |
| 9 | **Undercroft** *(new room)* | Dusty storage, a stair cobweb, and the dust bunnies' new home | **Carry-and-place**; then the Dust Bunny Boss *showing* | The boss arena, re-homed from the reef (§6.4) | **NOT BUILT** — Codex art exists (frames 33–34, `rooms/basement/*`) |
| 10 | **Royal Loo** *(new room, hidden behind the Bubble Bath)* | Soap ring, crooked paper rolls, one clean splash | **Finding a hidden room** — the first secret | A giggle and a sticker | **NOT BUILT** — Codex art exists (frames 30–32) |
| 11 | **Opera Hall** | The stage curtain is dusty; opening it reveals the stage | **That a career arc exists** — Day One opens the door and stops | The Opera career arc for Day Two | **HALF** — do not run an act on Day One; it is far too long |
| 12 | **Dream House Wing** | Dining, Royal Bedroom, Sleepover Bedroom, Movie Lounge | **Roleplay verbs**, then **the day ends** | Dinner → bed → Day One complete | **HALF** — verbs built, no day loop |

Ordering note: rooms 1–3 are mandatory and linear. Rooms 4–8 unlock together as
a **free-choice set** once the Playroom is done — the child picks the order, and
the hall door glow follows whatever is left. Rooms 9–10 unlock after any three
of 4–8. Rooms 11–12 close the day. Nothing can be failed, skipped permanently,
or missed: an unfinished room simply stays glowing tomorrow.

---

## 5. Implementation phases

Each phase is one branch, probe-green on CI before merge to `dev`, reversible.
`main.gd` gains **no new logic** — Day One is a satellite (`RefCounted`,
receives `main` by reference, all state on `main`), per the refactor rules.

| Phase | Work | Gate |
|---|---|---|
| **0** | *(this commit)* Land Codex art deactivated; write this plan | existing suite stays green |
| **1** | `scripts/day_one.gd` satellite + additive save keys + `scripts/probe_day_one.gd`. No visuals — the state machine and its probe first | new probe in `ci.sh` |
| **2** | `scripts/story_flipbook.gd`: tap-advanced 36-frame storybook overlay (Control + TextureRect, **no video, no OGV**) for the per-room beats. The *opener* is settled separately — owner cut the storybook and reserved that slot for the Roshan + Daddy flight movie (§1.2) | `probe_day_one` asserts frame count, hold-to-skip, replay, and that skipping saves |
| **3** | Arrival: Daddy standee at the lagoon, Roshan disembarks, one imp sighting, gate-only targeting | `probe_l2` extended |
| **4** | Grand Hall mess pass: dirty skins over the existing hall cards, Daddy's tool hand-off, the three bunnies re-framed as the travel tutorial, first persistent `clean_done` writes | `probe_castle_pearl_art`, `probe_day_one` |
| **5** | Room encounters 4–8, one room per commit, each with its own voice line + visual pointer | per-room probe assertions |
| **6** | New rooms: Undercroft, Royal Loo. Re-home the Dust Bunny Boss from the reef portal to the Undercroft | `probe_dust_boss` retargeted |
| **7** | Day close: inspection, dinner, bed, `day_one_done`, the Day One medal, tomorrow's objective voiced | `probe_day_one` end-to-end |
| **8** | **Activation**: re-encode the 36 frames for the phone (§7.2), drop the export exclusions, flip the flag, promote | full suite + a device pass on the M11 |

### 5.1 Save keys (additive only — never removed, per the hard rules)

```
day_one_guide_done : bool    — the Sky Lagoon control guide (SHIPPED 2026-08-03)
day_one_stage      : String  — "arrival" | "landing" | "castle" | "closing" | "done"
day_one_room       : String  — the room being cleaned, "" between rooms
clean_done         : Dictionary — "<room_id>:<target_id>" -> true   (persistent; the
                                  existing bunny clears are visit-scoped and stay that way)
day_one_done       : bool
daddy_met          : bool
tools_unlocked     : Array[String]
imp_sightings      : Dictionary — room_id -> true
story_pages_seen   : Dictionary — frame index -> true (drives the Library re-read)
```

All default to their empty value on an existing save, so a save written today
loads into Day One as "already arrived, castle unlocked, nothing cleaned" — no
child loses a crown, a medal or a companion to this feature.

---

## 6. Rooms without a clear purpose — proposals

Six rooms are currently a voice line and a sparkle burst. Each proposal below
gives the room a job **the game already needs done somewhere**, so the room
earns its place rather than being decorated.

### 6.1 Royal Library → **the album room** *(recommended)*

Today: `show_msg("A whole room of storybooks!")` and a burst.

The game has three progress surfaces with no home — the Critter Book, the medal
shelf, and now the 36-frame Day One story. All three are album-shaped and all
three currently live in HUD chrome or nowhere. Put them on the library shelves:
one shelf per book, tap a book to open it. The Huluu-storm intro that Day One
displaces becomes the first storybook on that shelf, so nothing is lost.

This also gives the library a real Day One encounter (sorting the fallen books
*is* learning to use the shelf) and makes the picture games reachable from a
place instead of a menu — a partial answer to [OW-6](design/04_OPEN_WORK.md).

### 6.2 Mermaid Pool → **the way down to the reef** *(recommended)*

Today: a message and a burst, with a rainbow waterfall and floats already
painted and interactive.

The charter's zone-1 reef promenade is unstarted and the reef is currently
**unreachable in normal play** ([OW-6](design/04_OPEN_WORK.md#ow-6)). The pool
is the child-legible door: the castle pool goes down to the ocean. It is also
the only place left where the legacy swim controller is honest — a shallow,
bounded, safe pool is exactly the right teaching ground for a verb that the
promenade otherwise deletes.

Day One encounter: the pool is cloudy; clearing it makes the water swimmable.

### 6.3 Bubble Bath → **the care room** *(recommended)*

Today: a message and a burst, with tub, sink, toilet and duck already
interactive.

The companion care loop (`companion.gd`: wants, bruises, hugs, baths) is a
menu. A four-year-old understands *taking your friend to the bath* far better
than a HUD badge. Move the bath want and the post-battle heal here: the stuffie
gets bathed in the tub, the bruise heals, the want clears. The Day One
encounter (fogged mirror, soap ring) teaches the identical wipe/scrub gesture.

### 6.4 Undercroft *(new)* → **the dust bunnies' home, and the boss's stage**

The Codex storyboard ends the bunny arc by **housing them, not defeating them**
(frames 33–34). That resolves a live tone conflict: `dust_boss.gd` frames a
dust bunny as a boss while `PROMPTS.md` insists *"dust bunnies are friendly
helpers, not pests, monsters, smoke, or realistic dirt."*

Proposed reconciliation: the small bunnies are family and get a basket home in
the Undercroft. The **big** one — the boss, whose art is still missing
(`DUST_BUNNY_BOSS_2026-08-02.md` §0) — is the one who *made* the mess, arrived
with the imp, and is not living down there yet. His "showing" happens on the
Undercroft stair on Day One; the fight itself is Day Two. This also moves the
boss out of a reef portal that the child cannot currently reach.

### 6.5 Sleepover Bedroom → **the friends room**

Three dream beds are already painted and sleepable. The game has five voiced
friends (Evie, Harper, Faron, Rosalina, Mewsha) who appear only inside
minigames. Let a bed show who is staying over tonight, and let tapping a
sleeping friend start the co-op activity that friend owns (brawl, dolls,
seek). Low cost, and it turns a decorative room into the co-op launcher.

### 6.6 Family Dining Room + Royal Bedroom → **the day rhythm**

Dinner marks the end of the day's work; bed ends the day, saves, and voices
tomorrow's objective. This is the smallest possible day loop and the game has
none. Day One is the natural place to establish it, and every later day reuses
it unchanged.

### 6.7 Cloud Movie Lounge → **keep as the photo channel**

It already shows real family photos (`MOVIE_IMAGES`). Leave it alone; do not
merge it with the library album. One room for *memories*, one for *progress*.

### 6.8 Royal Loo *(new)* → **the first secret**

Hidden behind the Bubble Bath, revealed by cleaning it. Codex art and three
storyboard frames exist. Pure delight, near-zero mechanics, and it teaches that
the castle has secrets — which is what makes a four-year-old re-enter a room.

---

## 7. Where the game is weak, and what Day One should fix

Findings specific to Day One. Game-wide findings live in
`design/04_OPEN_WORK.md`; the ones Day One touches are cross-referenced.

| # | Weakness | Severity | Fixed by |
|---|---|---|---|
| **D1-1** | The first-session intro told a **story the game no longer has** (Huluu's storm, "find the pearls, open the sky river") | high | **FIXED 2026-08-03** — cut; the opener is the flight movie or nothing (§1.2) |
| **D1-2** | **Daddy Mermaid is not in the game.** The co-lead of the owner's premise, with three sacred family recordings sitting unused, appears in exactly one minigame cutout | high | Phases 2–4 |
| **D1-3** | Nothing persists. Five bunnies exist; all are visit-scoped; no room can be *completed*; there is no "you did it" for the whole castle | high | Phases 1, 4–7 |
| **D1-4** | Six of thirteen rooms are a voice line and a sparkle. The castle is the game's hub and most of it is scenery | high | §6, Phase 5 |
| **D1-5** | No day boundary anywhere in the game. Nothing ends, so nothing can begin | medium | Phase 7 |
| **D1-6** | **Tone conflict**: dust bunnies are "friendly helpers, never pests" in the art direction and a boss in `dust_boss.gd` | medium | §6.4 |
| **D1-7** | The Codex Day One (7 rooms, tap-3-times, flat Control) and the shipped castle (13 rooms, 2.5D, walk-to-touch) are **two incompatible castles**. Whichever ships, the other's content is stranded | medium | §2.3 decision |
| **D1-8** | Two designed rooms don't exist (Undercroft, Royal Loo) while their art does | low | Phase 6 |
| **D1-9** | The Codex opener depends on **two `.ogv` movies that were never made**, black-screening on both, while 36 finished frames sit unused | medium | Phase 2 (flipbook, no video). The *opener* slot now shows nothing at all until the flight movie lands (§1.2) |
| **D1-14** | The promenade's landmark cards kept 35% raw parallax, so the pearl plane visibly slid off its painted dock on the first screen | medium | **FIXED 2026-08-03** (§1.4) |
| **D1-10** | The 36 frames are **33 MB of PNG** — too heavy for the target phone as-is | medium | Phase 8 (§7.2) |
| **D1-11** | **The controls are never taught.** Touch-to-travel, two-press activation and tap-is-the-button were each discoverable only by accident | high | **FIXED 2026-08-03** — `day_one_guide.gd` teaches all three in the Sky Lagoon (§1.3); the hall bunnies then rehearse travel inside the castle |
| **D1-12** | No Day One probe exists on `dev`. `probe_story_day_one.gd` lives only on a stale Codex branch | medium | Phase 1 |
| **D1-13** | Most of the world is unreachable from normal play ([OW-6](design/04_OPEN_WORK.md#ow-6)); the castle is the only hub the child actually visits | high | §6.1, §6.2 — partial |

### 7.1 What Day One deliberately does *not* fix

[OW-2](design/04_OPEN_WORK.md#ow-2) (`world_style` reversibility),
[OW-3](design/04_OPEN_WORK.md#ow-3)/[OW-4](design/04_OPEN_WORK.md#ow-4)
(parallax and standee depth) and [OW-21](design/04_OPEN_WORK.md#ow-21) (device
measurement) are prerequisites for *quality*, not for this content. They should
land before Phase 8 activation, not before Phase 1 — Day One is being built in
the castle rooms, which already use real Sprite3D depth, not on the promenade
where the depth findings bite.

### 7.2 Asset weight before activation

33 MB of cinematic PNG cannot ship as-is on a Helio G88 with a 3-year-old
phone's storage. Options, cheapest first: re-encode the 36 frames to WebP
(≈4–6 MB, lossless-ish at this palette); or halve to 512×288, which is still
above the flipbook's on-screen size on a 1280×720 canvas. Decide at Phase 8;
until then the frames are excluded from both export presets (§9).

---

## 8. Characters to introduce on Day One

The brief asks to start introducing characters. Day One is the right place for
five, and the wrong place for everyone else — a four-year-old meeting twelve
new faces in one session remembers none of them.

| Character | Art | Voice | Day One role | New? |
|---|---|---|---|---|
| **Mermaid Roshan** | `characters/roshan_25d/*` | `roshan_*.ogg` | The player | no |
| **Daddy Mermaid** | `characters/friends/daddy.webp` (protected) | `daddy1/2/3.ogg` (**sacred family recordings**) | Co-lead. Flies the plane, hands out the tools in the hall, works alongside her in every room, eats dinner, says goodnight | **yes — first real appearance** |
| **Baby Eagle** | `assets/book/baby_eagle.png` (protected) | `sparkle*.ogg` | Rescued in the Playroom, then the third pair of hands in every later room. Becomes the first stuffie | partly — rescue is built |
| **Princess Huluu** | `characters/friends/huluu.png` | `huluu*.ogg` | Already at the throne. On Day One she is the one who *welcomes them to the castle*, which is a better first meeting than a crown award | no |
| **The dust bunnies** | `dirty_cleanup_2d/critters/dust_bunnies/*` | `hop_boing.ogg` | The mess, then the helpers, then the neighbours who get a home | partly |
| **The Imp** | `assets/sprites/story/arrival_imp.png` | `imp_*.ogg` | The reason the castle is dirty. Seen fleeing at the landing and peeking once per room. **Never a threat, never fought on Day One** | **yes — first appearance outside the Opera** |

Deliberately held back for later days: Wacky Chuck, Kareem the shopkeeper,
Evie, Harper, Faron, Rosalina, Mewsha, the Dust Bunny Boss (a *showing* only).

---

## 9. The deactivation contract

The Codex Day One art is in the tree and is **inert**. Three properties hold,
and each is mechanically checkable:

1. **No script loads it.** Every landed path is unreferenced by
   `scripts/**/*.gd`, except the six `critters/dust_bunnies/*.png` cards that
   were already live before this commit.
   ```
   grep -rn "cinematics/dirty_castle\|dirty_cleanup_2d/\(targets\|tools\|effects\|progress\|rooms\)\|sprites/story" scripts/
   ```
   must return nothing.
2. **It does not ship.** Both export presets exclude
   `assets/cinematics/dirty_castle/*`,
   `assets/castle/dirty_cleanup_2d/{rooms,targets,tools,effects,progress}/*`,
   `assets/sprites/story/*`, and — by exact path — the one new critter pose
   `critters/dust_bunnies/dust_bunny_siblings.png`. APK size is unchanged by
   this commit. The rest of `critters/` is deliberately **not** excluded: those
   five cards are live in the hall and the playroom today.
3. **Licences are recorded.** `ASSET_LICENSES.md` §"Day One dirty-castle art
   brought forward from Codex (2026-08-03)" carries one entry per family, with
   source, licence and modifications, in this same commit.

### Activation checklist (Phase 8)

- [ ] Re-encode the 36 frames (§7.2) and update the licence entry's
      "modifications" clause.
- [ ] Remove the six Day One patterns from `exclude_filter` in **both**
      presets in `export_presets.cfg`.
- [ ] `scripts/probe_day_one.gd` green in `ci.sh`, and the full suite green.
- [ ] One session on the M11 with the child before promotion to `master`.

### Landed in this commit

| Path | Count | Size | Live? |
|---|---|---|---|
| `assets/cinematics/dirty_castle/*.png` | 36 | 33 MB | no — excluded |
| `assets/castle/dirty_cleanup_2d/{targets,tools,effects,progress,rooms}/**` | 90 | 17 MB | no — excluded |
| `assets/castle/dirty_cleanup_2d/manifest.json` | 1 | — | no |
| `assets/castle/dirty_cleanup_2d/critters/.../dust_bunny_siblings.png` | 1 | 168 KB | no — excluded by exact path |
| `assets/sprites/story/arrival_imp.png` | 1 | 442 KB | no — excluded |
| `assets_src/concepts/dirty_castle_cleanup_2026-07-22/{PROMPTS,STORYBOARD_36_PROMPTS}.md` | 2 | 68 KB | n/a — source |
| `assets_src/concepts/dirty_castle_cleanup_2026-07-22/processed/*.png` | 16 | 15 MB | n/a — source |

Not landed: 121 MB of full-resolution generator output (`cinematic_raw/`,
`raw/`, `scene_references/`) and the `audit/` resemblance ledgers — retrievable
from `codex/dirty-castle-2d`.

---

## 10. Open questions for the owner

These change the work materially and should not be guessed at.

1. **How long should Day One be?** Twelve rooms at one encounter each is a
   45–60 minute first session — far past the "short sessions" rule. The plan
   above makes rooms 1–3 mandatory and 4–8 free-choice so the child can stop
   anywhere, but the alternative is a **shorter mandatory Day One** (hall,
   playroom, one room of her choice, bed) with the rest becoming Day Two.
   *Recommendation: the shorter version.* The rooms are not going anywhere.
2. **The Dust Bunny Boss on Day One — showing only, or fight?** §6.4 assumes a
   showing on the Undercroft stair and the fight on Day Two, which also buys
   time for the missing boss art.
3. **Does the Mermaid Pool become the reef entrance?** (§6.2.) This is a world-
   geography decision that touches [OW-13](design/04_OPEN_WORK.md#ow-13).
4. **Do the 36 frames play as one long opening, or split per room?** The plan
   assumes split — 01–08 before the hall, 09–13 before the playroom, and so on
   — so the child never watches more than eight pictures in a row.
