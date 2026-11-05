from pathlib import Path
import json,sys,hashlib,importlib.util
import numpy as np
from PIL import Image
from scipy import ndimage
R=Path(__file__).resolve().parents[2];folder=Path(sys.argv[1]).resolve();out=R/'evidence/verification_v3';spec=importlib.util.spec_from_file_location('motion',R/'tools/audit_motion.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);samples=json.loads((folder/'samples.json').read_text());reports={}
def array(p):return np.asarray(Image.open(p).convert('RGBA'))
def alpha_at(a,p):
 x,y=np.round(p).astype(int);return int(a[max(0,y-1):y+2,max(0,x-1):x+2,3].min())
for clip in ['boxer','racer','popstar']:
 rows=[x for x in samples if x['action']==clip];d=m.motion_metrics(rows);d['frames']=len(rows);d['views']=sorted(set(x['view'] for x in rows));d['contact_frames']=sum(x['contact_active'] for x in rows)
 for key in ['contact_error','fixture_error','painted_wrist_error','knuckle_mitt_error']:d['max_'+key]=max(x.get(key,0) for x in rows)
 d['joint_min_alpha']={n:255 for n in ['LeftUpper','LeftFore','LeftHand','RightUpper','RightFore','RightHand']};d['mid_forearm_min_alpha']={'Left':255,'Right':255};d['max_bone_scale_error']=0
 for row in rows:
  a=array(folder/row['image'])
  for n in d['joint_min_alpha']:d['joint_min_alpha'][n]=min(d['joint_min_alpha'][n],alpha_at(a,row['bones'][n][4:6]))
  for side in ['Left','Right']:
   p=(np.array(row['bones'][side+'Fore'][4:6])+np.array(row['bones'][side+'Hand'][4:6]))/2;d['mid_forearm_min_alpha'][side]=min(d['mid_forearm_min_alpha'][side],alpha_at(a,p))
  for v in row['bones'].values():d['max_bone_scale_error']=max(d['max_bone_scale_error'],float(np.abs(np.linalg.svd(np.array([[v[0],v[2]],[v[1],v[3]]]),compute_uv=False)-1).max()))
 first=array(folder/rows[0]['image']);last=array(folder/rows[-1]['image']);d['endpoint_changed_pixels']=int(np.any(first!=last,axis=2).sum());d['endpoint_matrix_error']=max(abs(a-b) for n in rows[0]['bones'] for a,b in zip(rows[0]['bones'][n],rows[-1]['bones'][n]))
 d['pass']=d['max_angular_speed_deg_s']<140 and d['max_angular_acceleration_deg_s2']<650 and d['max_bone_scale_error']<1e-5 and d['max_contact_error']<=3 and d['max_fixture_error']<=3 and d['max_painted_wrist_error']<=3 and d['max_knuckle_mitt_error']<=3 and d['endpoint_changed_pixels']==0 and d['endpoint_matrix_error']<1e-5 and min(d['joint_min_alpha'].values())>192 and min(d['mid_forearm_min_alpha'].values())>192 and (clip!='boxer' or d['views']==['guard','jab','palm'])
 reports[clip]=d
report={'source_folder':str(folder.relative_to(R)),'input_frozen':'sport-stage-source-v3','actions':reports,'thresholds':{'angular_speed_deg_s':140,'angular_acceleration_deg_s2':650,'uniform_scale_error':1e-5,'contact_wrist_fixture_pixels':3,'joint_and_midarm_alpha':192,'loop_pixels':0},'pass':all(x['pass'] for x in reports.values()),'scope':'Actual image/transform/fixture sampling; does not certify naturalness, semantic grip/perspective, paint finish or human/device/child acceptance.'};(out/'object_action_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(0 if report['pass'] else 1)
