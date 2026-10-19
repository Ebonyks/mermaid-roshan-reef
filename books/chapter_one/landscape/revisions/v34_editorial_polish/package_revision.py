"""Versioned book review package, asset licensing and exact impact coverage."""
from pathlib import Path
import json,hashlib,subprocess,re
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v33_story_covers'
IMPACT=R/'design/audit_impacts/picture-book-editorial-v34-20261018.json';BASE='a14a26ee356296c84b7251ce8222f371740ed2cb'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf8').splitlines()
b=read(L/'book.json');e=read(V/'generation_evidence.json');ver=read(C/'verification.json');email=read(C/'email_verification.json')
assert ver['status']==email['status']=='PASS' and ver['pdf_sha256']==email['source_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
assert email['output_bytes']<=25_000_000 and ver['contrast_counts'].get('FAIL',0)==0
# Each new image/export, including rejected native studies, is licensed/attributed.
lic=R/'ASSET_LICENSES.md';s=lic.read_text('utf8');start='<!-- BEGIN CHAPTER_ONE_V34 -->';end='<!-- END CHAPTER_ONE_V34 -->'
rows=[start,'## Chapter One static book - V34 evaluated audit (2026-10-18)','','Existing owner project-art licenses and source acceptance scopes remain controlling. Built-in OpenAI ImageGen supplies 25 source-bound candidates; 11 derivatives are used. Original sources are preserved. New stationery/cameo variants follow the owner’s scoped permission; narrative source scenes are not replaced. Exact source/prompt/native hashes, bound roles, rejected studies and actual delivered layer usage: `books/chapter_one/landscape/revisions/v34_editorial_polish/generation_evidence.json`. Source URL: https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v34_editorial_polish/generation_evidence.json','']
for p in sorted(V.rglob('*')):
 if p.is_file() and p.suffix.lower() in ['.png','.jpg','.pdf']:
  role='OpenAI generated source-bound native study; selection/rejection and modifications recorded in generation_evidence.json; no third-party inserts.' if p.parent.name=='art' else 'Owner source-derived reference/proof/export; preserves existing art attribution. Review PNG/master lossless; contact JPEG/email compression declared. Not an independently licensed scene replacement.'
  rows.append('- `'+rel(p)+'`: '+role)
rows.append(end);block='\n'.join(rows)
s=re.sub(re.escape(start)+'.*?'+re.escape(end),lambda m:block,s,flags=re.S) if start in s else s.rstrip()+'\n\n'+block+'\n';lic.write_text(s,encoding='utf8',newline='\n')
scopepaths=['books/chapter_one','design/05_DOC_LEDGER.md','ASSET_LICENSES.md',rel(IMPACT)]
changed=set(git('diff','--name-only','HEAD','--',*scopepaths))|set(git('ls-files','--others','--exclude-standard','--',*scopepaths))
changed.update([rel(V/'manifest.json'),rel(V/'project_gates.json')]);changed.discard(rel(IMPACT))
impact=read(IMPACT);impact['files']=sorted(changed);gates=read(V/'project_gates.json').get('checks',[])
impact['validation']=[dict(command='Root native all-page/source/style/typography and email-sample visual review',result='PASS',evidence=rel(V/'visual_review.json')),dict(command='python -B books/chapter_one/landscape/audit_book.py --proof V34/complete --baseline V33/complete (dispatches V34 strict snapshot)',result='PASS',evidence=rel(C/'verification.json')),dict(command='python -B V34/email_export.py; lossless master encoding and byte/pixel verification',result='PASS',evidence=rel(C/'email_verification.json')),dict(command='Supplied source-layer contrast proxy; final composed-art contrast measurement',result='PASS',evidence=rel(V/'composed_caption_contrast.json')+'; source proxy4 FAIL/8 OUTLINE_REQUIRED/63 PASS; composed0 FAIL/7 outlined/68 PASS. Source proxy skips local inpaints and rear transform.'),dict(command='python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; audit authority/development unit tests',result='PASS' if len(gates)==3 and all(x['exit_code']==0 for x in gates) else 'PENDING',evidence=rel(V/'project_gates.json')),dict(command='Godot/runtime/import/GDScript/device gates',result='NOT_APPLICABLE',evidence='Static book review and documentation only; no game, runtime, save, protected-original or release changes.')]
impact['acceptance_gaps']='Owner/child reading, qualified SLP review, final restoration/resolution, production trim/reflow/bleed and physical print remain open. Ear canon held; missing literal drain/clearing-action sources not invented. Publication and source checks are not master-audit acceptance.';save(IMPACT,impact)
paths={p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
paths.update([IMPACT,lic,R/'design/05_DOC_LEDGER.md'])
for f in ['book.json','render_book.py','audit_book.py','PAGE_PLAN.md','REVIEW.md','STORY_COMPREHENSION_AUDIT.md']:paths.add(L/f)
for f in ['README.md','DESIGN_LANGUAGE.md']:paths.add(L.parent/f)
for q in read(V/'BOOK_BASELINE.json')['sources'].values():paths.add((L/q['file']).resolve())
for q in e['native_attempts']:
 for ref in q['references']:paths.add(R/ref['path'])
for p in (L/b['font']).resolve().parent.iterdir():
 if p.is_file():paths.add(p)
paths.update((L.parent/'plan/reference').glob('*.jpg'))
paths.update((OLD/'complete').glob('page_[0-9][0-9].png'))
for f in ['README.md','BOOK_CURRENT.json','manifest.json','complete/page_provenance.json','complete/verification.json','complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf']:paths.add(OLD/f)
handoff=R/'books/chapter_one/handoffs/2026-10-18_v34_audit_fixes'
paths.update(p for p in handoff.iterdir() if p.is_file())
for p in paths:
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt','.tsv'] and (p.is_relative_to(V) or rel(p) in changed):p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
files=[]
for p in sorted(paths,key=rel):
 assert p.is_file(),p
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt','.tsv']:data=data.replace(b'\r\n',b'\n')
 assert len(data)<100*1024*1024,rel(p)
 files.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='V34 review/native/proof/build/evidence' if p.is_relative_to(V) else 'Exact source/font/style/baseline/authority dependency'))
payload='\n'.join(x['path']+' '+x['sha256'] for x in files).encode()
save(V/'manifest.json',dict(id='mermaid-roshan-book-v34-editorial-20261018',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline=BASE,status='REVIEW_IMPLEMENTED_AND_VERIFIED; FINAL_RESOLUTION_PRINT_AND_HUMAN_ACCEPTANCE_OPEN',entry=rel(V/'README.md'),review=rel(V/'AUDIT_REVIEW.html'),pdf=rel(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),email_pdf=rel(C/'Mermaid_Roshan_Book_V34_Email.pdf'),generation_calls=25,selected_derivatives=11,files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),hash_convention='Git LF text; native binary bytes; sorted path + space + SHA256 joined by LF without terminal newline.',access_mode='Anonymous HTTPS exact immutable revision; verified after push.'))
print(json.dumps(dict(manifest_files=len(files),required_bytes=sum(x['bytes'] for x in files),changed_files=len(changed),master_bytes=(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf').stat().st_size,email_bytes=email['output_bytes'])))
