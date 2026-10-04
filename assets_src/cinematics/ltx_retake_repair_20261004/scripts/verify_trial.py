"""Meaningful source-side checks: editable export, timing and whole-frame provenance."""
from pathlib import Path
import json,hashlib,subprocess,tempfile
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parents[1];ase=r'C:\Program Files\Aseprite\Aseprite.exe';ffprobe=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
keys=json.loads((p/'inputs/tagged_exports/tagged_keys.json').read_text());assert [x['source_global_frame'] for x in keys['keys']]==[40,48,64]
for row,name in zip(keys['keys'],['original_0040.png','corrected_0048.png','original_0064.png']):
 assert np.array_equal(np.array(Image.open(p/'inputs/tagged_exports'/row['path']).convert('RGBA')),np.array(Image.open(p/'inputs'/name).convert('RGBA')))
apng=Image.open(p/'inputs/source_window.apng');assert apng.n_frames==25
for i in range(25):
 apng.seek(i)
 assert np.array_equal(np.array(apng.convert('RGB')),np.array(Image.open(p/f'inputs/source_frames/{i+40:04d}.png').convert('RGB')))
results=[]
for take in ['ltxv_guide_standard','ltxv_guide_strong','ltx23_retake_lowmem']:
 out=p/'results'/take;j=json.loads((out/'receipt.json').read_text());assert j['status']=='EXECUTION_PASS' and len(j['native_outputs'])==25
 scratch=Path(tempfile.mkdtemp(prefix='retake_final_ase_'))
 subprocess.run([ase,'-b','--script-param','input='+str(out/'repair_window.aseprite'),'--script-param','output='+str(scratch),'--script',str(p.parent/'ltx_registered_wave_20261004/scripts/reopen_wave.lua')],check=True,timeout=180)
 for i in range(25):
  native=out/f'native_frames/{i:04d}.png';assert sha(native)==j['native_outputs'][i]['sha256']
  assert np.array_equal(np.array(Image.open(native).convert('RGBA')),np.array(Image.open(scratch/f'reopened_{i:04d}.png').convert('RGBA')))
 v=json.loads((out/'verification.json').read_text());assert v['outside_replacement_original_bytes_preserved'] and not v['fixed_body_overlay']
 source=p.parent/'ltx_registered_wave_20261004/results/figure_wide_slow/native_frames'
 for i in list(range(41))+list(range(64,81)):assert sha(out/f'assembled_frames/{i:04d}.png')==sha(source/f'{i:04d}.png')
 streams=[]
 for name,count in [('window.mp4',25),('assembled.mp4',81)]:
  data=json.loads(subprocess.run([ffprobe,'-v','error','-show_streams','-of','json',str(out/name)],capture_output=True,text=True,check=True).stdout);video=next(x for x in data['streams'] if x['codec_type']=='video');assert int(video['nb_frames'])==count and video['avg_frame_rate']=='24/1'
  streams.append({'path':name,'dimensions':[video['width'],video['height']],'frames':count,'fps':video['avg_frame_rate']})
 results.append({'take':take,'status':'PASS','aseprite_pixel_equal_native_frames':25,'native_hashes_unchanged':True,'outside_review_splice_byte_preserved_frames':58,'video_streams':streams})
failed=p/'results/ltx23_retake_standard';assert json.loads((failed/'receipt.json').read_text())['status']=='FAILED' and not list((failed/'native_frames').glob('*.png'))
assert all(f.stat().st_size>0 for f in p.rglob('*') if f.is_file() and f.name!='.gdignore')
result={'status':'PASS','tagged_key_export_pixel_equal':3,'completed_takes':results,'failed_attempt_has_no_invented_frames':True,'all_artifacts_nonempty_except_intentional_godot_gdignore_marker':True,'quality_acceptance':'FAIL/REFERENCE_ONLY; see human review; machine checks do not establish accepted motion'}
(p/'environment/trial_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('TRIAL_MACHINE_VERIFICATION_PASS',len(results),'completed takes; 75 native Aseprite frame checks')
