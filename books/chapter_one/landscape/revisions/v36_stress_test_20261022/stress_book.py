"""Read-only book stress checks. Writes reports here and diagnostics under tmp/."""
from pathlib import Path
import contextlib, hashlib, io, json, re, subprocess, time
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
import pypdfium2 as pdfium

S = Path(__file__).resolve().parent
L = S.parents[1]
R = L.parents[2]
V = S.parent / 'v36_next_draft'
C = V / 'complete'
N = S.parent / 'v36_rear_composition_20261021'
T = R / 'tmp/pdfs/v36_stress_20261022'
T.mkdir(parents=True, exist_ok=True)

def read(p):
	return json.loads(p.read_text('utf8'))

def sha(p):
	return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, value):
	p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

b = read(L / 'book.json')
prov = read(C / 'page_provenance.json')
pdf_path = C / 'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'
email_path = C / 'Mermaid_Roshan_Book_V36_Email.pdf'
sealed = {p: sha(p) for p in [L / 'book.json', pdf_path, email_path]}
results = {'baseline': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip(), 'review_date': '2026-10-22', 'scope': 'Published V36 book plus new rear candidate; no art or manuscript edits.'}

# Execute the existing strict gate unchanged except for report destinations.
source = (V / 'verify_revision.py').read_text('utf8')
source = source.replace("save(V/'composed_caption_contrast.json'", "save(S/'composed_caption_contrast.json'")
source = source.replace("(V/'composed_caption_contrast.tsv')", "(S/'composed_caption_contrast.tsv')")
source = source.replace("save(C/'verification.json'", "save(S/'regression_verification.json'")
namespace = {'__file__': str(V / 'verify_revision.py'), 'S': S}
log = io.StringIO()
with contextlib.redirect_stdout(log):
	exec(compile(source, str(V / 'verify_revision.py'), 'exec'), namespace)
(S / 'regression_stdout.txt').write_text(log.getvalue(), encoding='utf8')
results['strict_regression'] = read(S / 'regression_verification.json')['status']

# Reopen both actual PDFs, compare text, page content, trim and native images.
master = PdfReader(pdf_path)
email = PdfReader(email_path)
image_checks = 0
mask_checks = 0
start = time.perf_counter()
doc = pdfium.PdfDocument(str(pdf_path))
edoc = pdfium.PdfDocument(str(email_path))
psnr = []
for n, (a, e) in enumerate(zip(master.pages, email.pages)):
	assert a.mediabox == e.mediabox
	assert a.extract_text() == e.extract_text()
	assert a.get_contents().get_data() == e.get_contents().get_data()
	for key in a['/Resources'].get('/XObject', {}):
		x = a['/Resources']['/XObject'][key].get_object()
		y = e['/Resources']['/XObject'][key].get_object()
		if x.get('/Subtype') != '/Image':
			continue
		assert (x['/Width'], x['/Height']) == (y['/Width'], y['/Height'])
		image_checks += 1
		if x.get('/SMask'):
			assert x['/SMask'].get_object().get_data() == y['/SMask'].get_object().get_data()
			mask_checks += 1
	aa = np.asarray(doc[n].render(scale=1).to_pil().convert('RGB'), dtype=float)
	ee = np.asarray(edoc[n].render(scale=1).to_pil().convert('RGB'), dtype=float)
	mse = float(np.mean((aa - ee) ** 2))
	psnr.append(100 if mse == 0 else float(10 * np.log10(255 ** 2 / mse)))
results['email'] = dict(pages=len(email.pages), bytes=email_path.stat().st_size, under_25_decimal_MB=email_path.stat().st_size <= 25000000, vector_text_content_trim_exact=True, native_image_placements=image_checks, decoded_alpha_masks_exact=mask_checks, minimum_psnr_db=min(psnr), all_psnr_over_40=all(v >= 40 for v in psnr))
results['pdf'] = dict(pages=len(master.pages), story_pages=len(b['pages']), dimensions_points=list(master.pages[0].mediabox), lossless_bytes=pdf_path.stat().st_size, rendered_all_pages=True, render_and_email_comparison_seconds=round(time.perf_counter()-start, 2), encrypted=master.is_encrypted)

# Do not call the logical 20pt design size physical 20pt in the 2x review PDF.
font_counts = Counter((q['font_size'], q['physical_font_size']) for q in prov['text_lines'])
words = []
for p in b['pages']:
	word_count = len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", p['text']))
	words.append(dict(page=p['page'], words=word_count, text=p['text']))
results['text'] = dict(total_story_words=sum(p['words'] for p in words), longest_pages=sorted(words, key=lambda p:p['words'], reverse=True)[:8], line_count=len(prov['text_lines']), logical_and_physical_font_counts=[dict(logical_pt=a, physical_review_pt=z, lines=k) for (a,z),k in sorted(font_counts.items())], editorial_limit='Word counts are descriptive; no clinical reading-level or SLP claim.')

# Real source pixels per inch at current physical placement, without print upscale.
ppi = []
for q in prov['layers']:
	if q['role'] not in ['story_art', 'full_art'] and not q['role'].startswith('full'):
		continue
	box = q.get('target_box_points')
	crop = q.get('source_box_pixels') or q.get('source_box')
	path = L / b['sources'][q['source_key']]['file']
	im = Image.open(path)
	if not box or box[2] == 0 or box[3] == 0:
		continue
	w, h = (crop[2]-crop[0], crop[3]-crop[1]) if crop else im.size
	ppi.append(dict(page=q['page'], source=q['source_key'], role=q['role'], native_size=list(im.size), effective_ppi_at_14x10=round(min(w/(box[2]*2/72), h/(box[3]*2/72)), 1)))
results['resolution'] = dict(placements=ppi, below_1800_bath_native_height=Image.open(L/b['sources']['v36_bath_candidate']['file']).height < 1800, bath_native_size=list(Image.open(L/b['sources']['v36_bath_candidate']['file']).size), print_limit='Current review size only; final trim not chosen; no universal PPI acceptance asserted.')

# Candidate rear is outside the actual PDF source graph.
used = {q['source_key'] for q in prov['layers']}
candidate_hash = sha(N / 'rear_scene_attempt1.png')
integrated = any(sha(L / b['sources'][k]['file']) == candidate_hash for k in used)
results['rear'] = dict(candidate_in_actual_book=integrated, existing_rear_reuses_story=b['back_cover'].get('story_scene_page'), candidate_sha256=candidate_hash, candidate_native_size=list(Image.open(N/'rear_scene_attempt1.png').size), latest_direction='New scene requested 2026-10-21; source reuse at story3 remains in current V36 PDF.')

# Contact sheets are review diagnostics, never authored art or delivery pixels.
for group in range(5):
	numbers = list(range(group*8, min(34, group*8+8)))
	canvas = Image.new('RGB', (2016, 2*390), '#e9f3f7')
	draw = ImageDraw.Draw(canvas)
	for i, n in enumerate(numbers):
		im = doc[n].render(scale=.5).to_pil().convert('RGB')
		canvas.paste(im, ((i%4)*504, (i//4)*390+24))
		draw.text(((i%4)*504+8, (i//4)*390+5), 'Cover' if n==0 else 'Rear' if n==33 else f'Story {n}', fill='black')
	canvas.save(T / f'contact_{group}.png')
for n in [3,4,7,9,14,16,19,20,22,23,25,28,29,33]:
	im = doc[n].render(scale=1).to_pil().convert('RGB')
	im.save(T/f'reading_{n:02}.png')
	# A 1280x720 landscape display letterboxes the14x10page to1008x720.
	assert im.size == (1008,720)

# Snapshot hashes remain exact after all tests.
assert all(sha(p) == h for p,h in sealed.items())
results['source_documents_unchanged'] = {p.relative_to(R).as_posix(): h for p,h in sealed.items()}
save(S / 'machine_results.json', results)
print(json.dumps({k:v for k,v in results.items() if k not in ['resolution','text','source_documents_unchanged']}, indent=2))
