from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image
from scipy import ndimage
R=Path(__file__).resolve().parents[1];folder=Path(sys.argv[1]) if len(sys.argv)>1 else R/'evidence/mixed_raw';records=json.loads((folder/'samples.json').read_text())
def pixels(a,cut):
 mask=a[:,:,3]>cut;labels,n=ndimage.label(mask);counts=np.bincount(labels.ravel());counts[0]=0;filled=ndimage.binary_fill_holes(mask);holes=filled&~mask;labs,n=ndimage.label(holes);hc=np.bincount(labs.ravel());hc[0]=0
 return {'components':int((counts>12).sum()),'max_hole':int(hc.max(initial=0)),'hole_pixels':int(holes.sum()),'hole_components':int((hc>12).sum()),'edge_alpha':int(np.count_nonzero(a[0,:,3])+np.count_nonzero(a[-1,:,3])+np.count_nonzero(a[:,0,3])+np.count_nonzero(a[:,-1,3]))}
references={};rows=[]
for rec in records:
 a=np.asarray(Image.open(folder/rec['image']).convert('RGBA'));p=pixels(a,96);strict=pixels(a,192);key=tuple(rec['parts'][k] for k in ['head','body','tail'])
 if rec['time']==0:references[key]=p
 ref=references[key];contacts={}
 for name in ['LeftUpper','LeftFore','LeftHand']:
  x,y=np.round(rec['bones'][name][4:6]).astype(int);contacts[name]=int(a[y-1:y+2,x-1:x+2,3].min())
 waist=a[462:490,480:620,3];waist_empty_rows=int(np.sum((waist>192).sum(axis=1)==0))
 ok=p['components']==1 and p['edge_alpha']==0 and p['max_hole']<=ref['max_hole']+8 and p['hole_pixels']<=ref['hole_pixels']+8 and p['hole_components']<=ref['hole_components'] and min(contacts.values())>192 and waist_empty_rows==0
 rows.append({**{k:rec[k] for k in ['parts','image','clip','time','fresh_equal']},'pixel_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'png_sha256':hashlib.sha256((folder/rec['image']).read_bytes()).hexdigest(),'pixels':p,'strict_alpha192':strict,'left_joint_min_alpha':contacts,'waist_empty_rows':waist_empty_rows,'outline_contact_pass':ok})
failed=[x for x in rows if not x['outline_contact_pass']];summary={'snapshots':len(rows),'combinations':len(references),'pass_count':len(rows)-len(failed),'fail_count':len(failed),'pass':not failed,'thresholds':{'significant_component_pixels':12,'inherited_alpha96_and_strict_alpha192':True,'raster_hole_allowance_pixels':8,'joint_alpha':192,'waist_empty_rows':0},'rows':rows,'scope':'Actual per-mix rendered outline/component/hole/joint/waist checks; fresh-state equality never supplies this result. Common-waist contract remains independently required.'}
(R/'evidence/mixed_outline_audit.json').write_text(json.dumps(summary,indent=2)+'\n');(R/'evidence/mixed_failure_index.json').write_text(json.dumps({'failures':failed,'status':'COMPATIBILITY_BLOCKED' if failed else 'MACHINE_FIT_ONLY_VISUAL_PENDING'},indent=2)+'\n');print('MIX_OUTLINES',len(rows)-len(failed),'PASS',len(failed),'FAIL')
raise SystemExit(0 if not failed else 1)
