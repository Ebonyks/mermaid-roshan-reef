"""Build the commissioned book review PDF without changing source artwork."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import re
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / 'book_plan.json').read_text(encoding='utf-8'))
PDF = HERE / 'output/pdf/Mermaid_Roshan_Song_Beneath_the_Pool_DRAFT.pdf'
MANIFEST = HERE / 'generation_manifest.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_art(spread):
    stem = 'spread_' + spread['id'] + '_' + spread['name']
    revised = HERE / 'native' / (stem + '_v2.png')
    return revised if revised.exists() else HERE / 'native' / (stem + '.png')


def records():
    from PIL import Image
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    previous_source_hashes = {item['path']: item for item in manifest.get('source_hashes', [])}
    sources = set(manifest['cast']['references'])
    for generation in manifest['generations']:
        sources.update(generation['references'])
        path = HERE / 'native' / Path(generation['saved_path']).name
        generation['native_sha256'] = sha(path)
        original = Path(generation['native_source'])
        generation['tool_cache_available'] = original.exists()
        if original.exists():
            generation['native_source_sha256'] = sha(original)
        elif 'native_source_sha256' not in generation:
            raise ValueError(f'Missing original output and archived hash: {original}')
        assert generation['native_sha256'] == generation['native_source_sha256'], path
        with Image.open(path) as source_image:
            generation['native_dimensions'] = list(source_image.size)
            generation['native_mode'] = source_image.mode
        generation['prompt_sha256_utf8'] = hashlib.sha256(generation['prompt'].encode()).hexdigest()
        generation['selected_for_story'] = path == selected_art(next(s for s in PLAN['spreads'] if s['id'] == generation['id']))
        if not generation['selected_for_story']:
            generation['status'] = 'SUPERSEDED_FOR_STORY_CONTINUITY'
    source_hashes = []
    for recorded_path in sorted(sources):
        normalized = recorded_path.replace('\\', '/')
        marker = '/mermaid-roshan-reef/'
        path = ROOT / normalized.split(marker, 1)[1] if marker in normalized else Path(recorded_path)
        if path.exists():
            source_hashes.append({'path': recorded_path, 'sha256': sha(path), 'available_at_record_update': True})
        elif recorded_path in previous_source_hashes:
            source_hashes.append({**previous_source_hashes[recorded_path], 'available_at_record_update': False})
        else:
            raise ValueError(f'Missing input source and archived hash: {recorded_path}')
    manifest['source_hashes'] = source_hashes
    cast_path = HERE / 'native/cast_identity.png'
    manifest['cast']['native_sha256'] = sha(cast_path)
    cast_original = Path(manifest['cast']['native_source'])
    if cast_original.exists():
        manifest['cast']['native_source_sha256'] = sha(cast_original)
    assert manifest['cast']['native_sha256'] == manifest['cast']['native_source_sha256']
    with Image.open(cast_path) as cast_image:
        manifest['cast']['native_dimensions'] = list(cast_image.size)
        manifest['cast']['native_mode'] = cast_image.mode
    manifest['calls_completed'] = 1 + len(manifest['generations'])
    manifest['edits'] = 'Four local corrections: remove premature cast in spreads 02/03/05 and restore tiny encore imp costumes in spread 13. Unaltered native originals preserved. PDF scales complete images and embeds separate RGB JPEG encodings at quality95/subsampling0, without resizing or retouching native sources.'
    manifest['tool_settings'] = {'transparent_background': False, 'one_output_per_call': True, 'native_dimensions': 'Chosen by built-in tool; measured in file manifest', 'seed': 'Not exposed'}
    manifest['book_format'] = '34 logical book pages: cover, title, 15 full story spreads (30 pages), refrain, back. PDF review keeps spreads intact: 19 landscape PDF sheets.'
    manifest['assembly_dependency'] = 'Book images load from repository-native copies. External generator caches and the supplied film reference are provenance inputs, not required PDF appearance files; unavailable originals retain their recorded hashes and explicit availability limits.'
    manifest['cover_source'] = 'native/spread_02_city_beneath_pool.png; too-early supporting cast rejected for story spread 02 but appropriate ensemble imagery for cover.'
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    text = [PLAN['title'], '', 'NEW BOOK - ILLUSTRATED DRAFT - 2026-10-09', '']
    for i, spread in enumerate(PLAN['spreads']):
        text += [f"Pages {3 + i * 2}-{4 + i * 2}: {spread['name'].replace('_', ' ')}", spread['left'], '', spread['right'], '']
    (HERE / 'MANUSCRIPT.txt').write_text('\n'.join(text), encoding='utf-8')
    ledger = ROOT / 'ASSET_LICENSES.md'
    content = ledger.read_text(encoding='utf-8')
    begin = '<!-- RUMI_UNDERPOOL_BOOK_20261009_BEGIN -->'
    end = '<!-- RUMI_UNDERPOOL_BOOK_20261009_END -->'
    section = [begin, '## Rumi under-pool new-book draft - 2026-10-09', '', 'Owner commissions a new illustrated book and two original mermaids. Source references retain their existing terms; user-supplied film image is an archetype reference only and is not copied into delivery pixels or this repository. All outputs are static review candidates excluded from runtime by `assets_src/.gdignore`.', '', '| Asset | Source / license | URL | Modifications / acceptance |', '|---|---|---|---|']
    for path in sorted((HERE / 'native').glob('*.png')):
        rel = path.relative_to(ROOT).as_posix()
        origin = 'Byte-identical archive of the owner-liked built-in ImageGen city preview' if path.name == 'city_concept_source.png' else 'OpenAI built-in ImageGen commissioned illustration; project identity references retain original provenance'
        section.append(f'| `{rel}` | {origin}; generated-output usage under OpenAI terms. | https://openai.com/policies/terms-of-use/ | Native output preserved; prompt/reference/hash/selection in adjacent generation manifest. New-book draft only; no runtime, print-production or owner acceptance. |')
    if PDF.exists():
        section.append(f'| `{PDF.relative_to(ROOT).as_posix()}` | Project-authored story/layout; embedded illustration sources listed above. | Source rows and generation manifest. | Complete-image placement, separate JPEG quality95/subsampling0 PDF encodings and embedded Georgia fonts; 19-sheet full-spread review of 34 logical book pages. Native source art unchanged. |')
    for path in sorted((HERE / 'verification').glob('*.png')):
        section.append(f'| `{path.relative_to(ROOT).as_posix()}` | Rendered review contact sheet derived from this book PDF; original image terms retained. | Source rows and generation manifest. | Reduced PDF-page previews only; no new scene generation or runtime use. |')
    section += [end, '']
    block = '\n'.join(section)
    if begin in content:
        content = re.sub(re.escape(begin) + r'.*?' + re.escape(end) + r'\n?', block, content, flags=re.S)
    else:
        first, rest = content.split('\n', 1)
        content = first + '\n\n' + block + '\n' + rest
    ledger.write_text(content, encoding='utf-8')
    impact_path = ROOT / 'design/audit_impacts/rumi-underpool-book-20261009.json'
    impact = json.loads(impact_path.read_text(encoding='utf-8'))
    impact['files'] = sorted({
        'audit/MASTER_AUDIT_2026-08-09.md', 'design/05_DOC_LEDGER.md', 'ASSET_LICENSES.md',
        'design/chapters/RUMI_UNDERPOOL_BOOK_20261009.md',
        *[p.relative_to(ROOT).as_posix() for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts],
    })
    impact_path.write_text(json.dumps(impact, indent=2) + '\n', encoding='utf-8')
    print(f'BOOK_RECORDS_OK native={len(list((HERE / "native").glob("*.png")))} calls={manifest["calls_completed"]}')


def build():
    from PIL import Image
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader
    from pypdf import PdfReader
    import pypdfium2

    pdfmetrics.registerFont(TTFont('GeorgiaBook', 'C:/Windows/Fonts/georgia.ttf'))
    pdfmetrics.registerFont(TTFont('GeorgiaBookBold', 'C:/Windows/Fonts/georgiab.ttf'))
    W, H = 1000, 720
    ink = HexColor('#263C66')
    cream = HexColor('#FFF8EC')
    accent = HexColor('#9278C2')
    style = ParagraphStyle('Story', fontName='GeorgiaBook', fontSize=20, leading=27, textColor=ink)
    small_style = ParagraphStyle('Small', fontName='GeorgiaBook', fontSize=14, leading=21, textColor=ink)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF), pagesize=(W, H), pageCompression=1)
    c.setTitle(PLAN['title'] + ' - illustrated draft')
    c.setAuthor('Mermaid Roshan story project')
    c.setSubject('34 logical book pages presented as 19 full-spread review sheets')
    layouts = []
    encoded_pictures = {}

    def base():
        c.setFillColor(cream)
        c.rect(0, 0, W, H, fill=1, stroke=0)

    def words(text, x, top, width, height, chosen=style):
        p = Paragraph(escape(text).replace('\n', '<br/>'), chosen)
        pw, ph = p.wrap(width, height)
        if ph > height:
            raise ValueError(f'Text overflow {ph} > {height}: {text}')
        p.drawOn(c, x, top - ph)
        return {'x': x, 'y': top - ph, 'width': pw, 'height': ph, 'text': text}

    def picture(path, x, y, width, height):
        key = str(path)
        if key not in encoded_pictures:
            encoded = io.BytesIO()
            with Image.open(path) as source:
                source.convert('RGB').save(encoded, format='JPEG', quality=95, subsampling=0, optimize=True)
            encoded.seek(0)
            encoded_pictures[key] = ImageReader(encoded)
        c.drawImage(encoded_pictures[key], x, y, width, height, preserveAspectRatio=True, anchor='c')

    def footer(label):
        c.setFillColor(accent)
        c.setFont('GeorgiaBook', 11)
        c.drawCentredString(W / 2, 19, label)

    # Cover: reuse ensemble city illustration, not another generation.
    base()
    c.setFillColor(ink)
    c.setFont('GeorgiaBookBold', 35)
    c.drawCentredString(W / 2, 662, 'Mermaid Roshan')
    c.setFont('GeorgiaBookBold', 29)
    c.drawCentredString(W / 2, 618, 'and the Song Beneath the Pool')
    picture(HERE / 'native/spread_02_city_beneath_pool.png', 30, 102, 940, 470)
    words("Rumi's undersea adventure", 315, 69, 380, 35, small_style)
    layouts.append({'pdf_sheet': 1, 'book_pages': [1], 'kind': 'cover'})
    c.showPage()

    base()
    c.setFillColor(ink)
    c.setFont('GeorgiaBookBold', 27)
    c.drawCentredString(W / 2, 661, 'A little voice. A whole city listening.')
    picture(HERE / 'native/cast_identity.png', 30, 170, 940, 470)
    words('Roshan joins Rumi, Hana and Nari in the city beneath Pearl Castle.\nAnd a little turtle has something important to tell them.', 120, 131, 780, 83, style)
    footer('2')
    layouts.append({'pdf_sheet': 2, 'book_pages': [2], 'kind': 'title_cast'})
    c.showPage()

    for index, spread in enumerate(PLAN['spreads']):
        base()
        art = selected_art(spread)
        if not art.exists():
            raise FileNotFoundError(art)
        picture(art, 24, 221, 952, 476)
        left = words(spread['left'], 48, 194, 438, 165)
        right = words(spread['right'], 526, 194, 426, 165)
        page = 3 + index * 2
        footer(f'{page}-{page + 1}')
        layouts.append({'pdf_sheet': index + 3, 'book_pages': [page, page + 1], 'kind': 'story_spread', 'art': art.relative_to(HERE).as_posix(), 'art_sha256': sha(art), 'text_boxes': [left, right]})
        c.showPage()

    base()
    c.setFillColor(ink)
    c.setFont('GeorgiaBookBold', 29)
    c.drawCentredString(W / 2, 663, 'Sing with me')
    picture(selected_art(PLAN['spreads'][12]), 150, 294, 700, 350)
    song_style = ParagraphStyle('Song', parent=style, fontSize=23, leading=34, alignment=1)
    words("Little voice, big blue sea.\nSing with you, sing with me.\nMake a space and let it through.\nThere's a place for me and you.", 130, 238, 740, 155, song_style)
    footer('33')
    layouts.append({'pdf_sheet': 18, 'book_pages': [33], 'kind': 'refrain'})
    c.showPage()

    base()
    c.setFillColor(ink)
    c.setFont('GeorgiaBookBold', 29)
    c.drawCentredString(W / 2, 639, 'Who will you hear?')
    picture(ROOT / 'gen2/generated/aquatic_turtle/v3.webp', 368, 313, 264, 264)
    words("Beneath Rumi's swimming pool lies a glowing mermaid city.\nBut when its song falls quiet, Roshan hears a tiny tap.\nCan four friends make room for one little voice?", 130, 263, 740, 140, style)
    words('An illustrated book draft - October 2026\nOriginal refrain and new supporting characters for this story.', 130, 72, 740, 48, small_style)
    layouts.append({'pdf_sheet': 19, 'book_pages': [34], 'kind': 'back'})
    c.showPage()
    c.save()

    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 19
    expected = [text for s in PLAN['spreads'] for text in [s['left'], s['right']]]
    for i, s in enumerate(PLAN['spreads']):
        extracted = reader.pages[i + 2].extract_text()
        normal = lambda text: re.sub(r'\s+', ' ', text).strip()
        for text in [s['left'], s['right']]:
            assert normal(text) in normal(extracted), (i, text)
    flat = [p for layout in layouts for p in layout['book_pages']]
    assert flat == list(range(1, 35))
    render_dir = ROOT / 'tmp/rumi_underpool_book_review_20261009'
    render_dir.mkdir(parents=True, exist_ok=True)
    doc = pypdfium2.PdfDocument(str(PDF))
    thumbs = []
    for i, page in enumerate(doc):
        image = page.render(scale=1.25).to_pil()
        image.save(render_dir / f'page_{i + 1:02d}.png')
        thumb = image.copy()
        thumb.thumbnail((400, 288))
        thumbs.append(thumb)
    for group_index, start in enumerate(range(0, len(thumbs), 10)):
        selected = thumbs[start:start + 10]
        sheet = Image.new('RGB', (820, ((len(selected) + 1) // 2) * 304), '#EDECF2')
        for i, thumb in enumerate(selected):
            sheet.paste(thumb, (10 + (i % 2) * 410, 8 + (i // 2) * 304))
        sheet.save(HERE / 'verification' / f'pdf_contact_{group_index + 1:02d}.png')
    record = {'result': 'PASS', 'pdf_sha256': sha(PDF), 'pdf_sheets': len(reader.pages), 'logical_book_pages': len(flat), 'story_spreads': len(PLAN['spreads']), 'all_prose_extracted_exactly': True, 'layout_overflow': False, 'rendered_pages': str(render_dir), 'layouts': layouts, 'limitations': 'Reading review, not imposed print production. All art/characters/story await owner creative review; no runtime/device/child acceptance.'}
    (HERE / 'verification/book_check.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(f'BOOK_PDF_OK sheets={len(reader.pages)} logical_pages={len(flat)} words={len(" ".join(expected).split())} sha256={record["pdf_sha256"]}')
    records()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--records-only', action='store_true')
    args = parser.parse_args()
    records() if args.records_only else build()
