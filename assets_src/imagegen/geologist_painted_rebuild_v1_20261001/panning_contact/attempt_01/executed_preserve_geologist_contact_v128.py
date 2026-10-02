from pathlib import Path
import shutil,json,hashlib
from PIL import Image
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=b/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001/panning_contact/attempt_01'
source=Path(r'C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-40184657-7d4b-4000-9e3f-c038579a4104.png')
assert not (out/'native.png').exists();shutil.copyfile(source,out/'native.png')
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
im=Image.open(out/'native.png');assert im.mode=='RGBA';alpha=im.getchannel('A')
bounds={str(t):alpha.point(lambda v:255 if v>=t else 0).getbbox() for t in [1,8,16,64,128,240]}
fields=[]
for name,color in [('audit_white.png',(255,255,255,255)),('audit_aqua.png',(223,244,244,255))]:
 display=Image.new('RGBA',im.size,color);display.alpha_composite(im);display.convert('RGB').save(out/name);fields.append(rel(out/name))
size=(1024,round(im.height*1024/im.width));im.resize(size,Image.Resampling.LANCZOS).save(out/'whole_canvas_1024.png')
write(out/'whole_canvas_1024.json',dict(source_path=rel(out/'native.png'),source_sha256=sha(out/'native.png'),output_path=rel(out/'whole_canvas_1024.png'),output_sha256=sha(out/'whole_canvas_1024.png'),source_dimensions=list(im.size),output_dimensions=list(size),method='Uniform complete-canvas normalization only',native_alpha_preserved=True,pixel_repair=False,review='PENDING_DIRECT'))
record=dict(generation_method='Codex built-in ImageGen',provider_native_path=str(source),native_path=rel(out/'native.png'),sha256=sha(out/'native.png'),dimensions=list(im.size),mode=im.mode,alpha_extrema=list(alpha.getextrema()),alpha_threshold_bounds=bounds,prompt_path=rel(out/'PROMPT.txt'),prompt_sha256=sha(out/'PROMPT.txt'),bound_inputs=json.loads((out/'PLAN.json').read_text()),native_pixels_preserved=True,attempt=1,neutral_displays=fields,source_review='PENDING_DIRECT_ALPHA_REVIEW',production_bound=False)
write(out/'GENERATION_RECORD.json',record);shutil.copyfile(__file__,out/'executed_preserve_geologist_contact_v128.py')
ip=b/'design/audit_impacts/job-pan-painted-placement-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(ip,d)
print(json.dumps({k:record[k] for k in ['sha256','dimensions','alpha_extrema','alpha_threshold_bounds']}))
