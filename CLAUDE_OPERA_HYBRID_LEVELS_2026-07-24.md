# Claude handoff — Opera House hybrid job levels

Date: 2026-07-24

Status: binding design direction for all twelve Opera career levels

## Owner decision

Every Opera career is one continuous two-act level:

```text
career door
  -> costume transformation
  -> ACT I: 2.5D job district teaches and rehearses the mechanic
  -> backstage threshold and safe checkpoint
  -> ACT II: formal Opera stage performance using the same mechanic
  -> friendly theater boss finale
  -> boss joins Roshan's curtain call
  -> return to lobby with the career star saved
```

The previous division between twelve non-stage job worlds and three separate
boss-only stages is obsolete. The job districts remain correct as Act I, and
the formal stage is now the second half of every job level.

This file supersedes any statement in the older handoffs that says:

- regular jobs never enter a theater stage;
- stage content is deferred to a separate boss phase;
- the three bosses are independent fifteenth-act style encounters; or
- a completed job returns to the lobby before its performance finale.

The older documents and art remain authoritative for the details explicitly
retained below.

## Experience target

The first half must make the child feel capable before the spectacle begins.
Act I introduces one verb with generous spacing, persistent guidance, and no
pressure. Act II then celebrates mastery by presenting the same verb with
music, curtains, lighting, and a friendly boss variation.

Do not switch from a learned mechanic to a generic sparkle attack. The
performance is the job:

- Pastry Roshan wins by assembling and decorating.
- Detective Roshan wins by finding clues.
- Ballerina Roshan wins by repeating dance steps.
- Candy Maker Roshan wins by timing the candy press.
- Doctor Roshan wins by completing the care sequence.
- Farmer Roshan wins by feeding the piggies.
- Boxer Roshan wins by bopping soft practice targets.
- Magician Roshan wins by tracking the bunny-fish.
- Painter Roshan wins by choosing and applying paint.
- Astronaut Engineer Roshan wins by fitting pipes.
- Racecar Driver Roshan wins by steering the tail-safe kart.
- Pop Star Roshan wins by performing the mapped dance directions.

“Boss fight” means a playful theatrical duet. There is no damage, defeat,
injury, hostile attack, health bar, timeout loss, or restart requirement. The
boss introduces changing cues and comic stage business, then becomes Roshan's
scene partner for the bow.

## Repository-visible source map

| Purpose | Repository-relative path |
| --- | --- |
| This authoritative hybrid guide | `CLAUDE_OPERA_HYBRID_LEVELS_2026-07-24.md` |
| Act I panoramas and construction kits | `assets_src/concepts/opera_jobs_2p5d_2026-07-24/` |
| Act II performance-finale keys | `assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/` |
| Finale generation record | `assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/PROMPTS.md` |
| Finale audit | `OPERA_JOB_HYBRID_FINALE_ART_AUDIT_2026-07-24.md` |
| Finale ledger | `audit/opera_job_hybrid_finale_ledger_2026-07-24.csv` |
| Finale contact sheet | `audit/opera_job_hybrid_finale_contact_sheet_2026-07-24.png` |
| Accepted outfit, implement, and state cards | `assets_src/concepts/opera_jobs_flat_2026-07-21/` |
| Exact older 576-card manifest | `audit/opera_job_flat_prototype_ledger_2026-07-21.csv` |
| Existing Opera boss models | `assets/art35/opera/opera_{dragon,phantom,maestro}.glb` |
| Existing formal stage model | `assets/art35/opera/opera_stage_apron.glb` |

The wide finale keys are composition and art-direction references. Rebuild
them as modular Mobile-safe 3D sets; do not use the whole image as one
interactive plane. The older 1024px cards remain the close-up references for
outfits, implements, readable states, and construction details.

## Required level rhythm

### 1. Career door and transformation

- Keep four career doors on each lobby floor.
- A door is the only normal entry point for its hybrid level.
- Play the existing costume transformation at the threshold.
- Voice the career and show the one primary interaction icon.
- Never require reading to choose or begin a level.

### 2. Act I — learn and rehearse

- Target approximately 60–90 seconds for a first play.
- Use the existing 2.5D district panorama and environment kit.
- Present the mechanic in three readable steps:
  1. one narrated demonstration with the visual pointer;
  2. one heavily guided child action;
  3. two or three independent repetitions with gentle correction.
- Keep the route left-to-right on one dominant gameplay plane.
- Pause forward progression while the active interaction is on screen.
- Wrong or late input creates a soft wobble, friendly voice hint, and another
  immediate chance. It must not spend progress or reset prior successes.
- Keep the current job-specific continuity locks, object counts, color
  mappings, species, and safety rules.

Act I should feel like visiting the actual job world. It is not a disguised
stage and should not show an audience, orchestra pit, or full proscenium.

### 3. Backstage threshold

The far-right completion landmark now opens into backstage rather than
returning directly to the lobby.

- Save a local resume checkpoint after the teaching section.
- Let music soften and preserve the child's completed Act I progress.
- Use a short curtain tunnel, costume mirror, prop table, and warm worklight.
- Place a large glowing stage-direction cue ahead.
- Voice: the audience is ready and Roshan will perform the job she just
  learned.
- A curtain wipe or lateral camera follow carries Roshan onto the stage.
- Do not insert a menu, results screen, loading choice, or second
  transformation.

If the app closes after this checkpoint, resume at the backstage threshold
with the same career outfit and no need to replay Act I.

### 4. Act II — theater performance

- Target approximately 45–75 seconds.
- Use a formal proscenium, visible curtains, footlights, scenic flats, and a
  quiet suggestion of an audience.
- Reuse the same input verb, targets, mappings, and corrective language from
  Act I.
- Present three to five performance beats, or the existing safe count where a
  job has a binding count such as seven candies or nine piggies.
- The boss may change timing, reveal order, lighting, or scenery. The boss
  must never invalidate the rule the child learned.
- Show progress as lit footlights, applause pearls, or filled medallion
  petals. Do not use boss health, damage ticks, red danger UI, or combat
  language.
- Missed cues loop back generously. The audience remains supportive.
- On the final beat, music resolves, the boss moves beside Roshan, and both
  bow during the curtain call.

### 5. Completion and return

- Award the career star only after the Act II curtain call.
- Save before transitioning back to the lobby.
- Return Roshan to the same career door.
- On replay, allow the whole level to run again. A later implementation may
  offer a non-reading visual shortcut to the backstage checkpoint, but the
  default remains the complete two-act story.

## Recurring floor bosses

Use the existing three Opera characters as recurring scene partners:

| Floor | Jobs | Recurring finale partner | Four-show arc |
| --- | --- | --- | --- |
| 1 — Lagoon Lights | Pastry Chef, Detective, Ballerina, Candy Maker | Curtain Dragon | Curious curtain troublemaker learns how each show works; after Candy Maker, proudly helps close the floor's revue |
| 2 — Starlight Balcony | Doctor, Farmer, Boxer, Magician | Shadow Phantom | Shy phantom experiments with light and concealment; after Magician, steps fully into the light for the bow |
| 3 — Grand Gallery | Painter, Astronaut Engineer, Racecar Driver, Pop Star | Midnight Maestro | Dramatic conductor challenges timing and sequence; after Pop Star, conducts the whole Opera finale |

The boss appears in every Act II on that floor. Each appearance needs one
clear entrance, one job-specific variation, one comic recovery, and one
curtain-call pose. The fourth job on each floor resolves the boss's small
story arc and unlocks the next floor or final celebration.

Do not create twelve new bosses. Do not redesign the existing three into
frightening villains. Keep their established silhouettes and toy-theater
materials.

## Twelve Act II contracts

All physical counts, orders, and color mappings below are binding in art,
guidance, interaction, recap, and QA.

| Job | Stage performance and learned verb | Boss variation | Binding finale continuity |
| --- | --- | --- | --- |
| Pastry Chef | Repeat the shown layer order, stir, and decorate the show cake | Curtain Dragon opens the recipe curtains and presents each layer call | One Roshan; one Dragon; three visibly different layer types; the live sequence may repeat types across its five calls; one bowl and one friendly oven |
| Detective | Search three curtain alcoves and follow the clue trail to the reveal | Dragon peeks from an alcove and accidentally exposes the next clue | One Roshan; one Dragon; exactly three searchable alcoves; magnifier cue; no clue hidden in decorative clutter |
| Ballerina | Watch and repeat the dance-tile sequence for three forgiving rounds | Dragon conducts the tile lights with tail and curtain flourishes | One Roshan; one Dragon; exactly four identities: coral shell, teal wave, plum ribbon, cream pearl |
| Candy Maker | Press inside the safe timing zone until seven show candies are complete | Dragon pulls the candy timing banner and cheers successful presses | One Roshan; one Dragon; one press; exactly seven completed candies; visible safe timing zone; resolves Floor 1 |
| Doctor | Follow the demonstrated care sequence for the same plush patient | Phantom briefly shades the next implement; a lantern reveal makes the correct step glow | One Roshan; one Phantom; exactly one coral five-armed starfish patient; stethoscope, thermometer, comfort/kiss cue, bandage, and one lantern |
| Farmer | Toss food to three groups of three passing piggies | Phantom slides moonlit scenery while lantern cues preserve readable timing | One Roshan; one Phantom; exactly nine piggies in three groups of three; exactly five filled food baskets; three empty picnic pads; no extra basket |
| Boxer | Complete friendly bubble-bop rounds against padded targets | Phantom animates the practice silhouettes and applauds clean timing | One Roshan; one Phantom; exactly three practice targets; soft bubble puffs; Roshan never strikes the boss |
| Magician | Track the bunny-fish through the same three-hat shuffle | Phantom adds harmless shadow doubles that disappear at reveal | One Roshan; one Phantom; one finned bunny-fish; exactly three hats in plum, teal, coral order; resolves Floor 2 |
| Painter | Choose the called color and paint the scenic sunrise in four calls | Maestro conducts the overhead color lights and raises the completed backdrop | One Roshan; one Maestro; exactly three stations in one row: plum, coral, cream; matching overhead lights |
| Astronaut Engineer | Fit straight, elbow, and ring pipe pieces, then open the bubble valve | Maestro conducts the socket lights in sequence | One Roshan; one Maestro; one each straight/elbow/ring piece and matching sockets; bubble-only rocket; no flame or smoke |
| Racecar Driver | Steer one tail-safe kart through broad gates and use bubble boost | Maestro conducts gate timing and moves scenic track flats | One Roshan; one Maestro; exactly one kart with Roshan's tail visible through the open channel; rounded track; no brands, numbers, fire, or smoke |
| Pop Star | Perform the existing mapped direction sequence with microphone cues | Maestro conducts the four lights, then joins the final chorus | One Roshan; one Maestro; exactly four tiles: plum-left, teal-up, cream-down, coral-right; resolves Floor 3 |

## Stage family and visual consistency

Build one reusable stage architecture per floor, then swap job dressing. This
keeps the Opera coherent while giving every career a distinct performance.

Shared architecture:

- rounded proscenium arch and deep side curtains;
- broad apron with an unobstructed gameplay strip;
- two or three shallow scenic-flat tracks;
- footlight or applause-progress sockets;
- boss entrance behind a side curtain or central scenic reveal;
- anchors for Roshan, boss, primary implements, pointer, camera, and bow;
- backdrop mount, overhead light bar, and low-cost audience silhouette band.

Floor palette:

- Floor 1: coral, warm cream, lagoon teal, berry-plum curtains, restrained
  brushed gold.
- Floor 2: moonlit aqua, lavender, deep plum, pearl cream, soft lantern gold.
- Floor 3: midnight navy, luminous teal, coral-magenta, cream, brighter
  conductor gold.

Job colors sit inside their floor family. Avoid realistic velvet, brass PBR,
wood grain, photographic texture, micro-ornament, or high-frequency noise.
Keep navy-purple outlines, aqua/lavender shadows, rounded silhouettes, and
large phone-readable material regions.

The Mermaid Roshan stained-glass piece remains a lobby identity feature. Do
not remove, cover, or replace it while revising the stage architecture.

## Suggested 3D structure

```text
OPERA_HYBRID_<JOB>
  ACT1_WORLD
    GEO_Playable
    GEO_Landmarks
    GEO_Scenic
    BG_Mid
    BG_Far
    COLLISION
    ANCHORS
  BACKSTAGE_LINK
    GEO_CurtainTunnel
    GEO_PropTable
    Anchor_Checkpoint
    Anchor_StageCue
  ACT2_STAGE
    GEO_FloorStage
    GEO_JobDressing
    GEO_ScenicFlats
    BG_Audience
    FX_ReferenceOnly
    COLLISION
    ANCHORS
```

Recommended Act II anchors:

```text
Anchor_RoshanStart
Anchor_BossEntrance
Anchor_BossHome
Anchor_Primary_01
Anchor_Primary_02
Anchor_Primary_03
Anchor_Pointer
Anchor_Camera
Anchor_CurtainCall_Roshan
Anchor_CurtainCall_Boss
```

Only active targets require collision. Scenic flats, audience silhouettes,
particles, foliage, and curtain dressing must not become physics bodies.

## Camera and transition

- Keep the Act I side-on camera and the stage camera on compatible screen
  scales so Roshan does not suddenly become tiny.
- Backstage may bend the route shallowly in Z, but do not rotate the child
  through a disorienting 180-degree turn.
- Land Act II at a stable side-on or gentle three-quarter view.
- Keep Roshan, the active implement, the boss cue, and the next visual pointer
  visible together.
- No camera shake. A small eased push-in is allowed for the final bow.
- On Speedy, use baked lighting, opaque scenic flats, sparse particles, and
  no expensive real-time audience or curtain simulation.

## Runtime migration from the current fifteen entries

The current runtime stores twelve job bits and three separate boss bits in
`m.opera_stars`. Save compatibility is binding. Do not reindex the existing
job bits and do not remove or rename the save key.

Preserve this legacy bit layout:

```text
Floor 1 jobs: bits 0,1,2,3    legacy floor marker: bit 4
Floor 2 jobs: bits 5,6,7,8    legacy floor marker: bit 9
Floor 3 jobs: bits 10,11,12,13 legacy floor marker: bit 14
```

Migration behavior:

1. Keep each career door attached to its existing job bit.
2. Remove the three boss entries from normal selectable act flow, but retain
   their bit positions as compatibility floor-resolution markers.
3. Completing a hybrid level sets its job bit only after the Act II curtain
   call.
4. When all four job bits on a floor are set, also set the legacy marker bit
   for that floor. This unlocks the next floor without invalidating old saves.
5. Treat an already-set legacy marker as completed floor resolution. Never
   clear it.
6. Count and display twelve career stars, not fifteen entries. Marker bits
   must not inflate visible progress.
7. `opera_done` becomes true when all twelve job bits are set; also normalize
   all three legacy marker bits at that point.
8. Preserve `opera_progress` as a derived count of the twelve job bits.
9. Existing saves with completed separate bosses remain completed. Existing
   saves with four completed jobs but no marker should receive the marker on
   load or the next Opera entry.
10. Keep the old medallions as decorative floor-completion celebrations or
    non-reading replay/resume portals only. They must not be required to earn
    a thirteenth, fourteenth, or fifteenth visible star.

Add new checkpoint state with defaults; never remove existing keys. A safe
shape is one per-career phase value (`act1`, `backstage`, or `complete`) plus
the current job identifier. If the exact checkpoint schema changes, document
the defaults and prove old saves still load.

The current internal `boss_hp` field may remain temporarily during mechanical
extraction, but it must not be shown as health and should be renamed to a
neutral beat counter when the hybrid implementation stabilizes.

## Implementation sequence

Build one vertical slice before multiplying the structure:

1. Pastry Chef door and existing costume transformation.
2. Pastry district Act I with demonstration, guided action, and rehearsal.
3. Backstage checkpoint and seamless curtain transition.
4. Lagoon Lights stage with the accepted Pastry finale composition.
5. Curtain Dragon's layer-call variation and shared curtain call.
6. Save, quit at backstage, resume, completion, replay, and lobby return.
7. Mobile camera/readability/performance capture.

After Pastry passes, extract reusable hybrid flow and stage-shell code. Then
build the remaining Floor 1 careers, validate the Dragon arc and legacy bit-4
unlock, and only then proceed upstairs.

Do not rewrite all twelve jobs at once. Preserve the existing live mechanics
and move them into the two-act structure one job at a time.

## Acceptance gates

A hybrid career fails review if any of the following is true:

- Act I does not teach the exact input used in Act II.
- The child returns to the lobby between learning and performing.
- The finale replaces the job mechanic with generic combat.
- Boss health, damage, danger, injury, fail, or punitive restart language is
  visible.
- A missed input removes prior progress.
- The boss vanishes instead of joining the curtain call.
- A binding count, order, color map, patient species, or safety feature drifts.
- The level requires reading.
- Roshan, the current target, or the pointer becomes too small at phone size.
- Act I reads as a literal stage or Act II reads as an unrelated minigame.
- The finale art falls below 4.5/5 for silhouette, consistency, readability,
  modelability, or continuity.
- A new texture exceeds 1024px longest side without a documented POT reason.
- The Speedy tier exceeds its transparent-overdraw or physics-body budget.

Required proof for each completed job:

- Act I wide gameplay capture;
- backstage checkpoint capture;
- Act II wide gameplay capture;
- one close interaction-state capture;
- curtain-call capture;
- first-play and replay behavior;
- old-save load and new-save resume behavior;
- Mobile renderer performance at the actual camera;
- automated probe coverage for completion without passive victory.
