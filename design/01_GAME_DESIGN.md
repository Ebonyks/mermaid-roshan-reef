# Master design — the game

_Consolidated 2026-08-02 and authority-reconciled 2026-08-09 from AUDIT_3_0, DESIGN_3_0, CONVERSATION_AUDIT,
GAME_AUDIT_v3_49, AUDIT_REPAIR, AUDIT_UPGRADE, GAME_REDESIGN_2P5D_2026-07-27,
WORLD_MAP_2026-07-27, MINIGAME_ENGINES, MEDALS, STUFFIE_COMPANIONS,
DUNGEON_DIFFICULTY_AUDIT, the eleven-document Opera chain, FABLE_INTERACTION
_HANDOFF_2026-07-25 and TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25._

---

## 1. The player, and the five rules that come from her

**Mermaid Roshan: Reef of Light** is an exact Godot 4.7.1-stable game built
for one specific four-year-old, played in landscape on a three-to-four-year-old
Android phone
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

## 2. The shape of the world — a true-2D living storybook

**Owner decision 2026-08-09 (binding, supersedes the dimensional parts of
`GAME_REDESIGN_2P5D_2026-07-27.md`).** The final game is a connected set of
true Canvas/Node2D storybook stages. `SideScrollStage`, a 3D play band,
depth-buffer sorting, and 3D camera staging are transition debt, not the final
medium. The 2026-07-27 charter remains historical evidence for the child-
readable navigation, touch-the-world, independent-card and differential-layer
goals that survive in 2D.

Three stated reasons, all of them accessibility reasons:

1. **Navigation** — free roaming without clear routes is too easy for a
   four-year-old to get lost in.
2. **Camera** — a predictable `Camera2D` and authored 2D composition remove
   the chased-camera burden.
3. **Input** — the analog stick was too ambitious for the age group.

Each panning stage targets four or five explicit Canvas depth classes where
the transparent-overdraw budget permits, a `Sprite2D` Roshan moving through a
clear play band, a gentle `Camera2D`, and obvious edge exits / door cards.
Fixed-camera activities may use fewer layers but remain subject to hierarchy,
ownership, cutoff, touch-target and figure/ground rules. **You cannot be lost
on a line.**

### The layering rule (owner note 2026-07-27 — binding on all stage design)

A stage set is never one painting. Every design is broken into depth-classed
pieces with a deliberate z home:

1. **Background layers** — `Sprite2D`/Canvas cards behind the play band;
   panning stages use at least two independently moving layers.
2. **Play-band cards** — individual cutouts with explicit owned `z_index` and
   2D parallax roles. Roshan passes in front of or behind the relevant card as
   the authored 2D ordering requires.
3. **Foreground occluders** — sparse Canvas framing only; never broad opaque
   scenery that hides Roshan.

**Corollary, binding on every art order:** anything Roshan can tap, pass, or
stand behind ships as its own sprite with its own 2D ordering role — never baked into a
mural. A mural that paints a "prop" at band depth is a layering bug.

> Current audit state: Sky Lagoon's one-mural-layer defect is
> `MA-VIS-002`; per-card occlusion coverage is `MA-VIS-005`. Closure requires
> true Canvas/`Sprite2D` evidence, not a legacy depth-buffer repair.

### Control grammar (replaces the stick)

1. **Touch the world and Roshan goes there.** Tap → she travels to that spot
   and stops (the goal persists to arrival). Hold → she follows the finger.
   The press is transformed into the live 2D stage coordinates.
2. **Tap a thing to use it.** The Hybrid Touch language, unchanged: discover
   ring → gold-ring acknowledge → approach → ready → act. Two-press
   activation on anything consequential.
3. **Tap = THE button** inside games.

The virtual stick, gamepad and keyboard remain functional behind the same
composite input read — an accessibility and desktop fallback, not the
curriculum. Final demotion of the auto-showing stick is the last phase of the
migration.

### Conversion order and evidence

The 2026-07-27 zone-order/pilot violation is `DISMISSED_NOT_A_DEFECT` under the
current rules. Sky Lagoon shipped before the proposed pilot; that process
lesson remains `HISTORICAL_EVIDENCE` but cannot be repaired retroactively. The
old requirement to keep a `world_style` route back to 3D is
`DISMISSED_NOT_IN_PROJECT`.

Current conversion is governed by `MA-2D-002` and the individual repair
protocol in `audit/MASTER_AUDIT_2026-08-09.md`: move one bounded gameplay
family at a time to Canvas/Node2D; preserve its verbs, saves, protected art and
no-fail behavior; archive retired 3D resources; run focused, passive,
teardown, re-entry, save/load, sibling and full-suite tests. Delete a legacy
resource only after its replacement or non-reachability proof is green.

At the synchronized committed snapshot, the exact GAME2D inventory remains
513 model files and 70 production 3D files and is **`UNSATISFIED`**. The old
zone table is preserved in `GAME_REDESIGN_2P5D_2026-07-27.md` as history; it
is not a current implementation queue.

### Geography — the world line (PROPOSAL, unapproved)

`WORLD_MAP_2026-07-27.md` proposed stitching every zone into one left-to-right
line with one branch:

```
TROPICAL OCEAN (far left, mirrored) → Reef home + lagoon shore → Pearl Castle
→ Mountain pass → Northern woods → Northern villages → Ice castle
                      └ branch ─→ FROZEN OCEAN (off the woods' shore)
```

**This geography is `DEFERRED_WITH_REASON`: it has never been approved and no
current work is authorized from it.** The separate reachability requirement is
`CONFIRMED_OPEN` as `MA-PLAY-001`: there is still no end-to-end fresh-save,
child-visible, no-cheat proof through every current destination. Re-enumerate
the live graph before adding routes; do not import the old destination list as
current fact without reproduction.

---

## 3. What the player does — the mode roster

Two legacy lifecycle families remain in the current code (detail in 03 §2):
**arena satellites** driven by main's
`_start_game → _tick_game → _end_game` lifecycle, and **standalone mode
nodes** that own their `_process` and report through a `finish_cb`. Lifecycle
ownership may survive conversion; any spatial presentation named below is
inventory/debt, never authorization to preserve or extend 3D.

| Mode | Verb | Current family / final presentation |
|---|---|---|
| Fetch (Chuck) | timed aim + throw | legacy arena → Canvas/Node2D |
| Dolls / catch babies | catch fallers | legacy stage → Canvas/Node2D |
| Toy-castle brawler (co-op) | move + bop | legacy stage → Canvas/Node2D |
| Seek (Lamb-a') | hide & seek | legacy arena → Canvas/Node2D |
| Treasure | checkpoint chain | legacy arena/course → Canvas/Node2D |
| Melody | collect 7 orbs | legacy theater → Canvas/Node2D |
| Shop | browse / buy | legacy cabin → Canvas/Control |
| Play-place course | checkpoint chain | legacy spatial course → Canvas/Node2D |
| Penguin / rainbow slide | steer, collect | rail behavior → Canvas/Node2D |
| Fairy pond | dodge + auto-shoot + nova | legacy spatial scroller → Canvas/Node2D |
| Kart race | steer / drift / turbo | legacy spline racer → Canvas/Node2D |
| Galaxy | explore / collect | legacy spatial one-off → Canvas/Node2D or owner-approved retirement |
| Combat arena | dodge + one-button shoot | legacy arena → Canvas/Node2D |
| Dungeon (10 rooms) | combat / puzzle alternation | legacy rooms → Canvas/Node2D; expansion deferred |
| Picture games ×5 | tap-to-place / chase | Canvas/Control |
| Dance | tap lanes on beat | Canvas/Control |
| Critter collection | approach + catch | 2D world cards |
| Stuffie battle | one-button attack + DODGE QTE | legacy arena → Canvas/Node2D |
| Opera careers ×13 | five-beat job performance | `OperaCareerWorld2D` / Canvas |

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
Battles are not turn-based: the child **controls the creature** in a 2D
overhead composition with one attack button plus forgiving DODGE quick-time
events. Current spatial arena staging is conversion debt. The Baby Eagle
playroom rescue is its wordless tutorial.

### The dungeon

The current dungeon has ten rooms alternating combat and puzzle, entered from
the castle and checkpointed by `dungeon_progress`. The proposed room-by-room
lock-and-key / “Zelda grammar” expansion in
`DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` is `DEFERRED_WITH_REASON`, not a
current defect or implementation authorization. Any retained dungeon gameplay
must migrate to true 2D. Zelda is a mechanics reference only — no Zelda
assets, symbols, names, UI or music, ever.

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

## 7. Design-idea lifecycle

The dated lifecycle in [04_OPEN_WORK.md](04_OPEN_WORK.md) and the master audit
controls; an older work order is never implementation authority by itself.

- **`CONFIRMED_OPEN`:** game-wide true-2D conversion, fresh-save no-cheat
  reachability proof, exact voice gaps, named Opera defects, visual evidence
  and layering gaps, probe classification, device performance, and child
  comprehension evidence.
- **`DEFERRED_WITH_REASON`:** the proposed world geography, dungeon lock/key
  expansion, Zelda-grammar verb expansion, chapter/daily-rhythm/naming/gifting/
  tending/decorating additions, and other new modes. Finish and prove the
  current game first.
- **`DISMISSED_NOT_IN_PROJECT` / `SUPERSEDED`:** dimensional rollback,
  `world_style` return-to-3D work, the old promenade pilot/order as a repair
  item, Meshy/Blender/model migration, 3D Opera bosses/companions/worlds, and
  landed-model retention. These remain dated history, not paused work.
- **Targeted polish:** slide-racer feel or kart parity may be considered only
  as a bounded current-mode defect with evidence; the old work orders do not
  authorize feature expansion or 3D implementation.
