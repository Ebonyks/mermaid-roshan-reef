# Roshan v4 Pose Stress Test — 2026-07-18

Held-pose range-of-motion audit of `assets/characters/roshan_v4.glb`,
complementing the animated motion cage (`tools/audit_motions.py`). Four
requested extreme arm poses were posed via direct linear-blend skinning
(same numpy method as the rig audit and final-model analysis) and judged
on tearing, triangle blowup, body penetration, left/right symmetry, and
pose-goal reach. Harness: `tools/audit_pose_stress.py` (exit-coded,
CI-runnable). QA captures: `tools/out/pose_stress/`.

## Results — all four poses PASS within the rig's envelope

| Pose | Tearing (99.9pct / max) | Tris >3× area | Penetration | Verdict |
|---|---|---|---|---|
| Arms overhead (wide V, L 1.9 / R 1.8 rad) | 0.026 / 0.050 | 145 | 0.000 | PASS — hands at crown height, 1.9 cm hair clearance |
| T-pose (0.72 rad) | 0.010 / 0.019 | 53 | 0.000 | PASS — hands level with shoulders, full span |
| Hands on hips (elbows out, 1.7 rad bend) | 0.009 / 0.018 | 42 | 0.015 max | PASS — hands frame the hips, 63 verts touch ≤1.5 cm |
| Arms forward (parallel reach) | 0.012 / 0.030 | 53 | 0.000 | PASS — hands 0.38–0.44 forward, no arm crossing |

Deformation quality is uniformly excellent — worst edge opening across all
four poses is 0.050 (cage gate 0.12), and the deltoid/armpit regions hold
together at every extreme. No shearing, no candy-wrapper twist, no
detached shells.

## Findings — three real limitations documented

**1. The strict poses clip; the envelope poses don't.** Her proportions
are storybook-chibi: the arm chain is 0.4156 while the head+hair shell
spans x ±0.29 at raised-hand height, and max hand reach (y ≈ 0.556) is
below the hair crown. Consequences, measured:

- *Strict vertical overhead* (arms beside ears): hands pass **7.9 cm into
  the head/hair shell** (902 verts beyond 5 mm). Geometrically unavoidable
  — no pose keeps arms vertical without entering hair. The clean form is
  the wide V shipped in the harness.
- *Palm-on-hip contact*: unreachable without **7.6 cm forearm-through-
  torso** clipping (622 verts). The hand is a single rigid joint (no
  wrist), so the palm cannot rotate flat onto the hip. The clean form
  holds hands 0.14–0.20 beside the hips with fingertip-level contact.

**2. The shipped cheer (and mildly wave) animation peaks clip today.**
This was invisible until now — the 79-check motion cage gates tearing,
clap contact, hyperextension, and hair, but not body penetration:

- `cheer` peak (armU ±(1,0,∓3) @ 2.4): **7.5 cm max penetration, 1,233
  forearm/hand verts** inside the head/hair shell. Both hands bury into
  the hair for the ~1.3 s hold. Visible in
  `tools/out/pose_stress/probe_game_cheer_peak_front.png`.
- `wave` peak (armU2 RIGHT @ 2.8): 6.6 cm, 23 verts — a brief brush,
  minor by comparison.
- `giggle` peak: clean (0 verts).

Recommended follow-up (not applied here — it changes shipped animation):
retune the cheer apex in `player.gd` from 2.4 toward ~1.9–2.0 on a wider
lateral axis, mirroring the V used here, and add a body-penetration gate
to `audit_motions.py` so regressions are caught. Both files' cheer values
must move together (the cage hardcodes the same keys).

**3. The hand skin is ~5 cm off mirror-symmetric.** Joints are perfectly
symmetric, but the right hand/forearm mesh sits lower and further out
than the left (constant 0.070 mirrored-centroid gap in every pose,
including rest). This is baked into the Meshy V5 sculpt's decimation, not
the rig. At game scale it is cosmetic, but it is why the right arm needs
a 0.1 rad wider overhead angle and why the right hand seats closer to the
hip (0.136 vs 0.195). A future re-decimation could symmetrize the arm
topology; nothing blocks shipping.

## Method notes

- Penetration is measured as depth along the nearest body-surface normal
  (grid-hashed nearest neighbor over the 33k body verts, arm/hand verts
  excluded from the surface), tolerance 5 mm, probe = verts with >0.4
  forearm/hand weight.
- "Body" includes the fixed hair shell (head-bone weighted); strand-driven
  hair locks are excluded (they simulate away at runtime).
- Renders are painter's-algorithm QA captures (front + three-quarter per
  pose, arm mesh tinted); they confirm the numbers, they are not
  Mobile-renderer evidence. On-device captures remain the promotion gate
  per `ART_SCORING_GOVERNANCE_2026-07-18.md`.
