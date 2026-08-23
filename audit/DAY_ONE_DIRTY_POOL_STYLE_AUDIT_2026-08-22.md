# Day One Dirty Pool style congruence audit — 2026-08-22

## Verdict

**Overall master-audit rating: 2/5 — major repair.**

The Day One pool rescue is functional, narratively purposeful, one-finger
readable, save-compatible, and implemented on the 2D Canvas. The corrected
sick-state seahorse now preserves the established fountain identity, has no
invented horn, and shows a soggy pink wrapper visibly blocking its mouth/nozzle.
Rumi now uses her owner-approved private-canon Violet identity and existing
authored swim, wave, and idle frames. Those corrections do not make the
generated dirt family congruent as a whole: the three pollution overlays remain
materially glossier, denser, and more halo-driven than the approved Mermaid
Pool anchor.

Under the master audit rubric, a green technical probe or a clean isolated
render cannot grant a high visual score. The pack therefore remains at 2/5
until the named art and evidence gaps below are repaired and accepted in
runtime context.

## Authority and evidence

- Rating meanings: `audit/MASTER_AUDIT_2026-08-09.md` §1.1.
- Binding visual rules: `DL-VIS-01`–`DL-VIS-08`, `DL-READ-01`–`DL-READ-06`,
  `DL-INT-02`–`DL-INT-03`, `DL-MOT-01`–`DL-MOT-07`, and `DL-SND-01`–`DL-SND-05`
  in `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.
- Approved identity/style anchors: the clean Mermaid Pool room, separated clean
  seahorse-fountain card, clean fountain animation sheet, and approved Roshan
  Canvas cutout. Protected sources were inspected but not modified.
- Rumi identity authority: owner-supplied attachment SHA-256 `96336314…fca26`
  matches the retained relationship sample byte-for-byte. The approved
  full-body identity, eight-pose atlas, and continuity card come from project
  commit `975d7e86291a5e5b69ffb417bfba45cf184ef756`. The runtime combines its
  approved idle/wave cells with the existing cell-safe pool swim row; no new
  Rumi generation was performed for this correction.
- `python tools/audit_lighting_images.py assets/castle/day_one_pool
  assets/characters/rumi` scanned all six runtime images: 0 unreadable. The four
  pool assets measure luminance p50 0.23, dynamic range 0.69, 0% crushed, 0%
  blown, 42° hue shift, and 0.1% measured ink; the two Rumi atlases measure
  luminance p50 0.33, dynamic range 0.69, 0% crushed, 0% blown, 71° hue shift,
  and 0% measured ink. The JSON and generated Markdown evidence are stored
  beside this report.
- All six runtime images are RGBA with 0–255 alpha. The corrected seahorse is
  936×1024. The algae mat touches the left and lower alpha bounds; that is a
  padding/cutoff warning, not a style pass. Every authored Rumi animation cell
  has nonzero edge-safe alpha padding.
- Exact Godot 4.7.1 import completed and
  `scripts/probe_day_one_pool_cleanup.gd` passed every focused check, including
  four ordered cleanup subjects, seahorse-last enforcement, dingy-lighting
  contract, sequential touch ownership, approved Rumi identity, four-cell swim,
  two-cell wave, two-cell idle, their runtime transition order, finale, and
  teardown.
- A fresh Castle run of `tools/audit_visual_design.py` was attempted with exact
  Godot 4.7.1. Its runtime-facts subprocess reached the tool's 180-second
  timeout and correctly downgraded runtime checks to `COVERAGE_GAP`. A later
  static-only attempt also failed to return within a bounded review window and
  was stopped. This report makes no causal attribution and does not treat that
  broad automated result as a fresh Castle-wide visual PASS.
- The dedicated screenshot probe passed under Godot 4.7.1's Forward Mobile
  renderer and captured all six states at 2560×1369, including the dirty
  seahorse-last frame, Rumi's authored swim-rise, and the settled approved Rumi
  reveal. Smallest-phone, M11, child, and owner acceptance remain open.

## Asset-by-asset findings

| Asset/state | Rating | Congruent strengths | Blocking or material gaps |
|---|---:|---|---|
| Approved clean Mermaid Pool room | 4/5 anchor | High-key aqua/lavender/cream field; child-readable pool, waterfall, floats, and established seahorse fountain | Existing owner/device acceptance remains outside this pool-specific review |
| `pool_algae_trash.png` | 2/5 | Pollution reads immediately; wrapper and harmless cup are recognizable; broad single-tap footprint | Glossy wet rendering, dense distributed highlights, dark/colored halo, too many equally weighted details, and alpha touching two canvas edges conflict with `DL-VIS-01`–`05` and calm phone-size grouping |
| `waterfall_growth.png` | 2/5 | Tall silhouette clearly blocks the waterfall and supports truthful cleaning | Monolithic dense curtain, repeated specular droplets, photographic/slimy microtexture, dark internal channels, and weak two-or-three-band simplification diverge from the matte storybook anchor |
| `pool_rim_grime.png` | 2/5 | Distinct from the pool mat; bottle cap, scraps, ribbon, and sponge communicate trash | PBR-like bubbles/gloss, broad colored halo, dense object scatter, and weak quiet-negative-space control compete with the intended next tap |
| Corrected `seahorse_sick.png` | 3/5 | Same fountain species, long snout, eye placement, crest, belly, curl, coral/paver base, palette, and pose; no horn; wrapper visibly lodged in mouth/nozzle; sympathetic and child-safe; real alpha; settled desktop runtime capture confirms the final-target composition | Still somewhat more saturated and highlight-dense than the clean rest card; smallest-phone squint review, owner acceptance, and clean/dirty cross-state identity review remain open |
| Approved Rumi atlas reveal | 4/5 | Exact owner-confirmed Violet/Rumi identity; enormous violet braid, sea-jacket, shell clasp, aqua-lavender tail, and coral fins are preserved. Authored cell-safe swim frames animate the rise, followed by authored wave and idle frames; fresh desktop mobile-renderer capture confirms her in-pool scale and identity | Private-project/IP-hold only; smallest-phone/device acceptance remains open; exact Rumi speech is still missing under `DL-SND-01`/`03` |
| Ordered cleanup composition | 4/5 | One live target at a time, direct pointer, truthful state removal, Roshan remains visible, seahorse is last, lighting/reward progression is clear, and the finale now uses authored Rumi acting; all six desktop mobile-renderer states captured successfully | The three pollution assets share one glossy green visual mass; exact Rumi voice and device acceptance remain open |

## Rule-level summary

| Rule family | Result | Reason |
|---|---|---|
| True 2D / runtime size | **Pass for this feature** | Canvas nodes and RGBA textures; all runtime images are at or below a 1024px longest edge |
| Identity preservation | **Pass for corrected seahorse and Rumi** | Seahorse derives from the clean fountain authority. Rumi derives from the exact owner-confirmed private-canon identity and retained relationship sample |
| Shape, contour, value, materials | **Fail for dirt pack** | The three pollution overlays use dense glossy rendering, colored halos, and microdetail rather than calm clusters and broad matte value bands |
| Child-readable hierarchy | **Workable** | Sequential targets and pointer are strong, but dense equal-weight details weaken the phone squint test |
| Truthful interaction and ordered motion | **Pass functionally** | Cleaning removes the visible state and the waterfall/light finale follows completion |
| Authored character motion | **Pass for Rumi reveal** | Four authored swim cells animate the rise, two authored wave cells perform the greeting, and two authored idle cells sustain her presence |
| Non-reader audio | **Coverage gap** | The objective path is visually cued, but Rumi's exact thank-you/introduction recording does not exist; caption plus generic cheer is not a complete substitute |
| Runtime/owner/device evidence | **Partial pass / coverage gap** | Focused probe and six-state desktop Forward Mobile capture are green; M11/phone, child, and owner acceptance remain absent |

## Bounded repair order

1. Keep the corrected seahorse and validate its dirty/clean identity at
   smallest-phone scale and on the target device; desktop mobile-renderer
   capture is complete.
2. Regenerate only the three pollution overlays against the clean pool anchor:
   matte broad bands, two or three calm clusters, restrained wet accents, clean
   plum/indigo contour, no aura/vignette, and safe alpha padding.
3. Keep the approved Rumi identity and authored atlas wiring; the desktop
   swim-to-wave-to-idle transition is validated, so complete smallest-phone and
   target-device review.
4. Add an authorized exact Rumi thank-you/introduction recording without
   modifying or substituting protected family voices.
5. Re-run import, focused/passive/full probes, fresh Castle visual facts, phone
   captures, and owner review. Only that evidence can raise the overall rating.
