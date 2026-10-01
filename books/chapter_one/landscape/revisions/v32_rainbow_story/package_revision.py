"""Package exact current sources/proof and every changed project file."""
from pathlib import Path
import hashlib,json,subprocess
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
BASE='07734bb43018ffdefef3644f337db8fa46038d5b'
IMPACT=R/'design/audit_impacts/picture-book-rainbow-story-v32-20261001.json'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf8').splitlines()
B=read(L/'book.json');layout=read(V/'complete/page_provenance.json');old=read(V/'BOOK_BASELINE.json');e=read(V/'generation_evidence.json')
license_path=R/'ASSET_LICENSES.md';content=license_path.read_text('utf8');marker='## Chapter One static book - V32 magical rainbow story (2026-10-01)'
if marker in content:content=content[:content.index(marker)].rstrip()+'\n'
rows=[marker,'','Owner-supplied project artwork and existing license/provenance remain controlling. Five built-in OpenAI image_gen calls address named static-book local gaps; four delivered components, including a chest source clipped at document level. Two chest candidates are rejected as clean standalone alpha masters; the second is not delivered. No full-scene redraw or protected-original edit. Exact prompts, source/native hashes, delivery scope and native limitations: `books/chapter_one/landscape/revisions/v32_rainbow_story/generation_evidence.json`. Source URL: https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v32_rainbow_story/generation_evidence.json','']
for p in sorted(V.rglob('*')):
 if not p.is_file() or p.suffix.lower() not in ['.png','.jpg','.pdf'] or '.optimized.' in p.name:continue
 note='Built-in source-conditioned local derivative or rejected candidate; originals/native bytes preserved. Delivered only through the declared alpha/contour or local polygons, per evidence.' if p.parent.name=='art' else 'Static rendered proof/review from attributed project artwork and embedded Sniglet; PNG/PDF lossless, JPEG contacts review-only.'
 rows.append('- `'+rel(p)+'`: '+note)
license_path.write_text(content.rstrip()+'\n\n'+'\n'.join(rows)+'\n',encoding='utf8',newline='\n')
changed=set(git('diff','--name-only','HEAD'))|set(git('ls-files','--others','--exclude-standard'))
changed.update([rel(V/'manifest.json'),rel(V/'project_gates.json')]);changed.discard(rel(IMPACT))
validation=[
 dict(command='Independent exact-hash native character/style/language review: six changed pages,28 explicit mapped identical V31 proofs, all32 captions',result='PASS' if (V/'visual_review.json').exists() and read(V/'visual_review.json').get('open_findings')==[] else 'PENDING',evidence=rel(V/'visual_review.json')),
 dict(command='python -B books/chapter_one/landscape/revisions/v32_rainbow_story/verify_revision.py',result='PASS' if read(V/'complete/verification.json').get('lossless_pdf_raster_matches_all34screenshots') else 'PENDING',evidence=rel(V/'complete/verification.json')),
 dict(command='python -B books/chapter_one/landscape/audit_book.py --proof V32/complete --baseline V31/complete',result='PASS' if read(V/'complete/stress_results.json')['mechanical_status']=='PASS' else 'PENDING',evidence=rel(V/'complete/stress_results.json')),
 dict(command='python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development',result='PASS' if (V/'project_gates.json').exists() and all(q['exit_code']==0 for q in read(V/'project_gates.json')['checks']) else 'PENDING',evidence=rel(V/'project_gates.json')),
 dict(command='Godot import/probes/device and GDScript parser/inference',result='NOT_APPLICABLE',evidence='Static book art/manuscript/layout/docs/evidence only. No runtime, .gd, scene, save, family voice or protected-original changes.')]
save(IMPACT,dict(id='picture-book-rainbow-story-v32-20261001',scope=read(V/'REVISION_SCOPE.json')['scope'],baseline=BASE,rules=read(V/'REVISION_SCOPE.json')['rules'],findings=[],no_findings_reason='Owner-directed static-book magic-water clarification and page-space/pacing refinement; no canonical game finding or game-wide closure.',files=sorted(changed),validation=validation,acceptance_gaps='Subjective internal craft findings are separate from owner/child enjoyable shared reading, qualified SLP and physical-print acceptance, which remain open. No runtime/device/release work commissioned.'))
paths={p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts and '.optimized.' not in p.name}
paths.update([IMPACT,license_path,R/'design/05_DOC_LEDGER.md'])
for f in ['book.json','render_book.py','audit_book.py','PAGE_PLAN.md','REVIEW.md','STORY_COMPREHENSION_AUDIT.md']:paths.add(L/f)
for f in ['README.md','DESIGN_LANGUAGE.md']:paths.add(L.parent/f)
for layer in layout['layers']:paths.add((L/B['sources'][layer['source_key']]['file']).resolve())
OLD=V.parent/'v31_story_clarity'
# Verifier seals all registered source files, even currently unused approved alternatives.
for source in old['sources'].values():paths.add((L/source['file']).resolve())
for p in (OLD/'complete').glob('page_*.png'):paths.add(p)
for f in ['README.md','BOOK_CURRENT.json','visual_review.json','character_final.json','style_final.json','language_final.json','generation_evidence.json','complete/page_provenance.json','complete/verification.json','manifest.json']:paths.add(OLD/f)
for row in e['generated']:
 for q in row['references']:paths.add(R/q['path'])
for p in (L/B['font']).resolve().parent.iterdir():
 if p.is_file():paths.add(p)
for p in (L.parent/'plan/reference').iterdir():
 if p.is_file() and p.suffix.lower() in ['.jpg','.png','.json']:paths.add(p)
for f in ['language_audit.json','manuscript_qa.json','language_round2.json','style_final.json']:paths.add(V.parent/'v29_polish'/f)
# Referenced identity/style/proof evidence must be durable, not a local-only pointer.
for audit in [read(V/'character_final.json'),read(V/'style_final.json'),read(V/'language_final.json')]:
 def gather(obj):
  if isinstance(obj,dict):
   for k,v in obj.items():
    if isinstance(v,str) and v.startswith(('books/','assets_src/')) and (R/v).is_file():paths.add(R/v)
    else:gather(v)
  elif isinstance(obj,list):
   for q in obj:gather(q)
 gather(audit)
for p in paths:
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt'] and (p.is_relative_to(V) or rel(p) in changed):p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
items=[]
for p in sorted(paths,key=rel):
 assert p.exists(),str(p)
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt']:data=data.replace(b'\r\n',b'\n')
 assert len(data)<100*1024*1024,rel(p)+' exceeds GitHub single-file limit'
 items.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='Current proof/native/review/build evidence' if p.is_relative_to(V) else 'Exact source/font/baseline/style/authority dependency'))
payload='\n'.join(q['path']+' '+q['sha256'] for q in items).encode()
save(V/'manifest.json',dict(id='mermaid-roshan-book-v32-rainbow-story-20261001',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline=BASE,status='COMPLETE_REVIEW_PROOF; OWNER_CHILD_PRINT_SLP_ACCEPTANCE_PENDING',entry=rel(V/'README.md'),review=rel(V/'AUDIT_REVIEW.html'),pdf=rel(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),generation_calls=e['generated_count'],delivered_components=e['selected_delivery_components'],rejected_standalone_alpha_candidates=e['rejected_standalone_alpha_candidates'],files=items,payload_sha256=hashlib.sha256(payload).hexdigest(),hash_convention='Git LF text; original binary bytes; sorted path + space + SHA256 joined by LF, no terminal newline.',access_mode='Anonymous HTTPS raw GitHub at exact published revision; verify remote manifest and every required file after push.'))
print(json.dumps(dict(manifest_files=len(items),manifest_bytes=sum(q['bytes'] for q in items),impact_files=len(changed),pdf_sha256=sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))))
