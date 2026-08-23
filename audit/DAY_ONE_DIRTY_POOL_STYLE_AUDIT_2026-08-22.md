# Day One Dirty Pool style congruence audit — 2026-08-22

## Verdict

**Overall master-audit rating: 2/5 — major repair.**

The Day One pool rescue is functional, narratively purposeful, one-finger
readable, save-compatible, and implemented on the 2D Canvas. The corrected
sick-state seahorse now preserves the established fountain identity, has no
invented horn, and shows a soggy pink wrapper visibly blocking its mouth/nozzle.
Those strengths do not make the generated art family congruent as a whole. The
three pollution overlays and Rumi remain materially glossier, denser, and more
halo-driven than the approved Mermaid Pool and Roshan anchors. Rumi also lacks
an owner-approved identity source and authored rise/acting frames.

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
- `python tools/audit_lighting_images.py assets/castle/day_one_pool` scanned all
  five runtime files: 0 unreadable, group luminance p50 0.23, dynamic range
  0.72, 0% crushed, 0% blown, 23° hue shift, and 0.1% measured ink. The JSON
  and generated Markdown evidence are stored beside this report.
- All five runtime assets are RGBA with 0–255 alpha. The corrected seahorse is
  936×1024. The algae mat touches the left and lower alpha bounds; that is a
  padding/cutoff warning, not a style pass.
- Exact Godot 4.7.1 import completed and
  `scripts/probe_day_one_pool_cleanup.gd` passed every focused check, including
  four ordered cleanup subjects, seahorse-last enforcement, dingy-lighting
  contract, sequential touch ownership, finale, and teardown.
- A fresh Castle run of `tools/audit_visual_design.py` was attempted with exact
  Godot 4.7.1. Its runtime-facts subprocess reached the tool's 180-second
  timeout and correctly downgraded runtime checks to `COVERAGE_GAP`. A later
  static-only attempt also failed to return within a bounded review window and
  was stopped. The current checkout contains unrelated local add-on changes;
  this report makes no causal attribution and claims no fresh Castle visual
  PASS.
- The dedicated screenshot probe also mounted the dirty pool but stalled before
  its first new capture. Existing earlier captures were not overwritten. The
  focused gameplay result is valid, but new in-context screenshot acceptance
  remains open.

## Asset-by-asset findings

| Asset/state | Rating | Congruent strengths | Blocking or material gaps |
|---|---:|---|---|
| Approved clean Mermaid Pool room | 4/5 anchor | High-key aqua/lavender/cream field; child-readable pool, waterfall, floats, and established seahorse fountain | Existing owner/device acceptance remains outside this pool-specific review |
| `pool_algae_trash.png` | 2/5 | Pollution reads immediately; wrapper and harmless cup are recognizable; broad single-tap footprint | Glossy wet rendering, dense distributed highlights, dark/colored halo, too many equally weighted details, and alpha touching two canvas edges conflict with `DL-VIS-01`–`05` and calm phone-size grouping |
| `waterfall_growth.png` | 2/5 | Tall silhouette clearly blocks the waterfall and supports truthful cleaning | Monolithic dense curtain, repeated specular droplets, photographic/slimy microtexture, dark internal channels, and weak two-or-three-band simplification diverge from the matte storybook anchor |
| `pool_rim_grime.png` | 2/5 | Distinct from the pool mat; bottle cap, scraps, ribbon, and sponge communicate trash | PBR-like bubbles/gloss, broad colored halo, dense object scatter, and weak quiet-negative-space control compete with the intended next tap |
| Corrected `seahorse_sick.png` | 3/5 | Same fountain species, long snout, eye placement, crest, belly, curl, coral/paver base, palette, and pose; no horn; wrapper visibly lodged in mouth/nozzle; sympathetic and child-safe; real alpha | Still somewhat more saturated and highlight-dense than the clean rest card; new settled runtime capture, smallest-phone squint review, owner acceptance, and clean/dirty cross-state identity review remain open |
| `rumi_violet.png` | 2/5 | Full-body violet mermaid silhouette and grateful wave are readable | Generic high-gloss big-eye character rendering, dense sparkling scales/hair, heavy violet aura, and value treatment do not match Roshan's smaller matte/cel-painted anchor. No canonical Rumi identity source exists in the repository. One translated static cutout does not satisfy an authored animated rise under `DL-MOT-07`; exact Rumi speech is also missing under `DL-SND-01`/`03` |
| Ordered cleanup composition | 3/5 | One live target at a time, direct pointer, truthful state removal, Roshan remains visible, seahorse is last, and lighting/reward progression is clear | The three pollution assets share one glossy green visual mass; fresh runtime capture coverage is open; the finale's static Rumi card and generic celebration voice keep it below strong |

## Rule-level summary

| Rule family | Result | Reason |
|---|---|---|
| True 2D / runtime size | **Pass for this feature** | Canvas nodes and RGBA textures; all runtime images are at or below a 1024px longest edge |
| Identity preservation | **Pass for corrected seahorse; open/fail for Rumi** | Seahorse now derives from the clean fountain authority. Rumi has no canonical identity authority and reads as a generic newly invented character |
| Shape, contour, value, materials | **Fail for pack** | Pollution and Rumi use dense glossy rendering, colored halos, and microdetail rather than calm clusters and broad matte value bands |
| Child-readable hierarchy | **Workable** | Sequential targets and pointer are strong, but dense equal-weight details weaken the phone squint test |
| Truthful interaction and ordered motion | **Pass functionally** | Cleaning removes the visible state and the waterfall/light finale follows completion |
| Authored character motion | **Fail for Rumi** | Static cutout translation/scale/fade is feedback motion, not authored animated rise/acting frames |
| Non-reader audio | **Coverage gap** | The objective path is visually cued, but Rumi's exact thank-you/introduction recording does not exist; caption plus generic cheer is not a complete substitute |
| Runtime/owner/device evidence | **Coverage gap** | Focused probe is green; new full runtime captures, M11/phone, child, and owner acceptance are absent |

## Bounded repair order

1. Keep the corrected seahorse and validate its dirty/clean identity in a fresh
   runtime capture at 1280×720 and smallest-phone scale.
2. Regenerate only the three pollution overlays against the clean pool anchor:
   matte broad bands, two or three calm clusters, restrained wet accents, clean
   plum/indigo contour, no aura/vignette, and safe alpha padding.
3. Do not regenerate Rumi again from prose alone. Obtain or nominate an
   owner-approved Rumi identity reference, then produce a small authored 2D
   rise/thank-you state set in the same character family as approved Roshan.
4. Add an authorized exact Rumi thank-you/introduction recording without
   modifying or substituting protected family voices.
5. Re-run import, focused/passive/full probes, fresh Castle visual facts, phone
   captures, and owner review. Only that evidence can raise the overall rating.
