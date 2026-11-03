"""Exact current cover/proof/source package and complete project-change coverage."""
from pathlib import Path
import hashlib,json,subprocess
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];BASE='2719d2fcf66afe4cb73b8445087e09dd52319849';OLD=V.parent/'v32_rainbow_story'
IMPACT=R/'design/audit_impacts/picture-book-story-covers-v33-20261017.json'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf8',stderr=subprocess.DEVNULL).splitlines()
b=read(L/'book.json');old=read(V/'BOOK_BASELINE.json');e=read(V/'generation_evidence.json');layout=read(V/'complete/page_provenance.json')
license_path=R/'ASSET_LICENSES.md';s=license_path.read_text('utf8');marker='## Chapter One static book - V33 story-faithful covers (2026-10-17)'
if marker in s:s=s[:s.index(marker)].rstrip()
rows=[marker,'','Existing owner project-art provenance/licenses remain controlling. Two built-in OpenAI ImageGen derivatives deliver only three small local polygons; no whole-scene redraw. Front removes obsolete painting cues and changes Puff facial expression; rear reuses exact authored story26 and adds a tiny canonical Lamma. Exact prompts, source/native hashes, roles and polygons: `books/chapter_one/landscape/revisions/v33_story_covers/generation_evidence.json`. Source URL: https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v33_story_covers/generation_evidence.json','']
for p in sorted(V.rglob('*')):
 if p.is_file() and p.suffix.lower() in ['.png','.jpg','.pdf']:
  note='Built-in local edit native candidate; only documented polygons exposed over preserved sources.' if p.parent.name=='art' else 'Reference-only caption-free PDF rendering; original scene/art source preserved, never delivery pixels.' if p.parent.name=='references' else 'Attributed source-derived book/review export with Sniglet. Master/PNG lossless; email RGB recompression and review-only JPEG contacts declared separately.'
  rows.append('- `'+rel(p)+'`: '+note)
license_path.write_text(s.rstrip()+'\n\n'+'\n'.join(rows)+'\n',encoding='utf8',newline='\n')
changed=set(git('diff','--name-only','HEAD'))|set(git('ls-files','--others','--exclude-standard'))
changed.update([rel(V/'manifest.json'),rel(V/'project_gates.json')]);changed.discard(rel(IMPACT))
impact=read(IMPACT);impact['files']=sorted(changed)
gates=read(V/'project_gates.json').get('checks',[])
impact['validation']=[
 dict(command='Root direct native before/after cover and email-sample review; inherited interior evidence only on32 identical PNG proofs',result='PASS',evidence=rel(V/'visual_review.json')),
 dict(command='python -B books/chapter_one/landscape/revisions/v33_story_covers/verify_revision.py',result=read(V/'complete/verification.json')['status'],evidence=rel(V/'complete/verification.json')),
 dict(command='python -B books/chapter_one/landscape/revisions/v33_story_covers/email_export.py',result=read(V/'complete/email_verification.json')['status'],evidence=rel(V/'complete/email_verification.json')),
 dict(command='python -B books/chapter_one/landscape/audit_book.py --proof V33/complete --baseline V32/complete',result=read(V/'complete/stress_results.json')['mechanical_status'],evidence=rel(V/'complete/stress_results.json')),
 dict(command='python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development',result='PASS' if len(gates)==3 and all(q['exit_code']==0 for q in gates) else 'PENDING',evidence=rel(V/'project_gates.json')),
 dict(command='Godot/import/runtime/GDScript/device gates',result='NOT_APPLICABLE',evidence='Static book cover art/layout/documentation only; no runtime, .gd, scene, save, protected original, family voice, device or release changes.')]
impact['acceptance_gaps']='Requested cover repair is reviewed; owner/child/physical-print acceptance remains open. Interior4 owner rejection remains open and is explicitly recorded; proposed replacement was not commissioned. No professional SLP review or whole-book/master-audit acceptance is claimed. Anonymous remote verification is performed after actual push.'
save(IMPACT,impact)
paths={p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
paths.update([IMPACT,license_path,R/'design/05_DOC_LEDGER.md'])
for f in ['book.json','render_book.py','audit_book.py','PAGE_PLAN.md','REVIEW.md','STORY_COMPREHENSION_AUDIT.md']:paths.add(L/f)
for f in ['README.md','DESIGN_LANGUAGE.md']:paths.add(L.parent/f)
for q in old['sources'].values():paths.add((L/q['file']).resolve())
for q in layout['layers']:paths.add((L/b['sources'][q['source_key']]['file']).resolve())
for q in e['generated']:
 for ref in q['references']:paths.add(R/ref['path'])
for p in (L/b['font']).resolve().parent.iterdir():
 if p.is_file():paths.add(p)
for p in (L.parent/'plan/reference').iterdir():
 if p.is_file() and p.suffix.lower() in ['.jpg','.png','.json']:paths.add(p)
for p in (OLD/'complete').glob('page_*.png'):paths.add(p)
for f in ['README.md','BOOK_CURRENT.json','manifest.json','visual_review.json','generation_evidence.json','complete/page_provenance.json','complete/verification.json','complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf']:paths.add(OLD/f)
for p in paths:
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt'] and (p.is_relative_to(V) or rel(p) in changed):p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
items=[]
for p in sorted(paths,key=rel):
 assert p.exists(),str(p)
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt']:data=data.replace(b'\r\n',b'\n')
 assert len(data)<100*1024*1024,rel(p)
 items.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='Current cover/native/proof/build/review evidence' if p.is_relative_to(V) else 'Exact source/font/style/baseline/authority dependency'))
payload='\n'.join(q['path']+' '+q['sha256'] for q in items).encode()
save(V/'manifest.json',dict(id='mermaid-roshan-book-v33-story-covers-20261017',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline=BASE,status='COVER_REPAIRS_REVIEWED; OWNER_CHILD_PRINT_AND_PRIOR_INTERIOR4_ITEM_OPEN',entry=rel(V/'README.md'),review=rel(V/'AUDIT_REVIEW.html'),pdf=rel(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),email_pdf=rel(V/'complete/Mermaid_Roshan_Book_V33_Email.pdf'),generated_count=2,delivered_scope='Three bounded polygons, no whole-scene replacement generation',files=items,payload_sha256=hashlib.sha256(payload).hexdigest(),hash_convention='Git LF text; native binary bytes; sorted path + space + SHA256 joined by LF, no terminal newline.',access_mode='Anonymous HTTPS at exact immutable GitHub revision; all required bytes verified after push.'))
print(json.dumps(dict(manifest_files=len(items),total_bytes=sum(q['bytes'] for q in items),impact_files=len(changed),email_bytes=read(V/'complete/email_verification.json')['output_bytes'])))
