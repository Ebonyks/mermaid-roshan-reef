"""Read-only landmark fit; write an Aseprite whole-image registration plan."""
from pathlib import Path
import importlib.util,json,cv2,numpy as np
ROOT=Path.cwd();P=ROOT/'assets_src/animation/roshan_wave_repair_20261010'
spec=importlib.util.spec_from_file_location('m',ROOT/'docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
family=P/'painted_family_02';pat=str(family/'cells/%04d.png');cal=314/256;off=(-25,-5)
pts,tracked=m.track(pat,16,cal,off);base=tracked[0]
transforms={}
for index,found in enumerate(tracked):
 keys=[key for key in base if key in found]
 A=np.float32([base[k] for k in keys]);B=np.float32([found[k] for k in keys]);M,_=cv2.estimateAffinePartial2D(A,B,method=cv2.LMEDS)
 scale=float(np.hypot(M[0,0],M[1,0]));factor=1/(scale*cal)
 width=round(314*factor);factor=width/314
 # Register the whole drawing at the tracked waist, preserving authored tilt.
 waist=found['waist'];target=np.array([135.5,143.0])
 translation=target-factor*np.array(waist)
 transforms[index]={'width':width,'x':round(float(translation[0])),'y':round(float(translation[1])),'diagnostic_figure_scale':scale,'source_waist':[float(v) for v in waist]}
mapping=['K0']*3+[1]*3+[2]*2+[3]*2+[4]*2+[5]*2+[6]*3+[5]*2+[6]*3+[5]*2+[4]*2+[3]*2+[2]*2+[1]*3+['K0']*8
assert len(mapping)==41
frames=[]
for i,key in enumerate(mapping):
 tick=lambda n:(n*1000+12)//24
 if key=='K0':row={'path':str(ROOT/'assets_src/animation/whole_sprite_pipeline_20261007/references/approved_K0.png'),'width':256,'x':0,'y':0,'exact':True}
 else:row={'path':str(family/f'cells/{key:04}.png'),'exact':False,**transforms[key]}
 row.update(index=i,key=key,duration_ms=tick(i+1)-tick(i));frames.append(row)
plan={'schema':'reef.whole-cel-assembly.v1','status':'DRAFT_UNREVIEWED','canvas':[256,256],'fps':24,'alpha_floor':16,'output':str(family/'draft_01'),'source_calibration':{'scale':cal,'offset':off},'method':'One bilinear uniform scale and integer translation per entire drawing; alpha<=16 cleared; no part edits; authored holds/return keys','frames':frames}
(family/'draft_01').mkdir(exist_ok=True)
(family/'draft_01/plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print('PLAN',len(frames),'frames',sum(r['duration_ms'] for r in frames),'ms')
