# Opera Gate Blockout Rollback

The Opera House gameplay uplift reached `origin/master` in commit `2227031`.
Its castle entrance was a functional visual blockout built directly in
`scripts/arena/castle_hall.gd`: gold box pillars and lintel, two crimson box
curtains, a rotated cube star, a translucent warm trigger veil, and a billboard
`Label3D` star.

The authored castle pass replaces only that visible assembly with
`assets/castle/pearl_kit/pearl_opera_gate.glb`. The veil, trigger position,
hysteresis, safe return offset, and Opera gameplay remain unchanged.

For exact rollback, recover `build_opera_gate()` from commit `2227031` and
remove the `pearl_opera_gate` placement/count from the castle art probe. The
original source remains byte-exact in Git; this folder is excluded from runtime
loading and records which version is the intentional rollback target.
