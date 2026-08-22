# Grok Imagine interface handoff — opening flight to Sky Lagoon

Status: manual interface workflow for storyboard, trial, and potential production footage. Grok output must pass visual, narrative, technical, licensing, and human-review gates; it is not disqualified solely because it was generated as video.

## Outcome and format

- Story duration: 42.5 seconds at 24 fps (1,020 timeline frames).
- Frame: 16:9 landscape. Use 720p in Grok Imagine for trials; retain every native download unchanged.
- Audio: off for visual trials. Family voices must be recorded separately; do not synthesize or clone Daddy or Roshan.
- Look: polished hand-painted 1990s television-anime storybook feeling—clean navy/violet linework, flat pastel value bands, restrained cel highlights, aqua/lavender shadows, expressive readable faces, soft painted clouds. Do not request a living artist or protected studio/franchise imitation.
- Dramatic arc: uncertainty → Roshan chooses Daddy's hand → safety → threshold crossing → wonder → readiness.
- Screen direction: Roshan screen-left and Daddy screen-right until the rear kingdom reveal.

## Interface recipe

1. Open Grok Imagine and choose **New project**. Name it `Mermaid Roshan — Opening Previz — Sky Lagoon Lock`.
2. Work in **Image** mode first. Select **Quality**, **16:9**, and the smallest useful image count. Generate and approve shot keyframes before selecting Video.
3. Upload only the reference files listed for that shot. Do not upload anything from `assets/book/`, `assets/audio/voices/`, `assets/characters/friends/`, any `rejected` folder, or any `runtime_rejected` folder.
4. Paste the global lock and the shot prompt from [SHOT_PROMPTS.md](SHOT_PROMPTS.md). Keep reference order exactly as listed.
5. For the final kingdom shots, approve a still that preserves the exact geography before trying motion. If the castle, path, playground, mountains, or lagoon shifts, reject it immediately.
6. Switch the approved still to **Video**, choose **6s**, **720p**, **16:9**, and turn the speaker/audio control off. Ask only for the motion described in the shot.
7. Download the native result, record the attempt in `trial_log.md`, and never overwrite it. Promote a clip only after human review of identity, topology, geography, motion, style, child readability, audio, and encoding quality.

## Reference deck

Use these repository files directly; their hashes are locked in [reference_manifest.json](reference_manifest.json).

| ID | Visual authority | Use |
|---|---|---|
| `ENV-HERO` | `assets_src/sky_lagoon/castle_symmetry_2026-07-29/qa_four_tower_fit_2screen.jpg` | **Primary final-shot geography.** Playground left, pearl path foreground, accepted castle right, mountains/cabins behind. |
| `ENV-PANO` | `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png` | Sky, cloud sea, valley, water, mountain palette and broader world continuity. Not a castle authority. |
| `CASTLE-V4` | `assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png` | Exact castle identity: two lower outer towers, two taller inner towers, central stained-glass gable, coral door and bridge. |
| `PLANE-V5` | `assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png` | Exact mint/aqua/lavender aircraft shell and three-window identity. |
| `ROSHAN-FRONT` | `assets/characters/roshan_25d/roshan_base.png` | Canonical face, hair, tiara, clothes and tail palette. |
| `ROSHAN-BACK` | `assets/characters/roshan_25d/roshan_swim_back.png` | Rear silhouette/pose authority for the final hero shots. It is an atlas; tell Grok to treat it as multiple pose studies, not multiple characters. |
| `DADDY-FRONT` | `assets_src/daddy_master.png` | Canonical Daddy identity: crown, glasses, blue ornate coat, teal cape and rainbow tail. No accepted rear drawing currently exists. |

The missing graphical handoff is an approved Daddy rear pose. Create this as a still-study before shot 17: use `DADDY-FRONT` alone, request a full-length back view with unchanged crown, cape, coat silhouette and tail colors on a plain neutral background, then obtain human approval. It is a reference candidate, not production art.

## Continuity lock (append to every Grok prompt)

`CONTINUITY_LOCK: one Roshan and one Daddy only; Roshan is a young mermaid child and Daddy is an adult merman; preserve their exact approved identity colors and clothing; no legs, feet, shoes, duplicated limbs, fused tails, owner swaps, costume changes, text, logos, UI, photorealism, 3D rendering, or extra characters. The airplane has exactly two passenger seats. Seat belts remain closed until their demonstrated release. Plane nose and door face screen-right; door opens outward. The exterior route is cassette/platform to exactly six pearl steps with exactly two lavender rails and then a separate landing platform. Daddy leads and Roshan never goes outside alone. The kingdom stays unreadable until shot 17. Preserve the handhold through the final frame.`

## Shot-by-shot storyboard

| # | Time / frames | Composition and action | Emotion / sound | Grok reference uploads |
|---:|---|---|---|---|
| 1 | 0:00–0:02 / 1–48 | Wide open sky. The approved plane crosses left-to-right. No island or kingdom. | Gentle curiosity; air and engine only. | `PLANE-V5`, `ENV-PANO` |
| 2 | 0:02–0:04 / 49–96 | Medium cabin two-shot, exactly two seats. Roshan left, Daddy right. A mild jolt; Daddy steadies his open hand, not Roshan. | Roshan uncertain; Daddy calm. | `ROSHAN-FRONT`, `DADDY-FRONT`, `PLANE-V5` |
| 3 | 0:04–0:06 / 97–144 | Roshan close-up: pendant arcs, fingers tighten, eyes rise toward Daddy. | Small breath; no dialogue. | `ROSHAN-FRONT` |
| 4 | 0:06–0:07.5 / 145–180 | Daddy close-up: he notices, softens his eyes, turns slightly, offers an open right palm. | Warm, patient silence. | `DADDY-FRONT` |
| 5 | 0:07.5–0:09.5 / 181–228 | Insert/two-shot. Roshan looks, reaches with her left hand, and completes the inner handhold with Daddy's right. | Daddy: “I'm right here, Roshan.” | `ROSHAN-FRONT`, `DADDY-FRONT` |
| 6 | 0:09.5–0:12 / 229–288 | Safe medium two-shot. Daddy draws Roshan into a gentle hug; one restrained sway; Roshan exhales. | Relief and safety. | `ROSHAN-FRONT`, `DADDY-FRONT` |
| 7 | 0:12–0:14.25 / 289–342 | Cabin touchdown: tiny settle, aqua light rolls across the window and faces. Belts still closed. | Daddy whispers, “We're here.” | `ROSHAN-FRONT`, `DADDY-FRONT`, `ENV-PANO` |
| 8 | 0:14.25–0:16.75 / 343–402 | Daddy demonstrates slowly: opens only his own belt; both belt halves rest beside his correct cushion. | Clear visual teaching beat. | `DADDY-FRONT` |
| 9 | 0:16.75–0:18.5 / 403–444 | Roshan copies, opening only her own belt; halves rest beside her cushion. | Daddy: “Ready?” Roshan: “Ready.” | `ROSHAN-FRONT`, `DADDY-FRONT` |
| 10 | 0:18.5–0:21.5 / 445–516 | Daddy rises first, offers right hand and waits. Roshan takes it with left hand and rises. | Consent and confidence. | `ROSHAN-FRONT`, `DADDY-FRONT` |
| 11 | 0:21.5–0:23.5 / 517–564 | Rear/side cabin tracking. They glide together toward the screen-right door; exactly two seats recede behind. | Light tail glide, cabin ambience. | `ROSHAN-BACK`, `DADDY-FRONT`, `PLANE-V5` |
| 12 | 0:23.5–0:26 / 565–624 | Door pad, seam, then outward opening. Wind lifts one Roshan hair streak and Daddy's cape edge. Outside is only bright sky. | First rush of new air. | `ROSHAN-FRONT`, `DADDY-FRONT`, `PLANE-V5`, `ENV-PANO` |
| 13 | 0:26–0:28.5 / 625–684 | Locked exterior route-establishing wide: plane upper-left, cassette/platform lower-right; exactly six pearl steps, two lavender rails, separate landing platform. Hold long enough to count. | Safe route becomes legible. | `PLANE-V5`, `ENV-PANO` |
| 14 | 0:28.5–0:32.5 / 685–780 | Daddy tests the first step, looks back, and leads. Both descend; tails visibly contact steps. Handhold maintained. | Courage through Daddy's example. | `ROSHAN-BACK`, `DADDY-FRONT`, `PLANE-V5`, `ENV-PANO` |
| 15 | 0:32.5–0:34.75 / 781–834 | Platform side two-shot. Kingdom remains fully offscreen. Daddy turns attention toward the unseen view. | Daddy: “Look, Roshan.” | `ROSHAN-FRONT`, `DADDY-FRONT`, `ENV-PANO` |
| 16 | 0:34.75–0:37.5 / 835–900 | Close two-shot from kingdom side. Roshan's eyes widen, mouth parts, then smiles. Daddy watches Roshan, not the kingdom. | Roshan: “Wow.” | `ROSHAN-FRONT`, `DADDY-FRONT`, `ENV-PANO` |
| 17 | 0:37.5–0:41 / 901–984 | Rear hero wide. Cut to the **approved geography** rather than asking Grok to invent an offscreen reveal. Roshan left, Daddy right, holding inner hands. Castle/path first read; playground second; water/mountains third. Roshan raises only her free right hand. Exactly two butterflies and one tiny train puff. Camera may ease back briefly, then locks. | Daddy: “Your reef is waiting.” | `ENV-HERO` first, `CASTLE-V4`, `ROSHAN-BACK`, approved Daddy-back study; optional `ENV-PANO` last |
| 18 | 0:41–0:42.5 / 985–1020 | Same accepted rear composition and exact camera. Roshan lowers her free hand. One sparkle appears left of the path. No wave, walk, UI, door opening or geography change. | Quiet wonder; musical resolve. | Approved shot-17 still **as first-frame image**; `ENV-HERO`, `CASTLE-V4` only if the interface permits additional references |

## Final-shot graphical handoff: non-negotiable map

For shots 17–18, `ENV-HERO` owns object placement. `CASTLE-V4` owns castle design. Neither prompt text nor another reference is allowed to overrule them.

- Left third: playground and open grass.
- Foreground center: pearl path entering from the bottom and leading toward the castle.
- Right half: four-tower castle, with the central gable/door visible and bridge aligned to the path.
- Background: cool mountain mass and small cabins; cloud sea and blue water remain secondary.
- Character pair: rear view on the foreground platform, Roshan left and Daddy right, together occupying roughly the lower central quarter without covering the castle door or path.
- Read order: castle/path → playground → water/mountains → characters' small gesture details.

Immediate rejection conditions: five or more towers; missing central gable; generic fairytale/theme-park castle; mirrored castle/playground sides; path that misses the bridge/door; extra sun; tropical palms; fog hiding geography; open castle door; extra character; separated hands; Daddy/Roshan costume drift; camera movement after the final lock.

## Cost/benefit trial order

1. **One still, shot 17 hero composition.** Cheapest test of geography and character-reference adherence. Stop if it fails twice.
2. **One 6-second 720p motion trial from the approved still.** Tests whether the camera, castle and handhold remain locked. Motion should be tiny.
3. **Daddy rear-view study.** Only commission this if the environment still passes; otherwise it is wasted generation.
4. **Cabin identity test (shots 2–5).** Tests two characters, hand ownership and exact two-seat continuity.
5. Only after both gates pass, generate the remaining shots as separate attempts. The 6-second interface minimum means substantial unused footage; treat it as a quality-control cost and trim to the authored timeline without stretching motion.

This ordering concentrates paid generations on the two real technical risks: exact final geography and two-character identity/hand continuity.

## Interface subscription findings (observed 2026-08-22)

The signed-in interface opened an upgrade dialog when **New project** was selected. The dialog showed these tiers with the annual-billing toggle enabled; verify checkout pricing before purchase because plans can change.

| Tier shown | Price shown | Relevant limits shown | Opening-cinematic value |
|---|---:|---|---|
| SuperGrok Lite | $10 USD/month | Basic images/video, a few creations per day, 480p, 6-second video | Cheapest geography/pose proof; too constrained for sustained 42.5-second iteration. |
| SuperGrok | $30 USD/month | 20× more usage, 720p, 30-second video stories | Best initial production trial: matches the current 720p canvas and provides iteration headroom. |
| SuperGrok Plus | $100 USD/month | 1080p video and significantly higher usage | Benefit is higher source resolution; weak value until identity and geography adherence are proven at 720p. |
| SuperGrok Heavy | $300 USD/month | Highest usage and additional agent/chat benefits | Poor fit for this single cinematic unless generation volume becomes the dominant bottleneck. |

Recommendation: do not buy Plus or Heavy for the first trial. Use direct New Generation if the existing account allowance permits it; otherwise buy at most one month of SuperGrok only after confirming that references upload correctly. One successful shot-17 still and one six-second video should be the purchase gate.
