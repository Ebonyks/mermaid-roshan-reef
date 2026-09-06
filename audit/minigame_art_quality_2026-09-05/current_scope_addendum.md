# Minigame art audit — current scope addendum

Status: **IN PROGRESS / 4.5 standard not met.** This addendum separates the preserved art candidate based on `775ceee1` from the gameplay candidate reconciled onto `8aab459ceea61c204aa943fb1d82e0cc62ea0ba0`. It does not convert historical screenshots or source-art scores into acceptance of a new build.

The [detailed art report](../../design/MINIGAME_ART_AUDIT_2026-09-05.md) contains the fifteen-career score table, picture-game findings, animation review, weak-asset registry and replacement protocol. Those subjective baseline composition scores range from 2.7 to 4.2; no reviewed Opera family is certified at 4.5. The retained brush reuse, pose-playback containment, lap flags and picture-game layout/payoff repairs belong to that preserved art candidate. They have not been silently folded into the separately reconciled gameplay candidate.

## Corrections when reading the earlier report

- The two typography fixture failures described there are historical. The reconciled candidate passes those forty tests, with one skipped.
- Grand Puff's rebuild is now integrated in `dev`. Its earlier art hashes/captures must be refreshed before grading the current encounter; describing it as merely parallel work is outdated.
- The first complete gameplay reconciliation run reached all 78 trusted probes and failed only the unique-career music check because Teacher reused Nursery's cue. Teacher now has a distinct music cue and the focused audio probe passes. The corrected complete local gate now passes all 78 trusted probes; the [gameplay reconciliation report](../../design/OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md) owns that status.
- The art registry has 56 records and is **not an exhaustive live-asset inventory**. The follow-up source scan found 346 unique literal resource paths, 97 dynamic loading sites and 24 minigame/adaptor source candidates without exact registry records. These are coverage leads, not proof of live reachability or quality scores. See [coverage inventory](missing_coverage.md) and its [data](missing_coverage.json).

## Reuse review before more generation

Luna visually inspected fourteen existing assets. The [reuse report](reuse_candidates.md) and [data](reuse_candidates.json) record the observed comparisons. No complete direct replacement family was found for the weak garden props.

Painted terrain flowers and two story-prop flowers are promising individual sources, but tall rooted plants, flower clusters and single decorative blossoms do not automatically fit the current 228-by-228 mature-state slots or supply five distinct mature results. A polished fairy-boss sprout belongs to a different growth role; a cracked-rock seed cannot represent the garden's seed. The farmer asset labeled as a carrot depicts a framed pig and is not a valid semantic substitute. Existing watering-can and carrot alternatives do not close the source-quality gaps. These findings rule out careless substitutions; they do not forbid adapting the layout around suitable approved art after a deliberate review.

## Next bounded replacement batch

The named missing set is a consistent sprout plus five mature flowers, a clean watering can with readable pour/contact orientation, and a correctly shaped carrot. Preserve the original files and compare candidate identity, painted finish, edges, phone readability, contact/motion, scene ownership, consistency and technical integrity separately. Approved equivalents should still be reused when their role and geometry fit.

First repair layout, anchors and state ownership using existing art. For a source replacement, keep the source, prompt, references, hashes and rejection history; verify actual alpha and clean contours before import. Capture every required idle/demo, contact, changed-state, payoff and settle state in the Mobile renderer. A different Sol/Luna reviewer must reject any applicable dimension below 4.5 or an unresolved blocking defect. A good source illustration cannot compensate for a weak runtime state, and a numerical average cannot erase a critical weakness.

The pending request for explicit permission to use non-destructive Python cutout cleanup remains unanswered. Rejected painted-checkerboard candidates remain outside runtime. Native background-resolution gaps require separate source work; cutout cleanup cannot repair them. Owner, child and device acceptance remain distinct from automated checks.
