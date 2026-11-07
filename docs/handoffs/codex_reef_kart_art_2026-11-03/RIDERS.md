# Reef Grand Prix seated cast

The 2026-11-07 owner-requested appearance stress test started at `8d6d7cce6748d1fb7d6fcee243f2a4d21f2f3290`. Baby Eagle appeared as Sparkle in the garage. The original race view layered a portrait under the vehicle. The wheel hid Baby Eagle's beak and the Zoom Cycle's bars obscured many faces. Bunny and Kitty inherited cropped sides, and Mama's baby could disappear into the seat.

The PC garage now names Baby Eagle directly and previews the selected driver in the selected ride. Eleven missing rear views use three new art sheets based on the original cast. The chassis, seatbacks and controls come from the existing rides. The exporter places each torso at the controls and restores the seatback in front, producing one whole sprite per ride and pose. Baby Eagle has straight, left and right views with a fixed body and tire position. The other new drivers have one seated key. Their ride carries the existing boost and spin feedback. Roshan retains four existing poses per ride with registered tire contacts. Those keys and the solo Imp card now have mipmaps for distant views.

[Exact prompts, source hashes and export procedure](../../../assets_src/imagegen/reef_kart_riders_20261107/GENERATION.json)

## Review

| Evidence | Coverage |
|---|---|
| Posed baseline and candidate | All 36 character–ride pairings, in solo and in each split-screen seat. Five poses plus opponent-distance captures in split-screen. |
| Moving review | Three solo Baby Eagle runs and six split-screen pairings through the four room courses. Controller events are simulated with the normal game clock. |
| Contact checks | Registered Roshan tire anchors, fixed Baby Eagle chassis pixels, gutter clearance, atlas mip levels and shared split-screen resources. |

[Baby Eagle comparison](../../../audit/cycles/reef-kart-riders-20261107/baby-eagle-comparison.jpg) · [Go-Kart](../../../audit/cycles/reef-kart-riders-20261107/go-kart.jpg) · [Zoom Cycle](../../../audit/cycles/reef-kart-riders-20261107/zoom-cycle.jpg) · [Monster Truck](../../../audit/cycles/reef-kart-riders-20261107/monster-truck.jpg)

[Audit impact](../../../design/audit_impacts/reef-kart-rider-art-20261107.json) · [Runtime evidence](../../../audit/cycles/reef-kart-riders-20261107/RUNTIME_EVIDENCE.json)

Desktop appearance and runtime checks are scoped to the PC candidate. Physical controller, tablet, child and owner acceptance remain open.
