# Bathroom cleanup action audit for Claude

November 10, 2026. Independent secondary review of Mermaid Roshanâ€™s browser prototype. The assignment is to inspect the three cleanup actions, identify what should change, and return a reconstruction recipe that another animator or developer can follow. The evidence is the November 10 build with the repaired arm binding and eased shoulder during rightward carry.

1. Verify the packet, then play the 32.5-second walkthrough at normal speed. Follow the [visual index](visual/frame_index.json) to step through the frames. [Walkthrough](visual/walkthrough.mp4) Â· [Action board](visual/action_board.jpg) Â· [Manifest](manifest.json)
2. Play the same sequence yourself. Download the HTML and open it in Chrome or Edge with WebGL available. Tap the parked brush, then draw loops at the sink, sweep the bathtub, and draw loops at the toilet. Try releasing at both ends of the tub and changing costume while Roshan swims. [Offline playtest](bathroom_playtest.html)
3. Read the source and the original test evidence before writing your conclusions. [Reviewer brief](CLAUDE_REVIEW.txt) Â· [Scene code](raw/scene/scene.mjs) Â· [Browser receipts](evidence/) Â· [Rig source](raw/rig/)

The packet preserves the exact picture stream of the prior walkthrough. The offline HTML uses silent placeholders for the three protected family recordings. Cue positions and timing remain available for reviewing synchronization. Browser behavior and the recorded picture are the scope of this handoff. Godot integration, Android performance, child playtesting, and owner acceptance require their own evidence. [Picture stream check](evidence/visual_stream.json) Â· [Cue timing](evidence/movie_receipt.json)

## Object and interaction breakdown

Coordinates and distances below use the prototypeâ€™s 1024 Ã— 576 logical canvas. The browser scales the stage, then converts touch positions back to that coordinate system. Each object has separate art, contact geometry, and completion state where applicable.

| Object | Source and role | What changes during the action |
|---|---|---|
| Bathroom and scenery | Registered dirty and clean room plates. Windows, shelves, bottles, floor, furniture and decor outside the active fixture are scenery. | The camera stays fixed. Clean artwork is clipped to the current fixtureâ€™s outline. Review the boundary for alignment, spill, or unintended neighboring changes. [Dirty plate](raw/art/dirty.png) Â· [Clean plate](raw/art/clean.png) Â· [Outlines](raw/scene/fixture_outlines.json) |
| Mermaid Roshan | One 17-bone actor with Original, Ballet, and Magician skins. Left-facing head, crown and ponytail use registered donor art. The body and costume geometry reflect across the direction change. | Root, torso, tail, arms, wrist, hair, and eyelids have separate motion. The skin can change during travel without recreating the actor or restarting its phase. [Rig project](raw/rig/project.json) Â· [Wardrobe examples](visual/wardrobe/) |
| Brush | One painted sprite. Parked grip (933, 319), angle 1.35 radians. The source uses distinct handle grip, end-of-handle, and bristle anchors. | The hand moves to the parked grip before the held flag changes. Carry uses the posed palm as the anchor. Work changes angle and foreshortening to follow the bristles at the surface. [Brush art](raw/art/brush.png) |
| Sink | Basin centered at (555, 194), ellipse radii (46, 13). Brush circles around the inside. | Needs at least 205 px of credited travel, 1.06 turns of accumulated angular travel, seven of eight sectors, and 2.55 s of credited motion. Grime fades with progress, then the basin reveals the clipped clean plate while Roshan lifts the brush. [Grime](raw/art/sink.png) |
| Bathtub | Drained bowl centered at (250, 240), work radii (59, 21). The long horizontal sweep tracks the shallow bowl. | Needs 345 px of credited travel, 85 px of lateral span, two reversals, and 2.55 s of credited motion. A higher handle grip, deeper pitch, and different reach solve keep the bristles inside the bowl. The front lip can cover the brush and lower tail on separate passes. The drained plate stays in place for the finish. Grime fades and small gleams signal completion. [Grime](raw/art/tub.png) |
| Toilet | Bowl centered at (832, 259), ellipse radii (25, 8). The toilet reuses the sinkâ€™s grime art at a smaller size. | Uses the same angular, sector and duration requirements as the sink, with 129 px of credited travel. A tighter arm stroke and higher finish lift fit the compact bowl. The clean reveal is clipped to this fixture. |
| Input guide, bubbles and HUD | Procedural stage overlays in the scene source. The watch mode also shows its simulated contact position. | Guidance changes with the active phase. Bubbles depend on credited travel, and completion advances once per fixture. Assess whether the cue, brush, and payoff are understandable for a child who does not read. |

A touch starts work only in the active fixtureâ€™s hit area when Roshan is ready. The bristles follow a projected and smoothed target. Credit requires fresh intentional movement within the hit area. Holding still, starting on scenery, or leaving the target should earn no extra progress. Releasing returns the scene to ready and preserves earned progress, while the next touch starts a fresh local direction sample. The work arm opens and folds with the stroke. Brush angle and foreshortening absorb most of the reach before the remaining displacement moves Roshanâ€™s root. [Contact and progress logic](raw/scene/scene.mjs)

## Animation and timing

These are rounded **simulation times** from the captured 30 fps run. The first encoded picture already advances two 60 Hz simulation ticks, so use the frame index for exact movie positions.

| Time | Action | Acting and contact cues to inspect |
|---|---|---|
| 0.00â€“0.70 s | Wait for the brush | Parked brush, relaxed hover, idle hair and sparse blink. Check that the brush is the obvious first target. |
| 0.70â€“2.87 s | Approach brush | A 2.15 s rightward swim. Tail load and extension drive travel. Free arms have a staggered recovery and hair lags the push. Look for distinct propulsion, glide, and braking. |
| 2.87â€“3.70 s | Reach and take | Torso and working hand extend into the parked handle over about 0.82 s. Check the frame where the handle begins moving with the palm. |
| 3.70â€“7.67 s | Carry to sink | Leftward travel with 0.48 s entry and 0.47 s exit turn allowances around a 3.0 s swim. Check grip, direction change, brush against fin, and whether the turn reads as a single actor changing direction. |
| 7.67â€“12.47 s | Sink hover, circular scrub, reveal | Hover until 8.53 s. Follow the shoulder, elbow and hand during the loop. Completion near 11.53 s begins a brief pose bridge, a 21 px brush lift, and the clipped reveal. |
| 12.47â€“16.07 s | Carry to tub | Another leftward leg, with 2.65 s of swimming between the turns. Watch hand/brush occlusion and the move into the lower basin. |
| 16.07â€“21.93 s | Tub hover, lateral sweeps, reveal | Work starts near 16.93 s. Watch reach, rake, and the near lip during extension and both reversals. Completion near 21.00 s brings a 23 px lift, local gleams, and a departure from the same drained tub. |
| 21.93â€“26.20 s | Carry to toilet | Rightward 4.25 s leg. Free shoulder leads, elbow folds later, hand trails, and the brush arm remains steadier. Compare this phrase with left carry at the same screen scale. |
| 26.20â€“31.27 s | Toilet hover, circular scrub, reveal | Work starts near 27.03 s. The narrower arm phrase fits the bowl. Completion near 30.33 s lifts the brush 28 px and reveals the clean bowl. |
| 31.27â€“32.50 s | Finish and hold | Completion panel and quiet hover. Watch the hair and tail settle and check the finish remains readable. |

The travel implementation integrates thrust from the returning fluke, applies drag and advances the pelvis along a registered route. The brush mount bridges pickup, turns, and work. The free elbow retains its anatomical bend through recovery. The brush arm uses a quieter bend. The weight repair distributes right forearm influences along the limb and reduces arm influence at the hair fringe. The final pose adjustment eases the rightward free shoulder to keep the costume underlays within the same strain limits. Inspect whether each correction is visible at normal speed. [Animation settings](raw/scene/acting_profile.json) Â· [Binding review](evidence/swim_binding_review.txt) Â· [Revision history](evidence/iteration_summary.json)

## Reconstruct and verify

For a folder download, run **python -B fetch_packet.py MANIFEST_URL DESTINATION** using the immutable raw manifest URL from the handoff. It downloads and verifies only this packet. [Download helper](fetch_packet.py)

- Run **python -B verify_packet.py** inside the downloaded packet. It checks the per-file SHA-256 and the sorted payload digest.
- Run **python -B rebuild_review.py --output bathroom_playtest.html** to rebuild the silent HTML from the raw assets, renderer modules, template, profile, outlines and scene code. The output should match the manifestâ€™s HTML hash. The raw rig archive is the editable source for Rigby2D. The preceding rig is included for comparing weights. The original rebound recipe accepts input and output paths. [Rebuild script](rebuild_review.py) Â· [Weight recipe](raw/scene/rebind_arm.py) Â· [Rigby license](raw/renderer/LICENSE-MIT.txt)
- Run **node test_playtest.mjs all** from the packet with a current Node release and Chrome installed. An optional third argument supplies a browser executable. Other modes are **reversal**, **swapview**, and **video**. The video mode also needs FFmpeg and writes its result at the packet root. Run probes in a writable copy and save outputs separately from the manifest-bound originals. [Browser harness](test_playtest.mjs)
- For an eventual Godot reconstruction, begin with the logical stage and plate registration, then bind the brush and hand sockets, implement touch and phase transitions, and verify stationary/off-target behavior before adding acting. Recreate the tail-driven route and per-fixture work poses with contact constraints, then restore view-specific occlusion and feedback. Compare at the same camera size with the visual frame index. The two browser render layers and foreground effects describe draw order, not a production engine dependency.

## Prior evidence and open review questions

The earlier browser run completed all fixtures in all three looks. It recorded 1,746 geometry samples at 0.8033â€“1.1957 strain, zero triangle flips or geometry exceptions, and 1,100 active contact samples. Tests also checked two release/resume points at the tub and three live wardrobe swaps. Visual checks identified a still-abrupt facing swap, a longer trailing left brush arm, and brief brush/fin overlap. Compare those observations to your own playback and distinguish sampled measurements from what you observed in motion. [All looks and real touch](evidence/all_receipt.json) Â· [Reversals](evidence/reversal_receipt.json) Â· [Live swaps](evidence/swapview_receipt.json) Â· [Prior visual notes](evidence/visual_critic_rebound02.txt)

The family voice cue labels correspond to sink, tub and toilet arrival. Their prior encoded offsets were 7.633, 16.033 and 26.150 s. The public packet supports reviewing the visual lead-in and cue placement. The original recordings remain in the projectâ€™s protected workflow.

Matched pre-repair frames are included for both travel directions. Compare them to the same recovery samples in the current build, then check whether the differences are visible in motion. [Left before](visual/comparison/baseline-carry-sink-247.png) · [Left after](visual/comparison/rebound02-carry-sink-247.png) · [Right before](visual/comparison/baseline-carry-toilet-19.png) · [Right after](visual/comparison/rebound02-carry-toilet-19.png)

For the secondary audit, return the object/beat issue table, an ordered refinement plan, and a reconstruction checklist. Give each claim an exact time, frame or source symbol and say which evidence you personally inspected. [Reviewer brief](CLAUDE_REVIEW.txt)
