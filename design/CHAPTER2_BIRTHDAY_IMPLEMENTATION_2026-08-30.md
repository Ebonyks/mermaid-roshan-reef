# Chapter 2 Birthday Implementation Contract

> **Production-spine supersession (owner direction, 2026-08-30):** this staged
> thirteen-career implementation record is historical. Current authority is
> `CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md`, including the exact
> order `[6, 0, 3, 10, 2, 13, 11, 1]`, Candy Maker's candied-strawberry cake
> finish, late Detective candle discovery, and persistent submilestone masks.

> **Roster supersession (owner direction, 2026-08-30):** the final Chapter 2
> may use no more than eight careers. See
> `CHAPTER2_EIGHT_CAREER_STORY_OPTIONS_2026-08-30.md` for the selected roster,
> ranked story uses, and proposed sequential spine. The thirteen-career mask
> documented below describes the current staged implementation only and must
> be reduced in one coordinated code/save/probe pass before integration.

This document is retained only as the superseded implementation history for
the post-tutorial birthday-prep draft. The production spine named above is the
sole current Chapter 2 authority. The useful surviving story note is that the
Ember King is the crash actor, while his child-scale son is the emotional
bridge and foreshadow for the later Ember Fortress story.

## Progression

The Dust Bunny defeat is the only Chapter 2 handoff boundary. It cleans the
castle, disables Day One, and opens the Opera House with exactly acts 0, 1, 2,
and 3 as non-star tutorials. Tutorial wins grant skills but do not write
`opera_stars` or count as party pieces.

After the four skills, the Detective plot action is available only in the
Library. It reveals the rainbow candle inside the magic storybook and keeps
it unlit. The Ballerina plot action is available only in the Stuffie Playroom,
where Roshan teaches the stuffed animals to dance and play together. These are
plot-triggered uses of learned characteristics, not general room abilities.

The Detective and Stuffie Ballet are also the first two party contributions.
The remaining eleven live Opera careers can then be completed in any order.
Chef Roshan bakes a gigantic three-tier birthday cake and Astronaut Roshan
builds a little rocket specifically to light the candle. The candle remains
unlit throughout discovery and preparation. When all thirteen live bits are
present and the Main Hall party starts, the rocket creates the one explicit
Chapter 2 ignition beat: a large, phone-readable rainbow flame appears above
the cake. A little ember child is spotted watching the celebration; moments
later, the Ember King crashes the party once and carries away the whole glowing
rainbow candle because he wants it for his own birthday party. The cake, rocket,
stuffies, and every other completed preparation remain safe. His son leaves a
northern Fire Mountain clue and provides the child-readable emotional bridge;
the King's birthday motive seeds a later story about what his own party needs.
The King remains the named crash actor. The party table remains assembled after
this event, which has no fail state.

## Stable party mapping

`scripts/chapter_two_party_plan.gd` is the pure-data source for this table.
The `act_index` values are the existing live Opera save bits; retired slots 4,
9, and 14 are never reused.

| Act | Career | Castle room | Party contribution | Cross-chapter seed |
| ---: | --- | --- | --- | --- |
| 0 | Chef | kitchen | bake the gigantic birthday cake | warm cake |
| 1 | Detective | library | find the unlit candle and whose-day clue | storybook clue |
| 2 | Ballerina | playroom | teach the stuffies to dance and play together | ribbon step |
| 3 | Candy Maker | kitchen | wrap party sweets | sweet trail |
| 5 | Doctor | playroom | repair stuffie guests | gentle hands |
| 6 | Farmer | dining_room | bring party food | garden path |
| 7 | Boxer | playroom | lead active party games and hang the sash | brave wave |
| 8 | Magician | opera_hall | perform for non-dancers | magic ribbon |
| 10 | Painter | craft_room | paint Main Hall decor | sunrise sign |
| 11 | Astronaut | mermaid_pool | build the little candle-lighting rocket | north star |
| 12 | Racer | movie_lounge | bring guests through transit | rainbow road |
| 13 | Pop Star | opera_hall | prepare song and microphone | echo song |
| 15 | Nursery | bubble_bath | welcome a quiet baby corner | warm welcome |

## Main Hall centerpiece states

`ChapterTwoPartyTable2D` stages the authored results rather than showing only
an abstract checklist. It reuses the approved Opera rocket and career icons,
the approved castle table/banner, and the code-native rainbow candle. The
runtime inventory contained no usable cake texture, so
`ChapterTwoGiantCake2D` fills that specific gap as a new true-2D, code-native
three-tier cake without modifying any protected art. The sequence is:

1. Preparation: gigantic cake and rocket appear when their career bits are
   earned; the found candle remains unlit.
2. Party start: cake sparkles and the rocket lights the large rainbow flame.
3. King crash: the King takes the whole candle for his own birthday; its
   picture dims and its centerpiece disappears, while cake and rocket remain.

The timing preserves those visual beats: 2.4 seconds for the ignition before
the Ember son scout announcement, then another 1.8 seconds before the King
crash. Leaving the Main Hall safely defers the crash until a live re-entry.

## Additive save contract

The new fields are additive and normalized by `ChapterTwoDirector`:

```text
chapter2_party_piece_mask
chapter2_party_started
chapter2_ember_scout_seen
chapter2_ember_king_crashed
chapter2_ember_son_seen
chapter2_candle_lit
chapter2_candle_taken
chapter2_story_complete
```

`chapter2_party_piece_mask` is restricted to the 13-bit live mask `0xBDEF`.
Detective and Ballerina bits are derived from their completed plot milestones.
Party start requires all thirteen bits and deterministically lights the candle.
A valid, one-shot crash extinguishes the local lit state and heals
`chapter2_candle_taken` true because the King carries the still-glowing candle
away for his own birthday party. `chapter2_candle_lit` describes the local Main
Hall prop, so it clears once the candle is gone. Son-seen and story-complete heal true from a valid King
crash; malformed early combinations heal false. Existing `opera_stars`,
`ember_found`, `ember_progress`, and `ember_done` remain independent.

Completed Chapter 2 remains represented in the save for continuity, but
`main.gd` exposes it as inactive to Castle route selection so the finished
chapter cannot suppress normal freeplay forever.

## Probe obligations

`scripts/probe_chapter2.gd` covers the boss boundary, non-star tutorial skill
handoff, live room gates, unlit discovery, the four causal career jobs,
Stuffie Ballet, 13-bit order-independent contributions, early party/crash
rejection, party-only rocket ignition, visible giant cake/rocket/candle state,
one-shot candle theft with the King's birthday motive and son metadata,
malformed-save healing, and save round trip. Godot runtime validation must use
the project’s required 4.7.2-stable binary.
