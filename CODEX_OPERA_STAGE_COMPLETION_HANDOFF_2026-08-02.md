# Codex handoff — art to COMPLETE the opera stage-interaction build (2026-08-02)

**Audience:** Codex — image generation + deterministic promotion.
**State of play:** the twelve painted career worlds are now playable stages
(walkable routes, roaming imp combat with tap/swipe, point-and-click task
stations, the detective's draggable magnifier, StorybookUI task cards) —
see OPERA_STAGE_INTERACTION_2026-08-02.md. Every system below currently
runs on a procedural or borrowed placeholder and is wired to load the real
asset the moment it lands at the stated path. Nothing here is speculative;
each request names the runtime consumer.

**Binding conventions (do not restate per item):** the weighted acceptance
gate (pass >= 4.5, target >= 4.7), automatic-rejection list, staging-folder
triple (`assets_src/concepts/opera_stage_completion_2026-08-02/{cards,
contact_sheets}/ + PROMPTS.md + REGENERATION_LEDGER.csv`), single controlled
promotion commit, one ASSET_LICENSES.md row per accepted file, and the
STYLE-JOBS / STYLE-HOUSE / IMP-IDENTITY contracts are all as written in
OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md. The sprite acceptance gate
(baseline y=504, height 480-490, semi-alpha <15%, one component, no interior
holes >200 px, no edge contact) is P6 of that document; run it per file.

---

## SET 1 — Costumed character state sprites (BLOCKS combat polish)

The roaming combat plays idle -> bopped -> bow state swaps. Only the two
base imps have states; when a costumed crew imp is bopped the sprite pops
to the base imp (identity break, visible every scuffle).

Runtime loader: `opera_career_world_2d.gd` combat layer
(`rival_<costume>_<state>.png`, falls back to base-imp states today).

1.1 **Fixes first (3 files):** `imp_captain_bow.png` (alpha hole through
    shorts — regenerate), `rival_detective.png` (ghosting/crop — full
    regen), `rival_boxer.png` (re-render at 512x512 standard framing).
1.2 **Re-render the 10 remaining rival idles** with complete feet and
    clean mattes (all currently hard-cropped at the last row; magician
    matte worst at 56% semi-alpha).
1.3 **Shared FX:** `fx_dizzy_stars.png` — 256x256 overlay, 3 gold stars +
    thin swirl ring, transparent center (engine rotates it; serves all 14
    characters).
1.4 **60 new state files** — `rival_<costume>_{bopped,bow,hop_a,hop_b,
    taunt}.png` for all 12 costumes, 512x512, per the P6 global rules
    (costume locks from each costume's idle; bopped WITHOUT baked stars;
    hop pair = crouch anticipation + airborne stretch for the roaming walk
    cycle).
1.5 **Adjacent, second pass:** the matching `roshan_<costume>_{glide,
    work}.png` pair per career (she now travels the stage between
    stations; glide = tail-kick travel pose facing viewer-right, work =
    tool-in-use pose). Same canvas/gate; her identity locks are the
    accepted `roshan_<costume>.png` idles.

## SET 2 — Storybook interaction kit (BLOCKS the "same language as menus" bar)

Runtime draws these procedurally in the StorybookUI palette today; raster
art replaces one draw call each. Full specs (canvas, NinePatch margins,
style wording) are P7 requests A/B/C in the 08-01 document:

2.1 `task_card_frame` — 1024x1024 POT landscape nine-patch, scallop/pearl
    repeatable edges, corner ornaments <= 200x200, optional separate
    256x192 crest sprite. Consumer: `_draw_task_card()`.
2.2 `station_marker` — 512x1024 upright shell-crowned sign/easel with a
    >= 360x360 icon window. Consumer: `_draw_station_marker()`.
2.3 `magnifier_prop` — 512x512 sticker-style magic magnifying glass
    (gold handle, aqua glass at ~25% opacity, purple-deep contour).
    Consumer: `_draw_lens_layer()` (drawn lens today).
2.4 Optional: `clue_sparkle` — 128x128 four-point gold sparkle with soft
    halo for the lens finds (vector twinkle today).

## SET 3 — Nursery career art (BLOCKS job 13 visual parity)

The Moonbeam Nursery is the only career on the code-native vector
backdrop, with an empty goal-prop dock. Full specs are P3-05 (08-01 doc):
3.1 `world_nursery.png` district painting (1672x941 generation, promoted
    full-bleed like the other twelve — also remove the probe exemption in
    `probe_opera_2d.gd` in the same commit).
3.2 `stage_nursery` on-stage scene (joins SET 4 family).
3.3 `goal_nursery` prop card (moonbeam star-mobile, navy-field 1024 card
    for the standard matting pipeline).

## SET 4 — On-stage finale scenes (12) — RESOLUTION DECISION RECORDED

P3-04 was deferred over the native-2048 gate; the owner has since ruled
(2026-08-01/02, recorded in OPERA_2D_REBUILD addendum 1) that the
1672x941 generator output promoted at 16:9 full-bleed IS acceptable for
these single-screen career stages — the same precedent as the twelve
district paintings now shipping. Deliver the twelve `stage_<career>`
scenes per the P3-04 shared contract (proscenium family, stations at the
thirds, clear center interaction zone, audience band <= bottom 15%) with
the recorded draft corrections (pop-star pad mapping coral=left/
teal=right/plum=up/cream=down; painter pots plum->coral->cream). Native
>= 2048x1152 masters remain PREFERRED when the generator allows; 1672x941
is the accepted floor. Consumer: `OperaWorldBackdrop2D.set_stage()` swaps
to `assets/opera/worlds/backdrops/stage_<career>.png` when present.

## SET 5 — Walk-cycle upgrade for the two base imps (small, high-reuse)

`imp_mischief_{hop_a,hop_b}.png` and `imp_captain_{hop_a,hop_b}.png` —
the co-op careers' crews and any career whose costumed set has not landed
yet keep using the base imps; a two-frame hop stops them skating along
the route. Same spec as 1.4.

---

## Delivery order and why

1. SET 1.1-1.3 (fixes + dizzy overlay) — removes the only visible defects.
2. SET 2 (three files) — completes the design-language bar everywhere.
3. SET 3 (nursery trio) — job 13 reaches parity.
4. SET 1.4 (60 states) — full per-costume animation.
5. SET 4 (12 stage scenes) — finale spectacle.
6. SET 1.5 + SET 5 — travel poses, base-imp hops.

Report per the standard delivery-report contents (branch + SHA, counts,
scores, promoted paths, deferred items, license rows, CI run URL).
