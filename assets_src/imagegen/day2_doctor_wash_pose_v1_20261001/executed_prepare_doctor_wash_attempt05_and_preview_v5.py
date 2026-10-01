from pathlib import Path
from PIL import Image
import datetime,hashlib,json,shutil

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'assets_src/imagegen/day2_doctor_wash_pose_v1_20261001'
source=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-b3cc25f8-5546-4200-8a5c-5028526c9485.png')
native=out/'attempt_04_native.png'
assert not native.exists();shutil.copyfile(source,native)
im=Image.open(native);alpha=im.getchannel('A');bbox=alpha.point(lambda x:255 if x>=16 else 0).getbbox()
review={'status':'REJECTED_UNBOUND_SOURCE','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_path':native.relative_to(r).as_posix(),'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'provider_path':str(source),'method':'Built-in image_gen; fresh text-only transparent request, no image bindings; exact native RGBA preserved.','prompt_sha256':json.loads((out/'ATTEMPT_04_PROMPT.json').read_text())['prompt_sha256'],'source_score':4.2,'gesture_meaning_score':4.6,'identity_style_score':4.2,'native_fit_score':None,'complete_action_score':None,'evaluation':'The clear attached soapy hands and connected two-lobed fin improve the work gesture. Flat contours are stronger than attempt3. The taller older facial/body proportions, long narrow tail and predominantly pink/lavender scale field still depart from the approved compact doctor atlas with rainbow tail and right-flowing rainbow hair. Compared directly with the full approved atlas, overall4.2 remains a rejected unbound source.','technical':{'mode':im.mode,'dimensions':list(im.size),'alpha_extrema':alpha.getextrema(),'alpha_ge16_bbox':bbox,'silhouette_width_over_height':(bbox[2]-bbox[0])/(bbox[3]-bbox[1])},'owner_approval':'PENDING'}
(out/'ATTEMPT_04_REVIEW.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
fourth=json.loads((out/'ATTEMPT_04_PROMPT.json').read_text())
prompt='''A single small Doctor Roshan game sprite in a polished drawn 2D fairy-tale storybook, with warm brown linework and broad painted pastel colour bands. Square canvas with true transparent RGBA background. Full body, generous transparent margins. A friendly young child mermaid, rounded soft cheeks, large drawn brown eyes, short small nose, sweet smile. A compact figure, about 85 percent as wide as tall, with head about one quarter of figure height. Short warm golden-brown wavy hair and bangs, a pearl flower above her right ear, and a broad rainbow hair lock streaming horizontally to the RIGHT in rounded painted waves. No long adult portrait hairstyle.

She wears an ivory short-sleeve doctor's coat with small coral collar, cuff and hem borders, a small coral heart patch, teal blouse with gold buttons, lavender waistband, little cream/coral medical satchel at her right hip. Both intact forearms bend to the middle of her chest, and her two attached hands rub together in a small cluster of opaque ivory/mint soap lather. No held tools, no detached hands.

The ONE broad short fish tail curls downward then UP to the RIGHT, ending level with the lower coat, making a compact wide C shape. The whole tail is RAINBOW, with broad bands of coral, peach, gold, mint, aqua, lilac and pink across rows of simple painted scales. Its single tip has ONE joined fish fin with TWO rounded fan lobes and a V notch. The two fin lobes have warm peach/gold leading bands and mint/aqua/lilac lower bands. The tail should not hang far below her coat; do not make a long narrow portrait, all-purple tail, single leaf fin, extra limbs or extra tails.

Keep the storybook illustration matte and softly painted, with restrained simple lavender/aqua shadows; no photorealism, no 3D or Pixar rendering, glossy highlights, thin hair strands, neon outline, halo, glitter, lettering, UI, sink, patient or scenery. One complete intact sprite, not an atlas. The washing gesture must be immediately readable at small game scale.'''
fifth=dict(fourth,attempt=5,preceding_rejected_candidate={'path':review['native_path'],'sha256':review['native_sha256'],'score':4.2,'tool_reference':False},targeted_change='Restore approved compact young storybook silhouette, horizontal right-flowing rainbow hair, rainbow tail field; keep attached wash gesture and two-lobed fin.',prompt=prompt,prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest())
(out/'ATTEMPT_05_PROMPT.json').write_text(json.dumps(fifth,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(Path(__file__),out/'executed_prepare_doctor_wash_attempt05_and_preview_v5.py')
p=r/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8');s+='\n| `'+review['native_path']+'` | OpenAI built-in image_gen, fresh text-only Doctor Roshan wash pose | OpenAI-generated project art; identity/design rights unchanged | Provider native exec-b3cc25f8-5546-4200-8a5c-5028526c9485.png; SHA-256 `'+review['native_sha256']+'` | Exact native RGBA unmodified; rejected source4.2; unbound review draft; no runtime, action or owner acceptance |\n';p.write_text(s,encoding='utf-8')
allowpath=r/'tmp/v2_preview_allowed.json';allowed=set(json.loads(allowpath.read_text()))
families=['audit/day_two_wash_complete_action_v1_20261001','assets_src/imagegen/day2_doctor_wash_pose_v1_20261001']
new=[]
for family in families:
 for p in (r/family).rglob('*'):
  if p.is_file() and p.suffix.lower() in {'.html','.json','.png','.webp','.log','.gd','.py'}:
   rel=p.relative_to(r).as_posix();assert not any(x.startswith('.') or x.lower() in {'secrets','keystore'} for x in Path(rel).parts)
   if rel not in allowed:new.append(rel);allowed.add(rel)
allowpath.write_text(json.dumps(sorted(allowed),indent=2)+'\n',encoding='utf-8')
dest=r/'audit/job_review_v2_20261001/review_tools'
shutil.copyfile(allowpath,dest/'V2_PREVIEW_ALLOWED.json')
(dest/'DECLARED_NEW_WASH_LINKS_V5.json').write_text(json.dumps({'status':'EXACT_LOCAL_ALLOWLIST_EXTENSION','new_paths':sorted(new),'families':families,'qualification':'Only explicitly enumerated authored review/source files added; loopback-only server, no directory listing. Owned server restart and browser/resource checks still pending.'},indent=2)+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in out.rglob('*') if x.is_file()]+[(dest/'V2_PREVIEW_ALLOWED.json').relative_to(r).as_posix(),(dest/'DECLARED_NEW_WASH_LINKS_V5.json').relative_to(r).as_posix()]));d['validation'].append({'command':'Direct doctor wash source attempt4 comparison with approved atlas','result':'FAIL','evidence':'assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/ATTEMPT_04_REVIEW.json; source4.2 remains rejected; younger compact rainbow identity attempt5 pending.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_score':4.2,'decision':review['status'],'next_prompt_sha256':fifth['prompt_sha256'],'new_explicit_preview_paths':len(new),'technical':review['technical']}))
