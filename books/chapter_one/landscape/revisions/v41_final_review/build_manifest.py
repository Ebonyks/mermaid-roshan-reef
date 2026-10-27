"""Seal exact staged V41 production/review/reference bytes, including V40 baseline dependencies."""
from pathlib import Path
import json,hashlib,subprocess
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1];prefix=V.relative_to(R).as_posix();oldprefix='books/chapter_one/landscape/revisions/v40_wide_arrival'
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
paths|={p for p in index if p.startswith(oldprefix+'/complete/') or p in [oldprefix+'/'+x for x in ['reassemble_master.py','verify_revision.py','BOOK_CURRENT.json','README.md','BUILD_REPORT.md','manifest.json','remote_verification.json','composition_provenance.json','compose_arrival.py']]}
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'))
paths|={(L/q['file']).resolve().relative_to(R).as_posix() for q in b['sources'].values()}
paths.add((L/b['font']).resolve().relative_to(R).as_posix())
recipe=json.loads((V/'world_composition_provenance.json').read_text('utf8'))
for q in recipe['layers']:paths.add(q['source'])
paths.update([recipe['source_contract']['path'],recipe['playground_source']['path']])
prior=json.loads((R/oldprefix/'composition_provenance.json').read_text('utf8'))
for q in prior['layers']:
 paths.add(q['source'])
 if q.get('output'):paths.add(q['output'])
paths.update(prior['source_authority'])
for q in json.loads((V/'generation_evidence.json').read_text('utf8'))['attempts']:
 paths.update(r['path'] for r in q['references'])
paths.update(q['path'] for rows in json.loads((R/'books/chapter_one/handoffs/2026-10-26_v41_print_edition/MANIFEST.json').read_text('utf8'))['groups'].values() for q in rows)
paths.add('books/chapter_one/handoffs/2026-10-26_v41_print_edition/MANIFEST.json')
paths|={'AGENTS.md','ASSET_LICENSES.md','books/chapter_one/README.md','books/chapter_one/DESIGN_LANGUAGE.md','books/chapter_one/landscape/PAGE_PLAN.md','books/chapter_one/landscape/REVIEW.md','books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md','books/chapter_one/landscape/audit_book.py','books/chapter_one/landscape/render_book.py','books/chapter_one/landscape/book.json','books/chapter_one/landscape/revisions/v34_editorial_polish/optimize_pdf_lossless.py','books/chapter_one/handoffs/2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md','books/chapter_one/handoffs/2026-10-18_v34_audit_fixes/CHARACTER_CONSISTENCY_2026-10-19.md','books/chapter_one/handoffs/2026-10-25_v38_audit_fixes/README.md','books/chapter_one/handoffs/2026-10-25_v38_audit_fixes/AUDIT.md','books/chapter_one/handoffs/2026-10-25_v38_audit_fixes/MANIFEST.json','design/05_DOC_LEDGER.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/audit_impacts/picture-book-v41-review-20261026.json'}
metadata=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json','design/audit_impacts/picture-book-v41-publication-20261026.json']
paths-=set(metadata)
assert not paths-index.keys(),sorted(paths-index.keys())
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);files=[]
for path in sorted(paths):
 proc.stdin.write((index[path]+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();assert header[1]==b'blob';size=int(header[2]);remain=size;h=hashlib.sha256()
 while remain:
  chunk=proc.stdout.read(min(1024*1024,remain));assert chunk;h.update(chunk);remain-=len(chunk)
 assert proc.stdout.read(1)==b'\n'
 role='Production/reference/review dependency'
 if path.startswith(prefix+'/art/'):role='Native outputs,source composition and bounded derivative repairs; generation/world records declare all edits'
 elif path.startswith(prefix+'/complete/'):role='Exact final proof/export/provenance or lossless master binary part'
 elif path.startswith(oldprefix+'/complete/'):role='Preserved V40 comparison proof/export/master binary part'
 files.append(dict(path=path,bytes=size,sha256=h.hexdigest(),role=role))
proc.stdin.close();assert proc.wait()==0
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
out=dict(id='mermaid-roshan-book-v41-review-20261026',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='0d1c49d11651e292a13885413a043f8044032836',entry=prefix+'/README.md',status='PART1_REVIEW_CANDIDATE_PRINT_PART2_HELD',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256 of sorted UTF8 path TAB sha256 TAB bytes LF, exact Git-index bytes',publication_metadata_excluded=metadata,receipt_excluded='Manifest and follow-up remote receipt/final publication-only peer verdict/dedicated publication impact excluded to avoid circular hashing. All art, sources, critique rounds and final-candidate evidence are sealed. Follow-up does not change a sealed payload member.',generation_calls=3,source_scene_preserved=True,visual_passes=5,acceptance='Owner-requested full-setting arrival and stronger dust. B2/A9 not needed at11in; printP1-P8 held until owner illustration acceptance. Physical print,child,SLP open. No game/release acceptance.')
(V/'manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8',newline='\n')
print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes; payload',out['payload_sha256'])
