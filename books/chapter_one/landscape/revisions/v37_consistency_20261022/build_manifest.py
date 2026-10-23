"""Seal staged Git bytes for the V37 review and its production dependencies."""
from pathlib import Path
import hashlib,json,subprocess
V=Path(__file__).resolve().parent;R=V.parents[4]
prefix=V.relative_to(R).as_posix();stress=V.parent/'v36_stress_test_20261022'
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
paths={q['path'] for q in json.loads((V.parent/'v36_next_draft/manifest.json').read_text('utf8'))['files']}
paths|={p for p in index if p.startswith(prefix+'/') or p.startswith(stress.relative_to(R).as_posix()+'/')}
paths|={'books/chapter_one/README.md','books/chapter_one/landscape/PAGE_PLAN.md','books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md','books/chapter_one/landscape/audit_book.py','books/chapter_one/landscape/book.json','books/chapter_one/landscape/render_book.py','design/audit_impacts/picture-book-stress-test-20261022.json','books/chapter_one/landscape/revisions/v34_editorial_polish/optimize_pdf_lossless.py','books/chapter_one/landscape/revisions/v36_next_draft/manifest.json'}
book=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));L=V.parents[1]
paths|={(L/q['file']).resolve().relative_to(R).as_posix() for q in book['sources'].values()}
for q in json.loads((V/'generation_evidence.json').read_text('utf8'))['records']:
 paths.add(q['input_origin']);paths.update(q['references'])
paths-={prefix+'/manifest.json',prefix+'/remote_verification.json'}
missing=paths-index.keys();assert not missing,sorted(missing)
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);files=[]
for path in sorted(paths):
 proc.stdin.write((index[path]+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();assert header[1]==b'blob',path
 size=int(header[2]);remain=size;h=hashlib.sha256()
 while remain:
  chunk=proc.stdout.read(min(1024*1024,remain));assert chunk;h.update(chunk);remain-=len(chunk)
 assert proc.stdout.read(1)==b'\n'
 role='review/provenance/build dependency'
 if '/art/' in path and path.startswith(prefix):role='native generated repair; selected/rejected scope in generation_evidence.json'
 elif '/inputs/' in path and path.startswith(prefix):role='exact source crop input'
 elif '/master_parts/' in path:role='byte-identical lossless master part or reconstruction descriptor'
 elif path.startswith(prefix) and ('/r0' in path or '/complete/' in path):role='exact revision proof/export or review diagnostic; see scoped audit records'
 files.append(dict(path=path,bytes=size,sha256=h.hexdigest(),role=role))
proc.stdin.close();assert proc.wait()==0
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
record=dict(id='mermaid-roshan-book-v37-stress-20261022',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='b5288f2ca2bab1e36d51fd9a00616de0dc30c2c0',status='SCOPED_VISUAL_REVIEW_PASS_PRINT_OWNER_PENDING',entry=prefix+'/README.md',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256 of sorted UTF8 path TAB sha256 TAB byte_count LF; exact Git-index bytes',receipt_excluded='manifest.json and remote_verification.json excluded to avoid circular hashing. Exact published payload revision is named by the separate anonymous remote receipt.',initial_runs=20,revision_cycles=7,audits_per_revision=5,generation_calls=33,selected_native_candidates=32,acceptance='No remaining identified character/composition defect in final scoped AI review. Print-resolution/trim/owner/child/SLP acceptance remains open; no game/release changes.')
(V/'manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n');print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes')
