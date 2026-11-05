from pathlib import Path
from PIL import Image
import json,hashlib,shutil
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
filename='exec-200bafd0-1323-4d12-b7de-ca73be2b8c84.png';p=V/'art/arrival_header_repair_attempt1.png';shutil.copy2(Path('C:/Users/Peter/.codex/generated_images/01a0bd6a-0b70-7682-bd4c-44a20e6eed2d')/filename,p)
b=read(L/'book.json');e=read(V/'generation_evidence.json');im=Image.open(p);digest=hashlib.sha256(p.read_bytes()).hexdigest()
b['sources']['v34_arrival_header_repair']=dict(file=p.relative_to(L).as_posix(),sha256=digest,native_size=list(im.size),provenance_record='revisions/v34_editorial_polish/generation_evidence.json');b['sources'].pop('v34_arrival_border',None)
b['pages'][0]['top_extension'].update(source='v34_arrival_header_repair',source_box=[0,0,im.width,24])
for q in e['native_attempts']:
 if q['id']=='arrival_border':q['selection']='NOT_DELIVERED';q['rejection']='Visible horizontal strip join at native proof; repaired using correctly composed fixed-geometry reference.'
if not any(q['id']=='arrival_header_repair' for q in e['native_attempts']):e['native_attempts'].append(dict(id='arrival_header_repair',attempt=1,filename=filename,path=p.relative_to(R).as_posix(),sha256=digest,native_size=list(im.size),selection='DELIVERED'))
e['count']=25;e['method']=e['method'].replace('24 built-in','25 built-in')+' Final header-only inpaint replaces rejected first outdraw; original source below the8pt header remains exactly translated, never redrawn.'
save(L/'book.json',b);save(V/'BOOK_CURRENT.json',b);save(V/'generation_evidence.json',e)
for name in ['document_revision.py','verify_revision.py']:
 p=V/name;s=p.read_text('utf8').replace('actual_generation_calls\']=24','actual_generation_calls\']=25').replace("e['count']==24","e['count']==25").replace('generation_calls=24','generation_calls=25').replace('24 candidates','25 candidates').replace('24 built-in','25 built-in').replace('24 image','25 image').replace('24 candidate','25 candidate').replace('24candidates','25candidates')
 if name=='document_revision.py':s=s.replace("'quiet_books_job.json']","'quiet_books_job.json','header_repair_job.json']")
 p.write_text(s,encoding='utf8',newline='\n')
print('Header-only seam repair applied;25 native attempts,12 selected derivatives.')
