# Bubble Duel original-feel rebuild — review evidence

This is an implementation and review record for the owner's November5 critique. It does not accept the game against the master audit or replace the owner's judgment of feel.

## Implemented

The old seek-a-target controller is removed. A press produces one flap impulse; left/right selects its direction. Holding or dragging does not supply more thrust, teleport toward a target, stop gravity, or line up a hit. A quick tap retains its direction until the30Hz simulation consumes it. The controller keeps momentum, soft speed caps, screen wrap, ceiling restitution, body velocity exchange, pop rebound, bubble-dependent lift and four inflation variants.

The six existing characters and shared purchased wardrobe/power items remain. Local versus uses independent loadouts. Cooperative friends share a team against up to three live rivals. A16-stage campaign changes opponent count/rank/equipment and inflation rules. Earned pearls and partial enemy bubbles/spares survive leaving or a90-second rest; a rest never pretends that a stage was won. Solo/co-op rescues protect the child's progress. Current Ride uses moving collectible pearls and ink hazards, with immediate banking and a saved best.

The entrance is the existing painted left elevator. Roshan walks to its landing before entering. The separate floating Opera launcher is removed; the developer job picker stays disabled. Story gates, career ownership, family art/voices and normal return/input control remain intact.

## Mechanical reference and selection

The preserved [owner source notes](reference/STUDY_NOTES.md) describe the original [Balloon Duel by Mousekliks/John Su](https://www.newgrounds.com/portal/view/177120). The [reference manifest](reference/manifest.json) records recovered source bytes and the missing-original-ZIP limitation. The original author's SWF was fetched only into ignored research storage; its header,30fps and SHA-256 matched the notes. It was not executed or copied into the game. The JS numerical oracle executes the owner's fresh implementation of those mechanics, not the copyrighted Flash binary.

There were two50-setting passes, each25 broad comparisons plus25 refinements. The first is frozen in[study-r1](study-r1/selection.json):599/600 natural bout ends. After correcting the UI press-direction latch, revalidation produced600/600 natural ends and selected the original default values; [selection.json](selection.json) records the full ranking. The earlier provisional2.5 pop rebound is superseded by the source2.0 rebound.

Iteration accounting is explicit: the second pass regenerated its25 refinement settings around the new measured winner. That produced75 distinct parameter sets across the two passes, exceeding the requested overall50 if treated as a total cap. This was a process overrun, not a paid generation campaign. Further new variants are stopped; the runner is locked to existing configurations for later revalidation. Both passes, rejected trials and source identities are retained.

The score is a declared fidelity/completion/pacing proxy, not a human fun rating. It weights source trace fidelity65%, natural completion25%, and proximity to a35-second simulated bout10%. The original defaults are gravity0.25, strength3, horizontal impulse factor0.75, soft-cap decay0.9, ceiling bounce/drag0.8, maximum speeds6/5 and pop rebound2 in logical units per original30Hz tick.

## Verification lanes

- Numerical oracle:17 cases/1,710 steps, strict0.001 logical-unit tolerance. [Reference check](reference-check.json). It covers motion, wrap ties, soft caps, ceiling/rescue, bubble counts, inflation and muted inputs; source art/combat geometry is separately adapted.
- Final production-geometry tuning:600 actual engine bouts across all six cast members, one/two/three enemies and all four inflation stages. [Phase1](phase1-results.json), [phase2](phase2-results.json).
- Final actual-viewport UI run:100 sessions,18,566 checks,0 failures;85 natural endings and15 explicit rest points, median43.15s. All36 local pairings, all16 stage IDs, all84 character/power/player activation fixtures, purchases, unknown save fields, focus/cancel/quick-tap behavior, a natural partial checkpoint return, complete Current Ride, blocked-write rollback and a fresh-process reload. [Report](ui-hover-final-100.json), [reload](ui-hover-final-100-reload.json). These are input-driven bot sessions, not100 human playthroughs. A continuation can finish damage earned in the previous visit; the report distinguishes that from a fresh contact.
- Source files are checked unchanged from the beginning to end of that final UI trial. [Source registry](source-registry.json) binds local literal bytes and canonical Git/LF bytes.
- Native review: Mobile renderer/Speedy, full screenshots and a gameplay-only motion export. Capture manifests retain hashes. Review packet completion, provisional visual observations, formal QA11, physical device, child and owner approval remain separate.
- Full local and exact-head remote regression/build status is recorded in the impact record at commit time; later CI/APK results do not retroactively change an earlier pending snapshot.

## Deliberate adaptations and acceptance limits

Art and sound use the existing Mermaid Roshan families. Runtime uses true2D drawing and source-alpha fin/body/socket geometry instead of the Flash rectangles. Contact resolution is simultaneous for fair local play. AI releases ceiling camping through real falling arcs. The child-safe rescue, finite rest points, cooperative teams and checkpointed campaign are deliberate adaptations. The original arena fish/registration/rank-loss and separate cosmetic-shop structure are not recreated one-for-one; lower-bound recovery and the Current Ride hazards supply the present shell's safe boundary behavior.

No protected original was modified and no new paid art was generated. Daddy, Baby Eagle and Rainbow Friend still use existing static sources; they have no newly accepted authored swim acting. Existing source-native background/detail, typography, exact motion/style, physical Android performance/two-person touch, child and owner acceptance gaps remain open. No4.6 master-audit acceptance score is fabricated from bot completion or an encode. Earlier candidate art ratings remain provisional; current scale/attachment observations are separately recorded in the visual review.

Game-wide master audit/strict-zero2D satisfaction remains UNSATISFIED. This task closes no MA finding.

Five native wearable-fit rejections were repaired and rechecked in[the candidate appearance review](appearance-review.json), including every applicable authored source key. All48 per-role candidate minimums are4.6; this is not a formal master-audit PASS. [Native gameplay review](gameplay-review-current.mp4) is a16-second visual-only diagnostic.

The final whitespace gate removed only terminal empty lines from the overlay. [Exact before/after proof](gate-cleanup/equivalence.json) preserves the original captured-source bytes; no program token or gameplay value changed. Full final CI checks the cleaned source.

The first full regression stopped at the unchanged2D gate: its file-reference detector treats `board.blend` as a Blender file path. The float property was mechanically renamed to `interpolation` at its declaration, assignment and lerp use. [Exact snapshots and proof](gate-cleanup/field-rename.json) bind the captured/tested source to this behavior-identical rename. [The initial failure](local-ci-initial-failure.json) is retained; neither the gate nor its debt manifest was changed. Final full CI exercises the renamed property.

Full local regression completed2026-11-06T11:24:08Z: official Godot4.7.2,82 trusted probes,exit0,3,771.75seconds; runtime source unchanged throughout. [Complete receipt](local-ci.json), [transcript](local-ci.log). The unchanged strict2D gate reports NO_REGRESSION, not whole-game satisfaction. Exact remote CI and the final Dev APK remain later delivery steps.

Integration review2026-11-06: work `73463083dcc39ed21fda320b89ff6d77b70de208` is combined with newer Dev `f1cced56d299695580509b0d3c96e75f7f5e75ce`. The initial merge changed only the shared painted shell motif and left all11 Bubble Duel sources unchanged. The later bounded venue-hover correction is separately recorded below. Both append-only attribute/ledger conflicts retain each task. [Combined full-regression receipt](integration-ci.json) now records the actual final82-probe PASS; its13code hashes,completeindex,file-set and389task-artifact hashes stayed unchanged. Earlier native captures and the82-probe receipt keep their original source scope; no new creative acceptance is inferred from this shared-UI merge.

Fresh combined960capture exposed a stale Opera tooltip. The approved engine cached the underlying portal hover across touch-only entry. Two native cursor-refresh calls now update ownership on arcade entry/return. [Review and retained failed trials](hover-review/review.json) distinguish native evidence from unsupported headless cursor assertions. The native capture probe now seeds real portal hover and requires correct modal/return ownership;960/1600 each8captures pass. New complete UI100 and full combined regression are pending rather than credited from the interrupted run. The interrupted suite is retained as CANCELED_NOT_A_PASS.

Final source after the bounded hover repair: [new100-session UI report](ui-hover-final-100.json) and [fresh-process reload](ui-hover-final-100-reload.json) PASS, 18,566checks/0failures,85natural endings plus15explicit saved rests,median43.15s,all84power cases. Source hashes match the final files. The unsupported headless hover trial and interrupted concurrent trial remain preserved as non-passes. The native hover gate rejects a deliberately hidden modal with exact exit9. Complete combined regression remains the next required gate.

Current combined source also passes the default1280 native fixture:74full-context captures plus480 gameplay readbacks, with real modal-hover and Back-return assertions. [Current16-second gameplay preview](gameplay-review-current.mp4) and [encoding/source receipt](motion-review-current.json) supersede the earlier movie for current UI context. This remains diagnostic gameplay footage, not accepted acting, device or final cinematic evidence.

A combined run stopped at the development-coverage gate before any gameplay probe because two exact-parent CI receipts were added while the gate was running. [Failure receipt](integration-ci-metadata-race.json) retains the source-stable0-probe failure. Their coverage entries are now present; the replacement run freezes all project files until completion, not only gameplay source. No audit or test requirement was weakened.

Final complete combined regression finished2026-11-06T13:48:13.618292+00:00: officialGodot4.7.2,82trusted command exits0,4386.62seconds. All389task artifacts,13code sources,full Git index and tracked/unignored inventory stayed unchanged until the child finished. Later metadata records this result; no runtime source changed. Exact latest combined topic/Dev CI and the new APK are the remaining publication checks. Formal/device/child/owner/fun acceptance stays open.
