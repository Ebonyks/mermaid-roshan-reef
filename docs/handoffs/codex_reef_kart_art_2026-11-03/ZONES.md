# Racer room journeys — 2026-11-05

Status: playable topic-branch candidate. The demo freeze remains; this is not a dev/master release or master-audit closure.

## Owner correction and controls

The [owner request](../../../audit/cycles/reef-kart-zones-20261105/owner_request.json) supersedes the original touch brake requirement: the single pedal is **gas**, with gold upward chevrons. Holding it accelerates; releasing gas coasts. The touch stick retains one-finger steer-and-go. Desktop W/Up or controller A/right trigger is gas; S/Down or B/left trigger remains the separate desktop brake/reverse control. The PC right trigger ignores the first 5% of travel and keeps analog throttle above that point. Pause, focus loss and disconnect clear inputs.

## Four parts of each room

| Course | First quarter | Second quarter | Third quarter | Last quarter |
|---|---|---|---|---|
| Playroom | Block-building slalom | Stuffie nook | Tent camp and soft cushions | Music and toy parade |
| Kitchen | Breakfast china | Copper oven bakery | Cool fridge corner | Shell sink and drying corner |
| Mermaid Pool | Shell towel-changing alcove | Seahorse fountain garden | Floating flower shallows | Rainbow waterfall return |
| Opera Hall | Pearl lobby | Music-box rehearsal | Curtains and footlight stage | Backstage magic wing |

Every section owns its palette, floor material and fixed landmark stations. Woven mats, tiles, boards and shell diamonds blend near their boundaries, with flush gold thresholds. The room field stores circular lap phase alongside road distance, so the material follows each road section rather than a screen overlay. The distant floor uses a fixed room color, so each camera sees the same floor outside the zone band. Curbs and the ground start/finish plane still match the driving geometry. Playroom straights now have a gentle block slalom and tent approach.

The old modulo-prop scatter is removed. Fixtures occupy authored world positions with road clearance checks. The pool towel cabinet is an isolated derivative of the existing room fixture, not a room background pasted over the track. Existing fridge, sink, oven, toys, tent, fountains, waterfall, music boxes, curtains and footlights are reused directly. The chandelier hangs above its ground anchor. Kitchen bowls rest on the painted bowl base. PC pickups and item effects stay readable when passing the camera and close trailing karts fade before they obscure the driver. Full source and generation inventory: [reuse](../../../audit/cycles/reef-kart-zones-20261105/reuse_inventory.json), [one missing fixture and exact prompt](../../../assets_src/imagegen/reef_kart_zones_20261105/generation_job.json), [lossless export](../../../assets_src/imagegen/reef_kart_zones_20261105/runtime_exports.json).

## Spoken item explanations

A neutral Guide explains the held item when its roulette completes, and explains the starting Zoom at GO. The embedded career defers this opening explanation through its existing four-second instruction window, preserving the steering sentence. Protected family recordings are unchanged. Both PC seats share one bounded speech queue. Simultaneous identical awards share an explanation. Spending an item clears its waiting explanation while a cue already speaking can finish. The embedded career uses its existing required voice lane and music ducking. Item icons remain visible while guidance plays. Touching the item icon skips familiar guidance. Pause, disconnect, focus loss, retry, result and teardown clear obsolete guidance.

| Item | Exact speech |
|---|---|
| Zoom | Zoom boost! Use your item button for a burst of speed! |
| Sparkle | Sparkle bubble! Use your item button to spin the imp ahead! |
| Sparkle, two players | Sparkle bubble! Use your item button to spin the racer ahead! |
| Kelp | Kelp trap! Use your item button to leave slippery kelp behind! |
| Pearls | Three pearls! Use your item button to collect them and raise your top speed! |

Five local Kokoro af_heart calls: four item explanations plus the two-player sparkle variant, no family cloning or paid API. One native cue survived an export-parser failure and was reused unchanged; the failure and initial source are preserved. All runtime cues are 48 kHz mono Vorbis, 96 kbps, measured around -16 LUFS-I and below -1.5 dBTP. [Generation evidence](../../../assets_src/audio/reef_kart_items_20261105/candidates/generation_manifest.json). Machine checks do not establish pronunciation, speaker, mix, child or device acceptance.

## Evidence and acceptance

The [impact record](../../../design/audit_impacts/reef-kart-zones-20261105.json) owns exact commands and results. Runtime captures distinguish posed section views from a continuously simulated towel-area pass; neither is a claim of child play or canonical QA11 certification. Canonical visual acceptance, human listening/mix, physical USB/Bluetooth, Lenovo Tab M11/older-phone performance, child comprehension and owner acceptance remain open. MA-OPERA-014, MA-VIS-008 and MA-AUDIO-001 retain their existing lifecycles.

The 2026-11-07 normal-speed solo and split-screen review follows the [full-speed impact](../../../design/audit_impacts/reef-kart-full-speed-20261107.json). All eight races finished before and after repair, and both seats crossed all zones on both laps. Late instructions fell from 36 to zero. All 76 repaired speech starts matched the recorded master waveform. The drive used simulated controllers at normal game speed. Physical device, human listening, child and owner acceptance remain separate.
