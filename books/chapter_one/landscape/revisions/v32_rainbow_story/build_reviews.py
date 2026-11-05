"""Build mapped V31/V32 review and binding previews from rendered proof pages.

Run only after BOOK_CURRENT.json, pagination.json and all 34 current proofs
are ready. This script describes the current artifacts; it assigns no scores.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path


V = Path(__file__).resolve().parent
BASELINE = V.parent / "v31_story_clarity"
PRIORITY = (4, 13, 14, 22, 30, 31)
PDF_NAME = "Mermaid_Roshan_LANDSCAPE_ROUGH.pdf"

CSS = """
*{box-sizing:border-box}body{margin:0;background:#16364d;color:#eef9ff;
font:17px/1.55 system-ui,sans-serif}header,main,footer{max-width:1700px;
margin:auto;padding:24px}h1{font-size:2rem;margin:.2em 0}h2{margin:.2em 0}
p{max-width:90ch}a{color:#b8edff}nav{display:flex;flex-wrap:wrap;gap:8px;
margin:20px 0}nav a,.badge{display:inline-block;border:1px solid #7095af;
padding:4px 10px;border-radius:8px;font-size:.9rem}section{margin:0 0 36px;
padding:20px;background:#23485f;border-radius:12px;scroll-margin-top:18px}
.comparison{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
gap:18px}.comparison.three{grid-template-columns:repeat(3,minmax(0,1fr))}
figure{margin:0;min-width:0;background:#16364d}figure img{width:100%;
height:auto;display:block}figcaption{padding:12px 15px}figcaption strong{
display:block}.caption{white-space:pre-wrap;margin:.5em 0 0;font-size:1rem}
.source-note,.note{background:#315971;padding:14px 18px;border-radius:8px}
.source-note{margin:10px 0 18px}.small{font-size:.88rem;color:#d4e7f4}
.spread{display:grid;grid-template-columns:1fr 1fr;gap:0;
border:2px solid #7391a6}.spread figure{border-radius:0}.blank{display:flex;
align-items:center;justify-content:center;aspect-ratio:7/5;background:#e9eff2;
color:#627582;padding:20px;text-align:center}.single{max-width:850px;
margin:30px auto}.single img{width:100%;display:block}.spread figcaption{
padding:8px 14px}.turn{border:2px solid #adddf0}.hash{overflow-wrap:anywhere}
@media(max-width:900px){.comparison,.comparison.three{grid-template-columns:1fr}
header,main,footer{padding:14px}section{padding:12px}h1{font-size:1.6rem}}
@media print{body{background:white;color:#17364b}header,main,footer{padding:0}
section{background:white;break-inside:avoid;border:0;border-radius:0}
a{color:#17364b}.note,.source-note{background:#edf5f8}.spread{border:0}}
"""


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def story_pages(book: dict) -> dict[int, dict]:
    pages = book["pages"]
    result = {int(page["page"]): page for page in pages}
    require(len(pages) == 32 and set(result) == set(range(1, 33)),
            "Expected exactly the 32 unique story pages, numbered 1 through 32.")
    return result


def label(number: int) -> str:
    return "Front cover" if number == 0 else "Rear cover" if number == 33 else f"Story {number}"


def proof_url(number: int, *, baseline: bool = False) -> str:
    prefix = "../v31_story_clarity/" if baseline else ""
    return f"{prefix}complete/page_{number:02d}.png"


def caption_text(number: int, pages: dict[int, dict]) -> str:
    return str(pages[number].get("text", "")) if number in pages else ""


def proof_figure(number: int, title: str, pages: dict[int, dict], *,
                 baseline: bool = False, note: str = "") -> str:
    url = proof_url(number, baseline=baseline)
    caption = caption_text(number, pages)
    return (
        '<figure><a href="' + url + '"><img loading="lazy" src="' + url
        + '" alt="' + html.escape(title, quote=True) + '"></a><figcaption><strong>'
        + html.escape(title) + '</strong>'
        + ('<div class="small">' + html.escape(note) + '</div>' if note else '')
        + ('<p class="caption">' + html.escape(caption) + '</p>' if caption else '')
        + '</figcaption></figure>'
    )


def document(title: str, header: str, content: str, footer: str = "") -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + html.escape(title) + '</title><style>' + CSS + '</style></head>'
        '<body><header>' + header + '</header><main>' + content + '</main>'
        '<footer>' + footer + '</footer></body></html>\n'
    )


def review_html(current: dict[int, dict], old: dict[int, dict], mapping: dict[int, dict],
                book_hash: str, pagination_hash: str, pdf_exists: bool) -> str:
    order = list(PRIORITY) + [n for n in range(34) if n not in PRIORITY]
    links = '<a href="complete/READ_BOOK.html">Current reader</a> · '
    links += '<a href="PRINT_DUMMY.html">Bound spread dummy</a>'
    if pdf_exists:
        links += ' · <a href="complete/' + PDF_NAME + '">Current PDF</a>'
    navigation = '<nav>' + ''.join(
        f'<a href="#page-{n:02d}">{html.escape(label(n))}</a>' for n in order
    ) + '</nav>'
    sections = []
    for number in order:
        row = mapping[number]
        baseline_number = row["baseline_page"]
        heading = f'<h2>{html.escape(label(number))}</h2>'
        heading += '<span class="badge">' + html.escape(str(row["status"])) + '</span>'
        source_note = ""
        if number == 4:
            require(baseline_number is None, "New story 4 must remain a new insert, not an old page.")
            figures = proof_figure(
                4, "V31 story 4 · source context", old, baseline=True,
                note="Existing dirty hall that now follows the inserted page as V32 story 5."
            )
            figures += proof_figure(number, "V32 story 4 · new inserted page", current)
            source_note = ('<p class="source-note">There is no before version of this new page. '
                           'The V31 hall is shown for story and visual context only.</p>')
        elif number == 31:
            require(baseline_number == 30, "New story 31 must map to the old reflection page 30.")
            figures = proof_figure(30, "V31 story 30 · reflection", old, baseline=True)
            figures += proof_figure(31, "V31 story 31 · gratitude and rest", old, baseline=True)
            figures += proof_figure(31, "V32 story 31 · combined page", current)
            source_note = ('<p class="source-note">The two V31 ending beats are shown together '
                           'beside their V32 combined page.</p>')
        else:
            require(isinstance(baseline_number, int), f"Missing baseline mapping for page {number}.")
            figures = proof_figure(
                baseline_number, "V31 " + label(baseline_number).lower(), old, baseline=True
            )
            figures += proof_figure(number, "V32 " + label(number).lower(), current)
        columns = 'comparison three' if number == 31 else 'comparison'
        sections.append(f'<section id="page-{number:02d}">' + heading + source_note
                        + f'<div class="{columns}">' + figures + '</div></section>')
    header = ('<h1>V32 · mapped before-and-after review</h1><p>34 authored pages: '
              'front cover, 32 story pages and rear cover. The six revised pages appear first; '
              'every cover and story page is included below. Page numbers identify story pages, '
              'with covers labeled separately.</p><p>' + links + '</p>'
              '<p class="note">Comparisons follow the pagination map, including moved pages. '
              'Captions beneath the images come from each version’s book data. Click an image '
              'to open its native proof. These previews carry no quality scores or approval claims.</p>'
              + navigation)
    footer = ('<p class="small hash">Current BOOK_CURRENT.json SHA-256: ' + book_hash
              + '<br>pagination.json SHA-256: ' + pagination_hash + '</p>')
    return document("Mermaid Roshan · V32 mapped review", header, ''.join(sections), footer)


def print_html(current: dict[int, dict], pdf_exists: bool) -> tuple[str, list[dict]]:
    blank = '<figure class="blank"><div>Unprinted inside cover</div></figure>'

    def interior(number: int) -> str:
        side = "right / recto" if number % 2 else "left / verso"
        return proof_figure(number, f"Story {number} · {side}", current)

    spreads = [{"id": "opening", "left": None, "right": 1}]
    sections = ['<section class="single"><h2>Front cover · exterior</h2>'
                + proof_figure(0, "Front cover", current) + '</section>',
                '<section id="opening"><h2>Opening</h2><div class="spread">'
                + blank + interior(1) + '</div></section>']
    for number in range(2, 32, 2):
        spreads.append({"id": f"spread-{number}", "left": number, "right": number + 1})
        turn = ' turn' if number in (22, 24, 26, 28) else ''
        sections.append(f'<section id="spread-{number}"><h2>Story {number}–{number + 1}</h2>'
                        + f'<div class="spread{turn}">' + interior(number)
                        + interior(number + 1) + '</div></section>')
    spreads.append({"id": "ending", "left": 32, "right": None})
    sections += ['<section id="ending"><h2>Ending</h2><div class="spread">'
                 + interior(32) + blank + '</div></section>',
                 '<section class="single"><h2>Rear cover · exterior</h2>'
                 + proof_figure(33, "Rear cover", current) + '</section>']
    links = '<a href="AUDIT_REVIEW.html">Mapped before-and-after review</a> · '
    links += '<a href="complete/READ_BOOK.html">Current reader</a>'
    if pdf_exists:
        links += ' · <a href="complete/' + PDF_NAME + '">Current PDF</a>'
    header = ('<h1>V32 · bound spread dummy</h1><p>34 authored pages: front cover, '
              '32 story pages and rear cover. 7 × 5 inches, landscape. This shows reading spreads '
              'with the intended binding positions; it is not printer-sheet imposition.</p>'
              '<p class="note">The front and rear artwork are exterior covers. PDF positions '
              '2–33 form the 32-page interior, beginning with story 1 on the right. The blank '
              'inside covers are cover surfaces, not added story pages. A cover-inclusive PDF '
              'should not be duplexed as a simple loose stack.</p><p>Story 23 is on the right: '
              'turning it reveals Grand Puff on story 24. Story 27 is on the right: turning '
              'it reveals rainbow Puff on story 28. No story artwork spans the gutter.</p><p>'
              + links + '</p>')
    return document("Mermaid Roshan · V32 bound spread dummy", header, ''.join(sections)), spreads


def main() -> None:
    book_path, pagination_path = V / "BOOK_CURRENT.json", V / "pagination.json"
    book, pagination = read_json(book_path), read_json(pagination_path)
    old_book = read_json(BASELINE / "BOOK_CURRENT.json")
    current, old = story_pages(book), story_pages(old_book)
    require(pagination.get("total_pages") == 34 and pagination.get("story_pages") == 32,
            "The pagination map must describe 34 authored pages and 32 story pages.")
    require(book.get("format_inches") == [7, 5], "Expected the 7 × 5 inch landscape format.")
    rows = pagination["rows"]
    mapping = {int(row["new_page"]): row for row in rows}
    require(len(rows) == 32 and set(mapping) == set(range(1, 33)),
            "pagination.json must map every story page exactly once.")
    require(all(row.get("baseline_page") is None or
                isinstance(row["baseline_page"], int) and 1 <= row["baseline_page"] <= 32
                for row in rows), "A baseline story mapping is invalid.")
    require(all(isinstance(row.get("status"), str) for row in rows), "Every mapping needs a status.")
    require(set(PRIORITY).issubset(set(pagination.get("changed_new_pages", []))),
            "A prioritized revised page is missing from pagination.json.")
    require(pagination.get("merged_baseline_pages") == [30, 31],
            "The combined ending must identify both V31 source pages 30 and 31.")
    mapping.update({0: {"new_page": 0, "baseline_page": 0, "status": "EXACT_REUSE"},
                    33: {"new_page": 33, "baseline_page": 33, "status": "EXACT_REUSE"}})
    reveal_pairs = [(23, 24), (27, 28)]
    require([tuple(pair) for pair in pagination.get("reveal_turns", [])] == reveal_pairs,
            "The door and bubble page turns must remain 23→24 and 27→28.")
    for setup, reveal in reveal_pairs:
        require(setup % 2 == 1 and reveal == setup + 1 and reveal % 2 == 0,
                "A reveal must follow a right-hand setup on the next left-hand page.")
    require("door" in caption_text(23, current).casefold()
            and "grand puff" in caption_text(24, current).casefold(),
            "Story 23→24 must contain the closed-door setup and Grand Puff reveal.")
    require("bubble" in caption_text(27, current).casefold()
            and "pop" in caption_text(28, current).casefold()
            and "rainbow" in caption_text(28, current).casefold(),
            "Story 27→28 must contain the bubble setup and rainbow POP reveal.")
    proof_records = []
    for number in range(34):
        current_path = V / "complete" / f"page_{number:02d}.png"
        old_path = BASELINE / "complete" / f"page_{number:02d}.png"
        require(current_path.is_file() and old_path.is_file(),
                f"Both V31 and V32 native proof {number:02d} must exist before building reviews.")
        compared_numbers = ([4] if number == 4 else [30, 31] if number == 31
                            else [mapping[number]["baseline_page"]])
        comparisons = []
        for compared_number in compared_numbers:
            compared_path = BASELINE / "complete" / f"page_{compared_number:02d}.png"
            comparisons.append({
                "page": compared_number,
                "role": "source_context" if number == 4 else "before",
                "png": proof_url(compared_number, baseline=True),
                "sha256": sha256(compared_path),
            })
        proof_records.append({"page": number, "current_png": proof_url(number),
                              "current_sha256": sha256(current_path),
                              "baseline_comparisons": comparisons})
    book_hash, pagination_hash = sha256(book_path), sha256(pagination_path)
    pdf_path = V / "complete" / PDF_NAME
    pdf_exists = pdf_path.is_file()
    audit = review_html(current, old, mapping, book_hash, pagination_hash, pdf_exists)
    dummy, spreads = print_html(current, pdf_exists)
    evidence = {
        "revision": book.get("revision"), "authored_pages": 34,
        "interior_story_pages": 32, "format_inches": [7, 5],
        "book_sha256": book_hash, "pagination_sha256": pagination_hash,
        "pdf": "complete/" + PDF_NAME if pdf_exists else None,
        "pdf_sha256": sha256(pdf_path) if pdf_exists else None,
        "exterior_covers": [
            {"role": "front", "proof_page": 0, "pdf_position_one_based": 1},
            {"role": "rear", "proof_page": 33, "pdf_position_one_based": 34}],
        "interior_pdf_positions_one_based": [2, 33],
        "first_story_side": "right / recto", "last_story_side": "left / verso",
        "unprinted_inside_cover_surfaces": 2, "reading_spreads": spreads,
        "reveals": [{"setup_story_page": setup, "setup_side": "right / recto",
                     "reveal_story_page": reveal, "reveal_side": "left / verso"}
                    for setup, reveal in reveal_pairs],
        "comparison_display_order": list(PRIORITY) + [n for n in range(34) if n not in PRIORITY],
        "story_mapping": rows,
        "new_page_4_comparison": {"before_page": None, "source_context_baseline_page": 4},
        "new_page_31_comparison": {"baseline_pages": [30, 31], "current_page": 31},
        "proofs": proof_records,
        "binding_note": "Reading arrangement only; not printer-sheet imposition. Covers are separate from the 32-page interior.",
    }
    # All inputs are checked and all outputs constructed before any output file is written.
    for name, content in (("AUDIT_REVIEW.html", audit), ("PRINT_DUMMY.html", dummy),
                          ("print_pagination.json", json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")):
        (V / name).write_text(content, encoding="utf-8", newline="\n")
    print("Built mapped 34-page review, bound spread dummy and print pagination metadata.")


if __name__ == "__main__":
    main()
