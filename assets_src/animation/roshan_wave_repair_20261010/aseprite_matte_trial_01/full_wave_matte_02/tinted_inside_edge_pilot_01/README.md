# tinted inside edge pilot 01 - one-cel diagnostic

This source-only frame14 test binds `assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01/full_wave_draft_06` and preserves the whole source PNG byte-exact. `source_and_seed_plan.json` records source/workflow hashes and the reviewed true-background hair-hole seed. Aseprite Lua performs all pixel writes on one complete cel; no body-part assembly, warp, erosion, dilation or Python pixel write occurs.

Connected outer field: minRGB >=170, chroma <=22. The four-pixel boundary band fits an actual stronger-painted same-cel neighbor within six pixels at depth >=2. RGB fit residual is 25 for nearly neutral pixels(chroma <=15),10 for colored pixels. Classified field pixels remain alpha0; only retained boundary pixels may be fitted. Original closed pale highlights remain unchanged. The whole drawing uses scale0.3125 to240x280 at(15,-10) into256x256.

Actual native and256 opaque black/light outputs were inspected. `review.json` measures 709 original strict closed pale pixels,0 modified pale pixels and0 modified pixels deeper than the band. Whole-wave identity/motion/geometry/device/owner acceptance remains absent. The actual512 K0/inside/dim comparison shows that cyan crown and bright fin rim are authored source paint; pale rims are not categorically defects.

`batch_clock.json` and preview clocks, when present, hold actual UTC/Stopwatch intervals; older tool-wall measurements are identified in review records. `pixel_processing_stats_raw.json` preserves emitted Aseprite counts with stale copied footer labels; canonical stats correct labels against the exact executed Lua hash and source plan. Seed-coordinate authority is the source plan because Aseprite nested JSON arrays emitted null. Generator/GPU/paid API calls:0.

This pilot is not selected as the final matte; the later dim-closed comparison further diagnoses the retained rim.
