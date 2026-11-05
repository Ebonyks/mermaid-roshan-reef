"""Seal exact Git-index bytes for the cover rebuild, final book and review packet."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1]
prefix=V.relative_to(R).as_posix()
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
controls=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'))
provenance=json.loads((V/'complete/cover_provenance.json').read_text('utf8'))
paths.update((L/q['file']).resolve().relative_to(R).as_posix() for q in provenance['layers'])
paths.add((L/controls['font']).resolve().relative_to(R).as_posix())
paths.update(['books/chapter_one/landscape/render_book.py','books/chapter_one/landscape/audit_book.py','books/chapter_one/landscape/book.json','books/chapter_one/DESIGN_LANGUAGE.md','books/chapter_one/README.md','books/chapter_one/landscape/PAGE_PLAN.md','books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md','ASSET_LICENSES.md','design/05_DOC_LEDGER.md','design/audit_impacts/picture-book-v43-dust-bunnies-cover-20261028.json'])
old='books/chapter_one/landscape/revisions/v42_doublewide_arrival/'
paths.update(old+p for p in ['manifest.json','remote_verification.json','complete/Mermaid_Roshan_Book_V42_Email.pdf','complete/page_00.png'])
paths.update(old+'complete/page_%02d.png'%i for i in range(1,34))
excluded=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json','design/audit_impacts/picture-book-v43-publication-20261029.json']
paths-=set(excluded)
assert not paths-index.keys(),sorted(paths-index.keys())
files=[]
for path in sorted(paths):
 data=subprocess.check_output(['git','cat-file','blob',index[path]],cwd=R)
 role='Existing cover source or publication/review dependency'
 if path.startswith(prefix+'/art/'):role='Preserved native bounded imagegen output; exact prompt/source/scope in corresponding record'
 elif path.startswith(prefix+'/complete/'):role='Final cover/book export or exact production/check record'
 elif path.startswith(prefix+'/review_iterations/'):role='Preserved rejected intermediate review artifact; never accepted delivery art'
 elif path.startswith(old+'complete/page_'):role='Exact V42 body proof used in new HTML reader; not reauthored'
 row=dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role=role,provenance='Owner project sources; source license entries remain controlling. New selected character/floor derivatives use built-in imagegen; originals preserved.')
 if Path(path).suffix.lower() in ('.png','.jpg'):
  im=Image.open(R/path);row['dimensions']=list(im.size);row['mode']=im.mode
 files.append(row)
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
manifest=dict(id='mermaid-roshan-book-v43-dust-bunnies-cover-20261028',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='5fbdc77157341686d5db5ca70fce597e9ab8e7b3',entry=prefix+'/README.md',status='COVER_REVIEW_OWNER_ACCEPTANCE_OPEN',scope='Self-contained cover-specific layered rebuild, full reading PDF and source/review packet. Larger historical body source/print archive remains the sealed V42 package; not a new full lossless book master.',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256(sorted UTF8 path TAB sha256 TAB bytes LF); canonical Git-index bytes',publication_metadata_excluded=excluded,generation_calls=2,acceptance='Independent scoped review and machine checks; owner/child/SLP/physical print and arrival imposition/gutter remain open. No game/dev/master/release.')
(V/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes; payload',manifest['payload_sha256'])
