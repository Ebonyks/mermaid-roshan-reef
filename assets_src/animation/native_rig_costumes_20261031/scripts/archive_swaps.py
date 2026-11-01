from pathlib import Path
import json,subprocess,hashlib,os
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];FF='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
for folder in sorted((ROOT/'evidence').glob('swaps_v*')):
 frames=sorted(folder.glob('*.png'));archive=folder/'snapshot_rgba.mkv'
 if not frames:continue
 seq=folder/'sequence';seq.mkdir(exist_ok=True)
 for i,source in enumerate(frames):
  target=seq/f'{i:04d}.png'
  if not target.exists():os.link(source,target)
 if not archive.exists():subprocess.run([FF,'-y','-v','error','-framerate','25','-i',str(seq/'%04d.png'),'-filter_complex','[0:v]split=2[c][a];[c]format=rgb24[color];[a]alphaextract[alpha]','-map','[color]','-map','[alpha]','-c:v:0','libx264rgb','-crf:v:0','0','-preset:v:0','veryfast','-c:v:1','ffv1','-level:v:1','3','-pix_fmt:v:1','gray',str(archive)],check=True)
 result=subprocess.run([FF,'-v','error','-i',str(archive),'-filter_complex','[0:v:0][0:v:1]alphamerge[out]','-map','[out]','-pix_fmt','rgba','-f','framemd5','-'],capture_output=True,text=True,check=True);decoded=[l.split(',')[-1].strip() for l in result.stdout.splitlines() if l.strip() and not l.startswith('#')];native=[{'file':p.name,'png_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rgba_md5':hashlib.md5(Image.open(p).convert('RGBA').tobytes()).hexdigest()} for p in frames];exact=len(decoded)==len(native) and all(a==b['rgba_md5'] for a,b in zip(decoded,native))
 (folder/'snapshot_archive.json').write_text(json.dumps({'pass':exact,'decoded_frames':len(decoded),'expected_frames':len(frames),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'snapshots':native,'scope':'Lossless RGB+alpha snapshots in lexicographic source filename order; not an animation cadence claim.'},indent=2)+'\n',encoding='utf-8')
 assert exact
 if folder.name=='swaps_v3':
  for start in range(0,len(frames),12):
   board=Image.new('RGB',(1440,1110),(225,233,243));draw=ImageDraw.Draw(board)
   for j,p in enumerate(frames[start:start+12]):
    tile=Image.new('RGBA',(1024,1024),(245,245,245,255));tile.alpha_composite(Image.open(p));tile=tile.convert('RGB').resize((350,330));x=(j%4)*360;y=(j//4)*370;board.paste(tile,(x,y));draw.text((x+5,y+335),p.stem.replace('_v1',''),fill=(30,40,60))
   board.save(ROOT/'review'/f'swap_combinations_{start//12+1:02}.jpg',quality=95)
 print('SWAP_ARCHIVE_OK',folder.name,len(frames),flush=True)
