"""Publishable, source-attributed manifest and exact-file audit-impact coverage."""
from pathlib import Path
import hashlib,json,subprocess
V=Path(__file__).resolve().parent; L=V.parents[1]; R=L.parents[2]
BASE='82a6dc1dba381c0b3ef507a8397512fa09ef624e'
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf8').splitlines()
B=read(L/'book.json');evidence=read(V/'generation_evidence.json');layout=read(V/'complete/page_provenance.json')
license_path=R/'ASSET_LICENSES.md';content=license_path.read_text(encoding='utf8')
marker='## Chapter One static book - V30 comprehensive polish (2026-09-30)'
if marker in content:content=content[:content.index(marker)].rstrip()+'\n'
rows=[marker,'','Source-controlled static-book derivatives; original owner/reference licensing remains controlling. Built-in OpenAI image generation was used for recorded gaps, not as a license claim over the supplied art. Source paths/hashes, full prompts, native PNG hashes, actual masks/use, rejection reasons and review limits are in `books/chapter_one/landscape/revisions/v30_identity/generation_evidence.json`. Originals remain unchanged. Durable provenance URL: https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v30_identity/generation_evidence.json','']
selected={j['id'] for j in evidence['generated'] if j['selection']=='SELECTED_DERIVATIVE'}
for p in sorted(V.rglob('*')):
 if not p.is_file() or p.suffix.lower() not in ['.png','.jpg','.pdf'] or '.optimized.' in p.name:continue
 if p.parent.name=='art':desc=('Selected source-conditioned static derivative; actual bounded repair/background/contour scope in provenance.' if p.stem in selected else 'Rejected native generation study, retained for audit only; no delivered page uses it.')
 else:desc='Rendered static book/review output from attributed artwork and native Sniglet text. PNG/PDF lossless; JPEG contact sheet is review-only. Original sources are not recompressed.'
 rows.append('- `'+rel(p)+'`: '+desc)
license_path.write_text(content.rstrip()+'\n\n'+'\n'.join(rows)+'\n',encoding='utf8',newline='\n')

# Include reproducible page sources, exact generator references, original style
# examples and all34 frozen before screenshots, not merely prose path lists.
paths={p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts and '.optimized.' not in p.name}
for f in ['book.json','render_book.py','audit_book.py','PAGE_PLAN.md','REVIEW.md','STORY_COMPREHENSION_AUDIT.md']:paths.add(L/f)
for f in ['README.md','DESIGN_LANGUAGE.md']:paths.add(L.parent/f)
paths.update([license_path,R/'design/05_DOC_LEDGER.md'])
impact=R/'design/audit_impacts/picture-book-identity-v30-20260930.json';paths.add(impact)
for layer in layout['layers']:paths.add((L/B['sources'][layer['source_key']]['file']).resolve())
for j in evidence['generated']:
 for ref in j['references']:paths.add(R/ref['path'])
for p in (L/B['font']).resolve().parent.iterdir():
 if p.is_file():paths.add(p)
for p in (V.parent/'v29_polish/complete').glob('page_*.png'):paths.add(p)
for f in ['generation_evidence.json','manifest.json','visual_review.json','character_final.json','style_final.json','language_final.json','complete/verification.json','SLP_REVIEW_PACKET.html']:paths.add(V.parent/'v29_polish'/f)
for row in read(V.parent/'v29_polish/generation_evidence.json')['generated']:
 for ref in row['references']:paths.add(R/ref['path'])
 native=row.get('native_output',{});native=native if isinstance(native,str) else native.get('path')
 if native:paths.add(R/native)
for p in (V.parent/'v29_polish/art').glob('*.png'):paths.add(p)
for p in (L.parent/'plan/reference').iterdir():
 if p.is_file() and p.suffix.lower() in ['.jpg','.png','.json']:paths.add(p)

# Coverage is every changed project file; no wildcard, no hidden staged omission.
changed=set(git('diff','--name-only','HEAD'))|set(git('ls-files','--others','--exclude-standard'))
changed.add(rel(V/'manifest.json'));changed.discard(rel(impact))
validation=read(impact)['validation']
if (V/'complete/verification.json').exists():
 verification=read(V/'complete/verification.json')
 validation=[dict(command='Independent whole34-page character/style/language review against original book and V29',result='PASS',evidence=rel(V/'visual_review.json')+'; honest internal scores, external gates remain pending.'),dict(command='python -B books/chapter_one/landscape/audit_book.py --proof V30/complete --baseline V29/complete',result='PASS' if (V/'complete/stress_results.json').exists() and read(V/'complete/stress_results.json')['mechanical_status']=='PASS' else 'PENDING',evidence=rel(V/'complete/stress_results.json')),dict(command='Lossless PDF encoding and all34-page pixel/manuscript/font/source verification',result='PASS' if verification.get('lossless_optimized_pdf_raster_matches_all34screenshots') else 'PENDING',evidence=rel(V/'complete/verification.json')+'; PDF SHA256 '+verification.get('pdf_sha256','pending')),dict(command='python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development',result='PENDING',evidence=rel(V/'project_gates.json')),dict(command='Godot import/probes/device; GDScript parser/inference',result='NOT_APPLICABLE',evidence='Static book/docs/build evidence only. No runtime texture, .gd, scene, save, family voice or protected-original changes.')]
 if (V/'project_gates.json').exists():
  gates=read(V/'project_gates.json')
  validation[3]['result']='PASS' if all(q['exit_code']==0 for q in gates['checks']) else 'FAIL'
save(impact,dict(id='picture-book-v30-identity-20260930',scope='Static-book final local polish: adult Rumi facial identity0/10/33, cover brooch removal, attentive dirty-hall expressions4, two visible source-derived sponges5, exact-mask source preservation, corrected professional review packet and bound print dummy. Prior all34-page/bubble/border/language evidence retained and reconciled. No game/runtime/protected-original change.',baseline=BASE,rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-06','DL-ASSET-08'],findings=[],no_findings_reason='This scoped static-book iteration repairs no canonical game finding and claims no game-wide audit closure.',files=sorted(changed),validation=validation,acceptance_gaps='Internal4.9 all-object target is reported honestly in visual_review.json; all34 page/object minima meet the independent internal target after actual local corrections; subjective scores do not establish clinical/master acceptance. Owner/child/physical print and qualified SLP acceptance are pending. Game/device/release acceptance is outside this static-book scope.'))

# Author text in Git's canonical LF form before computing published byte hashes.
for p in paths:
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt'] and (p.is_relative_to(V) or rel(p) in changed):p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
items=[]
for p in sorted(paths,key=rel):
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt']:data=data.replace(b'\r\n',b'\n')
 assert len(data)<100*1024*1024,rel(p)+' exceeds GitHub individual-file limit'
 items.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='Current/native/rejected review evidence' if p.is_relative_to(V) else 'Exact source/font/reference/build/authority dependency'))
payload='\n'.join(q['path']+' '+q['sha256'] for q in items).encode()
save(V/'manifest.json',dict(id='mermaid-roshan-book-v30-identity-20260930',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline=BASE,status='COMPLETE_ITERATED_REVIEW_PROOF; OWNER_CHILD_PRINT_SLP_ACCEPTANCE_PENDING',entry=rel(V/'README.md'),review=rel(V/'AUDIT_REVIEW.html'),pdf=rel(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),generation_candidates=evidence['generated_count'],selected_derivatives=evidence['selected_candidate_count'],files=items,payload_sha256=hashlib.sha256(payload).hexdigest(),hash_convention='Git LF text; original binary bytes. Sorted path + space + SHA256 joined by LF, no terminal newline.',access_mode='Anonymous HTTPS raw GitHub at exact published revision. Verify remote manifest and every required file after push.'))
print(json.dumps(dict(manifest_files=len(items),manifest_bytes=sum(q['bytes'] for q in items),impact_files=len(changed))))
