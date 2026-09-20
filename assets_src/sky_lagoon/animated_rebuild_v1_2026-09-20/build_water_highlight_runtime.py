from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'water';D=W/'assets/sprites/sky_lagoon/animated_v1'
report=[]
for name,width in [('arrival',256),('castle',512)]:
 atlas=Image.open(P/f'{name}-highlights-atlas.png').convert('RGBA')
 assert atlas.size==(width*4,768)
 frames=[atlas.crop(((n%4)*width,(n//4)*256,(n%4+1)*width,(n//4+1)*256)) for n in range(12)]
 hashes=[hashlib.sha256(f.tobytes()).hexdigest() for f in frames]
 assert len(set(hashes))==12
 arrays=[np.array(f).astype(float) for f in frames]
 # Compare rendered alpha, including the loop boundary, to detect a discontinuous reset.
 steps=[float(np.abs(arrays[n][:,:,3]-arrays[(n+1)%12][:,:,3]).mean()) for n in range(12)]
 assert steps[-1] <= max(steps[:-1])*1.5
 out=Image.new('RGBA',(width*4,1024 if name=='castle' else 768));out.paste(atlas,(0,0));out.save(D/f'water_{name}_highlights.png')
 report.append({'id':name,'frames':12,'frame_sha256':hashes,'mean_alpha_step':steps,'runtime_size':list(out.size),'loop_boundary_pass':True})
(P/'HIGHLIGHT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print('HIGHLIGHTS|12 unique frames per pool; loop alpha step and dimensions OK')
