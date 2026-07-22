# 3D Art Conversion Manifest

_Started: 2026-07-14_

This manifest turns the full art audit into a controlled future mesh queue.
Images in `assets_src/style_review_batch_04/` are concept masters and review
references. They are not runtime meshes. Each conversion must preserve the
source-art family, use Mobile-friendly geometry, and keep gameplay contracts
intact.

## Conversion states

| State | Meaning |
|---|---|
| `PROTECTED` | Source/family/child-owned art. No automatic regeneration or mesh reinterpretation. |
| `ROUTED` | A stronger approved GEN2 mesh/card already serves the runtime role. Legacy source remains fallback-only. |
| `CONCEPT_READY` | A new 2D master is staged and can be modeled after owner review. |
| `MODEL_PENDING` | The concept exists, but geometry, rigging, UVs, collision, or animation still need work. |
| `IMPLEMENTATION_PENDING` | The concept is approved in principle but needs splitting, shader/material wiring, or screenshot review. |
| `MOBILE_QA` | A production mesh is built and routed with fallback behavior; Godot Mobile import and gameplay screenshot review remain. |
| `RETIRE` | Keep only for historical or missing-file fallback; never add a new consumer. |

## Mesh queue

| Priority | Source role | Master/reference | State | Conversion notes |
|---:|---|---|---|---|
| P0 | Legacy kart coral, rock, shell, sand dollar, fish, and seaweed | `assets/props/gen2/*.glb`, `assets/props/gen2/*.png` | ROUTED | Preserve role aliases, child-readable scale, and existing collision/animation contracts. |
| P0 | Butterfly World legacy butterflies | `assets/props/gen2/butterfly_story.glb` | MOBILE_QA | Complete paired fore/hind wings and two runtime-driven pivots; cards and legacy GLBs are fallbacks. |
| P0 | Anemone | `assets/props/gen2/anemone_story.glb` | MOBILE_QA | Rooted joined mesh, broad base, ten countable tentacles, no face; wired to garden, cavern, and meadow roles. |
| P0 | Urchin | `assets/props/gen2/urchin_story.glb` | MOBILE_QA | Joined radial-spine mesh, non-character, no eyes or mouth; wired to meadow and fairy hazards. |
| P0 | Giant ambient fish | `assets/props/gen2/giant_fish_story.glb` | MOBILE_QA | Anatomical whale silhouette with paired fins, dorsal fin, horizontal flukes, and one tail action. |
| P0 | Monster truck | `assets/vehicles/monstertruck_story.glb` | MOBILE_QA | New rounded matte toy mesh is the preferred kart body; old rover remains missing-file fallback. Verify yaw, paint, and collision in Mobile. |
| P1 | Fish craft layers | `assets/mg/fish_body.png`, `fish_fins.png`, `fish_line.png` | MOBILE_QA | Registered color layers are live. All three images may be redeveloped together; preserve only the separate body/accent/line customization contract. The GEN2 clownfish remains the preferred spawned 3D friend. |
| P1 | Bush, flowers, trees, seed stages, coal, sun, and star | `assets/mg/*.png`, source in `assets_src/blender/low_score_batch_02.blend` | MOBILE_QA | Twenty-one Blender models feed touch-safe 2D renders; existing filenames preserve growth and placement contracts. |
| P1 | Christmas ornaments | `assets/mg/orn1.png`-`orn5.png`, `xtree.png` | MOBILE_QA | Five independent ornament models/renders; the tree is now separate, empty, and has no baked topper. |
| P1 | Kart checker and boost | `assets/kart/finish_banner.png`, `boost_ribbon.png` | MOBILE_QA | Runtime sprites preserve finish/ramp semantics. Decorated rock clusters were rejected as hazards because their stars and shells conflict with pickup language. |
| P1 | Fairy Pond backgrounds, shadow bugs, leaf shield, and Fairy Flower growth sequence | V3 continuous backgrounds in `assets_src/fairy_v3/concepts/*.png`; V2 subject masters in `assets_src/fairy_v2/concepts/*.png`; runtime reliefs in `assets/fairy/models/*.glb` | MOBILE_QA | Three texture-harmonized overhead pond plates and nine Blender-importable unlit reliefs are live. Dawn, twilight, and boss water now share grain, bank scale, contour weight, palette, and zero-delta adjoining edge rows. The boss uses seed, sprout, closed bud, opening blossom, and giant full purple bloom states with matching leaves. Analytic hitboxes and forgiving timing are unchanged; `probe_fairy_art.gd` protects import/geometry budgets and `tools/audit_fairy_art_v2.py` protects phase luminance, palette, and seams; Mobile screenshots remain the owner-review gate. |
| P2 | Tropical leaf/frond family | `assets/terrain/leaf.png` | MOBILE_QA | Approved broadleaf is live on crossed swaying cards. Additional fern/fan clumps remain optional 3D polish, not a score-2 blocker. |
| P2 | Castle/furniture/park/ship raw kit surfaces | `ART_REMEDIATION_BATCH_03.md` material sheets and current GEN2 references | MODEL_PENDING | Shared trim vocabulary, rounded edges, matte paint, no photoreal PBR. |
| P2 | Galaxy fruit/crystals/beetles | `ART_REMEDIATION_BATCH_03.md` candidates `012`, `013`, `029` | MODEL_PENDING | Retain distinct functional identity; use painted facet and shell materials rather than glossy generic pack skins. |
| P2 | Craft kitty/birdie | Protected owner-derived references plus current GEN2 rigged models | PROTECTED | Improve shader and mesh presentation only with source-faithful review; no automatic redesign. |

## Per-mesh acceptance gate

Before a candidate moves from this manifest into `assets/`:

1. The concept is scored at least 4/5 against `ART_STYLE_GUIDE.md`.
2. The silhouette is complete and anatomically/functionally correct from the
   gameplay camera and the expected interaction side.
3. Materials are matte-to-satin, with broad painted color regions and navy,
   plum, or warm-brown ink. No chrome, noisy micro-PBR, or accidental faces.
4. The mesh uses a stable scale, simple collision, and Mobile-safe draw calls.
   New textures are <=1024px on the longest side or power-of-two.
5. Any animation or layer contract is preserved and tested. A concept image
   cannot replace a rig, collision body, pickup holder, or line-layer contract.
6. The source, license, URL, and modifications are added to
   `ASSET_LICENSES.md` in the same change.
7. A Mobile screenshot at gameplay distance is reviewed before the old role is
   retired.

## Promotion record

Batch 01 promotes five Blender-authored meshes into preferred runtime routes;
details and measured budgets are in `ART_3D_BATCH_01.md`. Every route preserves
its previous asset as a missing-file fallback. The meshes remain in `MOBILE_QA`
rather than final acceptance because this environment has no Godot binary and
cannot produce a Mobile-render gameplay screenshot.

Batch 02 promotes 23 Blender-rendered picture-game PNGs while retaining their
existing touch and layer contracts; details are in `ART_3D_BATCH_02.md`. The
source scene contains 21 editable models. The Christmas tree is now empty, and
its five ornaments remain detachable. This family remains in `MOBILE_QA` until
the snowman, garden, trampoline, and Christmas screens are reviewed on-device.

Protected book art, legacy character models, family cutouts, and child-owned
toys were not transformed. Future promotion remains reviewable so a concept
image cannot silently replace rig, save, touch, collision, or animation
contracts.

Runtime Batch 03 promotes the registered craft-fish fills, fin-shaped rainbow
control, broadleaf card, kart finish banner, and kart ramp ribbon. It also
retires the visible HDR sky and glossy beach-ball consumers in favor of
Mobile-safe matte procedural treatments. See `ART_RUNTIME_REMEDIATION_BATCH_03.md`.

Fairy Pond V2 promotes three generated overhead pond plates, three distinct
shadow-bug species, a matching leaf-shield relief, and five authored Fairy
Flower growth-state reliefs. The GLBs preserve the illustrated silhouette with
real front/back/edge geometry and an overhead-camera contract; gameplay remains
analytic. The family stays `MOBILE_QA` until the new phase captures in
`probe_human_art_audit.gd` are reviewed under the Mobile renderer.
