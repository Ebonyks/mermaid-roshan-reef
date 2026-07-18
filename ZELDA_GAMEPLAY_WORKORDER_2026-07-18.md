# Zelda-Type Gameplay Expansion — Design Workorder (2026-07-18)

Companion to `JOLT_PHYSICS_AUDIT_2026-07-18.md`. Owner direction: enhance
gameplay and feel, expanding toward Legend-of-Zelda-type play as the game
grows, using more of the physics machinery where it earns its keep.

IP note (per CLAUDE.md art direction): Zelda/Wind Waker is a *mechanics and
rendering* reference only. No Zelda assets, symbols, names, UI, or music.

---

## 1. Where the game already is on the Zelda axis

More than expected — the *structure* exists, the *embodiment* doesn't:

| Zelda ingredient | Current state |
|---|---|
| Dungeon with rooms, checkpoints, boss | ✅ `DungeonLevel` — 10 rooms, combat/puzzle alternation, safe exits |
| No-fail combat, one button | ✅ `CombatArena` (analytic enemies/shots, bumps not damage) |
| Puzzle rooms (sequence/path/pairs/rotate) | ✅ `DungeonPuzzleRoom` — symbol puzzles, golden pointer, voice-led |
| Explorable overworld + sub-areas | ✅ reef, Sky Lagoon, castle, northern kingdom, courtyard |
| Traversal that is fun in itself | ⚠️ swim is solid but flat (no breach, no banking — see audit) |
| **Embodied interaction** (grab, push, throw, carry) | ❌ none — you tap USE near things |
| Items/tools that grow your verb set | ❌ cosmetic only (wardrobe/crafting) |
| Physicality (things topple, scatter, react) | ❌ only the dev-gated Jolt lab |

The telling detail: dungeon rooms teleport Roshan into an abstract room as a
**Sprite3D avatar** with its own `player_pos`/`MOVE_SPEED` — Zelda's loop
with the embodiment removed. In Zelda you carry your body, your tools, and
the world's physics *everywhere*; that continuity is most of the feel. The
expansion is therefore not "more modes" — it is **graduating adventure play
into the embodied world**.

## 2. Design pillars (unchanged, they bend but hold)

Every mechanic below passes: no fail states · non-reader (voice + `_say()`
+ visual pointer, symbols not text) · one finger + one button · mobile
renderer budget on the M11 · probe-deterministic (anything gating progress
stays analytic; see the audit's criticality rule).

Zelda without fail states is not a contradiction — exploration, tools,
locks-and-keys, and puzzle rooms never needed death; Wind Waker's joy is
mostly traversal + discovery + toy physics, all fail-free.

## 3. Mechanic roadmap, mapped to the physics boundary

### Tier E — Embodied verbs (analytic / ReefPhysics; progress may depend on these)

- **E1 Grab / carry / throw.** USE near a carryable prop → verb-layer scoop,
  prop rides a hand `BoneAttachment3D`; USE again → throw as a
  `ReefPhysics.free_medium` projectile (the fetch ball already flies this
  way). Unlocks: throw-at-switch, feed-a-critter, carry-the-key-pearl.
  This is THE keystone verb — most of Zelda's puzzle grammar is "move
  object A to place B."
- **E2 Push blocks.** Grid-snapped analytic push: hold stick into a block →
  it tweens one cell (blocked cells from the solids registry). Deterministic,
  probe-friendly, zero solver risk — Zelda block puzzles without Jolt.
- **E3 Switches, plates, doors.** Proximity/weight triggers (carried prop on
  a plate), shell-doors that stay open forever once opened (no relocking —
  no lost progress). All analytic dicts like the existing solids.
- **E4 Currents & jets.** Region velocity fields added to `player.vel` —
  fast fun rides, one-way shortcuts, lift shafts to the surface. Pure
  analytic, doubles as a traversal-feel win.
- **E5 Song as a tool.** The melody machinery becomes a Wind-Waker-baton
  analog: short echo-phrases in the world wake sleeping friends / open
  singing shells. Reuses `games/melody.gd` note UI.

### Tier J — Jolt garnish (non-critical only; gated on the M11 grading run)

- **J1 Play-corner knockables.** Graduate the physlab: ≤12 sleep-enabled
  bodies (barrel skittles by the shipwreck, pearl bowling). Nothing depends
  on them; solver jitter is charming, not harmful.
- **J2 Impact scatter.** Thrown props (analytic flight, E1) burst into brief
  Jolt debris on hit. Pattern: **logic analytic, garnish Jolt.**
- **J3 Rolling boulders / big set-pieces: NOT dynamic.** Authored kinematic
  paths that *look* physical. A dynamic boulder that wedges is a lost
  4-year-old.

### Tier S — Structure (the Zelda loop itself)

- **S1 Embodied puzzle rooms.** Port `DungeonPuzzleRoom` play into real
  arena spaces driven by `player.gd` (the castle basement / `arena_zones`
  pattern already supports interior floors). Same puzzles, real body.
- **S2 Tools progression.** Craftable/findable tools that add verbs — bubble
  wand (the combat shot, usable in the overworld), grabby starfish (E1),
  song shell (E5). Save keys additive per compatibility rule.
- **S3 Collectible spread.** Put existing collection/sticker items behind
  the new verbs (under a pushable block, behind a current, atop a throw
  target) — Zelda's heart-piece scavenger layer with zero new UI.
- **S4 Tap-to-look assist (lock-on lite).** Tap a distant interactive →
  camera orbit biases toward it + golden pointer fires. One-finger
  Z-targeting without a target button.

### Feel prerequisites (from the audit — do these first)

Banking/pitch, carving velocity alignment, speed-reactive camera, and the
parked ReefPhysics surface **breach**. Zelda-type play lives or dies on
traversal being fun before any puzzle exists.

## 4. Suggested generations (each ships probe-green to master)

1. **Feel:** audit Tier A (bank/pitch, camera, streamline pose), then merge
   the ReefPhysics player integration (breach + buoyancy) probe-gated.
2. **Hands:** E1 grab/carry/throw + `point`/`collect` verbs + E3
   switches/doors. New probes: probe_carry, probe_throw_switch.
3. **World:** E4 currents, E2 push-block grotto — the first embodied
   mini-dungeon inside the reef, S3 collectible spread.
4. **Toys:** J1/J2 pending the M11 physics grading; cleanse the lab into
   real play-corners or drop it per its header.
5. **Adventure v2:** S1 embodied dungeon rooms + S2 tools progression, one
   room per commit, `DungeonLevel` keeps owning order/checkpoints.

## 5. Probe policy for the expansion

Every new verb gets a probe (grab, push, current-ride); `probe_passive`
must stay silent (no auto-wins from new triggers); Tier J props get a
crash/persistence probe only — never a trajectory assertion, because solver
output is not deterministic across machines. The criticality boundary from
the Jolt audit is what makes this whole roadmap testable.
