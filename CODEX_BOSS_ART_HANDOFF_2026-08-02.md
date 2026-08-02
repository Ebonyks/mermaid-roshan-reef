# Codex handoff — boss animation, overlays and art production (2026-08-02)

**From:** the Dust Bunny Boss stress test
(`DUST_BUNNY_BOSS_STRESS_TEST_2026-08-02.md`)
**Scope:** the art weaknesses the stress test exposed — animation, overlays,
and the production gaps that will hit every boss and every combat screen after
this one, not only Grand Puff.

The gameplay is measured and working. What the visual pass found is that the
encounter's *meaning* is carried almost entirely by code-drawn primitives and
on-screen sentences, and that a non-reading 4-year-old is being asked to read.
That is art work, and it is the highest-leverage art work in the project right
now.

Reference frames (regenerate any time — this is the review loop):

```
DUSTBOSS_SHOT_OUT=/tmp/dustshots LIBGL_ALWAYS_SOFTWARE=1 \
  xvfb-run -a godot --rendering-method mobile --resolution 1280x720 \
  -s scripts/probe_dust_boss_shots.gd
```

Ten frames, one per beat: showing rise, demo flash, shielded hop, wind-up,
**window open**, struck/dizzy, dizzy prowl, angry prowl, angry window,
befriending.

---

## 0. The one-paragraph brief

Grand Puff is the largest member of the codex dust-bunny cast
(`dust_bunny_curl_ears.png`). Canon from the cast atlas prompt: *"Dust bunnies
are friendly helpers, not pests, monsters, smoke, or realistic dirt."* He is
not evil. He has hoarded the castle's shine into his attic nest, the fight is a
game he is playing too, and the third bonk **befriends** him. Every asset below
must read as cuddly mischief, never threat.

Style is unchanged and non-negotiable: polished flat-colour storybook, broad
cel-shaded shapes, fine navy-purple contour, pearl / lavender / aqua / coral /
restrained gold, readable on a small phone, `#00ff00` chroma workflow with
local alpha, ≤1024 px longest side or power-of-two, every new file gets its
`ASSET_LICENSES.md` line in the same commit.

---

## 1. Priority 1 — the boss has one pose for a fight with three moods

**The problem.** The fight's whole story is his mood: puffy → **dizzy** (bonked
once) → **angry** (bonked twice) → **friends**. In the build, all four are the
*same* 512×512 card with a colour multiply and a sine wobble. The measured
encounter spends 12.4 s in dizzy and 10.2 s in angry — a third of the fight
each — expressing them with a tint the child probably cannot name.

**Ask — one 3×2 atlas, `dust_bunny_boss_moods` (chroma-key, 512 per cell):**

| Cell | Pose | Must read as |
| --- | --- | --- |
| 1 | **puffy idle** — front-facing, spiral ears up, four pearl paws | "big, pleased with himself" |
| 2 | **squash / wind-up** — compressed to ~70 % height, ears flattened back, eyes squeezed shut | "he is about to spring" |
| 3 | **airborne / open** — stretched ~115 %, ears streaming, paws tucked, mouth a delighted O | "he is UP and this is the moment" |
| 4 | **dizzy** — tilted, spiral-swirl eyes, one ear drooping, tongue tip out | "I bonked him and he is silly now" |
| 5 | **angry** — puffed 15 % wider, ears rigid and forward, brows down, cheeks coral, a comic huff | "cross, not scary — he is going to be fast" |
| 6 | **friends** — deflated small, sitting, eyes closed happy, one paw waving | "we are friends now" |

Anti-goals: no teeth, no sharp eyes, no smoke, no shadow-monster silhouette, no
redesign of the face from the existing card.

**Why it is worth it:** with these six the fight's escalation becomes legible
without a single word, which is the point of the whole encounter.

---

## 2. Priority 2 — the tell is a generic star with an emoji on top

**The problem.** The vulnerability window — the one thing the child must read —
is currently `assets/mg/star.png` (the generic reward star, reused everywhere
else in the game) with a 👆 **emoji Label3D overlapping it**. See frame
`05_window_open.png`. Two failures: the icon means "reward" in every other
screen, and the pointer sits *on* the icon instead of beside it.

The stress test also showed the tell is currently redundant with the jump —
one design answer is fake-out leaps where he goes up **without** the star, and
that only works if "star on" versus "star off" is unmistakable at arm's length
on a phone.

**Ask — `boss_tell_set` (4 cells, transparent, 512 each):**

1. **shielded badge** — a small dull lavender-grey puff-crest, low contrast,
   clearly *closed*. It must not look like a dimmed version of the open badge;
   it must look like a different object.
2. **open badge** — a bright coral-gold burst-star with a white core and a
   thick navy contour, ~2× the shielded badge's area, designed to strobe.
3. **open badge, strobe frame B** — the same badge with the core bloomed and
   the points extended, so the flash is a two-frame animation instead of an
   alpha pulse.
4. **the pointer** — a chunky downward finger/arrow with a pearl cuff, designed
   to sit **above** the badge with clear space, never overlapping it.

Plus one **ring decal** (`boss_open_ring`, 1024 square, transparent): a soft
coral-gold ground ring that appears on the deck under him only while he is
open. Ground rings are the cheapest "here, now" signal there is, and this fight
has none.

---

## 3. Priority 3 — nine spoken lines that do not exist, so the game is asking her to read

**The problem, exactly.** The encounter fires nine voice events —
`dustboss_show`, `_tell`, `_leap`, `_dizzy`, `_hit`, `_angry`, `_again`,
`_win`, `_closer` — and **none of the clips exist**, so each falls back to a
generic pitched "yay". The information itself only ever appears as an on-screen
sentence: *"When he JUMPS and his star FLASHES — TAP him!"*, *"BONK! He is all
DIZZY"*, *"He is CROSS now"*. A non-reader gets a noise and a wall of text.
Family voice is the real fix and is not Codex's job — **carrying the same
meaning as pictures is.**

**Ask — `boss_speech_pictograms` (6 cells, 512 each, transparent):** each a
single wordless picture that can be shown in a small card where the sentence
is today.

| Cell | Says, without words |
| --- | --- |
| 1 | **the rule**: bunny silhouette airborne + open badge + a tapping finger, in one row |
| 2 | **too puffy**: a finger bouncing off his side with a poof, a small "nope" arc |
| 3 | **wait for it**: an hourglass-ish pearl timer with the shielded badge |
| 4 | **bonk!** a big coral impact star with three motion dashes |
| 5 | **he is cross**: the angry mood head plus three speed chevrons |
| 6 | **friends!**: the friends pose plus a coral heart |

Design them to read at ~180 px tall on a phone. These also unblock every future
boss: this is a reusable "combat speech" set, not a Grand Puff set.

---

## 4. Priority 4 — the arena is code-drawn primitives

**The problem.** The octagon is a cylinder mesh, the walls are boxes, the posts
are cylinders, the "dust mounds" are spheres that render as flat dark ellipses
(they read as holes in the floor), the crates are grey slabs, and the backdrop
is empty near-white. See `03_prowl_hop_shielded.png`. The set says nothing
about being an attic.

**Ask — the attic-in-the-round set, painted flats:**

| Asset | Size | Notes |
| --- | --- | --- |
| `attic_deck_octagon` | 1024² | a top-down octagonal deck: warm boards, a faint pearl duelling ring, dust drifts in the seams. Tiles onto the existing floor mesh |
| `attic_wall_panel` | 1024×512 | one wall run, repeated 8×: lavender panelling, a dado rail, one knot-hole |
| `attic_post_lamp` | 512² | corner post with a pearl lamp bead — the current white halos are the brightest thing on screen and steal attention from the tell |
| `attic_backdrop` | 2048×1024 | rafters, a round moon window, hanging sheets, cobwebs. Currently pure void |
| `attic_clutter_set` | 3×2 atlas | crate stack, rolled rug, hat box, broken chair, pearl jar, sheet-covered lump — standees for depth |
| `dust_nest` | 1024² | the lavender mound he rises out of in the showing, currently a grey sphere |

Contrast note from the capture: the boss is pale lavender on a pale lavender
deck under a near-white sky. **The deck and walls must sit darker and warmer
than he does** so his silhouette pops — that is a colour-script decision, not a
per-asset one, and it is the difference between a readable fight and a wash.

---

## 5. Priority 5 — the overlay covers the hero

**The problem.** The message banner is a wide pale panel across the middle of
the screen, and Roshan stands exactly behind it. In all ten captured frames the
hero is not visible in her own boss fight. The banner is also the thing
carrying the words she cannot read (§3).

**Ask — a boss HUD kit:**

- `boss_speech_card` (1024×384): a smaller storybook card sized for a
  **pictogram plus 3–4 words**, designed to live at the **top** of the frame.
- `boss_hp_pips` (3 cells): the three bonks as pearl→coral hearts, so progress
  is a picture and not `💜💜·`. Also needed for the medal tiers the audit
  proposes.
- `boss_button_bonk` (512²): the action button currently reads **"JUMP"** in a
  fight whose only verb is a bonk. A wordless paw-bonk glyph fixes it for every
  combat mode.

---

## 6. Priority 6 — nothing in the fight is animated

Everything moves by code tween: a sine wobble, a scale pulse, a tint. There is
no dust, no impact, no anticipation.

**Ask — effect sheets (chroma-key atlases, 3×2, 512 per cell):**

1. `boss_impact_fx` — bonk burst, star ring, three coral impact dashes, a
   pearl shockwave ring, a "seeing stars" halo, a comic sweat drop.
2. `boss_dust_fx` — landing poof, hop trail puffs, a takeoff ring, drifting
   motes (also the tappable prowl motes the audit proposes), a sneeze cloud, a
   settle puff for the "he inflates and re-settles" beat.
3. `boss_friendship_fx` — heart burst, confetti, a shine-returns sparkle
   column, the befriending glow.

**Animation notes for whoever wires these:** the beats that need art support
are (a) wind-up = squash + dust ring at his feet, (b) takeoff = stretch +
takeoff ring, (c) apex = the open badge and ground ring appear together,
(d) landing = poof + a deck shake, (e) bonk = impact burst + the mood change in
the same frame. Right now (a)–(e) are all the same static card at different
heights.

---

## 7. Reusable beyond this boss

Everything in §2, §3, §5 and §6 is deliberately specified as a **combat set**,
not a Grand Puff set. The game already has `combat_arena`, `stuffie_battle`,
the brawler and two dungeons sharing one overhead ring and no shared combat
art. If these land as generic sets, the next boss is a mood atlas and a colour
script rather than a from-scratch art order.

Suggested order if capacity is limited: **§1 (moods) → §2 (the tell) → §3
(pictograms) → §5 (overlay) → §6 (fx) → §4 (set dressing)**. The first three
change whether the fight can be understood; the last changes whether it is
beautiful.

---

## 8. Rules that still bind

- CC0 or project-original only; every file gets an `ASSET_LICENSES.md` entry in
  the same commit that adds it, with source, licence, URL and modifications.
- ≤1024 px longest side **or** power-of-two; VRAM compression only if POT
  (an NPOT texture with `compress/mode=2` deadlocks the headless importer).
- New `.import` sidecars are gitignored — commit the `.png`, not the sidecar.
- Never modify or recompress anything in `assets/book/`,
  `assets/audio/voices/` or `assets/characters/friends/`.
- Mobile renderer on every platform; no new `OmniLight3D`s — the arena is lit
  by unshaded material and additive halos only.
- Nothing here may introduce a fail state, a lost-progress path, or an
  objective that requires reading.
