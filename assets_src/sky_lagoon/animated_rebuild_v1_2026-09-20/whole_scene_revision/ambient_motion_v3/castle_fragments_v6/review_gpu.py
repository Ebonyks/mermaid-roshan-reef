from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
p=Path('tmp/sky-lagoon-whole-scene-v2/castle-layer-ownership-audit');g=p.parent/'whole-lawn-four-region-v2/gpu';rows=[];tiles=[]
for mode,label in [('day','canvas_screen_3_day_p0'),('night','canvas_screen_3_night_p2')]:
 for ident in ['castle_left_verge','castle_right_verge']:
  hidden=g/f'{label}_{ident}_hidden.png'
  if not hidden.exists():raise SystemExit('WAIT: queued GPU evidence not yet available; no verdict.')
  h=np.asarray(Image.open(hidden).convert('RGB')).astype(int);frames=[np.asarray(Image.open(g/f'{label}_{ident}_frame{k}.png').convert('RGB')).astype(int) for k in range(4)];visible=np.logical_or.reduce([(abs(a-h).max(2)>2) for a in frames]);moving=np.logical_or.reduce([(abs(a-frames[0]).max(2)>2) for a in frames]);ys,xs=np.where(visible|moving);box=None
  if len(xs):
   box=[max(0,int(xs.min())-15),max(0,int(ys.min())-15),min(h.shape[1],int(xs.max())+16),min(h.shape[0],int(ys.max())+16)]
   tile=Image.new('RGB',(1000,190),'#20343e');d=ImageDraw.Draw(tile);d.text((8,6),mode+' / '+ident,fill='white')
   for j,a in enumerate([h]+frames):
    im=Image.fromarray(a.astype('uint8')).crop(box);im.thumbnail((190,150));tile.paste(im,(j*200,30));d.text((j*200+4,175),'Hidden' if j==0 else f'Cel {j}',fill='white')
   tiles.append(tile)
  rows.append({'mode':mode,'id':ident,'visible_contribution_pixels_over_2_codes':int(visible.sum()),'moving_pixels_over_2_codes':int(moving.sum()),'visible_bbox_xyxy':box,'interpretation':'Actual rendered contribution only; source-space audit establishes that this legacy grass owner includes leaf/rock fragments.'})
if tiles:
 board=Image.new('RGB',(1000,190*len(tiles)),'#20343e')
 for i,t in enumerate(tiles):board.paste(t,(0,i*190))
 board.save(p/'runtime-contribution.jpg',quality=96)
report={'status':'RENDERED_VISIBILITY_MEASURED','checks':rows,'decision':'Review visual fragments before changing runtime ownership. Whole-plant animation remains separately owned.'};(p/'GPU_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
