# Stuffed-Friend Companions — design + implementation (2026-07-18)

Owner direction: a Pokemon-style system about which stuffed animals Mermaid
Roshan carries with her. Choose one friend (each with its own ability and
feel), it follows her through the world after she reaches Princess Huluu,
you paint its colours first, and it grows stronger with fish collectables.
Battles are NOT passive turn-based RPG: you CONTROL the creature in a 3D
arena — one attack button plus quick-time-event dodging with forgiving
timers. This is a primary new gameplay engine and a large wing of the game;
it is built to grow.

Everything passes the hard rules: no fail states, non-reader (voice +
pointer, symbols not text), one finger + one button, mobile renderer,
probe-deterministic analytic motion.

## The pieces

| Piece | File | Shape |
|---|---|---|
| Companion system | `scripts/companion.gd` | Phase-7 satellite (state on main) |
| Battle engine | `scripts/stuffie_battle.gd` | Family-B node (own camera/HUD, `finish_cb`), modeled on `combat_arena.gd` |
| Probe | `scripts/probe_stuffie.gd` | picker, follower, tokens, battle, QTE, save roundtrip |
| Save keys | `companion`, `companion_colors`, `fish_tokens`, `stuffie_wins` | added with defaults; deliberately NOT in `KNOWN_KEYS` (same pattern as `critters`) so pre-companion saves stay "complete" |

## The roster (data-driven — a third friend is one dictionary away)

`CompanionSystem.ROSTER`:
- **Sparkle the Baby Eagle** (`eagle`) — the book's baby-eagle art; rides the
  rigged **birdie** body (`craft_birdie_rigged.glb`). Attack: **PECK** (golden
  double-jab). Pro: speedy.
- **Kitty** (`kitty`) — rides the rigged **kitty** quadruped
  (`craft_kitty_rigged.glb`). Attack: **CLAW** (three pastel swipe streaks).
  Pro: big swipes.

Both bodies take the craft-studio 3-zone paint shader (body / accent /
third), so "you first choose its colors" reuses the proven pipeline, and the
picker preview tints the same `assets/mg` book-art layers the craft studio
uses. The owner mentioned the real stuffie may be a flamingo — if so, only
the ROSTER entry's name/colours change (or a new rigged body lands later).

## Unlock flow

Reaching Princess Huluu's throne in the Pearl Castle Grand Hall
(`huluu_greeted`) makes a **gift box** appear beside the Crown Star with the
golden pointer + a Huluu voice line. It is a walk-up-and-tap object, never an
auto-modal, so the crown path (and the audit bot) stay clear. Tapping it
opens the picker: friend cards on the left, live-tinted preview, three
palette rows (body 🎨 / trim ✨ / tummy 🤍), one giant "✔ LET'S GO!".
Choosing sparkles, saves, and the friend starts following in the reef.

## The follower (generalizes the peng_pal pattern)

Rubber-band follow at Roshan's flank (never magnets, warps back after big
teleports), seabed clearance, rigged gait FSM (idle/walk/run/happy via the
wrap's `"ap"` meta), cheer hearts when she rests, and a **helper beat**: every
~22s it dashes toward the nearest unfound friend with a sparkle trail and a
"This way!" voice line — the stuffie literally shows the way. Hidden during
minigames/arenas like the penguin.

## Battles — the sparring den

A pastel star-post ring near the shipwreck (built once the companion exists;
pointer + voice line). Swimming in starts `StuffieBattle`:

- **You control the creature** (stick/keys/pad/touch — the standard grammar).
- **One attack button**: the touch action bubble reads PECK / CLAW. Tap →
  analytic lunge at the nearest opponent; enough bops → the opponent gets
  dizzy (spins with stars) and is **befriended** (hops happily on the rim).
  Befriend everyone to win. Winning pays pearls and runs `_reward()`.
- **DODGE QTE**: one opponent at a time telegraphs (puffs + blinks + red
  sparkle) and a **giant pulsing DODGE bubble** appears (~2.2s window). Tap
  it (or X on a pad) → happy hop with sparkle trail. Miss → a harmless
  sparkle-bump and encouragement — no health, no damage, no fail state.
  Mercy: misses widen the window (+0.6s each, cap +1.8s), and after two
  straight misses ANY button counts as the dodge (mash-proof for age 4).
- **Ladder**: round1 (2 imps) → round2 (3 imps) → round3 (dragon-turtle
  friendly rematch), one round per visit, saved in `stuffie_wins`; after all
  three, visits rotate rounds forever (`_replays`).

## Upgrades — two tracks ("both")

- **Sparkle-fish tokens** (`fish_tokens`, incremental): 8 golden mini-fish
  slots scattered in the reef, respawning ~75s after capture. Roshan OR the
  stuffie swimming near one collects it (+1 level, sparkle, voice). Level →
  slightly faster attack cooldown and move speed (clamped).
- **Critter-Book fish** (milestone tiers): `tier()` = real fish catches from
  `collection_system.gd` (0–6). Tier 1: +0.5s dodge window. Tier 2: +30%
  attack reach. Tier 3: double-hit bops. Headroom for 4–6 reserved.

## Casual P2 (co-op)

- **In battle**: every connected pad already steers the creature — hand a
  gamepad to a grown-up and P1 watches or taps the bubbles. Zero setup.
- **In the overworld**: holding **R1 on a pad** makes its left stick steer
  the stuffie (leashed to 45u around Roshan) while `player.gd` mutes its own
  pad-move read (`companion_p2`), so Roshan stays on touch/keys. Release R1
  and the stuffie melts back into follow mode.

## Growth plan (why this is an engine, not a one-off)

- New companions = ROSTER dictionaries (+ optional rigged body).
- New opponents/rounds = `StuffieBattle.LADDER` entries; the QTE/befriend
  machinery is content-independent.
- Story battles later: `_start_stuffie_battle()` mirrors `_start_combat()`
  — any arena can hand control to the stuffie and get a `finish_cb` back
  (the MINIGAME_ENGINES.md contract).
- Companion "helps out at various times": the helper-beat hook in
  `companion.gd` is the seam for future assists (fetching pearls, opening
  shortcuts, minigame cameos).

## Probe coverage (`probe_stuffie.gd`, in ci.sh + probes.yml)

Fresh save exposes nothing → picker applies choice/colours → follower +
tokens + den appear → battle cannot be won passively → missed dodge bumps
without failing → pressed dodge counts → bops befriend and win the round →
ladder progress + pearls persist → all four save keys roundtrip through the
recovery reader.
