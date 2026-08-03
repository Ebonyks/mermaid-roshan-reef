## Delivered

**`C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md`** — replaced in place (git preserves rev 1). **3,478 lines**, titled *"Codex handoff — full-screen minigame scene art (2026-08-03, rev 2)"*.

Sources read before writing: the rev-1 handoff, the 2026-08-02 widget-art handoff (conventions), the live engine (`opera_gesture_surface.gd`, `opera_career_world_2d.gd`, `opera_nursery_catch.gd`), the fix commit `cd624567`, the on-disk widget inventory (154 PNGs), the ledger/manifest formats, and `OPERA_INGREDIENT_INTERACTION_DIRECTION_2026-08-03.md`.

## Section by section

**1. THE DIRECTION** — owner quote verbatim; caliber target grounded in three files that already passed the gate (`goal_chef.png`'s per-tier crumb texture and varying 4px plum contour, `goal_magician.png`'s velvet sheen band, `world_chef.png`'s ~40 objects); an 11-row before→after table, one line per template ("a flat `#FFDF95` rounded rectangle on the **outside front wall** of the bowl" → "milk streaming from a tipped jug into a bowl of tumbling ingredients"); plus §1.5 making the delivery a prerequisite for the ingredient-manipulation pass rather than a competitor (adds an `objects=name@x,y,r` ledger field and *(state-ready)* flags).

**2. WHAT CHANGED** — a seven-row table mapping rev 1's W-numbers to the code that now runs (ink-band reveal, charge progressive fill, completion pin+burst+0.9s hold, bounce rate-limit, held-finger gap clear, de-duped `set_fill`, affordance restore), each with file:symbol. Stated plainly: **this is now purely an art request.** §2.1 isolates the six residual engine items (E-0…E-6) as explicitly *not* Codex's problem, and withdraws two rev-1 asks that were wrong: the crank radial sweep (the cross-fade is now the design) and the `_done` suffix.

**3. THE FULL CONCEPT PER BEAT** — all **60 beats**, organised by template, each with SCENE / LAYERS / PROGRESS at 10-50-100 / SUCCESS / CONTENTS / FILES-with-new-or-replace-status. Rev 1's D4 exclusion is withdrawn with reasoning — magician CABINET, detective NAME and nursery BURP are all specified. No beat is held.

**4. THE LAYER GRAMMAR** — canvas standard (1024×576 replacing 1024×608, with the reason and the "not blocked on E-0" note); the five layer types; **IB-1…IB-7** for vertical ink bands (contents-only, band-is-the-budget, every-row-a-plausible-surface, ingredients at 15/35/55/75/92%, monotonic, opaque, declared); **TR-1…TR-6** for the trace wipe — including the finding that the horizontal branch still ignores ink bounds, so trace `_lit` ink must reach x ≤ 24 and x ≥ 1000 defensively; per-transform sprite rules; a today-vs-target engine draw-size table; and the extended ledger registration grammar.

**5. SHARED ASSETS** — 7 files serving all 60 beats, plus the 13 `goal_<career>.png` props already on disk and reusable as-is, plus a shared visual vocabulary (palette, varying contour, sparkle language, underwater bubble physics, contact deformation, chalk-ghost, green-is-reserved) reused by drawing rather than by file.

**6. PRIORITY** — Tier 1 is exactly the three beats the owner named (chef POUR, chef PIPE, chef STIR = 11 files), chosen because between them they exercise every layer type in the grammar and need **zero** engine changes. Tier 2 finishes the chef career end-to-end. Tier totals reconcile to 247.

**7. ACCEPTANCE** — the 2026-08-02 weighted gate plus 14 programmatic checks. **G-4 is the new headline criterion**, written to the measured failure: render at 0.00/0.50/1.00 and require (a) ≥12% of pixels in the declared band changed between adjacent pairs, (b) a reviewer able to *name* one thing present at 50% and absent at 10%, (c) a terminal 100% — with the "chef POUR stopped changing at t=2.16s of a 5.0s hold" measurement cited as the reason. Closes with G-14, the six-foot test: if you cannot name three ingredients, it is not finished.

**8. DELIVERY & MANIFEST** — **247 files (7 shared + 240 beat files); exactly 148 replace an existing widget PNG and exactly 92 are new slots** (`_success` ×59, `_fill` ×22, track `_hit` ×8, gauge `_needle` ×3). Reconciled against the three concept briefs' 208 — the difference is the universal `_success` family, which they predated because the completion hold did not exist when they were written. Staging protocol, engine work shipping alongside, and out-of-scope list unchanged in spirit.

## Corrections made against the source briefs

- **pour_nursery reversal withdrawn.** Rev 1 asked for a draining bottle with `axis=down`; the reveal fills bottom-up, so the beat is now *filling the bottle for the baby*. Probe contract at `probe_opera_nursery.gd:88` preserved.
- **`_success` / `_hit` grammar unified.** `_success` = the terminal held picture (universal, 11 templates); `_hit` = the momentary in-zone flash (gauge, track). The three gauge `_success` files are re-authored under `_hit`.
- **Trace ink-band gap flagged.** `_draw_progress_overlay`'s horizontal branch returns before `_ink_bounds` runs — the vertical fix was not mirrored. A brief specifying "ink band x=300→1000" would have produced 29% dead drag. Handled as engine item E-1 *and* a defensive authoring rule.
- **File-status audit.** Verified `widget_push_boxer_mover.png` and `widget_target_boxer_mark.png` both exist (the briefs implied otherwise), so they are marked *replace*, and the 148/92 split is exact rather than approximate.
- **Lanes registration.** Token centre pinned to y = 403 (`0.70h`, where the engine already draws the lit cell) so the art registers to the engine rather than requiring a y-coordinate change.
