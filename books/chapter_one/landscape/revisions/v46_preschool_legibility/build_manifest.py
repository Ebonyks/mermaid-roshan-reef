"""Seal canonical staged V46 output, rebuild dependencies and pinned before references."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=V.parents[4];prefix=V.relative_to(R).as_posix();baseline='116b33fa829f7397e55f70af01be45dc39b3f85b'
index={}
for row in subprocess.check_output(['git','ls-files','-s','-z'],cwd=R).split(b'\0'):
 if row:
  h,p=row.split(b'\t',1);mode,oid,stage=h.split();assert stage==b'0';index[p.decode()]=oid.decode()
impact='design/audit_impacts/picture-book-v46-preschool-legibility-20261101.json'
paths={p for p in index if p.startswith(prefix+'/')};paths.update(json.loads((R/impact).read_text('utf8'))['files']);paths.add(impact)
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));paths.add((L/b['font']).resolve().relative_to(R).as_posix())
paths.update(['books/chapter_one/landscape/revisions/v44_door_and_consistency/complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf','books/chapter_one/landscape/revisions/v44_door_and_consistency/complete/cover_provenance.json','books/chapter_one/landscape/revisions/v42_doublewide_arrival/complete/page_provenance.json'])
excluded=[prefix+'/manifest.json',prefix+'/remote_verification.json',prefix+'/peer_review/final_publication_acceptance.json','design/audit_impacts/picture-book-v46-publication-20261101.json'];paths-=set(excluded)
assert not paths-index.keys(),sorted(paths-index.keys());files=[]
for p in sorted(paths):
 data=subprocess.check_output(['git','cat-file','blob',index[p]],cwd=R);q=dict(path=p,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='V46 delivery/control/review or explicit overlay-rebuild dependency',provenance='Existing project artwork and Sniglet source license rows retained; vector-text derivative, no art generation/re-encoding; audit proofs labelled superseded.')
 if Path(p).suffix.lower()=='.png':q['dimensions']=list(Image.open(R/p).size)
 files.append(q)
ext=[]
for n in [18,22]:
 p=f'books/chapter_one/landscape/revisions/v45_story_language_r02_review/complete/page_{n:02}.png';data=subprocess.check_output(['git','show',baseline+':'+p],cwd=R);ext.append(dict(revision=baseline,path=p,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='Frozen before reference: original thin/overlong V45r02 lettering; not new delivery pixels'))
digest=lambda rows:hashlib.sha256(''.join(f"{q.get('revision','')}:{q['path']}\t{q['sha256']}\t{q['bytes']}\n" for q in rows).encode()).hexdigest()
m=dict(id='mermaid-roshan-book-v46-preschool-legibility-20261101',repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',baseline=baseline,entry=prefix+'/README.md',status='PRESCHOOL_COPY_AND_SOLID_INK_REVIEW_DRAFT_NO_HELD_WORD_PAGES',files=files,payload_sha256=digest(files),required_external_inputs=ext,external_inputs_sha256=digest(ext),payload_algorithm='SHA256(sorted UTF8 revision-or-empty COLON path TAB sha256 TAB bytes LF); canonical staged Git bytes',publication_metadata_excluded=excluded,scope='Standalone PDF overlay rebuild with native V44 PDF, font, renderer and editable controls. Full327-source/project audit needs complete checkout and sealed source list. No game/release or print acceptance.',acceptance='Scoped primary/independent editorial and technical review only; actual child/human spoken read-aloud, qualifiedSLP, owner/illustration, inherited art and physical-print/imposition gates remain open.')
(V/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf8',newline='\n')
print('V46 manifest',len(files),'outputs;',len(ext),'pinned before references;',sum(q['bytes'] for q in files),'output bytes;',m['payload_sha256'])
