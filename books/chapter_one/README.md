# Mermaid Roshan — Chapter One picture book

Dedicated branch: `codex/mermaid-roshan-picture-book`.

- [Book design language](DESIGN_LANGUAGE.md): owner rules and precise interpretation of the original Gemini prompt.
- [Original prompt](ORIGINAL_GEMINI_BACKGROUND_PROMPT.txt): owner-provided wording, formatting normalized only.
- [Illustrated plan](plan/DESIGN_PLAN.html): current 40-page CUTOUT-or-FULL-ART plan: 23 cutout pages, 17 full-art pages, explicit foreground/mound/removal assignments. Raw sources are collapsed reference inputs, never proposed reduced-page panels.
- [Written page plan](plan/PAGE_BY_PAGE_PLAN.md) and [editable table](plan/page_plan.csv).
- `plan/source_catalog.json`: original source chains and file hashes.
- `archive/rough_v5/`: preserved, superseded rough source package; run `python render_book.py` there to regenerate. It is not the accepted new layout.
- [Change evidence](../../design/audit_impacts/picture-book-dedicated-branch-20260920.json).

The book is not rebuilt yet. Page 12 is the blocked waterfall; page 13 is a distinct clearing-action requirement, with no reused page-12 placeholder. The existing material reviewed does not establish a valid clearing-action frame, so it stays an explicit gap rather than becoming invented art. Later rainbow flow remains on pages 14-15.

These assets are non-runtime. `.gdignore` prevents Godot import. Keep development on this dedicated branch; game integration/release is not part of this book task. Do not poll for the stopped Resolve handoff.

Regenerate the review HTML, Markdown, JSON and CSV with `python books/chapter_one/render_plan.py` from the repository root. The plan is the deliverable for this layout revision; actual cutout production and book rebuilding remain pending.
