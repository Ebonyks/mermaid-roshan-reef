# Reef Grand Prix turn and boost poses

The 2026-11-07 owner follow-up adds turning and boost posture to the selectable cast on all three vehicles. The baseline at `a71ec8bffd70441ef1f713b1ee0d100ce95721c0` held the rear view upright for ten cast members. Baby Eagle had authored head turns and reused the upright key during boosts.

The new Canvas cards use the existing rear-view paint. Each driver has an intermediate and full lean in both directions and an intermediate and full forward tuck. The upper silhouette moves over the shoulder line while the original grip, seat and tires keep their registration. The cycle leans farther than the kart and truck. Baby Eagle's strongest turns retain the authored side views. Roshan uses her existing authored pose sets. The solo Imp rival uses the same pose atlas as the selectable Imp. One atlas covers all three rides for each racer, and both chase cameras read the same motion state.

A first tuck flattened some heads. The second export moves the upper silhouette down while the shoulders compress. The driver returns through an intermediate pose when the boost expires. A turn settles through the middle before the boost tuck. Drift and zoom pickups use the same visual trigger because both set the race's boost state.

[Source bindings and authoring record](../../../assets_src/racer_pose_keys_20261107/JOB_CARD.json)

## Desktop validation

[Go-Kart](../../../audit/cycles/reef-kart-cast-motion-20261107/go-kart.jpg) · [Zoom Cycle](../../../audit/cycles/reef-kart-cast-motion-20261107/zoom-cycle.jpg) · [Monster Truck](../../../audit/cycles/reef-kart-cast-motion-20261107/monster-truck.jpg)

The test enters through the PC garage and drives each pairing at race speed in solo and both split-screen seats. Steering and boost use injected controller events on the normal game clock. Separate complete races exercise the same assets through all four rooms. [Exact runtime evidence](../../../audit/cycles/reef-kart-cast-motion-20261107/RUNTIME_EVIDENCE.json) · [Audit impact](../../../design/audit_impacts/reef-kart-cast-motion-20261107.json)

Physical controllers, tablet performance, child play and owner acceptance remain open.
