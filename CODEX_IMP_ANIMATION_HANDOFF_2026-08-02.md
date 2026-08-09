# CODEX HANDOFF — imp & rival combat animation states (2026-08-02)

**Requested by the owner as part of the "make the imps a meaningful enemy"
work.** The runtime half is done and merged with this document: the shared
imp brain (`scripts/imp_ai.gd`, spec in `IMP_AI.md`) now makes the imps
decide, telegraph, commit, swipe and recover. Every one of those beats is
already played on screen procedurally (squash, tilt, lift, tint). **This
handoff is the art that replaces the procedural stand-ins.**

Nothing here is blocking: every file is optional and falls through to what
exists today. Deliver in any order; each file that lands upgrades one
moment of the fight the same hour it is committed.

This supersedes and extends PRIORITY 6 of
`OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` (which asked for
`bopped` / `bow` / `hop_a` / `hop_b` / `taunt`). Those five are still
wanted and are re-listed here with their new runtime meaning — the brain
already uses `hop_a` as a wind-up and `hop_b` as a lunge if the dedicated
files are missing.

---

## 1. How the runtime picks a file (read this first)

`opera_career_world_2d.gd::_imp_texture()` resolves, in order:

```
<family>_<state>.png  →  <family>_<fallback state>.png  →  <family> idle
```

`<family>` is **the character's own sheet** and never crosses over:

| who is on stage | family prefix |
|---|---|
| the crew in a competitive career act (chef, detective, …) | `rival_<costume>` |
| the crew in a cooperative act (nursery) and every base-imp use | `imp_mischief` |
| the imp captain in a cooperative act | `imp_captain` |

A chef-hatted imp will therefore **never** borrow the bare imp's body for
one frame — a missing costume state falls to that costume's own idle, not
to another character. Fallback chain per pose:

| brain pose | tries | then | then |
|---|---|---|---|
| windup | `_windup` | `_hop_a` | idle |
| charge | `_charge` | `_hop_b` | idle |
| slash | `_slash` | `_hop_b` | idle |
| recover | `_recover` | — | idle |
| guard | `_guard` | — | idle |
| taunt / rally | `_taunt` | `_bow` | idle |
| flee | `_flee` | `_hop_b` | idle |
| stagger | `_stagger` | — | idle |
| bopped | `_bopped` | — | idle |

All files live in `assets/opera/worlds/actors/`.

---

## 2. Global rules (paste into every prompt)

Identical to the PRIORITY 6 contract — the base-imp six-sprite set is
still the quality benchmark:

- Canvas **512×512, RGBA, transparent background**. Semi-transparent
  fringe (16 < alpha < 240) **< 15%** of solid pixels; `imp_captain.png`
  (6.8%) is the target.
- **Full figure in frame**, ≥12 px clear margin on all four sides, feet
  complete including soles. Nothing touches a canvas edge.
- **Baseline/anchor lock:** soles at **y ≈ 504**; standing height
  (horn-tip to toe) **480–490 px**; pivot = bottom-centre **(256, 504)**;
  horizontal centroid within **256 ± 24**. Airborne poses (`charge`,
  `hop_b`, `bopped`) keep the same body scale and centroid window — never
  shrink the character to fit an effect.
- The engine anchors these sprites **by the feet** and mirror-flips them
  freely: no readable text or logos, and draw every pose facing
  **3/4-front, leaning to viewer-left**.
- **Alpha integrity:** exactly one connected solid component; no interior
  holes > 200 px except true see-through gaps between limbs and body.
  (This is the `imp_captain_bow` shorts bug — reject any output with
  background showing through solid cloth.)
- **Costume-consistency lock:** pass that character's existing idle
  (`rival_<costume>.png` / `imp_mischief.png` / `imp_captain.png`) as the
  style reference. Identical skin purple (`#d070f0` family), amber eyes,
  fangs, ear/horn shapes, tail; identical garments, colours, shoes, hat in
  **every** state. Held props (chef's whisk, detective's magnifier…)
  appear in **all** states, in the same hand — including bopped — so a
  state swap never pops a prop in or out. Dizzy-spiral eyes in `bopped`
  only.
- **No baked FX**: no stars, no speed lines, no dust, no glow. The runtime
  draws the telegraph ring, the swipe arc, the dust puff and the stolen
  sparkle. `fx_dizzy_stars.png` (P6 item 5) supplies bopped stars.
- Style: the imp set's soft painterly shading and line weight; pastel toy
  playset, navy/indigo contours (`#4a4f78`–`#1a1238`), never black.
- **Silhouette test:** every state must be tellable from that character's
  idle **at 25% scale, in black silhouette only**. That is the whole point
  — a four-year-old reads these at ~110 px tall, in motion, on a phone.

---

## 3. The states

Durations are what the brain actually holds each pose for (see
`IMP_AI.md`); "reads as" is the message the child must get without words.

| # | suffix | on screen | reads as | pose direction |
|---|---|---|---|---|
| 1 | `_windup` | **0.55–1.35 s** (the longest-held pose in the fight) | "I am about to lunge — bop me NOW" | Deep coil: knees bent hard, weight back on the heels, both arms drawn back and low, shoulders hunched, chin tucked, ears and tail swept BACK. Eyes wide and locked forward on the viewer. Mouth in a gritted grin. Body compressed to ~82% of standing height but soles still at y≈504. Must read as *stored energy*, the opposite of the taunt. |
| 2 | `_charge` | 0.4 s | "committed — this is happening" | Full-stretch lunge, airborne: body leaning ~30° forward, back leg trailing straight, front arm reaching, ears and tail streaming BACK, mouth open. Lift the whole figure 40–60 px (feet clear of the baseline) while keeping body scale. |
| 3 | `_slash` | 0.28 s | "the swipe" | Mid-swing at the end of the lunge: torso rotated through, leading arm swept across the body to the opposite hip, claw open, trailing arm counterweighted back, one foot planted. Feet return to y≈504. The engine rolls the sprite ±0.55 rad through the swing, so draw the pose neutral-upright and let the roll carry it. |
| 4 | `_recover` | **1.15–1.6 s** (second-longest — this is the counter window) | "I am wide open — hit me" | Slumped, off balance: knees buckled, shoulders dropped forward, arms hanging loose and low, head down, ears drooping, tail dragging. Body compressed to ~88% height. Panting mouth, eyes half-closed. Must look *harmless and inviting*, never scary. |
| 5 | `_guard` | 0.8 s (captains only) | "that one bounced off" | Both forearms crossed up in front of the face, elbows in, shoulders raised, body narrowed and slightly turned side-on, one foot braced back. Eyes peeking over the arms, cheeky. Height ~102% (up on the toes of the back foot, soles still at 504). |
| 6 | `_stagger` | 0.5 s | "ow! (giggling)" | Reeling backwards off one foot, arms flung out to the sides for balance, head snapped back, ears up, mouth in a surprised "O". **Not** dizzy-eyed — that is `bopped` only. The engine wobbles the sprite ±0.3 rad. |
| 7 | `_flee` | 1.1 s | "nope, running away" | Running away from the viewer: body turned three-quarters BACK, looking over the shoulder with a cheeky grin, arms pumping, one leg lifted high, ears and tail forward with the motion. This is the only state drawn from behind. |
| 8 | `_taunt` | 0.85–1.0 s | "come and get me!" | Standing tall, weight on one leg, one arm waving overhead, the other on the hip, chest out, cheeky grin, ears up, tail curled up. (P6 item 10 — unchanged.) |
| 9 | `_hop_a` | fallback for `_windup` | crouch anticipation | Knees bent, arms back, ears/tail down; soles at y≈504. (P6 item 8 — unchanged.) |
| 10 | `_hop_b` | fallback for `_charge`, `_slash`, `_flee` | airborne stretch | Legs tucked, arms up, ears/tail up, body lifted 40–60 px. (P6 item 9 — unchanged.) |
| 11 | `_bopped` | 0.62 s (spins out and fades) | "popped!" | Knocked back mid-air, limbs flailing, dizzy-spiral eyes, open wailing mouth, **no stars**. (P6 item 6 — unchanged.) |
| 12 | `_bow` | curtain call / taunt fallback | "good show" | Deep stage bow to viewer-left, one arm swept out, feet planted. (P6 item 7 — unchanged.) |

Tone note, binding: these are **mischief** imps in a children's opera.
Every pose is cheeky, never menacing — no bared weapons, no blood, no
snarling. The wind-up is a pantomime villain's "I'm gonna get you", not a
threat.

---

## 4. Manifest and priority

### Tier A — the base imp set (14 files, do these first)

They ship immediately in the cooperative acts, they are the style
reference for everything else, and they are what a future 3D→billboard
migration of the brawl/arena imps will use.

```
imp_mischief_windup.png   imp_captain_windup.png
imp_mischief_charge.png   imp_captain_charge.png
imp_mischief_slash.png    imp_captain_slash.png
imp_mischief_recover.png  imp_captain_recover.png
imp_mischief_guard.png    imp_captain_guard.png      ← captain guard is the used one
imp_mischief_stagger.png  imp_captain_stagger.png
imp_mischief_flee.png     imp_captain_flee.png
```

Plus the outstanding P6 fixes, still wanted:
`imp_captain_bow.png` (regenerate — 1,252 px alpha hole through the
shorts), `imp_mischief_taunt.png`, `imp_captain_taunt.png`,
`fx_dizzy_stars.png`.

### Tier B — the twelve costume crews (7 states × 12 = 84 files)

`rival_<costume>_{windup,charge,slash,recover,guard,stagger,flee}.png`
for: **chef, detective, ballerina, candymaker** (play-tested most), then
doctor, farmer, boxer, magician, painter, astronaut, racer, popstar.

Ship them **per costume, all seven at once** — a costume with three states
looks less coherent than one with none, because the fight keeps cutting
between finished and stand-in poses. One complete costume per batch is the
right unit of delivery.

Tier B also still wants the P6 items: the 12 idle re-renders (feet
cropped, magician's 56% semi-alpha matte, detective's ghosting) and the 5
P6 states per costume.

### Tier C — combat FX sprites (4 files, procedural today)

The runtime draws these with `draw_arc`/`draw_circle` right now; raster
art upgrades them without any code change beyond the loader.

| file | canvas | what |
|---|---|---|
| `fx_telegraph_ring.png` | 512×512 | gold alarm ring that sits on the ground under a winding-up imp, plus a separate `fx_telegraph_bang.png` 128×256 "!" glyph in the same gold — chunky, storybook, no outline black |
| `fx_slash_arc.png` | 512×256 | a single white/aqua swipe crescent, thick at the middle, tapering both ends, ~25% opacity core with a bright leading edge |
| `fx_dust_puff.png` | 256×256 | lavender-white ground puff for a launched charge |
| `fx_stolen_sparkle.png` | 128×128 | the gold star an imp runs off with after a bump (the child wins it back by popping that imp) |

---

## 5. Acceptance gate (run per file before commit)

Same programmatic gate as P6, plus two pose checks:

1. canvas 512×512 RGBA
2. solid-mass height 480–492 px for grounded poses (`windup` 390–460,
   `recover` 415–470, `guard` 480–500 are the deliberate exceptions)
3. bottom gap 6–10 px for grounded poses; `charge` / `hop_b` / `bopped`
   40–70 px
4. no solid pixels within 2 px of any canvas edge
5. bottom-row solid run < 100 px (crop detector)
6. semi-alpha < 15%
7. connected components = 1 (plus declared FX only)
8. no interior holes > 200 px outside limb gaps
9. dominant skin colour quantizes into the `#d070f0` family
10. **silhouette delta**: black-silhouette IoU against that character's own
    idle **< 0.75** (the pose must actually be a different shape)
11. **centroid lock**: horizontal centroid within 256 ± 24

These thresholds all pass on the imp benchmark files and fail on every
defect the Phase-2 sprite audit found.

---

## 6. Delivery

- Files → `assets/opera/worlds/actors/` (Tier C → `assets/opera/worlds/props/`).
- One `ASSET_LICENSES.md` row per file **in the same commit** (source,
  licence, URL, modifications — project-generated, © Mermaid Roshan LLC).
- Generator prompts + QA renders under
  `assets_src/imagegen/imp_animation_states_2026-08-02/`, per
  `assets/ART_GENERATION_CONTRACT.md`. Candidates without runtime captures
  on the Mobile renderer cap at 2/5 and must not ship.
- No runtime code change is needed to adopt Tier A/B: the loader already
  looks for every filename above. Tier C needs a ~10-line loader in
  `_draw_combat_fx`.
- Never touch `assets/book/`, `assets/audio/voices/`,
  `assets/characters/friends/`, and never regenerate Roshan.

## 7. Out of scope (do not start without an owner decision)

- The matching `roshan_<costume>_<state>.png` set. Roshan is not driven by
  the imp brain and her combat poses are a separate design question.
- 3D imp animation clips. `assets/dungeon/mischief_imp.glb` and
  `assets/ember_fortress/ember_imp.glb` carry no armature, and the brawl
  and arena play every pose on the transform. If those zones migrate to
  2.5D cutouts (GAME_REDESIGN_2P5D_2026-07-27), they reuse Tier A.
