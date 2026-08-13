# Master design — the game

_Consolidated 2026-08-02 and authority-reconciled 2026-08-09 from AUDIT_3_0, DESIGN_3_0, CONVERSATION_AUDIT,
GAME_AUDIT_v3_49, AUDIT_REPAIR, AUDIT_UPGRADE, GAME_REDESIGN_2P5D_2026-07-27,
WORLD_MAP_2026-07-27, MINIGAME_ENGINES, MEDALS, STUFFIE_COMPANIONS,
DUNGEON_DIFFICULTY_AUDIT, the eleven-document Opera chain, FABLE_INTERACTION
_HANDOFF_2026-07-25, TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25, and the
2026-08-09 Ballerina, Boxer, Opera-quality and music reconciliations._

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

At the synchronized merged working-tree snapshot, the exact GAME2D inventory
remains **`UNSATISFIED`**: 509 model files/509 active exports, 157 tracked and
352 active-untracked generated model sidecars, 66 production 3D files, 74
probe 3D files, one scene, and one configuration. Regression mode is exact
`NO_REGRESSION` and all 14 falsification controls pass; strict remains open. The
older `f3b0de07` 68/77 values remain historical evidence. The old zone table is preserved in
`GAME_REDESIGN_2P5D_2026-07-27.md` as history; it is not a current
implementation queue.

The current working slice completes exact local `scripts/ci.sh` under Godot
`4.7.1.stable.official.a13da4feb` with exit 0 after 1428.6 seconds: all 64
trusted local probes, 74 GAME2D units, 93 visual-contract units, and the Castle
frame-review candidate
`1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9`
(13 assets/104 frames) are green in their machine/review ledgers. Exact-head
remote is pending. Seventeen V4 Mobile 1280×720 captures were visually inspected
only as diagnostic/review evidence; neither the candidate nor those captures
grant device, child, owner, or authoritative visual acceptance.

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
| Dolls / catch babies | one-finger press/drag catch | bounded Canvas/Node2D activity |
| Toy-castle brawler (co-op) | move + bop | legacy stage → Canvas/Node2D |
| Seek (Lamb-a') | hide & seek with animated clues/reveal | fourteen-node Canvas meadow with animated Evie/Lamb-a' actors |
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
| Opera careers ×13 | 53 career-specific phases across 27 shipping modes | `OperaCareerWorld2D` / Canvas specialist surfaces |

### The thirteen careers — current content, distributed final home

Thirteen careers, 53 shipping phases and 27 unique shipping modes form a set
of short, career-specific performances.
`OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md`,
`OPERA_2D_REBUILD_2026-08-01.md`, and
`OPERA_STAGE_INTERACTION_2026-08-02.md` still define the shared Canvas shell.
The later `BALLERINA_PARTY_REBUILD_2026-08-09.md` and
`design/BOXING_GAME_PROJECT_2026-08-09.md` are binding specialist overrides.
`OPERA_QUALITY_OVERHAUL_2026-08-09.md` and
`OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md` support the remaining career-
specific quality work, but their dated 52-phase count and their superseded
Ballerina, Boxer, or real-kart prescriptions are not current authority.

The careers do **not** all belong in one final Opera hub. Direct owner direction
in `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` section 10 / `7426c187` assigns
them to the Castle rooms whose pictures and objects explain the job:

| Castle room | Career entry points |
|---|---|
| Royal Kitchen | Pastry Chef, Candy Maker |
| Opera Hall | Ballerina, Pop Star, Magician |
| Royal Library | Detective |
| Craft Room | Painter |
| Stuffie Playroom | Stuffie Doctor, Boxer |
| Bubble Bath | Nursery Nurse |
| Mermaid Pool | Astronaut Engineer |
| Family Dining Room | Farmer |
| Cloud Movie Lounge **or** Courtyard | Racer — choose one canonical home before implementation |

This mapping preserves all thirteen current career activities and their stable
star identities; it changes discovery, launch, and return ownership. Opera Hall
is one venue for the three performances, not the front door to every job. The
current native `OperaLobby2D` with three floor tabs and every live career card
is a useful transitional Canvas surface but a rejected final hub under
`MA-OPERA-012`. The retired finale cards are no longer present.

- Each room-owned picture entry instantiates the existing
  `OperaCareerWorld2D`/specialist surface for its job and returns to that same
  launching room. There is no floor ladder or all-career back door.
- Selecting a job instantiates `OperaCareerWorld2D` over the career's
  **painted world**. The paintings are not decorative backdrops — they **are**
  the stages. Default career routes use normalized painted-walkway waypoints,
  task stations anchored to real landmarks, and magnifier clue spots
  (`opera_stage_paths.gd`). Full-stage specialists such as Ballerina and Boxer
  intentionally bypass station wandering without bypassing the Canvas stage.
- **The career owns the verb.** The earlier universal five-beat template is no
  longer a requirement. Shared routing, rewards, assistance and curtain-call
  ownership survive, but generic `bop` filler does not: the current table has
  zero generic `bop` phases.
- **Ballerina is a three-act full-stage recital:** Pearl Mirror watch-and-
  match, Ribbon Trail pearl guidance, and Grand Twirl around the shell music
  box. It has no station wandering, rival score, imp fight, generic task card,
  or looping four-cell pose row. Progress is monotonic; held pose keys and a
  one-shot curtain call preserve readable mermaid anatomy.
- **Boxer is a five-phase padded touch game:** Glove Guide, Jab Practice, Soft
  Guard, Title Imp, and Belt. It is completable with one finger, has no health,
  damage, fail state, lost combo, or lost progress, and uses its dedicated
  Canvas boxing surface rather than a generic combat engine.
- **Racer is a three-phase true-Canvas act:** Tune, To the Line, and a
  child-driven racing-circle finale using the exact `op_racer_lap_two` cue. The
  current repair removes the ordinary-headless legacy lobby/kart split and
  proves ordinary unforced entry uses this same Canvas implementation. Focused
  and full local exact-Godot coverage is green; `MA-OPERA-010` remains
  `FIXED_PENDING_VERIFICATION` until exact-head remote and external acceptance
  gates complete.
- **Competition is scoped, not assumed.** Where a career retains a rival or
  finale meter, it stays hidden until its declared finale and cannot create a
  loss. Friendly contact is harmless; zero input never earns progress.
- **Nursery Nurse (job 13) is cooperative,** not competitive: Nurse Faron is a
  visible partner from the first beat, never framed as an opponent.
- Completing a performance yields Warm Cheers / Big Cheers / Standing Ovation
  by pace, accuracy and guided retries. Every completed career earns its star
  regardless.
- **Curtain Dragon, Shadow Phantom, and Midnight Maestro are not careers or
  finales.** Owner ruling `3d1236fe` cuts all three. The current repair removes
  their cards, gates, required completion bits, and boss runtime while keeping
  stable save slots 4/9/14 as permanent tombstones. Raw legacy bits remain
  readable and completion masks only `0xBDEF`, the thirteen career slots.
  Focused and full local exact-Godot migration/reward/passive/teardown coverage
  is green, so `MA-OPERA-011` is `FIXED_PENDING_VERIFICATION`; do not convert or rewrite the
  characters as Opera bosses. Existing art/music may remain inactive for future
  reuse. Section 17 / `ef2fd982` allows future Ember-henchman boss fights as
  separately justified content, never in the retired Opera slots.
- **Royal Kitchen Chef launch remains deliberately unchanged.** Its current
  career configuration is valid and covered by the focused Opera/Castle probes,
  so no child-facing failure is reproduced. A speculative recovery branch for a
  future invalid configuration would change the sealed Castle controller and
  requires renewed owner visual approval; that latent hardening belongs to
  `MA-CODE-002`, not this Opera retirement slice.

### Music and spoken guidance

`MUSIC_AUDIT_2026-08-09.md` is the binding music-domain authority. Every
meaningful room, world or self-contained activity should sound like itself,
while remaining part of one gentle storybook score. The current catalog adds
42 deterministic area cues to 15 legacy music-directory files; 14 legacy
files are score and `banjo.ogg` is an SFX. Hard cuts are the current child-
readable transition language, and intentional minigame reuse is allowed only
when the activity is genuinely the same musical idea and restores its caller.

Music supports family voice, never competes with it: objective VO and a visual
cue still carry the non-reader contract, music ducks while a family
voice speaks, and music-off remains absolute. Composition/render/hash/loop and
routing checks are green in the merged work, but two-wrap listening, voice
intelligibility, mono fold-down and Lenovo Tab M11 start/loop/mix review remain
open. No machine metric pre-certifies those human or device judgments.

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
| Opera phase set | 3–5 career-specific beats with distinct causal verbs; no generic combat filler | Current 53-phase table plus binding specialist documents |
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
- **Opera stars** — `opera_stars` keeps its stable 16-slot bit namespace so
  existing saves never shift careers. The thirteen live career slots remain;
  owner-cut boss slots 4, 9, and 14 are inert tombstones. Completion masks only
  the live careers (`0xBDEF`), effective `opera_progress` is 0–13, and no floor
  gate depends on a tombstone. Existing retired bits are preserved raw but never
  reassigned to a new act.
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
  reachability proof, exact voice gaps, the rejected three-page all-career Opera
  hub (`MA-OPERA-012`), visual evidence and layering gaps, probe classification,
  device performance, and child comprehension evidence. The legacy Opera
  lifecycle and cut-boss retirement repairs are separately
  `FIXED_PENDING_VERIFICATION` as `MA-OPERA-010`/`011`.
- **`DEFERRED_WITH_REASON`:** the proposed world geography, dungeon lock/key
  expansion, Zelda-grammar verb expansion, unadopted chapter/daily-rhythm/
  naming/gifting/tending/decorating additions, and other new modes. This does
  not defer the binding Castle-room career distribution or Opera-boss cut.
- **`DISMISSED_NOT_IN_PROJECT` / `SUPERSEDED`:** dimensional rollback,
  `world_style` return-to-3D work, the old promenade pilot/order as a repair
  item, Meshy/Blender/model migration, owner-cut Opera bosses, 3D companions/
  worlds, the three-floor all-career hub as a final design, and landed-model
  retention. Their still-reachable runtime forms remain named repair debt, not
  permission to preserve the superseded product structure.
- **Targeted polish:** legacy slide/kart feel outside the Opera may be
  considered only as a bounded current-mode defect with evidence. Opera
  Racer's intended path is the Canvas circle activity; the current repair has
  removed its ordinary-headless alternate path and awaits full/external
  verification. Old work orders never authorize feature expansion or 3D
  implementation.

The current branch-status boundary is equally strict: Candymaker is integrated;
Painter-purpose and Arborist worktrees remain uncommitted candidates; Boxer V2
is a docs-only branch proposal. None changes the 13-career/53-phase/27-mode
shipping table until independently reviewed and integrated.
