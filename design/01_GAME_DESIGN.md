# Master design — the game

_Consolidated 2026-08-02 and authority-reconciled 2026-08-09 from AUDIT_3_0, DESIGN_3_0, CONVERSATION_AUDIT,
GAME_AUDIT_v3_49, AUDIT_REPAIR, AUDIT_UPGRADE, GAME_REDESIGN_2P5D_2026-07-27,
WORLD_MAP_2026-07-27, MINIGAME_ENGINES, MEDALS, STUFFIE_COMPANIONS,
DUNGEON_DIFFICULTY_AUDIT, the eleven-document Opera chain, FABLE_INTERACTION
_HANDOFF_2026-07-25, TOUCH_CENTRIC_REVERSIBLE_HANDOFF_2026-07-25, and the
2026-08-09 Ballerina, Boxer, Opera-quality and music reconciliations._

_Document-authority sources `5ed0c754`/`7eb94595` remain the exact CHG-029
chain. Exact parent `e6edf559af219edd4e5ce38cab0c5094483be5c6` passes integrated
dev Probe Suite run `31722047536` with probes 34m25s/63-of-63, 36 document
tests, six/six stress, 316/316 inventory/ledger, 34 active/36 retained records,
and music 3m33s/42-of-42. Earlier branch run `31719143975` is corroborating e6
history. Current Sky true-Canvas source
`51d0abc0d32855a8ba32932599fedd8f59b398b7`, exact parent `1b7d6bda`, changes
19 paths (+3,318/-3,517) and passes official Godot 4.7.1 full local CI in
1,404.5 seconds/all 64. Run-14 is local Mobile/Speedy 20/20 with manifest/PNG
and probe hashes `AEAC7C72…DE34` and `B9EAF5E0…9C6C`; its source revision
remains unknown. Governance-only integrated head
`441adf35f7dbdeb67d36fbf1a2217b87d3040d47` preserves unchanged source
`51d0abc0`, passes exact local CI in 1,391.5 seconds/all 64, passes topic/dev
Probe runs `31760207048`/`31762132976`, and has exact-head Android run
`31763879294`. Both remote Sky diagnostics remain renderer failures after 20
PASS rows because missing `VK_KHR_surface` forces llvmpipe/
`gl_compatibility`; they upload PNGs but no JSON or Mobile PASS. Historical
`7391c53c` run `31728755204` retains the prior failed remote Sky renderer
subprocess. The
master audit/design language are
`CANONICAL_CURRENT`; the game-wide audit remains `IN_PROGRESS` /
`UNSATISFIED`._

---

## 1. The player, and the five rules that come from her

**Mermaid Roshan: Reef of Light** is an exact Godot 4.7.2-stable game built
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

> Current audit state: source `51d0abc0` repairs Sky Lagoon as an owned
> `CanvasLayer` -1 with a 6144×2048 `Node2D` master, 6×2 `Sprite2D` backdrop,
> differential layers/parallax, sole `Camera2D`, five readable animals, three
> playground actions, and master-coordinate movement/touch/routes. It reuses
> approved art unchanged. Exact local CI and run-14 are green, moving
> `MA-VIS-002` to `FIXED_PENDING_VERIFICATION`. Exact `441adf35` topic/dev
> machine suites and APK now exist, but the remote Sky subprocess still lacks
> a requested-Mobile renderer PASS/JSON. Target-device, child, owner, and
> accepted-visual evidence remain open, and broader `MA-VIS-006` stays
> `CONFIRMED_OPEN`.

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

At current source `51d0abc0d32855a8ba32932599fedd8f59b398b7`, the exact GAME2D inventory
remains **`UNSATISFIED`**: 509 model files/509 active exports, 157 tracked and
352 active-untracked generated model sidecars, 65 production 3D files, 70
probe 3D files, one scene, and one configuration. Regression mode is exact
`NO_REGRESSION` and all 14 falsification controls pass; strict remains open. The
older `f3b0de07` 68/77 values remain historical evidence. The old zone table is preserved in
`GAME_REDESIGN_2P5D_2026-07-27.md` as history; it is not a current
implementation queue.

Commit `09e5e356` completes exact local `scripts/ci.sh` under Godot
`4.7.1.stable.official.a13da4feb` with exit 0 after 1463.4 seconds: all 64
trusted local probes, 74 GAME2D units, 93 visual-contract units, and the Castle
frame-review candidate
`1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9`
(13 assets/104 frames) are green in their machine/review ledgers. Historical
exact-head verification run `31661887863` succeeds at predecessor
integrated SHA
`e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0`: Ubuntu succeeds in 33m8s through
checkout/checksum, exact Godot, static/import/full analyzer, all 63 trusted
probes, boot, Dust/Opera advisories, and Opera manifest. All five capture/upload
pairs completed at the workflow level and uploaded diagnostic artifacts;
Windows succeeds in
6m52s with terminal result
`MUSIC|check 42/42|picture_xmas`. Remote GAME2D remains exact 509/66/74
`NO_REGRESSION`/`UNSATISFIED`. Current `09e5e356` produced twenty-two V4 Mobile
1280×720 captures—nine room routes and thirteen career surfaces—inspected only
as diagnostic/review evidence; neither the candidate, those captures, nor the
five predecessor remote pairs grant device, child, owner, or authoritative
visual acceptance. At that product-runtime checkpoint, exact-head remote,
matching APK, exact voice, human listening, and strict-zero 2D evidence were
open; the later attempt and probe repair are recorded next.

Later GitHub run `31678156887` at pre-fix audit head `3fc151c8` is genuinely
red, but not from production behavior or a regex false positive. Ubuntu
`probe_opera` sampled the 0.25-second reveal after four frames, so only the
Detective and Nursery stable-Canvas compound checks ran before Castle ambient
layer 15 settled to Opera layer 11; their routes, passive behavior, saves,
rewards, exact-room returns, dedicated probes, every other executed gate/probe,
and Windows passed. Probe-only commit `ff068db` preserves runtime `09e5e356`,
replaces that guess with a bounded fail-closed semantic wait, and passes exact
local full CI in 1379.3 seconds with all 64 probes. Historical checkpoints
through exact parent `e6edf559` pass their bounded local/remote machine gates;
the parent's inherited Sky 21-OK/44-FAIL/DONE output remains predecessor
history. Historical source `7391c53c` and run `31728755204` preserve the prior
failed remote Sky renderer subprocess. Current product source `51d0abc0`
passes full local in 1,404.5 seconds/all 64 and run-14 is local Mobile/Speedy
20/20 with manifest/PNG/probe hashes but an unknown source revision.
Governance-only integrated head `441adf35` passes a separate exact local
1,391.5-second/all-64 run plus topic/dev Probe runs `31760207048`/
`31762132976`, each with 63/63 trusted headings and zero hard failures. Their
nonblocking Sky subprocesses still fail renderer identity after 20 PASS rows,
upload PNGs only, and provide no remote JSON/Mobile PASS.
Integrated-predecessor Android run `31724927769` uses raw checkout/package
source exact e6 and publishes that predecessor's matching dev APK
(596,041,412 bytes; SHA-256
`66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`).
Exact-head Android run `31763879294` publishes the governance-integrated
`441adf35` dev APK (596,033,220 bytes; SHA-256
`f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`) over
unchanged product source `51d0abc0`.
Device, child, owner, exact-voice, listening, strict-2D, and accepted-visual
gates remain open.

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
| Cloud Movie Lounge | Racer — canonical home selected at `09e5e356` |

Commit `09e5e356` implements this mapping while preserving all thirteen current
career activities and their stable sparse save/star identities. Opera Hall is
one venue for the three performances, not the front door to every job. The
native three-floor `OperaLobby2D` is deleted, no hidden/off-room route restores
it, and every activity returns to its exact launching room. Exact focused probes
and the full runtime 1463.4-second plus repaired-head 1379.3-second/64-probe
local suites are green, moving
`MA-OPERA-012` to `FIXED_PENDING_VERIFICATION`. The 22 captures are diagnostic;
the nine room captures show a residual P2 composition defect because the
154×154 lower-center cards obscure Roshan's lower body/tail. Parent
`e6edf559` is remote-green in dev run `31722047536`; current integrated head
`441adf35` is local/topic/dev-machine green and has its exact-head dev APK.
Its remote Sky diagnostic remains non-authoritative after falling back to
`gl_compatibility`, with no JSON/Mobile PASS. Device,
child, owner, exact-voice, listening, strict-2D, and accepted-visual evidence
remain open.

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
  and full local exact-Godot coverage plus exact-head remote CI are green;
  `MA-OPERA-010` remains `FIXED_PENDING_VERIFICATION` until external acceptance
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
  plus exact-head remote CI are green, so `MA-OPERA-011` is
  `FIXED_PENDING_VERIFICATION`; do not convert or rewrite the
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

Contiguous CHG-029 sources `5ed0c754`/`7eb94595` inventory and harden all 316
tracked Markdown paths exactly once and record all 36 material findings,
including retained terminal history, in
[`ACTIVE_FINDINGS_2026-08-13.md`](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md).
The chain's fail-closed validator has 36 focused tests and six mutation controls
green. Exact parent `e6edf559` preserves that verified authority and passes
integrated dev Probe Suite `31722047536`; earlier branch `31719143975` is
historical corroboration, so `MA-DOC-002` and `MA-DOC-005` remain
`VERIFIED_FIXED`. Manual/non-emitting CHG-031 owns exact 19-path source
`51d0abc0`, including `scripts/probe_northern.gd`; current catalog counts are
31 IDs/79 references/four emitters/25 planner tests/27 manual groups.

- **`CONFIRMED_OPEN`:** game-wide true-2D conversion, fresh-save no-cheat
  reachability proof, exact voice gaps, visual evidence and remaining layering
  gaps, probe classification, device performance, and child comprehension
  evidence. The single Opera lifecycle, cut-boss retirement, and implemented
  Castle-room distribution are separately `FIXED_PENDING_VERIFICATION` as
  `MA-OPERA-010`/`011`/`012`; none is closed by local diagnostics.
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
