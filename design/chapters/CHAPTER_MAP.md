# Chapter map

Status: SUPPORTING_CURRENT. Generated from chapter_map.json by tools/design_reference.py. This is the single home for chapter aliases, carried state and open threads. Numbers/names and owner marks retain provisional handoff defaults; code and save keys keep their names. A scoped commission does not commission a whole ending.

Read the [canon](../reference/CANON.md), [book source](../reference/BOOK_SOURCES.md), [guide](../09_CHAPTER_DEVELOPMENT_GUIDE.md) and [chapter board](../../audit/MASTER_AUDIT_2026-08-09.md#chapter-board).

## CH-1

**Chapter 1: Day One**

| Field | Value |
|---|---|
| Aliases | Day One |
| Premise | Roshan arrives at the dusty Pearl Castle and cleans it room by room: Bubble Bathroom (tutorial), Sparkle Pool, Stuffie Room and Art Room. The boss door then glows and she faces Grand Puff alone. |
| Authorization | Existing game and owner-directed Day One clips (2026-09-23); acceptance remains open. |
| Implementation | BUILT; acceptance open |
| Evidence rung | COMMISSIONED |
| Entry save condition | A new game: start menu, then the opening story clip. |
| End state | Grand Puff is beaten (day_one_giant_dust_bunny_boss_defeated). The transformation clip shows the family joining; the Rainbow Friend then follows Roshan. The Day Two transition bridges into the birthday. |
| Next-chapter obligation | Chapter 2 starts from the cleaned castle; Grand Puff is a friend, not a defeated enemy; the Rainbow Friend is present afterwards. |
| Code entry points | director: scripts/day_one_director.gd (DayOneDirector, extends RefCounted); save: DayOneDirector.serialize_state()/restore_state(); typed forwarding properties keep mutable state on ReefMain. SaveState merges additive day_one_* keys.; rooms: DayOneDirector.ROOM_ORDER: bathroom, pool, stuffie, art; story_clips: assets/cinematics/day_one_story/story_clips.json under DL-CIN-16; transition: scripts/day_two_transition_2d.gd (DayTwoTransition2D) |
| Trusted probes | [scripts/probe_day_one_director.gd](../../scripts/probe_day_one_director.gd); [scripts/probe_day_one_integration.gd](../../scripts/probe_day_one_integration.gd); [scripts/probe_day_one_story_clips.gd](../../scripts/probe_day_one_story_clips.gd) |
| Diagnostic/unrostered probes |  |
| Sources | [AGENTS.md#day-one-story-clips-between-scenes-owner-decision-2026-09-23](../../AGENTS.md#day-one-story-clips-between-scenes-owner-decision-2026-09-23); [design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md); [scripts/day_one_director.gd](../../scripts/day_one_director.gd); [scripts/rainbow_friend_follower.gd](../../scripts/rainbow_friend_follower.gd) |

## CH-2

**Chapter 2: Day Two, Roshan's birthday party**

| Field | Value |
|---|---|
| Aliases | Day Two, Chapter 2, Chapter Two, the birthday chapter |
| Premise | Eight ordered jobs prepare the birthday, followed by Roshan’s special dress and the lawn encounter. The rocket lights the separate candle and the King takes it; the preparations remain safe. Prince/scout staging is a scoped lawn-finale candidate. |
| Authorization | Chapter 2 spine incorporates owner direction through 2026-08-30; no new full-chapter commission is invented here. |
| Implementation | BUILT; MA-PLAY-005 (P0) IN_PROGRESS |
| Evidence rung | COMMISSIONED |
| Entry save condition | Day One complete (Grand Puff beaten), reached through the Day Two transition. |
| End state | chapter2_story_complete and chapter2_candle_taken are saved; the lawn finale plays; the free-play career cards appear. |
| Next-chapter obligation | The candle is gone and the Ember King has it. Chapter 3's reveal requires both saved facts. |
| Code entry points | director: scripts/chapter_two_director.gd (ChapterTwoDirector, extends RefCounted); save: ChapterTwoDirector.serialize_state()/restore_state()/normalise_save_patch; typed forwarding properties keep mutable state on ReefMain. Preserve namespaced story fields and separate global Opera progress.; plan: scripts/chapter_two_party_plan.gd; career order [6, 0, 3, 10, 2, 13, 11, 1]; voice: scripts/chapter_two_voice_catalog.gd; activity_handoff: OperaHouse.start with ChapterTwoDirector.opera_config_overrides (see MA-PLAY-005 reproduction) |
| Trusted probes | [scripts/probe_chapter2.gd](../../scripts/probe_chapter2.gd); [scripts/probe_chapter2_farmer_resume.gd](../../scripts/probe_chapter2_farmer_resume.gd); [scripts/probe_chapter2_lawn.gd](../../scripts/probe_chapter2_lawn.gd); [scripts/probe_alpha_milestone_save.gd](../../scripts/probe_alpha_milestone_save.gd) |
| Diagnostic/unrostered probes |  |
| Sources | [design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md](../../design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md); [design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md](../../design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md); [design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md](../../design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md); [design/FASHION_DESIGNER_ROSHAN_2026-10-06.md](../../design/FASHION_DESIGNER_ROSHAN_2026-10-06.md) |

## CH-3

**Chapter 3: The Fairy Conservatory**

| Field | Value |
|---|---|
| Aliases | Chapter 3, Fairy Conservatory |
| Premise | After the Ember King takes the candle, a wing-chime in the Main Hall wakes the moonflower relief. Roshan travels Castle, Rainbow Skyway, Butterfly House, Butterfly World, Fairy Pond and back. The 2026-09-30 prototype develops the faerie half of restoring the castle's magic: tree care, fruit harvest, fruit preparation, butterfly picnic, a gentle flower shooter, bringing faerie magic home. |
| Authorization | Scoped route and 2026-09-30 prototype only; no full ending/second-world commission. |
| Implementation | ROUTE BUILT (scoped); faerie restoration PROTOTYPE (isolated candidate); ENDING NOT COMMISSIONED |
| Evidence rung | COMMISSIONED |
| Entry save condition | chapter2_story_complete and chapter2_candle_taken. Legacy access: opera_done, or older saves with galaxy, bwdone or fairyskin. |
| End state | Not built. The second world and the full castle-restoration ending are outside the prototype's commission. |
| Next-chapter obligation | Unknown until the owner sets the ending. |
| Code entry points | director: none; route: scripts/arena/fairy_conservatory_door_2d.gd, scripts/arena/fairy_conservatory_handoff_2d.gd; prototype: scripts/fairy_restoration_prototype.gd; save: chapter3_fairy_door_revealed, chapter3_fairy_door_opened, chapter3_fairy_mission_started, read and written as ReefMain fields by scripts/save_state.gd |
| Trusted probes |  |
| Diagnostic/unrostered probes | [scripts/probe_fairy_conservatory_route.gd](../../scripts/probe_fairy_conservatory_route.gd); [scripts/probe_fairy_conservatory_handoff.gd](../../scripts/probe_fairy_conservatory_handoff.gd); [scripts/probe_fairy_restoration.gd](../../scripts/probe_fairy_restoration.gd) |
| Sources | [design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md](../../design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md); [design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md](../../design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md) |

## PROPOSED-LANTERN-NIGHT

**Rumi mermaid world (number/title provisional)**

| Field | Value |
|---|---|
| Aliases | Lantern Night beneath the Pool (later rewrite proposal, not selected book title) |
| Premise | The latest illustrated book, Here I Am!: Roshan’s first-line wish, reflection test, under-pool neighbourhood, Duri rescue, bathhouse feast, foam/bubble teamwork and community answer. Song Night and the still-missing candle follow that book. |
| Authorization | Owner 2026-10-31 selects this book world for the first planning trial; runtime is uncommissioned. |
| Implementation | Book exists at exact immutable source; planning proposal only, no game route or save schema. |
| Evidence rung | PLANNED |
| Entry save condition | Not set. |
| End state | Not set. |
| Next-chapter obligation | Roshan has spoken up and returned to the pool/home; candle still missing. No new magical power or forced Ember-story resolution. |
| Code entry points |  |
| Trusted probes |  |
| Diagnostic/unrostered probes |  |
| Sources | [design/reference/BOOK_SOURCES.md](../../design/reference/BOOK_SOURCES.md); [docs/handoffs/codex_rumi_book_revision_2026-10-17/GAME_INTEGRATION.md](../../docs/handoffs/codex_rumi_book_revision_2026-10-17/GAME_INTEGRATION.md); [docs/handoffs/codex_rumi_book_revision_2026-10-17/WORLD_BIBLE.md](../../docs/handoffs/codex_rumi_book_revision_2026-10-17/WORLD_BIBLE.md); [docs/handoffs/codex_rumi_book_revision_2026-10-17/README.md#5-owner-questions](../../docs/handoffs/codex_rumi_book_revision_2026-10-17/README.md#5-owner-questions); [design/chapters/RUMI_MERMAID_WORLD_BRIEF_20261031.md](../../design/chapters/RUMI_MERMAID_WORLD_BRIEF_20261031.md); [audit/cycles/chapter-guide-20261031/COLD_START_TRIAL.md](../../audit/cycles/chapter-guide-20261031/COLD_START_TRIAL.md) |

## PLANNING-NORTHERN

**(planning) Northern / Ice World**

| Field | Value |
|---|---|
| Aliases | Northern, Ice World |
| Premise | A cozy Northern restaurant Roshan helps run as a chef, with pictured customer orders, built around the existing Northern art family. |
| Authorization | Planning only; no runtime chapter commission. |
| Implementation | PLANNING (owner direction 2026-09-05); runtime not commissioned |
| Evidence rung | PLANNED |
| Entry save condition | Not set; owner-reserved. |
| End state | Not set; owner-reserved. |
| Next-chapter obligation | The Northern branch says not to invent a mandatory continuation of the Ember story. |
| Code entry points | region: scripts/arena/northern_kingdom.gd (contains spatial migration debt) |
| Trusted probes | [scripts/probe_northern.gd](../../scripts/probe_northern.gd) |
| Diagnostic/unrostered probes |  |
| Sources | [design/chapters/NORTHERN_ICE_WORLD.md](../../design/chapters/NORTHERN_ICE_WORLD.md) |

## Carried state

| Item | Existing state | Chapter must decide | Sources |
|---|---|---|---|
| CS-COMPANIONS | Baby Eagle and the stuffed-friend companions follow Roshan. | Whether companions are present, where they stand and whether any activity uses them. | [STUFFIE_COMPANIONS.md](../../STUFFIE_COMPANIONS.md); [scripts/companion.gd](../../scripts/companion.gd) |
| CS-RAINBOW-FRIEND | The Rainbow Friend (the rainbow dust bunny freed from Grand Puff's dusty shell) follows Roshan through the castle after Day One. | Presence and staging in the chapter's places. | [scripts/rainbow_friend_follower.gd](../../scripts/rainbow_friend_follower.gd) |
| CS-OUTFITS | Recurring characters keep earned outfits across the game (ODR-FASHION-PERSISTENCE-20261006). | Which outfits the chapter shows, unlocks or requires; never strip an earned look. | [scripts/fashion_designer.gd](../../scripts/fashion_designer.gd); [scripts/save_state.gd](../../scripts/save_state.gd) |
| CS-MEDALS | Bronze, silver and gold rankings. | Whether chapter activities award medals; the quiet-medal answer (ODR-MEDALS-QUIET-20261018) is on an unmerged branch. | [MEDALS.md](../../MEDALS.md); [scripts/medal_system.gd](../../scripts/medal_system.gd) |
| CS-CAREER-MASKS | The global career mask and chapter story masks are separate. | Its own story progression keys; it never redefines the global mask or reuses a retired identity (design 10 section 1). | [scripts/save_state.gd](../../scripts/save_state.gd); [scripts/chapter_two_director.gd](../../scripts/chapter_two_director.gd) |
| CS-FREE-PLAY-CARDS | After Chapter 2, career cards are available in free play. | Whether the chapter's activities join free play after the story, and how story and free-play progress stay separate. | [scripts/chapter_two_director.gd](../../scripts/chapter_two_director.gd); [scripts/start_menu.gd](../../scripts/start_menu.gd) |
| CS-GUIDE-VOICE | Exact objective voice plus visual guidance, within current guide and protected-voice permissions. | Name exact speaker/cue and pointer at every objective. A new narrator/performer is not inferred from missing audio. | [scripts/audio_director.gd](../../scripts/audio_director.gd); [design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md) |

## Open threads

| Thread | Continuity obligation | Owner mark and authority | Sources |
|---|---|---|---|
| TH-CANDLE | The Ember King carried the lit rainbow candle away for his own birthday. Who gets it back, and how, is unresolved. | OWNER_RESERVED; Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [design/10_CHAPTER_REFERENCE_LIBRARY.md#1-current-continuity-sources](../../design/10_CHAPTER_REFERENCE_LIBRARY.md#1-current-continuity-sources); [docs/handoffs/codex_rumi_book_revision_2026-10-17/README.md#5-owner-questions](../../docs/handoffs/codex_rumi_book_revision_2026-10-17/README.md#5-owner-questions) |
| TH-CASTLE-MAGIC | Restoring the castle's magic has a faerie half (the prototype) and an unbuilt second world and full ending. | OWNER_RESERVED (ending and second world); DELEGATED (activities inside an approved premise); Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md#1-commission-and-boundaries](../../design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md#1-commission-and-boundaries) |
| TH-DISGUISE | Fashion is to teach later disguise through dress-up games; the disguise mission has no chapter home. | OWNER_RESERVED (mission premise); DELEGATED (dress-up mechanics inside an approved chapter); Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [design/reference/owner_decisions.json](../../design/reference/owner_decisions.json) |
| TH-RAINBOW-FRIEND | The Rainbow Friend's role after Day One beyond following Roshan. | DELEGATED (presence and staging as a follower); OWNER_RESERVED (voice, personality or a story role); Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [AGENTS.md#day-one-story-clips-between-scenes-owner-decision-2026-09-23](../../AGENTS.md#day-one-story-clips-between-scenes-owner-decision-2026-09-23) |
| TH-EMBER-FAMILY | The Ember King's son, the Prince, is kind and conflicted about his father; he and the scout appear in Chapter 2 (chapter2_ember_son_seen, chapter2_ember_scout_seen). No later role is set. | OWNER_RESERVED; Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md](../../design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md); [scripts/chapter_two_director.gd](../../scripts/chapter_two_director.gd); [docs/handoffs/codex_master_audit_refinement_2026-09-30/seed/canon_seed.json](../../docs/handoffs/codex_master_audit_refinement_2026-09-30/seed/canon_seed.json) |
| TH-NORTHERN-STORY | The Northern chapter's main story role, entry and ending. | OWNER_RESERVED; Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [design/chapters/NORTHERN_ICE_WORLD.md#2-planning-promise-and-open-scope](../../design/chapters/NORTHERN_ICE_WORLD.md#2-planning-promise-and-open-scope) |
| TH-LANTERN-NIGHT | Whether/how the designated Rumi book becomes a playable chapter; current owner commissions the first planning trial only. Later Lantern Night names and story remain a distinct proposal. | OWNER_RESERVED; Provisional handoff Q2 default; major changes remain reserved by DL-PLAN-01. | [docs/handoffs/codex_rumi_book_revision_2026-10-17/README.md#5-owner-questions](../../docs/handoffs/codex_rumi_book_revision_2026-10-17/README.md#5-owner-questions) |

## Blocked sources

| Source | Limit | Evidence |
|---|---|---|
| BS-IKO-IKO | Iko Iko is used for the Day Two story only once its game-use rights are confirmed. | design/reference/owner_decisions.json (ODR-POPSTAR-SONG-20261018) |
| BS-NORTHERN-CONCEPT | The owner-confirmed July 29 Northern forest concept exists only on the rescue branch; no licence row was found for it. | assets_src/concepts/northern_forest_concept_2026-07-29.png at f07027af253badd8d37f0b3b6aeedb8cbab7336f, SHA-256 db0cc66cc90551774ffe28809c095658324634ccf8f27c5742b7735da489208d |
| BS-LEARNING-DECISIONS | The owner's learning-session answers (book question card, quiet medals, one new guide voice) are recorded only on an unmerged branch. | origin/claude/angry-roentgen-6a8f7b at 7b851b3d0be0dd83652751ca5c3085fc4b36b6b8 |
| BS-RUMI-BOOK | Only byte-identical source text is now on the reference shelf; selected art remains at c3e0da51. Book acceptance, source regression failure and runtime rights/voice/art checks stay separate. | design/reference/book_sources/SOURCES.json |
| BS-RUMI-PRIVATE-CANON | Rumi identity is approved private canon for private playtesting only under its existing IP hold; public marketing/merchandising is not cleared. This trial does not expand source rights. | assets_src/characters/rumi_2026-08-22/PROVENANCE.json |
