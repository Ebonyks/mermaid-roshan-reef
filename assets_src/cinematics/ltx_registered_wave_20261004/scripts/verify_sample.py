"""Verify study exports against source/native pixels and reopened Aseprite layers."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont
import numpy as np
a=argparse.ArgumentParser();a.add_argument('--take',default='registered');args=a.parse_args();p=Path(__file__).resolve().parents[1];take=args.take
ff=Path(r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe');ase=r'C:\Program Files\Aseprite\Aseprite.exe'
plate=np.array(Image.open(p/'inputs/fixed_body_plate.png').convert('RGBA'));fixed=plate[:,:,3]==255
reference=np.array(Image.open(p/'inputs/registered_rgba_00.png').convert('RGBA'));reference[reference[:,:,3]==0,:3]=0
scratch=Path(tempfile.mkdtemp(prefix='ltx_wave_reopen_'))
subprocess.run([ase,'-b','--script-param','input='+str(p/f'results/finished_{take}/wave.aseprite'),'--script-param','output='+str(scratch),'--script',str(p/'scripts/reopen_wave.lua')],check=True,timeout=120)
rows=[];native_hashes=[];final_hashes=[]
for i in range(41):
 src=p/f'results/{take}/native_frames/{i:04d}.png';dst=p/f'results/finished_{take}/frames/{i:04d}.png'
 raw=np.array(Image.open(src).convert('RGB'));final=np.array(Image.open(dst).convert('RGBA'));restore=np.array(Image.open(scratch/f'reopened_{i:04d}.png').convert('RGBA'))
 final[final[:,:,3]==0,:3]=0;restore[restore[:,:,3]==0,:3]=0
 nh=hashlib.sha256(raw.tobytes()).hexdigest();fh=hashlib.sha256(final.tobytes()).hexdigest();native_hashes.append(nh);final_hashes.append(fh)
 rows.append({'native_index':i,'native_png_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'final_png_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'fixed_opaque_body_equal':bool(np.array_equal(final[fixed],plate[fixed])),'reopened_visible_rgba_equal':bool(np.array_equal(final,restore)),'approved_rest_rgba_equal':bool(np.array_equal(final,reference)) if i in [0,40] else None,'moving_arm_parent':'inputs/registered_arm_00.png' if i in [0,40] else src.relative_to(p).as_posix()})
result={'status':'PASS' if all(x['fixed_opaque_body_equal'] and x['reopened_visible_rgba_equal'] for x in rows) and rows[0]['approved_rest_rgba_equal'] and rows[-1]['approved_rest_rgba_equal'] else 'FAIL','native_frames':41,'native_unique_pixel_frames':len(set(native_hashes)),'final_unique_pixel_frames':len(set(final_hashes)),'declared_same_rest_endpoints':[0,40],'frames':rows,'scope':'Pixel/frame provenance and editable master only; alpha fringes, shoulder/hand anatomy, action timing and human/device acceptance remain separate.'}
(p/f'results/finished_{take}/reopen_verification.json').write_text(json.dumps(result,indent=2)+'\n')
font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',15)
for name,indices,cols,scale in [('key_frames',[0,5,7,12,17,23,27,33,36,40],5,.7),('all_frames',list(range(41)),7,.43)]:
 for kind in [take,'finished_'+take]:
  frames='native_frames' if kind==take else 'frames';w,h=round(400*scale),round(470*scale);sheet=Image.new('RGB',(cols*w,((len(indices)+cols-1)//cols)*(h+24)),(220,213,236));draw=ImageDraw.Draw(sheet)
  for n,i in enumerate(indices):
   im=Image.open(p/f'results/{kind}/{frames}/{i:04d}.png').convert('RGBA').crop((280,20,680,490)).resize((w,h));x=n%cols*w;y=n//cols*(h+24);sheet.paste(im,(x,y+24),im);draw.text((x+5,y+3),str(i),font=font,fill=(20,20,20))
  sheet.save(p/f'results/{kind}/{name}.png')
media=[]
for kind,frames,bg in [(take,'native_frames',False),('isolated_'+take,'frames',True),('finished_'+take,'frames',True)]:
 inp=p/f'results/{kind}/{frames}';out=inp.parent/'preview.mp4';cmd=[str(ff),'-hide_banner','-loglevel','error','-y']
 if bg:cmd+=['-f','lavfi','-i','color=c=0xeeeeee:s=896x512:r=24']
 cmd+=['-framerate','24','-start_number','0','-i',str(inp/'%04d.png')]
 if bg:cmd+=['-filter_complex','[0:v][1:v]overlay=shortest=1']
 cmd+=['-frames:v','41','-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-an',str(out)]
 subprocess.run(cmd,check=True,timeout=120)
 probe=subprocess.run([str(ff.with_name('ffprobe.exe')),'-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,sample_aspect_ratio','-of','json',str(out)],capture_output=True,text=True,check=True);data=json.loads(probe.stdout);stream=data['streams'][0]
 if (stream['width'],stream['height'],int(stream['nb_read_frames']))!=(896,512,41) or stream['r_frame_rate']!='24/1':raise RuntimeError('Preview frame coverage/rate mismatch')
 media.append({'path':out.relative_to(p).as_posix(),'media':data,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(p/f'results/finished_{take}/media_verification.json').write_text(json.dumps(media,indent=2)+'\n')
print('VERIFIED',take,result['status'],'native_unique',result['native_unique_pixel_frames'],'final_unique',result['final_unique_pixel_frames'],flush=True)
if result['status']!='PASS':raise SystemExit(1)
