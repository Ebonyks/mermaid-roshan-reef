"""Apply the named owner corrections as bounded document layers over sealed V38."""
from pathlib import Path
import hashlib,json,os
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=read(V/'BOOK_BASELINE.json');P={p['page']:p for p in b['pages']}
b.update(revision='V39 · owner corrections: tails, Lamma, stained glass, demo landing and unwell puffs',status='V39 review candidate; owner/child/SLP/trim/physical-print acceptance open',download_pdf_href='Mermaid_Roshan_Book_V39_Email.pdf')
def source(key,p,role):
 im=Image.open(p);b['sources'][key]=dict(file=os.path.relpath(p,L).replace('\\','/'),sha256=sha(p),native_size=list(im.size),role=role,provenance='V39 input_provenance.json and generation_evidence.json; native/source originals preserved, only declared document masks/crop are used.')
for key,file,role in [('v39_daddy_tail','daddy_caudal_focused_attempt3.png','Only Daddy terminal-tail region after explicit independent anatomical diagnosis'),('v39_rumi_caudal','rumi_caudal_focused_attempt3.png','Rumi forked pink caudal fin; narrowly focused after explicit two-take diagnosis'),('v39_care24','care24_attempt1.png','Local little-puff facial/hand/tissue-box repair'),('v39_occlusion_floor','occlusion_floor_cleanplate_attempt2.png','Only two tiny floor/obsolete-remnant windows; no Roshan or Daddy silhouette pixels accepted'),('v39_care25','care25_attempt1.png','Local sofa-puff facial/hand/tissue-box/cheering-mark repair')]:source(key,V/'art'/file,role)
source('v39_foreground_lock',V/'inputs/cover_composed.png','Exact existing V38 composed-cover Roshan foreground fin; no generated pixels; original contour restoration after floor infill')
source('v39_lamma',R/'assets/minigames/seek/lamma_animation.png','Exact existing painted Lamma RGBA atlas first frame; no egg, native painted wool/feet, document clip/placement only')
source('v39_lamma_contact',R/'assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png','Existing soft teal contact-shadow RGBA; document opacity and flattening only')
source('v39_stained_glass',R/'assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png','Exact approved castle Roshan stained-glass portrait; uniform document scale and arch clip only')
source('v39_demo_landing',V/'inputs/demo_landing_frame_408.png','Exact owner-directed demo frame408 at17seconds; ground/wheels by slide and swings')
def patch(key,ref,canvas,poly,feather=1.5,**extra):return dict(source=key,reference_size=ref,source_canvas_box=canvas,polygon=poly,edge_feather_reference_pixels=feather,**extra)
cover=b['cover'].setdefault('local_patches',[])
r03=read(V/'peer_review/r03_BOOK_CURRENT.json')['cover']['local_patches'][len(read(V/'BOOK_BASELINE.json')['cover']['local_patches']):]
cover.extend(r03[:2])
cover[-1]['polygon']=[[103.8,673],[112,654],[135,636],[172,631],[210,632],[244,640],[279,648],[311,640],[342,630],[365,630],[348,652],[317,669],[288,674],[263,669],[243,669],[241,672],[251,680],[261,692],[270,708],[276,728],[276,735],[250,736],[207,733],[162,730],[132,715],[111.5,700]]

# Source clean plate fills only the foreground-occlusion gap and obsolete root remnant.
# Both complete mermaids remain original selected sources elsewhere.
cover.append(patch('v39_occlusion_floor',[1512,1080],[55,630,395,745],[[242,674],[260,674],[279,689],[283,710],[267,710],[256,707],[244,697]],feather=1.5))
# Restore exact original Roshan foreground-fin pixels last; source is the sealed
# caption-free V38 cover, not the generator's reconstructed hidden surfaces.
cover.append(patch('v39_foreground_lock',[1512,1080],[0,0,1512,1080],[[246,671],[260,670],[273,672],[285,676],[302,682],[320,692],[345,706],[370,720],[396,735],[396,750],[289,750],[287,732],[285,719],[282,707],[278,697],[271,686],[264,680],[256,676],[249,674]],feather=0))
# Native source alpha remains intact. A quiet existing soft shadow supplies floor contact.
cover.append(patch('v39_lamma_contact',[1512,1080],[1257,965,1410,986],[[1257,965],[1410,965],[1410,986],[1257,986]],feather=0,opacity=.35))
iw,ih=Image.open(R/'assets/minigames/seek/lamma_animation.png').size;cell=256;size=210;left=1225;top=775
cover.append(patch('v39_lamma',[1512,1080],[left,top,left+iw/cell*size,top+ih/cell*size],[[left,top],[left+size,top],[left+size,top+size],[left,top+size]],feather=0))
# Reuse the actual source portrait, without asking a generator to invent stained glass.
scale=.31;ox=1104.5-527*scale;oy=520-218*scale
P[1].setdefault('local_patches',[]).append(patch('v39_stained_glass',[1512,1080],[ox,oy,ox+1024*scale,oy+1024*scale],[[1075,608],[1075,555],[1078,541],[1088,529],[1104.5,520],[1120,531],[1129,544],[1134,559],[1134,609]],feather=.3))
P[2]['art']=['v39_demo_landing'];P[2]['background_theme']='Exact owner-directed demo ground landing on wheels beside slide/swings; preserve original source frame.'
P[2]['art_crop']=[136,0,1144,720]
# Keep the original little-puff silhouettes/ears and all banks. Only named local acting/prop pixels change.
P[24].setdefault('background_patches',[]).extend([
 patch('v39_care24',[1484,1060],[1040,890,1370,1040],[[1091,944],[1110,937],[1179,940],[1191,960],[1193,984],[1191,1014],[1131,1018],[1129,998],[1094,987]],feather=1.5),
 patch('v39_care24',[1484,1060],[1040,890,1370,1040],[[1246,947],[1315,947],[1324,963],[1324,986],[1313,1002],[1240,998],[1238,968]],feather=1.5)])
P[24]['background_theme']='Two little puffs look gently unwell beside a pop-up tissue box and their existing water flask; Grand Puff remains foreground only.'
P[24]['integrated_motifs']=[('little_puff_with_tissue_box' if x=='little_puff_tissue' else 'little_puff_unwell_with_water' if x=='little_puff_water_flask' else x) for x in P[24]['integrated_motifs']]
# Explicit prop bounds, distinct from each puff's pre-existing silhouette bounds.
P[24]['integrated_prop_bounds'].append([1137/1484,980/1060,52/1484,37/1060])
P[25].setdefault('background_patches',[]).extend([
 patch('v39_care25',[1512,1080],[1060,910,1280,1040],[[1073,924],[1110,924],[1110,968],[1073,968]],feather=2),
 patch('v39_care25',[1512,1080],[1060,910,1280,1040],[[1111,960],[1151,958],[1163,969],[1160,993],[1145,1004],[1110,999],[1106,975]],feather=1.5),
 patch('v39_care25',[1512,1080],[1060,910,1280,1040],[[1173,964],[1218,963],[1233,976],[1236,1019],[1222,1030],[1186,1030],[1172,1010],[1170,982]],feather=1.2)])
P[25]['background_theme']='Same tiny sofa and two gently unwell little puffs; aqua pop-up tissue box replaces cloth, cheering marks removed.'
P[25]['integrated_motifs']=[{'little_puff_waiting_to_help':'little_puff_resting_unwell','little_puff_folding_washcloth':'little_puff_unwell_with_tissue','folded_washcloth':'tissue_box'}.get(x,x) for x in P[25]['integrated_motifs']]
P[25]['integrated_prop_bounds'].append([1175/1512,987/1080,37/1512,24/1080])
save(V/'BOOK_CURRENT.json',b);save(L/'book.json',b)
g=read(V/'generation_jobs.json')
selected={'COVER_OCCLUSION_FLOOR_T02':'Only the occlusion-gap/root-remnant window; exact original Roshan foreground restored over it','DADDY_CAUDAL_FOCUSED_T03':'Daddy terminal tail only; broad attempts fully rejected','RUMI_CAUDAL_FOCUSED_T03':'Rumi caudal-fin/floor gap only, document fit explicitly recorded','CARE24_T01':'Named expression/hand/tissue-box masks only','CARE25_T01':'Named expression/hand/tissue-box and cheering-mark masks only'}
for q in g['records']:
 q['selected']=q['id'] in selected
 if q['selected']:q['selection_scope']=selected[q['id']]
save(V/'generation_evidence.json',g)
scope=read(V/'revision_scope.json');scope['allowed_new_windows']=dict(cover=cover[len(read(V/'BOOK_BASELINE.json')['cover']['local_patches']):],page1=P[1]['local_patches'][-1:],page24=P[24]['background_patches'][-2:],page25=P[25]['background_patches'][-3:]);scope['landing_selected']=dict(source='v39_demo_landing',frame=408,time_seconds=17,native_size=[1280,720],crop=[136,0,1144,720],native_resolution_status='Exact native demo still; review source, not a final-print-resolution claim');save(V/'revision_scope.json',scope)
print('Prepared V39 controls; named changes0/1/2/24/25; source keys',len(b['sources']))
