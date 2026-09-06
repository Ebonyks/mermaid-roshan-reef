# Geologist and Teacher pose-containment review — 2026-09-05

## Verdict

The `STORY_POSE_FRAMES` change is a valid **damage-containment correction**. It stops the visibly broken 7 fps cycling of unrelated pose keys and avoids Geologist idle cells 0/1, whose tails lack the complete fin. It does not turn either sheet into authored idle, travel, or work animation. Current runtime verification remains pending because this review did not run Godot.

Reviewed sources and SHA-256:

- `scripts/opera_roshan_actor.gd`: `556301bbaeefcc55f7a5c28744170872e488563719aee54856ad4c65c4e9cb6d`
- `assets/opera/worlds/actors/animation/roshan_geologist_sheet_a.png`: `1fd7080933fd49b27a9cbb2b20d9470e4fd654dec58db72e9aa9e081a6e24c37`
- `assets/opera/worlds/actors/animation/roshan_teacher_sheet_a.png`: `2bddeebd6ca4fe0647e1f6deb670bfcab4d1183f36417e0a033e59c4788dd28c`

## Code facts

The general actor timing table remains idle 4 fps, travel 8 fps, work 7 fps, and cheer 6 fps for ordinary career sheets. These values are code facts only; they do not prove smooth motion or coherent neighboring frames.

`STORY_POSE_FRAMES` now holds:

- Geologist: idle row 0 cell 3, travel row 1 cell 1, work row 2 cell 0.
- Teacher: idle row 0 cell 0, travel row 1 cell 0, work row 2 cell 0.

`show_pose()` applies those single cells and disables processing, so the ordinary 4/8/7 fps row loops no longer run for these states. `idle_frame()` also selects Geologist idle cell 3 for menu presentation. Cheer remains the only advancing sequence for these two careers: four row-3 cells, once, at `POSE_CHEER_FPS = 2.0`, holding the final frame. This matches the containment pattern used for Ballerina.

## Geologist sheet review

The sheet is a 4×4 set of discrete story poses, not four coherent frame sequences. At source size, Roshan's face, explorer cap, vest, pouch, rainbow hair and tail palette remain consistent. The selected cells are materially safer:

- **Idle 3** has the complete two-lobed rainbow fin and a calm open-hand pose. It fixes the incomplete-fin silhouette in idle 0/1.
- **Travel 1** is a readable horizontal swim with complete fin, intact hands and consistent costume.
- **Work 0** is a grounded crouch/reach pose with complete fin and clear downward attention, suitable as a held generic geology-work pose.

The prior work-row loop was unacceptable: cells 0–2 are crouch/reach variants while cell 3 abruptly becomes an upright crystal presentation. At 7 fps the crystal reappeared every four frames, about every 0.57 seconds, with large pose, hand, body-axis and prop changes. Holding cell 0 removes that false repeated action.

Remaining limitations:

- Held travel is static art translated by the world. It is not authored swimming animation under `DL-MOT-07`.
- Held work does not show brush/fossil contact, pan motion, river-stone placement, or geode contact. The environment supplies the verb while Roshan stays in one generic reach pose.
- The pose pivots and apparent occupied bounds differ across idle/travel/work. The selected cells look anatomically sound in the atlas, but runtime anchor stability and contact alignment are unverified.
- The cheer row changes from crystal presentation to clasped-hands joy, pointing, then arms-up cheer. At 2 fps once this reads as a slow sequence of celebratory keys and avoids looping the crystal. It is acceptable containment, though it is not a continuous geology-specific action.

Assessment: **source pose quality 4.4/5; containment selection 4.6/5; authored animation completeness 2.5/5**. No selected cell has an obvious remaining wrong fin, identity break, extra limb, or costume error. Runtime check is pending.

## Teacher sheet review

The sheet also contains discrete presentation keys rather than in-betweens. Source identity is consistent: face, jacket, badge/pouch details, hair and rainbow tail remain recognizable, with clean contours and complete anatomy in the selected cells.

- **Idle 0** is the neutral teacher pose and is a valid held rest.
- **Travel 0** holds the first horizontal swim cell. It avoids the smile/eye/arm and direction changes across the row, but remains a static translated card.
- **Work 0** holds the first pointer pose. It prevents the pointer from jumping through incompatible directions at 7 fps and gives the lesson a stable pointing gesture.

The old work-row loop was unacceptable: the pointer switches from raised left, extended right, low diagonal, and raised left/open palm every four frames. That sequence has no stable target, anticipation, contact or settle and would redirect attention every 0.57 seconds. Holding work cell 0 correctly keeps one instructional direction.

Remaining limitations:

- A single pointer direction cannot truthfully indicate every lesson target. Runtime layout must place the live object along that direction or use a separate object-bound pointer; otherwise `DL-READ-06` remains at risk.
- Held travel is not authored swimming animation under `DL-MOT-07`.
- Held work has no transition into pointing and no responsive contact/payoff with the selected learning object.
- The cheer row progresses from clasped hands to eyes-closed clasp, one raised fist, then two raised arms. At 2 fps once it is a legible slow curtain-call progression, but smoothness and pivot stability still require runtime sequence inspection.

Assessment: **source pose quality 4.4/5; containment selection 4.5/5; authored animation completeness 2.5/5**. No selected cell has an obvious identity, fin, limb or costume defect. Pointer-to-target truth remains runtime-dependent.

## Validator scope

`tools/audit_opera_roshan_animation.py` currently reports 13 career atlases and 208 reviewed cells. It does **not** include `roshan_geologist_sheet_a.png` or `roshan_teacher_sheet_a.png`. A passing result from that tool provides no source, pack, duplicate-frame, alpha-padding, identity, costume, anatomy or semantic-review claim for either new sheet.

Before either career can claim accepted animation, extend or add an equivalent audit inventory for both 1024×1024 sheets and all 32 cells, then capture actual runtime state transitions. Required evidence includes selected idle/travel/work cells, menu idle, cheer frame progression/final hold, stable bounds/pivots, and the live Teacher pointer target and Geologist tool/contact alignment. Until then status is `POSE_DAMAGE_CONTAINED; TRUE_AUTHORED_ANIMATION_PENDING`.

## Existing career work-row source audit

The following observations come from direct inspection of the current 1024×1024 runtime atlases. They are **source-sheet findings**, not claims about captured runtime cadence. The shared actor calls `work` after accepted task input, and ordinary career `work` advances the four row-2 cells at 7 fps. Because that is one complete four-cell cycle every 0.57 seconds, a row made of separate semantic keys reads as rapid prop/verb substitution rather than animation. The existing 13-career/208-frame validator can establish inventory, dimensions, alpha/padding and recorded human identity review; it does not establish temporal continuity, phase-appropriate acting, pivot stability in motion, or runtime contact.

Reviewed runtime sheets and SHA-256:

- Chef: `assets/opera/worlds/actors/animation/roshan_chef_sheet_a.png`, `78c666d2e87cc1cdcd2cde311c20e75a83ca86dae1366fe4aa9cacbee3e30566`
- Doctor: `assets/opera/worlds/actors/animation/roshan_doctor_sheet_a.png`, `bfffbd5389d63f8c9337a132bb20e09abbd4d8fc8471ec406fba2d722106a50e`
- Farmer: `assets/opera/worlds/actors/animation/roshan_farmer_sheet_a.png`, `f0c9947b093c489145945467af62e50ce748b56b344c55942b7532742bc64bc5`
- Painter: `assets/opera/worlds/actors/animation/roshan_painter_sheet_a.png`, `016dbac4a6c2342679410c19aa782d999557b92f4fc34f99f58d23dd714ea638`
- Astronaut: `assets/opera/worlds/actors/animation/roshan_astronaut_sheet_a.png`, `ccfb8e7af3a033e31e05af40fa62dc23b676aec6204ba8810e8cf79cbfc4d6fa`
- Racer: `assets/opera/worlds/actors/animation/roshan_racer_sheet_a.png`, `f62f881d42b439bde09a8bc7f6e0000125acd3e27aabf1fd39d90722ce75ca79`

### Chef

The work row keeps the bowl, whisk, costume, body axis and gaze coherent across all four cells. The whisk moves through distinct positions in the batter while the supporting hand continues to carry the same bowl. These are credible stirring keys, though the spacing is broad enough that actual 7 fps smoothness and contact still need a runtime sequence capture. The source rendering is polished and internally consistent: **source-sheet art quality 4.7/5; work-row animation appropriateness 4.4/5**.

The row truthfully represents **MIX/STIR** only, and most strongly STIR. It does not depict tipping batter, oven handling, frosting contact, or topping placement, so it should not be treated as a semantic animation for BAKE, FROST, or TOP. If phase-specific held mapping is needed before authored clips exist, use work cell 0 or 1 for MIX/STIR and an identity-safe neutral pose for the remaining phases; this is a containment proposal, not a substitute for the missing phase actions.

### Doctor

The work row is a set of different medical story poses. Cell 0 holds a stethoscope chest piece; cell 1 drops the stethoscope and makes a bare-hand examination/attention gesture; cell 2 introduces a long unrolled bandage; cell 3 changes to actively wrapping/holding the bandage. Cycling them at 7 fps makes the stethoscope vanish, the bandage appear, and the action jump from examination to wrapping every 0.57 seconds. Individual cells retain strong identity, clean contours and readable props, but the row is not one continuous action: **source-sheet art quality 4.6/5; work-row animation appropriateness 2.3/5**.

Visible semantic mapping is sufficiently clear to hold cell 0 for **FIND/X-RAY examination context**, cell 1 for a generic FIND response, and cells 2 or 3 for **CAST/BANDAGE**. No work-row cell depicts WASH, and the atlas alone does not prove scanner contact for X-RAY. These should be phase-selected poses rather than one loop until each verb has a dedicated temporal sequence.

### Farmer

The work row switches among separate farming verbs: cell 0 extends one hand while reaching toward the waist pouch, cell 1 kneels with both hands planted downward, cell 2 stands and presents a carrot with leafy top, and cell 3 returns upright with open hands and no carrot. At 7 fps Roshan repeatedly stands, kneels, produces a carrot, and loses it within one 0.57-second cycle. The art is attractive and the farmer costume and face remain consistent, but the row is a pose library rather than animation: **source-sheet art quality 4.6/5; work-row animation appropriateness 2.0/5**.

The visible mapping supports cell 0 as a **PLANT seed/scatter preparation**, cell 1 as **PLANT contact**, and cell 2 as a **TOSS vegetable preparation**. Cell 3 is only a generic presenting gesture. None of the four cells visibly depicts HERD movement or PICNIC placement, so those phases need neutral containment or purpose-made acting rather than cycling this row.

### Painter

All four work cells preserve the palette and brush, with the brush moving from low/side to raised and back while the palette remains in the supporting hand. Costume, silhouette and prop identity remain stable. The arm travel is large and the row lacks a pictured canvas/contact point, so source pixels alone cannot prove that the brush stroke lands on the live reveal surface or that the loop reads smoothly at 7 fps. Still, it is a coherent painting action rather than a set of unrelated phase keys: **source-sheet art quality 4.7/5; work-row animation appropriateness 4.3/5**.

Use the sequence for **PAINT** only. STAMPS and GALLERY require different verbs, and no cell clearly shows stamping or hanging/choosing a frame. A held work cell would be semantically weaker than the existing four-cell paint sequence for PAINT and is not recommended without runtime evidence of a cadence defect.

### Astronaut

Every work cell retains the same wrench and astronaut costume. Cells 0 and 1 grip the wrench with both hands in front; cell 2 shifts to an upright one-hand tool pose with the free hand on the hip; cell 3 raises the wrench overhead. The prop does not disappear, but the jump from two-hand tightening to presentation is a change of action intent rather than an in-between. Repeating all four at 7 fps reads as tighten, pose, celebrate, reset. Individual art is polished and consistent: **source-sheet art quality 4.7/5; work-row animation appropriateness 3.4/5**.

Cells 0–1 can serve **PIPES/VALVE tool-work** containment, while cell 3 is a completion/presentation key. The row does not visibly show leak patch contact or launch-button/countdown acting, so PATCH and LAUNCH should not inherit the full wrench loop as if it described those tasks. A dedicated two-cell 0↔1 loop may be plausible, but its cadence and hand/tool contact must be checked at runtime before acceptance.

### Racer corroboration

The Racer work row confirms the same category error in its strongest form: cell 0 presents a wrench, cell 1 holds a steering wheel and points, cell 2 raises a checkered flag, and cell 3 makes a fist/punch gesture. These are four separate actions, not consecutive frames of one action. At 7 fps the wrench, wheel and flag replace one another every 0.14 seconds and the four meanings repeat every 0.57 seconds. The individual character illustrations are clean and appealing, but the sequence is temporally unusable: **source-sheet art quality 4.7/5; work-row animation appropriateness 1.8/5**.

The exact phase mapping visible in the art is cell 0 for **TUNE**, cell 1 for **TO THE LINE/RACE steering instruction**, and cell 2 for a race finish or start signal. Cell 3 is a generic victory/action accent and should not loop during any of the three tasks. This corroboration does not replace runtime inspection of the current Racer packet; it establishes only what the atlas cells depict.

## Implication for repair

Do not apply one blanket hold policy to the five careers above. Preserve Chef's stir and Painter's paint sequences pending runtime cadence review; test Astronaut cells 0–1 as a bounded tool loop; route Doctor, Farmer and Racer by phase to the exact semantic key where one exists. Missing verbs remain authored-animation gaps. Acceptance still requires runtime captures showing the chosen pose or sequence during each named phase, stable anchoring, correct object contact, no rapid prop substitution, and a readable transition back to idle or cheer.

## Remaining career work-row source audit

These seven reviews complete direct source-pixel inspection of every current career work row. Scores describe the 1024×1024 atlas and whether its four row-2 keys form an appropriate sequence. They do not prove runtime smoothness, phase contact, scale, anchoring, or device presentation.

Reviewed runtime sheets and SHA-256:

- Detective: `assets/opera/worlds/actors/animation/roshan_detective_sheet_a.png`, `fb0a7d8b718d797484f1d0da22c330a7e01d0e0bb192f9296f3f288a30cf7e7c`
- CandyMaker: `assets/opera/worlds/actors/animation/roshan_candymaker_sheet_a.png`, `b858c07f52d4f67679a39dd039afc7123199646442c067368425f8f46deec179`
- Boxer: `assets/opera/worlds/actors/animation/roshan_boxer_sheet_a.png`, `dbda6f6edd01e48b74095915f338fe3f6eb690ccd5f0f314d50e6940bb33c7c9`
- Magician: `assets/opera/worlds/actors/animation/roshan_magician_sheet_a.png`, `768e6980fa8f4ca9cc3281a2fb1f23f0fcdeac8f2d524e6135b3be03eafc13cb`
- Nursery: `assets/opera/worlds/actors/animation/roshan_nursery_sheet_a.png`, `9880fc9ac328b0112d8a7162c656b2a2d9471a4995dd11bd606607f12ca13a52`
- Popstar: `assets/opera/worlds/actors/animation/roshan_popstar_sheet_a.png`, `0084e74b73042832f248c26f6688e484b7376ea6418caee09b2e4beeebfb0ee9`
- Ballerina: `assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png`, `c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995`

### Detective

All four work cells retain the magnifying glass, detective cap, cape, satchel and downward investigative attention. The body moves from a low close inspection through upright lens positions and back to a lens held directly before the face. This is a coherent family of searching keys, although the large low-to-upright body change may still snap when repeated at 7 fps. **Source-sheet art quality 4.7/5; work-row animation appropriateness 4.1/5.**

The sequence visibly supports **SEARCH**. It does not show placing clues on the CASE BOARD or opening/identifying the CROWN chest. Those phases should use a neutral detective key or purpose-made actions rather than presenting the search loop as phase-specific acting.

### CandyMaker

The work row consistently shows long candy tongs in one hand and a padded mitt in the other. Wrist, tong angle and expression vary, but the costume, body axis and both props remain stable. It can read as repeated candy handling; no candy or mold contact is visible in the isolated atlas, so its exact action remains incomplete. **Source-sheet art quality 4.6/5; work-row animation appropriateness 4.0/5.**

This row most clearly supports **SORT** with the tongs. It does not depict pouring SYRUP, twisting a wrapper for WRAP, or handing candy to a friend for SHARE. Keep those semantic limits explicit even if the generic work loop remains as incidental feedback.

### Boxer

The four work cells form a readable short combination: two extended punches with small head/torso changes, an opposite-side extension/guard transition, then a guarded reset. Gloves, outfit and body scale remain consistent, and no prop substitution occurs. The broad alternating arm positions are plausible boxing keys, but source inspection cannot establish timing, impact contact, or whether the apparent side change snaps at 7 fps. **Source-sheet art quality 4.6/5; work-row animation appropriateness 4.2/5.**

The sequence supports **JAB PRACTICE** and may serve the TITLE IMP/BELT punch moments if runtime contact is aligned. **GLOVE GUIDE** and **SOFT GUARD** ask for positioning/guard rather than a repeating punch; the row-2 final guard cell is the only visibly compatible held key for SOFT GUARD. The specialist surface owns these interactions, so acceptance depends on its actual pose/event routing, not the generic row alone.

### Magician

The work row preserves costume and wand identity but changes among distinct magical outcomes. Cell 0 surrounds Roshan with a glowing spiral; cell 1 changes that spiral's path and wand sweep; cell 2 introduces a rigid violet circular glyph around the wand; cell 3 replaces it with a large orange-violet portal beside her. The effect topology and action meaning change abruptly, so the four cells are a staged effect progression or pose library, not a safe generic loop. **Source-sheet art quality 4.7/5; work-row animation appropriateness 2.8/5.**

Cells 0–1 can support a bounded **VANISH/ROPE wand flourish** if runtime context makes the target clear; cells 2–3 visibly support **PORTAL** formation. No cell clearly depicts hat tracking or opening the CABINET. Repeating portal creation during every phase would give false semantic feedback.

### Nursery

The work row combines separate caregiving keys. Cell 0 presents a white cloth or folded pad; cell 1 changes to a small bottle held at the torso; cell 2 closes the eyes and cradles both arms without the prior visible object; cell 3 introduces a large peach towel/blanket. At 7 fps these objects appear and disappear while the arms jump between presenting, holding and cradling. Costume and face remain consistent, but the row is not one temporal action. **Source-sheet art quality 4.5/5; work-row animation appropriateness 2.1/5.**

The atlas supports cell 0 as **WASH HANDS** cloth context, cell 1 as **FEED** bottle context, cell 2 as **BURP/soothing** containment, and cell 3 as **BEDTIME** blanket context. It contains no clear CATCH BABIES pose. These are phase-specific held-key candidates only; live baby/object contact must be verified before any acceptance claim.

### Popstar

All four work cells keep the microphone at Roshan's mouth while facial expression, free-hand gesture and torso lean change. The mic, stage costume and singing intent stay continuous, with no unrelated prop replacement. The gestures are broad performance keys and may still pop without in-betweens, but the row reads as one sustained singing performance. **Source-sheet art quality 4.7/5; work-row animation appropriateness 4.3/5.**

The sequence directly supports **SOUND CHECK** and **RHYTHM**, and can provide incidental singing during ENCORE. It does not depict the requested DANCE arrow selection or a full-body spin, so it is not phase-complete acting for DANCE or ENCORE. Runtime microphone alignment and cadence remain unverified.

### Ballerina under `DL-MOT-09`

The work row contains four discrete ballet pose keys: an open diagonal/low reach, arms crowned overhead, a broad open second-position presentation, and a closed hand-to-heart pose. Neighboring silhouettes and arm placements change too much to be temporal in-betweens. The source art is polished and consistent, but ordinary 7 fps looping would be visibly wrong: **source-sheet art quality 4.7/5; ordinary work-row animation appropriateness 1.9/5; held-pose semantic appropriateness 4.7/5.**

Current code correctly treats Ballerina separately. `DL-MOT-09` requires the low/heart, open/second, or crown/fifth key to be held; `ballet_pose_cue` selects an individual row-2 cell, and Ribbon Trail changes among named pose keys by controlled progress rather than running the ordinary work loop. Cheer alone plays once and holds its final cell. The pictured keys support **PEARL MIRROR** pose matching and controlled recital poses during **RIBBON TRAIL**. **GRAND TWIRL** depends on the specialist surface's pearl motion; the atlas contains no continuous body-twirl animation. This source review affirms the held-key policy and makes no new runtime acceptance claim.

## Complete source-row conclusion

Across all 15 careers, the atlas gate must never be cited as proof that row playback is coherent. Chef, Detective, CandyMaker, Boxer, Painter and Popstar have recognizable single-verb work rows worth preserving for their matching phases pending runtime review. Astronaut has a plausible two-key tool subset. Doctor, Farmer, Magician, Racer, Nursery, Geologist and Teacher mix distinct verbs, props or directions and need phase routing or held containment while authored actions remain missing. Ballerina already has the required held-key exception. Every score above remains subordinate to actual phase capture and target-device review.

## Parent runtime verification

The retained pose policy subsequently passed `scripts/probe_opera_2d.gd` under exact Godot 4.7.2: all fifteen careers/seventy phases, stable Teacher/Geologist held rows, Geologist menu fin selection and non-repeating celebrations. See `validation/probe-opera-final.log`. These runtime state contracts do not establish visual smoothness or repair the missing authored action sequences.
