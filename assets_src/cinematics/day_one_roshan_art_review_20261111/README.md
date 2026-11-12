# Day One bathroom and Roshan rig art review

November 11, 2026. This packet supplies art for Claudeâ€™s bathroom revision and the owner-accepted Day One Rigby2D draft. Start with the original bathroom review, the follow-up work order and the accepted rig design. [Claudeâ€™s bathroom work order](https://github.com/Ebonyks/mermaid-roshan-reef/blob/12e04c6ee9a0d0bd6806c9b8dffda8622e708f4f/docs/handoffs/codex_bathroom_scene_revision_2026-11-11/README.md) Â· [Bathroom action board](references/bathroom_action_board.jpg) Â· [Packet manifest](manifest.json)

## Bathroom fixtures and payoff

| Work order | Art to review | How it fits |
|---|---|---|
| WO-A6 sink | [Registered clean sink](art/sink_clean_registered.png) | The ImageGen take supplies the finish reference. Color and brightness change on the source basin, trim, cabinet and plinth, whose coordinates stay fixed. A feathered fixture matte includes the brass faucet area. |
| WO-A6 toilet | [Registered clean toilet](art/toilet_clean_registered.png) | The original tank, lid, bowl and base supply all contours. A small aqua chip from the ImageGen take replaces the murky color inside the existing water opening. |
| WO-A5/A6 tub | [Registered water](art/tub_water_registered.png) Â· [Separate duck](art/rubber_duck.png) | Existing approved cyan water and duck paint were enough. The water is clipped inside the drained tub. Raise it from the bottom while drawing the existing lip in front. Float the separately anchored duck after the rise. |
| WO-A6 grime | [Grime test preview](evidence/grime_reuse_preview.png) | Existing sink and tub overlays are legible in the original fixture sizes. The toilet reuses the sink art at smaller scale. On the visibly changed footprints at 0.74 opacity, median CIE76 contrast is 36.35, 28.75 and 28.67 for sink, tub and toilet. |

The [registered preview](evidence/bathroom_registered_preview.png) shows all three local payoffs on the original drained room plate. The brightening is intentionally local. The sink and toilet take crops changed trim or scallops, so their full fixture pixels stay in [source takes](takes/) as review evidence. The displayed cutouts follow the original fixture geometry and preserve the room around them. [Original room](references/dirty_room.png) Â· [Matte and alpha measurements](evidence/static_verification.json)

## Roshanâ€™s Day One rig

- **R1 shoulders and sleeves.** The existing shoulder underlay and quarter-right paint supply the arm separation pilot. Use the original anatomy and per-look sleeves from the rig for the visible arm segments. [Approved figure](references/original_swim.png) Â· [Existing shoulder underlay](references/atlas_shoulder.png)
- **R2 hidden fills.** The neck and ponytail-root PNGs are small ImageGen donors for the parts newly exposed by head separation. Position and trim them beneath the source head and hair. [Neck](art/neck_underlay.png) Â· [Ponytail root](art/ponytail_root_underlay.png)
- **R3 hands.** Six transparent chips provide open palm, cylindrical grip and index point for both screen-side arms. Each 128 Ã— 128 chip has the same provisional wrist point at (64, 117). Relaxed hands come from the existing character paint. Keep grip sockets and brush depth tied to the palm when binding. [Hand sheet](takes/hands_take01.png) Â· [Crop and wrist map](registration.json)
- **R4 expressions.** Seven local feature donors cover wide eyes, smiling lids, gaze toward the child, worried brows, speech mouth, wide mouth and a closed smile. Align each chip to the existing eye or mouth landmarks and review the feathered seam on the original quarter-right face at play size. The generated full heads serve as source evidence. [Expression sheet](takes/face_take01.png) Â· [Isolated chips](art/)
- **R5 views.** The existing directional atlas and authored left-head paint supply the crossover and left-view source coverage. The work orderâ€™s first test is leftHeadScale = 1.0 and leftHeadDrop = 0 on that existing paint, followed by a width measurement within 1%. The front crossover still needs binding and in-motion checks. [Directional atlas](references/directional.png) Â· [Left-head source](references/left_head_original.png)

## Rebuild and review

Run **powershell -ExecutionPolicy Bypass -File build_review.ps1** on Windows with FFmpeg on PATH to rebuild the RGBA cutouts and static previews from the included references and takes. Run **python -B verify_art.py** with Pillow and NumPy to check the output and sealed file hashes. Registration values, source and output hashes, generation prompts and take dispositions are recorded in the packet. [Build script](build_review.ps1) Â· [Verification](verify_art.py) Â· [ImageGen job cards](job_cards.json)

The static export checks cover registration, transparency, hand wrist anchors, room pixels outside the fixture layers, and measured grime contrast. Rig binding, pose strain at full reach, animated tub fill and rim occlusion, full-speed and frame-step visual review, device performance, child testing and owner art approval remain open. The Day One gameplay integration and the findings MA-PLAY-004 and MA-ROSHAN-006 remain open.
