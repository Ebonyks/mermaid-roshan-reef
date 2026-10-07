from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import json,numpy as np,math
p=Path('assets_src/cinematics/ltx25_8gb_wave_20261004');m=json.loads((p/'scale_continuity/native_landmarks.json').read_text());keys=[0,3,7,17,22,27,36,40];raw={x['index']:x for x in m['guides']};names=list(raw[0]['landmarks']);root=np.array(raw[0]['landmarks']['bodice_waist_tip']);targets={}
for i in keys:
 if i==22:continue
 shift=root-np.array(raw[i]['landmarks']['bodice_waist_tip']);targets[i]={n:(np.array(raw[i]['landmarks'][n])+shift).tolist() for n in names}
targets[22]={n:((np.array(targets[17][n])+targets[27][n])/2).tolist() for n in names}
from scale_geometry import fit
records=[]
for i in keys:
 row=raw[i];record={'index':i,'source':row['source'].replace('\\','/'),'source_sha256':row['source_sha256'],'source_landmarks':row['landmarks'],'target_landmarks':targets[i],**fit(row['landmarks'],targets[i])};records.append(record)
plan={'status':'REJECTED_KEY_REQUIRES_COMPLETE_FIGURE_REDRAW','anchor_names':names,'canvas':[576,832],'root_target':root.tolist(),'target_method':'Pose-specific common-scale atlas-derived reference landmarks; all waist tips registered to the rest root. Mid-lowering anchors interpolate coordinates of neighboring poses only, no appearance pixel interpolation. Human anchor review remains required.','tolerances':{'maximum_anchor_residual_px':6,'pair_scale_ratio_deviation':.03,'status':'Provisional diagnostic thresholds; do not grant owner/visual acceptance'},'guides':records,'base_frames':[],'no_limb_warp_or_pixels_blended':True,'image_generation_calls':0,'model_generation_calls':0}
for frame in m['output_frames'][0]['frames']:
 i=frame['index'];a=max(k for k in keys if k<=i);b=min(k for k in keys if k>=i);f=0 if a==b else (i-a)/(b-a);target={n:((1-f)*np.array(targets[a][n])+f*np.array(targets[b][n])).tolist() for n in names}
 if 'landmarks' in frame:plan['base_frames'].append({'index':i,'source':f'results/base_two_pass/refined_frames/{i:04d}.png','source_sha256':frame['sha256'],'source_landmarks':frame['landmarks'],'target_landmarks':target,**fit(frame['landmarks'],target)})
 else:plan['base_frames'].append({'index':i,'pass':False,'status':'MANUAL_ANCHORS_REQUIRED'})
(p/'scale_continuity/registration_plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print('Multi-anchor preflight: rejected keys',[x['index'] for x in records if not x['pass']]);print('Key22 five-anchor residual',round(records[4]['max_anchor_residual_px'],2),'px; torso scale ratio',round(records[4]['pair_scale_ratios']['neck_base__bodice_waist_tip'],3));print('Base output requiring redraw after uniform-fit diagnostic:',[x['index'] for x in plan['base_frames'] if not x['pass']])
