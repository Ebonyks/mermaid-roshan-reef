# Claude Fable handoff — ornate shell UI and control repair

Date: 2026-07-29
Branch: `codex/ornate-shell-ui`
Base at task start: `origin/dev` (`5652a948`)

## Recovered visual source of truth

The remembered purple, shell-heavy interface is the selected July 19 prototype family in:

- `gen2/ui_prototypes_2026-07-19/pause_overlay_v1_1024x576.png`
- `gen2/ui_prototypes_2026-07-19/intro_story_v1_1024x576.png`
- `gen2/ui_prototypes_2026-07-19/hud_navigation_v1_1024x576.png`
- `gen2/ui_prototypes_2026-07-19/craft_studio_v2_1024x576.png`
- `gen2/UI_PROTOTYPE_REVISIONS_2026-07-19.md`
- prototype commit `75cf9b67` (`Add audit-backed UI image prototypes`)

The important language is deep-violet contouring, lilac/pearl-blue surfaces, scallop crests, pearls, and sparse coral/gold action accents. The prototype PNGs remain references only; they are not flattened into runtime overlays.

## What this branch changes

### Shared visual system

- `scripts/shell_ornament.gd` draws one scalable native scallop crest with ribs, lobes, violet outline, and a pearl hinge.
- `scripts/storybook_ui.gd` adds the recovered purple palette, stronger violet contour/shadow, `add_shell_crest()`, `add_pearl()`, and `adorn_panel()`.
- Shared button styling now propagates the deeper violet language throughout every existing StorybookUI consumer.
- Explicit shell-and-pearl adornment is applied to Pause, intro, craft preview, sticker book, critter book, the Stuffie watch, and the Tamagotchi care sheet.

### Gameplay HUD declutter

- The persistent top-left pearl/star/trophy/critter/medal report card is hidden, restoring the earlier owner-approved declutter from commit `23593f71`.
- The legacy persistent sentence objective is hidden.
- Voice captions remain transient.
- Picture target cards teach a changed target for 3.5 seconds, then disappear.
- Internal labels and saved counters are retained for compatibility; no save key was removed.

### Controls

- The lower-left visible cardinal ring is now a real fixed-center pad. A press on any side creates an immediate movement vector; dragging still works.
- Movement, action, and Pause use priority `_input` routing so a visible fixed control cannot be swallowed by another GUI Control. World taps still use `_unhandled_input`, preserving overlay ownership.
- The same priority route supports real touchscreen events and desktop mouse events.
- Pause also fires on `button_down`, so a child sliding off before finger-up cannot cancel it.
- The Stuffie watch remains at `(858, 22)`, in the upper-right hand area but left of Critter Book and the far-corner Pause button.

### Sky Lagoon action

- `SideScrollStage.walk_tick()` now implements a real no-fail hop with a small analytic vertical arc.
- The promenade medallion reads `JUMP` with no focus, `PLAY` for a highlighted toy/plane, and `ENTER` for the highlighted castle.
- A focused target owns the action edge; otherwise the same edge requests the hop.

## Validation

Static gates:

- `python -m gdtoolkit.parser <all changed .gd files>` — pass
- `python tools/lint_inference.py <all changed .gd files>` — pass
- `git diff --check` — pass

Runtime probes with local Godot 4.7 dev2:

- `probe_touch_router.gd -- --touch` — `TOUCH_ROUTER|ALL OK`
- `probe_ui_system.gd` — `UI_SYSTEM|RESULT|ALL OK`
- `probe_l2.gd` — `LAGOON25D|ALL: OK`
  - real hop measured `jump_y=0.288` on its first frame
  - PLAY/ENTER label focus contract passed

The local dev2 binary emits a known core `Dictionary::_unref` diagnostic during headless teardown, but all trusted probes exit 0 after their all-OK result. CI should run the project-pinned stable toolchain before integration.

## Fable continuation rules

- Extend `StorybookUI` components; do not add isolated one-off visual systems.
- Keep decoration sparse around functional targets. The child should see actions first, ornament second.
- Do not reintroduce persistent progress totals into free roam. Put collection detail inside its relevant book/menu.
- Keep the Stuffie watch inset and keep its Tamagotchi care actions picture-first and at least 110×110.
- Do not ship any prototype raster as a complete runtime UI screen.
- No protected book, voice, or friend art was modified and no new generated art was needed.
