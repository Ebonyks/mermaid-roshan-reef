# Chuck Animation Spec v1 — acceptance standards

Audited by `tools/audit_chuck_anim.py` against the exported GLB (the artifact
the game loads). Every criterion is measured per frame; a clip ships only when
every criterion passes. Units: model space (dog ≈ 1.9 tall, ground at rest paw
height). Frame rate 24fps.

## Global criteria (every clip)
| ID | Criterion | Threshold |
|----|-----------|-----------|
| G1 | No joint pops: max per-frame bone rotation delta | < 30° / frame |
| G2 | Loop closure (looping clips): first-vs-last pose difference | < 4° per bone |
| G3 | No deep ground penetration by any paw | < 0.08 below ground |
| G4 | Root stays laterally centered (in-place clips) | \|x\| < 0.05 |

## run (16f loop) — playful bound gait
The chosen gait is a BOUND (both front legs move together, both hind legs move
together, hind pushes then front catches). This is a real dog play-gait and
reads clearly at toy scale. "Harmony" criteria:
| ID | Criterion | Threshold |
|----|-----------|-----------|
| R1 | Front pair sync: FL vs FR contact-window midpoint offset | ≤ 1.5 frames |
| R2 | Hind pair sync: BL vs BR contact-window midpoint offset | ≤ 1.5 frames |
| R3 | Front/hind alternation: front contact midpoint offset from hind midpoint | 40–60% of cycle |
| R4 | Each paw has exactly ONE contact window per cycle | 3–9 frames long |
| R5 | Airborne suspension phase (no paw in contact) | ≥ 2 frames |
| R6 | Root vertical bob: exactly 1 cycle, amplitude | 0.06–0.20 |
| R7 | Spine flexes with stride (chest-hips pitch range) | 8°–35° |

## sit_idle (48f loop)
| ID | Criterion | Threshold |
|----|-----------|-----------|
| S1 | Haunches near ground (hips-root drop vs stand) | ≥ 0.45 |
| S2 | All grounded paws stationary (max drift over clip) | < 0.06 |
| S3 | Tail visibly alive: tail-tip travel range | ≥ 0.10 |
| S4 | Head/neck subtle motion only | ≤ 12° rotation range |

## sit_excited (32f loop)
S1–S3 as sit_idle, plus:
| E1 | Front-right paw bounce present (FR paw z range) | ≥ 0.06 |
| E2 | Body hop amplitude (root z range) | 0.02–0.08 |
| E3 | Tail wag faster than sit_idle (≥ 2 full cycles per clip) | ≥ 2 |

## pickup (20f one-shot)
| ID | Criterion | Threshold |
|----|-----------|-----------|
| P1 | Nose dips to ball height (head-bone tip min z above ground) | ≤ 0.55 |
| P2 | Dip reached in frames 6–14, recovered by clip end (head back within 15° of start) | — |
| P3 | Hind paws stay grounded throughout | drift < 0.08 |

## wag (32f loop — win celebration)
| ID | Criterion | Threshold |
|----|-----------|-----------|
| W1 | ≥ 3 paws grounded + stationary (drift) | < 0.06 |
| W2 | Tail wag amplitude (tail-tip lateral travel) | ≥ 0.25 |
| W3 | Full wag cycles per clip | ≥ 3 |
| W4 | Butt wiggle accompanies tail (hips yaw range) | 4°–15° |

## Context mapping (verified in-game by probe screenshots)
| Phase | Clip | Why it makes sense |
|-------|------|--------------------|
| aim | sit_idle | waiting patiently, watching Roshan |
| fly | sit_excited | ball in the air — can't contain himself |
| fetch | run | full-speed chase |
| pickup | pickup | nose down to grab the ball |
| return | run | carrying it back |
| arrival/win | wag | proud delivery |

## Audit → regenerate loop
1. `blender --background --python tools/audit_chuck_anim.py -- --glb <glb> --out <dir>`
2. Read `audit_report.json` (per-criterion PASS/FAIL) + per-clip film strips.
3. Human review of strips for anything metrics can't see.
4. Fix pose tables in animate_chuck.py, re-export, GOTO 1. Ship only all-green.
