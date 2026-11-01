# Replaceable costumes on the native Godot rig

Status: `PROPOSED / CANDIDATE`, source-only extension of the [initial rig study](../native_rig_stress_20261031/README.md). The owner commissioned compatibility with two costumes already present in Fashion Designer. This does not integrate the rig into the game or accept a production character. The current demo freeze remains in force.

The two outfits are **coral ballet** and **violet magician**, from `assets_src/fashion_designer/beta_20261025/native/`. Both retain the existing wardrobe motifs, with the original headpiece bitmaps reused directly. Two built-in ImageGen calls supplied fitted garment plates. Only bounded clothing RGB enters the body/tail layers; generated faces, hair, skin, hands, anatomy and fins are excluded. Original sources remain unchanged. See [provenance](provenance.json), [job cards](job_cards.json), and [binding registry](godot/costumes.json).

[Watch the side-by-side comparison](review/costume_comparison.mp4).

Final v5 source checks pass for both outfits and all three actions. All 27 slot mixes match fresh actors in 243 rendered snapshots; 19,248 additional live-instance selection calls preserve pose/eye state. Those calls are state stress, not 19,248 separately captured frames. Original restoration is exact across 291 frames; protected face/hand regions match across 582 costumed frames. Six Aseprite masters round-trip 582/582 RGBA frames exactly. Project regression and publication results remain separately recorded in the evidence receipts and exact-head Actions run.

## Using the demo

Open `godot/project.godot` in exactly Godot 4.7.2-stable with Mobile rendering. Keys 1/2/3 select shoulder-and-arm bend, blink and tail bend. Space pauses; B/M/O choose ballet/magician/original; H/J/K cycle head/body/tail independently. This is an adult review interface outside the game's saves and touch flows. The project references its sibling initial study, which must also be present.

`equip_catalog_ids()` accepts the existing six `head/body/tail_ballet/magician_v1` IDs, and the original `head_original`, `roshan_original`, `tail_original` choices. A partial dictionary changes only its named slots. Invalid IDs and slot mismatches reject the entire request without changing the current outfit. No save is read or written in this experiment.

## What stays shared

There is one Skeleton2D, fourteen Bone2D nodes, one AnimationPlayer and the unchanged initial arm/blink/tail curves. The three original meshes, vertices, triangles, skin weights and rest transforms remain shared. One additional headwear mesh is rigidly bound to Head and covers the union of these two headpieces. Garments never scale the actor, head, arms or bones.

Body and tail use separate RGB-and-mask textures on one Canvas material. The shader starts with the immutable original body, applies the tail mask, then the body mask, and preserves original alpha. A slot change replaces material inputs before the next draw. Headwear changes its texture or visibility. Seven resident clothing textures cover the tested set, including the blank original selection: there is no growing Cartesian texture cache, per-frame CPU image composition, second skeleton, or duplicate actor used for cross-fading.

The fitted clothes intentionally sit over Roshan's original pink/violet undershirt and iridescent tail. The original rainbow fin lobes remain visible. The tiara remains beneath the head accessory, matching the existing layered wardrobe approach. This is not a bare-body reconstruction or an accepted costume silhouette redesign.

## Reusing this setup for another costume

1. Resolve a real Fashion Designer catalog ID, source master, licensing and acceptance scope. Inventory existing garment art before generating a named missing fitting surface. A different character, view, sleeve or topology needs its own coverage; this trial proves only Roshan's tested front view.
2. Keep the shared rest pose, 1024-square coordinates, bone names, shoulder/elbow/wrist sockets and action curves fixed. Record garment registration separately from runtime motion. The final plates use uniform 0.66 scale and recorded offsets, not an internal body warp.
3. Derive body and tail masks that exclude face/hair/skin/limbs/fins. Limit edge extension to the recorded eight-source-pixel feather. Keep garment RGB straight, retain base alpha, and preserve a narrow waist overlap. Outside the fitted cloth, expose the original undergarment rather than stretching edge colors across missing art.
4. Put head accessories on Head with a rigid binding. Verify the actual mesh supports their full alpha footprint; the union mesh here does not guarantee that a larger new hat fits. New sleeves, skirts, capes or hair occlusion may require garment-specific topology and front/back layers. Do not stretch this bodice mesh to force them to fit.
5. Register stable catalog IDs and a compatible rig/view version. Apply all requested slots atomically. Partial changes retain unmentioned selections. The trial explicitly allowlists original/ballet/magician; another theme needs registry, builder and texture-initialization coverage. Unknown and future IDs fail closed in this prototype; a production adapter must preserve unknown saved data while presenting an explicit fallback, without rewriting saves.
6. Render every supported action and its endpoints with the actual Mobile engine. Run the unchanged original geometry and motion auditors, negative controls, source identity checks, lossless archive and Aseprite reopen/export comparison. Test all supported mixed selections against independent fresh instances, repeated live changes, original restoration, invalid requests and deliberately stale uniforms/textures.
7. Inspect the actual figure and detailed chronological sheets on light/dark backgrounds. Machine thresholds do not detect every fabric mapping artifact. Review normal-speed motion, garment/skin occlusion and seams, plus actual phone performance and owner/child acceptance before production adoption.

## The same audit, with extra wardrobe checks

The copied `audit_study.py` and `audit_motion.py` are byte-identical to the initial study. Their gates remain: visible triangle singular values 0.8-1.2, zero inverted visible triangles, bone scale error below 0.00001, rigid-head distance error below 0.01 px, one connected figure above the existing 12-pixel component floor, no frame-edge alpha, exact sampled loop endpoints, and the same source-relative eight-pixel hole allowance. Motion limits remain below 140 degrees/second and 650 degrees/second squared, attachment alpha above 192, one-hot eyelids and at least two fully closed blink frames at 30 fps. Slit, detached-piece, scaled-head and pose-pop negative controls remain mandatory.

Each costume gets all three clips at 30 fps: 97 arm, 73 blink and 121 tail samples, including matching endpoints. Each gets 120 cycles sampled at 15/24/30/60/120 Hz and 57,744 interleaved clip seeks. The added swap audit compares 243 rendered snapshots covering all 27 three-slot combinations, three actions and three action times against independently constructed fresh actors. It also checks 19,248 live swaps at those rates, stable node/material/texture counts, exact pose preservation, original restoration and catalog bindings. Intentionally stale body/head material inputs must be detected.

Final frozen inputs and exact results live in `evidence/frozen_inputs.json`, each `render_*_v5/` receipt, and `evidence/swaps_v3/swap_audit.json`. Results are summarized in `evidence/summary.json`; missing files mean pending, not passed. Native captures use desktop Vulkan/Mobile on an RTX 3060 Ti, not the Lenovo target.

## Lessons retained from the stress loop

The early preparations and v1-v3 renders are rejected/intermediate evidence. They exposed shoulder contamination, wrong garment sampling, waist/fin mapping boundaries and stretched edge colors. Some numerical geometry runs passed while those painted artifacts remained visible. Their green numerical result never accepted their appearance. A later exact protected-pixel check also rejected v4: one stray alpha=1 headwear speck tinted one face pixel per costume. Main-component matte cleanup removes that speck in v5 without relaxing the exact-pixel requirement. The final method uses bounded uniformly registered cloth over the immutable base, instead of extending fabric beyond its actual coverage. Intermediate inputs were edited during exploration; only the final input freeze is an exact-source acceptance candidate.

A successful base rig does not automatically qualify a costume. Coverage, material masks, view, occlusion and every reachable action belong to each garment's compatibility record. Likewise, smooth bone motion cannot establish natural acting. The tail intentionally deforms within the unchanged numerical bounds; this is not literal zero strain or a full swim/turn/contact performance.

## Evidence and reproduction

Run `python scripts/build_costumes.py` to rebuild the masks, registry and material audit variants. Run `scripts/run_candidates.ps1` for final desktop captures and the original geometry/motion gates. Run `godot/stress_swaps.gd` with an output directory for the exhaustive swap lane. `scripts/package_costumes.py` creates exact RGBA archives, normal/slow review clips and chronological sheets. Aseprite scripts produce and reopen six whole-figure review masters; source rig authoring remains native code and JSON, rather than a saved artist timeline.

The prototype still loads PNGs from source paths. APK resource packaging, scene-editor authoring ergonomics, production wardrobe/save integration, cache lifecycle and memory/performance on the Lenovo Tab M11 remain unimplemented or unverified. Seven 1024-square RGBA clothing inputs alone imply 28 MiB before engine overhead; this is an estimate, not a measured phone allocation. Actual 30 fps/device/child/owner checks remain separately blocking. No finding closes, no rejected earlier art becomes accepted, and game-wide master-audit satisfaction remains **UNSATISFIED**.

The broad regression lane also exposed a baseline probe sampling gap: Geologist closes its activity panel before showing its gallery finale. The original generic task-open guard measured no finale geometry. A bounded probe-only correction samples that existing presentation, keeps every canvas/overlap predicate, and requires a positive sample. The red runs, read-only diagnostic and final focused/full reruns are retained separately in `evidence/project_gate_receipt.json`; gameplay is unchanged and MA-CI-007 stays open.

The later complete rerun retains an intermittent unchanged Melody post-pause tap miss and its downstream progress-count failure. The same assertions pass in a read-only input trace and a separate uninstrumented retest; historical cause remains unproven. Latest individual probe verdicts, a green uninterrupted whole run, and exact published-head CI are different claims in the receipts. No Melody gameplay/assertion change or suite-wide finding closure is claimed.
