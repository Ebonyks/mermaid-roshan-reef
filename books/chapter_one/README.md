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
