# Fifteen-second production and editing model

Grok's maximum clip length is a shot ceiling, not an episode length. Build the hour-plus series from externally assembled shots.

## Practical duration targets

- 4–7 seconds: reactions, inserts, entrances, exits and single gestures.
- 7–12 seconds: most dialogue coverage and one complete physical action.
- 12–15 seconds: establishing shots or deliberately paced actions with a clear start and finish.
- Never ask one generation to perform multiple scene beats merely to fill 15 seconds.

## Continuity chain

1. Approve a sequence-opening anchor still.
2. Generate one shot at no more than 15 seconds.
3. Download the native result and extract/choose its accepted ending frame.
4. For uninterrupted action, use that ending frame as the next shot's starting composition.
5. For a cut, create a new anchor using the same character and location authorities plus explicit screen direction.
6. Assemble accepted clips in an editor; add approved voices, music and effects there.

## Planning arithmetic

One hour at an average accepted shot length of 8 seconds is roughly 450 shots before titles or holds. Do not create all shots as one undifferentiated Project stream. Organize them as episodes, sequences and shot IDs, with a continuity ledger per sequence.

Recommended naming:

`MR_E##_SQ##_SH###_v##_STATUS`

Example:

`MR_E01_SQ02_SH014_v03_APPROVED.mp4`

## Generation economy

Spend attempts on reusable anchors first: identity sheets, location masters, scale charts and recurring interaction poses. A reliable anchor can save many later retries. Reject early when identity, anatomy or geography drifts; polishing a structurally wrong clip is usually worse value than regenerating from a corrected start frame and smaller reference set.
