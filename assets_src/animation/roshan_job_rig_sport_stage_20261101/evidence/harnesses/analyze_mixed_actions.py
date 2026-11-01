from pathlib import Path
import json,hashlib,importlib.util,shutil
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];out=R/'evidence/verification_v3';folder=out/'mixed_actions_raw';samples=json.loads((folder/'samples.json').read_text());spec=importlib.util.spec_from_file_location('geometry_audit',R/'tools/audit_study.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);rows=[];keys=R/'review/frozen_v3/mixed_failures';keys.mkdir(exist_ok=True);kept=0
for sample in samples:
 a=np.asarray(Image.open(folder/sample['avatar_image']).convert('RGBA'));rest=Image.open(folder/sample['rest_image']).convert('RGBA');pix=g.pixel_checks(Image.fromarray(a));ref=g.pixel_checks(rest);joint={}
 for name in ['LeftUpper','LeftFore','LeftHand','RightUpper','RightFore','RightHand']:
  x,y=np.round(sample['bones'][name][4:6]).astype(int);joint[name]=int(a[y-1:y+2,x-1:x+2,3].min())
 waist=int(np.sum((a[462:490,480:620,3]>192).sum(axis=1)==0));contact=max(sample.get('contact_error',0),sample.get('painted_wrist_error',0),sample.get('knuckle_mitt_error',0));fixed=sample['fixture_error'];ok=g.seam_pass(pix,ref) and min(joint.values())>192 and waist==0 and contact<=3 and fixed<=3
 row={'parts':sample['parts'],'action':sample['action'],'time':sample['time'],'contact_error_max':contact,'fixture_error':fixed,'joint_min_alpha':joint,'waist_empty_rows':waist,'pixels':pix,'rest_pixels':ref,'pass':ok,'source_image':sample['image'],'avatar_image':sample['avatar_image'],'source_sha256':hashlib.sha256((folder/sample['image']).read_bytes()).hexdigest()}
 if sample['parts']['body']==sample['action'] and sample['parts']['tail']==sample['action']:
  fresh=np.asarray(Image.open(out/'action_repeatability_raw'/f"{sample['action']}_0096.png").convert('RGBA'));live=np.asarray(Image.open(folder/sample['image']).convert('RGBA'));row['fresh_fullset_changed_pixels']=int(np.any(fresh!=live,axis=2).sum())
 if not ok and kept<12:
  for field in ['rest_image','image','avatar_image']:shutil.copy2(folder/sample[field],keys/sample[field])
  row['review_copy']='review/frozen_v3/mixed_failures/'+sample['image'];kept+=1
 rows.append(row)
report={'scope':'108 actual object-contact poses: each action with its matching head and all36 current body/tail pairs. Character-only diagnostic renders hide fixed mitt/wheel/mic/axle, retaining worn glove and painted grips. Full scene also captured. Inherited seam and alpha floors preserved; this is not all-view or full-time mixed-action coverage.','rows':rows,'cases':len(rows),'contact_pass_count':sum(x['contact_error_max']<=3 and x['fixture_error']<=3 for x in rows),'outline_attachment_pass_count':sum(x['pass'] for x in rows),'fullset_fresh_comparisons':[{'action':x['action'],'changed_pixels':x['fresh_fullset_changed_pixels']} for x in rows if 'fresh_fullset_changed_pixels' in x],'pass':all(x['pass'] for x in rows)};(out/'mixed_action_audit.json').write_text(json.dumps(report,indent=2)+'\n');(out/'mixed_action_samples.json').write_text(json.dumps(samples,indent=2)+'\n');print('MIXED_OBJECT_CONTACT',len(rows),report['contact_pass_count'],'contact pass;',report['outline_attachment_pass_count'],'outline/attachment pass');raise SystemExit(0 if report['pass'] else 1)
