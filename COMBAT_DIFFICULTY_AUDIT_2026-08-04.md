# Combat difficulty audit — 2026-08-04

Owner brief: *"the current difficulty of combat in this game in its current
form. It feels too easy. I think the slash attack is too powerful, and there
should be visual indication that it only works for a narrow band, requiring a
more active style of combat. ... insure that the charge attack has a visual
indicator that demonstrates that it's working. Evaluate what balance would be
appropriate for a 4 year old in the context of the current game."*

Scope: timing, pacing and fun-factor of the shared combat system. Boss-specific
resistances and patterns stay out of this wing by owner decision.

---

## 0. The finding that reframes everything

**The combat wing was never in a build.** Every piece of it — the pop-chain
combo, the damage grammar, the charge attack, the partner system, the feel
stack, the throne sparring class — was implemented on `codex/tap-combat-feel`,
never PR'd, never merged, and left 198 dev commits behind. `HIT_ENGINE.md` on
dev cited `COMBO_SYSTEM.md` as if it existed; it did not, on dev.

So "the current form" the brief describes is the *design*, not the shipped
game. As of this audit the wing is merged onto current dev
(`claude/combat-wing-20260804`, probes green locally) and the numbers below are
what that merge actually contained before the pass.

**The slash did not exist at all.** `VERB_DAMAGE` carried a `"slice": 2` row
and a doc comment; no input path produced it, no code consumed it. There was
nothing to weaken — which is fortunate, because it means the verb could be
built bounded from the first line instead of nerfed after the fact.

---

## 1. Why it felt too easy — the mechanism

Not "the numbers are small". Three specific structural faults, in order of how
much each one flattens the fight.

### F1 — Waiting was the strongest move (severity: high)

The old charge ladder was 2/3/5 damage at 0.50/1.00/1.45 s, on top of a
press-fire tap that already dealt 1.

| Play | Actions | Time | Damage | Result on a 3-hp imp |
|---|---|---|---|---|
| Tap ×3 | 3 | ~1.20 s | 3 | dead |
| Press + hold to stage 2 | 1 | 1.00 s | 3 | dead |
| Press + hold to stage 3 | 1 | 1.45 s | 5 | dead, 2 wasted |

Holding was **faster and cost a third of the effort**. Stage 3 also fires
itself, so the optimal input was: put one finger down, wait, watch things die.
A game whose best strategy is to stop playing will always feel too easy, no
matter how much HP you add — adding HP just makes the parking longer.

This is the single largest contributor and the one the pass attacks hardest.

### F2 — The fight aimed itself (severity: high)

The brawler's bop reach was `BOP_R 6.0 + 4.0 × mercy` → up to **10.0 world
units**, against a segment 34 wide and 14 deep, with `_nearest_imp()` picking
the target regardless of where the finger landed. Effectively: press anywhere,
the nearest imp dies. There was no spatial play left — no closing distance, no
choosing a target, no reason to move. The recover-pose bonus multiplied it a
further ×1.4 (up to 14.0).

### F3 — The combo was a metronome, and its reward was a screen-wipe (severity: medium)

`CHAIN_T` is a 2.0 s window that refills on every landed hit. With reach that
generous, essentially every tap lands, so the chain sat pinned at 3 and **every
fourth tap was a SUPER**. The SUPER then splashed 1 damage inside
`SUPER_R = 10.0` — again, most of a segment. A guaranteed rhythmic wave-clear
is not a reward; it is the floor.

### F4 — Effort was invisible (severity: medium, and it cuts both ways)

A basic imp has 3 hp. Hits 1 and 2 produced a wobble, a sparkle and a bonk —
and *no persistent evidence anything had changed*. To a four-year-old that
reads as "my tapping does nothing," which is the same complaint as "too easy"
seen from the other side: the fight has no visible shape, so it is either
instant or it is noise. There was no readout of an enemy's remaining health
anywhere in the game.

### F5 — The charge's own indicator waited too long and read wrong (severity: medium)

`CHARGE_GRACE` was 0.30 s: for the first third of a second of holding, the
screen showed nothing at all. A four-year-old lifts. And what finally appeared
was a flat `TorusMesh` at the target's feet (`y + 0.15`) — in a 2.5D promenade
that reads as a puddle, not a power meter. Stage progress was signalled only by
a colour snap and a chime; there was no countable "2 of 3".

### F6 — The slash, unbuilt, was designed to be a screen-clear

The recovered `COMBO_SYSTEM.md` described SLICE as a horizontal Fruit-Ninja
swipe. The obvious implementation — cut everything the finger crosses, 2 damage
each — removes a whole wave in one gesture. The owner's instinct here was
correct in advance of the code.

---

## 2. What "appropriate for a 4-year-old" means here

The hard rule is unchanged: **no fail states**. So difficulty cannot come from
risk, punishment, or loss. It has to come from three other places:

1. **Duration.** An encounter should occupy 20–45 s of engaged attention, not
   5 s. Length comes from enemy *count* and from hits-per-enemy that are
   *visible*, never from enemies that feel unkillable.
2. **Effort-to-reward proportionality.** The child must be able to tell that
   doing more got her more. If the laziest input is the strongest, the fight is
   over before it starts — regardless of the numbers.
3. **Spatial and rhythmic participation.** Moving toward a target, aiming a
   swipe, holding a beat and letting go. These are the "more active style" the
   brief asks for, and all three are age-appropriate: a 4-year-old sustains
   roughly 2–3 taps/second, tracks a 2 s rhythm window comfortably, and can
   hold-and-release on a ~0.6 s window.

Corollary that guided every number below: **the fun verb must be the strong
verb.** Tapping is the fun one. Everything else prices itself against it.

---

## 3. The pass — before and after

| Knob | Was | Now | Why |
|---|---|---|---|
| Charge ladder | 2/3/5 @ 0.50/1.00/1.45 s | 2/3/4 @ 0.50/1.10/1.75 s | Full hold = 2.3 dmg/s, below tapping's ~2.5. Waiting is no longer optimal. |
| `CHARGE_GRACE` | 0.30 s | 0.12 s | The hold shows it is working almost immediately. |
| Charge readout | ring only, on the floor | ring **+ three stage lamps above the target**, next one visibly swelling | Countable, at head height, alive every frame of the hold. |
| Enemy health | invisible | **hit-point lamps that snuff out**, on any enemy with >1 hp | Effort becomes visible. No numerals, no reading. |
| Brawler reach | 6.0 → 10.0 (mercy) | 4.5 → 7.5 (mercy) | She has to close the distance. Mercy still rescues. |
| `SUPER_R` (engine + brawler) | 10.0 | 6.5 | A SUPER is a local reward, not a wave-clear. |
| SLICE | undefined | built, bounded — see below | The verb exists, and cannot clear a screen. |

### The slice, and the four limits she can see

| Limit | Value | What she sees |
|---|---|---|
| Narrow band | 54 px either side of the swipe line | the ribbon is drawn at exactly that width — what you see is what you cut |
| Fixed blade length | 420 px | the ribbon **stops** at the blade's end; dragging further gains nothing |
| Target cap | 2 enemies, nearest-first along the blade | a packed crowd cannot be one-shotted |
| Cooldown | 0.9 s | a spent blade draws grey and fizzles — a soft sound, never a buzzer |

Damage stays at 2. It is the reward for an aimed, committed gesture, and two
slices still do not fell a 4-hp advanced enemy on their own.

A finger that starts travelling cancels any charge it began — one finger, one
verb — so the swipe and the hold can never both resolve from one gesture.

### The resulting shape of the charge

Deliberately *not* "the charge is worse now". The curve is:

- release early (stage 1, ~0.5 s): brisk, efficient, an active rhythm
- release mid (stage 2, ~1.1 s): a solid single hit
- hold to full (stage 3, 1.75 s): the **biggest single hit, the worst rate**

Efficiency falls as you wait; magnitude rises. That is the correct shape: the
charge earns its place against high-hp targets and as a satisfaction beat,
without ever being the answer to "what should I do every time".
`probe_hit` asserts the top-of-ladder inequality directly, so it cannot
silently regress.

---

## 4. Deliberately not changed

- **Basic imp 3 hp.** The 1-2-3 tap combo *is* the identity of the system —
  one full combo fells one basic imp. Canon; keep.
- **Dust bunny 1 hp.** They are the day-one teaching fodder. The pop is the
  lesson.
- **`CHAIN_T` 2.0 s.** Correct for the age. The chain at four years old is a
  rhythm reward, not a difficulty gate.
- **Wave counts `[3, 4, 5]`.** Raising counts is the cheapest difficulty lever
  and the most tempting, but the faults above were structural. Fix the shape
  first, then measure on the phone. Flagged in §6.
- **Boss HP 7.** **This reverses the earlier recommendation** in
  `COMBAT_SYSTEM_AUDIT` (2026-08-01) to drop the pepper boss to 4. That
  recommendation was made under the assumption that combat was too long; the
  owner now reports the opposite. The boss is the one place where length is
  the point. Left at 7.
- **Mercy ramps.** Every one of them stays. Difficulty here means *engagement*,
  never a child stuck and upset.

---

## 5. Verification

Local, Godot 4.7.1-stable on PATH, per-probe `APPDATA`/`XDG` isolation:

`probe_hit` (extended with slice + charge-lamp coverage), `probe_combat`,
`probe_combat_tutorial`, `probe_partner`, `probe_passive`,
`probe_touch_router`, `probe_touch_stress`, `probe_touch_adversary`,
`probe_interaction`, `probe_imp_ai`, `probe_castle_pearl_art`, `probe_throne`,
`probe_dust_boss`, `probe_audit` — all green.

`probe_passive` matters most of the three: it is the zero-input negative test.
The slice is reported only from a travelled touch and the charge only from a
press, so neither verb can fire without a finger.

---

## 6. Open — needs the phone, not the repo

These are judgement calls that a headless probe cannot settle. Recommend one
play session and then a single tuning commit.

1. **Wave counts.** If encounters still end too quickly with the new reach and
   the un-dominated charge, raise `WAVES` `[3,4,5]` → `[4,5,6]`. Do this
   *after* feeling the reach change, not with it — one variable at a time.
2. **Slash band width on the real screen.** 54 px is tuned against the
   1280×720 base canvas. On the M11 it wants a look; if she misses often,
   widen the band before shortening the cooldown.
3. **Charge lamp placement** at `aim_h + 1.35` may collide with the hp lamp row
   at `aim_h + 1.05` on short enemies (dust bunnies are 1 hp, so no row — but
   check the imps).
4. **Whether the slice is discoverable at all.** It has no tutorial lesson yet.
   The throne sparring class teaches TAP → COMBO → CHARGE and graduates. A
   fourth SLICE lesson wants the ghost-finger demo and the `verb_chip_slice`
   art requested in the Codex handoff (`CODEX_COMBAT_ART_HANDOFF_2026-08-04.md`).
   Until that lands, the slice is an undiscovered bonus, not a taught verb.
5. **Haptics default.** `Juice.haptics_enabled` is hardcoded `true` with no
   parent toggle. Still open from the 2026-08-01 audit.
