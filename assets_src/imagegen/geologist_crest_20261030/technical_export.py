from pathlib import Path
import subprocess,hashlib,json,importlib.util,shutil
from PIL import Image
import numpy as np
U=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef');S=Path(__file__).parent;A=U/'assets_src/imagegen/geologist_crest_20261030';E=r'C:/Program Files/Aseprite/Aseprite.exe';N=A/'take01_native.png';commands=[]
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
 c=[E,'--batch',*map(str,args)];q=subprocess.run(c,capture_output=True,timeout=180,creationflags=0x08000000);assert q.returncode==0,q.stdout+q.stderr;commands.append(c)
assert Image.open(N).size==(1254,1254)
run([N,'--save-as',A/'crest_native.aseprite']);run([A/'crest_native.aseprite','--save-as',A/'native_roundtrip.png'])
aa=np.array(Image.open(N).convert('RGBA'));bb=np.array(Image.open(A/'native_roundtrip.png').convert('RGBA'));mask=(aa[:,:,3]>=16)|(bb[:,:,3]>=16);delta=int(np.count_nonzero(np.any(aa!=bb,axis=2)&mask));assert delta==0
run([A/'crest_native.aseprite','--scale',str(216/1254),'--save-as',A/'crest_uniform216.png'])
output=U/'assets/opera/worlds/ui/crests/opera_crest_geologist.png';lua=S/'export_whole_crest.lua';lua.write_text('local s=app.open("'+(A/'crest_uniform216.png').as_posix()+'")\nlocal n=Sprite(256,256,ColorMode.RGB)\nlocal im=Image(256,256,ColorMode.RGB)\nim:drawImage(s.cels[1].image,Point(20,20))\nn.cels[1].image=im\nn:saveAs("'+(A/'crest_whole256.aseprite').as_posix()+'")\nn:saveAs("'+output.as_posix()+'")\nn:close()\ns:close()\n',encoding='utf-8');run(['--script',lua])
spec=importlib.util.spec_from_file_location('measure',U/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);profile=mod.cutout_profile(output.read_bytes());assert profile['verdict']=='CUTOUT_OK',profile
out=dict(stable_id='FV-8C7C289334A2',baseline='803dbac68705d46bcb4a5da4d060a0ae8cf09d6d',backend='built-in image_gen.imagegen',model_version='NOT_EXPOSED',request_id='NOT_EXPOSED',seed='NOT_EXPOSED',usage='NOT_EXPOSED',returned_keys=['image_url','output_hint'],native_original=r'C:/Users/Peter/.codex/generated_images/01a119cc-74b1-7d23-b956-126129405418/exec-1dbb2517-9c02-4fe3-964b-52af2f6ad187.png',native_sha256=sha(N),native_dimensions=[1254,1254],static_takes=1,static_take_cap=2,rejected_takes=0,animation_calls=0,aseprite_version=subprocess.check_output([E,'--version'],text=True).strip(),native_visible_RGBA_changed_pixels=delta,technical_operations='Actual Aseprite native master and roundtrip preserve every visibleRGBA pixel. Uniform216/1254 complete-source resize then20px transparentpadding on eachside to256. No crop of authored pixels, recolour, deformation or code-drawn appearance.',commands=commands,exports=[dict(role='whole_geologist_crest',path=output.relative_to(U).as_posix(),dimensions=[256,256],sha256=sha(output),cutout=profile)],originals_preserved=True)
wr(A/'DERIVATION.json',out);wr(S/'DERIVATION.json',out)
for p in [A/'PLAN.json',S/'PLAN.json']:
 d=json.loads(p.read_text(encoding='utf-8'));d['generation'].update(state='TAKE01_WHOLE256_EXPORTED_NATIVE_CONTEXT_PENDING',native_sha256=sha(N));wr(p,d)
print('R113_TECHNICAL_EXPORT_PASS',profile,sha(output))
