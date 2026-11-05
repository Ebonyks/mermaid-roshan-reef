"""Seal exact staged V42 production/review/reference bytes, including preserved V41 dependencies."""
from pathlib import Path
import json,hashlib,subprocess
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1];prefix=V.relative_to(R).as_posix();oldprefix='books/chapter_one/landscape/revisions/v41_final_review'
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
paths={p for p in index if p.startswith(prefix+'/')}
oldmanifest=json.loads((R/oldprefix/'manifest.json').read_text('utf8'))
paths.update(q['path'] for q in oldmanifest['files'])
paths.update(oldprefix+'/'+p for p in ['manifest.json','remote_verification.json','peer_review/final_publication_acceptance.json'])
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'))
paths.update((L/q['file']).resolve().relative_to(R).as_posix() for q in b['sources'].values())
paths.add((L/b['font']).resolve().relative_to(R).as_posix())
paths.add('design/audit_impacts/picture-book-v42-doublewide-20261026.json')
metadata=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json','design/audit_impacts/picture-book-v42-publication-20261026.json']
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
 elif path.startswith(oldprefix+'/complete/'):role='Preserved V41 comparison proof/export/master binary part'
 files.append(dict(path=path,bytes=size,sha256=h.hexdigest(),role=role))
proc.stdin.close();assert proc.wait()==0
payload=''.join(f"{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in files).encode()
out=dict(id='mermaid-roshan-book-v42-doublewide-20261026',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline='69276b5cd05eb9deec6b7080af09fb7c3029bef1',entry=prefix+'/README.md',status='DOUBLEWIDE_ILLUSTRATION_REVIEW_BINDING_HELD',files=files,payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='SHA256 of sorted UTF8 path TAB sha256 TAB bytes LF, exact Git-index bytes',publication_metadata_excluded=metadata,receipt_excluded='Manifest and follow-up remote receipt/final publication-only peer verdict/dedicated publication impact excluded to avoid circular hashing. All art, sources, critique rounds and final-candidate evidence are sealed. Follow-up does not change a sealed payload member.',generation_calls=0,source_scene_preserved=True,visual_passes=5,acceptance='Owner-directed doublewide crop; all33 other proofs/captions/sources retained. Mixed-width review only: physical page assignment/parity/gutter and printP1-P8 held. Owner,physical,child,SLP open.')
(V/'manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8',newline='\n')
print('Manifest:',len(files),'files,',sum(q['bytes'] for q in files),'bytes; payload',out['payload_sha256'])
