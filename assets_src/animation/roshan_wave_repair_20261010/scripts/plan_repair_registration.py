from pathlib import Path
import importlib.util,json,cv2,numpy as np
ROOT=Path.cwd();P=ROOT/'assets_src/animation/roshan_wave_repair_20261010/whole_key_repair_01'
s=importlib.util.spec_from_file_location('m',ROOT/'docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
pat=str(P/'cells/%04d.png');cal=1.5;off=(-12,-5);pts,tracked=m.track(pat,9,cal,off)
base=tracked[0];rows=[]
x0,y0,x1,y1=[round(v*cal+off[i%2]) for i,v in enumerate(m.FACE_BOX)]
T=m.gray(pat%0)[y0:y1,x0:x1].astype(np.float32)
for i in range(9):
 found=tracked[i];ks=[k for k in base if k in found];a=np.float32([base[k] for k in ks]);b=np.float32([found[k] for k in ks]);M,inliers=cv2.estimateAffinePartial2D(a,b,method=cv2.LMEDS);fig=float(np.hypot(M[0,0],M[1,0]));I=m.gray(pat%i).astype(np.float32);best=None
 for dx in [-8,0,8]:
  for dy in [-8,0,8]:
   W=np.array([[fig,0,x0+M[0,2]+dx],[0,fig,y0+M[1,2]+dy]],np.float32)
   try:
    cc,W=cv2.findTransformECC(T,I,W,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,500,1e-6),None,5)
    head=float(np.sqrt(abs(np.linalg.det(W[:,:2]))))
    if 0.8<head<1.2 and (best is None or cc>best['cc']): best={'cc':float(cc),'head_scale':head}
   except cv2.error: pass
 rows.append({'index':i,'figure_scale':fig,'similarity_to_source0':M.tolist(),'tracked_features':len(found),'head':best})
print(json.dumps(rows,indent=1))
(P/'registration_analysis.json').write_text(json.dumps({'status':'DIAGNOSTIC_ONLY_NOT_ACCEPTANCE','calibration':{'scale':cal,'offset':off},'frames':rows},indent=2)+'\n')
