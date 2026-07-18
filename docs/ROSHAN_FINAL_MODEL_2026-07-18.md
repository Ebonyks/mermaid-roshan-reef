# Roshan redesign — final model analysis & recommendation (2026-07-18)

Scope: compare the most recent Meshy generations (48-hour window) against the
codex rig-repair line, independently re-measure the defects from
`docs/ROSHAN_RIG_AUDIT.md` (2026-07-15) on every candidate, and recommend the
final shipping model.

Method: direct source-GLB linear-blend skinning in numpy (no Blender, no
Godot — same approach as the rig audit), plus the repo's own gates:
`tools/glb_check.py`, the 79-check `tools/audit_motions.py` motion cage
(the CI "Roshan full motion cage" step), and the CI probe-suite results.

## Candidate inventory

| Candidate | Origin | Tris | Joints | Textures | Status |
|---|---|---|---|---|---|
| `assets/characters/roshan_v4.glb` | **Meshy V5 "Rainbow Mermaid Princess"** (owner generation `0716022221`, 409,082 tris) → codex in-house pipeline: shrink/decimate to 39,999 + 728 hidden safety tris, 57-bone fitted rig, 8 hair-physics chains | 40,727 | 57 | 2× 1024² POT | **shipping primary** |
| `assets/characters/roshan_v3.glb` | Meshy multi-view (07-11 turnarounds), earlier rig fit | 41,341 | 57 | 1× 2048² POT | fallback 1 |
| `assets/characters/roshan_v2.glb` | Meshy multi-view hero (gen2 turnarounds, 07-12) retargeted onto the classic 26-bone armature | 15,493 | 26 | 1× 1024² POT | fallback 2 |
| `assets/characters/roshan.glb` (v1) | classic card-era sculpt | 15,540 | 26 | 1610×2048 **NPOT** | last-resort fallback |
| `gen2/meshy/roshan_v2/static.glb` | raw Meshy hero output (unrigged, 2048² maps) | 15,493 | 0 | 2048² | design source only (`.gdignore`d) |
| `gen2/meshy/roshan_playable/static.glb` | Meshy from `roshan_sprite.png`; Meshy auto-rig rejected the mermaid silhouette | 8,198 | 0 | 2048² | superseded |

Key clarification of the timeline: **the newest Meshy design and the codex
updates are not competing models — they converged.** The owner's Meshy V5
sculpt (source file datestamped 07-16, inside the 48-hour window) became the
*mesh* of `roshan_v4.glb`; the codex commits of 07-15
(`5085012` arm surfaces → `d023f6b` sculpt replacement + cohesive rig →
`a308e52` swim pose + hair physics, branch `codex/replace-roshan-meshy-v5`)
are the *rig and integration* around it. The 07-16→07-18 codex window after
that was world art (northern kingdom, fairy pond, reef, pass 3.5) and did not
touch Roshan.

## Stress test — did the codex repairs fix the 07-15 audit defects?

Independent re-measurement (direct GLB parse + LBS; rest-pose skin residual
≤ 1.3e-6 on all candidates, so the numbers below are trustworthy):

| Metric (audit defect) | Audit v4 (07-15) | **v4 now** | v3 | v2 (meshy retarget) | v1 |
|---|---|---|---|---|---|
| L-hand bound verts (>0.12) | 174 | **532** | 217 | 68 | 84 |
| R-hand bound verts | 705 | **633** | 819 | 335 | 122 |
| L-hand bind envelope | 0.034×0.057×0.040 | **0.120×0.135×0.092** | 0.19×0.20×0.12 | 0.18×0.15×0.32 | — |
| Shoulder→wrist chain L / R | 0.331 / 0.461 (39% off) | **0.4156 / 0.4156 (0%)** | 0.336 / 0.398 | 0.867 / 0.824 | 0.867 / 0.824 |
| L-arm torso-contaminated verts | 863 of 977 (med 30%) | **94 of 1002 (med 22%)** | 0 | 213 (med 39%) | 16 (med 59%) |
| Geometric shells | 4 | **1** | 1 | 1 | 2 |
| Non-manifold edges | 59 | **0** | 48 | 23 | 18 |
| 90° shoulder-swing max edge stretch L / R | (shards) | **0.045 / 0.049** | 0.35 / 0.60 | 0.54 / 0.99 | 1.02 / 1.02 |
| Tris >3× area at 90° swing L / R | 216+ | **28 / 62** | 99 / 118 | 63 / 383 | 136 / 286 |

Every confirmed defect from the rig audit is fixed in the current v4, and it
now has the cleanest deformation in the fleet by roughly an order of
magnitude. The small symmetric torso blend that remains on both arms (94 L /
200 R verts) is the deliberate narrow shoulder blend the audit's repair plan
called for, and the motion cage's tearing gate bounds it (worst edge opening
0.054 at chest/armU2).

Repo gates, re-run in this session:

- `tools/glb_check.py`: all 26 procedural bone names present on every rigged
  candidate; v4 additionally carries all 7 cosmetic sockets + 8 hair strands.
- `tools/audit_motions.py --glb roshan_v4.glb`: **79/79 PASS**, including the
  two checks that close the audit's remaining pose complaints — *"clap hands
  make contact"* (min centroid distance now gated < 0.15, vs the audited
  0.2775 near-clap) and elbow hyperextension/over-fold guards, plus the eight
  monotonic hair chains (7,745 strand verts, zero escape into shirt/skin).
- CI probe suite: green at the current master content (run `0ee5eec` on
  `codex/northern-art-audit`; the identical-tree master run was a concurrency
  cancel, not a failure). Today's docs-only master merge (`e95ea8b`) is
  running as of this audit.

## Recommendation — final model

**Ship `roshan_v4.glb` as the final Roshan.** It is the only candidate that
is simultaneously the owner's newest Meshy design (V5 rainbow-mermaid sculpt:
native complete hands, cohesive arms) *and* the best rig ever measured in
this repo. No further model generation is needed; the redesign should be
declared converged.

Supporting decisions:

1. **Do not promote the gen2 Meshy retarget (`roshan_v2.glb`) beyond
   fallback.** Its rig is the worst of the fleet (hand asymmetry 68 vs 335
   bound verts, median torso contamination 39–56%, 90°-swing stretch up to
   0.99). Its value — the turnaround-sheet look — has been superseded by the
   V5 sculpt. Keep it only as the load-chain fallback it already is.
2. **Retire `gen2/meshy/roshan_playable/`** (sprite-derived, rig-rejected,
   8.2k tris, 9.3 MB of repo weight). It serves no pipeline role and can be
   deleted or archived.
3. **Keep the v4→v3→v2→v1 load chain in `player.gd` unchanged** — it is free
   insurance and probe-covered.
4. **The one remaining promotion gate is human, not technical:**
   `ART_STYLE_AUDIT.md` holds v4 at 4/5 pending an owner Mobile-renderer
   screenshot review (face planes, ink weight, tail-seam continuity). That
   on-device look check is the final sign-off for the redesign.

Watch items (none blocking):

- **Triangle budget on the phone:** 40,727 skinned tris / 57 bones is 2.6×
  the classic model. Fine for a single hero instance under the Mobile
  renderer, but if the 3–4-year-old phone shows thermal throttling in long
  sessions, a decimated LOD from the same pipeline is the lever.
- **Open boundary edges (13,201 after weld):** a byproduct of
  decimate-keep-visible plus disconnected hair locks/cards. One shell, zero
  non-manifold edges, no tearing under the cage — cosmetic only; watch for
  edge shimmer on device.
- **Rigid hands:** no palm/finger articulation (single hand joint per side).
  The clap now reaches contact and reads correctly at this art scale; adding
  finger chains is not worth the rig risk for this audience.
- **Legacy NPOT texture `roshan_0.png` (1610×2048)** — flagged again by
  `ART_AUDIT_2026-07-18.md`. It only loads with the v1 last-resort fallback;
  resize/POT-pad or document as an exception at leisure. The raw 2048²
  Meshy source maps in `gen2/` are safely behind `.gdignore` (headless-import
  deadlock cannot trigger).

## Follow-up (same day): shoulder-stretch fix after owner review

Owner human review reported the raw Meshy V5 preview reading cleaner than the
committed v4, with **arm/shoulder stretching** in-game. Root cause confirmed
by a full-edge sweep of every verb timeline (the cage's tearing gate samples
30k of ~81k edges and had passed at the threshold): the worst tearing edge of
every arm verb is a **chest↔armU blend vertex at the shoulder crease** —
jagged weight splits make adjacent vertices move very differently when the
arm rotates (cheer raises 137°). The unrigged Meshy preview never
articulates, which is why it can't show this. Full-sweep worst edge opening:
wave 0.073, look 0.064, cheer 0.060, giggle 0.058, clap 0.055 — at the
player's 3.7× scale, up to 0.27 world units of visible stretch.

Fix shipped: `tools/smooth_shoulder_weights.py` — a harmonic (Laplace)
re-solve of the arm-fraction field over the crease band, per side (252
vertices, ≥92% owned by chest/spine1/root + armU, forearm/hand excluded).
Weights only: geometry, joints, textures, hair chains, and the rest pose are
bit-for-bit unaffected. Measured result:

| Motion | before | after |
|---|---|---|
| wave (worst offender) | 0.0732 | **0.0563** |
| cheer | 0.0595 | **0.0502** |
| clap | 0.0552 | 0.0550 |
| twirl / look / giggle / sleep / swim ×3 speeds | — | unchanged |
| cage stress arm region (99.9pct / max) | 0.050 / 0.054 | **0.044 / 0.050** |

Motion cage: **79/79 PASS** on the fixed GLB. Remaining smaller offenders are
neck↔arm collar edges (look 0.064, giggle 0.058); two attempted collar
smoothing passes moved the discontinuity instead of removing it and were
rejected — a proper fix needs a clavicle-style blend or authored collar
weights, noted as future polish, not a blocker. The sleep-curl tail
compression (0.117 at tail6–tail8) is pre-existing, unrelated to arms, and
reads as intentional curling on device.
