"""Behavior checks for continuity gating and lossless Aseprite frame exports."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import json,subprocess,tempfile
import numpy as np
from PIL import Image
from verify_registered_guides import check,evaluate
from scale_geometry import fit
from measure_scale_landmarks import landmarks,digest
P=Path(__file__).resolve().parents[1]
ASE=r'C:\Program Files\Aseprite\Aseprite.exe'
checks=[]
source=check(write=False);checks.append('Eight actual Aseprite guide exports meet declared geometry limits')
target=source['rows'][0]['target_landmarks'];root=np.array(target['bodice_waist_tip'])
zoom={n:(root+1.1*(np.array(v)-root)).tolist() for n,v in target.items()}
assert not evaluate(zoom,target)['pass'];checks.append('Ten percent uncorrected global zoom rejected')
shift={n:(np.array(v)+[12,0]).tolist() for n,v in target.items()}
assert not evaluate(shift,target)['pass'];checks.append('Uncorrected whole-figure root translation rejected')
stretch={n:list(v) for n,v in target.items()};stretch['neck_base'][1]-=30
assert not fit(stretch,target)['pass'];checks.append('Internal torso stretch cannot pass a whole-figure uniform fit')
old=json.loads((P/'scale_continuity/registration_plan.json').read_text())['guides'][4]
assert not old['pass'];checks.append('Original independently generated key22 fails multi-anchor source gate')
decoded=json.loads((P/'scale_continuity/decoded_registration_plan.json').read_text())
final=[]
for row in decoded['frames']:
 f=P/f"scale_continuity/decoded_filtered/{row['index']:04d}.png";v={'index':row['index'],'sha256':digest(f),'source_fit_pass':row['pass']}
 if row['pass']:
  a,h=landmarks(f);v.update(evaluate(a,row['target_landmarks']))
 else:
  assert np.array_equal(np.array(Image.open(f).convert("RGBA")),np.array(Image.open(P/row['source']).convert("RGBA"))),'Rejected frame was concealed/changed'
  v.update({'pass':False,'status':'REDRAW_REQUIRED; original native pixels retained'})
 final.append(v)
checks.append('Every rejected decoded frame retains exact native RGB pixels; Aseprite adds opaque alpha only')
with tempfile.TemporaryDirectory(prefix='roshan-scale-roundtrip-') as tmp:
 for master,folder,count in [('registered_guides.aseprite','registered_guides',8),('decoded_filtered_review.aseprite','decoded_filtered',41)]:
  dest=Path(tmp)/folder;dest.mkdir()
  subprocess.run([ASE,'-b','--script-param','master='+str(P/'scale_continuity'/master),'--script-param','output='+str(dest),'--script',str(P/'scripts/export_roundtrip.lua')],check=True,timeout=120)
  for i in range(count):
   src=P/'scale_continuity'/folder/(f"guide_{source['rows'][i]['index']:04d}.png" if count==8 else f'{i:04d}.png')
   out=dest/f'{i:04d}.png'
   assert np.array_equal(np.array(Image.open(src).convert("RGBA")),np.array(Image.open(out).convert("RGBA"))),('Aseprite roundtrip differs',master,i)
checks.append('Registered guides and all41 filtered frames reopen/export pixel-exact')
report={'status':'MACHINE_FILTER_PASS','checks':checks,'decoded_frames':final,'decoded_geometry_pass_indices':[r['index'] for r in final if r['pass']],'redraw_required_indices':[r['index'] for r in final if not r['pass']],'accepted':False,'quality_status':'Human native identity/blur/motion/seam review remains separate'}
(P/'scale_continuity/filter_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('FILTER_CHECKS_PASS',len(checks),'DECODED_GEOMETRY_PASSES',len(report['decoded_geometry_pass_indices']),'REDRAW_REQUIRED',report['redraw_required_indices'])
