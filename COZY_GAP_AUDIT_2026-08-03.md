# Cozy-game gap audit (2026-08-03)

Question asked: *the game is meant to be a cozy game for a 4-year-old — what
major things are missing?* Known work-in-progress named by the owner:
**clothing customization** and **decorating the castle**. This document is the
codebase-grounded answer: what is genuinely absent, ranked by how much it costs
the cozy experience, with the two named items placed inside that ranking rather
than beside it.

Scope note: this is an analysis document only. No runtime code changes.

---

## 0. What is already strong (so it does not get rebuilt by mistake)

- **Fiddle-with-the-world affordances.** `castle_rooms_25d.gd` carries ~104
  props across 13 rooms, of which 38 have a `semantic_action` animation
  (`open_oven_door_and_warm_fire`, `topple_and_restack_blocks`,
  `turn_taps_and_fill_bubbles`, `chandelier_light_chase`, …) plus 18
  `roleplay_action` verbs. Tapping things and having them respond is the single
  most cozy-correct system in the game and it is already good.
- **No-fail discipline** is real and probe-enforced (`probe_passive.gd`,
  MEDALS.md: medals are add-only, never denied).
- **Care without decay.** `companion.gd` explicitly documents "one want at a
  time, wants wait forever, nothing ever decays" — exactly the right shape for
  this age. It is the one system in the game that models cozy correctly.
- **Save durability** — transactional writes, backup, schema versioning,
  legacy-key migration (`save_state.gd`).

The gaps below are not "the game is bad"; they are the places where a large,
well-built world does not yet close a cozy *loop*.

---

## 1. The world is not connected — the highest-cost gap

A cozy game is a place you wander. This one is currently a set of pockets, and
most of them are unreachable in normal play.

- `main.gd:4023-4026` — entering Sky Lagoon in the `court` phase builds the
  promenade and `return`s. `_populate_courtyard_touch_interactables()`
  (`main.gd:3633`) is therefore dead code, and `main.gd:3624` explicitly
  early-returns for the promenade phase.
- `sky_lagoon_promenade.gd` registers **five** targets total: plane, slide,
  swing, seesaw, castle gate (`:529-557, :641`).
- The destinations the retired courtyard used to offer are consequently
  orphaned: **Northern Kingdom** (`main.gd:3721`, dead branch), **Butterfly
  World / Galaxy** (`main.gd:3726`, dead branch), **Ember Fortress**, the ocean
  kingdom gates, the wall picture games, the Dream Stars, both Rainbow Race
  legs. The old 3D lagoon still contains the calls (`sky_lagoon.gd:2491, 2516`)
  but that build path no longer runs in the `court` phase.
- `WORLD_MAP_2026-07-27.md` still opens with *"Status: PROPOSAL. No code has
  been written against this."*

So the game today reads as: reef free-swim → portal → a five-target promenade →
castle interior. A large fraction of the shipped content is content the child
cannot walk to. **Everything else in this document is worth less until this is
fixed** — decorating a castle you can reach is fine, but the promise of a cozy
world is that there is somewhere to go tomorrow.

---

## 2. Nothing the child does changes the world permanently

This is the real cozy core loop, and it is the umbrella the owner's two named
items sit under: **earn → own → place → see it again tomorrow.**

Current state:

- **Decorating: does not exist in any form.** Every castle prop is a hard-coded
  dictionary entry with a fixed `pos`, `z`, `scale` and `tex_path`. There is no
  placement, no slot, no inventory, no ownership. `grep -i decor` across
  `scripts/` returns only `ember_fortress.gd:_build_decor` and
  `galaxy.gd:_build_decor` — static scenery builders — plus the opera cake
  `decorate` beat, which is a minigame phase, not room decor.
- **The save schema has no room state at all.** `save_state.gd:KNOWN_KEYS` has
  no decor, room, furniture, or placement key. A decor system needs new keys
  (added with defaults — never remove, per the hard rules).
- **Clothing: three mutually exclusive full skins.** `main.gd:517-521` —
  `classic`, `fairy`, `huluu`. `wardrobe_ui.gd` is a one-of-three picture
  picker. There are no slots, no layers, no colors, no unlocks, no per-piece
  ownership. `CHARACTER_CUSTOMIZATION.md` §4 specified the composable loadout
  system (sockets / material variants / morphs) in June and it was never built —
  and the 2026-07-27 redesign changed its physics anyway (see §8).

The consequence: a four-year-old can do a great deal in this game and own
nothing at the end of it. Everything won is a star, a sticker, a medal or a
number. The only persistent things she *makes* are craft-studio creatures
(`custom_fish`) — and even those auto-spawn into the reef rather than being
placed anywhere she chose.

---

## 3. The pearl economy has no sink

Directly connected to §2, and the reason clothing/decor pay for themselves.

- `shop.gd:212-224` hides every ware except **beans (2 pearls)**.
- `shop.gd:382-386` hard-refuses to sell anything but beans — the Rainbow Trail
  (60), Pearl Tiara (120) and Pearl Princess (250) remain in `SHOP_ITEMS` for
  save compatibility only, retired 2026-07-13 when their assets stopped fitting.
- The only other sinks are the four animal tanks (20/25/30/40) and two craft
  unlocks.

Total lifetime spendable: roughly 135 pearls. Everything earned after that is a
number that only grows. Clothing pieces and decor items are the obvious, correct
sink — they close the loop that is currently open at both ends.

---

## 4. Instructions and rewards are written English

`show_msg()` (`audio_director.gd:60-66`) sets HUD text and fires a **generic
per-speaker "talk" bark** — the words themselves are never spoken. There are 374
`show_msg` call sites across `scripts/` versus 46 event-specific `_say` calls
(the voice library does have event clips, e.g. `faron_op_nursery_catch.ogg`, so
the mechanism exists — the coverage does not).

For a non-reader that means the *content* of nearly every objective, hint,
reward and shop interaction is invisible; she gets a friendly noise and a wall
of text. UI labels are the same shape ("Pick your look!", "✦ WEAR IT!", the
pause menu) — glyph-supported, but text-first.

CLAUDE.md already binds new objectives to `_say()` + a visual pointer. The gap
is the accumulated back catalogue. A cozy game for this age should be fully
playable with the screen text removed.

---

## 5. The world has no rhythms

`save_state.gd:74-76`: `plays` increments per launch and `is_night = plays % 2`.
Day and night therefore flip **per app launch**, not with time. There is no
clock, no weather, no seasons, no "come back tomorrow" gift, no daily ritual,
nothing that is different because it is morning or because a day passed.

Gentle recurrence is most of what makes a cozy game feel alive between
sessions, and it is one of the cheapest systems here: the save file already
persists, it just never records a date.

---

## 6. Nothing to tend but the stuffie

`companion.gd` gets caretaking exactly right (feed / nap / bath / cuddle, no
decay, no nagging). Nothing else in the world can be tended:

- The animals bought out of the tanks swim away and are never interacted with
  again (`ANIMAL_SHOP`, `main.gd:576-590`).
- No planting, growing, watering, or harvesting anywhere in the game.
- No tidying that persists — the dust bunnies are combat encounters, not chores.
- No feeding, brushing, or naming any creature other than the companion.

For a four-year-old, tending is the most reliable cozy verb there is, and the
engine for it is already written and probe-gated.

---

## 7. No making-for-someone, no naming, no showing off

- **Craft studio** makes a fish, cat or bird by choosing two or three colors.
  That is the whole creation surface, and the output is not given to anyone or
  placed anywhere — it auto-spawns into the reef.
- **No gifting.** There is no way to give a friend anything, no mailbox, no
  "made this for you" beat, despite a roster of family-voiced friends.
- **No naming.** The stuffie, the released animals, the crafted creatures and
  the rooms are all unnamed. Naming needs no literacy if it is a picture/voice
  list rather than a keyboard.
- **No showing off.** The Sticker Book is the only "look at my things" surface
  and it shows achievements, not possessions. No photo/snapshot mode, no
  trophy shelf, no room the child can bring a visiting friend to.

---

## 8. Clothing and decorating — the shape they should now take

Both named items are the right instincts. Two notes on how the 2026-07-27
redesign changes their implementation, so they are not built to a stale spec:

**Clothing.** `CHARACTER_CUSTOMIZATION.md` assumed 3D bone sockets, materials
and morphs on the 26-bone rig. The redesign paused the 3D character migration
and made **sprite cutouts the target medium again**, so the cheaper and
better-looking path is now **layered 2D compositing** — base cutout + hair +
dress + crown + tail pattern, each its own transparent card, drawn in a fixed
order. This composes naturally in the promenade card
(`sky_lagoon_promenade.gd:_build_roshan_card`) and every existing consumer of
`skin_id` (kart driver `kart.gd:2062`, galaxy avatar `galaxy.gd:936`, ember
`ember_fortress.gd:801`) already reads a single identity value — they would read
a loadout instead. Save shape: add `"outfit"` (slot → piece id) and
`"outfit_owned"` with defaults; keep `"skin"` so old saves resolve to a preset
loadout.

**Decorating.** The prop tables in `castle_rooms_25d.gd` should split into
(a) fixed architecture and (b) **decor slots** — a handful of authored anchor
points per room, each accepting a category of item. Placement for a four-year-old
must be *tap the item, then tap a glowing slot* — never a free drag, which
demands precision she does not have. Save shape: `"room_decor"` (room id → slot
id → item id), added with a default of `{}`. Items are bought with pearls (§3)
and won from minigames, which finally gives the currency somewhere to go.

Both must inherit the existing rules: no fail state, every new objective carries
a `_say()` line and a pointer, no save key ever removed, new art within the
texture budget with an `ASSET_LICENSES.md` line in the same commit.

---

## 9. Balance observation

Counting shipped modes: kart racing, galaxy platformer, combat arena, dungeon,
Ember Fortress (6 rooms), toy-castle brawler, dust-bunny boss, fairy shooter,
stuffie battle — versus cozy content: four role-play rooms (8 verbs, of which 4
are "sleep" and 4 are "relax"), the craft studio, the companion care wing, the
shop. The action content is deeper and better-served by engines than the cozy
content is, and MEDALS.md adds a timed ranking layer on top of all of it.

The medal system is carefully no-fail and explicitly aimed at "the 6-8-year-old
she'll become", so this is not an argument to remove it. It is an argument that
the cozy half of the game currently has no equivalent depth — and that clothing,
decorating, tending and daily rhythm are precisely the systems that would give
it one.

---

## Recommended order

1. **Reconnect the world** (§1) — precondition; without it new cozy content is
   built into pockets the child cannot reach.
2. **Decor slots + clothing loadouts + pearl prices** (§2, §3, §8) — one loop,
   built together, because each is the other's payoff.
3. **Spoken content for existing messages** (§4) — the accessibility debt.
4. **Daily rhythm** (§5) — cheapest large win; needs a date in the save file.
5. **Tending beyond the stuffie, naming, gifting** (§6, §7) — reuses the care
   engine that already exists.
