from pathlib import Path
import json,numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];out=R/'evidence/verification_v3';folder=out/'controls';data=json.loads((folder/'controls.json').read_text());rows=[]
for row in data['rows']:
 c=row['control'];rec=row['record'];diff=row['changed_pixels'];result=None;reason=''
 if c=='none':result=True;reason='normal reference, fault detection not applicable'
 elif c=='grip_slip':result=rec['contact_error']>3 and diff>0;reason='actual grip error plus rendered change'
 elif c=='fixture_drift':result=rec['fixture_error']>3 and diff>0;reason='actual support-node transform plus rendered change'
 elif c=='original_underlay':result=diff>0 and rec.get('underlay_visible',False);reason='actual original texture/material reinsertion and rendered change'
 elif c=='identity_scale':
  v=rec['bones']['Head'];error=float(np.abs(np.linalg.svd([[v[0],v[2]],[v[1],v[3]]],compute_uv=False)-1).max());result=error>=1e-5 and diff>0;reason='actual Head transform and rendered change'
 elif c=='missing_arm':
  a=np.asarray(Image.open(folder/row['image']).convert('RGBA'));p=np.round((np.array(rec['bones']['RightFore'][4:6])+np.array(rec['bones']['RightHand'][4:6]))/2).astype(int);value=int(a[p[1]-1:p[1]+2,p[0]-1:p[0]+2,3].min());result=value<=192 and diff>0;reason='actual mid-forearm occupancy='+str(value)+' plus rendered change'
 elif c=='frozen_view':
  if row['clip']=='boxer':result=diff>0;reason='frozen guard surface differs from expected authored jab surface at contact; semantic human review remains separate'
  else:result=None;reason='not applicable: no authored boxer glove views in this action; unchanged image is expected'
 rows.append({'clip':row['clip'],'control':c,'detected':result,'reason':reason,'changed_pixels':diff,'image':row['image']})
poison=data['source_poison_rows'];report={'rows':rows,'surveyed_old_clothing_pixels':data['surveyed_old_clothing_pixels'],'undeleted_old_clothing_pixels':data['undeleted_old_clothing_pixels'],'source_poison_cases':len(poison),'max_source_poison_leak_pixels':max(x['source_leak_pixels'] for x in poison),'pass':all(x['detected'] is not False for x in rows) and data['surveyed_old_clothing_pixels']>0 and data['undeleted_old_clothing_pixels']==0 and not any(x['source_leak_pixels'] for x in poison),'scope':'Retained actual image faults; no fictional view control result for racer/popstar. Numerical detection never accepts naturalness.'};(out/'controls_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(0 if report['pass'] else 1)
