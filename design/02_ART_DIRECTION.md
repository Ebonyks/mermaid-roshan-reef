# Master design — art direction

_Consolidated 2026-08-02 and authority-reconciled 2026-08-09 from
ART_STYLE_GUIDE, ART_SCORING_GOVERNANCE_2026-07-18,
LIVING_CARD_DESIGN_LANGUAGE_2026-07-29, GAME_REDESIGN_2P5D_2026-07-27,
CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27, CEL_SHADING, the 24-document
ART_*/audit chain, the Sky Lagoon, Castle, Opera, Ember and Northern art
audits, VISUAL_DESIGN_AUDIT_2026-07-28, and the cinematic protocol pair
under `docs/`, plus the 2026-08-09 Opera animation, Ballerina and Boxer
reconciliations._

---

## 1. The promise

Mermaid Roshan's storybook, rendered as a **pastel toy playset**: rounded
geometry, broad painted colour blocks, navy/purple ink contours, aqua and
lavender shadows, graphic water, oversized child-readable props. Wind Waker is
a **rendering reference only** — no Zelda assets, symbols, UI, music or
character designs, ever.

The primary visual authority is the owner's book,
`Mermaid_Roshan_INTERIOR_A5.pdf` (original family artwork, © Mermaid Roshan
LLC, not redistributed). `ART_STYLE_GUIDE.md` remains authoritative for the
full shape / line / value / colour language and its sampled palette; it is too
detailed to fold in here and is still correct.

Condensed DNA:

- **Shape** — broad, rounded, slightly asymmetrical masses; the real object's
  silhouette survives stylization; exaggerate whatever explains an object's
  play value; detail grouped into two or three calm clusters, never spread
  evenly.
- **Line** — one clean confident contour, 2–4 screen px at 1280×720 for major
  silhouettes, 1–2 px interior. Deep indigo / plum / warm brown-black, related
  to the local material. No hatching, speed lines, distressed edges or white
  sticker rims.
- **Value** — high-key. Faces, hands and objective props never fall into a
  dark mass. Three value families; shadows aqua / blue-grey / lavender, never
  neutral black. Never bake dramatic lighting, vignette or crushed AO into a
  reusable texture.
- **Colour** — cool water colours occupy ~⅔ of an environment; warm rainbow
  colours identify characters, rewards and touch targets. Saturation peaks in
  small focal zones. No neon fields, no one-note all-blue scenes.

### The readability rule that outranks beauty

**Backgrounds frame; they never compete with the things a finger should find.**
The play band stays calmer than characters and tap targets, and the actionable
object must survive a phone-size squint test with the HUD present. The old
source-file mean-saturation/luminance comparison is only a diagnostic: it
equally weights mutually exclusive frames and decorative files and ignores the
rendered composite. It cannot by itself authorize recolouring or regeneration.
`MA-VIS-003`/`MA-VIS-004` require commit-pinned, state-local Canvas + HUD +
viewport evidence and runtime/device review. Fairy is likely a false positive;
Lagoon remains an unconfirmed hierarchy risk.

---

## 2. The medium — true-2D living cards (binding)

**Owner direction 2026-08-09:** the final game is true Canvas/Node2D 2D
game-wide. Codex-painted flats and approved illustrated cutouts remain the
primary art channel, but they are staged through `Node2D`, `CanvasItem`,
`Sprite2D`, `TextureRect`, `Camera2D`, 2D particles and explicit 2D ordering.
A flat image on `Sprite3D` is migration debt, not a final living card.

The Sprite3D structural prescription in
`LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` is `SUPERSEDED` for runtime
structure. Its durable art lessons survive: independently owned cards, stable
pivots, declared motion/intensity, restrained motion budgets, measured touch
footprints, unique source-pixel ownership, and explicit background/playable/
foreground roles.

Every animated card keeps a stable 2D anchor and named ordering/parallax role.
A grounded card uses a bottom-center pivot and a restrained `Sprite2D`/Canvas
contact shadow; non-grounded ornaments declare their semantic anchor (a
chimney mouth, for example). **The crop is the rig** means stable authored
pixel ownership, never permission to introduce a character skeleton or mesh.

### Two valid art lanes — and the rule that separates them

1. **Extraction lane.** Preserve the exact approved object pixels: remove them
   from a preserved master copy, heal only inside a declared mask, verify zero
   out-of-mask pixel change, re-slice without scaling, reinsert the original
   cutout at its owned `z_index`/parallax role.
2. **Ornament lane.** Generate a genuinely new object that does not duplicate a
   painted silhouette — smoke, a glint, a drifting leaf.

**Never paste a second tree, cabin, flower bank or prop over its painted
copy.** If the source master hash or the approved extraction bounds do not
match the working master, stop the extraction rather than guess.

The same rule governs multi-tile backgrounds: do not independently regenerate
an object across tile boundaries. If a readable object sits ambiguously
between two panels, remove it from the background, extract that same approved
artwork as a Canvas card, heal behind it, and reinsert it **once** at its
intentional 2D layer. Tiles must join seam-free before separated cards are
added.

### Motion hierarchy

- **Ambient** establishes weather and depth: restrained far-foliage sway, one
  clear-corridor cloud, thin chimney smoke.
- **Reactive** acknowledges Roshan only when an approved foreground/play-band card
  already exists, and never moves collision or touch bounds.
- **Authored staging** owns the strongest timing: a plane arriving, equipment
  playing, a castle inviting.

Budget per playable screen: **at most one dominant moving landmark plus three
quiet support loops.** Staggered cards forming one smoke column count as one
loop. The walk lane and touch targets stay calm. One bounded 2D stage tick owns
all ambient cards, performs no random calls, allocates no per-frame
collections, and clears its state on teardown.

Capabilities are conditional, not decoration quotas. Do not add a sway shader,
reactive foliage, a second cloud, glints or leaves merely to satisfy a list.

---

### Current character-animation authority

The merged Opera delivery contains 13 runtime costume atlases, each a 4×4
1024×1024 sheet with 256 px cells: **208 reviewed frames** in total. Native,
alpha-derived, pack and runtime hashes plus identity, costume, tail topology,
padding and prop-attachment review live in the tracked animation evidence;
`python tools/audit_opera_roshan_animation.py` is the blocking deterministic
gate. Passing that gate proves the recorded delivery contract, not owner 5/5
acceptance or phone-size readability.

`assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png` is the
current Ballerina atlas (SHA-256
`c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995`). It
supersedes every earlier Ballerina sheet or recommendation. Its cells are pose
keys, not smooth temporal in-betweens: audited adjacent-pose silhouette changes
of 41.6–47.3% make a looping row unacceptable. Runtime holds the chosen ballet
pose and plays the curtain call once, then holds its final frame. The binding
details are in `BALLERINA_PARTY_REBUILD_2026-08-09.md`; older Ballerina sections
in the Opera quality documents cannot restore the four-pad phrase, generic
crank or old animation playback.

Boxer similarly ships through its illustrated actor/rival frames and dedicated
Canvas surface. The three retained Boxer GLBs
(`opera_boxer_outfit.glb`, `opera_boxer_dressing.glb`, and
`opera_rival_boxer.glb`) are measured removal debt under `MA-2D-002`, not an
approved fallback, staging intermediate, or resource library for the 2D game.
A separate Boxer V2 branch currently adds documentation only; it has not
replaced this integrated art/runtime authority. Painter-purpose and Arborist
worktrees are uncommitted candidates, so their edited/generated art is not part
of the current accepted runtime roster. Candymaker's current illustrated art
and phone-safe pour are integrated. Branch or worktree presence alone never
grants source, runtime, device, or owner acceptance.

`assets_src/imagegen/opera_roshan_animation_2026-08-09/PROMPTS.md` and
`assets_src/imagegen/opera_minigame_quality_2026-08-09/REVIEW.md` record
generation/derivation provenance. A prompt, review sheet, or source hash never
overrules runtime-context review, the later specialist documents, device
evidence, or explicit owner acceptance.

Seek has an equally explicit bounded override. Its current Canvas meadow uses
frame-animated Roshan, Evie and Lamb-a' actors, four large routed tree targets,
and fourteen high-grade environment/actor nodes. The vinyl
`assets/characters/stickers/pearl_friend.png` pair card, `assets/mg/k_bush2.png`
preview draft and transform-only sticker wobble are **superseded for Seek**;
they may not be restored as its active characters or environment. Four former
meadow GLBs were byte-verified on the deprecated-resources branch before
retirement. The protected Evie/Lamb-a' reference pixels remain untouched, and
the missing exact Evie “tap the wiggly tree” recording remains separately open
under `MA-ACCESS-003`.

---

## 3. Technical art gates (hard limits)

| Gate | Rule |
|---|---|
| Renderer | **Mobile on every platform** (owner 2026-07-11). Forward+-only effects stay dormant behind a rendering-method guard. |
| Canvas | 1280×720 base, `canvas_items` / `expand`, landscape |
| Texture size | ≤1024 px longest side **or** power-of-two. VRAM compress only if POT. |
| Generated ornaments | normally ≤256 px |
| Import | Fix Alpha Border + mipmaps on; NPOT uses lossless compression mode |
| ⚠ Deadlock | NPOT + `compress/mode=2` hangs the headless importer at 0 % CPU |
| Background resolution | **≥2048×2048 native coverage per playable screen**, measured per screen, not across the panorama. A 3×1 stage therefore needs a ≥6144×2048 master, reconstructed as a 6×2 grid of non-overlapping 1024×1024 `Sprite2D` cards. A 2048-wide three-screen panorama is reference-only. |
| Overdraw | ≤8 cards individually covering >10 % of screen; ≤150 % cumulative transparent coverage |
| Ambient tick | <1 ms/frame on the Speedy proxy |
| Lights | Do not add 3D lights; existing OmniLights are measured migration debt to remove while preserving composition and the Speedy-tier budget |
| Audio | OGG, music ≥64 kbps, loop-tagged |
| Day/night | Day and night builds share 2D card placement and phase signatures; backdrop and foreground cards get coordinated night tint |
| Licensing | Every new asset gets an `ASSET_LICENSES.md` line (source, license, URL, modifications) **in the same commit** |

---

## 4. Quality governance — what a score means

**Owner amendment 2026-07-18** (`ART_SCORING_GOVERNANCE_2026-07-18.md`),
superseding the earlier "book art = automatic 5/5" clause:

- **5/5** — the asset survived the full stress-test loop: representative near,
  mid and gameplay-distance Mobile-renderer captures, with visual rejection
  iterations until clean, **and explicit owner acceptance**. Applies uniformly,
  including to book-derived assets.
- **4/5 and below** — the 2026-07-16 rubric, including its hard caps: no
  runtime captures → cap 2; primitive focal object → cap 1.
- **No score is granted for provenance.** Book fidelity as a quality *ceiling*
  is retired; book art as *identity* is not.
- An agent may rate a candidate 4/5. **Only the owner awards 5/5.**

Later passes have set stricter local floors — the Northern Kingdom rebuild
used a 4.9 ceiling with a 4.5 release floor; the castle item pass uses a 4.5
eligibility gate. Those are per-pass tightenings of the same scale, not new
scales.

### Art reuse and generation budget (owner decision 2026-07-28)

**The project is in art finalization, not open-ended redesign.**

- Inventory existing assets and source masters before generating anything.
- Prefer direct reuse, shared components, or non-destructive derived variants.
- **Do not regenerate or redesign approved art for novelty, preference or
  stylistic exploration.** Keep established character and environment designs
  stable while the artistic design is being finalized.
- Generate only when no reusable asset exists or reuse would materially fail
  the purpose. Record the specific gap in the commit and limit generation to it.
- Reuse never permits destructive edits to protected originals, licence
  violations, or bypassing asset constraints. Derived variants live at new
  paths with source attribution preserved.

---

## 5. Protected content (never modify)

Irreplaceable, never modified, recompressed destructively or substituted
without being asked:

- `assets/book/` — scanned book art
- `assets/audio/voices/` — recorded family voices
- `assets/characters/friends/` — friend and family portraits

They remain the identity reference. Roshan's anchors: chestnut hair,
front-left rainbow forelock, lavender clothing, green-right / pink-left tail.
Likeness and established costume are not optional decoration — never average a
face into a generic style, change skin tone, alter age, or redesign
proportions without approval.

`attic/gabby/` holds the removed Gabby assets under an IP hold. Preserved, not
reintroduced.

---

## 6. Pipeline status — what channel art comes from now

| Channel | Lifecycle / status 2026-08-09 |
|---|---|
| **Codex-painted 2D flats / Canvas cards** | **PRIMARY**; reuse approved work before generating a named gap |
| Illustrated character cutouts | **FINAL MEDIUM.** `Node2D`/`Sprite2D`, unshaded authored contours, restrained 2D idle motion/contact shadow/sparkles; never relit or redesigned to imitate a mesh |
| Opera costume atlases | **CURRENT 2D DELIVERY.** Thirteen hash-audited 4×4 sheets; Ballerina uses held pose keys and a one-shot curtain call. Earlier sheets remain rejected provenance, never fallback |
| gen2 Meshy / any 3D character migration | `SUPERSEDED`; removed, not paused. Work orders are history and landed models are removal debt, never fallback |
| Deterministic Blender/3D kits | `SUPERSEDED` as runtime direction; remaining reachable resources are exact shrinking debt, retired resources live only on the archive branch |
| CC0 imports (Tiny Treats, KayKit, Quaternius, Kenney, curated OpenGameArt) | Legacy. The broad replacement campaign is `DEFERRED_WITH_REASON`; repair named live defects individually, preserving provenance and deleting an old file only after its replacement/non-reachability proof is green. No speculative mass redesign. |
| Nano-banana / AI Studio texture generation | Historical; superseded by the flats pipeline |

The authority files were reconciled on 2026-08-09. Older 2.5D/3D documents
retain explicit historical or superseded labels in the ledger.

### Approaches already tried and rejected — do not repeat

| Rejected | Why | Recorded in |
|---|---|---|
| Procedural Blender PNW trees for Sky Lagoon | Built meshes before any approved 2D art direction; repeated crown blobs, mechanical branch scaffolds | SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21 |
| Codex-authored procedural Ember Fortress meshes | Same failure: meshes before an approved 2D design stage | EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22 |
| Realistic botanical reference sheets | Wrong family; not the storybook register | SKY_LAGOON_PNW_* |
| Doorway-vignette Main Hall composition | Mixed props from seven room sets into the hub | FABLE_CASTLE_MAIN_HALL_PROP_COMPATIBILITY_AUDIT_2026-07-28 |
| Downscaled 1024×341 runtime panorama | Violates the per-screen native resolution rule | SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27 |
| Whole-card bounce / spin / hover interaction FX | Reads as UI, not as the world; interactions must change a meaningful part of a prop while the card pivot stays fixed | CASTLE_INTERACTION_AUDIT_2026-08-01 |

**The generalized lesson, paid for twice:** source facts and green technical
gates cannot substitute for approved art direction. The final runtime medium
is 2D; do not start mesh construction at all.

---

## 7. Cinematics — the absolute rule

**Owner decision 2026-07-29, and it supersedes the reuse budget above.**
Authored cinematic delivery frames MUST be complete, flattened images produced
in the current approved Codex image-generation style. The quality problem is
the frame audit and regeneration process; it must never be worked around by
substituting a different production technique.

Forbidden in any delivery or review frame: tweening, morphing, optical-flow or
motion interpolation, cross-dissolving, sprite/cutout animation, chroma-key
compositing, skeletal or rig animation, procedural warping, translating a
static layer or camera, or duplicating a frame to conceal missing action —
**even if the transition metrics look smooth.**

- Repair subject drift frame by frame; regenerate each failed frame at its
  exact timeline index as a complete image.
- An intentional hold is allowed only when the direction brief calls for
  stillness, and the manifest must name the span and its narrative purpose.
- A neutral-field `POSITION_GUIDE_ONLY` composite may communicate position,
  bounding box, scale and orientation only. No guide pixel may reach a
  delivered frame. Guides live outside runtime `assets/`.
- Every regenerated frame records timeline index, candidate path and hash,
  accepted neighbour hashes, prompt hash, attempt number, method, declared
  action/hold state, subject geometry, guide metadata and human identity /
  topology / style review. `tools/audit_cinematic.py` is the blocking
  validator.

Full protocol: `docs/CINEMATIC_DIRECTION_AND_INTENT_PROTOCOL.md` (what the
audience should feel) and
`docs/TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md` (did the
finished work read as deliberate animation).

---

## 8. Art review — how a pass is accepted

1. **Inventory first.** Name every affected runtime role and its current
   score. Machine-readable ledgers live in `audit/*.csv`.
2. **Construct in the final medium.** Inventory approved 2D art, then build the
   Canvas/Node2D role; no model or spatial staging is an accepted intermediate.
3. **Runtime evidence, not isolated renders.** Near / mid / gameplay-distance
   captures under the Mobile renderer at 1280×720, Speedy tier.
4. **Deterministic gates where they exist** — `audit_visual_design.py`,
   `audit_scene_congruency.py`, `audit_castle_card_alpha.py`,
   `audit_castle_interactions.py`, `audit_fairy_art_v2.py`,
   `prepare_opera_minigame_art.py --check-only`,
   `audit_opera_roshan_animation.py`, and `audit_cinematic.py`. All but the
   visual-design audit are hard CI gates at the synchronized audit snapshot;
   the visual-design result remains unsatisfied with explicit
   review/manual/coverage gaps (`MA-VIS-006`).
5. **Licence line in the same commit.**
6. **The human pass no tool can do:** no words / letters / digits in world
   art, nothing frightening at child eye level, and the M11 squint test —
   every interactive socket still findable when you squint at the phone.
7. **Owner acceptance for 5/5.** Nothing else grants it.
