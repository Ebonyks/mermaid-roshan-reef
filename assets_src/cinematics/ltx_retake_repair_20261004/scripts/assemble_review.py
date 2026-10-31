from pathlib import Path
import json,subprocess,shutil,hashlib,tempfile,argparse
from PIL import Image,ImageDraw
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--take',required=True);a=ap.parse_args()
p=Path(__file__).resolve().parents[1];out=p/'results'/a.take;source=p.parent/'ltx_registered_wave_20261004/results/figure_wide_slow/native_frames';ase=r'C:\Program Files\Aseprite\Aseprite.exe';ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
(p/'inputs/source_frames').mkdir(exist_ok=True)
for i in range(40,65):shutil.copyfile(source/f'{i:04d}.png',p/f'inputs/source_frames/{i:04d}.png')
subprocess.run([ase,'-b','--script-param','packet='+str(p),'--script-param','take='+a.take,'--script',str(p/'scripts/finish_trial.lua')],check=True,timeout=180)
scratch=Path(tempfile.mkdtemp(prefix='retake_ase_roundtrip_'))
subprocess.run([ase,'-b','--script-param','input='+str(out/'repair_window.aseprite'),'--script-param','output='+str(scratch),'--script',str(p.parent/'ltx_registered_wave_20261004/scripts/reopen_wave.lua')],check=True,timeout=180)
for i in range(25):assert np.array_equal(np.array(Image.open(out/f'native_frames/{i:04d}.png').convert('RGBA')),np.array(Image.open(scratch/f'reopened_{i:04d}.png').convert('RGBA'))) 
native_size=Image.open(out/'native_frames/0000.png').size
production_frames=out/'native_frames';transform=None
if native_size!=(896,512):
 production_frames=out/'normalized_frames';production_frames.mkdir(exist_ok=True)
 subprocess.run([ase,'-b','--script-param','input='+str(out/'repair_window.aseprite'),'--script-param','output='+str(out),'--script',str(p/'scripts/normalize_window.lua')],check=True,timeout=180)
 transform={'method':'Aseprite whole-canvas bilinear scale','source_dimensions':list(native_size),'preview_dimensions':[896,512],'applied_to_complete_frame':True,'native_preserved':True,'quality_repair':False}
assembled=out/'assembled_frames';assembled.mkdir(exist_ok=True);rows=[]
for i in range(81):
 replacement=41<=i<=63
 src=production_frames/f'{i-40:04d}.png' if replacement else source/f'{i:04d}.png';dst=assembled/f'{i:04d}.png';shutil.copyfile(src,dst)
 rows.append({'global_index':i,'source':'generated_whole_frame_window' if replacement else 'original_native_frame','source_local_index':i-40 if replacement else i,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'outside_window_byte_preserved':not replacement})
frames=[np.array(Image.open(assembled/f'{i:04d}.png').convert('RGB')) for i in range(81)]
seams={}
for left,right in [(39,40),(40,41),(63,64),(64,65)]:
 delta=np.abs(frames[right][25:475,280:680].astype(float)-frames[left][25:475,280:680].astype(float));seams[f'{left}->{right}']={'figure_roi_mean_absolute_rgb_delta':float(delta.mean()),'diagnostic_only_not_motion_acceptance':True}
(out/'verification.json').write_text(json.dumps({'status':'PASS','native_dimensions':list(native_size),'comparison_transform':transform,'aseprite_roundtrip_complete_frames':25,'assembled_frames':81,'replacement_global_span_inclusive':[41,63],'outside_replacement_original_bytes_preserved':True,'fixed_body_overlay':False,'isolated_limb_render':False,'seam_diagnostics':seams,'frame_mapping':rows,'human_device_acceptance':'PENDING'},indent=2)+'\n')
for folder,name,count in [(out/'native_frames','window.mp4',25),(assembled,'assembled.mp4',81)]:
 subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-framerate','24','-i',str(folder/'%04d.png'),'-frames:v',str(count),'-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-an',str(out/name)],check=True,timeout=120)
indices=[0,2,4,6,8,10,12,16,20,24];sheet=Image.new('RGB',(5*320,2*398),(238,238,238));d=ImageDraw.Draw(sheet)
for j,i in enumerate(indices):
 im=Image.open(production_frames/f'{i:04d}.png').convert('RGB').crop((280,20,680,490)).resize((320,376));x=j%5*320;y=j//5*398;sheet.paste(im,(x,y+22));d.text((x+5,y+4),f'Global {i+40}',fill='black')
sheet.save(out/'contact.png')
print('ASE_ROUNDTRIP_AND_ASSEMBLY_PASS',a.take,flush=True)
