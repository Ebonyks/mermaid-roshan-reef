# Roshan playground cutoff repair — 2026-08-09

Status: **ACCEPTED 2D runtime repair**. Tool mode: Codex built-in image
generation, followed by the installed ImageGen chroma-key helper and a uniform
whole-canvas Lanczos resize to 512×512. No 3D source, model, rig, or render was
used.

## Triage

- `roshan_slide_2.png` and `roshan_swing_2.png` contained complete primary
  figures plus isolated right-edge generation debris. Their `_v2` files keep
  the original figure pixels and clear only the detached edge strip.
- `roshan_slide_3.png` and `roshan_swing_3.png` had their primary hair
  silhouettes cut by the left canvas edge. Complete 2D replacements were
  generated from the corresponding approved frame and accepted only after
  pose, identity, topology, alpha, component, and edge-margin review.
- Two slide candidates were rejected for material pose, face, or tail drift.
  They are not runtime assets and are not preserved here.

## Accepted prompt set

### Slide 3

The accepted built-in request used `roshan_slide_3.png` as the sole edit
target/reference. The normalized production request was:

> Re-create the same approved Mermaid Roshan sliding frame as a complete 2D
> storybook cutout on a perfectly uniform solid #00FF00 chroma background.
> Preserve her left-hand/right-hand sliding pose, joyful expression, pink
> ruffled top, brown hair with rainbow streak, curled rainbow-scaled tail and
> two-fin orientation. Repair the clipped left hair, keep the whole silhouette
> inside a square canvas with generous transparent margin, and add no prop,
> shadow, scenery, text, or extra object.

### Swing 3

The accepted built-in request used `roshan_swing_3.png` as the sole edit
target/reference:

> Create one polished replacement frame for this exact approved 2D game
> sprite. Keep Mermaid Roshan unmistakably the same child character and
> preserve the attached frame's exact swing pose and choreography: same joyful
> expression, both fists held at the same heights, same torso angle, same
> curled mermaid-tail direction, same two-fin orientation, same pink ruffled
> top with shell emblem, same brown hair with rainbow streak, and the same
> scale/framing. Repair only the production defect: her leftmost flowing hair
> is clipped by the canvas. Reconstruct the complete hair silhouette naturally
> and keep at least 12 pixels of clear margin around every edge. Match the
> attached soft storybook/anime linework, pastel rainbow scales, proportions,
> lighting, and detail level. Output a single square full-body character cutout
> on a perfectly uniform solid #00FF00 chroma background. No shadow, scenery,
> prop, ropes, text, border, checkerboard, or extra object.

## Processing and hashes

Chroma removal used:

```text
remove_chroma_key.py --auto-key border --soft-matte \
  --transparent-threshold 12 --opaque-threshold 220 --despill
```

| File | Role | SHA-256 |
|---|---|---|
| `roshan_slide_3_native_chroma.png` | accepted built-in native source | `be9f8a846cafed685625d72d99ed4463ea57b1748ba75ee31a2ba6cdee822cb4` |
| `roshan_swing_3_native_chroma.png` | accepted built-in native source | `10e0c299abfac2ad7c90ff7defb0d6628c7d035acb2046707f522e9e165a6f36` |
| `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2_v2.png` | cleaned runtime frame | `cb6cd27d5357bb59542bbdf95ef3fbf751759ce07046ea3607ec449c6a5d9613` |
| `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3_v2.png` | regenerated runtime frame | `8ec11afaf899b21548e4fdeeabc945cb90f5b62e6410a6319afaf22834e03271` |
| `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2_v2.png` | cleaned runtime frame | `211868892df1963e70300f71a02eb076b401d0af2dc2549ac229806cb99b7598` |
| `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3_v2.png` | regenerated runtime frame | `07cf65c0cc32189ca704a321e08ed9f90a6db04c666f6f086d4e8f99f33eb4be` |

The active audit requires a 512×512 alpha canvas, one visible connected
silhouette, no border contact, and at least eight pixels of margin for all four
revised frames.

## Runtime acceptance

The repaired roster passed `probe_l2.gd` under the exact Godot 4.7.1-stable
Mobile renderer. Its opt-in `PLAYGROUND_SHOT_OUT` path captured all four swing
compositions plus the two repaired slide poses as lossless full-viewport PNGs.
Human review confirmed that the accepted swing-frame hand anchor keeps both
fists on the ropes, the rider remains seated over the moving shell seat, both
slide poses remain attached to the chute, and no silhouette is cropped in the
child's real camera framing.
