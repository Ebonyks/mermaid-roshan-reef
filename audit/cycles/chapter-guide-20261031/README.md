# Chapter-guide refinement review

Status: `IN_PROGRESS / OWNER_REVIEW_PENDING` under MA-DOC-010. This implements the chapter-development slice of the [published handoff](../../../docs/handoffs/codex_chapter_guide_2026-10-31/README.md), from exact integration baseline a0bb2cf4691631a534e210a5fb60fd227213322f.

## Review entry

- [Master planning entry and chapter board](../../MASTER_AUDIT_2026-08-09.md#0-planning-entry)
- [Chapter guide](../../../design/09_CHAPTER_DEVELOPMENT_GUIDE.md), [brief template](../../../design/templates/CHAPTER_BRIEF_V1.md) and [generated recipe](../../../design/reference/recipes/new_chapter.md)
- [Canon](../../../design/reference/CANON.md), [single chapter map](../../../design/chapters/CHAPTER_MAP.md) and [book authority/mismatch queue](../../../design/reference/BOOK_SOURCES.md)
- [As-built chapter director contract](../../../design/03_TECHNICAL_ARCHITECTURE.md#chapter-directors)
- [Rumi cold-start proposal](../../../design/chapters/RUMI_MERMAID_WORLD_BRIEF_20261031.md) and [trial learning log](COLD_START_TRIAL.md)
- [Impact, verification and acceptance gaps](../../../design/audit_impacts/chapter-guide-refinement-20261031.json)

## Package disposition

| Package | Implemented scope | Remaining evidence |
|---|---|---|
| CG0 | [Exact-head measurements](BASELINE.json), overlap with MA-DOC-006 schema/backfill and MA-DOC-007 R04/R08/W2 recorded in impact | Measurements describe their exact baseline, not a runtime re-audit |
| CG1 | Real fresh-save traversal requirement, own-room story binding gate with two injected faults, reward/voice-before-clip requirement, all in guide/brief/recipe | MA-PLAY-005 fresh-save traversal remains its own repair; no gameplay closure |
| CG2 | Checked/generated canon slice, exact identity/book hashes, original 15 conflicts plus later Grand Puff care/source conflict, latitude and voice scope | Open questions stay explicit; no new voice or character art acceptance |
| CG3 | Five chapter entries, carried state, aliases, open threads, blocked sources and master routes | Names/thread marks are provisional; runtime Rumi chapter uncommissioned |
| CG4 | Verified director/save/activity/clip/voice touch list; current ReefMain forwarding corrected from handoff interpretation | Chapter 3 trusted-roster gap and target Mode Platform remain unbuilt |
| CG5 | Evidence ladder and generated master chapter board | No chapter newly gains PLAYABLE_REVIEW, phone or owner acceptance |
| CG6 | Stable task types; 51 receipt spans preserved verbatim with [source hashes](moved_spans.json), three index fault controls | Broader consolidation remains MA-DOC-007 work |
| CG7 | Source-backed September story decisions and current owner corrections appended; existing decisions preserved | [August 30 source-attribution gap](STORY_BACKFILL_NOTES.md); no fabricated historical answer |
| CG8 | Fresh-context trial uses the Rumi book world selected by the owner; proposal and learning log | Owner review, plus a future commissioned runtime autonomy trial |

## Evidence boundaries

The owner’s current correction makes the book control narrative mismatches and selects Rumi’s latest authored book for this planning trial. The October 17/18 Lantern Night rewrite remains a proposal. Protected originals, voice permissions, saved progress, child rules, demo freeze and release authority retain their own scopes. No game feature, image, audio, high-risk instruction or workflow changes in this task.

Implementation, machine verification and external acceptance are reported separately in the impact. The master audit remains **UNSATISFIED**. Owner review of this guide/proposal and the founding attribution source are required before MA-DOC-010 closure; passing gates does not supply either.

## Publication gate blocker

The documentation/source checks pass. The full game run exits 1 after all 82 probes: 79 exit 0; Opera 2D, Chapter 2 and New Game exit 1. Both child-process deadline failures pass later sequential rechecks with their original limits. The Opera geologist room-finale separation assertion repeats in a final standalone run after all other probes exit. Runtime/protected/high-risk sources are unchanged from a0bb2cf4. No probe, limit or runtime is repaired or relaxed here.

The [machine receipt](REGRESSION_RESULT.json) binds every literal native log, exact roster, recheck result, headless visual skip and execution limitation. The original full-suite failure remains FAIL. Full [regression log](verification/full_ci.log) and [standalone Opera failure](verification/chapter-guide-opera-serial-recheck.log) are included.

AGENTS.md requires full validation to print all-OK before any commit. Normal publication is blocked pending an explicit owner exception for a documentation-only review branch, or a separate runtime repair. A review-branch exception would not integrate red work into dev or accept the game. MA-DOC-010 remains IN_PROGRESS; the book source-attribution and owner-review gaps remain separate.
