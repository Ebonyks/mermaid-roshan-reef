# Daddy Mermaid moving-tail atlas provenance

Generated 2026-08-01 with the OpenAI built-in image generation tool. These are
project-owned animation derivatives guided by the protected, project-owned
Daddy Mermaid canonical art. They are not third-party assets.

## Protected references

| Role | Path | SHA-256 |
|---|---|---|
| Canonical identity and design authority | `assets_src/daddy_master.png` | `2eda6f76760b85984692dd35bf9ce69b631f6d9db4c8b7b8c013bb92cb632b77` |
| Protected runtime friend cutout | `assets/characters/friends/daddy.webp` | `9031736498f05662716988b6c9a8091dc148edf92ae1e8422fb5e4f2fd17c089` |
| Approved sticker-style reference | `assets/characters/stickers/daddy.png` | `402024ac72c5365aae8562d422b9f888a6f5cdef7b6539409747e8f965cd0122` |

All three references remain byte-for-byte unchanged.

## Accepted native generations

| Clip | Image generation output ID | Preserved source | Native size | SHA-256 |
|---|---|---|---:|---|
| idle | `exec-2bf899e9-6e24-4d13-b493-20ccacc6dcb8.png` | `daddy_idle_chroma.png` | 1774 x 887 | `4134f09cf480198457e97aff99116585fd97acfbb9ba28fd191fc5353908deda` |
| swim | `exec-d0ab4642-725c-49df-b86b-774830f10566.png` | `daddy_swim_chroma.png` | 1254 x 1254 | `13317e84f680c4c544f75be93e66f21ed251ac52eafab961c12f768268e45d6c` |
| gesture_a | `exec-59e4ef7e-d6f5-4862-9940-e004065aac31.png` | `daddy_gesture_a_chroma.png` | 1254 x 1254 | `0df1cc477e2163d953a44d21df598e5f39b6bd90836fb5499c1932d4d238fae3` |
| victory | `exec-e7b72eb2-48b9-477e-b023-fcd77c0836a1.png` | `daddy_victory_chroma.png` | 1774 x 887 | `851849de8f3a22f8acff03ca96b0dfa1f9ba5461ac5ee477b5006a2d41b896c2` |

Each accepted source is a complete generated atlas prompted on a flat green
field. Native generator greens vary slightly between sheets, so border-connected
extraction is measured from each sheet rather than assuming exact `#00ff00`
pixels. Production alpha is derived non-destructively: only the matte connected
to the canvas border is removed, so legitimate enclosed greens in the tail,
cape, and costume survive. The generated source files and their hashes are
preserved here; runtime resizing and sticker treatment happen only in new
derived files under `assets/characters/daddy_25d/`.

The prior sheets under `assets_src/imagegen/daddy_25d_2026-08-01/` were rejected
because their tail/fluke silhouettes were effectively static. A later gray-field
edit also repeated static poses and was rejected. None of those candidates is a
runtime source or ships as production art.

## Exact idle prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character idle animation sprite atlas — REDRAW
Input images: Image 5 is the protected canonical Daddy Mermaid identity and exact character-design authority. Images 1-3 are rejected first-pass animation sheets: use them only as secondary rendering references, not as motion references. Image 4 is a rejected gray-background edit and must be ignored completely. The first-pass sheets were rejected because the tail/fluke silhouette barely moved.
Primary request: Redraw one exact 4-column by 2-row atlas containing eight consecutive chronological frames of a seamless Daddy Mermaid IDLE loop. The exact same Daddy appears once in every equal cell, same upright front-three-quarter view. His torso and tail-root junction stay pinned to the same location while a gentle but unmistakable wave travels down the entire long tail. THE TAIL MUST VISIBLY CHANGE CURVE AND THE LARGE FLUKE MUST MOVE IN EVERY SUCCESSIVE FRAME.
Tail choreography in reading order:
1. relaxed long S-curve, lower tail bows left, fluke slightly left;
2. small bend begins at the hips while the fluke still lags left;
3. bend travels through the upper tail, mid-tail crosses center;
4. bend reaches the lower tail and fluke swings clearly right;
5. reverse bend begins at the hips, mid-tail forms the opposite S;
6. reverse wave travels downward while side fins lag;
7. fluke swings clearly left with a soft follow-through;
8. near-loop-closure pose approaching frame 1, with hair/cape settling.
Secondary acting: tiny inhale/exhale in shoulders, warm closed-eye smile, hands relaxed near/in coat pockets, crown and glasses stable. Hair, teal cape, side fins, and bifurcated fluke lag the tail wave naturally. This is quiet idle motion, not swimming across the canvas.
Subject invariants: preserve Daddy Mermaid exactly—same youthful adult face, closed crescent eyes, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, navy royal coat with identical gold piping/buttons, gold shell epaulettes and pearl chains, teal cape, two arms/two hands, and one continuous glittering rainbow-scaled mermaid tail with the same side fins and large bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and soft children's-storybook cel shading. No redesign.
Scene/backdrop: perfectly flat solid exact #00ff00 chroma-key background.
Composition/framing: exact 4 by 2 equal cells; one complete full-body Daddy per cell; torso, head, and tail-root anchor fixed in the same coordinates; identical apparent height and scale; generous padding for the moving fluke; crown, hands, tail, cape, side fins, and both fluke lobes fully visible; no overlap between cells.
Constraints: background one uniform #00ff00 with no shadow, gradient, texture, checkerboard, floor, water, bubbles, reflection, grid, border, label, text, icon, prop, watermark, sticker rim, or drop shadow. Do not use exact #00ff00 in Daddy. Every frame distinct. The moving tail remains one continuous anatomical tail attached at the same root. Two arms, two hands, one torso, one tail.
Avoid: static/repeated tail silhouette; fluke staying in the same place; moving the whole character instead of deforming the tail; root skating; identity/costume/face/glasses/crown drift; extra/missing/fused limbs; duplicated, detached, broken, shortened, or topology-changing tail; cropped fins; motion blur; camera changes; aggressive acting; 3D rendering; pixel art.
```

## Exact swim prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character SWIM/MOVING animation sprite atlas — full redraw with unmistakable tail propulsion.
Input images: Image 1 is the canonical Daddy Mermaid character reference and the exact identity, costume, anatomy, palette, and rendering authority. Image 2 is the approved green-background idle atlas layout/style and demonstrates the required articulated tail motion. Do not copy any earlier rejected static-tail sheet.

Primary request: Create one exact 4-column by 4-row atlas containing sixteen consecutive chronological frames of a seamless Daddy Mermaid swimming/moving loop, read left-to-right and top-to-bottom. The same Daddy appears once in every equal cell, angled slightly into a gentle forward swim, but his torso and the anatomical tail-root junction remain pinned to identical coordinates in every cell. A strong, smooth traveling body wave must pass from hips through the full long tail into the large bifurcated fluke. The lower-tail curve and fluke position/orientation must be clearly different in every successive frame. This is tail-powered swimming, not translating the whole character around the cell.

Exact tail choreography in reading order:
1 relaxed left C-curve, lower tail and fluke far left;
2 new bend begins at hips while fluke still lags far left;
3 upper-tail bend deepens, mid-tail forms an S;
4 wave reaches mid-tail and fluke begins crossing toward center;
5 lower-tail bend reaches fluke, fluke crosses center;
6 full rightward sweep, lower tail bows right and fluke clearly right;
7 rightward overshoot with fluke lobes flexed and side fins lagging;
8 upper body begins reversal while fluke remains right;
9 reverse bend begins at hips, tail forms opposite S, fluke lags right;
10 reverse wave reaches upper-mid tail;
11 reverse wave reaches lower-mid tail and fluke approaches center;
12 fluke crosses center toward left;
13 full leftward sweep, lower tail bows clearly left;
14 leftward overshoot with fluke lobes flexed and side fins lagging;
15 torso settles as the wave approaches the starting phase;
16 near-loop-closure pose flowing naturally into frame 1, not a duplicate.
Arms perform a small slow breaststroke-like cycle secondary to the tail: forward reach, gentle outward sweep, relaxed recovery; never obscure the coat or face. Hair, teal cape, side fins, and both fluke lobes trail the traveling wave with natural one-frame lag. Every frame must be visibly distinct.

Subject invariants: preserve Daddy Mermaid exactly—same youthful clean-shaven adult face, warm closed-crescent eyes, tiny calm smile, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, dark navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, two arms and two hands, and one continuous long glittering rainbow-scaled mermaid tail with the same side fins and large bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and polished children's-storybook cel shading. No redesign.

Scene/backdrop: perfectly flat solid exact #00ff00 chroma-key background.
Composition/framing: exact 4 by 4 equal cells; one complete full-body Daddy per cell; head, torso, and tail-root fixed at the same coordinates; identical apparent height and scale; generous padding for the entire left-right fluke sweep; crown, hands, cape, tail, side fins, and both fluke lobes fully visible; no overlap between cells.

Constraints: background must be one uniform #00ff00 with no shadow, gradient, texture, checkerboard, floor, water, bubbles, reflection, grid, dividers, border, label, text, icon, prop, watermark, sticker rim, or drop shadow. Do not use exact #00ff00 in Daddy. The moving tail stays one continuous anatomical tail attached at the same root. Two arms, two hands, one torso, one tail.

Avoid: static or repeated tail silhouette; fluke remaining in the same place; whole-character translation; root skating; identical frames; identity/costume/face/glasses/crown drift; beard; legs or feet; extra/missing/fused limbs; duplicated, detached, broken, shortened, or topology-changing tail; cropped fins; motion blur; camera changes; aggressive acting; 3D rendering; pixel art.
```

## Exact gesture_a prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character COMMON INTERACTIONS animation sprite atlas — redraw with visible tail acting.
Input images: Image 1 is the canonical Daddy Mermaid character and exact identity/costume/anatomy authority. Image 2 is the approved idle atlas showing articulated tail motion. Image 3 is the approved 16-frame swim atlas showing the required continuous long tail, large bifurcated fluke, anchored torso, clean outlines, palette, and polished storybook cel rendering. Never use the earlier rejected static-tail interaction sheet.

Primary request: Create one exact 4-column by 4-row atlas. Reading left-to-right within each row, each row is a distinct four-frame common interaction animation:
ROW 1 — friendly wave: frame 1 raises the outer hand, frame 2 hand waves outward, frame 3 waves inward, frame 4 lowers toward the relaxed pose.
ROW 2 — welcoming/inviting gesture: frame 1 opens both hands, frame 2 extends them warmly toward Mermaid Roshan, frame 3 holds the welcoming presentation, frame 4 draws them gently back.
ROW 3 — happy clap: frame 1 hands apart, frame 2 hands meet, frame 3 hands rebound apart, frame 4 hands meet softly again.
ROW 4 — reassuring hug/open-arms gesture: frame 1 arms begin opening, frame 2 arms open wide, frame 3 leans forward slightly with warm open arms, frame 4 begins returning toward neutral. This is a safe parent inviting a hug, not touching another visible character.

MANDATORY TAIL MOTION IN EVERY ROW: the torso and anatomical tail-root junction remain pinned in the same coordinates, but a clear secondary wave travels down the whole long tail through the four frames. In each row, frame 1 lower tail bows left and the large fluke is clearly left; frame 2 the bend reaches mid-tail and the fluke crosses near center; frame 3 lower tail bows clearly right and the fluke swings far right; frame 4 the reverse bend begins and the fluke follows back toward center/left. Side fins and both fluke lobes flex and lag. The tail/fluke silhouette must visibly change in every successive cell. Do not merely move the arms over a repeated static body. Every one of the sixteen cells must be a distinct drawing.

Subject invariants: preserve Daddy Mermaid exactly—same youthful clean-shaven adult face, warm closed-crescent eyes, tiny calm smile, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, dark navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, two arms and two hands, and one continuous long glittering rainbow-scaled mermaid tail with the same side fins and large bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and polished children's-storybook cel shading. No redesign. Crown and glasses remain stable; hair and cape have small natural overlap/follow-through.

Scene/backdrop: perfectly flat solid exact #00ff00 chroma-key background.
Composition/framing: exact 4 by 4 equal cells; one complete full-body Daddy per cell; head, torso, and tail-root fixed to consistent coordinates; identical apparent height and scale; generous horizontal and vertical padding for arms and moving fluke; crown, fingers, cape, tail, side fins, and both fluke lobes fully visible; no overlap between cells.

Constraints: one uniform #00ff00 background only—no shadow, gradient, texture, checkerboard, floor, water, bubbles, reflection, grid, dividers, border, label, text, icon, prop, second character, watermark, sticker rim, or drop shadow. Do not use exact #00ff00 in Daddy. Every frame is distinct. One continuous anatomical tail attached at the same root. Exactly two arms, two hands, one torso, one tail.

Avoid: static/repeated tail silhouette; fluke staying in one place; whole-character translation or root skating; repeating a pose; mixing row actions; identity/costume/face/glasses/crown drift; beard; legs or feet; extra/missing/fused fingers or limbs; duplicated, detached, broken, shortened, or topology-changing tail; cropped hands/fins/fluke; motion blur; camera changes; aggressive acting; combat weapons; text; 3D rendering; pixel art.
```

## Exact victory prompt

```text
Use case: stylized-concept
Asset type: 2.5D mobile game character COMBAT-SUCCESS VICTORY animation sprite atlas — full redraw with a strong celebratory tail flourish.
Input images: Image 1 is the canonical Daddy Mermaid identity/costume/anatomy authority. Image 2 is the approved moving-tail idle atlas. Image 3 is the approved 16-frame swim atlas and primary full-tail motion authority. Image 4 is the approved common-interactions atlas and gesture/rendering authority. Ignore every earlier rejected static-tail victory sheet.

Primary request: Create one exact 4-column by 2-row atlas containing eight consecutive chronological frames of Daddy Mermaid celebrating when Mermaid Roshan succeeds in combat, read left-to-right and top-to-bottom. This is a warm proud-parent victory cheer that can play once in about one second. Daddy remains in a fixed full-body stage position: head, torso, and anatomical tail-root junction stay pinned to the same coordinates while his arms cheer and a conspicuous coil-and-release wave travels through the entire long tail into the large bifurcated fluke. Every frame must have a visibly different tail/fluke silhouette.

Exact eight-frame acting and tail choreography:
1 anticipation: hands near chest, delighted closed-eye smile; lower tail bows left and fluke far left;
2 hands begin lifting; new bend starts at hips while fluke lags left;
3 arms open upward; wave reaches mid-tail, making a clear S-curve, fluke crosses toward center;
4 peak cheer: both arms high and open; lower tail sweeps right, fluke far right and lobes flare;
5 proud clap begins overhead/chest-high; reverse bend starts at hips while fluke still lags right;
6 hands meet in one joyful clap; reverse wave travels down mid-tail, fluke crosses center;
7 hands open in a “you did it!” presentation; lower tail sweeps clearly left and fluke far left with fin follow-through;
8 warm proud finish: one hand over heart and one hand presenting toward offscreen Mermaid Roshan; tail settles toward a balanced S-curve that can transition to idle, still distinct from frame 7.
Hair, teal cape, side fins, and both fluke lobes follow through naturally. Celebration is energetic but gentle and safe, never aggressive.

Subject invariants: preserve Daddy Mermaid exactly—same youthful clean-shaven adult face, warm closed-crescent eyes, tiny calm smile becoming a proud joyful grin, black rectangular glasses, pointed ears, long brown-and-sea-green hair, jeweled gold crown, dark navy high-collar royal coat with identical gold filigree/piping/buttons, gold shell clasps/epaulettes and pearl chains, teal cape, two arms and two hands, and one continuous long glittering rainbow-scaled mermaid tail with the same side fins and large bifurcated rainbow fluke. Exact proportions, costume, palette, clean dark-plum outlines, and polished children's-storybook cel shading. No redesign. Keep crown and glasses stable.

Scene/backdrop: perfectly flat solid exact #00ff00 chroma-key background.
Composition/framing: exact 4 by 2 equal cells; one complete full-body Daddy per cell; head, torso, and tail-root at consistent fixed coordinates; identical apparent height and scale; generous padding for raised hands and the full left-right fluke sweep; crown, fingers, cape, tail, side fins, and both fluke lobes fully visible; no overlap between cells.

Constraints: one uniform #00ff00 background only—no shadow, gradient, texture, checkerboard, floor, water, bubbles, reflection, grid, dividers, border, label, text, icon, prop, weapon, second character, watermark, sticker rim, or drop shadow. Do not use exact #00ff00 in Daddy. Every frame is distinct. One continuous anatomical tail attached at the same root. Exactly two arms, two hands, one torso, one tail.

Avoid: static or repeated tail silhouette; fluke remaining in one place; moving the whole character instead of deforming the tail; root skating; duplicated frames; identity/costume/face/glasses/crown drift; beard; legs or feet; extra/missing/fused limbs; duplicated, detached, broken, shortened, or topology-changing tail; cropped hands/fins/fluke; motion blur; camera changes; aggressive or taunting behavior; weapons; readable text; 3D rendering; pixel art.
```
