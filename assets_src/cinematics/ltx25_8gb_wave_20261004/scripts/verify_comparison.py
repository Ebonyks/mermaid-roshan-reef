from pathlib import Path
import ast,json,hashlib,subprocess
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parents[1]
m=json.loads((p/'comparison/mapping.json').read_text())
for i in range(m['frames']):
 with Image.open(p/f'comparison/frames/{i:04d}.png') as im:
  assert im.size==(2304,832)
  canvas=np.array(im.convert('RGBA'))
 for c,take in enumerate(m['columns']):
  source=m['source_indices'][take][i]
  with Image.open(p/f'results/{take}/refined_frames/{source:04d}.png') as im:
   assert np.array_equal(canvas[:,c*576:(c+1)*576],np.array(im.convert('RGBA'))),(i,take)
for i in range(41):
 assert (p/f'results/temporal_48fps/comparison24_frames/{i:04d}.png').read_bytes()==(p/f'results/temporal_48fps/refined_frames/{2*i:04d}.png').read_bytes()
files=list((p/'scripts').rglob('*.py'))
for f in files:ast.parse(f.read_text(encoding='utf-8'),filename=str(f))
ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe'
v=json.loads(subprocess.run([ff,'-v','error','-show_streams','-of','json',str(p/'comparison/native_four_takes.mp4')],capture_output=True,text=True,check=True).stdout)['streams'][0]
assert (v['width'],v['height'],int(v['nb_frames']),v['avg_frame_rate'])==(2304,832,41,'24/1')
j={'status':'PASS','native_comparison_frames':41,'byte_equal_complete_frame_columns':164,'exact_even_source_frame_selections':41,'python_sources_ast_parsed':len(files),'video_dimensions':[2304,832],'video_frames':41,'video_fps':24,'no_spatial_resampling':True,'no_pixel_repair':True}
(p/'environment/comparison_verification.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j),flush=True)
