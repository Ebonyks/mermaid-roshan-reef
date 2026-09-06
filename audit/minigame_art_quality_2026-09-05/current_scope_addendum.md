# Minigame art audit — current scope addendum

Status: **IN PROGRESS / 4.5 standard not met.** Original art captures came from the `775ceee1` worktree. Repairs were reconciled onto core gameplay base `f4a5de33` and published as `9df00099`, whose exact-head remote CI passed. The current follow-up merges dev parent `6d7c5e85` (navigation plus family-evening expansion) and adds eleven phase-specific pose holds. Source hashes and dated manifests distinguish these candidates; historical screenshots do not accept a new build.

The [detailed art report](../../design/MINIGAME_ART_AUDIT_2026-09-05.md) contains the fifteen-career score table, picture-game findings, animation review, weak-asset registry and replacement protocol. Those subjective baseline composition scores range from 2.7 to 4.2; no reviewed Opera family is certified at 4.5. The retained brush reuse, pose-playback containment, lap flags and picture-game layout/payoff repairs are included in published `9df00099`. The new configured-phase and Garden follow-ups have separate source/evidence boundaries.

## Corrections when reading the earlier report

- The two typography fixture failures described there are historical. The reconciled candidate passes those forty tests, with one skipped.
- Grand Puff's rebuild is now integrated in `dev`. Its earlier art hashes/captures must be refreshed before grading the current encounter; describing it as merely parallel work is outdated.
- The first complete gameplay reconciliation run reached all 78 trusted probes and failed only the unique-career music check because Teacher reused Nursery's cue. Teacher now has a distinct music cue and the focused audio probe passes. The corrected complete local gate now passes all 78 trusted probes; the [gameplay reconciliation report](../../design/OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md) owns that status.
- The art registry has 62 records and is **not an exhaustive live-asset inventory**. The follow-up source scan found 259 literal resource paths, 97 dynamic loading sites and 24 minigame/adaptor source candidates without exact registry records. These are coverage leads, not proof of live reachability or quality scores. See [coverage inventory](missing_coverage.md) and its [data](missing_coverage.json).

## Reuse review before more generation

Luna visually inspected fourteen existing assets. The [reuse report](reuse_candidates.md) and [data](reuse_candidates.json) record the observed comparisons. No complete direct replacement family was found for the weak garden props.

Painted terrain flowers and two story-prop flowers are promising individual sources, but tall rooted plants, flower clusters and single decorative blossoms do not automatically fit the current 228-by-228 mature-state slots or supply five distinct mature results. A polished fairy-boss sprout belongs to a different growth role; a cracked-rock seed cannot represent the garden's seed. The farmer asset labeled as a carrot depicts a framed pig and is not a valid semantic substitute. Existing watering-can and carrot alternatives do not close the source-quality gaps. These findings rule out careless substitutions; they do not forbid adapting the layout around suitable approved art after a deliberate review.

## Next bounded replacement batch

The named missing set is a consistent sprout plus five mature flowers, a clean watering can with readable pour/contact orientation, and a correctly shaped carrot. Preserve the original files and compare candidate identity, painted finish, edges, phone readability, contact/motion, scene ownership, consistency and technical integrity separately. Approved equivalents should still be reused when their role and geometry fit.

First repair layout, anchors and state ownership using existing art. For a source replacement, keep the source, prompt, references, hashes and rejection history; verify actual alpha and clean contours before import. Capture every required idle/demo, contact, changed-state, payoff and settle state in the Mobile renderer. A different Sol/Luna reviewer must reject any applicable dimension below 4.5 or an unresolved blocking defect. A good source illustration cannot compensate for a weak runtime state, and a numerical average cannot erase a critical weakness.

The pending request for explicit permission to use non-destructive Python cutout cleanup remains unanswered. Rejected painted-checkerboard candidates remain outside runtime. Native background provenance remains a separate fixed-scene review question; it is not a blanket regeneration mandate, and cutout cleanup cannot establish native background detail. Owner, child and device acceptance remain distinct from automated checks.

## Follow-up asset tracing on the navigation reconciliation

Luna traced these six exact asset dependencies; the parent independently verified every SHA-256 against the current worktree. This is an additional capture queue, not six newly accepted registry records. The registry now contains 62 records after adding these six exact asset sources; incomplete coverage and all missing candidate reviews remain open. Runtime scene scores remain unassigned until current captures exist.

| Exact asset | SHA-256 | Live role | Required capture states |
|---|---|---|---|
| `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png` | `d788366485da7a19958c34278bd05a4a4977be39582a9134d3e63a394d601143` | Bathroom filled tub and pool swimmer | bathroom visible; pool entry; progress; completion |
| `assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png` | `7c4f39ef353481f575a67636cf650cf967886e3f30ca5618f2961e0eb9e5c26b` | Bathroom supply hunt, sink and tub | tool ready; sink contact; tub contact; finale |
| `assets/castle/day_one_art_studio/magic_cleaning_brush.png` | `17e76b7f758f31a9b148167ff103a68bdf9543e7aac5794314a97bbd91066ef3` | Bathroom brush and reused Geologist brush | selected; tub contact; settle |
| `assets/castle/day_one_pool/activities/floating_trash_atlas.png` | `e554c4f253bcaa9e5893d9e4fffe03feef96528211f2458dc5d8fc81299f56df` | Pool skimmer atlas subframes | ready; each trash contact; partial; complete |
| `assets/castle/day_one_pool/activities/pool_skimmer.png` | `308c86843ace9fb3d4a65a0c514d41b367d87ceabaf5f3d3676f54ce9be4b9b3` | Pool skimmer tool | ready; drag contact; settled completion |
| `assets/castle/day_one_pool/activities/waterfall_scrubber.png` | `1b29ff463263be093a7e1ac33eb74e4075d6a795dd515d120107f66953b2dc7a` | Pool waterfall tool | clogged; scrub contact; cleared; completion |

The Day One routes are wired through `_sync_day_one_bathroom_cleanup` and `start_day_one_pool_cleanup` in `main.gd`; relevant source owners are `day_one_dust_bunny_swimmer.gd`, `day_one_bathroom_cleaning.gd`, `day_one_bathroom_cleanup.gd`, `pool_skimmer_activity.gd` and `pool_waterfall_activity.gd`.

The current Grand Puff source names absent `boss_tell_open.png` and `boss_tell_shielded.png` below `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/boss/`. Parent trace confirms `_stage_open` and `_place_boss` call `_apply_tell`, which falls back to `assets/mg/star.png` when those files are absent. This is a live semantic-art review gap, not a missing-resource crash: the same generic star substitutes for both tell identities. Review actual open/shielded presentation before replacement; do not invent hashes for absent assets or borrow unrelated parallel candidates. Existing 3D tell staging remains migration debt, not a template for new work.

Parent source-image inspection supports preserving the purple swimmer identity, pink star sponge silhouette and coordinated aqua/lavender/pearl pool-tool family for runtime review. The wrapper, can, cap, leaf, ribbon and sponge trash roles are visually distinct in the source atlas. These source observations do not establish action contact or full scene consistency. RGBA headers and alpha channels were checked read-only: swimmer 1024×683, sponge 512×512, trash atlas 1023×682, skimmer 1024×682 and waterfall scrubber 962×1024; all have zero-alpha corner pixels. Colored RGB outside a subject in an image viewer must not be labeled an opaque runtime halo without composited runtime evidence. No pixels were edited or new scores/acceptance assigned.


The six traced Day One assets now have individual open registry records with state-specific capture requirements, including each of the six trash-atlas roles. This expands the earlier 56-record snapshot to 62 records and 54 unique source paths. It does not fill the separate 24-code-source coverage gap or confer a 4.5 score.

## Family-evening expansion at dev 6d7c5e85

Sol independently reviewed the source delta from `aad0d450` to `6d7c5e85`. The single Comfy source record now requires dinner, movie, bedtime, handoff and restore states separately. It remains unscored: source inspection is not a rendered scene or animation review.

- Dinner removes apple, carrot and strawberry buttons as they enter the pot, then a single press sets `pot_stirred`. The spoken instruction describes stirring, but there is no stirring gesture or visible stirring state. Review ingredient scale/finish together, including the already weak carrot, and implement a causal result before acceptance.
- Movie reuses `movie_screen_frame.png` for all three scenes. Only metadata/caption changes; the crab, cloud-flight and family-hug narrative beats have no corresponding movie visuals in this layer. Three taps cannot establish a polished movie activity.
- Bedtime skips rendering family members once their `tucked_in` flag is true. The visual outcome is removal, with no blanket/bed/settled pose. Preserve protected character originals, but supply an observable tucked state and review the four mixed source-art families together.
- Cross-room progression uses spoken/text destination names. This layer supplies no destination picture/path pointer and may build no activity in an unrelated room. Inspect the actual navigation route and add child-readable guidance where missing.
- Required evidence includes each ingredient and family member, partial/complete states, pulse extrema, transitions, cancellation/reentry, and restored progress at every boundary. Bind the reused apple, carrot, strawberry, soup pot, movie screen, Rumi atlas region, Baby Eagle, Daddy, Roshan and applicable room art individually before declaring coverage complete.

These findings expand the repair backlog; they do not change the historical Opera scores or approve the new family-game art. The current full validation attempt remains pending.

Parent source-image inspection confirms a further semantic/composition issue: `room_kitchen_item_soup_pot.png` is an opaque illustrated kitchen crop containing a stove, oven, hanging pans and kettle around a small pot. It is not an isolated pot cutout. Placing that entire crop in the 280×260 pot button is a scene-within-scene risk and makes the spoken pot target ambiguous; inspect the mounted view before assigning a runtime score. The movie asset is an ornate lavender/pearl empty frame, so retaining it as scenery is reasonable, but it does not supply the three promised scenes. The carrot is the same tiny flat orange wedge previously flagged. Exact source pixels, dimensions and hashes are bound in [the family-evening source inventory](family_evening_sources.json); none were altered.

Luna then inspected all nine exact source images independently. Source-illustration scores were Baby Eagle 4.7, strawberry 4.8, Daddy 4.8, Roshan 4.6, Rumi atlas 4.7 and apple 4.6. These support reuse, not runtime acceptance. The current carrot scored 1.5 in this stricter source pass; the earlier 3.0 judgement remains dated history rather than being overwritten. The kitchen crop scored 3.2 **for the isolated-pot role**. Luna's 4.4 for the empty movie frame concerned its use as complete movie content; parent review retains the intentional frame and directs repair toward the missing scene content, not a needless decorative-frame regeneration. These scores and exact contexts are preserved in the source inventory.

## Current carrot and dinner follow-up

The preceding family inventory is a historical snapshot of dev `6d7c5e85`. The current candidate replaces the weak carrot with the unchanged approved Farmer token, preserves its outward Snowman nose angle through the chase waddle, and groups all three dinner targets in 116-pixel touch areas over the painted table. The source-only historical scores above do not rate the replacement. [The source-bound carrot follow-up](carrot_runtime_followup.md) records the failed capture methods, measured visible cutaway diagnostic and independent scene findings. The kitchen crop, movie-content and tucked-in-state gaps remain open.
