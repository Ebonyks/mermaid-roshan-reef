from pathlib import Path
import subprocess,hashlib,json,importlib.util,datetime
from PIL import Image
import numpy as np
R=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-geologist-seam-20261030');A=R/'assets_src/imagegen/geologist_geode_seams_20261030';E=r'C:/Program Files/Aseprite/Aseprite.exe';N=A/'take01_native.png';commands=[]
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
 c=[E,'--batch',*map(str,args)];q=subprocess.run(c,capture_output=True,timeout=180,creationflags=0x08000000);assert q.returncode==0,(q.stdout+q.stderr);commands.append(c)
run([N,'--save-as',A/'seams_native.aseprite']);run([A/'seams_native.aseprite','--save-as',A/'native_roundtrip.png']);aa=np.array(Image.open(N).convert('RGBA'));bb=np.array(Image.open(A/'native_roundtrip.png').convert('RGBA'));m=(aa[:,:,3]>=16)|(bb[:,:,3]>=16);changed=int(np.count_nonzero(np.any(aa!=bb,axis=2)&m));assert changed==0
roles=[('closed',27),('done',849)];lua=S/'export_whole_states.lua';t='local s=app.open("'+(A/'seams_native.aseprite').as_posix()+'")\nlocal original=s.cels[1].image\n'
for name,x in roles:t+='local n=Sprite(887,887,ColorMode.RGB)\nlocal im=Image(887,887,ColorMode.RGB)\nim:drawImage(original,Point(-'+str(x)+',-3))\nn.cels[1].image=im\nn:saveAs("'+(A/(name+'_crop.aseprite')).as_posix()+'")\nn:close()\n'
t+='s:close()\n';lua.write_text(t,encoding='utf-8');run(['--script',lua]);exports=[]
spec=importlib.util.spec_from_file_location('measure',R/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for name,x in roles:
 p=R/('assets/opera/worlds/props/geologist_geode_seam_'+name+'_painted.png');run([A/(name+'_crop.aseprite'),'--scale',str(512/887),'--save-as',p]);assert Image.open(p).size==(512,512);profile=mod.cutout_profile(p.read_bytes());assert profile['verdict']=='CUTOUT_OK',profile;exports.append(dict(role=name,path=p.relative_to(R).as_posix(),dimensions=[512,512],sha256=sha(p),crop=[x,3,887,887],uniform_scale=512/887,cutout=profile))
a=np.array(Image.open(R/exports[0]['path']).convert('RGBA'));b=np.array(Image.open(R/exports[1]['path']).convert('RGBA'));ma=a[:,:,3]>=16;mb=b[:,:,3]>=16;iou=float((ma&mb).sum()/(ma|mb).sum());assert iou>0.98,iou
out=dict(stable_id='FV-4502C5860C45',baseline='51b2e1ef7b32d155786277871fc3f5e941145ea6',backend='built-in image_gen.imagegen',model_version='NOT_EXPOSED',request_id='NOT_EXPOSED',seed='NOT_EXPOSED',usage='NOT_EXPOSED',exposed_result_fields=['image_url','output_hint'],native_original=json.loads((A/'GENERATION.json').read_text(encoding='utf-8'))['original'],native_sha256=sha(N),native_dimensions=[1774,887],takes=1,rejects=0,animation_calls=0,aseprite_version=subprocess.check_output([E,'--version'],text=True).strip(),native_visible_rgba_changed_pixels=changed,technical_operations='Actual Aseprite whole native sheet/master/roundtrip, integer crop887-square at27,3 and849,3. Eachcrop extends3transparentpixels below originalcanvas, no visibleart removed; same512/887 uniformscale. Complete authored closed/mint-cleft states, no tint/deformation/newappearance pixels/composited objectparts.',state_alpha16_mask_iou=iou,registration='Same integer crop y, x translations align native bbox centres within1px, unchanged uniform scale/common512canvas. Small authored mineral edge differences retained and declared, not synthetic morph/interpolation.',commands=commands,exports=exports)
wr(A/'DERIVATION.json',out);wr(S/'DERIVATION.json',out)
for root in [S,A]:
 p=root/'PLAN.json';d=json.loads(p.read_text(encoding='utf-8'));d['generation'].update(state='TAKE01_TWO_WHOLE_STATES_EXPORTED',native_sha256=sha(N));wr(p,d)
print(json.dumps(dict(roundtrip_visible_changed=changed,mask_iou=iou,exports=exports)))
