"""Owner-authorized Grand Puff video-to-Aseprite pixel transfer, 2026-09-15.
No generated poses, interpolation, affine acting, or claim of hand drawing.
Build needs FFmpeg, Pillow, numpy/scipy and Aseprite 1.3.18.4. Review-only.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets_src/characters/grand_puff_video_cels_2026-09-15'
TMP = ROOT / 'tmp/grand-puff-video-cels'
SOURCES = [
 ('laugh', 'f55d22365cd7f5380ea8d01abe471fe70399f822', 'r02/P01_LAUGH/P01_LAUGH_study_silent.mp4', '091ba1a3f544b9116770bef0dcc98bf56d6f1452a89a571b5cd32abbeeb2ef8f', 'Preferred laugh reference; retain unequal pulses and happy finish.'),
 ('huff', '616a5db3599b90ef7961ed07aafc674c41586147', 'r09/P02_ANGRY_WINDUP/P02_ANGRY_WINDUP_study_silent.mp4', 'e7e960c6a37ff491cceb75e9a8c7294580381cc742ee4c40f558e1023b9c08cd', 'Partial huff, not complete windup. Closed-eye effort and initial smile are preserved honestly.'),
 ('friendship', '8dd2d96a00e7776752ef67117f5685cd7f054103', 'r04/P03_FRIENDS/P03_FRIENDS_study_silent.mp4', 'b3ec9764a76dab379cedf25d54f637043ebd4f0e6cdddb68989fe9ff80dd888f', 'Preferred friendship reference; source shrink and roughly20px support drift retained, not silently corrected.')
]

def sha(data): return hashlib.sha256(data).hexdigest()
def write_json(path, value): path.write_bytes((json.dumps(value, indent=2)+'\n').encode())
def run(args): return subprocess.check_output(args, cwd=ROOT, stderr=subprocess.PIPE)
def luaquote(p): return json.dumps(str(p).replace('\\','/'))

def build(ffmpeg, aseprite):
 OUT.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)
 (OUT/'sources').mkdir(exist_ok=True); (OUT/'previews').mkdir(exist_ok=True)
 clips=[]
 for name, rev, rel, expected, limits in SOURCES:
  srcpath='assets_src/characters/grand_puff_personality_returns/'+rel
  source=OUT/'sources'/f'{name}.mp4'
  data=run(['git','show',rev+':'+srcpath]); assert sha(data)==expected
  source.write_bytes(data)
  meta=json.loads(run([str(Path(ffmpeg).with_name('ffprobe.exe')),'-v','error','-show_streams','-show_format','-of','json',str(source)]))
  stream=next(s for s in meta['streams'] if s['codec_type']=='video')
  assert (stream['width'],stream['height'],stream['r_frame_rate'])==(1280,720,'24/1')
  frames=np.frombuffer(run([ffmpeg,'-v','error','-i',str(source),'-f','rawvideo','-pix_fmt','rgb24','-']),dtype=np.uint8).reshape((-1,720,1280,3))
  folder=TMP/name; folder.mkdir(exist_ok=True)
  rows=[]
  for i,rgb in enumerate(frames):
   a=rgb.astype(np.int16)
   ink=(a[:,:,2]-a[:,:,1]>10)&(a[:,:,0]-a[:,:,1]>3)&(a[:,:,1]<220)
   labels,_=ndimage.label(ink); counts=np.bincount(labels.ravel());counts[0]=0
   mask=ndimage.binary_fill_holes(labels==counts.argmax())
   yy,xx=np.where(mask); bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
   assert bounds[0]>129 and bounds[2]<1151,(name,i,bounds)
   # One fixed center crop; no per-frame fitting, resizing, pose/anchor correction.
   crop=rgb[:,128:1152]; alpha=mask[:,128:1152].astype(np.uint8)*255
   rgba=np.dstack([crop,alpha]);rgba[alpha==0,:3]=0
   im=Image.fromarray(rgba); im.save(folder/f'{i:03d}.png')
   duration=round((i+1)*1000/24)-round(i*1000/24)
   rows.append({'source_frame_index':i,'source_time_seconds':i/24,'duration_ms':duration,'source_rgb_sha256':sha(rgb.tobytes()),'alpha_sha256':sha(alpha.tobytes()),'cel_rgba_sha256':sha(rgba.tobytes()),'source_bounds_xyxy':bounds,'source_boundary_contact':bounds[1]==0 or bounds[3]==720,'pixel_method':'source RGB preserved on opaque silhouette; exterior alpha0; fixed x128 crop'})
  Image.fromarray(frames[0][:,128:1152]).save(folder/'source_first_frame.png')
  clip={'id':name,'intent':limits,'source_commit':rev,'source_path':srcpath,'source_local':source.relative_to(OUT).as_posix(),'source_sha256':expected,'source_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+rev+'/'+srcpath,'canvas':[1024,720],'source_canvas':[1280,720],'crop_xyxy':[128,0,1152,720],'scale':1,'fps':24,'frames':rows,'native_path':f'grand_puff_{name}.aseprite','layers':['Source first frame - hidden reference','Character - exact video pixels','Pixel cleanup - editable empty layer'],'pivot':[512,674],'pivot_note':'Fixed canvas marker only; source floor motion retained. Not runtime-approved.','loop':False,'events':[],'runtime_integration':False,'interruptions':'Not applicable: standalone review document; gameplay remains unchanged.'}
  clips.append(clip)
  lua=['local s=Sprite(1024,720,ColorMode.RGB)','local ref=s.layers[1]',f'ref.name={luaquote(clip["layers"][0])}',f's:newCel(ref,1,Image{{fromFile={luaquote(folder/"source_first_frame.png")}}},Point(0,0))','ref.isVisible=false','ref.isEditable=false','local actor=s:newLayer()',f'actor.name={luaquote(clip["layers"][1])}']
  for i,row in enumerate(rows,1):
   if i>1:lua.append('s:newEmptyFrame()')
   lua += [f's.frames[{i}].duration={row["duration_ms"]}/1000',f's:newCel(actor,{i},Image{{fromFile={luaquote(folder/f"{i-1:03d}.png")}}},Point(0,0))']
  lua+=['local cleanup=s:newLayer()',f'cleanup.name={luaquote(clip["layers"][2])}',f'local tag=s:newTag(1,{len(rows)})',f'tag.name={luaquote(name+" - video-derived review")}',f's:saveAs({luaquote(OUT/clip["native_path"])})','s:close()']
  script=folder/'build.lua';script.write_bytes(('\n'.join(lua)+'\n').encode());run([aseprite,'--batch','--script',str(script)])
  print('Built',name,len(rows),'editable cels',flush=True)
 write_json(OUT/'CEL_MANIFEST.json',{'schema':'grand-puff-video-cels-v1','owner_exception':'2026-09-15 explicit video-pixel reconstruction request; AGENTS Grand Puff exception','method':'Automated pixel transfer and silhouette isolation, not hand-drawn reinterpretation. Every source frame preserved at1:1 within fixed crop.','clips':clips,'delivery_accepted':False,'previous_build_preserved':'ac4dd5e7ed6fcbb8c6d0aa4135e176d616830149 review-cycle branch; previous Aseprite candidate unchanged.'})

def verify(ffmpeg,aseprite):
 m=json.loads((OUT/'CEL_MANIFEST.json').read_text());results=[]
 for clip in m['clips']:
  name=clip['id'];folder=TMP/name;export=folder/'roundtrip';export.mkdir(exist_ok=True)
  lines=[f'local s=app.open({luaquote(OUT/clip["native_path"])})',f'assert(#s.frames=={len(clip["frames"])})','assert(s.width==1024 and s.height==720)','assert(#s.layers==3)','assert(not s.layers[1].isVisible)','local rows={}']
  for i,row in enumerate(clip['frames'],1):
   lines += [f'assert(math.floor(s.frames[{i}].duration*1000+0.5)=={row["duration_ms"]})',f'local im{i}=Image(1024,720,ColorMode.RGB)',f'im{i}:drawSprite(s,{i})',f'im{i}:saveAs({luaquote(export/f"{i-1:03d}.png")})']
  # Lua has a 200 local limit: scope each frame's temporary raster.
  lines=[('do '+line) if line.startswith('local im') else (line+' end') if ':saveAs(' in line else line for line in lines]
  lines+=['s:close()'];script=folder/'verify.lua';script.write_bytes(('\n'.join(lines)+'\n').encode());run([aseprite,'--batch','--script',str(script)])
  for i,row in enumerate(clip['frames']):
   a=np.asarray(Image.open(export/f'{i:03d}.png').convert('RGBA'));assert sha(a.tobytes())==row['cel_rgba_sha256'],(name,i)
  # Reviews are made from the native round-trip, never substituted build inputs.
  board=Image.new('RGB',(1024,848),'#193348');d=ImageDraw.Draw(board)
  d.text((16,10),name.upper()+' | Aseprite round-trip | exact video pixels | review candidate',fill='white')
  for k,i in enumerate([0,12,24,36,48,60,72,84,96,108,120,144]):
   i=min(i,len(clip['frames'])-1);im=Image.open(export/f'{i:03d}.png').convert('RGBA');im.thumbnail((252,178),Image.Resampling.LANCZOS);x=(k%4)*256;y=40+(k//4)*264
   board.paste(im,(x,y+24),im);d.text((x+8,y),f'frame {i} / {i/24:.2f}s',fill='white')
  board.save(OUT/'previews'/f'{name}_contact.png')
  # Side-by-side faithful source and Aseprite composite, constant 50% preview scale.
  source=OUT/clip['source_local']
  command=[ffmpeg,'-y','-v','error','-i',str(source),'-framerate','24','-i',str(export/'%03d.png'),'-filter_complex','[0:v]crop=1024:720:128:0,scale=512:360[left];color=c=0x193348:s=1024x720:r=24[bg];[bg][1:v]overlay=shortest=1,scale=512:360[right];[left][right]hstack=shortest=1[v]','-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'previews'/f'{name}_source_vs_aseprite.mp4')]
  run(command)
  assert sha(source.read_bytes())==clip['source_sha256']
  results.append({'clip':name,'native_sha256':sha((OUT/clip['native_path']).read_bytes()),'frames_verified':len(clip['frames']),'rgba_roundtrip':'exact byte match for every pixel of every cel','timing':'integer ms within0.5ms cumulative of source24fps','source_preserved':True,'visual_acceptance':'pending owner; source defects retained'})
  print('Verified',name,'all pixels and frame durations',flush=True)
 write_json(OUT/'VERIFICATION.json',{'schema':'grand-puff-video-cels-verification-v1','aseprite_version':run([aseprite,'--version']).decode().strip(),'results':results,'runtime_changes':False,'production_accepted':False})

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['build','verify','all'],default='all');p.add_argument('--ffmpeg',default='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe');p.add_argument('--aseprite',default='C:/Program Files/Aseprite/Aseprite.exe');a=p.parse_args()
 if a.phase in ('build','all'):build(a.ffmpeg,a.aseprite)
 if a.phase in ('verify','all'):verify(a.ffmpeg,a.aseprite)
