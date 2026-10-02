from pathlib import Path
from PIL import Image
import datetime, hashlib, html, json, re, shutil, subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'assets_src/imagegen/geologist_river_components_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
p=f/'attempt_01/REVIEW.json';d=read(p);im=Image.open(b/d['native_path']);a=im.getchannel('A').point(lambda v:255 if v>4 else 0)
windows=[(0,0,627,790),(627,0,1254,790),(0,790,627,1254),(627,790,1254,1254)]
for x,window in zip(d['components'],windows):
 q=a.crop(window).getbbox();region=[q[0]+window[0],q[1]+window[1],q[2]-q[0],q[3]-q[1]]
 x['earlier_region_annotation']=x['region'];x['region']=region
 x['region_annotation_correction']='Initial half-height quadrant at627 cut the nodes and included their tails in channel windows. Corrected from complete native directly inspected after browser card review; top/bottom separation uses790 in the transparent gap. No image pixel edited.'
write(p,d)
p=f/'REVIEW.json';r=read(p);r['components']=[x for attempt in [1,2] for x in read(f/('attempt_%02d/REVIEW.json'%attempt))['components']];r['region_annotation_correction']='Four first-attempt read-only windows corrected after browser inspection exposed node truncation. Original native pixels and source scores retained; complete nodes/closed channels directly re-inspected.';write(p,r)
p=f/'index.html';s=p.read_text(encoding='utf-8')
for x in r['components']:
 rx,ry,rw,rh=x['region'];dw,dh=x['source_dimensions'];z=340/max(rw,rh)
 pattern=r'(<article id="'+re.escape(x['id'])+r'">.*?<div class="region" style=")[^"]*("><img src="[^"]*" alt="[^"]*" style=")[^"]*(">.*?<pre>).*?(</pre>)'
 repl=lambda m:m[1]+f'width:{rw*z:.2f}px;height:{rh*z:.2f}px'+m[2]+f'width:{dw*z:.2f}px;height:{dh*z:.2f}px;left:{-rx*z:.2f}px;top:{-ry*z:.2f}px'+m[3]+html.escape(json.dumps(x,indent=2))+m[4]
 s,n=re.subn(pattern,repl,s,count=1,flags=re.S);assert n==1,x['id']
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/Path(__file__).name)
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v22.py')],cwd=b,check=True)
p=b/'design/audit_impacts/job-geology-river-painted-source-20261001.json';d=read(p);d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in f.rglob('*') if x.is_file()});write(p,d)
print('Four corrected whole-component windows',[(x['id'],x['region']) for x in r['components'][:4]])
