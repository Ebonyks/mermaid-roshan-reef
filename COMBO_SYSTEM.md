# Combo system — the four-verb encounter vocabulary (design workorder)

OWNER DECISION 2026-07-25: horizontal swipe is APPROVED as an input verb.
The player has demonstrated reliable Fruit-Ninja-style horizontal slicing,
so the "no gestures" line of the touch grammar (MINIGAME_ENGINES.md §4) is
amended for this one gesture: **mostly-horizontal swipe, either direction,
inside encounter focus only**. No other gestures (vertical, diagonal,
multi-touch, motion inputs) are added; everything else in §4 stands.

This doc is the design of the brawler combo system and the shared verb
vocabulary that boss fights (and later modes) are choreographed from.
Target client: the toy-castle brawler (`scripts/games/brawl.gd`, engine E2
brawl mode). Second client by migration: the stuffie battle's DODGE QTE.

---

## 1. Design stance

Combo depth for this player comes from three dials, in this order:

1. **Feedback escalation** — the game gets louder, sparklier, and more
   celebratory as a chain grows. This is where the fun lives.
2. **Verb variety** — four physical verbs (tap, mash, hold, slice), each
   with a fixed shape + color + sound identity learned once, recognized
   everywhere.
3. **Choreography** — bosses sequence the verbs in prompted chains. The
   *order and staging* varies per boss; the verbs never do.

Never dials: input precision (windows stay huge), memorization (every
step is prompted on screen), failure (a miss replays the prompt; mercy
escalates until success is inevitable).

Hard rules inherited unchanged: no fail states; every prompt fires a
`_say()` voice line + visual pointer (non-reader); mobile renderer; save
keys add-only; Phase-6 agency — no verb may auto-complete, so a
zero-input run can never clear an encounter (probe_passive must prove it).

## 2. The two input surfaces

The world grammar of MINIGAME_ENGINES.md §4 is untouched in free play:
**drag = point/steer, tap = THE button.** Verbs beyond tap live on a
second surface so they can never collide with movement:

- **Verb bubbles** — huge dedicated buttons in the `dodge_btn` mold
  (≥480×150 px at 720p, center-low). A bubble captures its touch, so
  TAP / MASH / HOLD on a bubble never fight the field's drag-to-move.
- **Encounter focus** — for SLICE (and boss chains generally) the game
  enters a short focus state: movement input is suspended, imps/boss
  freeze in a wobble pose, the camera pushes in slightly, and the whole
  screen belongs to the verb. This is why Fruit Ninja's swipe works at
  all — there is no movement verb competing for the finger. Focus states
  are short (one verb or one chain), then play resumes.

## 3. The four verbs

Each verb keeps ONE identity — color, shape, **motion**, sound family,
voice cue — across every mode, forever.

OWNER FEEDBACK 2026-07-25 — **prompt = demonstration, not symbol.** A
static glyph is a reading task in disguise; the prompt must PERFORM the
gesture it asks for, on a loop, until the player mirrors it. Every verb
bubble ships with a demo animation — a sparkle fingertip / comet acting
out the motion — and that looping motion IS the verb's identity. Emoji
glyphs stay only as secondary decoration inside the bubble. The demo
loops are Control tweens (scale/position/modulate), cheap under the
mobile renderer, and they run until first correct input, then yield to
the player's own feedback.

### TAP — hot pink, round bubble
Demo loop: a sparkle fingertip drops onto the bubble, dimples it with a
single squash-and-bounce, lifts off — one clear press, over and over.
One tap inside the window completes it.
- Window: 2.0–2.4 s telegraph (matches stuffie battle today).
- Mercy: window widens on a miss streak; after 2 misses, ANY input
  counts (the existing `stuffie_battle.gd` rule, kept verbatim).
- The stuffie battle's 🛡 DODGE is a themed TAP and migrates onto the
  shared helper unchanged.

### MASH — sunny gold, shaking bubble
Demo loop: the fingertip drums the bubble in rapid-fire — quick mini
squashes with puff bursts at tap tempo, the bubble jittering like it's
already being mashed. The animation shows the *rhythm* she should match.
Rapid multi-tap: every tap bumps a fill ring; burst at N taps.
- N = 6 base; ring NEVER drains — mashing is guaranteed forward
  progress, pure energy, zero timing skill.
- Mercy: after 8 s unfinished, N drops by 2 (floor 3).
- Feedback: bubble shakes harder per tap, pitch climbs per tap, burst is
  the biggest sparkle in the encounter. Voice cue: "Tap tap tap!"

### HOLD — lavender, calm bubble
Demo loop: the fingertip presses and STAYS — the bubble slowly inflates
while a ghost ring fills around it, then bursts; the sustained contact
is unmistakable next to MASH's drumming.
Press and hold; a ring fills over 1.2 s with a rising charge sparkle and
bursts automatically when full.
- Hold-until-full, NOT release-on-timing — release timing is a skill
  cliff; auto-burst is pure anticipation.
- Letting go early PAUSES the ring (never resets). Mercy: after two
  early releases, fill continues on its own at half speed while touched
  anywhere.
- This is the calm, dramatic verb — finishers, charging the pearl.

### SLICE — aqua, wide ribbon band (the new verb)
Demo loop: a comet streak sweeps horizontally across the band, leaving
a glittering trail, and the slice targets wobble as it passes — the
swipe literally performed in front of her, direction and extent shown,
no arrow glyph needed.
Fruit-Ninja moment: a horizontal ribbon band across mid-screen with 1–3
slice targets in a row; a sparkle trail follows the finger; dragging
across the band pops everything the trail crosses.
- Recognition (generous by design): one touch whose path crosses ≥40%
  of the band's width with net-horizontal motion (|Δx| ≥ 1.5·|Δy|),
  either direction. No speed floor beyond "not a stationary press":
  a slow deliberate drag across the band counts — at 4, intent is the
  skill, not velocity.
- Only ever spawned inside encounter focus (movement suspended), so a
  swipe can never be misread as steering — and in free play a swipe on
  the field simply keeps meaning "point where to be".
- Mercy: after 2 whiffed attempts the band widens and targets magnetize
  to the trail; after 4, tapping each target individually also counts.
- Feedback: trail + per-target pop-sparkle + a satisfying "shhhink"
  (pastel, not a blade — this is a ribbon of light, sea-themed).

## 4. Free-play layer: the pop-chain combo (brawler waves)

Always on during normal brawl waves; no new input to learn — it rides
the existing tap-to-pop (`brawl.gd:106`).

- Pops landed within a rolling **2.0 s** window chain: 1 → 2 → 3.
- HUD meter: star pips (⭐ fills), no numerals.
- Feedback ramp: `voice.pitch_scale` climbs with the chain
  (1.0 / 1.15 / 1.3 — replacing today's random pitch at `brawl.gd:115`),
  sparkle bursts grow, Huluu cheers at chain 3 (`_say("huluu", ...)`,
  reusing existing recorded lines — new voice recordings are
  owner-supplied only, never generated).
- **SUPER POP**: at chain 3 the meter glows; the next pop bursts every
  imp within radius 10 with a full-screen sparkle, then the chain
  resets bright and happy.
- Dropping a chain: pips just fade out. No sound, no downgrade sting —
  a lapsed chain must be emotionally invisible.
- Agency: only Roshan's taps chain. Huluu's stuns (human or AI) never
  count toward pops or chains — the Phase-6 rule is preserved exactly.

## 5. Boss fights: prompted verb chains

A boss encounter is a repeating loop: fight phase (free-play layer) →
boss staggers → **encounter focus** → a choreographed chain of 2–4
prompted verb steps → cinematic payoff → next fight phase. On the final
loop the last step is a HOLD or SLICE finisher.

- Steps appear ONE at a time — prompted, never memorized. Each step:
  its verb bubble/band playing its demo motion + golden pointer + voice
  cue. The demo keeps looping until her first correct input.
- A missed window never fails: the boss wiggles, the same step
  re-telegraphs, per-verb mercy escalates. The boss can NEVER escape a
  chain once staggered — slow is fine, stuck is impossible.
- Chains are data, not code:

```gdscript
# choreography dict — lives in the boss's config table
{"chain": [
	{"verb": "tap"},                       # bop the crown
	{"verb": "slice", "targets": 3},       # cut the balloon strings
	{"verb": "mash", "count": 6},          # topple him over
	{"verb": "hold", "time": 1.2, "finisher": true},
], "beat_sync": false}
```

- Variety across bosses = different verb orders, counts, staging
  (bubbles appearing where the boss part is), an interleaved TAP-dodge
  mid-chain, and optionally `beat_sync: true` pulsing prompts on the
  music beat (dance engine precedent, 0.46 s windows are proven).

## 6. Architecture: the shared VerbBubbles helper

`scripts/games/verb_bubbles.gd` — RefCounted satellite in the Phase-7
mold: receives `main` by reference, ALL state on `main.g` (`vb_*` keys),
UI nodes registered in `main.game_nodes` so `_clear_game` reclaims them.

```gdscript
var vb := VerbBubbles.new(main)
vb.begin({"verb": "mash", "count": 6})     # spawns the bubble/band + cue
var st := vb.tick(delta)   # → {"active", "verb", "progress", "done"}
vb.cancel()                # safe teardown (encounter interrupted)
# input feeds — the UI layer AND the probes call the same methods:
vb.feed_tap()              # TAP / MASH taps (bubble press)
vb.feed_hold(delta)        # HOLD while pressed
vb.feed_slice(from, to)    # a completed touch stroke in band-space
```

- One code path for real touches and probe input keeps the bots honest
  and deterministic; no verb completes without a `feed_*` call
  (probe_passive proof).
- Chain sequencing (`{"chain": [...]}`) is a thin loop above `begin()`
  owned by the boss code, not the helper.
- Migration (later, mechanical, probe-gated, one move per commit):
  stuffie battle DODGE → VerbBubbles TAP. Behavior identical.

## 7. Build order (each step probe-green before merge to dev)

1. **Pop-chain combo in brawl.gd** — meter, pitch ramp, SUPER POP.
   Smallest slice, immediately feelable, no new input surface.
   probe_audit extends: chain 3 then verify AoE pop; probe_passive:
   chains never grow without taps.
2. **VerbBubbles helper** — TAP + MASH + HOLD, with a probe driving all
   three via `feed_*`.
3. **SLICE** — recognition + ribbon band + encounter focus state in the
   E2 stage (movement suspension flag on `brawl_tick`).
4. **First boss** — imp king wave 4 in the brawler; one choreography
   dict; full chain loop; medals hook (MEDALS.md) for chain performance
   if desired (bronze floor stays guaranteed).
5. **DODGE migration** — stuffie battle onto VerbBubbles (mechanical).

New sounds (charge riser, shhhink, burst tiers): OGG, licensed lines in
ASSET_LICENSES.md same commit, or synthesized in-engine. No new textures
expected (bubbles are styled Controls like `dodge_btn`). No save keys
removed; any chain-stat keys added with defaults.
