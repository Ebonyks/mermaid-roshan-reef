"""Composed-proof corrections: true door continuity, safe text and quiet floor texture."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
b=read(L/'book.json');P={q['page']:q for q in b['pages']};e=read(V/'generation_evidence.json')
for q in read(V/'floor_outputs.json'):
 p=V/'art'/f"{q['id']}_attempt1.png";shutil.copy2(Path('C:/Users/Peter/.codex/generated_images/01a0bd6a-0b70-7682-bd4c-44a20e6eed2d')/q['filename'],p)
 q.update(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),native_size=list(Image.open(p).size))
 b['sources']['v34_'+q['id']]=dict(file=p.relative_to(L).as_posix(),sha256=q['sha256'],native_size=q['native_size'],provenance_record='revisions/v34_editorial_polish/generation_evidence.json')
 if not any(x['id']==q['id'] for x in e['native_attempts']):e['native_attempts'].append(q)
e['count']=len(e['native_attempts']);e['method']=e['method'].replace('20 built-in','22 built-in')+' Two additional bounded mosaic-floor repairs follow first composed-proof review.'
P[10]['local_patches'].append(dict(source='v34_dirty_pool_floor',reference_size=[1484,1060],polygon=[[490,815],[649,814],[890,815],[1181,812],[1320,825],[1317,1011],[1185,1032],[1000,1033],[749,1028],[488,1010]]))
P[15].setdefault('local_patches',[]).append(dict(source='v34_clean_pool_floor',reference_size=[1484,1060],polygon=[[230,825],[410,822],[706,829],[1011,823],[1250,827],[1268,1013],[1063,1034],[747,1038],[436,1030],[226,1007]]))
b['cover']['subtitle']['text']=''
P[3]['local_patches']=[dict(source='v34_entry_dust',reference_size=[1484,1060],polygon=[[809,487],[817,468],[837,460],[852,467],[866,490],[877,515],[869,528],[845,529],[822,520],[805,504]]),dict(source='v34_entry_dust',reference_size=[1484,1060],polygon=[[808,568],[840,568],[886,555],[915,541],[942,539],[952,554],[974,585],[1000,610],[1048,634],[1054,697],[1004,742],[952,748],[900,730],[843,736],[808,720],[805,685],[807,628]])]
P[13]['text']='Whoosh! A rainbow waterfall!\nThe pool’s magic made\nrainbow water.'
P[13]['caption'].update(x=188,y=89,width=286,color='white',outline=.85)
P[16]['caption'].update(x=28,width=170,y=267);P[16]['foreground_zone']=[202,66,276,242]
P[21]['foreground_zone']=[32,58,440,220]
P[22]['text']='One last door was shut. Roshan listened.';P[22]['caption'].update(y=34)
P[23]['local_patches']=[dict(source='v31_door_mystery',reference_size=[1484,1060],polygon=P[22]['local_patches'][0]['polygon'],placement=dict(source='v34_closed_door',box=P[23]['foreground_zone'])),dict(source='v34_mysterious_door',reference_size=[1484,1060],polygon=P[22]['local_patches'][0]['polygon'],placement=dict(source='v34_closed_door',box=P[23]['foreground_zone']))]
P[31]['placements'][0]['box']=[248,61,220,185]
for p in P.values():
 q=p['caption'];q['y']=min(316,q['y'])
 if 50<=q['y']<58 and '\n' in p['text']:q['y']=58
# No source-image warping: only physical vector scale and original pixels in source layers.
save(L/'book.json',b);save(V/'BOOK_CURRENT.json',b);save(V/'generation_evidence.json',e)
renderer=L/'render_book.py';s=renderer.read_text('utf8')
s=s.replace(' c.showPage();c.scale(S,S)',' c.showPage()')
s=s.replace("for p in B['pages']:\n PAGE=", "for p in B['pages']:\n c.scale(S,S)\n PAGE=")
s=s.replace("PAGE='back_cover'\nback_transform", "PAGE='back_cover'\nc.scale(S,S)\nback_transform")
s=s.replace("l,t,r,b=B['sources'][pk].get('alpha_box') or base_im.getchannel('A').getbbox()", "l,t,r,b=B['sources'][pk].get('source_box') or B['sources'][pk].get('alpha_box') or base_im.getchannel('A').getbbox()")
s=s.replace("text(subtitle['text'],subtitle['x'],subtitle['y'],subtitle['width'],subtitle['size'],True)", "if subtitle['text']:text(subtitle['text'],subtitle['x'],subtitle['y'],subtitle['width'],subtitle['size'],True)")
renderer.write_text(s,encoding='utf8',newline='\n')
print('Second composed-proof pass applied;22 native candidates, whole originals remain sealed.')
