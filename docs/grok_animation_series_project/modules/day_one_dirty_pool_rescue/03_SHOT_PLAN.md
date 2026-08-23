# Shot plan and continuity chain

## Authorities

- Game scene/state authority: commit `71198979`
- Style authority: owner-approved base video/style stills, then Series Style
  Bible
- Roshan authority: canonical character folder
- Rumi authority: canonical private-project character folder
- Location authority: `POOL_CLEAN_FULL`
- Fixture identity: `SEAHORSE_CLEAN`, `WATERFALL_CLEAN`
- Dirty-state content: four explicitly content-only runtime references
- Wardrobe: canonical Roshan and Rumi outfits; no substitutions
- Time/light: interior Day One, initially dingy, ending luminous and warm

## Continuity locks

- Screen direction: Roshan begins lower-left and generally moves/looks inward
  toward screen-right. Rumi rises near center and turns toward Roshan.
- Object ownership: the pink wrapper begins lodged in the seahorse mouth,
  transfers to Roshan's right hand during `SH060`, and is then removed from
  frame. It never teleports or returns.
- Geography: waterfall left-of-center, reef arch center-right, seahorse
  right-of-center, shell lounge left, towel shelf right.
- Dirt state: monotonically decreases `4 → 3 → 2 → 1 → 0`.
- Light state: improves subtly with each cleanup and reaches full clean-room
  light before Rumi's face is fully revealed.
- Rumi: absent through `SH070` opening; rise begins only after seahorse rescue.
- Camera: composed wides and restrained medium cuts; no orbit, handheld drift or
  geography reversal.

## Shot table

| Shot | Authored / request | Camera | Single clear action | Start state | Required end state |
|---|---:|---|---|---|---|
| `MR_E01_SQ020_SC010_SH010_dirty-arrival` | 5s / 6s | Locked wide, child-height | Roshan swims in from lower-left and stops as she sees the neglected pool | Approved dirty-room anchor, no Rumi | Roshan lower-left, concerned eyeline toward pool/seahorse; all four problems intact |
| `MR_E01_SQ020_SC010_SH020_seahorse-noticed` | 5s / 6s | Gentle cut to medium over Roshan toward right | Roshan notices the clogged seahorse and reaches forward without touching yet | Accepted `SH010` ending state | Wrapper clearly readable in nozzle; Roshan resolves to help; dirt count 4 |
| `MR_E01_SQ020_SC010_SH030_surface-clean` | 6s / 6s | Medium-wide pool center | Roshan gathers/lifts the broad surface algae and harmless trash out of the water | Dirt count 4 | Surface cluster gone, waterfall/rim/seahorse still dirty; dirt count 3 |
| `MR_E01_SQ020_SC010_SH040_waterfall-clean` | 6s / 6s | Medium on left waterfall, geography visible | Roshan pulls the hanging growth clear in one decisive motion | Dirt count 3 | Waterfall growth gone and faint rainbow flow returns; rim/seahorse dirty; dirt count 2 |
| `MR_E01_SQ020_SC010_SH050_rim-clean` | 5s / 6s | Low medium on foreground/right rim | Roshan sweeps the small rim cluster together and removes it | Dirt count 2 | Rim clean; only seahorse remains dirty; dirt count 1 |
| `MR_E01_SQ020_SC010_SH060_seahorse-rescue` | 7s / 8s | Intimate medium two-subject composition | Roshan gently extracts the pink wrapper from the mouth/nozzle and frees the tangled strand | Approved rescue anchor; wrapper lodged | Wrapper ends in Roshan's right hand; nozzle clear; growth releases; dirt count 0 |
| `MR_E01_SQ020_SC010_SH070_room-restored` | 7s / 8s | Return to locked wide | Clean water, rainbow waterfall, seahorse stream and room light return in a restrained sequence | Accepted `SH060` ending frame | Exact clean geography, luminous light, sparse ripples/glints; Rumi rise just beginning below center |
| `MR_E01_SQ020_SC010_SH080_rumi-rises` | 7s / 8s | Wide-to-medium gentle push, no reframe | Rumi swims up, settles upright and gives one broad friendly wave | Approved clean-reveal anchor / `SH070` ending | Rumi center, exact identity, waving toward Roshan; braid/sleeves settling |
| `MR_E01_SQ020_SC010_SH090_thank-you` | 7s / 8s | Warm medium two-shot | Rumi performs a silent dialogue-friendly thank-you/introduction; Roshan responds with relieved delight | Accepted `SH080` ending frame | Both distinct, safe, smiling and facing each other; clean room remains unchanged |

## Anchor stills before motion

1. `A01_DIRTY_ROOM_APPROVED` — complete dirty room with exact geography and no
   characters. Reject until all four problems are readable and style-repaired.
2. `A02_SEAHORSE_RESCUE_APPROVED` — Roshan and exact clogged seahorse at the
   moment before contact, with wrapper ownership unambiguous.
3. `A03_CLEAN_REVEAL_APPROVED` — exact clean room, Roshan lower-left and Rumi's
   approved scale/settled position near center.

Dependent motion must not begin until the controlling anchor is approved.

## Assembly

Request 6s or 8s clips as listed, trim to authored duration, and assemble at
16:9 for the 1280×720 target. Use straight cuts for authored angle changes.
Use accepted ending frames for uninterrupted actions. Never time-stretch,
interpolate, morph, cross-dissolve or duplicate frames to conceal failed motion.
