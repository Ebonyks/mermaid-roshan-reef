# GENERATION 2 REBUILD — master work order
# Thesis: Gen-1 was licensed scaffolding around family art. Gen-2 is a game
# where every asset is family-made or generated from the family's own style.
# KEEP: game design, world layout, minigame mechanics, all code, the probe
# suite, and every Mermaid Roshan asset (book art, voices, photos, Roshan's
# model + skins, friend cutouts, kid artwork, finale track).
# DISCARD (eventually — see strangler-fig rule): every third-party asset —
# the aquatic GLB pack, ambientCG terrain, Kenney nature/models, synth music
# loops, stock SFX, box-built geometry materials.

## Two architectural moves that make the rebuild safe and repeatable

**1. Strangler-fig replacement, never big-bang deletion.** Gen-1 assets are
the playable placeholders while gen-2 fills in role by role. The game must
boot and pass the full probe suite after EVERY commit of this entire effort.
Deleting a gen-1 file is the LAST commit of its role's replacement, never the
first. A half-rebuilt game that still plays end-to-end every night is the
whole point of having the bots.

**2. The Asset Registry (the decoupling that makes gen-3 cheap).** Today
main.gd hard-codes file paths (`_aq("ClownFish")`, `load("res://assets/...")`).
Gen-2 inserts one indirection: `assets/registry.json` mapping ROLE → file +
metadata (kind: sprite/flipbook/mesh/audio, frames, fps, scale, tint). Code
asks for roles ("small_fish_a", "reef_rock_large", "music_world"); the
registry answers with whatever the current generation provides. Swapping an
asset — including every future piece of Roshan's artwork — becomes a JSON
edit, not a code change. This is the mechanism for "continuous substantial
rebuilds" and continuous kid-art integration, permanently.

## What survives from the existing work orders
- **RACE_FEEL_WORKORDER + probe_race_feel** — untouched; it's design and
  physics, asset-agnostic. Sparkle Drift proceeds independently.
- **WW_STYLE_PIPELINE** — the five-layer 2.5D architecture, atlas/MultiMesh
  tech, sprite-life shader, screenshot-regression harness all survive.
  The GLB toon-bake lane (Lane A) is RETIRED as a style source — its assets
  are leaving — but imposter_bake.gd stays in tools/ as a structure-reference
  generator until the last GLB role is replaced.
- **ASSET_ENGINE_WORKORDER** — PROMOTED: Nano Banana generation is now the
  primary creation engine, not a refinement lane. The continuity argument is
  now load-bearing: the book art came from this model family, and gen-2's
  entire look derives from the book art. Lane C (kid-art ingestion) unchanged
  and eternal.
- **ANIMATION_INVESTMENT_WORKORDER** — the flipbook-from-GLB baker (A0/A1)
  is RETIRED with its source assets. The authoring lane (A2–A6) is promoted:
  gen-2 creatures are generated sprites + Spine (or Godot-native) rigs. The
  life system layers (ecosystem, reactivity, tap-to-delight) survive intact —
  they were always asset-agnostic.

## Phases

**G0 — Inventory & dependency map (mechanical, one session).**
Walk assets/; classify every file KEEP (family/original), DISCARD (3rd-party),
or TOOLING. Grep all scripts/scenes for every `res://` reference; emit
`gen2/dependency_map.json`: file → referencing lines → proposed role name.
Gate: zero unclassified files; the map is the rebuild's work queue.

**G1 — Asset Registry.**
Implement `AssetRegistry` (autoload, ~120 lines): `get_scene(role)`,
`get_sprite(role)`, `get_stream(role)`, with per-kind loaders (flipbook roles
return SpriteFrames). Mechanically rewrite every hard-coded path in the
dependency map to a role lookup; registry v1 points every role at its GEN-1
file. Gate: full probe suite green with zero behavior change — this commit
proves the indirection is invisible.

**G2 — Gen-2 style bible (family sources ONLY).**
Rebuild style_kit/ exclusively from: book art pages, Roshan's sprite/skins,
kid artwork, family photo palette pulls. Re-derive PROMPT.md on the free
tier until the human approves a 6-subject board. The WW brightness and 2.5D
staging remain as *composition* rules; the surface style is now 100%
Mermaid Roshan. Gate: human sign-off; PROMPT.md v2 committed.

**G3 — The cast list (role schema for the whole game).**
From the dependency map, write `gen2/roles.md`: ~25 flora roles, ~15 creature
roles (with required animations: swim, idle), 6 terrain/surface materials,
geometry kit roles for castle/play-place, 11 music slots, ~12 SFX slots,
UI/FX roles. Each role: gameplay function, size on screen, animation need,
generation lane (Nano Banana / kid-art / family-recorded / authored).
Gate: every DISCARD file in the map is covered by exactly one role.

**G4 — Level 1 rebuild (worst offender first; budget cap $10).**
For each reef role: generate (bake→structure ref while GLBs still exist, else
pure PROMPT.md) → rig/animate where the role demands it → atlas → registry
flip → device review by the human → gen-1 file deleted. Work in role batches
of ~6; probes + screenshot regression after each batch. Terrain: generated
tileable painterly textures replace ambientCG (same UVs, registry-served).
Gate per batch: probes green; final gate: zero DISCARD files referenced by
Level 1, orbit-camera sweep shows the gen-2 look everywhere.

**G5 — Sky Lagoon + castle rebuild (cap $8).**
Same recipe with their palettes. Castle geometry: generated texture kits on
the existing box layout first (cheap, preserves all trigger coordinates);
bespoke sprite architecture cards for beauty walls. The wall-picture frames
keep displaying book art — they were always gen-2 native.

**G6 — Audio, the family way.**
The gen-2 thesis has an audio conclusion worth saying out loud: the human is
a performing singer-songwriter with a ukulele, and finale.ogg already proves
bespoke music belongs here. Proposal: record 3–5 original ukulele beds
(reef/lagoon/castle/race + one lullaby) — the audio equivalent of the book
art, and the strongest possible continuity statement. Claude Code's part:
a `tools/prep_music.py` (trim, loop-point find, loudness normalize, OGG
encode, registry entry) so a phone recording becomes a game track in one
command. CC0 tracks remain the interim placeholder via the registry.
SFX: generated/recorded foley + the existing family voice pipeline; expand
voice lines to cover every objective (still the highest-value audio work).

**G7 — The ledger collapses (the victory condition).**
When the last DISCARD file leaves, ASSET_LICENSES.md shrinks to: family
originals (all rights reserved), AI-generated-from-own-style entries with
archived prompts, tool licenses (Spine runtime if chosen), and the Godot
engine. Verify Gemini output terms for LLC commercial use; date the check.
Gate: `ci.sh` green from clean clone; a repo-wide grep finds zero references
to any discarded path; export size reported (expect it to DROP).

## Guardrails
- The probe suite is the continuity spine of the whole rebuild: it encodes
  the game design being kept. Any probe regression during an asset swap means
  the swap broke behavior (usually a collision proxy or scale) — fix the
  asset, never the probe.
- Family assets are read-only inputs forever; originals live in assets_src/.
- Budget caps enforced by gen_sprite.py's ledger; expected total spend for
  the full gen-2 art pass: $18–25.
- Scale/collision contract per role in roles.md (footprint radius, pivot) so
  gameplay tuning survives any future generation swap untouched.
