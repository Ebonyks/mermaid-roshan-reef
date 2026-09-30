"""Refresh provenance for the separate before/after review package."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image
from pypdf import PdfReader
P=Path(__file__).resolve().parent;R=P.parents[3];REL=P.relative_to(R).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
jobs=json.loads((P/'generation_jobs.json').read_text(encoding='utf-8-sig'))
lookup={str(Path(j['generatedOriginal'])):P/j['output'] for j in jobs}
rejected={'fountain_clear':'The stream entered the cup, implying filling rather than clearing.','hug_cutout':'Superseded by edge-margin attempt.','hug_stationery':'Fountain too large for the border.'}
for j in jobs:
 j['method']='builtin OpenAI imagegen source-conditioned edit'
 j['prompt_sha256']=hashlib.sha256(j['prompt'].encode()).hexdigest()
 op=P/j['output'];im=Image.open(op)
 j['output_metadata']=dict(sha256=sha(op),bytes=op.stat().st_size,dimensions=list(im.size),mode=im.mode)
 j['disposition']='NOT_SELECTED' if j['id'] in rejected else 'REVIEW_CANDIDATE'
 j['reason']=rejected.get(j['id'],'Shown in a separate proposal; no owner or print acceptance claimed.')
 j['bound_references']=[]
 for rp in j['references']:
  rp=lookup.get(str(Path(rp)),Path(rp))
  j['bound_references'].append(dict(path=rp.relative_to(R).as_posix(),sha256=sha(rp),dimensions=list(Image.open(rp).size),role='Scene/identity authority or previous edit iteration; exact role specified in prompt.'))
(P/'generation_jobs.json').write_text(json.dumps(jobs,indent=2,ensure_ascii=False),encoding='utf8')
media=sorted(p for p in P.rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.pdf'])
lic=R/'ASSET_LICENSES.md';s=lic.read_text(encoding='utf8');mark='## Picture-book before/after proposals — 2026-09-30'
suffix=''
if mark in s:
 start=s.index(mark);end=s.find('\n## ',start+len(mark))
 suffix=s[end:] if end>=0 else ''
 s=s[:start].rstrip()
rows=[mark,'','Owner/project art rights and source provenance remain controlling. No external stock or newly inferred license. Exact sources, prompts, hashes and modifications: `books/chapter_one/previews/2026-09-30/generation_jobs.json` and `layout_evidence.json`. Originals and native outputs preserved; review proposals only.','']
for p in media:
 kind=p.parent.name
 desc={'art':'Builtin OpenAI source-conditioned edit, native output retained; exact sources and disposition in generation_jobs.json.',
 'before':'Unmodified whole-page V27 proof PNG copied byte-for-byte; existing project art/font provenance.',
 'after':'Lossless whole-page document screenshot at144dpi of native Sniglet/layout and source-conditioned derivatives; review only.',
 'comparisons':'Lossless review-sheet screenshot of V27/proposed pages or pagination diagrams; whole-page comparisons, not new narrative art.'}.get(kind,'ReportLab review PDF: existing/project art, source-conditioned derivatives and live Sniglet type; no print-master claim.')
 rows.append('- `'+p.relative_to(R).as_posix()+'`: '+desc)
lic.write_text(s.rstrip()+'\n\n'+'\n'.join(rows)+'\n'+suffix,encoding='utf8')
led=R/'design/05_DOC_LEDGER.md';s=led.read_text(encoding='utf8')
if REL+'/README.md' not in s:
 s+='\n| `'+REL+'/README.md` | 🟣 | `CANDIDATE`; ten separate before/after proposals and two pagination diagrams responding to the V27 review. Source/prompt/layout evidence; current book unchanged. No whole-book, child, print or owner acceptance. |\n'
 led.write_text(s,encoding='utf8')
preserved=[]
for name in ['book.json','render_book.py']:
 rp='books/chapter_one/landscape/'+name
 raw=subprocess.check_output(['git','show','7f6452aee60a6173034ca0df4b0b6a40893ef567:'+rp],cwd=R)
 local=(R/rp).read_bytes()
 preserved.append(dict(path=rp,git_blob_sha256=hashlib.sha256(raw).hexdigest(),working_file_sha256=sha(R/rp),content_unchanged=raw.replace(b'\r\n',b'\n')==local.replace(b'\r\n',b'\n'),note='Git LF versus Windows checkout CRLF; content compared after newline normalization.'))
for r in preserved:assert r['content_unchanged']
layout=json.loads((P/'layout_evidence.json').read_text(encoding='utf8'))
reader=PdfReader(P/'BEFORE_AFTER.pdf');assert len(reader.pages)==12
assert len(list((P/'after').glob('*.png')))==10
for p in (P/'after').glob('*.png'):assert Image.open(p).size==(1008,720)
for layer in layout['layers']:assert sha(R/layer['path'])==layer['sha256']
verification=dict(status='MECHANICAL_CHECKS_PASS_VISUAL_PROPOSALS_PENDING_OWNER',current_book_preserved=preserved,
 source_pdf_sha256='be69cff6e2be12b9d2cdb3665613e3b07ba6ab6323e1ae20b79cce22c701442d',
 source_revision='f857a65e95d5d7846af19f27046735a74cba4ec4',
 source_total_pages=34,comparison_pdf_pages=12,proposed_story_pages=10,
 native_type_minimum_points=min(x['size'] for x in layout['text_lines']),
 after_screenshots=dict(dimensions=[1008,720],format='lossless PNG',render_dpi=144),
 text_checks='Builder asserts each line fits its declared width and18pt page-edge clearance.',
 visual_review='All ten proposed pages and both page-turn sheets inspected. Native text render mode, closing eyeline, balloon-tail anchor, craft caption and diagram spacing corrected following render.',
 qualifications=['Separate proposals; unshown comprehensive-review queue remains open.',
 'Generated edits are source-conditioned, not guaranteed pixel-exact extractions.',
 'S19 proposed speaking figures exceed the existing bottom20% dialogue zone; layout acceptance pending.',
 'S15 fountain starts around82% height, slightly above the bottom15% decorative zone; final placement/occlusion remains open.',
 'S15 tiny upper hair contour needs final print-size inspection.',
 'S27 upper-only ceiling extension retains original lower scene; junction/perspective remains a print-review item.',
 'Only one hidden Lamb-a location shown. Other one/two locations and child discovery untested.',
 '1484x1060 scene outputs are approximately212ppi at7x5, not certified300ppi print masters.',
 'No actual re-pagination, full-book language rewrite, runtime changes or finding closure.'])
(P/'verification.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False),encoding='utf8')
payload=[]
for p in sorted(P.rglob('*')):
 if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts:
  payload.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size))
manifest=dict(id='picture-book-before-after-20260930-v1',status='VISUAL_PROPOSALS_NOT_APPLIED',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='7f6452aee60a6173034ca0df4b0b6a40893ef567',entry=REL+'/README.md',gallery=REL+'/PREVIEWS.html',recipient_access_required='Anonymous HTTPS read of exact revision',files=payload)
manifest['sorted_payload_sha256']=hashlib.sha256(('\n'.join(x['path']+' '+x['sha256'] for x in payload)).encode()).hexdigest()
(P/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
ip=R/'design/audit_impacts/picture-book-before-after-20260930.json';impact=json.loads(ip.read_text(encoding='utf-8-sig'))
impact['files']=[p.relative_to(R).as_posix() for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]+['ASSET_LICENSES.md','design/05_DOC_LEDGER.md']
impact['validation']=[
 dict(command='build_previews.py; build_evidence.py; full rendered-page visual inspection',result='PASS',evidence=REL+'/verification.json and layout_evidence.json. Mechanical/preview checks only; qualifications retained.'),
 dict(command='python -B tools/audit_document_authority.py',result='PENDING',evidence='Run after finalized payload.'),
 dict(command='python -B tools/audit_development.py --base auto',result='PENDING',evidence='Run after finalized impact coverage.'),
 dict(command='Game import/probes',result='NOT_APPLICABLE',evidence='Static book proposals only; no runtime assets/scripts changed.')]
impact['acceptance_gaps']='Separate proposals, not a completed revised book. S15 contour/decoration placement, S19 larger speaking-figure exception, S27 ceiling junction, generated identity, print resolution, child discovery and the remaining comprehensive-review queue stay open.'
ip.write_text(json.dumps(impact,indent=2),encoding='utf8')
print(json.dumps(dict(media_files=len(media),payload_files=len(payload),payload_bytes=sum(x['bytes'] for x in payload),source_hashes_unchanged=True)))
