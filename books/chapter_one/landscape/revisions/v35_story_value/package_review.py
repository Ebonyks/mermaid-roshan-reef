"""Publishable proposal closure, per-asset attribution and exact change coverage."""
from pathlib import Path
import hashlib,json,re,subprocess
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1]
I=R/'design/audit_impacts/picture-book-story-value-v35-20261019.json'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert read(V/'verification.json')['status']=='PASS'
lic=R/'ASSET_LICENSES.md';s=lic.read_text('utf8');start='<!-- BEGIN CHAPTER_ONE_V35_REVIEW -->';end='<!-- END CHAPTER_ONE_V35_REVIEW -->'
rows=[start,'## Chapter One V35 story-value / spoiler-free rear review (2026-10-18 owner request)','','Two built-in OpenAI ImageGen calls. The first full native candidate is excluded; one isolated head derivative from the second is used in candidate A with its exterior haze excluded and an original door foreground occluding it. Existing owner art, identity reference and font are unchanged. Prompts, exact sources, hashes, native outputs, contour/placement and acceptance limits are in `books/chapter_one/landscape/revisions/v35_story_value/generation_evidence.json` and `cover_proposal.json`. Source URL: https://github.com/Ebonyks/mermaid-roshan-reef/tree/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v35_story_value','']
for p in sorted(V.rglob('*.png')):
 role='OpenAI ImageGen source-bound native candidate; exact prompt/input SHA-256 and selection scope recorded. No new whole-scene delivery.' if p.parent.name=='art' else 'Browser-rendered owner-art document-layout proof; source image pixels preserved outside the declared cameo, with editable Sniglet copy. Retains existing source attribution; review only.'
 rows.append('- `'+rel(p)+'`: '+role)
rows.append(end);block='\n'.join(rows)
s=re.sub(re.escape(start)+'.*?'+re.escape(end),lambda _:block,s,flags=re.S) if start in s else s.rstrip()+'\n\n'+block+'\n'
lic.write_text(s,encoding='utf8',newline='\n')
paths=['books/chapter_one','ASSET_LICENSES.md','design/05_DOC_LEDGER.md',rel(I)]
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf8').splitlines()
changed=set(git('diff','--name-only','HEAD','--',*paths))|set(git('ls-files','--others','--exclude-standard','--',*paths))
changed.update([rel(V/'manifest.json'),rel(V/'project_gates.json')]);changed.discard(rel(I))
impact=read(I);impact['files']=sorted(changed)
g=read(V/'project_gates.json').get('checks',[]) if (V/'project_gates.json').exists() else []
impact['validation']=[dict(command='python -B books/chapter_one/landscape/revisions/v35_story_value/verify_review.py; root cover/contour/editorial review',result='PASS',evidence=rel(V/'verification.json')),dict(command='ASHA/AAP/Harvard primary guidance and exact V34 before/proposed text reviewed',result='PASS',evidence=rel(V/'story_review.json')+'; editorial inference, not a clinical efficacy claim.'),dict(command='python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; authority/development unit tests',result='PASS' if len(g)==3 and all(q['exit_code']==0 for q in g) else 'PENDING',evidence=rel(V/'project_gates.json')),dict(command='Game/runtime/GDScript/import/device gates',result='NOT_APPLICABLE',evidence='Concept review and static book cover candidates only; no current game or book manuscript/PDF change.')]
save(I,impact)
payload={p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
payload.update([I,lic,R/'design/05_DOC_LEDGER.md',L.parent/'README.md',L.parent/'DESIGN_LANGUAGE.md'])
c=read(V/'cover_proposal.json');payload.add(R/c['font'])
for q in c['candidates']:payload.add(R/q['base'])
payload.add(R/'assets/sprites/stuffie_studio/lamma.png')
# Source seal and current-reader references use the exact already-published baseline.
for q in read(V/'baseline_seal.json')['files']:payload.add(R/q['path'])
prior=L/'revisions/v34_editorial_polish/complete'
payload.update(prior.glob('page_[0-9][0-9].png'))
for f in ['READ_BOOK.html','verification.json','page_provenance.json']:payload.add(prior/f)
payload.update([prior.parent/'AUDIT_REVIEW.html',prior.parent/'AUDIT_EVALUATION.md',prior.parent/'manifest.json',prior.parent/'generation_evidence.json',prior.parent/'PRINT_DUMMY.html'])
files=[]
for p in sorted(payload,key=rel):
 assert p.is_file(),p
 if p.suffix.lower() in ['.py','.cjs','.json','.md','.html','.txt','.tsv'] and (p.is_relative_to(V) or rel(p) in changed):p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.cjs','.json','.md','.html','.txt','.tsv']:data=data.replace(b'\r\n',b'\n')
 assert len(data)<100*1024*1024,p
 files.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='V35 proposal/build/proof/evidence' if p.is_relative_to(V) else 'Unchanged exact baseline/source/font or updated navigation/authority'))
digest=hashlib.sha256('\n'.join(q['path']+' '+q['sha256'] for q in files).encode()).hexdigest()
save(V/'manifest.json',dict(id='chapter-one-v35-story-value-proposal',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='4f65c502beabb38bb3365920005e2e6f90ea13f0',status='PROPOSAL_PUBLISHED; OWNER_THEME_WORDING_COVER_CHOICES_OPEN; V34_MANUSCRIPT_UNCHANGED',entry='books/chapter_one/README.md',review=rel(V/'STORY_REVIEW.html'),files=files,payload_sha256=digest,hash_convention='Git LF text; native binaries. Sorted path + space + SHA256 joined with LF, no terminal LF.',generation_calls=2,selected_derivatives=1,access_mode='Anonymous HTTPS exact immutable revision verified after push.'))
print(json.dumps(dict(manifest_files=len(files),required_bytes=sum(q['bytes'] for q in files),changed_files=len(changed))))
