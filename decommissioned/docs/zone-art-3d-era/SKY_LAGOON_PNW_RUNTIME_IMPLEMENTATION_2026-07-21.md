# Sky Lagoon PNW runtime implementation (GEN2) — 2026-07-21

## Why the accepted 2D set was never implemented

The twenty-four accepted flat prototype cards
(`assets_src/concepts/sky_lagoon_pnw_flat/`, audited in
`SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md`) reached `dev` as
modeling references only. Three things stalled the runtime translation:

1. The first 3D implementation (`codex/sky-lagoon-pnw-trees`) converted
   species facts directly into procedural Blender graphs **before** any 2D
   art direction was approved. It passed every technical gate (green run
   `29840034919`) but was visually rejected — repeated crown blobs,
   mechanical branch scaffolds, poor value separation, near-black shrubs —
   and the branch was abandoned unmerged.
2. The corrective flat-prototype pass deliberately shipped no runtime
   changes ("no shipped GLB or scene placement changes in this pass"),
   leaving GEN2+GEN5 as the stated safe fallback.
3. The follow-up modeling hand-off was never written: the next asset order
   (`CODEX_ASSET_REQUESTS_2026-07-21.md`) pivoted entirely to the Pearl
   Opera House, and every subsequent dev commit was opera work. The cards
   sat orphaned in `assets_src/`.

## What this pass does

This pass is the missing 2D-to-3D translation, built to the card grammar
rather than to species anatomy:

- `tools/build_sky_lagoon_pnw_woody_plants.py` is rewritten (style gate
  `sky_lagoon_pnw_woody_gen2`). Every plant is a single readable
  silhouette of two to five primary volumes — stacked scalloped skirt
  tiers for conifers, big rounded lobed crown clouds for broadleaves,
  chunky mounds/fans/arches for shrubs — with one or two oversized
  botanical ornaments and a compact planted base (root flares, stones,
  tufts). No branch scaffolds, no leaf-level geometry, no textures.
- The tree ornament correction is honored: bigleaf maple carries two
  paired V-wing samaras with olive-gold seed bases, black cottonwood
  three coral catkin/seed strings, Garry oak four sparse golden acorns.
  No leaf badges anywhere.
- The runtime shrub roster is the full accepted variant set: six species
  × two structurally distinct A/B prototypes = twelve shrub GLBs.
  Trailing blackberry (Rubus ursinus) replaces the superseded evergreen
  huckleberry; trailing/creeping/arch/tunnel silhouettes are exclusive to
  blackberry, and the B variants use the terraced, spear-fan, candelabra,
  tiered-wedge, and clustered-tower architectures from the sheet.
- `scripts/arena/sky_lagoon.gd` restores the ecological placement pass
  from the abandoned branch, extended to the variant roster: snow admits
  conifers only; alder/cottonwood/salmonberry hold wet banks (within 42
  units of water); redcedar/hemlock/spruce/yew/maple/dogwood/salal stay
  within 82 units; shore pine/madrone/Garry oak/Oregon grape/currant/
  oceanspray/blackberry keep at least 20 units from water; nothing grows
  from water, paving, masonry, rails, or reserved footprints. The pond's
  non-native willow pair is replaced by red alder and black cottonwood on
  dry bank; twelve hero trees and twelve hero shrubs remain individually
  auditable anchors.
- `scripts/probe_l2.gd` checks the full 24-role kit and per-role
  placement counts; `scripts/probe_sky_lagoon_art.gd` captures dedicated
  close views of all twelve shrub variants plus the existing tree,
  landmark, and stained-glass views.
- `tools/audit_sky_lagoon_kit.py` enforces the GEN2 contract: 24 woody
  roles, one authored root each, species/habitat/style-gate extras,
  500–7500 triangles (trees) / 500–6500 (shrubs), at most 8 materials,
  no textures. Current builds run 782–2224 triangles at 6–8 materials —
  far lighter than the rejected GEN1 family.

## Evidence

- Structural gate: `SKYKIT|RESULT|OK|assets=15|woody=24` locally.
- Isolated reviews: fixed 0°/45°/135° turntables and contact sheets in
  `assets_src/blender/qa_sky_lagoon_pnw_woody_plants/`. The QA renderer
  now uses the Standard view transform with non-clipping sun energies so
  reviews show true albedo values instead of AgX-washed pastels.
- Per-role decisions: `audit/sky_lagoon_pnw_woody_gen2_ledger_2026-07-21.csv`.
  Isolated card-grammar scores are 4.5–4.8; runtime scores stay pending
  until the Mobile capture artifact from `probes.yml` is reviewed.
- The Mermaid Roshan stained glass is untouched; its capture and hash
  checks remain in the probe suite.

Final acceptance still follows the standing gates: green probes on the
exact head, then owner review of the Sky Lagoon capture artifact. This
document records the implementation, not a 5/5 award.
