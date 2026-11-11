# Reef Grand Prix stage art

## Course mechanics and original cartridge study

The November 10 course pass starts at `702471773fbc5280e06e73688a5f7d392d9b1f2d`. The reference run used the local 512 KiB US Super Mario Kart cartridge image in Snes9x. Its header reads `SUPER MARIO KART` and its SHA-256 is `2ada8919688087be60a6a48cace8f877add60c45d2e5d09e2442faa55be62a49`. Course selection, driving and the loaded Mode 7 tilemap came from that image. The ROM bytes were also inspected directly using the published overlay and object addresses. The ROM and emulator captures stay outside the game. [Nintendo instruction manual](https://www.nintendo.co.jp/clvs/manuals/common/pdf/CLV-P-SAAFE.pdf) · [ROM overlay addresses](https://smkdan.eludevisibility.org/smkovlof.html) · [ROM object clusters](https://smkdan.eludevisibility.org/smkomush.html)

| Original observation | Reef Grand Prix implementation |
| --- | --- |
| Mario Circuit 1 gives the wide paved line a clear curb and puts the pipes in specific clusters. Its ROM overlay table has three strip records of type 28. | Playroom Speedway has a block slalom with staggered sides, a wide rug cut through the bend and a boost on the cut. |
| Mario Circuit 2 puts its permanent launch strip near the end of an alignment straight. In two controlled emulator starts near the ramp, the aligned kart went airborne and the offset approach stayed grounded. Its overlapping roads read as different surfaces at the crossing. | Copper Pan Circuit places a narrow serving-board cut across the inside of the return hook. An offset pad rewards lining up the cut. Teapot and pitcher obstacles sit on the longer route. |
| Ghost Valley 1 shows an alternate landing before the player commits to the gap. The live tilemap confirms the open gap, and a paired run from the same emulator state showed that a standard hop carried farther into it. Both trial lines stopped short of the landing. Donut Plains 3 distinguishes a narrow bridge deck from surrounding water. | Seahorse Bridgeway has the narrowest shortcut, with a separate colored boardwalk across the shallows. Flower and star floats drift across part of the wider route. |
| Bowser Castle breaks its route into timed obstacle clusters. Rainbow Road spaces its strip overlays across several different sections. | Footlight Finale offers a rehearsal-carpet cut around the sweeping right corner, a moving music-box obstacle on the long line and a trophy to dodge near the lower turn. |

Each course has two main-line boosts and one alternate-line boost. The visible pad footprint is shared with contact logic. Each pad activates once per lap for each kart, in the forward direction. Obstacles cost speed briefly and leave steering available. Static and moving props reuse the existing painted room art. Shortcut surfaces and arrows are drawn on the world plane from the same endpoints and width used by driving. The shortcut uses a forward entry and rejoin within the same lap, with reversible signed progress and no course relocation. A sparkle fired on the alternate line follows that line to the merge. The [impact record](../../../design/audit_impacts/reef-kart-course-features-20261110.json) records machine and external acceptance separately.

The final PC check ran 151 assertions through the game checkout. Eight full split-screen races used two independently injected controller streams. Both racers completed at least one lap in every run and a driver reached the results screen. The shortcut driver took the alternate route on both laps of each challenge run.

| PC course | First finish on main-line run | First finish with shortcut | Difference |
| --- | ---: | ---: | ---: |
| Playroom Speedway | 26.22 s | 25.70 s | 0.52 s |
| Copper Pan Circuit | 47.03 s | 41.22 s | 5.82 s |
| Seahorse Bridgeway | 92.42 s | 89.02 s | 3.40 s |
| Footlight Finale | 87.92 s | 85.52 s | 2.40 s |

The 32 Mobile renderer captures cover each approach, cut, obstacle and main-line pad in both modes. They establish the rendered positions and both camera compositions. The Windows package starts all four courses with both seats and loads their art. Physical-controller and child/owner play remain open.

## November 7 stage art pass

This pass starts from `77252935800b8146694d1eceba930309f7999c8c` on the standalone PC demo branch. The four room paintings, sixteen zone themes, curb geometry and item rules are the existing reference. The approved room paintings remain as the far wall and surface source. The additions are isolated transparent cards placed in world space, with one distinct silhouette per zone, a wall-light grade, and separate collectible and cooldown art.

## Mario Kart reference study

| Reference | What works at speed | Reef application |
| --- | --- | --- |
| Ribbon Road | The oversized toy room reads at the horizon. Intermediate toy clusters change as the road turns, while the road edge carries a consistent border. | Build a block castle, reading fort, tent camp and toy station at different points beyond the Playroom shoulders. Keep low toys and established curbs at the closest layer. |
| Donut Plains 3 | Water, bank, and bridge are readable from their silhouettes and materials. The bridge is an event inside a continuous route. | Use distinct pool cabanas, fountain, lily island and waterfall beyond the rails. Keep the crossing and gold thresholds legible under the same camera. |
| Sweet Sweet Canyon | Familiar objects can be large and detailed when each area reserves one large readable shape. Multiple equivalent props at the same scale flatten the scene. | Shift the Kitchen from china service to bakery to preserves to the shell washing station. Keep smaller room props at the roadside scale. |
| Electrodrome | Stage architecture frames the bends, with stronger color and silhouette changes than the outer walls. | Use a balcony, rehearsal organ, proscenium and moon wing. Reserve the signs, curb and pickup row for driving information. |
| Nintendo item box and coin guide | Repeated silhouettes and consistent placement tell the player what they can collect and which line to choose. | Teal shell capsules and round gold pearls read differently. A low lit socket anchors an available capsule. The same spot is dark and empty during the existing cooldown. |

Official sources are the [Nintendo course gallery](https://www.nintendo.com/sg/switch/aabp/sp/course/index.html), [Nintendo driving and item guide](https://www.nintendo.com/jp/ichikara/aabpa/index_en.html) and [Nintendo course-design interview](https://www.nintendo.com/au/news-and-articles/ask-the-developer-vol-18-mario-kart-world-chapter-2/). These references informed composition and visual hierarchy. All painted additions use Mermaid Roshan room identity.

## Art and placement

Five built-in ImageGen sheets supply sixteen scenery cards and four pickup states. Native outputs and project room references are recorded in the [generation record](../../../assets_src/imagegen/reef_kart_stage_art_20261107/generation_job.json). The export trims disconnected alpha residue, preserves the antialiased contour and uses padded, mipmapped 1024-square scenery atlases plus a 512-square pickup atlas. Existing small room fixtures remain in the foreground. The larger cards use the same ground and camera projection in both seats.

| Course | Zone sequence |
| --- | --- |
| Playroom Speedway | Block castle, pillow reading fort, star tents, toy clock station |
| Copper Pan Circuit | Tea buffet, copper bakehouse, preserves hutch, shell washhouse |
| Seahorse Bridgeway | Changing cabanas, seahorse fountain, lily island, rainbow grotto |
| Footlight Finale | Opera box, pipe organ, footlight proscenium, backstage moon wing |

The first stress sweep found that the narrower camera could crop scenery and that nearby props blocked the new silhouettes. A horizon discontinuity and round pearl shadows also made some objects appear disconnected from the ground. The second pass placed scenic cards against sightlines in the narrower pane, penalized overlapping foreground props, blended the floor and wall at the horizon, and gave the new scenery and pearls flattened contact shadows. The course geometry and pickup timings are shared with the incoming branch.

## Playroom die-cast Easter egg

A stationary 2021 Crosstrek toy sits on a low shelf in the final Playroom sector. The existing roadside placement and landmark renderer handle its support and projection in both cameras. No discovery action or reward is required.

The factory finish is **Cool Gray Khaki**, code **PAF**, a muted blue-gray. The body gradient uses representative sRGB pixels from the model-year color gallery, including `#949eaa` on the center door, `#9aaaba` on the hood and `#6f7d8b` along the lower body. These are digital image samples under the gallery lighting. Original vector paths depict the raised rails, hatchback profile, wheel cladding and front fascia. Subaru’s artwork remains reference material. [Subaru US model-year brochure](https://www.subaru.com/content/dam/subaru/downloads/pdf/brochures/2021/crosstrek/2021_Crosstrek_Brochure.pdf) · [2021 Crosstrek gallery](https://www.subaruhawaii.com/2021Crosstrek.html) · [2021 Crosstrek paint-code bulletin](https://static.nhtsa.gov/odi/tsbs/2020/MC-10179430-0001.pdf)

[Scoped audit and verification](../../../design/audit_impacts/reef-kart-crosstrek-20261108.json)

## Desktop review

Each course runs the same ten visual scenarios in solo and split-screen. The sweep covers all four zone approaches, three internal zone boundaries, a ready item row, a collected capsule on cooldown and the finish wrap. Each scenario takes three successive frames at a race-speed spacing, for eighty cases and 240 frames. The position sweep is accompanied by eight full real-time races from the normal garage and controller input path.

| Desktop check | Result |
| --- | --- |
| Scenic approaches | Four different landmark silhouettes per course appear from both cameras. Nearby props still pass in front briefly where the course turns. |
| Section joins and finish wrap | The room lights and materials blend across joins, the lane rails remain continuous, and the wide ground checker stays visible at the finish. |
| Pickup and cooldown | All four courses show a bright capsule and separate pearl silhouette. A successful contact removes the capsule and leaves the socket visible until the existing timer refills it. A player already rolling an item leaves the available capsule in place. |
| Full-speed race path | Eight finishes, both laps’ four zones observed per seat, 106 item awards, and a median 60 FPS in all eight runs on the tested PC. The solo Kitchen and Pool races finished after one Imp-triggered restart each. |

- [Four-course preview](../../../audit/cycles/reef-kart-stage-art-20261107/stage-preview.jpg)
- [Playroom review sheet](../../../audit/cycles/reef-kart-stage-art-20261107/playroom.jpg)
- [Kitchen review sheet](../../../audit/cycles/reef-kart-stage-art-20261107/kitchen.jpg)
- [Pool review sheet](../../../audit/cycles/reef-kart-stage-art-20261107/mermaid_pool.jpg)
- [Opera Hall review sheet](../../../audit/cycles/reef-kart-stage-art-20261107/opera_hall.jpg)
- [Runtime evidence](../../../audit/cycles/reef-kart-stage-art-20261107/RUNTIME_EVIDENCE.json)
- [Audit impact](../../../design/audit_impacts/reef-kart-stage-art-20261107.json)

All 82 repository gameplay probes were verified. The aggregate run flagged two Slide input assertions, and the exact affected probe passed all three isolated reruns. The Racer-specific probes passed 115 assertions.

Desktop review uses the approved Godot 4.7.2 Mobile renderer. Physical controllers, Android performance and observed child and owner visual acceptance are separate.
