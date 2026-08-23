# Opening cinematic V2 — fresh-generation script

This is a manual Grok Imagine script. Do **not** paste the entire document as one generation request. Create the four still anchors first, then generate each numbered shot as its own fresh 6-second video request and trim externally to the authored duration.

## Why this version will behave better

- One camera setup and one causal beat per generation.
- No model-authored montage or cutaways.
- No whole PNW pack attached to an opening shot.
- Touchdown occurs inside the cabin; the airplane never parks on the playground.
- The six-step exterior route is approved as a still before characters use it.
- The castle does not appear until V2-S14.
- Rejected trial frames are not used as visual references.

## Canonical reference paths

- Roshan front: `../../../characters/roshan/ROSHAN_FRONT_IDENTITY.png`
- Roshan rear studies: `../../../characters/roshan/ROSHAN_REAR_POSE_SHEET.png`
- Daddy front: `../../../characters/daddy_mermaid/DADDY_FRONT_IDENTITY.png`
- Exact airplane: `../references/06_AIRPLANE_EXACT.png`
- Final geography: `../../../locations/sky_lagoon/01_SKY_LAGOON_FINAL_GEOGRAPHY.jpg`
- Exact castle: `../../../locations/sky_lagoon/02_CASTLE_EXACT_FOUR_TOWER.png`
- Broad panorama: `../../../locations/sky_lagoon/07_SKY_LAGOON_FULL_PANORAMA.png`

Do not attach the PNW flora/fauna pack to these shots. It is not needed to preserve the already-approved final geography and caused unrelated-animal leakage in the trial.

## Paste once in a new sequence chat

```text
OPENING V2 REBUILD. We are starting from canonical assets, not continuing or repairing the rejected 46.5-second trial. The trial failed because it invented early castle cutaways, forest/lake filler, an otter climbing a tiny airplane, a return to the cabin after exterior arrival, and a glowing portal instead of the six-step route. Never reproduce those events.

For every request below, generate one continuous uncut camera setup only. No montage, internal edit, time jump, flash-forward, cutaway, transition to another location, or surprise subject. Do not infer additional story beats. If the requested action cannot be completed reliably, hold the approved starting composition rather than inventing a cut.

Until shot V2-S14: no castle, kingdom, playground, lawn, forest path, lake path, cabin, animal, train, butterfly, extra passenger, or unrelated PNW asset unless that shot explicitly requests it. No otter, raccoon, hare, squirrel, frog, bird, pet, or wildlife anywhere in the opening.

Maintain exactly one child Mermaid Roshan and one adult Daddy Mermaid. Roshan remains screen-left and Daddy screen-right. Preserve their canonical faces, ages, crowns, clothes, separate mer-tails, and relative scale. No legs, feet, shoes, extra limbs, fused tails, body swaps, costume swaps, or age drift. Audio off. 16:9. Maximum six-second generated take per numbered shot.
```

## Prerequisite still anchors

Do not proceed to video until all four stills pass human review.

### A — CABIN_ANCHOR_V2

Attach Roshan front, Daddy front, then exact airplane.

```text
Create one 16:9 cabin continuity still, not a video. Exactly two merpeople and exactly two individual passenger seats. Young Mermaid Roshan sits screen-left; adult Daddy Mermaid sits screen-right. Both seat belts are visibly closed and owned by the correct seat. Preserve exact canonical faces, hair, crowns, clothes, body scale and separate tails. The cabin uses the exact mint/aqua/lavender airplane palette; three evenly spaced side windows are visible behind them; the aisle/door direction is screen-right. Keep empty space between their inner hands. Polished 1990s shōjo television-cel construction with navy/violet contours and deliberate two/three-tone shading. No extra seat, bench, passenger, animal, exterior scenery, castle, text, photorealism or 3D.
```

Reject if the cabin cannot plausibly fit inside the exterior aircraft, either belt is missing, or character identity drifts.

### B — ROUTE_ANCHOR_V2

Attach exact airplane only. The broad panorama may be attached last for sky palette, never geography.

```text
Create one locked 16:9 exterior layout still, no characters. The exact mint/aqua/lavender three-window airplane is suspended in open turquoise sky in the upper-left, nose and open door facing screen-right. From the open door/cassette platform, exactly six large pearl steps descend diagonally toward the lower-right. Exactly two continuous lavender handrails flank all six steps. The sixth step reaches a visibly separate floating landing platform. Show the entire countable route with generous clear space around it. There is no ground under the airplane and it is not parked. Background is only bright sky, soft cloud sea and distant atmospheric blue. No grass, playground, castle, kingdom, forest, lake path, mountain cabin, animal, character, extra step, missing step, extra rail, ramp, glowing portal, text or UI.
```

Reject unless all six steps, both rails, plane door, and separate platform are simultaneously visible.

### C — DADDY_REAR_V2

Attach Daddy front only.

```text
Create one full-body rear-view character authority of the exact same Daddy Mermaid on a plain light-neutral background. Preserve crown silhouette, long hair, teal cape, royal-blue coat silhouette and gold trim, adult scale, rainbow tail color order and broad fin. Neutral floating pose, hands relaxed and visible from behind. One character only. No new costume, face turn, legs, shoes, prop, environment, text, photorealism or 3D.
```

### D — FINAL_REVEAL_ANCHOR_V2

Attach final geography first, exact castle second, Roshan rear third, and accepted Daddy rear fourth.

```text
Create one locked 16:9 final rear-view hero still. Image 1 owns exact geography: playground left, pearl path entering from bottom-center, castle right, bridge aligned to path and closed door, water right, mountains and small cabins behind. Image 2 owns exact four-tower castle design. Images 3 and 4 own the two rear character silhouettes. Place Roshan lower center-left and Daddy lower center-right, together occupying no more than the lower central quarter. They hold Roshan's left hand to Daddy's right. Roshan's free right hand is raised in one small wonder gesture. Daddy looks down toward Roshan, not away from her. Keep the path, complete bridge and coral door unobscured. Exactly two tiny butterflies and one tiny distant train puff. No airplane, animal, extra character, front-facing pose, open door, extra tower, mirrored geography, tropical palm, fog, text, photorealism or 3D.
```

## Editorial schedule

| Shot | Final duration | Generate | Beat |
|---|---:|---:|---|
| V2-S01 | 2.0s | 6s | Plane crosses empty sky |
| V2-S02 | 3.0s | 6s | Cabin jolt; Daddy steadies open palm |
| V2-S03 | 2.0s | 6s | Roshan uncertainty close-up |
| V2-S04 | 2.0s | 6s | Daddy notices and offers hand |
| V2-S05 | 4.0s | 6s | Roshan chooses hand; gentle hug |
| V2-S06 | 2.5s | 6s | Touchdown felt inside cabin |
| V2-S07 | 2.25s | 6s | Daddy demonstrates his belt release |
| V2-S08 | 2.25s | 6s | Roshan copies her belt release |
| V2-S09 | 4.0s | 6s | Daddy offers hand; both rise and approach door |
| V2-S10 | 2.5s | 6s | Door opens to sky only |
| V2-S11 | 2.5s | 6s | Empty countable six-step route wide |
| V2-S12 | 4.0s | 6s | Daddy tests and leads descent |
| V2-S13 | 3.5s | 6s | Platform reaction; kingdom remains offscreen |
| V2-S14 | 4.0s | 6s | Exact rear Sky Lagoon reveal |
| V2-S15 | 2.0s | same accepted S14 take if possible | Quiet final hold |

Total authored duration: **42.5 seconds**.

## Fresh video prompts

### V2-S01 — empty-sky flight

Attach exact airplane. Add the panorama last only for sky/cloud palette.

```text
One continuous locked wide shot for six seconds. Empty turquoise sky and soft painted cloud sea. The exact mint/aqua/lavender three-window airplane enters from screen-left, travels smoothly toward screen-right at constant scale, and remains in clean profile. Use only gentle cloud drift and restrained hand-drawn cel motion. No island, mountain, ground, castle, playground, animal, character outside, camera chase, cut, text or design change. Audio off.
```

### V2-S02 — safe cabin jolt

Start from `CABIN_ANCHOR_V2`; attach Roshan and Daddy identities.

```text
Animate this exact cabin composition as one uncut medium two-shot. Both belts remain closed. A single mild downward settle occurs; Roshan's eyes widen and fingers tense near her own lap. Daddy stays seated screen-right and steadies only his open right palm in the inner space without touching Roshan. Tails and hair respond with one restrained delayed settle. End with Daddy calm and Roshan looking toward him. No belt opening, handhold, hug, standing, exterior cutaway, castle, animal, extra seat or camera move.
```

### V2-S03 — Roshan notices

Use an accepted S02 frame plus Roshan identity.

```text
One continuous Roshan close-up from the same cabin side. Roshan remains a young child. Her fingers tighten once, she takes one small breath, then raises her eyes toward Daddy offscreen-right. Keep her canonical tiara, face, hair streak, pink clothing and tail colors unchanged. Background cabin stays soft and stable. No Daddy body entering frame, no cutaway, dialogue, belt release, castle, animal, morphing or camera move.
```

### V2-S04 — Daddy offers

Use an accepted S02 frame plus Daddy identity.

```text
One continuous Daddy close-up from the matching cabin angle. Daddy notices Roshan offscreen-left, softens his eyes, turns only slightly, and slowly offers his open right palm toward screen-left. His own belt remains closed. Preserve crown, glasses, long hair, blue coat, gold trim, teal cape and adult scale. End on the patient open hand. No grab, hug, standing, belt opening, exterior cut, castle, animal or camera move.
```

### V2-S05 — chosen hand and reassurance

Start from a newly approved cabin two-shot based on the S04 end; attach both identities.

```text
One continuous medium two-shot. Roshan screen-left looks at Daddy's waiting right hand, reaches with her left hand, and completes exactly one inner handhold. Daddy waits until contact, then draws Roshan into one gentle side hug without releasing the hand. Roshan exhales and relaxes. Both belts remain closed throughout. Preserve two separate bodies and tails; no fused arms. End in a stable reassuring pose. No cutaway, castle, animal, standing, belt opening, extra passenger, dialogue animation or camera move.
```

### V2-S06 — touchdown inside only

Start from accepted S05 end; use the cabin anchor. Do not attach any exterior landscape.

```text
One continuous cabin two-shot. The airplane's arrival is felt only as one tiny vertical settle followed by stillness. A soft aqua light rolls once across the three windows and across Roshan and Daddy's faces. They remain seated and safe; both belts stay closed; their chosen handhold remains intact. Daddy whispers visually with one small reassuring expression, but generate no audio. No exterior view, castle reflection, island, lawn, animal, belt release, standing, cut or camera move.
```

### V2-S07 — Daddy demonstrates

Start from accepted S06 end; attach Daddy identity and cabin anchor.

```text
One continuous medium two-shot favoring Daddy. Roshan watches from screen-left. Daddy releases only his own seat belt slowly and clearly: hand moves to his own buckle, buckle opens once, the two belt halves rest beside Daddy's screen-right cushion. Roshan's belt stays visibly closed. No other action. Preserve correct hands, seats and body scale. No cutaway, animal, castle, standing or camera move.
```

### V2-S08 — Roshan copies

Start from accepted S07 end; attach Roshan identity and cabin anchor.

```text
One continuous matching two-shot favoring Roshan. Daddy's belt halves remain resting beside his cushion. Roshan copies the demonstrated action on her own seat: her hand reaches her own buckle, it opens once, and her belt halves rest beside her screen-left cushion. Daddy watches patiently without touching the buckle. No other action, cutaway, animal, castle, standing or camera move.
```

### V2-S09 — rise and approach

Start from accepted S08 end; attach both identities and cabin anchor.

```text
One continuous side/rear cabin shot. Daddy rises first on screen-right, offers his right hand and waits. Roshan takes it with her left, then rises. Together they glide slowly toward the screen-right door while exactly two empty seats recede behind them. Maintain the inner handhold, separate tails, correct child/adult scale and stable cabin geometry. End stopped beside the closed door. No door opening yet, exterior cut, castle, animal, extra seat, teleport or camera reversal.
```

### V2-S10 — sky threshold

Start from accepted S09 end; attach exact airplane and both identities.

```text
One continuous rear/side doorway shot. Roshan left and Daddy right remain inside, holding inner hands. The screen-right door seam releases and the door opens outward once. A safe breeze lifts one Roshan hair streak and only Daddy's cape edge. Outside is bright open turquoise sky and cloud glow only. Do not show ground, grass, playground, castle, mountain, forest, lake, animal, glowing portal, or the full route yet. They pause at the threshold and do not jump or teleport.
```

### V2-S11 — countable route

Animate only the approved `ROUTE_ANCHOR_V2`.

```text
One continuous locked exterior wide. Preserve the exact approved layout: airplane suspended upper-left; open door/cassette platform; exactly six pearl steps; exactly two lavender rails; visibly separate floating landing platform lower-right. No characters. Motion is limited to tiny cloud drift and one restrained airplane settle. Hold long enough to count every step. No lawn, playground, castle, kingdom, forest, lake, animal, extra step, missing rail, glowing portal, cut, pan, zoom or redesign.
```

### V2-S12 — careful descent

Start from a character-complete still built on `ROUTE_ANCHOR_V2`; attach Roshan rear, Daddy rear, and exact airplane.

```text
One continuous locked three-quarter route shot. Daddy is ahead on the upper step, Roshan one step behind, maintaining Roshan's left hand to Daddy's right. Daddy places his tail/body weight on the first pearl step, tests it, looks back at Roshan, then leads a slow descent. Show real contact with the visible steps; never float past or through them. Complete only the first several careful steps during this take and end balanced. Preserve exactly six steps and two rails. No grass, playground, castle, animal, teleport, portal, cut or camera move.
```

### V2-S13 — invitation before reveal

Use an approved platform-side still with both identities. The kingdom remains outside frame.

```text
One continuous platform-side medium two-shot. Roshan screen-left and Daddy screen-right have safely reached the separate landing platform and still hold inner hands. The airplane and steps may sit softly behind them; the kingdom is entirely offscreen-right. Daddy turns his attention toward the unseen view, then looks to Roshan. Roshan follows his eyeline and begins to brighten. No castle, playground, forest vista, lake vista, animal, cutaway, portal, walking, text or camera move.
```

### V2-S14 — exact reveal

Use `FINAL_REVEAL_ANCHOR_V2` as the starting image. Do not add lower-priority references unless necessary.

```text
Animate this exact approved rear-view illustration as one continuous locked shot. Preserve every pixel-level geographic relationship: playground left, path bottom-center, bridge aligned to closed castle door, exact four-tower castle right, water, mountains and cabins. Roshan remains small lower center-left; Daddy remains small lower center-right; their inner handhold never breaks. Roshan raises only her free right hand once in a small wonder gesture. Daddy looks toward Roshan. Two tiny butterflies make restrained arcs and one tiny train puff dissipates. No camera move, geography change, front-facing turn, walking, airplane, animal, new landmark, open door, tower change, text or morphing.
```

### V2-S15 — final quiet hold

Prefer the last two seconds of an accepted S14 take. If a separate generation is unavoidable, start only from the accepted S14 ending frame.

```text
Continue the exact accepted final rear composition for six seconds with effectively still staging. Roshan gently lowers only her free right hand; the inner handhold remains. Daddy remains still. One small sparkle appears left of the path. Preserve the locked camera, exact geography, castle, bridge, closed door, playground, characters and scale. No walking, wave, lip movement, camera motion, new object, animal, open door, UI, text or redesign.
```

## Assembly instructions

1. Download every native accepted take and retain its original filename/hash.
2. Trim to the authored durations; do not time-stretch.
3. Assemble at 1280×720, 24 fps with straight cuts.
4. Never insert a scenic cutaway merely to hide a failed action. Regenerate the failed shot from its last approved anchor.
5. Add family dialogue and licensed sound only after picture lock.
