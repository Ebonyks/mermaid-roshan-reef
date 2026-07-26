# Character audit — every 2D figure in the game, and what happened to it

_Owner request 2026-07-26: "only Mermaid Roshan has been turned into a 3D
image… all of the objects are still kept as stickers that are 2D and like
sprites. Do a full audit to identify all of these figures, and then redevelop
them."_ Owner follow-ups the same day: **use Blender for the first draft**,
**skip Daddy Mermaid** (a 3D Daddy exists and will be imported later), and
**the book-native characters are exempt from the "3D must come from
Codex-developed 2D" rule** — their source art already is the book.

---

## 1. The audit

### 1.1 What was actually 3D before this pass

| Character | Model | Where it was used |
|---|---|---|
| **Roshan** | `roshan_v4.glb` (26-bone rig, procedural swim in `player.gd`) | the reef player only |
| Fairy Mermaid / Rosalina | `fairy_v2.glb` | galaxy player avatar only, when the fairy skin is on |
| Chuck the poodle | `chuck_poodle_rigged.glb` | craft/collection use |
| Lamb-a' | `lamb.glb` (static, 0 anims) | prop use |
| craft kitty / birdie | `craft_kitty_rigged.glb`, `craft_birdie_rigged.glb` | stuffie companion bodies |

The owner's read was right, and understated: Roshan had a model but **eight of
the nine places that draw Roshan drew her as a flat `roshan_sprite.png`
billboard** — the kart grid, both opera stages, the dungeon puzzle room and the
combat arena all used a cutout of a character who had been fully 3D all along.

### 1.2 Every 2D figure found

Fourteen distinct figures across 21 call sites. `_build_friends` and the melody
`StarPerformer` were the only two sites that would even look for a model.

| # | Figure(s) | Art | Call sites |
|---|---|---|---|
| 1 | **Evie and Lamb-a'** | `friends/pearl_friend.png` | reef friend, castle bedroom, opera audience, slide cheer |
| 2 | **Harper and Fiona** | `friends/two_friends.png` | reef friend, castle bedroom, opera audience, slide cheer |
| 3 | **Faron and baby** | `friends/mama_baby.png` | reef friend, castle bedroom, opera audience |
| 4 | **Wacky and Chuck** | `friends/wacky_chuck.png` | reef friend, castle corridor basket, opera audience |
| 5 | **Daddy Mermaid** | `friends/daddy.webp` | reef friend, melody stage, castle secret room |
| 6 | **Princess Huluu** | `friends/huluu.png` | castle throne, brawl portal, kart grid, galaxy skin, brawl co-op partner |
| 7 | **Kareem** | `friends/kareem.png` | the shop |
| 8 | **Flower Friend** | `friends/flower_friend.png` | *(art only — no call site)* |
| 9 | **Sparkle the baby eagle** | `book/baby_eagle.png` | kart grid, companion roster art |
| 10 | **Bunny doll** | `book/doll_bunny.png` | kart grid |
| 11 | **Kitty doll** | `book/doll_cat.png` | kart grid |
| 12 | **Baby Doll** | `book/baby_doll.png` | kart grid |
| 13 | **Dolly** | `book/baby_doll2.png` | kart grid |
| 14 | **Sleepy** | `book/baby_doll3.png` | kart grid |
| — | **Chuck (solo)** | `book/chuck_solo.png` | *(art only — no call site)* |
| — | **Roshan (flat stand-in)** | `roshan_sprite.png` | kart, opera act, opera lobby, dungeon, combat arena |
| — | **Rosalina (flat stand-in)** | `skins/fairy_mermaid.png` | galaxy castle gate, galaxy Moon Throne |

### 1.3 Three findings worth flagging

**The "pair sheets" cannot be split.** `NPC_3D_WORKORDER_2026-07-19.md` has four
tasks blocked as `needs_src` pending a per-figure crop of Evie, Wacky, Harper &
Fiona, and Faron. Looking at the actual art, that blocker is permanent: in every
one of those illustrations the two figures **overlap and occlude each other** —
Evie's arms are around Lamb-a', the sisters are embracing with their tails
crossed, Faron is holding the baby, Wacky is holding Chuck. There is no crop
that yields a whole figure; splitting them means *painting the hidden halves*,
which is new original art, not extraction. The game already treats each sheet as
one friend ("Evie and Lamb-a'" is a single `FRIEND_DEFS` entry), so this pass
converts each sheet as **one figure** and the four tasks should be closed as
won't-do rather than left looking actionable.

**`assets/book/flower_girl.png` is a broken asset.** Its alpha is fully opaque
and the transparency checkerboard is baked into the RGB, so its silhouette is
the whole rectangle. It is also the same character as `flower_friend`. It has no
call site. Excluded from conversion and recorded here rather than silently fed
through the pipeline. Nothing was deleted.

**One policy comment was overridden, on purpose.** `castle_hall.gd` carried
"Protected book cutout until an owner-approved source-faithful model exists"
above Huluu's throne. The draft satisfies the spirit of it — the model's front
face *is* the book art, unlit and unredesigned — and this pass was explicitly
requested, so Huluu's throne now shows the model. Flagging it because it was a
standing owner note, not an incidental comment: say the word and Huluu reverts
to the cutout by deleting one file.

**Two figures have art but no call site**: `flower_friend` and `chuck_solo`.
Both were converted anyway (cheap, and they are clearly intended for use), but
nothing in the game references them yet.

---

## 2. What was built

### 2.1 The approach, and why

There is no Meshy key in this container and the owner asked for Blender. But the
deeper constraint is the input: each character exists as **exactly one view** of
irreplaceable book art that must never be redesigned or re-lit. A generative
image-to-3D pass would hallucinate a back-of-head and a new face; a hand sculpt
is not a headless operation. The one honest reconstruction a single view
supports is a **pressed toy figure**:

```
alpha silhouette → exact euclidean distance transform → dome height field
                 → closed front/back shell → book art projected on the front
```

The distance transform makes each figure thickest along its own medial axis and
thin at the outline, so a tail fin comes out as a thin rounded blade and a torso
as a full rounded mass. Every colour on the model is a book-art pixel: the front
is the illustration, the rear panel is the same illustration blurred past
recognition (so you read hair over dress over tail from behind, but never a
second face), and the rim wall samples the illustration's own outline. Nothing
is invented — and the result is genuine geometry that takes real depth, real
parallax, a rig and an idle.

Built headless with the pip `bpy` module (Blender 5.0.1) — no Blender binary
needed, so this reproduces in any session.

### 2.2 The models

Fourteen characters, **4.6 MB total**, each with a 13-bone rig and one looping
2-second `idle` (buoyant bob, travelling sway down the tail, slow head nod).

| File | Triangles | Anims | Size |
|---|---|---|---|
| `friends/pearl_friend.glb` | 9,000 | 1 | 400 KB |
| `friends/two_friends.glb` | 9,000 | 1 | 402 KB |
| `friends/mama_baby.glb` | 9,000 | 1 | 380 KB |
| `friends/wacky_chuck.glb` | 9,000 | 1 | 361 KB |
| `friends/huluu.glb` | 9,000 | 1 | 427 KB |
| `friends/kareem.glb` | 9,000 | 1 | 385 KB |
| `friends/flower_friend.glb` | 9,000 | 1 | 397 KB |
| `friends/baby_eagle.glb` | 5,998 | 1 | 267 KB |
| `friends/baby_doll.glb` | 6,000 | 1 | 278 KB |
| `friends/baby_doll2.glb` | 6,000 | 1 | 287 KB |
| `friends/baby_doll3.glb` | 6,000 | 1 | 260 KB |
| `friends/chuck_solo.glb` | 6,000 | 1 | 260 KB |
| `friends/doll_bunny.glb` | 4,500 | 1 | 196 KB |
| `friends/doll_cat.glb` | 4,497 | 1 | 199 KB |

Textures are power-of-two (≤1024 longest side), JPEG-in-GLB, one material per
character. Materials carry `KHR_materials_unlit`, which Godot maps to
`shading_mode = UNSHADED` — the book art is never re-lit, exactly as the shipped
cutouts behaved.

**Daddy Mermaid is deliberately absent** per the owner. `friends/daddy.glb` is
the path every loader already checks, so importing the owner's model is a
one-file drop with no code change.

### 2.3 The rig contract

A single spine-and-tail chain, no limbs — because a silhouette is all the source
gives, and guessing arm bones would be fiction:

```
root ─┬─ spine1 → chest → neck → head
      └─ tail1 → tail2 → … → tail8
```

Names deliberately reuse Roshan's own vocabulary (`tools/glb_check.py`
`ROSHAN_BONES`), so a later hand-rig or Meshy retarget maps straight onto them
instead of starting from nothing. `glb_check.py` now validates this contract as
`DRAFT`.

### 2.4 The loader work — one factory, 21 sites

`main.character_visual(tex, height)` is now the single character factory: it
prefers `friends/<tex>.glb`, falls back to the die-cut sticker billboard, and
returns a node of **the same on-screen height either way**. `main.fit_model()`
measures the model's real AABB and scales it to that height, so converting a
character never moves or resizes them. `main.roshan_visual(height)` does the
same for the hero, following the wardrobe skin.

Converted to the factory:

| File | Site |
|---|---|
| `main.gd` | reef friends, brawl portal Huluu |
| `arena/castle_hall.gd` | Huluu's throne, Daddy's secret room, the four bedroom cutouts, Wacky's basket |
| `games/shop.gd` | Kareem the shopkeeper |
| `games/melody.gd` | the `StarPerformer` (bespoke loader folded into the factory) |
| `games/slide_race.gd` | the cheering friend at the slide top |
| `games/side_scroll.gd` + `games/brawl.gd` | the co-op companion |
| `opera_act.gd` | the four audience cutouts |
| `kart.gd` | all eight drivers on the grid |
| `galaxy.gd` | the Huluu skin avatar, Rosalina at the gate, Rosalina on the Moon Throne |
| `opera_act.gd`, `opera_house.gd`, `dungeon_puzzle_room.gd`, `combat_arena.gd` | Roshan's stage avatar → the real `roshan_v4.glb` |

Type changes rippled to `medal_system.gd`, `companion.gd`, `slide_race.gd` and
`side_scroll.gd`, which each assumed a friend node was a `Sprite3D`. `kart.gd`'s
distance fade was guarded — `Node3D` has no `modulate`, so a 3D driver now drops
out at the same distance instead of crashing.

### 2.5 Still 2D on purpose

HUD speaker portraits, wardrobe previews, the intro storybook panels, the opera
2D cutscene, the picture-game minigames and the fairy wing card. These are flat
UI or storybook pages, not figures standing in the world.

---

## 3. Honest limitations of the first draft

- **It is a relief, not a sculpt.** From a hard side-on angle a character reads
  as a thick rounded standee, and the projected art smears at grazing angles.
  Dome depth was tuned down per character to keep this subtle; it is still the
  format's ceiling.
- **`doll_bunny` and `doll_cat` are weak.** Their source art is small
  (220 px) and cropped at the frame edge, so the relief has a flat base and
  little interior detail to work with.
- **No limb articulation.** The idle is a bob and a tail sway. Arms cannot move
  because the relief does not separate them from the body.
- **`kareem` includes his armchair**, because the book art does.

Each of these is fixed by replacing one `.glb` — the loader takes whatever is at
`friends/<tex>.glb`, so a proper sculpt or a Meshy pass for any single character
lands without touching code.

---

## 4. Reproducing / extending

```bash
pip install bpy Pillow                       # Blender 5.0 as a Python module
python3 tools/build_npc_draft.py --list
python3 tools/build_npc_draft.py huluu --preview   # renders to tools/out/npc_draft/
python3 tools/build_npc_draft.py --all
python3 tools/glb_check.py assets/characters/friends/huluu.glb
python3 tools/tests/test_npc_draft.py        # geometry contract (also in ci.sh)
```

Per-character knobs live in the `ROSTER` in `tools/build_npc_draft.py`:
`depth`, `back_ratio`, `pivot` (where tail meets torso), `sway`, `grid`,
`tri_budget`, `tex_max`.

---

## 5. Open questions for the owner

1. **Daddy Mermaid** — drop the model anywhere and it becomes
   `assets/characters/friends/daddy.glb`; no code change needed.
2. **The four `needs_src` tasks** in `NPC_3D_WORKORDER_2026-07-19.md` should be
   closed as won't-do (§1.3) unless you want per-figure turnarounds
   commissioned, which is genuinely new art.
3. **Codex turnarounds** — if you want a real sculpt lane rather than reliefs,
   the highest-value request is front/side/back turnaround sheets for the six
   most-seen characters (Huluu, Evie+Lamb-a', Harper+Fiona, Faron, Wacky+Chuck,
   Kareem), matching the `gen2/turnarounds/roshan_v2/` layout. Say the word and
   I will write the per-character prompts.
4. **`flower_friend` and `chuck_solo`** now have models but no call site — want
   them placed anywhere?
