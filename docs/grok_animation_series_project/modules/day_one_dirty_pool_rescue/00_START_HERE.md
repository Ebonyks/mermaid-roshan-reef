# Day One Mermaid Pool rescue — Grok handoff

## Purpose

This module hands the finished Day One Mermaid Pool scene and environment to
Grok for the next Mermaid Roshan animation sequence. It is a private beta/IP-
hold production module. It does not authorize public release, merchandising,
or reuse outside this project.

The game implementation and its exact local validation are fixed at commit
`7119897920e14724baaedd9c9dc254a95421027d`. Use that immutable commit for
environment and dirty-state references even if `dev` later advances.

## Story in one sentence

Roshan enters a dim, algae-covered Mermaid Pool, cleans four ordered problems
with the sick clogged seahorse last, restores the rainbow waterfall and light,
then meets Rumi as the approved violet-braided mermaid rises from the pool,
thanks her, and introduces herself.

## Read before generating

1. `../../project_guide/00_PROJECT_CONSTITUTION_COPY_PASTE.md`
2. `../../project_guide/01_STYLE_BIBLE.md`
3. `../../project_guide/02_CAST_REGISTRY.md`
4. `../../characters/roshan/IDENTITY_CARD.md`
5. `../../characters/rumi/IDENTITY_CARD.md`
6. `01_REFERENCE_UPLOAD_MATRIX.md`
7. `02_SCENE_ENVIRONMENT_AND_ACTION_BRIEF.md`
8. `03_SHOT_PLAN.md`
9. `04_GROK_PROMPTS_COPY_PASTE.md`
10. `05_REVIEW_GATES.md`

## Non-negotiable corrections

- The mermaid in the pool is **Rumi**, the owner-approved right-side character
  from `RUMI_AND_ROSHAN_RELATIONSHIP_SAMPLE.png`. Her former local codename is
  Violet Tide; use **Rumi** in story and prompts.
- Never use or describe the rejected unrelated pool mermaid formerly named
  `rumi_violet.png` / `rumi_wrong_identity_native.png`.
- Rumi retains her enormous violet braided high ponytail, pointed ears,
  star-shell earrings, lavender/navy gold-trim jacket, white shell top,
  turquoise-to-lavender tail and broad coral-pink split fin.
- The seahorse is the established magical fountain fixture, not a redesigned
  animal. The dirty state has a clearly visible soggy pink wrapper blocking its
  mouth/nozzle, plus soft seaweed growth. It has no horn and is never injured.
- Rumi does not appear before the seahorse is saved and the room begins to
  brighten.
- The runtime pollution cutouts are composition/content evidence only. The
  master audit rates their style 2/5 because they are too glossy, dense and
  halo-driven. Do not copy that rendering treatment into animation.
- Every delivered shot is a newly generated complete 16:9 frame sequence.
  Runtime sprites and screenshots are references only and may not be pasted,
  keyed, tweened or composited into final delivery pixels.
- Grok visual generation is audio off. Add only authorized recordings during
  editing; never synthesize or clone family voices.

## First message for the sequence chat

```text
This chat owns the Day One Mermaid Pool rescue sequence for the private Mermaid
Roshan animation series. Read the Project Constitution, Style Bible, Roshan and
Rumi identity cards, and every file in
modules/day_one_dirty_pool_rescue before generating.

Treat references by domain. The clean full Mermaid Pool controls geography and
recurring architecture. Clean fixture cutouts control seahorse and waterfall
identity. Dirty runtime cutouts control only which debris/growth is present and
where; they explicitly do not control rendering style. Canonical character
files control Roshan and Rumi. Approved base-video stills control finished
painted-cel style and motion cadence. An accepted previous ending frame controls
immediate continuity.

Before generating, return a concise confirmation of: (1) the four cleanup
states in order; (2) the exact Rumi identity locks; (3) the seahorse mouth-
blockage requirement; (4) fixed room geography; (5) why dirty cutouts are not
style authority; (6) the audio-off and 15-second rules. Name any file you cannot
open instead of guessing. Do not generate yet.
```

## Module state

- Handoff status: `READY_FOR_ANCHOR_GENERATION`
- Game source: commit `71198979`
- Branch CI evidence: GitHub Actions run `32614017038`, success
- Rumi: `APPROVED_PRIVATE_CANON`
- Clean room: approved recurring location anchor
- Dirty overlays: story/content reference only; animation restyling required
- Missing audio: exact Rumi thank-you/introduction recording remains pending
