"""Apply only source-faithful cover changes; all interiors remain sealed."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['exec-d516e4ee-ec77-4348-879e-12fd68bf7878.png','exec-9ecdcfaa-2532-43bf-9ffa-6151d2ebb603.png']
jobs=read(V/'generation_jobs.json');b=read(V/'BOOK_BASELINE.json');rows=[]
polys=[[
 [[1222,777],[1380,777],[1410,838],[1484,850],[1484,1060],[1095,1060],[1095,990],[1157,965],[1157,923],[1138,919],[1139,908],[1112,908],[1107,883],[1194,866],[1210,840]],
 [[1285,437],[1307,434],[1340,441],[1377,432],[1388,452],[1384,482],[1373,506],[1346,512],[1308,503],[1288,486]]
 ],[
 [[1004,356],[1045,356],[1047,404],[1014,405],[1008,398],[1004,381]]
 ]]
for i,(job,name) in enumerate(zip(jobs,files)):
 p=V/'art'/('front_cleanup.png' if i==0 else 'rear_lamma.png')
 shutil.copy2(Path('C:/Users/Peter/.codex/generated_images/01a0bd6a-0b70-7682-bd4c-44a20e6eed2d')/name,p)
 im=Image.open(p);assert im.size==(1484,1060)
 key='v33_front_cleanup' if i==0 else 'v33_rear_lamma'
 b['sources'][key]=dict(file=p.relative_to(L).as_posix(),sha256=sha(p),provenance=dict(method='built-in image_gen bounded local edit',evidence='revisions/v33_story_covers/generation_evidence.json',native_size=list(im.size),whole_candidate_not_delivered=True))
 rows.append(dict(**job,native_output=dict(path=p.relative_to(R).as_posix(),sha256=sha(p),dimensions=list(im.size),mode=im.mode),original_tool_filename=name,selection='SELECTED_BOUNDED_PIXELS_ONLY',delivery_polygons=polys[i],reference_size=[1484,1060],review='PENDING composed native proof inspection'))
b['cover']['local_patches'] += [dict(source='v33_front_cleanup',reference_size=[1484,1060],polygon=p) for p in polys[0]]
b['cover']['treatment']='Existing rendered story ensemble with bounded paint/craft debris removal and unwell Puff facial correction'
b['back_cover']=dict(art='v27_scrub',mode='full_art',story_scene_page=26,selection='Actual cooperative washing scene26 with exact original source layer transforms, caption omitted; obsolete craft-table composition retired.',local_patches=[dict(source='v33_rear_lamma',reference_size=[1484,1060],polygon=polys[1][0])])
b['revision']='V33 story-faithful covers';b['status']='V33 cover continuity review proof; owner/child/print acceptance pending'
assert b['pages']==read(V/'BOOK_BASELINE.json')['pages']
save(L/'book.json',b);save(V/'BOOK_CURRENT.json',b)
save(V/'generation_evidence.json',dict(baseline='2719d2fcf66afe4cb73b8445087e09dd52319849',generated_count=2,selected_local_derivatives=2,generated=rows,method='No full-scene redraw: front retains old complete base and identity patches, exposing only two local edits. Rear reuses exact existing scene26 source layers, exposing only a tiny shelf patch. All original art remains unchanged.'))
for name in ['optimize_pdf_lossless.py','verify_remote.py','run_project_gates.py']:
 shutil.copy2(V.parent/'v32_rainbow_story'/name,V/name)
print('Cover-only manuscript applied;32 interior page configurations exact.')
