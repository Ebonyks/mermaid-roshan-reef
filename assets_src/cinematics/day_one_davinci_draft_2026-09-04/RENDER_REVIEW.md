# Day One Resolve draft render review — 2026-09-04

## Claim and method

All thirteen MP4 exports were inspected through start/middle/end contact frames, with boundaries verified against `RESOLVE_READBACK.json` and compared with `design/DAY_ONE_DRAFT_BOUNDARY_EVIDENCE_2026-09-04.md`. This is a rough-cut visual review, not full-speed listening, per-frame identity, device, or cinematic delivery acceptance.

**Overall: `EDITORIAL_REFERENCE_ONLY`. `DELIVERY_ACCEPTED`: false.** The hard-cut assemblies are tangible and useful. C01, C02, C04, C09, C10, C11 and C12 have readable short-form arcs. C03, C05, C06 and C07 expose important causal/topology gaps. C13 is a selects reel, not an ending.

## Per-movie review

| Movie | Strength | Gap / disposition |
|---|---|---|
| C00 | Calm plane exterior and warm Roshan/Daddy cabin relationship over 24 seconds. | Generic grey plane is not proven pearl-plane authority; endpoint is cabin preparation, not direct dock continuity. Preview only. |
| C01 | Plane at dock → offered hand → castle approach reads cleanly. | Closed-door arrival is missing; façade is not proven against live lagoon topology. Partial preview only. |
| C02 | Door, dirty-hall reaction, evidence and Bathroom glow form a compact discovery. | Hall architecture and side doors shift visibly; evidence insert is too broad. Preview, not topology authority. |
| C03 | Dirty bath → distressed swimmer → tool reach is immediately understandable. | Threshold crossing is absent; tub/sink geometry changes; end implies sink work rather than a clean pre-contact gap. Partial preview. |
| C04 | Scrub, clear-water response and bright restored settle make a readable reward. | Bunny exit is absent and the endpoint does not prove the exact clean pool-route handoff. Play only after runtime completion. |
| C05 | Dirty giant pool, skimming, blocked waterfall and mouth obstruction are child-readable. | No bunny pair or final problem map; camera scale and seahorse construction shift. Strong partial discovery only. |
| C06 | The strongest emotional sequence: plug, flows, clear water, violet light, Rumi and a stable hug. | Rumi emergence is absent; the cut jumps from empty violet pool to Rumi already present. Sources and Roshan scale drift. Partial pacing reference only. |
| C07 | Dark clutter and the pinned Baby Eagle ending preserve concern without horror. | Middle Roshan image feels sleepy, not investigative; room becomes hall-like and gaze/swing beats are absent. Selects only; not runtime eligible. |
| C09 | Best runtime-adjacent room draft: supplies, grime and readiness are clear in ten seconds. | Supply counts/counters shift and the final measurable brush gap is unproven. Preview; current runtime capture remains authority. |
| C10 | Scrub → stored supplies → clean room → desk wake reads coherently. | Desk geometry and Roshan scale change; final hand gap is ambiguous. Preview only after cleanup commit. |
| C11 | Route lights → door → arena → Grand Puff gives the clearest suspense/reveal arc. | Puff appears already settled; valid landing/contact and exact FRIENDS identity remain unproven. Suitable pre-boss preview. |
| C12 | Strong two-second room montage with a warm Roshan/Daddy hug. | Recaps are not exact runtime endpoints. Play only after canonical boss victory and rainbow-friendship completion; never manufacture either state. |
| C13 | Roshan, Daddy and Rumi each have a legible action fragment. | Missing Eagle lift, rainbow-bunny birth and complete endpoint; Rumi is only 32 frames/1.33 seconds. `SELECTS_ONLY_INCOMPLETE`; never runtime playback. |

## Seam findings

- Resolve readback matches intended ranges and hard-cut durations; no dissolve or interpolation appears in the readback.
- Whole-frame normalization yields 1280×720 exports, but source composition creates major scale/topology discontinuities in C02, C03, C05, C06 and C07. Normalization must not conceal them.
- C06's empty-violet-pool → Rumi-present cut is an animation gap, not a runtime transition to smooth over.
- C11's door-open arena → settled Puff cut still lacks landing/contact.
- The earlier runtime capture packet recorded separate Bathroom pool-route ownership/identity and Pool waterfall-unlock-after-clear failures. The focused integration probe proves movie/event routing, pool/art room-entry navigation, bathroom handoff ownership, C11 teardown/cancellation behavior, C12 presentation, and queue ordering; it does not rerun those separate waterfall or Bathroom gameplay assertions. Keep those gameplay findings open. See [`INTEGRATION_VALIDATION.json`](INTEGRATION_VALIDATION.json) for the exact command and result. Focus/device performance and human playback review also remain open.

### Per-cut inspection highlights

- **C04 S01→S02:** a tight stone tub scrub cuts to a wide room where blue water floods most of the floor. This is not continuous bathroom geography. **C04 S02→S04:** the flooded floor then cuts dry while the sink, mirror, tub and bunny positions all change. Keep the whole movie visibly provisional.
- **C06 S01→S02:** the mouth-plug close-up cuts to a much more decayed, differently scaled seahorse. **S02→S03:** dirty pool/seahorse geometry jumps to an empty, pristine pool. **S03→S04→S05:** rainbow source, seahorse and pool rim repeatedly change scale and placement. **S06→S08:** violet light ends with Roshan beside an empty pool; the next frame already contains Rumi. **S08→S09:** Rumi/Roshan scale, costume detail and framing jump before the otherwise stable hug.
- **C11 S01→S02:** hall axis and boss-door placement change. **S02→S03:** the shell door changes from gold/purple to bright pearl-white. **S03→S04:** an empty arena cuts directly to a fully settled Puff, omitting descent/contact.
- **C12 S02→S03:** the Pool recap cuts to a modern rectangular bedroom that does not resemble the established Stuffie Room; this is the montage's most serious wrong-location insert. **S04→S05:** Art Room jumps to the arena as intended, but no visual cause establishes friendship. **S05→S06:** arena friendship jumps to Main Hall family hug; acceptable montage grammar only after canonical gameplay victory/friendship.
- **C13:** both cuts change principal actor cleanly, but the sequence is cumulative cleanup fiction without the required Eagle and rainbow-bunny actions. Ending on the 1.33-second Rumi rinse is an abrupt incomplete stop, confirming selects-only status.

## Integration-code risk review (read-only)

The current direction is sound where boss/Chapter Two state is saved independently of optional media, C11 defers the boss rather than covering it, and C12 is requested on the Day Two side of canonical victory.

The focused current probe closes the movie-routing portions of the three risks below; it does not constitute an OS focus or device test:

1. **C00/C01 queue cancellation — closed by probe.** The real arrival hook drains C00 then C01 exactly once under skip.
2. **Bathroom handoff retry — closed by probe.** C03 serial playback, bathroom completion/C04, route ownership, and re-entry duplicate suppression all pass.
3. **Deferred boss/Day Two latches — teardown path closed by probe.** C11 skip enters the real Dust Boss, the probe's simulated lifecycle notification cancels the active encounter/re-arms the door, and C12 skip reaches the Day Two presentation. An actual OS focus-loss run and device/performance acceptance remain open.

No code change follows from still frames alone; these are focused test requirements.

## Acceptance still open

- Full-speed visual/listening review and approved audio.
- Human identity, anatomy, topology, contact and child-safe affect review.
- Exact repaired runtime start/end comparisons.
- `tools/audit_cinematic.py` full-frame provenance and neighboring-frame evidence.
- Mobile renderer and Lenovo Tab M11 playback, skip, pause, interruption and performance gates.

These drafts are useful production artifacts. They do not change `DELIVERY_ACCEPTED` from false.

## V02 selection improvement

C04-S02 and C12-S03 are removed from active V02 selections after cut-board review. C04 V02 is the six-second scrub → clean endpoint draft; C12 V02 is the ten-second five-shot recap without the false modern-bedroom insert. V01 renders and boards remain historical evidence of why those cuts were rejected. Revised exports require a fresh endpoint/cut-board check and remain `EDITORIAL_REFERENCE_ONLY`.

The replacement renders have now been checked in `review/D1-C04_V02_CUT_BOARD.png` and `review/D1-C12_V02_CUT_BOARD.png`. C04 contains no flooded-floor frame; it cuts from the final dirty-basin scrub directly to the bright clean-room/bunny endpoint. That is a much stronger six-second reward draft, while the instantaneous topology/state change remains provisional. C12 contains no modern-bedroom frame; its five shots are clean Bathroom bunny, Pool/Rumi, Art desk, arena friendship, and Main Hall family hug. No other selected cut was changed. Both remain `EDITORIAL_REFERENCE_ONLY`, with V01 preserved in history.

Subsequent C12 V03 selection review found that V02 still used a false purple-arch/water-window room for the Art recap and a generic clawfoot Bathroom. V03 therefore reuses the existing C04 clean endpoint for Bathroom and the room-correct `C10_S04_v1_desk_wake_OFFICIAL.mp4` for Art, omits the unverified friendship vignette, and retains Pool/Rumi plus the family hug. The intended V03 duration is eight seconds. C04 remains unchanged at V02.

Final V03 render confirmation: `review/D1-C12_V03_CUT_BOARD.png` shows exactly the selected four-shot order and three hard cuts. The false Art room, modern bedroom and friendship vignette are absent; the final frame is the stable Main Hall family hug. No hard technical break was found in the replacement edit. Its Bathroom endpoint remains a provisional generated room rather than exact runtime pixels, so the result stays `EDITORIAL_REFERENCE_ONLY` and makes no rainbow-emergence or progress claim.
