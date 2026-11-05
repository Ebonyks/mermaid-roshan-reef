"""Manifest a reproducible, source-attributed static-book review revision."""
from pathlib import Path
import json,hashlib,subprocess
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
B=json.loads((L/'book.json').read_text(encoding='utf8'))
layout=json.loads((V/'complete/page_provenance.json').read_text(encoding='utf8'))
license_path=R/'ASSET_LICENSES.md';s=license_path.read_text(encoding='utf8')
marker='## Chapter One static book — V28 kindness revision (2026-09-30)'
if marker in s:s=s[:s.index(marker)].rstrip()+'\n'
rows=[marker,'','Owner-directed static-book derivatives of repository-owned references; original source licensing remains controlling. Generated art uses the built-in Codex image generator. Exact references, prompts, hashes, modifications and rejected studies are in `books/chapter_one/landscape/revisions/v28_kindness/generation_evidence.json`. No protected original changed.','']
for p in sorted(V.rglob('*')):
 if not p.is_file() or p.suffix.lower() not in ['.png','.jpg','.pdf'] or '.optimized.' in p.name:continue
 if p.name=='castle_entry_source.png':desc='Unchanged frame96 at4seconds from existing C02_S01_v1_door_open.mp4;1264×720; book full-art trim only.'
 elif p.name in ['castle_entry_ceiling.png','castle_entry_join.png']:desc='Native bounded architectural extension/join study; REJECTED_UNUSED for seam mismatch, retained as evidence, excluded from delivered page artwork.'
 elif p.name=='entry_layout_reference.png':desc='Disposable source-based book layout proof without text, used only to diagnose a join; not delivery artwork.'
 elif p.parent.name=='art':desc='Native bounded source-conditioned derivative; selected foreground or local bank patch as recorded in generation_evidence.json; no whole-scene replacement.'
 else:desc='Rendered book/review artifact from attributed sources, native Sniglet text and page layout; lossless PNG/PDF, or JPEG contact-sheet only. No source-image recompression.'
 rows.append('- `'+rel(p)+'`: '+desc)
license_path.write_text(s.rstrip()+'\n\n'+'\n'.join(rows)+'\n',encoding='utf8',newline='\n')
paths=set(p for p in V.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts and '.optimized.' not in p.name)
for f in ['book.json','render_book.py','audit_book.py','PAGE_PLAN.md','REVIEW.md','STORY_COMPREHENSION_AUDIT.md']:paths.add(L/f)
for f in ['README.md','DESIGN_LANGUAGE.md']:paths.add(L.parent/f)
paths.add(license_path)
paths.add(R/'design/audit_impacts/picture-book-kindness-v28-20260930.json')
for layer in layout['layers']:paths.add((L/B['sources'][layer['source_key']]['file']).resolve())
font=(L/B['font']).resolve();paths.update(p for p in font.parent.iterdir() if p.is_file())
evidence=json.loads((V/'generation_evidence.json').read_text(encoding='utf8'))
for job in evidence['generated']:
 for ref in job['references']:paths.add(R/ref['path'])
paths.add(R/evidence['extraction']['source'])
pv=L.parent/'previews/2026-09-30'
for f in ['generation_jobs.json','manifest.json','layout_evidence.json']:paths.add(pv/f)
for job in json.loads((pv/'generation_jobs.json').read_text(encoding='utf8')):
 if job['id'] in evidence['reuse']['selected']:
  for ref in job['refs']:paths.add(R/ref)
for old in [19,23,26]:paths.add(pv/'after'/f'story_{old:02}.png')
for old in [6,8,13,15,18,27,31]:paths.add(pv/'before'/f'story_{old:02}.png')
# All authored text must match Git's LF bytes before remote hash verification.
for p in paths:
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt'] and (p.is_relative_to(V) or p in [L/'book.json',L/'render_book.py',L/'audit_book.py',L/'PAGE_PLAN.md',L/'REVIEW.md',L/'STORY_COMPREHENSION_AUDIT.md',L.parent/'README.md',L.parent/'DESIGN_LANGUAGE.md',license_path]):
  p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
items=[]
for p in sorted(paths,key=lambda x:rel(x)):
 data=p.read_bytes()
 if p.suffix.lower() in ['.py','.json','.md','.html','.txt']:data=data.replace(b'\r\n',b'\n')
 items.append(dict(path=rel(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='review/source/build evidence'))
payload='\n'.join(x['path']+' '+x['sha256'] for x in items).encode()
save(V/'manifest.json',dict(id='mermaid-roshan-book-v28-kindness-20260930',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='4eb7c58bd81ac820949d122e97052e3b76213997',status='FULL_REVIEW_DRAFT; OWNER_CHILD_PRINT_ACCEPTANCE_PENDING',entry=rel(V/'README.md'),pdf=rel(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),files=items,payload_sha256=hashlib.sha256(payload).hexdigest(),hash_convention='Git canonical LF text; binary files unchanged; sorted path + space + SHA256 joined by LF, no final newline.',access_mode='Anonymous HTTPS raw GitHub at exact published revision; verify after push.'))
print(json.dumps(dict(files=len(items),bytes=sum(x['bytes'] for x in items),manifest=rel(V/'manifest.json'))))
