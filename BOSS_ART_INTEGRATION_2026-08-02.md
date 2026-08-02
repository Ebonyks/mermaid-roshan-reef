# Grand Puff — boss art integration manifest (2026-08-02)

The owner delivered the boss sheets from Codex on 2026-08-02 (fifteen images
across three batches, chroma-green or transparent). This is the map from those
cells to the runtime slots, and the exact steps to land them.

**The code is already waiting for them.** `DustBossGame.BOSS_POSES` declares
one drawing per beat, every entry is optional, and any file that is not
present falls back to the placeholder card — so the encounter runs identically
with none, some or all of the art in place. `probe_dust_boss.gd` asserts the
*map* (every beat resolves to a named pose, and a full fight shows idle,
wind-up, open, dizzy, angry and friends), so a cell wired to the wrong beat
fails the gate whether or not the files exist yet.

---

## 1. Where the files go

```
assets/castle/dirty_cleanup_2d/critters/dust_bunnies/boss/
    boss_idle.png            boss_windup.png      boss_open.png
    boss_struck.png          boss_dizzy.png       boss_angry.png
    boss_friends.png         boss_tell_open.png   boss_tell_shielded.png
assets/castle/dirty_cleanup_2d/critters/dust_bunnies/boss/fx/
    fx_boss_burst.png        fx_boss_ring.png     fx_boss_puff.png
    fx_boss_sparkle.png      fx_boss_swoosh.png
assets/castle/dirty_cleanup_2d/critters/dust_bunnies/minions/
    minion_idle.png          minion_hop_a.png     minion_hop_b.png
```

Rules that bind (CLAUDE.md): ≤1024 px longest side **or** power-of-two;
transparent PNG (chroma removed locally, not shipped green); no `.import`
sidecar (they are gitignored — commit the `.png` only); and **one
`ASSET_LICENSES.md` entry per file in the same commit**, recording source
(OpenAI/Codex generation under project direction), licence (project original),
and modifications (chroma key removal, cell crop, resize).

---

## 2. Cell map — which drawing plays which beat

Batch/image numbering follows the order they were sent.

| Runtime slot | Beat it plays | Source cell |
| --- | --- | --- |
| `boss_idle` | `prowl` and the showing, before any hit | B1/img1 top-left (wide scowling puff, crest sparkle, two pearls) — or B3/img12 top-left winking variant if a friendlier opening is wanted |
| `boss_windup` | `windup` — the 0.7 s squash before every leap | **B2/img6 top-right**: compressed puff with motion arcs closing in. This is the anticipation frame the fight has never had |
| `boss_open` | `vuln` — airborne, the only hittable beat | **B1/img1 bottom-left**: body lifted with the dust puff *below* it. Reads as "he is up there" even with the shadow removed |
| `boss_struck` | `struck` after hits 2 and 3 | **B2/img6 top-left**: eyes wide, fanged "oh!", four impact arrows converging |
| `boss_dizzy` | `struck` after hit 1 | **B1/img4 bottom-left**: spiral eyes, drooping ear, wobble arcs. Exactly the pose the audit asked for |
| `boss_angry` | `prowl`/`windup` once two hits have landed | **B3/img12 top-right**: brows down, fangs, steam puffs at both ears |
| `boss_friends` | `friends` — the befriending beat | **B2/img9 bottom-right**: eyes closed, laughing, crest ring glowing |
| `boss_tell_open` | the flashing badge over his head | **B1/img5 cell 3** (burst star cloud) or the crest halo from B2/img9 — must read as a *different object* from the shielded badge, not a brighter one |
| `boss_tell_shielded` | the badge while he is closed | the plain crest sparkle, small and dull (B1/img3 portrait crest, desaturated) |

### Effects (replacing the code-drawn CPU particles)

| Slot | Source cell | Used at |
| --- | --- | --- |
| `fx_boss_burst` | B2/img6 bottom-left — big ring with a dark core and radiating streaks | the bonk landing |
| `fx_boss_ring` | B1/img1 bottom-right ground ring, or B1/img5 cell 4 | his landing shockwave on the deck |
| `fx_boss_puff` | B2/img6 bottom-right / B1/img5 cell 5 | takeoff, hops, and the shielded-tap poof |
| `fx_boss_sparkle` | B1/img5 cell 6 (lone four-point sparkle) | the shine returning at the win |
| `fx_boss_swoosh` | B1/img5 cell 2 (bunny inside a crescent swoosh) | the leap arc |

### Minions (not this encounter, but they arrived with it)

B1/img2, B2/img7 and B3/img11 are a **small** eared dust bunny in idle, hop and
trailing-dust frames. These are not Grand Puff — they belong to the Main Hall
colony (`CASTLE_DUST_BUNNY_AI_2026-08-02.md` is growing that hall a generated
colony right now) and would upgrade those cards from three static poses to a
hop cycle. Filed here so they are not lost.

### Not yet placed

- **B2/img8 and B1/img3** are portraits on a cream background — poster art, not
  runtime cutouts. Good for the storybook/menu, not for the arena.
- **B2/img10** is a rainbow-tinted Grand Puff on transparency. It is not in the
  fight's palette; it reads as a *shiny/rare* variant. Suggestion: hold it for a
  rare-encounter reskin or the befriended companion form, rather than spending
  it as a mood.
- **B2/img9 top-left / bottom-left** (smug, and laughing with the crest ring)
  are alternates for `boss_angry` and `boss_friends`.

---

## 3. Landing procedure (about ten minutes)

1. Chroma-key each sheet locally, crop the cells, resize to ≤1024, save as
   transparent PNG at the paths in §1.
2. Add one `ASSET_LICENSES.md` block covering the set.
3. Run the gate:
   ```
   godot --headless --path . --import
   godot --headless -s scripts/probe_dust_boss.gd -- --touch
   DUSTBOSS_SHOT_OUT=/tmp/dustshots LIBGL_ALWAYS_SOFTWARE=1 \
     xvfb-run -a godot --rendering-method mobile --resolution 1280x720 \
     -s scripts/probe_dust_boss_shots.gd
   ```
   The probe proves the map; the ten captured frames are the visual review.
4. Drop `BOSS_H` from its placeholder 16.0 toward ~12 once the real art carries
   its own mass, and re-shoot. The stage re-solves its own framing from
   `BOSS_H`, so nothing else needs touching.

**No code change is required to land the art.** That was the point of wiring
the pose contract first.

---

## 4. What the art does and does not fix

Fixes, from `CODEX_BOSS_ART_HANDOFF_2026-08-02.md`: §1 (one pose for three
moods) and most of §2 (the tell being the generic reward star) and §6 (nothing
in the fight is animated).

Still open after the art lands:

- **§3 pictograms** — nine voice events still have no audio, so the rule and
  both phase changes still reach a non-reader as text. The mood sheets help
  (dizzy and angry are now self-evident) but *"wait for the flash"* is not yet
  sayable without words.
- **§4 the arena** — the octagon is still cylinder-and-box primitives against a
  near-white void.
- **§5 the overlay** — the message banner still sits exactly where Roshan
  stands, so the hero is hidden in her own boss fight.
- **Everything in the stress-test audit** — mashing still equals reading, the
  encounter is still a ~30 s fixed-length ride, and the unattended fight still
  never ends. Art makes the fight legible; it does not make it a fight.
