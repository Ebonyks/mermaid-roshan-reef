"""Seal the exact staged production/review files, including V37 comparison dependencies."""
from pathlib import Path
import json,hashlib,subprocess
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1];prefix=V.relative_to(R).as_posix()
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
oldprefix='books/chapter_one/landscape/revisions/v37_consistency_20261022'
paths|={p for p in index if p.startswith(oldprefix+'/complete/') or p in [oldprefix+'/reassemble_master.py',oldprefix+'/verify_revision.py',oldprefix+'/BOOK_CURRENT.json',oldprefix+'/README.md']}
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'))
paths|={(L/q['file']).resolve().relative_to(R).as_posix() for q in b['sources'].values()}
paths.add((L/b['font']).resolve().relative_to(R).as_posix())
for q in json.loads((V/'generation_evidence.json').read_text('utf8'))['records']:paths.update(q['references'])
for q in json.loads((V/'handoff_local_verification.json').read_text('utf8'))['files']:paths.add(q['path'])
paths|={'AGENTS.md','ASSET_LICENSES.md','books/chapter_one/README.md','books/chapter_one/DESIGN_LANGUAGE.md','books/chapter_one/landscape/PAGE_PLAN.md','books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md','books/chapter_one/landscape/audit_book.py','books/chapter_one/landscape/render_book.py','books/chapter_one/landscape/book.json','books/chapter_one/landscape/revisions/v34_editorial_polish/optimize_pdf_lossless.py','books/chapter_one/handoffs/2026-10-25_v38_audit_fixes/MANIFEST.json','design/05_DOC_LEDGER.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/audit_impacts/picture-book-v38-audit-fixes-20261025.json'}
paths.add('design/audit_impacts/picture-book-v38-peer-review-20261025.json')
paths-={prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json'}
publication_metadata=['design/audit_impacts/picture-book-v38-peer-publication-20261025.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json']
assert not paths-index.keys(),sorted(paths-index.keys())
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);files=[]
for path in sorted(paths):
 proc.stdin.write((index[path]+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();assert header[1]==b'blob';size=int(header[2]);remain=size;h=hashlib.sha256()
 while remain:
  chunk=proc.stdout.read(min(1024*1024,remain));assert chunk;h.update(chunk);remain-=len(chunk)
 assert proc.stdout.read(1)==b'\n'
 role='Production/reference/review dependency'
 if path.startswith(prefix+'/art/'):role='Native generated candidate, selected/rejected scope in generation_evidence.json'
 elif path.startswith(prefix+'/complete/'):role='Exact final proof/export/provenance or master binary part'
 elif path.startswith(oldprefix+'/complete/'):role='Preserved V37 comparison proof/export or exact baseline master part'
 files.append(dict(path=path,bytes=size,sha256=h.hexdigest(),role=role))
proc.stdin.close();assert proc.wait()==0
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
generation=json.loads((V/'generation_evidence.json').read_text('utf8'))
out=dict(id='mermaid-roshan-book-v38-audit-fixes-20261025',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='eb405fe45edbcc37b59bebebba475de445cffb58',peer_review_baseline='03d35a93b6e4b814f8026d0a5c6d44932ec33ec6',handoff_revision='1106170e845522afb48aadd20198500abed8cd28',entry=prefix+'/README.md',status='SCOPED_REVIEW_PASS_A9_NATIVE_RESOLUTION_HELD',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256 of sorted UTF8 path TAB sha256 TAB bytes LF, exact Git-index bytes',receipt_excluded='This manifest, remote_verification.json and peer_review/final_publication_acceptance.json are publication metadata excluded to prevent circular hashing. Critique/response rounds and all production evidence are included; final receipt and publication-only reviewer confirmation follow at a separate verified metadata commit.',generation_calls=generation['calls'],visual_passes=5,acceptance='A1-A8/A10 implemented; A9held. Owner/child/SLP/trim/physical print open. No game/release acceptance.')
out['publication_metadata_excluded']=publication_metadata
out['receipt_excluded']+=' The dedicated publication-impact record covers that follow-up without modifying any sealed payload file.'
(V/'manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8',newline='\n')
print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes; payload',out['payload_sha256'])
