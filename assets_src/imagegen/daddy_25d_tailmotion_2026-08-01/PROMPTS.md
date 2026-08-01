# Daddy Mermaid 2.5D animation source provenance

Generated 2026-08-01 with OpenAI's built-in image-generation tool through the
Codex `imagegen` skill. The generated originals remain at their tool output
paths; the four `*_chroma.png` files in this directory are byte-identical
project copies. Runtime atlases are non-destructive chroma-keyed, normalized
derivatives built by `tools/build_daddy_25d_atlases.py`.

Each source also retains `*_helper_keyed.png` and
`*_helper_despilled.png`, produced with the bundled imagegen
`remove_chroma_key.py` helper using border auto-keying and a soft matte. These
eight files are validation/despill intermediates, not accepted native sources,
authoritative topology masks, or runtime assets. The builder ignores helper
alpha because a broad color-distance matte can erase authored green pixels in
the rainbow tail; only helper RGB at the custom matte's thin outer edge is
eligible for despill.

## Protected references

These files are identity/style references only and were not modified:

| Reference | SHA-256 |
|---|---|
| `assets_src/daddy_master.png` | `2eda6f76760b85984692dd35bf9ce69b631f6d9db4c8b7b8c013bb92cb632b77` |
| `assets/characters/friends/daddy.webp` | `9031736498f05662716988b6c9a8091dc148edf92ae1e8422fb5e4f2fd17c089` |
| `assets/characters/stickers/daddy.png` | `402024ac72c5365aae8562d422b9f888a6f5cdef7b6539409747e8f965cd0122` |

## Accepted generated sources

| Clip | Project copy | Retained helper intermediates | Tool output ID | Native size | SHA-256 |
|---|---|---|---|---|---|
| Idle | `daddy_idle_chroma.png` | `daddy_idle_helper_{keyed,despilled}.png` | `exec-c17a0e3b-fc6a-4b9b-ad5f-4d759d3b2a12` | 1681x936 | `cee3b12bd0b8db3b29d79569f313f4e2a1d3fabad18b071dd0fc4e3546dfc73d` |
| Swim/move | `daddy_swim_chroma.png` | `daddy_swim_helper_{keyed,despilled}.png` | `exec-f6235ccc-09dc-4f77-b2cf-0a59ef68e12d` | 1254x1254 | `2c3a41ffb600d84e5de03db251a432f5054e7779c98fa27607b647e88b29a798` |
| Common interactions | `daddy_gesture_a_chroma.png` | `daddy_gesture_a_helper_{keyed,despilled}.png` | `exec-25c2506c-1ab4-406d-811f-981a570a0950` | 1254x1254 | `e768a6ca596721d3734d4e9743845a18d6471b7ce733b2900c501e5e5ea6dee9` |
| Combat victory | `daddy_victory_chroma.png` | `daddy_victory_helper_{keyed,despilled}.png` | `exec-ad52709b-2228-40e3-b830-119112b90c7e` | 1606x979 | `803add39f92af2220222a513966de66ea6bfa661fe079efcfd35dda8833d59b3` |

The acceptance gate runs on colored subject pixels before the white rim or
shadow is added. The authoritative matte removes only outer-border-connected
pixels within a Chebyshev distance of 32 from each sheet's border-mode key,
then extracts complete subjects globally rather than cropping nominal cells.
It finds exactly 8, 16, 16, and 8 large connected Daddy components in the four
sources respectively: one complete anatomical subject per frame, including
both fused fluke lobes. Helper alpha is not part of this gate. A rim or shadow
may never bridge a disconnected tail.

## Rejected generations

- First pass: `exec-1da981b3-1917-4e91-b93d-729ca40a2d7f`,
  `exec-ab21e0d0-62e7-4d5e-94bf-f1aa8283749e`, and
  `exec-2b5a8911-c2bd-44b6-afb8-54c21862532f`. Rejected because the tail
  silhouette barely changed; it read as a translated static cutout.
- Second pass: `exec-2bf899e9-6e24-4d13-b493-20ccacc6dcb8`,
  `exec-d0ab4642-725c-49df-b86b-774830f10566`,
  `exec-59e4ef7e-d6f5-4862-9940-e004065aac31`, and
  `exec-e7b72eb2-48b9-477e-b023-fcd77c0836a1`. It had strong tail timing,
  but was rejected because colored fluke lobes floated apart from the tail in
  39 of 48 frames. A later sticker rim falsely hid those anatomical gaps.
- `exec-d54d84f7-a5c4-4deb-937d-412f5806a64f` was an exploratory gray
  edit and was never accepted.

No rejected generation is a runtime asset or build input.

## Accepted idle prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character IDLE animation sprite atlas — topology repair redraw.
Input images: Image 1 is the protected canonical Daddy Mermaid and is absolute identity, costume, anatomy, palette, and topology authority. Image 2 is the rejected moving-tail idle atlas: preserve its successful eight-frame tail-wave timing and general acting, but redraw every frame because its fluke lobes float apart from the tail. Do not copy those gaps.

Primary request: Draw one exact 4-column by 2-row atlas of eight consecutive chronological frames of a seamless gentle idle loop. The same Daddy Mermaid appears once in every equal cell. His torso and anatomical tail-root stay anchored while a visible S-wave travels from hips through the entire long tail and into the fluke: frame 1 lower tail left; frame 2 bend starts at hips; frame 3 bend reaches mid-tail; frame 4 fluke swings clearly right; frame 5 reverse bend starts; frame 6 reverse wave travels downward; frame 7 fluke swings clearly left; frame 8 settles toward frame 1. Hair, cape, side fins, and fluke lag naturally. Every tail silhouette is distinct.

NONNEGOTIABLE CONTINUOUS TAIL TOPOLOGY IN EVERY CELL: Daddy has exactly one continuous filled rainbow tail silhouette. The tail tip widens into one single fused V-shaped bifurcated fluke. Both fluke lobes grow from the same thick solid rainbow base that is visibly fused to the tail tip. There must be NO green gap, slit, floating blade, detached lobe, or transparent separation anywhere between the tail and either fluke lobe. The two lobes may split only after a broad shared base. If all non-green subject pixels in one cell were flood-filled, the entire Daddy—including both fluke lobes—would be exactly one connected component before any outline or shadow. Make the colored anatomical connection thick and unmistakable; never rely on an outline, sticker rim, shadow, or nearby overlap to fake connection.

Subject invariants: preserve Daddy Mermaid exactly—youthful clean-shaven adult face, warm closed-crescent eyes, tiny calm smile, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, dark navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, two arms/two hands, and one long glittering rainbow-scaled mermaid tail with side fins and one large fused bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and polished children's-storybook cel shading. No redesign.

Scene/backdrop: perfectly flat solid bright chroma green background near #00ff00.
Composition/framing: exact 4 by 2 equal invisible cells; one complete full-body Daddy in each; identical scale; head/torso/tail-root aligned; subject uses no more than 72% of each cell width and 82% of its height; at least 10% uninterrupted green clearance around every hand, crown, cape, tail, and fluke; nothing crosses or touches a neighboring cell; generous room for the fluke sweep.

Constraints: no grid lines, dividers, borders, labels, text, icons, props, second character, watermark, sticker rim, drop shadow, floor, water, bubbles, reflection, or background texture. One complete anatomical subject per cell. Two arms, two hands, one torso, one tail, one fused two-lobed fluke. Every frame distinct.

Avoid: detached or floating fluke lobes; green/transparent gaps at the fluke base; multiple separate tail pieces; static/repeated tail; moving the whole character instead of deforming the tail; root skating; cell overlap; cropped anatomy; identity/costume drift; beard; legs/feet; extra/missing/fused limbs; motion blur; aggressive acting; 3D rendering; pixel art.
```

## Accepted swim/move prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character SWIM/MOVING animation sprite atlas — topology repair redraw.
Input images: Image 1 is the newly accepted topology-repaired idle atlas; copy its thick, fully fused two-lobed fluke construction, identity, rendering, scale, and generous cell padding. Image 2 is the protected canonical Daddy Mermaid and is absolute identity/costume/anatomy authority. Image 3 is the rejected 16-frame swim atlas: preserve its successful traveling-wave timing and varied propulsion silhouettes, but redraw every frame because its fluke pieces were anatomically disconnected.

Primary request: Draw one exact 4-column by 4-row atlas containing sixteen consecutive chronological frames of a seamless Daddy Mermaid swimming/moving loop, read left-to-right and top-to-bottom. His torso and anatomical tail root stay aligned while a powerful smooth wave passes hips → upper tail → mid-tail → lower tail → fluke, then reverses. Tail choreography: frames 1-4 left C-curve into S-wave; frames 5-8 fluke crosses center into a full right sweep and overshoot; frames 9-12 reverse bend begins at hips while fluke lags right then crosses center; frames 13-16 full left sweep, overshoot, and near-loop closure. Lower-tail curve and fluke orientation visibly change in every successive frame. Arms perform a gentle secondary breaststroke; hair, cape, side fins, and fluke follow through. Do not translate the whole cutout.

NONNEGOTIABLE CONTINUOUS TAIL TOPOLOGY IN ALL SIXTEEN CELLS: Daddy has exactly one continuous filled rainbow tail silhouette. The tail tip widens into one single fused V-shaped bifurcated fluke. Both fluke lobes grow from the same thick solid rainbow base visibly fused to the tail tip. There must be NO green gap, slit, floating blade, detached lobe, transparent separation, or separate colored island anywhere between tail and either lobe. The lobes may fork only after a broad shared base. A flood-fill of all non-green subject pixels in each cell must yield exactly one connected Daddy component before outlines or shadows. Make the colored connection thick enough to remain connected after chroma-key removal. Never rely on an outline, sticker rim, shadow, proximity, or overlap to fake connection.

Subject invariants: preserve Daddy exactly—youthful clean-shaven adult face, closed-crescent eyes, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, two arms/two hands, one long glittering rainbow-scaled mermaid tail with side fins and one fused large two-lobed rainbow fluke. Polished children's-storybook cel shading, clean dark-plum outlines. No redesign.

Scene/backdrop: perfectly flat solid bright chroma green near #00ff00.
Composition/framing: exact 4 by 4 equal invisible cells; one complete full-body Daddy per cell; identical scale; head/torso/tail-root aligned; subject uses no more than 72% of each cell width and 82% height; at least 10% uninterrupted green clearance around crown, hands, cape, tail, side fins, and entire fluke; nothing crosses or touches a neighboring cell; no row overlap.

Constraints: no grid/dividers/borders, labels, text, props, second character, watermark, sticker rim, drop shadow, floor, water, bubbles, or texture in background. One complete anatomical subject per cell; exactly two arms, two hands, one torso, one tail, one fused two-lobed fluke. Every frame distinct.

Avoid: detached/floating fluke lobes; green gaps at fluke base; multiple tail pieces; repeated/static tail; root skating; cross-cell bleed; clipped anatomy; identity/costume drift; beard; legs/feet; extra/missing/fused limbs; motion blur; aggressive acting; 3D rendering; pixel art.
```

## Accepted common-interactions prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character COMMON INTERACTIONS animation sprite atlas — topology repair redraw.

Input images, in order: Image 1 is the accepted topology-repaired swim atlas; copy its thick, fully fused two-lobed fluke construction, character identity, storybook rendering, scale discipline, and generous green cell clearance. Image 2 is the protected canonical Daddy Mermaid and is absolute identity, costume, anatomy, palette, and topology authority. Image 3 is the rejected interaction atlas; preserve only its friendly acting ideas and 4-row organization, but redraw every frame because its fluke lobes were anatomically disconnected.

Primary request: Draw one exact 4-column by 4-row atlas. Each row is a separate four-frame common interaction animation read left-to-right:
ROW 1 — friendly wave: frame 1 hand lifts and lower tail bends left; frame 2 open hand waves outward while a tail wave reaches mid-tail; frame 3 hand waves back while the fluke swings clearly right; frame 4 hand lowers as the reverse tail bend begins.
ROW 2 — welcoming invitation / “come here”: frame 1 both hands open near chest with tail curving right; frame 2 arms extend warmly while wave travels down-tail; frame 3 one palm beckons inward while fluke sweeps left; frame 4 arms settle open while fluke rebounds toward center.
ROW 3 — happy clap: frame 1 hands apart with tail bending left; frame 2 hands meet in a gentle clap while wave reaches mid-tail; frame 3 hands rebound apart while fluke swings strongly right; frame 4 hands approach again while reverse wave begins. No duplicated frames.
ROW 4 — reassuring hug / embrace: frame 1 arms open wide and tail curves right; frame 2 arms begin wrapping inward while wave travels downward; frame 3 warm self-hug pose while fluke swings clearly left; frame 4 arms reopen slightly while fluke rebounds.
Every row is one friendly, readable four-frame one-shot. In all sixteen cells the torso and anatomical tail root stay consistently aligned, while lower-tail curvature, side fins, and fluke orientation visibly change frame to frame. Hair and cape follow through. Do not translate the whole character.

NONNEGOTIABLE CONTINUOUS TAIL TOPOLOGY IN ALL SIXTEEN CELLS: Daddy has exactly one continuous filled rainbow tail silhouette. The tail tip widens into one single fused V-shaped bifurcated fluke. Both fluke lobes grow from the same thick solid rainbow base visibly fused to the tail tip. There must be NO green gap, slit, floating blade, detached lobe, transparent separation, or separate colored island anywhere between tail and either lobe. The two lobes may fork only after a broad shared base. If all non-green subject pixels in one cell were flood-filled, the entire Daddy—including both fluke lobes—would be exactly one connected component before outline, rim, or shadow. Make the colored anatomical connection thick and unmistakable enough to survive chroma-key removal. Never rely on an outline, white sticker rim, shadow, proximity, or overlap to fake connection.

Subject invariants: preserve Daddy Mermaid exactly—youthful clean-shaven adult face, warm closed-crescent eyes, tiny kind smile, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, dark navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, exactly two arms and two hands, and exactly one long glittering rainbow-scaled mermaid tail with side fins and one large fused bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and polished children's-storybook cel shading. No redesign.

Scene/backdrop: perfectly flat solid bright chroma green near #00ff00.
Composition/framing: exact 4 by 4 equal invisible cells; one complete full-body Daddy per cell; identical scale; head, torso, and tail-root aligned; subject uses no more than 72% of each cell width and 82% of its height; at least 10% uninterrupted green clearance around every hand, crown, cape, tail, side fin, and the entire fluke; nothing crosses or touches a neighboring cell or row; generous room for arm gestures and fluke sweeps.

Constraints: no grid lines, dividers, borders, labels, text, icons, props, second character, watermark, sticker rim, drop shadow, floor, water, bubbles, reflection, or background texture. One complete anatomical subject per cell. Two arms, two hands, one torso, one tail, one fused two-lobed fluke. Every frame distinct.

Avoid: detached or floating fluke lobes; green or transparent gaps at the fluke base; multiple separate tail pieces; static or repeated tail; moving the whole character instead of deforming the tail; root skating; cross-cell bleed; cropped anatomy; identity or costume drift; beard; legs or feet; extra, missing, or fused limbs; motion blur; aggressive acting; 3D rendering; pixel art.
```

## Accepted combat-victory prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character COMBAT VICTORY animation sprite atlas — topology repair redraw.

Input images, in order: Image 1 is the newly accepted topology-repaired interaction atlas; copy its thick fully fused two-lobed fluke construction, exact Daddy identity, storybook rendering, scale discipline, and generous green clearance. Image 2 is the protected canonical Daddy Mermaid and is absolute identity, costume, anatomy, palette, and topology authority. Image 3 is the rejected eight-frame victory atlas; preserve its joyful arms-up celebration concept and eight-frame chronology, but redraw every frame because its fluke lobes were anatomically disconnected.

Primary request: Draw one exact 4-column by 2-row atlas of eight consecutive chronological frames, read left-to-right across the top row and then left-to-right across the bottom row. This is Daddy's warm, exuberant victory when Mermaid Roshan succeeds in combat:
frame 1 — delighted anticipation, hands near chest, lower tail coiled clearly left;
frame 2 — arms start opening, bend begins at hips and travels down-tail;
frame 3 — arms rise, wave reaches mid-tail, fluke crosses center;
frame 4 — joyful full arms-up pose, tail releases into a strong right sweep and fluke fans wide;
frame 5 — celebratory peak with palms open, hair and cape lifted, fluke overshoots right;
frame 6 — arms begin settling outward, reverse bend starts at hips while the fluke lags right;
frame 7 — one warm proud wave toward Roshan, reverse wave reaches lower tail and fluke sweeps clearly left;
frame 8 — open welcoming finish, fluke rebounds near center for a readable final hold.
The torso and anatomical tail root remain aligned across all eight frames, but the full tail visibly coils, uncoils, sweeps, and rebounds. Hair, cape, side fins, and fluke follow through. Every silhouette is distinct. Do not translate the whole cutout. The mood is safe, proud, loving, and celebratory—not aggressive.

NONNEGOTIABLE CONTINUOUS TAIL TOPOLOGY IN ALL EIGHT CELLS: Daddy has exactly one continuous filled rainbow tail silhouette. The tail tip widens into one single fused V-shaped bifurcated fluke. Both fluke lobes grow from the same thick solid rainbow base visibly fused to the tail tip. There must be NO green gap, slit, floating blade, detached lobe, transparent separation, or separate colored island anywhere between tail and either lobe. The two lobes may fork only after a broad shared base. If all non-green subject pixels in one cell were flood-filled, the entire Daddy—including both fluke lobes—would be exactly one connected component before outline, rim, or shadow. Make the colored anatomical connection thick and unmistakable enough to survive chroma-key removal. Never rely on an outline, white sticker rim, shadow, proximity, or overlap to fake connection.

Subject invariants: preserve Daddy Mermaid exactly—youthful clean-shaven adult face, warm closed-crescent eyes, tiny kind smile, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, dark navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, exactly two arms and two hands, and exactly one long glittering rainbow-scaled mermaid tail with side fins and one large fused bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and polished children's-storybook cel shading. No redesign.

Scene/backdrop: perfectly flat solid bright chroma green near #00ff00.
Composition/framing: exact 4 by 2 equal invisible cells; one complete full-body Daddy per cell; identical scale; head, torso, and tail-root aligned; subject uses no more than 72% of each cell width and 82% of its height; at least 10% uninterrupted green clearance around every hand, crown, cape, tail, side fin, and the entire fluke; nothing crosses or touches a neighboring cell or row; generous room for raised arms and sweeping fluke.

Constraints: no grid lines, dividers, borders, labels, text, icons, props, weapons, second character, watermark, sticker rim, drop shadow, floor, water, bubbles, reflection, effects burst, or background texture. One complete anatomical subject per cell. Two arms, two hands, one torso, one tail, one fused two-lobed fluke. Every frame distinct.

Avoid: detached or floating fluke lobes; green or transparent gaps at the fluke base; multiple separate tail pieces; static or repeated tail; moving the whole character instead of deforming the tail; root skating; cross-cell bleed; cropped anatomy; identity or costume drift; beard; legs or feet; extra, missing, or fused limbs; motion blur; aggressive or threatening acting; 3D rendering; pixel art.
```
