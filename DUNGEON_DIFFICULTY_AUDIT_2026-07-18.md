# Dungeon Difficulty Audit & Zelda-Grammar Design — 2026-07-18

Scope: the ten-room dungeon (`scripts/dungeon_level.gd` sequencing
`scripts/combat_arena.gd` battles and `scripts/dungeon_puzzle_room.gd`
puzzles), entered through the castle `dungeon_gate` and checkpointed via
`dungeon_progress` in `reef_save.json`.

Three questions, answered in order:

1. Is each room actually playable by *this* player — a 4-year-old
   non-reader with one finger?
2. Is 10 the right number of rooms?
3. What should the linear, lock-and-key ("Legend of Zelda grammar")
   design look like, room by room?

This is a design document. No code changes ship with it; the
"Implementation notes" section at the end maps every recommendation onto
files, probe assertions, and hard rules so the changes can land as small
gated commits later.

---

## 1. What exists today

| # | Room | Engine | Mechanic | Params (dungeon_level.gd:7–16) |
|---|------|--------|----------|--------------------------------|
| 1 | Frozen Foyer | combat/ice | freeze all imps | 4 imps, ring, speed 1.1, attack gap 3.8 |
| 2 | Crystal Chimes | puzzle/sequence | copy 3-symbol order | solution [0,2,1], 3 pads |
| 3 | Frozen River | puzzle/path | copy 4-step left/right path | solution [0,1,1,0], 2 pads |
| 4 | Popcorn Ambush | combat/ice | freeze all imps | 6 imps, spiral, speed 1.45 |
| 5 | Pepper Lanterns | puzzle/torches | light 4 lanterns shortest→tallest | solution [1,3,0,2] |
| 6 | Turtle Gallery | puzzle/rotate | face 3 statues toward pearl | targets [1,0,3] |
| 7 | Claw Guardian | combat/fire | hit boss during peek window | hp 4, peek 4.8s |
| 8 | Moon Rune Vault | puzzle/pairs | match 2 pairs of 4 cards | ☾★☾★ |
| 9 | Elemental Door | puzzle/elemental | copy 5-step ice/fire order | solution [0,1,0,0,1] |
| 10 | Dragon-Turtle Throne | combat/dual | freeze shell, then fire at peek, ×4 | hp 4, shell 5.0s, peek 3.2s |

Systems already in place (verified in code, exercised by
`scripts/probe_dungeon.gd`):

- **No fail state anywhere.** Enemy contact and enemy shots only bump
  the player with a sparkle ("bubble shield", combat_arena.gd:463–472).
  Wrong puzzle taps produce a gentle voice hint and nothing else
  (dungeon_puzzle_room.gd:395). Wrong-element boss hits sparkle
  harmlessly. There is no timer, no health, no loss.
- **One-finger play.** Virtual stick + one context-relabeled action
  button (ICE / FIRE / USE via `action_label()`); combat auto-aims at
  the nearest target (combat_arena.gd:260), so aim skill is never
  required.
- **Checkpoint after every room.** `dungeon_progress` is written to disk
  on every room clear (+3 pearls each); the Home button is always
  visible and leaving mid-room keeps every earned checkpoint. Next visit
  resumes at the first uncleared room.
- **Voice + pointer on every objective.** Each room fires a `show_msg`
  voice line and every scene keeps a bouncing golden ▼ over the current
  clue or target.

This is a strong foundation. The audit below is therefore about
*cognitive* fit and pacing, not safety.

---

## 2. Room-by-room difficulty audit (age-4 lens)

Grading key — **PASS**: comfortably inside age-4 ability.
**MARGINAL**: solvable through the safe trial-and-error net, but the
concept or feedback needs a fix to be *understood* rather than
brute-forced. **OUT OF BAND**: the concept itself is developmentally
ahead of age 4.

| # | Room | Grade | Est. time (age 4) |
|---|------|-------|-------------------|
| 1 | Frozen Foyer | PASS | 1–1.5 min |
| 2 | Crystal Chimes | PASS | 1–2 min |
| 3 | Frozen River | MARGINAL | 1.5–2.5 min |
| 4 | Popcorn Ambush | PASS | 1.5–2 min |
| 5 | Pepper Lanterns | OUT OF BAND | 2–4 min |
| 6 | Turtle Gallery | MARGINAL | 2–3 min |
| 7 | Claw Guardian | PASS | 1.5–2.5 min |
| 8 | Moon Rune Vault | PASS (mis-slotted) | 1–1.5 min |
| 9 | Elemental Door | MARGINAL | 1.5–2.5 min |
| 10 | Dragon-Turtle Throne | PASS (finale-hard) | 2–3.5 min |

**Room 1 — Frozen Foyer (PASS).** Four slow imps, one button, auto-aim,
frozen imps pop into popcorn. A pure joy-and-onboarding room; correct as
the opener.

**Room 2 — Crystal Chimes (PASS).** Copying a *visible* 3-symbol order
is matching, not recall — squarely age-appropriate. The clue row stays
on screen the whole time, which is exactly right for a non-reader.

**Room 3 — Frozen River (MARGINAL).** The mechanic is fine: two big
arrow pads (real Left/Right pictogram models, not words), two choices
per step, wrong taps cost nothing. Two frictions: (a) the preview stones
that show the path are spawned at `scale 0.12`
(dungeon_puzzle_room.gd:172) — genuinely tiny from the fixed camera, so
the "clue" is hard to physically see; (b) after each correct step the
avatar teleports back to the start line (line 346), which reads as "did
I do something wrong?". Fix: enlarge the preview stones ~2×, light up
the *next* stone in gold, and swim-animate the reset instead of
snapping.

**Room 4 — Popcorn Ambush (PASS).** Same verbs as room 1, more imps,
spiral spawn, slightly faster. A correct "test what you learned" beat.

**Room 5 — Pepper Lanterns (OUT OF BAND).** Ordering four objects by
height is *seriation*, which typically consolidates at ages 5–7 — a
4-year-old can find "the littlest one" when asked, but "light them
shortest to tallest" as a standing instruction will not be understood;
the safe trial-and-error net turns the room into random tapping (up to
4 tries per step × 4 steps) rather than a solved puzzle. Two additional
problems: the lantern heights (3.0 / 4.2 / 5.5 / 7.0) put the two middle
sizes within ~30% of each other, and the room is fire-themed *before*
fire has been introduced (Claw Guardian is two rooms later). Fix — keep
the room, change the ask: the golden pointer moves to the correct next
lantern each step, converting seriation into a guided one-at-a-time
"find the littlest / now the next littlest" comparison (which IS age-4
appropriate), and move the room after the fire miniboss so the pepper
flame is a power the child just earned. Widen the two middle heights.

**Room 6 — Turtle Gallery (MARGINAL).** "Turn the golden noses to the
pearl" requires reasoning about facing/orientation from a fixed
three-quarter camera — hard at 4, but rescued by the tap-to-rotate-90°
loop (max 3 taps per statue). The real defect is feedback: the chime
pitch encodes the rotation *value*, not correctness
(dungeon_puzzle_room.gd:358), and nothing marks a statue as "done", so
the child cannot tell which of the three statues still needs turning.
Fix: when a statue reaches its target, flash it gold, play the win
chime, and leave a glow on it; the door already opening on the third
lock-in then reads as cause-and-effect.

**Room 7 — Claw Guardian (PASS).** A 4.8-second peek window with a
one-tap answer, wrong-time shots sparkle harmlessly, and claw swipes are
bubble-bumps. The pepper basket is already spawned as the "ability
source" prop (combat_arena.gd:194) — the design below promotes it into a
proper Zelda item moment.

**Room 8 — Moon Rune Vault (PASS, mis-slotted).** A 4-card, 2-pair
memory match with a 1.1-second mismatch-study window is the *easiest*
puzzle in the dungeon — matching pairs is mastered around age 3. Sitting
at slot 8 it inverts the difficulty ramp. Move it early (slot 3 in the
new design) as the confidence puzzle.

**Room 9 — Elemental Door (MARGINAL).** Five steps exceeds age-4
working memory in the abstract, but the clue row stays visible, so it is
"copy while looking", which is fine. The gap is *place-keeping*: the
only indication of which step you're on is the "2 / 5" numeral counter —
meaningless to a non-reader. Fix: bounce the golden pointer over the
current symbol in the clue row (the pointer already exists; it just
never moves along the sequence).

**Room 10 — Dragon-Turtle Throne (PASS as finale).** Rule-switching
(ice → fire → ice) is genuinely the hardest cognitive ask in the
dungeon, but every support is present: the action button relabels
ICE/FIRE per phase, wrong elements sparkle harmlessly, the "shell keeps
spinning" voice hint repeats every 1.5s until the right element is used,
and there is no fail. Eight correct taps total. Correct as the crown.

**Cross-cutting finding — numerals.** "ROOM 3 / 10", "2 / 5", and the
counter chips are the only reading-dependent UI in the dungeon. They're
harmless (adults use them) but every place a numeral is the *only*
carrier of state needs a pictorial twin — the progress-star strip
already does this for room count; the sequence puzzles need the moving
pointer (room 9 fix) to do the same for step count.

---

## 3. Is 10 the right number of rooms?

**Yes — keep 10.** But the unit that matters for a 4-year-old is the
*sitting*, not the dungeon, and the design must make sittings first-class.

The arithmetic: a full clear is ~15–25 minutes of age-4 play. That is
2–3× a comfortable sitting for structured play at this age (~8–12
minutes). If the dungeon demanded one sitting, 10 rooms would be wrong —
5 or 6 would be the ceiling. But it doesn't: there is a disk checkpoint
after *every* room, Home is always on screen, and resume is
probe-verified. Ten rooms is therefore not "one long level", it is a
**multi-day campaign of 3–4 room sittings** — which is exactly the
right shape for this player, and honestly more Zelda than a single
sitting would be (nobody clears a Zelda dungeon without putting the
controller down).

Why not cut to 6–8 anyway:

- Every room is a distinct mechanic or a deliberate re-test; there is no
  filler to cut. The problems found in §2 are ordering and feedback
  problems, not excess-content problems.
- `dungeon_progress` (0..10), the ten-star progress strip, the
  "Ten-room dungeon complete!" voice lines, the +50 completion bonus,
  and `probe_dungeon.gd`'s `ROOMS.size() == 10` / 4-combat-6-puzzle
  assertions all encode 10. Save-compat rules say never remove keys;
  shrinking the count would strand `dungeon_progress` values of 9–10 and
  re-record family voice lines for no player benefit.
- Ten stars on the strip is countable on fingers — the strip is itself a
  numeracy toy.

What 10 rooms *does* require (and the current build lacks): *designed
stopping points*. Right now every room boundary is identical, so the
natural end of a sitting is "whenever the child wanders off". The
design below groups the ten rooms into three wings with a celebration
landing after rooms 5 and 9 — fanfare, sparkle burst, a "what a hero!
Next time: the Fire Wing!" voice line. Landings make "we'll come back"
a triumphant beat instead of an interruption, and give the returning
player a narrative re-entry point.

---

## 4. The design: a linear lock-and-key dungeon (Zelda grammar)

The current dungeon is already secretly half a Zelda dungeon: linear
rooms, doors locked behind objectives, an ability (fire) that appears
mid-dungeon, and a two-ability finale. The design below makes the
grammar explicit — every door has a named lock, every lock has a key the
child visibly earned — and re-orders the existing ten rooms so the
difficulty ramp is monotonic with rest beats. **No room is added or
removed; this is a re-sequencing plus the feedback fixes from §2.**

### Grammar mapping

| Zelda concept | Reef of Light equivalent |
|---|---|
| Dungeon item #1 | **Ice Berry** — presented in room 1 (chest-style fanfare on the first freeze) |
| Small-key doors | Picture locks — each puzzle door opens when its picture goal is copied |
| Combat seals | "Frozen door" rooms — door thaws when every imp is popped |
| Miniboss guarding item #2 | **Claw Guardian** — the pepper basket beside the arena is the item chest; tapping USE on it grants **Pepper Flame** with a fanfare *before* the fight activates |
| Boss Key | **Elemental Door** — solving the 5-glyph ice/fire lock forges the golden Boss Key on screen; the throne door visibly takes it |
| Boss door | Dragon-Turtle Throne — requires both elements, i.e. both items |
| Dungeon map/compass | The ten-star progress strip + per-room golden ▼ pointer (already shipped) |

### Wing structure (sitting design)

- **Ice Wing** — rooms 1–5. Teach ICE, teach picture locks, exam.
  *Landing celebration after room 5.*
- **Fire Wing** — rooms 6–9. Earn FIRE from the miniboss, apply it,
  forge the Boss Key. *Landing celebration after room 9.*
- **Throne** — room 10. Spend both items. Full completion party.

Each wing is a 4–9 minute sitting. A sitting can also end anywhere
inside a wing (checkpoints are unchanged); landings are the *encouraged*
stops, not walls.

### Room-by-room design

Format — **Goal** is the spoken, non-reader objective (voice line +
pointer). **Lock** is the door condition. **Key** is what the child uses
or earns. Every room keeps: no fail state, Home always available,
checkpoint + 3 pearls on clear.

**ICE WING**

**Room 1 — Frozen Foyer** *(combat/ice, today's room 1)*
- Goal: "Take the Ice Berry! Freeze every mischief imp!"
- Lock: combat seal — all 4 imps frozen and popped.
- Key: **ITEM MOMENT — Ice Berry.** First room, first power. On the
  child's first successful freeze, pause the swarm ~1.5s for a fanfare +
  sparkle: "You got the ICE BERRY!" (Zelda item jingle beat, using the
  existing `_fanfare()`.)
- Tuning: unchanged (4 imps, ring, speed 1.1). Grade: PASS.

**Room 2 — Crystal Chimes** *(puzzle/sequence, today's room 2)*
- Goal: "Look at the three big crystal pictures — swim to the pads in
  the same order!"
- Lock: picture lock — 3-symbol order copied.
- Key: looking + matching. Teaches the dungeon's core sentence: *big
  picture shows it, pads do it, door opens*.
- Tuning: unchanged, plus the moving step-pointer from §2/room 9 (one
  mechanism shared by all sequence puzzles). Grade: PASS.

**Room 3 — Moon Rune Vault** *(puzzle/pairs, today's room 8 — moved up)*
- Goal: "Peek under two moon tiles — find the pictures that match!"
- Lock: picture lock — both pairs matched.
- Key: matching, the easiest ask in the dungeon; sits here as the
  confidence room so the ramp never inverts.
- Tuning: unchanged (4 cards, 1.1s mismatch-study window). Grade: PASS.

**Room 4 — Frozen River** *(puzzle/path, today's room 3)*
- Goal: "The ice stones show the path — freeze each step, left or
  right!"
- Lock: picture lock — 4-step path copied on the arrow pads.
- Key: the Ice Berry, thematically (each correct pad "freezes" a
  stepping stone into place) — first *apply-your-item* room.
- Tuning (the §2 fixes): preview stones at ~0.25 scale, next stone lit
  gold, avatar swims back to the start line instead of teleporting.
  Grade after fixes: PASS.

**Room 5 — Popcorn Ambush** *(combat/ice, today's room 4)*
- Goal: "Imps everywhere! Freeze them all — popcorn party!"
- Lock: combat seal — all 6 imps popped.
- Key: Ice Berry mastery; the Ice Wing exam.
- Tuning: unchanged (6 imps, spiral, speed 1.45).
- **LANDING: Ice Wing complete.** Fanfare + sparkle rain + voice:
  "The Ice Wing is safe! Next time — the Fire Wing!" Natural sitting
  end. Grade: PASS.

**FIRE WING**

**Room 6 — Claw Guardian** *(combat/fire miniboss, today's room 7)*
- Goal: "The pepper basket! Grab a spicy pepper — then tap FIRE when
  the turtle-lizard peeks!"
- Lock: miniboss seal — 4 peek-window hits.
- Key: **ITEM MOMENT — Pepper Flame.** The already-present basket
  becomes an interactive: swim to it, tap USE, fanfare — "You got the
  PEPPER FLAME!" — then the guardian wakes. Item is earned *at* the
  miniboss, per Zelda grammar.
- Tuning: unchanged (hp 4, peek 4.8s). Grade: PASS.

**Room 7 — Pepper Lanterns** *(puzzle/torches, today's room 5 — moved
after the fire item)*
- Goal (reworded): "Light the littlest lantern with your pepper flame…
  now the next littlest!" — one comparison at a time, spoken per step.
- Lock: picture lock — all 4 lanterns lit in size order.
- Key: Pepper Flame, freshly earned; guided comparison instead of
  standing seriation.
- Tuning (the §2 fixes): golden pointer sits on the correct next
  lantern each step; heights spread to ~2.5 / 4.2 / 5.6 / 7.2 so every
  adjacent pair is visibly different. Grade after fixes: PASS.

**Room 8 — Turtle Gallery** *(puzzle/rotate, today's room 6)*
- Goal: "Turn every shell statue's golden nose to the pearl!"
- Lock: picture lock — all 3 statues facing the pearl.
- Key: spatial play; hardest puzzle, correctly placed one room before
  the key ritual.
- Tuning (the §2 fixes): a statue that reaches its target flashes gold,
  plays the win chime, and keeps a glow — "done" is visible per statue.
  Grade after fixes: PASS (from MARGINAL).

**Room 9 — Elemental Door** *(puzzle/elemental, today's room 9)*
- Goal: "The great door shows ice and fire — copy its magic order!"
- Lock: **the Boss Key.** On solve, the door doesn't just open — it
  forges a big golden key (existing key-shaped fanfare moment: sparkle
  burst + the door prop's crystal recolored gold) that Roshan carries
  out. The throne room's door starts locked with a matching golden
  keyhole and visibly opens with it.
- Key: both items, interleaved — the finale's rehearsal, five taps.
- Tuning: unchanged solution [ice, fire, ice, ice, fire]; add the
  moving step-pointer over the clue row.
- **LANDING: Fire Wing complete + Boss Key held.** "You found the
  golden Boss Key! Next time — the Dragon-Turtle Throne!" Second
  natural sitting end. Grade after fixes: PASS.

**THRONE**

**Room 10 — Dragon-Turtle Throne** *(combat/dual, today's room 10)*
- Goal: "Freeze the spinning shell with ICE… now FIRE while it peeks!"
- Lock: boss seal — 4 freeze→flame cycles.
- Key: both items + the rule-switching skill rehearsed in room 9. The
  Boss Key opens the door on entry (pure ceremony, no input needed —
  the child watches their key work).
- Tuning: unchanged (hp 4, shell 5.0s, peek 3.2s, endless gentle
  re-hints on the wrong element).
- Completion: existing ten-star celebration, +50 pearls, "All ten
  rooms! The dungeon is sparkling and safe!" Grade: PASS.

### Resulting difficulty curve

```
combat-intro → easy puzzle → easiest puzzle → item-apply puzzle → combat exam
   (item 1)                                                      ★ landing
→ miniboss (item 2) → item-apply puzzle → hardest puzzle → key ritual
                                                          ★ landing
→ two-item finale
```

Monotonic within each wing, a rest beat at each wing start, and every
skill the finale needs (ICE, FIRE, switching between them) is earned and
rehearsed before it is tested.

---

## 5. Implementation notes (for whoever lands this)

Ordered smallest-risk first; each bullet is one gated commit.

1. **Reorder `ROOMS`** (dungeon_level.gd) to
   `[1, 2, 8, 3, 4, 7, 5, 6, 9, 10]` of today's indices. Engines and
   configs move untouched. `probe_dungeon.gd` hard-codes per-index
   expectations (room 2 = sequence with 3 interactives, index 9 =
   finale, pairs exercised where encountered) — update the probe in the
   same commit; the behavior change is the explicit goal, which the
   refactor rules allow. Mid-run saves keep their `dungeon_progress`
   count and simply resume in the re-ordered sequence — safe because
   every room is self-contained and fail-free (worst case: one room
   type replays). No save keys change.
2. **Step-pointer for sequence puzzles** (dungeon_puzzle_room.gd): in
   `_update_visuals()`, move `pointer.position` to the pictogram of the
   current `step` for `sequence`/`elemental`/`path`/`torches` instead of
   the static `clue_pos`. Replaces the numeral "2 / 5" as the primary
   place-keeper; keep the numerals for adults.
3. **Frozen River readability**: preview stone scale 0.12 → ~0.25,
   emissive gold on the next stone, tween the avatar reset.
4. **Turtle Gallery lock-in feedback**: in `_rotate_action()`, on a
   statue reaching its target, apply a gold emissive material + win
   chime; already-correct statues keep the glow.
5. **Pepper Lanterns guided mode**: pointer follows the correct next
   lantern; per-step voice lines ("littlest… next littlest…"); spread
   the middle heights. Requires two short new voice recordings (owner:
   family voices are irreplaceable — record, don't synthesize).
6. **Item moments + landings** (dungeon_level.gd + combat_arena.gd):
   Ice Berry fanfare on first freeze in room 1; basket USE-to-collect
   before the Claw Guardian activates; wing-landing fanfare + voice
   after rooms 5 and 9; Boss-Key forge visual in room 9 and keyhole
   ceremony in room 10. All reuse `_fanfare()`, `_sparkle_burst()`,
   `show_msg` — no new audio systems. New voice lines needed: item
   jingles ×2, landings ×2, boss-key ×2.

Hard-rule compliance: every new objective above speaks via the existing
voice path and is carried by the golden pointer (rule: voice + visual
pointer); no new OmniLights; no new textures; no save keys removed
(`dungeon_progress` semantics unchanged); all changes stay inside the
Mobile renderer budget (pointer moves and material swaps only). Full
probe suite (`scripts/ci.sh`) gates every commit, with
`probe_dungeon.gd` updated alongside step 1.
