# SOL_MASTER_AUDIT — strict third-pass packaging

This packet records the strict review boundary for motion-reference reconstruction. It is not a delivery acceptance claim.

## Blocking gates

Every candidate is checked for visual quality, identity/anatomy, room and prop topology, causal action, lighting/style, camera restraint, and first/end-frame seam continuity. A strict `REMAKE` card is required for any failed gate; an `OMIT_WRONG_EVENT` row is removed rather than regenerated. A `KEEP_WITH_TRIM` row is usable only through its stated frame/time boundary and remains motion reference.

## Priority groups

1. **Wrong-game events and the two-pin Stuffie rescue:** remove basket/four-bunny/wing-blast inventions; preserve one Baby Eagle held by exactly two rescue-pin bunnies and the contact-driven release order.
2. **Castle and room topology:** preserve the four-tower castle, fixed room projections, fixtures, entrances, and child-readable scale; no perspective or landmark drift.
3. **Causal hand/tool/action seams:** show the actual entry, handoff, pre-contact gap, physical contact, and resulting state; do not begin after the action or replace it with a dissolve/teleport.
4. **Pool state and camera:** preserve dirty-to-clean order, fixed sources, two-front meeting, giant-pool geography, and restrained pullbacks/tilts.
5. **C11/C13 arena identity:** preserve the octagonal arena, Grand Puff's three-tier scale and cute face, contained effects, and the exact one-rainbow-bunny tiny-cradle coda.

## Trims and provenance

The five trim decisions (C10-S03, C11-S02, C12-S05, C13-S01, C13-S02) identify bounded useful motion-reference spans. Trimming does not repair the missing seam or make any frame accepted delivery art. All generator cards are one shot each, action-first, DRAFT, and explicitly `generation_ready: false` / `delivery_accepted: false`; full-frame delivery still requires independent frame-by-frame acceptance and provenance.
