"""Apply owner-directed V28 to the preserved V27 manifest; no source raster edits."""
from pathlib import Path
import json, hashlib, copy
from PIL import Image
V=Path(__file__).resolve().parent
L=V.parents[1]
B=json.loads((V/'BOOK_BASELINE.json').read_text(encoding='utf8'))
P={p['page']:copy.deepcopy(p) for p in B['pages']}
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def source(key,file,operation):
 p=L/file
 B['sources'][key]={'file':file,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_size':list(Image.open(p).size),'provenance':{'operation':operation,'evidence':'revisions/v28_kindness/generation_evidence.json','status':'owner-approved preview where specified; new derivatives pending owner review'}}
def caption(p,x=32,y=318,width=440,align='center',halo=False):
 p['caption']=dict(x=x,y=y,width=width,size=18,align=align,color='navy',shadow=False,halo=halo)
for name in ['sink_action','lamba_bath','fountain_clear_v2','hug_cutout_v2','hug_stationery_v2','rescue_release','scrub_ceiling','rainbow_puff_cutout']:
 source('approved_'+name,'../previews/2026-09-30/art/'+name+'.png','Reuse owner-approved preview; see preview generation_jobs.json for original prompt and source bindings.')
for name in ['puff_reassurance','castle_entry_source','castle_entry_ceiling','castle_entry_join','apology_small_banks','lamba_toy_peek']:
 source('v28_'+name,'revisions/v28_kindness/art/'+name+'.png','Native extracted source or bounded derivative; see generation_evidence.json.')
P[6].update(art=['approved_sink_action'],layout='wide_cut',foreground_zone=[32,60,440,218],text='Round and round went the sponge.\nRoshan wiped the sink clean.',background_theme='Connected shell-sink cleaning action; existing bath accessories remain on low blue banks.')
caption(P[6])
P[8]['local_patch']=dict(source='approved_lamba_bath',reference_size=[1484,1060],polygon=[[83,782],[100,757],[128,758],[143,746],[178,747],[198,763],[208,787],[211,809],[186,824],[150,831],[107,826]])
P[8]['text']='Clean water filled the bath.\nThe dust bunny splashed again!'
P[13].update(art=['approved_fountain_clear_v2'],text='Roshan pulled the cup free!',focal_exclusions=[])
caption(P[13],207,316,270,'left',True)
P[15].update(mode='C',art=['approved_hug_cutout_v2'],layout='wide_cut',foreground_zone=[184,64,296,244],text='“You helped me!”\nsaid Rumi.\nShe gave Roshan\na great big hug.',integrated_background='approved_hug_stationery_v2',integrated_motifs=['tiny_cleared_seahorse_fountain'],integrated_prop_bounds=[[138/1484,868/1060,140/1484,114/1060]],marginal_bunny_count=0,border_assets=[],border_placements=[],background_theme='Connected hug silhouette; tiny cleared seahorse fountain recalls the rescue on the left bank.',bounds_note='Approved preview has fountain crest at y868/1060, above strict bottom-15% target. Retained transparently as owner-approved composition; not a geometric compliance claim.')
P[15].pop('focal_exclusions',None)
caption(P[15],40,263,148,'left')
P[18].update(art=['approved_rescue_release'],text='“I’ll help!” said Roshan.\nShe brushed one bunny away, then the other.')
P[19].update(text='Baby Eagle was free!\nNow they could play gently.',foreground_zone=[205,115,98,160],integrated_background='v23_bunny_apology_canvas',background_theme='Two small speaking bunnies on low banks address the freed Eagle; no oversized figures.',narrative_border_dialogue=True,integrated_prop_bounds=[[290/1484,868/1060,132/1484,104/1060],[1070/1484,868/1060,137/1484,104/1060]],bounds_note='Reduced to about9.8% page height. Ears begin at81.9% height; still above ideal85% line. Grounded small-bank composition retained as review candidate; no strict zone pass claimed.')
P[19]['background_patches']=[dict(source='v28_apology_small_banks',reference_size=[1484,1060],polygon=[[250,830],[450,830],[450,1009],[250,1009]]),dict(source='v28_apology_small_banks',reference_size=[1484,1060],polygon=[[1040,830],[1238,830],[1238,1009],[1040,1009]])]
P[19]['speech_bubbles']=[dict(text='Sorry!',box=[44,85,135,52],tail=[118,61]),dict(text='We were just\nplaying!',box=[309,85,165,65],tail=[387,61])]
caption(P[19])
P[20].update(text='“Come and play, Baby Eagle!”\nThe little dust bunnies played gently, too.')
P[20]['background_patches']=[dict(source='v28_lamba_toy_peek',reference_size=[1484,1060],polygon=[[366,928],[428,926],[458,941],[458,979],[442,990],[378,990],[366,960]])]
P[20]['integrated_motifs'].append('hidden_lamba_toy_peek')
P[22]['text']='Scrub, scrub! The table was clean.\nEverything was back in its place.'
P[24]['background_theme']='Completed castle rooms and converging route lights lead to the last shell door. Source castle hall retained.'
P[25]['text']='Grand Puff!\nHe was so dusty.\nHe did not feel well.'
P[26].update(art=['v28_puff_reassurance'],text='“Hold on, we’ll make you feel\nclean and better!” said Roshan.',background_theme='Roshan offers a soapy star sponge to uncomfortable Grand Puff. Small couch bunnies encourage the helpers; one eats popcorn. Attic jar and books remain.')
P[27].update(page_extension='approved_scrub_ceiling',text='Daddy, Rumi, and Baby Eagle helped Roshan.\nTogether, they washed Grand Puff. Scrub, scrub!')
P[31].update(art=['roshan_reflect_large','approved_rainbow_puff_cutout'],layout='placements',placements=[dict(source='roshan_reflect_large',box=[276,56,196,218]),dict(source='approved_rainbow_puff_cutout',box=[62,86,146,174])],text='“Your rainbow was there all along,\nGrand Puff. We helped it shine!”',background_theme='Roshan addresses the same rainbow Puff from the unchanged landing; cooperating puzzle bunnies stay small below.')
new=dict(page=3,mode='F',art=['v28_castle_entry_source'],layout='full_left',text='“Let’s look inside,\nDaddy,” said Roshan.',border_assets=[],border_placements=[],background_theme='Existing Grok frame at4seconds: Roshan and Daddy at open doors, dirty interior visible. Full-art left-anchored trim preserves both characters and the threshold; no generated wall pixels.',focal_exclusions=[[0,0,278,330],[280,0,150,280]],original_page=None,beat='castle_entry')
caption(new,289,318,185,'left',True)
new['caption']['color']='white'
order=[1,2,'entry',*range(3,20),21,22,*range(24,32),20,32]
assert len(order)==32
B['pages']=[]
for n,old in enumerate(order,1):
 p=copy.deepcopy(new if old=='entry' else P[old]);p['page']=n;p['original_page']=None if old=='entry' else old
 p.setdefault('beat','v27_'+str(old));B['pages'].append(p)
B['revision']='V28 — helping Grand Puff'
B['status']='V28_FULL_BOOK_REVIEW; OWNER_CHILD_PRINT_ACCEPTANCE_PENDING'
B['review_href']='../REVISION_REVIEW.html'
B['revision_notes']=['Owner approvals applied except oversized apology bunnies and removed craft-making beat.','New castle-entry page uses a full-art trim of an existing Grok frame; unsuccessful wall-extension studies are excluded.','Grand Puff receives reassurance, a soapy sponge and collaborative cleaning; no shell attack or dizziness. Book-only canon.','Door on23 hides Puff24 behind a page turn; bubbles27 hide rainbow28. Assumes story1 starts on a recto.','Former play invitation moved to31 for a gentle bridge into the bubble nap.','Two unprompted hidden Lamb-a appearances. Adult-only location record in revision evidence.']
B['limitations']=['Native art density varies; this is a review proof, not a press-ready 300ppi master.','New entry source is1264x720; full-page landscape trim is144ppi, with right-side architecture trimmed and both source characters preserved.','Waterfall clearing-action/source and rescue room-continuity questions remain from the comprehensive review.','Finale27–29 retain earlier low-density ceiling strips; only group-scrub ceiling26 is replaced.','Approved hug background crest and two-pixel toy-bunny ear exception remain explicit in bounds evidence.','Owner review of new derivatives, print dummy and child comprehension remain open. Resolve searching stays stopped.']
save(L/'book.json',B)
save(V/'pagination.json',dict(total_pages=34,story_pages=32,removed_v27_story_page=23,pages=[dict(story=p['page'],v27_story=p['original_page'],text=p['text']) for p in B['pages']],page_turns=[[23,24],[27,28]],note='Physical dummy assumes story1 is a recto. Covers are included in34total.'))
print('V28 manifest:32 story pages,2 covers')
