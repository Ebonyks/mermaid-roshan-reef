from pathlib import Path
import datetime,hashlib,json,shutil
from PIL import Image
import numpy as np
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=r/'assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001'
provider=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-288d8d67-89b3-47a3-ae2c-948a5f4ab387.png');native=out/'attempt01_native.png';assert not native.exists();shutil.copyfile(provider,native)
im=Image.open(native);assert im.mode=='RGBA';pixels=np.asarray(im);a=pixels[:,:,3]
alpha={'mode':im.mode,'dimensions':list(im.size),'sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'bytes':native.stat().st_size,'alpha_nonzero_fraction':float((a>0).mean()),'alpha_opaque_fraction':float((a==255).mean()),'bbox_alpha16':im.getchannel('A').point(lambda x:255 if x>=16 else 0).getbbox(),'bbox_alpha128':im.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),'pure_red_alpha1_pixels':int(((pixels[:,:,0]==255)&(pixels[:,:,1]==0)&(pixels[:,:,2]==0)&(a==1)).sum()),'pure_red_alpha_atleast16_pixels':int(((pixels[:,:,0]==255)&(pixels[:,:,1]==0)&(pixels[:,:,2]==0)&(a>=16)).sum()),'qualification':'NativeRGBA preserved. Transparency-display artifacts require neutral-background inspection; no hiddenRGB/alpha cleanup or subject repair.'}
(out/'ATTEMPT01_ALPHA.json').write_text(json.dumps(alpha,indent=2)+'\n',encoding='utf-8')
for name,color in [('white',(255,255,255,255)),('aqua',(218,244,239,255))]:
 diagnostic=Image.new('RGBA',im.size,color);diagnostic.alpha_composite(im);diagnostic.convert('RGB').save(out/('attempt01_review_'+name+'.png'))
prompt=out/'ATTEMPT01_PROMPT.json';d=json.loads(prompt.read_text(encoding='utf-8'));d.update(status='GENERATED_SOURCE_AUDIT_PENDING',native_path=native.relative_to(r).as_posix(),native_sha256=alpha['sha256'],provider_original=str(provider),source_pixels_modified=False);prompt.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(__file__,out/'executed_inspect_clean_hands_candidate_v38.py')
impact=r/'design/audit_impacts/job-wash-contact-study-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in out.rglob('*') if x.is_file()});impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps(alpha))
