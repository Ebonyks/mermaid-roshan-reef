# Codex Improvement Audit — Regen Pack Iteration 2 (2026-07-18)

Directive audit for the next Codex working session on the
`codex/full-texture-regeneration` candidate pack. Synthesizes
`FULL_TEXTURE_REGEN_IMPLEMENTATION_REVIEW_2026-07-18.md` (independent review,
all claims verified against the branch) and
`ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md` (companion critique, thesis
confirmed). Work through the priorities in order; each item carries an
acceptance criterion. Do not begin new generation until P0 is closed —
regenerating through a broken review pipeline produces more unmeasured 4/5s.

## P0 — QA integrity (blocks everything else)

1. **Fix the finalize join bug.** `tools/finalize_full_regen_review.py` keys
   render metrics by render-PNG path but looks them up by GLB asset path
   (lines 68–71 vs 87), so `render_status` is `not_applicable` on all 167
   ledger rows. Accept when: every model row carries a real render verdict.
2. **Remove unconditional stamps.** The same tool hardcodes
   `full_size_gallery_review: pass`, `phone_scale_review: pass`, and
   `candidate_score: 4/5` for every asset (lines 87–90, 101–103). Scores must
   come from measured checks plus recorded human review, and must be able to
   differ per file. Accept when: the asset ledger shows a non-uniform score
   distribution or documents, per file, the measured basis for an identical
   score — and at least one knowingly-flawed test asset FAILS the pipeline.
3. **Measure, don't trust.** `tools/stress_full_texture_regen.py` reads
   triangles, bounds, and anatomy component names from the generator's own
   manifest. Parse them from the GLB binary instead, and validate anatomy
   geometrically (distinct component vertex clusters with plausible relative
   sizes/positions), not by matching names the generator itself authored.
   Accept when: a renamed-blob test file fails the wing/leg/antenna checks.
4. **Delete or de-scope phantom role R088.** It has zero files but is scored
   4/5 with the evidence note "Reviewed in full-size and 112 px phone-scale
   galleries" — false. Manifest `candidate_roles` must equal asset-backed
   roles (currently claims 85, reality is 84).
5. **Strengthen the render gate.** Current pass = variance ≥20 and mean
   brightness 20–245 ("not blank"). Add: silhouette coverage bounds within
   frame, per-role scale sanity vs a reference dimension, and run the seam
   check on all four tile edges (currently horizontal-only, 7 hardcoded
   roles).

## P1 — Promotion mapping (turns candidates into shipped art)

6. **Add `runtime_target` to every manifest asset entry.** No candidate may
   be promoted without a named destination path and referencing script.
   Promotion commits must wire the file in the same commit (repo already
   carries 11 orphaned GLBs; do not add more).
7. **Promote textures first — they are the clearest wins.** Known mappings
   (verify each referencing script before overwrite; keep byte-identical
   backups per repo convention):

   | Candidate (R-role) | Runtime target | Referenced by |
   |---|---|---|
   | R007 caustics | `assets/terrain/caustics.png` | main.gd caustic passes |
   | R008 seamount backdrop | `assets/terrain/backdrop_seamounts.jpg` | main.gd backdrop cylinder |
   | R032/33/34 kitchen counter/floor/wood | `assets/terrain/kitchen_*_col.jpg` | castle_hall.gd / main.gd materials |
   | R050 dungeon floor | dungeon arena floor material | dungeon_art.gd / combat_arena.gd |
   | R066/67 boost ribbon / finish banner | `assets/kart/boost_ribbon.png`, `finish_banner.png` | kart.gd |
   | R071–R080 picture-game sprites | `assets/mg/*.png` (existing basenames) | picture_games.gd |
   | R084 ornament set | `assets/mg/orn1..5.png` | picture_games.gd |
   | R044 meadow ground ×3 | new — butterfly planet surface material | galaxy.gd (replaces procedural confetti shader) |

   R075/R076 (empty vs completed tree) and R078/R079 (fish body vs five fin
   files) must preserve the functional-separation contract exactly.
   Protected: R081 carrot, R082 watering can, R083 cat parts — no action.
8. **Promotion order after textures:** dungeon set → kart vehicles/dressing →
   butterfly gates/family → coral+flora (after P2 rework) → castle props.
   Each area promotion = one commit, probes green on CI, Mobile captures
   re-run for that area before the next.

## P2 — Art rework (findings from visual review)

9. **De-pedestal the coral family.** Every R003 growth variant carries the
   same blue-grey base rock; mass placement will grid on the repeated
   pedestal, and the placement audit's rule is that the seabed provides the
   support surface. Ship growth forms bare, or with ≥3 base variants used
   sparsely.
10. **Kelp/seagrass: cards → clumps.** The files are named `kelp_cards`; the
    original 1/5 complaint was card masses. Model volumetric blade clusters
    (twist, overlap, thickness) rather than planar fans.
11. **Train identity pass.** The six-car family reads as buses: rubber-tire
    wheels with hubs, window-band bodies, no coupling rods, small stack, no
    cowcatcher. Add locomotive cues plus a **track family** (rails, ties,
    curve segments, platform) — without it `courtyard_train.gd`'s primitive
    track survives promotion.
12. **Cool down the butterfly meadow ground.** Warm coral flowers claim ~40%
    of the field on a ground plane (style guide: cool two-thirds). Add a
    calmer low-flower base variant and reserve the current ones for feature
    patches.
13. **Kitchen reconciliation.** The candy-striped coral/gold painted-wood
    canvas clashes with the shipped muted kitchen GLB props. Promote the
    kitchen as one room pass (textures + prop tints together), not per-file.
14. **Drop the Northern candidates.** The shipped `assets/northern/` kit is
    Mobile-capture-validated and richer than the 17 pack miniatures.
    Mark them reference-only or delete; do not promote.

## P3 — Coverage the pack does not have

15. **World-scale roles need kits + layout code, not miniatures.** R001 reef
    hub, R014 sky world, R019 snow terrain, R023 castle hall, R043 Butterfly
    World overall (weakest file in the pack — a near-featureless sphere),
    R049/R051 arena, R085 alpine interiors: remove these from
    candidate-covered counts and open one kit workstream per area.
16. **Roles outside the 88-role ledger remain open** — from
    `ART_GAP_WORKORDER_2026-07-18.md`: castle architecture kit (columns,
    arches, balustrades, chandeliers, stairs), kart grandstands/crowd/pit
    garage, treasure loot piles, basement/shop/toy-room clutter, slide chute
    segments, fetch snowfield canvas, dungeon impact VFX, and the six
    zero-modeling quick-win wirings. The regen pack and the gap work order
    together are the full backlog; neither alone is "done."

## Standing rules (unchanged, apply to all of the above)

- Scoring per `ART_SCORING_GOVERNANCE_2026-07-18.md`: no self-awarded 5/5;
  4/5 requires measured near/mid/gameplay Mobile evidence; owner acceptance
  promotes.
- Style/technical contract per `assets/ART_GENERATION_CONTRACT.md` (palette,
  outlines, budgets, ≤1024-or-POT, license rows, no orphans, probes green).
- Protected zones untouched: `assets/book/`, `assets/audio/voices/`,
  `assets/characters/friends/`; Roshan generation stays in the Meshy
  pipeline, not this one.

## Definition of done for iteration 2

Ledger holds measured, per-file verdicts from a pipeline that can fail;
every promoted asset has a runtime target and is wired in its promotion
commit; texture wins are live in-game with green probes and fresh area
captures; coral/kelp/train reworked; Northern and world-scale miniatures
withdrawn; the pack directory contains only candidates that still await
promotion.
