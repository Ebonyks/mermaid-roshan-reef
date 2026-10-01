"""Package current exact sources/review/proof and cover every changed file."""
from pathlib import Path
import hashlib,json,subprocess
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
BASE='19ee6ce8ec4c20c05714f101d0d222a33477e400'
IMPACT=R/'design/audit_impacts/picture-book-story-clarity-v31-20260930.json'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf8').splitlines()
B=read(L/'book.json');layout=read(V/'complete/page_provenance.json');old=read(V/'BOOK_BASELINE.json');e=read(V/'generation_evidence.json')
license_path=R/'ASSET_LICENSES.md';content=license_path.read_text('utf8');marker='## Chapter One static book - V31 story clarity (2026-09-30)'
if marker in content:content=content[:content.index(marker)].rstrip()+'\n'
rows=[marker,'','Owner-supplied project artwork and existing license/provenance remain controlling. Five built-in OpenAI image_gen local derivatives repair named gaps only; original scene art and protected originals are unchanged. Exact prompts, reference/native hashes, bounded delivery masks and candidate-versus-delivered scope are in `books/chapter_one/landscape/revisions/v31_story_clarity/generation_evidence.json`. Source URL: https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v31_story_clarity/generation_evidence.json','']
for p in sorted(V.rglob('*')):
 if not p.is_file() or p.suffix.lower() not in ['.png','.jpg','.pdf'] or '.optimized.' in p.name:continue
 note='Built-in source-conditioned local derivative; delivered only through documented polygons over intact source base.' if p.parent.name=='art' else 'Rendered static proof/review from attributed artwork and embedded Sniglet; PNG/PDF lossless, JPEG contacts review-only.'
 rows.append('- `'+rel(p)+'`: '+note)
license_path.write_text(content.rstrip()+'\n\n'+'\n'.join(rows)+'\n',encoding='utf8',newline='\n')
changed=set(git('diff','--name-only','HEAD'))|set(git('ls-files','--others','--exclude-standard'))
changed.add(rel(V/'manifest.json'));changed.add(rel(V/'project_gates.json'));changed.discard(rel(IMPACT))
validation=[dict(command='Independent exact-hash native character/style/language review of five changed pages and29 identical V30 pages',result='PASS' if all((V/f).exists() for f in ['character_final.json','style_final.json','language_final.json','visual_review.json']) else 'PENDING',evidence=rel(V/'visual_review.json')),dict(command='python -B books/chapter_one/landscape/revisions/v31_story_clarity/verify_revision.py',result='PASS' if read(V/'complete/verification.json').get('lossless_pdf_raster_matches_all34screenshots') else 'PENDING',evidence=rel(V/'complete/verification.json')),dict(command='python -B books/chapter_one/landscape/audit_book.py --proof V31/complete --baseline V30/complete',result='PASS' if (V/'complete/stress_results.json').exists() and read(V/'complete/stress_results.json')['mechanical_status']=='PASS' else 'PENDING',evidence=rel(V/'complete/stress_results.json')),dict(command='python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development',result='PASS' if (V/'project_gates.json').exists() and all(q['exit_code']==0 for q in read(V/'project_gates.json')['checks']) else 'PENDING',evidence=rel(V/'project_gates.json')),dict(command='Godot import/probes/device and GDScript parser/inference',result='NOT_APPLICABLE',evidence='Only static book art/manuscript/layout/docs/evidence. No runtime, .gd, scene, save, family voice or protected-original changes.')]
save(IMPACT,dict(id='picture-book-story-clarity-v31-20260930',scope=read(V/'REVISION_SCOPE.json')['scope'],baseline=BASE,rules=read(V/'REVISION_SCOPE.json')['rules'],findings=[],no_findings_reason='Owner-directed static-book comprehension and mood corrections; no canonical game finding or game-wide closure.',files=sorted(changed),validation=validation,acceptance_gaps='Subjective internal craft findings are separate from owner/child enjoyable reading, qualified SLP and physical-print acceptance; those remain open. No runtime/device/release work commissioned.'))
paths={p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts and '.optimized.' not in p.name}
paths.add(IMPACT);paths.add(license_path);paths.add(R/'design/05_DOC_LEDGER.md')
for f in ['book.json','render_book.py','audit_book.py','PAGE_PLAN.md','REVIEW.md','STORY_COMPREHENSION_AUDIT.md']:paths.add(L/f)
for f in ['README.md','DESIGN_LANGUAGE.md']:paths.add(L.parent/f)
for layer in layout['layers']:paths.add((L/B['sources'][layer['source_key']]['file']).resolve())
OLD=V.parent/'v30_identity'
for layer in read(OLD/'complete/page_provenance.json')['layers']:paths.add((L/old['sources'][layer['source_key']]['file']).resolve())
for p in (OLD/'complete').glob('page_*.png'):paths.add(p)
for f in ['README.md','BOOK_CURRENT.json','visual_review.json','character_final.json','style_final.json','language_final.json','generation_evidence.json','complete/page_provenance.json','complete/verification.json','manifest.json']:paths.add(OLD/f)
for row in e['generated']:
 for ref in row['references']:paths.add(R/ref['path'])
for p in (L/B['font']).resolve().parent.iterdir():
 if p.is_file():paths.add(p)
for p in (L.parent/'plan/reference').iterdir():
 if p.is_file() and p.suffix.lower() in ['.jpg','.png','.json']:paths.add(p)
# Durable language-packet guidance/review links use these historical JSONs.
for f in ['language_audit.json','manuscript_qa.json','language_round2.json','style_final.json']:paths.add(V.parent/'v29_polish'/f)
for p in paths:
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt'] and (p.is_relative_to(V) or rel(p) in changed):p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
items=[]
for p in sorted(paths,key=rel):
 assert p.exists(),str(p)
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt']:data=data.replace(b'\r\n',b'\n')
 assert len(data)<100*1024*1024,rel(p)+' exceeds GitHub individual-file limit'
 items.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='Current proof/native/review/build evidence' if p.is_relative_to(V) else 'Exact source/font/baseline/style/authority dependency'))
payload='\n'.join(q['path']+' '+q['sha256'] for q in items).encode()
save(V/'manifest.json',dict(id='mermaid-roshan-book-v31-story-clarity-20260930',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline=BASE,status='COMPLETE_REVIEW_PROOF; OWNER_CHILD_PRINT_SLP_ACCEPTANCE_PENDING',entry=rel(V/'README.md'),review=rel(V/'AUDIT_REVIEW.html'),pdf=rel(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),generation_candidates=e['generated_count'],selected_local_derivatives=e['selected_candidate_count'],files=items,payload_sha256=hashlib.sha256(payload).hexdigest(),hash_convention='Git LF text; original binary bytes; sorted path + space + SHA256 joined by LF, no terminal newline.',access_mode='Anonymous HTTPS raw GitHub at exact published revision; verify remote manifest and all required files after push.'))
print(json.dumps(dict(manifest_files=len(items),manifest_bytes=sum(q['bytes'] for q in items),impact_files=len(changed),pdf_sha256=sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))))
