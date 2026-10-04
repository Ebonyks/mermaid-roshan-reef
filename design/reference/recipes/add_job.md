# REC-ADD-JOB: Add Job

Status: `SUPPORTING_CURRENT` planning recipe. It routes current authority; it grants no content commission, generation budget, acceptance or release beyond the owner instruction and binding contract.

Intent: `INT-ADD-JOB`. Example: add a bakery job. Minimum input: the job.

Default: Opera career row for a permanent job, through the live extension path at implementation head; an isolated venue scene only for an approved-scope prototype. Platform architecture is a proposal until its services exist. The thematic room is proposed from the castle rooms and confirmed by the owner.

## Read first

- `AGENTS.md`
- `audit/MASTER_AUDIT_2026-08-09.md`
- `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`
- `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`
- `design/05_DOC_LEDGER.md`
- `design/AUDIT_DEVELOPMENT_CONTRACT.md`
- `design/reference/strengths.json`
- `audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md`
- `docs/handoffs/codex_job_platform_architecture_2026-09-30/ARCHITECTURE.md`
- `docs/handoffs/codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md`
- `docs/handoffs/codex_visual_design_language_2026-09-30/ROSHAN_APPEARANCE_ANALYSIS.md`
- `scripts/opera_house.gd`
- `scripts/save_state.gd`
- `scripts/castle_career_routes.gd`
- `assets/audio/voices/VOICE_MANIFEST.md`
- `design/animation/ROSHAN_MOVEMENT_LANGUAGE.md`
- `audit/minigame_art_quality_2026-09-05/opera_native_coverage_followup.md`

Rules: `DL-AUTH-05` through `DL-AUTH-07`, `DL-PLAN-01` through `DL-PLAN-06`, and all affected child, interaction, save, medium, motion/cinematic, audio and acceptance rules. Consult live canonical findings; do not copy historical counts or superseded engine/3D directions.

Bound strengths (accepted first; candidates explicitly remain candidates): `S-01` (accepted), `S-02` (candidate), `S-03` (candidate), `S-12` (candidate), `S-13` (candidate).

Pattern references are the hash-bound seed entries in the strengths register and the gold-star reference patterns (`GS-*` in `design/reference/gold_star.json`, a candidate reference); no promoted PAT/EX exemplar is implied. Owner-decision defaults `ODR-LOOP-Q1`–`Q8` are operating defaults, not answers. The recorded Roshan decisions `ODR-ROSHAN-IDENTITY`, `ODR-ROSHAN-IRIDESCENT`, `ODR-ROSHAN-Q12`–`Q16` retain their exact scopes.

## Expand

1. Write a job card from the job itself: a one-sentence premise, a proposed thematic castle room with the reason it fits (or the Opera freeplay venue), four to six beats grouped Teach / Play / Twist / Bow where every beat is a different verb with a visible, truthful change that stays, Roshan's travel and contact for each beat, the exact voice line and pointer for each objective, the help ladder, the reward and the imp's role. Every beat requires the previous beat's saved state and the child's one-finger action; idle input, a timer or a demonstration never finishes a beat or awards progress. Do not copy another job's verbs or payoff. The planner's job_card lists the fields; it stores no answer for any job.
2. Inspect live registries before editing: scripts/opera_house.gd ACTS/LIVE_ACT_INDICES/ACTIVE_STAR_MASK/ACTIVE_ACT_COUNT; opera_competition.gd CAREERS; opera_career_world_2d.gd PHASES/FINALE_START/PHASE_STATIONS/GOAL_PROPS; opera_mastery.gd CAREERS/RULES; opera_performance_overlay.gd CAREER_COLORS; opera_hotspot_catalog.gd EXPECTED_PHASES/SPECS/ASSET_META. Compute phase, finale, station, voice, hotspot, probe and checkpoint counts from the approved card and the live extension contract; Teach / Play / Twist / Bow groups beats and does not fix the phase count.
3. Allocate the next save bit from the live namespace, including retired (tombstone) bits; the planner's save_allocation section derives the next bit, both masks, the retired bits and every clamp site at the current head. Add new keys with defaults and keep every existing reef_save.json key.
4. Update every opera_stars clamp the planner lists (load, write and the shared normaliser), the range and both mask/count authorities, the per-job normaliser and checkpoint cleanup. Test the new bit's round trip, external merge through the shared normaliser, tombstones and reward persistence. Re-read the sites at implementation head.
5. Inventory reuse first: the chosen room's approved backgrounds and props, related careers' props, and the approved Roshan identity. For Roshan the identity anchor is `roshan_base.png` or a base-world atlas; career art is a costume or pose reference only and `roshan_sprite.png` is never bound (it is retired, ODR-ROSHAN-Q16). The tail is iridescent; name the light state of the exemplar (ODR-ROSHAN-IRIDESCENT, ODR-ROSHAN-Q12). Name each missing piece of art; Codex builds only those, with provenance, licence, atlas-gate and typography entries. Check native resolution at shipping scale before any replacement; no redraw for novelty and no 3D.
6. Voice: bind the exact line, speaker and key to each objective. New provisional lines use the Parler candidate, selector and master pipeline in assets/audio/voices/VOICE_MANIFEST.md; the legacy Kokoro path is not used for new lines. Route the folder and prefix in audio_director.gd and the audio quality category; never imitate or alter family recordings. Music: propose the job's score in assets_src/audio/music/area_music_scores.json and tools/build_area_music.py EXPECTED_IDS with the scripts/probe_audio.gd REQUIRED_AREA_MUSIC entry, or a justified byte-identical reuse.
7. Plan reachability and lifecycle: castle_career_routes.gd ROOM_ACT_INDICES and probe EXPECTED_ROOM_ACTS; opera_stage_paths.gd PATHS/STATION_NAV; stage_inventory.json; living_world_catalog.gd row/EXPECTED_STAGE_COUNT; backdrop PALETTES or compliant screen tiles. Keep Day One and the locked Chapter Two roster separate unless commissioned.
8. Extend trusted probe coverage and pin counts: probe_opera, probe_opera_2d, probe_opera_nursery, probe_living_world, probe_audio and gesture quality. Cover correct/wrong/passive/random/repeat/save/re-entry/back/focus loss, Roshan travel/contact and the contest rematch. Use existing rosters unless explicitly authorized to add high-risk CI entries.
9. Run the focused and full gates, audit_stage_pathfinding --check, audit_opera_roshan_animation and a voice-per-phase review. Codex builds the phase boards at two aspects; deliver them and the exact dev APK for human, device, child and owner review. 5/5 is a target that needs owner acceptance in context (DL-VIS-07), never an inferred score. Include impact, ledger and licence rows; merge only exact-head green work to dev; release only on the owner's shorthand through the promote workflow.

## Variety

- Teach / Play / Twist / Bow groups the beats; live two-act specialist contracts keep their shape. Every beat is a different verb with a truthful, persistent change.
- Combine a familiar verb with a new tool and a new visible payoff; compare against the last two jobs and do not repeat their payoff.
- Competitive careers end in the DL-INT-14 imp contest: the imp stays hidden until the final act; one head-to-head contest uses a real skill of the job; the imp may win; his win plays a beat of at most 2 s and restarts the contest at once with nothing lost; he works only while the child plays; each rematch slows him or raises his target down to a floor. The contest-only restart scope still awaits owner confirmation. Learning careers invert the contest (one deliberate, silly mistake per round, never mean).

## Owner touchpoints

1. May this permanent job use this premise and thematic room? Default: wait: nothing permanent is added until the owner answers; an approved-scope practice prototype may continue. Trigger: New permanent career (DL-PLAN-01: silence grants no reserved permission).
2. Does the costume look right? Default: wait for the owner's look at Codex's costume board; meanwhile reuse the approved Roshan identity (roshan_base.png anchor) with her iridescent tail. Trigger: Named visual acceptance for a new costume; a generation budget must already be authorized.

## Build and check

Claude writes specifications, audits and study reports; Codex builds code and every image, board and capture. An owner's explicit request in the current task may change who implements non-image work; images keep the CLAUDE.md exception (an explicit owner request for one specific image covers only that image). A plan generated by `tools/plan_prompt.py` executes nothing.

- python -B tools/audit_document_authority.py
- python -B tools/audit_development.py --base auto
- Changed GDScript: python -m gdtoolkit.parser plus tools/lint_inference.py; exact Godot 4.7.2-stable import/full scripts/ci.sh and exact-head green branch CI before integration. No high-risk workflow edits without explicit task authority.
- Evidence lanes: machine; Mobile 1280x720 and wide-phone visual; older Android phone and M11 device; private child observation; owner review. Missing lanes remain open.
- Preserve original assets/book, assets/audio/voices and assets/characters/friends; license each new asset; true Canvas 2D, Mobile/Speedy, one finger, voice plus pointer, no punitive loss, no passive award, additive saves.

## Learn

- Add lessons with a named write_back target, references_used and strengths_observed to this task impact record.
- Capture owner corrections as source-bound decision entries; never infer owner answers from defaults.
- Update this recipe only from a concrete omission or accepted lesson, retaining revision history; propose a check/reference when a recurrence can be reproduced.
- Publish source-bound evidence and report implementation, machine verification and outstanding visual/device/child/owner gates separately.

## Revision and served prompts

- 2026-10-03: V1 implemented from the self-improvement handoff and current repository authorities.
- 2026-10-03: Cold-start review exposed missing child-controlled baking/retrieval, inherited phase counts, enlarged-background readiness and imprecise clamp labels. Added the ordered candidate chain, computed counts, source-bound gap and exact shared-normaliser descriptions.
- 2026-10-03: Review fixes (Claude): removed the stored bakery answer and baseline numbers; the planner derives save facts and gives a job card to design; reserved decisions wait for the owner; imp contest stated as DL-INT-14 says; Parler named for new voice lines.
- No completed served prompt or runtime/owner acceptance is claimed.
