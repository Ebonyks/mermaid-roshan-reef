# Daddy Mermaid 2.5D animation contract

These atlases are the sprite-authoritative Daddy Mermaid used by the reef
friend standee, the rainbow melody stage, and the combat-victory cameo. A
future Daddy GLB must not silently replace these authored animation callsites.

## Runtime clips

All cells are 256x256 and all textures use a four-column layout.

| Texture | Grid | Frames | Playback |
|---|---:|---:|---|
| `daddy_idle.png` | 4x2 | 8 | seamless loop at 4 fps |
| `daddy_swim.png` | 4x4 | 16 | seamless movement loop at 8 fps |
| `daddy_gesture_a.png` | 4x4 | 4 per row | one-shot at 6 fps |
| `daddy_victory.png` | 4x2 | 8 | one-shot at 8 fps plus a 0.30-second final hold |

Gesture rows are zero-based in code:

- Row 0: friendly wave
- Row 1: welcoming invitation
- Row 2: happy clap
- Row 3: reassuring hug

The victory clip lasts 1.30 seconds including its final hold, fitting inside
the combat arena's 1.40-second post-win window. Victory has higher priority
than gestures; movement has higher priority than idle but cannot interrupt an
active gesture or victory.

## Art and build invariants

- Every frame contains one continuous colored Daddy silhouette before any
  white rim or navy shadow is added. The tail and both bifurcated fluke lobes
  must be the same connected anatomical component.
- Sticker styling is cosmetic and is never allowed to bridge detached anatomy.
- Frame extraction is global rather than a naive equal-cell crop because some
  accepted poses cross an idealized cell boundary while remaining separated
  from neighboring subjects.
- The build normalizes every complete frame to a shared torso target. Runtime
  code changes only `Sprite3D.frame`; it must not add per-frame position,
  scale, pivot, or anchor corrections.
- Every frame is nonempty and unique, preserves transparent edge clearance,
  and shows measurable lower-tail/fluke silhouette change.
- Runtime textures are no larger than 1024 pixels on either side and are
  authored for Godot's Mobile renderer.

Rebuild with:

```powershell
python tools/build_daddy_25d_atlases.py
```

Accepted native sources, hashes, exact prompts, rejected-pass history, and
protected-reference hashes are recorded in
`assets_src/imagegen/daddy_25d_tailmotion_2026-08-01/PROMPTS.md`.
