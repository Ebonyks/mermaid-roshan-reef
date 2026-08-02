# Opera Codex Regeneration Requests — 2026-08-01

Definitive handoff for regenerating flawed opera codex art and generating the
missing assets the rebuilt career acts load. Written for a codex agent with no
other context: every request below is self-contained.

- **Serves:** `OPERA_2D_REBUILD_2026-08-01.md` (five-beat arc: imp scuffle →
  learn → do → captain steals the goal prop → dressed-rival stage finale).
  Architecture authority above it: `OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md`
  (2D lobby, OperaCareerWorld2D, hidden rival until the finale, three separate
  friendly 3D floor-boss finales). Hard rules above everything: `AGENTS.md`.
- **All paths in this document are repository-relative** to the game repo root
  (the folder containing `AGENTS.md`). Never use worktree or chat-cache paths.
- **Source of findings:** the 2026-08-01 per-career visual audit of the full
  codex package (36 flat sheets / 576 cards, 24 2.5D images, 12 finale keys,
  24 actor sprites, opera_house_flat 13 sheets / 172 cards), with the two
  corrections below applied.

## Corrections applied to the audit — read before acting

### A. Spurious finding discarded: Roshan's skin tone

The audit prompt misspecified the heroine and flagged "light/fair skin instead
of brown" as a blocker/major in every career. **This finding is discarded in
full.** Canonical Roshan (per the canonical book references) is a
**light-skinned mermaid girl with warm brown eyes, light-brown wavy hair with a
vivid rainbow streak, and a rainbow-scaled tail**. The codex art renders her
correctly. Do not repaint, regrade, or re-flag Roshan's skin tone anywhere in
this package, and do not carry the discarded flaw into any ledger or prompt.

### B. Reclassified: "finale key shows wrong antagonist"

The audit flagged every hybrid finale key for showing a dragon / phantom /
maestro "instead of the purple imp". **That was not drift.** The twelve keys in
`assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/` were generated to
the now-superseded hybrid-levels design in which the recurring **floor boss**
appears on stage with Roshan (Curtain Dragon floor 1, Shadow Phantom floor 2,
Midnight Maestro floor 3). Under the shipping design those keys are:

- **Valid** art-direction references for the three separate BOSS acts only.
- **Not usable** as references for the in-career imp-rival stage finales
  (beat 5 of the rebuild) — the rival there is the dressed purple imp, which
  appears in none of these keys.
- The shell/pearl motifs the audit flagged on the boss figures (shell bow
  clasps, shell fan, shell drum emblem) also dissolve on reclassification: the
  no-marine-motif rule applies to **imps only**, and these figures are house
  bosses.

**Legitimate residual flaw:** the floor-2/3 boss renderings (black-robed,
white skull-like masked phantom/maestro, dark faceless audiences) read
dark/spooky for a 4-year-old. Requests P4-03/P4-04 below cover a friendlier
re-render of those keys as boss-act references.

## House conventions this work must follow

### Weighted acceptance gate (restated)

Computer ceiling 4.9/5; **pass >= 4.5, target >= 4.7**. Weights:

| Criterion | Weight |
|---|---|
| Style/palette | 25% |
| Child-readable silhouette | 20% |
| Job/mechanic continuity | 20% |
| Roshan identity / prop cohesion | 15% |
| Modelability / mobile practicality | 10% |
| Completeness / uniqueness | 10% |

### Automatic-rejection list (restated verbatim)

wrong job/mechanic, boss content out of scope, realistic rendering, human legs
on Roshan, wrong species/order/state, text-heavy signage, copied third-party
imagery, clipped cells, repeated filler, off-palette dominance, micro-detail
unmodelable on Mobile.

### Regeneration protocol (per CLAUDE_START_HERE_OPERA_JOB_ASSET_REGENERATION_2026-07-24.md)

- Repository-relative paths only. Verify the package on disk before generating.
- **Path A (preferred): reuse/re-slice accepted cards.** Do not regenerate
  merely to make the art more realistic.
- **Path B: regenerate natively at >= 1024x1024** only when a new detail,
  fix, or angle is genuinely needed — never 256-and-upscale, never crop a 1024
  sheet cell and call it native (`tools/slice_opera_job_prototypes.py`
  normalizes-then-slices and is NOT a native-detail pipeline). Always supply
  **both** the existing accepted card (locks content/silhouette) **and** its
  source sheet (locks palette/line weight/scale) as image references.
- Candidates stage in the dated folder (section "Staging protocol" at the end),
  same asset_id filenames, ledger row per candidate, one controlled promotion
  commit, one ASSET_LICENSES.md line per accepted asset. Whole sheets promote
  only when all sixteen cells pass together. No `final2`/`better` filenames.
- **2048px rule (AGENTS.md, binding):** raster background resolution is
  measured per playable screen — every playable screen needs >= 2048x2048
  native coverage before runtime slicing into non-overlapping 1024x1024 POT
  Sprite3D/Sprite2D cards. Anything smaller is reference-only.

### Verbatim style contracts (quote by name in prompts; do not re-type variants)

**STYLE-HOUSE** — opera-house common contract (use for stage/lobby/seating/crest work):

> "Create a strict 4-by-4 flat concept-art asset sheet for the Pearl Opera
> House in Mermaid Roshan: Reef of Light. Use the attached accepted
> opera-house art as the binding style reference. Translate original
> early-20th-century live-theater design into a pastel toy-diorama: rounded
> low-poly-modelable forms, broad cel-shaded planes, matte painted surfaces,
> and navy/plum edge accents. Palette: peach, old rose, ivory, antique brass,
> mahogany, burgundy/plum, navy-purple shadows, and restrained seafoam/aqua
> reef accents. Use original shell-fan, wave, curtain-swag, and pearl motifs.
> Exactly sixteen isolated cells, left-to-right and top-to-bottom, one
> complete readable group per cell, generous navy separation, three-quarter
> orthographic product view, feasible as Godot Mobile geometry. No words,
> letters, numbers, UI, people, copyrighted characters, logos, crowns,
> generic star mascots, photorealism, tiny filigree, or captions."

(Adapt the first sentence's sheet-grid phrasing when generating a single card
or a wide master instead of a 4x4 sheet; everything else is binding.)

**STYLE-JOBS** — jobs-flat contract core (use for all career character/prop/state work):

> "Create a production-quality FLAT 2D CONCEPT ART SHEET, not a 3D render.
> Strict square 4-by-4 grid, exactly sixteen equal cells with thin dark navy
> dividers and a deep navy presentation background. ... Preserve Roshan's
> joyful young face, warm brown eyes, long wavy brown hair with a vivid
> rainbow streak, continuous rainbow-scaled mermaid tail, and split tail fin.
> Omit the backpack and everything printed on it. Roshan remains a mermaid in
> every pose: no human legs, shoes, or boots. Match the accepted Opera House
> finish: polished storybook cel illustration, rounded toy-like modelable
> forms, confident navy-purple outlines, aqua/lavender shadows, coral, teal,
> cream, and plum with restrained brushed gold, pearl, and shell accents."

Variant riders (append when applicable): **gameplay** cells add "immediately
readable by a non-reader using one finger" and "gentle retry rather than a
punitive fail state"; **stage-state** cells add "Communicate guidance,
progress, retry, and completion nonverbally with strong silhouettes, matching
colors/shapes, glow, paths, arrows, bubbles, and broad effects." All variants
prohibit: words/letters/numbers/logos/watermarks/generic stars/bosses/
photorealism/Blender rendering. (Adapt the grid phrasing for single-subject
cards; the finish/palette/identity language is binding.)

**IMP-IDENTITY** — authoritative rival/imp content lock (from
`assets_src/concepts/opera_rivals_2026-07-29/README.md` and
`authoritative_boxer_imp_reference.png`): purple humanoid imp, curled
**striped** horns (both visible), amber eyes, pointed ears, friendly fangs,
small hair tuft, curled tail. **ABSOLUTELY no shell, pearl, scallop, marine
badge, crest, medallion, or target motifs on any imp, ever.** Imps are
friendly mischief, never scary.

### Per-request format used below

Each request states: **asset_id** / **target path** (exact) / **canvas** /
**binding references** / **prompt** (contract name + request-specific
paragraph) / **content locks** / **was wrong** (one line). Table rows compress
the same fields.

---

## PRIORITY 1 — NEW assets the rebuilt acts load at exact paths

The five-beat rebuild's bop mechanic prefers these paths. Update
2026-08-01: at runtime the scuffle crews currently wear the career's accepted
rival costume slice (`assets/opera/worlds/actors/rival_<career>.png`), so these
two sprites are the crew's dedicated non-costumed upgrade plus the pose
variants below; `tools/prepare_opera_2d_props.py`'s shape-drawn placeholders
remain the last fallback. A bad candidate is worse than none — hold to the
gate.

### P1-01 — Mischief imp (scuffle crew)

- **asset_id:** `imp_mischief`
- **Target path:** `assets/opera/worlds/actors/imp_mischief.png`
- **Canvas:** 512x512, transparent background (or deep navy presentation field
  for deterministic matting — see delivery note below).
- **Binding references:**
  `assets_src/concepts/opera_rivals_2026-07-29/authoritative_boxer_imp_reference.png`
  (identity), any two of `assets/opera/worlds/actors/roshan_chef.png` /
  `roshan_detective.png` / `roshan_painter.png` (rendering style to match).
- **Prompt:** Begin with STYLE-JOBS (single-subject card phrasing), then:
  "One full-body mischief imp matching the attached authoritative imp
  reference exactly — IMP-IDENTITY — caught mid-bounce in a playful springing
  pose, arms up, grin wide, tail curled behind. No career costume: bare
  torso/simple imp look as in the reference. Painterly storybook rendering
  matching the attached Roshan actor sprites — soft painted shading and
  delicate line work, NOT thick-outline sticker/mascot cartoon. Single
  character, whole body inside the frame with margin, centered on a deep navy
  presentation field."
- **Content locks:** IMP-IDENTITY in full; both striped horns visible; whole
  silhouette inside canvas (no edge crops); friendly expression; no props.
- **Was wrong:** current file is a deliberately basic PIL shape placeholder.

### P1-02 — Imp captain (beat-4 boss of the scuffle)

- **asset_id:** `imp_captain`
- **Target path:** `assets/opera/worlds/actors/imp_captain.png`
- **Canvas:** 512x512, transparent (or navy field, as P1-01).
- **Binding references:** same as P1-01, plus the accepted P1-01 candidate
  once it exists (crew/captain must read as the same species and pipeline).
- **Prompt:** As P1-01, then: "This is the imp CAPTAIN: same species and
  rendering, slightly bigger and stockier build than the mischief imp, wearing
  ONLY a plain gold waistband (a simple flat gold sash — no buckle emblem, no
  medallion, no crest, nothing marine). Confident hands-on-hips or
  mid-bounce leader pose."
- **Content locks:** IMP-IDENTITY; plain gold waistband is the ONLY costume
  element; visibly larger than P1-01 at equal canvas scale.
- **Was wrong:** current file is the same shape placeholder with a gold
  rectangle.

### P1-03 — Optional pose variants (later polish, same gate)

- **asset_ids / target paths:** `imp_mischief_bopped` →
  `assets/opera/worlds/actors/imp_mischief_bopped.png`; `imp_mischief_bow` →
  `assets/opera/worlds/actors/imp_mischief_bow.png`; `imp_captain_bopped` →
  `assets/opera/worlds/actors/imp_captain_bopped.png`; `imp_captain_bow` →
  `assets/opera/worlds/actors/imp_captain_bow.png`
- **Canvas:** 512x512 each, same delivery as P1-01.
- **Binding references:** accepted P1-01/P1-02 (same character, same pipeline).
- **Prompt:** As P1-01/P1-02 with the pose swapped: *bopped* = dizzy and
  giggling, eyes as happy swirls, three small pale-gold stars circling the
  head (stars are the dizzy pictogram, allowed here as an effect, not a
  motif on clothing); *bow* = deep theatrical bow, one arm sweeping.
- **Content locks:** identical character to the accepted idle; no new costume
  elements; stars only around the head in the bopped poses.
- **Was wrong:** nothing — these do not exist; runtime works without them.

**Delivery note (all P1):** the runtime matting pipeline
(`tools/prepare_opera_2d_worlds.py` `_remove_edge_field`) deterministically
removes a deep navy presentation field. Deliver either pre-matted transparent
PNGs at the target paths, or navy-field cards in the staging folder for the
tool to matte — never any other background color.

---

## PRIORITY 2 — Corrections to accepted assets the game ships today

### P2-01 — Repainted eleven-costume rival sheet (systemic style fix)

- **asset_id:** `opera_rival_costume_sheet_master` (repaint candidate; stages
  under the same filename in the regeneration folder)
- **Target path (promotion):**
  `assets_src/concepts/opera_rivals_2026-07-29/opera_rival_costume_sheet_master.png`,
  then re-slice via `tools/prepare_opera_2d_worlds.py` to the eleven runtime
  actors `assets/opera/worlds/actors/rival_<career>.png` (boxer excluded — it
  uses the dedicated match asset).
- **Canvas:** native >= 1024x1024 sheet; **fixed row-major cell order
  identical to the current master:** pastry chef, detective, ballerina, candy
  maker, doctor, farmer, magician, painter, astronaut engineer, racecar
  driver, pop star, 12th cell empty.
- **Binding references:** current
  `assets_src/concepts/opera_rivals_2026-07-29/opera_rival_costume_sheet_master.png`
  (costume content lock), `authoritative_boxer_imp_reference.png` (identity),
  two `roshan_*` actor sprites (rendering style).
- **Prompt:** Begin with STYLE-JOBS, then: "Repaint the attached eleven-costume
  imp rival sheet in the painterly storybook rendering of the attached Roshan
  actor sprites — soft painted shading, delicate confident line work — NOT the
  current thick-outline sticker/mascot style. Keep every costume, pose, and
  cell position exactly as in the attached sheet. Every imp obeys
  IMP-IDENTITY, with BOTH curled striped horns clearly visible in every cell
  (through or around any hat/helmet)."
- **Content locks (per-cell fixes the repaint must land):**
  - *pastry chef cell:* restore the curled striped horns — the shipped
    `rival_chef.png` has **no horns at all** (blocker; different character).
  - *doctor cell:* no stray fragments — shipped `rival_doctor.png` carries a
    disconnected teal/cream striped dome baked in below the feet.
  - *farmer cell:* no stray fragments — shipped `rival_farmer.png` carries a
    gold sliver top-right and a purple ellipse cut by the bottom edge. (The
    farmer cell's clearly striped horns are the best in the set — keep them.)
  - *candy maker cell:* horn tips visible and striped (currently hidden under
    the beanie, unstriped where they show).
  - *magician cell:* both horns visible (currently one), no smudge under feet.
  - *astronaut cell:* horns restored (currently absent — only ears show
    through the helmet); replace the steel-grey wrench with a coral/gold
    palette wrench.
  - *pop star cell:* replace the photorealistic dark-metal microphone with the
    career's pearl/shell/coral mic design
    (`cards/opera_job_pop_star_gameplay_microphone_idle.png` reference);
    lighten the off-palette black tee/navy jeans block.
  - *racecar cell:* keep the marine-motif-clean striped helmet.
  - All cells: zero shell/pearl/marine/crest/medallion motifs (this lock
    already passes today — do not regress it).
- **Was wrong:** all eleven rivals are flat sticker/mascot cartoons beside a
  painterly Roshan — "two different games on one stage" — plus the per-cell
  identity defects above.
- **Note:** whole-sheet rule applies — promote only when all eleven costume
  cells pass together; until then the current slices remain in play.

### P2-02 / P2-03 — Boxer imp marine-motif blockers (imp rule violations)

These are the only *true* marine-motif violations post-correction (the finale
"violations" were reclassified under Correction B).

| asset_id | Target (regenerated cell → re-slice) | Canvas | Binding references | Was wrong |
|---|---|---|---|---|
| `opera_job_boxer_gameplay_imp_bow_group` | `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_boxer_gameplay_imp_bow_group.png` (from `boxer_gameplay_sheet_2026-07-21.png`) | native 1024x1024 card | existing card + source sheet + `authoritative_boxer_imp_reference.png` | All three bowing imps wear purple bows with gold scallop-SHELL clasps (blocker); card also bled a neighbor sliver, cropped the left imp, and has a face smudge |
| `opera_job_boxer_stage_imp_cells` (three cells: imp_peek_state, bop_state, gentle_retry) | corresponding cells of `assets_src/concepts/opera_jobs_flat_2026-07-21/boxer_stage_states_sheet_2026-07-21.png` → cards of the same names | native 1024x1024 per card | existing cards + source sheet + imp reference | Stage-state imps wear top hats with a cream scallop-SHELL badge (blocker). The shell on the pop-up barrel PROP is fine — only imp clothing violates the rule |

- **Prompt (both):** STYLE-JOBS + gameplay/stage rider, then: "Regenerate the
  attached cell with identical composition, pose, and props, but the imps'
  bows/hats are PLAIN (no clasp emblem, no badge, nothing marine). Align the
  imps to IMP-IDENTITY — curled striped horns, amber eyes, friendly fangs —
  so they read as the same species as the scuffle imps (the current
  hornless cat-eared mascots predate the authoritative imp)."
- **Content locks:** composition and prop set unchanged; IMP-IDENTITY;
  whole subjects inside the cell.

### P2-04..P2-07 — Shipped Roshan actor sprite fixes

All four ship at `assets/opera/worlds/actors/` and are runtime-loaded. Style,
pose, and costume are otherwise approved — fix ONLY the named defect. Where a
regen is needed, Path B: native >= 1024, both references (the current actor +
its source outfit sheet), then matte to a 512x512 actor.

| asset_id | Target path | Fix | Was wrong |
|---|---|---|---|
| P2-04 `roshan_boxer_fulltail` | `assets/opera/worlds/actors/roshan_boxer.png` | Re-cut from `assets_src/concepts/opera_jobs_flat_2026-07-21/boxer_outfit_sheet_2026-07-21.png` hero cell with the full tail in frame, or regenerate the identical pose full-body | Sprite is hard-cropped at the bottom canvas edge mid-tail; the cut line shows on stage |
| P2-05 `roshan_magician_cleanup` | `assets/opera/worlds/actors/roshan_magician.png` | Erase the un-matted solid navy wedge in the concave area under the tail; repaint the wand tip as a clean glowing pearl (currently a dark fuzzy scribble). Manual cleanup acceptable (matting repair, not art change); else Path B regen | Matting failure ships a black wedge glued to her hip on light stages |
| P2-06 `roshan_doctor_stethoscope` | `assets/opera/worlds/actors/roshan_doctor.png` | Repaint the held stethoscope to the canonical gameplay design (`cards/opera_job_doctor_gameplay_stethoscope.png`); remove the flat navy paddle mass swallowing the forearm/cuff | Prop garble: stethoscope reads as a hand-mirror/lollipop melting into the sleeve; dark blob at phone size |
| P2-07 `roshan_farmer_hairfix` | `assets/opera/worlds/actors/roshan_farmer.png` | Erase the solid black/navy backing wedges baked behind and below the rainbow hair streak (alpha repair, no art change) | Leftover sheet background pokes past the rainbow contour; dark blobs on light stages |

### P2-08 — Farmer gameplay sheet painterly repaint

- **asset_id:** `farmer_gameplay_sheet` (repaint candidate)
- **Target path (promotion):**
  `assets_src/concepts/opera_jobs_flat_2026-07-21/farmer_gameplay_sheet_2026-07-21.png`
  → re-slice its 16 cards.
- **Canvas:** native >= 1024x1024 sheet, same 4x4 grid, same 16 cell subjects
  in the same order (apple, berries, carrot, corn, happy_piggy_group,
  hay_bale, mud_splash, piggy_fed, piggy_hop, piggy_munch,
  piggy_target_medallion, piggy_trot_a, piggy_trot_b, pumpkin, toss_arc,
  vegetable_basket).
- **Binding references:** current gameplay sheet (content/count lock) +
  `farmer_outfit_sheet_2026-07-21.png` and
  `farmer_stage_states_sheet_2026-07-21.png` (the painterly style to match).
- **Prompt:** STYLE-JOBS + gameplay rider, then: "Repaint the attached farmer
  gameplay sheet in the same soft painterly storybook rendering as the
  attached farmer outfit and stage sheets — the current sheet is a glossy
  thick-outline sticker style that clashes with every other farmer asset.
  Identical subjects, counts, and cell order. Separate the worried-pig and
  happy-pig medallions so the two circles no longer overlap."
- **Content locks:** Farmer continuity lock — exactly nine piggies / five
  baskets / three pads, nothing baked into scenery; pig cycle poses
  (trot_a/trot_b/hop/munch/fed) preserved 1:1; `piggy_fed` stays a clean
  single-subject cell (it is the runtime goal prop, see P4-05).
- **Was wrong:** whole-sheet style drift — the only sheet in the package in
  the sticker style; the same pigs and produce exist twice in irreconcilable
  styles.

### P2-09 — Canonical prop designs: conflicting sheet cells regenerated to match

One design per career prop is hereby canonical — chosen as the design already
used by the runtime actor sprite / runtime goal prop, or by recorded
continuity lock. Regenerate ONLY the conflicting cells (Path B, native 1024
per card, both references), leave canonical cells untouched. Superseded
finale-key variants need no fix (reference-only, Correction B).

| ID | Career / prop | Canonical design (and why) | Regenerate to match | Was wrong |
|---|---|---|---|---|
| P2-09a | chef / oven | Gameplay pink arch-with-shell oven (`oven_open`/`oven_closed` cards — the runtime state pair) | stage `oven_alcove` cell | 3 competing ovens across gameplay/stage/2.5D (2.5D kiosk stays reference-only) |
| P2-09b | chef / finished cake | Gameplay `finished_cake` 3-layer vanilla/coral/plum with cherries (**runtime goal prop** `goal_chef.png`) | stage `cake_reveal` + `presentation_cart` cells | 3 different hero cakes in the non-finale sheets; no canonical reveal chain |
| P2-09c | chef / toppings | Gameplay cherry / cream / chocolate (topping cards exist per item) | stage `topping_pedestals` + `placement_glows` cells | Stage shows cherry/grapes/pearl-cream — a child matching toppings to glows cannot find chocolate |
| P2-09d | detective / magnifier | Teal handle with shell pommel (outfit sheet + **runtime actor** `roshan_detective.png`) | gameplay `magnifier` card + stage `magnifier_pointer` cell | 3 designs of the career's icon prop |
| P2-09e | detective / treasure chest | Teal-and-gold (gameplay `chest_closed`/`chest_open` — the runtime open/close pair) | stage `chest_pedestal` + `case_complete_tableau` cells | Chest flips to coral/red between state sets |
| P2-09f | ballerina / music box | Coral shell + gold treble clef (gameplay `music_box` — **runtime goal prop** `goal_ballerina.png`) | outfit-sheet music-box cell | Outfit variant contains a tiny HUMAN-LEGGED ballerina figurine — the only legged human in the deck, lore-breaking |
| P2-09g | candymaker / candy roster | The 7 sliced gameplay candies: coral flower, coral round, cream heart, plum bow, plum wrapped, teal shell, teal spiral (`wrapped_candy_reward` is the runtime goal prop) | stage `shelf_complete` cell (and see P2-09h) | 3 conflicting rosters — scene key adds a star candy and cupcake that exist nowhere as sprites |
| P2-09h | candymaker / shelf | Exactly SEVEN slots whose silhouettes match the 7-candy roster 1:1 | stage `seven_slot_shelf` cell | Named seven-slot, drawn with NINE, several slots match no candy (bottles, gummy bear; no bow) |
| P2-09i | candymaker / timing gauge | Fan gauge with pearl pointer (gameplay sheet; also on the press pavilion in scene key and finale — best continuity) | stage round-dial and arc-gauge cells (`timing_pointer` family); regenerate pointer states with a bigger, phone-readable needle | 3 competing timing-UI designs; fan-gauge pointer states nearly indistinguishable at phone size |
| P2-09j | magician / shuffle hats | Purple hats with coral/cream/teal bands (gameplay `coral_band_hat`/`cream_band_hat`/`teal_band_hat` — the 3-distinct-token system). The separate 2.5D plum/teal/coral PAVILION order stays its own world-landmark lock | stage-states hat cells incl. `final_reveal` | Stage sheet gives every hat an identical teal band — the child cannot track "which hat" across screens |
| P2-09k | magician / wand | Purple wand with glowing PEARL tip (outfit sheet + **runtime actor** `roshan_magician.png`) | gameplay `pearl_wand` card | Gameplay wand has a cream scallop-shell pompom tip — a second signature-wand design |
| P2-09l | painter / hero brush | Red handle, rainbow round-mop brush (outfit sheet + **runtime actor** `roshan_painter.png`) | gameplay flat-housepainter brush cells: `coral_loaded_brush`, `cream_loaded_brush`, `plum_loaded_brush` (keep the plum/coral/cream load colors) | 4 brush designs across the career; the loaded-state trio uses a different brush than the one Roshan holds |
| P2-09m | popstar / arrow color mapping | **Continuity lock: coral=left, teal=right, plum=up, cream=down** (gameplay button cards, recorded lock) | stage `dance_floor` + arrow-wheel cells (2.5D/finale variants are reference-only) | Color-to-direction differs in nearly every asset; color IS the instruction channel for a pre-reader |
| P2-09n | popstar / speakers | Stage-states purple/teal stacked towers (`speaker_stacks` — the stage-build family) | gameplay `speaker` cell | 3 unrelated speaker designs |
| P2-09o | racer / steering wheel | Gameplay `steering_wheel` card: teal/coral two-tone rim, gold shell hub (the steer-UI card; the actor's third design is off-palette maroon) | outfit-sheet accessory-wheel cell; repaint the wheel held in `assets/opera/worlds/actors/roshan_racer.png` to match | 2 conflicting concept designs plus a third dark-maroon wheel baked into the runtime actor |
| P2-09p | doctor / stethoscope | Gameplay `stethoscope` card design | outfit-sheet stethoscope cell (r2c4); actor repaint covered by P2-06 | Two tube-routing/earpiece designs of the same prop |
| P2-09q | doctor / four-step board | One left-to-right arrow flow | stage `four_step_board` cell | Arrows alternate right/left/right/left — reads as a zigzag, not a sequence, to a pre-reader |
| P2-09r | racer / zoom strip | Same teal strip in both states, active = glowing/lit version | gameplay `zoom_strip_active` cell (recolor) | Active state changes hue entirely (teal→coral); a 4-year-old may not read them as the same pad |

**Prompt (all P2-09 rows):** STYLE-JOBS + the matching rider, then: "Regenerate
the attached cell keeping its composition and function identical, changing
ONLY the [prop] to exactly match the attached canonical reference card." Attach
the canonical card + the cell's source sheet.

---

## PRIORITY 3 — Stage/backdrop raster masters (2048px-per-playable-screen rule)

Career worlds ship today as code-native vector sets
(`scripts/opera_world_backdrop_2d.gd`), which legitimately satisfies the
crispness requirement — these masters are an UPGRADE path, not a blocker. Any
raster that goes to runtime must meet AGENTS.md: **native >= 2048x2048 per
playable screen, sliced into non-overlapping 1024x1024 POT cards**.

### P3-01 — Proscenium stage-finale backdrop master (the beat-5 stage)

- **asset_id:** `opera_stage_finale_master`
- **Target path:** stage in the regeneration folder; proposed runtime
  promotion `assets/opera/worlds/stage/finale_stage_<col><row>.png` (2x2 grid
  of 1024x1024 cards; final path assigned at the integration commit — the
  runtime currently draws this proscenium in code, and swapping it in is an
  owner call).
- **Canvas:** native >= 2048x2048 (one playable screen).
- **Binding references:**
  `assets_src/concepts/opera_house_flat/opera_house_stage_scene_key_2026-07-21.png`
  (binding composition/style),
  `cards/opera_stage_elliptical_proscenium.png`,
  `cards/opera_stage_house_curtain_states.png`,
  `cards/opera_stage_stage_apron_footlights.png`.
- **Prompt:** STYLE-HOUSE (single wide master phrasing), then: "One complete
  stage-facing finale backdrop: elliptical proscenium arch with shell crown,
  deep plum curtain swags tied open at the sides, brass trim, a broad apron
  with a row of lit globe footlights, pearl accents on the arch and swag —
  and an EMPTY center stage (no characters, no props, no audience) so runtime
  actors, the goal prop, and score UI composite on top. Objects must not sit
  ambiguously across the 1024px tile boundaries; keep the center stage area
  clean of detail."
- **Content locks:** empty center stage; no text; no baked characters;
  tile-boundary rule (AGENTS.md: boundary-straddling objects are extracted as
  depth cards and the background healed — easier to avoid at generation time).
- **Was wrong:** nothing exists — the best stage source is a 1024x576
  flattened scene key, 2-8x below the rule.

### P3-02 — Per-career world backdrop masters (optional upgrade, 12)

- **asset_ids:** `opera_world_master_<career>` for chef, detective, ballerina,
  candymaker, doctor, farmer, boxer, magician, painter, astronaut, racer,
  popstar.
- **Canvas:** native >= 2048x2048 per playable screen (a wider world needs a
  proportionally wider native master, e.g. 2 screens → >= 4096x2048).
- **Binding references:** the career's
  `assets_src/concepts/opera_jobs_2p5d_2026-07-24/<career>_2p5d_scene_key_2026-07-24.png`
  (layout blueprint — reference-only at its 1024x576 size) and
  `<career>_environment_texture_kit_2026-07-24.png` (materials/trim).
- **Prompt:** STYLE-JOBS palette dialect on STYLE-HOUSE construction language,
  then: "Rebuild the attached scene key's world as a clean native-resolution
  backdrop: same landmarks and route, simplified for phone readability, no
  characters, no gameplay props baked in (runtime places them), no text."
- **Content locks:** per-career continuity locks (farmer nine-pads,
  boxer three pads, magician pavilion order plum/teal/coral, painter station
  order plum/coral/cream, etc. — see the locks list in the audits); nothing
  interactive baked into scenery.
- **Was wrong:** nothing broken — vector sets ship; these upgrade them.
  Generate only if the owner opts in; P3-01 has priority.

### P3-03 — Audience seating cards (missing from all 172 house cards)

- **asset_id:** `opera_house_audience_kit`
- **Target path:** stage in the regeneration folder; promoted sheet+cards join
  `assets_src/concepts/opera_house_flat/` as a 14th kit.
- **Canvas:** native >= 1024x1024 sheet, 4x4 cells (STYLE-HOUSE grid).
- **Binding references:** `opera_house_stage_scene_key_2026-07-21.png` (the
  only place seats exist, baked), `cards/opera_stage_side_box.png`,
  `cards/opera_architecture_curved_balcony_fascia.png`.
- **Prompt:** STYLE-HOUSE, then: "Sixteen isolated audience-seating modules
  for the house side of the finale scene: single seat, straight seat row,
  curved seat row, seat block (two rows), aisle end-cap, balcony seat strip,
  side-box interior seat pair, and matching empty/occupied variants where the
  occupants are the established friendly creature cast in silhouette-simple
  form (starfish, bunny-fish, piggies — never humans)."
- **Content locks:** no humans (the original no-people contract left zero
  audience — creature occupants are the sanctioned exception); modules
  tileable side-by-side; navy separation between cells.
- **Was wrong:** audience seating exists ONLY as baked paint inside the stage
  scene key — no seat, seat-row, or seat-block card anywhere; any raster
  stage scene with a visible house needs it.

---

### P3-04 — Per-career ON-STAGE minigame scene backgrounds (12) — owner drafts reviewed 2026-08-01

The owner supplied five stylized first drafts in review (pastry district v2,
painter stage, pop-star stage, detective stage, astronaut stage — generated
at 1672x941, not yet on disk in the repo). They are ACCEPTED DIRECTION for a
twelve-scene family: the career's finale/stage phases (stage_mode from the
captain scuffle onward) swap the district painting for an on-stage scene.
Deliver every draft plus the remaining seven careers into the staging folder.

- **Target paths (after promotion + slicing):**
  `assets/opera/worlds/backdrops/stage_<career>.png` for
  chef, detective, ballerina, candymaker, doctor, farmer, boxer, magician,
  painter, astronaut, racer, popstar. Runtime swap is a three-line change in
  `opera_world_backdrop_2d.gd` (already structured for it: `set_stage`).
- **Canvas:** native >=2048x1152 (16:9) master per scene, sliced to 1024x1024
  POT cards for promotion (AGENTS.md 2048px-per-playable-screen rule). The
  1672x941 drafts are reference-only.
- **Shared contract (every scene):** elliptical proscenium + red/plum
  curtains + shell-and-pearl crest + brass trim + footlight row, matching
  the reviewed drafts and the stage/backstage kit grammar; audience
  silhouette band confined to the bottom 15% (the game overlays the real
  family cutouts there); the CENTER 60% width x middle 55% height must stay
  low-detail and prop-free — the interaction panel and gesture surface sit
  there; career stations sit at the horizontal THIRDS (they align with the
  three choice lanes); stage-right lower area stays clear (the goal-prop
  card docks there before the steal); NO characters, NO text/numerals, no
  baked spotlights over the center zone.
- **Gameplay-fit modifications found in the reviewed drafts:**
  - *Pop star stage:* the four arrow pads MUST use the canonical mapping
    coral=LEFT, teal=RIGHT, plum=UP, cream=DOWN (the reviewed draft shows
    teal up / plum left / red right / cream down — regenerate the pad
    colors; the rainbow path and rhythm ribbon are approved).
  - *Painter stage:* pot order plum -> coral -> cream stage-left-to-right is
    correct in the draft — lock it; space the three pots at the thirds;
    keep the sunrise backdrop panels behind, splat puddles clear of center.
  - *Detective stage:* the three curtained arches are the MATCH choice
    lanes — keep them evenly spaced at the thirds; glowing footprint trail
    should read left-to-right (the TRAIL swipe direction); magnifier
    pedestal may stay center-low but under the clear-zone line.
  - *Astronaut stage:* straight/elbow/ring pipe trio and flower-socket pads
    at the thirds (choice lanes) — correct in the draft; valve tower with
    wheel stage-right of center; rocket fully stage-right, above the
    goal-prop dock; bubbles never flame.
  - *Pastry district v2:* accepted direction for the P3-02 district-master
    refresh (giant whisk bowl, shell oven, cake-stand towers, hero-cake
    stage); keep the mid-band walkway clear where the panel sits.
  - Remaining seven scenes: follow each career's stage_states sheet props
    and the continuity locks in this document.
- **Was wrong / missing:** no on-stage scene art exists at any resolution;
  the runtime currently draws a code proscenium overlay on the district
  painting during stage phases.

### P3-05 — Nursery (job 13) world painting, stage scene and goal prop

The Moonbeam Nursery career (cooperative, Nurse Faron) shipped with authored
actor/baby sprites but no painted world, stage scene, or goal-prop card. Its
backdrop currently falls back to the code-native vector set and its goal-prop
dock is empty (both degrade gracefully).

- **`world_nursery` district painting** — target
  `assets/opera/worlds/backdrops/world_nursery.png`, same family and spec as
  the twelve accepted 2p5d career keys (1672x941 generation, 16:9): a
  moonlit underwater nursery district — crescent-moon lamps, cradle pods,
  pillow drifts, bottle-warmer kiosk, star mobiles — entry left, open
  mid-band walkway (the interaction panel sits there), destination right.
  Palette: seafoam teal, cream, soft lavender, pearl gold; night-calm.
  Also remove the probe exemption in probe_opera_2d.gd when it lands.
- **`stage_nursery` on-stage scene** — joins the P3-04 twelve-scene family
  (same shared contract): three cradle stations at the thirds, moonbeam
  spotlights, blanket rail stage-right; audience band per contract.
- **`goal_nursery` prop card** — a moonbeam star-mobile with three hanging
  plush charms (matches the baby trio), 1024x1024 navy-field card for the
  standard matting pipeline → `assets/opera/worlds/props/goal_nursery.png`.
  This is the prop the imp captain steals in BABY CHASE.
- **Content locks:** the three babies match `assets/opera/worlds/nursery/
  baby_0..2.png`; Faron matches `faron_nursery.png`; no shell/pearl/marine
  motifs on any imp; bubbles never flame; no text.

## PRIORITY 4 — Housekeeping regenerations

### P4-01 — Crest card re-slice (all 16) + flat job_crest re-slices

- **asset_ids:** `opera_crest_<name>` x16 (ballerina, boxer, candy, chef,
  detective, doctor, dragon, engineer, farmer, house, maestro, magician,
  painter, phantom, racer, singer); plus flat `opera_job_<career>_outfit_job_crest`
  cards for pastry_chef, detective, ballerina, painter, astronaut_engineer.
- **Target paths:** `assets_src/concepts/opera_house_flat/cards/opera_crest_*.png`;
  `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_*_outfit_job_crest.png`.
- **Method:** **Path A re-slice** — the source sheets are clean; the blind
  uniform 256px grid missed every drawn oval. Re-cut with per-cell bounds from
  `opera_house_crest_wayfinding_kit_2026-07-21.png` and the career outfit
  sheets. The astronaut outfit sheet's bottom row has SIX sub-cells (not
  four), so it needs custom bounds — its rocket crest badge never received a
  card at all. Regenerate (Path B, native 1024) only cells a re-slice cannot
  recover.
- **Was wrong:** every sampled crest card clips its own frame and bleeds
  slivers of neighboring crests — the entire wayfinding/portal-signage system
  is unusable as sprites; five career job_crest cards have the same
  misregistration (the astronaut one is the worst).

### P4-02 — Multi-state cards split into per-state cards

| asset_id | Source card | Split into | Extra requirement |
|---|---|---|---|
| `opera_stage_house_curtain_closed` / `_open` | `assets_src/concepts/opera_house_flat/cards/opera_stage_house_curtain_states.png` | 2 cards | — |
| `opera_architecture_medallion_dark` / `_lit` | `cards/opera_architecture_medallion_states.png` | 2 cards | — |
| `opera_upper_access_floor_selector_ground` / `_middle` / `_full` | the floor-selector trio in `opera_house_upper_floor_access_kit_2026-07-21.png` | 3 cards | Strengthen dark-state contrast — today all three shells read as lit in every state; the lock/unlock UI cannot drive off them |

Path A re-slice where the sheet already separates states; Path B native-1024
regen for the floor selector (the contrast fix is an art change). STYLE-HOUSE.

### P4-03 — Friendly floor-2/3 boss redesign cards (do FIRST, gates P4-04)

- **asset_ids:** `boss_shadow_phantom_friendly`, `boss_midnight_maestro_friendly`
- **Target path:** regeneration folder cards (art-direction references, not
  runtime).
- **Canvas:** native >= 1024x1024, single character card each.
- **Binding references:** the current phantom/maestro as rendered in any F2/F3
  finale key (silhouette/role lock);
  `assets/art35/opera/opera_phantom.glb` / `opera_maestro.glb` exist as the
  in-game 3D bosses — the redesigns must still read as the same characters.
- **Prompt:** STYLE-HOUSE character phrasing, then: "Redesign this opera-house
  boss as a FRIENDLY toy-theatre character for a 4-year-old: keep the cloaked
  conductor silhouette and role, but replace the black robe and white
  skull-like mask with plush rounded forms, warm plum/lavender/pearl colors, a
  soft smiling face (a gentle domino half-mask is fine — never skull-like),
  visible friendly eyes. Playful, huggable, zero menace."
- **Content locks:** same character read (a child who met the finale key
  version must recognize them); no marine-motif restriction (house bosses may
  carry shell/pearl motifs — that rule is imps-only).
- **Was wrong:** the F2/F3 boss renderings read dark/spooky (black-robed,
  white skull-like mask, faceless dark audiences) — the legitimate residue of
  Correction B.

### P4-04 — F2/F3 finale-key re-renders with the friendly bosses (8 keys)

- **asset_ids / target paths:** re-render candidates for
  `assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/<career>_performance_boss_finale_2026-07-24.png`
  for the eight F2/F3 careers — doctor, farmer, boxer, magician (Shadow
  Phantom) and painter, astronaut_engineer, racecar_driver, pop_star
  (Midnight Maestro). The four F1 Curtain Dragon keys are fine as-is.
- **Canvas:** generate natively wide (>= 1536x864), deliver 1024x576
  normalized like the rest of the package.
- **Binding references:** the existing key (binding composition — these
  passed at 4.8-4.9 on composition) + the accepted P4-03 redesign card.
- **Prompt:** STYLE-JOBS palette + finale phrasing, then: "Re-render the
  attached finale key with the identical composition, stage, and Roshan, but
  the boss replaced by the attached friendly redesign, and the audience
  silhouettes warmed (recognizable friendly creature shapes, softly lit, not
  featureless black)."
- **Content locks:** these remain **boss-act references only** (Correction B)
  — never sources for the in-career imp-rival finales; boss and Roshan must
  be able to bow together; no damage/health bars/fire/weapons/defeated boss.
- **Was wrong:** spooky boss rendering (see P4-03); everything else about the
  keys was accepted.

### P4-05 — Native-1024 re-renders of the 12 goal-prop cards (priority subset)

The rebuild mats these exact cards into runtime goal props
(`tools/prepare_opera_2d_props.py` → `assets/opera/worlds/props/goal_<career>.png`).
They are currently 4x Lanczos upscales of ~256px sheet cells — soft at
runtime scale, and the single most-seen prop art in every act (shown at the
workbench, stolen in beat 4, won back at the curtain call). Path B: native
>= 1024x1024 single-subject card on a deep navy field, references = existing
card + its source gameplay sheet, identical subject and silhouette.

| Career | Card to re-render natively (in `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`) |
|---|---|
| chef | `opera_job_pastry_chef_gameplay_finished_cake.png` |
| detective | `opera_job_detective_gameplay_pearl_tiara.png` |
| ballerina | `opera_job_ballerina_gameplay_music_box.png` (fix the clipped shell lid at the top edge) |
| candymaker | `opera_job_candy_maker_gameplay_wrapped_candy_reward.png` (remove the neighbor-cell scoop handle and tong tip) |
| doctor | `opera_job_doctor_gameplay_recovered_starfish.png` (one coral five-armed starfish — species lock) |
| farmer | `opera_job_farmer_gameplay_piggy_fed.png` (painterly, per P2-08) |
| boxer | `opera_job_boxer_gameplay_championship_belt.png` (canonical design per P2-09; fix the right-edge grid cut) |
| magician | `opera_job_magician_gameplay_bunny_fish_reveal.png` (finned bunny-fish, never a land rabbit) |
| painter | `opera_job_painter_gameplay_framed_sunrise.png` |
| astronaut | `opera_job_astronaut_engineer_gameplay_rocket_front.png` |
| racer | `opera_job_racecar_driver_gameplay_shell_trophy.png` (fix residual gridline fragments) |
| popstar | `opera_job_pop_star_gameplay_microphone_finale.png` |

After promotion, re-run `tools/prepare_opera_2d_props.py` to refresh the
runtime props (deterministic, non-destructive).

### P4-06 — Misc edge cleanup (Path A, no regeneration)

Re-cut with corrected bounds / erase debris; one line each:

- `assets_src/concepts/opera_house_flat/cards/opera_stage_scenic_backdrop.png`
  — neighbor-flat sliver on the right edge.
- `cards/opera_lobby_services_handwashing_bubble_markers.png` — neighbor
  sliver along the top.
- `cards/opera_stage_elliptical_proscenium.png` — column bases clip the
  bottom edge.
- `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_farmer_stage_states_piggy_finale.png`
  — source cell overflows its grid (rightmost pig bisected); regen the cell if
  a crop must lose a pig.

---

## Staging protocol (binding for every request above)

1. **All candidates land in**
   `assets_src/concepts/opera_regeneration_2026-08-01/cards/` (individual
   candidates, same asset_id filenames as their targets) and
   `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/`
   (review sheets), alongside:
   - `assets_src/concepts/opera_regeneration_2026-08-01/PROMPTS.md` — exact
     prompts + provenance (external `exec-*.png` names are provenance-only).
   - `assets_src/concepts/opera_regeneration_2026-08-01/REGENERATION_LEDGER.csv`
     — one row per candidate: asset_id, family, accepted reference path,
     prompt revision, generation id, native dimensions, score, status
     (candidate/rejected/accepted), rejection reason.
2. **Score every candidate against the weighted gate** (pass >= 4.5, target
   >= 4.7) and the automatic-rejection list. Rejected candidates stay in the
   ledger with reasons; rejected files never enter the repo proper.
3. **One controlled promotion commit** moves accepted files to their real
   target paths, rebuilds the contact sheet and ledger, and re-runs the
   derivation tools (`tools/prepare_opera_2d_worlds.py`,
   `tools/prepare_opera_2d_props.py`) where runtime slices/mats derive from a
   promoted source. Whole sheets (P2-01, P2-08, P3-03) promote only when all
   cells pass together.
4. **One `ASSET_LICENSES.md` line per accepted asset** ("OpenAI-generated
   project concept art", date, modifications), plus an audit note.
5. Delivery report: branch + SHA, reuse/regen/reject/accept counts, native
   resolution confirmation, per-career counts, min/max/mean scores, promoted
   paths, deferred assets, license updates, CI run URL.


---

## PRIORITY 6 — Imp & rival animation-state program (2026-08-02)

> **EXTENDED 2026-08-02 → `CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md`.**
> The shared imp brain (`scripts/imp_ai.gd`) now plays wind-up, charge,
> slash, recover, guard, stagger and flee as well. Everything below is
> still wanted and unchanged; the new handoff adds those seven states,
> the per-character fallback chain the loader uses, and a pose-aware
> acceptance gate. Read both, deliver from the handoff's tier list.

Stage-roaming combat plays the characters as state sprites (idle / bopped /
bow now; hop and taunt next). The base-imp six-sprite set is the quality
benchmark; the audit found one defect in it and systemic foot-crops in the
rival idles. Full audit: the Phase-2 sprite audit (imp_audit) — spec below
is paste-ready.

## 4. Codex generation spec for the twelve costumed rivals

**Characters (12):** astronaut, ballerina, boxer, candymaker, chef, detective, doctor, farmer, magician, painter, popstar, racer.

**Global rules — paste into every codex prompt:**
- Canvas **512×512, RGBA, transparent background**. No background halo: semi-transparent fringe (16<alpha<240) must be **<15%** of solid pixels; hard-edged matte like `imp_captain.png` (6.8%) is the target.
- **Full figure in frame**: minimum 12 px clear margin on all four sides; nothing may touch a canvas edge. Feet complete, including soles.
- **Baseline/anchor lock**: soles rest at **y ≈ 504** (8 px bottom gap). Standing height (horn-tip to toe) **480–490 px**. Sprite pivot = bottom-center **(256, 504)**; horizontal centroid within **256 ± 24**. Airborne frames (`hop_b`, `bopped`) keep the same body scale and centroid window — do not shrink the character to fit FX.
- **Facing**: 3/4-front, bow/taunt lean to viewer-left (matches imp set). Engine mirror-flips, so no readable text/logos on costumes.
- **Alpha integrity**: exactly one connected solid component (plus declared FX only); **no interior holes >200 px** except true see-through gaps between limbs and body. (This is the `imp_captain_bow` shorts bug — reject any output with background showing through solid cloth.)
- **Costume-consistency lock**: pass that character's existing idle (`rival_<costume>.png`) as the style/reference image. Identical skin purple (`#d070f0` family), amber eyes, fangs, ear/horn shapes, tail; identical costume garments, colors, shoes, and hat in **every** state. Held props (chef's whisk, detective's magnifier, etc.) appear in **all** states, same hand — including bopped — so state swaps never pop a prop in or out. Dizzy-spiral eyes in bopped only; amber eyes everywhere else.
- **Bopped states: NO baked stars** — the shared `fx_dizzy_stars.png` overlay provides them.
- Rendering style: match the imp 6-set's soft painterly shading and line weight (not the crisper `rival_boxer` outline style).

### Numbered codex request list

**Fixes to existing files:**
1. `imp_captain_bow.png` — regenerate (same pose/costume). Reject cause: 1,252 px alpha hole through the shorts; also slim the belly/forearms ~10% toward `imp_captain.png` proportions.
2. `rival_detective.png` — full regenerate. Reject cause: ghost/double-exposure artifacts, detached crescent artifact top-right, 38% semi-alpha matte, feet cropped at canvas bottom.
3. `rival_boxer.png` — re-render at 512×512 standard framing (feet at y≈504, height 480–490 px). Art content is approved; only canvas/scale/baseline are wrong.
4. Remaining 10 rival idles (`rival_astronaut/ballerina/candymaker/chef/doctor/farmer/magician/painter/popstar/racer.png`) — regenerate with complete feet (all currently hard-cropped at the last row) and clean mattes (<15% semi-alpha; magician currently 56%).

**New shared FX:**
5. `fx_dizzy_stars.png` — 256×256 RGBA overlay: 3 gold stars + thin swirl ring, transparent center; loops by engine rotation. One file serves all characters.

**New per-character states — 5 files × 12 characters (60 files), filename pattern `rival_<costume>_<state>.png`:**
6. `rival_<costume>_bopped.png` — knocked back mid-air, limbs flailing, dizzy-spiral eyes, open wailing mouth, **no stars** (pose reference: `imp_mischief_bopped.png` / `imp_captain_bopped.png`).
7. `rival_<costume>_bow.png` — deep stage bow to viewer-left, one arm swept out, feet planted (pose reference: `imp_mischief_bow.png`).
8. `rival_<costume>_hop_a.png` — crouch anticipation: knees bent, arms back, ears/tail down; soles at y≈504.
9. `rival_<costume>_hop_b.png` — airborne stretch: legs tucked, arms up, ears/tail up; body lifted ~40–60 px, same body scale.
10. `rival_<costume>_taunt.png` — standing, one arm waving overhead, cheeky grin, weight on one leg; soles at y≈504.

Full manifest (rows 6–10 expanded): `rival_astronaut_bopped.png`, `rival_astronaut_bow.png`, `rival_astronaut_hop_a.png`, `rival_astronaut_hop_b.png`, `rival_astronaut_taunt.png` — and identically for `ballerina`, `boxer`, `candymaker`, `chef`, `detective`, `doctor`, `farmer`, `magician`, `painter`, `popstar`, `racer`.

**Acceptance gate (run per file before commit):** canvas 512×512 RGBA; solid-mass height 480–492 (standing) ; bottom gap 6–10 px; no solid pixels within 2 px of any canvas edge; bottom-row solid run <100 px (crop detector); semi-alpha <15%; connected components = 1; no interior holes >200 px outside limb gaps; dominant skin quantized color in the `#d070f0` family. These thresholds all pass on the imp benchmark files and fail on every defect found above.

*(Out of scope but adjacent: the matching `roshan_<costume>.png` set in the same directory will need the identical state expansion; same spec applies.)*

---

## PRIORITY 7 — Storybook task-card frame, station marker, magnifier (2026-08-02)

The runtime draws these procedurally today (StorybookUI language); raster
art upgrades them. Extracted from the UI design-language report:

## 4. Codex art request spec (per assets/ART_GENERATION_CONTRACT.md)

Contract constraints that bind any request: textures ≤1024 px longest side OR power-of-two; Mobile renderer must read correctly; every asset ships with generator/source + QA renders + ASSET_LICENSES.md row (project-generated, © Mermaid Roshan LLC) and must be PLACED by runtime code in the same workstream (no orphans); never touch assets/book/, assets/audio/voices/, assets/characters/friends/ or regenerate Roshan.

Request A — task_card_frame (landscape nine-patch):
- Canvas 1024x1024 RGBA (POT), frame drawn as a 920x760 landscape border centered, transparent center ≥560x420. Corner ornament zones ≤200x200 so NinePatch margins of 200 protect them; edge middles must be a REPEATABLE scallop/pearl run (uniform lobes, no centered medallion) so TILE_FIT stretching is invisible. Optional matching crest as a SEPARATE 256x192 RGBA sprite to overlay top-center (keeps the nine-patch clean).
- Style contract wording: "Pastel toy playset, cel-shaded storybook diorama. Cream scallop-shell lobes (#f5ebd1) outer ring, lavender band (#a87dd6 lightened), gold trim (#f5b838), aqua pearl accents (#45c4c7 / #B3F7FF). Navy/indigo contour lines #4a4f78–#1a1238, never black; shadows aqua/lavender, high-key, no baked spotlights or vignettes. No faces on the frame. Flat broad color fields, rounded slightly-asymmetrical masses, child-readable at 50% scale."
- Must harmonize with StyleBoxFlat neighbors: contour weight ≈5 px at 460-wide display, corner rounding reading ≈44 px.

Request B — station_marker (world-space task beacon):
- Canvas 512x1024 RGBA (POT), single upright sign/easel: rounded post + shell-crowned header board with transparent (or cream #f5ebd1) inner window ≥360x360 for a runtime-set task icon. Reuse the v3 easel language (wood + silver trim + pink scallop crest) or the lavender/gold frame language of v2 — one family, stated explicitly in the request. Bottom 96 px = soft contact-shadow blob baked separately (see sky_lagoon_contact_shadow.png precedent) or omitted.

Request C — magnifier prop (search/inspect tasks; none exists in assets):
- Canvas 512x512 RGBA (POT), single sticker-style magnifying glass at 45 degrees: gold handle #f5b838, lavender grip #a87dd6, aqua-tinted glass #45c4c7 at ~25% opacity with one white crescent specular, PURPLE_DEEP #382485 contour. No face, no rainbow (rainbow is a reward accent only). Silhouette must read at 64 px.
- Deliver each with QA renders at gameplay scale on the Mobile renderer per the contract's stress-test loop; candidates without runtime captures cap at 2/5 and must not ship.
