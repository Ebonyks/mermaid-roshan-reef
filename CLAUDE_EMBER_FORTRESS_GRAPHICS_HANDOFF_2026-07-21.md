# Claude handoff — Ember Fortress regenerated graphics

## Mission and status

Maintain or continue the full graphics regeneration of the generic, IP-safe
volcanic world internally requested as “Bowser World.” The shipped identity is
**Ember Fortress**. Do not introduce Nintendo, Mario, Bowser, Zelda, or other
branded characters, symbols, architecture, music, UI, or terminology.

The 2026-07-21 pass inventoried 42 active visual roles, replaced/rebuilt all
roles below 4/5, and produced a 39-GLB deterministic Blender kit. The candidate
has Godot 4.4.1 Forward Mobile runtime evidence and is agent-rated **4/5**.
Only the owner may award 5/5.

## Location

- Work branch: `codex/bowser-world-graphics`
- Worktree: `.worktrees/bowser-world-graphics`
- Original base: `origin/dev` at `0a04efff`
- Integration target after exact-HEAD green CI: `dev`
- Never commit, merge, or push `master` directly.

Run `tools/claude_ember_fortress_handoff.ps1 -Strict` from this worktree to
print this packet with live branch, HEAD, status, evidence, and verification
metadata. The helper is read-only.

## Read first

1. `AGENTS.md` and `SECURITY.md`
2. `assets/ART_GENERATION_CONTRACT.md`
3. `assets/OBJECT_GENERATION_AUDIT_LOG.md` entry A17
4. `EMBER_FORTRESS_GRAPHICS_AUDIT_2026-07-21.md`
5. `audit/ember_visual_inventory_2026-07-21.csv`
6. `scripts/ember_fortress.gd`, `scripts/dungeon_art.gd`, and
   `scripts/probe_ember.gd`

## Authoritative assets and evidence

- Runtime kit: `assets/ember_fortress/*.glb` (39 files)
- Editable source: `assets_src/blender/ember_fortress_kit.blend`
- Reproducible generator: `tools/build_ember_fortress_kit.py`
- Metrics and isolated QA: `assets_src/blender/qa_ember_fortress_kit/`
- Runtime Mobile captures: `audit/ember_runtime_2026-07-21/`
- Runtime capture probe: `scripts/probe_ember_art.gd`
- Gameplay/state probe: `scripts/probe_ember.gd`

The final measured library is 25,038 triangles and 1,901,852 bytes, with no
textures. `ember_planet.glb` is the largest asset at 5,516 triangles. Runtime
does not instantiate the entire library at once.

## Routing and behavior contracts

- `DungeonArt.PATHS` is unchanged for ordinary dungeons.
- `DungeonArt.EMBER_PATHS` is selected only when the progress field is
  `ember_progress`; do not leak the theme into other rooms.
- The authored planet is a centered visual shell around the exact analytic
  `PLANET_R = 40` gameplay surface. Do not ground-align it like an ordinary GLB.
- Five lantern bodies use separate authored flames and beacons. Unlit/lit and
  persistent sticker states must stay visually distinct.
- The Great Gate is an open frame plus a separate opaque modeled flame veil;
  opening hides the veil, not the frame.
- The King stays beside the approach line and must not occlude the gate.
- The home ring stands upright over its authored south-pole plaza.
- Ember stepping stones intentionally use 0.82 scale; the shared default still
  uses its previous scale.
- Imported Blender child names can receive suffixes. `DungeonArt.find_part`
  and pictogram selection deliberately accept deterministic wildcard suffixes.
- Speedy shows at most the nearest lantern OmniLight and hides King/avatar
  detail lights. Do not add OmniLights without a new Speedy cull contract.

Gameplay invariants: five lanterns; gate opens only at five; six-room dungeon;
independent Ember save keys; no fail states; friendly lava/geysers; always
available home ring; one-finger controls; voice plus visual guidance; analytic
movement with no mass physics bodies.

## Score and review rules

- No runtime evidence: maximum 2/5.
- Primitive focal art, clipping, inversion, state ambiguity, or camera
  occlusion: maximum 1/5.
- Forward Mobile runtime evidence plus correct role/scale permits 4/5.
- Only owner acceptance permits 5/5.

Do not use isolated renders as substitutes for runtime composition. Preserve
all rejected lessons recorded in the audit: far-plane sky clipping, spherical
ground-alignment, gate/King occlusion, floating flames, edge-on home ring,
polar triangle fan, tiny stepping stones, and overlapping pictogram children.

## Verification and continuation

Required before any further push or dev integration:

```powershell
python -m gdtoolkit.parser scripts/combat_arena.gd scripts/dungeon_art.gd scripts/dungeon_level.gd scripts/dungeon_puzzle_room.gd scripts/ember_fortress.gd scripts/probe_ember.gd scripts/probe_ember_art.gd
python tools/lint_inference.py scripts/combat_arena.gd scripts/dungeon_art.gd scripts/dungeon_level.gd scripts/dungeon_puzzle_room.gd scripts/ember_fortress.gd scripts/probe_ember.gd scripts/probe_ember_art.gd
git diff --check
godot --headless -s scripts/probe_ember.gd
```

Then run the complete trusted suite through `scripts/ci.sh` or the existing
probes workflow. A green run must correspond to the exact work-branch HEAD.
Reconcile with current `origin/dev`, re-run gates if HEAD changes, merge into
dev, and push dev only after the exact integration commit is green.

Do not modify protected book art, family voices, friend cutouts, or Roshan’s
identity assets. No old asset needed a backup because this pass adds a dedicated
runtime directory and changes routing; shared GLBs remain byte-identical.
