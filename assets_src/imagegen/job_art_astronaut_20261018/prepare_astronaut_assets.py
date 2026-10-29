from pathlib import Path
import json,hashlib,shutil,subprocess
from PIL import Image
import numpy as np
root=Path.cwd();src=root/'assets_src/imagegen/job_art_astronaut_20261018';out=root/'assets/opera/worlds/widgets'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((src/'prompts.json').read_text());by={r['id']:r for r in rows}
records=json.loads((src/'pipe_registration.json').read_text())['records']
def bbox(im):
    b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();assert b
    return (max(0,b[0]-4),max(0,b[1]-4),min(im.width,b[2]+4),min(im.height,b[3]+4))
def prepare(id,native_id,size=(256,256),family=None,filename=None,growth=1.):
    native=root/by[native_id]['native_path'];image=Image.open(native).convert('RGBA');assert image.getchannel('A').getextrema()[0]==0
    b=bbox(image)
    if family:
        boxes=[bbox(Image.open(root/by[n]['native_path']).convert('RGBA')) for n in family]
        b=(min(x[0] for x in boxes),min(x[1] for x in boxes),max(x[2] for x in boxes),max(x[3] for x in boxes))
    crop=image.crop(b);scale=min((size[0]-16)/crop.width,(size[1]-16)/crop.height)*growth
    small=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',size);xy=((size[0]-small.width)//2,8 if id.startswith('launch_flame') else (size[1]-small.height)//2);canvas.alpha_composite(small,xy)
    output=out/(filename or ('widget_'+id+'.png'));canvas.save(output)
    records.append({'id':id,'native':native.relative_to(root).as_posix(),'native_sha256':sha(native),'output':output.relative_to(root).as_posix(),'output_sha256':sha(output),'dimensions':list(size),'source_crop':list(b),'uniform_scale':scale,'placement':list(xy),'growth_scale':growth,'method':'Uniform downsample and transparent crop/pad only. No painting, warp, recolor or rotation.'})
prepare('pipe_plate','pipe_plate',family=['pipe_plate','pipe_plate_selected_retry'])
prepare('pipe_plate_selected','pipe_plate_selected_retry',family=['pipe_plate','pipe_plate_selected_retry'])
prepare('pipe_intake','pipe_intake',family=['pipe_intake','pipe_intake_fueled'])
prepare('pipe_intake_fueled','pipe_intake_fueled',family=['pipe_intake','pipe_intake_fueled'])
prepare('pipe_napping_imp','imp_napping',filename='widget_pipe_napping_imp.png')
for n in range(3):prepare('patch_'+str(n),'patch_'+str(n),filename='widget_target_astronaut_piece_'+str(n)+'.png')
prepare('launch_cloud','launch_cloud')
for n,growth in enumerate([.55,.7,.85,1.]):prepare('launch_flame_'+str(n),'launch_flame_clean',(256,512),growth=growth)
# Align the tank's one outlet with the existing left-entry lane. Its whole
# contour remains inside the canvas; only uniform scale/translation is used.
code=(src/'prepare_pipe_family.py').read_text().split('records=[];')[0]
space={};exec(code,space);native=root/by['pipe_tank']['native_path'];image=Image.open(native).convert('RGBA');b=bbox(image)
port=space['port_center'](image,(.78,.35,1,.72));target=np.array([240.,128.]);scale=min(8./(b[2]-port[0]),232./(port[0]-b[0]),120./(port[1]-b[1]),120./(b[3]-port[1]))
offset=target-port*scale;crop=image.crop(b);small=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(256,256));xy=tuple(round(v) for v in offset+np.array(b[:2])*scale);canvas.alpha_composite(small,xy);output=out/'widget_pipe_tank.png';canvas.save(output)
records.append({'id':'pipe_tank','native':native.relative_to(root).as_posix(),'native_sha256':sha(native),'output':output.relative_to(root).as_posix(),'output_sha256':sha(output),'source_port':port.tolist(),'target_port':target.tolist(),'uniform_scale':float(scale),'translation':offset.tolist(),'source_crop':list(b),'method':'Uniform downsample, crop and transparent pad/translation; exact outlet center; no warped tank or painted connector.'})
guide_record=json.loads((src/'guide_reuse.json').read_text())
assert sha(root/guide_record['native']) == guide_record['native_sha256']
assert sha(root/guide_record['output']) == guide_record['output_sha256']
records.append(guide_record)
old=[]
for n in range(3):
    path='assets/opera/worlds/widgets/widget_target_astronaut_piece_'+str(n)+'.png';data=subprocess.check_output(['git','show','6fb96aeb441952c1053cc5ce18435fc57fc1d1ab:'+path]);old.append({'path':path,'baseline':'6fb96aeb441952c1053cc5ce18435fc57fc1d1ab','original_sha256':hashlib.sha256(data).hexdigest(),'replacement':'Owner-commissioned JB-AST-03 square/circle/star painted metal patch family.'})
provenance={'provider':'builtin ImageGen','model_revision':'unexposed; owner approved available tool','baseline':'6fb96aeb441952c1053cc5ce18435fc57fc1d1ab','records':records,'replaced_placeholders':old,'limits':'Candidate only; source and current Mobile scene/transition/input review at4.5 remain required; device/child/owner remain open.'};(src/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
job={'id':'astronaut-launch-effects-20261018','action':'Rocket exhaust grows while the existing deliberate hold charges the launch.','fixed_parts':'Approved rocket identity and existing launch movement/input/save logic; upper-center plume attachment.','moving_parts':'Existing progress selects four uniform whole-picture growth scales; four whole cloud cutouts follow the existing exhaust centers.','method':'One usable native ImageGen flame-only still,4declared scale derivatives and an ImageGen cloud; Canvas growth. These are not4independent authored keys, character acting, or generated video. No frame campaign.','attempts':2,'cap':2,'usage':'2builtin flame calls, first rejected for unwanted hardware and second local cleanup selected;1cloud call; monetary revision/usage unexposed; no CLI/API spend.','native_reject':'launch_flame_full_native.png includes unwanted metal nozzle.','growth_scales':[.55,.7,.85,1.0],'pivot':'Top-center,8px runtime transparent margin; draw behind the existing rocket to preserve nozzle contact.','review':'All affected growth boundaries/contact/settle need current Mobile/frame-step review. No final motion/device/child/owner acceptance.'};(src/'launch_effect_job.json').write_text(json.dumps(job,indent=2)+'\n')
license=root/'ASSET_LICENSES.md';text=license.read_text()
for n in range(3):
    needle='- `assets/opera/worlds/widgets/widget_target_astronaut_piece_'+str(n)+'.png` - 256x256 project-original'
    text=text.replace(needle,'- Historical placeholder at6fb96aeb (replaced2026-10-18): `assets/opera/worlds/widgets/widget_target_astronaut_piece_'+str(n)+'.png` - 256x256 project-original')
for row in rows:
    path=row['native_path']
    if '| `'+path+'` |' not in text:text+='\n| `'+path+'` | OpenAI builtin ImageGen; model revision unexposed | Owner-requested generated game object; OpenAI output terms | https://openai.com/policies/terms-of-use/ | Native preserved; '+row['status']+'; exact prompt/hash in assets_src/imagegen/job_art_astronaut_20261018/prompts.json. |'
for row in records:
    path=row['output']
    if '| `'+path+'` |' not in text:text+='\n| `'+path+'` | OpenAI ImageGen runtime derivative | Owner-requested generated object; OpenAI output terms | https://openai.com/policies/terms-of-use/ | '+row['output_sha256']+'; uniform source-preserving preparation/registration in assets_src/imagegen/job_art_astronaut_20261018/provenance.json. |'
text+='\n| `assets_src/imagegen/job_art_astronaut_20261018/guide_hand_reused_native.png` | OpenAI builtin ImageGen, exact campaign source | Owner-requested generated guide; OpenAI output terms | https://openai.com/policies/terms-of-use/ | Original source/prompt and exact reuse hash in provenance.json. |\n';license.write_text(text)
impact=root/'design/audit_impacts/job-art-astronaut-20261018.json';d=json.loads(impact.read_text());d['files']=sorted(set(d['files']+['ASSET_LICENSES.md']+[p.relative_to(root).as_posix() for p in src.rglob('*') if p.is_file()]+[r['output'] for r in records]));impact.write_text(json.dumps(d,indent=2)+'\n')
# This saved preparation script consumes retained local sources.
# The sibling pipe-registration script is retained separately.
print('Prepared',len(records),'runtime assets; preserved26generation attempts plus exact reused hand source')
