"""Full native-frame preservation and Aseprite round-trip, with diagnostic regional motion facts."""
from pathlib import Path
import subprocess,tempfile,json,hashlib,argparse
from PIL import Image,ImageDraw
import numpy as np
a=argparse.ArgumentParser();a.add_argument('--take',default='figure_wide_root');args=a.parse_args();p=Path(__file__).resolve().parents[1];out=p/'results'/args.take;count=81 if args.take=='figure_wide_slow' else 41;factor=2 if count==81 else 1;ase=r'C:\Program Files\Aseprite\Aseprite.exe';ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
subprocess.run([ase,'-b','--script-param','packet='+str(p),'--script-param','take='+args.take,'--script',str(p/'scripts/finish_figure.lua')],check=True,timeout=120)
scratch=Path(tempfile.mkdtemp(prefix='whole_figure_reopen_'))
subprocess.run([ase,'-b','--script-param','input='+str(out/'wave_full_figure.aseprite'),'--script-param','output='+str(scratch),'--script',str(p/'scripts/reopen_wave.lua')],check=True,timeout=120)
rows=[];unique=[];raws=[]
for i in range(count):
 f=out/f'native_frames/{i:04d}.png';a=np.array(Image.open(f).convert('RGBA'));b=np.array(Image.open(scratch/f'reopened_{i:04d}.png').convert('RGBA'));assert np.array_equal(a,b)
 unique.append(hashlib.sha256(a.tobytes()).hexdigest());raws.append(a[:,:,:3]);rows.append({'index':i,'native_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'reopened_visible_rgba_equals_complete_native':True,'visible_pixels_from':'Full native frame; no body plate, region mask, limb replacement, source endpoint substitution or global sharpening.'})
regions={'shoulders':(420,185,520,245),'bodice':(438,205,495,278),'head_hair':(412,70,563,195),'tail':(414,288,627,450)};facts={}
for name,(x0,y0,x1,y1) in regions.items():
 vals=[]
 for i in range(1,count):
  delta=np.max(np.abs(raws[i][y0:y1,x0:x1].astype(int)-raws[0][y0:y1,x0:x1].astype(int)),axis=2);vals.append(float(np.mean(delta>12)))
 facts[name]={'max_changed_pixel_fraction_vs_frame0_threshold_12':max(vals),'note':'Diagnostic raster change, not semantic/anatomical motion or acceptance.'}
result={'status':'PASS','native_frames':count,'native_unique_frames':len(set(unique)),'whole_frame_master_round_trip':True,'fixed_body_overlay':False,'isolated_limb_render':False,'regional_raster_changes':facts,'frames':rows,'acceptance':'REFERENCE_ONLY; frame preservation is not human continuity/blur/device acceptance.'}
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
for name,indices,cols,scale in [('key_frames',[i*factor for i in [0,3,7,12,17,23,27,33,36,40]],5,.7),('all_frames',list(range(count)),7,.43)]:
 w,h=round(400*scale),round(470*scale);s=Image.new('RGB',(cols*w,((len(indices)+cols-1)//cols)*(h+24)),(238,238,238));d=ImageDraw.Draw(s)
 for n,i in enumerate(indices):
  im=Image.open(out/f'native_frames/{i:04d}.png').convert('RGB').crop((280,20,680,490)).resize((w,h));x=n%cols*w;y=n//cols*(h+24);s.paste(im,(x,y+24));d.text((x+4,y+3),str(i),fill='black')
 s.save(out/(name+'.png'))
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-framerate','24','-start_number','0','-i',str(out/'native_frames/%04d.png'),'-frames:v',str(count),'-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-an',str(out/'preview.mp4')],check=True,timeout=120)
probe=subprocess.run([ff.replace('ffmpeg.exe','ffprobe.exe'),'-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_read_frames','-of','json',str(out/'preview.mp4')],capture_output=True,text=True,check=True);data=json.loads(probe.stdout);s=data['streams'][0];assert (s['width'],s['height'],s['r_frame_rate'],s['nb_read_frames'])==(896,512,'24/1',str(count))
(out/'media_verification.json').write_text(json.dumps({'media':data,'sha256':hashlib.sha256((out/'preview.mp4').read_bytes()).hexdigest()},indent=2)+'\n')
print('FULL_FIGURE_VERIFY PASS unique',len(set(unique)),flush=True)
