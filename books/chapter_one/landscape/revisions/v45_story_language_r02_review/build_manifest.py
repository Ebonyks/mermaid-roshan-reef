"""Seal staged V45 bytes and explicitly pin the distinct incoming work order."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=V.parents[4];prefix=V.relative_to(R).as_posix()
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  h,p=row.split(b'\t',1);mode,oid,stage=h.split();assert stage==b'0';index[p.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));paths.add((L/b['font']).resolve().relative_to(R).as_posix())
paths.update(['books/chapter_one/landscape/render_book.py','books/chapter_one/landscape/audit_book.py','books/chapter_one/landscape/book.json','books/chapter_one/README.md','books/chapter_one/DESIGN_LANGUAGE.md','books/chapter_one/landscape/PAGE_PLAN.md','books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md','ASSET_LICENSES.md','design/05_DOC_LEDGER.md','design/audit_impacts/picture-book-v45-story-language-20261101.json'])
paths.update(json.loads((R/'design/audit_impacts/picture-book-v45-story-language-20261101.json').read_text('utf8'))['files'])
h='books/chapter_one/handoffs/2026-10-31_v45_story_language/'
paths.update(h+p for p in ['README.md','CRITIQUE.md','MANUSCRIPT.json','MANIFEST.json'])
paths.update(['books/chapter_one/landscape/revisions/v44_door_and_consistency/complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf','books/chapter_one/landscape/revisions/v44_door_and_consistency/complete/cover_provenance.json','books/chapter_one/landscape/revisions/v42_doublewide_arrival/complete/page_provenance.json'])
excluded=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json','design/audit_impacts/picture-book-v45-publication-20261101.json'];paths-=set(excluded)
assert not paths-index.keys(),sorted(paths-index.keys());files=[]
for p in sorted(paths):
 data=subprocess.check_output(['git','cat-file','blob',index[p]],cwd=R)
 q=dict(path=p,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='V45 export/control/review evidence or explicit rebuild dependency',provenance='Owner project; V44 picture/source licenses retained. Vector text-only derivative; no generation, no image re-encoding. Rejected variants explicitly labelled under audit/.')
 if Path(p).suffix.lower()=='.png':q['dimensions']=list(Image.open(R/p).size)
 files.append(q)
incoming=json.loads((R/h/'MANIFEST.json').read_text('utf8'));ext=[dict(path=q['path'],revision='550a0b86216dee020d5070428ab4ddcfe0da4dc1',bytes=q['bytes'],sha256=q['sha256'],role='Frozen incoming work-order dependency, not a hash assertion about mutable current root documents') for q in incoming['files']]
ext.sort(key=lambda q:(q['revision'],q['path']))
digest=lambda rows:hashlib.sha256(''.join(f"{q.get('revision','')}:{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in rows).encode()).hexdigest()
m=dict(id='mermaid-roshan-book-v45r02-story-language-20261101',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='550a0b86216dee020d5070428ab4ddcfe0da4dc1',art_baseline='49a199846c61a39a3735e162214706b3687f12d3',entry=prefix+'/README.md',status='23_OF25_CAPTIONS_IMPLEMENTED_11_AND15_HELD',files=files,payload_sha256=digest(files),required_external_inputs=ext,external_inputs_sha256=digest(ext),payload_algorithm='SHA256(sorted UTF8 revision-or-empty COLON path TAB sha256 TAB bytes LF); staged canonical Git bytes',publication_metadata_excluded=excluded,scope='Text-only r02 strict review; two declared held pages exactV44. Parallel V45 packet at01004e37 is preserved. Self-contained PDF overlay rebuild with baselinePDF/font/renderer. Full historical source seal needs complete Git clone. No full lossless print master,game,dev/master or release.',acceptance='Machine and independent scoped review only. Human/child/SLP/owner new-facts/print and inherited art findings remain open. Input48hashes are explicitly pinned at550a0b8, since root current docs necessarily change.')
(V/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf8',newline='\n')
print('V45 manifest',len(files),'members',sum(q['bytes'] for q in files),'bytes;',len(ext),'pinned input dependencies;',m['payload_sha256'])
