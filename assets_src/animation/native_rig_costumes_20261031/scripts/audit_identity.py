"""Exact source restoration and protected face/hand pixels on actual engine captures."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'native_rig_stress_20261031'
def affine(v):
 a,b,c,d,x,y=v;return np.array([[a,c,x],[b,d,y],[0,0,1.]])
def region(points,transform):
 q=np.c_[np.array(points),np.ones(len(points))]@transform.T;im=Image.new('1',(1024,1024));ImageDraw.Draw(im).polygon([tuple(v[:2]) for v in q],fill=1);return np.array(im,dtype=bool)
def main():
 folder=ROOT/'evidence/render_original_v2';records=json.loads((folder/'samples.json').read_text(encoding='utf-8'));first=records[0]
 regions={'face':('Head',[(491,231),(611,231),(610,292),(550,312),(492,292)]),'left_hand':('LeftHand',[(369,518),(416,518),(416,577),(369,577)]),'right_hand':('Torso',[(680,513),(728,513),(728,576),(680,576)])}
 rows=[];restore_bad=[];control=False
 for clip,count in [('arm_bend',97),('blink',73),('tail_bend',121)]:
  rr=[r for r in records if r['clip']==clip];assert len(rr)==count
  for r in rr:
   name=f"{r['frame']:04}.png";original=np.array(Image.open(folder/clip/name).convert('RGBA'));prior=np.array(Image.open(OLD/'evidence/render_v10'/clip/name).convert('RGBA'))
   if not np.array_equal(original,prior):restore_bad.append({'clip':clip,'frame':r['frame'],'changed_pixels':int(np.any(original!=prior,axis=2).sum())})
   for theme in ['ballet','magician']:
    current=np.array(Image.open(ROOT/f'evidence/render_{theme}_v5'/clip/name).convert('RGBA'));diff=np.any(current!=original,axis=2);counts={}
    for key,(bone,points) in regions.items():
     transform=affine(r['bones'][bone])@np.linalg.inv(affine(first['bones'][bone]));mask=region(points,transform);counts[key]=int((diff&mask).sum())
     if not control and key=='face':
      faulty=original.copy();pos=np.argwhere(mask)[0];faulty[pos[0],pos[1],0]^=1;control=bool((np.any(faulty!=original,axis=2)&mask).sum()>0)
    # Headwear is above this protected lower-body region for the bounded tested poses.
    counts['alpha_below_235']=int(np.sum(current[235:,:,3]!=original[235:,:,3]))
    rows.append({'theme':theme,'clip':clip,'frame':r['frame'],'changed_protected_pixels':counts})
 frozen=json.loads((ROOT/'evidence/frozen_inputs.json').read_text(encoding='utf-8'));drift=[n for n,h in frozen['files'].items() if hashlib.sha256((ROOT.parents[2]/n).read_bytes()).hexdigest()!=h]
 report={'pass':not restore_bad and all(not any(r['changed_protected_pixels'].values()) for r in rows) and control and not drift,'original_rgba_frames_compared':len(records),'original_restoration_mismatches':restore_bad,'costumed_frame_cases':len(rows),'negative_control_one_face_pixel_detected':control,'frozen_input_mismatches':drift,'rows':rows,'limits':'Exact bounded face/hand regions and alpha below235, plus whole-original restoration. Does not accept unseen views, arbitrary clothing occlusion or target-device performance.'}
 (ROOT/'evidence/identity_audit.json').write_text(json.dumps(report,separators=(',',':'))+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2));raise SystemExit(0 if report['pass'] else 1)
if __name__=='__main__':main()
