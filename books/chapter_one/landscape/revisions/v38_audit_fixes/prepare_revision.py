"""Apply only the owner-authorized V38 controls; preserve the sealed V37 baseline."""
from pathlib import Path
import json,hashlib
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=read(V/'BOOK_BASELINE.json');P={p['page']:p for p in b['pages']}
b['revision']='V38 · accepted V37 audit fixes · A9 native resolution held'
b['status']='V38 review candidate; owner/child/SLP/trim/physical-print acceptance open'
b['download_pdf_href']='Mermaid_Roshan_Book_V38_Email.pdf'
b['review_href']='../REVISION_REVIEW.html'
P[22]['text']='In the art room, Roshan put\nthe paints in their places.\nThen she scrubbed the table. Scrub, scrub!'
P[18]['text']='Chirp, chirp!\n“Someone in the playroom\nneeds help!” said Roshan.'
P[16]['caption'].pop('line_colors',None)
P[16]['caption'].update(color='navy',y=110,line_baselines=[110,84,58])
b['cover']['subtitle'].update(text='A Pearl Castle\nfriendship story',x=338.0,y=262,width=90.2,size=13,align='right',color='navy',line_baselines=[262,246])
def source(key,file,role):
 p=V/'art'/file;im=Image.open(p)
 b['sources'][key]=dict(file=p.relative_to(L).as_posix(),sha256=sha(p),native_size=list(im.size),role=role,provenance='V38 generation_evidence.json; original sources preserved, only declared local polygons used')
source('v38_pail','bank_pail_attempt1.png','A5 bounded bank repair')
source('v38_rear_additions','rear_additions_attempt1.png','A6 Lamma and A7 cobweb local windows only')
source('v38_rear_dust','rear_carpet_attempt2.png','A7 four new drift windows only')
source('v38_door_dust','door_dust_attempt2.png','A8 plain threshold dust')
def patch(k,ref,box,poly,feather=2,**extra):return dict(source=k,reference_size=ref,source_canvas_box=box,polygon=poly,edge_feather_reference_pixels=feather,**extra)
P[9]['background_patches']=[patch('v38_pail',[1484,1060],[1090,920,1330,1050],[[1152,946],[1186,946],[1198,960],[1199,985],[1218,990],[1236,1005],[1237,1021],[1208,1025],[1170,1018],[1147,1005],[1145,972]])]
P[9]['integrated_motifs']=[('shell_pail_clean_water' if m=='bath_plug_chain' else m) for m in P[9]['integrated_motifs']]
P[9]['integrated_prop_bounds'][-1]=[1145/1484,946/1060,92/1484,79/1060]
# Door geometry and true alpha remain the original. Only the opaque inner threshold is patched.
P[5].setdefault('local_patches',[]).append(patch('v38_door_dust',[1100,1429],[240,740,860,1090],[[377,836],[415,834],[450,849],[490,840],[548,837],[577,850],[608,835],[645,833],[680,850],[700,841],[735,845],[753,864],[747,877],[375,877]],feather=2,placement=dict(source='v34_closed_door',box=P[5]['foreground_zone'])))
rear=b['back_cover'].setdefault('local_patches',[])
# Exact source framing remains the V37 rear. Keep its existing hair repair.
rear.append(patch('v38_rear_additions',[1484,1060],[0,0,1484,1060],[[537,520],[558,522],[576,534],[587,539],[580,550],[570,566],[553,576],[539,568]],feather=1.5))
rear.append(patch('v38_rear_additions',[1484,1060],[0,0,1484,1060],[[1376,0],[1484,0],[1484,106],[1458,103],[1425,81],[1398,51],[1376,26]],feather=1.5))
# These four small windows lie on bare carpet, away from originals, shells and tail.
for x,y,w,h in [(647,729,92,42),(827,831,94,49),(1108,995,101,45),(1366,939,99,53)]:
 rear.append(patch('v38_rear_dust',[1484,1060],[600,700,1484,1060],[[x,y+12],[x+18,y],[x+w-19,y+2],[x+w,y+18],[x+w-9,y+h-4],[x+26,y+h],[x,y+h-12]],feather=2))
save(L/'book.json',b);save(V/'BOOK_CURRENT.json',b)
g=read(V/'generation_jobs.json')
for q in g['records']:
 p=R/q['output'];im=Image.open(p);q.update(output_sha256=sha(p),native_size=list(im.size),mode=im.mode,alpha_bounds=im.getchannel('A').getbbox() if im.mode=='RGBA' else None)
 q['bound_reference_records']=[dict(path=s,sha256=sha(R/s),native_size=list(Image.open(R/s).size)) for s in q['references']]
save(V/'generation_evidence.json',g)
save(V/'revision_scope.json',dict(baseline='eb405fe45edbcc37b59bebebba475de445cffb58',handoff='1106170e845522afb48aadd20198500abed8cd28',changed_pdf_pages=[0,5,9,16,18,22,33],unchanged_pdf_pages=[n for n in range(34) if n not in [0,5,9,16,18,22,33]],native_resolution_gap=dict(item='A9',status='HELD',reason='Both native takes below1800px group height with small contour drift; handoff stop condition. Exact V37 cutout and placement retained. Print-edition upscale deferred.'),allowed_local_windows=dict(page5=P[5]['local_patches'][-1:],page9=P[9]['background_patches'],rear=rear[1:]),caption_changes=['A1 manual line breaks22','A2 navy and baselines16','A3 manual line breaks18','A4 two13pt right-aligned subtitle lines'],scope='Static picture-book review only. No game/runtime/dev/master/release/print edition.'))
print('V38 controls prepared; source keys',len(b['sources']))
