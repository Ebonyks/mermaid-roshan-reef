"""Seal canonical staged bytes for all V45 deliverables and rebuild dependencies."""
from pathlib import Path
import hashlib,io,json,subprocess
from PIL import Image
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1]
prefix=V.relative_to(R).as_posix()
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
    if row:
        head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0'
        index[path.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
excluded=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/publication_validation.json','design/audit_impacts/picture-book-v45-publication-20261031.json']
paths-=set(excluded)
paths.update(['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md',
 'design/audit_impacts/picture-book-v45-language-20261031.json','books/chapter_one/DESIGN_LANGUAGE.md',
 'books/chapter_one/README.md','books/chapter_one/landscape/render_book.py','books/chapter_one/landscape/audit_book.py',
 'books/chapter_one/landscape/book.json','books/chapter_one/landscape/PAGE_PLAN.md',
 'books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md'])
old='books/chapter_one/landscape/revisions/v44_door_and_consistency/'
paths.update(old+p for p in ['README.md','BOOK_CURRENT.json','manifest.json','remote_verification.json','CONSISTENCY_AUDIT.md',
 'complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf','complete/cover_provenance.json'])
paths.add('books/chapter_one/landscape/revisions/v42_doublewide_arrival/complete/page_provenance.json')
handoff='books/chapter_one/handoffs/2026-10-31_v45_story_language/'
paths.update(handoff+p for p in ['README.md','CRITIQUE.md','MANUSCRIPT.json','MANIFEST.json'])
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));paths.add((L/b['font']).resolve().relative_to(R).as_posix())
assert not paths-index.keys(),sorted(paths-index.keys())
files=[]
for path in sorted(paths):
    data=subprocess.check_output(['git','cat-file','blob',index[path]],cwd=R)
    role='Preserved source/provenance or current book-authority dependency'
    if path.startswith(prefix+'/complete/'):role='Current reading export, PDF-derived proof or verification record; no new artwork'
    elif path.startswith(prefix+'/qa/'):role='Retained preflight snapshot; final complete/verification.json owns current machine verdict'
    elif path.startswith(prefix+'/'):role='V45 control, editorial, reproduction or evidence artifact'
    q=dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role=role)
    if Path(path).suffix.lower() in ['.png','.jpg']:
        im=Image.open(io.BytesIO(data));q.update(dimensions=list(im.size),mode=im.mode)
    files.append(q)
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
manifest=dict(id='mermaid-roshan-book-v45-story-language-20261031',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='550a0b86216dee020d5070428ab4ddcfe0da4dc1',entry=prefix+'/README.md',status='READING_REVIEW_DRAFT_25_CAPTION_CHANGES_ONE_DECLARED_EDITORIAL_ADAPTATION',scope='24exact proposed caption changes plus a concise page11 adaptation; exact proposed bubbles; artwork/covers/order/type sizes preserved. No new art/game/print-edition acceptance.',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256(sorted UTF8 path TAB sha256 TAB bytes LF); canonical Git-index bytes',publication_metadata_excluded=excluded,generation_calls=0,acceptance='Publication and scoped machine/layout review only. Owner/new facts/page11 adaptation, real oral/child reading, SLP, inherited BK44-O01/O02 and physical print/arrival mapping remain open.')
(V/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes; payload',manifest['payload_sha256'])
