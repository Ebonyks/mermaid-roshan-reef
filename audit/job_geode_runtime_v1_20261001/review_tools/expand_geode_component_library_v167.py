from pathlib import Path
import datetime,hashlib,html,json,shutil
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'audit/job_geode_runtime_v1_20261001'
p=out/'ARTWORK_ITEMS.json';d=json.loads(p.read_text());source=b/d['items'][4]['path'];size=Image.open(source).size
assert size==(1024,683),size
details=[
 ('Tall cyan crystal in the left cavity',(264,205,131,245),'The tall rear crystal has three broad cyan/cream faces and a readable tapered tip. The lilac crystal and smaller cyan crystal overlap its lower edge, while its base remains embedded in the plum mineral bed. The bright upper planes separate it from the darker cavity without a floating loot outline.'),
 ('Middle lilac crystal in the left cavity',(358,313,87,170),'The lilac middle crystal provides a clear color contrast beside the tall cyan crystal. Its pale top and darker side face retain the painted facet language. Its lower tip is seated in the cavity and partly covered by the small front crystal; that overlap supports depth rather than a detached reward.'),
 ('Small cyan crystal in the left cavity',(313,377,76,108),'The small front crystal is a compact three-face cyan form in front of the rear crystal. Its lower edge disappears into the cream/plum cavity material, preserving rooted ownership. It is decorative detail inside the large geode touch target; fine facet visibility on the physical phone is still unverified.'),
 ('Tall lilac crystal in the right cavity',(655,220,134,231),'The tallest right crystal mirrors the left cavity hierarchy through a contrasting lilac identity. A pale peaked top and broad violet side planes remain visible behind the two cyan forms. Its base stays seated in the mineral bed, and the cream rim frames its silhouette without creating a separate pickup layer.'),
 ('Middle cyan crystal in the right cavity',(588,306,121,173),'The middle cyan crystal leans into the cavity beside the taller lilac form. Broad aqua faces and a pale top provide clear separation from the lavender bed. The smaller cyan crystal overlaps its foot; the layered bases read as one embedded cluster rather than three dropped prizes.'),
 ('Small cyan crystal in the right cavity',(673,408,77,85),'The smallest right crystal has a compact pale cap, aqua front and darker side face. Its visible foot meets the mineral bed below the leaning cyan crystal, so it belongs to the rock. Like the left front crystal, it is a decorative reveal detail; physical-device readability and complete timed continuity remain pending.')]
cards=[]
for q,(title,box,prose) in zip(d['items'][4:],details):
 q['evaluation']=prose;q['display_title']=title;q['review_annotation_source_rect']=list(box)
 q['physical_phone_readability_score']=None
 q['qualification']='Source/component finish4.6 and sampled mounted ownership4.6 only. Six painted components in one open-geode source image; no independent loot objects or new derivative pixels. Physical device and full timed action remain unreviewed.'
 left='LEFT' in q['id'];view='53 91 448 501' if left else '524 91 448 500'
 x,y,w,h=box
 cards.append('<article><h3>'+html.escape(title)+'</h3><svg role="img" aria-label="'+html.escape(title)+'; yellow rectangle is a review annotation" viewBox="'+view+'" style="width:100%;height:auto"><image width="1024" height="683" href="../../'+q['path']+'"/><rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(w)+'" height="'+str(h)+'" rx="9" fill="none" stroke="#e1a700" stroke-width="4" stroke-dasharray="9 5"/></svg><p><strong>Finish and sampled rooted ownership:4.6/5.</strong> '+html.escape(prose)+'</p><small>'+q['id']+' · Cavity view from the unchanged source. Yellow mark is review annotation only. Complete action/device/child/owner approval remains open.</small></article>')
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
report=out/'index.html';s=report.read_text(encoding='utf-8');marker='<h2>Every current native view</h2>';assert marker in s and 'id="embedded-components"' not in s
section='<section id="embedded-components"><h2>Six crystals embedded in the geode</h2><p>These are individually evaluated painted details in one source image. Each cavity view retains its original raster pixels; the yellow rectangle identifies the reviewed component and is a library annotation. No extra asset or collectible is created.</p><div class="grid">'+''.join(cards)+'</div></section>'
report.write_text(s.replace(marker,section+marker,1),encoding='utf-8',newline='\n')
target=out/'review_tools/expand_geode_component_library_v167.py';shutil.copyfile(__file__,target)
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{q.relative_to(b).as_posix() for q in out.rglob('*') if q.is_file()});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Six component-specific prose evaluations and source-preserving annotated cavity windows added.')
