# Human Art Review Audit - 2026-07-16

## Correction

This audit supersedes the conclusion in `ART_RESIDUAL_LOW_SCORE_AUDIT.md` that there were no active, automatically replaceable 0-2/5 art roles. That conclusion was not supported by gameplay-level visual review. Earlier audits frequently scored the existence, routing, or intended style of an asset instead of the appearance of the finished object in the Mobile renderer.

The current build contains many visible 0-2/5 assets and several whole areas whose art remains at prototype quality. The largest remaining failures are the castle architecture and interiors, Sky Lagoon castle and clouds, Butterfly World, kart presentation, generic picture-game art, and repeated reef dressing.

Detailed item-level results are in `audit/human_art_ledger_2026-07-16.csv`. After the verified Dungeon Art V2 pass, the audit records **88 roles: 8 at 0/5, 38 at 1/5, 25 at 2/5, 15 at 3/5, and two protected book assets at 5/5**. That leaves 71 active or pipeline roles at 0-2/5. Thirteen dungeon roles advanced to provisional 3/5 through Mobile gameplay captures; none advanced to 4/5 without owner review. Protected book and family assets are not replacement targets, even when their runtime presentation needs repair.

## New Scoring Gate

Scores apply to a runtime role, not merely its source file.

| Score | Required evidence |
|---|---|
| 0 | Missing, broken, corrupt, or unmistakably debug/prototype representation. |
| 1 | Functional placeholder: basic primitive, flat slab, generic symbol, severe anatomy failure, or composition that obscures play. |
| 2 | Usable draft with recognizable intent, but generic modeling, weak texture, repetition, poor silhouette, or inconsistent rendering. |
| 3 | Cohesive production candidate that works in one verified gameplay view but still has visible polish or variation issues. |
| 4 | Passes representative near, mid, and gameplay-distance Mobile screenshots; correct silhouette, material response, scale, composition, and repetition behavior. |
| 5 | Book-source asset preserved exactly, or a production asset that is both exceptionally faithful and validated throughout its actual use. |

Hard caps:

- A routed or generated candidate without runtime screenshots is capped at 2/5.
- A focal object built mainly from unmodified engine primitives is capped at 1/5.
- A repeated crossed-card or billboard family is capped at 2/5 until mass-placement review passes.
- Texture quality and model quality are scored separately. A painted texture cannot make a box-built focal prop pass.
- A family score cannot hide a poor member. Every distinct runtime role gets its own row.
- Any asset with clipping, camera occlusion, inverted placement, or bloom-obscured readability is capped at 1/5 in that role.
- Human review is required before promotion to 4/5 or 5/5.

## Runtime Findings

### Reef Hub: 1/5 overall

The hub is overexposed and visually congested. Large quantities of repeated crossed-card coral and foliage create nearly identical silhouettes, severe overdraw, and weak depth. Bright portal effects and white clipping obscure Roshan and the focal route. The underlying generated coral can be useful source material, but the current mass-placement system is not a production presentation.

Highest priorities: rebalance exposure and emissive values, replace repeated card masses with several authored low-poly clumps, establish near/mid/far density rules, and remove props from camera and navigation sightlines.

### Sky Lagoon: 1/5 overall

The castle reads as cylinders, boxes, and cones with flat fills. Clouds have clustered tops but dark disc-like undersides. The rainbow beam dominates the world, terrain is sparse, paintings behave like freestanding slabs, and object scale is inconsistent. These are focal assets and should have failed the former audit.

Highest priorities: authored castle silhouette kit, modeled cloud family with soft toon undersides, restrained rainbow path treatment, snow/rock terrain breakup, and deliberate composition passes for every landmark approach.

### Castle Hall and Wings: 0-1/5 overall

Architecture is predominantly large box primitives. Stairs are floating slabs, walls and ceilings are broad monochrome planes, and many room props are assembled from boxes, cylinders, or spheres. The incoming kitchen textures are credible 2-3/5 surface drafts, but the kitchen room remains 1/5 because the stove, counter, pans, teapot, kettle, and table are primitive constructions.

Highest priorities: modular authored wall/arch/stair/column kit, modeled kitchen set, modeled bedroom and bath sets, reduced bloom, and room-specific silhouette language.

### Castle Stars: 1-2/5

Dream, crown, and chamber stars are code-built layered prisms. They are recognizable but lack authored profiles, texture detail, and a validated focal presentation. No star receives 4/5 merely because a new route exists.

### Butterfly World and Gates: 1/5 overall

Butterfly World is a sparse sphere with repeated palms and weak environmental storytelling. The home-gate capture showed the planet occluding the view and the gate reading as a slab-like construction at an incoherent orientation. Gate wings need book-derived butterfly structure, a readable body and hinge, and inspection from both sides during transition.

### Dungeon and Combat: provisional 3/5 overall

Dungeon Art V2 replaces the focal blockout geometry with a batched shell-stone arena, coral-glass buttresses, modeled imps, a complete dragon-turtle, shell door, basket, pedestals, lanterns, statues, stepping stones, and eleven sculpted pictograms. Combat, both boss phases, sequence, lantern, and repeated pair-card states were captured in the Mobile renderer. The pepper projectile remains a 1/5 transient token, and every rebuilt role remains capped at 3/5 until owner review covers near and mid distances across all room palettes.

### Kart World: 1/5 overall

The selection area has severe bloom, oversized UI, repeated coral cards blocking the view, generic pads, and inconsistent prop scale. Several vehicle sources may be acceptable candidates, but their showcase, track dressing, boost language, barriers, and finish treatment need a full composition and material pass.

### Picture-Game Textures: 1-2/5

`coal.png`, `star.png`, `sun.png`, `tree.png`, `xtree.png`, `k_bush2.png`, `fish_body.png`, and `fish_fins.png` are generic low-poly renders or simplistic shapes. They do not qualify as provisional 4/5 art. The carrot and watering can are book-source exceptions and must remain unchanged. Cat parts are protected from auto-generation. The butterfly requires a complete, animation-ready dorsal design derived from the book butterfly language.

## Incoming Development Wings

| Wing | Branch | Gate result | Required action |
|---|---|---:|---|
| Alpine house interiors | `origin/codex/alpine-house-interiors` | Hold at 1-2 | Capture every room; score architecture, furniture, lighting, and repeated props separately before merge. |
| Kitchen textures | `origin/codex/kitchen-textures` | Textures 2-3, room 1 | Keep texture candidates, rebuild primitive kitchen models, then perform Mobile room review. |
| Dungeon/adventure | merged | 3 candidate | Review Dungeon Art V2 in the shipped build; polish owner-rejected roles and replace the remaining pepper token. |
| Kart expansion | merged | 1-2 | Rebuild showcase composition and track language; verify each vehicle independently. |
| Castle differentiation | merged/in progress | 1-2 | Color changes do not satisfy differentiation; require authored silhouettes and surfaces. |
| Northern/undersea additions | active branches | Unverified, max 2 | Add runtime captures to this same probe before any art score is promoted. |

## Rebuild Order

1. **P0 focal landmarks:** Sky Lagoon castle, castle hall architecture, butterfly gates, castle stars, and cloud family.
2. **P0 new gameplay review:** owner-review Dungeon Art V2 across every room palette; polish rejected roles and replace the remaining pepper token.
3. **P1 readability:** reef exposure, portal bloom, card density, kart showcase, and camera occlusion.
4. **P1 authored prop sets:** kitchen, bedroom, bath, throne, stairs, railings, and castle wall modules.
5. **P2 texture and sprite families:** picture-game fish, trees, sun, coal, star, bush, ornaments, and animation-ready butterfly.
6. **P2 environmental variation:** coral clumps, kelp, seagrass, snow terrain, palms, rocks, and track dressing.

Every replacement keeps its previous source in the existing dated `backups/art_pre_*` structure, with a manifest mapping active path to backup path. Book assets, family voices, friend cutouts, the carrot, and the watering can remain source-locked. Stuffed animals and the craft cat remain excluded from automatic generation.

## Audit Tooling Change

`scripts/probe_human_art_audit.gd` captures representative runtime views for the reef, Sky Lagoon, castle hall, stars, Butterfly World, dungeon rooms, and kart world. Future visual wings must add captures before merge. Static primitive counts are only a risk detector; screenshot review on the Mobile renderer is the acceptance gate.

The clean-worktree import also exposed numerous corrupt or invalid provenance images under `gen2/generated` and `gen2/turnarounds`. That did not prevent all captures, but it can omit referenced models and makes a clean-machine visual audit unreliable. Those files need a separate integrity audit and quarantine; they must not be interpreted as passing assets because an already-imported cache exists elsewhere.
