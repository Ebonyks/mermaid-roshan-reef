# R148 painted Racer item bubble

The painted sea-glass frame replaces the visible flat circles, hue arcs and glint around the item control. R148 uses the existing `FV-CD4F06A6937B` Turbo control frame role. The touch center, radius and item icons retain their current behavior. [Candidate and review](https://github.com/Ebonyks/mermaid-roshan-reef/blob/774b0d134be93c5751ac8c03efeec85c8a854674/docs/handoffs/codex_flat_vector_art_2026-10-07/r148_racer_painted_item_bubble_runtime/README.md)

The source passed 88 local commands. At both configured viewport widths, changes stay inside the item control bounds and the PC cases match pixel for pixel. The initial empty state was faint against the track, so the final candidate uses higher empty opacity. [Production record](PRODUCTION_RECORD.json) · [Verified source bytes](SOURCE_REMOTE_VERIFICATION.json) · [Server check snapshot](SOURCE_CI_AT_INTAKE.json)

49 bounded source artifacts and 47 partial Dev artifacts. Named role and family lower bounds are 282 and 36. R148 adds one bounded source artifact for the existing Turbo control frame. Retained events are 8,161 bounded and 4,457 excluded, totaling 12,618. Formal, device, child and owner acceptance remain open. Whole-game totals remain unknown.

Formal QA11, natural routes, full-speed review, physical device testing, child and owner acceptance are separate from local and package checks. [Canonical manifest](CANONICAL_MANIFEST.json)

## Dev integration

The verified R148 candidate is on Dev. [Dev evidence](dev_integration_20261107/README.md)

## Verified Dev Android package

Version code 2373 contains the painted item bubble from Dev `774b0d1`. [Android package verification](android_verified_20261107/README.md)
