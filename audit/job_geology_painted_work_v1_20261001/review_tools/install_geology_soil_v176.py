from pathlib import Path
import hashlib,json,shutil,subprocess
from PIL import Image
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geology_painted_work_v1_20261001';s=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001/fossil_soil/attempt_02'
native=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-ef428440-18a6-45e0-913b-c538b83752ee.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert not (s/'native_generated.png').exists();shutil.copyfile(native,s/'native_generated.png')
image=Image.open(native);bounds=image.getchannel('A').point(lambda v:255 if v>4 else 0).getbbox();print('Native',image.size,'visible bounds',bounds)
derivative=s/'whole_canvas_1024.png'
cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','error','-i',str(native),'-vf','scale=1024:1024:flags=lanczos','-frames:v','1',str(derivative)]
result=subprocess.run(cmd,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert result.returncode==0,result.stderr.decode()
scaled=Image.open(derivative);bounds=scaled.getchannel('A').point(lambda v:255 if v>4 else 0).getbbox()
region=[bounds[0],bounds[1],bounds[2]-bounds[0],bounds[3]-bounds[1]]
target=r/'assets/opera/worlds/geology/painted_work_v1_20261001/fossil_soil.png';assert not target.exists();shutil.copyfile(derivative,target)
review={'status':'SOURCE_DIRECT_REVIEW_MOUNTED_PENDING','attempt':2,'source_score':4.6,'material_score':4.6,'cover_geometry_score':None,'owner_acceptance':None,'native_dimensions':list(image.size),'native_path':(s/'native_generated.png').relative_to(r).as_posix(),'native_sha256':sha(native),'derivative_path':derivative.relative_to(r).as_posix(),'derivative_sha256':sha(derivative),'runtime_path':target.relative_to(r).as_posix(),'atlas_region':region,'generation_method':'OpenAI built-in image_gen, fresh complete transparent source','prompt_sha256':sha(s/'PROMPT.txt'),'production_transform':'One whole-canvas uniform Lanczos resize to1024x1024 PNG only. Native RGBA retained. No mask, alpha cleanup, subject warp, relighting or compositing. Atlas sampling measured from alpha>4 bounding box; insignificant outer alpha specks remain in source bytes.','normalization_command':cmd,'review':'Hand-painted ochre/cream broad bands and lavender edge shadows match the source family. Few corner stone clusters frame a calm opaque central soil bed. Deeper footprint meets the concealment role in principle; fit and40-cell continuous sampling require actual native engine evidence. Never infer runtime/pass from source finish.'}
write(s/'REVIEW.json',review);write(f/'SOIL_SOURCE_REVIEW.json',review)
p=r/'scripts/opera_geology_surface.gd';text=p.read_text()
text=text.replace('const FOSSIL_RECT := Rect2(500.0, 215.0, 560.0, 300.0)',f'const FOSSIL_SOIL_WIDTH := 300.0 * {region[2]}.0 / {region[3]}.0\nconst FOSSIL_RECT := Rect2(780.0 - FOSSIL_SOIL_WIDTH * 0.5, 215.0, FOSSIL_SOIL_WIDTH, 300.0)')
text=text.replace('var _pan_grain_texture: Texture2D = null','var _pan_grain_texture: Texture2D = null\nvar _fossil_soil_texture: Texture2D = null')
text=text.replace('_pan_grain_texture = _geode_atlas(WORK_ART + "grain.png", Rect2(228, 120, 569, 439))','_pan_grain_texture = _geode_atlas(WORK_ART + "grain.png", Rect2(228, 120, 569, 439))\n\t_fossil_soil_texture = _geode_atlas(WORK_ART + "fossil_soil.png", Rect2('+', '.join(map(str,region))+'))')
old='''					draw_rect(Rect2(FOSSIL_RECT.position \\
						+ Vector2(column, row) * cell_size,
						cell_size + Vector2.ONE), Color("#c99159"), true)'''
new='''					if _fossil_soil_texture != null:
						var source_cell := _fossil_soil_texture.get_size()
							/ Vector2(FOSSIL_GRID_COLS, FOSSIL_GRID_ROWS)
						draw_texture_rect_region(_fossil_soil_texture,
							Rect2(FOSSIL_RECT.position + Vector2(column, row) * cell_size,
								cell_size), Rect2(Vector2(column, row) * source_cell, source_cell))'''
new=new.replace('var source_cell := _fossil_soil_texture.get_size()\n','var source_cell := _fossil_soil_texture.get_size() \\\n')
assert old in text;assert 'FOSSIL_SOIL_WIDTH' in text;text=text.replace(old,new);p.write_text(text,encoding='utf-8')
capture=f/'capture_geology_painted_work.gd';text=capture.read_text();assert '/attempt_02/' in text;text=text.replace('/attempt_02/','/attempt_03/');capture.write_text(text,encoding='utf-8');(f/'attempt_03').mkdir()
with (r/'ASSET_LICENSES.md').open('a',encoding='utf-8') as out:
 for path,role,mod in [(s/'native_generated.png','soil source attempt2','Complete original RGBA generation, preserved'),(derivative,'soil source production derivative','Whole-canvas uniform1024 resize only'),(target,'soil runtime','Exact derivative byte copy; AtlasTexture/cell regions preserve source layout'),(s.parent/'attempt_01/native_generated.png','soil rejected attempt1','Complete native source preserved outside runtime')]:
  out.write('| `'+path.relative_to(r).as_posix()+'` | Owner-commissioned OpenAI ImageGen; fossil soil source attempts1/2, prompt/provenance in source family | Generated asset for this project; no third-party URL; SHA256 '+sha(path)+' | '+mod+' |\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
impact=r/'design/audit_impacts/job-geology-painted-work-20261001.json';d=json.loads(impact.read_text());d['scope']+=' Soil attempt1 is preserved4.5source/4.0cover geometry rejected; attempt2 source4.6 is only uniformly normalized whole-canvas. Align the8x5 brush bed to measured source aspect and40cell source regions, avoiding stretch, changing no clearing threshold/save indices. Native concealment/partial-clear checks required in attempt03.';d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for folder in [f,s.parent,r/'assets/opera/worlds/geology/painted_work_v1_20261001'] for x in folder.rglob('*') if x.is_file()});write(impact,d)
print('Installed soil attempt2 at measured region',region,'after preserved first geometry failure; native review pending.')
