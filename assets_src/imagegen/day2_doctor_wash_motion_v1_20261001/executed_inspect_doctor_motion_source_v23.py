from pathlib import Path
from PIL import Image
import hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'assets_src/imagegen/day2_doctor_wash_motion_v1_20261001'
provider=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-714def18-196e-4a0b-98a0-0107131b2c71.png')
target=out/'motion_key01_attempt01_native.png';assert not target.exists();shutil.copyfile(provider,target)
prompt=json.loads((Path(__file__).parent/'doctor_motion_prompt01.json').read_text(encoding='utf-8'))
prompt['prompt_sha256']=hashlib.sha256(prompt['prompt'].encode()).hexdigest();prompt['provider_original']=str(provider);prompt['output_path']=target.relative_to(r).as_posix();prompt['output_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
(out/'MOTION_KEY01_ATTEMPT01_PROMPT.json').write_text(json.dumps(prompt,indent=2)+'\n',encoding='utf-8',newline='\n')
image=Image.open(target).convert('RGBA');alpha=image.getchannel('A')
samples={str(xy):image.getpixel(xy) for xy in [(680,760),(685,765),(690,770),(695,780),(700,775),(705,750)] if xy[0]<image.width and xy[1]<image.height}
window=alpha.crop((670,735,735,810))
info=dict(dimensions=list(image.size),mode=image.mode,sha256=prompt['output_sha256'],bbox_alpha16=alpha.point(lambda x:255 if x>=16 else 0).getbbox(),bbox_alpha128=alpha.point(lambda x:255 if x>=128 else 0).getbbox(),inspection_window=[670,735,735,810],window_alpha_extrema=window.getextrema(),samples=samples,qualification='Alpha measurements only; direct source/composite review remains pending.')
(out/'MOTION_KEY01_ATTEMPT01_ALPHA.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8',newline='\n')
for name,color in [('white',(255,255,255,255)),('aqua',(207,239,237,255))]:
 background=Image.new('RGBA',image.size,color);background.alpha_composite(image)
 background.convert('RGB').save(out/('motion_key01_attempt01_review_'+name+'.png'))
shutil.copyfile(__file__,out/'executed_inspect_doctor_motion_source_v23.py')
print(json.dumps(info))
