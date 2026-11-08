# Reef Grand Prix head and seat motion

The owner rejected the previous pose pass at `e233e003b0de17f58aa783cc3597c0f2d7ac1367`. In the earlier full turns, row-by-row stretching widened the Imp's ears and warped Kitty and Bunny. Sleepy's knit cap changed shape under steering and boost. [Before and after](../../../audit/cycles/reef-kart-rigid-heads-20261107/comparison.jpg)

Every selectable racer now starts with one painted neutral drawing for each ride. In a turn, the rider leans around the seat with a small rigid rotation. During a boost, the rider lowers toward the controls. The original cockpit foreground places the lower body behind the seat. Ear spacing, horn silhouettes, and the knitted cap keep the same painted geometry across the poses. Roshan uses her original helmet and hair from the neutral drawing on each ride. She is fitted once per ride so the whole helmet and tail stay in frame. Her upper head follows the rigid transform while the shoulder junction settles into the fixed cockpit. The solo Imp rival uses the same pose family as the selectable Imp.

One flattened sprite is rendered per driver. The intermediate turn and boost keys still settle through the neutral pose and both chase cameras read one shared state. [Source bindings and export recipe](../../../assets_src/racer_rigid_poses_20261107/JOB_CARD.json)

## Desktop review

[Go-Kart](../../../audit/cycles/reef-kart-rigid-heads-20261107/go-kart.jpg) · [Zoom Cycle](../../../audit/cycles/reef-kart-rigid-heads-20261107/zoom-cycle.jpg) · [Monster Truck](../../../audit/cycles/reef-kart-rigid-heads-20261107/monster-truck.jpg)

The independent shape test reprojects the painted head by the declared rigid motion and compares it to the exported key. It also compares the unchanged lower cockpit and tire pixels across each seven-key sequence. The baseline turn and boost keys are tested against the same standard. Normal-clock controller exercises cover all 36 driver and ride combinations in solo and in each split-screen seat. Four complete races cover the four courses. [Runtime evidence](../../../audit/cycles/reef-kart-rigid-heads-20261107/RUNTIME_EVIDENCE.json) · [Audit impact](../../../design/audit_impacts/reef-kart-rigid-heads-20261107.json)

Physical controller, tablet, child, and owner acceptance remain open.
