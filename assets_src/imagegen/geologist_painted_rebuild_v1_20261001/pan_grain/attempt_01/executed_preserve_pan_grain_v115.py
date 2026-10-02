from pathlib import Path
import shutil,json,hashlib
from PIL import Image
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001/pan_grain/attempt_01';source=Path(r'C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-e467390c-8ab1-4312-a1d1-047530faaa40.png');assert not (out/'native.png').exists();shutil.copyfile(source,out/'native.png')
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
im=Image.open(out/'native.png');assert im.mode=='RGBA';alpha=im.getchannel('A');bounds={str(t):alpha.point(lambda p:255 if p>=t else 0).getbbox() for t in [1,8,16,64,128,240]}
previews=[]
for name,color in [('audit_white.png',(255,255,255,255)),('audit_aqua.png',(223,244,244,255))]:
 field=Image.new('RGBA',im.size,color);field.alpha_composite(im);field.convert('RGB').save(out/name);previews.append(rel(out/name))
record=dict(generation_method='Codex built-in ImageGen',provider_native_path=str(source),native_path=rel(out/'native.png'),sha256=sha(out/'native.png'),dimensions=list(im.size),mode=im.mode,alpha_extrema=list(alpha.getextrema()),alpha_threshold_bounds=bounds,prompt_path=rel(out/'PROMPT.txt'),prompt_sha256=sha(out/'PROMPT.txt'),reference=json.loads((out/'PLAN.json').read_text()),native_pixels_preserved=True,attempt=1,neutral_displays=previews,source_review='PENDING_DIRECT_NEUTRAL_ALPHA_REVIEW',production_bound=False);write(out/'GENERATION_RECORD.json',record);shutil.copyfile(__file__,out/'executed_preserve_pan_grain_v115.py')
impact=b/'design/audit_impacts/job-pan-painted-placement-20261001.json';d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
print(json.dumps({k:record[k] for k in ['sha256','dimensions','mode','alpha_extrema','alpha_threshold_bounds']}))
