# Phase-pose containment follow-up

Date: 2026-09-05

## Scope

This bounded visual follow-up covers eleven ordinary, phase-configured diagnostic states: Doctor WASH, FIND, X-RAY, CAST, BANDAGE; Farmer PLANT, TOSS, HERD, PICNIC; and Racer TUNE, TO THE LINE. RACE is excluded because the actor is hidden. Other career phases and all non-Opera minigame families remain open.

Reviewed authored 4x4 work-row atlases:

- assets/opera/worlds/actors/animation/roshan_doctor_sheet_a.png
- assets/opera/worlds/actors/animation/roshan_farmer_sheet_a.png
- assets/opera/worlds/actors/animation/roshan_racer_sheet_a.png

Doctor CAST uses the corrected cell 2 candidate; the earlier cell 1 proposal is rejected.

## Evidence and provenance boundary

Capture groups are diagnostic state-configured captures with ordinary frame processing:

- evidence/phase-poses/baseline/ — 18 PNGs
- evidence/phase-poses/baseline-extended/ — 15 PNGs
- evidence/phase-poses/candidate/ — 33 PNGs

Supporting harnesses, logs, and manifests are under evidence/phase-poses/. The manifest also binds the three exact atlas PNGs, dimensions and work-row geometry, verified byte-identical to published 9df. Code-content SHA-256 values are explicitly distinguished from Git object IDs. Baseline and extended captures predate the candidate mapping. The candidate reflects a pending source change set; its exact source hashes are authoritative for that capture and must not be relabeled as the previously published 9df revision. Prior 9df CI 34009153104 is separate provenance.

These are state-configured diagnostics, not natural user-navigation traces. They use normal processing after configuration, but do not establish human review, target-device behavior, frame cadence, or a 4.5/5 art-quality pass. No numerical art score is assigned because motion cadence and device presentation were not reviewed.

## Reviewed containment mapping

| Career | Phase | Work-row cell | Result |
|---|---|---:|---|
| Doctor | WASH | 1 | Accept provisionally for containment |
| Doctor | FIND | 1 | Accept provisionally for containment |
| Doctor | X-RAY | 1 | Accept provisionally for containment |
| Doctor | CAST | 2 | Accept provisionally; corrected candidate |
| Doctor | BANDAGE | 2 | Accept provisionally for containment |
| Farmer | PLANT | 1 | Accept provisionally for containment |
| Farmer | TOSS | 3 | Accept provisionally for containment |
| Farmer | HERD | 3 | Accept provisionally for containment |
| Farmer | PICNIC | 2 | Accept provisionally for containment |
| Racer | TUNE | 0 | Accept provisionally for containment |
| Racer | TO THE LINE | 1 | Accept provisionally for containment |

Cell numbering is zero-based within the authored 4x4 work row. This is containment evidence only; it does not claim that the atlas supplies a complete animation sequence.

## Visual comparison findings

Candidate 0.0 and 0.4 frames retain the same selected actor pose while the intended phase surface remains visible: Doctor WASH uses the listening/exam pose over the wash station; FIND shows the exam pose with the starfish choices; X-RAY shows the exam pose beside the x-ray display; CAST shows the doctor actor with the cast prop and cell 2 is materially clearer than cell 1; BANDAGE retains the bandage interaction surface. Farmer PLANT keeps the kneeling planting pose over the soil beds; TOSS keeps the extended throwing pose with the pig choice surface; HERD keeps the herd gesture with piglets; PICNIC keeps the food-holding pose with the picnic panel. Racer TUNE keeps the wrench pose beside the kart; TO THE LINE keeps the pointing/ready pose beside the start-line surface.

The authored storybook backgrounds, Mermaid Roshan, and specialist actor cutouts retain their established contour, palette, and lighting relationships in these reviewed frames. Diagnostic overlay and phase controls remain visible, so these are not clean delivery frames. No new navigation-control occlusion changed the mapping conclusion; final navigation/UI review remains a separate runtime gate.

## Accepted and rejected conclusion

Accepted for limited containment: the eleven table mappings, with Doctor CAST at cell 2. Rejected: Doctor CAST at cell 1 because it communicates the cast interaction less clearly in the reviewed source and capture context.

No other mapping is rejected by this bounded capture set. This does not approve unreviewed phases, RACE, smooth animation, target-device readability, or game-wide art quality.

## Required next gate

Reaudit the integrated source at the actual navigation path and on the target Mobile device. Review each live phase through natural user input, including transition cadence and contact timing. Keep this report as containment evidence; it must not be converted into a 4.5/5 acceptance claim while animation cadence remains unreviewed.

## Navigation integration gate

The combined local suite initially rejected the new global menu glyph U+2630 as unclassified. Its live caller is `scripts/navigation_controller.gd`; it conveys the Menu action at the Sky Lagoon root. The typography manifest now classifies it as critical and records missing evidence. This repairs the inventory omission without granting font coverage, child comprehension, or Mobile/device acceptance. No typography test or acceptance threshold was relaxed.

The same navigation consolidation removed the final live references to ten previously inventoried symbols: U+1F499, U+2161, U+2195, U+2198, U+266C, U+2691, U+2702, U+270B, U+2727, U+27B6. Their now-stale classification entries were removed after scanning the current sources. The fail-on-stale and fail-on-unclassified checks remain enabled.

The first added pose probe incorrectly sent its zero-credit gesture after task completion, when that gesture legitimately advances to the next phase. The corrected probe excludes pending transitions, uses the existing trusted diagnostic entry for unopened active tasks, and requires explicit coverage of all eleven phase names. Its focused Godot 4.7.2 run on the pending `9df00099` + `6d7c5e85` merge passed every pose and coverage assertion. These calls are diagnostic seams, not natural child input or animation evidence. The original failed full-suite log is preserved.

The same earlier full run failed two Slide Canvas return/teardown assertions. A fresh isolated focused full-game probe passed both unchanged assertions; the earlier failure remains recorded and under timing review. Combined validation remains pending until its actual exit status is known.

Luna's read-only Slide follow-up found that the teardown assertion includes the fresh-movement result through `neutral_return_guard.exact`; its failure is therefore derivative, not independent evidence of leaked/failing teardown. The substantive check samples after one `process_frame` following pushed touch/drag. Deferred return-guard retirement, touch ownership and Player processing may make that boundary sensitive to scheduling, but the saved log does not prove the precise cause. No threshold or runtime behavior was changed. If it recurs, capture guard/controls/stick/pose/position/velocity/source-census before input, immediately after input and at the next two processing boundaries before choosing a repair. The unchanged focused suite passed on the fresh isolated candidate.

The September6 full candidate05 completed all78 trusted probes but reproduced the Slide assertions and a zero-fish compound failure. The [preserved diagnostics](evidence/slide-diagnostics/manifest.json) subsequently reproduced the fresh gesture turning Roshan without planar motion: its previous successes could depend on gravity. The repaired probe requires an upward stick gesture and planar movement. Its zero-fish driver now has a wider safe target and a frame-duration-aware gain after an accelerated15FPS diagnostic caught the center fish during an overcorrection. The actual trusted probe passes with normal CI flags; slow accelerated diagnostics retain unrelated earlier timing/gold-setup failures and are not green suite or device evidence. Runtime Slide mechanics and reward assertions are unchanged. Complete post-repair validation remains pending.
