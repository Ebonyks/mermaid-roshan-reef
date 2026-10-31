from pathlib import Path
from PIL import Image
import numpy as np,cv2,sys,shutil
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import ltx_wave_experiment as runner
source=root/'assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01/full_wave_draft_01'
folder=root/'assets_src/animation/roshan_wave_repair_20261010/aseprite_matte_trial_01/full_wave_matte_01';folder.mkdir(exist_ok=False);(folder/'sources').mkdir()
rows=[];unusual=[]
for n in range(41):
 p=source/f'{n:04d}.png';dest=folder/'sources'/p.name;shutil.copyfile(p,dest)
 a=np.array(Image.open(p).convert('RGB'));eligible=((a.max(2)-a.min(2)<=10)&(a.min(2)>=205)).astype('uint8')
 count,labels,stats,centroids=cv2.connectedComponentsWithStats(eligible,connectivity=4)
 outside=set(labels[0])|set(labels[-1])|set(labels[:,0])|set(labels[:,-1]);candidates=[]
 for i,(x,y,w,h,area) in enumerate(stats):
  if i not in outside and 405<=x<=505 and 180<=y<=265 and 20<=area<=600 and w<=70 and h<=60:
   candidates.append((i,int(x),int(y),int(w),int(h),int(area)))
  if i!=0 and i not in outside and x<215 and y<390 and area>=20:unusual.append({'frame':n,'bbox':[int(x),int(y),int(w),int(h)],'area':int(area)})
 if len(candidates)!=1:raise ValueError(f'Hair-gap component not unique at{n}: {candidates}')
 i,x,y,w,h,area=candidates[0];mask=(labels==i).astype('uint8');distance=cv2.distanceTransform(mask,cv2.DIST_L2,3);yy,xx=np.unravel_index(np.argmax(distance),distance.shape)
 rows.append({'index':n,'source_path':runner.relative(root,p),'source_sha256':runner.sha(p),'preserved_source_path':runner.relative(root,dest),'preserved_source_sha256':runner.sha(dest),'source_size':list(Image.open(p).size),'hair_gap_component':{'label':i,'bbox':[x,y,w,h],'area':area,'seed':[int(xx),int(yy)],'criterion':'Unique enclosed neutral component in the inspected pink/rainbow hair-loop region; NOT a whole-image neutral erase','review_status':'PENDING_CONTACT_SHEET_MODEL_REVIEW'}})
runner.write_json(folder/'source_and_seed_plan.json',{'schema':'reef.whole-cel-matte-source-seed-plan.v1','sources':rows,'unusual_other_closed_neutral_components':unusual,'note':'Seeds derived by read-only component measurement; must visually inspect all41source hair-gap crops before applying. ApprovedK0 shows the corresponding hair-loop gap transparent. Pale closed highlights remain protected.'})
print({'frames':len(rows),'hair_component_area_range':[min(r['hair_gap_component']['area'] for r in rows),max(r['hair_gap_component']['area'] for r in rows)],'seed_ranges':[[min(r['hair_gap_component']['seed'][j] for r in rows),max(r['hair_gap_component']['seed'][j] for r in rows)] for j in range(2)],'unusual':unusual})
