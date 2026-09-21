from pathlib import Path
from PIL import Image
import subprocess,numpy as np,json,math,hashlib
p=Path(__file__).resolve().parent;out=p/'exports';out.mkdir(exist_ok=True);records=[]
for bank,world,cycle in [('near',(300,950),4.8),('far',(600,900),8.0)]:
 folder=p/bank
 r=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','base='+str(folder),'--script',str(folder/'author.lua')],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180)
 assert r.returncode==0,r.stderr
 arrays=[]
 for k in range(4):
  im=Image.open(folder/f'bank-{k:02d}.png').convert('RGBA');im=im.convert('RGBa').resize((im.width//2,im.height//2),Image.Resampling.LANCZOS).convert('RGBA');arrays.append(np.asarray(im).astype(float)/255)
 alpha=np.minimum.reduce([a[:,:,3:4] for a in arrays]);fields={'add':[],'subtract':[]}
 for k,a in enumerate(arrays):
  delta=(a[:,:,:3]-arrays[0][:,:,:3])*alpha
  for sign,label in [(1,'add'),(-1,'subtract')]:
   rgb=np.rint(np.clip(delta*sign,0,1)*255).astype('uint8');fields[label].append(Image.fromarray(np.dstack([rgb,np.full(rgb.shape[:2],255,dtype='uint8')])))
 H,W=arrays[0].shape[:2]
 for start in range(0,W,1020):
  end=min(start+1020,W);ww=end-start;cw=2**math.ceil(math.log2(ww+4));ch=2**math.ceil(math.log2(H+4))
  for label in ['add','subtract']:
   atlas=Image.new('RGBA',(cw*2,ch*2),(0,0,0,255));regions=[]
   for k,im in enumerate(fields[label]):
    patch=im.crop((start-2,-2,end+2,H+2));patch.putalpha(255);atlas.paste(patch,(k%2*cw,k//2*ch));regions.append([k%2*cw+2,k//2*ch+2,ww,H])
   file=f'cloud_bank_{bank}_{start//1020}_{label}.png';atlas.save(out/file);records.append({'file':file,'sha256':hashlib.sha256((out/file).read_bytes()).hexdigest(),'size':list(atlas.size),'position':[world[0]+start*2,world[1]],'regions':regions,'cycle':cycle})
(out/'EXPORT.json').write_text(json.dumps(records,indent=2)+'\n');print('CLOUD_EXPORTS',len(records),flush=True)
