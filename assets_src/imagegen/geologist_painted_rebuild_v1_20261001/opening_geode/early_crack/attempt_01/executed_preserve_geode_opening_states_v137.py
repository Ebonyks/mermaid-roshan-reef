from pathlib import Path
import json,hashlib,shutil
from PIL import Image
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');root=b/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001';providers={'early_crack':r'C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-08e8b215-7673-426d-989f-bd36d4d88801.png','middle_open':r'C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-42125de4-7ece-49ae-949f-96f8304cac13.png'}
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
rows=[]
for state,path in providers.items():
 out=root/('opening_geode/'+state+'/attempt_01');assert not (out/'native.png').exists();shutil.copyfile(path,out/'native.png');im=Image.open(out/'native.png');assert im.mode=='RGBA';alpha=im.getchannel('A');bounds={str(t):alpha.point(lambda v:255 if v>=t else 0).getbbox() for t in [1,8,16,64,128,240]}
 for name,color in [('audit_white.png',(255,255,255,255)),('audit_aqua.png',(223,244,244,255))]:
  field=Image.new('RGBA',im.size,color);field.alpha_composite(im);field.convert('RGB').save(out/name)
 size=(1024,round(im.height*1024/im.width));im.resize(size,Image.Resampling.LANCZOS).save(out/'whole_canvas_1024.png');der=Image.open(out/'whole_canvas_1024.png');da=der.getchannel('A');db=da.point(lambda v:255 if v>=16 else 0).getbbox()
 write(out/'whole_canvas_1024.json',dict(source_path=rel(out/'native.png'),source_sha256=sha(out/'native.png'),output_path=rel(out/'whole_canvas_1024.png'),output_sha256=sha(out/'whole_canvas_1024.png'),source_dimensions=list(im.size),output_dimensions=list(size),alpha16_footprint=db,method='Uniform complete-canvas normalization only',native_alpha_preserved=True,pixel_repair=False,review='PENDING_DIRECT'))
 rec=dict(generation_method='Codex built-in ImageGen',provider_native_path=path,native_path=rel(out/'native.png'),sha256=sha(out/'native.png'),dimensions=list(im.size),mode=im.mode,alpha_extrema=list(alpha.getextrema()),alpha_threshold_bounds=bounds,prompt_sha256=sha(out/'PROMPT.txt'),bound_inputs=json.loads((out/'PLAN.json').read_text()),native_pixels_preserved=True,attempt=1,neutral_displays=[rel(out/'audit_white.png'),rel(out/'audit_aqua.png')],source_review='PENDING_DIRECT_ALPHA_REVIEW',production_bound=False);write(out/'GENERATION_RECORD.json',rec);shutil.copyfile(__file__,out/'executed_preserve_geode_opening_states_v137.py');rows.append(dict(state=state,sha256=rec['sha256'],dimensions=rec['dimensions'],alpha=rec['alpha_extrema'],bounds=rec['alpha_threshold_bounds'],derivative_bounds=db))
 ip=b/'design/audit_impacts/job-geode-opening-continuity-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(ip,d)
print(json.dumps(rows))
