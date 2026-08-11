# Pearl Opera minigame quality audit and implementation record

Date: 2026-08-09
Audience: one non-reading four-year-old, one finger, short sessions, no fail states
Shipping path audited: `OperaCareerWorld2D.PHASES` (13 careers, 52 phases)

## Decision standard

Every phase was reviewed against seven child-facing criteria on a 1-5 scale:

1. **Theme** - the visible object and action are the named job.
2. **Uniqueness** - the phase has an identity beyond a recoloured shared meter.
3. **One-finger playability** - targets are large, causal, and reachable.
4. **Fun** - touch produces an immediate, legible reaction and a satisfying payoff.
5. **Pace** - the beat is short enough for the audience and does not stall.
6. **No-fail clarity** - the wordless demonstration teaches the real successful action.
7. **Replay value** - repetition comes from a small authored pattern set or expressive
   interaction, not procedural churn.

`K` means keep the mechanic, `R` means repair its presentation or contract, and `X`
means replace the interaction. A repair may still replace a wrong object layer.

## Executive finding

The shipping table names 19 modes, but 37 of 52 phases (71%) were still assembled
from only `choice`, `circle`, `hold`, `swipe`, and `tap`. The strongest identities
came from the thirteen specialist beats: lens search, oven, dance phrase, candy sort,
X-ray, farm lob, boxer combo, title round, paint reveal, pipes, kart, nursery catch,
and echo song. Those specialist games are retained.

The central defect was more serious than repetition: several movers were the wrong
semantic object. Chef MIX rotated a second bowl as a pitcher, Candy SYRUP rotated a
candy-and-mold tableau, Racer TUNE spun the complete kart, Magician CABINET showed
the rope card, and Nursery FEED had no bottle. Generic target taps also accepted any
point while promising cake toppings, candy handoffs, picnic snacks, or rocket repairs.

### Career-level scorecard before this pass

Scores are `Theme / Uniqueness / One finger / Fun / Pace / Clarity / Replay`.

| Career | Score | Audit verdict |
|---|---:|---|
| Chef | 4/3/5/4/4/3/3 | Keep the arc; repair pour art, oven contract, and toppings. |
| Detective | 3/3/4/2/2/1/2 | Keep lens; replace case board and crown payoff. |
| Ballerina | 5/3/5/4/4/3/3 | Keep; improve phrase mercy and wordless cues. |
| Candymaker | 4/3/5/4/4/3/3 | Keep sort; repair syrup, wrapping, and handoff semantics. |
| Doctor | 5/3/5/4/4/3/3 | Keep; repair choice cue and distinguish cast feedback. |
| Farmer | 3/3/5/3/4/2/3 | Keep lob; replace fake planting and anchor the picnic. |
| Boxer | 5/5/5/5/4/3/4 | Keep; strongest distinct career. |
| Magician | 3/1/4/2/3/2/2 | Replace wrong-art reskins; add a signature cabinet action. |
| Painter | 5/4/5/4/5/5/3 | Keep; cohesive and child-readable. |
| Astronaut | 5/4/4/4/3/3/4 | Keep pipes; repair demo selection and patch causality. |
| Racer | 4/4/4/4/3/3/5 | Keep race; repair pit-stop art and pre-race travel. |
| Nursery | 3/4/5/4/4/3/3 | Keep catch; repair bottle, burp pulse, and blankets. |
| Popstar | 5/4/5/4/4/3/4 | Keep echo; repair dance cue and encore object. |

## Per-phase audit and disposition

| Career | Phase | Before | Decision | Required child-facing result |
|---|---|---|:---:|---|
| Chef | MIX | Whole bowl rotated as a pitcher; flat fill | R | Real batter pitcher tilts, stream lands, bowl visibly fills to brim. |
| Chef | STIR | Correct whisk, repeated circle grammar | K | Whisk and batter react continuously; shorter rotation goal. |
| Chef | BAKE | Strong oven, any-screen completion, generic success disk | R | Only the mitt removes cake; achieved baked cake remains visible. |
| Chef | FROST | Themed trace; path acceptance too loose | K/R | Wide forgiving frosting corridor, visible ribbon growth. |
| Chef | TOP | Whole cake followed finger; generic disks | R | Seven large cake sockets accept real topping sprites once each. |
| Detective | SEARCH | Strong lens; demo cannot reach upper clues | R | Demo visits the next unresolved clue with the lens fully onscreen. |
| Detective | CASE BOARD | Static three-choice chest reskin | X | Drag paw, feather, and ribbon clues to matching silhouettes. |
| Detective | CROWN | Abstract moving bar; any tap wins | X | Tap the chest handle, see it open, and reveal the pearl crown. |
| Ballerina | PHRASE | Strong call/repeat; one mistake erases all four | R | Preserve a correct prefix or replay a shorter mercy phrase. |
| Ballerina | POSE | Generic expanding glow | R | Pose hold opens the stage blossom and visibly sustains it. |
| Ballerina | RIBBON | Correct object and gesture | K | Keep authored ribbon path and completion flourish. |
| Ballerina | TWIRL | Themed but shared crank | K | Keep; use the actual ribbon/mirror-ball mover. |
| Candymaker | SYRUP | Candy-and-molds rotated as jug; ended at 90% | X/R | Real syrup jug fills molds to 100% before ding/completion. |
| Candymaker | SORT | Strong direct conveyor sort | K/R | Keep; add piece squash, bin bounce, and wrapped payoff. |
| Candymaker | WRAP | Themed object, generic crank | R | Alternate visible wrapper ends rather than spin a tableau. |
| Candymaker | SHARE | No recipients; arbitrary marks | X/R | Place individual candies at six generous handoff anchors. |
| Doctor | WASH | Themed basin fill | K | Keep bubbles and achieved shine. |
| Doctor | FIND | Good plush art; later answers invisible | R | Re-cue every new plush after a correct choice. |
| Doctor | X-RAY | Strong scanner mechanic | K/R | Keep; instruction and scanner sweep must agree. |
| Doctor | CAST | Correct bandage, repeated crank | R | Make wrap growth, not scalar rotation, the dominant feedback. |
| Doctor | BANDAGE | Themed swipe | K/R | Reveal around the plush in a wide wrap corridor. |
| Farmer | PLANT | Piglets/hay represented planting | X | Move seeds to five glowing holes; each hole visibly sprouts. |
| Farmer | TOSS | Strong pull-and-release arc | K/R | Cycle approved foods and animate a pig munch on landing. |
| Farmer | HERD | One group shifted only 42 px | R | Move several pigs across the card and through the gate. |
| Farmer | PICNIC | Whole group followed finger; generic disks | X/R | Place three distinct foods once, beside the three visible piggies. |
| Boxer | COMBO | Strong mitt phrase and duck | K | Keep direct mitt recoil and duck interlude. |
| Boxer | TITLE ROUND | Full AI/pose animation | K | Keep; best-animated Opera phase. |
| Boxer | BELT | Appropriate short payoff, any tap | K/R | One generous belt hotspot, crest glow, then curtain call. |
| Magician | VANISH | Unrelated text-bearing lamb card | X/R | Hat, wand, fade, and reveal are the visible action. |
| Magician | TRACK | One shuffle, then blind choices | X/R | Run a visible hat permutation for every round. |
| Magician | ROPE | Correct rope trace | K | Keep; wide forgiving corridor. |
| Magician | CABINET | Exact rope-card duplicate | X | Downward handle swipe opens the cabinet and reveals the act. |
| Magician | PORTAL | Plausible art, shared crank | R | Keep the circle but animate portal light, not a whole stage. |
| Painter | PAINT | Strong coverage painting | K/R | Keep; add brush cursor and soft paint bloom. |
| Painter | STAMPS | Creative free placement, generic stamp | K/R | Painter alone keeps free placement; use real stamp sprites. |
| Painter | GALLERY | Short appropriate choice | K | Keep; hold the hung sunrise as achieved art. |
| Astronaut | PIPES | Strong route puzzle; stepped fuel | K/R | Keep; select a compatible demo tile and interpolate fuel travel. |
| Astronaut | PATCH | Whole rocket followed finger; arbitrary disks | X/R | Five deterministic leak anchors accept repair patches once. |
| Astronaut | VALVE | Correct valve rotation | K | Keep; improve bubble travel if budget permits. |
| Astronaut | LAUNCH | Correct fiction, weak static rocket | K/R | Countdown hold builds flame/shake and ends in launch lift. |
| Racer | TUNE | Complete kart rotated on a track | X/R | Stationary kart/pit card with an isolated wrench action. |
| Racer | TO THE LINE | Correct kart, only 42 px of travel | R | Kart crosses most of the card to the starting arch. |
| Racer | RACE | Unique full kart game, long first lap | K/R | Keep; target a shorter first lap or faster repeat entry. |
| Nursery | WASH HANDS | Baby card used instead of clear basin | R | Use the basin scene and bubbles. |
| Nursery | CATCH BABIES | Strong catch; progress bar overlap | K/R | Keep; cradle demo travels and settled babies remain visible. |
| Nursery | FEED | Swaddled baby used as held tool | X | Bottle moves to mouth, tilts, drains, and baby reacts. |
| Nursery | BURP | False timing bar over cooldown rule | R | Pat pulse and baby reaction show the real gentle pace. |
| Nursery | BEDTIME | Baby shifted down, no blanket action | X | Blankets travel over three babies; sleeping state holds. |
| Popstar | SOUND CHECK | Themed but generic hold | K/R | Microphone/note visibly grows and pulses with the hold. |
| Popstar | DANCE | Good arrows, later cues invisible | R | Re-cue every step and animate the pressed arrow/floor. |
| Popstar | RHYTHM | Strong untimed echo memory | K/R | Keep; clear every lit-note glow without waiting for more input. |
| Popstar | ENCORE | Entire proscenium stage rotated | R | Rotate/pulse a beat or microphone flourish, never the whole stage. |

## Blocking correctness findings

- Multi-step choice phases became blind after the first accepted choice because input
  disabled the demo and only wrong choices re-flashed the answer.
- Candy SYRUP used goal `4.5` although its controlled pour emits `5.0`, completing
  before the brim/ding.
- Echo's accepted-note glow decayed in state without requesting redraw.
- Oven input ignored the demonstrated mitt handle and accepted a tap anywhere.
- The third pipe-board demo selected tray slot zero even when that tile was incompatible.
- Nursery catch content and settled babies overlapped the generic progress bar.
- The BURP card displayed a timing zone although success was governed by a simple
  gentle-tap cooldown.
- X-RAY and Farmer TOSS were associated with unrelated painted landmarks.

## Art reuse and generation decision

The art pass inventoried the approved Opera flat-card masters before generation.
Existing sources already provide clue tokens and boards, crown chest states, cake
toppings, candy pieces, farmer foods, paint stamps, hats, wand, cabinet and reveal,
finished cake, kart/pit art, and popstar beat objects. These are non-destructively
derived; they are not redesigned.

Only four isolated tool roles had no clean approved source: Chef batter pitcher,
Candymaker syrup jug, Nursery feeding bottle, and Racer wrench. They were generated
together as one tightly scoped chroma source board, then independently alpha-matted,
cropped, and packed. The accepted board has four complete, separated objects with no
text, characters, detached pieces, cropping, or cross-cell overlap. Exact prompt,
source references, hashes, transformations, runtime hashes, and visual review live in
`assets_src/imagegen/opera_minigame_quality_2026-08-09/`.

## Animation contract

Object liveness is causal, not decorative:

- Idle demonstrations act on the real control and stop inviting false touches.
- Direct manipulation changes the object under the finger.
- Wrong/outside input may sparkle and re-hint but cannot silently advance.
- Each accepted unit produces object-local motion (move, tilt, squash, fill, reveal,
  recoil, sprout, open, wrap, or reaction), not only Roshan bounce/confetti.
- Completion holds the achieved object state for the existing 2.2-second celebration.
- Static base cards remain cheap; only the isolated object ROI is animated, respecting
  the Speedy mobile overdraw budget.

## Implemented result

The shipping career table and gesture surface now implement the audit rather than only
describing it:

- Detective received a real optical search, horizontal clue-matching board, and
  handle-opened crown chest.
- Ballerina received a four-pad memory phrase with prefix mercy, a causal blossom
  hold, one-pass ribbon trace, and a short ribbon twirl.
- Candymaker received a real syrup vessel, deterministic drag sorting, wrapper-local
  motion, and six visible candy recipients.
- Doctor's scanner, cast, and bandage now act on the patient; later choice answers are
  always re-cued.
- Farmer received five sprouting seed beds, three cycling lob foods with pig reactions,
  a one-journey three-pig herd, and one unique picnic food per visible piggy.
- Magician received coherent vanish, shuffle, rope, cabinet, and portal actions. The
  doorway stays stationary while only the inner portal field rotates.
- Astronaut pipe teaching chooses a useful tile; repairs use one-use leak anchors; the
  valve stays object-local; launch shows exhaust, shake, and lift.
- Racer's wrench installs only the missing rear wheel, the kart reaches its arch in one
  continuous push, and the existing kart race remains the payoff.
- Nursery uses a basin, the approved bottle, paced pats, and three persistent physical
  blanket tucks. None of those phases reuses combat or a copied baby card.
- Chef, Painter, Pop Star, and Boxer retain their strongest job identities while their
  shared verbs now animate the named object instead of a generic meter or whole card.
- Frosting, ribbon, bandage, and rope are ordered authored journeys: a complete pictured
  traversal completes once; reverse or off-object scrubbing pays nothing and re-hints.
- Long pushes likewise normalize one demonstrated start-to-finish journey to one phase,
  eliminating repeated left-to-right scrubbing.

The art pack contains 36 governed runtime PNGs plus three governed source/review images.
Thirty-two runtime roles were derived non-destructively from approved repository art;
only the four genuinely missing isolated tools were generated together on one source
board. The build tool reproduces all 39 governed files byte-for-byte.

## Verification contract

The release checks for this pass must prove:

- all 13 careers and 52 shipping phases load;
- all new specialist modes accept real input and reject stationary/outside shortcuts;
- every successive choice is visibly cued;
- Detective lens demos reach their actual clues;
- Candy pour cannot complete below the brim;
- oven completion requires the mitt;
- every non-Painter target anchor pays at most once;
- Nursery feed, burp, bedtime, and catch occupy non-overlapping card geometry;
- source-to-runtime art derivation is deterministic and passes alpha-margin checks;
- object pixels change between idle, active, and achieved captures without relying on
  the ghost hand or Roshan animation.

Recorded family voices are protected owner assets and are never modified by this pass.
Where an existing exact line contradicts a rebuilt action, a compatible existing family
cue may be selected; remaining rerecord needs stay explicit rather than silently changing
protected recordings.

## Verification result

Final local validation on exact Godot `4.7.1-stable`:

- full `scripts/ci.sh`: exit 0 after fresh import and every trusted project probe;
- Opera gesture/object-animation probe: **ALL OK (214 checks)**;
- all-13-career Canvas integration: **ALL OK**;
- Detective, pipes, Nursery, UI, and zero-input/passive probes: **ALL OK**;
- full-tree GDScript parser, inference lint, and `git diff --check`: pass;
- deterministic minigame-art rebuild: **39 files match**;
- Roshan animation audit: **13 careers / 208 reviewed frames**.

The generated prop board and derivatives have passed Codex visual/topology/artifact QA.
Owner visual acceptance and a short four-year-old Android Speedy playtest remain pending;
fun and replay ratings should be treated as engineering-review estimates until that
playtest, not as a substitute for observing the child.
