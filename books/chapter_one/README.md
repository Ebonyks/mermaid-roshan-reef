# Mermaid Roshan — Chapter One picture book

Dedicated branch: `codex/mermaid-roshan-picture-book`.

The current stress-revised deliverable is a **7 x 5 inch landscape rough: 32 story pages plus front/back covers**. Existing scenes run full-art; reduced illustrations are alpha silhouettes. Sniglet and the blue two-mound background carry the original book design language.

- [Current manuscript](landscape/book.json) and [page assignments](landscape/PAGE_PLAN.md).
- [Build and review notes](landscape/REVIEW.md).
- [Design rules](DESIGN_LANGUAGE.md) and [original background prompt](ORIGINAL_GEMINI_BACKGROUND_PROMPT.txt).
- [Previous portrait plan](plan/PAGE_BY_PAGE_PLAN.md), superseded by landscape pagination.
- `archive/rough_v5/`: preserved older source package, not the current layout.

Run `python books/chapter_one/landscape/render_book.py --output output/pdf/landscape` from the repository root. This creates the 34-page PDF, faithful page-image HTML reader, five contact sheets and verification JSON. The renderer requires Pillow, reportlab and pypdfium2.

The waterfall action is narrated using existing obstruction art followed by a distinct rainbow frame; a true clearing-action illustration remains absent. Some original storyboard sources have low print resolution. This is a review rough, not a print master or cinematic delivery acceptance.

These assets are non-runtime; `.gdignore` prevents import. Work stays on the dedicated book branch. Do not restart the stopped Resolve handoff search.

Create a portable editable ZIP after rendering with `python books/chapter_one/landscape/package_book.py --proof output/pdf/landscape --output output/pdf/Mermaid_Roshan_EDITABLE_SOURCE.zip`. The archive includes only used image assets, the font/license and all required build inputs. `page_provenance.json` records actual image-layer use, including both covers and blue backgrounds.

The owner rejected the earlier v7 visual quality. [Comprehensive stress review](landscape/STRESS_TEST.md) records the concrete issues, per-page changes and remaining source/identity gaps. Mechanical and portable-rebuild checks do not imply visual acceptance.

The prior v16 border-performance rough implemented the [reviewed art direction](landscape/BORDER_ART_DIRECTION.md) across the twelve reduced pages. Main story art/text match v15; page22 remains full art. The earlier [study review](landscape/BORDER_DIRECTION.html) is preserved as planning history, not the current book. Exact edits and review limits are in landscape/border_rollout_evidence.json.

After saving the direction to the branch, the [whole-story comprehension cycle](landscape/STORY_COMPREHENSION_AUDIT.md) reviewed all 32 pages. Its verdict is REVISE, with foreground/action gaps prioritized before further border polish.

Current edition: **v17 repository story details**. Rubbish and messy-art states now match the cleanup beats; lower-right bunny reactions escalate across pages24–26; Roshan uses distinct existing poses; the cover is a new composition of existing cutouts. The portable source and PDF are rebuilt from the same current manifest. See landscape/repo_detail_evidence.json.
