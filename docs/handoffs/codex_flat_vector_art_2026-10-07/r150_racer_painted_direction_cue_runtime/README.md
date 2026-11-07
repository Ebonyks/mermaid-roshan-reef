# R150 painted Racer direction cue

A warm painted arrow replaces the flat gold polygon in the Opera Racer wrong-way HUD. Item `FVR-91F160FB9770` belongs to the already documented Racer HUD scope. The wider painted proportions use a slightly shorter vertical footprint while keeping the original anchor, horizontal tip, left/right logic and bob. The arrow has no touch region.

The exact Mobile/Speedy comparison covers left and right at two bob phases, recovery and PC split-view exclusion at 1280×720 and 1600×720. The eight visible pairs change pixels only within the measured original cue extent. Four hidden pairs are pixel-identical. The configured heading uses the game's actual classifier and steering correction. [Ten-axis comparison](TEN_AXIS_COMPARISON.json) · [Pixel comparison](../../../../assets_src/review/r150_racer_direction_cue_20261107/PAIR_PIXEL_COMPARISON.json)

One built-in ImageGen request produced the preserved native arrow using the unprotected painted gold pedal as a material reference. Its model version was unexposed. The preserved source has a technical crop and RGBA resize. [Generation record](../../../../assets_src/imagegen/racer_wrong_way_arrow_20261107/GENERATION_JOB.json)

All 88 required local commands passed against 5,592 runtime inputs, including 82 trusted commands with the expected headless human art skip. [Local machine results](evidence/full_machine/FINAL_RESULT.json) Natural-route and full-speed review, formal QA11, physical device, child and owner evidence remain separate.

[Candidate delivery manifest](MANIFEST.json)
