# Art review card v1 (draft template)

One card per reviewed image, sheet or in-scene state. It replaces the nine
separate art rubrics with one rule: vetoes first, then six axes, and the
weakest axis decides. A reviewer writes it in words; scores are opinions
with a named evidence level, never acceptance by themselves.

## 1. What was reviewed

```text
review_id:      RV-<family>-<name>-<yyyymmdd>
style_card:     <SC-id, or "existing art">
files:          <path> sha256:<...>   (one line per file)
family:         <F-id>
identity:       <ID-... for each character shown, or "none">
evidence_level: FILE | SHEET | IN_SCENE_CAPTURE | DEVICE | OWNER
capture:        <path of the phone-size runtime capture, required from IN_SCENE_CAPTURE>
reviewer:       <name or agent>
```

## 2. Vetoes (any one rejects the image)

| Code | Veto |
|---|---|
| V-IDENTITY | A character differs from its identity sheet (face, age, hair, outfit, tail, colours, part counts) |
| V-ANATOMY | Missing, extra or fused limbs, fins, ears or fingers; impossible joins |
| V-ALPHA | Fake transparency, painted checkerboard, halo or black matte rim, neighbour-frame bleed, cut-off at the cell edge |
| V-TEXT | Words, numbers or labels painted into world art |
| V-THIRD-PARTY | A third-party character, brand, logo or game asset |
| V-LINE | Contour outside the family band (for example neutral black where the family is plum) without a recorded exception |
| V-SHADOW | Neutral-black shading where the zone's shadow hue applies |
| V-SUBJECT | The subject is replaced or decorated beyond recognition (faces on props, merged concepts) |

## 3. Six axes, scored 0–5 (the weakest axis is the score)

| Axis | Question |
|---|---|
| Silhouette and readability | Does it read as one shape at phone size and at 112 px? |
| Line | Contour colour and width match the family? |
| Colour and value | Palette within the family's measured range; three value bands; high-key? |
| Material and finish | Painted bands and matte-to-satin, not noise or a mesh look? |
| Identity | Matches the identity sheet in every frame? (Write "n/a" when no character is shown) |
| Fit in the scene | Same light, scale, perspective and layer role as its neighbours in the real state? |

Pass for runtime: every axis at least 4.5 at evidence level
`IN_SCENE_CAPTURE` or higher. Only the owner gives 5/5 (`DL-VIS-07`). An
isolated-file review never passes an image for runtime (`DL-VIS-08`).

## 4. Outcome

```text
vetoes:   <codes or "none">
axes:     silhouette <n> | line <n> | colour <n> | material <n> | identity <n> | fit <n>
score:    <weakest axis>   level: <evidence level>
result:   ACCEPTED -> EX-<id> (what it teaches)  |  REJECTED -> AX-<id> (reason codes)  |  REVISE
notes:    <one or two sentences a future card can reuse>
```
