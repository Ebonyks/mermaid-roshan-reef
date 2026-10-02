from pathlib import Path
import json,hashlib,shutil,datetime
from PIL import Image
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
prefix='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/washing_pan/attempt_02';out=r/prefix
native=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-ad5f64a4-0c35-4410-ae30-e6dfb585c3ee.png')
inputs=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/pan_refine_v104_inputs.json');args=json.loads(inputs.read_text(encoding='utf-8'))
assert not (out/'native.png').exists();shutil.copyfile(native,out/'native.png');assert (out/'native.png').read_bytes()==native.read_bytes()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
(out/'PROMPT.txt').write_text(args['prompt'],encoding='utf-8',newline='\n');shutil.copyfile(inputs,out/'GENERATION_INPUT.json');shutil.copyfile(__file__,out/'executed_preserve_pan_refinement_v106.py')
im=Image.open(out/'native.png');assert im.mode=='RGBA';alpha=im.getchannel('A');bounds={str(n):list(alpha.point(lambda p:255 if p>=n else 0).getbbox()) for n in [1,16,128,240]}
references=[dict(path=rel(Path(p)),sha256=sha(Path(p)),role='ESTABLISHED_PAN_IDENTITY_COLOR_PERSPECTIVE') for p in args['references']]
previews=[]
for name,color in [('white',(255,255,255,255)),('aqua',(222,243,244,255))]:
 target=out/('audit_'+name+'.png');Image.alpha_composite(Image.new('RGBA',im.size,color),im).convert('RGB').save(target);previews.append(dict(path=rel(target),sha256=sha(target),role='AUDIT_DISPLAY_ONLY_WHOLE_NATIVE_CANVAS_ON_NEUTRAL_FIELD',not_runtime_art=True))
factor=1024/max(im.size);size=(round(im.width*factor),round(im.height*factor));der=out/'whole_canvas_1024.png';im.resize(size,Image.Resampling.LANCZOS).save(der)
write(out/'whole_canvas_1024.json',dict(path=rel(der),sha256=sha(der),dimensions=list(size),source_path=rel(out/'native.png'),source_sha256=sha(out/'native.png'),method='WHOLE_CANVAS_UNIFORM_DOWNSCALE_RGBA',alpha_preserved=True,pixel_repair=False,qualification='Uniform complete-canvas derivative only. No crop, mask, alpha cleanup, recolor or repainted pixels; native retained. Source/mounted/action review independent.'))
record=dict(id='washing_pan',attempt=2,native_path=rel(out/'native.png'),native_sha256=sha(out/'native.png'),native_dimensions=list(im.size),mode=im.mode,alpha_extrema=list(alpha.getextrema()),alpha_bounds_by_threshold=bounds,prompt_path=rel(out/'PROMPT.txt'),prompt_sha256=sha(out/'PROMPT.txt'),provider_native_path=str(native),provider_native_preserved=True,generation_method='BUILT_IN_CODEX_IMAGEGEN',transparent_background_requested=True,reference_images=references,audit_previews=previews,source_score=None,mounted_score=None,complete_action_score=None,owner_approval=None,runtime_binding_changed=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());write(out/'GENERATION_RECORD.json',record)
p=r/'ASSET_LICENSES.md';existing=p.read_text(encoding='utf-8');lines=[]
for target,description in [(out/'native.png','Exact provider-native ImageGen output, no modifications'),(out/'audit_white.png','Whole native canvas alpha displayed on white, audit-only'),(out/'audit_aqua.png','Whole native canvas alpha displayed on aqua, audit-only'),(der,'Uniform whole-canvas1024-long-edge technical derivative, original retained')]:
 if rel(target) not in existing:lines.append('| `'+rel(target)+'` | OpenAI ImageGen, owner-authorized Mermaid Roshan weak-pan refinement | Generated project artwork, provenance retained | `'+prefix+'/GENERATION_RECORD.json` | '+description+'; unbound review draft, not owner/runtime/action acceptance. |')
with p.open('a',encoding='utf-8',newline='\n') as stream:stream.write('\n'+'\n'.join(lines)+'\n')
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json';d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
print(json.dumps(dict(native=record['native_path'],sha256=record['native_sha256'],dimensions=record['native_dimensions'],alpha_extrema=record['alpha_extrema'],opaque_bounds=bounds['16'],derivative_size=list(size)),indent=2))
