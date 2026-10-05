from pathlib import Path
import subprocess,shutil,json,hashlib
from PIL import Image
p=Path(__file__).resolve().parents[1]
subprocess.run([r'C:\Program Files\Aseprite\Aseprite.exe','-b','--script-param','packet='+str(p),'--script',str(p/'scripts/export_bridge.lua')],check=True,timeout=120)
rows=[]
for idx,name in [(0,'original_0040.png'),(8,'corrected_0048.png'),(24,'original_0064.png')]:
 f=p/'inputs'/('exported_'+name);assert Image.open(f).size==(896,512)
 dst=Path(r'H:\MermaidReefTools\LocalVideo\input')/('retake_trial_'+name);shutil.copyfile(f,dst)
 rows.append({'local_index':idx,'global_index':idx+40,'path':str(f.relative_to(p)).replace('\\','/'),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'whole_canvas_export':True})
(p/'environment/aseprite_bindings.json').write_text(json.dumps({'master':'inputs/repair_keys.aseprite','guides':rows,'registration_is_not_pixel_freeze':True},indent=2)+'\n')
print('ASEPRITE_GUIDES_EXPORTED_AND_BOUND',flush=True)
