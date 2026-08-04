# Codex handoff — the boss arena itself (2026-08-03)

**From:** the 24-encounter arena stress test
(`DUST_BUNNY_BOSS_ARENA_STRESS_2026-08-03.md`)
**Scope:** the STAGE. The 2026-08-02 handoff asked for Grand Puff and got him —
the jump, laugh, flinch, angry and implode sheets are excellent and are not
being re-opened. This one is about the room he is standing in, which does not
exist, and about the props that would give the fight's quiet two thirds
something to be about.

> **One sentence:** a beautifully animated boss is fighting on a bare lavender
> slab floating in flat pink void, 40–45% of every frame is empty background,
> and 100% of the moments he must be *read* he is drawn against a pastel prop
> of his own hue and shape family.

**Reference frames** (regenerate any time — this is the review loop):

```
DUSTBOSS_SHOT_OUT=/tmp/dustshots LIBGL_ALWAYS_SOFTWARE=1 \
  xvfb-run -a godot --rendering-method mobile --resolution 1280x720 \
  -s scripts/probe_dust_boss_shots.gd
```

**Style is unchanged and non-negotiable.** Polished flat-colour storybook,
broad cel-shaded shapes, fine navy-purple contour, pearl / lavender / aqua /
coral / restrained gold, readable on a small phone. `#00ff00` chroma workflow
with local alpha. ≤1024 px longest side **or** power-of-two. Unshaded in
engine — never re-lit. Every file gets its `ASSET_LICENSES.md` line in the same
commit that adds it. Wind Waker is a rendering reference only.

**Canon.** Grand Puff is the biggest dust bunny in the Pearl Castle attic. Dust
bunnies are *friendly helpers, not pests, monsters, smoke or realistic dirt*.
He is not evil — he has hoarded the castle's shine into his nest, the fight is
a game he is playing too, and the third bonk **befriends** him. The room must
read as cuddly mischief, never threat. No cobwebs-as-menace, no gloom, no
spiders.

**Camera contract.** Fixed 3/4 view, never pans, never follows. The octagon's
far rim sits around 45% of the frame height and the near rim runs off the
bottom edge; **everything above the far rim is currently empty**. That band —
the top ~45% of a 1280×720 phone — is the single largest piece of unclaimed
screen in the game.

---

## Priority 1 — the attic (the room does not exist)

Four flats, drawn as one continuous painting split for depth. They sit behind
the ring as billboards; the engine will place them, you only need the art and
its ground line.

| # | file | size | what it is |
|---|---|---|---|
| 1.1 | `attic_backwall.png` | 2048×768 (POT) | The back wall of a castle attic: pale timber boarding, a low sloping roof line, two rafters crossing the top, a round dormer window off-centre with soft moonlight coming through. Pearl / lavender / dusty rose. This is the piece that fills the empty 45%. |
| 1.2 | `attic_rafters.png` | 1024×512 | A separate near-camera beam pair with a hanging dust sheet draped over one, to break the top edge of the frame. Bottom 40% transparent. |
| 1.3 | `attic_sidewall_l.png` / `attic_sidewall_r.png` | 1024×768 each | Angled side walls, mirrored, so the octagon reads as sitting *in* a room rather than in front of a picture of one. Stacked hat boxes, a leaning picture frame, a rolled rug — all pale, all silhouette-simple. |
| 1.4 | `attic_lightshaft.png` | 512×1024 | An additive moonbeam falling from the dormer with dust motes suspended in it. Soft, low-alpha, no hard edges. This is the one element allowed to be pure atmosphere. |

**Value contract for the whole set:** everything in 1.1–1.4 must sit at least
**two value steps lighter or cooler than Grand Puff's card**. He is mid-value
lavender; the room must not be. This is the fix for the 100% silhouette clash.

---

## Priority 2 — the deck (the floor is a flat colour)

| # | file | size | what it is |
|---|---|---|---|
| 2.1 | `attic_floor_octagon.png` | 1024×1024 (POT) | Top-down painted octagon deck: attic floorboards running one way, a swept-clean lighter ring in the middle where the fight happens, a scatter of pearl dust caught in the board seams toward the edges. **Boards must run edge-to-edge; the middle third carries the least detail** — that is where the boss stands and where he must separate. |
| 2.2 | `attic_deck_rim.png` | 1024×256 | The repeating rim panel — low skirting board with a dust-bunny-height gap under it, one panel per octagon side. |
| 2.3 | `attic_deck_post.png` | 256×768 | The corner post: a stacked bobbin/spool of thread with a pearl bead lamp on top. Eight of these ring the arena. Currently they are white cylinders that bloom to blobs. |

---

## Priority 3 — the tell (still outstanding from 2026-08-02)

This is the highest-value single item in the document. It was ordered on
2026-08-02 and did not land, so the game is falling back to
`res://assets/mg/star.png` — **the generic reward star it uses for "you won a
sticker" everywhere else.** Open and shielded are currently the same object at
two alphas, which the previous handoff explicitly said must not happen.

| # | file | size | what it is |
|---|---|---|---|
| 3.1 | `boss_tell_shielded.png` | 256×256 | CLOSED. A dull pewter clasp / buckled shell — clearly a *shut* thing. Low chroma, no gold, no rays. Must not read as a reward. |
| 3.2 | `boss_tell_open.png` | 256×256 | OPEN. The same object burst open: gold, rayed, radiating. A different **shape**, not the same shape brighter — a four-year-old reads silhouette long before she reads brightness. |
| 3.3 | `boss_tell_open_strobe.png` | 512×512, 2×2 atlas | Four strobe frames of 3.2 so the flash is authored rather than a sine on `modulate`. |

Both badges will be drawn at roughly **60 px on the phone** (the boss card is
172 px and the badge is ~1/3 of him). Design them to survive that: one shape,
one silhouette, no interior detail smaller than 1/8 of the badge.

---

## Priority 4 — scenery that reads as an object

Measured: the boss occupies **33%** of the ring's reachable cells and Roshan
**46%** — two thirds of the floor is never visited. Do not dress the rim
evenly. Spend the detail where the fight is, and make the three props that
*are* seen actually read.

| # | file | size | what it is |
|---|---|---|---|
| 4.1 | `attic_nest_hero.png` | 1024×768 | **The hero prop.** Grand Puff's nest — a deep bowl of swept dust and lost pearls, castle shine glinting inside it, big enough to read as the reason the room exists. He rises out of this in the showing. Currently an invisible sphere. |
| 4.2 | `attic_crate_pearl.png` | 512×512 | A forgotten pearl crate: slatted box, lid ajar, pearls spilling. Must be **darker and warmer** than the boss. 95 of 126 measured silhouette clashes were against these. |
| 4.3 | `attic_dustmound.png` | 512×384 | A banked dust mound. Same warning: it is currently the boss's exact hue. Give it a warmer, dustier cast and a flatter, wider silhouette so a round bunny never disappears into it. |
| 4.4 | `attic_shadow_soft.png` | 256×256 | A soft radial contact shadow with feathered alpha. The current shadow is a hard-edged navy quad that reads as a rectangular hole in the floor. |

---

## Priority 5 — making the fight more interesting

The stress test found where the spare time is, and it is not where you would
guess. **Dead air is not the problem** — the longest stretch with nothing
moving is 0.40 s median. The problem is that 36% of the encounter is a prowl
with nothing the child can read or affect, and a further 15% is a fixed 7.0 s
hold after every bonk. Those are the two slots to fill, and they are already
reserved, uninterrupted screen time.

### 5a. The prowl (36% of the fight) — give the room something to do

| # | file | size | what it is |
|---|---|---|---|
| 5.1 | `attic_laundry_line.png` | 1024×256 | A line of pastel sheets strung across the back of the ring. He bounces through them; they billow. Turns a repetitive hop into an event. |
| 5.2 | `attic_sheet_billow.png` | 1024×1024, 2×2 atlas | Four frames of one sheet puffing outward as he passes. |
| 5.3 | `attic_crate_burst.png` | 1024×1024, 2×2 atlas | A pearl crate popping its lid and throwing pearls when he lands on it. The single cheapest way to make the prowl matter — his landing spot becomes something to watch. |
| 5.4 | `attic_motes.png` | 512×512 | A drifting dust-mote sheet for the light shaft. Ambient only. |

### 5b. The wind-up (7.8%) — telegraph WHERE, not just WHEN

Right now the wind-up says *he is about to leap*; it does not say *he will
land there*. A floor telegraph turns a reaction test into an anticipation
game, which is dramatically easier and more fun for a four-year-old.

| # | file | size | what it is |
|---|---|---|---|
| 5.5 | `attic_landing_ring.png` | 512×512 | A soft chalk ring that blooms on the deck where he is going to come down. Pastel, additive, no text, no arrow. |
| 5.6 | `attic_landing_ring_hot.png` | 512×512 | The same ring at the instant of the flash — gold, matched to `boss_tell_open.png` so the two read as one signal. |

### 5c. The struck hold (15%, fixed 7.0 s) — the room reacts

The child has just landed three taps and the game freezes for seven seconds.
Give her something to have caused.

| # | file | size | what it is |
|---|---|---|---|
| 5.7 | `attic_shine_return_a/b/c.png` | 1024×768 each | Three progressive dressings of the back wall: **a** dim and dusty (start), **b** one third of the pearls glowing back, **c** the attic bright and clean. One state per landed round. This is the fight's scoreboard, drawn as the room itself — no pips, no numbers, no reading. |
| 5.8 | `attic_dust_updraft.png` | 1024×1024, 2×2 atlas | A column of dust flung upward on impact, so the bonk has a consequence bigger than the boss. |

### 5d. Roshan's side

She does not appear in a single one of the ten captured frames. That is
partly an engineering fix (see the stress-test report, E2), but she also needs
a mark:

| # | file | size | what it is |
|---|---|---|---|
| 5.9 | `attic_hero_ring.png` | 256×256 | A gentle pastel ring that sits under Roshan on the deck, so a four-year-old can always find herself in an arena full of dust. |
| 5.10 | `boss_pip_full.png` / `boss_pip_spent.png` | 128×128 each | Three little dust-puff pips for the rounds left. Drawn as puffs, not hearts — losing a puff is what happens to *him*, and nothing in this fight may look like damage to *her*. |

---

## Delivery

- Drop into `assets/castle/dirty_cleanup_2d/attic_arena/` (new folder) except
  the three `boss_tell_*` files, which belong in
  `assets/sprites/dust_bunnies/boss/` beside the existing sheets.
- Atlases are **row-major 2×2**, four cells, uniform cell size, matching the
  convention `scripts/dust_bunny_boss_sprite.gd` already reads.
- Every file: `ASSET_LICENSES.md` line in the same commit (source, license,
  URL, modifications).
- **Nothing here blocks the game.** Every path is optional in code the same way
  the boss poses are — a missing file falls back and the encounter runs. Ship
  them in priority order; 3.1/3.2 (the tell) and 1.1 (the back wall) are worth
  more than the rest of the document combined.

## What this handoff deliberately does not ask for

- **No new Grand Puff poses.** The five sheets that landed are good.
- **No re-styling of the octagon's geometry.** The ring is convex on purpose
  (a dragged finger always makes progress) and the camera solve is measured
  correct — nothing cropped, tell inside the safe area on 126/126 windows.
- **No darker or scarier attic.** He is a friend by the end of the fight and
  the room has to be somewhere a four-year-old wants to be before that.
