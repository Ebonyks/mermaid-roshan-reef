"""Seal exact staged bytes for the repair and comprehensive audit packet."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1];prefix=V.relative_to(R).as_posix()
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));provenance=json.loads((V/'complete/cover_provenance.json').read_text('utf8'))
paths.update((L/q['file']).resolve().relative_to(R).as_posix() for q in provenance['layers'])
paths.add((L/b['font']).resolve().relative_to(R).as_posix())
paths.update(q['source']['path'] for q in json.loads((V/'asset_derivations.json').read_text('utf8'))['files'])
paths.update(q['path'] for q in json.loads((V/'audit/primary_book_audit.json').read_text('utf8'))['identity_sources'])
paths.update(['books/chapter_one/landscape/render_book.py','books/chapter_one/landscape/audit_book.py','books/chapter_one/landscape/book.json','books/chapter_one/DESIGN_LANGUAGE.md','books/chapter_one/README.md','books/chapter_one/landscape/PAGE_PLAN.md','books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md','ASSET_LICENSES.md','design/05_DOC_LEDGER.md','design/audit_impacts/picture-book-v44-door-consistency-20261029.json'])
v43='books/chapter_one/landscape/revisions/v43_dust_bunnies_cover/'
paths.update(v43+p for p in ['manifest.json','remote_verification.json','BOOK_CURRENT.json','complete/Mermaid_Roshan_and_the_Dust_Bunnies_V43.pdf','complete/page_00.png'])
v42='books/chapter_one/landscape/revisions/v42_doublewide_arrival/'
paths.update(v42+p for p in ['manifest.json','remote_verification.json'])
paths.update(v42+'complete/page_%02d.png'%i for i in range(1,34))
excluded=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json','design/audit_impacts/picture-book-v44-publication-20261029.json']
paths-=set(excluded);assert not paths-index.keys(),sorted(paths-index.keys())
files=[]
for path in sorted(paths):
 data=subprocess.check_output(['git','cat-file','blob',index[path]],cwd=R)
 role='Existing source or explicit publication/review dependency'
 if path.startswith(prefix+'/art/'):role='Preserved native bounded imagegen output; attempt1 rejected, attempt2 architecture-only selection'
 elif path.startswith(prefix+'/complete/'):role='Final review export, actual render or exact check record'
 elif path.startswith(prefix+'/audit/'):role='Comprehensive audit/diagnostic evidence, never generator appearance authority'
 elif path.startswith(v42+'complete/page_'):role='Exact carried body proof used by HTML reader'
 row=dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role=role,provenance='Owner project sources; original licensing retained. New media derivations explicitly mapped in V44 asset_derivations.json; no protected original changed.')
 if Path(path).suffix.lower() in ['.png','.jpg']:
  im=Image.open(R/path);row['dimensions']=list(im.size);row['mode']=im.mode
 files.append(row)
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
manifest=dict(id='mermaid-roshan-book-v44-door-consistency-20261029',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='5284b6dc0774ef24059790ab7a3a45da15c28c05',entry=prefix+'/README.md',status='DOOR_REPAIR_REVIEWED_WHOLE_BOOK_TWO_OPEN_CONTINUITY_FINDINGS',scope='Self-contained cover repair, full reading PDF, all34-entry primary/independent audit evidence and reader proofs. Strict historical source seal requires full Git clone; not a new full-book lossless print archive.',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256(sorted UTF8 path TAB sha256 TAB bytes LF); canonical Git-index bytes',publication_metadata_excluded=excluded,generation_calls=2,acceptance='Scoped repair review and machine checks only. Whole-book geography/fountain findings, owner/child/SLP/physical print and arrival imposition remain open. No game/dev/master/release.')
(V/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes; payload',manifest['payload_sha256'])
