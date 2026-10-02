from pathlib import Path
import json, hashlib, shutil, datetime
from PIL import Image

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
inputs=Path(__file__).with_name('geology_imagegen_v91_inputs.json')
jobs=json.loads(inputs.read_text(encoding='utf-8'))
queue=json.loads((out/'GENERATION_QUEUE_V1.json').read_text(encoding='utf-8'))
records=[]
for job in jobs:
    prompt=job['prompt'] or next(x['prompt'] for x in queue['jobs'] if x['id']==job['id'])
    src=Path(job['provider_native_path']); data=src.read_bytes()
    dst=out/job['id']/('attempt_%02d'%job['attempt']); dst.mkdir(parents=True,exist_ok=True)
    native=dst/'native.png'
    if native.exists(): assert native.read_bytes()==data, 'Cannot rewrite a different original'
    else: shutil.copyfile(src,native)
    (dst/'PROMPT.txt').write_text(prompt+'\n',encoding='utf-8',newline='\n')
    im=Image.open(native); assert im.mode=='RGBA'
    a=im.getchannel('A')
    boxes={str(t):a.point(lambda p:255 if p>=t else 0).getbbox() for t in [1,16,128,240]}
    previews=[]
    for label,color in [('white',(255,255,255,255)),('aqua',(194,230,228,255))]:
        preview=dst/('audit_'+label+'.png'); canvas=Image.new('RGBA',im.size,color);canvas.alpha_composite(im);canvas.convert('RGB').save(preview)
        previews.append(dict(path=preview.relative_to(r).as_posix(),sha256=hashlib.sha256(preview.read_bytes()).hexdigest(),role='AUDIT_DISPLAY_ONLY_WHOLE_NATIVE_CANVAS_ALPHA_ON_NEUTRAL_FIELD',not_runtime_art=True))
    rec=dict(id=job['id'],attempt=job['attempt'],native_path=native.relative_to(r).as_posix(),native_sha256=hashlib.sha256(data).hexdigest(),native_dimensions=list(im.size),mode=im.mode,alpha_extrema=list(a.getextrema()),alpha_clear_pixels=a.histogram()[0],alpha_bounds_by_threshold=boxes,prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),prompt_path=(dst/'PROMPT.txt').relative_to(r).as_posix(),generation_method='BUILT_IN_CODEX_IMAGEGEN',provider_native_path=str(src),provider_native_preserved=True,transparent_background_requested=True,reference_images=[],source_direct_generated_display_review=True,source_score=None,mounted_score=None,complete_action_score=None,owner_approval=None,runtime_binding_changed=False,audit_previews=previews,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (dst/'GENERATION_RECORD.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8',newline='\n');records.append(rec)
shutil.copyfile(Path(__file__),out/'executed_preserve_geology_imagegen_v91.py')
shutil.copyfile(inputs,out/'executed_geology_imagegen_v91_inputs.json')
(out/'GENERATED_NATIVE_REGISTER_V1.json').write_text(json.dumps(dict(status='SIX_NATIVE_GENERATIONS_PRESERVED_INDIVIDUAL_REVIEW_PENDING',records=records),indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps([{k:x[k] for k in ['id','attempt','native_dimensions','alpha_bounds_by_threshold','native_sha256']} for x in records],indent=2))
