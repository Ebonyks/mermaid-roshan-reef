# Reef Grand Prix stage art

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
