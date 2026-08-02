# The Dust Bunny Boss — character sheet and AI contract (2026-08-02)

Owner direction (2026-08-02): build the AI behaviour of the **big dust bunny**
from the codex art database. He gets his own boss arena with a **showing**
before the fight, and — unlike every other enemy in the game — he cannot be
hit whenever you like. He is open only in **moments of inner vulnerability**:
while he is **jumping in the air** and the **icon on his head flashes
briefly**. He takes **three damage**, the windows are spaced so three is the
amount a small player actually places over a fight, he becomes **dizzy** after
the first hit, and **angry and faster** after the second.

Implementation: `scripts/games/dust_boss.gd` (Family-A satellite: logic only,
`main` by reference, all state on `m.g` under `db_*`).
Probe: `scripts/probe_dust_boss.gd`.

---

## 1. Who he is (what the codex branches say)

There is no separate boss character in the codex art database — there is a
**dust-bunny cast**, and he is its largest member. The cast was generated for
the Pearl Castle cleanup section; the sheet prompt lives in
`assets_src/concepts/dirty_castle_cleanup_2026-07-22/PROMPTS.md`
("Sprite atlas 04 — dust-bunny cast", branch `codex/dirty-castle-2d`) and
specifies six poses:

> a round front-facing bunny with tall spiral curl ears and pearl paws; a
> happy sibling pair; a hopping bunny with one curled lavender motion tail; a
> bunny peeking from beneath a pearl shell; a sleepy curled bunny with one
> soap-bubble breath; and a smiling family of three. […] pearl paws, big warm
> brown-purple eyes, tiny smiles, coral blush, rounded lavender cloud curls,
> and fine navy-purple outlines. […] **Dust bunnies are friendly helpers, not
> pests, monsters, smoke, or realistic dirt.**

The first of those — `dust_bunny_curl_ears.png`, the large front-facing pose
with the full spiral ears and four pearl paws — is the boss. It is the only
cast member that was never wired into the runtime: the Main Hall spawns the
sleepy, shell-hide and hop poses
(`CASTLE_DUST_BUNNY_SPAWN_GUIDE_2026-07-29.md`), the Playroom rescue reuses
the hop pose twice (`STUFFIE_PLAYROOM_RESCUE_GUIDE_2026-07-29.md`), and the
family card is a hall prop. The big one stayed on `codex/dirty-castle-2d`
unused. It is brought forward here unchanged (see `ASSET_LICENSES.md`).

Everything else in the branches is supporting material rather than character
canon: the hall bunnies are the castle's mascots with idle-life animations
(`FABLE_CASTLE_ANIMATION_INTERACTIVITY_HANDOFF_2026-07-29.md` §"Bunny idle
life"), the cinematic frames show Baby Eagle sweeping bunnies toward a
dustpan, and the effects family (`fx_dust_bunny_hop`, `fx_dust_poof`,
`fx_dust_bunny_friend_heart`) is all motion, poof and **friendship** — no
combat art exists for them anywhere.

**So the fight is written to that canon.** He is not a monster and nobody
loses: he is the Great Dust Bunny of the castle attic who has been hoarding
every speck of the castle's shine into his nest. Bonking him is a game he is
playing too — he giggles when taps bounce off, sulks when he is dizzy, huffs
when he is cross, and the third hit **befriends** him: he bursts into stars,
deflates into a small cuddly puff, and gives the castle's shine back.

## 2. The showing

The fight never opens on the fight. `build()` enters state `showing`
(6.4 s):

1. he swells up out of a lavender dust nest at the far end of the attic;
2. he takes one big parade hop;
3. the star over his head **flashes three times** while the message and the
   voice line name the tell: *"When he JUMPS and his star FLASHES — TAP him!"*

Taps during the showing do nothing at all. The child is being taught the one
rule of the fight, not tested on it. He is also met once more before that: the
attic door in the reef has him peeking out of it, so he is a character she has
seen before he is ever an opponent.

## 3. The AI state machine

| State | What he does | Can he be hit? |
| --- | --- | --- |
| `showing` | rises, parades, demonstrates the tell | no |
| `prowl` | hops around the plane; sometimes bounces at Roshan for a harmless giggly bump | no — taps poof off |
| `windup` | squashes down, star begins to glimmer (0.7 s telegraph) | no |
| `vuln` | **leaps, hovers, star strobes gold, finger pointer appears** | **yes — one hit** |
| `struck` | recoil, spin, star burst; becomes dizzy / angry | no |
| `friends` | deflates into a cuddly puff, stars, win banner | fight over |

`prowl → windup → vuln → prowl` is the loop; a landed hit inserts `struck`.

**Damage exists in exactly one place in the file** (`_tick_vuln`): state is
`vuln`, the tap is a fresh input edge from `SideScrollStage.brawl_tick`, and
Roshan is inside `reach()` of him. That is why zero-input play can never
scratch him (`probe_passive`), and why a tap at any other moment is a poof and
a giggle rather than a miss.

## 4. The three phases

`PHASES` in `dust_boss.gd` is the whole tuning surface — one row per number of
landed hits:

| Hits landed | Phase | Hop speed | Hop gap | Prowl between windows | Window | Chases her |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 0 | `puffy` | 10.0 | 0.78 s | 3.4 s | 2.6 s | 30% of hops |
| 1 | `dizzy` | 6.4 | 1.15 s | 4.0 s | 3.2 s | 15% of hops |
| 2 | `angry` | 16.5 | 0.46 s | 2.4 s | 2.1 s | 65% of hops |

- **Hit 1 → dizzy.** He lands hard, his ears spin, and he wobbles in place for
  an extra 2.6 s before the next prowl. He then moves *slower* than he started
  and his next window is the *longest* in the fight — the reward for the first
  hit is a breather.
- **Hit 2 → angry.** He puffs up 12%, tints warm, huffs for 1.5 s, and then
  moves at **1.65× his opening pace** with the shortest windows and the most
  chasing. This is the only difficulty step in the fight.
- **Hit 3 → friends.** No third escalation: the fight ends.

## 5. Window spacing (why three damage is what a player places)

- One landed hit **closes the window** (`HITS_PER_WINDOW = 1`), so three hits
  means three separate windows — the number is the pacing, not a health bar
  that can be burned down in one flurry.
- A window is 2.6 s of unmistakable strobing (dizzy 3.2 s, angry 2.1 s) with a
  0.7 s wind-up in front of it, and the gap between windows (2.4–4.0 s of
  prowl) is longer than the window itself. Watch, wait, tap.
- He **leaps toward Roshan**, so the skill is timing, not aim. `reach()` is
  12 units on a 50-unit-wide stage: standing near him matters, but she does
  not have to be precise.
- Typical fight: ~35–45 s, three windows if she reads the tell, more windows
  (never fewer hits) if she does not.

## 6. Mercy — the fight cannot be lost, only lengthened

A window that closes unhit is not a failure. It increments `db_miss`, which:

- lengthens **every later window** by 0.45 s (cap +2.2 s);
- grows her tap **reach** by 1.6 units (cap +6.0);
- **slows him down** by 7% per miss (cap −40%).

So a child who cannot yet read the tell gets a boss who gradually turns into a
slow, wide-open, long-flashing target — and the first missed window also
re-states the tell in voice and text. There is no health bar on Roshan, no
timer, no fail line reachable from play: the giggly bump costs nothing, and
three shielded taps in a row make him giggle the rule back at her.

## 7. Presentation contract

- The boss is a **cutout**, per the 2026-07-27 art direction: unshaded
  billboarded `Sprite3D` at 11.5 units (Roshan is ~7), alpha-scissor, contact
  shadow, never re-lit and never redesigned.
- **The tell is one sprite.** `assets/mg/star.png` sits above his head: small
  and dim lavender (alpha 0.42) while he is shielded, 1.35–1.7× and strobing
  gold at ~3.5 Hz the instant he is open, with an additive glow behind him and
  a 👆 pointer over his head. No text is required to play.
- Phase is legible without words: dizzy wobbles and rocks, angry throbs, warm
  tint, faster hops.
- HUD is pips, not numbers: `⭐ TAP NOW!` / `Watch his star…` plus 💜 per hit.
- Arena: the castle attic (`_enter_arena("dustboss")`) — lavender dusk, one
  round moon window, pearl crates, wood floor. No new lights.

## 8. Probe surface (`scripts/probe_dust_boss.gd`)

Asserts, all through real `touch_ui` tap edges:

- the attic portal exists and opening it starts the fight **in the showing**;
- taps during the showing, the prowl and the wind-up land **no damage**, but a
  shielded tap still answers with a poof;
- the wind-up becomes an airborne window with the star flashing;
- an open window with Roshan on the far side of the attic is **not** a free
  hit;
- a tap on the flash lands exactly one damage and closes the window; further
  taps add nothing;
- hit 1 is dizzy and slower than the opening pace; hit 2 is angry and faster
  than either earlier phase, with shorter windows;
- a window let go increments the mercy count, lengthens the next window and
  grows her reach — and the fight is still running;
- the third hit ends the fight as `friends`, the banner closes it, and the
  portal pearls are paid.

Registered in `scripts/ci.sh` and `.github/workflows/probes.yml`.

## 9. If the owner meant "three damage per window"

The reading implemented here is **three damage total, one per window**, which
is what makes hit 1 → dizzy and hit 2 → angry line up with the windows. If the
intent was instead up to three damage inside a single window, it is one
constant: `HITS_PER_WINDOW` in `dust_boss.gd` (and `HP` if the fight should
still end after three). Nothing else in the state machine changes.
