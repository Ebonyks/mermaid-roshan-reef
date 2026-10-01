# Reference plan: from 200 dated audits to 14 reference documents (2026-09-30)

**Status:** `PROPOSED / CANDIDATE` plan prepared by Claude. Companion to
[STALENESS_AUDIT.md](STALENESS_AUDIT.md); executed through [README.md](README.md).
Line ranges were read at `dev` `6fc2f48e` and are guides: re-locate by heading
before extracting. Items marked *(nv)* were not verified by the sweeps.

## 1. Rules for every reference

- **Two anchors never merge into references.** The rulebook
  ([design 06](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md)) holds
  every rule; references link to `DL-*` IDs and never restate them. The
  [master audit](../../../audit/MASTER_AUDIT_2026-08-09.md), the finding
  register and the change log hold status and evidence.
- **References hold durable knowledge only:** decisions with dates,
  measured thresholds, protocols, patterns, known pitfalls and rejected
  approaches. No commit hashes, CI run IDs, durations or hand-copied counts;
  counts come from generated status or the job catalogue.
- **Where they live:** `design/reference/REF_<DOMAIN>.md`, next to the design
  reference shelf of the
  [refinement handoff](../codex_master_audit_refinement_2026-09-30/README.md).
  Ledger state 🟣 until the owner accepts a reference, then 🔵 (never 🟢: they
  hold no rules).
- **Each reference starts with** a one-paragraph scope, its sources (old path,
  new archive path) and the date of its last re-verification.

## 2. The fourteen references

| # | Reference | Absorbs | Do not carry over |
|---|---|---|---|
| R01 | `REF_OPERA_CAREERS.md` | 11 root `OPERA_*` audits and specs (§3) | 52/53-phase and 19/27-mode counts, coordinates, lobby layout, rival GLBs, old scores. The step-by-step build recipe belongs in the job playbook (refinement Stage J) |
| R02 | `REF_CASTLE.md` | 11 castle documents | Sprite3D depth values, 3344×941 coordinates, dated counts, V2/V3 inventories |
| R03 | `REF_DAY_ONE.md` | 2 pool audits; extracts from the persona runs and both Day One handoffs | File:line anchors; modelled timings presented as measured |
| R04 | `design/10_CHAPTER_REFERENCE_LIBRARY.md`, extended | Chapter 2 decision history and story-option rationale | Dialogue scripts; career order from drafts |
| R05 | `REF_WORLDS.md` | 13 Sky Lagoon, Ember and Northern documents | Camera and card-centre numbers; 3D or procedural tree plans |
| R06 | `REF_ART_STYLE_AND_PRODUCTION.md` (built from the 2D sections of `ART_STYLE_GUIDE.md`) | 10 art documents | Blender, Meshy, GLB and rig sections; old texture channel; per-pass score tables |
| R07 | `REF_ANIMATION.md` | 3 animation documents | 2.5D staging and rig work; `design/animation/*` stays the binding home |
| R08 | `design/reference/CANON.md` (refinement WP-4) | 2 Lamba documents | Rigs, recordings |
| R09 | `REF_AUDIO_VOICE.md` | `MIC_SPELLS.md`; extracts from the voice manifest and ledgers | Loudness rules (already `DL-SND-*`); `MUSIC_AUDIT_2026-08-09.md` stays as is |
| R10 | `REF_INTERFACE.md` | 7 interface and touch documents | Sprite3D and Camera3D touch contracts, screen counts |
| R11 | `REF_ENGINES_AND_ENCOUNTERS.md` | 11 engine, race, combat and boss documents | Spline, Jolt and 3D arena geometry; `HIT_ENGINE.md`, `MEDALS.md` and the boss design documents stay |
| R12 | `REF_CINEMATICS.md` | 9 cinematic documents | Pose reuse and compositing (now forbidden), clip hashes, acceptance claims |
| R13 | `REF_PERFORMANCE_DEVICE.md` (built from the Lenovo Tab M11 protocol) | 4 documents | 3D lights and the lighting lab; old-head timings |
| R14 | `REF_PROCESS_AND_RELEASE_HISTORY.md` | `RELEASE_GATE_VERDICT_2026-08-05.md`; the archive index | Run IDs, commit narration |

### Outlines with sources

**R01 Opera careers.**
1. Authority and counts: design 06 `DL-INT-07` to `DL-INT-14`; counts from the job catalogue, never typed.
2. Architecture and data: imp-contest `CURRENT_STATE_ANALYSIS.md` L17-44; `OPERA_CAREER_COMPETITION_SYSTEM` L55-59; `OPERA_STAGE_INTERACTION` L6-32; two-act performances L8-16.
3. Interaction contract: widget input audit L26-32 ("trickle by assist, not by payout") and L135-142 (no precision gates; a four-year-old reacts in 600–900 ms); minigame quality audit L144-155; quality overhaul L47-63; ingredient direction L3-26; mechanics re-audit L58-60 (watch, your turn, response, assist).
4. Timing and pacing: act pacing L3-10; mechanics re-audit L62-80; two-act L95-105; framing audit L239-241 and L339-350 (pull-back ladder).
5. Rival, imps and contests: imp-contest analysis L46-112; two-act L16, L30-40, L78-80; competition system L123-127 (imp identity lock); design 06 `DL-INT-14`.
6. Persistence: mechanics re-audit L919-927; two-act L125-129.
7. Art and scene: minigame art audit L108-133 (eight-step protocol, no averaging, pose sheets are not loops, ImageGen checkerboard trap); mechanics re-audit L84-111; framing audit L21-103 and L380-432; overhaul L65-79 (4×4 atlas contract).
8. Voice and narrative: narrative audit L28-40 and L291-316 (5–12-word lines, key word first or last; ritual versus emotional lines); mechanics re-audit L906 (an empty `vo` is not silence).
9. Audit methods and pitfalls: mechanics re-audit L15-19, L46-52, L950-956; feedback audit L13 and L372-391; playability audit L5, L119, L127, L133 (correct play must beat mashing); minigame quality audit L9-21 (rubric).
10. Open defects still true in code (Chapter 2 ballet goals, wrong-choice crumbs, ballet hold, spotlights, no free-play checkpoints, Geologist art and voice reuse) — move to findings, not the reference.

**R02 Castle.**
1. Medium and resolution: 2.5D layer audit L89-149 (native-2K rule, source precedence); `castle_rooms_25d.gd` header.
2. Door language and guidance: design 07 L5-66; door handoff L86-130, L213-335, L492-540 (painted-geometry rule, one highlight, squint test).
3. Travel and pathfinding: stage pathfinding protocol L1-65; its README L9-41.
4. Object interactions: native interactions v4 audit L62-176 (six rules, rejection taxonomy); interaction audit L91-131; dust-bunny spawn guide L5-9 and L55-71; Dream House L3-12.
5. Ambient life: living-world audit L5-8 and L260-311 (two quiet accents plus one idle surprise; 16–22 s delay; no rewards).
6. Art QA: transparency audit L16-44 and L348-417 (four-pass method, CI guards); v4 audit L178-247; pool integration spec L30-101.
7. Current status pointers: pathfinding inventory; Door Guidance v2 status.

**R03 Day One** (and R04 for Day Two).
1. Canon and owner decisions: rebuild handoff L88-102; design 07 L22-47.
2. Child model and attention: playthrough PROTOCOL L30-47 (1.5–3 s reaction to a new prompt; silence over 5 s loses her); player-experience handoff L348-359 (voice and pointer within 1.0 s; re-prompt at 5 and 12 s; 3:1 agency to passive); run 16 L79-98 (attention reservoir, safe stops); rebuild handoff L144-161.
3. Voice, pointer and touch: rebuild handoff L367-393.
4. Room activities: dirty-pool audit L8-68 (three causal one-finger tasks; scale numbers); pool integration spec L30-101 (no global wash; aqua or lavender shadows; desaturate props 15–25%); player-experience handoff L237-245 (pitfalls).
5. Grand Puff: rebuild handoff L195-318 and L461-535; boss encounter visual audit L61-258 (evidence ladder; one hazard plus one progress cue; reusable presentation contract).
6. Save and resume: rebuild handoff L395-414 and L546-562.
7. Chapter 2 (R04): production spine L9-118; cake progression L10-51; lawn finale L14-20 and L156-239; story options L36-46.
8. Art review: Day Two art library report L5-13 and L114-127; minigame art audit L112-123.
9. Audit method: player-experience handoff L27-96 (16 personas, convergence, Stage 0 rule); rebuild handoff L59-66 (evidence levels).

**R06 Art style and production.**
1. Authority: design 02 L14-26; style guide L5-29 without its precedence item 4.
2. Visual DNA and palette: style guide L337-421; design 02 L28-44.
3. Identity and protected sources: style guide L69-80 and L425-460; design 02 L277-293.
4. Motif families and castle grammar: style guide L98-336.
5. Readability and composition: design 02 L46-56; style guide L515-524 and L604-615.
6. 2D medium, lanes and motion budgets: design 02 L91-148; living-card language L25-80.
7. Technical gates: design 02 L220-236.
8. Light on painted art: lighting audit L288-290, L365-381, L404-454, L562-591 (headroom spec; one shadow hue per zone).
9. Generation and new-art protocol: object generation log L18-34 and L492-655 (rule IDs); style guide L617-673; aesthetics plan L173-191; repair plan L58-91; design 02 L260-273.
10. Scoring and acceptance: scoring governance L19-33; human review audit L23-31 (seven caps); design 02 L240-258 and L363-383.
11. Audit tooling: visual audit tool L42-103, L297-330, L444-467.
12. Rejected approaches: design 02 L312-325; Pacific Northwest prototype audit L29-42 and L102-120; style audit L20-27, L264, L340-341.
13. Non-binding backlog: aesthetics plan L83-157.

**R09 Audio and voice.**
1. Protected recordings and speakers: voice manifest L93-96 (add Faron); `CLAUDE.md`; design 06 `DL-SND-05`, `DL-SND-11`.
2. Musical language: music audit L126-166 (Roshan motif; sparkle cadence is not the fanfare; no lyrics).
3. Coverage, ownership and ambience: music audit L29-45, L67-94, L275-306.
4. Mix, loudness and delivery: music audit L168-201; voice manifest L15-21; audio quality audit L29-35 (grades).
5. Voice pipeline and resolver: voice manifest L3-73; repetition audit L18-31.
6. Writing Roshan's lines: contextual voice ledger L6-18 (3–12 words, one thought per breath).
7. Provenance and acceptance: music audit L308-401; voice manifest L32-51; audio quality audit L85-107.

**R12 Cinematics.**
1. Rules and the `DL-CIN-16` exception: design 02 L329-359; design 06 `DL-CIN-01` to `DL-CIN-16`; `AGENTS.md` story-clip section.
2. Direction: direction protocol L29-152; opening brief V2 L14-33.
3. Quality gate: temporal integrity protocol L25-68, L110-147, L290-376.
4. Generator handoff: master formula L10-265; retrospective L11-16 and L66-127.
5. Continuity and endpoints: continuity protocol L15-162; footage analysis L50-169.
6. Location and identity locks: location authority audit L9-20 and L40-49; overnight recut audit L47-73 and L142-195.
7. Failure taxonomy: footage audit GH2-01 to GH2-14 (L11-166); media inventory L62-68; full-frame process audit L105-137.
8. Encoding and runtime: cartoon video pipeline L78-102 (Theora quality 6, GOP 64, 720p decode ceiling); the clip manifest.
9. Status vocabulary: media inventory L33-40; master formula L235-242.

**R13 and R14 Performance and process.**
1. Device and budgets: Lenovo protocol L23-66 (9 mm fingertip is about 49 design px; a desktop pass is not a device pass); design 06 `DL-PERF-*`.
2. Measurement lanes: Lenovo protocol L68-174 (emulator invalid for GPU and thermal).
3. Hotspots to re-verify: tablet performance evaluation L44-239 (no frame cap; debug APK; never-hidden fade rect); alpha polish audit L51-88 (VRAM versus disk).
4. Typography: font audit L93-200.
5. Child-play guardrails: dungeon difficulty audit L20-27 and L179-214; release gate verdict L19-41 (no one-move dead ends); audit repair L22-47 (ten failure classes).
6. Branching and APK channels: workflow branching L23-106; Android release (after correcting it).
7. Backup (with its real status) and security (link only).
8. Document governance: design 00 L130-166; ledger L1-41; the archive index.

R05, R07, R08, R10 and R11 follow the same shape; their sources are listed in
§3 and their scopes in the table above.

## 3. Classification of the documents

Paths are at the repository root unless prefixed `audit/`, `design/` or
`docs/`; `.md` is omitted. † marks a document holding a rule that must move to
design 06 first (STALENESS_AUDIT section 6).

**Keep as is (76).** `AGENTS`, `CLAUDE`, `ASSET_LICENSES`, `SECURITY`,
`BACKUP`, `WORKFLOW_BRANCHING_2026-07-18`, `MUSIC_AUDIT_2026-08-09`,
`BALLERINA_PARTY_REBUILD_2026-08-09`, `OPERA_ACT_PACING_2026-07-25`†,
`HIT_ENGINE`, `MEDALS`†, `STUFFIE_COMPANIONS`, `VISUAL_AUDIT_TOOL`; the three
active Codex work orders (Day One player experience, Day One rebuild, door
highlight); `audit/MASTER_AUDIT_2026-08-09`, the finding register and the
change log; `audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30`, the Day Two art library
report, `audit/animation/README`, the stage pathfinding protocol and README;
`design/00` to `design/10`, templates, animation languages, Northern chapter;
boss splash language, bunny boss rebuild, Boxer project, development contract;
Chapter 2 cake, spine and lawn finale; Fairy Conservatory; the 09-05 to 09-30
career records (Tree Book, two-act shows, Geologist, Teacher, Racer, Painter);
the Grok formula and continuity protocol, Day One cinematic plan, video
handoffs README, visual repair plan; `docs/ANDROID_RELEASE` (after correction),
the direction and temporal protocols, the Grok series navigation; and every
`docs/handoffs/*` packet (hash-recorded).

**Keep as evidence (72).** `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03` (owner
decisions §10, §16, §17 — copy them into the decision register);
`CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26` (linked from packets);
`OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01` (named in a provenance
manifest); `audit/OPERA_MECHANICS_REAUDIT_2026-09-05`, `audit/MASTER_AUDIT_2026-08-26`,
`audit/BOSS_ENCOUNTER_VISUAL_AUDIT_2026-09-05`, the combat tutorial capture
index, `audit/FONT_TYPOGRAPHY_AUDIT_2026-08-30`, the Grok footage and overnight
recut audits, the voice timelines README, the Opera regeneration audit; the 18
Day One playthrough files; the 18 minigame art quality files (hash-recorded);
`design/MINIGAME_ART_AUDIT_2026-09-05` and the two DaVinci documents; 21 review
documents inside `assets_src/` packets.

**Absorb, then archive (85).**
- R01: `OPERA_2D_REBUILD`†, `OPERA_CAREER_COMPETITION_SYSTEM`†, `OPERA_STAGE_INTERACTION`†, `OPERA_NURSERY_JOB_12`†, `OPERA_INGREDIENT_INTERACTION_DIRECTION`†, `OPERA_FEEDBACK_AUDIT`, `OPERA_FRAMING_PACING_ANIMATION_AUDIT`, `OPERA_LOGICAL_REBUILD_SPEC`, `OPERA_MASTER_PACKAGE`, `OPERA_MINIGAME_QUALITY_AUDIT`, `OPERA_QUALITY_OVERHAUL`.
- R02: `CASTLE_ROOM_LED_CODEX_IMPLEMENTATION`, `CASTLE_DREAM_HOUSE`, `CASTLE_INTERACTION_AUDIT`, `CASTLE_NATIVE_INTERACTIONS_V4_AUDIT`, `FABLE_CASTLE_ANIMATION_INTERACTIVITY_HANDOFF`, `FABLE_CASTLE_2K_REGEN_HANDOFF`, `FABLE_CASTLE_ITEM_STYLE_AUDIT`, `CASTLE_PERSONAL_BANNER_STYLE_AUDIT`, `audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT`, `CASTLE_DUST_BUNNY_SPAWN_GUIDE`†, `STUFFIE_PLAYROOM_RESCUE_GUIDE`.
- R03: `audit/DAY_ONE_DIRTY_POOL_STYLE_AUDIT`, `audit/DAY_ONE_POOL_NATURAL_INTEGRATION_SPEC`.
- R05: the four Sky Lagoon reductive, resolution, congruency and living-card documents; the three Sky Lagoon art, quality and style audits†; the animal art work order and two `docs/audits` animal documents; the two Ember Fortress concept audits; `OBJECT_PLACEMENT_AUDIT`.
- R06: `ART_STYLE_GUIDE`† (becomes R06), `ART_SCORING_GOVERNANCE`, `ART_HUMAN_REVIEW_AUDIT`, `ART_NON5_MAX_POTENTIAL_CRITIQUE`, `ART_ASSET_LIBRARY`, `ASSET_AUDIT`, the background-flats and water-FX work orders, `assets/OBJECT_GENERATION_AUDIT_LOG`, `gen2/generated/ANALYSIS`.
- R07: `CODEX_IMP_ANIMATION_HANDOFF`, `CODEX_ROSHAN_SPRITE_REGENERATION`, `ROSHAN_SPRITE_CUTOFF_AUDIT`.
- R08: the two Lamba takeover documents.
- R09: `MIC_SPELLS`.
- R10: `FABLE_INTERACTION_HANDOFF`, `TOUCH_CENTRIC_REVERSIBLE_HANDOFF`, `TOUCH_AUDIT`, `OPERA_WIDGET_INPUT_AUDIT`, the two Claude Fable UI handoffs, `MENU_UI_SYSTEM_AUDIT`.
- R11: `MINIGAME_ENGINES`, `RACE_ENGINE`, `RACE_FEEL_WORKORDER`, `KART_FEEL`, `PHYSICS_ENGINE`, `COMBO_SYSTEM`†, `IMP_AI`, `DUST_BUNNY_BOSS`, `BOSS_CONVERGENCE_DECISION`, `COMBAT_DIFFICULTY_AUDIT`, `COMBAT_TUTORIAL_CODEX_ASSETS`.
- R12: `audit/GROK_HANDOFF_RETROSPECTIVE`, `audit/CINEMATIC_MEDIA_INVENTORY`, `design/GROK_FOOTAGE_ANALYSIS_AND_ENDPOINT_HANDOFF`, `design/GROK_LOCATION_GEOMETRY_AUTHORITY_AUDIT`, the two Grok Day One movie handoffs *(nv: delivery status)*, `docs/OPENING_CINEMATIC_ART_DIRECTION_BRIEF_V2`, `docs/OPENING_CINEMATIC_FULL_FRAME_PROCESS_AUDIT`, `docs/CARTOON_VIDEO_PIPELINE`.
- R13: `audit/LENOVO_TAB_M11_EMULATION_PROTOCOL` (becomes R13), `audit/TABLET_PERF_EVALUATION`, `LIGHTING_SHADER_AUDIT`, `LIVING_CARD_DESIGN_LANGUAGE`.
- R14: `RELEASE_GATE_VERDICT`.

**Archive now (119).** 3D art batches and conversion manifests; the
2026-07 art audits, batches, prompts and remediation passes; the old texture
channel (`NB_*`, `TEXTURE_SOURCE_AUDIT`, `FULL_TEXTURE_REGEN_*`); 3D-era Codex
art work orders; cel-shading, colour consistency, 2.5D lighting, visual design
and CC0 replacement documents; superseded castle audits (Pearl art, V2, V3,
Dream House 2D repair, Fable 2.5D layer, main-hall prop compatibility, visual
polish intervention, Sprite3D lighting continuity); the Claude Opera 3D,
hybrid and 2.5D handoffs; the flat, 2.5D and hybrid Opera art audits; the
superseded Opera redesign, gimmick, request, census, logical-rebuild and
widget documents; the exploration, widget-concept, narrative and playability
documents; the 2026-08-03 animation handoffs with their review kit (move the
kit with its handoff); the 3D character pipeline, customization, runbook, NPC
work order and the three `docs/ROSHAN_*` model documents; Ember, Sky Lagoon
and Northern Blender handoffs and audits; Pacific Northwest prototypes,
Northern asset batches, dungeon audits, `WORLD_MAP`, the Zelda work order;
`LIVING_WORLD_STAGE_AUDIT`, `REEF_FLORA`, `REEF_REDESIGN_AUDIT`; the Chapter 2
bible, party-role and plot drafts and the two superseded Chapter 2 design
documents; the 2026-08 boss and combat art handoffs; `AUDIT_3_0`,
`GAME_AUDIT_v3_49`, `CONVERSATION_AUDIT`, `AUDIT_REPAIR`, `AUDIT_UPGRADE`,
`CODE_AUDIT_2026_07`, `DESIGN_3_0`, `ALPHA_POLISH_AUDIT`,
`HOURLY_INTEGRATION_AGENT`; camera, 2.5D redesign, Jolt, water physics and
cozy-gap audits; the superseded opening-cinematic regeneration audit and the
generation-two kit audit. Lift the few lessons the art, performance and
process sweeps identified (for example the VRAM-versus-disk measurement and
the ten audit-repair failure classes) into R06, R13 and R14 as you go.

**Delete candidates (2).** `audit/day_one_pool_lighting_image_audit_2026-08-22`
(tool output; its ledger note miscounts) and `tools/out/lighting_image_audit`
(default output of `tools/audit_lighting_images.py`; stop tracking
`tools/out/`). Owner approval required.

## 4. Root cleanup: 196 files to 6

- **Stay at the root:** `AGENTS.md`, `CLAUDE.md`, `ASSET_LICENSES.md`,
  `SECURITY.md`, `BACKUP.md`, and the frozen
  `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` (plus the
  non-Markdown castle depth manifest).
- **Archive destination:** `audit/archive/docs/<domain>/<same filename>`, so a
  filename cited in prose can still be found. Add `!/audit/archive/` to
  `.gitignore`; `audit/` already has `.gdignore` and is excluded from export.
- **Coordinated moves (edit their referrers in the same change):**
  `WORKFLOW_BRANCHING` to `docs/ops/` (AGENTS and the task index); `MUSIC_AUDIT`
  to `design/domains/audio/` (task index); `VISUAL_AUDIT_TOOL` to `docs/tools/`
  (`scripts/ci.sh` comment, `tools/visual_audit_spec.json`); Ballerina and act
  pacing to `design/domains/opera/`; `HIT_ENGINE`, `MEDALS`,
  `STUFFIE_COMPANIONS` to `design/domains/systems/` (`CLAUDE.md` names two —
  owner-gated); the three active Codex work orders to `docs/handoffs/`; the
  birthday review and Opera regeneration requests to `audit/archive/evidence/`.
- **Links and generators to update with the moves:**
  `design/10_CHAPTER_REFERENCE_LIBRARY.md` (three links),
  `design/chapters/NORTHERN_ICE_WORLD.md`, the review-kit README, the master
  task index, `tools/audit_castle_item_style.py`, `tools/build_full_regen_audit.py`,
  the `tools/claude_ember_*.ps1` scripts, and about 25 code comments.
