"""Export the completed fifth take and Aseprite registration review; no new job."""
from pathlib import Path
import subprocess,shutil,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from measure_scale_landmarks import landmarks
P=Path(__file__).resolve().parents[1]
ASE=r'C:\Program Files\Aseprite\Aseprite.exe'
FF=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
def ase(script,**params):
 args=[ASE,'-b']
 for k,v in params.items():args+=['--script-param',k+'='+str(v)]
 subprocess.run(args+['--script',str(P/'scripts'/script)],check=True,timeout=180)
def main():
 src=Path(r'H:\MermaidReefTools\LocalVideo\ltx25\results\scale_registered');dst=P/'results/scale_registered'
 assert json.loads((src/'receipt.json').read_text())['status']=='EXECUTION_PASS'
 if not dst.exists():shutil.copytree(src,dst)
 assert (dst/'receipt.json').read_bytes()==(src/'receipt.json').read_bytes()
 ase('export_review.lua',take=dst)
 subprocess.run([sys.executable,'-X','utf8','-s','-B',str(P/'scripts/plan_decoded_registration.py')],check=True)
 ase('filter_decoded_in_aseprite.lua',packet=P)
 f=P/'scale_continuity/decoded_registration_plan.json';plan=json.loads(f.read_text());count=0
 for row in plan['frames']:
  if not row['pass']:continue
  observed,h=landmarks(P/f"scale_continuity/decoded_filtered/{row['index']:04d}.png")
  delta=np.round(np.array(row['target_landmarks']['bodice_waist_tip'])-observed['bodice_waist_tip']).astype(int)
  if np.any(delta):
   assert np.max(abs(delta))<=3,'Measured raster shift too large; manual review required'
   row['placement']=(np.array(row['placement'])+delta).tolist();row['raster_rounding_translation_adjustment']=delta.tolist();count+=1
 f.write_text(json.dumps(plan,indent=2)+'\n');print('RASTER_ROUNDING_ADJUSTED',count,flush=True)
 ase('filter_decoded_in_aseprite.lua',packet=P)
 subprocess.run([sys.executable,'-X','utf8','-s','-B',str(P/'scripts/verify_scale_filter.py')],check=True)
 ase('apply_scale_gate_tags.lua',packet=P)
 ase('scale_comparison.lua',packet=P)
 for folder,out in [(dst/'refined_frames',dst/'native.mp4'),(P/'scale_continuity/decoded_filtered',P/'scale_continuity/filtered_review.mp4'),(P/'scale_continuity/comparison_frames',P/'scale_continuity/scale_comparison.mp4')]:
  subprocess.run([FF,'-v','error','-framerate','24','-i',str(folder/'%04d.png'),'-frames:v','41','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(out)],check=True,timeout=180)
 (P/'scale_continuity/comparison_mapping.json').write_text(json.dumps({'columns':['original_base_native','registered_input_take_native','aseprite_filtered_review'],'column_dimensions':[576,832],'frames':41,'fps':24,'source_indices':list(range(41)),'no_comparison_resizing_or_interpolation':True,'filtered_transforms':'decoded_registration_plan.json','failed_frames_retained_unchanged':True,'accepted':False},indent=2)+'\n')
 print('SCALE_REVIEW_EXPORTED',flush=True)
if __name__=='__main__':main()
