# Northern World Art Audit - 2026-07-17

## Scope and gate

This audit applies the runtime-role rubric in `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md` to the Northern Kingdom introduced at the Alpine village cave star. It reviews the mountain-pass arrival, magical forest, small fjord town, docks, center castle, and guiding wisps. It does not modify or rescore protected book art, family voices, or friend cutouts.

The 4/5 gate requires representative near, mid, and gameplay-distance Mobile-renderer screenshots with correct silhouette, material response, scale, composition, and repetition. Human review remains mandatory before an official 4/5 promotion. A generated source or isolated Blender render alone is capped at 2/5.

## Baseline result

GitHub Actions run `29585564212` captured eleven fixed Mobile-renderer views from commit `82bc236`. The trusted probe suite and capture job passed. The screenshots establish that every new Northern asset role was below 4/5:

| Runtime family | Baseline | Evidence |
|---|---:|---|
| Pass arch and four peaks | 1/5 | Focal arch is box pillars/lintel with a flat veil and Label3D snowflake; mountains are tapered cylinders with separate cone-like caps. |
| Forest pines and mushrooms | 2/5 | Recognizable imported props, but repeated generic silhouettes and weak family variation; clipped white presentation reduces depth. |
| Six houses | 1/5 | Box bodies, roof cards, inset box doors/windows, and palette swaps. Near view is partially obscured and does not read as authored architecture. |
| Two docks | 1/5 | One broad slab with three posts; no plank rhythm, rope, edge language, or town-specific silhouette. |
| Center castle | 1/5 | Box curtain walls and keep, borrowed towers, roof cards, and a Label3D crown. Near view is a wall sheet that hides the destination. |
| Eight wisps | 1/5 | SphereMesh plus TorusMesh tokens; the near capture is nearly lost in the overexposed ground. |
| Northern lighting/composition | 1/5 | Terrain and pale focal surfaces clip toward white across gameplay, near, and overview views. |

The item-level baseline is recorded in `audit/northern_asset_ledger_2026-07-17.csv`.

## Regeneration

All sub-4 roles were regenerated as a project-authored, texture-free Blender 4.4.3 kit. The design follows the repository language: rounded low-poly toy geometry, matte pastel materials, navy/plum accents, aqua/lavender shadow colors, oversized child-readable features, controlled asymmetry, snow pillows, and no borrowed franchise symbols.

- Pass: irregular stacked-stone arch with a modeled six-arm snowflake; two asymmetrical sculpted crag families with snow shelves.
- Forest: three layered, jagged pine profiles and two complete mushroom-cluster profiles.
- Town: six individually modeled timber houses. Palette, dormer/porch/wing, chimney, window, trim, and footprint variation prevent a family score from hiding a weak member.
- Fjord: uneven plank dock with posts, sagging modeled rope, and a readable fish carving.
- Castle: one authored four-tower courtyard, crenellated walls, open approach gate, gabled keep, bay towers, large door, windows, flags, snow ridge, and modeled crown crest.
- Wisps: crossed flame profiles with a heart and five orbiting motes, using restrained emissive material without new OmniLights.

The first modeling pass exposed a half-dimension construction error that separated roofs and facade trim. Those exports were rejected and regenerated; the checked-in QA renders show the corrected joined silhouettes.

## Mobile budget

The editable `.blend` retains separate modeling pieces, while each runtime GLB is export-batched into one mesh with material surfaces. The full 46-instance layout totals 73,500 triangles before visibility-range culling. The largest asset is the 12,816-triangle castle; each house is 1,788-2,444 triangles. No runtime texture memory is added because the family uses embedded flat materials only. Existing analytic solids remain the sole collision system.

The Northern scene also moves to the established `bright_pastel` scene grade with reduced sun, ambient, bloom, and darker grass/cobble tints to restore color separation in the Mobile renderer.

## Candidate iteration 1 rejected

GitHub Actions run `29588787382` passed import, static gates, the full Godot analyzer, all trusted probes, and the eleven-view capture. Visual review still rejected the build. The general imported-CC0 `_toonify` path was lifting the kit's already-authored pastel materials a second time, so walls, roofs, snow, docks, and wisps clipped toward white. The larger replacement pine also occluded the fixed near-house review. The follow-up keeps the embedded authored materials, disables northern-only screen bloom, reduces exposure and wisp emission, and moves the near-house camera to the unobstructed inward facade.

## Final Mobile evidence

Commit `90b6b83` corrected the material path. GitHub Actions run `29609915332` then passed static gates, import, the full Godot analyzer, every trusted probe, and all eleven Mobile captures. Visual review confirmed the intended authored palette, readable house fronts, modeled dock detail, open castle approach, and restrained wisp emission. The review also found three defects in the fixed evidence cameras: two frames intersected scenery and the wisp frame was too distant. These were capture defects rather than runtime asset defects, but invalid frames were not counted as quality evidence.

The viewpoints were corrected and rerun. Run `29624007719` passed every gate and established clear forest and near-wisp views; its alternate pass camera still intersected a different peak and was rejected. The final centerline pass view was captured by run `29624457732` from commit `8a9289d`. That exact revision passed:

- gdtoolkit parsing and Variant-inference lint;
- deadlock-guarded clean import;
- the full Godot script analyzer and Roshan motion cage;
- every trusted gameplay, save/load, passive, picture-game, lagoon, northern, and kart probe;
- all first-world and eleven northern-world Mobile-render captures.

The accepted Mobile set shows the complete pass arch and peak corridor, three distinct pine profiles, both mushroom families, all six varied timber houses, the rope-and-plank dock, the castle at gameplay/mid/near distances, and a near wisp with the continuing trail and destination in view. No focal role is a primitive blockout, no family depends on crossed cards or billboards, no reviewed asset is hidden by camera occlusion, and the authored materials retain silhouette separation without bloom clipping.

## Final score and decision

Every item in `audit/northern_asset_ledger_2026-07-17.csv` now clears the internal silhouette, material, scale, composition, and repetition checks for a **4/5-ready candidate**. Per the repository hard cap, the recorded score remains **provisional 3/5 pending owner review**; this is an administrative review cap, not a remaining automatic-regeneration defect. No further automatic regeneration is triggered. An official 4/5 promotion requires the owner to accept the shipped Mobile views.
