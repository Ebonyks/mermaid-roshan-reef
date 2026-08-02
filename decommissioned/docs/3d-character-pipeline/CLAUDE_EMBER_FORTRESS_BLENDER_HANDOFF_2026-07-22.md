# Claude handoff — Ember Fortress Blender production

## Mission

Build the complete Ember Fortress 3D kit in Blender from the approved 2D
boards in `assets_src/concepts/ember_fortress_claude_2026-07-22/`. **Claude
owns all Blender modeling in this chain.** Do not use Codex-generated meshes,
Blender files, or mesh-generator code from `codex/bowser-world-graphics`.
That earlier chain was rejected because it skipped 2D design approval.

The shipped identity is generic and IP-safe **Ember Fortress**. Do not add or
imitate Nintendo, Mario, Bowser, Zelda, or any other branded character,
architecture, symbol, UI, music, or terminology.

## Read first

1. `AGENTS.md`, `SECURITY.md`, and `assets/ART_GENERATION_CONTRACT.md`.
2. `EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22.md`.
3. `audit/ember_visual_inventory_2026-07-22.csv`.
4. `assets_src/concepts/ember_fortress_claude_2026-07-22/PROMPTS.md`.
5. `assets_src/concepts/ember_fortress_claude_2026-07-22/CLAUDE_EXPORT_MANIFEST.csv`.
6. `EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md` and
   `assets_src/concepts/ember_fortress_claude_2026-07-22/expansion_40/CLAUDE_EXPANSION_40_MANIFEST.csv`.
7. `assets/OBJECT_GENERATION_AUDIT_LOG.md`, especially A17/A18 and R-GOV1–4,
   R-ROLE1–4, R-REP1–3, and R-QA1–8.

Run this first:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\claude_ember_blender_handoff.ps1 -Strict
```

The helper is read-only and validates the six boards, 40 expansion cards, 42
baseline inventory roles, 40 enrichment roles, 79 export rows, image dimensions,
branch/status, and absence of premature runtime GLBs.

## Authoritative design sources

- `01_world_layout.png`: world silhouette, lava routes, polar plazas, sky.
- `02_citadel_architecture.png`: modular architecture and gate states.
- `03_landmark_turnarounds.png`: sentry, King, ash moon.
- `04_overworld_props.png`: lantern assembly/states and world props.
- `05_dungeon_kit.png`: room shell, door, puzzle/dressing props.
- `06_combat_kit.png`: imps, boss states, basket, fire/ice projectiles.
- `expansion_40/*.png`: forty individual architecture, terrain, interactive,
  ambient-life, and guidance cards; review them through `contact_1.png` through
  `contact_4.png` before modeling.

The CSV contracts override any accidental scale text or decorative ambiguity
inside generated pixels. Treat the boards as shape, palette, construction, and
state references—not license to invent extra props, characters, bases, faces,
or scene dressing.

## Production stages

1. **Structural pass:** Model one family at a time in Blender. Use real
   assemblies with clean origins, applied transforms, simple embedded Mobile
   materials, and no runtime textures unless separately approved.
2. **Measured export:** Export each manifest row to
   `assets/ember_fortress/<export_name>.glb`. The core and expansion manifests
   together require 79 exports. Parse dimensions, triangle count,
   mesh islands, materials, textures, and bounds from each GLB; do not trust a
   generator-side manifest.
3. **Isolated review:** Render front, side, back/three-quarter where applicable,
   plus every interactive state. Prove the review catches a known-bad control.
4. **Integration:** Route Ember-only art without overwriting ordinary dungeon
   assets. Shared state remains on `ReefMain`; preserve five lanterns, six
   rooms, no-fail play, voice plus pointer guidance, and save compatibility.
5. **Runtime review:** Capture representative 1280×720 Forward Mobile/Speedy
   frames for arrival, gate closed/open, lantern unlit/lit, geyser, home ring,
   ash moon, combat room, and puzzle room.

Do not batch all 39 exports before reviewing the focal pilot family. The pilot
order is: planet/plazas, Great Gate/frame/veil, lantern assembly, home ring,
arena/door, King, boss. A failed focal pilot blocks the remaining family.

After the core focal pilots pass, build the enrichment kit in four ten-object
families. Respect each row's placement cap and a Speedy runtime cap of 28
visible enrichment instances in the active camera sector. Do not add OmniLights,
transparent smoke, full-screen heat refraction, or collision to ambient flora.

## Non-negotiable design and gameplay contracts

- Planet visual shell remains centered on the analytic 40 m radius world. Do
  not ground-align or vertically offset the sphere.
- Great Gate is an open frame plus a separate opaque modeled veil. Opening
  hides the veil only.
- Ember King is broad, original, shell-free, and staged beside the approach.
- Lantern flames sit inside the bowls; unlit/lit states differ by geometry and
  silhouette, not color alone.
- Home ring stands upright and faces the approach over a quiet south plaza.
- Arena rays lie in the floor plane. Stepping stones remain child-readable.
- Pictogram export contains three individually addressable children and shows
  exactly one at runtime.
- Fire/ice projectiles and boss phases remain shape-distinct under grayscale.
- Speedy permits at most the nearest lantern OmniLight; no new uncapped lights.
- No fail state, damage lava, reading-dependent objective, mass physics body,
  or protected-asset modification.

## Evidence and score rules

- 2D boards are E1 and do not receive a runtime art score.
- Parsed GLBs and isolated Blender renders are E2 and cannot exceed 2/5 for
  runtime quality.
- Representative Forward Mobile runtime evidence permits 4/5.
- Only owner acceptance of shipped runtime views permits 5/5.

Do not call this complete because Blender renders look good or CI is green.
Both runtime composition and owner review remain distinct gates.

## Git integration

Create `claude/ember-fortress-blender` from fresh `origin/dev`. Keep each family
mechanical and reviewable. Never commit to `master`. Before `dev` integration,
reconcile with current `origin/dev`, run parser/inference lint for every changed
GDScript, run the focused Ember probe and complete trusted suite, and require
green CI for the exact reconciled head.
