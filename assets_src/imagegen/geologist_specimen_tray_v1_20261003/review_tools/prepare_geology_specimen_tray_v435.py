from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'assets_src/imagegen/geologist_specimen_tray_v1_20261003';assert not F.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
base=subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,check=True).stdout.decode().strip()
assert base=='1652a9bb33af0d11a594b5996df66d2266c02d39'
prior=read(R/'design/audit_impacts/job-geode-current-recheck-20261002.json')
ip=R/'design/audit_impacts/job-geology-specimen-tray-20261003.json'
write(ip,{'id':'job-geology-specimen-tray-20261003','baseline':base,'scope':'Bounded fresh text-only painted empty specimen-tray candidate for the three named flat Geologist invitation tray drawings scored2.9. Inventory existing tray sources first; preserve all original assets, prior accepted painted geology props and failed candidates. Use built-in ImageGen without uploading any existing image or changing protected artwork. Save exact native alpha, prompt and generation provenance; directly audit silhouette/material/alpha/perspective/readability before any reuse study or binding. One reusable shared tray source, no mass redesign, no current runtime/contact/action acceptance, no cinematic delivery or finding closure.','rules':prior['rules'],'findings':prior['findings'],'files':[(F/x).relative_to(R).as_posix() for x in ['PLAN.json','PROMPT.txt','review_tools/'+Path(__file__).name]],'validation':[{'command':'Individual native ImageGen specimen-tray review and in-context reuse study','result':'PENDING','evidence':(F/'PLAN.json').relative_to(R).as_posix()}],'acceptance_gaps':'Generated source must be directly reviewed; source style score alone cannot grant mounted whole-room/contact/action/device/child/owner acceptance. Production bytes remain unchanged until a separately planned reversible binding passes applicable gates.'})
(F/'review_tools').mkdir(parents=True)
inventory=[]
for path,role,assessment in [
 ('assets/galaxy/tray_nano_wood_tray_1.png','Potential tray reuse by filename','Direct native inspection shows a full-canvas repeating wooden plank texture, not an isolated hollow tray; unsuitable for specimen containment.'),
 ('assets/galaxy/tray_plate_oval_001.png','Potential tray reuse by filename','Direct native inspection shows a tiny horizontal colour/edge strip, not a complete inspectable tray; unsuitable for this role.'),
 ('assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_08_serving_tray.png','Existing serving-tray reference','Direct native inspection: several complete serving views painted onto opaque cream sheet, fine near-vector lines and narrow low contrast rims; no transparent isolated rounded rectangular specimen tray matching the current painted geology props. Preserve source, do not substitute it as accepted specimen art.'),
 ('assets/opera/worlds/geology/painted_work_v1_20261001/mineral.png','Reusable approved-review painted geology material','Direct native reinspection supports reuse of the same aqua/lavender crystal cluster; do not regenerate it merely for novelty. Keep its existing attributed review and current action limits.'),
 ('assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png','Reusable approved-review painted geology material','Direct native reinspection supports reuse of the same cream ammonite in lavender stone; do not regenerate it merely for novelty. Keep its existing attributed review and clearing/contact limits.'),
 ('assets/opera/worlds/geology/painted_work_v1_20261001/work_slab.png','Reusable reviewed painted support','Existing production support retained; complete mounted room and specimen clearance still need review.')]:
  p=R/path
  with Image.open(p) as im:dimensions=list(im.size);mode=im.mode
  inventory.append({'path':path,'sha256':sha(p),'dimensions':dimensions,'mode':mode,'role':role,'reuse_assessment':assessment,'transmitted_to_imagegen':False})
prompt='''Use case: illustration-story.
Asset type: one reusable transparent 2D specimen tray for a young child's painted storybook geology game.
Primary request: generate one single EMPTY shallow rounded rectangular ceramic specimen tray, viewed from slightly above at a gentle three-quarter tabletop angle. Its broad inside floor is clearly visible, its low front rim and rounded side walls form one continuous hollow container, and its broad flat base rests naturally on a tabletop plane. Wide shape, about twice as wide as it is deep. No handles, no dividers, no lid, no contents.
Style: polished hand-painted children's storybook gouache, soft visible brush texture within broad simple value bands, slightly irregular authored contours, restrained warm cream highlights, plum/navy painted contour, lavender outer walls, muted aqua inner floor and purple contact shadow. Rounded toy-playset forms, tactile but deliberately illustrated. Keep the silhouette and hollow rim extremely readable at only110pixels wide. Even soft authored light, no dramatic reflections.
Composition: one complete isolated tray centered and large with generous clean transparent margins; show the entire tray and a small soft contact shadow only. Request1024x1024 native RGBA with genuine transparent background.
Avoid: photorealism, shiny3D plastic, mesh/render look, flat vector clip art, thin geometric outlines, multiple tray views, atlas/spritesheet, crystalline contents, hands, characters, text, labels, symbols, backdrop, tabletop artwork, baked checkerboard, opaque white/cream square, cut edges, extraneous floating ornaments.
'''
(F/'PROMPT.txt').write_text(prompt,encoding='utf-8',newline='\n')
write(F/'PLAN.json',{'status':'PREPARED_BEFORE_GENERATION','baseline':base,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'named_gap':'Three actual Geologist invitation trays remain flat outlined rectangles scored2.9. Need a hollow painted specimen-container source; no suitable isolated existing tray established by inventory.','inventory':inventory,'prompt_path':(F/'PROMPT.txt').relative_to(R).as_posix(),'prompt_sha256':sha(F/'PROMPT.txt'),'generation_method':'OpenAI built-in ImageGen, new text-only transparent generation','reference_uploads':[],'references_uploaded':False,'production_binding':False,'owner_acceptance':None,'minimum_source_floor':4.5,'inclusive_refinement_priority':4.5,'required_review':['Hollow continuous rim and contained floor','Consistent painted geology palette/style','Simple complete silhouette and transparent alpha','Three-quarter resting perspective','Readability at110pixel width','Every original preserved; no score transferred to current room or hand action']})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
print('GEOLOGY_SPECIMEN_TRAY_PREPARED|six-source inventory|fresh text only|no production edits')
