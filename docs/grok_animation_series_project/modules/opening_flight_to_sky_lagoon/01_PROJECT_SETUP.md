# Using Grok Projects for continuity

## What Projects improve

According to xAI's current Imagine announcement, Projects organize work in the sidebar, multiple agents can work in parallel, and Search can locate earlier generations. Grok's official product page also describes iterative image/video editing within a thread. Use these features as a production desk:

- keep all opening outputs in one searchable workspace;
- give every asset and attempt a stable name;
- preserve the prompt/revision history beside the output;
- compare alternate anchor stills without mixing them into the accepted chain;
- run independent design-risk tests in parallel;
- continue a successful still or clip through follow-up iterations rather than restarting from text.

Sources: [Grok Imagine Video 1.5 announcement](https://x.ai/news/grok-imagine-video-1-5), [Grok product page](https://x.ai/grok?q=to+imagine), [Imagine overview](https://docs.x.ai/developers/model-capabilities/imagine).

## What Projects do not guarantee

Do not assume that an image uploaded somewhere in the Project is automatically used as visual conditioning for every generation. Explicitly attach the reference images needed for the current shot. The Project is the organizational memory; the actual attached images and starting frame are the visual control.

Official reference-to-video documentation permits up to seven reference images and a maximum 15-second duration, but reference overload can make authority ambiguous. This package normally uses two to four references per shot. Source: [xAI reference-to-video documentation](https://docs.x.ai/developers/model-capabilities/video/reference-to-video).

## Recommended Project work areas

### 1. `A — Character Anchors`

Purpose: Daddy rear-view study, Roshan/Daddy scale sheet, canonical handhold still. These may be explored in parallel because they do not depend on final motion.

Accept only one Daddy rear study and one canonical handhold. Rename accepted results:

- `APPROVED_DADDY_REAR_v01`
- `APPROVED_HANDHOLD_INNER_v01`

### 2. `B — Cabin and Airplane`

Purpose: shots 1–12. After the cabin identity still is accepted, generate shots sequentially. Do not use multiple agents to generate adjacent cabin shots independently.

### 3. `C — Exit Route`

Purpose: shots 13–16. First approve a locked route still with six steps and two rails. Generate the actual descent sequentially from that authority.

### 4. `D — Sky Lagoon Reveal`

Purpose: shots 17–18. This is the highest-priority geography gate. Use the exact geography reference first and castle reference second. Approve the still before generating video.

## Safe use of multiple agents

Run these four tasks in parallel only at the anchor stage:

1. Daddy rear-view design study.
2. Final Sky Lagoon geography-only still—no characters.
3. Cabin two-seat layout still with characters seated.
4. Six-step/two-rail exterior route still.

Then stop parallel work. A human selects one accepted result for each anchor. All dependent shots inherit those exact anchors sequentially.

## Naming convention

`B{block}_S{shot}_{kind}_a{attempt}_{status}`

Examples:

- `B4_S17_STILL_a01_REJECT_tower-count`
- `B4_S17_STILL_a03_APPROVED`
- `B4_S17_VIDEO_a02_REVIEW`
- `B1_S05_VIDEO_a04_APPROVED`

Never call two different designs “approved.” Rejected outputs stay searchable but must carry `REJECT_` and the failure reason.

## Continuation rule

For shots with uninterrupted action, export or capture the accepted final frame and use it as the next shot's starting image. Do not use this rule across an authored cut that deliberately changes camera angle; there, attach the character and environment authorities and create a new approved still first.
