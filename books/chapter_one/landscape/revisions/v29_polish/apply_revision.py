"""Apply inspected derivative art and manuscript edits to the frozen V28 mapping."""
from pathlib import Path
import json,hashlib
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1]
B=json.loads((V/'BOOK_BASELINE.json').read_text(encoding='utf8'));P={p['page']:p for p in B['pages']}
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def add(id):
 p=V/'art'/f'{id}.png';im=Image.open(p);k='v29_'+id
 B['sources'][k]=dict(file=p.relative_to(L).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),native_size=list(im.size),provenance_record='revisions/v29_polish/generation_evidence.json')
 return k
def patch(id,poly):return dict(source=add(id),reference_size=[1484,1060],polygon=poly)
bank_path=V/'bank_annotations.json'
assert bank_path.exists(), 'Final measured bank annotations are required'
bank_info=json.loads(bank_path.read_text(encoding='utf8'))
for n in [5,7,8,16,20,24,25,30,31]:
 p=P[n];id=bank_info[str(n)]['candidate'];p['integrated_background']=add(id)
 p.pop('background_patches',None);p['integrated_prop_bounds']=bank_info[str(n)]['bounds'];p['integrated_motifs']=bank_info[str(n)]['motifs'];p['marginal_bunny_count']=bank_info[str(n)]['bunnies'];p['background_theme']=bank_info[str(n)]['intent'];p['bounds_note']='Final native visible-subject annotation; exact hidden occlusion/shadow opacity not measurable for generated pixels.'
P[3]['art']=[add('castle03')];P[3]['layout']='full';P[3]['caption'].update(x=268,y=55,width=206,size=18,color='navy',shadow=False)
# Actual restored-frame character focal regions, in PDF points. The old V28
#16:9 doorway boxes included blank floor and do not describe this7:5 source.
P[3]['focal_exclusions']=[[0,0,145,330],[176,80,110,175],[258,165,72,40],[95,1,161,88]]
P[3]['focal_review_note']='Native castle03 inspected: complete Daddy, Roshan head/body, reaching arm and tail/fins excluded. New caption begins12pt right of the broad fin envelope; doorway floor is caption space, not an actor focal region.'
P[9]['local_patch']=patch('lamma09',[[72,773],[94,739],[191,733],[215,757],[216,798],[166,820],[96,822]])
P[14]['art']=[add('fountain14')];P[14]['caption'].update(x=30,y=55,width=444,size=18,align='center',color='navy',halo=False,shadow=False)
P[17]['local_patch']=patch('listen17',[[606,130],[850,130],[980,220],[980,395],[938,522],[610,522],[603,409],[626,325],[612,250]])
P[18]['art']=[add('rescue18')];P[19]['art']=[add('rescue19')]
P[19]['local_patch']=patch('neck19_final',[[448,389],[477,385],[514,391],[537,403],[535,465],[516,476],[458,451]])
P[16]['art']=[add('hug16')]
# Use the coherent stationery derivative, avoiding rectangular wash seams.
# Main story foreground21 remains exact; background prop designs remain visually stable.
for n in [11,21]:
 P[n]['integrated_background']=add('bubbles'+str(n));P[n].pop('background_patches',None)
 if str(n) in bank_info:
  P[n]['integrated_prop_bounds']=bank_info[str(n)]['bounds']
  P[n]['bounds_note']='Final regenerated native background bounds; visual design preservation, not pixel-exact extraction.'
P[6]['local_patch']=patch('floor06_final',[[0,930],[180,955],[450,948],[730,914],[820,858],[844,767],[920,754],[1060,744],[1260,748],[1484,787],[1484,1060],[0,1060]])
P[13]['local_patch']=patch('caption13',[[0,738],[350,727],[740,732],[1140,735],[1484,749],[1484,1060],[0,1060]])
P[22]['local_patch']=patch('table22',[[1156,596],[1205,593],[1241,610],[1247,631],[1200,638],[1154,628]])
P[25]['art']=[add('sponge25')]
for n in [27,28,29]:P[n]['page_extension']='approved_scrub_ceiling'
P[32]['local_patches']=[patch('nap32',[[298,791],[309,751],[354,736],[397,755],[440,784],[449,866],[406,879],[306,869]]),patch('nap32',[[1082,830],[1104,783],[1143,782],[1202,793],[1240,835],[1225,890],[1119,891]])]
# Bounded text refinements; refrains and finished narrative retained.
P[4]['text']='Inside, dust covered the floor.\n“Let’s clean it together!”\nsaid Roshan.'
P[11]['text']='Rumi had lived in Pearl Castle\nfor hundreds of years.\n“I’ll help!” said Roshan. Scoop, scoop!'
P[14]['text']='A cup was stuck in the seahorse fountain.\nRoshan pulled it free!'
P[19]['text']='“I’ll help!” said Roshan.\nShe gently brushed one bunny away, then the other.'
P[18]['text']='In the playroom, two dust bunnies sat on Baby Eagle.\nThey wanted to play, but he was stuck.'
P[20]['text']='Baby Eagle was free!\n“Let’s play gently,” said Roshan.'
# Source establishes one visibly orange lane and two green lanes; don't invent another action frame.
P[12]['text']='One stream ran clear.\nThen Roshan cleared the other two.'
for p in B['pages']:
 q=p['caption'];q['halo']=False;q['shadow']=False
 if p['mode']=='F' and p['page'] not in [2,9,14,18,19,22,23]:q['color']='white';q['shadow']=True
 if p['page'] in [1,4,6,10,12,13,15,17,26,27,28,29,32]:q['size']=20
P[3]['caption'].update(color='navy',shadow=False)
P[1]['caption'].update(x=285,y=72,width=188)
P[4]['caption'].update(x=228,y=85,width=246,size=18,color='white')
P[6]['caption'].update(y=59)
P[19]['caption'].update(size=18,y=58)
P[23]['caption'].update(size=20,color='navy')
# Caption18 already is long; reserve a proper three-line region by giving32pt safety margin.
P[18]['caption'].update(size=18,y=62)
P[20]['foreground_zone']=[205,126,98,160]
P[20]['speech_bubbles']=[dict(text='Sorry!',box=[50,70,124,48],tail=[117,55]),dict(text='We were just\nplaying!',box=[310,70,166,62],tail=[389,55])]
P[32]['caption'].update(y=316)
for n in [23,26,27,28,29]:P[n]['caption']['y']=316
for n in [10,15]:P[n]['caption']['y']+=2
# A restrained native 0.4pt navy contour supports white type across painted highlights.
# This is editable typography, never a raster caption, box or opaque image strip.
for p in B['pages']:
 p['caption']['outline']=.4 if p['caption']['color']=='white' else 0
 p['caption']['shadow']=False
B['revision']='V29 · comprehensive polish';B['review_href']='../AUDIT_REVIEW.html';B['status']='iterated full review proof; external acceptance pending'
B['limitations']=['Internal craft target4.9/5 is separate from master release-proven acceptance; owner, child and print proof remain outstanding.','Actual speech-language pathologist review is required for an SLP-approved label; developmental guidance is applied but professional approval is not claimed.','Native generated masters are generally1484x1060 (~212ppi at7x5), not300ppi. Source masters/crops are measured, never silently upscaled.','Source story identity/staging retained, exact canonical landing/covers/strong21 preserved. New decorative performances are marginal echoes, not new game events.']
B['revision_notes'].append('V29: independent34-page audits; source-preserving quality repairs; lower-bank event performances; clearer speaker, residence, fountain, playroom and gentle-rescue wording; two recognizable unprompted Lamma peeks; bubble-pattern and typography proofs reviewed separately.')
save(L/'book.json',B)
print('Applied',B['revision'])
