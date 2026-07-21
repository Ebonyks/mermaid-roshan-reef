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
- **Baby Eagle** (`eagle`) — the book's baby-eagle art; rides the rigged
  **birdie** body (`craft_birdie_rigged.glb`). Attack: **PECK** (golden
  double-jab). Pro: speedy. (Voice fallback shares the existing baby-eagle
  "sparkle" pitch key.)
- **Mewsha** (`mewsha`) — rides the rigged **kitty** quadruped
  (`craft_kitty_rigged.glb`). Attack: **CLAW** (three pastel swipe streaks).
  Pro: big swipes. (Voice clips land as `mewsha_*.ogg`.)

Both bodies take the craft-studio 3-zone paint shader (body / accent /
third), so "you first choose its colors" reuses the proven pipeline, and the
picker preview tints the same `assets/mg` book-art layers the craft studio
uses. The owner mentioned the real stuffie may be a flamingo — if so, only
the ROSTER entry's name/colours change (or a new rigged body lands later).

## Unlock flow (owner 2026-07-19: meeting Huluu IS the trigger)

Reaching Princess Huluu's throne in the Pearl Castle Grand Hall
(`huluu_greeted`) plays her greeting, and ~3s later her offer — **"I want
you to have a new friend!"** — opens the picker right there: friend cards on
the left (Mewsha / Baby Eagle), live-tinted preview, three palette rows
(body 🎨 / trim ✨ / tummy 🤍), one giant "✔ LET'S GO!". Choosing sparkles,
saves, and the friend starts following in the reef. If the picker is closed
without choosing, a **gift box** appears beside the Crown Star (pointer +
voice hint) as the walk-up-and-tap re-entry, so the moment is never lost.

## The follower (generalizes the peng_pal pattern)

Rubber-band follow at Roshan's flank (never magnets, warps back after big
teleports), rigged gait FSM (idle/walk/run/happy via the wrap's `"ap"` meta —
the 3D bodies are the existing rigged craft models, birdie built from the
baby-eagle book art), cheer hearts when she rests, and a **helper beat**:
every ~22s it dashes toward the nearest unfound friend with a sparkle trail
and a "This way!" voice line. Owner 2026-07-19: it follows **all the time** —
every free-roam world (reef seabed clamp, lagoon terrain clamp, castle +
northern kingdom by Roshan's height band); it hides only inside self-driven
engines (kart, slides, battles, 2D canvas games) so it never photobombs a
mode's own camera. **Never lost** (owner 2026-07-20): a zone watch snaps the
stuffie to Roshan's side on every game-context change, and a freed/orphaned
node is detected and respawned beside her.

## The Stuffie Den (swap room, owner 2026-07-19)

A dedicated castle room at the west end of the Dreaming Floor corridor
(Wacky & Chuck's basket holds the east end): every stuffed friend from the
roster sits on a gold wall shelf under its name — the current companion
wears its painted coat and a floating 💗, the rest wear book-art defaults
and a sparkle ✦. Walk up and tap a shelf friend → the picker opens
preselected on it (repaint or confirm) — so the stuffie is swappable ANY
time, and a new roster entry automatically gains a shelf.

## THE CAPTURE LOOP (owner 2026-07-20 — integral to the game)

Most boss battles fought as a stuffie let you take the boss **home**:
befriend it in the arena (never hurt — dizzy stars and hearts) → it asks to
come home → it appears on its own shelf in the Stuffie Den → it becomes a
carryable companion for future missions. **Lamb-a'** is the first capturable
(the `boss_lamma` ladder round, using the existing `lamb.glb` plushie body).
Before capture her Den shelf shows a ❓ mystery, seeding anticipation.

Adding a future toy (the owner will photo-scan real stuffed animals via the
Meshy photo→3D pipeline, as the craft creatures were made):
1. Drop the scanned `.glb` in assets + a line in ASSET_LICENSES.md.
2. Add a ROSTER entry in `companion.gd` with `"model"`, `"emoji"`,
   `"locked": "friend_<id>"` (and `"paintable": false` — a real toy comes
   exactly as it is).
3. Add a LADDER round in `stuffie_battle.gd` with `"boss_model"` and
   `"award": "<id>"`.
Everything else — Den shelf, picker card, follower body, battle avatar,
save persistence (a `friend_<id>` key inside the existing `stuffie_wins`
dict — no schema change) — is automatic.

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
  friendly rematch) → **boss_lamma** (Lamb-a' capture — see THE CAPTURE
  LOOP), one round per visit, saved in `stuffie_wins`; after all rounds,
  visits rotate forever (`_replays`).

## Growth — Tamagotchi care (owner 2026-07-20; REPLACES the collectible model)

The stuffie grows because she TAKES CARE of it. Every so often (45–75s of
free-roam) it shows a want bubble: 🍎 hungry · 💤 sleepy · 🫧 bath ·
❤ cuddle · 🎾 play — with a voice line. Swim close, tap THE button, and a
short care moment plays (snack flies over and gets munched, Zzz drift up,
bubble scrub, hug hearts, zoomies) → **+1 care point**, heart, chime.

GENTLE by design — the anti-Tamagotchi rules: one want at a time, wants
wait forever, nothing decays, nothing gets sick, care is never lost, and a
want can never fulfil itself (probe-enforced). Care is shared across
friends: it is HER nurturing that grows, whichever stuffie she carries.

- `care_points` (persisted; legacy `fish_tokens` migrated in on load, the
  old key still written for save compat)
- `stage()` = 1 + points/4, shown as ⭐ pips (never numerals) at each
  level-up celebration (fanfare + rainbow sparkle ring)
- battle perks ride the stages: speed/cooldown scale with points; tier 1:
  +0.5s dodge window; tier 2: +30% attack reach; tier 3: double-hit bops;
  headroom for 4–6 reserved.

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
