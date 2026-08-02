# Master design — the game

_Consolidated 2026-08-02 from AUDIT_3_0, DESIGN_3_0, CONVERSATION_AUDIT,
GAME_AUDIT_v3_49, AUDIT_REPAIR, AUDIT_UPGRADE, GAME_REDESIGN_2P5D_2026-07-27,
WORLD_MAP_2026-07-27, MINIGAME_ENGINES, MEDALS, STUFFIE_COMPANIONS,
DUNGEON_DIFFICULTY_AUDIT, the eleven-document Opera chain, FABLE_INTERACTION
_HANDOFF_2026-07-25 and TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25._

---

## 1. The player, and the five rules that come from her

**Mermaid Roshan: Reef of Light** is a Godot 4.4 game built for one specific
four-year-old, played in landscape on a three-to-four-year-old Android phone
(target device: Lenovo Tab M11, Helio G88 / Mali-G52, "Speedy" quality tier)
with one finger, in short sessions.

Every design decision is weighed against her. Five rules follow, and none of
them is negotiable by any later document:

1. **No fail states.** Nothing is ever lost, no timer ends a game early, no
   run can be failed. Difficulty escalates *help*, never punishment: widen
   the target, slow the spawn, magnetize the pickup.
2. **No reading.** She cannot read. Every objective fires a voice line via
   `_say()` **and** shows a visual pointer. Text may decorate; it may never
   carry meaning.
3. **One finger, one button.** Tap = the button, everywhere. Touch the world
   to travel. No gestures beyond tap / hold / swipe / circle, no multi-touch
   requirement, no thumb coordination.
4. **Zero tolerance for lost progress.** Save keys are only ever added, never
   removed. Medals and stars are upgrade-only. The save file is backed up
   transactionally in-game and off-device (see 03 §7).
5. **Short sessions.** Any activity must be enterable, winnable and exitable
   inside a few minutes, from anywhere, without an adult.

**The child is growing.** The medal system (§5) exists because bronze keeps
the no-fail promise for the four-year-old of today while gold is a real
precision target sized for the six-to-eight-year-old she will become. Design
new content on both rails.

---

## 2. The shape of the world — the 2.5D promenade

**Owner decision 2026-07-27 (binding charter, `GAME_REDESIGN_2P5D_2026-07-27.md`).**
The game is being fundamentally redesigned from a free-swim 3D world into a
connected set of **2.5D storybook promenade stages** — diorama pages the child
walks across — built on the E2 `SideScrollStage` engine.

Three stated reasons, all of them accessibility reasons:

1. **Navigation** — free-roam 3D is too easy for a four-year-old to get lost in.
2. **Camera** — a chased 3D camera is a problem to manage; a staged side-on
   camera is not. The camera problem is *deleted*, not managed.
3. **Input** — the analog stick was too ambitious for the age group.

Each promenade is a parallax flat stack (4–5 painted layers), a play plane
(the real rigged 3D Roshan walking a wide x-band with a shallow z-band), a
fixed side-on camera with gentle follow, and edge exits / door cards
connecting stages into a linear-with-branches map. **You cannot be lost on a
line.**

### The layering rule (owner note 2026-07-27 — binding on all stage design)

A stage set is never one painting. Every design is broken into depth-classed
pieces with a deliberate z home:

1. **Background murals** — behind the walk band, can never overlap Roshan.
2. **Play-band standees** — individual cutouts standing at real depth *inside*
   the band. Roshan passes in front of or behind each one depending on her z,
   sorted by the real depth buffer. This is the heart of the look.
3. **Foreground occluders** — between her and the camera. Sparse framing only.

**Corollary, binding on every art order:** anything Roshan can tap, pass, or
stand behind ships as its own sprite with its own depth — never baked into a
mural. A mural that paints a "prop" at band depth is a layering bug.

> Status note: as of 2026-08-02 the shipped Sky Lagoon promenade violates both
> the parallax rule and the standee-depth rule. See [04 OW-2 and OW-3](04_OPEN_WORK.md).

### Control grammar (replaces the stick)

1. **Touch the world and Roshan goes there.** Tap → she travels to that spot
   and stops (the goal persists to arrival). Hold → she follows the finger.
   The press is projected onto the play plane: x free, screen height mapped
   into the depth band.
2. **Tap a thing to use it.** The Hybrid Touch language, unchanged: discover
   ring → gold-ring acknowledge → approach → ready → act. Two-press
   activation on anything consequential.
3. **Tap = THE button** inside games.

The virtual stick, gamepad and keyboard remain functional behind the same
composite input read — an accessibility and desktop fallback, not the
curriculum. Final demotion of the auto-showing stick is the last phase of the
migration.

### Zone migration order (charter §2)

| # | Zone | Becomes | State 2026-08-02 |
|---|---|---|---|
| 1 | Reef home (free-swim) | Reef Promenade — **the pilot** | **not started** (OW-4) |
| 2 | Pearl Castle halls | One promenade per floor; stairs = door cards | partly — `castle_rooms_25d.gd` ships a Sprite3D two-screen hub + 7 rooms |
| 3 | Courtyard | Promenade; train keeps its rail | not started |
| 4 | Sky Lagoon | 2–3 linked promenades | **shipped first, out of order** (`sky_lagoon_promenade.gd`) |
| 5 | Northern kingdom | Promenade chain | not started |
| 6 | Ember Fortress / Butterfly World | Promenades | not started (Ember has approved 2D concept art) |
| 7 | Galaxy | LAST, or retired to a picture-game — owner call | not started; 11.7 MB of orphaned art |

Each zone is its own branch, its own painted set, its own probe, merged to
`dev` only green. Free-swim code for a migrated zone is attic'd — never
deleted — one full promotion cycle later.

### Geography — the world line (PROPOSAL, unapproved)

`WORLD_MAP_2026-07-27.md` proposes stitching every zone into one left-to-right
line with one branch:

```
TROPICAL OCEAN (far left, mirrored) → Reef home + lagoon shore → Pearl Castle
→ Mountain pass → Northern woods → Northern villages → Ice castle
                      └ branch ─→ FROZEN OCEAN (off the woods' shore)
```

**This has never been approved and no code has been written against it.** Four
decisions are still open — see [04 OW-9](04_OPEN_WORK.md). Its single most
important finding stands independently of the geography question: *the game is
not currently stitched at all.* The courtyard hub that connected the zones was
orphaned by the promenade rewrite, leaving both ocean kingdoms, the Magic
Cave, Butterfly World, Ember Fortress, both Rainbow Race legs and the wall
picture games unreachable in normal play. Restoring reachability is a
precondition for everything else, not a polish task ([04 OW-5](04_OPEN_WORK.md)).

---

## 3. What the player does — the mode roster

Two architectural families (detail in 03 §2): **arena satellites** driven by
main's `_start_game → _tick_game → _end_game` lifecycle, and **standalone mode
nodes** that own their `_process` and report through a `finish_cb`.

| Mode | Verb | Perspective | Engine |
|---|---|---|---|
| Fetch (Chuck) | timed aim + throw | 3D arena | one-off |
| Dolls / catch babies | catch fallers | 2.5D stage | **E2** |
| Toy-castle brawler (co-op) | walk the plane + bop | 2.5D stage | **E2 brawl** |
| Seek (Lamb-a') | hide & seek | 3D arena | one-off |
| Treasure | checkpoint chain | 3D arena | K1 (via slide course) |
| Melody | collect 7 orbs | 3D theater | bespoke → K1 |
| Shop | browse / buy | 3D cabin | one-off |
| Play-place course | checkpoint chain | 3D vertical | K1 host |
| Penguin / rainbow slide | steer, collect | on-rails | slide_race → E4 `rail` |
| Fairy pond | dodge + auto-shoot + nova | overhead scroller | **E3** (single-tenant) |
| Kart race | steer / drift / turbo | 3D spline | **E4** |
| Galaxy | explore / collect | spherical platformer | deliberate one-off |
| Combat arena | dodge + one-button shoot | overhead octagon | → E1 |
| Dungeon (10 rooms) | combat / puzzle alternation | overhead octagon | → E1 |
| Picture games ×5 | tap-to-place / chase | 2D canvas | K2 |
| Dance | tap lanes on beat | 2D canvas | K2 |
| Critter collection | approach + catch | ambient in-world | — |
| Stuffie battle | one-button attack + DODGE QTE | overhead octagon | own node |
| Opera careers ×13 | five-beat job performance | staged 2D | OperaCareerWorld2D |

### The Pearl Opera — the largest wing

Thirteen careers, each a self-contained two-minute performance. Architecture
authority: `OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md`; structure
authority: `OPERA_2D_REBUILD_2026-08-01.md`; interaction authority:
`OPERA_STAGE_INTERACTION_2026-08-02.md`.

- Entry opens a **native 2D lobby** (`OperaLobby2D`) — three floor tabs,
  picture-first job cards, star progress, spoken hints. No 3D lobby, avatar,
  camera or lift is built in normal play.
- Selecting a job instantiates `OperaCareerWorld2D` over the career's
  **painted world**. The paintings are not backdrops — they **are** the
  stages: each carries a walkable route of normalized waypoints tracing the
  painted walkways, 4–5 task stations anchored to real painted landmarks, and
  8 magnifier clue spots (`opera_stage_paths.gd`).
- **Every career runs the same five-beat arc:** short imp scuffle (~10 s) →
  learn the job, one gentle verb (~8 s) → do the job, 2–3 distinct verbs, no
  verb repeated (~30 s) → big scuffle, the imp captain steals the career's
  goal prop (~15 s) → stage finale, the dressed rival enters, winning wins the
  prop back (~35 s).
- **The rival stays hidden until the finale.** Score bars, timer and rival
  movement are paused and invisible for the first four beats. The finale is
  normalized to the last 2 phases (~30 %) of every act.
- **Combat is kid-safe.** Imps are friendly mischief; taps anywhere fizzle
  sparkles and still trickle progress; nothing can be lost. The captain's two
  bops are reserved so he can never be mashed past.
- **Nursery Nurse (job 13) is cooperative,** not competitive: Nurse Faron is a
  visible partner from the first beat, never framed as an opponent.
- Completing a performance yields Warm Cheers / Big Cheers / Standing Ovation
  by pace, accuracy and guided retries. Every completed career earns its star
  regardless.

### The stuffed-friend companions

A Pokémon-shaped wing with the fail states removed (`STUFFIE_COMPANIONS.md`,
authoritative). Choose one stuffed friend, paint its colours, it follows
Roshan after she reaches Princess Huluu, and it grows through **Tamagotchi
care** (owner 2026-07-20 — this replaced the earlier collectible model).
Battles are not turn-based: the child **controls the creature** in an overhead
arena with one attack button plus forgiving DODGE quick-time events. The
Baby Eagle playroom rescue is its wordless tutorial.

### The dungeon

Ten rooms alternating combat and puzzle, entered from the castle,
checkpointed by `dungeon_progress`. `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md`
holds the full room-by-room age-4 difficulty read and a lock-and-key
("Zelda grammar") redesign that has **not** been implemented. Zelda is a
mechanics reference only — no Zelda assets, symbols, names, UI or music, ever.

---

## 4. Pacing standards

| Activity class | Standard | Source |
|---|---|---|
| Opera career act | ~2 minutes of real play; advisory sim band 70–150 s median | OPERA_2D_REBUILD_2026-08-01 |
| Opera act beats | 3–4 distinct beats with **different verbs**; no verb twice in one act | OPERA_ACT_REDESIGN_2026-07-25 |
| Arena minigame | enterable → winnable → exitable in a few minutes | AUDIT_REPAIR |
| Any objective | voiced within ~2 s of becoming active, pointer visible | hard rule |

"Longer" must never mean "more of the same". An act that presses fourteen
candies instead of seven is twice as long and half as good.

---

## 5. Progress, reward and currency

`MEDALS.md` is authoritative for the ranking system; this is the summary.

- **Stars** — one per friend / career / major activity. The primary progress
  currency, shown on the HUD, persisted per name.
- **Pearls** — the spendable currency (`pearls`, lifetime `pearls_ever`),
  earned everywhere, spent at the Manta Pearl Shop.
- **Medals** — 🥉🥈🥇 per game id, purely glyph-based for a non-reader.
  Bronze = completion, always awarded, never denied. **Upgrade-only:** a
  slower replay keeps the better medal. **Win-path only:** `probe_passive`
  asserts that zero-input play can never touch `m.medals`.
- **Opera stars** — a bitmask (`opera_stars`, 16-bit since job 13), with
  floor gating on the lobby.
- **Companion growth** — `fish_tokens`, `care_points`, `stuffie_wins`.

All of it funnels through one `_reward()` director; no mode may write pearls,
stickers or save state on its own path.

### Save contract

`reef_save.json`, transactional with a `.bak` recovery path. `KNOWN_KEYS` is
append-only:

```
schema_version won found finale music quality touch_mode pearls pearls_ever
portal_unlocked skin level2 plays custom_fish custom_friends crafts galaxy
bwdone fairyskin combat_ice combat_fire dungeon_progress dungeon_done
opera_progress opera_stars opera_done opera_pantry stickers owned animals
critters companion companion_colors fish_tokens stuffie_wins care_points
companion_resting companion_bruises lagoon_plane_departed
```

`medals` and `critters` sit deliberately outside `KNOWN_KEYS` so pre-medal
saves still read as schema-complete. Renamed friends migrate forward by
legacy key (`Daddy Mermaid` ← `Gabby`) so no star is ever lost.

---

## 6. Cast and story

Canonical characters come from the owner's book, `Mermaid_Roshan_INTERIOR_A5.pdf`:
Roshan, Evie / Lamb-a', Harper & Fiona, Faron, Wacky & Chuck, Princess Huluu,
Daddy Mermaid. **Gabby is removed** under an IP hold; her assets are preserved
in `attic/gabby/` and must not be reintroduced without an owner-approved
redesign. Her reef slot became Daddy Mermaid on 2026-07-19.

Roshan's identity anchors, which no art pass may drift: chestnut hair, front-
left rainbow forelock, lavender clothing, green-right / pink-left tail.

The opening cinematic is produced under a separate, stricter regime — see
02 §7.

---

## 7. Design work that is decided but unbuilt

Listed here so it is not rediscovered a fourth time; tracked with status in
[04_OPEN_WORK.md](04_OPEN_WORK.md).

- The **dungeon lock-and-key redesign** (DUNGEON_DIFFICULTY_AUDIT_2026-07-18 §4).
- The **Zelda-grammar verb set** — grab / push / switch, embodied rooms
  (ZELDA_GAMEPLAY_WORKORDER_2026-07-18, tiers E and S).
- The **world stitch** and its reachability probe (WORLD_MAP_2026-07-27 §7).
- The **reef promenade pilot** and `world_style` reversibility toggle
  (GAME_REDESIGN_2P5D charter §3, P2).
- **Slide-racer feel** work (RACE_FEEL_WORKORDER) and kart-class drift/turbo
  parity (KART_FEEL).
