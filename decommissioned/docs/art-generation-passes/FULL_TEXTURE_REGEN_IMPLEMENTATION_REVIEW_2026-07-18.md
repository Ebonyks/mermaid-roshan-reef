# Full Texture Regen Pack — Implementation Review (2026-07-18)

Independent evaluation of `codex/full-texture-regeneration` (pack commit
`2486864`) and its companion critique branch `codex/non5-art-critique`
(`a755710`). Method: visual review of all gallery sheets and per-file renders,
independent GLB/texture parsing of all 167 candidates, full sha256 manifest
verification, code review of the stress/render/finalize tools, and
verification of the companion critique's factual claims.

## Verdict

The pack is the best-organized art delivery this repo has produced — isolated
from runtime, fully manifested and hash-verified, palette-locked, provenance-
retained, and honest about protected assets. The candidate art itself is a
real step up in two categories (2D painted textures; small readable props) and
adequate-to-weak in one (world-scale roles). But the QA layer that awarded
every candidate 4/5 is **stamping, not measuring** — including one broken
join that silently discarded render validation — so the pack's scores should
be treated as aspirations until re-reviewed. The companion critique's central
thesis (generator-auditor non-independence) is correct and verifiably so.

## What was delivered

- 137 texture-free GLBs (6.2 MB total, median 1,216 tris, max 9,922, mean 4.0
  materials) + 30 PNG textures (23 MB, zero size-rule violations)
- A locked 24-color set-wide palette — tighter than any prior batch (art35
  used 144 colors); pastel bands + navy/ink accents, zero pure-white slots
- 28 accepted + 1 rejected image-gen sources retained; editable Blender source;
  88-role manifest keyed to the human-audit ledger; complete license rows
- A CI probe (`probe_full_texture_regen.gd`) wired into probes.yml that locks
  pack counts and budgets
- All 167 manifest sha256 hashes verified correct; zero unmanifested files

## Strengths

1. **Process discipline.** Deliberate runtime isolation, protected-asset
   compliance (carrot/watering-can untouched, R020 rebuilds frames only, cat
   parts left manual-only), dated candidate directory, self-documented
   nine-class failure analysis, and a phone-scale re-render pass. This is the
   stress-test-loop governance working as intended — up to the review stage.
2. **The 2D texture set is the strongest 2D work in the repo.** The painted
   seamount backdrop, watercolor caustics, navy-cobble dungeon floor with
   sparkles, kitchen tile/counter canvases, and the picture-game sprite set
   (star/sun/tree/coal/fish with thick navy contours) directly answer
   long-open residuals — several are items 4 and 6 of the gap work order.
3. **Prop-scale 3D is consistently good.** Butterfly gates and the butterfly
   family (correct 4-wing/6-leg/antennae anatomy, real species variation),
   dungeon set (imps, boss, basket, torches, pictogram plaques), go-kart and
   monster truck, coral growth families split into six distinct structures,
   Northern houses. Silhouettes hold at the 112 px phone-scale sheets.
4. **The companion critique is rigorous.** Its headline claims verify against
   the repo (71 identical evidence sentences in the review ledger — exactly
   true; all 85 generated roles uniformly 4/5 — true; the protected-5/5 vs
   scoring-governance contradiction — real). It is the right document to
   drive the next iteration.

## Integrity findings (must fix before any promotion)

1. **The review ledger is stamped, not measured.**
   `tools/finalize_full_regen_review.py` unconditionally writes
   `full_size_gallery_review: pass`, `phone_scale_review: pass`, and
   `candidate_score: 4/5` for every asset (lines 87–90, 101–103). The
   README's "pass at 4/5 candidate threshold" gallery claims are these
   stamps.
2. **Render validation never reached the ledger.** The finalize tool keys
   render metrics by render-PNG path but looks them up by GLB path (lines
   68–71 vs 87), so `render_status` is `not_applicable` on all 167 rows.
   The (already weak) render gate — variance ≥20, brightness 20–245, i.e.
   "not blank" — was silently discarded.
3. **Circular structural QA.** Triangle counts, bounds, and anatomy component
   names are read from the generator's own manifest, not measured from the
   GLBs; anatomy checks are name-matching against names the same generator
   authored. A blob named `front_wing_left` passes.
4. **Phantom role R088.** `pipeline_generated_provenance_integrity` has zero
   files yet is stamped 4/5 with the evidence note "Reviewed in full-size and
   112 px phone-scale galleries" — false on its face; the manifest's
   `candidate_roles: 85` overstates asset-backed roles (84).
5. **No promotion mapping.** No manifest field names a runtime destination
   path for any candidate. Promotion is undefined per-role — the same
   routed-vs-visible failure mode the repo hit on 07-15/16, now one orphan
   pile larger if merged as-is (the repo already carries 11 orphaned GLBs).

## Art-direction critique (per candidate quality)

1. **World-scale roles answered with diorama miniatures.** R001 reef hub,
   R014 sky-world composition, R019 snow terrain, R023 castle hall overall,
   R043 Butterfly World overall (a near-featureless mint sphere — weakest
   file in the pack), R049/R051 arena, R085 alpine interiors. These roles are
   compositions needing kits plus layout code; a single prop-scale GLB cannot
   be promoted into them. Nominal coverage of "85/85 roles" overstates what
   the pack can actually deploy.
2. **Northern Kingdom duplication.** 17 candidates regenerate a wing that
   shipped a Mobile-capture-validated, 4/5-ready authored kit yesterday
   (`assets/northern/`, four Actions runs of evidence). The miniatures are
   simpler than the shipped kit (no rope sag, fish carving, crenellation
   detail). Promoting them would be a regression; carrying them is dead
   weight. Drop or mark reference-only.
3. **Train identity.** The six-car family is charming but reads as buses:
   rubber-tire wheels with hubs, window-band bodies, no coupling rods,
   understated stack, no cowcatcher — and no track/ties/rails/platform
   family, so `courtyard_train.gd`'s primitive track remains regardless.
4. **Coral pedestal repetition.** Every R003 growth variant carries the same
   blue-grey base rock. Mass placement will grid on the repeated pedestal —
   the pack's own lesson 4 (seamless ≠ non-repetitive) applied to geometry —
   and it fights the placement audit's rule that the seabed provides the
   support surface.
5. **Kelp/seagrass are still cards.** The files are named `kelp_cards` /
   `seagrass_cards`; the blades are better-authored planar fans, but the
   original 1/5 complaint was card masses. These are nicer cards.
6. **Butterfly meadow ground runs hot.** The three seam-safe variants are
   rich, but warm coral flowers claim roughly 40% of the field on a ground
   plane, against the style guide's cool-two-thirds rule; at tiling density
   it may vibrate. The variants + no-grid rule help; a calmer base variant
   would help more.
7. **Kitchen palette collision.** The candy-striped coral/gold painted-wood
   canvas will clash with the shipped muted kitchen GLB props; promotion
   needs a per-room reconciliation pass, not per-file swaps.

## Coverage vs the known gap list

The pack regenerates the 88 *audited* roles; it does not touch the primitive
roles outside that ledger. Still open from `ART_GAP_WORKORDER_2026-07-18.md`:
castle architecture kit (the R023/R025/R026 miniatures are minimal), kart
grandstands/crowd/pit garage, treasure loot piles, basement/shop/toy-room
clutter, slide chute segments, fetch snowfield, dungeon impact VFX, and the
six quick-win wirings. The two documents are complementary; neither alone is
"the art is done."

## Recommended next steps

1. Fix the finalize join bug and remove the unconditional stamps; re-run
   review so the ledger holds measured verdicts. Delete or de-scope R088.
2. Add a `runtime_target` field per manifest asset and stage promotion
   area-by-area (textures first — backdrop, caustics, dungeon floor, picture
   games — they are the clearest wins and the least wiring).
3. Split world-scale roles out of the pack into kit+layout workstreams; do
   not count them as candidate-covered.
4. Drop the Northern candidates (superseded by shipped kit).
5. Iterate train (rails family + locomotive identity cues) and de-pedestal
   the coral family before any reef promotion.
6. Measure, don't trust: make the stress tool parse triangles/bounds from
   GLBs directly and validate anatomy by geometry (component vertex clusters),
   per the companion critique's independence requirement.
