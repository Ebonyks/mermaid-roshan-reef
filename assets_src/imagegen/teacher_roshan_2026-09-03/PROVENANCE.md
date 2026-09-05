# Teacher Mermaid Roshan actor provenance

## Scope and reuse decision

No Teacher Roshan career art existed in the repository. The established Opera
Roshan 4x4 actor family was reused as the format, scale, identity, and motion
contract; only the missing teacher costume and teacher gestures were generated.
Learning cards remain separate gameplay art so letters, numbers, and shapes can
stay crisp and be changed without regenerating Roshan.

## Accepted source and derivatives

- Generation method: OpenAI built-in ImageGen.
- Selected result: `exec-5cc28ed5-8d15-4e7c-9438-1fffb7501145`.
- Identity reference: `assets/characters/roshan_25d/roshan_base.png`.
- anatomy/layout reference:
  `assets/opera/worlds/actors/animation/roshan_doctor_sheet_a.png`.
- Teacher costume reference: rejected attempt 1, used only to preserve the
  successful outfit language while repairing its missing fins.
- Native selected source:
  `raw/teacher_roshan_sheet_raw.png`, preserved unchanged at 1254x1254 RGB;
  SHA-256 `609f68a7fd2ddcb94858339cd641a982b73964058e840497c914f1782a3a72df`.
- Alpha native: `teacher_roshan_sheet_alpha_native.png`, 1254x1254 RGBA;
  SHA-256 `09dd9d7ec5e0b641cd12c1a80ede88691a8ff41265de319edd2b7238e671a065`.
- Runtime atlas:
  `assets/opera/worlds/actors/animation/roshan_teacher_sheet_a.png`,
  1024x1024 RGBA;
  SHA-256 `2bddeebd6ca4fe0647e1f6deb670bfcab4d1183f36417e0a033e59c4788dd28c`.
- Static fallback actor: `assets/opera/worlds/actors/roshan_teacher.png`,
  512x512 RGBA;
  SHA-256 `5f63276e14d55969d6103c8cbf94fce6a0154c5e4900a44f9ea485885b7bcb7a`.
- Pack report: `teacher_roshan_sheet_pack_report.json`;
  SHA-256 `23e94f23de0d2a5abc2db89772c186257e9524739be509dae414f69f7b2c1c3d`.

`tools/build_teacher_actor.py` removes only border-connected neutral
presentation pixels. It then calls the established
`tools/prepare_opera_roshan_animation.py` packer, which groups each complete
figure by source-cell centroid and applies one shared scale with safe 256px-cell
padding. The static fallback is idle cell zero, uniformly resized as a complete
cell in premultiplied-alpha space. No subject pixels were repainted,
composited, warped, or selectively resized after generation.

## Human and technical review

- Identity, age, face, brown hair, and rainbow streak match Roshan: pass.
- Teacher costume is child-readable at gameplay scale: pass.
- Exactly sixteen figures in idle/travel/work/cheer rows: pass.
- Every figure has one continuous mermaid tail and a visible terminal fin: pass.
- No human legs or split lower body: pass.
- All four teaching pointers are attached to a hand: pass.
- Actual alpha outside figures: pass.
- Every packed cell is nonempty and has at least 16px nominal safe padding:
  pass; exact bounds are recorded in the pack report.
- External learning cards are not baked into the actor: pass.

## Rejected attempts

- `exec-ec83280f-cd63-4868-9658-b4124c0944fe`: the teacher design and layout
  were useful, but multiple idle/work figures ended in tail stumps without a
  fin. Preserved unchanged as
  `rejected/teacher_roshan_sheet_attempt_1_missing_fins.png`; SHA-256
  `5fff0a0349482f6300d4f0ace052b59355afc9827884a7a0c405cbdfd3a6ce4d`.
- `exec-559fd40a-90e8-42a7-b35a-c8bf4067792a`: rejected entirely because a
  transparency-only edit regenerated an opaque vignette and changed atlas
  geometry. It is not stored in the repository and none of its pixels entered
  the delivery assets.

## Exact accepted prompt

```text
Use case: stylized-concept
Asset type: corrected production 2D game character animation atlas for Mermaid Roshan: Reef of Light
Input images:
- Image 1 is the exact approved Mermaid Roshan identity reference: face, child age, brown hair and rainbow streak, body proportions, rainbow tail colors, and large two-lobed fin.
- Image 2 is the approved Opera Doctor Roshan atlas and is the binding anatomy/layout reference: every one of sixteen figures has one complete long mermaid tail and a fully visible large two-lobed fin inside its cell.
- Image 3 is the prior Teacher Roshan candidate and is a costume/design reference only: preserve its aqua blouse, lavender scalloped vest, coral bow and pouch, badge motif, friendly preschool-teacher character, and coral pearl-tipped pointer. Correct its missing-fin defect.
Primary request: regenerate Teacher Roshan as an exact 4-column by 4-row animation atlas for future Opera House learning games about letters, numbers, and shapes.
Atlas layout: exactly sixteen separate full-body figures, four columns by four rows, read left-to-right. Reduce each figure enough that the complete hair, both hands, pointer, one long tail, and one large two-lobed fin have generous clearance inside their own cell. No overlaps across cell boundaries.
MANDATORY TAIL TOPOLOGY IN EVERY SINGLE CELL: exactly one continuous thick rainbow mermaid tail emerges from the waist, remains a long visible C- or S-curve, and ends in one large, obvious, fully visible two-lobed fish fin. All sixteen figures must show the complete tail and complete fin. No pointed tail ends, no missing fins, no hidden fins, no tiny fins, no cropped fins, no tail stumps, no legs, no feet, no split lower body.
Row 1 IDLE: four gentle teacher poses—welcoming smile, thoughtful hand near chin, friendly wave, open-hand invitation.
Row 2 TRAVEL: four chronological swimming poses—anticipation, push, glide, settling.
Row 3 WORK: four chronological teaching poses using the same short coral pointer with rounded pearl tip—ready, point outward, gentle tap toward empty space, encouraging open-hand finish. The pointer must touch her hand and never cover or replace the tail.
Row 4 CHEER: four chronological celebration poses—small clap, delighted smile, one arm raised, both arms raised.
Style/medium: polished true-2D storybook game cutouts matching the references; clean hand-painted cel shading, restrained highlights, navy-purple outlines, aqua/lavender shadows. Never 3D or photorealistic.
Costume: the same Teacher design from Image 3: soft aqua blouse, lavender scalloped cardigan/vest, coral bow, small shell/star teacher badge, tidy coral waist pouch, and three small clean learning-icon badges (uppercase A, numeral 3, triangle). No words or sentences.
Background: perfectly uniform solid light neutral gray presentation field, RGB #F0F0F0, for deterministic border-connected removal. No checkerboard, transparency preview, gradient, glow, shadow, scenery, bubbles, sparkles, labels, captions, borders, grid lines, or watermark.
Identity constraints: preserve Roshan’s exact face, eyes, age, brown hair shape, rainbow streak, torso proportions, and identity colors.
Prop constraints: at most one pointer per work or cheer figure; pointer attached naturally to her hand; no chalkboard, desk, apple, glasses, books, students, other characters, floating props, or detached pieces.
Avoid: redesigning Roshan, adult proportions, tiny figures, cropped anatomy, merged cells, duplicate body parts, duplicate fins, malformed hands, garbled text, detached pointer, extra objects.
```
