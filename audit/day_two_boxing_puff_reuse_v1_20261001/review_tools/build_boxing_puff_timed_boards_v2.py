from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
r=Path.cwd();f=r/'audit/day_two_boxing_puff_reuse_v1_20261001/native_timed_reuse_v2';d=json.loads((f/'CAPTURE_RECEIPT.json').read_text());out=f/'inspection_boards';assert not out.exists();out.mkdir();boards=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for ai,a in enumerate(d['actions']):
 frames=d['frames'][a['first_frame']:a['last_frame']+1]
 for batch in range(0,len(frames),9):
  rows=frames[batch:batch+9];board=Image.new('RGB',(1440,885),(236,242,250));draw=ImageDraw.Draw(board);draw.text((12,8),f"Unbound exact clean-puff reuse · {a['width']} {a['mode']} · complete native frames, no motion synthesis",font=font,fill=(32,42,65))
  for i,x in enumerate(rows):
   im=Image.open(f/x['path']).convert('RGB');im.thumbnail((472,266),Image.Resampling.LANCZOS);px=(i%3)*480;py=35+(i//3)*282;board.paste(im,(px,py+22));draw.text((px+3,py),f"#{x['index']} t={x['seconds']:.3f}s hit={x['landed_punches']} puff={x['impact_time']:.3f}",font=font,fill=(32,42,65))
  name=f'action_{ai:02d}_board_{batch//9:02d}.webp';board.save(out/name,format='WEBP',lossless=True);boards.append({'path':'inspection_boards/'+name,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest(),'action':ai,'frame_indices':[x['index'] for x in rows],'role':'Full-canvas ordered visual inspection board; uniform whole-frame display thumbnails with labels, never runtime pixels'})
(out/'MANIFEST.json').write_text(json.dumps({'status':'ORDERED_FULL_CANVAS_INSPECTION_BOARDS','boards':boards},indent=2)+'\n',encoding='utf-8');print('BOXING_NATIVE_FRAMES',len(d['frames']),'BOARDS',len(boards));print(json.dumps(d['actions'],indent=2));
for i,a in enumerate(d['actions']):
 frames=d['frames'][a['first_frame']:a['last_frame']+1];first_hit=next(x for x in frames if x['landed_punches']>0);peak=max(frames,key=lambda x:x['impact_time']);print('ACTION_DIRECT_NATIVE_INDICES',i,a['first_frame'],first_hit['index'],peak['index'],a['last_frame'])
