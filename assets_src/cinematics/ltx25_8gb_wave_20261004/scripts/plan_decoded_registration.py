"""Read native decoded frames; plan Aseprite whole-frame edits and reject spans."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import json,numpy as np
from measure_scale_landmarks import landmarks,digest
from scale_geometry import fit
from verify_registered_guides import evaluate
P=Path(__file__).resolve().parents[1]
source=json.loads((P/'scale_continuity/registration_plan.json').read_text())
keys={r['index']:r['target_landmarks'] for r in source['guides']};indices=sorted(keys)
rows=[]
for i in range(41):
 a=max(k for k in indices if k<=i);b=min(k for k in indices if k>=i);u=0 if a==b else (i-a)/(b-a)
 target={n:((1-u)*np.array(keys[a][n])+u*np.array(keys[b][n])).tolist() for n in keys[a]}
 f=P/f'results/scale_registered/refined_frames/{i:04d}.png'
 row={'index':i,'source':f.relative_to(P).as_posix(),'source_sha256':digest(f),'target_landmarks':target}
 try:
  measured,h=landmarks(f);v=fit(measured,target)
  row.update(source_landmarks=measured,native_check=evaluate(measured,target),**v)
  row['status']='UNIFORM_REGISTRATION_CANDIDATE' if v['pass'] else 'REDRAW_REQUIRED_PROPORTIONS'
 except ValueError as error:row.update({'status':'MANUAL_ANCHORS_REQUIRED','pass':False,'reason':str(error)})
 rows.append(row)
report={'status':'SOURCE_ONLY','canvas':[576,832],'fps':24,'frames':rows,'raw_native_pass_indices':[r['index'] for r in rows if r.get('native_check',{}).get('pass')],'proportion_fit_pass_indices':[r['index'] for r in rows if r['pass']],'rejected_indices':[r['index'] for r in rows if not r['pass']],'failed_frames_retained':True,'edit_scope':'Only complete-canvas uniform resize/translation for passing proportion fits; failed frames retained unchanged and tagged. No limb warp, no frame holds or interpolation.','accepted':False}
(P/'scale_continuity/decoded_registration_plan.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('NATIVE_ANCHOR_PASSES',len(report['raw_native_pass_indices']),'REGISTERABLE',len(report['proportion_fit_pass_indices']),'REJECTED',report['rejected_indices'],flush=True)
