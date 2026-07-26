# CODEX REQUEST — full-cast 2D character turnarounds (one continuous set)

_Owner directive 2026-07-26: "have them generate all objects in new, unique form
for continuity rather than combining codex and nano banana assets."_

**Read this whole file before generating anything.** It is a request for one
self-contained batch, not a list of gap-fills.

---

## 1. Why this batch exists

Every 3D character source in this repo today came from the **nano banana lane**
(`tools/gen2_turnaround.py`, `models/gemini-3-pro-image`) or from mechanical
processing of the book art. The remaining 3D work needs more 2D views than
exist. Patching those gaps with Codex output would leave the cast half
nano-banana and half Codex — two generators' hands on one family of characters,
visible as drifting faces, line weights and palettes between figures standing
next to each other in the same scene.

So: **Codex generates the entire cast fresh, in one pass, as one continuous
set.** Nothing in this batch composites, traces, upscales, or extends a
nano-banana image. The existing art is *reference only*.

### The one thing that must not drift

"New, unique form" means **newly drawn in a single unified style** — it does
**not** mean new characters. These are one specific family, drawn for one
specific four-year-old. Every figure must remain unmistakably the same person,
pet or toy as the book art:

- same face, hair colour and hairstyle
- same tail/outfit colours and markings
- same age read and body proportions
- same recognisable likeness a parent would nod at

Only the rendering hand changes. If a choice would trade likeness for style,
**keep the likeness.** `ART_STYLE_GUIDE.md` §"Source reference map" lists the
book pages to study per character; `assets/characters/friends/` and
`assets/book/` hold the protected originals. Study them, never edit them.

---

## 2. What to deliver

**Three views per character**, matching the pipeline's existing multi-view
contract (`gen2/turnarounds/<role>/`):

| View | Camera |
|---|---|
| `front` | straight on, facing the viewer, body symmetrical, **arms and tail/limbs clearly separated from the torso** |
| `side` | direct left profile, fully flat |
| `back` | directly from behind, same pose |

The front view's limb separation is load-bearing: every auto-rig attempt so far
was rejected at pose estimation because limbs were fused into the silhouette.

**One figure per image.** Never draw two characters in one frame — see §4.

### Technical delivery contract

| Property | Requirement |
|---|---|
| Format | PNG |
| Size | ≥1024 px on the longest side; **1536 preferred** (we downsample; we cannot invent detail) |
| Background | **solid, flat `#FF00FF` magenta**, no gradient, no texture, no vignette |
| Framing | whole figure in frame, centred, ≥6% padding on every side — the figure must **never touch the frame edge** |
| Forbidden | ground shadow, cast shadow, drop shadow, text, watermark, signature, sparkles, bubbles, props not named in the row, background scenery, borders, frames |
| Pose | neutral and relaxed, identical across all three views of a character |
| Line | crisp dark navy-purple contour, consistent weight across the whole batch |

**On the magenta key:** intake uses
`tools/extract_connected_chroma.py`, which removes only *border-connected* key
pixels — so a rose or pink inside the figure survives even if it reads close to
the key. Still, keep rainbow gradients' pink band at ≤80% saturation so nothing
in the subject is fully saturated magenta. Do **not** use white: several figures
in this cast are white or near-white (Lamb-a', the baby, the dolls) and would
lose their silhouette.

### Filenames

```
gen2/codex_turnarounds/<role>/front.png
gen2/codex_turnarounds/<role>/side.png
gen2/codex_turnarounds/<role>/back.png
```

Use the exact `<role>` string from the tables in §3. A new directory
(`codex_turnarounds/`, not `turnarounds/`) keeps this set physically separate
from the nano-banana lane, so provenance stays auditable and neither set can be
silently mixed into the other.

---

## 3. The roster

20 characters × 3 views = **60 images**.

### Tier 1 — reef friends (most-seen; do these first)

| # | `<role>` | Character | Identity notes |
|---:|---|---|---|
| 1 | `evie` | Evie | mermaid girl, long brown hair, pink-and-gold scaled tail, striped sleeve top |
| 2 | `lamba` | Lamb-a' | pale blue-white fluffy plush lamb, small, round, friendly |
| 3 | `harper` | Harper | younger mermaid sister, blonde, flower crown, pale ruffled top, peach-gold tail |
| 4 | `fiona` | Fiona | older mermaid sister, brown wavy hair, coral-orange top, orange-gold tail |
| 5 | `faron` | Faron | mermaid woman, honey-blonde wavy hair, deep maroon dress, maroon flowing tail |
| 6 | `faron_baby` | Faron's baby | infant in a pale knitted romper with a soft bonnet |
| 7 | `wacky` | Wacky | grandfather merman, silver hair, glasses-free, green jacket, olive-green scaled tail |
| 8 | `chuck` | Chuck | small black poodle, curly coat, red collar |

### Tier 2 — story NPCs

| # | `<role>` | Character | Identity notes |
|---:|---|---|---|
| 9 | `huluu` | Princess Huluu | mermaid princess, blonde, pink petal-layered bodice, pink-and-gold tail, crown/headpiece |
| 10 | `kareem` | Kareem | boy, short brown hair, grey-and-white striped long-sleeve shirt. **Draw him standing, no armchair** — the chair in the book art is scenery and must not become part of the model |
| 11 | `flower_friend` | Flower Friend | mermaid girl, long brown hair with rainbow strands, pink top, rainbow scaled tail, holds a round multicolour flower |
| 12 | `daddy` | Daddy Mermaid | merman king, long brown hair, gold crown, navy-and-gold tunic, teal cape, rainbow tail. **See §5 — generate only if the owner confirms** |

### Tier 3 — toys and the kart grid

| # | `<role>` | Character | Identity notes |
|---:|---|---|---|
| 13 | `sparkle` | Sparkle the baby eagle | plush bird, mint-and-pink pastel body, pink wing, large friendly eyes, small bow on the head |
| 14 | `doll_bunny` | Bunny doll | plush rabbit, dusty-rose body, long floppy ears, simple dot eyes |
| 15 | `doll_cat` | Kitty doll | round squishy plush cat, grey tabby, pale blue belly patch |
| 16 | `baby_doll` | Baby Doll | baby doll, bald, pink romper with a panda motif, jointed limbs |
| 17 | `baby_doll2` | Dolly | baby doll, wispy blonde hair, lilac-and-white layered dress |
| 18 | `baby_doll3` | Sleepy | baby doll, soft beige sleepsuit with a bow, calm closed-mouth expression |

### Tier 0 — the hero pair (owner decision, see §5)

| # | `<role>` | Character | Identity notes |
|---:|---|---|---|
| 19 | `roshan` | Mermaid Roshan | brown hair with a **rainbow forelock**, rainbow-and-lavender scaled tail. The title character — the single most important likeness in the project |
| 20 | `rosalina` | Fairy Mermaid (Rosalina) | Roshan's fairy skin: same face, plus large rainbow butterfly wings and a tiara |

---

## 4. Draw every figure separately — this is the point

Four of the book illustrations show **two figures embracing**: Evie hugging
Lamb-a', Harper and Fiona with their tails crossed, Faron holding her baby, and
Wacky holding Chuck. Because they overlap and occlude one another, no crop of
those images yields a whole figure, which is why the four `needs_src` tasks in
`NPC_3D_WORKORDER_2026-07-19.md` have been permanently blocked (full reasoning
in `CHARACTER_2D_AUDIT_2026-07-26.md` §1.3).

**This batch is what unblocks them.** Drawing Evie alone, complete and
unoccluded, is authored art — legitimate here, and something no automated crop
could ever produce. So:

- one figure per image, complete anatomy, nothing hidden behind another body
- no hugging, holding, carrying or overlapping poses
- Lamb-a', the baby and Chuck are each their **own** character with their own
  three views, not an accessory attached to someone else
- do **not** also deliver combined pair sheets — the game composes the pairs at
  runtime from the individual models

---

## 5. Two decisions the owner must make before generating

**Daddy Mermaid (`daddy`, row 12).** The owner has an existing 3D Daddy waiting
to be imported and asked for no draft effort on him (2026-07-26). If that model
came from the nano-banana lane, continuity argues for regenerating him here; if
it is already stylistically consistent with this batch, skip row 12. **Ask
before generating.** Skipping it does not block any other row.

**Roshan and Rosalina (rows 19–20).** Roshan already ships as `roshan_v4.glb`: a
26-bone rig driven by a bespoke procedural swim in `scripts/player.gd`. A new
Roshan means a mesh retarget onto that existing armature (the
`tools/roshan_v2_retarget.py` lane), not a drop-in replacement — real work, and
it touches the most-loved asset in the project.

The honest trade: **leaving Roshan out is exactly the mixed-provenance problem
this batch exists to solve** — she stands beside these characters in almost
every scene, so if anyone drifts it will be most visible on her. Including her
is the consistent choice; skipping her is the safe one. Rows 1–18 are
independent either way, so this decision can be deferred without holding up the
batch.

---

## 6. Shared prompt contract

One separate image-generation call per image (60 calls). Paste the block below,
substituting `{VIEW}`, `{CHARACTER}` and `{IDENTITY}` from §3, and attach the
character's book art from `assets/characters/friends/` or `assets/book/` as the
likeness reference.

> Single isolated children's storybook character turnaround view for a video
> game, drawn in modern flat-colour anime with soft storybook painting: rounded
> cel-shaded forms, painted pastel skin and fabric, crisp dark navy-purple
> contour of even weight, aqua and lavender shadow accents, high-key and
> emotionally warm. No photorealism, no gritty texture, no painterly volume.
>
> Subject: {CHARACTER} — {IDENTITY}. Match the attached reference art's
> likeness exactly: same face, same hair colour and style, same outfit and tail
> colours, same age and proportions. Only the drawing style and camera change.
>
> Camera: the character seen {VIEW}. Neutral relaxed standing/floating pose,
> arms held slightly away from the body, tail or legs clearly separated from
> the torso so the full silhouette reads.
>
> ONE character only, alone in frame, complete anatomy, nothing cropped,
> centred with generous padding, never touching the frame edge. Perfectly flat
> solid #FF00FF magenta background with no gradient or texture, and no fully
> saturated magenta anywhere on the character. No ground shadow, no cast
> shadow, no text, no watermark, no signature, no sparkles, no bubbles, no
> props, no scenery, no border.

`{VIEW}` strings:

- `front` → "directly from the FRONT, facing the viewer straight on, body symmetrical"
- `side` → "in a direct LEFT SIDE view, a full flat profile"
- `back` → "directly from BEHIND, facing away from the viewer"

**Consistency across the batch matters as much as any single image.** Generate a
character's three views in one session so they agree with each other, and keep
line weight, palette temperature and shading softness identical from row 1 to
row 20. If a later row drifts from an earlier one, regenerate the later one.

---

## 7. Intake (what happens after delivery)

```bash
# 1. key out the magenta (border-connected only, so interior pinks survive),
#    tight-cropped with padding. Args are positional: input then output.
for r in gen2/codex_turnarounds/*/; do
  for v in front side back; do
    python3 tools/extract_connected_chroma.py "$r$v.png" "$r${v}_rgba.png" \
      --key '#ff00ff' --threshold 60 --crop --padding 8
  done
done

# 2. first-draft relief models from the new front views. Each ROSTER row in
#    tools/build_npc_draft.py needs its `source` repointed at the keyed
#    front_rgba.png (one line per row) — the builder does not pick up a new
#    directory on its own.
python3 tools/build_npc_draft.py --all --preview
python3 tools/glb_check.py assets/characters/friends/<role>.glb

# 3. or the sculpt lane, once a Meshy key exists — the three views feed
#    multi-image-to-3d, which is what stops it hallucinating the far side
python3 tools/meshy_pipeline.py launch
```

The individual-figure delivery also needs a small runtime change: the reef
friend entries are pairs (`pearl_friend` = Evie + Lamb-a'), so
`main.character_visual()` gains a composed-pair path that parents two models
under one holder. Not Codex's problem — noted here so the dependency is visible.

Then: an `ASSET_LICENSES.md` row per new file in the same commit, and the probe
suite green on CI before anything merges.

### Acceptance checks

A row is accepted only when all of these hold:

1. Three views present, same character, same pose, mutually consistent.
2. Likeness a parent would recognise without being told who it is.
3. Background keys out cleanly to a tight silhouette with no magenta fringe and
   no holes punched in the character.
4. Front view's limbs and tail read as separate from the torso.
5. Longest side ≥1024 px.
6. Style indistinguishable from the other 19 rows.
7. Exactly one figure, complete, unoccluded.

Reject and regenerate on: a fused silhouette, a drifted face, a second figure, a
prop or shadow that was not asked for, or a frame-touching crop.

---

## 8. Scope boundaries

- **Nothing in `assets/` is edited by this batch.** The book art and the family
  voices are protected source; this produces new files in
  `gen2/codex_turnarounds/` only.
- **Gabby is excluded** — removed 2026-07-19 on an IP hold, assets parked in
  `attic/gabby/`. Do not generate, stage or reintroduce her.
- **No Zelda / Wind Waker assets, symbols, UI, music or character designs.**
  Wind Waker is a rendering reference for cel shading only.
- **Environments, props and textures are out of scope.** Characters only; the
  world has its own pipeline (`ART_STYLE_GUIDE.md`, the `gen2` prop lane).
- `assets/book/flower_girl.png` is a **broken duplicate** of the Flower Friend
  (opaque alpha, checkerboard baked into the RGB). Use
  `assets/characters/friends/flower_friend.png` as the reference for row 11 and
  ignore `flower_girl.png` entirely.
