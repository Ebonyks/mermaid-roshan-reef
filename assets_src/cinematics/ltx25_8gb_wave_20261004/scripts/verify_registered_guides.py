"""Read-only geometry gate on Aseprite exports. No Python image edits."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from measure_scale_landmarks import landmarks,digest
P=Path(__file__).resolve().parents[1]
PAIRS=[('image_left_eye','image_right_eye'),('crown_gem','image_left_eye'),('crown_gem','image_right_eye'),('crown_gem','bodice_waist_tip'),('neck_base','bodice_waist_tip')]
def evaluate(measured,target,root_tolerance=1):
 errors={n:float(np.linalg.norm(np.array(measured[n])-target[n])) for n in target}
 ratios={a+'__'+b:float(np.linalg.norm(np.array(measured[a])-measured[b])/np.linalg.norm(np.array(target[a])-target[b])) for a,b in PAIRS}
 ok=max(errors.values())<=6 and errors['bodice_waist_tip']<=root_tolerance and all(abs(v-1)<=.03 for v in ratios.values())
 return {'native_residuals_px':errors,'native_pair_ratios':ratios,'pass':bool(ok)}
def check(write=True):
 plan=json.loads((P/'scale_continuity/registration_plan.json').read_text());rows=[]
 for row in plan['guides']:
  f=P/f"scale_continuity/registered_guides/guide_{row['index']:04d}.png"
  with Image.open(f) as im:assert im.size==(576,832),('Unexpected canvas',f)
  a,h=landmarks(f);v=evaluate(a,row['target_landmarks'])
  rows.append({'index':row['index'],'path':str(f.relative_to(P)).replace('\\','/'),'sha256':digest(f),'landmarks':a,'target_landmarks':row['target_landmarks'],**v})
  print('REGISTERED',row['index'],'max_error',round(max(v['native_residuals_px'].values()),3),'root_error',round(v['native_residuals_px']['bodice_waist_tip'],3),'pass',v['pass'],flush=True)
 report={'status':'SOURCE_GEOMETRY_PASS' if all(x['pass'] for x in rows) else 'SOURCE_GEOMETRY_FAIL','tolerances':{'max_native_anchor_error_px':6,'root_error_px':1,'pair_ratio_deviation':.03},'rows':rows,'accepted':False,'human_identity_review':'Pending owner; assistant inspection sees complete figure, matching costume/tiara/tail, no isolated limb replacement.'}
 if write:(P/'scale_continuity/registered_preflight.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 else:
  sealed=json.loads((P/'scale_continuity/registered_preflight.json').read_text())
  assert sealed['status']=='SOURCE_GEOMETRY_PASS','Recorded source preflight failed'
  for actual,expected in zip(rows,sealed['rows'],strict=True):
   assert all(actual[field]==expected[field] for field in ['index','path','sha256','target_landmarks']),('Source/contract changed after preflight',actual['index'])
 assert report['status']=='SOURCE_GEOMETRY_PASS','No model submission permitted: guide geometry fails'
 return report
if __name__=='__main__':check()
