# Day One — DaVinci game-cohesion draft V03

Editorial review only. These are real DaVinci timelines and rendered drafts,
not final accepted cinematics. Production playback and APK assets are unchanged.

## Open and review

Open `project/Day_One_Game_Cohesion_Draft_V03.drp` in DaVinci Resolve. The local
project is **Mermaid Roshan - Day One Game Cohesion Draft 2026-09-04**. If media
is offline on another machine, relink the `01_VERIFIED_SOURCES` bin to this
packet's `sources/` directory. Individual scene timelines are also saved as
`project/D1-Cxx.drt` files.

| Scene | Review MP4 | Duration | Game draft preview |
| --- | --- | ---: | --- |
| C00 Opening flight | [Watch](exports/D1-C00.mp4) | 24 s | Arrival event |
| C01 Landing / approach | [Watch](exports/D1-C01.mp4) | 11.5 s | After C00 |
| C02 Dirty Main Hall | [Watch](exports/D1-C02.mp4) | 11 s | Dirty-castle discovery |
| C03 Dirty bathroom | [Watch](exports/D1-C03.mp4) | 9 s | Before bathroom interaction |
| C04 Restored bathroom | [Watch V02](exports/D1-C04_V02.mp4) · [V01 history](exports/D1-C04.mp4) | 6 s | Bathroom cleanup completion; flood shot omitted |
| C05 Dirty pool | [Watch](exports/D1-C05.mp4) | 11.5 s | Before pool interaction |
| C06 Pool / Rumi | [Watch](exports/D1-C06.mp4) | 27 s | Pool cleanup completion; emergence gap remains |
| C07 Pinned Eagle selects | [Watch](exports/D1-C07.mp4) | 10 s | No — incomplete room continuity |
| C08 Stuffie restoration | No coherent assembly | — | No — wrong-event footage omitted |
| C09 Dirty art room | [Watch](exports/D1-C09.mp4) | 10 s | Before art interaction |
| C10 Restored art room | [Watch](exports/D1-C10.mp4) | 10 s | Art cleanup completion |
| C11 Boss approach | [Watch](exports/D1-C11.mp4) | 12 s | Actual boss trigger, before gameplay |
| C12 Castle recap | [Watch V03](exports/D1-C12_V03.mp4) · [V02 history](exports/D1-C12_V02.mp4) · [V01 history](exports/D1-C12.mp4) | 8 s | Four-shot recap after recorded boss victory / existing FRIENDS state; no rainbow-emergence claim |
| C13 Friends cleanup selects | [Watch](exports/D1-C13.mp4) | 9.33 s | No — Eagle action / rainbow emergence absent |

Run the exact Godot 4.7.2 project locally with the additional user argument
`--day-one-draft-movies` to opt into eligible event previews. For example:

```powershell
.\tools\launch_day_one_draft_review.ps1 -Visible
```

Use a disposable review save profile for a new Day One playthrough; existing
completed saves do not replay completed story events. Do not delete the child's
save. The launcher creates an isolated temporary Windows app-data profile and
verifies the exact engine version; it leaves the child's normal save untouched.
Tapping anywhere skips the movie. Missing/ineligible media uses the existing
game behavior. Draft files remain under `assets_src/`, excluded by the existing
Android export filter.

## What changed

54 active shot selections using 52 unique sources form 13 timelines (159.33 seconds total), including two incomplete
selects timelines that are deliberately not event-playable. Downloads was searched
before assembly: 40 Grok clips, one Imagine clip, and three earlier review masters
were found. Three clips improved the pool violet-light buildup, Roshan/Rumi hug,
and pinned-Eagle selects. Originals were preserved byte for byte.

V02 removes C04-S02's impossible bathroom-floor flood and C12-S03's modern
rectangular bedroom. Their V01 exports remain alongside V02 as rejection history;
runtime preview selects the current per-movie declared versions.

C12 V03 further replaces the false Bathroom and Art recap shots with the existing
room-correct C04 clean endpoint and C10 desk wake, then omits the unverified
friendship vignette. C04 remains V02; runtime uses each movie's declared version.

Picture edits are straight cuts and native 24 fps trims. Whole-frame scale-to-fit
preserves the narrower 1264×720 Main Hall source with black side padding. There is
no optical flow, interpolation, dissolve, subject crop, warp, or frame-hold repair.
The exports are video-only; the game retains its existing score and family voices.

The most important remaining gaps are Rumi's causal emergence, the Stuffie Room's
two-pin rescue/restoration, and Baby Eagle's cleanup plus the single rainbow-bunny
friendship ending. A recap or a similarly colored shot is not a substitute.

## Evidence and authority

- [Executable edit decisions](../../../design/day_one_davinci_draft_edit.json)
- [Assembly/source provenance](ASSEMBLY_MANIFEST.json)
- [Resolve timeline readback](RESOLVE_READBACK.json)
- [Exports and hashes](EXPORT_MANIFEST.json)
- [Runtime eligibility](runtime_manifest.json)
- [Decoded media verification](VALIDATION.json)
- [Game integration probes and tested source hashes](INTEGRATION_VALIDATION.json)
- [Complete packet file hashes](PAYLOAD_MANIFEST.json)
- [Downloads inventory](DOWNLOADS_INVENTORY.json)
- [Render review](RENDER_REVIEW.md)
- [Gameplay boundary evidence](../../../design/DAY_ONE_DRAFT_BOUNDARY_EVIDENCE_2026-09-04.md)
- [Cohesion decisions](../../../design/DAY_ONE_DAVINCI_COHESION_2026-09-04.md)
- [Source v3 handoff](../day_one_grok_handoff_v3_2026-09-04/README.md)

Source timing is zero-based `[in, out)`; DaVinci timelines begin at `01:00:00:00`.
Green/orange clip colors and shot markers distinguish retained footage from
provisional remake references. Strict audit decisions are preserved, not upgraded
by editorial selection. Review documents describe sampled visual evidence, not
full-speed human approval or full-frame delivery evidence.

`ARCHIVE_COMPLETE`, `GENERATION_READY`, and `DELIVERY_ACCEPTED` are not granted by
this draft assembly. The binding cinematic and device gates still apply. No game
room was redesigned to match a generated continuity error.
