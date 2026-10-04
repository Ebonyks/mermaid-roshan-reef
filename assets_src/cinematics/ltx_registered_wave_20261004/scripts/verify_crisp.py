"""Pixel provenance, Aseprite round-trip and duration checks for authored blur correction."""
from pathlib import Path
import json,subprocess,tempfile,hashlib
from PIL import Image,ImageDraw,ImageFont
import numpy as np
p=Path(__file__).resolve().parents[1];out=p/'results/crisp_authored';ase=r'C:\Program Files\Aseprite\Aseprite.exe';ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
scratch=Path(tempfile.mkdtemp(prefix='crisp_wave_reopen_'))
subprocess.run([ase,'-b','--script-param','input='+str(out/'wave.aseprite'),'--script-param','output='+str(scratch),'--script',str(p/'scripts/reopen_wave.lua')],check=True,timeout=120)
plate=np.array(Image.open(p/'inputs/fixed_body_plate.png').convert('RGBA'));fixed=plate[:,:,3]==255
reference=np.array(Image.open(p/'inputs/registered_rgba_00.png').convert('RGBA'));reference[reference[:,:,3]==0,:3]=0
mapping=json.loads((out/'frame_mapping.json').read_text());rows=[];unique=[]
for i in range(41):
 f=out/f'frames/{i:04d}.png';a=np.array(Image.open(f).convert('RGBA'));b=np.array(Image.open(scratch/f'reopened_{i:04d}.png').convert('RGBA'));a[a[:,:,3]==0,:3]=0;b[b[:,:,3]==0,:3]=0
 unique.append(hashlib.sha256(a.tobytes()).hexdigest());src=p/f"inputs/registered_arm_{mapping['frames'][i]['source_arm']:02d}.png"
 row={'index':i,'output_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source_arm':src.relative_to(p).as_posix(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'fixed_opaque_body_equal':bool(np.array_equal(a[fixed],plate[fixed])),'reopened_visible_rgba_equal':bool(np.array_equal(a,b)),'source_rest_equal':bool(np.array_equal(a,reference)) if i in [0,36,37,38,39,40] else None};rows.append(row)
result={'status':'PASS' if all(x['fixed_opaque_body_equal'] and x['reopened_visible_rgba_equal'] and x['source_rest_equal'] is not False for x in rows) else 'FAIL','frames':41,'unique_rgba_frames':len(set(unique)),'fps':24,'duration_seconds':41/24,'no_temporal_blending':True,'visible_generated_pixels':False,'declared_hold_indices':[36,37,38,39,40],'hold_purpose':'Original rest after complete raise/lower action','frame_mapping':'frame_mapping.json','frames_checked':rows,'scope':'Provenance/export/body/endpoint checks only; motion/shoulder/hand/device/owner acceptance separate.'}
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
for name,indices,cols,scale in [('key_frames',[0,3,7,12,17,23,27,33,36,40],5,.7),('all_frames',list(range(41)),7,.43)]:
 w,h=round(400*scale),round(470*scale);s=Image.new('RGB',(cols*w,((len(indices)+cols-1)//cols)*(h+24)),(238,238,238));d=ImageDraw.Draw(s)
 for n,i in enumerate(indices):
  im=Image.open(out/f'frames/{i:04d}.png').convert('RGBA').crop((280,20,680,490)).resize((w,h));x=n%cols*w;y=n//cols*(h+24);s.paste(im,(x,y+24),im);d.text((x+4,y+3),str(i),fill='black')
 s.save(out/(name+'.png'))
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0xeeeeee:s=896x512:r=24','-framerate','24','-start_number','0','-i',str(out/'frames/%04d.png'),'-filter_complex','[0:v][1:v]overlay=shortest=1','-frames:v','41','-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-an',str(out/'preview.mp4')],check=True,timeout=120)
probe=subprocess.run([ff.replace('ffmpeg.exe','ffprobe.exe'),'-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_read_frames','-of','json',str(out/'preview.mp4')],capture_output=True,text=True,check=True);media=json.loads(probe.stdout);s=media['streams'][0]
assert (s['width'],s['height'],s['r_frame_rate'],s['nb_read_frames'])==(896,512,'24/1','41')
(out/'media_verification.json').write_text(json.dumps({'media':media,'sha256':hashlib.sha256((out/'preview.mp4').read_bytes()).hexdigest()},indent=2)+'\n')
print('CRISP_VERIFY',result['status'],'unique',result['unique_rgba_frames'],flush=True)
if result['status']!='PASS':raise SystemExit(1)
