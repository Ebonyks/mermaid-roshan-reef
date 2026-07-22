# Ember Fortress 2D concept restart audit — 2026-07-22

## Outcome

The previous Codex-authored procedural Blender pass is rejected as the
production chain. It created meshes before an approved 2D design stage. None
of those GLBs, Blender sources, generators, runtime integrations, or claimed
replacement scores are present on this branch or eligible for `dev`.

This restart inventories all 42 active visual roles in the original generic,
IP-safe volcanic world called **Ember Fortress**. The 38 roles needing design
or presentation work are covered by six new 2D production boards. Four
already-valid/protected roles remain unchanged. Claude owns the Blender build
from these boards; Codex has not created replacement meshes in this chain.

## Evaluation scale

- **1/5:** broken placement/state, engine primitive, or unreadable focal role.
- **2/5:** functional but generic, repetitive, weakly themed, or unproved.
- **3/5:** coherent and readable but missing focal finish or evidence.
- **4/5:** authored, correctly scaled, and inspected in representative Godot
  4.4 Forward Mobile gameplay views.
- **5/5:** owner-accepted shipped result only.

The new boards are E1 design evidence. They are not runtime replacements and
receive no numeric candidate art score. The baseline scores and every required
gate are recorded in `audit/ember_visual_inventory_2026-07-22.csv`.

## 2D design package

All boards are original OpenAI built-in image-generation outputs, normalized
to a 1024-pixel longest edge, stored under
`assets_src/concepts/ember_fortress_claude_2026-07-22/`, and excluded from
runtime use by the existing `assets_src/.gdignore` boundary.

1. `01_world_layout.png` — planet, lava paths, polar plazas, sky and sparks.
2. `02_citadel_architecture.png` — four towers, rampart, flag, gate and veil.
3. `03_landmark_turnarounds.png` — sentry, Ember King and ash moon.
4. `04_overworld_props.png` — lantern states, beacon, geyser, crags, crystals,
   and upright home ring.
5. `05_dungeon_kit.png` — arena, door, puzzle and dressing kit.
6. `06_combat_kit.png` — imps, dual-state boss, basket and projectiles.
7. `contact_sheet.png` — review-only composite of the six modeling boards.

`PROMPTS.md` records the normalized production prompt set. Image labels are visual aids; the
numeric contracts in the ledger and export manifest override generated text.

## Scope and scale findings

The runtime scope is a spherical 40 m analytic-radius world plus a six-room
dungeon. The concept boards explicitly correct the earlier baseline defects:

- authored 80 m planet silhouette with broad phone-readable lava paths;
- 20 m north citadel plaza and 15 m south portal plaza;
- four non-identical 5.4–5.85 m tower silhouettes;
- 9 m open gate frame with a separate 6.2 m removable flame veil;
- 5.8 m King designed to stand beside the gate approach;
- lantern flame registered inside its 3.2 m assembly, with shape-distinct
  unlit/lit states and a 20 m distant beacon;
- upright 9.5 m home ring instead of an edge-on torus;
- 54 m source arena, large stepping stones, thick route markers, and exactly
  one visible pictogram at a time;
- fire and ice projectiles distinguished by shape as well as color;
- an original dual-state boss with no branded shell, horns, or franchise cues.

## Protected and retained roles

Roshan's active avatar appears in overworld and dungeon rows but is protected
and remains byte-identical. The existing overworld HUD/pause and dungeon
pointer/HUD already score 4/5 for phone readability and remain unchanged.
Book art, family voices, friend art, wardrobe identity assets, and all other
worlds are outside this restart.

## Completion boundary

The work is now at `concept_ready`, not `runtime_pass`. Claude must produce the
39 exports in `CLAUDE_EXPORT_MANIFEST.csv`, retain editable `.blend` sources,
provide isolated multi-angle/state renders, and integrate them through an
Ember-only route without overwriting shared dungeon assets. Only representative
Forward Mobile captures can make a role eligible for 4/5; only owner review can
award 5/5.

No push to `dev` is authorized from this concept branch until Claude's exact
integrated head passes parser/lint, Ember probes, the complete trusted suite,
and runtime visual review after reconciliation with current `origin/dev`.
