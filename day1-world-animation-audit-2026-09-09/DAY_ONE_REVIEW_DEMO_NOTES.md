# Mermaid Roshan — one continuous review and demo movie

Watch [the complete MP4](https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/day1-world-animation-audit-2026-09-09/MERMAID_ROSHAN_DAY_ONE_REVIEW_DEMO_2026-09-09.mp4).

137.666667 seconds (2:17.667), 3,304 native frames, 1280×720, 24 fps. Stereo sound includes 18 complete existing Roshan lines, contextual foley, ambience and continuous musical phrases across related scenes. The film is a cinematic montage for review/demo, not a recorded gameplay playthrough. Interactive gameplay between films is elided; no black placeholders or artificial stills were added to stand in for missing action.

## What changed

- Preserved the full owner-selected otter opening and the superior Downloads footage already incorporated in the V05 DaVinci edits, including the Rumi reunion.
- Inserted the latest reviewed bathroom, art-room, family-hug and hall-map trims in their actual source-local ranges, without stretching them to obsolete durations.
- Placed team cleaning and the locked `D1-C13-S05_FIX_ASSEMBLED_10s.mp4` before castle cleanup. The giant is intact in S04 and gone at the S05 friend-reveal cut.
- Retained multiple active cleanup angles. Omitted the failed C14 setup with the extra bird and the C02 invitation with simultaneous route glows.
- Omitted the entire art-completion voice line because the shortened pre-contact edit cannot support it. All remaining lines are complete, un-stretched and non-overlapping. No new speech or character imitation was generated; no embedded Grok audio is mixed in.
- Continued the finale music from the rainbow-friend reveal through the clean-castle payoff and family hug.

## Review points still visible

Times below refer to this single movie, not the earlier per-scene files.

| Movie time | Concrete limitation |
| --- | --- |
| 00:37.417 | The owner-selected opening depicts Daddy with legs at its endpoint; the next castle-door shot depicts his mermaid tail. This inherited join remains visible, not repaired or newly approved. |
| 00:39.667–00:42.667 | The corrected hall map is usable for geography but its dirt dressing remains weaker than the dusty reaction insert immediately following it. |
| 00:44.208 | The failed route-invitation beat is omitted. This montage cuts from dusty reaction to bathroom discovery; the game's interactive navigation is not shown. |
| 01:31.875–01:33.250 | The revised art-room approach cuts before unstable contact. The low shelved workbench is present; a proper contact/settle payoff remains missing. No duplicate hold or old bare-desk/rune shot fills it. |
| 01:41.750 | Boss encounter to team-cleaning edit elides the playable battle and helpers' arrival. It is not proof of a complete continuous encounter. |
| 01:49.250 | Owner-locked giant-clear hard cut: giant plus suds immediately before, four helpers plus one tiny rainbow friend after. Continuous suds removal is still not proven. |
| 01:53.750 | Team cleanup begins directly on Roshan and the tiny friend's paper action; the failed full-team setup is omitted. |
| 02:06.000 | Existing C14 contact/result hard cut changes dirty floor to clean. Use as rough editorial payoff, not evidence of continuous cleaning. |
| 02:12.000–02:17.667 | Brief clean-room recap and Day Two narration finish on the family hug. The retained pool recap and older film sources have not received a new full game-world audit in this compilation task. |

## Verification and acceptance

Machine checks: exact 24 fps and frame count, full audio/video decode, 14 chapter markers, original source hashes unchanged, muxed picture packet match, exact 6,608,000-sample authored audio endpoint. AAC decode exposes 896 padding samples beyond that authored endpoint; MP4 duration is correctly bounded. All 3,304 frames match their intended source indices in a reduced-resolution luma comparison (minimum per-frame PSNR 48.21 dB). This verifies the conform, not visual acceptance.

Sound meter: -17.7 LUFS integrated, 2.5 LU range, -3.5 dBTP. Existing `filler_v1` Roshan dialogue remains **provisional synthetic contextual** audio, not approval of family voices. No listening or device review is claimed.

Root inspected six join sheets covering all 24 newly assembled joins and the two internal reveal/result cuts. No new blank filler or wrong source order was found. Those sampled checks do not replace every-frame identity/topology review.

This movie is **ROUGH_DRAFT_MOTION_REFERENCE**, not production-final cinematic delivery. `DELIVERY_ACCEPTED=false`; no generation-readiness claim; no runtime changes; no owner/device acceptance granted. A new finished MP4 on GitHub does not cure the earlier source-tree archive or full-game gate blockers.

## Editorial package

`DAY_ONE_REVIEW_DEMO_EDIT_MANIFEST.json` contains exact 0-based, end-exclusive source and timeline ranges, hashes, cue positions and limitations. `DAY_ONE_REVIEW_DEMO_CHAPTERS.json` contains the movie's chapter times. The edit package contains the 25 conformed video segments, exact stereo mix, separate dialogue/foley/ambience/score stems, source plans/license ledger, comparison evidence and build scripts.

`DAY_ONE_REVIEW_DEMO_PORTABLE_RESOLVE.xml` reconstructs the same cut from the package's `parts/` and WAV media. Import into a **new** Resolve project at 24 fps; if media is offline, relink to the extracted package directory. Do not overwrite the earlier project. The source-range XML is also retained. These XML files are structurally checked but **not import-tested in Resolve**. The single MP4 is the immediately playable deliverable.

The new conform was rendered with FFmpeg from the pre-existing DaVinci V05 edited films and reviewed inserts. It was not rendered in a newly opened DaVinci session. Full-canvas encoding and straight cuts only; no visual interpolation, morphing, retiming, dissolves, compositing or generated filler was introduced.

The newly uploaded `QC_REVIEW_V2` response was narrowly checked during compilation. `D1-C02-R02_QCFIX2.mp4` still lights the blue drop alongside the pearls from approximately f12 onward (clear at f13–18 and f24/f48); the roughly 0.42-second exclusive opening cannot carry the required invitation action. It remains omitted. `C14-S01_QCFIX2_LOCKED_STILL_6s.mp4` is not a substitute for team action. This assembly uses the specific reviewed source hashes in the manifest, not filenames claiming approval.
