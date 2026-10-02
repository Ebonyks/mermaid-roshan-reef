from pathlib import Path
import json,hashlib,shutil,datetime
from PIL import Image
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
base=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
input_path=Path(__file__).with_name('geode_embedded_v97_inputs.json')
job=json.loads(input_path.read_text(encoding='utf-8'))
out=base/'open_geode/attempt_02';assert not out.exists();out.mkdir(parents=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
src=Path(job['provider_native_path']);dst=out/'native.png';shutil.copyfile(src,dst);assert sha(src)==sha(dst)
im=Image.open(dst);assert im.mode=='RGBA';alpha=im.getchannel('A')
boxes={str(t):alpha.point(lambda p:255 if p>=t else 0).getbbox() for t in [1,16,128,240]}
previews=[]
for label,color in [('white',(255,255,255,255)),('aqua',(194,230,228,255))]:
 p=out/('audit_'+label+'.png');canvas=Image.new('RGBA',im.size,color);canvas.alpha_composite(im);canvas.convert('RGB').save(p)
 previews.append(dict(path=rel(p),sha256=sha(p),role='AUDIT_DISPLAY_ONLY_WHOLE_NATIVE_CANVAS_ON_NEUTRAL_FIELD',not_runtime_art=True))
prompt=job['prompt'];(out/'PROMPT.txt').write_text(prompt+'\n',encoding='utf-8',newline='\n')
refs=[dict(path=p,sha256=sha(r/p),role='CLOSED_GEODE_IDENTITY_MATERIAL' if i==0 else 'PAINTED_CRYSTAL_FACET_COLOR_ONLY_NOT_LOOSE_REWARD') for i,p in enumerate(job['references'])]
record=dict(id=job['id'],attempt=2,native_path=rel(dst),native_sha256=sha(dst),native_dimensions=list(im.size),mode=im.mode,alpha_extrema=alpha.getextrema(),alpha_bounds_by_threshold=boxes,prompt_path=rel(out/'PROMPT.txt'),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),provider_native_path=str(src),provider_native_preserved=True,generation_method='BUILT_IN_CODEX_IMAGEGEN',transparent_background_requested=True,reference_images=refs,audit_previews=previews,source_score=None,mounted_score=None,complete_action_score=None,owner_approval=None,runtime_binding_changed=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
write(out/'GENERATION_RECORD.json',record)
der=out/'whole_canvas_1024.png';scale=min(1,1024/max(im.size));size=tuple(round(n*scale) for n in im.size);im.resize(size,Image.Resampling.LANCZOS).save(der)
write(out/'whole_canvas_1024.json',dict(path=rel(der),sha256=sha(der),dimensions=list(size),source_path=rel(dst),source_sha256=sha(dst),method='WHOLE_CANVAS_UNIFORM_DOWNSCALE_RGBA_PNG',alpha_preserved=True,pixel_repair=False,qualification='Technical derivative only; native original retained without crop, mask, recolor or alpha cleanup.'))
shutil.copyfile(input_path,base/'executed_geode_embedded_v97_inputs.json');shutil.copyfile(__file__,base/'executed_preserve_geode_embedded_v97.py')
write(base/'GEODE_OWNER_CORRECTION_V2.json',dict(status='OWNER_REQUIRED_EMBEDDED_CRYSTALS_REBUILD_GENERATED_REVIEW_PENDING',request='Geode opens to show crystals inside it; crystals must stay embedded in its cavities and never drop out as loot.',superseded_open_source='open_geode/attempt_01/native.png',historical_source_finish_score=4.6,current_semantic_score=3.0,new_open_source=rel(dst),detached_crystal_source_role='EXCLUDED_FROM_GEODE_REVEAL; source finish opinion does not authorize loot behavior.',production_changed=False))
license_path=r/'ASSET_LICENSES.md';text=license_path.read_text(encoding='utf-8')
for p in [dst,der,*[r/x['path'] for x in previews]]:
 line='| '+rel(p)+' | Codex built-in ImageGen; owner-directed geode cavity correction | OpenAI generated game artwork | Local generation provenance: '+rel(out/'GENERATION_RECORD.json')+' | Native original preserved; '+('uniform whole-canvas technical downscale' if p==der else 'neutral audit display only' if 'audit_' in p.name else 'unmodified native generation')+'; unbound review draft |'
 if rel(p) not in text:text+='\n'+line
license_path.write_text(text.rstrip()+'\n',encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['scope']+=' Owner correction: opened geode must reveal crystals permanently embedded inside both mineral cavities; remove detached reward interpretation from the reversible staging. Preserve earlier source and opinions as historical.';d['files']=sorted(set(d['files'])|{rel(p) for p in base.rglob('*') if p.is_file()});write(impact,d)
halfboxes=[]
for left,right in [(0,im.width//2),(im.width//2,im.width)]:
 box=alpha.crop((left,0,right,im.height)).point(lambda p:255 if p>=16 else 0).getbbox();halfboxes.append([box[0]+left,box[1],box[2]+left,box[3]])
print(json.dumps(dict(native=record['native_dimensions'],alpha=alpha.getextrema(),bounds=boxes,half_boxes=halfboxes,derivative_size=size,sha256=sha(dst)),indent=2))
