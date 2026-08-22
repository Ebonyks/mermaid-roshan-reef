# Manual Grok Project interface setup

This package is designed for the signed-in Grok web interface, not an API or browser automation.

## Create the Project

1. In Grok Imagine, choose **New project**.
2. Name it `Mermaid Roshan — Animation Series`.
3. Paste the bootstrap message from `../GROK_START_HERE.md`, including the dedicated GitHub branch URL. Ask Grok to read and confirm the five requested items before generating.
4. Open a Project chat named `00 — Series Bible` and paste the fenced block from `00_PROJECT_CONSTITUTION_COPY_PASTE.md`.
5. Attach or paste `01_STYLE_BIBLE.md`, `02_CAST_REGISTRY.md`, and `03_PROJECT_ARCHITECTURE.md` in that chat. Ask Grok to summarize the authority hierarchy without generating art; correct any misunderstanding before production.
6. Create one Project chat named `01 — Character Library`. Introduce each character folder separately. Do not upload the whole cast in one request.
7. Create separate Project chats for locations and for each episode/sequence. The first included sequence is `opening_flight_to_sky_lagoon`.

The branch is a stable read-only knowledge source for Grok. Continue attaching the exact reference images needed by an Imagine generation; do not assume that browsing the branch automatically conditions the video model.

## Introduce a character

1. Paste that character's `IDENTITY_CARD.md`.
2. Add the primary identity image with the image-attachment control beside the prompt field.
3. Add only the supporting turnaround/motion/relationship image needed for the current check.
4. Paste the **Reference conflict check** prompt from `05_COPY_PASTE_PROMPT_TEMPLATES.md` and verify Grok names the correct immutable traits.
5. Do not generate production video until the written summary is correct.

For Rumi, start with `RUMI_FULL_BODY_IDENTITY.png`. Introduce the pose atlas in a second message. Add `RUMI_AND_ROSHAN_RELATIONSHIP_SAMPLE.png` only when explaining her bond and scale relative to Roshan.

## Generate one shot

1. Open the correct sequence chat.
2. Select **Video**, **16:9**, and a duration no greater than **15s**. Prefer 6s or 10s when that cleanly contains the beat.
3. Attach the accepted starting frame first, then the relevant character identity, location authority and one style frame. Normally use two to four images; add more only when each has a distinct declared job.
4. Paste the filled shot template. Explicitly label every attachment: `Image 1 = start frame`, `Image 2 = Rumi identity`, and so on.
5. Generate manually. Download the native result immediately and rename it with the series convention.
6. Run the continuity-review prompt in the same sequence chat. Mark the local ledger `APPROVED`, `REVIEW`, or `REJECT`.

## Continue past 15 seconds

Do not ask Grok to “continue the full scene.” Extract or select the accepted ending frame of the prior clip, attach it as Image 1, restate the unchanged authority pack, and generate the next independently named shot. Join accepted shots in the external edit.

## Avoid Project-history drift

Project memory and chat history help organization, but they do not replace attachments. Never say only “same Rumi,” “same castle,” or “continue as before.” Reattach the controlling identity/geography/start-frame images and declare their domains every time continuity materially matters.
