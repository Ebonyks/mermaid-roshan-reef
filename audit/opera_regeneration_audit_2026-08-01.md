# Opera regeneration audit — 2026-08-01

- Accepted generated candidates: 74
- Rejected candidates: 8
- Accepted score range: 4.8–4.8; mean 4.80
- Human gates: identity/topology, child-readable silhouette, canonical prop
  continuity, no clipping/neighbor debris, and imp marine-motif prohibition.
- Native masters: retained under `assets_src/concepts/opera_regeneration_2026-08-01/cards/` with SHA-256 evidence in the ledger.
- Delivery transforms: full-canvas resize for approved sheet/finale outputs;
  deterministic edge-field matting and fit for actors/props; no subject warp,
  interpolation, compositing, or pixel borrowing.
- P3-01: rejected for runtime use at 1254x1254; kept review-only.
- P3-02: not generated because the request makes it owner-opt-in and no opt-in
  was supplied.
- P3-04: deferred; the available generator's 1672x941 wide output cannot meet
  the binding native 2048x1152 gate. Current code-native stage art remains the
  compliant runtime path.
- Lamba: accepted owner-directed replacement for rabbit-fish/bunny-fish art.
  Protected source art and family voice files were not modified. Remaining
  voice and legacy-3D migration is assigned to Fable in the dated handoff.

## Validation

- Python compilation: PASS for the evidence, promotion, actor, and prop tools.
- GDScript parser and inference lint: PASS for
  `scripts/opera_career_world_2d.gd`.
- Godot import: PASS with Godot 4.7.1.
- `probe_opera_2d`: PASS for all twelve careers, including magician.
- Full `scripts/ci.sh` after reconciling `origin/dev`: FAIL outside this
  change's scope. With UTF-8 console output enabled, current `dev` reports
  visual-design errors for the Fairy Pond background and Sky Lagoon
  reversibility/parallax/background hierarchy, followed by stale Castle
  interaction manifest hashes. The Opera visual-design result is an orphan-art
  warning only; the dedicated Opera 2D probe passed all twelve careers in the
  earlier complete wrapper run.
